#!/usr/bin/env python

import os
import sys

# Add Cloudlfare to path for testing
sys.path.insert(0, os.path.abspath('../Cloudflare'))
from CloudFlare import CloudFlare


def test_ips():
    cf = CloudFlare()
    ips = cf.ips.get()
    assert ips

