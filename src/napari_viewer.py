import argparse
import dask_zarr as dz
import napari


def main(z_url):

    # Test example, knowing that the file contains only 3 groups, 
    # and at most 10 scales
    plane_names_scale = [['%s/%s' % (r, s) for r in [0]] for s in range(10)]

    # Retrieve a list of stacks to form the pyramid representation of the image
    stack_list = [
        dz.get_lazy_stacks(z_url, plane_names) 
        for plane_names in plane_names_scale
    ]

    viewer = napari.Viewer()
    img = viewer.add_image(stack_list, multiscale=True)
    napari.run()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-z', '--zurl', dest='z_url', type=str,
                        help='Path or url to a zarr file')

    args = parser.parse_args()

    main(args.z_url)
