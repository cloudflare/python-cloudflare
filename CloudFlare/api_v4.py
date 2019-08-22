""" API core commands for Cloudflare API"""

def api_v4(self):
    """ API core commands for Cloudflare API"""

    # The API commands for /user/
    user(self)
    user_audit_logs(self)
    user_load_balancers(self)
    user_load_balancing_analytics(self)
    user_virtual_dns(self)
    user_workers(self)

    # The API commands for /zones/
    zones(self)
    zones_spectrum(self)
    zones_amp(self)
    zones_analytics(self)
    zones_argo(self)
    zones_dns_analytics(self)
    zones_dnssec(self)
    zones_firewall(self)
    zones_load_balancers(self)
    zones_logs(self)
    zones_media(self)
    zones_rate_limits(self)
    zones_settings(self)
    zones_ssl(self)
    zones_workers(self)

    # The API commands for /railguns/
    railguns(self)

    # The API commands for /organizations/
    organizations(self)
    organizations_audit_logs(self)
    organizations_virtual_dns(self)
    organizations_workers(self)

    # The API commands for /certificates/
    certificates(self)

    # The API commands for /ips/
    ips(self)

    # The API commands for /account/
    account(self)
    account_load_balancing_analytics(self)
    account_secondary_dns(self)

def user(self):
    """ API core commands for Cloudflare API"""

    self.add('AUTH', "user")
    self.add('VOID', "user/billing")
    self.add('AUTH', "user/billing/history")
    self.add('AUTH', "user/billing/profile")
    self.add('VOID', "user/billing/subscriptions")
    self.add('AUTH', "user/billing/subscriptions/apps")
    self.add('AUTH', "user/billing/subscriptions/zones")
    self.add('VOID', "user/firewall")
    self.add('VOID', "user/firewall/access_rules")
    self.add('AUTH', "user/firewall/access_rules/rules")
    self.add('AUTH', "user/invites")
    self.add('AUTH', "user/organizations")
    self.add('AUTH', "user/subscriptions")

def zones(self):
    """ API core commands for Cloudflare API"""

    self.add('AUTH', "zones")
    self.add('AUTH', "zones", "activation_check")
    self.add('AUTH', "zones", "available_plans")
    self.add('AUTH', "zones", "available_rate_plans")
    self.add('AUTH', "zones", "custom_certificates")
    self.add('AUTH', "zones", "custom_certificates/prioritize")
    self.add('AUTH', "zones", "custom_hostnames")
    self.add('AUTH', "zones", "custom_pages")
    self.add('AUTH', "zones", "dns_records")
    self.add('AUTH', "zones", "dns_records/export")
    self.add('AUTH', "zones", "dns_records/import")
    self.add('AUTH', "zones", "keyless_certificates")
    self.add('AUTH', "zones", "pagerules")
    self.add('AUTH', "zones", "purge_cache")
    self.add('AUTH', "zones", "railguns")
    self.add('AUTH', "zones", "railguns", "diagnose")
    self.add('AUTH', "zones", "secondary_dns")
    self.add('AUTH', "zones", "subscription")
    self.add('AUTH', "zones", "subscriptions")

def zones_spectrum(self):
     """ API core commands for Cloudflare API"""

     self.add('VOID', "zones", 'spectrum')
     self.add('AUTH', "zones", 'spectrum/apps')

