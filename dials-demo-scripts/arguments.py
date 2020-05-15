import argparse
import glob

from libtbx.phil import parse
from dxtbx.model.experiment_list import ExperimentListFactory

master_phil = parse(
    """
  input {
    experiments = None
      .type = path
      .multiple = True
    reflections = None
      .type = path
      .multiple = True
  }

  foo = 10
    .type = int
  bar = None
    .type = str

  output {
    experiments = None
      .type = path
      .multiple = True
    reflections = None
      .type = path
      .multiple = True
  }
"""
)


class ArgumentSlayer(object):
    """Thin wrapper around argparse and phil to get DIALS arguments
    parsed without actually loading all the data files."""

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--debug", action="store_const", const=True)
        parser.add_argument("phil", nargs="+")

        args = parser.parse_args()

        debug = args.debug

        clai = master_phil.command_line_argument_interpreter()
        self._working_phil = master_phil.fetch(clai.process_and_fetch(args.phil))
        self._params = self._working_phil.extract()

        self._input_experiments = None
        self._input_reflections = None

    def __repr__(self):
        return self._working_phil.format(python_object=self._params).as_str()

    def input_experiments(self):
        if self._input_experiments:
            return self._input_experiments
        input_experiments = sum(map(glob.glob, self._params.input.experiments), [])
        self._input_experiments = ExperimentListFactory.from_filenames(
            input_experiments
        )

        return self._input_experiments

    def input_experiment_names(self):
        return sum(map(glob.glob, self._params.input.experiments), [])


if __name__ == "__main__":
    slayer = ArgumentSlayer()
    print(slayer)
    experiments = slayer.input_experiments()
    for expt in experiments:
        print(expt)
