#!/bin/bash
#
# Script test_CryoconM32_overview_embed_GUI.sh
#
# Runs the overview EDM screen for embedding for the Cryocon M32 
# temperature controller.
#

. /dls_sw/tools/bin/changeports 6064

edm -eolc -x -m "tctrlr=BL06J-EA-TCTL-01,device=BL06J-EA-TCTL-01,record1=T1,record2=T2" CryoconM32_overview_embed.edl&

exit
