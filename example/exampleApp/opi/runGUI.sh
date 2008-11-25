#!/bin/bash
. /home/tools/bin/changeports 6064
EDMDATAFILES=.:/dls_sw/work/R3.14.8.2/support/CryoconM32/data
#EDMDATAFILES=.:../../../CryoconM32App/opi/edl
export EDMDATAFILES
edm -x -eolc -m "tmon=TS-ID-TMON-01,device=TS-ID-TMON-01,record1=T1,record2=T2,record3=T3,record4=T4" M32.edl &

