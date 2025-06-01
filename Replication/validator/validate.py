import os

from config import config
from utils.utils import create_folder_if_not_exist


def validate_openjml(code_with_spec, classname):
    create_folder_if_not_exist(os.path.abspath(".") + "/tmp")
    tmp_filename = os.path.abspath(".") + "/tmp/{filename}.java".format(
        filename=classname
    )
    tmp_file = open(tmp_filename, "w")
    tmp_file.write(code_with_spec)
    tmp_file.close()
    cmd = (
        os.path.abspath(".")
        + "/openjml/openjml --esc --esc-max-warnings={max_warning} --arithmetic-failure=quiet --nonnull-by-default --timeout={timeout_seconds} --quiet -nowarn --prover={prover} ".format(
            max_warning=config.get("max_warning", 1),
            prover=config.get("prover", "z3"),
            timeout_seconds=config.get("validator_timeout", 180),
        )
        + tmp_filename
    )
    res_lines = os.popen(cmd).readlines()
    res = ""
    for line in res_lines:
        res = res + line
    if len(res) == 0:
        print("no error found by validator!")
    return res