def zones_settings(self):
    """ API core commands for Cloudflare API"""

    self.add('AUTH', "zones", "settings")
    self.add('AUTH', "zones", "settings/advanced_ddos")
    self.add('AUTH', "zones", "settings/always_online")
    self.add('AUTH', "zones", "settings/always_use_https")
    self.add('AUTH', "zones", "settings/browser_cache_ttl")
    self.add('AUTH', "zones", "settings/browser_check")
    self.add('AUTH', "zones", "settings/cache_level")
    self.add('AUTH', "zones", "settings/challenge_ttl")
    self.add('AUTH', "zones", "settings/development_mode")
    self.add('AUTH', "zones", "settings/email_obfuscation")
    self.add('AUTH', "zones", "settings/hotlink_protection")
    self.add('AUTH', "zones", "settings/ip_geolocation")
    self.add('AUTH', "zones", "settings/ipv6")
    self.add('AUTH', "zones", "settings/minify")
    self.add('AUTH', "zones", "settings/mirage")
    self.add('AUTH', "zones", "settings/mobile_redirect")
    self.add('AUTH', "zones", "settings/origin_error_page_pass_thru")
    self.add('AUTH', "zones", "settings/polish")
    self.add('AUTH', "zones", "settings/prefetch_preload")
    self.add('AUTH', "zones", "settings/response_buffering")
    self.add('AUTH', "zones", "settings/rocket_loader")
    self.add('AUTH', "zones", "settings/security_header")
    self.add('AUTH', "zones", "settings/security_level")
    self.add('AUTH', "zones", "settings/server_side_exclude")
    self.add('AUTH', "zones", "settings/sort_query_string_for_cache")
    self.add('AUTH', "zones", "settings/ssl")
    self.add('AUTH', "zones", "settings/tls_client_auth")
    self.add('AUTH', "zones", "settings/true_client_ip_header")
    self.add('AUTH', "zones", "settings/tls_1_2_only")
    self.add('AUTH', "zones", "settings/tls_1_3")
    self.add('AUTH', "zones", "settings/websockets")
    self.add('AUTH', "zones", "settings/waf")
    self.add('AUTH', "zones", "settings/webp")
    self.add('AUTH', "zones", "settings/http2")
    self.add('AUTH', "zones", "settings/pseudo_ipv4")
    self.add('AUTH', "zones", "settings/opportunistic_encryption")
    self.add('AUTH', "zones", "settings/automatic_https_rewrites")
    self.add('AUTH', "zones", "settings/brotli")
    self.add('AUTH', "zones", "settings/privacy_pass")

def zones_analytics(self):
    """ API core commands for Cloudflare API"""

    self.add('VOID', "zones", "analytics")
    self.add('AUTH', "zones", "analytics/colos")
    self.add('AUTH', "zones", "analytics/dashboard")

def zones_firewall(self):
    """ API core commands for Cloudflare API"""

    self.add('VOID', "zones", "firewall")
    self.add('VOID', "zones", "firewall/access_rules")
    self.add('AUTH', "zones", "firewall/access_rules/rules")
    self.add('AUTH', "zones", "firewall/lockdowns")
    self.add('AUTH', "zones", "firewall/ua_rules")
    self.add('VOID', "zones", "firewall/waf")
    self.add('AUTH', "zones", "firewall/waf/packages")
    self.add('AUTH', "zones", "firewall/waf/packages", "groups")
    self.add('AUTH', "zones", "firewall/waf/packages", "rules")

def zones_rate_limits(self):
    """ API core commands for Cloudflare API"""

    self.add('AUTH', "zones", "rate_limits")

def zones_dns_analytics(self):
    """ API core commands for Cloudflare API"""

    self.add('VOID', "zones", "dns_analytics")
    self.add('AUTH', "zones", "dns_analytics/report")
    self.add('AUTH', "zones", "dns_analytics/report/bytime")

def zones_amp(self):
    """ API core commands for Cloudflare API"""

    self.add('VOID', "zones", "amp")
    self.add('AUTH', "zones", "amp/viewer")

def zones_logs(self):
    """ API core commands for Cloudflare API"""

    self.add('VOID', "zones", "logs")
    self.add('AUTH_UNWRAPPED', "zones", "logs/received")
    self.add('AUTH_UNWRAPPED', "zones", "logs/received/fields")

def railguns(self):
    """ API core commands for Cloudflare API"""

    self.add('AUTH', "railguns")
    self.add('AUTH', "railguns", "zones")

def organizations(self):
    """ API core commands for Cloudflare API"""

    self.add('AUTH', "organizations")
    self.add('AUTH', "organizations", "members")
    self.add('AUTH', "organizations", "invite")
    self.add('AUTH', "organizations", "invites")
    self.add('AUTH', "organizations", "railguns")
    self.add('AUTH', "organizations", "railguns", "zones")
    self.add('AUTH', "organizations", "roles")
    self.add('VOID', "organizations", "firewall")
    self.add('VOID', "organizations", "firewall/access_rules")
    self.add('AUTH', "organizations", "firewall/access_rules/rules")
    self.add('VOID', "organizations", "load_balancers")
    self.add('AUTH', "organizations", "load_balancers/monitors")
    self.add('AUTH', "organizations", "load_balancers/pools")

