import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--concurrency_level", type=int, default=1,
                    help='Number of concurrent hosts that are pinged at the same time')
parser.add_argument("-t", "--timeout", type=int, default=5,
                    help='The number of seconds after giving up on pinging a host (default 5s)')

args = parser.parse_args()