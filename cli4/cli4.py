#!/usr/bin/env python

import os
import sys
sys.path.insert(0, os.path.abspath('..'))
import CloudFlare

import re
import getopt
import json
try:
	import yaml
except ImportError:
	yaml = None

def convert_zones_to_identifier(cf, zone_name):
	params = {'name':zone_name,'per_page':1}
	try:
		zones = cf.zones.get(params=params)
	except CloudFlare.CloudFlareAPIError as e:
		exit('cli4: %s - %d %s' % (zone_name, e, e))
	except Exception as e:
		exit('cli4: %s - %s' % (zone_name, e))

	for zone in zones:
		if zone_name == zone['name']:
			return zone['id']

	exit('cli4: %s - zone not found' % (zone_name))

def convert_dns_record_to_identifier(cf, zone_id, dns_name):
	# this can return an array of results as there can be more than one DNS entry for a name.
	params = {'name':dns_name}
	try:
		dns_records = cf.zones.dns_records.get(zone_id, params=params)
	except CloudFlare.CloudFlareAPIError as e:
		exit('cli4: %s - %d %s' % (dns_name, e, e))
	except Exception as e:
		exit('cli4: %s - %s' % (dns_name, e))

	r = []
	for dns_record in dns_records:
		if dns_name == dns_record['name']:
			r.append(dns_record['id'])
	if len(r) > 0:
		return r

	exit('cli4: %s - dns name not found' % (dns_name))

def convert_certificates_to_identifier(cf, certificate_name):
	try:
		certificates = cf.certificates.get()
	except CloudFlare.CloudFlareAPIError as e:
		exit('cli4: %s - %d %s' % (certificate_name, e, e))
	except Exception as e:
		exit('cli4: %s - %s' % (certificate_name, e))

	for certificate in certificates:
		if certificate_name in certificate['hostnames']:
			return certificate['id']

	exit('cli4: %s - no zone certificates found' % (certificate_name))

def convert_organizations_to_identifier(cf, organization_name):
	try:
		organizations = cf.user.organizations.get()
	except CloudFlare.CloudFlareAPIError as e:
		exit('cli4: %s - %d %s' % (organization_name, e, e))
	except Exception as e:
		exit('cli4: %s - %s' % (organization_name, e))

	for organization in organizations:
		if organization_name == organization['name']:
			return organization['id']

	exit('cli4: %s - no organizations found' % (organization_name))

def convert_invites_to_identifier(cf, invite_name):
	try:
		invites = cf.user.invites.get()
	except CloudFlare.CloudFlareAPIError as e:
		exit('cli4: %s - %d %s' % (invite_name, e, e))
	except Exception as e:
		exit('cli4: %s - %s' % (invite_name, e))

	for invite in invites:
		if invite_name == invite['organization_name']:
			return invite['id']

	exit('cli4: %s - no invites found' % (invite_name))

def convert_virtual_dns_to_identifier(cf, virtual_dns_name):
	try:
		virtual_dnss = cf.user.virtual_dns.get()
	except CloudFlare.CloudFlareAPIError as e:
		exit('cli4: %s - %d %s\n' % (virtual_dns_name, e, e))
	except Exception as e:
		exit('cli4: %s - %s\n' % (virtual_dns_name, e))

	for virtual_dns in virtual_dnss:
		if virtual_dns_name == virtual_dns['name']:
			return virtual_dns['id']

	exit('cli4: %s - no virtual_dns found' % (virtual_dns_name))

