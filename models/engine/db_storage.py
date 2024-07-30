#!/usr/bin/python3
"""Database storage engine module"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.place import place_amenity

class_mapping = {
    "User": User,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Place": Place,
    "Review": Review
}


class DBStorage:
    """DBStorage class to manage database storage using SQLAlchemy"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new DBStorage instance"""
        db_user = getenv('HBNB_MYSQL_USER')
        db_pwd = getenv('HBNB_MYSQL_PWD')
        db_host = getenv('HBNB_MYSQL_HOST')
        db_name = getenv('HBNB_MYSQL_DB')
        environment = getenv('HBNB_ENV')
        self.__engine = create_engine(
            f'mysql+mysqldb://{db_user}:{db_pwd}@{db_host}/{db_name}',
            pool_pre_ping=True
        )

        if environment == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects in the current session"""
        obj_dict = {}
        if cls is None:
            for class_type in class_mapping.values():
                objs = self.__session.query(class_type).all()
                for obj in objs:
                    key = f'{obj.__class__.__name__}.{obj.id}'
                    obj_dict[key] = obj
        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = f'{obj.__class__.__name__}.{obj.id}'
                obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """Add new object to the current session"""
        if obj:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as error:
                self.__session.rollback()
                raise error

    def save(self):
        """Commit all changes to the current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current session if not None"""
        if obj:
            self.__session.query(type(obj)).filter(
                type(obj).id == obj.id
            ).delete()

    def reload(self):
        """Reload the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        self.__session = scoped_session(session_factory)()

    def close(self):
        """Close the current SQLAlchemy session"""
        self.__session.close()
