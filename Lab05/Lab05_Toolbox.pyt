# -*- coding: utf-8 -*-

import arcpy
import os


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Building Proximity"
        self.description = "Defines which buildings on TAMU's campus are near to a targeted building"
        self.canRunInBackground = False
        self.category = "Building Tools"

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(displayName= "Work GDB folder path", name = "GDBFolderpath", datatype="DEFolder", parameterType="Required", direction= "Input")
        param1 = arcpy.Parameter(displayName="Work GDB Name", name="GDB_Name", datatype= "GPString", parameterType="Required", direction="Input")
        param2 = arcpy.Parameter(displayName="Garage CSV file path", name="garagecsvfileaddress", datatype="DEFile", parameterType="Required", direction="Input")
        param3 = arcpy.Parameter(displayName="Garage Name", name="garage_name", datatype="GPString", parameterType="Reguired", direction="Input")
        param4 = arcpy.Parameter(displayName="Campus GDB folder path", name="CampusGDBFolderPath", datatype="DeFolder", parameterType="Required", direction="Input")
        param5 = arcpy.Parameter(displayName="Selected Garage Name", name="selectedGarageName", datatype="GPString", parameterType="Required", direction="Input")
        param6 = arcpy.Parameter(displayName="Buffer Radius", name="bufferradius", datatype="GPDouble", parameterType="Required", direction="Input")
        params = [param0,param1, param2, param3, param4, param5, param6]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        GDB_Folder = parameters[0].valueAsText
        GDB_Name = parameters[1].valueAsText
        garage_csv_file = parameters[2].valueAsText
        garageLayer_name = parameters[3].valueAsText
        campusGDB_Folder = parameters[4].valueAsText
        Selected_Garage_Name = parameters[5].valueAsText
        bufferSize_input = parameters[6].valueAsText
        
        campus = os.path.join(campusGDB_Folder, "Campus.gdb")
        WorkGDB = GDB_Name + ".gdb"
        database = os.path.join(GDB_Folder, WorkGDB)
        arcpy.env.overwriteOutput = True
        if arcpy.Exists(database):
            pass
        else:
            arcpy.CreateFileGDB_management(GDB_Folder, WorkGDB)
        arcpy.env.workspace = database

        #importing garage csv
        garages = arcpy.management.MakeXYEventLayer(garage_csv_file, "x", "y", garageLayer_name)

        #search 
        structure = campus + "/Structures"
        where_clause = "BldgName = '%s' " % Selected_Garage_Name
        cursor = arcpy.SearchCursor(structure, where_clause=where_clause)

        shouldProceed = False

        for row in cursor:
            if row.getValue ("BldgName") == Selected_Garage_Name:
                shouldProceed = True
            break

        if shouldProceed:
            #select garage as feature layer
            selected_garage_layer_name = database + "/garage_slected"
            garage_feature = arcpy.Select_analysis(structure, selected_garage_layer_name, where_clause)

            #Buffer the selected building
            garage_buff_name = database+ "/building_buffed_%s" % (bufferSize_input)
            arcpy.Buffer_analysis(garage_feature, garage_buff_name, bufferSize_input + " meter")

            #Clip
            arcpy.Clip_analysis(structure, garage_buff_name, database + "/clip")
            arcpy.AddMessage("Success!!!!!!")
        else:
            arcpy.AddError("Seems we could not find the building you entered")

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return