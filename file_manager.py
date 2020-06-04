import os
import tempfile


class File:
    def __init__(self, file_path):
        self.__file_path = file_path
        if not os.path.exists(self.__file_path):
            with open(self.__file_path, "w"):
                pass
        self.__fd = open(self.__file_path, "r")
    
    def __str__(self):
        return self.__file_path

    def __iter__(self):
        return self
        
    def __next__(self):
        try:
            result = self.__fd.readline()
            if not len(result):
                raise StopIteration
            return result
        except EOFError:
            raise StopIteration
        
    def read(self):
        try:
            with open(self.__file_path, "r") as file:
                return file.read()
        except PermissionError:
            return ''

    def write(self, content):
        try:
            with open(self.__file_path, "w") as file:
                file.write(content)
        except PermissionError:
            pass

    def __add__(self, other):
        first_content = self.read()
        second_content = other.read()
        first_file_name = os.path.basename(self.__file_path)
        second_file_name = os.path.basename(other.__file_path)
        new_file_path = os.path.join(tempfile.gettempdir(), first_file_name + second_file_name)
        with open(new_file_path, "w") as file:
            file.write(first_content)
            file.write(second_content)
        return File(new_file_path)


if __name__ == "__main__":
    f = File("/home/igor/Projects/hello/.gitignore")
    for i in f:
        print(i.strip("\n"))
