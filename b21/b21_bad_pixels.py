import sys
import numpy
import h5py
import bitshuffle

from dials.array_family import flex

from dials.algorithms.spot_finding.threshold import DispersionThresholdStrategy


def chunk_read_image(d_id, image_number):
    offset = (image_number, 0, 0)
    filter_mask, chunk = d_id.read_direct_chunk(offset)
    blob = numpy.fromstring(chunk[12:], dtype=numpy.uint8)
    image = bitshuffle.decompress_lz4(blob, (ny, nx), dt)
    flex_image = flex.int(image.astype("int32"))
    return flex_image


def main():
    args = sys.argv[1:]
    meta, data = args[0:2]

    with h5py.File(meta, "r") as f:
        mask = f["/mask"][()]
        bitmask = flex.int(mask) == 0

    thresholder = DispersionThresholdStrategy(gain=1)

    total = None
    with h5py.File(data, "r") as f:
        d_id = f["/data"].id
        nz, ny, nx = f["/data"].shape
        dt = f["/data"].dtype

        for j in range(nz):
            image = chunk_read_image(d_id, j)
            signal_pixels = thresholder(image, mask=mask)

            if total is None:
                total = signal_pixels.as_1d().as_int()
            else:
                total += signal_pixels.as_1d().as_int()

    hot_mask = total >= (nz // 2)
    hot_pixels = hot_mask.iselection()

    for h in hot_pixels:
        print("    mask[%d, %d] = 8" % (h % nx, h // nx))


if __name__ == "__main__":
    main()
