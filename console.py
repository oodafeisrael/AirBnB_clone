#!/usr/bin/python3
import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models import storage
import cmd
import re


def parse_arguments(args):
    c_brc = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", args)
    brkts = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", args)
    if c_brc is None:
        if brkts is None:
            return [i.strip(",") for i in split(args)]
        else:
            tokens = split(args[:brkts.span()[0]])
            ret_list = [i.strip(",") for i in tokens]
            ret_list.append(brkts.group())
            return ret_list
    else:
        tokens = split(args[:c_brc.span()[0]])
        ret_list = [i.strip(",") for i in tokens]
        ret_list.append(c_brc.group())
        return ret_list


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "
    valid_classes = {
                "BaseModel",
                "User",
                "Place",
                "City",
                "State",
                "Amenity",
                "Review"}

    def do_quit(self, args):
        """Command to exit the program"""
        return True

    def do_EOF(self, args):
        """Exit the program"""
        print("\nExiting HBNBCommand. Goodbye!")
        return True

    def emptyline(self):
        """Do nothing on empty input line"""
        pass

    def default(self, args):
        """
        Default behavior for cmd module if input
        is invalid

        """
        self.prepro_cmd(args)

    def prepro_cmd(self, args):
        """Intercepts commands to test for class.syntax()"""
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", args)
        if not match:
            return args
        classname, method, args = match.groups()
        match_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if match_uid_and_args:
            uid = match_uid_and_args.group(1)
            attr_or_dict = match_uid_and_args.group(2)
        else:
            uid = args
            attr_or_dict = False

            attr_and_value = ""
        if method == "update" and attr_or_dict:
            match_dict = re.search('^({.*})$', attr_or_dict)
            if match_dict:
                self.update_dict(classname, uid, match_dict.group(1))
                return ""

                match_attr_and_value = re.search(
                  '^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
            if match_attr_and_value:
                attr_and_value = (match_attr_and_value.group(
                    1) or "") + " " + (
                      match_attr_and_value.group(2) or "")
        command = method + " " + classname + " " + uid + " " +
        attr_and_value
        self.onecmd(command)
        return command

    def do_create(self, args):
        """
        Creates a new instance of a Model, saves
        it (to the JSON file) and prints the id

        """

        try:
            if not args:
                raise SyntaxError()
            args_list = args.split(" ")

            kwargs = {}
            for i in range(1, len(args_list)):
                key, val = tuple(args_list[i].split("="))
                if val[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        val = eval(val)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = val

            if not kwargs:
                obj = eval(args_list[0])()
            else:
                obj = eval(args_list[0])(**kwargs)
                storage.new(obj)
            print(obj.id)
            obj.save()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, args):
        """Prints the string representation of an instance""".

        arg_list = parse_arguments(args)
        obj_dict = storage.all()
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.valid_classes:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(arg_list[0], arg_list[1])])

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id"""

        arg_list = parse_arguments(args)
        obj_dict = storage.all()
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.valid_classes:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in
        obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(arg_list[0], arg_list[1])]
            storage.save()

    def do_all(self, args):
        """
        Prints all string representation of
        all instances
        """
        arg_list = parse_arguments(args)
        if len(arg_list) > 0 and arg_list[0] not in
        HBNBCommand.valid_classes:
            print("** class doesn't exist **")
        else:
            obj_list = [str(obj) for obj in storage.all().values()
                        if len(arg_list) == 0 or arg_list[0] ==
                        obj.__class__.__name__]
            print(obj_list)

    def do_count(self, args):
        """Counts the instances of a class."""
        arg_list = parse_arguments(args)
        count = sum(1 for obj in storage.all().values()
                    if arg_list[0] == obj.__class__.__name__)
        print(count)

    def do_update(self, line):
        """Updates an instance by adding or updating attribute."""

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(rex, line)

        if not match:
            print("** invalid syntax for update **")
            return

        classname, uid, attribute, value = match.groups()

        if not classname:
            print("** class name missing **")
            return

        if classname not in storage.classes():
            print("** class doesn't exist **")
            return

        if uid is None:
            print("** instance id missing **")
            return

        key = f"{classname}.{uid}"

        if key not in storage.all():
            print("** no instance found **")
            return

        if attribute is None:
            print("** attribute name missing **")
            return

        if value is None:
            print("** value missing **")
            return

        value = value.replace('"', '')

        try:
            value = storage.attributes()[classname][attribute](value)
        except (KeyError, ValueError):
            pass

        setattr(storage.all()[key], attribute, value)
        storage.all()[key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
