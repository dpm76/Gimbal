'''
Created on 23/10/2015

@author: david
'''
from abc import ABCMeta

class I2CSensor(object):
    '''
    Abstract class for I2C sensors
    '''
    __metaclass__ = ABCMeta
    
    def _setAddress(self, address):
        
        self._address = address
        

    def _readWord(self, regH, regL):

        byteH = self._bus.read_byte_data(self._address, regH)
        byteL = self._bus.read_byte_data(self._address, regL)
    
        word = (byteH << 8) | byteL
        if (byteH & 0x80) != 0:
            word = -(0xffff - word + 1)
    
        return word
    

    def _readWordHL(self, reg):
    
        return self._readWord(reg, reg+1)
    

    def _readWordLH(self, reg):

        return self._readWord(reg+1, reg)
    

    def _writeWord(self, regH, regL, word):
    
        byteH = word >> 8
        byteL = word & 0xff
    
        self._bus.write_byte_data(self._address, regH, byteH)
        self._bus.write_byte_data(self._address, regL, byteL)


    def _writeWordHL(self, reg, word):
    
        self._writeWord(reg, reg+1, word)


    def _writeWordLH(self, reg, word):
    
        self._writeWord(reg+1, reg, word)

