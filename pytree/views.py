# -*- coding: utf-8 -*-

# %%
import subprocess
from os.path import abspath, dirname

import yaml
from flask import jsonify, render_template, request
from flask_cors import cross_origin
from yaml import FullLoader

from pytree import app

# %%

yaml_config_file = dirname(abspath(__file__)) + ".yml"
with open(yaml_config_file, "r") as f:
    pytree_config = yaml.load(f, Loader=FullLoader)


@app.context_processor
def yaml_config_vars():
    return dict(yaml_config_vars=get_yaml_config_vars())


# %%


def get_yaml_config_vars():
    return pytree_config


# %%


@app.route("/")
def home(name=None):
    return render_template("home.html", name=name)


# %%


@app.route("/profile/get")
@cross_origin()
def get_profile():
    """Docstring"""
    cpotree = pytree_config["vars"]["cpotree_executable"]
    point_clouds = pytree_config["vars"]["pointclouds"]
    polyline = request.args["coordinates"]
    if polyline == "":
        return "Empty coordinates"

    maxLevel = request.args["maxLOD"]
    minLevel = request.args["minLOD"]
    width = request.args["width"]
    point_cloud = request.args["pointCloud"]
    potree_file = point_clouds[point_cloud]
    attributes = [request.args["attributes"]]
    p = subprocess.Popen(
        [cpotree, potree_file, "--stdout"]
        + attributes
        + [
            "-o",
            "stdout",
            "--coordinates",
            polyline,
            "--width",
            width,
            "--min-level",
            minLevel,
            "--max-level",
            maxLevel,
        ],
        bufsize=-1,
        stdout=subprocess.PIPE,
    )

    [out, err] = p.communicate()

    return out


# %%


@app.route("/profile/config")
@cross_origin()
def profile_config_gmf2():

    vars = pytree_config["vars"].copy()

    if "cpotree_executable" in vars:
        vars.pop("cpotree_executable")

    if "pointclouds" in vars:
        vars.pop("pointclouds")

    if "log_folder" in vars:
        vars.pop("log_folder")

    return jsonify(vars)


# %%


class PointAttribute:
    def __init__(s, name, elements, bytes):
        s.name = name
        s.elements = elements
        s.bytes = bytes


# %%


class PointAttributes:

    POSITION_CARTESIAN = PointAttribute("POSITION_CARTESIAN", 3, 12)
    POSITION_PROJECTED_PROFILE = PointAttribute("POSITION_PROJECTED_PROFILE", 2, 8)
    COLOR_PACKED = PointAttribute("COLOR_PACKED", 4, 4)
    RGB = PointAttribute("RGB", 3, 3)
    RGBA = PointAttribute("RGBA", 4, 4)
    INTENSITY = PointAttribute("INTENSITY", 1, 2)
    CLASSIFICATION = PointAttribute("CLASSIFICATION", 1, 1)

    def __init__(s):
        s.attributes = []
        s.bytes = 0

    def add(s, attribute):
        s.attributes.append(attribute)
        s.bytes = s.bytes + attribute.bytes * attribute.elements

    @staticmethod
    def fromName(name):
        return getattr(PointAttributes, name)


# %%
