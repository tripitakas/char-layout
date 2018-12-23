import json
from .check_mulsubcol import check_multiple_subcolumns
from .mark_mulsubcol import mark_subcolumns
from .use_noteid import calc_order

# A 是否包含在B当中
def is_contained_in(A,B):
    threshold = 20
    if A['x']-B['x']>=-threshold:
        if A['x']+A['w']-B['x']-B['w']<=threshold:
            if A['y']-B['y']>=-threshold:
                if A['y']+A['h']-B['y']-B['h']<=threshold:
                    return True
    return False




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
    #print(char_list)
    #print(json_str)



