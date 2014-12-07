#-------------------------------------------------------------------------------
# Name:        print dataframes
# Purpose:
#
# Author:      mfell
#
# Created:     04/12/2014
# Copyright:   (c) Canadian Malartic Corporation 2014
# Licence:     GPL
#-------------------------------------------------------------------------------

import arcpy
from arcpy import mapping

def toggleVisible(lyrs):
    for l in lyrs:
        l.visible = not l.visible
    arcpy.RefreshActiveView()

def main():
    mxd = mapping.MapDocument("CURRENT")
    if not mxd.activeView == "PAGE_LAYOUT":
        mxd.activeView = "PAGE_LAYOUT"

    dataFrames = mapping.ListDataFrames(mxd)
    toPrint = []
    for df in dataFrames:
        layerList = mapping.ListLayers(df)
        if any(lyr.isGroupLayer and lyr.visible for lyr in lyrList) or (any([lyr.visible for lyr in layerList]) and not any(lyr.isGroupLayer for lyr in lyrList)):
            dfnames = [[frame, frame.name.split("_")] for frame in dataFrames if frame <> df and len(frame.name.split("_")) > 1 and frame.name.split("_")[0] == df.name.split("_") and frame.name.split("_")[1] == df.name.split("_")[1]]

            toPrint.append(df)
        for layer in layerList:
            layer.visible = False
    arcpy.RefreshActiveView()

    for df in toPrint:
        lyrs = mapping.ListLayers(df)
        toggleVisible(lyrs)
        mapping.PrintMap(mxd)
        toggleVisible(lyrs)





if __name__ == '__main__':
    main()
