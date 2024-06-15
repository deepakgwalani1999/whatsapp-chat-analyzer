# convert the textual data to data frame
import re
import pandas as pd
def preprocessor(data):
    pattern=r"\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{2}\u202f\w[A-z]"
    messages=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)
    dates=re.findall(pattern,data)
    df=pd.DataFrame({"dates":dates,"messages":messages})
    df["dates"]=pd.to_datetime(df["dates"])


    user=[]
    text=[]
    for record in df["messages"]:
        entery=re.split(r"-\s([\w\W]+?):\s",record)
        if entery[1:]:
            user.append(entery[1])
            text.append(entery[2])
        else:
            user.append("unknown system message")
            text.append(entery[0])
    df.drop(columns=["messages"],inplace=True)
    df["user"]=user
    df["text"]=text
    df["month_num"]=df["dates"].dt.month
    df["only_date"]=df["dates"].dt.date
    df["year"]=df["dates"].dt.year
    df["month"]=df["dates"].dt.month_name()
    df["day_name"]=df["dates"].dt.day_name()
    df["date"]=df["dates"].dt.day
    df["hour"]=df["dates"].dt.hour
    df["minutes"]=df["dates"].dt.minute
    periods=[]
    for hour in df[["day_name","hour"]]["hour"]:
        if(hour==23):
            periods.append(str(hour)+"-"+str(00))
        elif(hour==0):
            periods.append(str(00)+"-"+str(hour+1))
        else:
            periods.append(str(hour)+"-"+str(hour+1))
        
    df["periods"]=periods
        
    print(df)

    return df


file=open("WhatsApp Chat with Veera.txt","r",encoding="utf-8")

data=file.read()

preprocessor(data)
