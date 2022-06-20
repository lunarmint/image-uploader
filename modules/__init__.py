import logging

from flask import Flask

from modules.uploader.uploader import uploader_blueprint
from modules.viewer.viewer import viewer_blueprint

log = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    app.register_blueprint(uploader_blueprint)
    app.register_blueprint(viewer_blueprint)
    return app
