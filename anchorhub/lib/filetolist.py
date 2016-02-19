"""
Class for FileToList
"""


class FileToList(object):
    """
    FileToList is a helper class used to import text files and turn them into
    lists, with each index in the list representing a single line from the
    text file.
    """
    @staticmethod
    def to_list(file_path):
        """
        Static method. Takes in a file path, and outputs a list of stings.
        Each element in the list corresponds to a line in the file.
        :param file_path: string file path
        :return: A list of strings, with elements in the list corresponding
        to lines in the file pointed to in file_path
        """
        l = []
        f = open(file_path, 'r')
        for line in f:
            l.append(line)
        f.close()
        return l
