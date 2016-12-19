""" Cloudflare v4 API"""

# py3 compatible
try:
    from cloudflare import CloudFlare
except:
    from .cloudflare import CloudFlare

__version__ = '1.4.2'
