"""N O T E B O O K"""

from collections import UserDict, UserString
from information import start_info_nb, help_info_nb
from prettytable import PrettyTable
from prompt_tool_nb import Completer, RainbowLexer
from prompt_toolkit import prompt
import pickle

filename = "notebook.bin"


class NoteBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, n=1):
        index = 1
        print_block = '-' * 100 + '\n'
        for record in self.data.values():
            print_block += str(record) + '\n'
            if index < n:
                index += 1
            else:
                yield print_block
                index, print_block = 1, '-' * 100 + '\n'
        yield print_block


class Filed:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"{self.value}"


class Name(Filed):
    pass


class Note(Filed):
    pass


class Tag(Filed):
    pass


class Record:

    def __init__(self, name, *notes):
        self.name = name
        self.notes = list(notes)
        self.tags = "-"

    def __repr__(self):
        return f'Title: {self.name}, Notes: {self.notes}, Tags: {self.tags}'

    def add_title(self, name):
        self.name = name

    def add_note(self, notes):
        self.notes.append(notes)

    def add_tag(self, tags):
        self.tags = tags


def decor_error(func):
    """Decorator for handling exceptions """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return f"{chr(128679)} IndexError..."
        except KeyError:
            return f"{chr(128679)} KeyError..."
        except ValueError:
            return f"{chr(128679)} ValueError..."
        except AttributeError:
            return f"{chr(128679)} AttributeError..."

    return wrapper


@decor_error
def hello(*args, **kwargs: NoteBook):
    return f"{chr(129299)} How can I help you?\n"


@decor_error
def add_note(*args, **kwargs: NoteBook):
    """Added note in notebook"""

    nb = kwargs.get('nb')
    name = Name(args[0])
    notes_row = " ".join(args[1:])
    notes = Note(notes_row)
    rec = nb.get(name.value)
    if rec:
        rec.add_note(notes.value)
    else:
        rec = Record(name, notes.value)
    nb.add_record(rec)
    return f"add Name: {name}, note: {notes}"


@decor_error
def del_note(*args, **kwargs: NoteBook):
    """Deletes note from notebook"""

    nb = kwargs.get('nb')
    name = Name(args[0])
    rec = nb.get(name.value)
    if rec:
        nb.pop(name.value)
        return f"{chr(9989)}Note {name} deleted {chr(10060)} "
    return f"{chr(10062)} Note {name} isn't in the NoteBook"


@decor_error
def add_tag(*args, **kwargs: NoteBook):
    """Added tag in note"""

    nb = kwargs.get('nb')
    name = Name(args[0])
    tags_row = ", ".join(args[1:])
    tags = Tag(tags_row)
    rec = nb.get(name.value)
    if rec:
        rec.add_tag(tags.value)
    else:
        return f"{chr(10062)} Note {name} isn't in the NoteBook"
    return f'Tag {tags} added in note {name}'


@decor_error
def find(*args, **kwargs: NoteBook):
    """Find notes that contain the specified text"""

    nb = kwargs.get('nb')
    sub = args[0]
    for value in nb.values():
        value = str(value)
        if sub.lower() in value.lower():
            print(f'{"-" * 80}\n{value}')
        if not value:
            return f"{chr(10062)} {sub} not in notebook"
    return f'{"-" * 80}\nOn >{sub}<, found the following notes'


@decor_error
def show_all(*args, **kwargs: NoteBook):
    """Display the contents of a NoteBook"""

    nb = kwargs.get('nb')
    x = PrettyTable()
    x.align = 'l'
    for i in nb.values():
        x.field_names = ['Names', 'Notes', 'Tags']
        x.add_row([i.name, "\n".join(i.notes), i.tags])
    return x


def exit_save_change(nb: NoteBook):
    """Request to save information"""

    while True:
        user_input_save = input(f"{chr(128221)}Save change? y/n: ")
        if user_input_save == "y":
            save_to_file(nb)
            break
        elif user_input_save == "n":
            break
        else:
            continue
    print(f"{chr(128075)} Good bye!")


def save_to_file(nb):
    """Save notes to the file"""

    with open(filename, "wb") as fh:
        pickle.dump(nb, fh)
        print(f"{chr(9989)} Notes saved in file")


def read_from_file():
    """Uploading data from a file"""

    try:
        with open(filename, "rb") as fh:
            return pickle.load(fh)
    except FileNotFoundError:
        return NoteBook()


"""Dictionary with commands(key - function: value - command)"""

COMMANDS = {
    hello: "hello",
    add_note: "add",
    del_note: "del",
    add_tag: "tag",
    find: "find",
    show_all: "show",
    help_info_nb: "info"
}


def parser_command(user_input: str):
    """The function parses the string entered by the user, splits it into a command and other arguments"""

    for command, key_word in COMMANDS.items():
        if user_input.lower().split()[0] == key_word:
            return command, user_input.replace(key_word, "").strip().split()
    return None, None


def main():
    """Main function"""

    print(start_info_nb())
    nb = read_from_file()

    while True:
        user_input = prompt(f"\nEnter command {chr(10151) * 3} ", completer=Completer, lexer=RainbowLexer())
        if user_input:
            if user_input.lower() in ["close", "exit", "."]:
                exit_save_change(nb)
                break
            command, data = parser_command(user_input)
            if not command:
                print(f"\nSorry {chr(129400)}, I don't understand you!\n")
            else:
                print(command(*data, nb=nb))


if __name__ == "__main__":
    main()
