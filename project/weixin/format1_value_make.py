
from pprint import pprint
str_define = '''
        //{1}-str定义
	    char* {0} = NULL;
	    char* {0}_str = NULL;
	    uint32_t {0}_len;'''

int_define = '''
        //{1}-int定义
        uint32_t {0}_data = 0;'''

str_free = '''
        //{0}_str  free
        hal_free({0}_str);'''

str_data_load = '''
        //{0}
        find = HAL_GetArrayArgsAsBytes(str_{0}, str_{0}_len, i, &{0}, &{0}_len);
        if (find != 0) {{
            HAL_SetErrCode({1});
            continue;
        }}
		{0}_str = hal_malloc({0}_len + 1);
		hal_memcpy({0}_str, {0}, {0}_len);
		{0}_str[{0}_len] = 0;
'''

int_data_load = '''
        //{0}
		find = HAL_GetArrayArgsAsUint32(str_{0}, str_{0}_len, i, &{0}_data);
		if (find != 0) {{
			HAL_SetErrCode({1});
			continue;
		}}
'''





if __name__ == '__main__':
    db_col_data_list = list_make(errcode=9001)
    pprint(db_col_data_list)

    # load data
    load_data_result = ''''''
    for item in db_col_data_list:
        if (item[2] == 'str'):
            load_data_result+=str_data_load.format(
                f'{item[0]}_{item[3]}',
                item[5],
            )
        elif (item[2] == 'int'):
            load_data_result += int_data_load.format(
                f'{item[0]}_{item[3]}',
                item[5],
            )

    print(load_data_result)

    #define
    define_result = ''''''
    for item in db_col_data_list:
        if(item[2] == 'str'):
            define_result += str_define.format(
                                    '{}_{}'.format(item[0], item[3]),
                                     item[1])
        elif (item[2] == 'int'):
            define_result += int_define.format(
                '{}_{}'.format(item[0], item[3]),
                item[1])
    #
    print('define'.center(100, '='))
    print(define_result)
    # #
    # #free
    # free_result = ''''''
    # for item in db_col_data_list:
    #     if (item[2] == 'str'):
    #         free_result += str_free.format('{}_{}'.format(item[0], item[3]))
    # print('free'.center(100,'='))
    # print(free_result)










