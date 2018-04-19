
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


class session:
    def __new__(self,path=None):
        #creates and configures  the engine
        if path is None:
            engine=create_engine("sqlite:///"+os.getcwd()+"/unfollowbot")
        else:
            engine=create_engine("sqlite:///"+path)

        Session=sessionmaker(bind=engine)
        session=Session()
        return session,engine