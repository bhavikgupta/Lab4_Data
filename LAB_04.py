import arcpy
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

### >>>>>> Add your code here
INPUT_DB_PATH = "D:\\Lab4_Data\\Campus.gdb"
CSV_PATH = "D:\\Lab4_Data\\garages.csv"
OUTPUT_DB_PATH = "D:\\Lab4_Data"
OUTPUT_GDB_NAME ="Output.gdb"


### <<<<<< End of your code here

arcpy.env.workspace = INPUT_DB_PATH

# Layers need to be kept
layers_to_keep = ["GaragePoints", "LandUse", "Structures", "Trees"]

# list all feature clases
feature_classes = arcpy.ListFeatureClasses()
print(feature_classes)
# delete other classes
for fc in feature_classes:
    if fc not in layers_to_keep:
        print("Deleting" ,fc)
        arcpy.management.Delete(fc)

# create GDB management
### >>>>>> Add your code here
output_gdb_path = os.path.join(OUTPUT_DB_PATH, OUTPUT_GDB_NAME)
if not arcpy.Exists(output_gdb_path):
    arcpy.management.CreateFileGDB(OUTPUT_DB_PATH, OUTPUT_GDB_NAME)

    ### <<<<<< End of your code here

# Load .csv file to input GDB
### >>>>>> Add your code here
if not os.path.exists("Garages"):
   arcpy.management.XYTableToPoint(CSV_PATH, "Garages",
                                "X", "Y")
### <<<<<< End of your code here

# Print spatial references before re-projection
print(f"Before Re-Projection...")
print(f"garages layer spatial reference: {arcpy.Describe('Garages').spatialReference.name}.")
print(f"Structures layer spatial reference: {arcpy.Describe('Structures').spatialReference.name}.")

# Re-project
## >>>>>>>>> change the codes below
target_ref = arcpy.Describe("Garages").spatialReference

arcpy.management.Project(
   "Structures",
   "Structures_Projected",
   target_ref
)
## <<<<<<<< End of your code here
# print spatial references after re-projection
print(f"After Re-Projection...")
print(f"garages layer spatial reference: {arcpy.Describe('Garages').spatialReference.name}.")
print(f"re-projected Structures layer spatial reference: {arcpy.Describe('Structures_Projected').spatialReference.name}")

### >>>>>> Add your code here
# Buffer analysis
radiumStr = "150 meter"
buffer_output="garages_buffered"
arcpy.analysis.Buffer("Garages", buffer_output, radiumStr)


# Intersect analysis
inFeatures=["garages_buffered","Structures_Projected"]
intersectOutput="intersection"
arcpy.analysis.Intersect(inFeatures, intersectOutput)

# Output features to the created GDB
layers_to_output = ["Garages", "Structures", "garages_buffered","intersection"]
 
# Run CopyFeatures for each input shapefile
for layer in layers_to_output:
    # Determine the new output feature class path and name
    
    out_featureclass=os.path.join(output_gdb_path,layer)
    arcpy.management.CopyFeatures(layer, out_featureclass)
    print(f"Layer {layer} Exported to Output.gdb")  
### <<<<<< End of your code here
