# -*- encoding: utf-8 -*-
"""
First, install the latest release of Python wrapper: $ pip install ovh
"""
import ovh
import requests

import config
import ovh_api


def main():
    # Load config from config file

    # Instanciate an OVH Client.
    # You can generate new credentials with full access to your account on
    # the token creation page (https://eu.api.ovh.com/createToken/)
    client = ovh.Client(
        endpoint=config.get_setting('ovh_api_endpoint'),  # Endpoint of API OVH Europe (List of available endpoints)
        application_key=config.get_setting('ovh_application_key'),  # Application Key
        application_secret=config.get_setting('ovh_application_secret'),  # Application Secret
        consumer_key=config.get_setting('ovh_consumer_key'),  # Consumer Key
    )

    # Get IP-address(-es), one per requested record type
    # for each record type:
    #   - Get record ID to change
    #   if no record ID:
    #     - create new record with IP
    #   else:
    #     - change record to point to new IP, if record IP != IP

    for record_type in config.get_setting('ovh_dns_types').split(","):
        zone_name = config.get_setting('ovh_dns_zone')
        subdomain = config.get_setting('ovh_dns_subdomain')

        if record_type.casefold() == "A".casefold():
            ip_addr = requests.get("http://ipv4.icanhazip.com/").text
        else:
            ip_addr = requests.get("http://ipv6.icanhazip.com/").text

        record_id = ovh_api.ovhapi_get_recordid(client, zone_name, subdomain, record_type)
        if record_id == -1:
            ovh_api.ovhapi_create_record(client, zone_name, subdomain, record_type, ip_addr)
        else:
            current_record_ip = ovh_api.ovhapi_get_record(client, zone_name, record_id)["target"]
            if current_record_ip != ip_addr:
                ovh_api.ovhapi_modify_record(client, zone_name, record_id, ip_addr)


if __name__ == '__main__':
    main()
