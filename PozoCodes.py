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
  'NOTYPE':'0',
  'ERRORCODE':'E',
  'SENDER':'S',
  'COMMAND':'C',
  
# 100 - 199 commands

  'NOPE':100,      # no command - do nothing
  'SET_TIME':101,  # set time from seconds after epoch
  'PING':103,      # get response if alive
  'PONG':104,      # inform POZO ping response recieved succesfully
  'FREERAM':105,    # get free ram of POZO
  'GETTIME':106,    # get system time of POZO
  
  'SETHIGH':107,    # set pin number N high
  'SETLOW':108,     # set pin number N low
  'GETPIN':109,     # get status of pin

  'GET1WNUM':110,   # get number of devices
  'READ1WNUM':111,  # read value from 1 wire device number ...
  'READ1WADDR':112, # read address of 1 wire device
  'READ1WTEMP':113, # read temperature of 1 wire device  
  
  
# 200 - 299 response codes

# 500 - 599 sender codes
  'OTHER':500,
  'JARDIN':501,
  'POZO':502,
  'PUENTE':503,
  }