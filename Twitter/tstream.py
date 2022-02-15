import tweepy
from keys import *

# Create a StreamListener
class TwitterStream(tweepy.Stream):

    def on_data(self, raw_data):
        self.process_data(raw_data)

        return True

    def process_data(self, raw_data):
        print(raw_data)

    def on_error(self, status_code):
        # Returning false disconnects the stream
        if status_code == 420:
            return False

# Start the Stream
if __name__ == "__main__":

    stream = TwitterStream(
        API_KEY, API_KEY_SECERT,
        ACCESS_TOKEN, ACCESS_TOKEN_SECRET
    )

    stream.filter(track=['python'])



