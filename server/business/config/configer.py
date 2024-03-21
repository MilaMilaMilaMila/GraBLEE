import configparser

values = configparser.ConfigParser()

# connection_params - host and port which server will listen
# set your own connection params or use existing
# this params will be written in values.ini
config_values = {
    "WINDOWS": {
        "port": 5000,
        "host": "127.0.0.1",
        "listeners_amount": 2,
        "key": "some_key_12345678",
    },
    "MAC": {
        "port": 8080,
        "host": "127.0.0.1",
        "listeners_amount": 2,
        "key": "some_key_12345678",
    },
    "REMOTE": {
        "port": 21,
        "host": "84.38.181.98",
        "listeners_amount": 2,
        "key": "some_key_12345678",
    },
}

for section in config_values:
    values.add_section(section)
    params = config_values[section]
    for param in params:
        values.set(section, param, str(params[param]))

with open('config/values.ini', 'w') as configfile:
    values.write(configfile)

config = configparser.ConfigParser()

# get values from values.ini and write manually in config_.ini
configuration = {
    "port": "{PORT}",
    "host": "{HOST}",
    "listeners_amount": "{LISTENERS_AMOUNT}",
    "key": "{KEY}",
}

section = "CONNECTION_PARAMS"
config.add_section(section)
for param in configuration:
    config.set(section, param, configuration[param])

with open('config/config_.ini', 'w') as configfile:
    config.write(configfile)