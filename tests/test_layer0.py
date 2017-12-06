from sc_scrape import Scraper
from User import Users, User

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

user_base = Users()

user_base.load_users('layer0.json')


user = user_base.get('/gabeleibo')


all_users = user.get_followings()

for follower in user.get_followers():
    if follower not in all_users:
        all_users.append(follower)

amounts = []
for user in all_users:
    current = user_base.get(user)
    amount = current.followers_count + current.followings_count
    amounts.append(amount)



# histogram of the data
plt.hist(amounts, 25, facecolor='orange')
plt.xlabel('Total Followers/Followings')
plt.ylabel('Frequency')
plt.title('Histogram: Layer 0')
plt.axvline(800, color='red', linestyle ='--')
plt.text(730,10,'Cutoff: 800', rotation=90)
plt.text(1600,7,'"Celebrity Group"',color='blue')
plt.text(200,15,'"Friend Group"',color='blue')
plt.grid(True)
plt.show()
