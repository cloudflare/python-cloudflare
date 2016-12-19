""" reading the config file for Cloudflare API"""

import os
import re
# py3 compatible
try:
	from ConfigParser import RawConfigParser, NoOptionError, NoSectionError
except:
    from configparser import ConfigParser, RawConfigParser, NoOptionError, NoSectionError

def read_configs():
    """ reading the config file for Cloudflare API"""

    # envioronment variables override config files
    email = os.getenv('CF_API_EMAIL')
    token = os.getenv('CF_API_KEY')
    certtoken = os.getenv('CF_API_CERTKEY')
    extras = os.getenv('CF_API_EXTRAS')

    # grab values from config files
    config = RawConfigParser()
    config.read([
        '.cloudflare.cfg',
        os.path.expanduser('~/.cloudflare.cfg'),
        os.path.expanduser('~/.cloudflare/cloudflare.cfg')
    ])

    if email is None:
        try:
            email = re.sub(r"\s+", '', config.get('CloudFlare', 'email'))
        except (NoOptionError, NoSectionError):
            email = None

    if token is None:
        try:
            token = re.sub(r"\s+", '', config.get('CloudFlare', 'token'))
        except (NoOptionError, NoSectionError):
            token = None

    if certtoken is None:
        try:
            certtoken = re.sub(r"\s+", '', config.get('CloudFlare', 'certtoken'))
        except (NoOptionError, NoSectionError):
            certtoken = None

    if extras is None:
        try:
            extras = re.sub(r"\s+", ' ', config.get('CloudFlare', 'extras'))
        except (NoOptionError, NoSectionError):
            extras = None

        if extras:
            extras = extras.split(' ')

    return [email, token, certtoken, extras]

