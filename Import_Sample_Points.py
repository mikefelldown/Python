import arcpy, time
from xml.dom import minidom
import datetime as dt

arcpy.AddMessage("Osisko Prospecting Sample Importer")
arcpy.AddMessage("Fast and easy, just like you!")
arcpy.AddMessage("")
                 

arcpy.AddMessage("Loading sample points...")

sdePath = r"Database Connections\KL_Exploration.sde"
inFC = sdePath + r"\KL_Exploration.DBO.rock_samples"
otherpts = sdePath + "\KL_Exploration.DBO.other_waypoints"
mygpx = arcpy.GetParameterAsText(0)
sampler1Name = arcpy.GetParameterAsText(1)
sampler2Name = arcpy.GetParameterAsText(2)

tzcorrection = time.timezone / 86400.0 + (0.041666666666666664 * time.daylight)
#create Spatial Reference for WGS84 system
sr = arcpy.SpatialReference(4326)

propertyOutline = arcpy.da.SearchCursor(sdePath+ "\KL_Exploration.DBO.Property_Outline_WGS84","SHAPE@").next()
prop = propertyOutline[0]

myxml = minidom.parse(mygpx)
wptList = myxml.getElementsByTagName("wpt")

def checkName(ident):
    valid = False 
    checkrows = arcpy.da.SearchCursor(inFC,["SampleID"],"SampleID = '" + ident + "'")
    try:
        checkrow = checkrows.next()
        if checkrow:
            arcpy.AddError("Sample number " + ident + " has already been used.")        
    except StopIteration:
        if not ident[0].isalpha() or not ident[1:].isdigit() or len(ident) <> 7:
            arcpy.AddWarning("Sample number " + ident + " does not appear to be valid.")
        elif ident[-2:] in ('33','66','99'):
            arcpy.AddWarning("Sample number " + ident + " should have been a control sample.")
            valid = True
        else :
            valid = True
    finally:
        return valid

def translateDate(d):
    return d.replace("AOU","AUG")

arcpy.SetProgressor("step","Importing samples...",0,len(wptList),1)
sampleCount = 0

for wpt in wptList:
    pntName = wpt.getElementsByTagName("name")[0].firstChild.nodeValue
    arcpy.SetProgressorPosition()   
    SampleID = pntName[0:10].strip()
    pnt = arcpy.Point()
    pnt.Y = float(wpt.getAttribute("lat"))
    pnt.X = float(wpt.getAttribute("lon"))
    elevation = wpt.getElementsByTagName("ele") if "ele" in [node.nodeName for node in wpt.childNodes] else 0
    pnt.Z = elevation if type(elevation) == int else float(elevation[0].firstChild.nodeValue)
    geom = arcpy.Geometry("POINT",pnt,sr)
    onProp = prop.contains(geom)
    if wpt.getElementsByTagName("time"):
        pointDate = dt.datetime.strptime(wpt.getElementsByTagName("time")[0].firstChild.nodeValue, '%Y-%m-%dT%H:%M:%SZ') - datetime.timedelta(tzcorrection)
    elif wpt.getElementsByTagName("cmt")[0].firstChild.nodeValue.find("AM") > 0  or wpt.getElementsByTagName("cmt")[0].firstChild.nodeValue.find("PM") > 0:
        pdate = translateDate(wpt.getElementsByTagName("cmt")[0].firstChild.nodeValue)
        pointDate = dt.datetime.strptime(pdate, "%d-%b-%y %I:%M:%S%p")
    else:
        try:
            pointDate = dt.datetime.strptime(wpt.getElementsByTagName("cmt")[0].firstChild.nodeValue, "%d-%b-%y %H:%M:%S")
        except:
            continue
    SampleDate = pointDate   
    if checkName(pntName[0:10]):
        with arcpy.da.InsertCursor(inFC,["SHAPE@","SampleID","SampleDate","Prospector1","Prospector2","OnProperty"]) as rows:
            rows.insertRow([geom,SampleID,SampleDate,sampler1Name,sampler2Name,onProp])
            sampleCount += 1
    else:
        with arcpy.da.InsertCursor(otherpts,["SHAPE@","Waypoint_name","Waypoint_date","Prospector1","Prospector2","OnProperty"]) as rows:
            rows.insertRow([geom,SampleID,SampleDate,sampler1Name,sampler2Name,onProp])
            

# Update UTM coordinates
arcpy.AddMessage("Sample count: " + str(sampleCount))

arcpy.SetProgressor("default","Updating UTM coordinates...")

with arcpy.da.UpdateCursor(inFC,["SHAPE@","UTM_E","UTM_N","Elevation"],"UTM_E is NULL or UTM_N is NULL") as rows:

    for row in rows:
        feat = row[0].getPart()
        row[1] = feat.X
        row[2] = feat.Y
        row[3] = feat.Z
        rows.updateRow(row)

# Import tracks

current = arcpy.GetParameterAsText(3)
indate = arcpy.GetParameterAsText(4) if type(arcpy.GetParameter(4)) <> type(None) else dt.datetime.today()
if type(indate) == unicode:
    indate = dt.datetime.strptime(indate, "%d/%m/%Y %H:%M:%S %p")
    if indate.day < 13:
        indate = dt.date(indate.year,indate.day,indate.month)
tracklist = minidom.parse(current).getElementsByTagName("trk")
arcpy.SetProgressor("default","Importing tracks...")
for track in tracklist:
    title = track.getElementsByTagName("name")[0].firstChild.nodeValue
    title = translateDate(title)
    try:
        trackdate = dt.datetime.strptime(title,"Current Track: %d %b %Y %H:%M") if title.find("Current Track") > -1 else dt.datetime.strptime(title,"%d-%b-%y %H:%M:%S")
    except ValueError:
        trackdate = dt.datetime.strptime(track.getElementsByTagName("time")[0].firstChild.nodeValue,"%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(tzcorrection)
    if trackdate.year == indate.year and trackdate.month == indate.month and trackdate.day == indate.day:
        arcpy.AddMessage("SUCCESS!")
        nodes = arcpy.Array()
        trackpts = track.getElementsByTagName("trkpt")
        for p in trackpts:
            lat = float(p.getAttribute("lat"))
            lon = float(p.getAttribute("lon"))
            ele = float(p.getElementsByTagName("ele")[0].firstChild.nodeValue) if len(p.getElementsByTagName("ele")) > 0 else 0
            pnt = arcpy.Point(lon,lat,ele)
            nodes.add(pnt)
        line = arcpy.Polyline(nodes,sr,True)
        with arcpy.da.InsertCursor(sdePath + r"\KL_Exploration.DBO.traverse_tracks",["SHAPE@","TrackDate","Prospector1","Prospector2"]) as rows:
            rows.insertRow([line,trackdate.date(),sampler1Name,sampler2Name])


    



