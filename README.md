# HCS_visualization_tools
Tools to visualize HCS data stored in zarr files.
The tools work locally or can be run in a remote server.

## Visualization options

### Lazy data loading
The [dask](https://dask.org/) package is used to retrieve the HCS data from [zarr](https://zarr.readthedocs.io/en/stable/#) files.
This allows to visualize large scale images without the need to fully load them in memory.

### Using napari
[Napari]( https://napari.org/) is a multi-dimensional viewer that displays numpy arrays as images.
This package can be easily extended to integrate more functionalities.
#### Example usage
```
python ./src/napari_viewer.py -z HCS_image.zarr
```
#### Running napari in a server
To run the viewer from a server, build and shell into the container defined by **hcs_zarr_viewers.def**.
The server must allow **X11** forwarding to open the viewer.

### Using neuroglancer
[Neuroglancer](https://github.com/google/neuroglancer) is a web-based volumetric data viewer.
It can be used to visualize three-dimensional data. The limitation of working with **zarr** files is that neuroglancer requires more coding to work with the pyramid representation that **zarr** offers.
#### Example usage
To use the viewer based on neuroglancer, run it in interactive mode. Otherwise, the web environment will be closed before it can be used.
At running the viewer, it will print an url path that can be pasted in the browser.
```
python -i ./src/neuroglancer_viewer.py -z HCS_image.zarr
```
#### Running neuroglancer in a server
To run the neuroglancer viewer from a server, build and shell into the container defined by **hcs_zarr_viewers.def**.
Before running the code, export the environment variable **HOSTNAME_IP** to point to the server’s IP.
```
export HOSTNAME_IP=$(hostname -i)
```

### Using vizarr
[Vizarr](https://github.com/hms-dbmi/vizarr) is a minimal viewer to display **zarr** inside **jupyter** notebooks.
To use vizarr, it is needed to install de [ImJoy Jupyter extension](https://github.com/imjoy-team/imjoy-jupyter-extension).
#### Example usage
The ```imjoy_viewer.ipynb``` notebook provides an example of HCS data visualization in Jupyter.
#### Running vizarr in a server
For now, vizarr cannot be used in a jupyter notebook hosted in a remote server. To do so, it would be necessary to modify the container definition to allow the ImJoy Jupyter extension installation.

# Limitations
The example codes provded in this repository work with images stored in **zarr** files.
For now, the groups selecetion is hardcoded, so only the group **'0'** is accessible.
This could be improved by inspecting the structure of the zarr file and identifying the groups structure.
