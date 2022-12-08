from colorama import init, Fore, Style

init(autoreset=True)


INFO = f'{Fore.GREEN}INFO{Style.RESET_ALL}'
WARNING = f'{Fore.YELLOW}WARNING{Style.RESET_ALL}'
ERROR = f'{Fore.RED}ERROR{Style.RESET_ALL}'


def info(msg: str):
    print(f'[{INFO}] {msg}')


def warning(msg: str):
    print(f'[{WARNING}] {msg}')


def error(msg: str):
    print(f'[{ERROR}] {msg}')
