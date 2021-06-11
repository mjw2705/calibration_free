import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.font_manager as fm
from distance_utils import *


# font_path = 'C:\Windows\Fonts\GULIM.TTC'
# font = fm.FontProperties(fname=font_path)
names = ['hhs', 'hny', 'jgw', 'jwh', 'knh', 'lgy', 'lmk', 'lsg', 'mjw', 'nes', 'sgh', 'ssw', 'ysk']
# distance = ['twoeyeend', 'nose_leyeend', 'nose_reyeend', 'twoeyein', 'nose_leyein', 'nose_reyein', 'upnose_leyein',
#             'upnose_reyein', 'outface', 'lout_chin', 'rout_chin', 'lmouse', 'rmouse', 'lmouseend', 'rmouseend']
distance = ['nose_leyeend', 'outface', 'lout_chin',
            'rout_chin', 'lmouse', 'rmouse', 'lmouseend', 'rmouseend']
color = ['red', 'brown', 'orange', 'green', 'cyan', 'blue', 'purple', 'hotpink', 'gray', 'black', 'lawngreen']

load_csv = './csv'
saved_dir = 'scatter_8'

for n in names:
    left_arr = []
    right_arr = []
    for dis in distance:
        # 100cm
        f = open(f'{load_csv}/{n}_100_{dis}.csv', 'r', encoding='utf-8')
        data = csv.reader(f)
        next(data)
        ll_list100 = []
        rr_list100 = []
        for da in data:
            ll_list100.append(da[:9])
            rr_list100.append(da[9:])
        f.close()

        # 150cm
        f = open(f'{load_csv}/{n}_150_{dis}.csv', 'r', encoding='utf-8')
        data = csv.reader(f)
        next(data)
        ll_list150 = []
        rr_list150 = []
        for da in data:
            ll_list150.append(da[:9])
            rr_list150.append(da[9:])
        f.close()

        l_list100 = []
        r_list100 = []
        l_list150 = []
        r_list150 = []
        for i, j, k, q in zip(ll_list100, rr_list100, ll_list150, rr_list150):
            i_str = ' '.join(i)
            j_str = ' '.join(j)
            k_str = ' '.join(k)
            q_str = ' '.join(q)

            l_list100.append(list(map(float, i_str.split())))
            r_list100.append(list(map(float, j_str.split())))
            l_list150.append(list(map(float, k_str.split())))
            r_list150.append(list(map(float, q_str.split())))

        l_dis100 = np.array(l_list100)
        r_dis100 = np.array(r_list100)
        l_dis150 = np.array(l_list150)
        r_dis150 = np.array(r_list150)

        # 100-150 정규화 차이
        l_diff = []
        r_diff = []
        for i in range(len(l_dis150)):
            l_diff.append(np.abs(l_dis150[i] - l_dis100[i]))
            r_diff.append(np.abs(r_dis150[i] - r_dis100[i]))
        l_diff = np.array(l_diff)
        r_diff = np.array(r_diff)

        # 정규화 차이 평균 9개
        left = l_diff.mean(axis=0)
        right = r_diff.mean(axis=0)
        left_arr.append(left)
        right_arr.append(right)

    # scatter
    # num = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    # y = np.random.standard_normal(9)
    # plt.subplot(1, 2, 1)
    # for i, lf in enumerate(left_arr):
    #     colors = cm.rainbow(np.linspace(0, 1, len(left_arr)))
    #     plt.scatter(lf, y, color='1.0', edgecolors=colors[i], label=distance[i])
    # plt.xlabel('diff')
    # plt.title('Left')
    # plt.subplot(1, 2, 2)
    # for i, rt in enumerate(right_arr):
    #     # y = np.random.standard_normal(len(left_arr))
    #     colors = cm.rainbow(np.linspace(0, 1, len(left_arr)))
    #     plt.scatter(rt, y, color='1.0', edgecolors=colors[i], label=distance[i])
    # plt.xlabel('diff')
    # plt.title('Right')
    # plt.legend(distance)
    # plt.savefig(f'{saved_dir}/{n}.png')
    # plt.tight_layout()
    # plt.show()

    # scatter 그리기
    num = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    y = np.random.randn(9)

    for i, lf in enumerate(left_arr):
        colors = cm.rainbow(np.linspace(0, 1, len(left_arr)))
        plt.scatter(num, lf, color='1.0', edgecolors=color[i], label=distance[i])
    plt.ylabel('diff')
    plt.title('Left')
    plt.legend(distance)
    plt.savefig(f'{saved_dir}/{n}_left.png')
    plt.tight_layout()
    plt.show()

    for i, rt in enumerate(right_arr):
        # y = np.random.standard_normal(len(left_arr))
        colors = cm.rainbow(np.linspace(0, 1, len(left_arr)))
        plt.scatter(num, rt, color='1.0', edgecolors=color[i], label=distance[i])
    plt.ylabel('diff')
    plt.title('Right')
    plt.legend(distance)
    plt.savefig(f'{saved_dir}/{n}_right.png')
    plt.tight_layout()
    plt.show()


#     # 선그래프
#     num = [0, 1, 2, 3, 4, 5, 6, 7, 8]
#     plt.subplot(1, 2, 1)
#     for i, lf in enumerate(left_arr):
#         colors = cm.rainbow(np.linspace(0, 1, len(left_arr)))
#         plt.plot(num, lf, '.-', color=color[i])
#     plt.title('Left')
#     plt.ylabel('diff')
#
#     plt.subplot(1, 2, 2)
#     for i, rt in enumerate(right_arr):
#         colors = cm.rainbow(np.linspace(0, 1, len(left_arr)))
#         plt.plot(num, rt, '.-', color=color[i])
#     plt.title('Right')
#
#     plt.legend(distance)
#     plt.savefig(f'{n}.png')
#     plt.tight_layout()
#     plt.show()
# #
#     # f = open(f'hny_{dis}.csv', 'w', encoding='utf-8', newline='')
#     # writer = csv.writer(f)
#     # writer.writerow(left)
#     # writer.writerow(right)
#     # f.close()
