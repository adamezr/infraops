from dataclasses import dataclass
from typing import List

import psutil

from infraops.utils.status import Status


EXCLUDED_FS_TYPES = {
    "tmpfs",
    "devtmpfs",
    "squashfs",
    "overlay",
    "proc",
    "sysfs",
    "devfs",
}


@dataclass
class FilesystemMount:
    device: str
    mountpoint: str
    fstype: str
    usage_percent: float
    total_gb: float
    used_gb: float
    free_gb: float
    status: Status


@dataclass
class FilesystemResult:
    mounts: List[FilesystemMount]
    status: Status
    details: str


def _evaluate_status(usage_percent: float) -> Status:
    if usage_percent >= 90:
        return Status.CRITICAL

    if usage_percent >= 75:
        return Status.WARNING

    return Status.OK


def collect_filesystems() -> FilesystemResult:
    mounts: List[FilesystemMount] = []

    for partition in psutil.disk_partitions(all=False):
        if partition.fstype in EXCLUDED_FS_TYPES:
            continue

        try:
            usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        except OSError:
            continue

        usage_percent = usage.percent
        status = _evaluate_status(usage_percent)

        mounts.append(
            FilesystemMount(
                device=partition.device,
                mountpoint=partition.mountpoint,
                fstype=partition.fstype,
                usage_percent=usage_percent,
                total_gb=usage.total / (1024 ** 3),
                used_gb=usage.used / (1024 ** 3),
                free_gb=usage.free / (1024 ** 3),
                status=status,
            )
        )

    if not mounts:
        return FilesystemResult(
            mounts=[],
            status=Status.UNKNOWN,
            details="No eligible filesystems found",
        )

    worst_mount = max(
        mounts,
        key=lambda m: m.usage_percent,
    )

    overall_status = max(
        mount.status for mount in mounts
    )

    details = (
        f"{worst_mount.mountpoint} "
        f"{worst_mount.usage_percent:.1f}% utilized "
        f"({worst_mount.used_gb:.1f} GB / {worst_mount.total_gb:.1f} GB)"
    )

    return FilesystemResult(
        mounts=mounts,
        status=overall_status,
        details=details,
    )
