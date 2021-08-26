# coding=utf-8

import urllib
import numpy as np
import json

import cv2
import requests
import sys

LIMIT_PX = 1024
LIMIT_BYTE = 1024*1024  # 1MB
LIMIT_BOX = 40


def kakao_ocr_resize(image_path):
    """
    ocr detect/recognize api helper
    ocr api의 제약사항이 넘어서는 이미지는 요청 이전에 전처리가 필요.

    pixel 제약사항 초과: resize
    용량 제약사항 초과  : 다른 포맷으로 압축, 이미지 분할 등의 처리 필요. (예제에서 제공하지 않음)

    :param image_path: 이미지파일 경로
    :return:
    """
    image = image_path
    height, width, _ = image.shape

    if LIMIT_PX < height or LIMIT_PX < width:
        ratio = float(LIMIT_PX) / max(height, width)
        image = cv2.resize(image, None, fx=ratio, fy=ratio)
        height, width, _ = height, width, _ = image.shape

        # api 사용전에 이미지가 resize된 경우, recognize시 resize된 결과를 사용해야함.
        image_path = "{}_resized.jpg".format(image_path)
        cv2.imwrite(image_path, image)

        return image_path
    return None


def kakao_ocr(image_path, appkey):
    """
    OCR api request example
    :param image_path: 이미지파일 경로
    :param appkey: 카카오 앱 REST API 키
    """
    API_URL = 'https://dapi.kakao.com/v2/vision/text/ocr'

    headers = {'Authorization': 'KakaoAK {}'.format(appkey)}

    # image = cv2.imread(image_path)
    # image = cv2.imshow('image', image_path)
    # image = image_path
    # jpeg_image = cv2.imwrite(".jpg", image_path)
    # jpeg_image = cv2.imencode(".jpg", image_path)
    # jpeg_image = cv2.imencode(".jpg", image)[1]
    # image_path= np.fromstring(image_path, dtype=int, sep='\n')
    data = image_path.tobytes()


    return requests.post(API_URL, headers=headers, files={"image": data})


def main(image_url):
    if len(sys.argv) != 3:
        print("Please run with args: $ python example.py /path/to/image appkey")
    image_url, appkey = image_url, '@준기 여기에 앱키 넣으시오!!'

    # resp = urllib.request.urlopen(image_url)
    # image_path = np.asarray(bytearray(resp.read()), dtype="uint8")
    # image_path = cv2.imdecode(image_path, cv2.IMREAD_COLOR)
    image_nparray = np.asarray(bytearray(requests.get(image_url).content), dtype=np.uint8)
    image_path = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)
    image = cv2.imwrite('ocrimg.jpeg', image_path)

    resize_impath = kakao_ocr_resize(image_path)
    if resize_impath is not None:
        image_path = resize_impath
        print("원본 대신 리사이즈된 이미지를 사용합니다.")

    output = kakao_ocr(image_nparray, appkey).json()
    outputdata = json.dumps(output, ensure_ascii=False, sort_keys=True, indent=2)
    outputdata = json.loads(outputdata)
    ocr_text = ""
    for i in range(len(outputdata['result'])):
        ocr_text += (outputdata['result'][i]['recognition_words'][0])
    print(ocr_text)
    return ocr_text
    # print("[OCR] output:\n{}\n".format(json.dumps(output, sort_keys=True, indent=2)))


if __name__ == "__main__":
    main()