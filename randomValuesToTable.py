import arcpy
import numpy as np
import numpy.random

# # USING FILE PATHING
# arcpy.env.workspace = "H:\Services\Service Jobs Open\Imaging Services\23-1 - City of Toronto - 2023\Assets\30_QC\Etobicoke Centre\TORONTO_2023_Etobicoke_Centre_From_DCIL_13_Aug_2024.gdb"
# # This is just pointing to the actual table
# feature_class = "\Road_Paint_Point_CS_20240827"
# # Creating this new field to a variable to use in getRandomValue function
# field_name = "random_value"

# Definining the main agent in this script our getRandomValue function
def getRandomValue():
    return numpy.random.random()


# Getting our map from ArcMap to use
currentMap = arcpy.mapping.MapDocument("CURRENT")

# Getting active data frame from map
df = arcpy.mapping.ListDataFrames(currentMap)[0]

# Selecting first selected layer as feature layer
# since cannot do user popup window to request raw_input in ArcMap software
layers = [layer for layer in arcpy.mapping.ListLayers(currentMap, "", df) if layer.isFeatureLayer]
selected_layer = layers[0]
feature_class = selected_layer.dataSource

# We are reading from table layer (total) and then using that as our check for defining sample_size
def calculateSampleSize():
   if 1 <= layer <= 8:
       sample_size = 2
   elif 9<= layer <= 15:
       sample_size = 3
   elif 16<= layer <= 25:
       sample_size = 5
   elif 26<= layer <= 50:
       sample_size = 8
   elif 51<= layer <=90:
       sample_size = 13
   elif 91<= layer <= 150:
       sample_size = 20
   elif 151<= layer <= 280:
       sample_size = 32
   elif 281<= layer <=500:
       sample_size = 50
   elif 501<= layer <=1200:
       sample_size = 80
   elif 1201<= layer <=3200:
       sample_size = 125
   elif 3201<= layer <= 10000:
       sample_size = 200
   elif 10001 <= layer <= 35000:
       sample_size = 315
   elif 35001 <= layer <= 150000:
       sample_size = 500
   else:
       sample_size = 800
   return sample_size

def rejectionNumber(sample_size):
    if 1<= sample_size <= 3:
        rejection_number = 1
    elif 4<= sample_size <= 13:
        rejection_number = 2
    elif 14<= sample_size <=20:
        rejection_number = 3
    elif 21<= sample_size <=32:
        rejection_number = 4
    elif 33<= sample_size <= 50:
        rejection_number = 6
    elif 51<= sample_size <= 80:
        rejection_number = 8

    # Main formula below after fetching acceptance and quality level of our table's sample size


# Delete random_value field if already exists - this is also needed for rerunning script and creating new random samples
field_names = [field.name for field in arcpy.ListFields(feature_class)]
if "random_value" in field_names:
    arcpy.DeleteField_management(feature_class, "random_value")

# Creating the new field using AddField_management tool - accessing our layer to modify attribute table.
# FLOAT IS A MUST FOR DECIMALS
arcpy.AddField_management(feature_class, "random_value", "FLOAT")


# In each row, update the newly created random_value field_name by using a list on row and calling our function on all rows
with arcpy.da.UpdateCursor(feature_class, ["random_value"]) as cursor:
    for row in cursor:
        row[0] = getRandomValue()
        cursor.updateRow(row)
print("Random values have been assigned to the 'random_value field in the %s layer." % selected_layer.name)





