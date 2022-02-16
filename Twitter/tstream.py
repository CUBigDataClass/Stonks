from tweepy import Stream
from json import loads
from keys import *

class TwitterStream(Stream):
    """
    Inherits from tweepy's Stream class. We are only modifying the few functions
    we need to customize, namely what to do when new tweets come through.
    """

    def on_data(self, raw_data):
        """
        Gets called every time a new tweet gets filtered through.
        """
        self.process_data(raw_data)

        return True

    def process_data(self, raw_data):
        response = loads(raw_data)

        print(response['text'])
        print(f'followers: {response["user"]["followers_count"]}')
        print(f'timestamp: {response["created_at"]}\n')

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

    stream.filter(track=['Microsoft'], languages=['en'])
