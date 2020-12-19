import ovh


def ovhapi_get_recordid(ovh_client: ovh.Client, zone_name: str, subdomain: str, record_type: str):
    """
Simple wrapper function for getting the record IDs for a given zone, subdomain and record type.
Prints a warning if more than one record matches.

    :param ovh_client: A valid OVH-API-Client object
    :param zone_name: The OVH zone name
    :param subdomain: The subdomain to find
    :param record_type: The record type to find
    :return: The first record id
    """
    record_ids: list = ovh_client.get('/domain/zone/' + zone_name + '/record',
                                      fieldType=record_type,
                                      subDomain=subdomain)

    if len(record_ids) > 1:
        print("WARNING: More than one record matched! Returning only the first.", record_ids)
    elif len(record_ids) == 0:
        print("WARNING: No records found!")
        return -1

    return record_ids[0]


def ovhapi_refresh_zone(ovh_client: ovh.Client, zone_name: str):
    """
Simple wrapper for refreshing a DNS zone

    :param ovh_client: A valid OVH-API-Client object
    :param zone_name: The OVH zone name
    """
    ovh_client.post('/domain/zone/' + zone_name + '/refresh')


def ovhapi_create_record(ovh_client: ovh.Client, zone_name: str, subdomain: str, record_type: str, record_target: str):
    """
Simple wrapper function for creating a record with a given zone, subdomain, record type and target.
After creation it refreshes the zone.

    :param ovh_client: A valid OVH-API-Client object
    :param zone_name: The OVH zone name
    :param subdomain: The subdomain to create a record for
    :param record_type: The record type to create
    :param record_target: The record target (the IP address)
    :return: The ID of the newly created record
    """
    answer = ovh_client.post('/domain/zone/' + zone_name + '/record',
                             fieldType=record_type,
                             subDomain=subdomain,
                             target=record_target)

    if not answer["id"]:
        print(answer)
        raise Exception("Unknown error, no record id returned!")

    print("The {}-record {} was created for {}".format(
        answer['fieldType'], answer['id'], answer['zone'] + '.' + answer['subDomain']))

    # Refresh zone (apply changes)
    ovhapi_refresh_zone(ovh_client, zone_name)

    return answer["id"]


def ovhapi_modify_record(ovh_client: ovh.Client, zone_name: str, record_id: int, record_target: str):
    """
Simple wrapper function for modifying a record with a given zone, subdomain, record type and target.
After modification it refreshes the zone.

    :param ovh_client: A valid OVH-API-Client object
    :param zone_name: The OVH zone name
    :param record_id: The record ID to modify. Call ovhapi_get_recordid() to get this ID.
    :param record_target: The record target (the IP address)
    """
    ovh_client.put('/domain/zone/' + zone_name + '/record/' + str(record_id),
                   target=record_target)

    # Refresh zone (apply changes)
    ovhapi_refresh_zone(ovh_client, zone_name)


def ovhapi_get_record(ovh_client: ovh.Client, zone_name: str, record_id: int):
    """
Simple wrapper function for getting a record with a given zone and record id.

    :param ovh_client: A valid OVH-API-Client object
    :param zone_name: The OVH zone name
    :param record_id: The record ID to modify. Call ovhapi_get_recordid() to get this ID.
    """
    answer = ovh_client.get('/domain/zone/' + zone_name + '/record/' + str(record_id))

    return answer
