import datetime
import logging
import os
import random
import string

import PIL
import magic
from PIL import Image
from flask import request, Blueprint, jsonify
from pillow_heif import register_heif_opener
from werkzeug.utils import secure_filename

from utils.config import config

uploader_blueprint = Blueprint("uploader_blueprint", __name__)

log = logging.getLogger(__name__)


@uploader_blueprint.route("/api/upload", methods=["POST"])
def upload():
    if not request.files:
        return "No file part.", 400

    file = request.files["file"]

    try:
        register_heif_opener()
        image = Image.open(file)
        filename = generate_filename(filename=file.filename, extension="webp")
        file_path = create_directory(filename)
        image_without_exif = strip_exif(image)
        image_without_exif.save(
            fp=file_path,
            format="webp",
            lossless=config["webp"]["lossless"],
            quality=config["webp"]["quality"],
            method=config["webp"]["method"],
        )
    except PIL.UnidentifiedImageError:
        mime_type = get_mime_type(file)
        if not is_mime_allowed(mime_type):
            return "Unsupported media type.", 415

        filename = generate_filename(file.filename)
        file_path = create_directory(filename)
        file.save(file_path)

    index = file_path.rsplit("\\", 2)[1]
    response = {"url": f"{request.host_url}api/view/{index}/{filename}"}
    return jsonify(response), 200


def get_mime_type(file) -> str:
    file.seek(0)
    mime_type = magic.from_buffer(file.read(2048), mime=True)
    return mime_type


def is_mime_allowed(mime_type: str) -> bool:
    return mime_type.split("/", 1)[0] in config["mime_type"]["whitelisted"]


def create_directory(filename: str) -> str:
    current_utc = datetime.datetime.utcnow().strftime("%Y%m%d")
    upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "uploads", current_utc)
    if not os.path.exists(upload_dir):
        os.mkdir(upload_dir)

    return os.path.join(upload_dir, filename)


def strip_exif(image: Image) -> Image:
    data = list(image.getdata())
    image_without_exif = Image.new(mode=image.mode, size=image.size)
    image_without_exif.putdata(data)
    return image_without_exif


def generate_filename(filename: str, extension: str = None) -> str:
    if not extension:
        extension = filename.rsplit(".", 1)[1]

    if config["random_name"] > 0 or filename == "":
        random_string = "".join(
            random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(config["random_name"])
        )
        return f"{random_string}.{extension}"

    return f"{secure_filename(filename).rsplit('.', 1)[0]}.{extension}"
