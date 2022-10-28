import os
from application import app


def get_image(id):
    for file_name in os.listdir(app.config['UPLOAD_PATH']):
        if f'{id}' in file_name:
            return file_name

    return 'capa_padrao.jpg'
