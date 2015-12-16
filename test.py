#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      mfell
#
# Created:     10/12/2015
# Copyright:   (c) Canadian Malartic Corporation 2015
# Licence:     007
#-------------------------------------------------------------------------------
import arcpy

x = arcpy.GetParameterAsText(0)

def main():
    if x == "":
        arcpy.AddMessage("HEllo")

if __name__ == '__main__':
    main()
