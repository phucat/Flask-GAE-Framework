import os.path

from google.appengine.ext import vendor

# Add any libraries installed in the "lib" folder.
vendor.add('lib')


def patched_expanduser(path):
    return path

os.path.expanduser = patched_expanduser
