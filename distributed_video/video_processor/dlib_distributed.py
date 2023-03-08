#!pip install dlib

import cv2
import imutils
from scipy.spatial import Delaunay
import dlib
import numpy as np
from typing import Tuple


# initialise model from dat file path - model file url : https://github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat
def initialise_model(model_path):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(model_path)

    return detector, predictor


# fetch coordinates from image using dlib
def get_coordinates(
    detector, predictor, image: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    # Resize to 500x500
    image = imutils.resize(image, width=500)
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # get face-rectangles from image - facial detection
    rects = detector(gray, 1)
    print(rects)
    print(type(rects))
    if len(rects) > 0:
        # get coordinates inside each rectangle (face)
        for i, rect in enumerate(rects):
            shape = predictor(gray, rect)
            print(shape)
            shape = np.zeros((68, 2), dtype=int)
            for i in range(0, 68):
                shape[i] = (
                    predictor(gray, rect).part(i).x,
                    predictor(gray, rect).part(i).y,
                )
    else:
        shape = None

    return shape, image


# draw delaunay traingles on facial landmarks
def draw_delaunay(shape: np.ndarray, image: np.ndarray) -> np.ndarray:
    # import delaunay function from scipy library
    delaunay = Delaunay(shape)
    triangles = delaunay.simplices

    # Plot the Delaunay triangles on the face
    for triangle in triangles:
        pt1 = tuple(shape[triangle[0]])
        pt2 = tuple(shape[triangle[1]])
        pt3 = tuple(shape[triangle[2]])
        cv2.line(image, pt1, pt2, (0, 255, 0), 2)
        cv2.line(image, pt2, pt3, (0, 255, 0), 2)
        cv2.line(image, pt3, pt1, (0, 255, 0), 2)

    return image


def dlib_main(image, frame_no):
    detector, predictor = initialise_model(
        "/home/phani/Desktop/disributed/project/distributed-video-processing/distributed_video/assets/shape_predictor_68_face_landmarks.dat"
    )
    # image = cv2.imread('/home/phani/Desktop/disributed/project/distributed-video-processing/distributed_video/assets/face.jpg')
    print("reached to dlib function")
    shape, image = get_coordinates(detector, predictor, image)
    if shape is not None:
        output = draw_delaunay(shape, image)
    else:
        output = image
    cv2.imwrite((str(frame_no) + ".jpg"), output)
    return "frame saved: " + str(frame_no)
