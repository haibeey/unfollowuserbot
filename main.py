import tweepy
from config import CONSUMER_KEY,CONSUMER_SECRET,ACCESS_SECRET,ACCESS_TOKEN
from model import User


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

class main(object):
    def __init__(self,api):
        self.api=api

    def set_api(self,api):
        self.api=api

    def add_user_local(self,id_userid_handle):
        '''
        The adds a new  user to the local database,id_userid_handle can 
        either be the id or handle or user id or twitter id
        '''
        user=self.api.get_user(id_userid_handle)
        local_user=User.add_new_user(user.screen_name,user.id,user.id)
       
    

    def get_unfollowers(self,id_userid_handle):
        current_followers=[user  for user in self.api.get_user(id_userid_handle).followers()]
        local_user=User.get_user(id_userid_handle)

        unfollowed_user=local_user.who_unfollow_me(current_followers)
        
        return unfollowed_user

    def get_new_followers(self,id_userid_handle):
        current_followers=[user for user in self.api.get_user(id_userid_handle).followers()]
        local_user=User.get_user(id_userid_handle)

        followed_user=local_user.who_follow_me(current_followers)
        
        return followed_user

if __name__=="__main__":
    User.init_database_tables()
    m=main(api)
    me=api.me()
    m.add_user_local(me.id)
    print(m.get_unfollowers(me.id))
    