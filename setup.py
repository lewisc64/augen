from distutils.core import setup

config = {
    "name": "augen",
    "packages": ["augen", "augen.music", "augen.dtmf"],
}

setup(**config)
