#!python

__desc__ = """
dht22_temp_monitor: display or store environmental temperature and humidity on stdout or Redis.
Redis keys are {hostname}.temperature, {hostname}.humidity and {hostname}.time.

USAGE: python dht22_temp_monitor [-r|--redis address] [-f|--frequency seconds] -h|--help

-r, --redis: (optional) log values to redis, otherwise stdout
-f, --frequency: (optional) number of seconds between samples, if omitted, run once and exit.
"""

__author__ = "Rob Campbell"
__version__ = "0.1.0"
__license__ = "The Unlicense"

import argparse
import socket
import redis
import sched, time
import math
import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4


def get_temp_and_humidity():
    """Read twice for better accuracy"""
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    return (round(temperature, 1), round(humidity, 1))

def write_to_redis(address):
    hostname = socket.gethostname()
    temperature, humidity = get_temp_and_humidity()
    r = redis.Redis(host=address, port=6379, db=0)
    r.set(hostname + '.temperature', temperature)
    r.set(hostname + '.humidity', humidity)
    r.set(hostname + '.temperature.time', math.floor(time.time()))

def write_to_console(dummy):
    temperature, humidity = get_temp_and_humidity()
    print(f"{temperature}℃ , {humidity}%")

def main(args):
    """ Main entry point of the app """

    freq = args.frequency
    scheduler = sched.scheduler()

    if args.redis :
        action = write_to_redis
        address = args.redis
    else:
        action = write_to_console
        address = ""

    print("cpu_temp_monitor starting up")
    print(args)

    # First one is free!
    action(address)

    while freq > 0:
        # print("cpu_temp_monitor, scheduler loop tick")
        scheduler.enter(freq, 1, action, (address,))
        
        scheduler.run()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser(usage=__desc__)

    # Optional argument flag which defaults to False
    parser.add_argument("-r", "--redis", help="store values in redis at location", type=str, default="")

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-f", "--frequency", help="set frequency in seconds, if omitted, run once and exit", type=int, default=0)

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)
