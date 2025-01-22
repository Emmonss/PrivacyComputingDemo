psql  ='''
set tee.sz_ida.sz_data_party.primary = id;
set tee.sz_ida.sz_data_party.packagesize = 500;
set tee.bank_ida.cmb_data_party.primary = id;
set tee.bank_ida.cmb_data_party.packagesize = 500;

SELECT
  /*+ FUNC(TEE)*/
  $(FUC_NAME) (
    sz_xid = sz_ida.sz_data_party.id,
    $(SZ_DATA)
    yh_yid = bank_ida.cmb_data_party.id,
    $(YH_DATA)
  )
FROM
  sz_ida.sz_data_party,
  bank_ida.cmb_data_party
WHERE
  sz_ida.sz_data_party.id = bank_ida.cmb_data_party.id
'''

sz_data_item = '''sz_{0} = sz_ida.sz_data_party.{0},
    '''

yh_data_item = '''yh_{0} = bank_ida.cmb_data_party.{0},
    '''


from project.weixin.format1_main import list_make
from pprint import pprint
if __name__ == '__main__':
    sz_num = 136
    yh_num = 25
    db_col_data_list = list_make( sz_num = sz_num,yh_num = yh_num,errcode=9001)
    # pprint(db_col_data_list)
    FUCNAME = "CMBTEST241220"

    sz_item = ''''''
    yh_item = ''''''
    for item in db_col_data_list:
        if not (item[1] == '税局测试key' or item[1] == '银行测试key'):
            if(item[0]=='sz'):
                sz_item+=sz_data_item.format(item[3])
            elif(item[0]=='yh'):
                yh_item += yh_data_item.format(item[3])

    # print(sz_item)
    # print(yh_item)

    result = psql.replace("$(FUC_NAME)", FUCNAME) \
        .replace("$(SZ_DATA)", sz_item[:-5]) \
        .replace("$(YH_DATA)", yh_item[:-6])
    print(result)