'''
Created on 5.6.2014

@author: A417280
'''

# POZO Terminal - command prompt

import socket
import sys
import time
import re
import PozoCodes #@UnresolvedImport
import PozoCommand #@UnresolvedImport
import Queue

VERBOSE = 0
history = Queue.LifoQueue(20)

def millis():
    return int(round(time.time() * 1000))

def print_define(key, value): 
    print "#define {0:<10} {1}".format(key,value)

def print_define_char(key, value):
    print "#define {0:<10} \'{1}\'".format(key,value)

def print_define_str(key, value):
    print "#define {0:<10} \"{1}\"".format(key,value)


def pozo_commnad(socket):
    # create_message
    # send_message
    # get response
    # translate response
    # print response
    #     repeat above if required
    #     obey verbose
    return


    
def print_pozocode_h():
    print("/*")
    print("* PozoCodes.h")
    print("*")
    print("* Created on: {0}".format(time.strftime("%d/%m/%Y")))
    print("* Author: Norad Sparta")
    print("*/\n\n")
    print("#ifndef POZOCODES_H_")
    print("#define POZOCODES_H_")
    print("\n")
          
    for key, value in PozoCodes.pozocode.iteritems():
        if type(value) is int:
            print_define(key, value)
        elif type(value) is long:
            print_define(key, value)
        elif type(value) is str:
            if len(value) == 1:
                print_define_char(key, value)
        else:
            print_define_str(key, value)
                    
    print("\n\n#endif /* POZOCODES_H_ */")
      
def open_connection(host='192.168.0.15', port = 80):

    #create an INET, STREAMing socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print 'ERROR: Failed to create socket'
        sys.exit()
     
    if VERBOSE > 0:
        print 'Socket Created'
  
    try:
        remote_ip = socket.gethostbyname( host )
 
    except socket.gaierror:
        #could not resolve
        print 'ERROR Hostname could not be resolved. Exiting'
        sys.exit()
 
    #Connect to remote server
    s.connect((remote_ip , port))
 
    if VERBOSE > 0:
        print 'Socket Connected to ' + host + ' on ip ' + remote_ip
        
    return s



# creates command strip
# A[xxxx] where A is command code
# 
def cre_value_strip(cmd_name, value):
    return "{0}:{1}:".format(PozoCodes.pozocode.get(cmd_name),value)

def cre_long_strip(value):
    return "{0}:{1}:".format(PozoCodes.pozocode.get('LONG'),value)

def cre_double_strip(value):
    return "{0}:{1}:".format(PozoCodes.pozocode.get('DOUBLE'),value)

def cre_timedate_strip(value):
    return "{0}:{1}:".format(PozoCodes.pozocode.get('TIMEDATE'),value)

def cre_byte_strip(value):
    return "{0}:{1}:".format(PozoCodes.pozocode.get('BYTE'),int(value,2))
    
def cre_cmd_strip(cmd_name, value_name):
    return "{0}:{1}:".format(PozoCodes.pozocode.get(cmd_name),PozoCodes.pozocode.get(value_name))



def get_pozo_command(cmd,value_type,value):
    return "C{:0=4d}".format(PozoCodes.pozocode.get(cmd))
   
def novalue():
    return  "W:0:"

def pozo_ping():
    msg = cre_value_strip('SENDER','JARDIN')
    msg = msg + cre_cmd_strip('COMMAND','PING')
    return msg

def pozo_freeram():
    msg = cre_cmd_strip('SENDER','JARDIN')
    msg = msg + cre_cmd_strip('COMMAND','FREERAM')
    return msg
    
def pozo_full_freeram(s):
    msg = cre_cmd_strip('SENDER','JARDIN')
    msg = msg + cre_cmd_strip('COMMAND','FREERAM')
    print msg
    answ = send_msg(s, msg)
    answ = retrieve_reply_body( answ )
    pc = parse_answer(answ)
    print pc.value1
    return msg
    
    
def pozo_gettime():
    msg = cre_cmd_strip('SENDER','JARDIN')
    msg = msg + cre_cmd_strip('COMMAND','GETTIME')
    return msg

def pozo_pinstatus():
    msg = cre_cmd_strip('SENDER','JARDIN')
    msg = msg + cre_cmd_strip('COMMAND','PINSTATUS')
    return msg

   
