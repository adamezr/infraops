from dataclasses import dataclass

import psutil

from infraops.utils.status import Status


@dataclass
class CPUResult:
    usage_percent: float
    status: Status
    details: str


def collect_cpu() -> CPUResult:

    usage = psutil.cpu_percent(interval=1)

    if usage >= 90:
        status = Status.CRITICAL

    elif usage >= 75:
        status = Status.WARNING

    else:
        status = Status.OK

    return CPUResult(
        usage_percent=usage,
        status=status,
        details=f"{usage:.1f}% utilized"
    )
