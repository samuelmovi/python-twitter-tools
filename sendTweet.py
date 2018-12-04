#!/usr/bin/env python

"""
Example script for python-twitter, a Python wrapper for the Twitter API.

Script's functions:
    - read user credentials from file
    - authenticate user using said credentials
    - ask for content to post as new user update (aka tweet)
    - enter character 0 to exit application

Requirements: a 'credentials' text file with the following format

# consumer_key
your_consumer_key_here
# consumer_secret
your_consumer_secret_here
# access_token_key
your_access_token_key_here
# access_token_secret
your_access_token_secret_here

"""

import twitter

api = None
my_consumer_key = ""
my_consumer_secret = ""
my_access_token_key = ""
my_access_token_secret = ""



def read_credentials():
    print("[#] Reading stored credentials from file...")
    global my_consumer_key
    global my_consumer_secret
    global my_access_token_key
    global my_access_token_secret

    with open("credentials", "r") as file:
        counter = 0
        while True:
            line = file.readline()
            if not line:
                break
            if line.startswith("#"):
                # skip commentary lines starting with '#'
                continue
            else:
                if counter is 0:
                    my_consumer_key = line.strip()
                elif counter is 1:
                    my_consumer_secret = line.strip()
                elif counter is 2:
                    my_access_token_key = line.strip()
                elif counter is 3:
                    my_access_token_secret = line.strip()
                elif counter > 3:
                    # in case there are empty lines trailing the file
                    break
                counter += 1


def authenticate_app():
    print('[#] Authenticating with Twitter API server...')
    global api
    global my_consumer_key
    global my_consumer_secret
    global my_access_token_key
    global my_access_token_secret

    # need to catch auth failures
    api = twitter.Api(consumer_key=my_consumer_key,
                           consumer_secret=my_consumer_secret,
                           access_token_key=my_access_token_key,
                           access_token_secret=my_access_token_secret)


def send_tweet(text):
    global api
    if text != '0':
        try:
            status = api.PostUpdate(text)
            print('[#] "{}" just posted: {}'.format(status.user.name, status.text))
        except Exception as e:
            print("[!] Error while trying to post update: {}".format(e))


def main():
    print('\n[#] Welcome to Python-Twitter CLI App')
    print('[#] Initializing the Application...')
    read_credentials()
    authenticate_app()
    # print("[#] Application successfully initialized!")

    while True:
        print("[#] Enter text for your next tweet [0 to exit]:")
        text = input('\t> ')
        if text != '0':
            send_tweet(text)
        elif text == '0':
            break
    print('[#] Exiting program now...')
    exit()


if __name__ == "__main__":
    main()
