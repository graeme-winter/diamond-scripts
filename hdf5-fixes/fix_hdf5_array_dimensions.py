import h5py
import sys
import os


def fix_hdf5_array_dimensions(in_filename, out_filename):
    "Read each chunk; report size or error." ""

    assert os.path.exists(in_filename)
    assert not os.path.exists(out_filename)

    with h5py.File(in_filename, "r") as f:
        data = f["/data"]
        nn = data.shape[0]
        ny, nx = data.shape[1:3]
        last = 0
        for j in range(nn):
            offset = (j, 0, 0)
            try:
                filter_mask, chunk = data.id.read_direct_chunk(offset)
            except RuntimeError:
                last = j
                break

        print("True vs. claimed size: %d vs. %d" % (nn, last))

        with h5py.File(out_filename, "w") as fout:
            dout = fout.create_dataset("data", (last, ny, nx), chunks=(1, ny, nx))
            for j in range(last):
                offset = (j, 0, 0)
                filter_mask, chunk = data.id.read_direct_chunk(offset)
                dout.id.write_direct_chunk(offset, chunk, filter_mask)
            print("Wrote %d chunks to %s" % (last, out_filename))


if __name__ == "__main__":
    fix_hdf5_array_dimensions(sys.argv[1], sys.argv[2])
