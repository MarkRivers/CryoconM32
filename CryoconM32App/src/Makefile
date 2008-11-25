TOP=../..

include $(TOP)/configure/CONFIG

# -------------------------------
# Build an Diamond Support Module
# -------------------------------

LIBRARY_IOC += CryoconM14

# CryoconM14.dbd will be installed into <top>/dbd
DBD += CryoconM14.dbd

# CryoconM14.dbd will be created from these files
CryoconM14_DBD += base.dbd
#CryoconM14_DBD += asyn.dbd
#CryoconM14_DBD += stream.dbd

# CryoconM14_registerRecordDeviceDriver.cpp will be created
# CryoconM14.dbd
CryoconM14_SRCS += CryoconM14_registerRecordDeviceDriver.cpp

# These two lines are needed for non-vxWorks builds, such as Linux
#CryoconM14_SRCS_DEFAULT += CryoconM14Main.cpp
#CryoconM14_SRCS_vxWorks += -nil-

# Add locally compiled object code
#CryoconM14_SRCS +=

# The following adds object code from base/src/vxWorks
CryoconM14_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# This line says that this IOC Application depends on the
# xxx Support Module
#CryoconM14_LIBS += xxx

# We need to link this IOC Application against the EPICS Base libraries
CryoconM14_LIBS += $(EPICS_BASE_IOC_LIBS)

include $(TOP)/configure/RULES
