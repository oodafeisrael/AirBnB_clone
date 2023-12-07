#!/usr/bin/python3
import uuid
from datetime import datetime
import models


class BaseModel:
    """ parent class methods:"""

    def __init__(self, *args, **kwargs):
        """
           Initialize attributes

        """

        if kwargs:
            for key, val in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    val = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, val)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """Return class name, id, and dictionary"""

        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """
        update current datetime
        invoke save function
        & save to serialized file

        """

        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Return a dictionary of BaseModel and string formats of period"""

        obj_dict = self.__dict__.copy()
        obj_dict["__class__"] = self.__class__.__name__
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        return obj_dict
