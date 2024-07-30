#!/usr/bin/env python3
"""
Module for the HBNBCommand console.
"""
import cmd
import re
import shlex
import ast
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City


def parse_curly_braces(arg):
    """
    Parses the curly braces for the update command.
    """
    braces_content = re.search(r"\{(.*?)\}", arg)

    if braces_content:
        id_with_comma = shlex.split(arg[:braces_content.span()[0]])
        obj_id = [i.strip(",") for i in id_with_comma][0]

        data_str = braces_content.group(1)
        try:
            parsed_dict = ast.literal_eval("{" + data_str + "}")
        except Exception:
            print("** invalid dictionary format **")
            return
        return obj_id, parsed_dict
    else:
        parts = arg.split(",")
        if parts:
            try:
                obj_id = parts[0]
            except Exception:
                return "", ""
            try:
                attr_name = parts[1]
            except Exception:
                return obj_id, ""
            try:
                attr_value = parts[2]
            except Exception:
                return obj_id, attr_name
            return f"{obj_id}", f"{attr_name} {attr_value}"

class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand console class for interactive command line.
    """
    prompt = "(hbnb) "
    valid_classes = ["BaseModel", "User", "Amenity", "Place", "Review", "State", "City"]

    def emptyline(self):
        """
        Do nothing on receiving an empty line.
        """
        pass

    def do_EOF(self, arg):
        """
        Handle EOF (Ctrl+D) to exit the program.
        """
        return True

    def do_quit(self, arg):
        """
        Quit command to exit the program.
        """
        return True

    def do_create(self, arg):
        """
        Create a new instance of BaseModel and save it to the JSON file.
        Usage: create <class_name>
        """
        try:
            class_name = arg.split(" ")[0]
            if len(class_name) == 0:
                print("** class name missing **")
                return
            if class_name and class_name not in self.valid_classes:
                print("** class doesn't exist **")
                return

            kwargs = {}
            commands = arg.split(" ")
            for i in range(1, len(commands)):
                key = commands[i].split("=")[0]
                value = commands[i].split("=")[1]
                if value.startswith('"'):
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = value

            if kwargs == {}:
                new_instance = eval(class_name)()
            else:
                new_instance = eval(class_name)(**kwargs)
            storage.new(new_instance)
            print(new_instance.id)
            storage.save()
        except ValueError:
            print(ValueError)
            return

    def do_show(self, arg):
        """
        Show the string representation of an instance.
        Usage: show <class_name> <id>
        """
        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(commands[0], commands[1])
            if key in objects:
                print(objects[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """
        Delete an instance based on the class name and id.
        Usage: destroy <class_name> <id>
        """
        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(commands[0], commands[1])
            if key in objects:
                del objects[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """
        Print the string representation of all instances or a specific class.
        Usage: <User>.all()
               <User>.show()
        """
        objects = storage.all()
        commands = shlex.split(arg)

        if len(commands) == 0:
            for key, value in objects.items():
                print(str(value))
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            for key, value in objects.items():
                if key.split('.')[0] == commands[0]:
                    print(str(value))

    def do_count(self, arg):
        """
        Counts and retrieves the number of instances of a class.
        Usage: <class name>.count()
        """
        objects = storage.all()
        commands = shlex.split(arg)

        if arg:
            class_name = commands[0]
        count = 0

        if commands:
            if class_name in self.valid_classes:
                for obj in objects.values():
                    if obj.__class__.__name__ == class_name:
                        count += 1
                print(count)
            else:
                print("** invalid class name **")
        else:
            print("** class name missing **")

    def do_update(self, arg):
        """
        Update an instance by adding or updating an attribute.
        Usage: update <class_name> <id> <attribute_name> "<attribute_value>"
        """
        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(commands[0], commands[1])
            if key not in objects:
                print("** no instance found **")
            elif len(commands) < 3:
                print("** attribute name missing **")
            elif len(commands) < 4:
                print("** value missing **")
            else:
                obj = objects[key]
                braces_content = re.search(r"\{(.*?)\}", arg)

                if braces_content:
                    try:
                        data_str = braces_content.group(1)
                        parsed_dict = ast.literal_eval("{" + data_str + "}")
                        attr_names = list(parsed_dict.keys())
                        attr_values = list(parsed_dict.values())

                        try:
                            setattr(obj, attr_names[0], attr_values[0])
                        except Exception:
                            pass
                        try:
                            setattr(obj, attr_names[1], attr_values[1])
                        except Exception:
                            pass
                    except Exception:
                        pass
                else:
                    attr_name = commands[2]
                    attr_value = commands[3]

                    try:
                        attr_value = eval(attr_value)
                    except Exception:
                        pass
                    setattr(obj, attr_name, attr_value)

                obj.save()

    def default(self, arg):
        """
        Default behavior for cmd module when input is invalid.
        """
        arg_list = arg.split('.')
        class_name = arg_list[0]
        command = arg_list[1].split('(')
        method = command[0]
        extra_arg = command[1].split(')')[0]

        method_dict = {
            'all': self.do_all,
            'show': self.do_show,
            'destroy': self.do_destroy,
            'update': self.do_update,
            'count': self.do_count
        }

        if method in method_dict.keys():
            if method != "update":
                return method_dict[method]("{} {}".format(class_name, extra_arg))
            else:
                if not class_name:
                    print("** class name missing **")
                    return
                try:
                    obj_id, arg_dict = parse_curly_braces(extra_arg)
                except Exception:
                    pass
                try:
                    return method_dict[method]("{} {} {}".format(class_name, obj_id, arg_dict))
                except Exception:
                    pass
        else:
            print("*** Unknown syntax: {}".format(arg))
            return False


if __name__ == '__main__':
    HBNBCommand().cmdloop()
