# -*- coding: utf-8 -*-
#!/usr/bin/python

# PID controller example.

import socket
import time
import pid
import sys

# PID Configuration

#channel = 0 - tank 1,channel = 1 - tank 2
channel = 0
setPoint = float(sys.argv[1]) 

#process variable
pv = 0.0

#manipulated variable
mv = 0.0

integral_ = 0.0
sampleTime = 0.01

#e = sp - pv
error = setPoint-pv
errorPrevious = 0.0

#PID parameters
kp = 1.2
ki = 0.01
kd = 0.0001
kwd = 0.0

# Manipulated Variable
def setMV():
    global sock,mv
    msg = 'WRITE %d %f\n' % (channel, mv)
    sock.sendall(msg)
    ack = sock.recv(64)

# Process Variable
def getPV():
    global sock,pv
    try:
        msg = 'READ %d' % channel
        sock.sendall(msg)
        pv = float(sock.recv(64))*6.25
        print(pv)
    except socket.error, (value,message):
        sock.close()
        print "Error ao receber via socket. " + message
        connected = False

# Socket
ip = '192.168.1.39'
port = 20081
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    print "Conectado com o simulador!\n"
except socket.error, (value,message):
    sock.close()
    print "Erro ao abrir socket. " + message

while True: 
    integral_ = pid.integral(error,sampleTime,integral_,ki)
    mv = pid.pid(error,errorPrevious,sampleTime,integral_,kp,ki,kd)
    getPV()
    setMV()
    errorPrevious = error
    error = setPoint-pv
    time.sleep(0.1)

