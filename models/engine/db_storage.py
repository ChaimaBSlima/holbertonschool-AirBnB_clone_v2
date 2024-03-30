#!/usr/bin/python3
"""

"""
# handles the details of how to connect to the database and execute SQL commands
from sqlalchemy import create_engine
from os import getenv
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.exc import InvalidRequestError
from models.base_model import Base, BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """
    New engine DBStorage: (models/engine/db_storage.py)
    """
    __engine = None
    __session = None
    def __init__(self) -> None:
        username = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        database_name = getenv("HBNB_MYSQL_DB")
        database_url = "mysql+mysqldb://{}:{}@{}/{}".format(username,
                                                            password,
                                                            host,
                                                            database_name)
        self.__engine = create_engine(database_url, pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        query on the current database session
        (self.__session) all objects depending 
        of the class name (argument cls)
        """
        classes = [State, City, User, Place]
        if cls is None:
            obj = self.__session.query(State).all()
            for cls in classes:
                obj.extend(self.__session.query(cls).all())
        else:
            if isinstance(cls, str):
                cls = globals()[cls]  
            obj = self.__session.query(cls).all()
        return {"{}.{}".format(type(o).__name__, o.id): o for o in obj}

    
    def new(self, obj):
        """
        add the object to the current
        database session (self.__session)
        """
        obj1 = self.__session.merge(obj)
        self.__session.add(obj1)


    def save(self):
        """"
         commit all changes of the current
         database session (self.__session)
        """
        self.__session.commit()    

                
    def delete(self, obj=None):
        """ delete from the current database
        session obj if not None """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        "create all tables in the database (feature of SQLAlchemy) "
        Base.metadata.drop_all(self.__engine)
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
