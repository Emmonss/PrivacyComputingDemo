def list_make( sz_num = 2,  yh_num = 2, errcode = 9001):
    db_col_data_list = []
    # (head, 注释, type, 字段名, 数据平台映射名, errcode)
    db_col_data_list.append(('sz', '税局测试key', 'str', 'xid', 'xid', str(errcode)))
    for i in range(sz_num):
        errcode += 1
        db_col_data_list.append(
            ('sz', '税局测试字段x{}'.format(i),
             'int', 'x{}'.format(i), 'x{}'.format(i),
             str(errcode)))

    errcode += 1
    db_col_data_list.append(('yh', '银行测试key', 'str', 'yid', 'yid', str(errcode)))
    for i in range(1,yh_num+1):
        errcode += 1
        db_col_data_list.append(
            ('yh', '银行测试字段y{}'.format(i),
             'int', 'y{}'.format(i), 'y{}'.format(i),
             str(errcode)))

    return db_col_data_list