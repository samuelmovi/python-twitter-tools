#!/usr/bin/env python

"""
Example script for python-twitter, a Python wrapper for the Twitter API.

Script's functions:
    - read user credentials from file
    - authenticate user using said credentials
    - retrieve last update
    - ask for confirmation to delete
    - delete published update if confirmed

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
    try:
        # can't catch authenticating errors ?!?
        api = twitter.Api(consumer_key=my_consumer_key,
                          consumer_secret=my_consumer_secret,
                          access_token_key=my_access_token_key,
                          access_token_secret=my_access_token_secret)
    except Exception as e:
        print("\n[!] Exception while authenticating: {}\n".format(e))


def retrieve_tweets_ids():
    global api
    tweet_ids = []
    print("[#] Retrieving tweets ids...")
    try:
        reply = api.GetUserTimeline()
        for status in reply:
            tweet_ids.append(status.id_str)
        return tweet_ids
    except Exception as e:
        print("\n[!] Error while retrieving tweets: {}\n".format(e))


def main():
    global api
    print('\n[#] Welcome to Python-Twitter CLI App')
    print('[#] Initializing the Application...')
    read_credentials()
    authenticate_app()
    # print("[#] Application successfully initialized!")
    tweet_ids = retrieve_tweets_ids()

    try:
        status = api.GetStatus(tweet_ids[0])

        print("[#] Are you sure you want to delete the following tweet:\n")
        print("\t[User Name] {}".format(status.user.name))
        print("\t[Timestamp] {}".format(status.created_at))
        print("\t[ID] {}".format(status.id_str))
        print("\t[Text] {}".format(status.text))
        choice = input("\n[Yes/No]: ")

        if choice in ("Yes", "Y", "yes", "y"):
            status = api.DestroyStatus(tweet_ids[0])
            print("\n[>] Tweet {} has been successfully destroyed".format(status.id_str))
        else:
            print("[#] Tweet deletion cancelled")
    except Exception as e:
        print("\n[!] Error while deleting tweets: {}\n".format(e))

    print("\n[#] Exiting the program now...\n")


if __name__ == "__main__":
    main()
