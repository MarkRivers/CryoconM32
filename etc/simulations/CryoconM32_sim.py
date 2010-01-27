#!/bin/env python2.4
import time
from pkg_resources import require
require('dls_serial_sim')
from dls_serial_sim import serial_device
#from autotestframework import serial_device
import re, os

# This is a helper class.
# This is so we can instantiate 2 objects to match the 2 instantiations of the sensor template.
class Sensor(object):
    def __init__(self , arg_channel="A"):
        self.channel = arg_channel
        self.sensorRaw = 0.0034
        self.temp = 12.0
        self.tempUnits = "K"
        self.tempMin = 4.0
        self.tempMax = 324.0
        self.tempVariance = 3.152
        self.tempSlope = 0.051
        self.tempOffset = 288.0
        return

    def getChannel(self):
        return self.channel

    def getSensorRaw(self):
        return self.sensorRaw

    def getTemp(self):
        return self.temp
        
    def getTempUnits(self):
        return self.tempUnits

    def getTempMin(self):
        return self.tempMin

    def getTempMax(self):
        return self.tempMax

    def getTempVariance(self):
        return self.tempVariance

    def getTempSlope(self):
        return self.tempSlope

    def getTempOffset(self):
        return self.tempOffset

# Another Helper class. So we can instantiate 2 objects to match the 2 instantiations of the
# loop template.
class Loop(object):
    allowedLoopTypes = ['Off' , 'PID', 'Man' , 'Table' , 'RampP']
    
    def __init__(self, arg_loopID, arg_sensor):
        self.loopID = arg_loopID
        self.sensor = arg_sensor
        self.setpointT = 0.0
        self.loopType = "PID"
        self.loopRamp = "NO"
        self.loopRampRate = 100.0
        self.loopPGain = 2.5
        self.loopIGain = 10.0
        self.loopDGain = 0.0
        self.loopManOutput = 5.04
        return

    def getLoopID(self):
        return self.loopID

    def getLoopSource(self):
        return "CH" + self.sensor.getChannel()

    def getSetpointT(self):
        return self.setpointT

    def setSetpointT(self, arg_setpointT):
        self.setpointT = arg_setpointT
        return

    def getLoopType(self):
        return self.loopType

    def setLoopType(self, arg_loopType):
        if arg_loopType in Loop.allowedLoopTypes :
            # NOTE: This is a best guess what the behaviour is if you try to
            # set one of these when the Ramp status is not appropriate.
            if arg_loopType == "PID" and self.Ramp == "YES" :
                self.loopType = "RampP"
            elif arg_loopType == "RampP" and self.Ramp == "NO" :
                self.loopType = "PID"
            else :
                # This is what should happen most of the time, the normal case for an allowed loop type.
                self.loopType = arg_loopType
        else :
            # This not a valid loop type, but it does not normally generate an error, it is just ignored.
            if self.diagnosticLevel() > 1:
                print "CryocomM32_sim: Loop: setLoopType: argument" + arg_loopType + " not in allowed list of loop types " + Loop.allowedLoopTypes

        return

    def getLoopRampRate(self):
        return self.loopRampRate

    def setLoopRampRate(self, arg_loopRampRate):
        self.loopRampRate = arg_loopRampRate
        return

    def getLoopRamp(self):
        return self.loopRamp
# If ever we write a setLoopRamp function, it will have to interact with the loop type too.

    def getLoopPGain(self):
        return self.loopPGain

    def setLoopPGain(self, arg_loopPGain):
        self.loopPGain = arg_loopPGain
        return

    def getLoopIGain(self):
        return self.loopIGain

    def setLoopIGain(self, arg_loopIGain):
        self.loopIGain = arg_loopIGain
        return

    def getLoopDGain(self):
        return self.loopDGain

    def setLoopDGain(self, arg_loopDGain):
        self.loopDGain = arg_loopDGain
        return

    def getLoopManOutput(self):
        return self.loopManOutput
    
    def setLoopManOutput(self, arg_loopManOutput):
        self.loopManOutput = arg_loopManOutput
        return

