""" API core commands for Cloudflare API"""


def api_v4(self):
    """ API core commands for Cloudflare API"""

    # The API commands for /user/
    setattr(self, "user",
            self._add_with_auth(self._base, "user"))
    user = getattr(self, "user")
    setattr(user, "billing",
            self._add_unused(self._base, "user/billing"))
    user_billing = getattr(user, "billing")
    setattr(user_billing, "history",
            self._add_with_auth(self._base, "user/billing/history"))
    setattr(user_billing, "profile",
            self._add_with_auth(self._base, "user/billing/profile"))
    setattr(user_billing, "subscriptions",
            self._add_unused(self._base, "user/billing/subscriptions"))
    user_billing_subscriptions = getattr(user_billing, "subscriptions")
    setattr(user_billing_subscriptions, "apps",
            self._add_with_auth(self._base, "user/billing/subscriptions/apps"))
    setattr(user_billing_subscriptions, "zones",
            self._add_with_auth(self._base, "user/billing/subscriptions/zones"))
    setattr(user, "firewall",
            self._add_unused(self._base, "user/firewall"))
    user_firewall = getattr(user, "firewall")
    setattr(user_firewall, "access_rules",
            self._add_unused(self._base, "user/firewall/access_rules"))
    user_firewall_access_rules = getattr(user_firewall, "access_rules")
    setattr(user_firewall_access_rules, "rules",
            self._add_with_auth(self._base, "user/firewall/access_rules/rules"))
    setattr(user, "organizations",
            self._add_with_auth(self._base, "user/organizations"))
    setattr(user, "invites",
            self._add_with_auth(self._base, "user/invites"))
    setattr(user, "virtual_dns",
            self._add_with_auth(self._base, "user/virtual_dns"))

    # The API commands for /zones/
    setattr(self, "zones",
            self._add_with_auth(self._base, "zones"))
    zones = getattr(self, "zones")
    setattr(zones, "activation_check",
            self._add_with_auth(self._base, "zones", "activation_check"))
    setattr(zones, "available_plans",
            self._add_with_auth(self._base, "zones", "available_plans"))
    setattr(zones, "available_rate_plans",
            self._add_with_auth(self._base, "zones", "available_rate_plans"))
    setattr(zones, "custom_certificates",
            self._add_with_auth(self._base, "zones", "custom_certificates"))
    zones_custom_certificates = getattr(zones, "custom_certificates")
    setattr(zones_custom_certificates, "prioritize",
            self._add_with_auth(self._base, "zones",
                                "custom_certificates/prioritize"))
    setattr(zones, "custom_pages",
            self._add_with_auth(self._base, "zones", "custom_pages"))
    setattr(zones, "dns_records",
            self._add_with_auth(self._base, "zones", "dns_records"))
    setattr(zones, "keyless_certificates",
            self._add_with_auth(self._base, "zones", "keyless_certificates"))
    setattr(zones, "pagerules",
            self._add_with_auth(self._base, "zones", "pagerules"))
    setattr(zones, "purge_cache",
            self._add_with_auth(self._base, "zones", "purge_cache"))
    setattr(zones, "railguns",
            self._add_with_auth(self._base, "zones", "railguns"))
    zones_railguns = getattr(zones, "railguns")
    setattr(zones_railguns, "diagnose",
            self._add_with_auth(self._base, "zones", "railguns", "diagnose"))
    setattr(zones, "settings",
            self._add_with_auth(self._base, "zones", "settings"))
    zones_settings = getattr(zones, "settings")
    setattr(zones_settings, "advanced_ddos",
            self._add_with_auth(self._base, "zones", "settings/advanced_ddos"))
    setattr(zones_settings, "always_online",
            self._add_with_auth(self._base, "zones", "settings/always_online"))
    setattr(zones_settings, "browser_cache_ttl",
            self._add_with_auth(self._base, "zones",
                                "settings/browser_cache_ttl"))
    setattr(zones_settings, "browser_check",
            self._add_with_auth(self._base, "zones", "settings/browser_check"))
    setattr(zones_settings, "cache_level",
            self._add_with_auth(self._base, "zones", "settings/cache_level"))
    setattr(zones_settings, "challenge_ttl",
            self._add_with_auth(self._base, "zones", "settings/challenge_ttl"))
    setattr(zones_settings, "development_mode",
            self._add_with_auth(self._base, "zones",
                                "settings/development_mode"))
    setattr(zones_settings, "email_obfuscation",
            self._add_with_auth(self._base, "zones",
                                "settings/email_obfuscation"))
    setattr(zones_settings, "hotlink_protection",
            self._add_with_auth(self._base, "zones",
                                "settings/hotlink_protection"))
    setattr(zones_settings, "ip_geolocation",
            self._add_with_auth(self._base, "zones", "settings/ip_geolocation"))
    setattr(zones_settings, "ipv6",
            self._add_with_auth(self._base, "zones", "settings/ipv6"))
    setattr(zones_settings, "minify",
            self._add_with_auth(self._base, "zones", "settings/minify"))
    setattr(zones_settings, "mirage",
            self._add_with_auth(self._base, "zones", "settings/mirage"))
    setattr(zones_settings, "mobile_redirect",
            self._add_with_auth(self._base, "zones",
                                "settings/mobile_redirect"))
    setattr(zones_settings, "origin_error_page_pass_thru",
            self._add_with_auth(self._base, "zones",
                                "settings/origin_error_page_pass_thru"))
    setattr(zones_settings, "polish",
            self._add_with_auth(self._base, "zones", "settings/polish"))
    setattr(zones_settings, "prefetch_preload",
            self._add_with_auth(self._base, "zones",
                                "settings/prefetch_preload"))
    setattr(zones_settings, "response_buffering",
            self._add_with_auth(self._base, "zones",
                                "settings/response_buffering"))
    setattr(zones_settings, "rocket_loader",
            self._add_with_auth(self._base, "zones", "settings/rocket_loader"))
    setattr(zones_settings, "security_header",
            self._add_with_auth(self._base, "zones",
                                "settings/security_header"))
    setattr(zones_settings, "security_level",
            self._add_with_auth(self._base, "zones", "settings/security_level"))
    setattr(zones_settings, "server_side_exclude",
            self._add_with_auth(self._base, "zones",
                                "settings/server_side_exclude"))
    setattr(zones_settings, "sort_query_string_for_cache",
            self._add_with_auth(self._base, "zones",
                                "settings/sort_query_string_for_cache"))
    setattr(zones_settings, "ssl",
            self._add_with_auth(self._base, "zones", "settings/ssl"))
    setattr(zones_settings, "tls_client_auth",
            self._add_with_auth(self._base, "zones",
                                "settings/tls_client_auth"))
    setattr(zones_settings, "true_client_ip_header",
            self._add_with_auth(self._base, "zones",
                                "settings/true_client_ip_header"))
    setattr(zones_settings, "tls_1_2_only",
            self._add_with_auth(self._base, "zones", "settings/tls_1_2_only"))
    setattr(zones_settings, "tls_1_3",
            self._add_with_auth(self._base, "zones", "settings/tls_1_3"))
    # setattr(zones_settings, "tlsadd_auth",
    #         self._add_with_auth(self._base, "zones", "settings/tlsadd_auth"))
    # setattr(zones_settings, "trueadd_ip_header",
    #         self._add_with_auth(self._base, "zones", "settings/trueadd_ip_header"))
    setattr(zones_settings, "websockets",
            self._add_with_auth(self._base, "zones", "settings/websockets"))
    setattr(zones_settings, "waf",
            self._add_with_auth(self._base, "zones", "settings/waf"))
    setattr(zones, "analytics",
            self._add_unused(self._base, "zones", "analytics"))
    zones_analytics = getattr(zones, "analytics")
    setattr(zones_analytics, "colos",
            self._add_with_auth(self._base, "zones", "analytics/colos"))
    setattr(zones_analytics, "dashboard",
            self._add_with_auth(self._base, "zones", "analytics/dashboard"))
    setattr(zones, "firewall",
            self._add_unused(self._base, "zones", "firewall"))
    zones_firewall = getattr(zones, "firewall")
    setattr(zones_firewall, "access_rules",
            self._add_unused(self._base, "zones", "firewall/access_rules"))
    setattr(zones_firewall, "waf",
            self._add_unused(self._base, "zones", "firewall/waf"))
    zones_firewall_waf = getattr(zones_firewall, "waf")
    setattr(zones_firewall_waf, "packages",
            self._add_with_auth(self._base, "zones", "firewall/waf/packages"))
    zones_firewall_waf_packages = getattr(zones_firewall_waf, "packages")
    setattr(zones_firewall_waf_packages, "groups",
            self._add_with_auth(self._base, "zones", "firewall/waf/packages",
                                "groups"))
    setattr(zones_firewall_waf_packages, "rules",
            self._add_with_auth(self._base, "zones", "firewall/waf/packages",
                                "rules"))
    zones_firewall_access_rules = getattr(zones_firewall, "access_rules")
    setattr(zones_firewall_access_rules, "rules",
            self._add_with_auth(self._base, "zones",
                                "firewall/access_rules/rules"))

    # The API commands for /railguns/
    setattr(self, "railguns",
            self._add_with_auth(self._base, "railguns"))
    railguns = getattr(self, "railguns")
    setattr(railguns, "zones",
            self._add_with_auth(self._base, "railguns", "zones"))

    # The API commands for /organizations/
    setattr(self, "organizations",
            self._add_with_auth(self._base, "organizations"))
    organizations = getattr(self, "organizations")
    setattr(organizations, "members",
            self._add_with_auth(self._base, "organizations", "members"))
    setattr(organizations, "invite",
            self._add_with_auth(self._base, "organizations", "invite"))
    setattr(organizations, "invites",
            self._add_with_auth(self._base, "organizations", "invites"))
    setattr(organizations, "railguns",
            self._add_with_auth(self._base, "organizations", "railguns"))
    organizations_railguns = getattr(organizations, "railguns")
    setattr(organizations_railguns, "zones",
            self._add_with_auth(self._base, "organizations", "railguns",
                                "zones"))
    setattr(organizations, "roles",
            self._add_with_auth(self._base, "organizations", "roles"))
    setattr(organizations, "firewall",
            self._add_unused(self._base, "organizations", "firewall"))
    organizations_firewall = getattr(organizations, "firewall")
    setattr(organizations_firewall, "access_rules",
            self._add_unused(self._base, "organizations",
                             "firewall/access_rules"))
    organizations_firewall_access_rules = getattr(organizations_firewall,
                                                  "access_rules")
    setattr(organizations_firewall_access_rules, "rules",
            self._add_with_auth(self._base, "organizations",
                                "firewall/access_rules/rules"))
    setattr(organizations, "virtual_dns",
            self._add_with_auth(self._base, "organizations", "virtual_dns"))

    # The API commands for /certificates/
    setattr(self, "certificates",
            self._add_with_cert_auth(self._base, "certificates"))

    # The API commands for /ips/
    setattr(self, "ips",
            self._add_noauth(self._base, "ips"))

    # The API commands for /zones/:zone_id/dnssec
    setattr(zones, "dnssec",
            self._add_with_auth(self._base, "zones", "dnssec"))

    # The API commands for /zones/:zone_id/ssl
    setattr(zones, "ssl",
            self._add_unused(self._base, "zones", "ssl"))
    zones_ssl = getattr(zones, "ssl")
    setattr(zones_ssl, "analyze",
            self._add_with_auth(self._base, "zones", "ssl/analyze"))
    setattr(zones_ssl, "certificate_packs",
            self._add_with_auth(self._base, "zones", "ssl/certificate_packs"))
    setattr(zones_ssl, "verification",
            self._add_with_auth(self._base, "zones", "ssl/verification"))

    # The API commands for CTM /zones/:zone_id/load_balancers & /user/load_balancers
    setattr(zones, "load_balancers",
            self._add_with_auth(self._base, "zones", "load_balancers"))

    setattr(user, "load_balancers",
            self._add_unused(self._base, "user/load_balancers"))
    user_load_balancers = getattr(user, "load_balancers")
    setattr(user_load_balancers, "global_policies",
            self._add_with_auth(self._base,
                                "user/load_balancers/global_policies"))
    setattr(user_load_balancers, "monitors",
            self._add_with_auth(self._base, "user/load_balancers/monitors"))
    setattr(user_load_balancers, "notifiers",
            self._add_with_auth(self._base, "user/load_balancers/notifiers"))
    setattr(user_load_balancers, "origins",
            self._add_with_auth(self._base, "user/load_balancers/origins"))
    setattr(user_load_balancers, "pools",
            self._add_with_auth(self._base, "user/load_balancers/pools"))
    setattr(user_load_balancers, "maps",
            self._add_with_auth(self._base, "user/load_balancers/maps"))
