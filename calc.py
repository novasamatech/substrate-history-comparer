from settings import *
from src.call_by_address import call_by_address


def main():
    for address in addresses:
        call_by_address(address=address)


if __name__ == "__main__":
    main()