def cli4(args):
	verbose = False
	output = 'json'
	method = 'GET'

	usage = 'usage: cli4 [-h|--help] [-v|--verbose] [-q|--quiet] [-j|--json] [-y|--yaml] [--get|--patch|--post|-put|--delete] [item=value ...] /command...'

	try:
		opts, args = getopt.getopt(args, 'hvqjy', ['help', 'verbose', 'quiet', 'json', 'yaml', 'get', 'patch', 'post', 'put', 'delete'])
	except getopt.GetoptError:
		exit(usage)
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			exit(usage)
		elif opt in ('-v', '--verbose'):
			verbose = True
		elif opt in ('-q', '--quiet'):
			output = None
		elif opt in ('-y', '--yaml'):
			output = 'yaml'
		elif opt in ('--get'):
			method = 'GET'
		elif opt in ('-P', '--patch'):
			method = 'PATCH'
		elif opt in ('-O', '--post'):
			method = 'POST'
		elif opt in ('-U', '--put'):
			method = 'PUT'
		elif opt in ('-D', '--delete'):
			method = 'DELETE'

	digits_only = re.compile('^[0-9]+$')

	# next grab the params. These are in the form of tag=value
	params = {}
	while len(args) > 0 and '=' in args[0]:
		tag, value = args.pop(0).split('=', 1)
		if value == 'true':
			value = True
		elif value == 'false':
			value = False
		elif value[0] is '=' and digits_only.match(value[1:]):
			value = int(value[1:])
		elif (value[0] is '{' and value[-1] is '}') or (value[0] is '[' and value[-1] is ']'):
			# a json structure - used in pagerules
			try:
				#value = json.loads(value) - changed to yaml code to remove unicode string issues
				if yaml is None:
					exit('cli4: install yaml support')
				value = yaml.safe_load(value)
			except ValueError:
				exit('cli4: %s="%s" - can\'t parse json value' % (tag, value))
		params[tag] = value

	# what's left is the command itself
	if len(args) != 1:
		exit(usage)

	command = args[0]
	# remove leading and trailing /'s
	if command[0] == '/':
		command = command[1:]
	if command[-1] == '/':
		command = command[:-1]

	# bread down command into it's seperate pieces; these are then checked against the CloudFlare class to confirm there is a method that matches
	parts = command.split('/')

	cmd = []
	identifier1 = None
	identifier2 = None

	hex_only = re.compile('^[0-9a-fA-F]+$')

	cf = CloudFlare.CloudFlare(debug=verbose)

	m = cf
	for element in parts:
		if element[0] == ':':
			element = element[1:]
			if identifier1 is None:
				if len(element) in [32, 40, 48] and hex_only.match(element):
					# raw identifier - lets just use it as-is
					identifier1 = element
				elif cmd[0] == 'certificates':
					# identifier1 = convert_certificates_to_identifier(cf, element)
					identifier1 = convert_zones_to_identifier(cf, element)
				elif cmd[0] == 'zones':
					identifier1 = convert_zones_to_identifier(cf, element)
				elif cmd[0] == 'organizations':
					identifier1 = convert_organizations_to_identifier(cf, element)
				elif (cmd[0] == 'user') and (cmd[1] == 'organizations'):
					identifier1 = convert_organizations_to_identifier(cf, element)
				elif (cmd[0] == 'user') and (cmd[1] == 'invites'):
					identifier1 = convert_invites_to_identifier(cf, element)
				elif (cmd[0] == 'user') and (cmd[1] == 'virtual_dns'):
					identifier1 = convert_virtual_dns_to_identifier(cf, element)
				else:
					exit("/%s/%s :NOT CODED YET 1" % ('/'.join(cmd), element))
				cmd.append(':' + identifier1)
			else:
				if len(element) in [32, 40, 48] and hex_only.match(element):
					# raw identifier - lets just use it as-is
					identifier2 = element
				elif (cmd[0] and cmd[0] == 'zones') and (cmd[2] and cmd[2] == 'dns_records'):
					identifier2 = convert_dns_record_to_identifier(cf, identifier1, element)
				else:
					exit("/%s/%s :NOT CODED YET 2" % ('/'.join(cmd), element))
				# identifier2 may be an array - this needs to be dealt with later
				if isinstance(identifier2, list):
					cmd.append(':' + '[' + ','.join(identifier2) + ']')
				else:
					cmd.append(':' + identifier2)
					identifier2 = [identifier2]
		else:
			try:
				m = getattr(m, element)
				cmd.append(element)
			except:
				if len(cmd) == 0:
					exit('cli4: /%s - not found' % (element))
				else:
					exit('cli4: /%s/%s - not found' % ('/'.join(cmd), element))

	results = []
	if identifier2 is None:
		identifier2 = [None]
	for i2 in identifier2:
		try:
			if method is 'GET':
				r = m.get(identifier1 = identifier1, identifier2 = i2, params = params)
			elif method is 'PATCH':
				r = m.patch(identifier1 = identifier1, identifier2 = i2, data = params)
			elif method is 'POST':
				r = m.post(identifier1 = identifier1, identifier2 = i2, data = params)
			elif method is 'PUT':
				r = m.put(identifier1 = identifier1, identifier2 = i2, data = params)
			elif method is 'DELETE':
				r = m.delete(identifier1 = identifier1, identifier2 = i2, data = params)
			else:
				pass
		except CloudFlare.CloudFlareAPIError as e:
			exit('cli4: /%s - %d %s' % (command, e, e))
		except Exception as e:
			exit('cli4: /%s - %s - api error' % (command, e))

		results.append(r)

	if len(results) == 1:
		results = results[0]

	if output == 'json':
		print(json.dumps(results, indent=4, sort_keys=True))
	if output == 'yaml' and yaml is not None:
		print(yaml.safe_dump(results))

