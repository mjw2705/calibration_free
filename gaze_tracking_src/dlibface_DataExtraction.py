import cv2
import csv
import dlib
import numpy as np
import time
from eye import *
from utils import *



def click_event(event, x, y, flags, param):
    global click_pt

    if event == cv2.EVENT_LBUTTONDOWN:
        click_pt = [x, y]

def calib_board(frame_shape, n_point, i, j):
    whiteboard = np.ones((frame_shape[1], frame_shape[0], 3), np.uint8)

    w_interval = frame_shape[0] // (points[n_point] ** 0.5 - 1)
    h_interval = frame_shape[1] // (points[n_point] ** 0.5 - 1)

    x = int(w_interval * j)
    y = int(h_interval * i)
    x = init_x if x < init_x else x
    y = init_y if y < init_y else y
    if x > frame_shape[0] - init_x: 
        x = frame_shape[0] - init_x
    if y > frame_shape[1] - init_y:
        y = frame_shape[1] - init_y
    
    whiteboard = cv2.circle(whiteboard, (x, y), 10, (0, 0, 255), -1)
    
    cv2.namedWindow("whiteboard", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("whiteboard", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("whiteboard", whiteboard)
    cv2.setMouseCallback("whiteboard", click_event)

    return x, y



path = './jw_data/jw_data7/'
whole_dir = 'whole_img'
face_dir = 'face_img'
check_dir = 'check_img'
land_path = './saved_model/shape_predictor_68_face_landmarks.dat'

click_pt = []
face_size = (224, 224)
frame_shape = (640, 480)
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
# cap = cv2.VideoCapture('ex2.mp4')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_shape[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_shape[1])
cap.set(cv2.CAP_PROP_FPS, 30)

points = [9, 16, 25]
n_point, i, j = 0, 0, 0
init_x, init_y = 10, 10

face_detector = dlib.get_frontal_face_detector()
land_detector = dlib.shape_predictor(land_path)

createDir(path)
createDir(path+whole_dir)
createDir(path+face_dir)
createDir(path+check_dir)

f1 = open(f'./{path}/whole_landmark.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(f1)
writer.writerow(['ImageID', 'click_point', 'left_center', 'right_center', 'Landmarks'])

f2 = open(f'./{path}/face_landmark.csv', 'w', encoding='utf-8', newline='')
writer2 = csv.writer(f2)
writer2.writerow(['ImageID', 'click_point', 'left_center', 'right_center', 'Landmarks'])

land_detect, face_detect = False, False
prev_lms = []
prev_bbox = []

while cap.isOpened():
    success, image = cap.read()
    image = cv2.resize(image, (frame_shape))
    # image = cv2.flip(image, 1)
    if not success:
        print("Ignoring empty camera frame.")
        continue

    faces = face_detector(image)
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if faces:
        cur_bbox = face_box(faces[0])

        cur_bbox, prev_bbox, land_detect = low_pass_filter(cur_bbox, prev_bbox, face_detect, 'face')
        
        sx, sy, ex, ey = cur_bbox
        face_img = image[sy:ey, sx:ex].copy()
        face_img = cv2.resize(face_img, (face_size))

        landmarks = land_detector(img_gray, faces[0])
        cur_lms = lms_shape_to_np(landmarks, land_add=2)

        cur_lms, prev_lms, land_detect = low_pass_filter(cur_lms, prev_lms, land_detect, 'landmark')
        cur_left_lms = cur_lms[LEFT_EYE_POINTS]
        cur_right_lms = cur_lms[RIGHT_EYE_POINTS]

        rel_lms = Convert_rel_lms(cur_lms, cur_bbox)
        abs_lms = Convert_abs_lms(face_size, rel_lms)

        left_eye = Eye(image, cur_left_lms)
        right_eye = Eye(image, cur_right_lms)

        if left_eye.eye_x and right_eye.eye_x:
            left_x = left_eye.eye_box[0] + left_eye.eye_x
            left_y = left_eye.eye_box[1] + left_eye.eye_y
            right_x = right_eye.eye_box[0] + right_eye.eye_x
            right_y = right_eye.eye_box[1] + right_eye.eye_y
            left = str(left_x) + " " + str(left_y)
            right = str(right_x) + " "  + str(right_y)

            eye_lms = [[left_x, left_y], [right_x, right_y]]
            rel_eye_lms = Convert_rel_lms(eye_lms, cur_bbox)
            abs_eye_lms = Convert_abs_lms(face_size, rel_eye_lms)
            
            abs_left_x, abs_left_y = abs_eye_lms[0][:]
            abs_right_x, abs_right_y = abs_eye_lms[1][:]
            abs_left = str(abs_left_x) + " " + str(abs_left_y)
            abs_right = str(abs_right_x) + " "  + str(abs_right_y)
            Draw_eyeball(face_img, (abs_left_x, abs_left_y))
            Draw_eyeball(face_img, (abs_right_x, abs_right_y))

        x, y = calib_board(frame_shape, n_point, i, j)
        if i >= int(points[n_point] ** 0.5):
            i = 0
            n_point += 1
            if n_point == len(points):
                break
        if j >= int(points[n_point] ** 0.5):
            j = 0
            i += 1
        
        if click_pt:
            if abs(click_pt[0] - x) < 8 and abs(click_pt[1] - y) < 8:
                cal_pt = f'{points[n_point]}_{i}_{j}'
                print(cal_pt)
                print(f'x : {click_pt[0]}, y : {click_pt[1]}')
                cv2.imwrite(path+whole_dir+f'/whole_{cal_pt}.jpg', image)
                cv2.imwrite(path+face_dir+f'/face_{cal_pt}.jpg', face_img)
                Draw_eyeball(image, (left_x, left_y))
                Draw_eyeball(image, (right_x, right_y))
                check_img = image[sy:ey, sx:ex].copy()
                check_img = cv2.resize(check_img, (face_size))
                cv2.imwrite(path+check_dir+f'/check_{cal_pt}.jpg', check_img)

                '''whole'''
                w_id = f'whole_{cal_pt}.jpg'
                clk_point = str(click_pt[0]) + " " + str(click_pt[1])
                cur_lms = np.concatenate(cur_lms).tolist()
                cur_lms = ' '.join(str(lms) for lms in cur_lms)
                writer.writerow([w_id, clk_point, left, right, cur_lms])

                '''face'''
                f_id = f'face_{cal_pt}.jpg'
                clk_point = str(click_pt[0]) + " " + str(click_pt[1])
                abs_lms = np.concatenate(abs_lms).tolist()
                abs_lms = ' '.join(str(lms) for lms in abs_lms)
                writer2.writerow([f_id, clk_point, abs_left, abs_right, abs_lms])

                j += 1
                click_pt.clear()
            else:
                click_pt.clear()

        cv2.rectangle(image, (sx, sy), (ex, ey), (255, 255, 0), 2)
        Draw_landmark(image, cur_left_lms)
        Draw_landmark(image, cur_right_lms)


    cv2.imshow('image', image)
    cv2.imshow('face_img', face_img)
    if cv2.waitKey(1) == 27:
        break

f1.close()
f2.close()
cv2.destroyAllWindows()
cap.release()