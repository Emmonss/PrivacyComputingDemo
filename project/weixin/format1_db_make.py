
from pprint import  pprint
from format1_utils import list_make

load_db_col_data  ='''
    // 获取{0}
	char *str_{1} = NULL;
	uint32_t str_{1}_len = 0;
	ret = HAL_GetArgsAt("{2}", {4}, &str_{1}, &str_{1}_len, 0);
	if (ret != 0) {{
		HAL_SetErrCode({3});
		return;
	}}
'''

count_col_data = '''
    //计算数量:{2}
    uint32_t {0}_count = (int) (hal_ReadLittleEndianInt32((void*) (str_{1})));
'''


if __name__ == '__main__':
    #(head, 注释, type, 字段名, 数据平台映射名, errcode)
    db_col_data_list = list_make(errcode=8001)
    pprint(db_col_data_list)
    result = ""
    for item in db_col_data_list:
        result += load_db_col_data.format(item[1],
                                          f'{item[0]}_{item[3]}',
                                          f'{item[0]}_{item[4]}',
                                          item[5],
                                          len(f'{item[0]}_{item[3]}')
                                          )

    for item in db_col_data_list:
        if item[1] == '税局测试key' or item[1] == '银行测试key':
            result+=count_col_data.format(item[0],f'{item[0]}_{item[3]}',item[1])

    print(result)

