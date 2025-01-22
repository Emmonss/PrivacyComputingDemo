
import pandas as pd

insert_sql = '''
INSERT INTO `cqsw`.`swtest01`
(tax_pay_id, comp_name, dtbs, x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, x19, x20, x21, x22, x23, x24, x25, x26, x27, x28, x29, x30, x31, x32, x33, x34, x35, x36, x37, x38, x39, x40, x41, x42, x43, x44, x45, x46, x47, x48, x49, x50, x51, x52, x53, x54, x55, x56, x57, x58, x59, x60, x61, x62, x63, x64, x65, x66, x67, x68, x69, x70, x71, x72, x73, x74, x75, x76, x77, x78, x79, x80, x81, x82, x83, x84, x85, x86, x87, x88, x89, x90, x91, x92, x93, x94, x95, x96, x97, x98, x99, x100, x101, x102, x103, x104, x105, x106, x107, x108, x109, x110, x111, x112, x113, x114, x115, x116, x117, x118, x119, x120, x121, x122, x123, x124, x125, x126, x127, x128, x129, x130, x131, x132)
VALUES(${fuck});
'''

thres_sql = '''
INSERT INTO `test`.`cmb_data_party`
(id, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15, y16, y17, y18, y19, y20, y21, y22, y23, y24, y25)
VALUES(${fuck});
'''

date = '2025-01-07'
comp_name = 'test'
from pprint import pprint
import numpy as np


if __name__ == '__main__':
    thres = pd.read_csv('./csv/thres.csv').values.tolist()[0]
    data = pd.read_csv('./csv/测试全文.csv').values.tolist()


    thres_data = ''''''
    for item in thres:
        thres_data+=",{}".format(item)
    pprint(np.shape(data))
    fw = open('./sql/cqsw.sql', 'w', encoding='utf-8')
    fw2 = open('./sql/zhthres.txt', 'w', encoding='utf-8')
    for row in data:
        insert_data = ''' '{}','{}','{}' '''.format(row[0],comp_name,date)
        for item in row[1:]:
            insert_data+=',{}'.format(item)
        # print(f"insert_data:{insert_data}")
        insert_sqls = insert_sql.replace('${fuck}',insert_data)
        fw.write(insert_sqls)

        thres_datas = "'{}'{}".format(row[0],thres_data)
        thres_sqls = thres_sql.replace('${fuck}',thres_datas)
        fw2.write(thres_sqls)

    fw.close()
    fw2.close()
        # break


