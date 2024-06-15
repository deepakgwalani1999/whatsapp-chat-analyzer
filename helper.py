from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import emoji
extract=URLExtract()
def fetch_count(df,person):
    if(person=="Overall"):
        num_messages=df.shape[0]
    else:
        num_messages=df[df["user"]==person].shape[0]
    return num_messages

def fetch_word_count(df,person):
    words=[]
    if(person=="Overall"):
        for message in df["text"]:
            words.extend(message.split())
        word_count=len(words)
    else:
        for message in df[df["user"]==person]["text"]:
            words.extend(message.split())
        word_count=len(words)
    
    return word_count

def fetch_media_count(df,person):
    if person=="Overall":
        media_count= df[df["text"]=="<Media omitted>\n"].shape[0]
    else: 
        df1=df[df["user"]==person]
        df2=df1[df1["text"]=="<Media omitted>\n"]
        media_count=df2.shape[0]
    
    return media_count

def fetch_link_count(df,person):
    links=[]
    if(person=="Overall"):

        for message in df["text"]:
            links.extend(extract.find_urls(message))
        link_count=len(links)
         
    else:
        for message in df[df["user"]==person]["text"]:
            links.extend(extract.find_urls(message))
        link_count=len(links)

    return link_count
def create_word_cloud(df,person):
    
    if person!="Overall":
        df=df[df["user"]==person]
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color="purple")
    wc_df=wc.generate(df["text"].str.cat(sep=" "))
    return wc_df

def most_common_words(df,person):
    words=[]
    if person!="Overall":
        df=df[df["user"]==person]
    temp=df[df["user"]!="unknown system message"]
    temp=temp[temp["text"]!="<Media omitted>\n"]
    f=open("stop_hinglish","r")
    stop_words=f.read()
    for message in temp["text"]:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    word_df=pd.DataFrame(Counter(words).most_common(20))
    
    

    return word_df

def emoji_sent(df,person):
    if person!="Overall":
        df=df[df["user"]==person]

    
    emojis=[]
    for message in df["text"]:
        emojis.extend([e for e in message if emoji.is_emoji(e)])
    
    
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def show_monthly_interactions(df,person):
    df["month_num"]=df["dates"].dt.month
    if person!="Overall":
        df=df[df["user"]==person]
    timeline=df.groupby(["year","month_num","month"])["text"].count().reset_index()
    time=[]
    
    for x in range(timeline.shape[0]):
        time.append(timeline["month"][x]+"-"+str(timeline["year"][x]))
    timeline["time"]=time

    return timeline
def show_daily_interactions(df,person):
    df["only_date"]=df["dates"].dt.date
    if person!="Overall":
        df=df[df["user"]==person]
    daily_timeline=df.groupby("only_date").count()["text"].reset_index()

    return daily_timeline
def show_activity_chart(df,person):
    df["day_name"]=df["dates"].dt.day_name()
    if person!="Overall":
        df=df[df["user"]==person]
    activity_chart=df["day_name"].value_counts().reset_index()
    return activity_chart
def show_monthly_activity_chart(df,person):
    if person !="Overall":
        df=df[df["user"]==person]
    month_activity=df["month"].value_counts().reset_index()
    return month_activity
def show_activity_time_in_day(df,person):
    if person!="Overall":
        df=df[df["user"]==person]
    time_table=df.pivot_table(index="day_name",columns="periods",values="text",aggfunc="count")
    return time_table


    
    


    


