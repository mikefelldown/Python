import urllib, arcpy
from bs4 import BeautifulSoup

params = urllib.urlencode({"txtDiv" : "80", "HolderName" : "Osisko Mining Ltd"})

pagetext = urllib.urlopen(r"http://www.mci.mndm.gov.on.ca/Claims/Cf_Claims/clm_clr.cfm",params)

soup = BeautifulSoup(pagetext)

table = soup.findAll("table")[1]

rows = table.findAll("tr")[1:]

claimnos = [row.findAll("td")[1].string.strip() for row in rows]

claims = arcpy.da.SearchCursor(r"Database Connections\KL_Exploration.sde\KL_Exploration.DBO.Property\KL_Exploration.DBO.QMI_ClaimFabric",["CLAIM_NUM"],"CLAIM_NUM IS NOT NULL AND CLAIM_NUM <> ' ' AND Registered_owners LIKE 'OSISKO%'")

osiskoClaims = [s[0] for s in claims]

claimList = [r for r in claimnos if r not in osiskoClaims]

print ", ".join(claimList)

