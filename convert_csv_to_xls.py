import os, csv, xlwt

os.chdir(r"C:\Users\mfell\Documents\ArcGIS")

csvList = [f for f in os.listdir(os.getcwd()) if f.find(".csv") > 0]

for csvfile in csvList:
    book = xlwt.Workbook()
    sheet1 = book.add_sheet(csvfile[:-4])
    with open(csvfile,'rb') as myfile:
        reader = csv.reader(myfile)
        r = 0
        for line in reader:
            c = 0
            for element in line:
                sheet1.write(r,c,element)
                c += 1
            r += 1
    book.save(csvfile[:-4]+".xls")


            
    