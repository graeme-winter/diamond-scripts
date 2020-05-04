from dials.util.options import OptionParser
from dials.util.options import flatten_experiments
from dials.array_family import flex


def read_data():
    parser = OptionParser(read_experiments=True, read_experiments_from_images=True)

    # trivial parameter list... but an easy way for generic access to images
    params, options = parser.parse_args(show_diff_phil=False)

    experiments = flatten_experiments(params.input.experiments)

    if len(experiments) != 1:
        parser.print_help()
        sys.exit("Please pass images\n")
        return

    imagesets = experiments.imagesets()

    if len(imagesets) != 1:
        sys.exit("Please pass only one set of images")

    imageset = imagesets[0]

    for j in range(len(imageset)):
        # in general the detector image is made up of separate panels -
        # in most case there will be exactly one however allow in this
        # structure for multi-panel detectors - image and mask here are
        # tuples

        image = imageset[j]
        mask = imageset.get_mask(j)

        # count negative pixels and the total of positive pixels
        negative = 0
        total = 0

        for panel, panel_mask in zip(image, mask):
            negative += (~panel_mask).count(True)
            total += flex.sum(panel.as_1d().select(panel_mask.as_1d()))

        print("%d %d %d" % (j + 1, negative, total))


if __name__ == "__main__":
    read_data()
