#!/usr/bin/env python

"""
Example script for python-twitter, a Python wrapper for the Twitter API.

Script's functions:
    - initialize twitter bot object
    - present user with options to explore the module's diverse functionality

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

class TwitterBot(object):

    api = None
    my_consumer_key = ""
    my_consumer_secret = ""
    my_access_token_key = ""
    my_access_token_secret = ""

    tweet_ids = []

    def __init__(self):
        self.read_credentials()
        self.authenticate_app()

    def read_credentials(self):
        print("[#] Reading stored credentials from file...")

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
                        self.my_consumer_key = line.strip()
                    elif counter is 1:
                        self.my_consumer_secret = line.strip()
                    elif counter is 2:
                        self.my_access_token_key = line.strip()
                    elif counter is 3:
                        self.my_access_token_secret = line.strip()
                    elif counter > 3:
                        # in case there are empty lines trailing the file
                        break
                    counter += 1

    def authenticate_app(self):
        print('[#] Authenticating with Twitter API server...')
        self.api = twitter.Api(consumer_key=self.my_consumer_key,
                               consumer_secret=self.my_consumer_secret,
                               access_token_key=self.my_access_token_key,
                               access_token_secret=self.my_access_token_secret)

    # TWEETS
    def send_tweet(self, text):
        if text is not '0':
            try:
                status = self.api.PostUpdate(text)
                print('\n[>] "{}" just posted: {}\n'.format(status.user.name, status.text))
            except Exception as e:
                print("\n[!] Error while trying to post update: {}\n".format(e))

    def retrieve_tweets_ids(self):
        print("[#] Retrieving tweets ids...")
        try:
            reply = self.api.GetUserTimeline()
            for status in reply:
                self.tweet_ids.append(status.id_str)
            return self.tweet_ids
        except Exception as e:
            print("\n[!] Error while retrieving all tweets: {}\n".format(e))

    def retrieve_timeline(self):
        print("[#] Retrieving user's timeline...")
        try:
            reply = self.api.GetUserTimeline()
            print("\n[>] Timeline tweets [{} total]:\n".format(len(reply)))
            for status in reply:
                print("\t[User Name] {}".format(status.user.name))
                print("\t[Timestamp] {}".format(status.created_at))
                print("\t[ID] {}".format(status.id_str))
                print("\t[Text] {}\n".format(status.text))
        except Exception as e:
            print("\n[!] Error while retrieving all tweets: {}\n".format(e))

    def delete_last_tweet(self):
        try:
            self.tweet_ids = self.retrieve_tweets_ids()
            status = self.api.GetStatus(tweet_ids[0])

            print("[#] Are you sure you want to delete the following tweet:\n")
            print("\t[User Name] {}".format(status.user.name))
            print("\t[Timestamp] {}".format(status.created_at))
            print("\t[ID] {}".format(status.id_str))
            print("\t[Text] {}".format(status.text))

            choice = input("\n[Yes/No]: ")
            if choice in ("Yes", "Y", "yes", "y"):
                response = self.api.DestroyStatus(self.tweet_ids[0])
                print("\n[>] Tweet Destroyed: {}\n".format(response.text))
            else:
                print("[#] Tweet deletion cancelled")
        except Exception as e:
            print("\n[!] Exception while deleting las tweet: {}\n".format(e))

    def delete_all_tweets(self):
        try:
            self.tweet_ids = self.retrieve_tweets_ids()
            deleted_tweets = []
            print("[#] Proceeding with the deletion...")
            for tweet in self.tweet_ids:
                response = self.api.DestroyStatus(tweet)
                deleted_tweets.append(response)
            print("[>] The following {} tweets have been deleted:".format(len(deleted_tweets)))
            for tweet in deleted_tweets:
                print("\t{} >> {}".format(tweet.created_at, tweet.text))
        except Exception as e:
            print("\n[!] Exception while deleting all tweets: {}\n".format(e))

    # FAVORITES
    def retrieve_all_favorites(self):
        try:
            reply = self.api.GetFavorites()
            for status in reply:
                print("\t[User Name] {}".format(status.user.name))
                print("\t[Timestamp] {}".format(status.created_at))
                print("\t[ID] {}".format(status.id_str))
                print("\t[Text] {}\n".format(status.text))
        except Exception as e:
            print("\n[!] Error while retrieving user's likes: {}\n".format(e))

    def delete_all_favorites(self):
        deleted_fav = []
        try:
            reply = self.retrieve_all_favorites()
            for status in reply:
                response = self.api.DestroyFavorite(status_id=status.id_str)
                deleted_fav.append(response)
            print("\n[>] The following {} favorite tweets have been unmarked:".format(len(deleted_fav)))
            for fav in deleted_fav:
                print("\t[User Name] {}".format(fav.user.name))
                print("\t[Timestamp] {}".format(fav.created_at))
                print("\t[ID] {}".format(fav.id_str))
                print("\t[Text] {}\n".format(fav.text))
        except Exception as e:
            print("\n[!] Exception while deleting likes: {}\n".format(e))

    # LISTS
    def retrieve_all_lists(self):
        try:
            lists = self.api.GetLists()
            for lst in lists:
                print("\t[Description]: {}".format(lst.description))
                print("\t[Name]: {}".format(lst.full_name))
                print("\t[Member Count]: {}\n".format(lst.member_count))
        except Exception as e:
            print("\n[!] Exception while retrieving lists: {}\n".format(e))

    def delete_all_lists(self):
        deleted_lists = []
        try:
            reply = self.retrieve_all_lists()
            for lst in reply:
                response = self.api.DestroyList(list_id=lst.id)
                deleted_lists.append(response)
            print("\n[>] The following {} favorite tweets have been unmarked:".format(len(deleted_lists)))
            for lst in deleted_lists:
                print("\t[Description]: {}".format(lst.description))
                print("\t[Name]: {}".format(lst.full_name))
                print("\t[Member Count]: {}\n".format(lst.member_count))
        except Exception as e:
            print("\n[!] Exception while deleting lists: {}\n".format(e))

def main():
    print('\n[#] Welcome to Python-Twitter CLI App')
    print('\n[#] Initializing the Application...')
    bot = TwitterBot()

    while True:
        print("\n[#] Choose your next action:")
        choice = input("\n\t[1] Send new tweet"
                       "\n\t[2] Read user's timeline"
                       "\n\t[3] Delete the last Tweet"
                       "\n\t[4] Delete All Tweets"
                       "\n\t[5] Read user's favorite content"
                       "\n\t[6] Delete user's favorite content"
                       "\n\t[7] Read user's lists"
                       "\n\t[8] Delete user's lists"
                       "\n\t[0] Exit program"
                       "\n\n[?] Choice: ")
        if choice == '1':
            # Send new tweet
            print('[#] Introduce the text for your next tweet [0 to return]:')
            text = input('\n\t> ')
            if text == '0':
                print("[#] Returning to main menu...")
                continue
            bot.send_tweet(text)
        elif choice == '2':
            # Read user's timeline
            bot.retrieve_timeline()
        elif choice == '3':
            # Delete the last Tweet
            bot.delete_last_tweet()
        elif choice == '4':
            # Delete All Tweets
            choice = input("[!] Confirm deletion of the user's tweets\n\t[Yes/No] ")
            try:
                if choice in ("Yes", "Y", "yes", "y"):
                    bot.delete_all_tweets()
                else:
                    print("[#] Tweet deletion cancelled\n")
            except Exception as e:
                print("\n[!] Exception during tweets deletion: {}\n".format(e))
        elif choice == '5':
            # Read user's favorite content
            print("\n[>] Retrieving user's likes...")
            bot.retrieve_all_favorites()
        elif choice == '6':
            # Delete user's favorite content
            print("[#] Deleting user's favorite tweets...")
            choice = input("\t> Are you sure? [Yes/No]: ")
            if choice in ("Yes", "Y", "yes", "y"):
                bot.delete_all_favorites()
            else:
                print("[#] User's favorites Deletion cancelled\n")
        elif choice == '7':
            # Read user's lists
            print("[#] Retrieving user's lists...\n")
            bot.retrieve_all_lists()
        elif choice == '8':
            # Delete user's lists
            print("[#] Deleting user's lists...")
            choice = input("\t> Are you sure? [Yes/No]: ")
            if choice in ("Yes", "Y", "yes", "y"):
                bot.delete_all_lists()
            else:
                print("[#] List Deletion cancelled\n")
        elif choice == '0':
            break
        else:
            print("\n[!] You can't even choose right?! Let's try again...\n")

    print('\n[#] Exiting program now...\n')
    exit()


if __name__ == "__main__":
    main()
