from infraops.collectors.cpu import collect_cpu
from infraops.collectors.filesystem import collect_filesystems
from infraops.collectors.logs import collect_logs
from infraops.collectors.memory import collect_memory
from infraops.collectors.processes import collect_processes
from infraops.reporters.terminal import TerminalReporter


def run_health(args):

    reporter = TerminalReporter(
        use_color=not args.no_color
    )

    reporter.print_header(
        "InfraOps System Health Report"
    )

    cpu = collect_cpu()
    memory = collect_memory()
    filesystem = collect_filesystems()
    processes = collect_processes()
    logs = collect_logs()

    reporter.print_status(
        "CPU",
        cpu.status,
        cpu.details
    )

    reporter.print_status(
        "Memory",
        memory.status,
        memory.details
    )

    reporter.print_status(
        "Filesystem",
        filesystem.status,
        filesystem.details
    )

    reporter.print_status(
        "Processes",
        processes.status,
        processes.details
    )

    reporter.print_status(
        "Logs",
        logs.status,
        logs.details
    )

    reporter.print_footer()

    return 0
