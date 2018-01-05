from models.user import Users, User
import numpy as np

# initialize the database
user_base = Users()

# load in users - same for layer 0 or 1
user_base.load_users('output/layer1.json')

#collect the sums of each users follower and following counts
sums = []
for user in user_base.users:
    total_count = user.followers_count + user.followings_count
    sums.append(total_count)

print("Number of Nodes: " + str(len(sums)))
print("Mean Connections per Node: " + str(np.mean(sums)))
