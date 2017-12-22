from models.user import Users, User
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

# initialize the database
user_base = Users()

# load in users
user_base.load_users('output/layer0.json')
user = user_base.get('/gabeleibo')

# Get the follwer + following count for each User
amounts = []
for user in user.get_friends():
    current = user_base.get(user)
    amount = current.followers_count + current.followings_count
    amounts.append(amount)

# Histogram of the data
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
