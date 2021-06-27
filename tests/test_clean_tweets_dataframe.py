import os
import sys
import unittest
import pandas as pd
import pandas.api.types as ptypes

sys.path.append(os.path.abspath(os.path.join('..')))

from clean_tweets_dataframe import Clean_Tweets

df = pd.read_csv("./processed_tweet_data.csv")

class TestCleanTweetsDataframe(unittest.TestCase):
    
    def setUp(self):
        self.df = df.copy(deep=True)
        self.cleaner = Clean_Tweets(self.df)

    def test_drop_duplicate(self):
        df = self.cleaner.drop_duplicate(self.df)
        self.assertTrue(not df.duplicated().any())
   
    def test_convert_to_datetime(self):
        df = self.cleaner.convert_to_datetime(self.df)
        self.assertTrue(type(df['created_at'].dtype == ptypes.DatetimeTZDtype))

    def test_convert_to_datetime(self):
        df = self.cleaner.convert_to_numbers(self.df)
        self.assertTrue(
            ptypes.is_numeric_dtype(df['polarity']))
        self.assertTrue(
            ptypes.is_numeric_dtype(df['subjectivity']))
        self.assertTrue(
            ptypes.is_numeric_dtype(df['retweet_count']))
        self.assertTrue(
            ptypes.is_numeric_dtype(df['favorite_count']))
        
    
    def test_handle_missing_values(self):
       df = self.cleaner.handle_missing_values(self.df)
       self.assertTrue(df.isna().sum().sum() == 0)
    
    def test_remove_non_english_tweets(self):
      df = self.cleaner.remove_non_english_tweets(self.df)
      df = df[df['lang'] != 'en']
      self.assertEqual(df.shape[0], 0)


if __name__ == '__main__':
    unittest.main()
