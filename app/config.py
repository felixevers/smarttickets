import os
from typing import Union, Tuple

to_load: Union[str, Tuple[str, any]] = [
    # flask settings
    ("CROSS_ORIGIN", True),
    ("DEBUG", True),
    ("FLASK_DEBUG", True),
    ("FLASK_ENV", "development"),

    # sqlalchemy
    ("MYSQL_HOSTNAME", "localhost"),
    ("MYSQL_PORT", 3306),
    ("MYSQL_DATABASE", "smarttickets"),
    ("MYSQL_USERNAME", "smarttickets"),
    ("MYSQL_PASSWORD", "smarttickets"),
    ("SQLALCHEMY_TRACK_MODIFICATIONS", False),

    # flask-restplus
    ("SWAGGER_UI_JSONEDITOR", True),
    ("RESTPLUS_MASK_SWAGGER", False),

    # flask-mail
    ("MAIL_ENABLED", False),
    ("MAIL_SERVER", "localhost"),
    ("MAIL_PORT", 25),
    ("MAIL_USE_TLS", False),
    ("MAIL_USE_SSL", False),
    ("MAIL_USERNAME", "smarttickets"),
    ("MAIL_PASSWORD", "smarttickets"),
    ("MAIL_DEFAULT_SENDER", "smarttickets"),

    # frontend rendering
    ("FRONTEND", "./frontend/dist/frontend"),

    # timezone
    ("TIMEZONE", "Europe/Berlin"),
]

# the final configuration dict
config: dict = {}

# load all configuration values from the env
for key in to_load:
    if isinstance(key, tuple):
        if key[0] in os.environ:
            config[key[0]] = os.environ.get(key[0])
        else:
            config[key[0]] = key[1]
    elif key in os.environ:
        config[key] = os.environ.get(key)

# set sqlalchemy database connection uri
config["SQLALCHEMY_DATABASE_URI"]: str = \
    f"mysql+pymysql://{config['MYSQL_USERNAME']}:{config['MYSQL_PASSWORD']}@" \
    f"{config['MYSQL_HOSTNAME']}:{config['MYSQL_PORT']}/{config['MYSQL_DATABASE']}"
