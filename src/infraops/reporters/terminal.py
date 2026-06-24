from infraops.utils.colors import Colors
from infraops.utils.status import Status


class TerminalReporter:

    def __init__(self, use_color: bool = True):
        self.colors = Colors(enabled=use_color)

    def print_status(self, name: str, status: Status, details: str = ""):

        if status == Status.OK:
            label = self.colors.colorize(
                "OK",
                Colors.GREEN
            )

        elif status == Status.WARNING:
            label = self.colors.colorize(
                "WARNING",
                Colors.YELLOW
            )

        elif status == Status.CRITICAL:
            label = self.colors.colorize(
                "CRITICAL",
                Colors.RED,
                Colors.BOLD
            )

        else:
            label = self.colors.colorize(
                "UNKNOWN",
                Colors.CYAN
            )

        print(f"{name:<15} {label:<15} {details}")

    def print_header(self, title: str):

        print()
        print("=" * 60)
        print(title)
        print("=" * 60)

    def print_footer(self):

        print("=" * 60)
        print()
