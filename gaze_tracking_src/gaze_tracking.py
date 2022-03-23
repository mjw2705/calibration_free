import cv2
from eye import *
from utils import *


frame_shape = (640, 480)
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
# cap = cv2.VideoCapture('ex.mp4')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_shape[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_shape[1])
cap.set(cv2.CAP_PROP_FPS, 30)
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('ex.avi', fourcc, 30, (frame_shape))

while cap.isOpened():

    success, image = cap.read()
    image = cv2.resize(image, (frame_shape))
    image = cv2.flip(image, 1)
    if not success:
        print("Ignoring empty camera frame.")
        continue

    face_lms = Face_mesh(image)
    
    if face_lms:
        cur_bbox = face_roi(frame_shape, face_lms)
        sx, sy, ex, ey = cur_bbox
        face_img = image[sy:ey, sx:ex].copy()

        left_lms = [face_lms[l_idx] for l_idx in left_idx]
        right_lms = [face_lms[r_idx] for r_idx in right_idx]
        nose_lms = [face_lms[n_idx] for n_idx in nose_idx]

        abs_left_lms = Convert_abs_lms(frame_shape, left_lms)
        abs_right_lms = Convert_abs_lms(frame_shape, right_lms)
        abs_nose_lms = Convert_abs_lms(frame_shape, nose_lms)
        abs_face_lms = Convert_abs_lms(frame_shape, face_lms)

        left_eye = Eye(image, abs_left_lms)
        right_eye = Eye(image, abs_right_lms)

        if left_eye.eye_x and right_eye.eye_x:
            left_x = left_eye.eye_box[0] + left_eye.eye_x
            left_y = left_eye.eye_box[1] + left_eye.eye_y
            right_x = right_eye.eye_box[0] + right_eye.eye_x
            right_y = right_eye.eye_box[1] + right_eye.eye_y

            Draw_eyeball(image, (left_x, left_y))
            Draw_eyeball(image, (right_x, right_y))

        Draw_landmark(image, abs_nose_lms)

    cv2.imshow('image', image)
    cv2.imshow('face', face_img)
    # out.write(image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

# out.release()
cap.release()
cv2.destroyAllWindows()