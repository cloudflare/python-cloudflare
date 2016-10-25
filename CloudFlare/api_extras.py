""" API extras for Cloudflare API"""

import re


def api_extras(self, extras=None):
    """ API extras for Cloudflare API"""

    for extra in extras:
        if extra == '':
            continue
        extra = re.sub(r"^.*/client/v4/", '/', extra)
        extra = re.sub(r"^.*/v4/", '/', extra)
        extra = re.sub(r"^/", '', extra)

        # build parts of the extra command
        parts = []
        nn = 0
        for element in extra.split('/'):
            if element[0] == ':':
                nn += 1
                continue
            try:
                parts[nn]
            except IndexError:
                parts.append([])
            parts[nn].append(element)

        # insert extra command into class
        element_path = []
        current = self
        for element in parts[0]:
            element_path.append(element)
            try:
                m = getattr(current, element)
                # exists - but still add it there's a second part
                if element == parts[0][-1] and len(parts) > 1:
                    api_call_part1 = '/'.join(element_path)
                    api_call_part2 = '/'.join(parts[1])
                    setattr(m, parts[1][0],
                            self._add_with_auth(self._base, api_call_part1,
                                                api_call_part2))
                current = m
                continue
            except:
                pass
            # does not exist
            if element == parts[0][-1] and len(parts) > 1:
                # last element
                api_call_part1 = '/'.join(element_path)
                api_call_part2 = '/'.join(parts[1])
                setattr(current, element,
                        self._add_with_auth(self._base, api_call_part1,
                                            api_call_part2))
            else:
                api_call_part1 = '/'.join(element_path)
                setattr(current, element,
                        self._add_with_auth(self._base, api_call_part1))
            current = getattr(current, element)

