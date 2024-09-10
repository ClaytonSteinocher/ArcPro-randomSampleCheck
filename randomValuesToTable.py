import arcpy
import numpy as np
import numpy.random
import tkinter as tk
from tkinter import simpledialog

# Initialize Tkinter for popup
root = tk.Tk()
# Hide the main window
root.withdraw()

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

# Ideally popup happens here asking for user to select Layer
selected_layer_index = simpledialog.askinteger("Layer Selection", "Enter the layer index (0-based):")

# Getting current project map from ArcGIS Pro
aprx = arcpy.mp.ArcGISProject("CURRENT")
# Assuming first map
map_view = aprx.listMaps()[0]

# Putting all feature layers from the map into an accessible list
layers = [layer for layer in map_view.listLayers() if layer.isFeatureLayer]

# Checking if the selected layer index is valid
if 0 <= selected_layer_index < len(layers):
    selected_layer = layers[selected_layer_index]
    feature_class = selected_layer.dataSource

    # Deleting random_value field if it already exists to rerun script
    field_names = [field.name for field in arcpy.ListFields(feature_class)]
    if "random_value" in field_names:
        arcpy.DeleteField_management(feature_class, "random_value")

    # Creating the new field using AddField_management tool
    # Accessing our feature_class layer to modify its attribute table
    arcpy.AddField_management(feature_class, "random_value", "FLOAT")

    # Calculating the number of rows in our feature class
    # So that calculateSampleSize function can run through and take only a sample
    feature_count = int(arcpy.GetCount_management(feature_class).getOutput(0))
    sample_size = calculateSampleSize(feature_count)

    # Using direct indexing instead of count += 1 for updating cursor per row
    # Since newer version of Python with ArcPro version
    with arcpy.da.UpdateCursor(feature_class, ["random_value"]) as cursor:
        count = 0
        for row in cursor:
            if count < sample_size:
                # Setting the field random_value using getRandomValue function
                row[0] = getRandomValue()
                cursor.updateRow(row)
                count += 1
            else:
                # Stop once sample_size is reached to avoid IterationError or infinite loop
                break

    ## Printing out not just the sample size just created, but also the rejection number for
    # the user to stay aware of as they go through this random sample manually.
    ## This way we can completely remove the need for that excel's sheet functionality.
    rejection_number = rejectionNumber(sample_size)
    print(f"Sample size: {sample_size}, Rejection number: {rejection_number}")
    print(f"Random values assigned to {sample_size} rows in layer: {selected_layer.name}")
else:
    print("Invalid layer index selected.")

# Cleaning up Tkinter now
root.destroy()