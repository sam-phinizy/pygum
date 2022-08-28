from nox_poetry import session


@session
def lint(session) -> None:
    session.run("pre-commit", "run")
