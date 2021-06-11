import csv
from distance_utils import *


root_dir = './data/'
names = ['hhs', 'hny', 'jgw', 'jwh', 'knh', 'lgy', 'lmk', 'lsg', 'mjw', 'nes', 'sgh', 'ssw', 'ysk']

for n in names:

    dis = [100, 150]
    for d in dis:
        name = f'{n}_{d}'

        f = open(f'{root_dir+name}/{name}_whole.csv', 'r', encoding='utf-8')
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

        # 동공과 코 거리 왼/오 각각 9개
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

        for dist in distance:
            dis = dist(label, l_dis, r_dis)

            f = open(f'csv/{name}_{dist.__name__}.csv', 'w', encoding='utf-8', newline='')
            writer = csv.writer(f)
            writer.writerow(['l_distance'])
            for l in dis[0]:
                writer.writerow(l)
            writer.writerow(['r_distance'])
            for r in dis[1]:
                writer.writerow(r)

            f.close()

