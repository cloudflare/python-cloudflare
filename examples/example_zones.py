#!/usr/bin/env python
"""Cloudflare API code - example"""

import os
import sys
import re

sys.path.insert(0, os.path.abspath('..'))
import CloudFlare
import CloudFlare.exceptions

def main():
    """Cloudflare API code - example"""

    # Grab the first argument, if there is one
    try:
        zone_name = sys.argv[1]
        params = {'name':zone_name, 'per_page':1}
    except IndexError:
        params = {'per_page':50}

    cf = CloudFlare.CloudFlare()

    # grab the zone identifier
    try:
        zones = cf.zones.get(params=params)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones %d %s - api call failed' % (e, e))
    except Exception as e:
        exit('/zones.get - %s - api call failed' % (e))

    # there should only be one zone
    for zone in sorted(zones, key=lambda v: v['name']):
        zone_name = zone['name']
        zone_id = zone['id']
        if 'email' in zone['owner']:
            zone_owner = zone['owner']['email']
        else:
            zone_owner = '"' + zone['owner']['name'] + '"'
        zone_plan = zone['plan']['name']

        try:
            dns_records = cf.zones.dns_records.get(zone_id)
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            exit('/zones/dns_records %d %s - api call failed' % (e, e))

        print zone_id, zone_name, zone_owner, zone_plan

        prog = re.compile('\.*'+zone_name+'$')
        dns_records = sorted(dns_records, key=lambda v: prog.sub('', v['name']) + '_' + v['type'])
        for dns_record in dns_records:
            r_name = dns_record['name']
            r_type = dns_record['type']
            r_value = dns_record['content']
            r_ttl = dns_record['ttl']
            r_id = dns_record['id']
            print '\t%s %60s %6d %-5s %s' % (r_id, r_name, r_ttl, r_type, r_value)

        print ''

    exit(0)

if __name__ == '__main__':
    main()

