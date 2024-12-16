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

# Query the database
query = "SELECT * FROM articles"
df = pd.read_sql(query, engine)


# -- 3. Channel-wise Contribution --
channel_counts = df['channel'].value_counts()


plt.figure(figsize=(10, 6))
channel_counts.plot(kind='barh', color='purple')
plt.title('Channel-wise Article Contribution')
plt.xlabel('Number of Articles')
plt.ylabel('Channel')
plt.tight_layout()
plt.savefig("channels_fuck.png")
