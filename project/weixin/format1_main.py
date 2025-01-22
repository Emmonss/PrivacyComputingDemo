
from format1_value_make import str_define,int_define,str_free,str_data_load,int_data_load
from format1_db_make import load_db_col_data,count_col_data
from format1_utils import list_make
from format1 import format1


if __name__ == '__main__':
    ######################################################
    db_col_data_list = list_make(errcode=8001)
    used = []

    db_result = ""
    for item in db_col_data_list:
        db_result += load_db_col_data.format(item[1],
                                          f'{item[0]}_{item[3]}',
                                          f'{item[0]}_{item[4]}',
                                          item[5],
                                          len(f'{item[0]}_{item[3]}')
                                          )
    count_data = '$(LOAD_DB_COUNT)'
    for item in db_col_data_list:
        if item[1] == '税局测试key' or item[1] == '银行测试key':
            db_result += count_col_data.format(item[0], f'{item[0]}_{item[3]}', item[1])
        if item[1] == '税局测试key':
            count_data = f'{item[0]}_count'

    ######################################################
    data_col_data_list = list_make(errcode=9001)
    # define
    define_result = ''''''
    for item in data_col_data_list:
        if (item[2] == 'str'):
            define_result += str_define.format(
                '{}_{}'.format(item[0], item[3]),
                item[1])
        elif (item[2] == 'int'):
            define_result += int_define.format(
                '{}_{}'.format(item[0], item[3]),
                item[1])

    # print('define'.center(100, '='))
    # print(define_result)
    #
    #load
    # load data
    load_data_result = ''''''
    for item in data_col_data_list:
        if (item[2] == 'str'):
            load_data_result += str_data_load.format(
                f'{item[0]}_{item[3]}',
                item[5],
            )
        elif (item[2] == 'int'):
            load_data_result += int_data_load.format(
                f'{item[0]}_{item[3]}',
                item[5],
            )
    # print(load_data_result)

    # free
    free_result = ''''''
    for item in db_col_data_list:
        if (item[2] == 'str'):
            free_result += str_free.format('{}_{}'.format(item[0], item[3]))
    # print('free'.center(100, '='))
    # print(free_result)


    # ######################################################
    format1 = format1.replace("$(LOAD_DB)",db_result).replace("$(LOAD_DB_COUNT)",count_data)
    format1 = format1.replace("$(DEFINE_ITEM)", define_result)\
                    .replace("$(FREE_STR_ITEM)", free_result)\
                    .replace("$(LOAD_DATA_ITEM)",load_data_result)
    print(format1)
    pass