#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mfell
#
# Created:     10/12/2015
# Copyright:   (c) Canadian Malartic Corporation 2015
# Licence:     007
#-------------------------------------------------------------------------------
import arcpy

import re



def check_field_name(fname, desc_obj, field_type, fc):
    if fname in [x.name for x in desc_obj.fields]:
        pat = re.compile(r'\d+$')
        test = re.search(pat, fname)
        if test:
            fname = re.sub(pat, str(int(test.group())+1), fname)
            fname = check_field_name(fname, desc_obj, field_type, fc)

        else:
            fname = check_field_name(fname + "_1", desc_obj, field_type, fc)
    else:
        arcpy.AddField_management(fc, fname, field_type)
    arcpy.AddMessage(fname)
    return fname

def main():
    fc = arcpy.GetParameterAsText(0)
    near_field = arcpy.GetParameterAsText(1)
    ref_field = arcpy.GetParameterAsText(2)
    desc = arcpy.Describe(fc)
    oid = desc.fields[0].name
    if near_field:
        near_field = check_field_name(near_field, desc, "DOUBLE", fc)
    else:
        near_field = check_field_name("near_distance", desc, "DOUBLE", fc)

    if ref_field:
        ref = check_field_name("reference", desc, "TEXT", fc)
        rows = arcpy.da.UpdateCursor(fc,[oid, "SHAPE@", near_field, ref])
    else:
        rows = arcpy.da.UpdateCursor(fc, [oid, "SHAPE@", near_field])
    for row in rows:
        min_dist = float('inf')
        ref = None
        search = arcpy.da.SearchCursor(fc, [oid, "SHAPE@"],oid + " <> " + str(row[0]))
        for s in search:
            dist = row[1].distanceTo(s[1])
            min_dist = min(dist, min_dist)
            if min_dist == dist and ref_field != "":
                ref = arcpy.da.SearchCursor(fc, [ref_field], oid + " = " + str(s[0])).next()[0]
        row[2] = min_dist
        if len(row)>3:
            row[3] = ref
        rows.updateRow(row)
        del s, search
    del row, rows

if __name__ == '__main__':
    main()
