import pandas as pd
import re
import string
import nltk
import seaborn as sns
sns.set_style('darkgrid')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import datetime
import warnings
warnings.filterwarnings("ignore")


class SentimentAnalyzer:

    def __init__(self, tweet_text):
        self.df = pd.DataFrame(???)

    def make_dataframe(self, responses):
        #Takes the text of the tweet and converts it into a dataframe.
        self.df = self.df.append(pd.Series(responses, index=df.columns[:len(responses)]), ignore_index=True)


    def url_removal(self, df):
        #removes the url from the tweet
        self.df['Tweet'] = self.df['Tweet'].apply(lambda x:re.sub(r"http\S+", "", x))

    def punctuation_removal(self, df):
        #Removing of the Punctuations from the tweet's text
        punctuation_removal = string.punctuation
        def remove_punctuation(text):
            return text.translate(str.maketrans('', '', punctuation_removal))
        self.df['Tweet'] = self.df['Tweet'].apply(lambda text: remove_punctuation(text))

    def single_and_double_character_space_removal(self, df):
        #Removal of Single and Double character space from the tweet's text
        self.df['Tweet'] = self.df['Tweet'].apply(lambda x:re.sub(r'\s+[a-zA-Z]\s+', '', x))
        self.df['Tweet'] = self.df['Tweet'].apply(lambda x:re.sub(r'\s+', ' ', x, flags=re.I))

    def stopwords_removal(self,df):
        #Removing Stop words from the tweet like ["like", "such", "a"]
        #NLTK has a predefined list of stopwords which makes it easy to just remove them from the tweet's text.
        STOPWORDS = set(stopwords.words('english'))
        def remove_stopwords(text):
            return " ".join([word for word in str(text).split() if word not in STOPWORDS])
        self.df['Tweet'] = self.df['Tweet'].apply(lambda text: remove_stopwords(text))

    def remove_emoji(self, df):
        #Removal of Emoji's from the tweet's text
        def emoji(string):
            emoji_pattern = re.compile("["
                                       u"\U0001F600-\U0001F64F"  # emoticons
                                       u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                       u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                       u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                       u"\U00002500-\U00002BEF"  # chinese char
                                       u"\U00002702-\U000027B0"
                                       u"\U00002702-\U000027B0"
                                       u"\U000024C2-\U0001F251"
                                       u"\U0001f926-\U0001f937"
                                       u"\U00010000-\U0010ffff"
                                       u"\u2640-\u2642"
                                       u"\u2600-\u2B55"
                                       u"\u200d"
                                       u"\u23cf"
                                       u"\u23e9;"
                                       u"\u231a"
                                       u"\ufe0f"  # dingbats
                                       u"\u3030"
                                       "]+", flags=re.UNICODE)
            return emoji_pattern.sub(r'', string)
        self.df['Tweet'] = self.df['Tweet'].apply(str)
        self.df['Tweet'] = self.df['Tweet'].apply(emoji)

    def tokenization(self, df):
        #tokenizing the entire tweet's text
        #example: "I like dog" becomes ["I", "like", "dog"]
        def tokens(text):
            text = re.split('\W+', text)
            return text
        self.df['Tokenized'] = self.df['Tweet'].apply(lambda x: tokens(x.lower()))

    def lemmatizer(self, df):
        #lemmatization-capable machine would know that “studies” is the singular verb form of the word “study” in the present tense.
        wn = nltk.WordNetLemmatizer()
        def lemmatizor(text):
            text = [wn.lemmatize(word) for word in text]
            return text
        self.df['Lemmatized'] = self.df['Tokenized'].apply(lambda x: lemmatizor(x))

    def sentiment_score_generator(self, df):
        #Generating the Sentiment Score
        #The compound score generated indicates the level of polarity towards positive and Negative sentiment.
        #If a compound score is more towards -1, then the tweet has a strong negative sentiment.
        #If a compound score is more towards +1, then the tweet has a strong positive sentiment.
        sid = SIA()
        self.df['sentiments'] = self.df["Tweet"].apply(lambda x: sid.polarity_scores(' '.join(re.findall(r'\w+',str(x).lower()))))
        self.df['Positive Sentiment'] = self.df['sentiments'].apply(lambda x: x['pos']+1*(10**-6))
        self.df['Neutral Sentiment'] = self.df['sentiments'].apply(lambda x: x['neu']+1*(10**-6))
        self.df['Negative Sentiment'] = self.df['sentiments'].apply(lambda x: x['neg']+1*(10**-6))

        print(self.df)
