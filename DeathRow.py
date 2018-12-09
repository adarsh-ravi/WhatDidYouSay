import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from pandas import DataFrame, Series
import re
import nltk
from nltk.corpus import stopwords
from collections import Counter
from pywordcloud import pywordcloud
import boto3
from bs4 import BeautifulSoup
import requests
import json

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Histogram plot of the age received
xl = pd.ExcelFile("Texas_Last_Statement_Excel.xlsx")
df_lastStatement = xl.parse("Sheet1")
df_lastStatement_age = df_lastStatement.dropna(how='any', axis=0)
plt.hist(df_lastStatement_age["Received Age"], bins=10)
plt.title("Age when people received sentence")
plt.xlabel("Age")
plt.ylabel("Count")
plt.show()
plt.gcf().clear()

# Box plot showing the age distribution
sns.boxplot(y=df_lastStatement_age["Received Age"])
plt.show()
plt.gcf().clear()

print("Minimum Age: {}".format(min(df_lastStatement_age["Received Age"])))
print("Average Age: {}".format((max(df_lastStatement_age["Received Age"]) - min(df_lastStatement_age["Received Age"])) / 2))
print("Maximum Age: {}".format(max(df_lastStatement_age["Received Age"])))

# Pie chart of the race of the sentenced people
race_count = Counter(df_lastStatement["Race"])
# print(race_count)
plt.pie(race_count.values(), labels=race_count.keys(), autopct='%1.2f%%')
plt.title("Race of people who were convicted")
plt.show()
plt.gcf().clear()

# Number of executions every year since 1982
df_lastStatement["Date"] = pd.to_datetime(df_lastStatement["Date"])
df_lastStatement["Year"] = df_lastStatement["Date"].dt.year
year_count = Counter(df_lastStatement["Year"])
sns.barplot(list(year_count.keys()), list(year_count.values()), color="indianred")
plt.xticks(rotation=90)
plt.title("# of inmates executed each year (1982-2017)")
plt.xlabel("Year")
plt.ylabel("Count")
plt.show()
plt.gcf().clear()

# Education level of the inmates on death row
edu_Count = Counter(df_lastStatement["Education level"])
sns.barplot(x=list(edu_Count.keys()), y=list(edu_Count.values()), color="seagreen")
plt.xlabel("Highest Education Level Earned")
plt.ylabel("Count")
plt.title("Education level of death row inmates")
plt.show()
plt.gcf().clear()

# Language Processing: Combine all statement into a single string and remove any stop words.
statementList = list()
lemmatization = nltk.WordNetLemmatizer()
for statement in df_lastStatement["Last Statement"]:
    statement = re.sub("[^a-zA-Z]", " ", statement)
    statement = statement.lower()
    statement = nltk.word_tokenize(statement)
    statement = [i for i in statement if i not in set(stopwords.words("english"))]
    statement = [lemmatization.lemmatize(i)for i in statement]
    statement = " ".join(statement)
    statementList.append(statement)
allStatements = ' '.join(statementList)
pywordcloud.create(allStatements, outfile="popularWords.html", uppercase=False, showfreq=False, frequency=100, removepunct=False, minfont=1.5, maxfont=10, hovercolor="green", showborder=False, fontfamily='calibri', width="1500px", height="400px")

# Calling AWS Sentiment Analysis API and writing the output into a text file.
# comprehend = boto3.client(aws_access_key_id='AKIAIEM3STY2AUEZKKRQ', aws_secret_access_key='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', service_name='comprehend', region_name='us-east-2')
#
# sentimentList = []
# for text in statementList:
# # for i in range(0, 1):
#     jsonStr = json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4)
#     i = json.loads(jsonStr)
#     sentimentList.append(i["Sentiment"])
#     # print(i["SentimentScore"])
# print(sentimentList)
# text_file = open("H:\Output.txt", "w")
# strSentiment = " ".join(sentimentList)
# text_file.write(strSentiment)

# Use the output from the sentiment analysis of each statement and plot a scatter plot.
text_file = open("H:\Output.txt", "r")
strSentiment = " ".join(text_file)
strSentiment = str.replace(strSentiment, ',', '')
text_file.close()
# strSentimentList = ' '.join(str)
pywordcloud.create(strSentiment, outfile="Sentiments.html", uppercase=True, showfreq=False, frequency=100, removepunct=False, minfont=1.5, maxfont=10, hovercolor="green", showborder=False, fontfamily='calibri', width="1000px", height="400px")
sentimentCount = Counter(strSentiment.split())
# print(sentimentCount)

sns.barplot(x=list(sentimentCount.keys()), y=list(sentimentCount.values()), color="darkslategray")
plt.title("Sentiment of the Last Statement")
plt.xlabel("Sentiments")
plt.ylabel("Count")
plt.show()
plt.gcf().clear()

victims = {"White": df_lastStatement["White victim"].sum(),
           "Black": df_lastStatement["Black victim"].sum(),
           "Hispanic": df_lastStatement["Hispanic victim"].sum(),
           "Others": df_lastStatement["Victim of other races"].sum()
           }
sns.barplot(x=list(victims.values()), y=list(victims.keys()), color="teal")
plt.title("Race of the victims")
plt.ylabel("Race")
plt.xlabel("Count")
plt.show()
plt.gcf().clear()

url = 'https://www.bbc.com/news/magazine-31698154'
result = requests.get(url)
c = result.content
soup = BeautifulSoup(c, "lxml")
summary = soup.find('div', attrs={"class": "story-body__inner"})
p = summary.find_all('p')
strReport = ''
for x in p:
    strReport += x.text

strReport = strReport.lower()
strReport = nltk.word_tokenize(strReport)
strReport = [i for i in strReport if i not in set(stopwords.words("english"))]
strOmitList = ['interview', 'storyville', 'leslee', 'article', 'bbc', 'four', 'article', 'broadcast']
strReport = [i for i in strReport if i not in strOmitList]
strReport = [lemmatization.lemmatize(i) for i in strReport]
strReport = ' '.join(strReport)

pywordcloud.create(strReport, outfile="Rapist.html", uppercase=True, showfreq=True, frequency=100, removepunct=False, minfont=1.5, maxfont=6, hovercolor="green", showborder=False, fontfamily='calibri', width="1300px", height="800px")
# print(strReport)

