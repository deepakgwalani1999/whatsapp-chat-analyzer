import streamlit as st
from preprocessor import  preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file=st.sidebar.file_uploader("Choose File")
if uploaded_file is not None:
    byte_data= uploaded_file.getvalue()
    data=byte_data.decode("utf-8")
    df=preprocessor(data)
    st.title("Statistics")
    person_list=df["user"].unique().tolist()
    if "unknown system message" in person_list:
        person_list.remove("unknown system message")
    person_list.sort()
    person_list.insert(0,"Overall")

    person=st.sidebar.selectbox("Show Analysis WRT.. ",person_list)
    if st.sidebar.button("Show Analysis"):
        col1, col2, col3, col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(helper.fetch_count(df,person))
        
        with col2:
            st.header("Total Words")
            st.title(helper.fetch_word_count(df,person))
    
        with col3:
            st.header("Total Media Sent")
            st.title(helper.fetch_media_count(df,person))
            
        with col4:
            st.header("Total Links Shared")
            st.title(helper.fetch_link_count(df,person))
        
        #finding buissiest  user in whatsapp chatbox
        def show_active_users(df,person):
            if(person=="Overall"):
                col1,col2=st.columns(2)

                with col1:
                    st.header("User Contribution")
                    x= df["user"].value_counts()
                    st.dataframe(x)

                with col2:
                    st.title("Contribution")
                    fig,axis=plt.subplots()
                    axis.bar(list(x.index),list(x.values),color="Black")
                    plt.xticks(rotation="vertical")
                    st.pyplot(fig)
        show_active_users(df,person)

#WordCloud
        st.title("Word Cloud")
        df_wc=helper.create_word_cloud(df,person)
        fig,axis=plt.subplots()
        axis.imshow(df_wc)
        st.pyplot(fig)
#Most Common words
        
        st.title("Let's See Words Stats")
        col1,col2=st.columns(2)
        with col1:
            st.title("Most Common Words Used In Chat")
            fig,axis=plt.subplots()
            word_df=helper.most_common_words(df,person)
            st.dataframe(word_df)
        with col2:
            st.title("Top 20  Common Words Written")
            axis.barh(word_df[0],word_df[1],color="Green")
            plt.xticks(rotation="horizontal")
            st.pyplot(fig)
#emojis used
        st.title("User's Favourite Emoticons")
        col1,col2=st.columns(2)
        with col1:
            st.header("Emojis Used Most Frequently")
            emoji_df=helper.emoji_sent(df,person)
            st.dataframe(emoji_df)
    
        with col2:
            st.header("Use Of Paricular Emoticons")
            fig, ax=plt.subplots()
            ax.pie(emoji_df[1],labels=emoji_df[0],autopct="%0.02f%%")
            plt.tight_layout()
            st.pyplot(fig)
        st.title("Interactions...")
    #Monthly Interactions
        col1,col2=st.columns(2)
        with col1:
            st.header("Monthly Interactions")
            timeline=helper.show_monthly_interactions(df,person)
            fig,ax=plt.subplots()
            ax.plot(timeline["time"],timeline["text"],color="Orange")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

    
    #daily_intercation
        with col2:
            st.header("Daily Interactions")
            daily_timeline=helper.show_daily_interactions(df,person)
            fig,ax=plt.subplots()
            ax.plot(daily_timeline["only_date"],daily_timeline["text"],color="Purple")
            plt.xticks(rotation="vertical")

            st.pyplot(fig)
    #activity_map
        st.title("User's Activity map")
        col1,col2=st.columns(2)
        with col1:
            st.title("Most Busy Days")
            activity_chart=helper.show_activity_chart(df,person)
            fig,ax=plt.subplots()
            ax.bar(activity_chart["day_name"],activity_chart["count"],color="Brown")
            plt.xticks(rotation="vertical")

            st.pyplot(fig)
        with col2:
            st.title("Most Busy Months")
            month_activity=helper.show_monthly_activity_chart(df,person)
            fig,ax=plt.subplots()
            ax.bar(month_activity["month"],month_activity["count"],color="yellow")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
    #Most Active day for user
        st.title("Most Active At Time")
        time_table=helper.show_activity_time_in_day(df,person)
        fig,ax=plt.subplots()
        ax=sns.heatmap(time_table)
        st.pyplot(fig)


        
    
        





    



            
                
