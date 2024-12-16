import mysql.connector
from termcolor import colored
import re
from transformers import pipeline


class Database:
    def __init__(self, config):
        self.connection = mysql.connector.connect(**config)
        self.cursor = self.connection.cursor()

# i think we be fetching all the articles where we find the keywords we are looking for
    def fetch_articles(self, keyword):
        query = """
            SELECT article_title, article_body
            FROM articles
            WHERE article_title LIKE %s OR article_body LIKE %s
        """
        self.cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()


class SentimentAnalyzer:
    def __init__(self):
        self.pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
        self.sentiment_labels = {
            1: ("Shumë negativ", "red"),
            2: ("Negativ", "red"),
            3: ("Neutral", None),
            4: ("Pozitiv", "green"),
            5: ("Shumë pozitiv", "green")
        }

    def analyze(self, text):
        analysis = self.pipeline(text)[0]
        sentiment_score = int(analysis['label'].split()[0]) # i think we are passing the color based on the sentiment score here right ???
        sentiment, color = self.sentiment_labels[sentiment_score]
        return sentiment, color, sentiment_score


class KeywordAnalyzer:
    def __init__(self, db, sentiment_analyzer, keywords):
        self.db = db
        self.sentiment_analyzer = sentiment_analyzer
        self.keywords = keywords

    def highlight_keyword(self, text, keyword, color):
        keyword = keyword.lower()
        words = text.split()
        highlighted_words = [
            colored(word, color, attrs=['bold', 'underline']) if color and keyword in word.lower() else word
            for word in words
        ]
        return ' '.join(highlighted_words)

    def process_article(self, keyword, body):
        sentences = re.split(r'[.!?]', body)
        keyword_sentences = [s.strip() for s in sentences if keyword.lower() in s.lower()]
        results = []

        for sentence in keyword_sentences:
            sentiment, color, score = self.sentiment_analyzer.analyze(sentence)
            highlighted = self.highlight_keyword(sentence, keyword, color)
            results.append((highlighted, sentiment, score))

        return len(results), results

    def analyze_keywords(self):
        for keyword in self.keywords:
            print(colored(f"\nDuke analizuar: {keyword}", 'cyan'))
            articles = self.db.fetch_articles(keyword)

            if not articles:
                print(colored(f"Asnjë rezultat për: {keyword}", 'red'))
                continue

            total_count = 0
            for title, body in articles:
                count, results = self.process_article(keyword, body)
                total_count += count

                print(f"\n{colored('Titulli:', 'yellow')} {self.highlight_keyword(title, keyword, None)}")
                for idx, (sentence, sentiment, score) in enumerate(results, 1):
                    color = 'green' if sentiment in ["Pozitiv", "Shumë pozitiv"] else 'red' if sentiment in ["Negativ", "Shumë negativ"] else 'yellow'
                    print(f"{colored(f'[{idx}]', 'blue')} {sentence} [{colored(sentiment, color)}] - Score: {score}")

            print(f"{colored('Gjithsej raste:', 'magenta')} {total_count}")


if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "user": "root",
        "database": "news_analysis"
    }
    keywords = ["Integrimi", "Bashkimi Europian", "Ballkani Perëndimor", "Zgjerimi i BE"]

    db = Database(db_config)
    sentiment_analyzer = SentimentAnalyzer()
    analyzer = KeywordAnalyzer(db, sentiment_analyzer, keywords)

    analyzer.analyze_keywords()
    db.close()