#!/usr/bin/env python

"""
Example script for python-twitter, a Python wrapper for the Twitter API.

Script's functions:
    - read user credentials from file
    - authenticate user using said credentials
    - retrieve and print the content of the user's timeline

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
    # need to catch auth failures
    api = twitter.Api(consumer_key=my_consumer_key,
                  consumer_secret=my_consumer_secret,
                  access_token_key=my_access_token_key,
                  access_token_secret=my_access_token_secret)


def read_tweets():
    print("[#] Retrieving user's tweets...")
    global api
    try:
        reply = api.GetUserTimeline()
        print("\n[>] Tweets in user's timeline:")
        for status in reply:
            print("\t[User Name] {}".format(status.user.name))
            print("\t[Timestamp] {}".format(status.created_at))
            print("\t[ID] {}".format(status.id_str))
            print("\t[Text] {}\n".format(status.text))
    except Exception as e:
        print("\n[!] Error while retrieving tweets: {}\n".format(e))


def main():
    print('\n[#] Welcome to Python-Twitter CLI App')
    print('[#] Initializing the Application...')
    read_credentials()
    authenticate_app()
    # print("[#] Application successfully initialized!")
    read_tweets()
    print("[#] Exiting program now...\n")


if __name__ == "__main__":
    main()
