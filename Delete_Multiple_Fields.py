import arcpy

layer = arcpy.GetParameterAsText(0)
fieldList = arcpy.GetParameterAsText(1).split(";")

for item in fieldList:
    arcpy.DeleteField_management(layer,item)

