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

# List all layers in active data frame from map
layers = [layer for layer in arcpy.mapping.ListLayers(currentMap, "", df) if layer.isFeatureLayer]

# Popup window prompting user what layer they wish to select
print("Please select a layer to modify: ")
for idx, layer in enumerate(layers):
    print("%d: %s" % (idx + 1, layer.name))

# Setting the user's choice to a variable to use for later
layer_index = int(raw_input("Enter the number corresponding to the layer: "))

# Taking this user input picking the layer and using that to choose which layer to run script onto
if 0 <- layer < len(layers):
    selected_layer = layers[layer_index]
    feature_class = selected_layer.dataSource

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
else:
    print("Invalid layer selection.")






