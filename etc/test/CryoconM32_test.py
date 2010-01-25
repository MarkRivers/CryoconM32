#!/dls_sw/tools/bin/python2.4

# Test suite to use with pyUnit

from pkg_resources import require
require('dls.autotestframework')
from dls.autotestframework import *

################################################
# Test suite for the CryoconM32 temperature controller
    
class CryoconM32TestSuite(TestSuite):

    def createTests(self):
        # Define the targets for this test suite
        # The ioc has to be started with screen for the sake of interfacing with Hudson, the integration engine.
        # Something to do with what happens to the IOC stdin.
        Target("simulation", self,
            iocDirectory="iocs/example_sim",
            iocBootCmd="bin/linux-x86/stexample.sh",
            epicsDbFiles="db/example_expanded.db",
            runIocInScreenUnderHudson=True,   
#            simulationCmds=['python2.4 data/CryoconM32_sim.py'],
            simDevices=[SimDevice("SIM-TS-TCTRL-01", 9017, rpc=True)],
            guiCmds=['edm -m "P=SIM-EA-TCTRL-01,tctrlr=SIM-TS-TCTRL-01,device=SIM-TS-TCTRL-01,record1=T1,record2=T2" -eolc -x data/CryoconM32_detail.edl'])
        Target("hardware", self,
            iocDirectory="iocs/example",
            iocBootCmd="bin/linux-x86/stexample.sh",
            epicsDbFiles="db/example_expanded.db",
            guiCmds=['edm -m "P=SIM-TS-TCTRL-01,tctrlr=SIM-TS-TCTRL-01,device=SIM-TS-TCTRL-01,record1=T1,record2=T2" -eolc -x data/CryoconM32_detail.edl'])

        # The tests
        CaseIdentify(self)
        CaseChangeSetpoints(self)
        CaseChangePIDs(self)
        return

################################################
# Intermediate test case class that provides some utility functions
# for this suite

class CryoconM32Case(TestCase):
    # This arg_a is needed for the parent class constructor.
    def __init__(self, arg_a):
        '''Constructor.  First calls the base class constructor.'''
        TestCase.__init__(self , arg_a)
        self.pvPrefix = "SIM-TS-TCTRL-01:"
        return
        
    def dummy(self):
        ''' Dummy for now til I think of some common functions.
        '''
        return
    
################################################
# Test cases
#
# The EPICS implementation uses 3 templates.
# The tests are split up according to which template they are exercising.
#

# -----------------------------------------------
# System tests
class CaseIdentify( CryoconM32Case ):
    def runTest(self):
        '''Get the unit to identify itself.'''
        print "Model = " + self.getPv(self.pvPrefix + "SYS:MODEL")
        print "Hardware Revision = " + self.getPv(self.pvPrefix + "SYS:HWREV")
        print "Firmware Revision = " + self.getPv(self.pvPrefix + "SYS:FWREV")
        return
    
# -----------------------------------------------
# Control loop tests.
# Note control loop types in use restricted to PID and MAN but the real instrument
# supports other loop types.
class CaseChangeSetpoints( CryoconM32Case ):
    def changeLoopSetpoint(self, arg_loopID, arg_value):
        '''Change setpoint temperature (or other controlled output) on given control loop.'''
        print "changeLoopSetpoint: loopID = " + arg_loopID + " arg_value = " + str(arg_value)

        # Need a delta for accepting numeric comparison of PV float values.
        my_delta = 0.0001

        # Construct names of PVs to be used.
        my_demandPv = self.pvPrefix + "DMD:LOOP" + arg_loopID + ":SETPOINT"
        my_statusPv = self.pvPrefix + "STS:LOOP" + arg_loopID + ":SETPOINT"

        # Grab existing status value.
        my_before = self.getPv(my_statusPv)

        # Write new demand value and verify it was OK.
        self.putPv(my_demandPv , arg_value )
        self.verifyPvFloat(my_demandPv , arg_value , my_delta )

        # Wait for status to be updated and then verify the new status.
        self.sleep(2)
        my_after = self.verifyPvFloat(my_statusPv , arg_value , my_delta )
        print "changeLoopSetpoint: Setpoint changed from " + str(my_before) + " to " + str(my_after)
        return
    
    def runTest(self):
        '''Change the setpoint temperatures for both control loops.'''
        self.changeLoopSetpoint ( "1" , 3.5 )
        self.changeLoopSetpoint ( "2" , 9.0 )
        return

