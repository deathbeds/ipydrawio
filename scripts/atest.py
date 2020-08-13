""" Run acceptance tests with robot framework
"""
# pylint: disable=broad-except
import os
import shutil
import sys
import time
from os.path import join

import robot

from . import project as P

# sets of tags to be combined with AND, marked as non-critical
NON_CRITICAL = []


def get_stem(attempt, extra_args):
    stem = "_".join([P.PLATFORM, P.PY_MAJOR, str(attempt)]).replace(".", "_").lower()

    if "--dryrun" in extra_args:
        stem = f"dry_run_{stem}"

    return stem


def atest(attempt, extra_args):
    """ perform a single attempt of the acceptance tests
    """

    if "FIREFOX_BINARY" not in os.environ:
        os.environ["FIREFOX_BINARY"] = shutil.which("firefox")

        prefix = os.environ.get("CONDA_PREFIX")

        if prefix:
            app_dir = join(prefix, "bin", "FirefoxApp")
            os.environ["FIREFOX_BINARY"] = {
                "Windows": join(prefix, "Library", "bin", "firefox.exe"),
                "Linux": join(app_dir, "firefox"),
                "Darwin": join(app_dir, "Contents", "MacOS", "firefox"),
            }[P.PLATFORM]

    print("Will use firefox at", os.environ["FIREFOX_BINARY"])

    assert os.path.exists(os.environ["FIREFOX_BINARY"])

    stem = get_stem(attempt, extra_args)

    for non_critical in NON_CRITICAL:
        extra_args += ["--noncritical", "AND".join(non_critical)]

    if attempt != 1:
        previous = P.ATEST_OUT / f"{get_stem(attempt - 1, extra_args)}.robot.xml"
        if previous.exists():
            extra_args += ["--rerunfailed", str(previous)]

    out_dir = P.ATEST_OUT / stem

    args = [
        "--name",
        f"{P.PLATFORM}{P.PY_MAJOR}",
        "--outputdir",
        out_dir,
        "--output",
        P.ATEST_OUT / f"{stem}.robot.xml",
        "--log",
        P.ATEST_OUT / f"{stem}.log.html",
        "--report",
        P.ATEST_OUT / f"{stem}.report.html",
        "--xunitskipnoncritical",
        "--xunit",
        P.ATEST_OUT / f"{stem}.xunit.xml",
        "--variable",
        f"OS:{P.PLATFORM}",
        "--variable",
        f"PY:{P.PY_MAJOR}",
        "--randomize",
        "all",
        *(extra_args or []),
        P.ATEST,
    ]

    print("Robot Arguments\n", " ".join(["robot"] + list(map(str, args))))

    os.chdir(P.ATEST)

    if out_dir.exists():
        print("trying to clean out {}".format(out_dir))
        try:
            shutil.rmtree(out_dir)
        except Exception as err:
            print("Error deleting {}, hopefully harmless: {}".format(out_dir, err))

    try:
        robot.run_cli(list(map(str, args)))
        return 0
    except SystemExit as err:
        return err.code


def attempt_atest_with_retries(*extra_args):
    """ retry the robot tests a number of times
    """
    attempt = 0
    error_count = -1

    retries = int(os.environ.get("ATEST_RETRIES") or "0")

    while error_count != 0 and attempt <= retries:
        attempt += 1
        print("attempt {} of {}...".format(attempt, retries + 1))
        start_time = time.time()
        error_count = atest(attempt=attempt, extra_args=list(extra_args))
        print(error_count, "errors in", int(time.time() - start_time), "seconds")

    return error_count


if __name__ == "__main__":
    sys.exit(attempt_atest_with_retries(*sys.argv[1:]))
