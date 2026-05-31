"""
AWS Fargate-optimized logger.

Outputs structured JSON to stdout enriched with ECS Fargate metadata.
Designed for awslogs driver or FireLens (Fluent Bit) log collection.

Follows Open/Closed Principle — extends EKSLogger pattern without modifying it.
"""

import json
import sys
import os
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from .interfaces import LogLevel


class FargateLogger:
    """Fargate-optimized structured JSON logger.

    Automatically enriches log entries with ECS task metadata
    (cluster, task ARN, service, container) fetched from the
    Task Metadata Endpoint v4.

    Usage:
        from ucbl_logger import FargateLogger

        logger = FargateLogger(service_name="my-service")
        logger.info("Request processed", request_id="abc123", duration_ms=42)
    """

    def __init__(
        self,
        service_name: str = "ucbl-service",
        log_level: str = "INFO",
        include_metadata: bool = True,
    ):
        """Initialize the Fargate logger.

        Args:
            service_name: Application/service name for log identification.
            log_level: Minimum log level to emit (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            include_metadata: Whether to enrich logs with Fargate task metadata.
        """
        self._service_name = service_name
        self._log_level = getattr(LogLevel, log_level.upper(), LogLevel.INFO) if hasattr(LogLevel, log_level.upper()) else LogLevel.INFO
        self._include_metadata = include_metadata
        self._metadata_collector = None
        self._static_context: Dict[str, Any] = {}

        if include_metadata:
            self._init_metadata()

    def _init_metadata(self) -> None:
        """Initialize the metadata collector (lazy, fails gracefully)."""
        try:
            from .enhanced.metadata.fargate_collector import FargateMetadataCollector
            collector = FargateMetadataCollector()
            if collector.is_available():
                self._metadata_collector = collector
                # Cache static context (doesn't change during task lifetime)
                self._static_context = collector.get_runtime_context()
        except Exception:
            pass  # Not in Fargate — no metadata enrichment

    def _should_log(self, level: str) -> bool:
        """Check if the given level meets the minimum threshold."""
        levels = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3, "CRITICAL": 4}
        return levels.get(level, 0) >= levels.get(self._log_level.name if hasattr(self._log_level, 'name') else "INFO", 1)

    def _emit(self, level: str, message: str, **kwargs: Any) -> None:
        """Emit a structured JSON log entry to stdout."""
        if not self._should_log(level):
            return

        entry: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": level,
            "service": self._service_name,
            "message": message,
        }

        # Add Fargate metadata
        if self._static_context:
            task = self._static_context.get("task", {})
            container = self._static_context.get("container", {})
            platform = self._static_context.get("platform", {})
            entry["ecs"] = {
                "cluster": task.get("cluster", platform.get("cluster", "")),
                "task_arn": task.get("task_arn", ""),
                "task_definition": f"{task.get('family', '')}:{task.get('revision', '')}",
                "container": container.get("container_name", ""),
                "launch_type": task.get("launch_type", "FARGATE"),
                "az": task.get("availability_zone", ""),
            }
            if platform.get("account_id"):
                entry["aws"] = {
                    "account_id": platform["account_id"],
                    "region": platform.get("region", ""),
                }

        # Add caller-provided context
        if kwargs:
            entry["context"] = kwargs

        print(json.dumps(entry, default=str), file=sys.stdout, flush=True)

    # --- Public logging methods ---

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log at DEBUG level."""
        self._emit("DEBUG", message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """Log at INFO level."""
        self._emit("INFO", message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log at WARNING level."""
        self._emit("WARNING", message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Log at ERROR level."""
        self._emit("ERROR", message, **kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        """Log at CRITICAL level."""
        self._emit("CRITICAL", message, **kwargs)

    def exception(self, message: str, exc: Optional[Exception] = None, **kwargs: Any) -> None:
        """Log an exception at ERROR level with traceback."""
        import traceback
        tb = traceback.format_exc() if exc is None else traceback.format_exception(type(exc), exc, exc.__traceback__)
        kwargs["traceback"] = "".join(tb) if isinstance(tb, list) else tb
        self._emit("ERROR", message, **kwargs)

    # --- Context methods ---

    def with_context(self, **kwargs: Any) -> "FargateLogger":
        """Return a new logger instance with additional static context.

        Follows Liskov Substitution — returned logger behaves identically.
        """
        new_logger = FargateLogger(
            service_name=self._service_name,
            log_level=self._log_level.name if hasattr(self._log_level, 'name') else "INFO",
            include_metadata=self._include_metadata,
        )
        new_logger._static_context = {**self._static_context}
        new_logger._metadata_collector = self._metadata_collector
        new_logger._static_context["extra"] = kwargs
        return new_logger
