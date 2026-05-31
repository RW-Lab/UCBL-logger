"""
AWS Fargate metadata collector.

Fetches runtime metadata from the ECS Task Metadata Endpoint v4.
Follows Single Responsibility — only collects metadata, does not log.
"""

import os
import logging
from typing import Dict, Any, Optional

from .fargate_interfaces import IFargateMetadataCollector
from .fargate_models import FargateTaskMetadata, FargateContainerMetadata, FargateRuntimeContext

logger = logging.getLogger(__name__)

# ECS injects this env var in Fargate tasks
_METADATA_URI_ENV = "ECS_CONTAINER_METADATA_URI_V4"


class FargateMetadataCollector(IFargateMetadataCollector):
    """Collects metadata from the ECS Task Metadata Endpoint v4.

    The endpoint is available at the URI in ECS_CONTAINER_METADATA_URI_V4
    environment variable, injected by the ECS agent into every Fargate container.

    Implements caching to avoid repeated HTTP calls for the same task lifecycle.
    """

    def __init__(self, cache_ttl: int = 300):
        """Initialize the collector.

        Args:
            cache_ttl: Cache time-to-live in seconds. Metadata is static
                       for the task lifetime, so a long TTL is safe.
        """
        self._cache_ttl = cache_ttl
        self._metadata_uri = os.environ.get(_METADATA_URI_ENV, "")
        self._task_cache: Optional[Dict[str, Any]] = None
        self._container_cache: Optional[Dict[str, Any]] = None
        self._cache_time: float = 0

    def is_available(self) -> bool:
        """Check if running in a Fargate environment."""
        return bool(self._metadata_uri)

    def collect_task_metadata(self) -> Dict[str, Any]:
        """Collect task-level metadata from the ECS endpoint."""
        data = self._fetch_task_metadata()
        if not data:
            return {}
        return {
            "task_arn": data.get("TaskARN", ""),
            "cluster": data.get("Cluster", ""),
            "family": data.get("Family", ""),
            "revision": data.get("Revision", ""),
            "desired_status": data.get("DesiredStatus", ""),
            "known_status": data.get("KnownStatus", ""),
            "availability_zone": data.get("AvailabilityZone", ""),
            "launch_type": data.get("LaunchType", "FARGATE"),
        }

    def collect_container_metadata(self) -> Dict[str, Any]:
        """Collect container-level metadata."""
        data = self._fetch_container_metadata()
        if not data:
            return {}
        return {
            "container_arn": data.get("ContainerARN", ""),
            "container_name": data.get("Name", ""),
            "docker_id": data.get("DockerId", ""),
            "image": data.get("Image", ""),
            "image_id": data.get("ImageID", ""),
            "desired_status": data.get("DesiredStatus", ""),
            "known_status": data.get("KnownStatus", ""),
            "cpu_limit": data.get("Limits", {}).get("CPU", 0),
            "memory_limit": data.get("Limits", {}).get("Memory", 0),
        }

    def collect_platform_metadata(self) -> Dict[str, Any]:
        """Collect platform-level metadata (cluster, service, region)."""
        task = self._fetch_task_metadata()
        if not task:
            return {}
        # Extract account and region from task ARN
        # Format: arn:aws:ecs:region:account:task/cluster/task-id
        task_arn = task.get("TaskARN", "")
        parts = task_arn.split(":")
        return {
            "cluster": task.get("Cluster", ""),
            "region": parts[3] if len(parts) > 3 else "",
            "account_id": parts[4] if len(parts) > 4 else "",
            "launch_type": task.get("LaunchType", "FARGATE"),
            "availability_zone": task.get("AvailabilityZone", ""),
        }

    def get_runtime_context(self) -> Dict[str, Any]:
        """Get full runtime context combining all metadata sources."""
        task = self.collect_task_metadata()
        container = self.collect_container_metadata()
        platform = self.collect_platform_metadata()
        return {
            "task": task,
            "container": container,
            "platform": platform,
        }

    def get_task_arn(self) -> Optional[str]:
        """Get the ECS task ARN."""
        data = self._fetch_task_metadata()
        return data.get("TaskARN") if data else None

    def get_cluster_name(self) -> Optional[str]:
        """Get the ECS cluster name."""
        data = self._fetch_task_metadata()
        return data.get("Cluster") if data else None

    def get_task_definition(self) -> Optional[str]:
        """Get the task definition family:revision."""
        data = self._fetch_task_metadata()
        if not data:
            return None
        return f"{data.get('Family', '')}:{data.get('Revision', '')}"

    def get_launch_type(self) -> str:
        """Get the launch type."""
        data = self._fetch_task_metadata()
        return data.get("LaunchType", "FARGATE") if data else "UNKNOWN"

    # --- Private methods ---

    def _fetch_task_metadata(self) -> Optional[Dict[str, Any]]:
        """Fetch task metadata from the ECS endpoint (cached)."""
        import time
        now = time.time()
        if self._task_cache and (now - self._cache_time) < self._cache_ttl:
            return self._task_cache

        if not self._metadata_uri:
            return None

        try:
            import urllib.request
            import json
            url = f"{self._metadata_uri}/task"
            with urllib.request.urlopen(url, timeout=2) as resp:
                self._task_cache = json.loads(resp.read())
                self._cache_time = now
                return self._task_cache
        except Exception as e:
            logger.debug("Failed to fetch Fargate task metadata: %s", e)
            return None

    def _fetch_container_metadata(self) -> Optional[Dict[str, Any]]:
        """Fetch container metadata from the ECS endpoint (cached)."""
        if not self._metadata_uri:
            return None

        if self._container_cache:
            return self._container_cache

        try:
            import urllib.request
            import json
            with urllib.request.urlopen(self._metadata_uri, timeout=2) as resp:
                self._container_cache = json.loads(resp.read())
                return self._container_cache
        except Exception as e:
            logger.debug("Failed to fetch Fargate container metadata: %s", e)
            return None
