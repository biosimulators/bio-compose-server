import os

import biosimulators_pysces as bp
import biosimulators_masspy as bm
from kisao import AlgorithmSubstitutionPolicy
from biosimulators_utils.config import Config


fp = "test_fixtures/Elowitz-Nature-2000-Repressilator.omex"
# config = Config(ALGORITHM_SUBSTITUTION_POLICY=AlgorithmSubstitutionPolicy.SAME_FRAMEWORK)


def test_pysces(config=None):
    return bp.exec_sedml_docs_in_combine_archive(fp, "./outputs")


def test_masspy(config=None):
    return bm.exec_sedml_docs_in_combine_archive(fp, "./outputs")
