import os
import secrets
from fastapi import HTTPException, status
from PIL import Image

static = 'static'


async def save_picture(file, folder_name: str = '', file_name: str = None):
    random_str = secrets.token_hex(4)
    _, f_ext = os.path.splitext(file.filename)
    print(f_ext)

    if f_ext.lower() not in [".png", ".jpg"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="uploaded file is not a valid image")

    picture_name = str(file_name.lower()) + random_str + f_ext

    path = os.path.join(static, folder_name)
    if not os.path.exists(path):
        os.makedirs(path)

    picture_path = os.path.join(path, picture_name)
    img = Image.open(file.file)
    img.save(picture_path)

    return f'{static}/{folder_name}/{picture_name}'
