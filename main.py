import os

from modules import create_app
from utils.config import config

app = create_app()

if __name__ == "__main__":
    upload_dir = os.path.join(os.path.dirname(__file__), "modules", "static", "uploads")
    if not os.path.exists(upload_dir):
        os.mkdir(upload_dir)

    app.run(threaded=True, host=config["host"], port=config["port"], debug=True)
