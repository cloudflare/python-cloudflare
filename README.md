# cloudflare-python

## Installation

Two methods are provided to install this software.
Use PyPi (see [package](https://pypi.python.org/pypi/cloudflare) details) or GitHub (see [package](https://github.com/cloudflare/python-cloudflare) details).

### Via PyPI

```bash
    $ sudo pip install cloudflare
    $
```

Yes - that simple! (the sudo may not be needed in some cases).

### Via github

```bash
    $ git clone https://github.com/cloudflare/python-cloudflare
    $ cd python-cloudflare
    $ ./setup.py build
    $ sudo ./setup.py install
    $
```

Or whatever variance of that you want to use.
There is a Makefile included.

## Cloudflare name change - dropping the capital F

In Sepember/October 2016 the company modified its company name and dropped the capital F.
However, for now (and for backward compatibility reasons) the class name stays the same.

## Cloudflare API version 4

The Cloudflare API can be found [here](https://api.cloudflare.com/).
Each API call is provided via a similarly named function within the _CloudFlare_ class.
A full list is provided below.

## Example code

All example code is available on GitHub (see [package](https://github.com/cloudflare/python-cloudflare) in the [examples](https://github.com/cloudflare/python-cloudflare/tree/master/examples) folder.

## Getting Started

A very simple listing of zones within your account; including the IPv6 status of the zone.

```python
from CloudFlare.cloudflare import CloudFlare

def main():
    cf = CloudFlare()
    zones = cf.zones.get(params = {'per_page':50})
    for zone in zones:
        zone_name = zone['name']
        zone_id = zone['id']
        settings_ipv6 = cf.zones.settings.ipv6.get(zone_id)
        ipv6_status = settings_ipv6['value']
        settings_ssl = cf.zones.settings.ssl.get(zone_id)
        ssl_status = settings_ssl['value']
        print(zone_id, ssl_status, ipv6_status, zone_name)

if __name__ == '__main__':
    main()
```

A more complex example follows.

```python
from CloudFlare.cloudflare import CloudFlare,exceptions

def main():
    zone_name = 'example.com'

    cf = CloudFlare()

    # query for the zone name and expect only one value back
    try:
        zones = cf.zones.get(params = {'name':zone_name,'per_page':1})
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones.get %d %s - api call failed' % (e, e))
    except Exception as e:
        exit('/zones.get - %s - api call failed' % (e))

    if len(zones) == 0:
        exit('No zones found')

    # extract the zone_id which is needed to process that zone
    zone = zones[0]
    zone_id = zone['id']

    # request the DNS records from that zone
    try:
        dns_records = cf.zones.dns_records.get(zone_id)
    except exceptions.CloudFlareAPIError as e:
        exit('/zones/dns_records.get %d %s - api call failed' % (e, e))

    # print the results - first the zone name
    print zone_id, zone_name

    # then all the DNS records for that zone
    for dns_record in dns_records:
        r_name = dns_record['name']
        r_type = dns_record['type']
        r_value = dns_record['content']
        r_id = dns_record['id']
        print '\t', r_id, r_name, r_type, r_value

    exit(0)

if __name__ == '__main__':
    main()
```

## Providing Cloudflare Username and API Key

When you create a _CloudFlare_ class you can pass up to four paramaters.

 * Account email
 * Account API key
 * Optional Origin-CA Certificate Token
 * Optional Debug flag (True/False)

```python
from CloudFlare.cloudflare import CloudFlare,exceptions

# A minimal call - reading values from environment variables or configuration file
cf = CloudFlare()

# A minimal call with debug enabled
cf = CloudFlare(debug=True))

# A full blown call with passed basic account information
cf = CloudFlare(email='user@example.com', token='00000000000000000000000000000000')

# A full blown call with passed basic account information and CA-Origin info
cf = CloudFlare(email='user@example.com', token='00000000000000000000000000000000', certtoken='v1.0-...')
```

If the account email and API key are not passed when you create the class, then they are retreived from either the users exported shell environment variables or the .cloudflare.cfg or ~/.cloudflare.cfg or ~/.cloudflare/cloudflare.cfg files, in that order.

There is one call that presently doesn't need any email or token certification (the */ips* call); hence you can test without any values saved away.

### Using shell environment variables
```bash
$ export CF_API_EMAIL='user@example.com'
$ export CF_API_KEY='00000000000000000000000000000000'
$ export CF_API_CERTKEY='v1.0-...'
$
```

These are optional environment variables; however, they do override the values set within a configuration file.

### Using configuration file to store email and keys

```bash
$ cat ~/.cloudflare/cloudflare.cfg
[CloudFlare]
email = user@example.com
token = 00000000000000000000000000000000
certtoken = v1.0-...
extras =
$
```

The *CF_API_CERTKEY* or *certtoken* values are used for the Origin-CA */certificates* API calls.
You can leave *certtoken* in the configuration with a blank value (or omit the option variable fully).

The *extras* values are used when adding API calls outside of the core codebase.
Technically, this is only useful for internal testing within Cloudflare.
You can leave *extras* in the configuration with a blank value (or omit the option variable fully).

## Exceptions and return values

### Response data

The response is build from the JSON in the API call.
It contains the **results** values; but does not contain the paging values.

You can return all the paging values by calling the class with raw=True. Here's an example without paging.

```python
#!/usr/bin/env python

import json
from CloudFlare.cloudflare import CloudFlare

def main():
    cf = CloudFlare()
    zones = cf.zones.get(params={'per_page':5})
    print len(zones)

if __name__ == '__main__':
    main()
```

The results are as follows.

```
5
```

When you add the raw option; the APIs full structure is returned. This means the paging values can be seen.

```python
#!/usr/bin/env python

import json
from CloudFlare.cloudflare import CloudFlare

def main():
    cf = CloudFlare(raw=True)
    zones = cf.zones.get(params={'per_page':5})
    print zones.length()
    print json.dumps(zones, indent=4, sort_keys=True)

if __name__ == '__main__':
    main()
```

This produces.

```
5
{
    "result": [
        ...
    ],
    "result_info": {
        "count": 5,
        "page": 1,
        "per_page": 5,
        "total_count": 31,
        "total_pages": 7
    }
}
```

A full example of paging is provided below.


### Exceptions

The library will raise **CloudFlareAPIError** when the API call fails.
The exception returns both an integer and textual message in one value.

```python
from CloudFlare.cloudflare import CloudFlare,exceptions

    ...
    try
        r = ...
    except exceptions.CloudFlareAPIError as e:
        exit('api error: %d %s' % (e, e))
    ...
```

The other raised response is **CloudFlareInternalError** which can happen when calling an invalid method.

In some cases more than one error is returned. In this case the return value **e** is also an array.
You can itterate over that array to see the additional error.

```python
import sys
from CloudFlare.cloudflare import CloudFlare,exceptions


    ...
    try
        r = ...
    except exceptions.CloudFlareAPIError as e:
        if len(e) > 0:
            sys.stderr.write('api error - more than one error value returned!\n')
            for x in e:
                sys.stderr.write('api error: %d %s\n' % (x, x))
        exit('api error: %d %s' % (e, e))
    ...
```

## Included example code

The [examples](https://github.com/cloudflare/python-cloudflare/tree/master/examples) folder contains many examples in both simple and verbose formats.

## A DNS zone code example

```python
#!/usr/bin/env python

import sys
from CloudFlare.cloudflare import CloudFlare

def main():
    zone_name = sys.argv[1]
    cf = CloudFlare()
    zone_info = cf.zones.post(data={'jump_start':False, 'name': zone_name})
    zone_id = zone_info['id']

    dns_records = [
        {'name':'foo', 'type':'AAAA', 'content':'2001:d8b::1'},
        {'name':'foo', 'type':'A', 'content':'192.168.0.1'},
        {'name':'duh', 'type':'A', 'content':'10.0.0.1', 'ttl':120},
        {'name':'bar', 'type':'CNAME', 'content':'foo'},
        {'name':'shakespeare', 'type':'TXT', 'content':"What's in a name? That which we call a rose by any other name ..."}
    ]

    for dns_record in dns_records:
        r = cf.zones.dns_records.post(zone_id, data=dns_record)
    exit(0)

if __name__ == '__main__':
    main()
```

## CLI

All API calls can be called from the command line.
The command will convert domain names on-the-fly into zone_identifier's.

```bash
$ cli4 [-V|--version] [-h|--help] [-v|--verbose] [-q|--quiet] [-j|--json] [-y|--yaml] [-r|--raw] [-d|--dump] [--get|--patch|--post|-put|--delete] [item=value ...] /command...

```

For API calls that need a set of date or parameters passed there is a item=value format.
If you want a numeric value passed, then _==_ can be used to force the value to be treated as a numeric value.

The output from the CLI command is in JSON or YAML format (and human readable).

### Simple CLI examples

 * ```cli4 /user/billing/profile```
 * ```cli4 /user/invites```

 * ```cli4 /zones/:example.com```
 * ```cli4 /zones/:example.com/dnssec```
 * ```cli4 /zones/:example.com/settings/ipv6```
 * ```cli4 --put /zones/:example.com/activation_check```
 * ```cli4 /zones/:example.com/keyless_certificates```

 * ```cli4 /zones/:example.com/analytics/dashboard```

### More complex CLI examples

Here is the creation of a DNS entry, followed by a listing of that entry and then the deletion of that entry.

```bash
$ $ cli4 --post name="test" type="A" content="10.0.0.1" /zones/:example.com/dns_records
{
    "id": "94e028933c87b4bff3c70a42e6daac4f",
    "name": "test.example.com",
    "type": "A",
    "content": "10.0.0.1",
    ...
}
$

$ cli4 /zones/:example.com/dns_records/:test.example.com | jq '{"id":.id,"name":.name,"type":.type,"content":.content}'
{
  "id": "94e028933c87b4bff3c70a42e6daac4f",
  "name": "test.example.com",
  "type": "A",
  "content": "10.0.0.1"
}

$ cli4 --delete /zones/:example.com/dns_records/:test.example.com | jq -c .
{"id":"94e028933c87b4bff3c70a42e6daac4f"}
$
```

There's the ability to handle dns entries with multiple values.
This produces more than one API call within the command.

```
$ cli4 /zones/:example.com/dns_records/:test.example.com | jq -c '.[]|{"id":.id,"name":.name,"type":.type,"content":.content}'
{"id":"bca0c4a5e3691e62841627e4dc3a19ed","name":"test.example.com","type":"A","content":"192.168.0.1"}
{"id":"d94f788e6bf72ba2a54145ad04b34f08","name":"test.example.com","type":"AAAA","content":"2001:d8b::1"}
$
```

Here are the cache purging commands.

```bash
$ cli4 --delete purge_everything=true /zones/:example.com/purge_cache | jq -c .
{"id":"d8afaec3dd2b7f8c1b470e594a21a01d"}
$

$ cli4 --delete files='[http://example.com/css/styles.css]' /zones/:example.com/purge_cache | jq -c .
{"id":"d8afaec3dd2b7f8c1b470e594a21a01d"}
$

$ cli4 --delete files='[http://example.com/css/styles.css,http://example.com/js/script.js]' /zones/:example.com/purge_cache | jq -c .
{"id":"d8afaec3dd2b7f8c1b470e594a21a01d"}
$

$ cli4 --delete tags='[tag1,tag2,tag3]' /zones/:example.com/purge_cache | jq -c .
cli4: /zones/:example.com/purge_cache - 1107 Only enterprise zones can purge by tag.
$
```

A somewhat useful listing of available plans for a specific zone.

```bash
$ cli4 /zones/:example.com/available_plans | jq -c '.[]|{"id":.id,"name":.name}'
{"id":"a577b510288e82b26486fd1df47000ec","name":"Pro Website"}
{"id":"1ac039f6c29b691475c3d74fe588d1ae","name":"Business Website"}
{"id":"94f3b7b768b0458b56d2cac4fe5ec0f9","name":"Enterprise Website"}
{"id":"0feeeeeeeeeeeeeeeeeeeeeeeeeeeeee","name":"Free Website"}
$
```

### Paging CLI examples

The **--raw** command provides access to the paging returned values.
See the API documentation for all the info.
Here's an example of how to page thru a list of zones (it's included in the examples folder as **example_paging_thru_zones.sh**).

```bash
:
tmp=/tmp/$$_
trap "rm ${tmp}; exit 0" 0 1 2 15
PAGE=0
while true
do
	cli4 --raw per_page=5 page=${PAGE} /zones > ${tmp}
	domains=`jq -c '.|.result|.[]|.name' < ${tmp} | tr -d '"'`
	result_info=`jq -c '.|.result_info' < ${tmp}`
	COUNT=`      echo "${result_info}" | jq .count`
	PAGE=`       echo "${result_info}" | jq .page`
	PER_PAGE=`   echo "${result_info}" | jq .per_page`
	TOTAL_COUNT=`echo "${result_info}" | jq .total_count`
	TOTAL_PAGES=`echo "${result_info}" | jq .total_pages`
	echo COUNT=${COUNT} PAGE=${PAGE} PER_PAGE=${PER_PAGE} TOTAL_COUNT=${TOTAL_COUNT} TOTAL_PAGES=${TOTAL_PAGES} -- ${domains}
	if [ "${PAGE}" == "${TOTAL_PAGES}" ]
	then
		## last section
		break
	fi
	# grab the next page
	PAGE=`expr ${PAGE} + 1`
done
```

It produces the following results.

```
COUNT=5 PAGE=1 PER_PAGE=5 TOTAL_COUNT=31 TOTAL_PAGES=7 -- accumsan.example auctor.example consectetur.example dapibus.example elementum.example
COUNT=5 PAGE=2 PER_PAGE=5 TOTAL_COUNT=31 TOTAL_PAGES=7 -- felis.example iaculis.example ipsum.example justo.example lacus.example
COUNT=5 PAGE=3 PER_PAGE=5 TOTAL_COUNT=31 TOTAL_PAGES=7 -- lectus.example lobortis.example maximus.example morbi.example pharetra.example
COUNT=5 PAGE=4 PER_PAGE=5 TOTAL_COUNT=31 TOTAL_PAGES=7 -- porttitor.example potenti.example pretium.example purus.example quisque.example
COUNT=5 PAGE=5 PER_PAGE=5 TOTAL_COUNT=31 TOTAL_PAGES=7 -- sagittis.example semper.example sollicitudin.example suspendisse.example tortor.example
COUNT=1 PAGE=7 PER_PAGE=5 TOTAL_COUNT=31 TOTAL_PAGES=7 -- varius.example vehicula.example velit.example velit.example vitae.example
COUNT=5 PAGE=6 PER_PAGE=5 TOTAL_COUNT=31 TOTAL_PAGES=7 -- vivamus.example
```


### DNSSEC CLI examples

```bash
$ cli4 /zones/:example.com/dnssec | jq -c '{"status":.status}'
{"status":"disabled"}
$

$ cli4 --patch status=active /zones/:example.com/dnssec | jq -c '{"status":.status}'
{"status":"pending"}
$

$ cli4 /zones/:example.com/dnssec
{
    "algorithm": "13",
    "digest": "41600621c65065b09230ebc9556ced937eb7fd86e31635d0025326ccf09a7194",
    "digest_algorithm": "SHA256",
    "digest_type": "2",
    "ds": "example.com. 3600 IN DS 2371 13 2 41600621c65065b09230ebc9556ced937eb7fd86e31635d0025326ccf09a7194",
    "flags": 257,
    "key_tag": 2371,
    "key_type": "ECDSAP256SHA256",
    "modified_on": "2016-05-01T22:42:15.591158Z",
    "public_key": "mdsswUyr3DPW132mOi8V9xESWE8jTo0dxCjjnopKl+GqJxpVXckHAeF+KkxLbxILfDLUT0rAK9iUzy1L53eKGQ==",
    "status": "pending"
}
$
```

## Implemented API calls

The **--dump** argument to cli4 will produce a list of all the call implemented within the library.

```bash
$ cli4 --dump
/certificates
/ips
/organizations
...
/zones/ssl/analyze
/zones/ssl/certificate_packs
/zones/ssl/verification
$
```

### Table of commands

|`GET`   |`PUT`   |`POST`  |`PATCH` |`DELETE`|API call|
|--------|--------|--------|--------|--------|:--------|
|`GET`   |        |`POST`  |        |`DELETE`|/certificates|
|`GET`   |        |        |        |        |/ips|
|`GET`   |        |        |`PATCH` |        |/organizations|
|`GET`   |        |`POST`  |`PATCH` |`DELETE`|/organizations/:identifier/firewall/access_rules/rules|
|        |        |        |`PATCH` |        |/organizations/:identifier/invite|
|`GET`   |        |`POST`  |        |`DELETE`|/organizations/:identifier/invites|
|`GET`   |        |        |`PATCH` |`DELETE`|/organizations/:identifier/members|
|`GET`   |        |`POST`  |`PATCH` |`DELETE`|/organizations/:identifier/railguns|
|`GET`   |        |        |        |        |/organizations/:identifier/railguns/:identifier/zones|
|`GET`   |        |        |        |        |/organizations/:identifier/roles|
|`GET`   |        |`POST`  |`PATCH` |`DELETE`|/organizations/:identifier/virtual_dns|
|`GET`   |        |`POST`  |`PATCH` |`DELETE`|/railguns|
|`GET`   |        |        |        |        |/railguns/:identifier/zones|
|`GET`   |        |        |`PATCH` |        |/user|
|`GET`   |        |        |        |        |/user/billing/history|
|`GET`   |        |        |        |        |/user/billing/profile|
|`GET`   |        |        |        |        |/user/billing/subscriptions/apps|
|`GET`   |        |        |        |        |/user/billing/subscriptions/zones|
|`GET`   |        |`POST`  |`PATCH` |`DELETE`|/user/firewall/access_rules/rules|
|`GET`   |        |        |`PATCH` |        |/user/invites|
|`GET`   |        |        |        |`DELETE`|/user/organizations|
|`GET`   |        |`POST`  |`PATCH` |`DELETE`|/user/virtual_dns|
|`GET`   |        |`POST`  |`PATCH` |`DELETE`|/zones|
|        |`PUT`   |        |        |        |/zones/:identifier/activation_check|
|`GET`   |        |        |        |        |/zones/:identifier/analytics/colos|
|`GET`   |        |        |        |        |/zones/:identifier/analytics/dashboard|
|`GET`   |        |        |        |        |/zones/:identifier/available_plans|
|        |`PUT`   |        |        |        |/zones/:identifier/custom_certificates/prioritize|
|`GET`   |        |`POST`  |`PATCH` |`DELETE`|/zones/:identifier/custom_certificates|
|`GET`   |`PUT`   |        |        |        |/zones/:identifier/custom_pages|
|`GET`   |`PUT`   |`POST`  |        |`DELETE`|/zones/:identifier/dns_records|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/firewall/waf/packages/:identifier/groups|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/firewall/waf/packages/:identifier/rules|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/firewall/waf/packages|
|`GET`   |        |`POST`  |`PATCH` |`DELETE`|/zones/:identifier/firewall/access_rules/rules|
|`GET`   |        |`POST`  |`PATCH` |`DELETE`|/zones/:identifier/keyless_certificates|
|`GET`   |`PUT`   |`POST`  |`PATCH` |`DELETE`|/zones/:identifier/pagerules|
|        |        |        |        |`DELETE`|/zones/:identifier/purge_cache|
|`GET`   |        |        |        |        |/zones/:identifier/railguns/:identifier/diagnose|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/railguns|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings|
|`GET`   |        |        |        |        |/zones/:identifier/settings/advanced_ddos|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/always_online|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/browser_cache_ttl|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/browser_check|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/cache_level|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/challenge_ttl|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/development_mode|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/email_obfuscation|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/hotlink_protection|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/ip_geolocation|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/ipv6|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/minify|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/mirage|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/mobile_redirect|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/origin_error_page_pass_thru|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/polish|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/prefetch_preload|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/response_buffering|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/rocket_loader|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/security_header|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/security_level|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/server_side_exclude|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/sort_query_string_for_cache|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/ssl|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/tls_1_2_only|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/tls_client_auth|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/true_client_ip_header|
|`GET`   |        |        |`PATCH` |        |/zones/:identifier/settings/waf|

## Adding extra API calls manually

Extra API calls can be added via the configuration file
```bash
$ cat ~/.cloudflare/cloudflare.cfg
[CloudFlare]
extras =
    /client/v4/command
    /client/v4/command/:command_identifier
    /client/v4/command/:command_identifier/settings
$
```

While it's easy to call anything within Cloudflare's API, it's not very useful to add items in here as they will simply return API URL errors.
Technically, this is only useful for internal testing within Cloudflare.

## Issues

The following error can be caused by an out of date SSL/TLS library and/or out of date Python.

```
/usr/local/lib/python2.7/dist-packages/requests/packages/urllib3/util/ssl_.py:318: SNIMissingWarning: An HTTPS request has been made, but the SNI (Subject Name Indication) extension to TLS is not available on this platform. This may cause the server to present an incorrect TLS certificate, which can cause validation failures. You can upgrade to a newer version of Python to solve this. For more information, see https://urllib3.readthedocs.org/en/latest/security.html#snimissingwarning.
  SNIMissingWarning
/usr/local/lib/python2.7/dist-packages/requests/packages/urllib3/util/ssl_.py:122: InsecurePlatformWarning: A true SSLContext object is not available. This prevents urllib3 from configuring SSL appropriately and may cause certain SSL connections to fail. You can upgrade to a newer version of Python to solve this. For more information, see https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning.
  InsecurePlatformWarning
```

The solution can be found [here](https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning) and/or [here](http://stackoverflow.com/questions/35144550/how-to-install-cryptography-on-ubuntu).

## Python 2.x vs 3.x support

```
As of May/June 2016 the code is now tested againt pylint.
This was required in order to move the codebase into Python 3.x.
The motivation for this came from [Danielle Madeley (danni)](https://github.com/danni).

While the codebase has been edited to run on Python 3.x, there's not been enough Python 3.x testing performed.
If you can help in this regard; please contact the maintainers.
```

As of October 2016, the code was updated to be compatible with 3.5. There is currently no testing. 

## Credit

This is based on work by [Felix Wong (gnowxilef)](https://github.com/gnowxilef) found [here](https://github.com/cloudflare-api/python-cloudflare-v4).
It has been seriously expanded upon.

## Copyright

Portions copyright [Felix Wong (gnowxilef)](https://github.com/gnowxilef) 2015 and Cloudflare 2016.
