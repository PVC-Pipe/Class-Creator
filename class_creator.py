# class_creator.py
# By: BentoBot
# creates a class based off user inputs

import keyword
from collections import namedtuple
from textwrap import dedent

class_name = ""
# {field : type annotation}
fields = {}

def camel_to_snake(string: str) -> str:
    return "".join(["_" + c.lower() if c.isupper() else c for c in string]).strip("_")

def snake_to_pascal(string: str) -> str:
    return string.replace("_", " ").title().replace(" ", "")

while True:
    class_name = input("Input the name of the class (DO NOT input '_' to indicate private): ").strip()
    
    try:
        if not class_name.isidentifier() or keyword.iskeyword(class_name):
            raise IndexError

        first_letter = class_name[0]
        
        if not first_letter.isalpha():
            print("The class name must start with a letter.")
            raise IndexError

        elif first_letter.islower():
            yes_or_no = False
            while not yes_or_no:
                response = input("User classes should start with a capital letter. Do you want to capitalize the first letter? [y/n]: ").strip()
                if response.lower() == 'y':
                    class_name = class_name[0].upper() + class_name[1:]
                    yes_or_no = True
                elif response.lower() == 'n':
                    yes_or_no = True

        if class_name.find('_') != -1:
            yes_or_no = False
            while not yes_or_no:
                response = input("Classes should be PascalCase. Do you want to convert to PascalCase? [y/n]: ").strip()
                if response.lower() == 'y':
                    class_name = snake_to_pascal(class_name)
                    yes_or_no = True
                elif response.lower() == 'n':
                    yes_or_no = True
        
        yes_or_no = False
        while not yes_or_no:
            response = input("Is this class private? [y/n]: ").strip()
            if response.lower() == 'y':
                class_name = f"_{class_name}"
                yes_or_no = True
            elif response.lower() == 'n':
                yes_or_no = True

        valid_class = False
        yes_or_no = False
        while not yes_or_no:
            response = input(dedent(f"""\
                Your class is: `{class_name}`
                Is that correct? [y/n]: """)).strip()

            if response.lower() == 'y':
                valid_class = True
                yes_or_no = True
            elif response.lower() == 'n':
                yes_or_no = True

        if valid_class == True:
            break
    
    except IndexError:
        print("Input a valid class name.")
        pass

while True:
    try:
        all_fields = False
        yes_or_no = False
        while not yes_or_no:
            field_list = "\n".join([f"{k}: {v}" for k, v in fields.items()])

            response = input(str(
                "Current fields:\n"
                + field_list +
                "\n"
                "Do you want to input another field (ALL FIELDS WILL BE PRIVATE)? [y/n]: ")).strip()

            if response.lower() == 'y':
                yes_or_no = True
            elif response.lower() == 'n':
                all_fields = True
                yes_or_no = True

        if all_fields:
            break

        field = input("Input another field: ").strip()

        if not field.isidentifier() or keyword.iskeyword(field):
            raise IndexError

        first_letter = field[0]
        if not first_letter.isalpha():
            print("The field name must start with a letter.")
            raise IndexError

        elif first_letter.isupper():
            yes_or_no = False
            while not yes_or_no:
                response = input("Fields should start with a lowercase letter. Do you want to uncapitalize the first letter? [y/n]: ").strip()
                if response.lower() == 'y':
                    class_name[0].lower()
                    yes_or_no = True
                elif response.lower() == 'n':
                    yes_or_no = True

        if not field.islower():
            yes_or_no = False
            while not yes_or_no:
                response = input("Fields should be snake_case. Do you want to convert to snake_case? [y/n]: ").strip()
                if response.lower() == 'y':
                    field = camel_to_snake(field)
                    yes_or_no = True
                elif response.lower() == 'n':
                    yes_or_no = True

        field = f"_{field}"

        type_annotation = ""
        
        valid_type_annotation = False
        yes_or_no = False
        while not valid_type_annotation:
            type_annotation = input(f"Input a type annotation for {field}: ").strip()
            while not yes_or_no:
                response = input(f"You input `{type_annotation}` is this correct? [y/n]: ").strip()
                if response.lower() == 'y':
                    valid_type_annotation = True
                    yes_or_no = True
                elif response.lower() == 'n':
                    yes_or_no = True

        valid_field = False
        yes_or_no = False
        while not yes_or_no:
            response = input(dedent(f"""
                Does this field look correct?
                `{field}: {type_annotation}`
                [y/n]: """)).strip()
            if response.lower() == 'y':
                valid_field = True
                yes_or_no = True
            elif response.lower() == 'n':
                yes_or_no = True

        if valid_field:
            fields[field] = type_annotation

    except IndexError:
        print("Input a valid field name.")
        pass

Field = namedtuple('Field', 'annotation optional')

print("Declare each field as OPTIONAL OR NOT OPTIONAL:")
for k, v in fields.items():
    yes_or_no = False
    while not yes_or_no:
        response = input(f"Is `{k}: {v}` optional? [y/n]: ").strip()
        if response.lower() == 'y':
            fields[k] = Field(annotation=v, optional=True)
            yes_or_no = True
        elif response.lower() == 'n':
            fields[k] = Field(annotation=v, optional=False)
            yes_or_no = True

fourspace = "    "
eightspace = f"{fourspace}{fourspace}"
twelvespace = f"{eightspace}{fourspace}"
newline = "\n"
twonewline = "\n\n"

imports = {
    'List' : False,
    'Dict' : False,
    'Optional' : False
}
for v in fields.values():
    if 'List' in v.annotation:
        imports['List'] = True
    elif 'Dict' in v.annotation:
        imports['Dict'] = True
    if v.optional:
        imports['Optional'] = True

imports_list = [k for k, v in imports.items() if v]

imports_str = ""
if len(imports_list) > 0:
    imports_str = "from typing import " + ", ".join(imports_list) + "\n\n"

class_str = f"class {class_name}:"
annotations_str = "\n".join([f"{fourspace}{k}: {v.annotation}" for k, v in fields.items()])

fields_init_str = ", ".join([f"{k[1:]}: Optional[{v.annotation}] = None" if v.optional else f"{k[1:]}: {v.annotation}" for k, v in fields.items()])
init_str = f"{fourspace}def __init__(self, {fields_init_str})"

fields_dec_str = "\n".join([f"{eightspace}if {k[1:]} == None:{newline}{twelvespace}{k[1:]} = []{newline}{eightspace}self.{k} = {k[1:]}" if v.annotation.startswith("List") else f"{eightspace}if {k[1:]} == None:{newline}{twelvespace}{k[1:]} = {{}}{newline}{eightspace}self.{k} = {k[1:]}" if v.annotation.startswith("Dict") else f"{eightspace}self.{k} = {k[1:]}" for k, v in fields.items()])

properties_str = "\n\n".join([f"{fourspace}@property{newline}{fourspace}def {k[1:]}(self) -> {v.annotation}:{newline}{eightspace}return self.{k}{twonewline}{fourspace}@{k[1:]}.setter{newline}{fourspace}def {k[1:]}(self, {k[1:]}: {v.annotation}) -> None:{newline}{eightspace}self.{k[1:]} = {k[1:]}" for k, v in fields.items()])

doc_str = f"{imports_str}{class_str}{newline}{annotations_str}{twonewline}{init_str}{newline}{fields_dec_str}{twonewline}{properties_str}"

snake_class = camel_to_snake(class_name)

with open(f"{snake_class}.py", "w") as file:
    file.write(doc_str)

print(f"Your class is in the file `{snake_class}.py`")