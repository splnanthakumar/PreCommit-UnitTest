import os
import sys

from invoke import task, run

UNITTEST_DIR = "tests/unittests"
ENV_PYTHON_PATH = "PYTHONPATH"
DEFAULT_VIRTUAL_ENV_DIR = ".venv"


@task(name="unittest", aliases=['ut'])
def setup(app=None, branch=None, venv=DEFAULT_VIRTUAL_ENV_DIR, coverage=False):
    print("unittest ....")
    app_path = os.getcwd()
    path = app_path.rsplit('/', 1)

    folder = path[0]
    app = path[1] if not app else app

    print("current folder path : %s" % folder)
    print("app : %s " % app)

    # checkout app with mentioned branch
    _checkout(app, app_path, branch)

    # create virtual environment and install dependencies
    _create_app_env(app, app_path, venv)

    # export python path
    _export_python_path(app_path)

    # execute unittest and generate reports
    _execute_ut(app, app_path, venv, coverage)


def _checkout(app, app_path, branch):
    print "branch is : {}".format(branch)
    if not branch:
        run("git branch | grep '*'")
        print "Running UT for the above branch "
    else:
        result = run("cd {} && git checkout {} && git reset --hard origin/{}".format
                     (app_path, branch, branch),
                     warn=True)
        err_msg = "App {} has not been checked out with the branch: {}".format(app, branch)
        if _is_cmd_executed(result.ok, err_msg):
            print "Checked out latest branch {} on repo {}".format(result.stdout, app_path)


def _create_app_env(app, app_path, venv):
    print "creating virtual environment for {}".format(app)
    # create test virtual environment
    run("pip install virtualenv")
    if not os.path.isdir(venv):
        run("cd {} && virtualenv {} ".format(app_path, venv))
    else:
        print "venv is already exist"

    _install_requirements(app_path, venv, "{}/requirements.txt".format(app_path))
    _install_requirements(app_path, venv, "{}/test_requirements.txt".format(app_path))


def _export_python_path(app_path):
    python_path = os.environ.get(ENV_PYTHON_PATH, "")
    print "python path BEFORE....{}".format(python_path)

    if not python_path:
        os.environ[ENV_PYTHON_PATH] = app_path
    elif app_path not in python_path:
        os.environ[ENV_PYTHON_PATH] += ":" + app_path

    print "python path AFTER....{}".format(os.environ.get(ENV_PYTHON_PATH, ""))


def _execute_ut(app, app_path, venv, coverage=False):
    unittest_dir_path = "{}/{}".format(app_path, UNITTEST_DIR)
    print "unittest dir path : {}".format(unittest_dir_path)

    if not os.path.isdir(unittest_dir_path):
        print "[ERROR] - No unittests folder found for this app {}. Exiting".format(app)
        sys.exit(1)

    if coverage:
        print "running unittests with coverage reports..."

        result = run(
            "cd {} && source {}/bin/activate && nosetests {} -v "
            "--with-coverage && coverage html -d ./cov_report.html ".format(
                app_path, venv, unittest_dir_path), warn=True)
        _is_cmd_executed(result.ok)
    else:
        print "running unittests..."
        result = run(
            "cd {} && source {}/bin/activate && nosetests {} -v "
            "--nologcapture --with-xunit --xunit-file=./report.xml ".format(
                app_path, venv, unittest_dir_path), warn=True)
        _is_cmd_executed(result.ok)


def _install_requirements(app_path, venv, requirement_file_path):
    if not os.path.isfile(requirement_file_path):
        print "File: {} Not found in {} ".format(requirement_file_path, app_path)
    else:
        print "Installing dependencies from {} file ...".format(requirement_file_path)
        # Install requirements of the current application
        run("cd {} && . {}/bin/activate && pip install -r {}".format(
            app_path, venv, requirement_file_path), warn=True,
            hide=True)


def _is_cmd_executed(is_executed, error_message=None):
    if not is_executed:
        print "[ERROR] - {}".format(error_message if error_message else "Something went wrong!")
        sys.exit(1)
    else:
        return True


if __name__ == '__main__':
    setup()