def certificates(self):
    """ API core commands for Cloudflare API"""

    self.add('CERT', "certificates")

def ips(self):
    """ API core commands for Cloudflare API"""

    self.add('OPEN', "ips")

def zones_argo(self):
    """ API core commands for Cloudflare API"""

    self.add('VOID', "zones", "argo")
    self.add('AUTH', "zones", "argo/tiered_caching")
    self.add('AUTH', "zones", "argo/smart_routing")

def zones_dnssec(self):
    """ API core commands for Cloudflare API"""

    self.add('AUTH', "zones", "dnssec")

def zones_ssl(self):
    """ API core commands for Cloudflare API"""

    self.add('VOID', "zones", "ssl")
    self.add('AUTH', "zones", "ssl/analyze")
    self.add('AUTH', "zones", "ssl/certificate_packs")
    self.add('AUTH', "zones", "ssl/verification")
    self.add('VOID', "zones", "ssl/universal")
    self.add('AUTH', "zones", "ssl/universal/settings")

def zones_workers(self):
    """ API core commands for Cloudflare API"""

    self.add('VOID', "zones", "workers")
    self.add('AUTH', "zones", "workers/filters")
    self.add('AUTH', "zones", "workers/routes")
    self.add('AUTH', "zones", "workers/script")

def zones_load_balancers(self):
    """ API core commands for Cloudflare API"""

    self.add('AUTH', "zones", "load_balancers")

def user_load_balancers(self):
    """ API core commands for Cloudflare API"""

    self.add('VOID', "user/load_balancers")
    self.add('AUTH', "user/load_balancers/monitors")
    self.add('AUTH', "user/load_balancers/pools")

def user_virtual_dns(self):
    """ API core commands for Cloudflare API"""

    self.add('AUTH', "user/virtual_dns")
    self.add('VOID', "user/virtual_dns", "dns_analytics")
    self.add('AUTH', "user/virtual_dns", "dns_analytics/report")
    self.add('AUTH', "user/virtual_dns", "dns_analytics/report/bytime")
    return

def user_workers(self):
    """ API core commands for Cloudflare API"""

    self.add('VOID', "user/workers")
    self.add('AUTH', "user/workers/scripts")

def organizations_virtual_dns(self):
    """ API core commands for Cloudflare API"""

    self.add('AUTH', "organizations", "virtual_dns")
    self.add('VOID', "organizations", "virtual_dns", "dns_analytics")
    self.add('AUTH', "organizations", "virtual_dns", "dns_analytics/report")
    self.add('AUTH', "organizations", "virtual_dns", "dns_analytics/report/bytime")
    return

def user_audit_logs(self):
    """ API core commands for Cloudflare API"""

    self.add('AUTH', "user/audit_logs")

def user_load_balancing_analytics(self):
    """ API core commands for Cloudflare API"""

    self.add('VOID', "user", "load_balancing_analytics")
    self.add('AUTH', "user", "load_balancing_analytics/events")
    self.add('AUTH', "user", "load_balancing_analytics/entities")

def organizations_audit_logs(self):
    """ API core commands for Cloudflare API"""

    self.add('AUTH', "organizations", "audit_logs")

def organizations_workers(self):
    """ API core commands for Cloudflare API"""

    self.add('VOID', "organizations", "workers")
    self.add('AUTH', "organizations", "workers/scripts")

def account(self):
    """ API core commands for Cloudflare API"""

    self.add('VOID', "account")

def account_load_balancing_analytics(self):
    """ API core commands for Cloudflare API"""

    self.add('VOID', "account", "load_balancing_analytics")
    self.add('AUTH', "account", "load_balancing_analytics/events")
    self.add('AUTH', "account", "load_balancing_analytics/entities")

def account_secondary_dns(self):
    """ API core commands for Cloudflare API"""

    self.add('VOID', "account", "secondary_dns")
    self.add('AUTH', "account", "secondary_dns/masters")
    self.add('AUTH', "account", "secondary_dns/tsigs")

def zones_media(self):
    """ API core commands for Cloudflare API"""

    self.add('AUTH', "zones", "media")
    self.add('AUTH', "zones", "media", "embed")
    self.add('AUTH', "zones", "media", "preview")

