from ki import ki
from flask import render_template


@ki.route("/")
def index():
    return render_template("/general/index.html")


@ki.route("/about")
def about():
    return render_template("/general/about.html")


@ki.route("/contact")
def contact():
    return render_template("/general/contact.html")


@ki.route("/glossar/baumbeet")
def glossar_baumbeet():
    return render_template("/general/baumbeete.html")


@ki.route("/map")
def map():
    return render_template("/general/map.html")