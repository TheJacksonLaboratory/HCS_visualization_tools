from dask import delayed
import dask.array as da


def get_from_file(url, plane_names):
    dask_arrays_list = [da.from_zarr(url, component=plane) for plane in plane_names]
    return dask_arrays_list


def get_lazy_stacks(z, plane_names):
    if isinstance(z, str):
        lazy_arrays = get_from_file(z, plane_names=plane_names)
    else:
        raise TypeError('Z must be the path/url to a zarray')

    return da.stack(lazy_arrays, axis=0)
