from dataclasses import dataclass

import psutil

from infraops.utils.status import Status


@dataclass
class MemoryResult:
    total_gb: float
    used_gb: float
    available_gb: float
    usage_percent: float
    status: Status
    details: str


def collect_memory() -> MemoryResult:

    memory = psutil.virtual_memory()

    usage = memory.percent

    if usage >= 90:
        status = Status.CRITICAL

    elif usage >= 75:
        status = Status.WARNING

    else:
        status = Status.OK

    total_gb = memory.total / (1024 ** 3)
    used_gb = memory.used / (1024 ** 3)
    available_gb = memory.available / (1024 ** 3)

    return MemoryResult(
        total_gb=total_gb,
        used_gb=used_gb,
        available_gb=available_gb,
        usage_percent=usage,
        status=status,
        details=(
            f"{usage:.1f}% utilized "
            f"({used_gb:.1f} GB / {total_gb:.1f} GB)"
        )
    )
