import argparse
from typing import Iterator

import ipaddress


def parse_addresses(network: str) -> Iterator[ipaddress.IPv4Address]:
    """ List all the network IP addresses.

    Args:
        network (str): The network as a string, e.g.:
            - 192.168.0.0/24
            - 192.168.1.0/255.255.255.0

    Returns:
        Generator: A generator with all the IP addresses for the network.
    """
    return ipaddress.IPv4Network(network).hosts()


def main(network: str, concurrency_level: int, timeout: int):
    """ Main function.

        Args:
        network (str): The network as a string
    """


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("network", type=str,
                        help="The network with subnet and netmask, e.g. 192.168.0.0/24")
    parser.add_argument("-c", "--concurrency_level", type=int, default=1,
                        help="Number of concurrent hosts that are pinged at the same time")
    parser.add_argument("-t", "--timeout", type=int, default=5,
                        help="The number of seconds after giving up on pinging a host (default 5s)")

    args = parser.parse_args()
    print(args)

    main(network=args.network, concurrency_level=args.concurrency_level, timeout=args.timeout)
