import os
import rasterio
from rasterio.mask import mask
from rasterio.features import geometry_mask
from rasterio.windows import from_bounds
from rasterio.windows import Window
import numpy as np
import matplotlib as plt  
from matplotlib import pyplot
import geopandas as gpd
from matplotlib.colors import ListedColormap
import earthpy as et
import earthpy.plot as ep
import fiona
from shapely.geometry import shape
from tqdm import tqdm
from datetime import datetime



##.................... Dissolving shapefile based on District Name................

# ##importing Texas dataset
# texas_boundary = gpd.read_file("D:\OneDrive - Texas A&M University\PhD\PhD_Courses\GEOG 676 GIS Programming\Group Project\Data\Shp\County.shp")
# texasBoundary = texas_boundary[["DIST_NM", "geometry"]] #Selecting the coloumns that will be u
# texasDst = texasBoundary.dissolve (by ="DIST_NM") 
# print(texasDst) #Checking the dissolved result


# # Use tqdm to show progress
# with tqdm(total=1, desc="Saving Shapefile") as pbar:
#     texasDst.to_file("D:\PhD_TAMU\Courses\GEOG 676 GIS Programming\Group Project\Data\Shp\TexasDst.shp") #saving created shapefile
#     pbar.update(1)


# ##.................... Recoding LULC................

# Open the NLCD raster data
# nlcd_raster_path = "D:\OneDrive - Texas A&M University\PhD\PhD_Courses\GEOG 676 GIS Programming\Group Project\Data\Raster\LULC.tif"
# nlcd_raster = rasterio.open(nlcd_raster_path)
# print("nlcd", nlcd_raster)

# # Read the data
# data = nlcd_raster.read()
# nlcd = data.copy()
# nlcd = nlcd.astype("int8")
# print(nlcd.dtype)

# # Reclassify values
# reclass_mapping = {
#     0: 0, 11: 0, 21: 0, 22: 0, 23: 0, 24: 0, 31: 4, 41: 0, 42: 0,
#     43: 0, 52: 1, 71: 2, 81: 3, 82: 0, 90: 0, 95: 0
# }

# for original_value, new_value in tqdm(reclass_mapping.items(), desc="Reclassifying values"):
#     nlcd[np.where(nlcd == original_value)] = new_value


# # Save the reclassified raster
# output_raster_path = 'D:\OneDrive - Texas A&M University\PhD\PhD_Courses\GEOG 676 GIS Programming\Group Project\Data\Raster/nlcd_reclass.tif'
# with rasterio.open(output_raster_path, 'w',
#                    driver=nlcd_raster.driver,
#                    height=nlcd_raster.height,
#                    width=nlcd_raster.width,
#                    count=nlcd_raster.count,
#                    crs=nlcd_raster.crs,
#                    transform=nlcd_raster.transform,
#                    dtype=nlcd.dtype
#                    ) as dst:
#     dst.write(nlcd)


# ##.................... Normalizing LULC value ...................

# # Open the raster dataset
# lulc = rasterio.open('D:\PhD_TAMU\Courses\GEOG 676 GIS Programming\Group Project\Data\Raster/nlcd_reclass.tif')

# # Get metadata
# profile = lulc.profile
# dtype = lulc.dtypes[0]

# # Create a tqdm progress bar
# with tqdm(total=100, desc='Writing Normalized LULC') as pbar:
#     # Calculate the total number of blocks
#     total_blocks = lulc.count * lulc.height // lulc.block_shapes[0][0]

#     # Iterate over windows (blocks) of the raster
#     for _, window in lulc.block_windows():

#         # Read the data for the current window
#         lulc_data = lulc.read(window=window)

#         # Calculate the min and max values for the current window
#         lulc_min_value = np.min(lulc_data)
#         lulc_max_value = np.max(lulc_data)

#         # Normalize the data for the current window
#         normalized_lulc = (lulc_data - lulc_min_value) / (lulc_max_value - lulc_min_value)

#         # Write the normalized data to the output raster
#         with rasterio.open('D:\PhD_TAMU\Courses\GEOG 676 GIS Programming\Group Project\Data\Raster/final_normalized_LULC.tif', 'w',
#                            **profile) as dst:
#             dst.write(normalized_lulc, window=window)

#         # Update the progress bar
#         pbar.update(100 / total_blocks)

# print("LULC Normalization is complete.")



# ##.................... Recoding Slope................

