import cv2
import math
import numpy as np

class Eye(object):
    def __init__(self, frame, landmarks):
        self.frame = frame
        self.landmarks = landmarks
        self.margin = 5
        # self.margin = 0
        self.average_iris_size = 0.33
        self.eye_box = None
        self.eye_frame = None
        self.eye_x, self.eye_y = None, None
        self.num_frames = 30
        self.thresholds = []

        self.analyzing()
    
    ## dlib_eye
    # def get_eyemask(self, frame):
    #     frame_h, frame_w = frame.shape[:2]
    #     region = np.array(self.landmarks[:, :2], dtype=np.int32)
    #     mask = np.zeros((frame_h, frame_w), dtype=np.uint8)
    #     mask = cv2.fillConvexPoly(mask, region, 255)
    #     kernel = np.ones((9, 9), np.uint8)
    #     mask = cv2.dilate(mask, kernel, 5)

    #     min_x = np.min(region[:, 0]) - self.margin
    #     max_x = np.max(region[:, 0]) + self.margin
    #     min_y = np.min(region[:, 1]) - self.margin
    #     max_y = np.max(region[:, 1]) + self.margin

    #     image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #     image_gray[min_y:max_y, min_x:max_x] = cv2.equalizeHist(image_gray[min_y:max_y, min_x:max_x])
    #     eyes = cv2.bitwise_and(frame, frame, mask=mask)
    #     mask = (eyes == [0, 0, 0]).all(axis=2)
    #     eyes[mask] = [255, 255, 255]
    
    #     self.eye_frame = eyes[min_y:max_y, min_x:max_x]
    #     self.eye_frame = cv2.cvtColor(self.eye_frame, cv2.COLOR_BGR2GRAY)
    #     self.eye_box = (min_x, min_y)
    #     cv2.imshow('eye_frame', self.eye_frame)

    def get_eyemask(self, frame):
        frame_h, frame_w = frame.shape[:2]
        image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        region = np.array(self.landmarks[:, :2], dtype=np.int32)

        min_x = np.min(region[:, 0]) - self.margin
        max_x = np.max(region[:, 0]) + self.margin
        min_y = np.min(region[:, 1]) - self.margin
        max_y = np.max(region[:, 1]) + self.margin

        image_gray[min_y:max_y, min_x:max_x] = cv2.equalizeHist(image_gray[min_y:max_y, min_x:max_x])
        black_frame = np.zeros((frame_h, frame_w), np.uint8)
        mask = np.full((frame_h, frame_w), 255, np.uint8)
        cv2.fillPoly(mask, [region], (0, 0, 0))
        eye = cv2.bitwise_not(black_frame, image_gray.copy(), mask=mask)
        self.eye_frame = eye[min_y:max_y, min_x:max_x]
        self.eye_box = (min_x, min_y)
        cv2.imshow('eye_frame', self.eye_frame)

    def blinking_ratio(self, landmark):
        left = (landmark[0][0], landmark[0][1])
        right = (landmark[3][0], landmark[3][1])
        top = (int(landmark[1][0] + landmark[2][0] / 2), int(landmark[1][1] + landmark[2][1] / 2))
        bottom = (int(landmark[4][0] + landmark[5][0] / 2), int(landmark[4][1] + landmark[5][1] / 2))

        eye_width = math.hypot((left[0] - right[0]), (left[1] - right[1]))
        eye_height = math.hypot((top[0] - bottom[0]), (top[1] - bottom[1]))

        try:
            ratio = eye_width / eye_height
        except ZeroDivisionError:
            ratio = None

        return ratio

    def Image_processing(self, frame, threshold):
        kernel = np.ones((3, 3), np.uint8)
        new_frame = cv2.bilateralFilter(frame, 10, 15, 15)
        new_frame = cv2.erode(new_frame, kernel, iterations=3)
        new_frame = cv2.threshold(new_frame, threshold, 255, cv2.THRESH_BINARY)[1]

        return new_frame

    def get_iris_size(self, frame):
        if self.margin != 0:
            frame = frame[self.margin:-self.margin, self.margin:-self.margin]
        height, width = frame.shape[:2]
        nb_pixels = height * width
        nb_blacks = nb_pixels - cv2.countNonZero(frame)
        iris_size = nb_blacks / nb_pixels

        return iris_size

    def best_pupil_thres(self):
        trials = {}
        for threshold in range(5, 130, 3):
            new_frame = self.Image_processing(self.eye_frame, threshold)
            iris_sizes = self.get_iris_size(new_frame)
            trials[threshold] = iris_sizes
        best_threshold, iris_size = min(trials.items(), key=(lambda p: abs(p[1] - self.average_iris_size)))
        
        return best_threshold

    def Is_threshold(self):
        return len(self.thresholds) >= self.num_frames

    def get_threshold(self):
        best_thres = self.best_pupil_thres()
        self.thresholds.append(best_thres)

    def Detect_iris(self, frame):
        # cnts, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # try:
        #     cnt = max(cnts, key=cv2.contourArea)  # finding contour with #maximum area
        #     M = cv2.moments(cnt)
        #     x = int(M['m10'] / M['m00'])
        #     y = int(M['m01'] / M['m00'])
        #     return x, y
        # except:
        #     pass
        # return None, None

        contours, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
        contours = sorted(contours, key=cv2.contourArea)

        try:
            moments = cv2.moments(contours[-2])
            x = int(moments['m10'] / moments['m00'])
            y = int(moments['m01'] / moments['m00'])
            return x, y
        except (IndexError, ZeroDivisionError):
                pass
                return None, None

    def analyzing(self):
        self.blinking = self.blinking_ratio(self.landmarks)
        self.get_eyemask(self.frame)

        if not self.Is_threshold():
            self.get_threshold()

        threshold = int(sum(self.thresholds) / len(self.thresholds))
        # new_frame = self.Image_processing(self.eye_frame, threshold)
        new_frame = cv2.threshold(self.eye_frame, threshold, 255, cv2.THRESH_BINARY)[1]
        # kernel = np.ones((5, 5), np.uint8)
        # new_frame = cv2.morphologyEx(new_frame, cv2.MORPH_OPEN, kernel) 
        new_frame = cv2.erode(new_frame, None, iterations=2)
        new_frame = cv2.dilate(new_frame, None, iterations=1) 
        new_frame = cv2.medianBlur(new_frame, 3)
        cv2.imshow('new_frame', new_frame)
        self.eye_x, self.eye_y = self.Detect_iris(new_frame) 