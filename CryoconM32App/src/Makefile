TOP=../..

include $(TOP)/configure/CONFIG

# -------------------------------
# Build an Diamond Support Module
# -------------------------------

LIBRARY_IOC += CryoconM32

# CryoconM32.dbd will be installed into <top>/dbd
DBD += CryoconM32.dbd

# CryoconM32.dbd will be created from these files
CryoconM32_DBD += base.dbd
CryoconM32_DBD += asyn.dbd
CryoconM32_DBD += stream.dbd
CryoconM32_DBD += calcSupport.dbd

# CryoconM32_registerRecordDeviceDriver.cpp will be created
# CryoconM32.dbd
CryoconM32_SRCS += CryoconM32_registerRecordDeviceDriver.cpp

# These two lines are needed for non-vxWorks builds, such as Linux
#CryoconM32_SRCS_DEFAULT += CryoconM32Main.cpp
#CryoconM32_SRCS_vxWorks += -nil-

# Add locally compiled object code
#CryoconM32_SRCS +=

# The following adds object code from base/src/vxWorks
CryoconM32_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# This line says that this IOC Application depends on the
# xxx Support Module
#CryoconM32_LIBS += xxx

# We need to link this IOC Application against the EPICS Base libraries
CryoconM32_LIBS += $(EPICS_BASE_IOC_LIBS)

include $(TOP)/configure/RULES
