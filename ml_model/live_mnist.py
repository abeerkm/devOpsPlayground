import re
import imageio
import cv2
import numpy as np
from keras.models import load_model
from aiohttp import web
import base64
from PIL import Image
import io

font = cv2.FONT_HERSHEY_SIMPLEX
SIZE = 28


def annotate(frame, label, location=(20, 30)):
    """writes label on image"""

    cv2.putText(frame, label, location, font,
                fontScale=0.5,
                color=(255, 255, 0),
                thickness=1,
                lineType=cv2.LINE_AA)


def extract_digit(final_img, rect, pad=10):
    x, y, w, h = rect
    cropped_digit = final_img[y-pad:y+h+pad, x-pad:x+w+pad]
    cropped_digit = cropped_digit/255.0

    # only look at images that are somewhat big:
    if cropped_digit.shape[0] >= 32 and cropped_digit.shape[1] >= 32:
        cropped_digit = cv2.resize(cropped_digit, (SIZE, SIZE))
    else:
        return
    return cropped_digit


def img_to_mnist(frame):
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
    gray_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, blockSize=321, C=28)
    return gray_img


def getI420FromBase64(codec):
    base64_data = re.sub('^data:image/.+;base64,', '', codec.decode())
    byte_data = base64.b64decode(base64_data)
    image_data = io.BytesIO(byte_data)
    img = Image.open(image_data)
    img.load()  # required for png.split()
    background = Image.new("RGB", img.size, (255, 255, 255))
    background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
    background.save('image.jpg', 'JPEG', quality=80)
    # img.save('image.png', "PNG")


async def predict(request):
    data = await request.content.read()
    getI420FromBase64(data)
    im = imageio.imread('image.jpg')
    final_img = img_to_mnist(im)
    # image_shown = image
    contours, hierarchy = cv2.findContours(final_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    rects = [cv2.boundingRect(contour) for contour in contours]
    rects = [rect for rect in rects if rect[2] >= 3 and rect[3] >= 8]

    pred = 0

    for rect in rects:
        x, y, w, h = rect
        mnist_frame = extract_digit(final_img, rect, pad=15)

        if mnist_frame is not None:
            mnist_frame = np.fliplr(mnist_frame)
            mnist_frame = np.expand_dims(mnist_frame, 2)  # needed for keras
            mnist_frame = np.expand_dims(mnist_frame, 0)  # needed for keras


            class_prediction = model.predict(mnist_frame)
            class_prediction = np.argmax(class_prediction)
            # cv2.rectangle(image_shown, (x - 15, y - 15), (x + 15 + w, y + 15 + h), color=(255, 255, 0))
            label = labelz[class_prediction]
            print(label)
            pred = int(class_prediction)

            # annotate(image_shown, label, location=(rect[0], rect[1]))

    # cv2.imshow('frame', image_shown)
    return web.json_response({'prediction': pred})


def main():
    app = web.Application()
    app.add_routes([web.get('/predict', predict)])
    web.run_app(app, host='0.0.0.0')


if __name__ == '__main__':
    print("loading model")
    model = load_model("full_model.h5")
    labelz = dict(enumerate(["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]))
    main()
