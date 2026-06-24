from infraops.collectors.cpu import collect_cpu
from infraops.reporters.terminal import TerminalReporter
from infraops.utils.status import Status


def run_health(args):

    reporter = TerminalReporter(
        use_color=not args.no_color
    )

    reporter.print_header(
        "InfraOps System Health Report"
    )

    cpu = collect_cpu()

    reporter.print_status(
        "CPU",
        cpu.status,
        cpu.details
    )

    reporter.print_status(
        "Memory",
        Status.OK,
        "Collector not implemented yet"
    )

    reporter.print_status(
        "Filesystem",
        Status.OK,
        "Collector not implemented yet"
    )

    reporter.print_status(
        "Processes",
        Status.OK,
        "Collector not implemented yet"
    )

    reporter.print_status(
        "Logs",
        Status.OK,
        "Collector not implemented yet"
    )

    reporter.print_footer()

    return 0
