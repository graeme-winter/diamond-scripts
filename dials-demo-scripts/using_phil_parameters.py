from dials.util.options import OptionParser
from dials.util.options import flatten_experiments

import iotbx.phil

phil_scope = iotbx.phil.parse(
    """
image_range = None
  .type = ints(value_min=0, size=2)
  .help = "Image range for analysis e.g. 1,1800"
"""
)


def do_thing():
    parser = OptionParser(
        phil=phil_scope, read_experiments=True, read_experiments_from_images=True
    )

    # parse user's command line arguments, including parameters, show diffs
    params, options = parser.parse_args(show_diff_phil=True)

    experiments = flatten_experiments(params.input.experiments)

    if len(experiments) != 1:
        parser.print_help()
        sys.exit("Please pass images\n")
        return

    imagesets = experiments.imagesets()

    if len(imagesets) != 1:
        sys.exit("Please pass only one set of images")

    imageset = imagesets[0]

    if params.image_range:
        print("Image range set to: %d %d" % tuple(params.image_range))
        image_range = params.image_range
    else:
        image_range = 0, len(imageset)

    for j in range(*image_range):
        print(j)


if __name__ == "__main__":
    do_thing()
