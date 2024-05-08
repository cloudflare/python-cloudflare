""" warning message if version is 2.20 or above (technically, there's no version above 2.20.0) """

import sys

from . import __version__

MAJOR_VERSION_WARNING = """\
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   WARNING  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!! You're seeing this warning because you've upgraded the Python package 'cloudflare' to version  !!
!! 2.20.* via an automated upgrade without version pinning. Version 2.20.0 exists to catch any    !!
!! of these upgrades before Cloudflare releases a new major release under the release number 3.x. !!
!!                                                                                                !!
!! Should you determine that you need to revert this upgrade and pin to v2.19.* it is recommended !!
!! you do the following: pip install --upgrade cloudflare==2.19.* or equivilant.                  !!
!!                                                                                                !!
!! Or you can upgrade to v3.x. NOTE: Release 3.x will not be code-compatible or call-compatible   !!
!! with previous releases. To see more about upgrading to next major version, please see:         !!
!! https://github.com/cloudflare/python-cloudflare/discussions/191                                !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\
"""

def warning_2_20():
    """ warning_2_20 """

    if __version__ < '2.20.0':
        return None
    return MAJOR_VERSION_WARNING

def print_warning_2_20(warning):
    """ print_warning_2_20 """
    print(warning, file=sys.stderr)
