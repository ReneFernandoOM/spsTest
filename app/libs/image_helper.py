import re
from typing import Dict

import boto3
from flask import current_app
from flask_restful import abort
from werkzeug.datastructures import FileStorage


def upload_image_to_s3(image: FileStorage, pet_id: int) -> str:
    """
    Guarda la imagen en un s3 bucket.
    """
    if not is_extension_allowed(image):
        return False
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(current_app.config["BUCKET"])
    s3_filepath = f"{pet_id}/{image.filename}"
    bucket.Object(s3_filepath).put(Body=image.read())

    return s3_filepath


def get_image_from_s3(s3_key: str) -> Dict:
    s3 = boto3.client("s3")
    file = s3.get_object(Bucket=current_app.config["BUCKET"], Key=s3_key)

    return file


def delete_image_from_s3(s3_key: str) -> None:
    s3 = boto3.resource("s3")
    s3.Object(current_app.config["BUCKET"], s3_key).delete()


def is_extension_allowed(file: FileStorage) -> bool:
    """
    Comprueba que la extensión sea jpg, png o jpeg
    """
    filename = file.filename

    regex = f"^.*\.(jpg|png|jpeg)$"
    return re.match(regex, filename) is not None
