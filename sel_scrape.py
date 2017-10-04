from selenium import webdriver
import requests
from bs4 import BeautifulSoup, element
import time

user_ref = '/gabeleibo'
url = 'https://soundcloud.com'+ user_ref + '/followers'


driver = webdriver.Chrome()
driver.get(url)
lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match=False
while(match==False):
        lastCount = lenOfPage
        time.sleep(2)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True

soup = BeautifulSoup(driver.page_source, 'html.parser')
html_followers = soup.find_all('div', attrs={'class': 'userBadgeListItem__title'})
followers = []
for follower in html_followers:
    user_name = follower.a.contents[0].split('\n')
    user_name = user_name[1].strip()
    followers.append(user_name)
print(followers)
driver.quit()
