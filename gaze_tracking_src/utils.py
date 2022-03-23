import cv2
import os
import numpy as np
import mediapipe as mp


LEFT_EYE_POINTS = [36, 37, 38, 39, 40, 41]
RIGHT_EYE_POINTS = [42, 43, 44, 45, 46, 47]
eye_top = [37, 38, 43, 44]
eye_bottom = [40, 41, 46, 47]
eye_side_left = [36, 42]
eye_side_right = [39, 45]
NOSE_POINTS = [27, 28, 29, 30, 31, 32, 33, 34, 35]
gaps = [20, 2]

# fash mesh
# 큰 눈
# left_idx = [22, 23, 24, 110, 25, 130, 247, 30, 29, 27, 28, 56, 190, 243, 112, 26] # 16개
# right_idx = [463, 414, 286, 258, 257, 259, 260, 467, 359, 255, 339, 254, 253, 252, 256, 341]

left_idx = [33, 246, 161, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 163, 7]
right_idx = [362, 398, 384, 385, 386, 387, 388, 466, 263, 249, 390, 373, 374, 380, 381, 382]
nose_idx = [6, 197, 195, 5, 4, 115, 131, 79, 20, 94, 250, 309, 344, 360]

def face_roi(frame_shape, face_lms):
    sx, sy = frame_shape
    ex, ey = 0, 0
    for lms in face_lms:
        cx, cy = int(lms[0] * frame_shape[0]), int(lms[1] * frame_shape[1])
        if cx < sx: sx = cx
        if cy < sy: sy = cy
        if cx > ex: ex = cx
        if cy > ey: ey = cy

    bbox = sx, sy, ex, ey
    return bbox

def Face_mesh(image):
    face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=True,
                                                max_num_faces=1,
                                                min_detection_confidence=0.7)
    image.flags.writeable = False
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)
    image.flags.writeable = True

    if results.multi_face_landmarks:
        for landmarks in results.multi_face_landmarks:
            face_lms = [[lms.x, lms.y, lms.z] for lms in landmarks.landmark] #len 468
        return face_lms
    return None

def Convert_abs_lms(frame_shape, lms):
    abs_lms = np.array(lms)
    abs_lms[:, 0] = abs_lms[:, 0] * frame_shape[0]
    abs_lms[:, 1] = abs_lms[:, 1] * frame_shape[1]
    return abs_lms[:, :2]

def Convert_rel_lms(lms, bbox):
    rel_lms = np.zeros((len(lms), 2), dtype="float")
    lms = np.array(lms)
    rel_lms[:, 0] = (lms[:, 0] - bbox[0]) / (bbox[2]- bbox[0])
    rel_lms[:, 1] = (lms[:, 1] - bbox[1]) / (bbox[3]- bbox[1])
    return rel_lms[:, :2]

def Draw_landmark(image, lms):
    for lm in lms:
        cv2.circle(image, (int(lm[0]), int(lm[1])), 1, (0, 0, 255), -1, cv2.LINE_AA)

def Draw_eyeball(image, center):
    cv2.line(image, (int(center[0]), int(center[1] - 1)), (int(center[0]), int(center[1] + 1)), (0, 255, 0))
    cv2.line(image, (int(center[0] - 1), int(center[1])), (int(center[0] + 1), int(center[1])), (0, 255, 0))


def face_box(bbox):
    x1 = bbox.left()
    y1 = bbox.top()
    x2 = bbox.right()
    y2 = bbox.bottom()
    bbox = x1, y1, x2, y2
    return bbox

def lms_shape_to_np(landmarks, land_add, dtype="int"):
    coords = np.zeros((68, 2), dtype=dtype)

    # for i in range(0, 68):
    #     coords[i] = (landmarks.part(i).x, landmarks.part(i).y)
    for i in range(0, 68):
        x = landmarks.part(i).x
        y = landmarks.part(i).y
        if i in eye_top:
            coords[i] = (x, y - land_add)
        elif i in eye_bottom:
            coords[i] = (x, y + land_add)
        elif i in eye_side_left:
            coords[i] = (x - (land_add-2), y)
        elif i in eye_side_right:
            coords[i] = (x + (land_add+2), y)
        else:
            coords[i] = (x, y)

    return coords

def is_blinking(left, right):
    blink_ratio = (left + right) / 2
    return blink_ratio > 3.8

def low_pass_filter(cur, prev, detect, mode):
    if mode == 'face':
        if detect:
            if abs(prev[0] - cur[0]) < gaps[0]:
                cur[0] = prev[0]
            else:
                prev[0] = cur[0]
            if abs(prev[1] - cur[1]) < gaps[0]:
                cur[1] = prev[1]
            else:
                prev[1] = cur[1]
            if abs(prev[2] - cur[2]) < gaps[0]:
                cur[2] = prev[2]
            else:
                prev[2] = cur[2]
            if abs(prev[3] - cur[3]) < gaps[0]:
                cur[3] = prev[3]
            else:
                prev[3] = cur[3]
        else:
            detect = True
            prev = cur

    if mode == 'landmark':
        if detect:
            idx = 0
            for land, prev_land in zip(cur, prev):
                if abs(land[0] - prev_land[0]) < gaps[1]:
                    cur[idx][0] = prev_land[0]
                else:
                    prev[idx][0] = land[0]
                if abs(land[1] - prev_land[1]) < gaps[1]:
                    cur[idx][1] = prev_land[1]
                else:
                    prev[idx][1] = land[1]
                idx += 1
        else:
            detect = True
            prev = cur

    return cur, prev, detect



def createDir(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print("Error: Failed to create dir")