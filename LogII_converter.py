#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mfell
#
# Created:     24/06/2014
# Copyright:   (c) Osisko Mining Ltd 2014
# Licence:     GPL
#-------------------------------------------------------------------------------

import xlwt, os
from xlwt.Style import easyxf
from datetime import datetime

project = None
drill = None
coresize= None
drillStart= None
drillEnd= None
geo= None
location= None
holeID= None
Northing= None
Easting= None
Elevation= None
Length= None
Unit = None


def decodeDate(line):
    try:
        thedate = datetime.strptime(line.strip(),'"%B %d, %Y"')
        return thedate

    except ValueError:
        newDate = '"' + raw_input("I cannot under stand the date " + line) + '"'
        thedate = decodeDate(newDate)
        return thedate

def processHeader(line):
    """
    parse header data
    """
    global project
    global drill
    global coresize
    global drillStart
    global drillEnd
    global geo
    global location

    if line[:3] == "PR " or line[:3] == "PRJ":
        project = line[2:].split('"')[1].strip()
    elif line[:3] == "DR ":
        drill = line[2:].split('"')[1]
    elif line[:3] == "CS ":
        coresize = line[2:].split('"')[1]
    elif line[:3] == "DS ":
        drillStart = decodeDate(line[2:])
    elif line[:3] == "DC ":
        drillEnd = decodeDate(line[2:])
    elif line[:3] == "LB ":
        geo = line[2:].split('"')[1]
    elif line[:3] == "LOC":
        location = line[3:].split('"')[1]
    elif line[:3] == "MA ":
        pass

def processFirst(line):
    """
    parse first line of .in file
    """
    global holeID
    global Northing
    global Easting
    global Elevation
    global Length
    elements = [x for x in line[2:].split(" ") if x <> ""]
    holeID = elements[0]
    Northing = elements[1]
    Easting = elements[2]
    Elevation = elements[3]
    Length = elements[4]

def processSurveys(line):
    """
    process surveys (category 2) of .in file
    """
    vars = line.split(" ")
    while "" in vars:
        vars.remove("")
    return vars


def processAssays(line):
    vars = [x for x in line.split(" ") if x <> ""]
    if len(vars)> 8:
        vars[7] = " ".join(vars[7:])
        vars = vars[:8]
    while "" in vars:
        vars.remove("")
    return vars




def processDesc(line):
    if line[0] == "4":
        items = [x.strip() for x in line[2:].split(" ") if x <> ""]
        if len(items) > 3:
            items[2] = " ".join(items[2:])
            items = items[:3]
        items[2] = "; ".join(items[2].split(" "))
        return items

    elif line[0] == "5":
        data = line[2:].strip().strip("\"$ ")
        return data

def processSubDesc(line):
    items = [x.strip("[") for x in line[2:].split(" ") if x <> ""]
    if len(items) > 3:
        items[2] = " ".join(items[2:])
        items = items[:3]
        items[2:] = items[2].split("]")
    return items

def main():
    description = []
    mainLith = True
    os.chdir(r"C:\Projects\temp")
    filename = r"X:\DATA FILES\PROPERTIES\ANOKI\Temp\Historic Anoki McBean Logs - Master Database - Surpac Database\57322-0.IN"
    while not filename:
        filename = raw_input("LogII file name (.in) : ")

    #create new ms excel workbook and populate with worksheets
    try:
        xls = xlwt.Workbook()
        sheets = [xls.add_sheet(ws, cell_overwrite_ok=True) for ws in ['Index','Coords','Survey','Assay','Lithology','Sublithology']]

        # write index headers
        sheets[0].write(0,0,'Project')
        sheets[0].write(0,1,'HoleID')

        # write collar headers
        for i in enumerate(['Project','HoleID','Northing','Easting','Elevation','Length','Contractor','Core Size','Start Date','End Date','Author','Location']):
            sheets[1].write(0,i[0],i[1])

        # write survey headers
        for i in enumerate(['Project','HoleID','Depth','Azimuth','Dip']):
            sheets[2].write(0,i[0],i[1])

        # write assay headers
        for i in enumerate(['Project','HoleID','SampleID','From','To','Pyrite','AU','AU1','AU2','Comments']):
            sheets[3].write(0,i[0],i[1])

        # write lithology headers
        for i in enumerate(['Project','HoleID','From','To','Code','Description']):
            sheets[4].write(0,i[0],i[1])
            sheets[5].write(0,i[0],i[1])

    except:
        print "Could not create Excel workbook"

    # parse datafile and write data to worksheets
    with open(filename,'rb') as logIIfile:
        while True:
            firstline = logIIfile.readline()
            if firstline[0] == '1' or firstline[0] == '0':
                processFirst(firstline)
                break
        for l in logIIfile.readlines():
            if l[0] == "1":
                processHeader(l[1:].strip())
            elif l[0] == "2":
                data = processSurveys(l[1:].strip())
                r2 = sheets[2].last_used_row + 1
                sheets[2].write(r2,0,project)
                sheets[2].write(r2,1,holeID or None)
                sheets[2].write(r2,2,data[0])
                sheets[2].write(r2,3,data[1])
                sheets[2].write(r2,4,data[2])

            elif l[0] == "3":
                data = processAssays(l[1:].strip())
                r3 = sheets[3].last_used_row + 1
                sheets[3].write(r3,0,project)
                sheets[3].write(r3,1,holeID)
                for var in enumerate(data):
                    sheets[3].write(r3,var[0]+2,var[1])

            elif l[0] == "4":
                sheets[4].flush_row_data()
                sheets[5].flush_row_data()
                mainLith = True
                data = processDesc(l)
                row = sheets[4].last_used_row + 1
                sheets[4].write(row,0,project)
                sheets[4].write(row,1,holeID)
                for item in enumerate(data):
                    sheets[4].write(row,item[0]+2,item[1])
                description = []
            elif l[0] == "5" and l.find("\"\"") == -1:
                if [x for x in list(l[2:]) if x <> " "][0].isdigit():
                    mainLith = False
                    row = sheets[5].last_used_row + 1
                    data = processSubDesc(l)
                    description = []
                    sheets[5].write(row,0,project)
                    sheets[5].write(row,1,holeID)
                    for item in enumerate(data[:3]):
                        sheets[5].write(row,item[0]+2,item[1])
                    if len(data) > 3:
                        description.append(data[3])
                else:
                    description.append(processDesc(l))

                sheets[4 if mainLith else 5].write(row, 5, " ".join(description))


    # write index and collar data to worksheets
    r = sheets[0].last_used_row + 1
    sheets[0].write(r,0,project)
    sheets[0].write(r,1,holeID)

    r1 = sheets[1].last_used_row + 1
    sheets[1].write(r1,0,project)
    sheets[1].write(r1,1,holeID)
    sheets[1].write(r1,2,Easting)
    sheets[1].write(r1,3,Northing)
    sheets[1].write(r1,4,Elevation)
    sheets[1].write(r1,5,Length)
    sheets[1].write(r1,6,drill)
    sheets[1].write(r1,7,coresize)
    sheets[1].write(r1,8,drillStart,easyxf(num_format_str='YYYY-MM-DD'))
    sheets[1].write(r1,9,drillEnd,easyxf(num_format_str='YYYY-MM-DD'))
    sheets[1].write(r1,10,geo)
    sheets[1].write(r1,11,location)

    # save file and end
    xls.save(holeID + ".xls")



if __name__ == '__main__':
    main()
