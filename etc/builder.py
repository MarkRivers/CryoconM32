from iocbuilder import Substitution
from iocbuilder.arginfo import *
from iocbuilder.modules.streamDevice import AutoProtocol
from iocbuilder.modules.asyn import AsynOctetInterface
from iocbuilder.modules.calc import Calc

class CryoconM32(Substitution, AutoProtocol):
    '''CryoconM32 temperature controller device class (includes sensors and control loops configured with other classes).'''
    Dependencies = [Calc]

    # The __init__ method specifies arguments and defaults
    def __init__(self, tctrlr, port, egu="K"):
        # Filter the list of local variables by the argument list,
        # then initialise the super class
        self.__super.__init__(**filter_dict(locals(), self.Arguments))

    # __init__ arguments
    ArgInfo = makeArgInfo(__init__,
        tctrlr = Simple('The PV prefix for the temperature controller', str),
        port   = Ident ('Asyn Port', AsynOctetInterface),
        egu    = Simple('Engineering units for sink temperature', str))

    # Substitution attributes
    TemplateFile = 'M32_system.template'
    Arguments = ArgInfo.Names()

    # AutoProtocol attributes
    ProtocolFiles = ['CryoconM32.protocol']

class CryoconM32_sensor(Substitution):
    '''A sensor channel for the CryoconM32'''

    # The __init__ method specifies arguments and defaults
    def __init__(self, tctrlr, record, device, sensor, egu, adel, hihi, high, low, lolo, scan="2", name = '', desc = '', gda = True):
        # If gda then define gda_name and gda_desc
        if gda:
            gda_name, gda_desc = name, desc
        else:
            gda_name, gda_desc = '', ''
        # Grab Asyn port and temperature controller prefix from "owning" CryoconM32 object.
        port=tctrlr.args['port']
        tctrlr = tctrlr.args['tctrlr']
        # Filter the list of local variables by the argument list,
        # then initialise the super class
        self.__super.__init__(**filter_dict(locals(), self.Arguments))

    # __init__ arguments
    ArgInfo = makeArgInfo(__init__,
        tctrlr = Ident('CryoconM32 object', CryoconM32),
        record = Simple('Raw output suffix', str),
        device = Simple('Sensor output prefix', str),
        sensor = Choice('Sensor output suffix', ["A","B"]),
        egu    = Simple('Engineering units for the sensor output', str),
        adel   = Simple('Archive deadband increment', float),
        hihi   = Simple('hihi alarm for sensor reading', float),
        high   = Simple('high alarm for sensor reading', float),
        low    = Simple('low alarm for sensor reading', float) ,
        lolo   = Simple('lolo alarm for sensor reading', float),
        scan   = Simple('Scan rate, e.g. 2 or .1', str),
        name   = Simple('Object name, also used for gda_name if gda', str),
        desc   = Simple('Object description, also used for gda_desc if gda', str),
        gda    = Simple('Set to True to make available to gda', bool))

    # Substitution attributes
    TemplateFile = 'M32_sensor.template'
    Arguments = ArgInfo.Names() + ['port']

class CryoconM32_control(Substitution):
    '''A control loop for the CryoconM32'''

    # The __init__ method specifies arguments and defaults
    def __init__(self, tctrlr, loop, rampratelim, scan='2', name = '', desc = '', gda = True):
        # If gda then define gda_name and gda_desc
        if gda:
            gda_name, gda_desc = name, desc
        else:
            gda_name, gda_desc = '', ''

        port=tctrlr.args['port']
        tctrlr = tctrlr.args['tctrlr']

        # Filter the list of local variables by the argument list,
        # then initialise the super class
        self.__super.__init__(**filter_dict(locals(), self.Arguments))

    # __init__ arguments
    ArgInfo = makeArgInfo(__init__,
        tctrlr      = Ident('CryoconM32 object', CryoconM32),
        loop        = Choice('Loop number', [1,2]),
        rampratelim = Simple('Limit to the ramprate', float),
        scan        = Simple('Scan rate', str),
        name        = Simple('Object name, also used for gda_name if gda', str),
        desc        = Simple('Object description, also used for gda_desc if gda', str),
        gda         = Simple('Set to True to make available to gda', bool))

    # Substitution attributes
    TemplateFile = 'M32_control.template'
    Arguments = ArgInfo.Names() + ['port']

