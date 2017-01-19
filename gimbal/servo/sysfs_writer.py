# -*- coding: utf-8 -*-

'''
Created on 06/04/2015

@author: david
'''
from os import system

class SysfsWriterFactory(object):
    """
    Creates SysfsWriter object
    """
    
    def create(self):
        """
        Creates writer
        """
        
        return SysfsWriter()
    

class SysfsWriter(object):
    """
    System filesystem's writer
    """
    
    @staticmethod
    def writeOnce(text, path):
        """
        Writes on any path immediately
        deprecated("Will be removed. Use 'object.setPath(\"path\").write(\"contents\").close()' instead")
        @param text: Contents as string
        @param path: filepath
        """
        
        system("echo {0} > {1}".format(text, path))
        

    def __init__(self):
        '''
        Constructor
        '''
        
        self._file = None
    
        
    def setPath(self, path):
        """
        Set filepath. Any write opperation will be performed on this path
        @param path: Filepath
        """
    
        if self._file and not self._file.closed:
            self._file.close()
    
        self._file = open(path, "a")
        
        return self
        
        
    def write(self, text):
        """
        Writes contents on the current path. It flushes immediately.
        If no path was previously set, an exception will be risen.
        @param text: Contents as string
        """
        
        self._file.write(text)
        self._file.flush()
        
        return self
    
        
    def close(self):
        """
        Closes the current path
        """
        
        if self._file and not self._file.closed:
            self._file.close()
        
        return self
    