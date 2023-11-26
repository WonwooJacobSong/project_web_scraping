"""
This project is a Python script that utilizes web scraping to gather information from various websites. 
It includes functionalities to retrieve today's weather in Toronto from Google, display today's news in Toronto from a local news website, 
and provide the current standings of Premier League teams. The script uses the requests library to make HTTP requests, 
BeautifulSoup for web scraping, and involves functions for each of the three main features.
"""

import requests
from bs4 import BeautifulSoup


def create_soup(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'lxml')
    return soup

#The scrape_weather function fetches current temperature, the percentage of rain or snow, and the weather forecast for Toronto from a Google search page.
def scrape_weather():
    print("Today's weather in Toronto")
    url = "https://www.google.com/search?q=toronto+weather&rlz=1C1CHBF_enCA960CA961&oq=toronto+wea&aqs=chrome.0.0i512l2j69i57j0i512l7.1590j1j7&sourceid=chrome&ie=UTF-8"
    soup = create_soup(url)
    curr_temp = soup.find("span", attrs={"class": "wob_t q8U8x"}).get_text().strip()
    print(curr_temp, "°C")  
    forcast_rain = soup.find("span", attrs={"id": "wob_pp"}).get_text()
    print("Percentage of rain or snow:", forcast_rain)
    weather_forcast = soup.find("span", attrs={"id": "wob_dc"}).get_text()
    print(weather_forcast)
    print()

# The scrape_news function extracts and displays the headlines and links to news articles from a local news website in Toronto.
def scrape_news():
    print("Today's news in Toronto")
    url = "https://toronto.ctvnews.ca/more/local-news"
    soup = create_soup(url)
    title = soup.findAll("h2", attrs={"class": "teaserTitle"})
    for i in range(5):
        print(i, title[i].get_text().strip())
        link = title[i].a["href"]
        print("https://toronto.ctvnews.ca{0}".format(link))
        print()
        
# The team_name function allows the user to input a team number and name to retrieve information about that specific Premier League team's overview. 
# The script uses the team's name to construct a URL for the Premier League website and fetches relevant details.
def team_name():
    url = "https://www.premierleague.com/tables"
    soup = create_soup(url)
    teams = soup.findAll("span", attrs={"class": "long"})
    print("This is the Premier League table")
    for i in range(20):
        print(i+1, teams[i].get_text())
    print("Please type the number and team name in lowercase without spaces.")
    print("For example: 12 crystalpalace")
    team_number, input_teamname = input().split()
    team_number = int(team_number) 
    input_teamname = input_teamname.lower()   
    team_mapping = {
        "arsenal": "/1/",
        "manchestercity": "/11/",
        "newcastleunited": "/23/",
        # Add the rest of the teams here
    }
    middle_url = team_mapping.get(input_teamname, None)
    if middle_url is None:
        print("Wrong number and name. Please try again.")
        return
    endpoint = teams[team_number-1].get_text().lower().replace(" ", "-") + "-overview"
    before_url = "https://www.premierleague.com/clubs"
    url = before_url + middle_url + endpoint
    soup = create_soup(url)
    print("If you want to check the overview, visit here:", url)

if __name__ == "__main__":
    scrape_weather()
    scrape_news()
    team_name()
