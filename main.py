from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

import cv2
import numpy as np

from API import run_fastapi_app
from FaceRec.app.main import run_flask


def preprocess_image(image_path: str) -> np.ndarray:

    image = cv2.imread(image_path)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    value = 40
    h, s, v = cv2.split(hsv)
    v = cv2.add(v, value)
    final_hsv = cv2.merge((h, s, v))
    image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle=10, scale=1.0)
    image = cv2.warpAffine(image, M, (w, h))

    return image


if __name__ == "__main__":
    preprocessed_image = preprocess_image("path_to_image.jpg")

    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(run_flask)
        executor.submit(run_fastapi_app)
