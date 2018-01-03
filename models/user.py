import json

class User:
    def __init__(self, user_name=None, href=None, followers = [],
     followings = [], follower_count = None, following_count = None):
        self.user_name = user_name
        self.href = href
        self.followers = followers
        self.followings = followings
        self.followers_count = follower_count
        self.followings_count = following_count

    def set_counts(self, counts):
        self.followers_count, self.followings_count = counts['followers_count'],\
        counts['followings_count']

    def get_followers(self):
        return self.followers

    def get_followings(self):
        return self.followings

    def get_friends(self):
        """Return friends - not to double count mutal followers/ings"""
        all_users = self.get_followings()

        for follower in self.get_followers():
            if follower not in all_users:
                all_users.append(follower)

        return all_users

    def has_counts(self):
        return self.followers_count != None and self.followings_count != None

    def is_complete(self):
        has_followers = len(self.followers) > 0 or self.followers_count == 0
        has_followings = len(self.followings) > 0 or self.followings_count == 0
        return has_followers and has_followings and self.has_counts()

    def is_celebrity(self):
        return (self.followers_count + self.followings_count) > 800

    def __str__(self):
        return str(self.__dict__)

class Users:
    def __init__(self):
        self.users=[]

    def load_users(self, file_name):

        def object_decoder(encoded_user):
            decoded_user = User()
            for option in encoded_user.keys():
                setattr(decoded_user, option, encoded_user[option])
            return decoded_user

        with open(file_name, 'r') as infile:
            self.users = json.load(infile, object_hook=object_decoder)

    def save_users(self, file_name):
        data = [user.__dict__ for user in self.users]
        with open(file_name, 'w') as outfile:
            json.dump(data, outfile)

    def add(self,user):
        self.users.append(user)

    def find(self, href):
        for index, user in enumerate(self.users):
            if user.href == href:
                return index
        return -1

    def get(self, href):
        index = self.find(href)
        if index > -1:
            return self.users[index]
        return None

    def get_all_hrefs(self):
        user_hrefs = []
        for user in self.users:
            user_hrefs.append(user.href)
        return user_hrefs

    def remove(self, user):
        index = self.find(user.href)
        if index > -1:
            return self.users.pop(index)
        else:
            raise IndexError('User index not found')

    def process(self, scraper, users):
        """ Takes the list of user information (scraper output)
         and converts it to User objects that are added to the
         database with their followers/following counts using
         the passed in scraper, the list of completed user users hrefs
         are returned """
        users_hrefs = []
        for user in users:
            #Try to find the user in the database to avoid replication
            user_name, href = user['user_name'], user['href']
            current = self.get(href)
            #if user is not found then create it
            if current is None:
                new_user = User(user_name,href)
                counts = scraper.get_counts(new_user)
                new_user.set_counts(counts)
                if new_user.is_celebrity():
                    continue
                self.add(new_user)
                print(new_user.user_name)
            users_hrefs.append(href)
        return users_hrefs
