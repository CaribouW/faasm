from os import makedirs, listdir
from os.path import join, exists, splitext
from shutil import rmtree
from subprocess import run
import requests
from invoke import task

from faasmtools.env import PROJ_ROOT
from faasmtools.endpoints import (
    get_faasm_invoke_host_port,
    get_faasm_upload_host_port,
    get_knative_headers,
)
from faasmtools.compile_util import wasm_cmake, wasm_copy_upload


FUNC_DIR = join(PROJ_ROOT, "func")
FUNC_BUILD_DIR = join(PROJ_ROOT, "build", "func")
NATIVE_FUNC_BUILD_DIR = join(PROJ_ROOT, "build", "native-func")


def _get_all_user_funcs(user):
    # Work out all the functions for this user (that we assume will have been
    # built)
    funcs = list()
    for func_file in listdir(join(FUNC_BUILD_DIR, user)):
        name, ext = splitext(func_file)
        if ext != ".wasm":
            continue

        funcs.append(name)

    return funcs

def _copy_built_function(user, func):
    src_file = join(FUNC_BUILD_DIR, user, ".".join([func, "wasm"]))
    wasm_copy_upload(user, func, src_file)



@task(default=True, name="compile")
def compile(ctx, user, func, clean=False, debug=False, native=False):
    """
    Compile a function
    """
    if native:
        if exists(NATIVE_FUNC_BUILD_DIR) and clean:
            rmtree(NATIVE_FUNC_BUILD_DIR)

        makedirs(NATIVE_FUNC_BUILD_DIR, exist_ok=True)

        build_cmd = ["cmake", "-GNinja", FUNC_DIR]

        build_cmd = " ".join(build_cmd)
        print(build_cmd)
        run(
            "cmake -GNinja {}".format(FUNC_DIR),
            check=True,
            shell=True,
            cwd=NATIVE_FUNC_BUILD_DIR,
        )

        run(
            "ninja {}".format(func),
            shell=True,
            check=True,
            cwd=NATIVE_FUNC_BUILD_DIR,
        )
    else:
        # Build the function (gets written to the build dir)
        wasm_cmake(FUNC_DIR, FUNC_BUILD_DIR, func, clean, debug)

        # Copy into place
        _copy_built_function(user, func)

