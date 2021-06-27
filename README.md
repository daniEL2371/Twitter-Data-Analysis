# Twitter-Data-Analysis

### What is done

A. Data Extraction

B. Data Preprocessing

C. Data Exploration and Visualzation

D. Data Preparation

E. Data Modeling

F. Dashboard

G. Testing

H. Travis CI integration


#### Data Extraction

1. extract_data_frame.py: extracts the data from data/covid19.json and construct a dataframe called processed_tweet_data.csv and saves it into the root dir

#### Data Preprocessing

1. notebooks/dataPreProcessing.ipynb: 

    A. Cleaning
        
        - cleans the processed_tweet_data.csv and saves the cleaned dataframe in a file called    
        cleaned_tweet_data.csv
        
        - imports clean_tweet_dataframe.py and uses its method to clean the dataframe
    
    B. Exploration
    
        - Data exploration is also done inside this note book

#### Data Preparation and Data Modeling

1 notebooks/modelGeneration.ipynb

    A. Sentiment Analysis: Using the cleaned_tweet_data.csv, Data is prepared for sentiment analysis and Sentiment Analysis model is implemented using SGD classifier.
    
    B. Topic Modeling: Using the cleaned_tweet_data.csv, Data is prepared for Topic Modeling and Topic Modeling model is implemented using Latent Dirichlet Allocation
    

#### Dashboard

1. add_data.py:

        Connects to a database,
        creates tweets db,
        creates TweetInformation table and inserts a dataframe from cleaned_tweet_data.csv.
   
  
  ***Note: Replace your db username and db password inside this file in DBConnect method ***

2. schema.sql: A schema Describing A TweetInformation Table

3. dashboard.py: A dashoard is implemeted using streamlit. The dashboard has two pages for Data Visualzation.

    
    ***Note: dashboard.py imports tweeter_data_explorator.py which has several helpers method to explore the data ***

#### tests

1. test_clean_tweets_dataframe.py:  unit test for clean_tweets_dataframe.py

3. test_extract_dataframe.py: unit test for extract_dataframe.py

#### CI automation

1. .travis.yml: config file for travis CI automation




