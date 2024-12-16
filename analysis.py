from sqlalchemy.orm import sessionmaker
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import pandas as pd
from wordcloud import WordCloud

# Create an engine and session
engine = create_engine('mysql+mysqlconnector://root@localhost:3306/news_analysis', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


# TODO return the image in the server of news analysis keyboard and put it somewhere in the analysis tab
# Query the database
query = "SELECT * FROM articles"
df = pd.read_sql(query, engine)

# Convert `time_of_post` to datetime, handle invalid values
df['time_of_post'] = pd.to_datetime(df['time_of_post'], errors='coerce')

# Filter out rows where time_of_post is NaT (invalid datetime)
df = df[df['time_of_post'].notna()]

# Display first few rows
print(df.head())

# -- 1. Category Distribution --
category_counts = df['category'].value_counts()

plt.figure(figsize=(10, 6))
category_counts.plot(kind='bar', color='skyblue')
plt.title('News Category Distribution')
plt.xlabel('Category')
plt.ylabel('Number of Articles')
plt.tight_layout()
plt.savefig("category_distribution.png")

# -- 2. Articles Posted Over Time --
articles_over_time = df.groupby(df['time_of_post'].dt.date).size()

plt.figure(figsize=(12, 6))
articles_over_time.plot(kind='line', marker='o', color='green')
plt.title('Articles Posted Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Articles')
plt.grid()
plt.tight_layout()
plt.savefig("articles_over_time.png")

# -- 3. Channel-wise Contribution --
channel_counts = df['channel'].value_counts()


plt.figure(figsize=(10, 6))
channel_counts.plot(kind='barh', color='purple')
plt.title('Channel-wise Article Contribution')
plt.xlabel('Number of Articles')
plt.ylabel('Channel')
plt.tight_layout()
plt.savefig("channel_contribution.png")

# -- 4. Most Common Words in Article Titles --
text = " ".join(title for title in df['article_title'].dropna())

wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Most Common Words in Article Titles')
plt.tight_layout()
plt.savefig("wordcloud_titles.png")

# -- 5. Articles per Category Over Time --
category_time = df.groupby([df['time_of_post'].dt.date, 'category']).size().unstack(fill_value=0)

category_time.plot(kind='area', stacked=True, figsize=(12, 6), alpha=0.8)
plt.title('Articles per Category Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Articles')
plt.legend(title='Category')
plt.tight_layout()
plt.savefig("category_over_time.png")

# -- 6. Article Length Analysis --
df['article_length'] = df['article_body'].str.len()

avg_length_by_category = df.groupby('category')['article_length'].mean()

plt.figure(figsize=(10, 6))
avg_length_by_category.plot(kind='bar', color='orange')
plt.title('Average Article Length by Category')
plt.xlabel('Category')
plt.ylabel('Average Length (characters)')
plt.tight_layout()
plt.savefig("article_length_by_category.png")

# -- 7. Image Usage Analysis --
image_usage = df['image_url'].notna().value_counts()

plt.figure(figsize=(6, 6))
image_usage.plot(kind='pie', labels=['With Images', 'Without Images'], autopct='%1.1f%%', colors=['blue', 'red'])
plt.title('Image Usage in Articles')
plt.ylabel('')
plt.tight_layout()
plt.savefig("image_usage.png")

# -- 8. Articles by Day of the Week --
df['day_of_week'] = df['time_of_post'].dt.day_name()


day_counts = df['day_of_week'].value_counts()

plt.figure(figsize=(10, 6))
day_counts.plot(kind='bar', color='teal')
plt.title('Articles by Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Number of Articles')
plt.tight_layout()
plt.savefig("articles_by_day.png")
