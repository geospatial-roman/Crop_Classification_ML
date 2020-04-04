import rasterio
import numpy as np
from rasterio.mask import mask
import os
from skimage import measure
import matplotlib.patches as patches
from matplotlib.lines import Line2D
import matplotlib as mpl
from matplotlib import cm


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


class LegendHelper:

    def __init__(self):

        self.patch_legend = [
                   patches.Patch(facecolor=[0,0,0,0], edgecolor='r', linewidth =3,
                         label='Training Area'),
                    patches.Patch(facecolor=[0,0,0,0], edgecolor='b', linewidth =3,
                         label='Test Area'),
                    patches.Patch(facecolor=cm.viridis(1/5), edgecolor=cm.viridis(1/5),
                         label='Corn'),
                    patches.Patch(facecolor=cm.viridis(2/5), edgecolor=cm.viridis(2/5),
                         label='Dry Beans'),
                    patches.Patch(facecolor=cm.viridis(3/5), edgecolor=cm.viridis(3/5),
                         label='Soy Beans'),
                    patches.Patch(facecolor=cm.viridis(4/5), edgecolor=cm.viridis(4/5),
                         label='Sugar Beets'),
                    patches.Patch(facecolor=cm.viridis(5/5), edgecolor=cm.viridis(5/5),
                         label='Spring Wheat')
                         ]

        self.line_legend = [
                    Line2D([0], [0], color=cm.viridis(1/5), lw=2, label='Corn'),
                    Line2D([0], [0], color=cm.viridis(2/5), lw=2, label='Dry Beans'),
                    Line2D([0], [0], color=cm.viridis(3/5), lw=2, label='Soy Beans'),
                    Line2D([0], [0], color=cm.viridis(4/5), lw=2, label='Sugar Beets'),
                    Line2D([0], [0], color=cm.viridis(5/5), lw=2, label='Spring Wheat'),

        ]