# #Open the slope raster data
# slope_raster = rasterio.open("D:\PhD_TAMU\Courses\GEOG 676 GIS Programming\Group Project\Data\Raster\Slope.tif")
# print("slope", slope_raster)
# data = slope_raster.read()   
# # print (data.dtype)
# slope = data.copy()

# conditions = [
#     (slope < 0.5),
#     ((slope >= 0.5) & (slope <= 20)),
#     (slope > 20)
# ]

# # Preserve original values for the specified range
# values = [0, slope, 0]


# # Initialize an empty array for the final result
# result_slope = np.zeros_like(slope, dtype=np.float32)

# # Iterate over chunks of the array
# chunk_size = 100  # Adjust the chunk size as needed
# num_chunks = len(range(0, slope.shape[0], chunk_size))

# # Create a tqdm progress bar
# for i, start_idx in tqdm(enumerate(range(0, slope.shape[0], chunk_size)), total=num_chunks, desc='Processing'):
#     end_idx = min(start_idx + chunk_size, slope.shape[0])
    
#     # Apply conditions to the chunk
#     chunk_result = np.select(conditions, values, default=0)

#     # Update the result array with the processed chunk
#     result_slope[start_idx:end_idx, :, :] = chunk_result


# # Save the result
# with rasterio.open('D:\PhD_TAMU\Courses\GEOG 676 GIS Programming\Group Project\Data\Raster\Slope_reclass.tif', 'w',
#                    driver=slope_raster.driver,
#                    height=slope_raster.height,
#                    width=slope_raster.width,
#                    count=slope_raster.count,
#                    crs=slope_raster.crs,
#                    transform=slope_raster.transform,
#                    dtype=data.dtype

# ) as dst:
#     dst.write(result_slope)

# print("Processing complete. Result saved to: {output_path}")


##.................... Normalizing Slope value ....................

# # Normalizing Slop value

# # Open the raster dataset
# slope1 = rasterio.open('D:/OneDrive - Texas A&M University/PhD/PhD_Courses/GEOG 676 GIS Programming/Group Project/Data/Raster/Slope_reclass.tif')

# # Get metadata
# profile = slope1.profile
# dtype = slope1.dtypes[0]

# # Create a tqdm progress bar
# with tqdm(total=100, desc='Writing Normalized Slope') as pbar:
#     # Calculate the total number of blocks
#     total_blocks = slope1.count * slope1.height // slope1.block_shapes[0][0]

#     # Iterate over windows (blocks) of the raster
#     for _, window in slope1.block_windows():

#         # Read the data for the current window
#         slope_data = slope1.read(window=window)

#         # Calculate the min and max values for the current window
#         slope_min_value = np.min(slope_data)
#         slope_max_value = np.max(slope_data)

#         # Normalize the data for the current window
#         normalized_slope = (slope_data - slope_min_value) / (slope_max_value - slope_min_value)

#         # Write the normalized data to the output raster
#         with rasterio.open('D:/OneDrive - Texas A&M University/PhD/PhD_Courses/GEOG 676 GIS Programming/Group Project/Data/Raster/normalized_slope.tif', 'w',
#                            **profile) as dst:
#             dst.write(normalized_slope, window=window)

#         # Update the progress bar
#         pbar.update(100 / total_blocks)

# print("Slope Normalization is complete.")



##.................... Normalizing GHI value ....................

# # Open the shapefile
# with fiona.open("D:\PhD_TAMU\Courses\GEOG 676 GIS Programming\Group Project\Data\Shp/TexasState.shp", "r") as shapefile:
#     shapes = [shape(feature["geometry"]) for feature in shapefile]

# # Open the GHI raster
# ghi_path = "D:\PhD_TAMU\Courses\GEOG 676 GIS Programming\Group Project\Data\Raster/GHI.tif"
# ghi_output_path = "D:\PhD_TAMU\Courses\GEOG 676 GIS Programming\Group Project\Data\Raster/normalized_GHI.tif"

# with rasterio.open(ghi_path) as src:
#     # Create a timestamp for the output filename
#     timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

#     # Set the output filename with a timestamp
#     masked_output_filename = f'D:\PhD_TAMU\Courses\GEOG 676 GIS Programming\Group Project\Data\Raster/GHI_masked_{timestamp}.tif'

