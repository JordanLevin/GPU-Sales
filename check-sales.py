#!/usr/bin/python3

import requests
import time
import json
import praw
from twilio.rest import Client

reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit('buildapcsales')

def send_text(title):
    with open("auth.txt") as auth:
        sid = auth.readline().strip()
        token = auth.readline().strip()

    client = Client(sid, token)

    client.messages.create(
            to='+19145222264',
            from_='+12019039600',
            body=title
            )

def main():
    recently_seen = []
    while True:
        for submission in subreddit.new(limit=10):
            if submission not in recently_seen:
                if '1070' in submission.title:
                    send_text(submission.title)
                recently_seen.append(submission)
            if len(recently_seen) > 15:
                del recently_seen[0]
        time.sleep(30)

if __name__ == "__main__":
    main()
