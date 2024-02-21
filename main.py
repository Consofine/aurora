import time
import schedule
import argparse
import asyncio

from dotenv import load_dotenv
from aurora import check_aurora

from metrics import test_accuracy
from max_keeper import MaxKeeper
from messenger import send_uptime_email

load_dotenv()


def main_loop():
    max_keeper = MaxKeeper()
    schedule.every(5).minutes.do(check_aurora, max_keeper)
    schedule.every(1).day.do(send_uptime_email)  # text or email

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="aurora",
        description="A python tool for repeatedly checking northern lights forecasts and sending text updates when the aurora are active",
    )

    # parser.add_argument("filename")
    parser.add_argument(
        "-t",
        "--test",
        help="Run in test mode, with supplied number of iterations",
    )

    args = parser.parse_args()

    if args.test:
        try:
            asyncio.run(test_accuracy(int(args.test)))
        except ValueError:
            print("Error: {} not a valid integer".format(args.test))
    else:
        main_loop()
