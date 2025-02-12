from bs4 import BeautifulSoup
import requests
import csv

class WebScrapingProcess:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.quotes = []
        self.authors = []

    def scrape_page(self):
        # Page to scrape
        page_to_scrape = requests.get(self.url)
        if page_to_scrape.status_code == 200:
            self.soup = BeautifulSoup(page_to_scrape.text, "html.parser")
        else:
            print(f"Failed to retrieve the page. Status code: {page_to_scrape.status_code}")
            self.soup = None

    def find_quotes_authors(self):
        if self.soup:
            # Find quotes and authors
            self.quotes = self.soup.findAll("span", attrs={"class": "text"})
            self.authors = self.soup.findAll("small", attrs={"class": "author"})
        else:
            print("Soup is not initialized. Cannot find quotes and authors.")

    def get_quotes_authors(self):
        return [(quote.text, author.text) for quote, author in zip(self.quotes, self.authors)]

def create_file(filename, data):
    with open(filename, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["QUOTES", "AUTHORS"])
        for quote, author in data:
            writer.writerow([quote, author])
    print(f"Data successfully written in {filename}")

if __name__ == "__main__":
    url = "https://quotes.toscrape.com/"
    scraper = WebScrapingProcess(url)
    scraper.scrape_page()
    scraper.find_quotes_authors()
    data = scraper.get_quotes_authors()
    create_file("scraped_quotes.csv", data)
