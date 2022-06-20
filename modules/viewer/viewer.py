import logging
import os.path

from flask import Blueprint, render_template

viewer_blueprint = Blueprint("viewer_blueprint", __name__, template_folder="templates", static_folder="static")

log = logging.getLogger(__name__)


@viewer_blueprint.route("/api/view/<index>/<filename>", methods=["GET"])
def view(index, filename):
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "uploads", index, filename)
    if not os.path.isfile(file_path):
        return render_template("error.html"), 404

    return render_template("view.html", file_path=f"uploads/{index}/{filename}", filename=filename), 200
