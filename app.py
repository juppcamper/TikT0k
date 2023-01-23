import streamlit as st
from tiktokapipy.api import TikTokAPI
import pandas as pd

import os
os.system("playwright install")

st.set_page_config(layout="wide")

st.title("TikTok Scraper")

st.markdown("This application uses TikTokPy by Russel Newton and is currently under development by Jonathan Kemper. Expect errors. Enter the name of an account in the field below and select the number of videos to scrape with the slider in the sidebar")

names = st.text_input("Account")

video_limit = st.sidebar.slider("Select the number of videos to display", min_value=1, max_value=100, value=50)

df = pd.DataFrame(columns = ["account", "id", "cover", "dynamic_cover", "url", "length", "time", "likes", "views", "shares", "comments", "description", "sound_name", "sound_url"])

def UserNameInfo(df):

    with TikTokAPI() as api:
        user = api.user(names, video_limit = video_limit)
        print(len(user.videos._light_models))
        for video in user.videos:
            account = video.author
            id = video.id
            time = video.create_time.strftime("%d.%m.%Y, %H:%M:%S")
                
            cover = video.video.cover
            dynamic_cover = video.video.dynamic_cover
                
            url = video.video.play_addr

            likes = video.stats.digg_count
            views = video.stats.play_count
            shares = video.stats.share_count
            comments = video.stats.comment_count
                
            length = video.video.duration
            description = video.desc
                
            sound_name = video.music.title
            sound_url = video.music.play_url
                # sound_author = video.music.author_name

            df = pd.concat([df, pd.DataFrame([[account,id,cover,dynamic_cover,url,length,time,likes,views,shares,comments,description,sound_name,sound_url]], columns = df.columns)], ignore_index=True)
        st.dataframe(df)

        columns = ["views", "likes", "shares", "comments", "length"]
        selected_columns = st.multiselect("Select columns", columns)

        for col in selected_columns:
            st.bar_chart(df[col], subplots=(1, len(selected_columns)))


    
UserNameInfo(df)
