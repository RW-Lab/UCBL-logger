"""
Data models for AWS Fargate metadata.

Immutable dataclasses representing Fargate runtime context.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class FargateTaskMetadata:
    """Represents ECS Fargate task-level metadata."""

    task_arn: str = ""
    cluster: str = ""
    family: str = ""
    revision: str = ""
    desired_status: str = ""
    known_status: str = ""
    availability_zone: str = ""
    launch_type: str = "FARGATE"
    pull_started_at: str = ""
    pull_stopped_at: str = ""


@dataclass(frozen=True)
class FargateContainerMetadata:
    """Represents ECS Fargate container-level metadata."""

    container_arn: str = ""
    container_name: str = ""
    docker_id: str = ""
    image: str = ""
    image_id: str = ""
    desired_status: str = ""
    known_status: str = ""
    cpu_limit: int = 0
    memory_limit: int = 0


@dataclass(frozen=True)
class FargateRuntimeContext:
    """Complete Fargate runtime context for log enrichment."""

    task: FargateTaskMetadata = field(default_factory=FargateTaskMetadata)
    container: FargateContainerMetadata = field(default_factory=FargateContainerMetadata)
    service_name: str = ""
    account_id: str = ""
    region: str = ""
