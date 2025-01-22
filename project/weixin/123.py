
import pandas as pd

data = [{"sz_id":"shxy_code911","res1":2,"res2":-5,"res3":-6,"res4":-1.333333504},{"sz_id":"shxy_code910","res1":2,"res2":-5,"res3":-6,"res4":-1.333333504},{"sz_id":"shxy_code9","res1":2,"res2":-5,"res3":-6,"res4":-1.333333504},{"sz_id":"shxy_code8","res1":2,"res2":-5,"res3":-6,"res4":-1.333333504},{"sz_id":"shxy_code7","res1":2,"res2":-5,"res3":-6,"res4":-1.333333504},{"sz_id":"shxy_code6","res1":2,"res2":-5,"res3":-6,"res4":-1.333333504},{"sz_id":"shxy_code5","res1":2,"res2":-5,"res3":-6,"res4":-1.333333504},{"sz_id":"shxy_code4","res1":2,"res2":-5,"res3":-6,"res4":-1.333333504},{"sz_id":"shxy_code3","res1":2,"res2":-5,"res3":-6,"res4":-1.333333504},{"sz_id":"shxy_code2","res1":2,"res2":-5,"res3":-6,"res4":-1.333333504}]
sorted_data = sorted(data, key=lambda x: x["sz_id"],reverse=False)
if __name__ == '__main__':
    from pprint import pprint
    ppp = pd.DataFrame(sorted_data)
    print(ppp)
    ppp.to_csv('./csv/241230_01.csv',encoding='utf-8',index=False)
