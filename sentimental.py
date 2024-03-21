from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flair.models import TextClassifier
from flair.data import Sentence
classifier = TextClassifier.load('en-sentiment')

def give_score_textblob_sentiment(text):
    res = TextBlob(text)
    print(res)
    score = res.sentiment.polarity
    if score > 0:
        sentiment_category = "Positive"
    elif score < 0:
        sentiment_category = "Negative"
    else:
        sentiment_category = "Neutral"
    return sentiment_category

def give_score_vadare_sentiment(text):
    sid_obj= SentimentIntensityAnalyzer()
    scores = sid_obj.polarity_scores(text)
    compound_score = scores['compound']
    if compound_score >= 0.5:
        return "Positive"
    elif compound_score <= -0.5:
        return "Negative"
    else:
        return "Neutral"
    
def give_score_flair_sentiment(text):
    sentence = Sentence(text)
    classifier.predict(sentence)
    score = sentence.labels[0].score
    value = sentence.labels[0].value
    print(score)
    return value


text1 = "This is the best Face Recognition at this price."

text2 = "This is not the best Face Recognition at this price"

print(give_score_textblob_sentiment(text1))

print(give_score_textblob_sentiment(text2))

print(give_score_vadare_sentiment(text1))

print(give_score_vadare_sentiment(text2))

print(give_score_flair_sentiment(text1))

print(give_score_flair_sentiment(text2))