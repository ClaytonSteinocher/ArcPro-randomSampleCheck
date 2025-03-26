# Created by Clayton Steinocher - last updated 03/26/2025

import arcpy
import numpy as np
import numpy.random
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

# Initialize Tkinter for popup
root = tk.Tk()
# Hide the main window
root.withdraw()

# Definining the main agent in this script our getRandomValue function
def getRandomValue():
    return numpy.random.random()

# We are reading from table layer (total) and then using that as our check for defining sample_size
def calculateSampleSize(feature_count):
   if 1 <= feature_count <= 8:
       sample_size = 2
   elif 9<= feature_count <= 15:
       sample_size = 3
   elif 16<= feature_count <= 25:
       sample_size = 5
   elif 26<= feature_count <= 50:
       sample_size = 8
   elif 51<= feature_count <=90:
       sample_size = 13
   elif 91<= feature_count <= 150:
       sample_size = 20
   elif 151<= feature_count <= 280:
       sample_size = 32
   elif 281<= feature_count <=500:
       sample_size = 50
   elif 501<= feature_count <=1200:
       sample_size = 80
   elif 1201<= feature_count <=3200:
       sample_size = 125
   elif 3201<= feature_count <= 10000:
       sample_size = 200
   elif 10001 <= feature_count <= 35000:
       sample_size = 315
   elif 35001 <= feature_count <= 150000:
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

   # This isnt using direct indexing - think we are still using ArcMap version base for this function. Worth digging into maybe later
    def updateRows(feature_class, sample_size):
        try:
            # Collecting all rows into memory
            rows = []
            with arcpy.da.UpdateCursor(feature_class, ["OID@", "random_value"]) as cursor:
                for row in cursor:
                    # OID and value placeholder
                    rows.append([row[0], row[1]])
            # Shuffling the row list
            np.random.shuffle(rows)

            # Selecting the OIDS to update
            sampled_oids = set([row[0] for row in rows[:sample_size]])

            # Updating only the sampled rows
            with arcpy.da.UpdateCursor(feature_class, ["OID@", "random_value"]) as cursor:
                for row in cursor:
                    if row[0] in sampled_oids:
                        row[1] = getRandomValue()
                        cursor.updateRow(row)

        # Throwing error here if this is the problem card - i think maybe
        except Exception as e:
            messagebox.showerror("Update rows error", f"An error occured: {str(e)}")
            raise e
        # Clearing here too before printout in case its too late by when printout is closing out script
        finally:
            arcpy.ClearWorkspaceCache_management()
            # Deleting cursor too maybe that is it
            if cursor:
                del  cursor

    # Calling function directly below it
    updateRows(feature_class, sample_size)

    # Creating printout function so that we can use e as Exception to help debug this better
    def printout():
        try:
            rejection_number = rejectionNumber(sample_size)
            # ## Using messagebox from tkinter to printout not just the sample size just created, but also the rejection number for
            # # the user to stay aware of as they go through this random sample manually.
            # ## This way we can completely remove the need for that excel's sheet functionality.
            messagebox.showinfo("Success", f"Sample size: {sample_size}, Rejecton number :{rejection_number}\n"
                                           f'Random values assigned to {sample_size} rows in layer: {selected_layer.name}')
        except Exception as e:
            messagebox.showerror("Error", f"An error occured:  {str(e)}")
        finally:
            # Cleaning up Tkinter and the lock hopefully
            arcpy.ClearWorkspaceCache_management()
    # Let's make sure to call this or else no printout...lol
    printout()
    # Saving map object after final printout to release any save locks if that is it
    aprx.save()
else:
    messagebox.showerror("Error", "Invalid layer index selected.")