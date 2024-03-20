#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime


Base = declarative_base()
class BaseModel:
    """A base class for all hbnb models"""
    
    id = ""
    created_at = datetime.utcnow()
    updated_at = datetime.utcnow()

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    setattr(self, key, datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f'))
                elif key != '__class__':
                    setattr(self, key, value)
        else:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            storage.new(self)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.save()
        storage.new(self)

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = self.__dict__.copy()
        dictionary.pop('_sa_instance_state', None)
        for key, value in dictionary.items():
            if isinstance(value, datetime):
                dictionary[key] = value.isoformat()
        dictionary['__class__'] = type(self).__name__
        return dictionary

    def delete(self):
        """Delete the current instance from storage"""
        from models import storage
        storage.delete(self)

class City(BaseModel):
    """City class"""
    __tablename__ = 'cities'
    
    name = ""
    state_id = ""

    def __init__(self, *args, **kwargs):
        """Instantiates a new city"""
        super().__init__(*args, **kwargs)
        if kwargs:
            self.name = kwargs.get('name', "")
            self.state_id = kwargs.get('state_id', "")

class State(BaseModel):
    """State class"""
    __tablename__ = 'states'
    
    name = ""

    def __init__(self, *args, **kwargs):
        """Instantiates a new state"""
        super().__init__(*args, **kwargs)
        if kwargs:
            self.name = kwargs.get('name', "")

            # For DBStorage
            if 'cities' in kwargs:
                self.cities = kwargs['cities']
            else:
                self.cities = []

    if storage_type == 'db':
        cities = relationship("City", backref="state",
                              cascade="all, delete-orphan")
    else:
        @property
        def cities(self):
            """Getter attribute that returns the list of City instances"""
            from models import storage
            city_list = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list