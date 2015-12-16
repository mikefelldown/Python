#-------------------------------------------------------------------------------
# Name:        Create Points at Intersections
# Purpose:
#
# Author:      mfell
#
# Created:     19/07/2015
# Copyright:   (c) Canadian Malartic Corporation 2015
# Licence:     007
#-------------------------------------------------------------------------------
import arcpy

infc = arcpy.GetParameterAsText(0)
outfc = arcpy.GetParameterAsText(1)

outfc = arcpy.ValidateTableName(outfc)


def main():
    rows = arcpy.da.SearchCursor(infc,["SHAPE@"])
    arcpy.CreateFeatureclass_management(arcpy.env.workspace,outfc,"POINT")
    lines = [row[0] for row in rows]
    arr = arcpy.Array()
    for l in lines:
        x = lines.pop(0)
        for j in lines:
            if not x.disjoint(j):
                pts = x.intersect(j, 1)
                for pt in pts:
                    ins = arcpy.da.InsertCursor(outfc,["SHAPE@"])
                    ins.insertRow([pt])
                    del ins
        else:
            continue
    del row, rows
    try:
        mxd = arcpy.mapping.MapDocument("CURRENT")
        fl = arcpy.MakeFeatureLayer_management(arcpy.env.workspace + r'\\'+ outfc, outfc)
        lyr = arcpy.mapping.Layer(outfc)
        arcpy.mapping.AddLayer(mxd.activeDataFrame, lyr)
    except:
        arcpy.AddMessage("nothing")
if __name__ == '__main__':
    main()
