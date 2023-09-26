import os
import secrets
from fastapi import HTTPException, status
from uuid import uuid4
from PIL import Image
from fastapi import File, UploadFile

from fastapi.staticfiles import StaticFiles

static = 'static'


def save_picture(file, folder_name: str = ''):
    random_str = secrets.token_hex(4)
    _, f_ext = os.path.splitext(file.filename)

    if f_ext.lower() not in ["png", "jpg"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="uploaded file is not a valid image")

    try:
        img = Image.open(file.file)
        img.verify()
        img.close()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"There was an error verifying the uploaded image {e}")

    picture_name = random_str + f_ext

    path = os.path.join(static, folder_name)
    if not os.path.exists(path):
        os.makedirs(path)

    picture_path = os.path.join(path, picture_name)

    output_size = (125, 125)
    img = Image.open(file.file)

    img.thumbnail(output_size)
    img.save(picture_path)

    return f'{static}/{folder_name}/{picture_name}'
