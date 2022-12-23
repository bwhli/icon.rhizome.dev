from dotenv import dotenv_values


def load_env():
    return dict(dotenv_values())


ENV = load_env()
