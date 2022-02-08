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
Each API call is provided via a similarly named function within the **CloudFlare** class.
A full list is provided below.

## Example code

All example code is available on GitHub (see [package](https://github.com/cloudflare/python-cloudflare) in the [examples](https://github.com/cloudflare/python-cloudflare/tree/master/examples) folder).

## Blog

This package was initially introduced [here](https://blog.cloudflare.com/python-cloudflare/) via Cloudflare's [blog](https://blog.cloudflare.com/).

## Getting Started

A very simple listing of zones within your account; including the IPv6 status of the zone.

```python
import CloudFlare

def main():
    cf = CloudFlare.CloudFlare()
    zones = cf.zones.get()
    for zone in zones:
        zone_id = zone['id']
        zone_name = zone['name']
        print(zone_id, zone_name)

if __name__ == '__main__':
    main()
```

This example works when there are less than 50 zones (50 is the default number of values returned from a query like this).

Now lets expand on that and add code to show the IPv6 and SSL status of the zones. Lets also query 100 zones.

```python
import CloudFlare

def main():
    cf = CloudFlare.CloudFlare()
    zones = cf.zones.get(params = {'per_page':100})
    for zone in zones:
        zone_id = zone['id']
        zone_name = zone['name']

        settings_ssl = cf.zones.settings.ssl.get(zone_id)
        ssl_status = settings_ssl['value']

        settings_ipv6 = cf.zones.settings.ipv6.get(zone_id)
        ipv6_status = settings_ipv6['value']

        print(zone_id, zone_name, ssl_status, ipv6_status)

if __name__ == '__main__':
    main()
```

In order to query more than a single page of zones, we would have to use the raw mode (described more below).
We can loop over many get calls and pass the page parameter to facilitate the paging.

Raw mode is only needed when a get request has the possibility of returning many items.

```python
import CloudFlare

def main():
    cf = CloudFlare.CloudFlare(raw=True)
    page_number = 0
    while True:
    	page_number += 1
        raw_results = cf.zones.get(params={'per_page':5,'page':page_number})
        zones = raw_results['result']

        for zone in zones:
            zone_id = zone['id']
            zone_name = zone['name']
            print(zone_id, zone_name)

        total_pages = raw_results['result_info']['total_pages']
        if page_number == total_pages:
            break

if __name__ == '__main__':
    main()
```

A more complex example follows.

```python
import CloudFlare

def main():
    zone_name = 'example.com'

    cf = CloudFlare.CloudFlare()

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
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones/dns_records.get %d %s - api call failed' % (e, e))

    # print the results - first the zone name
    print(zone_id, zone_name)

    # then all the DNS records for that zone
    for dns_record in dns_records:
        r_name = dns_record['name']
        r_type = dns_record['type']
        r_value = dns_record['content']
        r_id = dns_record['id']
        print('\t', r_id, r_name, r_type, r_value)

    exit(0)

if __name__ == '__main__':
    main()
```

## Providing Cloudflare Username and API Key

When you create a **CloudFlare** class you can pass up to four parameters.

 * API Token or API Key
 * Account email (only if an API Key is being used)
 * Optional Origin-CA Certificate Token
 * Optional Debug flag (True/False)
 * Optional Profile name (the default is `Cloudflare`)

```python
import CloudFlare

    # A minimal call - reading values from environment variables or configuration file
    cf = CloudFlare.CloudFlare()

    # A minimal call with debug enabled
    cf = CloudFlare.CloudFlare(debug=True)

    # An authenticated call using an API Token (note the missing email)
    cf = CloudFlare.CloudFlare(token='00000000000000000000000000000000')

    # An authenticated call using an API Key
    cf = CloudFlare.CloudFlare(email='user@example.com', token='00000000000000000000000000000000')

    # An authenticated call using an API Key and CA-Origin info
    cf = CloudFlare.CloudFlare(email='user@example.com', token='00000000000000000000000000000000', certtoken='v1.0-...')

    # An authenticated call using using a stored profile (see below)
    cf = CloudFlare.CloudFlare(profile="CompanyX"))
```

If the account email and API key are not passed when you create the class, then they are retrieved from either the users exported shell environment variables or the .cloudflare.cfg or ~/.cloudflare.cfg or ~/.cloudflare/cloudflare.cfg files, in that order.

If you're using an API Token, any `cloudflare.cfg` file must either not contain an `email` attribute or be a zero length string and the `CF_API_EMAIL` environment variable must be unset or be a zero length string, otherwise the token will be treated as a key and will throw an error.

There is one call that presently doesn't need any email or token certification (the */ips* call); hence you can test without any values saved away.

### Using shell environment variables

```bash
$ export CF_API_EMAIL='user@example.com' # Do not set if using an API Token
$ export CF_API_KEY='00000000000000000000000000000000'
$ export CF_API_CERTKEY='v1.0-...'
$
```

These are optional environment variables; however, they do override the values set within a configuration file.

### Using configuration file to store email and keys

```bash
$ cat ~/.cloudflare/cloudflare.cfg
[CloudFlare]
email = user@example.com # Do not set if using an API Token
token = 00000000000000000000000000000000
certtoken = v1.0-...
extras =
$
```

More than one profile can be stored within that file.
Here's an example for a work and home setup (in this example work has an API Token and home uses email/token).

```bash
$ cat ~/.cloudflare/cloudflare.cfg
[Work]
token = 00000000000000000000000000000000
[Home]
email = home@example.com
token = 00000000000000000000000000000000
$
```

To select a profile, use the `--profile profile-name` option for `cli4` command or use `profile="profile-name"` in the library call.

```bash
$ cli4 --profile Work /zones | jq '.[]|.name' | wc -l
      13
$

$ cli4 --profile Home /zones | jq '.[]|.name' | wc -l
       1
$
```

Here is the same in code.

```python
#!/usr/bin/env python

import CloudFlare

def main():
    cf = CloudFlare.CloudFlare(profile="Work")
    ...
```

### Advanced use of configuration file for authentication based on method

The configuration file can have values that are both generic and specific to the method.
Here's an example where a project has a different API Token for reading and writing values.

```bash
$ cat ~/.cloudflare/cloudflare.cfg
[Work]
token = 0000000000000000000000000000000000000000
token.get = 0123456789012345678901234567890123456789
$
```

When a GET call is processed then the second token is used. For all other calls the first token is used.
Here's a more explict verion of that config:

```bash
$ cat ~/.cloudflare/cloudflare.cfg
[Work]
token.delete = 0000000000000000000000000000000000000000
token.get = 0123456789012345678901234567890123456789
token.patch = 0000000000000000000000000000000000000000
token.post = 0000000000000000000000000000000000000000
token.put = 0000000000000000000000000000000000000000
$
```

This can be used with email values also.

### About /certificates and certtoken

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
import CloudFlare

def main():
    cf = CloudFlare.CloudFlare()
    zones = cf.zones.get(params={'per_page':5})
    print(len(zones))

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
import CloudFlare

def main():
    cf = CloudFlare.CloudFlare(raw=True)
    zones = cf.zones.get(params={'per_page':5})
    
    print(zones.length())
    print(json.dumps(zones, indent=4, sort_keys=True))

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
import CloudFlare

    ...
    try
        r = ...
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('api error: %d %s' % (e, e))
    ...
```

The other raised response is **CloudFlareInternalError** which can happen when calling an invalid method.

In some cases more than one error is returned. In this case the return value **e** is also an array.
You can iterate over that array to see the additional error.

```python
import sys
import CloudFlare

    ...
    try
        r = ...
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        if len(e) > 0:
            sys.stderr.write('api error - more than one error value returned!\n')
            for x in e:
                sys.stderr.write('api error: %d %s\n' % (x, x))
        exit('api error: %d %s' % (e, e))
    ...
```

### Exception examples

Here's examples using the CLI command cli4 of the responses passed back in exceptions.

First a simple get with a clean (non-error) response.

```
$ cli4 /zones/:example.com/dns_records | jq -c '.[]|{"name":.name,"type":.type,"content":.content}'
{"name":"example.com","type":"MX","content":"something.example.com"}
{"name":"something.example.com","type":"A","content":"10.10.10.10"}
$
```

Next a simple/single error response.
This is simulated by providing incorrect authentication information.

```
$ CF_API_EMAIL='someone@example.com' cli4 /zones/
cli4: /zones - 9103 Unknown X-Auth-Key or X-Auth-Email
$
```

More than one call can be done on the same command line. In this mode, the connection is preserved between calls.
```
$ cli4 /user/organizations /user/invites
...
$
```
Note that the output is presently two JSON structures one after the other - so less useful that you may think.

Finally, a command that provides more than one error response.
This is simulated by passing an invalid IPv4 address to a DNS record creation.

```
$ cli4 --post name='foo' type=A content="1" /zones/:example.com/dns_records
cli4: /zones/:example.com/dns_records - 9005 Content for A record is invalid. Must be a valid IPv4 address
cli4: /zones/:example.com/dns_records - 1004 DNS Validation Error
$
```

## Included example code

The [examples](https://github.com/cloudflare/python-cloudflare/tree/master/examples) folder contains many examples in both simple and verbose formats.

## A DNS zone code example

```python
#!/usr/bin/env python

import sys
import CloudFlare

def main():
    zone_name = sys.argv[1]
    cf = CloudFlare.CloudFlare()
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

## A DNS zone delete code example (be careful)

```python
#!/usr/bin/env python

import sys
import CloudFlare

def main():
    zone_name = sys.argv[1]
    cf = CloudFlare.CloudFlare()
    zone_info = cf.zones.get(params={'name': zone_name})
    zone_id = zone_info['id']

    dns_name = sys.argv[2]
    dns_records = cf.zones.dns_records.get(zone_id, params={'name':dns_name + '.' + zone_name})
    for dns_record in dns_records:
        dns_record_id = dns_record['id']
        r = cf.zones.dns_records.delete(zone_id, dns_record_id)
    exit(0)

if __name__ == '__main__':
    main()
```

## CLI

All API calls can be called from the command line.
The command will convert domain names prefixed with a colon (`:`) into zone_identifiers: e.g. to view `example.com` you must use `cli4 /zones/:example.com` (the zone ID cannot be used).

```bash
$ cli4 [-V|--version] [-h|--help] [-v|--verbose] [-q|--quiet] [-j|--json] [-y|--yaml] [-r|--raw] [-d|--dump] [--get|--patch|--post|--put|--delete] [item=value ...] /command...

```

### CLI parameters for POST/PUT/PATCH

For API calls that need to pass data or parameters there is various formats to use.

The simplest form is ```item=value```. This passes the value as a string within the APIs JSON data.

If you need a numeric value passed then **==** can be used to force the value to be treated as a numeric value within the APIs JSON data.
For example: ```item==value```.

if you need to pass a list of items; then **[]** can be used. For example:

```
pool_id1="11111111111111111111111111111111"
pool_id2="22222222222222222222222222222222"
pool_id3="33333333333333333333333333333333"
cli4 --post global_pools="[ ${pool_id1}, ${pool_id2}, ${pool_id3} ]" region_pools="[ ]" /user/load_balancers/maps
```

Data or parameters can be either named or unnamed.
It can not be both.
Named is the majority format; as described above.
Unnamed parameters simply don't have anything before the **=** sign, as in ```=value```.
This format is presently only used by the Cloudflare Load Balancer API calls.
For example:

```
cli4 --put ="00000000000000000000000000000000" /user/load_balancers/maps/:00000000000000000000000000000000/region/:WNAM
```

Data can also be uploaded from file contents. Using the ```item=@filename``` format will open the file and the contents uploaded in the POST.

### CLI output

The output from the CLI command is in JSON or YAML format (and human readable). This is controled by the **--yaml** or **--json** flags (JSON is the default).

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
    "id": "00000000000000000000000000000000",
    "name": "test.example.com",
    "type": "A",
    "content": "10.0.0.1",
    ...
}
$

$ cli4 /zones/:example.com/dns_records/:test.example.com | jq '{"id":.id,"name":.name,"type":.type,"content":.content}'
{
  "id": "00000000000000000000000000000000",
  "name": "test.example.com",
  "type": "A",
  "content": "10.0.0.1"
}

$ cli4 --delete /zones/:example.com/dns_records/:test.example.com | jq -c .
{"id":"00000000000000000000000000000000"}
$
```

There's the ability to handle dns entries with multiple values.
This produces more than one API call within the command.

```
$ cli4 /zones/:example.com/dns_records/:test.example.com | jq -c '.[]|{"id":.id,"name":.name,"type":.type,"content":.content}'
{"id":"00000000000000000000000000000000","name":"test.example.com","type":"A","content":"192.168.0.1"}
{"id":"00000000000000000000000000000000","name":"test.example.com","type":"AAAA","content":"2001:d8b::1"}
$
```

Here are the cache purging commands.

```bash
$ cli4 --delete purge_everything=true /zones/:example.com/purge_cache | jq -c .
{"id":"00000000000000000000000000000000"}
$

$ cli4 --delete files='[http://example.com/css/styles.css]' /zones/:example.com/purge_cache | jq -c .
{"id":"00000000000000000000000000000000"}
$

$ cli4 --delete files='[http://example.com/css/styles.css,http://example.com/js/script.js]' /zones/:example.com/purge_cache | jq -c .
{"id":"00000000000000000000000000000000"}
$

$ cli4 --delete tags='[tag1,tag2,tag3]' /zones/:example.com/purge_cache | jq -c .
cli4: /zones/:example.com/purge_cache - 1107 Only enterprise zones can purge by tag.
$
```

A somewhat useful listing of available plans for a specific zone.

```bash
$ cli4 /zones/:example.com/available_plans | jq -c '.[]|{"id":.id,"name":.name}'
{"id":"00000000000000000000000000000000","name":"Pro Website"}
{"id":"00000000000000000000000000000000","name":"Business Website"}
{"id":"00000000000000000000000000000000","name":"Enterprise Website"}
{"id":"0feeeeeeeeeeeeeeeeeeeeeeeeeeeeee","name":"Free Website"}
$
```

### Cloudflare CA CLI examples

Here's some Cloudflare CA examples. Note the need of the zone_id= parameter with the basic **/certificates** call.

```bash
$ cli4 /zones/:example.com | jq -c '.|{"id":.id,"name":.name}'
{"id":"12345678901234567890123456789012","name":"example.com"}
$

$ cli4 zone_id=12345678901234567890123456789012 /certificates | jq -c '.[]|{"id":.id,"expires_on":.expires_on,"hostnames":.hostnames,"certificate":.certificate}'
{"id":"123456789012345678901234567890123456789012345678","expires_on":"2032-01-29 22:36:00 +0000 UTC","hostnames":["*.example.com","example.com"],"certificate":"-----BEGIN CERTIFICATE-----\n ... "}
{"id":"123456789012345678901234567890123456789012345678","expires_on":"2032-01-28 23:23:00 +0000 UTC","hostnames":["*.example.com","example.com"],"certificate":"-----BEGIN CERTIFICATE-----\n ... "}
{"id":"123456789012345678901234567890123456789012345678","expires_on":"2032-01-28 23:20:00 +0000 UTC","hostnames":["*.example.com","example.com"],"certificate":"-----BEGIN CERTIFICATE-----\n ... "}
$
```

A certificate can be viewed via a simple GET request.
```bash
$ cli4 /certificates/:123456789012345678901234567890123456789012345678
{
    "certificate": "-----BEGIN CERTIFICATE-----\n ... ",
    "expires_on": "2032-01-29 22:36:00 +0000 UTC",
    "hostnames": [
        "*.example.com",
        "example.com"
    ],
    "id": "123456789012345678901234567890123456789012345678",
    "request_type": "origin-rsa"
}
$
```

Creating a certificate. This is done with a **POST** request. Note the use of **==** in order to pass a decimal number (vs. string) in JSON. The CSR is not shown for simplicity sake.
```bash
$ CSR=`cat example.com.csr`
$ cli4 --post hostnames='["example.com","*.example.com"]' requested_validity==365 request_type="origin-ecc" csr="$CSR" /certificates
{
    "certificate": "-----BEGIN CERTIFICATE-----\n ... ",
    "csr": "-----BEGIN CERTIFICATE REQUEST-----\n ... ",
    "expires_on": "2018-09-27 21:47:00 +0000 UTC",
    "hostnames": [
        "*.example.com",
        "example.com"
    ],
    "id": "123456789012345678901234567890123456789012345678",
    "request_type": "origin-ecc",
    "requested_validity": 365
}
$
```

Deleting a certificate can be done with a **DELETE** call.
```bash
$ cli4 --delete /certificates/:123456789012345678901234567890123456789012345678
{
    "id": "123456789012345678901234567890123456789012345678",
    "revoked_at": "0000-00-00T00:00:00Z"
}
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

### Paging thru lists (using cursors)

Some API calls use cursors to read beyond the initally returned values. See the API page in order to see which API calls do this.

```
$ ACCOUNT_ID="00000000000000000000000000000000"
$ LIST_ID="00000000000000000000000000000000"
$
$ cli4 --raw /accounts/::${ACCOUNT_ID}/rules/lists/::${LIST_ID}/items > /tmp/page1.json
$ after=`jq -r '.result_info.cursors.after' < /tmp/page1.json`
$ echo "after=$after"
after=Mxm4GVmKjYbFjy2VxMPipnJigm1M_s6lCS9ABR9wx-RM2A
$
```

Once we have the ```after``` value, we can pass it along in order to read the next hunk of values. We finish when ```after``` returns as null (or isn't present).

```
$ cli4 --raw cursor="$after" /accounts/::${ACCOUNT_ID}/rules/lists/::${LIST_ID}/items > /tmp/page2.json
$ after=`jq -r '.result_info.cursors.after' < /tmp/page2.json`
$ echo "after=$after"
after=null
$
```

We can see the results now in two files.

```
$ jq -c '.result[]' < /tmp/page1.json | wc -l
      25
$

$ jq -c '.result[]' < /tmp/page2.json | wc -l
       5
$

$ for f in /tmp/page?.json ; do jq -r '.result[]|.id,.ip,.comment' < $f | paste - - - ; done | column -s'   ' -t
0fe44928258549feb47126a966fbf4a0  0.0.0.0           all zero
2e1e02120f5e466f8c0e26375e4cf4c8  1.0.0.1           Cloudflare DNS a
9ca5fd0ac6f54fdbb9dedd3fb72ce2da  1.1.1.1           Cloudflare DNS b
b3654987446743738c782f36ebe074f5  10.0.0.0/8        RFC1918 space
90bec8ce37d242faa2e27d1e78c1d8e2  103.21.244.0/22   Cloudflare IP
970a3c810cda41af9bef2c36a1892f7e  103.22.200.0/22   Cloudflare IP
3ec8516158bf4f3cac18210f611ee541  103.31.4.0/22     Cloudflare IP
ee9d268367204e6bb8e5e4c907f22de8  104.16.0.0/12     Cloudflare IP
93ae02eda9774c45840af367a02fe529  108.162.192.0/18  Cloudflare IP
62891ebf6db44aa494d79a6401af185e  131.0.72.0/22     Cloudflare IP
cac40cd940cc470582b8c912a8a12bea  141.101.64.0/18   Cloudflare IP
f6d5eacd81a2407f8e0d81caee21e7f8  162.158.0.0/15    Cloudflare IP
3d538dfc38ab471d9d3fe78332acfa4e  172.16.0.0/12     RFC1918 space
f353cb8f98424837ad35382a22b9debe  172.64.0.0/13     Cloudflare IP
78f3e1a0bafc41f88d4d40ad49a642e0  173.245.48.0/20   Cloudflare IP
c23a545475c54c32a7681c6b508d3e80  188.114.96.0/20   Cloudflare IP
f693237c9e294fe481221cbc2d7c20ef  190.93.240.0/20   Cloudflare IP
6d465ab3a0994c07827ebdcf8f34d977  192.168.0.0/16    RFC1918 space
1ad1e634b3664bac939086185c62faf7  197.234.240.0/22  Cloudflare IP
5d2968e7b3114d8e869a379d71c8ba86  198.41.128.0/17   Cloudflare IP
6a69de60b31448fa864f0a3ac5abe8d0  224.0.0.0/24      Multicast
30749cce89af4ab3a80e308294f46a46  240.0.0.0/4       Class E
2b32c67ea4d044628abe39f28662d8f0  255.255.255.255   all ones
cc7cd828b2fb4bcfb9391c2d3ef8d068  2400:cb00::/32    Cloudflare IP
b30d4cbd7dcd48729e8ebeda552e48a8  2405:8100::/32    Cloudflare IP
49db60758c8344959c338a74afc9748a  2405:b500::/32    Cloudflare IP
96e9eca1923c40d5a84865145f5a5d6a  2606:4700::/32    Cloudflare IP
21bc52a26e10405d89b7180ddcf49302  2803:f800::/32    Cloudflare IP
ff78f842188e4b869eb5389ae9ab8f41  2a06:98c0::/29    Cloudflare IP
0880cdfc40b14f6fa0639522a728859d  2c0f:f248::/32    Cloudflare IP
$
```

The ```result_info.cursors``` area also contains a ```before``` value for reverse scrolling.

As with ```per_page``` scrolling, raw mode is used.

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

### Zone file upload and download CLI examples (uses BIND format files)

Refer to [Import DNS records](https://api.cloudflare.com/#dns-records-for-a-zone-import-dns-records) on API documentation for this feature.

```bash
$ cat zone.txt
example.com.            IN      SOA     somewhere.example.com. someone.example.com. (
                                2017010101
                                3H
                                15
                                1w
                                3h
                        )

record1.example.com.    IN      A       10.0.0.1
record2.example.com.    IN      AAAA    2001:d8b::2
record3.example.com.    IN      CNAME   record1.example.com.
record4.example.com.    IN      TXT     "some text"
$

$ cli4 --post file=@zone.txt /zones/:example.com/dns_records/import
{
    "recs_added": 4,
    "total_records_parsed": 4
}
$
```

The following is documented within the **Advanced** option of the DNS page within the Cloudflare portal.

```
$ cli4 /zones/:example.com/dns_records/export | egrep -v '^;;|^$'
$ORIGIN .
@	3600	IN	SOA	example.com.	root.example.com.	(
		2025552311	; serial
		7200		; refresh
		3600		; retry
		86400		; expire
		3600)		; minimum
example.com.	300	IN	NS	REPLACE&ME$WITH^YOUR@NAMESERVER.
record4.example.com.	300	IN	TXT	"some text"
record3.example.com.	300	IN	CNAME	record1.example.com.
record1.example.com.	300	IN	A	10.0.0.1
record2.example.com.	300	IN	AAAA	2001:d8b::2
$
```

The egrep is used for documentation brevity.

This can also be done via Python code with the following example.
```
#!/usr/bin/env python
import sys
import CloudFlare

def main():
    zone_name = sys.argv[1]
    cf = CloudFlare.CloudFlare()

    zones = cf.zones.get(params={'name': zone_name})
    zone_id = zones[0]['id']

    dns_records = cf.zones.dns_records.export.get(zone_id)
    for l in dns_records.splitlines():
        if len(l) == 0 or l[0] == ';':
            continue
        print(l)
    exit(0)

if __name__ == '__main__':
    main()
```

### Cloudflare Workers

Cloudflare Workers are described on the Cloudflare blog at
[here](https://blog.cloudflare.com/introducing-cloudflare-workers/) and
[here](https://blog.cloudflare.com/code-everywhere-cloudflare-workers/), with the beta release announced
[here](https://blog.cloudflare.com/cloudflare-workers-is-now-on-open-beta/).

The Python libraries now support the Cloudflare Workers API calls. The following javascript is lifted from [https://cloudflareworkers.com/](https://cloudflareworkers.com/) and slightly modified.

```
$ cat modify-body.js
addEventListener("fetch", event => {
  event.respondWith(fetchAndModify(event.request));
});

async function fetchAndModify(request) {
  console.log("got a request:", request);

  // Send the request on to the origin server.
  const response = await fetch(request);

  // Read response body.
  const text = await response.text();

  // Modify it.
  const modified = text.replace(
  "<body>",
  "<body style=\"background: #ff0;\">");

  // Return modified response.
  return new Response(modified, {
    status: response.status,
    statusText: response.statusText,
    headers: response.headers
  });
}
$
```

Here's the website with it's simple ```<body>``` statement

```
$ curl -sS https://example.com/ | fgrep '<body'
  <body>
$
```

Now lets add the script. Looking above, you will see that it's simple action is to modify the ```<body>``` statement and make the background yellow.

```
$ cli4 --put @- /zones/:example.com/workers/script < modify-body.js
{
    "etag": "1234567890123456789012345678901234567890123456789012345678901234",
    "id": "example-com",
    "modified_on": "2018-02-15T00:00:00.000000Z",
    "script": "addEventListener(\"fetch\", event => {\n  event.respondWith(fetchAndModify(event.request));\n});\n\nasync function fetchAndModify(request) {\n  console.log(\"got a request:\", request);\n\n  // Send the request on to the origin server.\n  const response = await fetch(request);\n\n  // Read response body.\n  const text = await response.text();\n\n  // Modify it.\n  const modified = text.replace(\n  \"<body>\",\n  \"<body style=\\\"background: #ff0;\\\">\");\n\n  // Return modified response.\n  return new Response(modified, {\n    status: response.status,\n    statusText: response.statusText,\n    headers: response.headers\n  });\n}\n",
    "size": 603
}
$
```

The following call checks that the script is associated with the zone. In this case, it's the only script added by this user.

```
$ cli4 /user/workers/scripts
[
    {
        "created_on": "2018-02-15T00:00:00.000000Z",
        "etag": "1234567890123456789012345678901234567890123456789012345678901234",
        "id": "example-com",
        "modified_on": "2018-02-15T00:00:00.000000Z"
    }
]
$
```

Next step is to make sure a route is added for that script on that zone.

```
$ cli4 --post pattern="example.com/*" script="example-com" /zones/:example.com/workers/routes
{
    "id": "12345678901234567890123456789012"
}
$

$ cli4 /zones/:example.com/workers/routes
[
    {
        "id": "12345678901234567890123456789012",
        "pattern": "example.com/*",
        "script": "example-com"
    }
]
$
```

With that script added to the zone and the route added, we can now see the website has been modified because of the Cloudflare Worker.

```
$ curl -sS https://example.com/ | fgrep '<body'
  <body style="background: #ff0;">
$
```

All this can be removed; hence bringing the website back to its initial state.

```
$ cli4 --delete /zones/:example.com/workers/script
12345678901234567890123456789012
$ cli4 --delete /zones/:example.com/workers/routes/:12345678901234567890123456789012
true
$

$ curl -sS https://example.com/ | fgrep '<body'
  <body>
$
```

Refer to the Cloudflare Workers API documentation for more information.

## Cloudflare GraphQL

The GraphQL interface can be accessed via the command line or via Python.

```
    query="""
      query {
        viewer {
            zones(filter: {zoneTag: "%s"} ) {
            httpRequests1dGroups(limit:40, filter:{date_lt: "%s", date_gt: "%s"}) {
              sum { countryMap { bytes, requests, clientCountryName } }
              dimensions { date }
            }
          }
        }
      }
    """ % (zone_id, date_before[0:10], date_after[0:10])

    r = cf.graphql.post(data={'query':query})

    httpRequests1dGroups = zone_info = r['data']['viewer']['zones'][0]['httpRequests1dGroups']
```

See the [examples/example_graphql.sh](examples/example_graphql.sh) and [examples/example_graphql.py](examples/example_graphql.py) files for working examples.
Here is the working example of the shell version:

```
$ examples/example_graphql.sh example.com
2020-07-14T02:00:00Z	34880
2020-07-14T03:00:00Z	18953
2020-07-14T04:00:00Z	28700
2020-07-14T05:00:00Z	2358
2020-07-14T06:00:00Z	34905
2020-07-14T07:00:00Z	779
2020-07-14T08:00:00Z	35450
2020-07-14T10:00:00Z	17803
2020-07-14T11:00:00Z	32678
2020-07-14T12:00:00Z	19947
2020-07-14T13:00:00Z	4956
2020-07-14T14:00:00Z	34585
2020-07-14T15:00:00Z	3022
2020-07-14T16:00:00Z	5224
2020-07-14T18:00:00Z	79482
2020-07-14T21:00:00Z	10609
2020-07-14T22:00:00Z	5740
2020-07-14T23:00:00Z	2545
2020-07-15T01:00:00Z	10777
$
```

For more information on how to use GraphQL at Cloudflare, refer to the [Cloudflare GraphQL Analytics API](https://developers.cloudflare.com/analytics/graphql-api).
It contains a full overview of Cloudflare's GraphQL features and keywords.

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

As of May/June 2016 the code is now tested against pylint.
This was required in order to move the codebase into Python 3.x.
The motivation for this came from [Danielle Madeley (danni)](https://github.com/danni).

~~While the codebase has been edited to run on Python 3.x, there's not been enough Python 3.x testing performed.~~
~~If you can help in this regard; please contact the maintainers.~~

As of January 2020 the code is Python3 clean.

As of January 2020 the code is shipped up to pypi with Python2 support removed.

As of January 2020 the code is Python3.8 clean. The new `SyntaxWarning` messages (i.e. `SyntaxWarning: "is" with a literal. Did you mean "=="?`) meant minor edits were needed.

## Credit

This is based on work by [Felix Wong (gnowxilef)](https://github.com/gnowxilef) found [here](https://github.com/cloudflare-api/python-cloudflare-v4).
It has been seriously expanded upon.

## Changelog

An automatically generated CHANGELOG is provided [here](CHANGELOG.md).

## Copyright

Portions copyright [Felix Wong (gnowxilef)](https://github.com/gnowxilef) 2015 and Cloudflare 2016.
