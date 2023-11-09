import os
from roboflow import Roboflow
from PIL import Image

IMG_PATH = 'C:\\Python\\my_projects\\Work\\img\\'


def start():
    rf = Roboflow(api_key="AujVadRIqTT8kja5pvId")
    project = rf.workspace().project("women-fashion-styles")
    model = project.version(1).model

    num = 0
    for enum, photo in enumerate(os.listdir(IMG_PATH)):
        if photo[-3:] != 'jpg':
            continue
        temp_pict = IMG_PATH + photo
        with Image.open(temp_pict) as im:
            (width, height) = im.size
        if width < 200 or height < 200:
            try:
                os.remove(temp_pict)
                print(f'remove {photo}')
            except:
                print(f'cant remove {photo}')
            continue

        pred = model.predict(temp_pict, confidence=65, overlap=40).json()['predictions']
        if len(pred) == 0:
            try:
                os.rename(temp_pict,
                      IMG_PATH + 'temp\\' + photo     )
            except:
                print(f'cant remove {photo}')

        else:
            try:
                os.rename(IMG_PATH + photo, IMG_PATH + 'done\\' + photo)
            except Exception as ex:
                print(f'cant move {photo}, {ex}')
        if enum % 500 == 0:
            print(enum)

if __name__ == '__main__':
    start()



