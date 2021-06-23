import pandas as pd
from pandas.io.parsers import read_csv


class Clean_Tweets:
    """
    The PEP8 Standard AMAZING!!!
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df
        print('Automation in Action...!!!')

    def drop_unwanted_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        remove rows that has column names. This error originated from
        the data collection stage.  
        """
        unwanted_rows = df[df['retweet_count'] == 'retweet_count'].index
        df.drop(unwanted_rows, inplace=True)
        df = df[df['polarity'] != 'polarity']

        return df

    def drop_duplicate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        drop duplicate rows
        """
        df.drop_duplicates(inplace=True)
        print(df)

        return df

    def convert_to_datetime(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        convert column to datetime
        """

        df['created_at'] = pd.to_datetime(
            df['created_at'])

        return df

    def convert_to_numbers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        df['polarity'] = pd.to_numeric(df["polarity"])
        df["subjectivity"] = pd.to_numeric(df["subjectivity"])
        df["retweet_count"] = pd.to_numeric(df["retweet_count"])
        df["favorite_count"] = pd.to_numeric(df["favorite_count"])
        df["friends_count "] = pd.to_numeric(df["polarity"])

        return df

    def remove_non_english_tweets(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        remove non english tweets from lang
        """

        df = df.drop(df[df['lang'] != 'en'].index)

        return df

    def clean_data(self, df: pd.DataFrame, save) -> pd.DataFrame:

        df = self.drop_duplicate(df)
        df = self.convert_to_numbers(df)
        df = self.remove_non_english_tweets(df)
        df = self.drop_unwanted_column(df)
        df = self.convert_to_datetime(df)

        if save:
            df.to_csv('cleaned_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')

        return df


def read_processed_data(csv_path):

    try:
        df = pd.read_csv(csv_path)
        print("file read as csv")
    except FileNotFoundError:
        print("file not found")


if __name__ == "__main__":
    proccessed_df = read_csv('processed_tweet_data.csv')
    cleaner = Clean_Tweets(proccessed_df)
    cleaner.clean_data(proccessed_df, save=True)
    # cleaner.drop_duplicate(proccessed_df)
    # print(proccessed_df)
