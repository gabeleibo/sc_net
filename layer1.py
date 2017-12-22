from models.scraper import Scraper
from models.user import Users, User
import atexit

def title(title):
    print('-'*10 + title + '-'*10)

#inictialize the working database/ Scraper and old database
user_base = Users()
prev_user_base = Users()

user_base.load_users('output/layer1.json')
prev_user_base.load_users('output/layer0.json')

scraper = Scraper()

# Go through each User in the Layer 0 database to analyize
for prev_user in prev_user_base.users:
    user = user_base.get(prev_user.href)
    # in case user was already deleted for being a celebrity
    if user == None:
        title(prev_user.user_name)
        title('Removed')
        continue

    title(user.user_name)
    # if they are Celebrities, remove them
    if user.is_celebrity():
        user_base.remove(user)
        title('Removed')
        continue
    # if they don't have follower/following counts, get them
    if not user.has_counts():
        print('Analyizing Counts...')
        counts = scraper.get_counts(user)
        user.set_counts(counts)
        print(counts)
        #if they are Celebrities, remove them
        if user.is_celebrity():
            user_base.remove(user)
            title('Removed')
            continue
    #Now that all Celebrities removed, get follower/followings list
    if not user.is_complete():
        #get the users followers and followings:
        print('Scraping followings...')
        followings = scraper.get_followings(user)
        print('Scraping followers...')
        followers= scraper.get_followers(user)

        #process followings
        title('Followings')
        user.followings = user_base.process(scraper, followings)

        #process followers
        title('Followers')
        user.followers = user_base.process(scraper, followers)

    user_base.save_users('output/layer1.json')
    title('Complete')

#Close the Scraper no matter if the script fails (atexit)
@atexit.register
def clean_exit():
    scraper.exit()
