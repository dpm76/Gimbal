'''
Created on 19 ene. 2017

@author: david
'''

class SysfsWriterDummyFactory(object):
    """
    Creates SysfsWriterDummy object
    """
    
    def create(self):
        """
        Creates writer
        """
        
        return SysfsWriterDummy()


class SysfsWriterDummy(object):
    """
    System filesystem's writer dummy
    """

    def __init__(self):
        
        self._dummyFiles = {}
        self._workingFilePath = ""
        
        
    def setPath(self, path):
        """
        Set filepath. Any write opperation will be performed on this path
        @param path: Filepath
        """
        
        self._workingFilePath = path
        
        return self
        
        
    def write(self, text):
        """
        Writes contents on the current path. It flushes immediately.
        If no path was previously set, an exception will be raised.
        @param text: Contents as string
        """

        if self._workingFilePath:
            self._dummyFiles[self._workingFilePath] = text
        else:
            raise Exception("No working path set or file was closed.")
        
        return self
    
        
    def close(self):
        """
        Closes the current path
        """
        
        self._workingFilePath = ""
        
        return self
    
    
    def read(self, path):
        """
        Returns the contents of a path, or an exception raised if the path doesn't exist
        @param path: Filepath
        """
    
        if path in self._dummyFiles:
            contents = self._dummyFiles[path]
        else:
            raise Exception("The path '{0}' doesn\'t exist.".format(path))
        
        return contents 
    