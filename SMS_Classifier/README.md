# SMS Classifier

## Overview 

Will tell if a message is either 'ham' or 'spam'

![freeCodeCamp Social Banner](https://s3.amazonaws.com/freecodecamp/wide-social-banner.png)

## How to use

To clone and run this application, you'll need Git and Jupyter installed on your computer. From your command line:

```bash
# Retrieve git folder
$ git clone https://github.com/Scylidose/ml-projects.git

$ cd ml-projects/SMS_Classifier

# Run notebook
$ jupyter notebook
```

You can then access the application with the given address.  

## Data Steps

### Fetch Data

- Comma-separated values (csv) file containing FreeCodeCamp Python curriculum SMS data.

### Pre-process Data

- Removed irrelevant punctuation and english stopwords.  

- Tokenized sentence.  

- Stemmed tokens.  

- Lowered tokens

### Data Exploration

- Most frequent words.  

- Count of spam and ham values.

- Count of estimated Sentiment values per category.  

- Displayed the WordCloud.  

### Model

- Multinomial Naïve Bayes :  
    - Alpha value of 5  
    - Prior is True  

### Accuracy

- Confusion Matrix  

- Classification report

