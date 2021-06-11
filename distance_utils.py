import cv2
import numpy as np
import math


def error_check(in_str):
    if '  ' in in_str:
        d = in_str.split('  ')
        x = d[0].replace(' ', '')
        y = d[1].replace(' ', '')

        xy = f'{x} {y}'
    else:
        xy = in_str

    return xy


# 두 눈 끝 사이
def twoeyeend(label, l_dis, r_dis):
    a = []
    for i in range(len(label)):
        b = label[i][45] - label[i][36]
        a.append(math.sqrt(pow(b[0], 2) + pow(b[1], 2)))

    a = np.array(a)
    ll = []
    rr = []
    for i in range(len(label)):
        ll.append(l_dis[i] / a[i])
        rr.append(r_dis[i] / a[i])

    return ll, rr


# 코-왼눈끝
def nose_leyeend(label, l_dis, r_dis):
    a = []
    for i in range(len(label)):
        b = label[i][33] - label[i][36]
        a.append(math.sqrt(pow(b[0], 2) + pow(b[1], 2)))

    a = np.array(a)
    ll = []
    rr = []
    for i in range(len(label)):
        ll.append(l_dis[i] / a[i])
        rr.append(r_dis[i] / a[i])

    return ll, rr


# 코-오눈끝
def nose_reyeend(label, l_dis, r_dis):
    a = []
    for i in range(len(label)):
        b = label[i][33] - label[i][45]
        a.append(math.sqrt(pow(b[0], 2) + pow(b[1], 2)))

    a = np.array(a)
    ll = []
    rr = []
    for i in range(len(label)):
        ll.append(l_dis[i] / a[i])
        rr.append(r_dis[i] / a[i])

    return ll, rr


# 양눈 안쪽
def twoeyein(label, l_dis, r_dis):
    a = []
    for i in range(len(label)):
        b = label[i][42] - label[i][39]
        a.append(math.sqrt(pow(b[0], 2) + pow(b[1], 2)))

    a = np.array(a)
    ll = []
    rr = []
    for i in range(len(label)):
        ll.append(l_dis[i] / a[i])
        rr.append(r_dis[i] / a[i])

    return ll, rr


# 코-왼눈안
def nose_leyein(label, l_dis, r_dis):
    a = []
    for i in range(len(label)):
        b = label[i][33] - label[i][39]
        a.append(math.sqrt(pow(b[0], 2) + pow(b[1], 2)))

    a = np.array(a)
    ll = []
    rr = []
    for i in range(len(label)):
        ll.append(l_dis[i] / a[i])
        rr.append(r_dis[i] / a[i])

    return ll, rr


# 코-오눈안
def nose_reyein(label, l_dis, r_dis):
    a = []
    for i in range(len(label)):
        b = label[i][33] - label[i][45]
        a.append(math.sqrt(pow(b[0], 2) + pow(b[1], 2)))

    a = np.array(a)
    ll = []
    rr = []
    for i in range(len(label)):
        ll.append(l_dis[i] / a[i])
        rr.append(r_dis[i] / a[i])

    return ll, rr


# 코 맨위-왼눈안
def upnose_leyein(label, l_dis, r_dis):
    a = []
    for i in range(len(label)):
        b = label[i][27] - label[i][39]
        a.append(math.sqrt(pow(b[0], 2) + pow(b[1], 2)))

    a = np.array(a)
    ll = []
    rr = []
    for i in range(len(label)):
        ll.append(l_dis[i] / a[i])
        rr.append(r_dis[i] / a[i])

    return ll, rr


# 코 맨위-오눈안
def upnose_reyein(label, l_dis, r_dis):
    a = []
    for i in range(len(label)):
        b = label[i][27] - label[i][42]
        a.append(math.sqrt(pow(b[0], 2) + pow(b[1], 2)))

    a = np.array(a)
    ll = []
    rr = []
    for i in range(len(label)):
        ll.append(l_dis[i] / a[i])
        rr.append(r_dis[i] / a[i])

    return ll, rr


# 두 광대 사이
def outface(label, l_dis, r_dis):
    a = []
    for i in range(len(label)):
        b = label[i][16] - label[i][0]
        a.append(math.sqrt(pow(b[0], 2) + pow(b[1], 2)))

    a = np.array(a)
    ll = []
    rr = []
    for i in range(len(label)):
        ll.append(l_dis[i] / a[i])
        rr.append(r_dis[i] / a[i])

    return ll, rr


# 왼광대-턱
def lout_chin(label, l_dis, r_dis):
    a = []
    for i in range(len(label)):
        b = label[i][8] - label[i][0]
        a.append(math.sqrt(pow(b[0], 2) + pow(b[1], 2)))

    a = np.array(a)
    ll = []
    rr = []
    for i in range(len(label)):
        ll.append(l_dis[i] / a[i])
        rr.append(r_dis[i] / a[i])

    return ll, rr


# 오광대-턱
def rout_chin(label, l_dis, r_dis):
    a = []
    for i in range(len(label)):
        b = label[i][8] - label[i][16]
        a.append(math.sqrt(pow(b[0], 2) + pow(b[1], 2)))

    a = np.array(a)
    ll = []
    rr = []
    for i in range(len(label)):
        ll.append(l_dis[i] / a[i])
        rr.append(r_dis[i] / a[i])

    return ll, rr


# 왼눈끝-입술아래
def lmouse(label, l_dis, r_dis):
    a = []
    for i in range(len(label)):
        b = label[i][36] - label[i][57]
        a.append(math.sqrt(pow(b[0], 2) + pow(b[1], 2)))

    a = np.array(a)
    ll = []
    rr = []
    for i in range(len(label)):
        ll.append(l_dis[i] / a[i])
        rr.append(r_dis[i] / a[i])

    return ll, rr


# 오눈끝-입술아래
def rmouse(label, l_dis, r_dis):
    a = []
    for i in range(len(label)):
        b = label[i][45] - label[i][57]
        a.append(math.sqrt(pow(b[0], 2) + pow(b[1], 2)))

    a = np.array(a)
    ll = []
    rr = []
    for i in range(len(label)):
        ll.append(l_dis[i] / a[i])
        rr.append(r_dis[i] / a[i])

    return ll, rr


# 왼눈끝-왼입술끝
def lmouseend(label, l_dis, r_dis):
    a = []
    for i in range(len(label)):
        b = label[i][36] - label[i][48]
        a.append(math.sqrt(pow(b[0], 2) + pow(b[1], 2)))

    a = np.array(a)
    ll = []
    rr = []
    for i in range(len(label)):
        ll.append(l_dis[i] / a[i])
        rr.append(r_dis[i] / a[i])

    return ll, rr


# 오눈끝-오입술끝
def rmouseend(label, l_dis, r_dis):
    a = []
    for i in range(len(label)):
        b = label[i][45] - label[i][54]
        a.append(math.sqrt(pow(b[0], 2) + pow(b[1], 2)))

    a = np.array(a)
    ll = []
    rr = []
    for i in range(len(label)):
        ll.append(l_dis[i] / a[i])
        rr.append(r_dis[i] / a[i])

    return ll, rr