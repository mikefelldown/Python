import arcpy
from datetime import datetime
import pyodbc

db = "C:\Users\mfell\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\KL_Exploration.sde"
cnxn = pyodbc.connect("DSN=KL_QAQC; TrustedConnection=yes")
count = 0

def update_samples(rows):
    global count
    for row in rows:
        results = cnxn.execute("SELECT sampleid, name, value, labcertificate, preferred from dbo.LabJobResults where sampleid = '%s' and name in ('Au_AA23_g/t', 'Au_GRA21_g/t') and preferred = 1" % (row[0])).fetchall()
        if results:
            print "Sample %s found." % (results[0][0])
            count +=1 
            for result in results:
                if result[1] == "Au_GRA21_g/t":
                    row[1] = float(result[2])
                    row[3] = result[1]
                elif result[1] == "Au_AA23_g/t" and type(row[1]) == type(None):
                    if result[2][0] == "<":
                        row[1] = 0
                        row[2] = result[2]
                    else:
                        row[1] = float(result[2])
                    row[3] = result[1]
                    
                row[4] = result[3]
                row[5] = datetime.now()
            rows.updateRow(row)

with arcpy.da.UpdateCursor(db + "\KL_Exploration.DBO.rock_samples",["SampleID","Au_ppm","Au_BDL","Au_Method","CertificateID","LoadDate"],"Au_ppm is Null") as curs:
    update_samples(curs)
    
with arcpy.da.UpdateCursor(db + "\KL_Exploration.DBO.QC_samples",["SampleID","Au_ppm","Au_BDL","Au_Method","CertificateID","LoadDate"],"Au_ppm is Null") as stds:
    update_samples(stds)

del cnxn
print "Samples updated: %d" % (count)

