import arcpy 


###....... Creating Geodatabase for Lab04.............### 
folder_path = r"D:\\PhD_TAMU\\Courses\\GEOG 676 GIS Programming\\Lab\\GISProgramming"
gdb_name = "GISProgramming_Lab04.gdb"
gdb_path = folder_path + "\\" + gdb_name
# arcpy.CreateFileGDB_management(folder_path,gdb_name)

###... Reading CSV file and creating garage point layer....##
csv_path = r"D:\\PhD_TAMU\\Courses\\GEOG 676 GIS Programming\\Lab\\GISProgramming\\Lab04\\Lab04_Data\\garages.csv"
garage_layer_name= "Garage_Points"
garages=arcpy.MakeXYEventLayer_management(csv_path, 'X', 'Y', garage_layer_name)


# print(garages)

###.... putting the garages file to gdb..........###
input_layer= garages
arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)

##.......get the garage points layer in gdb..........###
garage_points = gdb_path + "\\" + garage_layer_name

##........Copying bulding data from campus.gdb to GISProgramming_Lab04.gdb.........
campus = r"D:\\PhD_TAMU\\Courses\\GEOG 676 GIS Programming\\Lab\\GISProgramming\\Lab04\\Lab04_Data\\Campus.gdb"
building_campus = campus + "\\Structures"

##... Copying to the destination path for building feature
buildings = gdb_path+ "\\" + "Buildings"
# arcpy.Copy_management(building_campus, buildings)


## Changing the projection of the garage_points to building layer
spatial_ref = arcpy.Describe(buildings).spatialReference
garageReprojected = gdb_path+ "\Garage_Points_reprojected"
arcpy.Project_management(garage_points, garageReprojected, spatial_ref)

## Buffering the garage data
garageBufferPath = gdb_path + "\Garage_Points_buffered"
garageBuffered = arcpy.Buffer_analysis(garageReprojected, garageBufferPath, 150)

## Intersecting buffer with building
buildingIntersectionpath = gdb_path + "\Garage_Building_Intersection"
arcpy.Intersect_analysis([garageBuffered, buildings], buildingIntersectionpath, "ALL")

## Converting information of nearby building to csv
arcpy.TableToTable_conversion(gdb_path + "\Garage_Building_Intersection.dbf", r"D:\\PhD_TAMU\\Courses\\GEOG 676 GIS Programming\\Lab\\GISProgramming\\Lab04\\Lab04_Data", "nearbyBuilding.csv")
