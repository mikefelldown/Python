import arcpy
import bs4, urllib

arcpy.env.workspace = r"C:\Users\mfell.QM\Documents\ArcGIS\Default.gdb"

with arcpy.da.UpdateCursor("Claims_20140424",["CLAIM_NUM","Registered_Owners"],"Registered_Owners is NULL") as rows:
    for row in rows:
        print row[0]
        params = params = urllib.urlencode({'txtDiv' : '80','Claim_View__Claim_Number' : row[0],'Claim_View__Twp_Name' : '','Claim_View__Claim_Due_Date': ''})                        
        try:
            page = urllib.urlopen(r"http://www.mci.mndm.gov.on.ca/Claims/Cf_Claims/clm_csr.cfm?%s" % params)
        except:
            continue
        soup = bs4.BeautifulSoup(page.read())
        table = soup.findAll("table")[1]
        tr = table.findAll("tr")
        owners = []
        try:
            for r in tr[1:]:
                td = r.findAll("td")
                owners.append(td[2].getText())
            row[1] = ", ".join(owners)
        except:
            row[1] = "import error"
        rows.updateRow(row)
    




        
        
                                  