from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text, Integer, DateTime
from datetime import datetime

# Base and Engine setup
Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://root@localhost:3306/news_analysis', echo=True)

# Articles Table
class Articles(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    article_title = Column(String(255), unique=True)
    article_link = Column(String(255))
    time_of_post = Column(String(50))
    category = Column(String(100))
    article_body = Column(Text)
    image_url = Column(String(255))
    channel = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    keyword_count = Column(Integer, default=0)  # New column to store the count of keywords


# Keywords Table
class Keywords(Base):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True, autoincrement=True)
    keyword = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Ensure tables and columns exist
with engine.connect() as connection:
    inspector = inspect(engine)

    # Check and add missing columns in Articles table
    try:
        columns = inspector.get_columns('articles')
        column_names = [column['name'] for column in columns]

        if 'keyword_count' not in column_names:
            print("Adding 'keyword_count' column...")
            connection.execute(
                text("ALTER TABLE articles ADD COLUMN keyword_count INT DEFAULT 0")
            )
            print("'keyword_count' column added successfully.")
    except Exception as e:
        print(f"Error inspecting or altering Articles table: {e}")

    # Check if Keywords table exists, and create if not
    try:
        if not inspector.has_table('keywords'):
            print("Creating 'keywords' table...")
            Base.metadata.create_all(engine)
            print("'keywords' table created successfully.")
    except Exception as e:
        print(f"Error creating Keywords table: {e}")


# Add default keywords
def add_default_keywords(session):
    default_keywords = ['shba', 'Bashkimi Europian', 'Europa', 'BE', 'Ballkani Perëndimor', 'Zgjerimi i BE']
    for keyword in default_keywords:
        # Add keyword only if it doesn't already exist
        exists = session.query(Keywords).filter_by(keyword=keyword).first()
        if not exists:
            session.add(Keywords(keyword=keyword))
            print(f"Added keyword: {keyword}")
    session.commit()


# Count keywords in articles and save in the Articles table
def update_keyword_counts(session):
    """
    Count occurrences of keywords in each article's article_body and save the count in the Articles table.
    """
    # Fetch all keywords from the Keywords table
    keywords = [keyword.keyword for keyword in session.query(Keywords).all()]
    if not keywords:
        print("No keywords found in the database.")
        return

    # Fetch all articles
    articles = session.query(Articles).all()

    print(f"Processing {len(articles)} articles...")

    for article in articles:
        if article.article_body:
            # Count occurrences of all keywords in the article body
            keyword_count = sum(article.article_body.lower().count(keyword.lower()) for keyword in keywords)
            article.keyword_count = keyword_count  # Save the count in the keyword_count column
            print(f"Updated article {article.id} with keyword count: {keyword_count}")

    session.commit()
    print("Keyword counts updated successfully.")


# Main execution
# if __name__ == '__main__':
#     # Create session
#     Session = sessionmaker(bind=engine)
#     session = Session()
#
#     try:
#         # Add default keywords to the database
#         add_default_keywords(session)
#
#         # Update keyword counts in articles
#         update_keyword_counts(session)
#     except Exception as e:
#         print(f"Error during execution: {e}")
#     finally:
#         session.close()
