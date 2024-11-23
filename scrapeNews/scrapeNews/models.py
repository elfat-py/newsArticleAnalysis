from sqlalchemy import create_engine, Column, String, Text, Integer
from sqlalchemy.ext.declarative import declarative_base

# Define the base for models
Base = declarative_base()

# Database engine
engine = create_engine('mysql+mysqlconnector://root:rootkeris@localhost:3306/news_db', echo=True)

# Define the Article model
class ArticleKlan(Base):
    __tablename__ = 'articles_klan'

    id = Column(Integer, primary_key=True, autoincrement=True)  # Unique identifier
    article_title = Column(String(255), unique=True)  # No autoincrement for primary key (title is unique)
    article_link = Column(String(255))
    article_description = Column(Text)
    time_of_post = Column(String(50))
    category = Column(String(100))
    article_body = Column(Text)
    image_url = Column(String(255))

# Ensure the table is created
Base.metadata.create_all(engine)
