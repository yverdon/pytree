# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join

import yaml
from flask_cors import CORS
from yaml import FullLoader

from pytree import app

# %%
pytree_config_file = join(dirname(abspath(__file__)), "pytree.yml")
with open(pytree_config_file, "r") as f:
    pytree_config = yaml.load(f, Loader=FullLoader)
# %%
if __name__ == "__main__":
    DEBUG = pytree_config["vars"]["debug"]
    if DEBUG:
        CORS(app)
        app.run(debug=True, host="0.0.0.0", port=5000)
    else:
        app.run()
