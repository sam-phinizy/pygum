from nox_poetry import session


@session
def lint(session) -> None:
    session.install("pre-commit")
    session.run("pre-commit", "run")
