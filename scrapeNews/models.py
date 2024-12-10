from sqlalchemy import create_engine, Column, String, Text, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://root@localhost:3306/news_analysis', echo=True)

class Articles(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, autoincrement=True)  # Unique identifier
    article_title = Column(String(255), unique=True)
    article_link = Column(String(255))
    time_of_post = Column(String(50))
    category = Column(String(100))
    article_body = Column(Text)
    image_url = Column(String(255))
    channel = Column(String(100))


Base.metadata.create_all(engine)
