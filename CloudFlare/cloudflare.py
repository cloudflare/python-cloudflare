""" Cloudflare v4 API"""
from __future__ import absolute_import

import json
import requests

from .logging_helper import CFlogger
from .utils import user_agent, sanitize_secrets
from .read_configs import read_configs
from .api_v4 import api_v4
from .api_extras import api_extras
from .exceptions import CloudFlareError, CloudFlareAPIError, CloudFlareInternalError

BASE_URL = 'https://api.cloudflare.com/client/v4'

class CloudFlare(object):
    """ Cloudflare v4 API"""

    class _v4base(object):
        """ Cloudflare v4 API"""

        def __init__(self, email, token, certtoken, base_url, debug, raw, use_sessions):
            """ Cloudflare v4 API"""

            self.email = email
            self.token = token
            self.certtoken = certtoken
            self.base_url = base_url
            self.raw = raw
            self.use_sessions = use_sessions
            self.session = None
            self.user_agent = user_agent()

            if debug:
                self.logger = CFlogger(debug).getLogger()
            else:
                self.logger = None

        def call_with_no_auth(self, method, parts,
                              identifier1=None, identifier2=None, identifier3=None,
                              params=None, data=None, files=None):
            """ Cloudflare v4 API"""

            headers = {}
            self._add_headers(headers)
            return self._call(method, headers, parts,
                              identifier1, identifier2, identifier3,
                              params, data, files)

        def _add_headers(self, headers):
            """ Add default headers """
            headers['User-Agent'] = self.user_agent
            headers['Content-Type'] = 'application/json'

        def _add_auth_headers(self, headers):
            """ Add authentication headers """
            if self.email is None and self.token is None:
                raise CloudFlareAPIError(0, 'no email and no token defined')
            if self.token is None:
                raise CloudFlareAPIError(0, 'no token defined')
            if self.email is None:
                headers['Authorization'] = 'Bearer %s' % (self.token)
            else:
                headers['X-Auth-Email'] = self.email
                headers['X-Auth-Key'] = self.token

        def _add_certtoken_headers(self, headers):
            """ Add authentication headers """
            if self.certtoken is None:
                raise CloudFlareAPIError(0, 'no cert token defined')
            headers['X-Auth-User-Service-Key'] = self.certtoken

        def call_with_auth(self, method, parts,
                           identifier1=None, identifier2=None, identifier3=None,
                           params=None, data=None, files=None):
            """ Cloudflare v4 API"""

            headers = {}
            self._add_headers(headers)
            self._add_auth_headers(headers)
            if type(data) == str:
                # passing javascript vs JSON
                headers['Content-Type'] = 'application/javascript'
            if files:
                # overwrite Content-Type as we are uploading data
                headers['Content-Type'] = 'multipart/form-data'
                # however something isn't right and this works ... look at again later!
                del headers['Content-Type']
            return self._call(method, headers, parts,
                              identifier1, identifier2, identifier3,
                              params, data, files)

        def call_with_auth_unwrapped(self, method, parts,
                                     identifier1=None, identifier2=None, identifier3=None,
                                     params=None, data=None, files=None):
            """ Cloudflare v4 API"""

            headers = {}
            self._add_headers(headers)
            self._add_auth_headers(headers)
            if type(data) == str:
                # passing javascript vs JSON
                headers['Content-Type'] = 'application/javascript'
            if files:
                # overwrite Content-Type as we are uploading data
                headers['Content-Type'] = 'multipart/form-data'
                # however something isn't right and this works ... look at again later!
                del headers['Content-Type']
            return self._call_unwrapped(method, headers, parts,
                                        identifier1, identifier2, identifier3,
                                        params, data, files)

        def call_with_certauth(self, method, parts,
                               identifier1=None, identifier2=None, identifier3=None,
                               params=None, data=None, files=None):
            """ Cloudflare v4 API"""

            headers = {}
            self._add_headers(headers)
            self._add_certtoken_headers(headers)
            return self._call(method, headers, parts,
                              identifier1, identifier2, identifier3,
                              params, data, files)

        def _network(self, method, headers, parts,
                     identifier1=None, identifier2=None, identifier3=None,
                     params=None, data=None, files=None):
            """ Cloudflare v4 API"""

            if self.logger:
                self.logger.debug('Call: %s,%s,%s,%s,%s,%s',
                                  str(parts[0]),
                                  str(identifier1),
                                  str(parts[1]),
                                  str(identifier2),
                                  str(parts[2]),
                                  str(identifier3))
                self.logger.debug('Call: optional params and data %s %s',
                                  str(params),
                                  str(data))
                if files:
                    self.logger.debug('Call: upload file %r', files)

            if (method is None) or (parts[0] is None):
                # should never happen
                raise CloudFlareInternalError(0, 'You must specify a method and endpoint')

            if parts[1] is not None or (data is not None and method == 'GET'):
                if identifier1 is None:
                    raise CloudFlareAPIError(0, 'You must specify identifier1')
                if identifier2 is None:
                    url = (self.base_url + '/'
                           + parts[0] + '/'
                           + identifier1 + '/'
                           + parts[1])
                else:
                    url = (self.base_url + '/'
                           + parts[0] + '/'
                           + identifier1 + '/'
                           + parts[1] + '/'
                           + identifier2)
            else:
                if identifier1 is None:
                    url = (self.base_url + '/'
                           + parts[0])
                else:
                    url = (self.base_url + '/'
                           + parts[0] + '/'
                           + identifier1)
            if parts[2]:
                url += '/' + parts[2]
            if identifier3:
                url += '/' + identifier3

            if self.logger:
                self.logger.debug('Call: method and url %s %s', str(method), str(url))
                self.logger.debug('Call: headers %s', str(sanitize_secrets(headers)))

            method = method.upper()

            if self.logger:
                self.logger.debug('Call: doit!')

            if self.use_sessions:
                if self.session is None:
                    self.session = requests.Session()
            else:
                self.session = requests

            try:
                if method == 'GET':
                    response = self.session.get(url,
                                                headers=headers,
                                                params=params,
                                                data=data)
                elif method == 'POST':
                    if type(data) == str:
                        response = self.session.post(url,
                                                     headers=headers,
                                                     params=params,
                                                     data=data,
                                                     files=files)
                    else:
                        response = self.session.post(url,
                                                     headers=headers,
                                                     params=params,
                                                     json=data,
                                                     files=files)
                elif method == 'PUT':
                    if type(data) == str:
                        response = self.session.put(url,
                                                    headers=headers,
                                                    params=params,
                                                    data=data)
                    else:
                        response = self.session.put(url,
                                                    headers=headers,
                                                    params=params,
                                                    json=data)
                elif method == 'DELETE':
                    if type(data) == str:
                        response = self.session.delete(url,
                                                       headers=headers,
                                                       params=params,
                                                       data=data)
                    else:
                        response = self.session.delete(url,
                                                       headers=headers,
                                                       params=params,
                                                       json=data)
                elif method == 'PATCH':
                    if type(data) == str:
                        response = self.session.request('PATCH', url,
                                                        headers=headers,
                                                        params=params,
                                                        data=data)
                    else:
                        response = self.session.request('PATCH', url,
                                                        headers=headers,
                                                        params=params,
                                                        json=data)
                else:
                    # should never happen
                    raise CloudFlareAPIError(0, 'method not supported')
                if self.logger:
                    self.logger.debug('Call: done!')
            except Exception as e:
                if self.logger:
                    self.logger.debug('Call: exception! "%s"' % (e))
                raise CloudFlareAPIError(0, 'connection failed.')

            if self.logger:
                self.logger.debug('Response: url %s', response.url)

            # Create response_{type|code|data}
            try:
                response_type = response.headers['Content-Type']
                if ';' in response_type:
                    # remove the ;paramaters part (like charset=, etc.)
                    response_type = response_type[0:response_type.rfind(';')]
                response_type = response_type.strip().lower()
            except:
                # API should always response; but if it doesn't; here's the default
                response_type = 'application/octet-stream'
            response_code = response.status_code
            response_data = response.content
            if type(response_data) != str:
                response_data = response_data.decode("utf-8")

            if self.logger:
                self.logger.debug('Response: %d, %s, %s',
                                  response_code, response_type, response_data)

            if response_code >= 500 and response_code <= 599:
                # 500 Internal Server Error
                # 501 Not Implemented
                # 502 Bad Gateway
                # 503 Service Unavailable
                # 504 Gateway Timeout
                # 505 HTTP Version Not Supported
                # 506 Variant Also Negotiates
                # 507 Insufficient Storage
                # 508 Loop Detected
                # 509 Unassigned
                # 510 Not Extended
                # 511 Network Authentication Required

                # the libary doesn't deal with these errors, just pass upwards!
                # there's no value to add and the returned data is questionable or not useful
                response.raise_for_status()

                # should not be reached
                raise CloudFlareInternalError(0, 'internal error in status code processing')

            #if response_code >= 400 and response_code <= 499:
            #    # 400 Bad Request
            #    # 401 Unauthorized
            #    # 403 Forbidden
            #    # 405 Method Not Allowed
            #    # 415 Unsupported Media Type
            #    # 429 Too many requests
            #
            #    # don't deal with these errors, just pass upwards!
            #    response.raise_for_status()
            #
            #if response_code >= 300 and response_code <= 399:
            #    # 304 Not Modified
            #
            #    # don't deal with these errors, just pass upwards!
            #    response.raise_for_status()
            #
            # should be a 200 response at this point

            return [response_type, response_code, response_data]

        def _raw(self, method, headers, parts,
                 identifier1=None, identifier2=None, identifier3=None,
                 params=None, data=None, files=None):
            """ Cloudflare v4 API"""

            [response_type, response_code, response_data] = self._network(method,
                                                                          headers, parts,
                                                                          identifier1,
                                                                          identifier2,
                                                                          identifier3,
                                                                          params, data, files)

            if response_type == 'application/json':
                # API says it's JSON; so it better be parsable as JSON
                # NDJSON is returned by Enterprise Log Share i.e. /zones/:id/logs/received
                if hasattr(response_data, 'decode'):
                    response_data = response_data.decode('utf-8')
                try:
                    response_data = json.loads(response_data)
                except ValueError:
                    if response_data == '':
                        # This should really be 'null' but it isn't. Even then, it's wrong!
                        if response_code == requests.codes.ok:
                            # 200 ok
                            response_data = {'success': True,
                                             'result': None}
                        else:
                            # 3xx & 4xx errors
                            response_data = {'success': False,
                                             'code': response_code,
                                             'result': None}
                    else:
                        # Lets see if it's NDJSON data
                        # NDJSON is a series of JSON elements with newlines between each element
                        try:
                            r = []
                            for l in response_data.splitlines():
                                r.append(json.loads(l))
                            response_data = r
                        except:
                            # While this should not happen; it's always possible
                            if self.logger:
                                self.logger.debug('Response data not JSON: %r', response_data)
                            raise CloudFlareAPIError(0, 'JSON parse failed - report to Cloudflare.')

                if response_code == requests.codes.ok:
                    # 200 ok - so nothing needs to be done
                    pass
                else:
                    # 3xx & 4xx errors - we should report that somehow - but not quite yet
                    # response_data['code'] = response_code
                    pass
            elif response_type == 'text/plain' or response_type == 'application/octet-stream':
                # API says it's text; but maybe it's actually JSON? - should be fixed in API
                if hasattr(response_data, 'decode'):
                    response_data = response_data.decode('utf-8')
                try:
                    response_data = json.loads(response_data)
                except ValueError:
                    # So it wasn't JSON - moving on as if it's text!
                    # A single value is returned (vs an array or object)
                    if response_code == requests.codes.ok:
                        # 200 ok
                        response_data = {'success': True, 'result': str(response_data)}
                    else:
                        # 3xx & 4xx errors
                        response_data = {'success': False,
                                         'code': response_code,
                                         'result': str(response_data)}
            elif response_type == 'text/javascript' or response_type == 'application/javascript':
                # used by Cloudflare workers
                if response_code == requests.codes.ok:
                    # 200 ok
                    response_data = {'success': True,
                                     'result': str(response_data)}
                else:
                    # 3xx & 4xx errors
                    response_data = {'success': False,
                                     'code': response_code,
                                     'result': str(response_data)}
            elif response_type == 'text/html':
                # used by media for preview
                if response_code == requests.codes.ok:
                    # 200 ok
                    response_data = {'success': True,
                                     'result': str(response_data)}
                else:
                    # 3xx & 4xx errors
                    response_data = {'success': False,
                                     'code': response_code,
                                     'result': str(response_data)}

            else:
                # Assuming nothing - but continuing anyway
                # A single value is returned (vs an array or object)
                if response_code == requests.codes.ok:
                    # 200 ok
                    response_data = {'success': True,
                                     'result': str(response_data)}
                else:
                    # 3xx & 4xx errors
                    response_data = {'success': False,
                                     'code': response_code,
                                     'result': str(response_data)}

            # it would be nice to return the error code and content type values; but not quite yet
            return response_data

        def _call(self, method, headers, parts,
                  identifier1=None, identifier2=None, identifier3=None,
                  params=None, data=None, files=None):
            """ Cloudflare v4 API"""

            response_data = self._raw(method, headers, parts,
                                      identifier1, identifier2, identifier3,
                                      params, data, files)

            # Sanatize the returned results - just in case API is messed up
            if 'success' not in response_data:
                if 'errors' in response_data:
                    if self.logger:
                        self.logger.debug('Response: assuming success = "False"')
                    response_data['success'] = False
                else:
                    if 'result' not in response_data:
                        # Only happens on /certificates call
                        # should be fixed in /certificates API
                        if self.logger:
                            self.logger.debug('Response: assuming success = "False"')
                        r = response_data
                        response_data['errors'] = []
                        response_data['errors'].append(r)
                        response_data['success'] = False
                    else:
                        if self.logger:
                            self.logger.debug('Response: assuming success = "True"')
                        response_data['success'] = True

            if response_data['success'] is False:
                errors = response_data['errors'][0]
                code = errors['code']
                if 'message' in errors:
                    message = errors['message']
                elif 'error' in errors:
                    message = errors['error']
                else:
                    message = ''
                if 'messages' in response_data:
                    errors['error_chain'] = response_data['messages']
                if 'error_chain' in errors:
                    error_chain = errors['error_chain']
                    for error in error_chain:
                        if self.logger:
                            self.logger.debug('Response: error %d %s - chain',
                                              error['code'],
                                              error['message'])
                    if self.logger:
                        self.logger.debug('Response: error %d %s', code, message)
                    raise CloudFlareAPIError(code, message, error_chain)
                else:
                    if self.logger:
                        self.logger.debug('Response: error %d %s', code, message)
                    raise CloudFlareAPIError(code, message)

            if self.logger:
                self.logger.debug('Response: %s', response_data['result'])
            if self.raw:
                result = {}
                # theres always a result value
                result['result'] = response_data['result']
                # theres may not be a result_info on every call
                if 'result_info' in response_data:
                    result['result_info'] = response_data['result_info']
                # no need to return success, errors, or messages as they return via an exception
            else:
                # theres always a result value
                result = response_data['result']
            return result

        def _call_unwrapped(self, method, headers, parts,
                            identifier1=None, identifier2=None, identifier3=None,
                            params=None, data=None, files=None):
            """ Cloudflare v4 API"""

            response_data = self._raw(method, headers, parts,
                                      identifier1, identifier2, identifier3,
                                      params, data, files)
            if self.logger:
                self.logger.debug('Response: %s', response_data)
            result = response_data
            return result

    class _add_unused(object):
        """ Cloudflare v4 API"""

        def __init__(self, base, p1, p2=None, p3=None):
            """ Cloudflare v4 API"""

            self._base = base
            self._parts_unused = [p1, p2, p3]

        def __call__(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            # This is the same as a get()
            return self.get(identifier1, identifier2, identifier3, params, data)

        def __str__(self):
            """ Cloudflare v4 API"""

            return '[%s]' % ('/' + '/:id/'.join(filter(None, self._parts_unused)))

        def get(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            raise CloudFlareAPIError(0, 'get() call not available for this endpoint')

        def patch(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            raise CloudFlareAPIError(0, 'patch() call not available for this endpoint')

        def post(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None, files=None):
            """ Cloudflare v4 API"""

            raise CloudFlareAPIError(0, 'post() call not available for this endpoint')

        def put(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            raise CloudFlareAPIError(0, 'put() call not available for this endpoint')

        def delete(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            raise CloudFlareAPIError(0, 'delete() call not available for this endpoint')

    class _add_noauth(object):
        """ Cloudflare v4 API"""

        def __init__(self, base, p1, p2=None, p3=None):
            """ Cloudflare v4 API"""

            self._base = base
            self._parts = [p1, p2, p3]

        def __call__(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            # This is the same as a get()
            return self.get(identifier1, identifier2, identifier3, params, data)

        def __str__(self):
            """ Cloudflare v4 API"""

            return '[%s]' % ('/' + '/:id/'.join(filter(None, self._parts)))

        def get(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            return self._base.call_with_no_auth('GET', self._parts,
                                                identifier1, identifier2, identifier3,
                                                params, data)

        def patch(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            raise CloudFlareAPIError(0, 'patch() call not available for this endpoint')

        def post(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None, files=None):
            """ Cloudflare v4 API"""

            raise CloudFlareAPIError(0, 'post() call not available for this endpoint')

        def put(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            raise CloudFlareAPIError(0, 'put() call not available for this endpoint')

        def delete(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            raise CloudFlareAPIError(0, 'delete() call not available for this endpoint')

    class _add_with_auth(object):
        """ Cloudflare v4 API"""

        def __init__(self, base, p1, p2=None, p3=None):
            """ Cloudflare v4 API"""

            self._base = base
            self._parts = [p1, p2, p3]

        def __call__(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            # This is the same as a get()
            return self.get(identifier1, identifier2, identifier3, params, data)

        def __str__(self):
            """ Cloudflare v4 API"""

            return '[%s]' % ('/' + '/:id/'.join(filter(None, self._parts)))

        def get(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            return self._base.call_with_auth('GET', self._parts,
                                             identifier1, identifier2, identifier3,
                                             params, data)

        def patch(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            return self._base.call_with_auth('PATCH', self._parts,
                                             identifier1, identifier2, identifier3,
                                             params, data)

        def post(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None, files=None):
            """ Cloudflare v4 API"""

            return self._base.call_with_auth('POST', self._parts,
                                             identifier1, identifier2, identifier3,
                                             params, data, files)

        def put(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            return self._base.call_with_auth('PUT', self._parts,
                                             identifier1, identifier2, identifier3,
                                             params, data)

        def delete(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            return self._base.call_with_auth('DELETE', self._parts,
                                             identifier1, identifier2, identifier3,
                                             params, data)

    class _add_with_auth_unwrapped(object):
        """ Cloudflare v4 API"""

        def __init__(self, base, p1, p2=None, p3=None):
            """ Cloudflare v4 API"""

            self._base = base
            self._parts = [p1, p2, p3]

        def __call__(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            # This is the same as a get()
            return self.get(identifier1, identifier2, identifier3, params, data)

        def __str__(self):
            """ Cloudflare v4 API"""

            return '[%s]' % ('/' + '/:id/'.join(filter(None, self._parts)))

        def get(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            return self._base.call_with_auth_unwrapped('GET', self._parts,
                                                       identifier1, identifier2, identifier3,
                                                       params, data)

        def patch(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            return self._base.call_with_auth_unwrapped('PATCH', self._parts,
                                                       identifier1, identifier2, identifier3,
                                                       params, data)

        def post(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None, files=None):
            """ Cloudflare v4 API"""

            return self._base.call_with_auth_unwrapped('POST', self._parts,
                                                       identifier1, identifier2, identifier3,
                                                       params, data, files)

        def put(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            return self._base.call_with_auth_unwrapped('PUT', self._parts,
                                                       identifier1, identifier2, identifier3,
                                                       params, data)

        def delete(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            return self._base.call_with_auth_unwrapped('DELETE', self._parts,
                                                       identifier1, identifier2, identifier3,
                                                       params, data)

    class _add_with_cert_auth(object):
        """ Cloudflare v4 API"""

        def __init__(self, base, p1, p2=None, p3=None):
            """ Cloudflare v4 API"""

            self._base = base
            self._parts = [p1, p2, p3]

        def __call__(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            # This is the same as a get()
            return self.get(identifier1, identifier2, identifier3, params, data)

        def __str__(self):
            """ Cloudflare v4 API"""

            return '[%s]' % ('/' + '/:id/'.join(filter(None, self._parts)))

        def get(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            return self._base.call_with_certauth('GET', self._parts,
                                                 identifier1, identifier2, identifier3,
                                                 params, data)

        def patch(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            return self._base.call_with_certauth('PATCH', self._parts,
                                                 identifier1, identifier2, identifier3,
                                                 params, data)

        def post(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None, files=None):
            """ Cloudflare v4 API"""

            return self._base.call_with_certauth('POST', self._parts,
                                                 identifier1, identifier2, identifier3,
                                                 params, data, files)

        def put(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            return self._base.call_with_certauth('PUT', self._parts,
                                                 identifier1, identifier2, identifier3,
                                                 params, data)

        def delete(self, identifier1=None, identifier2=None, identifier3=None, params=None, data=None):
            """ Cloudflare v4 API"""

            return self._base.call_with_certauth('DELETE', self._parts,
                                                 identifier1, identifier2, identifier3,
                                                 params, data)

    def add(self, t, p1, p2=None, p3=None):
        """add api call to class"""

        a = []
        if p1:
            a += p1.split('/')
        if p2:
            a += p2.split('/')
        if p3:
            a += p3.split('/')

        branch = self
        for element in a[0:-1]:
            try:
                branch = getattr(branch, element)
            except:
                # should never happen
                raise CloudFlareAPIError(0, 'api load name failed')
        name = a[-1]

        if t == 'VOID':
            f = self._add_unused(self._base, p1, p2, p3)
        elif t == 'OPEN':
            f = self._add_noauth(self._base, p1, p2, p3)
        elif t == 'AUTH':
            f = self._add_with_auth(self._base, p1, p2, p3)
        elif t == 'CERT':
            f = self._add_with_cert_auth(self._base, p1, p2, p3)
        elif t == 'AUTH_UNWRAPPED':
            f = self._add_with_auth_unwrapped(self._base, p1, p2, p3)
        else:
            # should never happen
            raise CloudFlareAPIError(0, 'api load type mismatch')

        setattr(branch, name, f)

    def api_list(self, m=None, s=''):
        """recursive walk of the api tree returning a list of api calls"""
        if m is None:
            m = self
        w = []
        for n in sorted(dir(m)):
            if n[0] == '_':
                # internal
                continue
            if n in ['delete', 'get', 'patch', 'post', 'put']:
                # gone too far
                continue
            a = getattr(m, n)
            d = dir(a)
            if '_base' in d:
                # it's a known api call - lets show the result and continue down the tree
                if 'delete' in d or 'get' in d or 'patch' in d or 'post' in d or 'put' in d:
                    # only show the result if a call exists for this part
                    if '_parts' in d:
                        w.append(s + '/' + n)
                w = w + self.api_list(a, s + '/' + n)
        return w

    def __init__(self, email=None, token=None, certtoken=None, debug=False, raw=False, use_sessions=True):
        """ Cloudflare v4 API"""

        base_url = BASE_URL

        # class creation values override configuration values
        [conf_email, conf_token, conf_certtoken, extras] = read_configs()

        if email is None:
            email = conf_email
        if token is None:
            token = conf_token
        if certtoken is None:
            certtoken = conf_certtoken

        if email == '':
            email = None
        if token == '':
            token = None
        if certtoken == '':
            certtoken = None
        self._base = self._v4base(email, token, certtoken, base_url, debug, raw, use_sessions)

        # add the API calls
        api_v4(self)
        if extras:
            api_extras(self, extras)

    def __call__(self):
        """ Cloudflare v4 API"""

        raise TypeError('object is not callable')

    def __enter__(self):
        """ Cloudflare v4 API"""
        return self

    def __exit__(self, t, v, tb):
        """ Cloudflare v4 API"""
        if t is None:
            return True
        # pretend we didn't deal with raised error - which is true
        return False

    def __str__(self):
        """ Cloudflare v4 API"""

        if self._base.email is None:
            return '["%s"]' % ('REDACTED')
        else:
            return '["%s","%s"]' % (self._base.email, 'REDACTED')

    def __repr__(self):
        """ Cloudflare v4 API"""

        if self._base.email is None:
            return '%s,%s(%s,"%s","%s",%s,"%s")' % (
                self.__module__, type(self).__name__,
                'REDACTED', 'REDACTED',
                self._base.base_url, self._base.raw, self._base.user_agent
            )
        else:
            return '%s,%s(%s,"%s","%s","%s",%s,"%s")' % (
                self.__module__, type(self).__name__,
                self._base.email, 'REDACTED', 'REDACTED',
                self._base.base_url, self._base.raw, self._base.user_agent
            )

