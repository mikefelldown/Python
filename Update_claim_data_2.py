import arcpy, urllib, bs4, os
from xml.dom import minidom
from datetime import datetime

ws = r"Database Connections\KL_Exploration.sde"
fc = arcpy.GetParameterAsText(0)
cid = arcpy.GetParameterAsText(1)
exp = arcpy.GetParameterAsText(2)
wr = arcpy.GetParameterAsText(3)
ta = arcpy.GetParameterAsText(4)
tr = arcpy.GetParameterAsText(5)

desc = arcpy.Describe(fc)
fields = [i.name for i in desc.fields]


# Find data field indexes from list of field names
cii = fields.index(cid)
exi = fields.index(exp)
wri = fields.index(wr)
tai = fields.index(ta)
tri = fields.index(tr)
cu  = fields.index("Claim_Units")
twp = fields.index("Township")
try:
    dvi = fields.index("DateVal")
except:
    dvi = None

ed = arcpy.da.Editor(ws)
ed.startEditing(False, True)
ed.startOperation()
with arcpy.da.UpdateCursor(fc,"*","\"" + cid + "\" is not NULL") as rows:
    count = int(arcpy.GetCount_management(fc).getOutput(0))

    arcpy.SetProgressor("step","Updating claim data...",0,count,1)

    for row in rows:
        if row[cii].isdigit():
            arcpy.SetProgressorPosition()
            params = urllib.urlencode({"Div":80,"Claim_View__Claim_Number":row[cii]})
            try:
                pagetext = urllib.urlopen("http://www.mci.mndm.gov.on.ca/Claims/Cf_Claims/clm_csd.CFM?%s&Div=80" % params).read()
            except:
                arcpy.AddWarning("Error loading page for claim " + row[cii])
                continue
            soup = bs4.BeautifulSoup(pagetext)
            # Get data tables from html doc and clean up for import into xml format
            try:
                tables = soup.findAll("table")
                if tables[2].findAll("td")[2].text.find("ACTIVE") < 0:
                    raise Exception("Claim number %s has been cancelled" % row[cii])
                tds = tables[3].findAll("td")
                td2 = tables[4].findAll("td")
                anniversary = datetime.strptime(tds[1].string,"%Y-%b-%d")
                row[exi] = anniversary
                row[wri] = int(tds[5].string.replace("$","").replace(",","").strip())
                row[tai] = int(td2[1].string.replace("$","").replace(",","").strip())
                row[tri] = int(td2[5].string.replace("$","").replace(",","").strip())
                row[twp] = td2[3].string
                row[cu] =  int(td2[11].string)

                if dvi:
                    datediff = anniversary - datetime.today()
                    row[dvi] = datediff.days
                rows.updateRow(row)
            except:
                arcpy.AddWarning("Error on claim " + row[cii])

ed.stopOperation()
ed.stopEditing(True)
del ed

"""dir = arcpy.GetInstallInfo("desktop")["InstallDir"]
translator = dir + "Metadata/Translator/ESRI_ISO2ISO19139.xml"
arcpy.env.workspace = r"C:\Temp"
os.chdir(arcpy.env.workspace)
arcpy.env.overwriteOutput = 1

arcpy.ExportMetadata_conversion(fc,translator,"temp_meta.xml")

metaxml = minidom.parse("temp_meta.xml")

abstract = metaxml.getElementsByTagName("abstract")
gco = metaxml.getElementsByTagName("gco:CharacterString")[0]

dateString = datetime.strftime(datetime.today(),"%B %d, %Y")

gco.firstChild.nodeValue = "Mineral property tenure status updated " + dateString + "."

outxml = open("temp_meta.xml","wb")
outxml.write(metaxml.toxml())
outxml.close()


arcpy.ImportMetadata_conversion("temp_meta.xml","FROM_ISO_19139" ,fc)

os.remove("temp_meta.xml")"""

