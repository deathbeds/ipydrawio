import shutil
import subprocess
import sys
import time

from . import project as P

PABOT_DEFAULTS = [
    "--testlevelsplit",
    "--processes",
    "4",
    "--artifactsinsubfolders",
    "--artifacts",
    "png,log,txt,drawio,xml",
]


def run_tests(attempt=0, extra_args=None):
    extra_args = extra_args or []

    stem = P.get_atest_stem(attempt=attempt, extra_args=extra_args)
    out_dir = P.ATEST_OUT / stem

    if attempt > 1:
        prev_stem = P.get_atest_stem(attempt=attempt - 1, extra_args=extra_args)
        previous = P.ATEST_OUT / prev_stem / P.ATEST_OUT_XML
        if previous.exists():
            extra_args += ["--rerunfailed", str(previous)]

    runner = ["pabot", *PABOT_DEFAULTS]

    if "--dryrun" in extra_args:
        runner = ["robot"]

    args = [
        *runner,
        *extra_args,
        "--name",
        f"""{P.PLATFORM} py{P.PY_MAJOR}s""",
        "--outputdir",
        out_dir,
        "--variable",
        f"OS:{P.PLATFORM}",
        "--variable",
        f"PY:{P.PY_MAJOR}",
        "--randomize",
        "all",
        "--xunitskipnoncritical",
        "--xunit",
        ".".join(["xunit", "xml"]),
        ".",
    ]

    if out_dir.exists():
        print(">>> trying to clean out {}".format(out_dir), flush=True)
        try:
            shutil.rmtree(out_dir)
        except Exception as err:
            print(
                "... error, hopefully harmless: {}".format(err),
                flush=True,
            )

    if not out_dir.exists():
        print(">>> trying to prepare output directory: {}".format(out_dir), flush=True)
        try:
            out_dir.mkdir(parents=True)
        except Exception as err:
            print(
                "... Error, hopefully harmless: {}".format(err),
                flush=True,
            )

    str_args = [*map(str, args)]
    print(">>> ", " ".join(str_args), flush=True)

    proc = subprocess.Popen(str_args, cwd=P.ATEST)

    try:
        return proc.wait()
    except KeyboardInterrupt:
        proc.kill()
        return proc.wait()


def attempt_atest_with_retries(extra_args=None):
    """retry the robot tests a number of times"""
    extra_args = list(extra_args or [])
    attempt = 0
    error_count = -1

    retries = P.ATEST_RETRIES
    extra_args += P.ATEST_ARGS

    while error_count != 0 and attempt <= retries:
        attempt += 1
        print("attempt {} of {}...".format(attempt, retries + 1), flush=True)
        start_time = time.time()
        error_count = run_tests(attempt=attempt, extra_args=extra_args)
        print(
            error_count,
            "errors in",
            int(time.time() - start_time),
            "seconds",
            flush=True,
        )

    return error_count


if __name__ == "__main__":
    sys.exit(attempt_atest_with_retries(extra_args=sys.argv[1:]))
