from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

main_page = Blueprint(
    "index_page", __name__, template_folder="templates", static_folder="static"
)


@main_page.route("/", defaults={"page": "index"})
@main_page.route("/<page>")
def show(page):
    try:
        # return "MAIN PAGE TEST"
        return render_template("%s.html" % page)
    except TemplateNotFound:
        abort(404)
