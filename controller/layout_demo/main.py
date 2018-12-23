import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from check_mulsubcol import check_multiple_subcolumns
from mark_mulsubcol import mark_subcolumns
from use_noteid import calc_order

# A 是否包含在B当中
def is_contained_in(A,B):
    threshold = 20
    if A['x']-B['x']>=-threshold:
        if A['x']+A['w']-B['x']-B['w']<=threshold:
            if A['y']-B['y']>=-threshold:
                if A['y']+A['h']-B['y']-B['h']<=threshold:
                    return True
    return False


# 显示字框
def show(char_list, coordinate_char_list, indices, ax, filename):
    for i in indices:
        xleft = coordinate_char_list[i]['x']
        xright = xleft+coordinate_char_list[i]['w']
        yup = coordinate_char_list[i]['y']
        ydown = yup+coordinate_char_list[i]['h']
        A = char_list[i]
        if A['subcolumn_id'] == 0:
            #plt.plot([xleft,xright],[yup,yup],'r-')
            #plt.plot([xleft, xright], [ydown, ydown], 'r-')
            #plt.plot([xleft, xleft], [yup, ydown], 'r-')
            #plt.plot([xright, xright], [yup, ydown], 'r-')
            rect = plt.Rectangle((xleft, yup), coordinate_char_list[i]['w'], coordinate_char_list[i]['h'], color='r', alpha=0.1)
            ax.add_patch(rect)
        else:
            radius = min([coordinate_char_list[i]['h'], coordinate_char_list[i]['w']])/2
            circ = plt.Circle(((xleft+xright)/2, (yup+ydown)/2), radius, color='g', alpha=0.5)  # 圆心，半径，颜色，α
            ax.add_patch(circ)
#        plt.text(xleft,-ydown,str(i)+','+str(A['up_connect'])+','+str(A['down_connect']))
#        plt.text(xleft,-ydown,str(A['column_id'])+'-'+str(A['ch_id'])+'-'+str(A['subcolumn_id'])+'-'+str(A['note_id']))
#        plt.text(xleft, ydown,str(A['column_order']))
    plt.savefig(filename, dpi = 300)
#    plt.show()
    return
# 显示连线
def show_connection(char_list, coordinate_char_list, indices):
    for order in range(1,len(indices)):
        for i in indices:
            if char_list[i]['column_order']==order:
                A = coordinate_char_list[i]
            if char_list[i]['column_order'] == order+1:
                B = coordinate_char_list[i]
        Ax = A['x']+A['w']*3/4
        Ay = A['y']+A['h']*3/4
        Bx = B['x']+B['w']*3/4
        By = B['y']+B['h']*1/4
        if Ay<By:
            plt.plot([Ax,Bx],[Ay,By],'g-')
            #plt.arrow(Ax,Ay, Bx-Ax, By-Ay, color='g', linestyle='-')
        else:
            plt.plot([Ax,Bx],[Ay,By],'r-')
    return

# main 函数
#########################################################################
if __name__ == '__main__':
    # 文件路径
    filename = "data/JX_165_7_12"
    # 加载字框数据
    with open(filename+".json", 'r', encoding='UTF-8') as load_f:
        data_dict = json.load(load_f)
        coordinate_char_list = data_dict['chars']
    # 加载栏框和列框数据
    with open(filename + "_column" + ".json", 'r') as load_f:
        data_dict = json.load(load_f)
        coordinate_block_list = data_dict['blocks']
        coordinate_column_list = data_dict['columns']
#########################################################################
    # 定义新的字框数据结构
    char_list = []
    for i in range(0, len(coordinate_char_list)):
        char_list.append({'block_id': 0, 'column_id': 0, 'ch_id': 0, 'subcolumn_id': 0, 'note_id': 0, 'column_order':0})

    # 标记栏框和列框
    for i in range(0, len(coordinate_char_list)):
        for i_b in range(0, len(coordinate_block_list)):
            if is_contained_in(coordinate_char_list[i], coordinate_block_list[i_b]):
                char_list[i]['block_id'] = i_b+1
        for i_c in range(0, len(coordinate_column_list)):
            if is_contained_in(coordinate_char_list[i], coordinate_column_list[i_c]):
                char_list[i]['column_id'] = i_c+1
##########################################################################
    # 逐列处理
    for i_b in range(0, len(coordinate_block_list)):
        for i_c in range(0, len(coordinate_column_list)):
            # 统计列内字框的索引
            char_indices_in_column = []
            for i in range(0, len(coordinate_char_list)):
                if char_list[i]['column_id'] == i_c+1 and char_list[i]['block_id']==i_b+1:
                    char_indices_in_column.append(i)
            # 按高度重新排序
            idx_sorted = sorted(range(len(char_indices_in_column)),
                                key=lambda k: coordinate_char_list[char_indices_in_column[k]]['y'])
            sorted_char_indices = []
            for i in range(0, len(char_indices_in_column)):
                sorted_char_indices.append(char_indices_in_column[idx_sorted[i]])

            # 判断是否存在夹注小字
            flag_multiple_subcolumns = check_multiple_subcolumns(coordinate_char_list, sorted_char_indices)
            # 按高度排序，标记大字
            if flag_multiple_subcolumns == 0:
                order = 1
                for i in sorted_char_indices:
                    char_list[i]['ch_id'] = order
                    char_list[i]['column_order'] = order
                    order = order + 1
            else:
                # 标记夹注小字
                mark_subcolumns(coordinate_char_list, char_list, sorted_char_indices)
                calc_order(char_list, sorted_char_indices)
    # 保存数据
    py2json = {}
    py2json['char_list'] = char_list
    json_str = json.dumps(py2json)
    print(char_list)
    print(json_str)



    #print(char_list)
    # 读取图片
    pic = mpimg.imread(filename + ".jpg")
    fig, ax = plt.subplots()
    im = ax.imshow(pic, cmap='gray')
    plt.axis('off')
    show(char_list, coordinate_char_list, [n for n in range(0,len(char_list))], ax=ax, filename=filename + '_note.jpg')

    fig, ax = plt.subplots()
    im = ax.imshow(pic, cmap='gray')
    plt.axis('off')
    for i_b in range(0, len(coordinate_block_list)):
        for i_c in range(0, len(coordinate_column_list)):
            # 统计列内字框的索引
            char_indices_in_column = []
            for i in range(0, len(coordinate_char_list)):
                if char_list[i]['column_id'] == i_c+1 and char_list[i]['block_id']==i_b+1:
                    char_indices_in_column.append(i)

            show_connection(char_list, coordinate_char_list, char_indices_in_column)
    plt.savefig(filename+'_lines.jpg', dpi = 300)
    #plt.show()
