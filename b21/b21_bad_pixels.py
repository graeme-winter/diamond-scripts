import sys
import numpy
import h5py
import bitshuffle

from dials.array_family import flex

from dials.algorithms.spot_finding.threshold import DispersionThresholdStrategy


def signal(mask, image):
    thresholder = DispersionThresholdStrategy(gain=1)
    threshold_mask = thresholder(image, mask=mask)
    return threshold_mask


def main():
    args = sys.argv[1:]
    meta, data = args[0:2]

    with h5py.File(meta, "r") as f:
        mask = f["/mask"][()]
        bitmask = flex.int(mask) == 0

    total = None
    with h5py.File(data, "r") as f:
        d_id = f["/data"].id
        nz, ny, nx = f["/data"].shape
        dt = f["/data"].dtype

        for j in range(nz):
            offset = (j, 0, 0)
            filter_mask, chunk = d_id.read_direct_chunk(offset)
            blob = numpy.fromstring(chunk[12:], dtype=numpy.uint8)
            image = bitshuffle.decompress_lz4(blob, (ny, nx), dt)
            image = flex.int(image.astype("int32"))
            signal_pixels = signal(bitmask, image)
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
