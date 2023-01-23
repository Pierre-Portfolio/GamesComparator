from django.shortcuts import render
from django.http import JsonResponse

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
Steam = str("https://store.steampowered.com/search/?term=")
IG = str("https://www.instant-gaming.com/fr/rechercher/?gametype=games&query=")
G2A = str("https://www.g2a.com/fr/category/gaming-c1?f[product-kind][0]=10&query=")
EpicGames = str("https://store.epicgames.com/en-US/browse?q=")
GOG = str("https://www.gog.com/fr/games?query=")

def homepage_render(request):
    page = render(request, "homepage.html")
    return page

#Function which return a Json object
def ReturnElem(title =  None, picture_url = None, price = None, opinion = None, link = None ):
    # Create a dictionary with the information
    game_info = {
        'title': title[:16],
        'opinion' : opinion,
        'price': price,
        'link' : link,
        'picture_url': picture_url
    }

    return game_info

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
        opinion = opinion_element["data-tooltip-html"].split("<br>")[0]

        price = result.find('div', class_='search_price').text.replace(' ','').replace('\r\n','')
        if(len(price.split("€")) != 1):
            prices = price.split("€")
            price = prices[1] + "€"
        
    except AttributeError:
        title = " - "
        picture_url = " - "
        price = " - "
        opinion = " - "
        url = " - "
    # Return the informations
    return ReturnElem(title, picture_url, price, opinion, url)

# Instant Gaming
def ScrappingIG(userSearch):
    # scraping
    driver = webdriver.Chrome()
    IG_url = str(IG + userSearch.replace(" ","%20"))
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome('chromedriver', chrome_options=options)
    driver.get(IG_url)
    # we select the correct data 
    try:
        title = driver.find_elements(By.CLASS_NAME, "title")[4].get_attribute('innerHTML');
        picture_url = driver.find_elements(By.CLASS_NAME, "picture")[0].get_attribute('src');
        price = driver.find_elements(By.CLASS_NAME, "price")[1].get_attribute('innerHTML');
        opinion = " - "
        url = IG_url
    except IndexError:
        title = " - "
        picture_url = " - "
        price = " - "
        opinion = " - "
        url = " - "
    except ConnectionError:
        title = " - "
        picture_url= " - "
        price = " - "
        opinion = " - "
        url = " - "
    # Closes the current window
    driver.close()
    
    # Return the informations
    return ReturnElem(title, picture_url, price, opinion, url)

# G2A
def ScrappingG2A(userSearch):
    # scraping
    driver = webdriver.Chrome()
    G2A_url = G2A + userSearch.replace(" ","+")
    driver.get(G2A_url)

    # we select the correct data
    try:
        title = driver.find_elements(By.XPATH, "//h3")[6].text;
    except IndexError:
        title = " I "

    try:
        picture_url = driver.find_elements(By.XPATH, "//img")[1].get_attribute('src');
    except IndexError:
        picture_url = " I "

    try:
        price_before = driver.find_elements(By.XPATH, "//span")[212].text.split(" ");
        price = price_before[1] + price_before[0]
    except IndexError:
        price = " I "
    
    opinion = " - "
    url = G2A_url
        
    # Closes the current window
    driver.close()
    
    # Return the informations
    return ReturnElem(title, picture_url, price, opinion, url)

#Epicgames
def ScrappingEpics(userSearch):
    # scraping
    driver = webdriver.Chrome()
    EP_url = str(EpicGames + userSearch.replace(" ","%20")+'&sortBy=relevancy')
    driver.get(EP_url)

    # we select the correct data 
    try:
        title = driver.find_elements(By.CLASS_NAME, "css-rgqwpc")[0].get_attribute('innerHTML');
        picture_url = driver.find_elements(By.CLASS_NAME, "css-174g26k")[0].get_attribute('src');
        price = driver.find_elements(By.CLASS_NAME, "css-119zqif")[5].get_attribute('innerHTML');
        opinion=" - ";
    except IndexError:
        title=" - ";
        picture_url=" - ";
        price=" - ";
        opinion=" - ";
        EP_url = " - ";

    # Closes the current window
    driver.close()
    
    # Return the informations
    return ReturnElem(title, picture_url, price, opinion, EP_url)

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
        title=" - ";
        picture_url=" - ";
        price=" - ";
        opinion=" - ";
        GOG_url= " - "
        
    # Return the informations
    return ReturnElem(title, picture_url, price, opinion, GOG_url)

def APIgames(request):
    userSearch = request.GET['q']
    
    table=[]

    #Scrapping
    table.append(ScrappingSteam(userSearch))
    table.append(ScrappingIG(userSearch))
    table.append(ScrappingG2A(userSearch))
    table.append(ScrappingEpics(userSearch))
    table.append(ScrappingGOG(userSearch))

    return JsonResponse(table, safe=False)