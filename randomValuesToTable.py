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

# We are reading from table layer (total) and then using that as our check for defining sample_size
def calculateSampleSize(feature_class):
   if 1 <= feature_class <= 8:
       sample_size = 2
   elif 9<= feature_class <= 15:
       sample_size = 3
   elif 16<= feature_class <= 25:
       sample_size = 5
   elif 26<= feature_class <= 50:
       sample_size = 8
   elif 51<= feature_class <=90:
       sample_size = 13
   elif 91<= feature_class <= 150:
       sample_size = 20
   elif 151<= feature_class <= 280:
       sample_size = 32
   elif 281<= feature_class <=500:
       sample_size = 50
   elif 501<= feature_class <=1200:
       sample_size = 80
   elif 1201<= feature_class <=3200:
       sample_size = 125
   elif 3201<= feature_class <= 10000:
       sample_size = 200
   elif 10001 <= feature_class <= 35000:
       sample_size = 315
   elif 35001 <= feature_class <= 150000:
       sample_size = 500
   else:
       sample_size = 800
   return sample_size

# Defining rejection number to print to console at end
def rejectionNumber(sample_size):
    if 1<= sample_size <= 4:
        rejection_number = 1
    elif 5<= sample_size <= 19:
        rejection_number = 2
    elif 20<= sample_size <=31:
        rejection_number = 3
    elif 32<= sample_size <=49:
        rejection_number = 4
    elif 50<= sample_size <= 79:
        rejection_number = 6
    elif 80<= sample_size <= 124:
        rejection_number = 8
    elif 125<= sample_size <= 199:
        rejection_number = 11
    elif 200<= sample_size <= 314:
        rejection_number = 15
    else:
        rejection_number = 22
    return rejection_number

# Getting our map from ArcMap to use
currentMap = arcpy.mapping.MapDocument("CURRENT")

# Getting active data frame from map
df = arcpy.mapping.ListDataFrames(currentMap)[0]

# Selecting first selected layer as feature layer
# since cannot do user popup window to request raw_input in ArcMap software
layers = [layer for layer in arcpy.mapping.ListLayers(currentMap, "", df) if layer.isFeatureLayer]
selected_layer = layers[0]
feature_class = selected_layer.dataSource


# Delete random_value field if already exists - this is also needed for rerunning script and creating new random samples
field_names = [field.name for field in arcpy.ListFields(feature_class)]
if "random_value" in field_names:
    arcpy.DeleteField_management(feature_class, "random_value")

# Creating the new field using AddField_management tool - accessing our layer to modify attribute table.
# FLOAT IS A MUST FOR DECIMALS
arcpy.AddField_management(feature_class, "random_value", "FLOAT")

# Getting the number of rows in our feature class so that calculateSampleSize function can run that total through and take a sample
feature_rows = int(arcpy.GetCount_management(feature_class).getOutput(0))
sample_size = calculateSampleSize(feature_rows)

# Moving away from direct indexing to row.setValue instead since older version of Python
cursor = arcpy.UpdateCursor(feature_class)
count = 0
for row in cursor:
    if count < sample_size:
        # Setting the field random_value using getRandomValue function
        row.setValue("random_value", getRandomValue())
        # Updating each row one by one and add 1 to count after each row modified
        cursor.updateRow(row)
        count += 1
    else:
        break
# Deleting cursor afterwards to avoid locks or errors
del cursor

# Print actually does work at least if run from terminal - TODO: Figure out if possible to popup terminal then if run from toolbox
print("Random values have been assigned to the 'random_value field in the %s layer." % selected_layer.name)

rejection_printout = rejectionNumber(sample_size)
# Printing rejection number as well based on sample size to complete save any need to reference that excel sheet
print("Out of your sample size in this random_sample field, you have a rejection number of: " + str(rejection_printout))