def send_msg( msg ):
    s = open_connection()        

    #Send some data to remote server
    message = "GET " + "/" + msg + " HTTP/1.1\r\n\r\n"
    try :
        #Set the whole string
        s.sendall(message)
    except socket.error:
        #Send failed
        print 'ERROR: Send failed'
        sys.exit()
 
    if VERBOSE > 0:
        print 'Message send successfully'
 
    #Now receive data
    x = 100;
    while (x > 0):
        reply = s.recv(500)
        if (len(reply) > 0):
            break;
        x -= 1
    
    if VERBOSE > 0:
        print "X={0}".format(x)

    s.close()
                    
    return reply
   
   
   
def retrieve_reply_body( reply ):

    #retrieve message body from the response from Pozo
    pozoid = 'POZO/'
    idx = reply.find(pozoid)
    idx = idx + len(pozoid)
    msg_body = reply[idx:]
    if VERBOSE > 0:
        print msg_body
    return msg_body



def parse_answer(answr):
    pc = PozoCommand.PozoCommand()
    splited = re.split(":", answr)
    if VERBOSE > 0: 
        print splited   
    iscode = False;
    for x in splited:
        if (iscode == False):
            code = x
            iscode = True
        else:
            value = x
            iscode = False
            pc.store_code_value(code, value)

            if VERBOSE > 0: 
                print "CODE:{0}:VALUE:{1}".format(code, value)

    return pc

   
def pozo_settime(timedate):  
    msg = cre_cmd_strip('SENDER','JARDIN')
    msg = msg + cre_cmd_strip('COMMAND','SET_TIME')
    msg = msg + cre_timedate_strip(timedate)
    return msg
        
        
def pozo_full_ping():
    cmd = pozo_ping()
    startime = millis()
    answ = send_msg(cmd)
    delay = millis() - startime
    pc = parse_answer(retrieve_reply_body( answ ))
    if int(pc.command) == int(PozoCodes.pozocode.get('PING')):
        print 'POZO response in {0}ms'.format(delay)
    else:
        print 'unknown response'     
    
def pozo_full_gettime():
    cmd = pozo_gettime()
    if VERBOSE > 0: 
        print cmd
    answ = send_msg(cmd)
    answ = retrieve_reply_body( answ )
    if VERBOSE > 0: 
        print answ
    pc = parse_answer(str(answ)) 
    print time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(float(pc.value1)))


def pozo_full_pinstatus():
    cmd = pozo_pinstatus()
    if VERBOSE > 0: 
        print cmd
    answ = send_msg(cmd)
    answ = retrieve_reply_body( answ )
    if VERBOSE > 0: 
        print answ
    pc = parse_answer(str(answ)) 
    print "{0:07b}  {1}s".format(pc.value1, pc.value2)
  
def pozo_full_sethigh(pinnum):
    msg = cre_cmd_strip('SENDER','JARDIN')
    msg = msg + cre_cmd_strip('COMMAND','SETHIGH')
    msg = msg + cre_long_strip(pinnum)
    print "COMMAND: {0}".format(msg)        
    answ = send_msg(msg)
    answ = retrieve_reply_body( answ )
    ''' pc = parse_answer(answ) '''
    print "ANSWER: {0}".format(answ)        

def pozo_full_setlow(pinnum):
    msg = cre_cmd_strip('SENDER','JARDIN')
    msg = msg + cre_cmd_strip('COMMAND','SETLOW')
    msg = msg + cre_long_strip(pinnum)
    print "COMMAND: {0}".format(msg)        
    answ = send_msg(msg)
    answ = retrieve_reply_body( answ )
    print "ANSWER: {0}".format(answ)        


def pozo_full_get1wnum():
    msg = cre_cmd_strip('SENDER','JARDIN')
    msg = msg + cre_cmd_strip('COMMAND','GET1WNUM')
    print msg
    answ = send_msg(msg)
    answ = retrieve_reply_body( answ )
    pc = parse_answer(answ)   
    print pc.value1        


