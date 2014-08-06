'''
Created on 9.6.2014

@author: A417280
'''
pozocode = {

# 000 - 020 error codes    
  'NOTOK' : 1,
  'OK': 0,
  'BADFORMAT': 2, 
  'BADTYPE': 3, 
  'OUTOFRANGE': 4, 

  'NULLPTR': 25,

# 021 - 050  

# 031 - 040  value types
  'INTEGER': 'I',
  'LONG': 'L',
  'DOUBLE': 'D',
  'FLOAT': 'F',
  'TIMEDATE': 'T',
  'NOTYPE':'N',
  'ERRORCODE':'E',
  'SENDER':'S',
  'COMMAND':'C',
  'BYTE':'B',
  'STRVALUE':'R',
  
  
# 100 - 199 commands

  'NOPE':100,      # no command - do nothing
  'SET_TIME':101,  # set time from seconds after epoch
  'PING':103,      # get response if alive
  'PONG':104,      # inform POZO ping response received successfully
  'FREERAM':105,    # get free ram of POZO
  'GETTIME':106,    # get system time of POZO
  
  'SETHIGH':107,    # set pin number N high
  'SETLOW':108,     # set pin number N low
  'GETPIN':109,     # get status of pin
  'SETBINARY':110,  # set all pins according BYTE  0 = low 1 = high
  'PINSTATUS':111,  # get pin status and remaining time, zero remaining time mean infinite 

  'GET1WNUM':120,   # get number of devices
  'READ1WNUM':121,  # read value from 1 wire device number ...
  'READ1WADDR':122, # read address of 1 wire device
  'READ1WTEMP':123, # read temperature of 1 wire device  
  
  
# 200 - 299 response codes

# 500 - 599 sender codes
  'OTHER':500,
  'JARDIN':501,
  'POZO':502,
  'PUENTE':503,
  }