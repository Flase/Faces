#! /usr/bin/env python
import os
import cv2
import argparse

from face_detection import select_face, select_all_faces
from face_swap import face_swap

def my_func(args):
    # Read images
    src_img = cv2.imread(args.src)
    dst_img = cv2.imread(args.dst)

    # Select src face
    src_points, src_shape, src_face = select_face(src_img)
    # Select dst face
    dst_faceBoxes = select_all_faces(dst_img)

    if dst_faceBoxes is None:
        print('Detect 0 Face !!!')
        exit(-1)

    output = dst_img
    for k, dst_face in dst_faceBoxes.items():
        output = face_swap(src_face, dst_face["face"], src_points,
                           dst_face["points"], dst_face["shape"],
                           output, args)

    dir_path = os.path.dirname(args.out)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    cv2.imwrite(args.out, output)

    ##For debug
    if not args.no_debug_window:
        cv2.imshow("From", dst_img)
        cv2.imshow("To", output)
        cv2.waitKey(0)

        cv2.destroyAllWindows()
