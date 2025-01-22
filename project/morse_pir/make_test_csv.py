from faker import Faker
import pandas as pd
import random

faker = Faker(locale='zh_CN')
def make_csv_20250110(length = 10):
    result = dict()
    # col = ['id', 'edu', 'work_exp','work_loc','rigist_year','wealth']


    work_item = ['北京','上海','南京','杭州','深圳','广州','成都','武汉']
    edu_item = ['其他','小学','初中','高中','大学','大专','硕士','博士','博士后']
    gen = ['男','女']
    id_list = []
    name_list = []
    edu_list= []
    work_exp_list = []
    work_loc_list = []
    rigist_year_list = []
    wealth_list = []
    gender_list = []
    query_list = []


    for i in range(length):
        id_list.append(f"id_{faker.ean8()}")
        name_list.append(faker.name())
        edu_list.append(edu_item[random.randint(0,len(edu_item)-1)])
        work_exp_list.append(random.randint(0,30))
        work_loc_list.append(work_item[random.randint(0,len(work_item)-1)])
        rigist_year_list.append(random.randint(1990,2024))
        wealth_list.append(random.randint(1,1000)*10000)
        gender_list.append(gen[random.randint(0,1)])
        query_list.append(faker.phone_number())

    result['id'] = id_list
    result['name'] = name_list
    result['edu'] = edu_list
    result['work_exp'] = work_exp_list
    result['work_loc'] = work_loc_list
    result['rigist_year'] = rigist_year_list
    result['wealth'] = wealth_list
    result['gender'] = gender_list
    result['query'] = query_list
    res_pd = pd.DataFrame(result)

    res_pd.to_csv('./csv_result/20250110.csv',header=True,index=False)
    # print(res_pd)
    print("done!")



if __name__ == '__main__':
    make_csv_20250110(length=10000)
    # name_set = set()
    # fw = open('shen.txt','w',encoding='utf-8')
    # for i in range(100000):
    #     name = faker.name()
    #     if name.startswith("沈") and name not in name_set:
    #         name_set.add(name)
    #         print(name)
    #         fw.write(f"{name}\n")
    # fw.close()
    pass