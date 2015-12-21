#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mfell
#
# Created:     17/12/2015
# Copyright:   (c) Canadian Malartic Corporation 2015
# Licence:     007
#-------------------------------------------------------------------------------

import arcpy

fc = arcpy.GetParameterAsText(0)
targetfc = arcpy.GetParameterAsText(1)

def main():
    rows = arcpy.da.SearchCursor(fc,["SHAPE@"])
    ins = arcpy.da.InsertCursor(targetfc, ["SHAPE@"])
    for row in rows:

        pnt_array = arcpy.Array()
        factor = int(max(row[0].length/20, 10))

        for r in range(factor+1):
            nextpnt = row[0].positionAlongLine(float(r)/factor,"TRUE").getPart()
            pnt_array.append(nextpnt)
            #arcpy.AddMessage((r, nextpnt.X, nextpnt.Y))

##        if (pnt_array[0].X, pnt_array[0].Y) <> (pnt_array[len(pnt_array)-1].X, pnt_array[len(pnt_array)-1].Y):
##            arcpy.AddMessage("closing line")
##            pnt_array.append(pnt_array[0])

        pgon = arcpy.Polygon(pnt_array)
        ins.insertRow([pgon])
    del row, rows, ins

if __name__ == '__main__':
    desc = arcpy.Describe(fc)
    if desc.shapeType == "Polyline":
        main()
    else:
        arcpy.AddError("{0} is a {1} feature class.".format(fc, desc.shapeType))