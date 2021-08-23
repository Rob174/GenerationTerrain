import matplotlib.pyplot as plt
import numpy as np
import rasterio
from numba import jit
from numpy.lib.stride_tricks import sliding_window_view

# @jit(nopython=True)
def window(arr, shape=(3, 3)):

    # Find row and column window sizes
    r_win = int(np.floor(shape[0] / 2))
    c_win = int(np.floor(shape[1] / 2))
    x, y = arr.shape
    for i in range(x):
        xmin = max(0, i - r_win)
        xmax = min(x, i + r_win + 1)
        for j in range(y):
            ymin = max(0, j - c_win)
            ymax = min(y, j + c_win + 1)
            yield arr[xmin:xmax, ymin:ymax]




class FlowProcessor:
    def __init__(self, array):
        self.array = array
        self.flow_directions = np.zeros(self.array.shape)
        self.constant_position = 4

    @staticmethod
    # @jit(parallel=True)
    def numba_create_flow_directions(array,height,width,flow_directions):
        windows = window(array, (3, 3))
        for i in range(height):
            for j in range(width):
                window_flow = next(windows)
                flow_directions[i, j] = np.argmin(window_flow)
    def create_flow_directions(self):
        return FlowProcessor.numba_create_flow_directions(self.array,*self.array.shape,self.flow_directions)

    def one_step_rainfall(self,previous_array_rain):
        return FlowProcessor.numba_one_step_rainfall(previous_array_rain,self.flow_directions,*self.flow_directions.shape)

    @staticmethod
    @jit(parallel=True)
    def numba_one_step_rainfall(previous_array_rain,flow_directions,height,width):
        windows_flow = window(flow_directions, (3, 3))
        windows_array = window(array, (3, 3))
        result = np.zeros((height,width))

        kernel_add = np.arange(8,-1,-1).reshape((3,3))
        for i in range(height):
            for j in range(width):
                window_flow = next(windows_flow)
                window_array = next(windows_array)
                wflow = window_flow
                to_add = wflow[wflow == kernel_add]
                win_val_flat = window_array.flatten()
                add = 0
                for id in to_add:
                    if win_val_flat[int(id)] > 0:
                        add += 1
                result[i, j] = max(0, previous_array_rain[i, j] + add - int(flow_directions[i, j] != 4)) + 1
        return result


if __name__ == '__main__':
    array = rasterio.open(r"C:\Users\robin\Documents\projets\GenerationTerrain\data_raw\geotiff\0.tiff").read(1)
    flow = FlowProcessor(array)
    flow.create_flow_directions()
    plt.figure(1)
    plt.title(f"Source")
    plt.imshow(array, cmap="viridis")

    plt.figure(2)
    plt.title(f"Flow")
    plt.imshow(flow.flow_directions, cmap="viridis")
    array_rain = np.ones(array.shape)
    for step in range(10):
        print(f"{step=}", end="\r")
        array_rain = flow.one_step_rainfall(array_rain)

    plt.figure(3)
    plt.title(f"Rain end")
    plt.imshow(array_rain, cmap="viridis")
    plt.show()
    s = 0
