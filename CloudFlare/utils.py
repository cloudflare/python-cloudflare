""" misc utilities  for Cloudflare API"""


def sanitize_secrets(secrets):
    """ misc utilities  for Cloudflare API"""
    redacted_phrase = 'REDACTED'

    if secrets is None:
        return None

    secrets_copy = secrets.copy()
    if 'password' in secrets_copy:
        secrets_copy['password'] = redacted_phrase
    elif 'X-Auth-Key' in secrets_copy:
        secrets_copy['X-Auth-Key'] = redacted_phrase
    elif 'X-Auth-User-Service-Key' in secrets_copy:
        secrets_copy['X-Auth-User-Service-Key'] = redacted_phrase

    return secrets_copy
