import arcpy, math
from arcpy import da
from arcpy import mapping

arcpy.env.overwriteOutput = True

thismap = mapping.MapDocument("CURRENT")

df = mapping.ListDataFrames(thismap)

lyrs = mapping.ListLayers(df[0])


with da.SearchCursor("Sources",["TransferID"]) as rows:
    sources = list(set([r for r in rows]))
    for row in sources:
        arcpy.AddMessage(row[0])
        thismap.description = "Map No. " + row[0]
        source = da.SearchCursor("Sources",["TransferID","SourceID"], "\"TransferID\" = '" + row[0] + "'")
        src = ", ".join(["'" + str(int(s[1])) + "'" for s in source])
        lyrs[2].definitionQuery = "\"CLAIM_NUM\" in (" + src + ")"
        dest = da.SearchCursor("Destinations",["TransferID","DestinationID"], "\"TransferID\" = '" + row[0] + "'")
        des = ", ".join(["'" + str(int(s[1])) + "'" for s in dest])
        lyrs[0].definitionQuery = "\"CLAIM_NUM\" in (" + des + ")"
        arcpy.SelectLayerByAttribute_management(lyrs[0], "SWITCH_SELECTION")
        arcpy.SelectLayerByAttribute_management(lyrs[2], "SWITCH_SELECTION")
        lyrs[0].labelClasses[0].SQLQuery = "\"CLAIM_NUM\" not in (" + src +  ") or \"CLAIM_NUM\" is NULL"
        lyrs[1].labelClasses[0].SQLQuery = "\"CLAIM_NUM\" not in (" + src + ", " + des + ") or \"CLAIM_NUM\" is NULL"
        df[0].zoomToSelectedFeatures()
        if df[0].scale < 24000:
            df[0].scale = 24000
        else:
            df[0].scale = math.ceil(df[0].scale/1000) * 1000
        arcpy.SelectLayerByAttribute_management(lyrs[0], "CLEAR_SELECTION")
        arcpy.SelectLayerByAttribute_management(lyrs[2], "CLEAR_SELECTION")
        mapping.ExportToPDF(thismap, row[0] + ".pdf")
