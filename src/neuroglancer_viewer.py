import numpy as np
import argparse
import dask_zarr as dz

import neuroglancer.server as ngs
import neuroglancer
import neuroglancer.cli

import os

# Make the server accessible through a given ip
HOST_IP = os.getenv('HOSTNAME_IP')
if HOST_IP is not None:
    ngs.stop()
    ngs.global_server_args = dict(bind_address=HOST_IP, bind_port=0)
    ngs.start()


def main(z_url, state):
    # Test example, knowing that the file contains only 3 groups, 
    # and at most 10 scales
    plane_names_scale = [['%s/%s' % (r, s) for r in [0]] for s in range(10)]

    # Retrieve a list of stacks to form the pyramid representation of the image
    stack_list = [
        dz.get_lazy_stacks(z_url, plane_names) 
        for plane_names in plane_names_scale
    ]

    x0 = stack_list[0][0, 0, :, 0]
    x1 = stack_list[1][0, 0, :, 0]
    x2 = stack_list[2][0, 0, :, 0]
    
    state.dimensions = neuroglancer.CoordinateSpace(
                                    names=["c", "x", "y"], 
                                    units=["", "nm", "nm"],
                                    scales=[1, 1, 1]
                                    )

    state.layers['dask_s2'] = neuroglancer.ImageLayer(
        source=neuroglancer.LocalVolume(x2, 
            dimensions=neuroglancer.CoordinateSpace(
                names=["z", "x", "y"], 
                units=["nm", "nm", "nm"],
                scales=[1, 4, 4]), 
            voxel_offset=[0, 0, 0]))
    
    state.layers['dask_s1'] = neuroglancer.ImageLayer(
        source=neuroglancer.LocalVolume(x1, 
            dimensions=neuroglancer.CoordinateSpace(
                names=["z", "x", "y"], 
                units=["nm", "nm", "nm"],
                scales=[1, 2, 2]), 
            voxel_offset=[0, 0, 0]))
    state.layers['dask_s1'].visible = False

    state.layers['dask_s0'] = neuroglancer.ImageLayer(
        source=neuroglancer.LocalVolume(x0, 
        dimensions=neuroglancer.CoordinateSpace(
            names=["z", "x", "y"], 
            units=["nm", "nm", "nm"], 
            scales=[1, 1, 1])))
    state.layers['dask_s0'].visible = False
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-z', '--zurl', dest='z_url', type=str,
                        help='Path or url to a zarr file')

    neuroglancer.cli.add_server_arguments(parser)
    args = parser.parse_args()
    
    neuroglancer.cli.handle_server_arguments(args)

    viewer = neuroglancer.Viewer()
    with viewer.txn() as s:
        main(args.z_url, s)

    print(viewer)
