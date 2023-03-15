<h1 align="center">TweetFeel</h1>

<p align="center">
  <b><i>Logistic Regression.</i></b><br><br>
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"> <img src="https://img.shields.io/badge/Jinja-000000?style=for-the-badge&logo=jinja&logoColor=white"> <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white"> <img src="https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E"> <img src="https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white"><br>
<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
</p>

## Overview 

Will get the global sentiment behind a word using Twitter.

![Sentiment_Estimator_png](https://github.com/Scylidose/Sentiment_Estimator/blob/master/img/estimation-gif.gif)  

## Features

- Display percentage of happiness of a given word  

- Show sentiment count, word cloud and most used words.  

- Retrieve and display random tweets with its estimated sentiment.  


## How to use

To clone and run this application, you'll need Git and Flask installed on your computer. From your command line:

```bash
# Retrieve git folder
$ git clone https://github.com/Scylidose/TweetFeel.git

$ cd TweetFeel/

# Install dependencies 
$ pip3 install -r requirements.txt

# Run application
$ make run
```

You can then access the application with the given address.  

## Data Steps

### Fetch Data

- Comma-separated values (csv) file containing Sentiment140 dataset with 1.6 million tweets  
https://www.kaggle.com/kazanova/sentiment140

- Get atmost 100 tweets from a search query using **Tweepy** API in a JSON format.  

### Pre-process Data

- Removed irrelevant punctuation, mentionned user, link and english stopwords.  

- Tokenized sentence.  

- Lemmatized tokens.  

- Deleted words longer than 15 characters.

- TF-IDF Transformation.

### Data Exploration

- Most frequent words and Bi-grams.  

- Count of estimated Positive and Negative tweets.  

- Displayed the WordCloud.  

### Model

- Logistic Regression :  
    - L2 Penalty  
    - Tolerance value of 0.001  
    - C value of 1  

### Accuracy

- Confusion Matrix  

- Accuracy classification score (Jaccard Score)  

