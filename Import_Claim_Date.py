import arcpy
import bs4, urllib
from datetime import datetime

ed = arcpy.da.Editor("C:\Users\mfell.QM\Documents\ArcGIS\Default.gdb")
arcpy.env.workspace = r"C:\Users\mfell.QM\Documents\ArcGIS\Default.gdb"

##ed.startEditing()
##
##ed.startOperation()


with arcpy.da.UpdateCursor("Claims_20140424",["CLAIM_NUM","DateAcquir"],"CLAIM_NUM is not null and DateAcquir is null") as rows:
    for row in rows:
        arcpy.AddMessage("Getting data for " +row[0])
        params = urllib.urlencode({'Div' : '80','Claim_View__Claim_Number' : row[0]})                        
       
        page = urllib.urlopen(r"http://www.mci.mndm.gov.on.ca/Claims/Cf_Claims/clm_csd.cfm?%s" % params)
        
        soup = bs4.BeautifulSoup(page.read())
        table = soup.findAll("table")[3]
        date_text = table.findAll("td")[3].getText()
        row[1] = datetime.strptime(date_text,"%Y-%b-%d")
        rows.updateRow(row)
    



##ed.stopOperation()
##
##ed.stopEditing(True)
        
        
                                  