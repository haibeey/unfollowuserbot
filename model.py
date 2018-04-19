from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer,ForeignKey,create_engine
from sqlalchemy.orm import relationship,sessionmaker
from session import session
from collections import Counter
from sqlalchemy.exc import IntegrityError

#my session object
S=session()
SESSION=S[0]
ENGINE=S[1]

class User(declarative_base()):
    __tablename__="user"
    id=Column(Integer,primary_key=True)
    screen_name=Column(String)
    user_id=Column(Integer)
    number_of_followers=Column(Integer,default=0)

    follower_id=Column(Integer,ForeignKey(id))
    follower=relationship("User")


    @classmethod
    def add_new_user(cls,screen_name,id,user_id):
        if not (cls.get_user(id) is None or \
            cls.get_user(user_id) is None or \
            cls.get_user(screen_name) is None):
            print("user present")
            return 
        user=User(screen_name=screen_name,id=id,user_id=user_id)
        SESSION.add(user)
        SESSION.commit()
        print("new user inserted")
    @classmethod
    def init_database_tables(cls):
        cls.metadata.create_all(ENGINE)
        print("table created")
    @classmethod
    def get_user(cls,id_screenname_userid):
        user=SESSION.query(cls).filter(cls.id==id_screenname_userid).first()
        if user:
            return user
        user=SESSION.query(cls).filter(cls.screen_name==id_screenname_userid).first()
        if user:
            return user
        user=SESSION.query(cls).filter(cls.user_id==id_screenname_userid).first()
        if user:
            return user
        return None
        
    def __repr__(self):
        return self.screen_name

    def remove_local_followers(self,container):
        if not isinstance(container,list):
            self.follower.remove(container)
            self.number_of_followers-=1
            SESSION.commit()
        else:
            for ex_friend in container:
                 self.follower.remove(ex_friend)
            self.number_of_followers-=len(container)
            SESSION.commit()
    def add_local_followers(self,container):
        if not isinstance(container,list):
            self.follower.append(container)
            self.number_of_followers+=1
            SESSION.commit()
        else:
            for ex_friend in container:
                new_user=User(id=ex_friend[0],user_id=ex_friend[1],screen_name=ex_friend[2])
                self.follower.append(new_user)
            self.number_of_followers+=len(container)
            SESSION.commit()

    def who_unfollow_me(self,current_followers,attribute="id"):
        assert hasattr(self,attribute),"model class User has no attribute : "+str(attribute)

        friends=self.follower
        current_followers={getattr(user,attribute):user for user in current_followers}

        who_unfollow_me=[]

        for user in friends:
            if not getattr(user,attribute) in current_followers:
                who_unfollow_me.append(user)

        self.remove_local_followers(who_unfollow_me)

        return who_unfollow_me

    def who_follow_me(self,current_followers,attribute="id"):
        assert hasattr(self,attribute),"model class User has no attribute : "+str(attribute)

        local_followers=self.follower
        
        friends={getattr(user,attribute):user for user in local_followers}

        who_follow_me=[]

        for user in current_followers:
            if getattr(user,attribute) not  in friends:
                who_follow_me.append((user.id,user.id,user.screen_name))
        self.add_local_followers(who_follow_me)

        return who_follow_me
    

if __name__=="__main__":
    #initialised the table
    user=User.init_database_tables()
    #user=User.get_user("handle")
    #print(user)
    #print(user.who_follow_me([]))