import arcpy, pyodbc

arcpy.env.workspace = r"C:\Users\mfell\Documents\ArcGIS\Default.gdb"

search = arcpy.da.SearchCursor(r"C:\Users\mfell\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\gt_KL_Logger.sde\gt_KL_Logger.dbo.tblCoord",["idNuSondage","Coord3Est","Coord3Nord","Coord3Elev"])

local = arcpy.SpatialReference(r"C:\Users\mfell\Documents\ArcGIS\UC_Geology_Grid.prj")
nad83 = arcpy.SpatialReference(26917)

tempname = arcpy.CreateUniqueName("temp",arcpy.env.workspace)

temp = arcpy.CreateFeatureclass_management(arcpy.env.workspace,tempname.rsplit("\\",1)[1],"POINT","","DISABLED","ENABLED",local)

arcpy.AddField_management(temp,"id_key","LONG")

with arcpy.da.InsertCursor(temp,["SHAPE@","id_key"]) as ins:

    for row in search:
        if row[1] <> 0 and row[1] is not None:
            if row[3]:        
                elev = (row[3] + 2715.98) / 0.3048 if row[3] <> 0 else 0
            else:
                elev = 0
            pnt = arcpy.Point(row[1],row[2],elev)
            point = arcpy.PointGeometry(pnt,nad83)
            ins.insertRow([point,row[0]])

del search

'''sch = arcpy.da.SearchCursor(temp,["id_key","SHAPE@X","SHAPE@Y","SHAPE@Z"])
cnxn = pyodbc.connect('DSN=UpperCanada;TrustedConnection=yes')
cursor = cnxn.cursor()

for row in sch:
    cursor.execute("UPDATE tblcoordTest SET Coord1EST = %f, Coord1NORD = %f, Coord1ELEV = %f WHERE idKey=%s" % (row[1],row[2],row[3],row[0]))
    cursor.commit()

del row, sch
del cnxn
del cursor'''

#arcpy.Delete_management(temp)