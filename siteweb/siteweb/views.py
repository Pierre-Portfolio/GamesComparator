from django.shortcuts import render

# Import packages for Beautiful Soup
import urllib
import bs4
import requests
from urllib import request
from bs4 import BeautifulSoup
import json

# importing packages for selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

# Global var
Steam = "https://store.steampowered.com/search/?term="
IG = "https://www.instant-gaming.com/fr/rechercher/?gametype=games&query="
G2A = "https://www.g2a.com/fr/category/gaming-c1?f[product-kind][0]=10&query="
EpicGames = "https://store.epicgames.com/en-US/browse?q="
GOG = "https://www.gog.com/fr/games?query="

def homepage_render(request):
    page = render(request, "homepage.html")
    return page

#Function which return a Json object
def ReturnJsonElem(title =  None, picture_url = None, price = None, opinion = None ):
    # Create a dictionary with the information
    game_info = {
        'title': title,
        'picture_url': picture_url,
        'price': price,
        'opinion' : opinion
    }

    # Convert the dictionary to a JSON object
    game_info_json = json.dumps(game_info)

    return game_info_json

# Steam
def ScrappingSteam(userSearch):
    # Send a GET request to the Steam search page for FIFA 22
    url = str(Steam + userSearch)
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first result on the page
    result = soup.find('a', class_='search_result_row')
    
    # Find the opinion of the game
    opinion_element = soup.find("span", {"class": "search_review_summary positive"})

    # Extract the title, picture, and price from the result
    try:
        title = result.find('span', class_='title').text
        picture_url = result.img['src']
        price = result.find('div', class_='search_price').text.replace(' ','')
        opinion = opinion_element["data-tooltip-html"]
    except AttributeError:
        title='0';
        picture_url='0';
        price='0';
        opinion='0';
    # Return the informations
    return ReturnJsonElem(title, picture_url, price, opinion)

#Epicgames
def ScrappingEpics(userSearch):
    # scraping
    driver = webdriver.Chrome()
    EP_url = str(EpicGames + userSearch.replace(" ","%20")+'&sortBy=relevancy')
    driver.get(EP_url)
    #xpath='/html/body/div[1]/div/div[4]/main/div[2]/div/div/div/div/section/div/section/div/section/section/ul/li/div/div/a/div/div/div[2]/div[3]/div/div/div/div/span'

    # we select the correct data 
    try:
        title = driver.find_elements(By.CLASS_NAME, "css-rgqwpc")[0].get_attribute('innerHTML');
        picture_url = driver.find_elements(By.CLASS_NAME, "css-174g26k")[0].get_attribute('src');
        price = driver.find_elements(By.CLASS_NAME, "css-119zqif")[5].get_attribute('innerHTML');
        opinion='0';
    except IndexError:
        title='0';
        picture_url='0';
        price='0';
        opinion='0';
    # Closes the current window
    # driver.close()
    
    # Return the informations
    return ReturnJsonElem(title, picture_url, price, opinion)

# GOG
def ScrappingGOG(userSearch):
    GOG_url = str(GOG + userSearch.replace(" ","%20"))
    request_text = request.urlopen(GOG_url).read()
    htmlpage = bs4.BeautifulSoup(request_text, "html")
    try:
        title = htmlpage.find_all(class_="product-tile__title")[0].get('title')
        picture_url='0'
        price = htmlpage.find_all(class_ = "final-value")[0].text
        opinion='0'
    except IndexError:
        title='0';
        picture_url='0';
        price='0';
        opinion='0';
        
    # Return the informations
    return ReturnJsonElem(title, picture_url, price, opinion)

def APIgames(userSearch):
    table=[]
    # Steam
    table.append(ScrappingSteam(userSearch))

    #IG
    #table.append(ScrappingIG(userSearch))

    # G2A
    #table.append(ScrappingG2A(userSearch))

    # Epic Game
    table.append(ScrappingEpics(userSearch))

    #GOG
    table.append(ScrappingGOG(userSearch))
    
    return table