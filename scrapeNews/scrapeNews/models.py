from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base

# Define the base for models
Base = declarative_base()

# Database engine
engine = create_engine('mysql+mysqlconnector://root:elgert1234@localhost:3307/news_db')

# Define the Article model
class ArticleKlan(Base):
    __tablename__ = 'articles_klan'

    article_title = Column(String(255), primary_key=True, autoincrement=True)
    article_link = Column(String(255))
    article_description = Column(Text)
    time_of_post = Column(String(50))
    category = Column(String(100))
    article_body = Column(Text)
    image_url = Column(String(255))

# Create all tables
Base.metadata.create_all(engine)
