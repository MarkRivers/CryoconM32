#!/bin/bash
#
# Script test_CryoconM32_detail_GUI.sh
#
# Runs the detail EDM screen for the Cryocon M32 temperature controller.
#

. /dls_sw/tools/bin/changeports 6064

edm -eolc -x -m "tctrlr=BL06J-EA-TCTL-01,device=BL06J-EA-TCTL-01,record1=T1,record2=T2" CryoconM32_detail.edl&

exit
