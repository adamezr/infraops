from dataclasses import dataclass
from pathlib import Path

from infraops.utils.status import Status


@dataclass
class LogResult:
    status: Status
    details: str


LOG_DIRECTORIES = [
    "/var/log",
]


LARGE_LOG_WARNING_MB = 500
LARGE_LOG_CRITICAL_MB = 1024


def collect_logs() -> LogResult:

    largest_file = None
    largest_size_mb = 0

    for log_dir in LOG_DIRECTORIES:

        path = Path(log_dir)

        if not path.exists():
            continue

        try:
            for file in path.rglob("*"):

                if not file.is_file():
                    continue

                try:
                    size_mb = file.stat().st_size / (1024 * 1024)

                    if size_mb > largest_size_mb:
                        largest_size_mb = size_mb
                        largest_file = file

                except (
                    PermissionError,
                    OSError,
                ):
                    continue

        except (
            PermissionError,
            OSError,
        ):
            continue

    if largest_file is None:
        return LogResult(
            status=Status.UNKNOWN,
            details="No log files found"
        )

    if largest_size_mb >= LARGE_LOG_CRITICAL_MB:
        status = Status.CRITICAL

    elif largest_size_mb >= LARGE_LOG_WARNING_MB:
        status = Status.WARNING

    else:
        status = Status.OK

    return LogResult(
        status=status,
        details=(
            f"{largest_file.name} "
            f"({largest_size_mb:.1f} MB)"
        )
    )
