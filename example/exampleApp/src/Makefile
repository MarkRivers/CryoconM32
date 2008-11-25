TOP=../..

include $(TOP)/configure/CONFIG

# ------------------------
# Build an IOC Application
# ------------------------

-include $(STREAM)/StreamDevice/src/CONFIG_STREAM

PROD_IOC = example

# example.dbd will be installed into <top>/dbd
DBD += example.dbd

# example.dbd will be created from these files
example_DBD += base.dbd
example_DBD += utility.dbd
example_DBD += drvIpac.dbd
example_DBD += Hy8515.dbd
example_DBD += asyn.dbd
example_DBD += drvAsynSerialPort.dbd
example_DBD += stream.dbd
example_DBD += CryoconM14.dbd

# example_registerRecordDeviceDriver.cpp will be created
# example.dbd
example_SRCS += example_registerRecordDeviceDriver.cpp

# These two lines are needed for non-vxWorks builds, such as Linux
#example_SRCS_DEFAULT += exampleMain.cpp
#example_SRCS_vxWorks += -nil-

# Add locally compiled object code
#example_SRCS +=

# The following adds object code from base/src/vxWorks
example_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# This line says that this IOC Application depends on the
# xxx Support Module
example_LIBS += utility
example_LIBS += Ipac
example_LIBS += drvHy8515
example_LIBS += asyn
example_LIBS += stream
example_LIBS += pcre
example_LIBS += CryoconM14

# We need to link this IOC Application against the EPICS Base libraries
example_LIBS += $(EPICS_BASE_IOC_LIBS)

# ---------------------------------------------------
include $(TOP)/configure/RULES
