from dataclasses import dataclass, field
from typing import Union
import pathlib
import os


DIR_PATH = pathlib.Path(__file__).parent.resolve()


@dataclass
class Folder:
    """ Folder item."""
    name: str
    contents: dict[str, Union['Folder', 'File']] = field(default_factory=dict)
    # the file path, making a list so its easy to hash into correct position
    uid: list[str] = field(default_factory=list)
    _size: int = 0

    @property
    def size(self) -> int:
        """ Returns the size of the folder"""
        # sum the size of all objects
        self._size = 0
        for content in self.contents.values():
            self._size += content.size
        return self._size

    def has_content(self, content_name: str, content_type: str = '') -> bool:
        """ Return True if the Folder has a specified File, else False """
        if content_name not in self.contents.keys():
            return False
        if content_type != '':
            if isinstance(self.contents[content_name]) != content_type:
                return False
        return True

    def add(self, content: Union['Folder', 'File']) -> None:
        """ Adds the given content to the Folder """
        content_type = type(content)
        content.uid = self.uid + [content.name]
        if self.has_content(content.name, content_type):
            pass
        self.contents[content.name] = content

    def remove(self, content_name) -> None:
        """ Adds the specified content to the Folder """
        if self.has_content(content_name):
            pass
        del self.contents[content_name]

    def __getitem__(self, name):
        return self.contents[name]

    def __iter__(self):
        return iter(self.contents.items())

    def __str__(self) -> str:
        msg = 'Folder(name={name},contents={contents}'
        return msg.format(name=self.name, contents=self.contents.values())


@dataclass
class File:
    """File item."""
    name: str
    size: int
    uid: list[str] = field(default_factory=list)  # unique identifier, the file_path


def find_command_indicies(data: list) -> list:
    """ get the indicies of all the commands in the input """
    i = 0
    command_indicies = []
    for line in data:
        line_elements = line.split(' ')
        if line_elements[0] == '$':
            command_indicies.append(i)
        i += 1
    return command_indicies


def create_file_system(data: list) -> Folder:
    """ Builds the filesystem from the input data"""
    command_indicies = find_command_indicies(data)

    # start with a filesystem containing root directory
    file_system = Folder(name='/', contents={}, uid=['/'])
    p_w_d = file_system.uid
    working_folder = file_system

    # construct the filesystem given the input
    for iter_index, command_index in enumerate(command_indicies):
        command_elements = data[command_index].split(' ')
        command = command_elements[1]

        # if there is an ls command we look for any new files or folders
        if command == 'ls':

            # get the indicies of the command output
            output_start = command_index + 1
            try:
                output_end = command_indicies[iter_index+1]
            except:
                output_end = len(data)
            output_range = range(output_start, output_end)

            # iterate over the outputs of the command
            for output_index in output_range:
                output_elements = data[output_index].split(' ')
                lead_element = output_elements[0]

                if lead_element == 'dir':
                    folder_name = output_elements[1]
                    # does nothing if already exists
                    working_folder.add(Folder(name=folder_name))

                else:  # must be a file
                    file_size, file_name = output_elements
                    # does nothing if the file already exists
                    working_folder.add(File(name=file_name, size=int(file_size)))

        # update the pwd based on cd command
        elif command == 'cd':

            # extract the input given to the cd command
            direction = command_elements[2]

            # go up the directory (..), down (any letter), or to root (/)
            if direction == '..':
                p_w_d.pop()
            elif direction == '/':
                p_w_d = ['/']
            else:
                p_w_d.append(direction)

        # move to the new working directory
        if p_w_d == ['/']:
            # special case for going to the root directory
            working_folder = file_system
        else:
            # find our place
            working_folder = file_system
            for level in p_w_d[1:]:
                working_folder = working_folder.contents[level]

    return file_system


def folder_traverse(folder: Folder, folder_sizes: dict[str, Folder]) -> dict[str, Folder]:
    """ Does the recursive traverse of a Folder """
    for _, subfolder in folder:
        if isinstance(subfolder, Folder):
            folder_sizes['/'.join(subfolder.uid)] = subfolder.size
            folder_sizes = folder_traverse(subfolder, folder_sizes)

    return folder_sizes


def get_folder_sizes(filesystem: Folder) -> dict[str, int]:
    """ Return the size of folders """
    folder_sizes = {}
    folder_sizes = folder_traverse(folder=filesystem, folder_sizes=folder_sizes)
    return folder_sizes


def part_1(folder_sizes: dict[str, int]) -> None:
    ''' Executes part 1 calculation'''
    threshold = 100000
    part_1_answer = 0
    for size in folder_sizes.values():
        if size <= threshold:
            part_1_answer += size

    return part_1_answer


def part_2(file_system: Folder, folder_sizes: dict[str, int]) -> int:
    ''' Executes part 2 calculation'''

    space_needed = 30000000
    total_space_available = 70000000

    total_used_space = file_system.size
    unused_space = total_space_available - total_used_space

    big_enough = []
    for size in folder_sizes.values():
        if (unused_space + size) >= space_needed:
            big_enough.append(size)
    part_2_answer = min(big_enough)

    return part_2_answer


if __name__ == "__main__":
    INPUT_FILE = 'input.txt'
    INPUT_PATH = os.path.join(DIR_PATH, INPUT_FILE)
    with open(INPUT_PATH, 'r') as f:
        data = f.read().splitlines()

    file_system = create_file_system(data)
    folder_sizes = get_folder_sizes(file_system)

    # part 1
    part_1_answer = part_1(folder_sizes)
    part_1_msg = "Sum of folder sizes that are smaller than 100,000: {answer}"
    print(part_1_msg.format(answer=part_1_answer))

    # part 2
    part_2_answer = part_2(file_system, folder_sizes)
    part_2_msg = "The smallest folder that can be deleted has a size of {answer}"
    print(part_2_msg.format(answer=part_2_answer))
