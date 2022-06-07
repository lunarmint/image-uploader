import os

from modules import create_app
from utils.config import config

app = create_app()

if __name__ == "__main__":
    img_dir = os.path.join(os.getcwd(), "img")
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)

    app.run(threaded=True, host=config["host"], port=config["port"], debug=True)
