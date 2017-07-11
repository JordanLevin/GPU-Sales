#!/usr/bin/python3

import logging
import requests
import time
import praw
from twilio.rest import Client

reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit('buildapcsales')
logging.basicConfig(filename='texts.log',level=logging.DEBUG)

'''
Sends a text containing the title variable to a phone number using twilio
Looks for auth info in auth.txt
'''
def send_text(title):
    logging.info('Sending text about %s',title)
    with open('auth.txt') as auth:
        sid = auth.readline().strip()
        token = auth.readline().strip()

    client = Client(sid, token)

    client.messages.create(
            to='+19145222264',
            from_='+12019039600',
            body=title
            )

'''
Looks in /r/buildapcsales for new posts. If a word in items.txt is found
a text is sent
'''
def main():
    keywords = []
    with open('items.txt') as words:
        data = words.readlines()
        for item in data:
            keywords.append(item.strip())
    recently_seen = []
    while True:
        for submission in subreddit.new(limit=10):
            if submission not in recently_seen:
                for word in keywords:
                    if word.lower() in submission.title.lower():
                        send_text(submission.title)
                recently_seen.append(submission)
            if len(recently_seen) > 15:
                del recently_seen[0]
        time.sleep(30)

if __name__ == "__main__":
    main()
