"""
Interfaces for AWS Fargate metadata collection.

Follows Interface Segregation Principle — Fargate-specific contracts
separate from Kubernetes contracts.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class IContainerMetadataCollector(ABC):
    """Generic container metadata collector interface.

    Platform-agnostic contract for collecting runtime metadata
    from the container orchestration platform.
    """

    @abstractmethod
    def collect_task_metadata(self) -> Dict[str, Any]:
        """Collect task/pod-level metadata."""
        ...

    @abstractmethod
    def collect_container_metadata(self) -> Dict[str, Any]:
        """Collect container-level metadata."""
        ...

    @abstractmethod
    def collect_platform_metadata(self) -> Dict[str, Any]:
        """Collect platform-level metadata (cluster, service, etc.)."""
        ...

    @abstractmethod
    def get_runtime_context(self) -> Dict[str, Any]:
        """Get full runtime context (combined metadata)."""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the metadata source is reachable."""
        ...


class IFargateMetadataCollector(IContainerMetadataCollector):
    """Fargate-specific metadata collector interface.

    Extends the generic container interface with Fargate-specific
    capabilities (task role, launch type, ENI details).
    """

    @abstractmethod
    def get_task_arn(self) -> Optional[str]:
        """Get the ECS task ARN."""
        ...

    @abstractmethod
    def get_cluster_name(self) -> Optional[str]:
        """Get the ECS cluster name."""
        ...

    @abstractmethod
    def get_task_definition(self) -> Optional[str]:
        """Get the task definition family:revision."""
        ...

    @abstractmethod
    def get_launch_type(self) -> str:
        """Get the launch type (FARGATE or EC2)."""
        ...