def pozo_full_read1wtemp(sensor):
    msg = cre_cmd_strip('SENDER','JARDIN')
    msg = msg + cre_cmd_strip('COMMAND','READ1WTEMP')
    msg = msg + cre_long_strip(sensor)
    print msg
    answ = send_msg(msg)
    answ = retrieve_reply_body( answ )
    pc = parse_answer(answ)   
    print pc.value1        


def pozo_full_read1waddr(sensor):
    msg = cre_cmd_strip('SENDER','JARDIN')
    msg = msg + cre_cmd_strip('COMMAND','READ1WADDR')
    msg = msg + cre_long_strip(sensor)
    print msg
    answ = send_msg(msg)
    answ = retrieve_reply_body( answ )
    pc = parse_answer(answ)   
    print pc.value1        


def pozo_full_setbinary(value, period = 60):
    msg = cre_cmd_strip('SENDER','JARDIN')
    msg = msg + cre_cmd_strip('COMMAND','SETBINARY')
    msg = msg + cre_byte_strip(value)
    msg = msg + cre_long_strip(period)
    print msg
    answ = send_msg(msg)
    answ = retrieve_reply_body( answ )
    pc = parse_answer(answ)   
    print pc.value1        


def pozo_help():
    pass


def execute_command(arg): 
    
    goahead = True                   
    if ("ping" in arg[0]):
        pozo_full_ping()
            
    elif ("freeram" in arg[0]):
        cmd = pozo_full_freeram()
        print cmd
        answ = send_msg(cmd)

    elif ("header" in arg[0]):
        print_pozocode_h()
        print "\n\n"
            
    elif ("settime" in arg[0]):
        cmd = pozo_settime(int(time.time()))
        print cmd
        answ = send_msg(cmd)
        print (answ)
            
    elif ("gettime" in arg[0]):
        pozo_full_gettime()
            
    elif ("sethigh" in arg[0]):
        if (len(arg)>1):
            for x in range(1, len(arg)):
                pozo_full_sethigh(arg[x])
                time.sleep(1)
        else:
            print ("too few parameters")    
    elif ("setlow" in arg[0]):
        if (len(arg)>1):
            for x in range(1, len(arg)):
                pozo_full_setlow(arg[x])
                time.sleep(1)
        else:
            print ("too few parameters")
            
    elif ("setbinary" in arg[0]):
        if (len(arg)<=1):
            print ("too few parameters")    
        elif(len(arg)==2):    
            pozo_full_setbinary(arg[1])
        else:
            pozo_full_setbinary(arg[1], arg[2])
                
    elif ("get1wnum" in arg[0]):
        pozo_full_get1wnum()
            
    elif ("read1wnum" in arg[0]):
        pozo_full_get1wnum()

    elif ("read1wtemp" in arg[0]):
        if (len(arg)>1):
            pozo_full_read1wtemp(arg[1])
        else: 
            ''' default is sensor number 1 '''
            pozo_full_read1wtemp(1)

    elif ("read1waddr" in arg[0]):
        if (len(arg)>1):
            pozo_full_read1waddr(arg[1])
        else: 
            ''' default is sensor number 1 '''
            pozo_full_read1waddr(1)
   
    elif ("pinstatus" in arg[0]):
        pozo_full_pinstatus()

    elif ("verbose" in arg[0]):
        VERBOSE = arg[1]


    elif ("help" in arg[0]):
            pass
    else:
        ''' not recognized command '''
        print ("pozo>?")
        
    return goahead;

    
prompt = 'pozo> '

def interactive():
    ''' control interactive command line mode '''
    goahead = True
    while(goahead):    
        ''' read user input ''' 
        user_input = raw_input(prompt)
        
        if ("last" in user_input):
            ''' if command is 'last' get last command from the queue '''
            user_input = history.get();
            ''' print out last command on the prompt '''
            print("{0}{1}", prompt, user_input )
        else:
            ''' ... else store command for history '''
            history.put(user_input)

        arg = user_input.split()

        
        if("quit" in arg[0]):
            print('bye!')
            goahead = False;
            
        elif("connect" in arg[0]):
            ''' second argument can be ip address '''
            if (len(arg)>1):
                ''' s = open_connection(arg[1]) '''
            else:
                ''' s = open_connection() '''
        else:
            
            goahead = execute_command(arg)

            
