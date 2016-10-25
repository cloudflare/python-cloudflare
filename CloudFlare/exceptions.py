""" errors for Cloudflare API"""


class CloudFlareError(Exception):
    """ errors for Cloudflare API"""

    class _code_message(object):
        """
        a small class to save away an integer and string
        (the code and the message)
        """

        def __init__(self, code, message):
            self.code = code
            self.message = message

        def __int__(self):
            return self.code

        def __str__(self):
            return self.message

    def __init__(self, code, message, error_chain=None):
        """ errors for Cloudflare API"""

        self.e = self._code_message(int(code), str(message))
        self.error_chain = None
        if error_chain is not None:
            self.error_chain = []
            for e in error_chain:
                self.error_chain.append(
                    self._code_message(int(e['code']), str(e['message'])))

    def __int__(self):
        """ integer value for Cloudflare API errors"""
        return int(self.e)

    def __str__(self):
        """ string value for Cloudflare API errors"""
        return str(self.e)

    def __len__(self):
        """ Cloudflare API errors can contain a chain of errors"""
        if self.error_chain is None:
            return 0
        else:
            return len(self.error_chain)

    def __getitem__(self, ii):
        """ Cloudflare API errors can contain a chain of errors"""
        return self.error_chain[ii]

    def __iter__(self):
        """ Cloudflare API errors can contain a chain of errors"""
        if self.error_chain is None:
            raise StopIteration
        for e in self.error_chain:
            yield e

    def next(self):
        if self.error_chain is None:
            raise StopIteration()


class CloudFlareAPIError(CloudFlareError):
    """ errors for Cloudflare API"""
    pass


class CloudFlareInternalError(CloudFlareError):
    """ errors for Cloudflare API"""
    pass

