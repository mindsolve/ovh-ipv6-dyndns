# -*- encoding: utf-8 -*-
"""
First, install the latest release of Python wrapper: $ pip install ovh
"""
import json
import ovh

# Instanciate an OVH Client.
# You can generate new credentials with full access to your account on
# the token creation page (https://eu.api.ovh.com/createToken/)
client = ovh.Client(
    endpoint='ovh-eu',  # Endpoint of API OVH Europe (List of available endpoints)
    application_key='aaaaaa',  # Application Key
    application_secret='aaaaaaaaaaaaa',  # Application Secret
    consumer_key='aaaaaaaaaaaaaaaaaaaaa',  # Consumer Key
)

result = client.put('/domain/zone/example.com/record/111111',
                    subDomain='home6',  # Resource record subdomain (type: string)
                    target='2a02::1',  # Resource record target (type: string)
                    )

# Pretty print
print(json.dumps(result, indent=4))
