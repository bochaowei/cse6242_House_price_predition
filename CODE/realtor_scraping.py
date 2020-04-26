#from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd
def web_scraper(city,state):
    #driver = webdriver.Chrome()
    #driver.get('https://www.realtor.com/realestateandhomes-search/'+str(city)+'_'+str(state)+'/overview')
    ##driver.get('https://www.zillow.com/atlanta-ga/home-values/')

    #content = driver.page_source
    page = requests.get('http://api.scraperapi.com?api_key=39ce280eb0133a5cd1b4ff62887205c5&url=https://www.realtor.com/realestateandhomes-search/'+str(city)+'_'+str(state)+'/overview')
    content = page.text
    soup = BeautifulSoup(content, 'html.parser')
    result = soup.find_all('div', class_='jsx-1842353757 home-value-stat-value')
    value=[]
    for re in result:
      value.append(re.text.strip('$ K'))
    #driver.quit()
    return value
