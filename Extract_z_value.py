import arcpy
import os

fc = arcpy.GetParameterAsText(0)
field = arcpy.GetParameterAsText(1)
raster = arcpy.GetParameterAsText(2)
workspace = os.path.dirname(fc)

def update_points():
    ed = arcpy.da.Editor(workspace)
    ed.startEditing()

    with arcpy.da.UpdateCursor(fc,["SHAPE@XY",field]) as upd:
        
        for p in upd: 
            z = arcpy.GetCellValue_management(raster,"{0} {1}".format(p[0][0], p[0][1]))
            p[1] = round(float(z[0]),1)
            upd.updateRow(p)

    ed.stopEditing(True)
    #del ed

if arcpy.Describe(fc).shapeType == "Point":
    update_points()
else:
    arcpy.AddError("The input feature class type must be point.")
    


