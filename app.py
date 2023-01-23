import streamlit as st
from tiktokapipy.api import TikTokAPI
import pandas as pd

import os
os.system("playwright install")


st.title("TikTok Scraper")

st.markdown("This application uses the (inofficial API TikTokPy by Russel Newton)[https://github.com/Russell-Newton/TikTokPy] and is currently under development by Jonathan Kemper. Expect errors.")

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
        st.bar_chart(df['views'])
            # df.to_csv('{}_videos.csv'.format(account), mode='a', index=False, header=False)
        
    
UserNameInfo(df)
