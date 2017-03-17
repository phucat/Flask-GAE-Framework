import os
import yaml


def _is_app_spot():
    return os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/')


def _is_testbed():
    # local dev server = Development/1.0
    # testbed = Development/2.0. (testbed)
    return os.getenv('SERVER_SOFTWARE', '').endswith('(testbed)')


def import_env_variables():
    buff = None
    with open("env_variables.yaml", 'r') as stream:
        try:
            buff = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    if buff is not None:
        for v in buff["env_variables"]:
            # print v, buff["env_variables"][v]
            os.environ[v] = buff["env_variables"][v]


class Config(object):

    @staticmethod
    def get(field):
        # import has to be done on each request as os.environ does not
        # retain values
        if _is_testbed():
            import_env_variables()
        return os.environ[field]
