import rasterio
import numpy as np
from rasterio.mask import mask
import os
from skimage import measure


class RasterHelper:

    def __init__(self):

        self.n = 0

    
    # Normalize bands into 0.0 - 1.0 scale

    def normalize(self, array):
        array_min, array_max = array.min(), array.max()
        return (array - array_min) / (array_max - array_min)


    def open_multiband_scene(self, directory, aoi, pooling=False):


        # loop over directory and open all single band tiffs
        multiband_array = []

        for _, dirs, _ in os.walk(directory):
            for dir in dirs:
                multiband =  []
                for filename in os.listdir(os.path.join(directory, dir)):
                    #check if file is a tiff
                    if filename.endswith(".tiff"): 
                        file_path = os.path.join(directory, dir, filename)
                        # open multiband tiff using Rasterio
                        raster = rasterio.open(file_path)

                        # clip to extent
                        out_img, _ = mask(raster, shapes=aoi, crop=True)

                        # normalize
                        band = self.normalize(out_img[0])

                        #pool pixels 
                        if pooling:
                            band = measure.block_reduce(band, (4,4), np.max)

                        # append to multiband list
                        band = np.where(band == 0, np.nan, band)
                        multiband.append(band)
                        raster.close()

                multiband_array.append(np.asarray(multiband, dtype=float))

        print(f" Files were loaded sucessfully. " )

        return multiband_array