import csv
from utils import *

'''
100, 150cm id 비교해서 같은 id만 계산
'''
def read_csv(name, dis):
    name_dis = f'{name}_{dis}'

    f = open(f'{root_dir + name_dis}/{name_dis}_whole.csv', 'r', encoding='utf-8')
    datas = csv.reader(f)
    next(datas)

    data_list = []
    for data in datas:
        data_list.append(data)
    f.close()

    # id, 왼쪽/오른쪽 동공 중심, 랜드마크 좌표 가져오기
    id = []
    l_labels = []
    r_labels = []
    labels = []
    for i in data_list:
        id.append(i[0])
        l_xy = error_check(i[3])
        r_xy = error_check(i[4])
        l_labels.append(list(map(float, l_xy.split(' '))))
        r_labels.append(list(map(float, r_xy.split(' '))))
        labels.append(list(map(int, i[5].split(' '))))

    id = np.array(id)
    l_label = np.array(l_labels)
    r_label = np.array(r_labels)
    labels = np.array(labels)

    # 좌표값 x,y로 묶기
    label = []
    for i in labels:
        label.append(i.reshape(-1, 2))
    label = np.array(label)

    return id, l_label, r_label, label


# 왼/오 동공-코거리 각각 9개 정규화값 csv 저장
def normal_dist(name, dis, l_label, r_label, label, saved_dir):
    name_dis = f'{name}_{dis}'

    # 동공과 코 거리계산 왼/오 각각 9개
    l_dis = []
    r_dis = []
    for i, (l, r) in enumerate(zip(l_label, r_label)):
        l_dis1 = []
        r_dis1 = []
        for j in range(27, 36):
            a = l - label[i][j]
            b = r - label[i][j]
            l_dis1.append(math.sqrt(pow(a[0], 2) + pow(a[1], 2)))
            r_dis1.append(math.sqrt(pow(b[0], 2) + pow(b[1], 2)))
        l_dis.append(l_dis1)
        r_dis.append(r_dis1)

    l_dis = np.array(l_dis)
    r_dis = np.array(r_dis)

    # 왼/오 동공-코거리 각 9개 정규화값 csv 저장
    distance = [twoeyeend, nose_leyeend, nose_reyeend, twoeyein, nose_leyein, nose_reyein, upnose_leyein, upnose_reyein,
                outface, lout_chin, rout_chin, lmouse, rmouse, lmouseend, rmouseend]

    for distan in distance:
        dis = distan(label, l_dis, r_dis)

        f = open(f'{saved_dir}/{name_dis}_{distan.__name__}.csv', 'w', encoding='utf-8', newline='')
        writer = csv.writer(f)
        writer.writerow(['l_distance', '', '', '', '', '', '', '', '', 'r_distance'])
        for l, r in zip(dis[0], dis[1]):
            merge_list = []
            merge_list.extend(l)
            merge_list.extend(r)
            writer.writerow(merge_list)
        f.close()


root_dir = './data/'
names = ['hhs', 'hny', 'jgw', 'jwh', 'knh', 'lgy', 'lmk', 'lsg', 'mjw', 'nes', 'sgh', 'ssw', 'ysk']
saved_dir = 'csv'

for n in names:
    a = read_csv(n, 100)
    b = read_csv(n, 150)
    inter1015 = np.intersect1d(a[0], b[0])  # id 비교해서 100, 150 둘다 있는 id만

    id00 = []
    l_label00 = []
    r_label00 = []
    label00 = []
    id50 = []
    l_label50 = []
    r_label50 = []
    label50 = []

    for i in range(len(a[0])):
        if a[0][i] in inter1015:
            id00.append(a[0][i])
            l_label00.append(a[1][i])
            r_label00.append(a[2][i])
            label00.append(a[3][i])
    for i in range(len(b[0])):
        if b[0][i] in inter1015:
            id50.append(b[0][i])
            l_label50.append(b[1][i])
            r_label50.append(b[2][i])
            label50.append(b[3][i])

    id100 = np.array(id00)
    l_label100 = np.array(l_label00)
    r_label100 = np.array(r_label00)
    label100 = np.array(label00)
    id150 = np.array(id50)
    l_label150 = np.array(l_label50)
    r_label150 = np.array(r_label50)
    label150 = np.array(label50)

    normal_dist(n, 100, l_label100, r_label100, label100, saved_dir)
    normal_dist(n, 150, l_label150, r_label150, label150, saved_dir)