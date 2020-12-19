# This is the configuration loader for the request_ip_block script

# The priority is as follows:
# - Environment variables
# - Configuration file (config.ini)
# - Console input

import os
import configparser
import shutil

from typing import Optional

settings = {}
prompts = {'ovh_application_key': "The OVH-API Application Key",
           'ovh_application_secret': "The OVH-API Application Secret",
           'ovh_consumer_key': "The OVH-API Consumer Key",
           'ovh_domains': "The FQDN to update",
           'ovh_dns_types': "The DNS entry types to update, comma-separated (A, AAAA)"}


def get_scriptdir() -> str:
    """
Simply returns the directory where the script/program resides in.
*Even if packaged via pyinstaller*
    :return: Full filepath to script base dir
    """
    import os
    import sys
    if getattr(sys, "frozen", False):
        # noinspection PyUnresolvedReferences
        scriptdir = sys._MEIPASS  # type: str
    else:
        scriptdir = os.path.dirname(os.path.realpath(__file__))

    return scriptdir


# Check if config file exists, but only on first load
if not os.path.isfile(os.path.join(get_scriptdir(), "config.ini")):
    print("Hint: The configuration file is missing!")
    try:
        shutil.copyfile(os.path.join(get_scriptdir(), "config.example.ini"),
                        os.path.join(get_scriptdir(), "config.ini"))
        print("-> The default configuration has been written to config.ini.")
        print("-> Please change config.ini accordingly.")
    except (IOError, shutil.SameFileError):
        print("[WARN] Copying failed. Continuing without.")


def __get_conffile_setting(setting_name: str) -> Optional[str]:
    """
Private method for getting a setting from the configuration file
    :param setting_name: Name of the setting to search
    :return: Setting value from config file, if any. Returns `None` if not defined
    """
    config_ini = None
    # Load general settings
    ini_location = os.path.join(get_scriptdir(), "config.ini")
    if os.path.isfile(ini_location):
        config_ini = configparser.ConfigParser()
        config_ini.read(ini_location)

    if config_ini is None:
        return None
    section_title = setting_name.split('_')[0].upper()
    if not config_ini.has_section(section_title):
        return None
    if not config_ini.has_option(section_title, setting_name):
        return None
    return config_ini.get(section_title, setting_name, fallback=None)


def __get_prompt_setting(setting_name: str, prompt_msg: Optional[str] = None, secret_input: bool = None) -> str:
    """
Private method for requesting a setting/config option by user input
    :param setting_name: Name of the setting to ask for
    :param prompt_msg: Optional prompt message
    :return: The user-entered string, cannot be "" or None
    """
    while True:
        # Check whether there is a custom prompt for the setting
        if prompt_msg is not None:
            this_prompt = prompt_msg
        elif prompts.get(setting_name) is not None:
            this_prompt = prompts[setting_name]
        else:
            this_prompt = setting_name

        if secret_input is True:
            import getpass
            input_str = getpass.getpass("{}: ".format(this_prompt))
        else:
            input_str = input("{}: ".format(this_prompt))

        if input_str is not None and input_str != "":
            return input_str
        else:
            print("-> Error! Invalid Input, please try again.")


def get_setting(setting_name: str, prompt_msg: str = None, do_prompt: Optional[bool] = True, default: str = None,
                force_prompt: bool = False, **kwargs):
    """
**Method for retrieving a configuration option/setting.**

This method searches an option in the following order:

#. "settings"-dict
    This caches the basic variables
#. Environment variables (uppercase).
    E.g.: setting "tufin_username" -> env variable "TUFIN_USERNAME"
#. Configuration file
    E.g. setting "tufin_username" -> Section "[TUFIN]", option "tufin_username" (for ini file)
#. User prompt (if `do_prompt` is True)
    Asks the user interactively for an answer, optionally with a custom prompt message. (prompt_msg)

    :param setting_name: The configuration option
    :param prompt_msg: An optional user prompt, if user has to interact. Ignored if do_prompt is False
    :param do_prompt: Whether or not to ask the user, if the setting is not defined via ENV or config file
    :param force_prompt: Whether to ignore all other sources and only prompt the user (implies do_prompt=True)
    :param default: A default return value. Only returned if setting not defined and `do_prompt` is False
    :return: The configuration value. Param 'default' if 'do_prompt' is false, otherwise always str.
    """

    if kwargs.get("secret_input") is None:
        if "password" in setting_name or "secret" in setting_name:
            kwargs["secret_input"] = True
        else:
            kwargs["secret_input"] = False

    if not force_prompt:
        if settings.get(setting_name) is not None:
            return settings[setting_name]

        env_setting = os.getenv(setting_name.upper())
        if env_setting is not None:
            return env_setting

        conffile_setting = __get_conffile_setting(setting_name)
        if conffile_setting is not None:
            return conffile_setting

        if not do_prompt:
            return default

    prompt_setting = __get_prompt_setting(setting_name, prompt_msg=prompt_msg, secret_input=kwargs.get("secret_input"))
    if prompt_setting is not None:
        return prompt_setting

    print("[ERROR] Failure while trying to read setting \"{}\". This is a bug.".format(setting_name))
    exit(1)


def set_setting(setting_name: str, setting_value: str) -> None:
    """
    Small helper function for setting a setting to a value

    :param setting_name: The setting to set
    :param setting_value: The str value to set the setting to
    :return: Nothing
    """
    settings[setting_name] = str(setting_value)


def reset_setting(setting_name: str):
    """
    Simple method for removing a setting
    :param setting_name:
    :return:
    """
    try:
        settings[setting_name] = None
    except KeyError:
        pass


def populate_settings_dict():
    # Populate settings dict
    for setting in settings:
        if settings[setting] is not None:
            continue

        if "password" in setting or "secret" in setting or "_key" in setting:
            secret_input = True
        else:
            secret_input = False

        settings[setting] = get_setting(setting, secret_input=secret_input)


populate_settings_dict()
