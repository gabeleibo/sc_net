from models.scraper import Scraper
from models.user import Users, User
import atexit

def title(title):
    print('-'*10 + title + '-'*10)

# initialize the working database/ Scraper
user_base = Users()
scraper = Scraper()

# create the root user
user = User('gabeleibo', '/gabeleibo')
user_base.add(user)

# get root users counts
print('Analyizing Counts...')
counts = scraper.get_counts(user)
user.set_counts(counts)
print(counts)

# get the root users followers and followings:
print('Scraping followings...')
followings = scraper.get_followings(user)
print('Scraping followers...')
followers= scraper.get_followers(user)

# process followings - creates user objects and get counts for each
## Set keep_celebs to true if your Analyizing the network (like in
## celeb_chart.py) otherwise skip if you are creating the network graph
title('Followings')
user.followings = user_base.process(scraper, followings, True)

# process followers
title('Followers')
user.followers = user_base.process(scraper, followers, True)

#Close the scraper instance and save layer0
scraper.exit()
user_base.save_users('output/layer0.json')
title('File Saved')

#Close the Scraper no matter if the script fails (atexit)
@atexit.register
def clean_exit():
    scraper.exit()