class CryoconM32(serial_device):
    Terminator = "\n"
    
    def __init__(self):
        '''Constructor.  Remember to call the base class constructor.'''
        # See file CryoconM32.protocol for comment on what these functions do.
        serial_device.__init__(
            self,
            protocolBranches = ["getSensorraw" ,
                                "getTemp" ,
                                "getTempUnits" ,
                                "getTempMin" ,
                                "getTempMax" ,
                                "getTempVariance" ,
                                "getTempSlope" ,
                                "getTempOffset" ,
                                "getSetpointT" ,     "setSetpointT" ,
                                "getLoopType" ,      "setLoopType" ,
                                "getLoopSource" ,
                                "getLoopRamp" ,
                                "getLoopRampRate" ,  "setLoopRampRate" ,
                                "getLoopPGain" ,     "setLoopPGain" ,
                                "getLoopIGain" ,     "setLoopIGain" ,
                                "getLoopDGain" ,     "setLoopDGain" ,
                                "getLoopManOutput" , "setLoopManOutput" ,
                                "reseed" ,
                                "getFirmwareRev" ,
                                "getHardwareRev" ,
                                "getModel" ,
                                "getControllerName" ,
                                "getAmbientT" ,
                                "getSinkT" ,
                                "getStatsTime" ,
                                "resetStats" ,
                                "getFilterTC" ,
                                "getDisplayRes" ,
                                "getPUControl" ,
                                ])

        print "CryoconM32_sim: Initialising."
        self.on = 0

        self.channelA = Sensor("A")
        self.channelB = Sensor("B")
        self.channels = { "A" : self.channelA , "B" : self.channelB }
        
        self.loop1 = Loop("1", self.channelA)
        self.loop2 = Loop("2", self.channelB)
        self.loops = { "1" : self.loop1 , "2" : self.loop2 }
        
        self.firmwareRev = "Simulation XYZ"
        self.hardwareRev = "Simulation ABC"
        self.model = "CryoconM32"
        self.controllerName = "Magnet-22"
        self.ambientT = "+32C"
        self.sinkT = "+50C"
        self.calcStatsReset()
        
        print "CryoconM32_sim: Initialised."
        return

    def doReseed(self):
        self.covered("reseed")
        return
    
    def getFirmwareRev(self):
        self.covered("getFirmwareRev")
        return self.firmwareRev
    
    def getHardwareRev(self):
        self.covered("getHardwareRev")
        return self.hardwareRev

    def getModel(self):
        self.covered("getModel")
        return self.model

    def getControllerName(self):
        self.covered("getControllerName")
        return self.controllerName

    def getAmbientT(self):
        self.covered("getAmbientT")
        return self.ambientT
    
    def getSinkT(self):
        self.covered("getSinkT")
        return self.sinkT
    
    def calcStatsTime(self):
        self.statsTime = str(int(time.time() - self.statsTimeZero))
        return
    
    def getStatsTime(self):
        self.calcStatsTime()
        self.covered("getStatsTime")
        return self.statsTime

    def calcStatsReset(self):
        # This method is used both as part of object initialisation and to perform the reset on request.
        if self.diagnosticLevel() > 4:
            print "calcStatsReset: BEFORE: statsTimeZero = " + str(self.statsTimeZero) + ", statsTime = " + str(statsTime)

        # This is a floating point number.  Will need to be converted to report integer number of seconds.
        # It may or may not report whole seconds or fractions of seconds, not guaranteed from manual definition.
        self.statsTimeZero = time.time()
        self.statsTime = "0"
        if self.diagnosticLevel() > 4:
            print "calcStatsReset: AFTER: statsTimeZero = " + str(self.statsTimeZero) + ", statsTime = " + str(statsTime)

        return
    
    def doStatsReset(self):
        # This method is to handle a user instruction to reset.
        self.calcStatsReset()
        self.covered("resetStats")
        return
    
    def reply(self, arg_command):
        '''This function must be defined. It is called by the serial_sim system
        whenever an asyn command is send down the line. Must return a string
        with a response to the command or None.'''
        if self.diagnosticLevel() > 4:
            print "CryocomM32_sim: Received command " + arg_command
        result = None

        my_command = arg_command.strip()

        # Parse the command
        w = my_command.split()
        
        if len(w) == 0:
            if self.diagnosticLevel() > 1:
                print "CryoconM32_sim: Empty command string."
            return result

        query = my_command.endswith("?")

        my_word = w[0]

        if my_word.startswith("INP"):
            t = w[1].split(":")
            my_channel = t[0]
            my_sensor = self.channels[my_channel]

            if not my_sensor :
                if self.diagnosticLevel() > 2:
                    print "CryoconM32_sim: Invalid sensor channel " + my_channel + " in command " + my_command    
                    print "CryoconM32_sim: Allowed values: " + self.channels.keys()
            else :
                my_param = t[1].rstrip("?")

                if my_param == "SENPR" :
                    if query :
                        result = my_sensor.getSensorRaw()
                        self.covered("getSensorraw")
                        
                elif my_param == "TEMP" :
                    if query :
                        result = my_sensor.getTemp()
                        self.covered("getTemp")
            
                elif my_param == "UNITS" :
                    if query :
                        result = my_sensor.getTempUnits()
                        self.covered("getTempUnits")

                elif my_param == "MINIMUM" :
                    if query :
                       result = my_sensor.getTempMin()
                       self.covered("getTempMin")

                elif my_param == "MAXIMUM" :
                    if query :
                        result = my_sensor.getTempMax()
                        self.covered("getTempMax")

                elif my_param == "VARIANCE" :
                    if query :
                       result = my_sensor.getTempVariance()
                       self.covered("getTempVariance")
        
                elif my_param == "SLOPE" :
                    if query :
                        result = my_sensor.getTempSlope()
                        self.covered("getTempSlope")

                elif my_param == "OFFSET" :
                    if query :
                        result = my_sensor.getTempOffset()
                        self.covered("getTempOffset")
                else :
                    if self.diagnosticLevel() > 2:
                        print "CryoconM32_sim: no match to parameter " + my_param + " in word " + my_word + " in command " + my_command

        elif my_word.startswith("LOO"):
            t = w[1].split(":")
            my_loopID = t[0]
            my_loop = self.loops[my_loopID]
            if not my_loop :
                if self.diagnosticLevel() > 2:
                    print "CryoconM32_sim: Invalid control loop ID" + my_loopID + " in word " + my_word + " in command " + my_command
                    print "CryoconM32_sim: Allowed values: " + self.loops.keys()
            else :
                my_param = t[1].rstrip("?")
                if my_param == "SETPT" :
                    if query :
                        result = my_loop.getSetpointT()
                        self.covered("getSetpointT")
                    else :
                        my_value = float(w[2])
                        result = my_loop.setSetpointT(my_value)
                        self.covered("setSetpointT")
                elif my_param == "TYPE" :
                    if query :
                        result = my_loop.getLoopType()
                        self.covered("getLoopType")
                    else :
                        my_value = w[2]
                        result = my_loop.setLoopType(my_value)
                        self.covered("setLoopType")
                elif my_param == "SOURCE" :
                    if query :
                        result = my_loop.getLoopSource()
                        self.covered("getLoopSource")
                elif my_param == "RAMP" :
                    if query :
                        result = my_loop.getLoopRamp()
                        self.covered("getLoopRamp")
                elif my_param == "RATE" :
                    if query :
                        result = my_loop.getLoopRampRate()
                        self.covered("getLoopRampRate")
                    else :
                        my_value = float(w[2])
                        result = my_loop.setLoopRampRate(my_value)
                        self.covered("setLoopRampRate")
                elif my_param == "PGAIN" :
                    if query :
                        result = my_loop.getLoopPGain()
                        self.covered("getLoopPGain")
                    else :
                        my_value = float(w[2])
                        result = my_loop.setLoopPGain(my_value)
                        self.covered("setLoopPGain")
                elif my_param == "IGAIN" :
                    if query :
                        result = my_loop.getLoopIGain()
                        self.covered("getLoopIGain")
                    else :
                        my_value = float(w[2])
                        result = my_loop.setLoopIGain(my_value)
                        self.covered("setLoopIGain")
                elif my_param == "DGAIN" :
                    if query :
                        result = my_loop.getLoopDGain()
                        self.covered("getLoopDGain")
                    else :
                        my_value = float(w[2])
                        result = my_loop.setLoopDGain(my_value)
                        self.covered("setLoopDGain")
                elif my_param == "PMANUAL" :
                    if query :
                        result = my_loop.getLoopManOutput()
                        self.covered("getLoopManOutput")
                    else :
                        my_value = float(w[2])
                        result = my_loop.setLoopManOutput(my_value)
                        self.covered("setLoopManOutput")
                else :
                    if self.diagnosticLevel() > 2:
                        print "CryoconM32_sim: no match to parameter " + my_param + " in word " + my_word + " in command " + my_command

        elif my_word.startswith("SYS"):
            t = my_word.split(":")
            my_param = t[1]
            if my_param.startswith("RESEED"):
                if query :
                    if self.diagnosticLevel() > 2:
                        print "CryoconM32_sim: Unexpected question mark in command " + my_command    
                else :
                    result = self.doReseed()
            elif my_param.startswith("FWREV"):
                if query :
                    result = self.getFirmwareRev()
            elif my_param.startswith("HWREV"):
                if query :
                    result = self.getHardwareRev()
            elif my_param.startswith("NAME"):
                if query :
                    result = self.getControllerName()
            elif my_param.startswith("AMBIENT"):
                if query: 
                    result = self.getAmbientT()
            elif my_param.startswith("HTRST"):
                if query:
                    result = self.getSinkT()
            else :
                if self.diagnosticLevel() > 2:
                    print "CryoconM32_sim: no match to parameter " + my_param + " in word " + my_word + " in command " + my_command
        elif my_word.startswith("*IDN"):
            if query :
                result = self.getModel()
        elif my_word.startswith("STA"):
            t = my_word.split(":")
            my_param = t[1]
            if my_param.startswith("TIME"):
                if query :
                    result = self.getStatsTime()
            elif my_param.startswith("RESET"):
                if query :
                    if self.diagnosticLevel() > 2:
                        print "CryoconM32_sim: Unexpected question mark in command " + my_command    
                else :
                    result = self.doStatsReset()
            else :
                if self.diagnosticLevel() > 2:
                    print "CryoconM32_sim: no match to parameter " + my_param + " in word " + my_word + " in command " + my_command
        else :
            if self.diagnosticLevel() > 2:
                print "CryoconM32_sim: no match to command word " + my_word + " in command " + my_command
        
        if self.diagnosticLevel() > 4:
            print "CryoconM32: Returning result " + result
        if self.diagnosticLevel() > 2 and set:
            print "CryoconM32: Returning result " + result

        return result
                                        
    # This is the backdoor.
    def command(self, text):
        '''Interface function for commands from the test suite.'''
        return

    def initialise(self):
        '''Called by the framework when the power is switched on.'''
        self.on = 1

if __name__ == "__main__":
    # little test function that runs only when you run this file
    # Not used by built IOC
    dev = CryoconM32()
    dev.start_ip(9017)
    dev.start_debug(9018)
    # do a raw_input() to stop the program exiting immediately
    raw_input()
