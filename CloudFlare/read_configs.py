""" reading the config file for Cloudflare API"""
                                   
import sys
import os
import re

if sys.version_info > (3,):
    import configparser as ConfigParser
else:
    import ConfigParser


def read_configs():
    """ reading the config file for Cloudflare API"""

    # environment variables override config files
    email = os.getenv('CF_API_EMAIL')
    token = os.getenv('CF_API_KEY')
    certtoken = os.getenv('CF_API_CERTKEY')
    extras = os.getenv('CF_API_EXTRAS')

    # grab values from config files
    config = ConfigParser.RawConfigParser()
    config.read([
        '.cloudflare.cfg',
        os.path.expanduser('~/.cloudflare.cfg'),
        os.path.expanduser('~/.cloudflare/cloudflare.cfg')
    ])

    if email is None:
        try:
            email = re.sub(r"\s+", '', config.get('CloudFlare', 'email'))
        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
            email = None

    if token is None:
        try:
            token = re.sub(r"\s+", '', config.get('CloudFlare', 'token'))
        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
            token = None

    if certtoken is None:
        try:
            certtoken = re.sub(r"\s+", '', config.get('CloudFlare', 'certtoken'))
        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
            certtoken = None

    if extras is None:
        try:
            extras = re.sub(r"\s+", ' ', config.get('CloudFlare', 'extras'))
        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
            extras = None

        if extras:
            extras = extras.split(' ')

    return [email, token, certtoken, extras]

