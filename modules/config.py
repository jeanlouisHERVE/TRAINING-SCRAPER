#!/usr/bin/python
import configparser
from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def get_database_name(config_file="database.ini"):
    config = configparser.ConfigParser()
    config.read(config_file)

    if "postgresql" in config:
        db_config = config["postgresql"]
        db_name = db_config.get("database")
        return db_name
    else:
        raise ValueError("No 'postgresql' section found in the configuration file.")


def get_superuser_informations(config_file="database.ini"):
    config = configparser.ConfigParser()
    config.read(config_file)

    if "postgresql" in config:
        db_config = config["postgresql"]
        user_name = db_config.get("user")
        user_password = db_config.get("password")
        return user_name, user_password
    else:
        raise ValueError("No 'postgresql' section found in the configuration file.")
