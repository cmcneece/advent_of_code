from dataclasses import dataclass
from typing import Union


@dataclass
class Folder:
    """ Folder item."""
    name: str
    _uid: list  # unique identified, the file_path
    contents: dict[str, Union['Folder', 'File']]  # itemname : Folder or File
    _size: int = 0

    @property
    def size(self) -> int:
        """ Returns the size of the folder"""
        # sum the size of all objects
        self._size = 0
        for content in self.contents.items():
            self._size += content.size
        return self._size

    def has_file(self, content_name) -> bool:
        """ Return True if the Folder has a specified File, else False """
        if content_name not in self.contents.keys():
            return False
        if isinstance(self.contents[content_name]) != File:
            return False
        return True

    def has_folder(self, content_name) -> bool:
        """ Return True if the Folder has a specified Folder, else False """
        if content_name not in self.contents.keys():
            return False
        if isinstance(self.contents[content_name]) != Folder:
            return False
        return True

    def add(self, content) -> None:
        """ Adds the give content to the Folder """
        if self.has_file(content.name) or self.has_folder(content.name):
            msg = 'Folder already has object {content_name}'
            Exception(msg.format(content_name=content.name))
        self.contents[content.name] = content

    def remove(self, content_name) -> None:
        """ Adds the specified content to the Folder """
        if self.has_file(content_name) or self.has_folder(content_name):
            msg = 'Folder does not have object {content_name}'
            Exception(msg.format(content_name=content_name))
        del self.contents[content_name]

    def keys(self):
        return self.contents.keys()

    def items(self):
        return self.contents.items()

    def values(self):
        return self.contents.values()

    def __getitem__(self, name):
        return self.contents[name]

    def __iter__(self):
        return iter(self.contents)

    def __str__(self) -> str:
        msg = 'Folder(name={name},contents={contents}'
        return msg.format(name=self.name, contents=self.contents.values())


@dataclass
class File:
    """File item."""
    name: str
    size: int
    _uid: list  # unique identified, the file_path


def find_command_indicies(data) -> list:
    """ get the indicies of all the commands in the input """
    i = 0
    command_indicies = []
    for line in data:
        line_elements = line.split(' ')
        if line_elements[0] == '$':
            command_indicies.append(i)
        i += 1
    return command_indicies


def create_file_system(data) -> Folder:
    """ Builds the filesystem from the input data"""
    command_indicies = find_command_indicies(data)

    # start with a filesystem containing root directory
    file_system = Folder(name='/', contents={}, _uid=['/'])
    p_w_d = file_system._uid
    working_folder = file_system

    # construct the filesystem given the input
    for iter_index, command_index in enumerate(command_indicies):
        line_elements = data[command_index].split(' ')
        command = line_elements[1]

        # if there is an ls command we look for any new files or folders
        if command == 'ls':

            # get the indicies of the command output
            if iter_index == len(command_indicies)-1:
                break
            output_range = range(command_index, command_indicies[iter_index+1])[1:]

            # iterate over the outputs of the command
            for output_index in output_range:
                output_elements = data[output_index].split(' ')

                lead_element = output_elements[0]

                if lead_element == 'dir':
                    folder_name = output_elements[1]
                    uid = p_w_d + [folder_name]

                    # if we have already seen the folder move on
                    if working_folder.has_folder(folder_name):
                        continue

                    # otherwise, create the folder
                    working_folder.add(Folder(name=folder_name, contents={}, _uid=uid))

                else:  # must be a file
                    file_name = output_elements[1]
                    file_size = output_elements[0]
                    uid = p_w_d + [folder_name]

                    # if we have already seen the file move on
                    if working_folder.has_file(file_name):
                        continue

                    # otherwise, create the file
                    working_folder.add(File(name=file_name, size=file_size, _uid=uid))

        # if there is a cd command we have to move to a different part of the folder structure
        elif command == 'cd':

            direction = line_elements[2]

            if direction == '..':
                p_w_d.pop()
            elif direction == '/':
                p_w_d = ['/']
            else:
                p_w_d.append(direction)

        if p_w_d == ['/']:
            # special case for going to the root directory
            working_folder = file_system      
        else:
            # find our place 
            working_folder = file_system
            for level in p_w_d[1:]:
                working_folder = working_folder.contents[level]

    return file_system


if __name__ == "__main__":
    input_path = 'test_input.txt'
    with open(input_path, 'r') as f:
        data = f.read().splitlines()

    file_system = create_file_system(data)

    print(file_system)