#     # Open the output file for writing masked GHI
#     with rasterio.open(masked_output_filename, 'w', **src.profile) as dest:
#         for geom in tqdm(shapes, desc='Masking GHI'):
#             out_image, out_transform = mask(src, [geom], crop=True)
#             dest.write(out_image)

# # Open the masked GHI raster
# masked_ghi = rasterio.open(masked_output_filename)
# masked_ghi_data = masked_ghi.read()

# # Replace NaN values with a default value (e.g., 0)
# masked_ghi_data = np.nan_to_num(masked_ghi_data, nan=0)

# # Calculate the min and max values
# ghi_min_value = np.min(masked_ghi_data)
# ghi_max_value = np.max(masked_ghi_data)

# # Check if min and max are equal
# if ghi_min_value == ghi_max_value:
#     # Set all values to a default value (e.g., 0 or 1)
#     normalized_ghi = np.ones_like(masked_ghi_data) * 0  # You can change 0 to any default value
# else:
#     # Normalize the masked GHI data with a progress bar
#     with tqdm(total=100, desc='Normalizing GHI') as pbar:
#         normalized_ghi = np.zeros_like(masked_ghi_data, dtype=np.float32)
#         for i in tqdm(range(masked_ghi_data.shape[1]), desc='Normalization Progress'):
#             for j in range(masked_ghi_data.shape[2]):
#                 normalized_ghi[:, i, j] = (masked_ghi_data[:, i, j] - ghi_min_value) / (ghi_max_value - ghi_min_value)
#             pbar.update(100 / masked_ghi_data.shape[1])

# print("GHI Min Value:", ghi_min_value)
# print("GHI Max Value:", ghi_max_value)
# print("Normalized GHI:", normalized_ghi)

# # Create a timestamp for the normalized output filename
# normalized_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# # Set the output filename with a timestamp
# normalized_output_filename = f'D:\PhD_TAMU\Courses\GEOG 676 GIS Programming\Group Project\Data\Raster/normalized_GHI_{normalized_timestamp}.tif'

# # Write the normalized GHI data to a new raster file
# with rasterio.open(normalized_output_filename, 'w', **masked_ghi.profile) as dst:
#     dst.write(normalized_ghi)

# print("GHI Masking and Normalization is complete. Output saved to:", normalized_output_filename)


# ##.................... Normalizing Temperature data ....................
# def normalize_and_write_temperature(temp_path, output_directory):
#     # Open the raster dataset
#     with rasterio.open(temp_path) as src:
#         # Get metadata
#         profile = src.profile
#         dtype = src.dtypes[0]

#         # Create a tqdm progress bar
#         with tqdm(total=100, desc='Normalizing Temperature') as pbar:
#             # Calculate the total number of blocks
#             total_blocks = src.count * src.height // src.block_shapes[0][0]

#             # Iterate over windows (blocks) of the raster
#             for _, window in src.block_windows():

#                 # Read the data for the current window
#                 temp_chunk = src.read(window=window)

#                 # Calculate the min and max values for the current window
#                 min_value = np.min(temp_chunk)
#                 max_value = np.max(temp_chunk)

#                 # Normalize the data for the current window
#                 normalized_chunk = (temp_chunk - min_value) / (max_value - min_value)

#                 # Write the normalized data to the output raster
#                 with rasterio.open(f'{output_directory}/normalized_Temp_final.tif', 'w', **profile) as dst:
#                     dst.write(normalized_chunk, window=window)

#                 # Update the progress bar
#                 pbar.update(100 / total_blocks)

#     print("Temperature Normalization is complete.")

# # Path to the temperature raster file
# temp_path = 'D:\PhD_TAMU\Courses\GEOG 676 GIS Programming\Group Project\Data\Raster/Temperature.tif'

# # Path to the directory where normalized temperature file will be saved
# output_directory = 'D:\PhD_TAMU\Courses\GEOG 676 GIS Programming\Group Project\Data\Raster/'

# # Normalize temperature data
# normalize_and_write_temperature(temp_path, output_directory)


# ##.................... Normalizing Precipitation data ...................
# def normalize_and_write_precipitation(prep_path, output_directory):
#     # Open the raster dataset
#     with rasterio.open(prep_path) as src:
#         # Get metadata
#         profile = src.profile

#         # Create a tqdm progress bar
#         with tqdm(total=100, desc='Normalizing Precipitation', position=0, leave=True) as pbar:
#             # Calculate the total number of blocks
#             total_blocks = src.count * src.height // src.block_shapes[0][0]

