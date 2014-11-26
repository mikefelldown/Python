#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mfell
#
# Created:     25/10/2014
# Copyright:   (c) Canadian Malartic Corporation 2014
# Licence:     GPL
#-------------------------------------------------------------------------------
import xlrd
import pyodbc
from datetime import datetime
import os

today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

# Helper functions for making SQL transactions
def insertRecord(cur, filename, sampleID, name, v):
    insertString = [today, filename.split("\\")[-1], sampleID, "Original", name, "", str(v), filename.split("\\")[-1]]
    cur.execute("Insert into [gt_QAQC_Tools]..[LabJobResults] (LoadDate, CertNum, SampleID, SampleType, Name, Reference, Value, OrigFileName) values (?,?,?,?,?,?,?,?)",(insertString))
    cur.commit()

def replaceRecord(cur, filename, sampleID, name, v):
    cur.execute("Delete from [gt_QAQC_Tools]..[LabJobResults] where SampleID =? and Name =?",(sampleID, name))
    cur.commit
    insertRecord(cur, filename, sampleID, name, v)


def main():
    # Get excel import sheet
    filename = r"C:\Users\mfell.QM\Documents\XL3-71677.xlsx"
    while filename is None:
        filename = raw_input("Full path to excel file: ") or None
    wb = xlrd.open_workbook(filename)
    ws = wb.sheet_by_index(0)

    # Connect to database and create cursor
    cnxn = pyodbc.connect("DRIVER={SQL Server}; SERVER=OSK-QMI-SQL01; DATABASE = gt_QAQC_Tools; Trusted_Connection = yes")
    cur = cnxn.cursor()

    #insertstring = [today, filename.split("\\")[-1],"Canadian Malartic Corporation", "-1", today, today, "UB","Internal",filename.split("\\")[-1],"1"]
    #cur.execute("Insert into [gt_QAQC_Tools]..[LabJobCert] (LoadDate, CertNum, Client, NumSamples, DateRecieved, DateFinalised, Project, Lab, OrigFileName, QAQCAccepted) values (?,?,?,?,?,?,?,?,?,?)",(insertstring))
    #cur.commit()
    #Iterate through rows of excel sheet and insert or replace data
    headers = [ws.cell(0,x).value for x in range (ws.ncols)]
    print "Enter the number for the first element:"
    for i in range(len(headers)):
        print "{0}:".format(i) + headers[i],
    first = raw_input()
    elements = [ws.cell(0,x).value for x in range(first,ws.ncols,2)]
    for row in range(ws.nrows - 1):
        sampleID = ws.cell(row+1,headers.index("SAMPLE")).value
        if sampleID == "":
            continue

        vals = {}
        for e in range(len(elements)):
            vals[elements[e]] = ws.cell(row+1,first + e * 2).value
        for k,v in vals.iteritems():
            name = 'NITON_XRF_' + k + '_ppm'
            if cur.execute("Select SampleID from [gt_QAQC_Tools]..[LabJobResults] where SampleID =? and Name =?",(sampleID, name)).rowcount == 0:
                insertRecord(cur, filename, sampleID, name, v)
            else:
                replaceRecord(cur, filename,sampleID, name, v)

if __name__ == '__main__':
    main()
