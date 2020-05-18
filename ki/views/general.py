from ki import ki, db
from ki.models import Trees, PLZ
from flask import render_template, request, abort
from datetime import date


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


@ki.route("/map", methods=["GET", "POST"])
def map():
    if request.method == "GET":
        plz = request.args.get("plz", default=None, type=int)
        if len(str(plz)) != 5 and float(plz).is_integer() is False \
           or plz is None:
            return abort(400)
        else:
            regions = PLZ.query.filter(PLZ.plz.between(plz-2, plz+2)).all()
            y, x = 0, 0
            for region in regions:
                if region.coords[0] > x:
                    x = region.coords[0]
                if region.coords[1] > y:
                    y = region.coords[1]
            q = Trees.query
            q = q.filter(Trees.x < x)
            q = q.filter_by(Trees.y < y)
            trees = q.all()
            return render_template("/general/map.html", plz=plz, trees=trees)
    elif request.method == "POST":
        if "tree-id" not in request.form.keys():
            pass
        else:
            id = request.form["tree-id"]
        tree = Trees.query.get_or_404(id)
        tree.reserved = True
        tree.reserved_at = date.today()
        db.session.commit()
