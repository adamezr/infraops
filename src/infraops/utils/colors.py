class Colors:
    RESET = "\033[0m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    RED = "\033[0;31m"
    CYAN = "\033[0;36m"
    BOLD = "\033[1m"

    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def colorize(self, text: str, *codes: str) -> str:
        if not self.enabled:
            return text
        return "".join(codes) + text + self.RESET
