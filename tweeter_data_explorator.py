# This is a class used to explore the tweeter data
# it expects a data frame to be instantiated

class TweeterDataExplorator:
    
    def __init__(self, df):
        
        self.df = df
    
    
    def read_head(self):
        return self.df.head()
    
    # returning the number of rows columns and column information
    def get_info(self):
        row_count, col_count = self.df.shape
    
        print(f"Number of rows: {row_count}")
        print(f"Number of columns: {col_count}")

        return (row_count, col_count), self.df.info()
    
    # gets number of distnict values in a given coumn
    def get_count(self, column_name):
        return self.df[column_name].value_counts()
    
    # returns the number of negative polarities, neutral polarities and positive polarities in a dict
    def get_polarities_count(self):
        postive_count = tweet_df[tweet_df['polarity'] > 0].shape[0]
        neutral_count = tweet_df[tweet_df['polarity'] == 0].shape[0]
        negative_count = tweet_df[tweet_df['polarity'] < 0].shape[0]
        
        return {"postive": postive_count, "neutral": neutral_count, "negative": negative_count}

        
    # constructs a hashtag data frame for every tweets and returns it
    def get_hash_tag_df(self):        
        hash_tags = self.df.clean_text.apply(self.__find_hashtags)
        
        flattened_hash_tags = []
        
        for hash_tag_list in hash_tags:
            for hash_tag in hash_tag_list:
                flattened_hash_tags.append(hash_tag)
        
        hashtag_df = pd.DataFrame(columns=['hashtag'])
        hashtag_df['hashtag'] = flattened_hash_tags
        
        return hashtag_df
    
    #  this returns the value count of top hash tags used in a data frame
    # if top is not specifed, it returns with a value count of every hashtag used
    def most_used_hash_tag(self, top=None):
        return self.get_hash_tag_df()['hashtag'].value_counts().head(top)
        
    def visualze_polarity(self):
        return 
    
    # returns value count of top language used
    # if top is not specifed, it returns with a value count of language of every language used
    def most_used_language(self, top=None):
        return self.df['lang'].value_counts().head(top)
    
    # returns value count of top users tweeted
    # if top is not specifed, it returns with a value count of language of every users who tweeted
    def authors(self, top=None): 
        return self.df['original_author'].value_counts().head(top)
    
    
    def most_retweeted_tweet(self):
        pass
    
    # private function that finds hash tags from a text
    def __find_hashtags(self, tweet):
        
        try:
            return re.findall('(#[A-Za-z]+[A-Za-z0-9-_]+)', tweet)
        except:
            return []