'''
Created on 9.6.2014

@author: A417280
'''

import PozoCodes

class PozoCommand(object):
    '''
    classdocs
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
        self.sender = 501
        self.errorcode = 0
        self.command = 100
        self.value1 = 0
        self.value2 = 0
        self.numofvalues = 0
        self.timedate = 0

    # creates command strip
    # A[xxxx] where A is command code
    # 
    def cre_value_strip(self, cmd_name, value):
        return "{0}[{1}]".format(PozoCodes.pozocode.get(cmd_name),value)

    def cre_long_strip(self, value):
        return "{0}[{1}]".format(PozoCodes.pozocode.get('LONG'),value)

    def cre_byte_strip(self, value):
        return "{0}[{1}]".format(PozoCodes.pozocode.get('BYTE'),value)

    def cre_double_strip(self, value):
        return "{0}[{1}]".format(PozoCodes.pozocode.get('DOUBLE'),value)

    def cre_timedate_strip(self, value):
        return "{0}[{1}]".format(PozoCodes.pozocode.get('TIMEDATE'),value)


    def cre_cmd_strip(self, cmd_name, value_name):
        return "{0}[{1}]".format(PozoCodes.pozocode.get(cmd_name),PozoCodes.pozocode.get(value_name))

    def store_value(self,value):
        if (self.numofvalues == 0):
            self.value1 = value
            ++self.numofvalues
        if (self.numofvalues == 1):
            self.value2 = value
            ++self.numofvalues    

    def store_code_value(self, code, value):
        if (code == PozoCodes.pozocode.get('SENDER')):
            self.sender = value
        elif (code == PozoCodes.pozocode.get('ERRORCODE')):
            self.errorcode = value        
        elif (code == PozoCodes.pozocode.get('COMMAND')):
            self.command = int(value) 
        elif (code == PozoCodes.pozocode.get('INTEGER')):
            self.store_value(int(value))        
        elif (code == PozoCodes.pozocode.get('LONG')):
            self.store_value(value)        
        elif (code == PozoCodes.pozocode.get('FLOAT')):
            self.store_value(float(value))        
        elif (code == PozoCodes.pozocode.get('DOUBLE')):
            self.store_value(float(value))
        elif (code == PozoCodes.pozocode.get('TIME')):
            self.timedate = int(value) 
        elif (code == PozoCodes.pozocode.get('BYTE')):
            self.store_value(value)
        elif (code == PozoCodes.pozocode.get('STRVALUE')):
            self.store_value(value)
                                   

    # create_message
    # send_message
    # get response
    # translate response
    # print response
    #     repeat above if required
    #     obey verbose

    def pozo_gettime(self):
        msg = self.cre_cmd_strip('SENDER','JARDIN')
        msg = msg + self.cre_cmd_strip('COMMAND','GETTIME')
        return msg