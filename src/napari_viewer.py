import argparse
import numpy as np
import dask.array as da
import napari
import zarr


def show_image(z_url, group):
    z = zarr.open(z_url, mode="r")['%s' % group]

    pyr = []
    for r in z.keys():
        pyr.append(np.moveaxis(da.from_zarr(z['%s' % r])[0, :, 0, ...], 0, -1))

    v = napari.view_image(pyr, multiscale=True, rgb=True)
    napari.run()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-z', '--zurl', dest='z_url', type=str,
                        help='Path or url to a zarr file')
    parser.add_argument('-g', '--group', dest='group', type=str,
                        help='Group stored inside the zarr file')

    args = parser.parse_args()

    show_image(args.z_url, args.group)
