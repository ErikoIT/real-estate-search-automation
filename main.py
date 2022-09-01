from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import lxml

ZILLOW_URL = "https://www.zillow.com/frisco-tx/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Frisco%2C%20TX%22%2C%22mapBounds%22%3A%7B%22west%22%3A-96.94386390820313%2C%22east%22%3A-96.73237709179688%2C%22south%22%3A33.075812933905716%2C%22north%22%3A33.2247084948804%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A18208%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22mp%22%3A%7B%22max%22%3A1500%7D%2C%22price%22%3A%7B%22max%22%3A327509%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"

MY_HTTP_HEADER = {
    "Accept-Language": "en-GB,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0"
}

request = requests.get(url=ZILLOW_URL, headers=MY_HTTP_HEADER)
website_result = request.text

soup = BeautifulSoup(website_result, "html.parser")
house_cards = soup.find_all(name="div", class_="list-card-info")

price_elements = soup.select(".list-card-price")
prices = [price.get_text().split("+")[0] for price in price_elements if "$" in price.text]

link_elements = soup.select(".list-card-info a")
links = []
for link in link_elements:
    href = link["href"]
    if "href" not in href:
        links.append(f"https://www.zillow.com{href}")
    else:
        links.append(href)

address_elements = soup.select(".list-card-info a")
addresses = [address.get_text().split(" | ")[-1] for address in address_elements]

for n in range(len(links)):
    service = Service("C:/Development/chromedriver.exe")

    driver = webdriver.Chrome(service=service)
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSewQ6tmFmGrGndf7fqihgrsaWp8aIHdgVjQLZXnPmzIx9f8vQ/viewform?usp"
               "=sf_link")
    form_address = driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")
    form_price = driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")
    form_link = driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")
    submit = driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div/span/span")

    form_address.send_keys(addresses[n])
    form_price.send_keys(prices[n])
    form_link.send_keys(links[n])
    submit.click()
