import arcpy
import numpy

mylayer = arcpy.GetParameterAsText(0)
outputworkspace = arcpy.GetParameterAsText(1) or r"C:\Users\mfell.QM\Documents\ArcGIS\Default.gdb"
desc = arcpy.Describe(mylayer)
shapeField = desc.ShapeFieldName
fields = [f.name for f in desc.Fields]
shapeIndex = fields.index(shapeField)
suffix = ""
arcpy.env.workspace = outputworkspace



while arcpy.Exists("%s_poly%s" % (mylayer, suffix)):
                   if suffix:
                       suffix = str(int(suffix) + 1)
                   else:
                       suffix = str(1)

outfcname = "%s_poly%s" %(mylayer, suffix)

outfc = arcpy.CreateFeatureclass_management(outputworkspace,outfcname,"POLYGON",mylayer,"DISABLED","DISABLED",desc.SpatialReference)

with arcpy.da.SearchCursor(mylayer,["SHAPE@"]) as rows:
    for row in rows:
        for part in row[0]:
            if not (part[0].X == part[part.count-1].X and part[0].Y == part[part.count-1].Y):
                part.add(part[0])
            with arcpy.da.InsertCursor(outfc,["SHAPE@"]) as ins:
                ins.insertRow([arcpy.Polygon(part)])



