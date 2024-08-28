import arcpy
import numpy as np
import numpy.random

# Routing to our layer where we want to create this field to
arcpy.env.workspace = "H:\Services\Service Jobs Open\Imaging Services\23-1 - City of Toronto - 2023\Assets\30_QC\Etobicoke Centre\TORONTO_2023_Etobicoke_Centre_From_DCIL_13_Aug_2024.gdb"
# This is just pointing to the actual table
feature_class = "\Road_Paint_Point_CS_20240827"
# Creating this new field to a variable to use in getRandomValue function
field_name = "random_value"

# Definining the main agent in this script our getRandomValue function
def getRandomValue():
    return numpy.random.random()

# Creating the new field using AddField_management tool - accessing our table and then setting the name and type. FLOAT IS A MUST FOR DECIMALS
arcpy.AddField_management(feature_class, "random_value", "FLOAT")

# IF WE NEED TO DELETE THIS FIELD UNCOMMENT OR COPY PASTE THE BELOW
# arcpy.DeleteField_management(feature_class, "random_value")

# In each row, update the newly created random_value field_name by using a list on row and calling our function on all rows
with arcpy.da.UpdateCursor(feature_class, [field_name]) as cursor:
    for row in cursor:
        row[0] = getRandomValue()
        cursor.updateRow(row)





