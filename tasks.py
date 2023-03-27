# type: ignore

from invoke import task

PATHS = "slotted setup.py tasks.py docs/source/conf.py tests"


@task
def conform(c):
    c.run("isort {} -m 3 -l 88 --up --tc --lbt 0".format(PATHS))
    c.run("black {}".format(PATHS))


@task
def lint(c):
    c.run("isort {} -m 3 -l 88 --up --tc --lbt 0 --check-only".format(PATHS))
    c.run("black {} --check".format(PATHS))
    c.run(
        "flake8 {} --count --select=E9,F63,F7,F82 --max-line-length 88 --show-source "
        "--statistics".format(PATHS)
    )
    c.run(
        "flake8 {} --count --ignore=F811,F405,F403,F401,E203,E731,C901,W503 "
        "--max-line-length 88 --statistics".format(PATHS)
    )


@task
def mypy(c):
    c.run("mypy slotted --strict")


@task
def tests(c):
    c.run("python -m pytest -vv -rs tests")
    c.run("python -m pytest --doctest-modules -vv -rs README.rst")


@task
def docs(c):
    c.run("sphinx-build -M html ./docs/source ./docs/build")


@task
def checks(c):
    conform(c)
    lint(c)
    mypy(c)
    tests(c)
    docs(c)
