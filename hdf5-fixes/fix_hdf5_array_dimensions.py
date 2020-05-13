import h5py
import sys
import os
import bitshuffle.h5

def fix_hdf5_array_dimensions(in_filename):
    with h5py.File(in_filename, "r+") as f:
        data = f["/data"]
        filter_info = data.id.get_create_plist().get_filter(0)
        nn = data.shape[0]
        last = 0
        for j in range(nn):
            offset = (j, 0, 0)
            try:
                filter_mask, chunk = data.id.read_direct_chunk(offset)
            except RuntimeError:
                last = j
                break

        print("True vs. claimed size: %d vs. %d" % (nn, last))

        data.resize(last, axis=0)

if __name__ == "__main__":
    fix_hdf5_array_dimensions(sys.argv[1])
