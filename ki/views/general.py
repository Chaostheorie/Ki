from ki import ki
from flask import render_template


@ki.route("/")
def index():
    return render_template("/general/index.html")
