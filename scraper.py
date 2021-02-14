import argparse
import time
import json
import csv
import sys

import pytchat


def main(link, minutes):
    writer = csv.writer(sys.stdout, dialect='unix', quoting=csv.QUOTE_MINIMAL)
    chat = pytchat.create(video_id=link)
    end_time = time.time() + (minutes * 60)

    writer.writerow(['date-time', 'author', 'message'])
    while chat.is_alive() and time.time() < end_time:
        msg = chat.get().sync_items()
        for m in msg:
            writer.writerow([m.datetime, m.author.name, m.message])

    return 1


def _start():
    parser = argparse.ArgumentParser()
    parser.add_argument('-id', '--video-id', dest='video', required=True, type=str)
    parser.add_argument('-m', '--minutes', dest='minutes', required=True,type=float)

    args = vars(parser.parse_args())
    link = args['video']
    minutes = args['minutes']
    try:
        main(link, minutes)
    except Exception as e:
        raise Exception("Unhandeled exception occures {}".format(e))

    sys.exit()


if __name__ == '__main__':
    _start()