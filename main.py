import sys
import requests
from bs4 import BeautifulSoup
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.config import Config

Config.set("graphics", "width", "500")
Config.set("graphics", "height", "200")
Config.set("graphics", "resizable", "0")

class WebScraper:
    def __init__(self, url):
        self.url = url
        self.home_link = None
        self.away_link = None
        self.date = None

    def fetch_div_img(self, div):
        image = div.find("img")
        if not image:
            print("No img in div")
            return None
        link = image["src"]
        return link

    def scrape(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            print(f"Failed to fetch content! Status code: {response.status_code}")
            sys.exit(1)

        soup = BeautifulSoup(response.text, "html.parser")
        next_match_div = soup.find("div", class_ = "next-match-wrapper")
        if not next_match_div:
            print("Failed to fetch next match div")
            sys.exit(1)

        home_div = next_match_div.find("div", class_ = "team-1")
        away_div = next_match_div.find("div", class_ = "team-2")
        date_div = next_match_div.find("div", class_ = "time")

        if not home_div:
            print("Failed to fetch home team div")
            sys.exit(1)
        if not away_div:
            print("Failed to fetch away team div")
            sys.exit(1)
        if not date_div:
            print("Failed to fetch time div")
            sys.exit(1)

        paragraphs = date_div.find_all('p')

        self.home_link = self.fetch_div_img(home_div)
        self.away_link = self.fetch_div_img(away_div)
        self.date = [str(p.text) for p in paragraphs]

class ImageFetcherApp(App):
    def __init__(self, url, **kwargs):
        super().__init__(**kwargs)
        self.scraper = WebScraper(url)

    def build(self):
        self.title = "KKP Notification"
        self.scraper.scrape()
        root = BoxLayout(orientation = 'horizontal', spacing = 50)

        self.image1 = AsyncImage(source = self.scraper.home_link, size_hint = (None, None), size = (200, 200))
        root.add_widget(self.image1)

        date_text = " Next game: \n" + self.scraper.date[0] + "\n" + self.scraper.date[1]

        root.add_widget(Label(text = date_text, font_size = 15, halign = "center"))

        self.image2 = AsyncImage(source = self.scraper.away_link, size_hint = (None, None), size = (200, 200))
        root.add_widget(self.image2)

        return root

if __name__ == "__main__":
    target_url = "https://partizan.basketball/"
    ImageFetcherApp(target_url).run()