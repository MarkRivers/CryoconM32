from iocbuilder import Substitution
from iocbuilder.arginfo import *
from iocbuilder.modules.streamDevice import AutoProtocol
from iocbuilder.modules.asyn import AsynOctetInterface

class M32_system(Substitution, AutoProtocol):
    '''A brief description for this class goes here'''

    # The __init__ method specifies arguments and defaults
    def __init__(self, tctrlr, port, egu):
        # Filter the list of local variables by the argument list,
        # then initialise the super class
        self.__super.__init__(**filter_dict(locals(), self.Arguments))

    # __init__ arguments
    ArgInfo = makeArgInfo(__init__,
        tctrlr = Simple('Description for tctrlr', str),
        port   = Ident ('Asyn Port', AsynOctetInterface),
        egu    = Simple('Description for egu', str))

    # Substitution attributes
    TemplateFile = 'M32_system.template'
    Arguments = ArgInfo.Names()

    # AutoProtocol attributes
    ProtocolFiles = ['CryoconM32.protocol']


class M32_sensor(Substitution, AutoProtocol):
    '''A brief description for this class goes here'''

    # The __init__ method specifies arguments and defaults
    def __init__(self, record, device, sensor, port, egu, scan, adel, hihi, high, low, lolo, tctrlr, name = '', desc = '', gda = True):
        # If gda then define gda_name and gda_desc
        if gda:
            gda_name, gda_desc = name, desc
        else:
            gda_name, gda_desc = '', ''
        # Filter the list of local variables by the argument list,
        # then initialise the super class
        self.__super.__init__(**filter_dict(locals(), self.Arguments))

    # __init__ arguments
    ArgInfo = makeArgInfo(__init__,
        record = Simple('Description for record', str),
        device = Simple('Description for device', str),
        sensor = Simple('Description for sensor', str),
        port   = Ident ('Asyn Port', AsynOctetInterface),
        egu    = Simple('Description for egu', str),
        scan   = Simple('Description for scan', str),
        adel   = Simple('Description for adel', str),
        hihi   = Simple('Description for hihi', str),
        high   = Simple('Description for high', str),
        low    = Simple('Description for low', str),
        lolo   = Simple('Description for lolo', str),
        tctrlr = Simple('Description for tctrlr', str),
        name   = Simple('Object name, also used for gda_name if gda', str),
        desc   = Simple('Object description, also used for gda_desc if gda', str),
        gda    = Simple('Set to True to make available to gda', bool))

    # Substitution attributes
    TemplateFile = 'M32_sensor.template'
    Arguments = ArgInfo.Names()

    # AutoProtocol attributes
    ProtocolFiles = ['CryoconM32.protocol']


class M32_control(Substitution, AutoProtocol):
    '''A brief description for this class goes here'''

    # The __init__ method specifies arguments and defaults
    def __init__(self, tctrlr, loop, scan, port, rampratelim, name = '', desc = '', gda = True):
        # If gda then define gda_name and gda_desc
        if gda:
            gda_name, gda_desc = name, desc
        else:
            gda_name, gda_desc = '', ''
        # Filter the list of local variables by the argument list,
        # then initialise the super class
        self.__super.__init__(**filter_dict(locals(), self.Arguments))

    # __init__ arguments
    ArgInfo = makeArgInfo(__init__,
        tctrlr      = Simple('Description for tctrlr', str),
        loop        = Simple('Description for loop', str),
        scan        = Simple('Description for scan', str),
        port        = Ident ('Asyn Port', AsynOctetInterface),
        rampratelim = Simple('Description for rampratelim', str),
        name        = Simple('Object name, also used for gda_name if gda', str),
        desc        = Simple('Object description, also used for gda_desc if gda', str),
        gda         = Simple('Set to True to make available to gda', bool))

    # Substitution attributes
    TemplateFile = 'M32_control.template'
    Arguments = ArgInfo.Names()

    # AutoProtocol attributes
    ProtocolFiles = ['CryoconM32.protocol']


