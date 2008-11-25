TOP=../..
include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE

#----------------------------------------------------
#  Optimization of db files using dbst (DEFAULT: NO)
#DB_OPT = YES

#----------------------------------------------------
# In a Diamond IOC Application, build db files from
# template files like this
#
DB += example.db

USES_TEMPLATE += $(CRYOCONM14)/db/M32_system.template
USES_TEMPLATE += $(CRYOCONM14)/db/M32_sensor.template

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE
