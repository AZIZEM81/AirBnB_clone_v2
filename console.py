#!/usr/bin/python3
"""Console module for HBNB project"""
import cmd
import shlex
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """HBNB console"""
    prompt = '(hbnb) '
    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }

    def do_create(self, arg):
        """Create a new instance of a class"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        new_instance = self.classes[args[0]]()
        for param in args[1:]:
            try:
                key, value = param.split('=')
                value = value.strip('"')
                value = value.replace('_', ' ')
                if value.isdigit():
                    value = int(value)
                elif '.' in value and value.replace('.', '').isdigit():
                    value = float(value)
                setattr(new_instance, key, value)
            except ValueError:
                continue
        new_instance.save()
        print(new_instance.id)

    # ... (other console methods)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
