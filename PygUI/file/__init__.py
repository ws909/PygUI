from enum import Enum as _Enum

"""
language = Norwegian
settings = local
users = 2
"""


class FileType(_Enum):
    PygUIsettings = "pyguisettings"
    txt = "txt"

    def __init__(self, *args):
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<FileType: %s>" % self


# Currently only set up for pyguisettings
def read(file: str, of_type: FileType or str) -> {str: str} or None or Exception:
    if isinstance(of_type, str):
        try:
            of_type = FileType(of_type)
        except ValueError:
            return None

    try:
        with open(file + "." + str(of_type.value)) as file:

            dictionary: {str: str} = {}

            for line in file:
                if not len(line) > 0:
                    continue

                line = line.strip("\n").replace(" ", "")

                key, value = line.split("=")
                dictionary[key] = value

            return dictionary

    except FileNotFoundError:
        return FileNotFoundError

    except ValueError:
        return ValueError


# Currently only set up for pyguisettings
def get(file: str, of_type: FileType or str, *content: str) -> {str: str} or None or Exception:
    if isinstance(of_type, str):
        try:
            of_type = FileType(of_type)
        except ValueError:
            return None

    try:
        with open(file + "." + str(of_type.value)) as file:

            dictionary: {str: str} = {}

            content = list(content)

            for line in file:
                if not len(line) > 0:
                    continue

                line = line.strip("\n").replace(" ", "")

                key, value = line.split("=")

                if key in content:
                    dictionary[key] = value

                    content.remove(key)

                    if len(content) == 0:
                        break

            return dictionary

    except FileNotFoundError:
        return FileNotFoundError

    except ValueError:
        return ValueError


# Currently only set up for pyguisettings
def overwrite(file: str, of_type: FileType or str, content: {str: str}) -> None or Exception:
    if isinstance(of_type, str):
        try:
            of_type = FileType(of_type)
        except ValueError:
            return

    try:
        file = open(file + "." + str(of_type.value), "w")

        line = ""

        for key, value in content.items():
            line += key + " = " + value + "\n"

        line = line[:-1]

        file.write(line)

    except FileNotFoundError:
        return

    except IOError:
        return

    finally:
        try:
            file.close()
        except AttributeError:
            pass


# Currently only set up for pyguisettings
def append(file: str, of_type: FileType or str, content: {str: str}) -> None or Exception:
    if isinstance(of_type, str):
        try:
            of_type = FileType(of_type)
        except ValueError:
            return

    try:
        with open(file + "." + str(of_type.value), "r") as r_file:
            lines = sum(1 for _ in r_file)

        with open(file + "." + str(of_type.value), "a") as file:

            line = ""

            for key, value in content.items():
                line += "\n" + key + " = " + value

            if lines == 0:
                line = line[1:]

            file.write(line)

    except FileNotFoundError:
        return


# Currently only set up for pyguisettings
def update(file: str, of_type: FileType or str, content: {str: str}) -> None or Exception:
    if isinstance(of_type, str):
        try:
            of_type = FileType(of_type)
        except ValueError:
            return

    try:
        file_name = file

        with open(file_name + "." + str(of_type.value), "r") as file:
            data = file.read()

        lines = data.split("\n")
        data = ""

        for line in lines:
            if not len(line) > 0:
                continue

            raw_line = line.replace(" ", "")
            key, value = raw_line.split("=")

            if key in content:
                value = content[key]
                content.pop(key)

                line = key + " = " + value

            data += line + "\n"

        data = data[:-1]

        with open(file_name + "." + str(of_type.value), "w") as file:
            file.write(data)

    except FileNotFoundError:
        return FileNotFoundError

    except ValueError:
        return ValueError


def read_1(file: str, of_type: FileType or str, content: [any]) -> {any: str} or None or Exception:
    if isinstance(of_type, str):
        try:
            of_type = FileType(of_type)
        except ValueError:
            return

    try:
        file_name = file

        with open(file_name + "." + str(of_type.value), "r") as file:
            data = file.read()

        lines = data.split("\n")
        data = {}

        index = 0

        for value in lines:

            if not value.__len__() > 0:
                continue

            data[content[index]] = value

            index += 1

        return data

    except FileNotFoundError:
        return FileNotFoundError

    except ValueError:
        return ValueError


class File:
    # Set up private properties, and public, computed properties for the file.

    @property
    def name(self) -> str:
        return self._name

    @property
    def extension(self) -> str:
        return self._type

    def __init__(self, file: str, of_type: FileType):
        self._name: str = file
        self._type: str = of_type.value


if __name__ == "__main__":
    update("test", FileType.PygUIsettings, {"S3": "Awesome"})
    print(get("test", FileType.PygUIsettings, "language", "S4"))
    print(read("test", FileType.PygUIsettings))