class CaseChangeManualOutputs( CryoconM32Case ):
    def changeLoopManualOutput(self, arg_loopID, arg_value):
        '''
        Change manual output request on given control loop.  Expect this test to work for all loop types.
        However it will only actually change the control loop output if the loop type is MAN for manual
        If the looptype is not MAN, the device is simply storing the parameter in case it is subsequently told to change the looptype to MAN.
        (Currently the EPICS database does not support setting the looptype as it is not wished to expose this functionality to the users).
        '''
        print "changeLoopManualOutput: loopID = " + arg_loopID + " arg_value = " + str(arg_value)

        # Need a delta for accepting numeric comparison of PV float values.
        my_delta = 0.0001

        # Construct names of PVs to be used.
        my_demandPv = self.pvPrefix + "DMD:LOOP" + arg_loopID + ":MANUAL"
        my_statusPv = self.pvPrefix + "STS:LOOP" + arg_loopID + ":MANUAL"
        my_looptypePv = self.pvPrefix + "STS:LOOP" + arg_loopID + ":LOOPTYPE"

        # Grab and report the looptype, which may well be important to understand what happens.
        my_looptype = self.getPv(my_looptypePv)
        print "changeLoopManualOutput: Loop type = " + my_looptype
        
        # Grab existing status value.
        my_before = self.getPv(my_statusPv)

        # Write new demand value and verify it was OK.
        self.putPv(my_demandPv , arg_value )
        self.verifyPvFloat(my_demandPv , arg_value , my_delta )

        # Wait for status to be updated and then verify the new status.
        self.sleep(2)
        my_after = self.verifyPvFloat(my_statusPv , arg_value , my_delta )

        print "changeLoopManualOutput: Manual output changed from " + str(my_before) + " to " + str(my_after)
        
        return

    def runTest(self):
        '''Change the manual output request for both control loops.'''
        self.changeLoopManualOutput( "1" , 7.3 )
        self.changeLoopManualOutput( "2" , 4.9 )
        
        return

class CaseChangePIDs ( CryoconM32Case ) :
    def changeLoopPID ( self , arg_loopID, arg_value_P , arg_value_I , arg_value_D ) :
        '''
        Change control loop PID parameters for given control loop.  Expect this test to work for all looptypes.
        However it will only actually change the control output if the loop type is PID.  If the looptype is not PID,
        the device is simply storing the parameters in case it is subsequently told to change the looptype to PID.
        (Currently the EPICS database does not support setting the looptype as it is not wished to expose this functionality to the users).
        '''

        print "changeLoopPID: loopID = " + arg_loopID + " arg_value_P = " + str(arg_value_P) + " arg_value_I = " + str(arg_value_I) + " arg_value_D = " + str(arg_value_D) 

        # Pug the 3 argument values in a lookup we can loop over.
        my_PIDs = { "P" : arg_value_P , "I" : arg_value_I , "D" : arg_value_D }

        # Need a delta for accepting numeric comparison of PV float values.
        my_delta = 0.0001

        # Construct names of loop type PV to be used.
        my_looptypePv = self.pvPrefix + "STS:LOOP" + arg_loopID + ":LOOPTYPE"

        # Grab and report the looptype, which may well be important to understand what happens.
        my_looptype = self.getPv(my_looptypePv)
        print "changeLoopPID: Loop type = " + my_looptype
        
        for my_key in my_PIDs.keys() :
            print "changeLoopPID: " + my_key + " gain"
            
            # Construct names of PVs to be used.
            my_demandPv = self.pvPrefix + "DMD:LOOP" + arg_loopID + ":" + my_key + "GAIN"
            my_statusPv = self.pvPrefix + "STS:LOOP" + arg_loopID + ":" + my_key + "GAIN"

            print "changeLoopPID: Demand PV = " + my_demandPv + " Status PV = " + my_statusPv 

            # Grab existing status value.
            my_before = self.getPv(my_statusPv)

            print "changeLoopPID: Existing value = " + str(my_before)

            # Write new demand value and verify it was OK.
            self.putPv(my_demandPv , my_PIDs[my_key] )
            self.verifyPvFloat(my_demandPv , my_PIDs[my_key] , my_delta )

            # Wait for status to be updated and then verify the new status.
            self.sleep(3)
            my_after = self.verifyPvFloat(my_statusPv , my_PIDs[my_key] , my_delta )

            print "changeLoopPID: " + my_key + " gain changed from " + str(my_before) + " to " + str(my_after)

        return

    def runTest(self):
        '''Change the PID parameters for both control loops.'''
        self.changeLoopPID( "1" , 2.57 , 1.8 , 0.02 )
        self.changeLoopPID( "2" , 3 , 2.2 , 0.0001 )
        return
    
# -----------------------------------------------
# Sensor channel tests.
#

################################################
# Main entry point

if __name__ == "__main__":
    # Create and run the test sequence
    CryoconM32TestSuite()

    
