from bs4 import BeautifulSoup
import json
import requests
from selenium import webdriver
import requests
from bs4 import BeautifulSoup, element
import time

class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def exit(self):
        self.driver.quit()

    def get_counts(self, user):
        """Fetches the count of followers and followings for any user
        via standard HTML scraping"""
        user_ref = user.href
        page = requests.get('https://soundcloud.com'+ user_ref )
        soup = BeautifulSoup(page.content, 'html.parser')
        html_str = soup.prettify()
        JSON_index_start = html_str.find('var c=')
        JSON_index_end = html_str.find(',o=Date.now()')
        sc_JSON = html_str[JSON_index_start+6:JSON_index_end]
        sc_JSON = json.loads(sc_JSON)
        try:
            followings_count = (sc_JSON[3]['data'][0]['followings_count'])
            followers_count = (sc_JSON[3]['data'][0]['followers_count'])
            return {'followers_count': followers_count, 'followings_count':followings_count}
        except IndexError:
            return self.get_counts(user)

    def get_user_collection(self, user, col_type):
        """Fetches a users entire followers list or following list based on
        the col_type (collection type - "followers" or "following") using a
        Chrome Driver to simulate JS"""
        #url location of the collection and collection type (followers or followings)
        url = 'https://soundcloud.com'+ user.href + '/' + col_type
        self.driver.get(url)
        #Scrolling to the bottom to load enitre page due to JS pagination
        scroll_script = """
            window.scrollTo(0, document.body.scrollHeight);
            var pageLength = document.body.scrollHeight;
            return pageLength;
        """
        page_length = self.driver.execute_script(scroll_script)
        while(True):
            last_count = page_length
            time.sleep(2) #allows time for the page to load after a scroll
            page_length = self.driver.execute_script(scroll_script)
            if last_count == page_length:
                break

        #Extracting Data with BeautifulSoup
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        html_user_collection = soup.find_all('div',\
        attrs={'class': 'userBadgeListItem__title'})
        user_collection = []
        #Cleaning data into a logical format
        for user in html_user_collection:
            href = user.a['href']
            user_name = user.a.contents[0].split('\n')
            user_name = user_name[1].strip()
            user_collection.append({'user_name':user_name, 'href': href})
        return user_collection

    #function wrappers to avoid typos in url strings
    def get_followers(self, user):
        return self.get_user_collection(user, 'followers')
    def get_followings(self, user):
        return self.get_user_collection(user, 'following')
