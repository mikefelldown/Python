import arcpy
from xml.dom import minidom
import time, datetime

mygpx = arcpy.GetParameterAsText(0)
inFC = arcpy.GetParameterAsText(1)
samplerName = arcpy.GetParameterAsText(2)
propertyName = arcpy.GetParameterAsText(4)

tzcorrection = time.timezone / 86400.0

myxml = minidom.parse(mygpx)

spatialRef = arcpy.SpatialReference(r"C:\Program Files (x86)\ArcGIS\Desktop10.0\Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj")

wptList = myxml.getElementsByTagName("wpt")

rows = arcpy.InsertCursor(inFC, spatialRef)
checkrows = arcpy.SearchCursor(inFC)
sampleList = []

arcpy.SetProgressor("step", "Importing waypoints", 0, len(wptList), 1)

for checkrow in checkrows:
    sampleList.append(checkrow.SampleID)

del checkrow, checkrows    

def checkName(ident):
    if ident in sampleList:
        return False
    else:
        sampleList.append(ident)
        return True
    

for wpt in wptList:
    row = rows.newRow()
    pntName = wpt.getElementsByTagName("name")[0].firstChild.nodeValue
    if checkName(pntName[0:10]):
        row.SampleID = pntName[0:10].strip()
        pnt = arcpy.Point()
        lat = wpt.getAttribute("lat")
        lon = wpt.getAttribute("lon")
        pnt.Y = float(lat)
        pnt.X = float(lon)
        elevation = wpt.getElementsByTagName("ele")
        pnt.Z = float(elevation[0].firstChild.nodeValue)
        row.Shape = pnt
        row.Prospector = samplerName
        row.Property = propertyName
        pointDate = datetime.datetime.strptime(wpt.getElementsByTagName("time")[0].firstChild.nodeValue, '%Y-%m-%dT%H:%M:%SZ') - datetime.timedelta(tzcorrection)
        row.SampleDate = pointDate
        rows.insertRow(row)
        arcpy.SetProgressorPosition()
    else:
        arcpy.AddError("Sample number " + pntName + " has already been used.")
        arcpy.SetProgressorPosition()
        
    
del row, rows
arcpy.ResetProgressor()

# update UTM coords

rows = arcpy.UpdateCursor(inFC)

for row in rows:
    feat = row.getValue("Shape")
    pnt = feat.getPart()
    row.UTM_E = pnt.X
    row.UTM_N = pnt.Y
    row.Elevation = pnt.Z
    rows.updateRow(row)

del row, rows

arcpy.RefreshActiveView()



    