#             # Create an empty array to accumulate values across all blocks
#             total_data = np.zeros((src.count, src.height, src.width), dtype=src.dtypes[0])

#             # Iterate over windows (blocks) of the raster
#             for i, (_, window) in enumerate(src.block_windows()):
#                 # Read the data for the current window
#                 prep_chunk = src.read(window=window)

#                 # Accumulate values across blocks
#                 total_data[:, window.row_off: window.row_off + window.height, window.col_off: window.col_off + window.width] += prep_chunk

#                 # Calculate the progress percentage
#                 progress_percent = i / total_blocks * 100

#                 # Update the tqdm progress bar
#                 pbar.update(progress_percent - pbar.n)

#             # Normalize the data for the entire raster
#             min_value = np.min(total_data)
#             max_value = np.max(total_data)
#             normalized_data = (total_data - min_value) / (max_value - min_value)

#             # Write the normalized data to the output raster
#             with rasterio.open(f'{output_directory}/normalized_Prep_final.tif', 'w', **profile) as dst:
#                 dst.write(normalized_data)

#         # Close the tqdm progress bar
#         pbar.close()

#     print("\nPrecipitation Normalization is complete.")

# # Path to the precipitation raster file
# prep_path = 'D:\PhD_TAMU\Courses\GEOG 676 GIS Programming\Group Project\Data\Raster/Precipitation.tif'

# # Path to the directory where normalized precipitation file will be saved
# output_directory = 'D:\PhD_TAMU\Courses\GEOG 676 GIS Programming\Group Project\Data\Raster/'

# #Normalize precipitation data
# normalize_and_write_precipitation(prep_path, output_directory)


# ##................... Solar suitable area identificaiton ...................

# prep = rasterio.open('D:\PhD_TAMU\Courses\GEOG 676 GIS Programming\Group Project\Data\Raster/normalized_Prep.tif')
# temp = rasterio.open('D:\PhD_TAMU\Courses\GEOG 676 GIS Programming\Group Project\Data\Raster/normalized_Temp.tif')
# lulc = rasterio.open('D:\PhD_TAMU\Courses\GEOG 676 GIS Programming\Group Project\Data\Raster/normalized_LULC.tif')
# ghi = rasterio.open('D:\PhD_TAMU\Courses\GEOG 676 GIS Programming\Group Project\Data\Raster/normalized_GHI.tif')
# slope = rasterio.open('D:\PhD_TAMU\Courses\GEOG 676 GIS Programming\Group Project\Data\Raster/normalized_slope.tif')

# prep_data = prep.read()
# temp_data = temp.read()
# lulc_data = lulc.read()
# ghi_data = ghi.read()
# slope_data = slope.read()

# suitable_area = temp_data+lulc_data+ghi_data+slope_data-prep_data

# with rasterio.open('D:\PhD_TAMU\Courses\GEOG 676 GIS Programming\Group Project\Data\Raster/suitable_area.tif', 'w',
#                    driver=prep.driver,
#                    height=prep.height,
#                    width=prep.width,
#                    count=prep.count,
#                    crs=prep.crs,
#                    transform=prep.transform,
#                    dtype=prep_data.dtype

# ) as dst:
#       dst.write(suitable_area)


# # Normalization of the Suibtale area

# suitableArea = rasterio.open('D:\PhD_TAMU\Courses\GEOG 676 GIS Programming\Group Project\Data\Raster/suitable_area.tif')
# suitableArea_data = suitableArea.read()
# suitableArea_min_value = np.min(suitableArea_data)
# suitableArea_max_value = np.max(suitableArea_data)
# print(suitableArea_min_value)
# print(suitableArea_max_value)

# normalized_suitableArea = (suitableArea_data - suitableArea_min_value) / (suitableArea_max_value - suitableArea_min_value)
# print(normalized_suitableArea) 

# with rasterio.open('D:\PhD_TAMU\Courses\GEOG 676 GIS Programming\Group Project\Data\Raster/normalized_suitableArea.tif', 'w',
#                    driver=suitableArea.driver,
#                    height=suitableArea.height,
#                    width=suitableArea.width,
#                    count=suitableArea.count,
#                    crs=suitableArea.crs,
#                    transform=suitableArea.transform,
#                    dtype=suitableArea_data.dtype

# ) as dst:
#       dst.write(normalized_suitableArea)



