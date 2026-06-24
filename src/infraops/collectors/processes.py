from dataclasses import dataclass

import psutil

from infraops.utils.status import Status


@dataclass
class ProcessInfo:
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float


@dataclass
class ProcessResult:
    top_cpu_process: ProcessInfo
    top_memory_process: ProcessInfo
    status: Status
    details: str


def collect_processes() -> ProcessResult:
    processes = []

    for proc in psutil.process_iter([
        "pid",
        "name",
        "cpu_percent",
        "memory_percent"
    ]):
        try:
            cpu_percent = proc.info.get("cpu_percent") or 0.0
            memory_percent = proc.info.get("memory_percent") or 0.0

            processes.append(
                ProcessInfo(
                    pid=proc.info.get("pid") or 0,
                    name=proc.info.get("name") or "unknown",
                    cpu_percent=float(cpu_percent),
                    memory_percent=float(memory_percent),
                )
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
            TypeError,
            ValueError,
        ):
            continue

    if not processes:
        return ProcessResult(
            top_cpu_process=ProcessInfo(0, "none", 0.0, 0.0),
            top_memory_process=ProcessInfo(0, "none", 0.0, 0.0),
            status=Status.UNKNOWN,
            details="No process data available",
        )

    top_cpu = max(processes, key=lambda p: p.cpu_percent)
    top_memory = max(processes, key=lambda p: p.memory_percent)

    status = Status.OK

    if top_cpu.cpu_percent >= 90:
        status = Status.CRITICAL
    elif top_cpu.cpu_percent >= 75:
        status = Status.WARNING

    details = (
        f"CPU: {top_cpu.name} ({top_cpu.cpu_percent:.1f}%) | "
        f"MEM: {top_memory.name} ({top_memory.memory_percent:.1f}%)"
    )

    return ProcessResult(
        top_cpu_process=top_cpu,
        top_memory_process=top_memory,
        status=status,
        details=details,
    )
