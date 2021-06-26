import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
from add_data import db_execute_fetch
import plotly.express as px

import re


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
        polarity_score_df = pd.DataFrame(columns=['polarity_score'])
        polarity_score_df['polarity_score'] = self.df['polarity'].apply(
            self.text_category)
        return polarity_score_df['polarity_score'].value_counts().rename_axis('polarity_score').to_frame('polarity_score')

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
        return self.get_hash_tag_df()['hashtag'].value_counts().head(top).rename_axis('hashtags').to_frame('counts')

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

    def text_category(self, p: float) -> str:
        if p > 0:
            return "positive"
        elif p == 0:
            return "neutral"
        else:
            return "negative"
    # private function that finds hash tags from a text

    def __find_hashtags(self, tweet):

        try:
            return re.findall('(#[A-Za-z]+[A-Za-z0-9-_]+)', tweet)
        except:
            return []


st.set_page_config(page_title="Tweet Data Information", layout="wide")


def loadData():
    query = "select * from TweetInformation"
    df = db_execute_fetch(query, dbName="tweets", rdf=True)
    return df


def wordCloud(df):
    df = loadData()
    cleanText = ''
    for text in df['clean_text']:
        tokens = str(text).lower().split()

        cleanText += " ".join(tokens) + " "

    wc = WordCloud(width=650, height=450, background_color='white',
                   min_font_size=5).generate(cleanText)
    return wc


class Dashboard:

    def __init__(self, title: str) -> None:
        self.title = title
        self.page = None
        self.df = self.load_data()
        self.tweeterDataExplorator = TweeterDataExplorator(self.df)

    def load_data(self):
        query = "select * from TweetInformation"
        df = db_execute_fetch(query, dbName="tweets", rdf=True)
        return df

    def barChart(self, data, title, X, Y):

        msgChart = (alt.Chart(data).mark_bar().encode(alt.X(f"{X}:N", sort=alt.EncodingSortField(field=f"{Y}", op="values",
                    order='ascending')), y=f"{Y}:Q"))
        st.altair_chart(msgChart, use_container_width=True)

    def render_siderbar(self, pages, select_label):
        st.sidebar.markdown("# Pages")
        self.page = st.sidebar.selectbox(f'{select_label}', pages)

    def render_top_authors(self):
        st.markdown("## Top authors")

        top = st.number_input(label="Top", step=1, value=5, key="top_authors")
        df_res = self.tweeterDataExplorator.authors(top=int(top))

        st.bar_chart(data=df_res, width=0, height=0,
                     use_container_width=True)

    def render_top_hashtags(self):
        st.markdown("## Top hashtags")

        top = st.number_input(label="Top", step=1, value=5, key="top_hashtags")
        df_res = self.tweeterDataExplorator.most_used_hash_tag(top=int(top))

        st.bar_chart(data=df_res, width=0, height=0,
                     use_container_width=True)

    def render_polarity(self):
        st.markdown("## Polarity score")
        df = self.tweeterDataExplorator.get_polarities_count()

        fig = px.pie(df, values="polarity_score",
                     names="polarity_score", width=500, height=350)
        fig.update_traces(textposition='inside', textinfo='percent+label')

        st.plotly_chart(fig)

    def render_visulazation(self):
        self.render_top_hashtags()
        self.render_top_authors()
        self.render_polarity()
        self.render_word_cloud()

    def render_word_cloud(self):
        st.markdown("## Tweet Text Word Cloud")

        wc = wordCloud(self.df)
        st.image(wc.to_array())

    def render(self):
        st.title(f"Welcome To {self.title}")
        self.render_siderbar(['Data', "Data Visualizations"], "select page: ")

        if (self.page == "Data"):

            st.title("Data")
            location = author = hashtag = lang = polarity = None

            filters = st.sidebar.multiselect(
                label="Choose filter", options=["location", "lang", "hashtags", "authors", "polarity"])

            column_filters = st.multiselect(
                "Choose columns to include", options=self.df.columns)

            if ("location" in filters):
                location = st.sidebar.multiselect("choose Location of tweets", list(
                    self.df['place'].unique()))

            if ("lang" in filters):
                lang = st.sidebar.multiselect("choose Language of tweets",
                                              list(self.df['lang'].unique()))

            if ("hashtags" in filters):
                hashtag = st.sidebar.text_input("Hashtag")

            if ("authors" in filters):
                author = st.sidebar.text_input("Author")

            if ("polarity" in filters):
                polarity = st.sidebar.selectbox("choose polarity score",
                                                options=["None", "positive", "neutral", "negative"])

            filtered_df = self.df

            if (column_filters and len(column_filters) > 0):
                try:
                    filtered_df = self.df[column_filters]
                except:
                    pass

            if (location and len(location) > 0):
                try:
                    filtered_df = filtered_df[filtered_df['place'].apply(
                        lambda x: x in location)]
                except:
                    pass

            if (lang and len(lang) > 0):
                try:
                    filtered_df = filtered_df[filtered_df['lang'].apply(
                        lambda x: x in lang)]
                except:
                    pass

            if (hashtag):
                try:
                    filtered_df = filtered_df[filtered_df['hashtags'].apply(
                        lambda x: "#" + hashtag in x.split(" ") or hashtag in x.split(" "))]
                except:
                    pass

            if (author):
                try:
                    filtered_df = filtered_df[filtered_df['original_author'].apply(
                        lambda x: x.lower().find(author.lower()) != -1)]
                except:
                    pass

            if (polarity):

                try:
                    if polarity == "None":
                        pass
                    elif polarity == "positive":
                        filtered_df = filtered_df[filtered_df['polarity'].apply(
                            lambda x: x > 0)]
                    elif polarity == "negative":
                        filtered_df = filtered_df[filtered_df['polarity'].apply(
                            lambda x: x < 0)]
                    else:
                        filtered_df = filtered_df[filtered_df['polarity'].apply(
                            lambda x: x == 0)]
                except:
                    pass

            st.write(filtered_df)

        elif (self.page == "Data Visualizations"):
            st.title("Data Visualizations")
            self.render_visulazation()

        print(self.page)


if __name__ == "__main__":
    dashboard = Dashboard("Tweeter Data Dashboard")
    dashboard.render()
