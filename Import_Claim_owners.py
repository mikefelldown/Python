import arcpy
import BeautifulSoup as bs4
import urllib

arcpy.env.workspace = r"Database Connections/KL_Exploration.sde/KL_Exploration.DBO.Property"
ws = r"Database Connections\KL_Exploration.sde"

ed = arcpy.da.Editor(ws)
ed.startEditing(False, True)
ed.startOperation()

with arcpy.da.UpdateCursor("KL_Exploration.DBO.QMI_ClaimFabric",["CLAIM_NUM","Registered_Owners"],"Registered_Owners is NULL") as rows:
    for row in rows:
        print row[0]
        params = urllib.urlencode({'txtDiv' : '80','Claim_View__Claim_Number' : row[0],'Claim_View__Twp_Name' : '','Claim_View__Claim_Due_Date': ''})
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

ed.stopOperation()
ed.stopEditing(True)
del ed





