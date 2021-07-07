import argparse
import asyncio
import concurrent
import ipaddress
import logging
import socket
from concurrent.futures import ThreadPoolExecutor
from typing import Iterator

import aioping


# Configure the logging module
FORMAT = '[%(asctime)-15s] %(levelname)s %(name)s %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
LOGGER = logging.getLogger("pingthem")
# Don't want to see aioping logs
logging.getLogger('aioping').setLevel(logging.WARNING)


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


async def do_ping(sem: asyncio.Semaphore, host: str, timeout: int):
    """ Pings given IP address.

    Args:
        host (str): IP address, e.g.
            - 192.168.1.1

    Returns:
        None
    """
    await sem.acquire()
    try:
        LOGGER.info(f"Pinging {host}...")
        delay = await aioping.ping(host, timeout, socket.AddressFamily.AF_INET) * 1000
        LOGGER.info(f"Ping {host}: {delay:.2f}")
    except TimeoutError:
        LOGGER.warning(f"Pinging {host} timed out after {timeout}s.")
    finally:
        sem.release()


async def main(network: str, concurrency_level: int, timeout: int):
    """ Main function.

        Args:
        network (str): The network as a string
    """
    parsed_ips = parse_addresses(network)
    import pdb; pdb.set_trace()

    LOGGER.info(f"About to ping {ipaddress.IPv4Network(network).num_addresses} IP addresses.")
    sem = asyncio.Semaphore(concurrency_level)
    loop = asyncio.get_event_loop()

    tasks = []
    for ip in parsed_ips:
        task = loop.create_task(do_ping(sem, str(ip), timeout))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    LOGGER.info('Done running the tasks')


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

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(network=args.network, concurrency_level=args.concurrency_level, timeout=args.timeout))
