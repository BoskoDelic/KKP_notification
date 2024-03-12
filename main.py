import sys
import requests
from bs4 import BeautifulSoup

def fetch_div_img(div):
    image = div.find("img")
    if not div:
        print("No img in home_div")
    link = image["src"]

    return link

def web_scraper(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch content! Status code: {response.status_code}")
        sys.exit(1)

    soup = BeautifulSoup(response.text, "html.parser")
    next_match_div = soup.find("div", class_ = "next-match-wrapper")
    if not next_match_div:
        print("Failed to fetch next match div")
        sys.exit(1)
    
    paragraphs = next_match_div.find_all('p')
    if not paragraphs:
       print("Failed to fetch next match game time")
       sys.exit(1)
    
    game_time = ""
    for el in paragraphs:
        game_time += el.text + " "
    
    game_time = game_time.strip()
    
    home_div = next_match_div.find("div", class_ = "team-1")
    away_div = next_match_div.find("div", class_ = "team-2")

    if not home_div:
        print("Failed to fetch home team div")
        sys.exit(1)
    if not away_div:
        print("Failed to fetch away team div")
        sys.exit(1)

    home_link = fetch_div_img(home_div)
    away_link = fetch_div_img(away_div)

    print(home_link)

if __name__ == "__main__":
    target_url = "https://partizan.basketball/"

    web_scraper(target_url)