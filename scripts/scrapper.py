import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from pymongo import MongoClient

# Optional: Clear old data
CLEAR_COLLECTION = False

# MongoDB Atlas Connection 
MONGO_URI = "mongodb+srv://geo_user:geo_pass_123@cluster0.kuskxsb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client["geo_news_db"]
collection = db["articles"]

print(f"Connected to MongoDB Atlas collection: {collection.full_name}")

if CLEAR_COLLECTION:
    collection.delete_many({})
    print("Cleared old articles from collection.")

def initialize_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://geo.tv')
    return driver

def scrape_articles(driver):
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articles = soup.find_all('article')
    print(f"Found {len(articles)} articles")

    inserted_count = 0

    for article in articles:
        title_tag = article.find('h2')
        content_tag = article.find('p')

        title = title_tag.text.strip() if title_tag else "No Title"
        content = content_tag.text.strip() if content_tag else "No Content"

        if not title or title == "No Title":
            print("Skipping article with no title")
            continue

        result = collection.update_one(
            {"title": title},
            {"$set": {"content": content}},
            upsert=True
        )

        if result.upserted_id:
            print(f"Inserted new article: {title}")
            inserted_count += 1
        elif result.modified_count > 0:
            print(f"Updated existing article: {title}")
            inserted_count += 1
        else:
            print(f"No changes for article: {title}")

    return inserted_count

def main():
    driver = initialize_driver()
    try:
        inserted_count = scrape_articles(driver)
        print(f"\nTotal articles processed: {inserted_count}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
