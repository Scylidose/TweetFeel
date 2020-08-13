# Predict Stock Price

## Overview 

Will predict the close value of the Basic Attention Token currency based on its open value.

![CryptoCurrency png](https://github.com/Scylidose/ml-projects/blob/master/img/crypto_bat-img.png)  

## Features

- Display close value for the current day based of the open value.  

- Show diverse plot values from the last 30 days.  

- Show algorithm accuracy based on last year close value.  


## How to use

To clone and run this application, you'll need Git and Flask installed on your computer. From your command line:

```bash
# Retrieve git folder
$ git clone https://github.com/Scylidose/ml-projects.git

$ cd ml-projects/Predict_Stock_Prices

# Install dependencies 
$ pip3 install -r requirements.txt

# Run application
$ make run
```

You can then access the application with the given address.  

## Data Steps

### Fetch Data

- Get Comma-separated values (csv) file everyday containing values about the Basic Attention Token cryptocurrency from the **yfinance** module (Yahoo Finance, https://finance.yahoo.com/quote/BAT-CAD/history). The data is ranged between the day BAT was published until the day the file is downloaded.  

### Pre-process Data

- Removed non-informative columns and Not Available data rows.  

- Scaled Open and Close values with a MinMax Scaler.  


### Data Exploration

- Plot of open and close values per day (for the last 30 days).  

- Plot of highest and lowest values per day (for the last 30 days).  

- Plot of the volume values per day (for the last 30 days).  

- Plot of the close value from last year until today.   

### Model

- Recurrent Neural Network :  
    - LSTM -> 150 Units  
    - Dropout -> Probability of 0.3  
    - LSTM -> 150 Units  
    - Dropout -> Probability of 0.3  
    - LSTM -> 150 Units  
    - Dropout -> Probability of 0.3  
    - Dense -> 1 Unit  
    <br />
    - Optimizer -> Adam  
    - Loss -> Mean Squarred Error

### Accuracy

- R2 Score.  


