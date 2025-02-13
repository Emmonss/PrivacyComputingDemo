
import mysql.connector
from mysql.connector import Error


class MySQLConn:
    def __init__(self,conn_dict):
        try:
            self.conn = mysql.connector.connect(
                host=conn_dict.host,
                database=conn_dict.database,
                user=conn_dict.user,
                password=conn_dict.password
            )
            self.cursor = self.conn.cursor()
            print("成功连接到数据库")
        except Error as e:
            print(f"Error: {e}")
            self.conn = None
            self.cursor = None


    def commit(self,sql):
        if self.conn is None or not self.conn.is_connected():
            print("游标初始化失败 请先初始化游标")
        try:
            # 执行 SQL 查询
            self.cursor.execute(sql)
            # 获取查询结果
            results = self.cursor.fetchall()

            return results
        except Error as e:
            print(f"Error: {e}")
            return None

    def close(self):
        if self.conn is not None and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
            print("数据库连接已关闭")

    def reconn(self,conn_dict):
        try:
            self.conn = mysql.connector.connect(
                host=conn_dict.host,
                database=conn_dict.database,
                user=conn_dict.user,
                password=conn_dict.password
            )
            self.cursor = self.conn.cursor()
            print("成功连接到数据库")
        except Error as e:
            print(f"Error: {e}")
            self.conn = None
            self.cursor = None



if __name__ == '__main__':
    conn_dict = {
        "host" : '121.5.153.102',
        "database" : 'test',
        "user" : 'root',
        "password" : 'pzmabc123'
    }
    conn_dict = DictToObject(conn_dict)
    sql = "select * from test.transfer_data"
    sql_conn = MySQLConn(conn_dict)
    results = sql_conn.commit(sql)
    for row in results:
        print(row)

    sql_conn.close()
    sql_conn.reconn(conn_dict)
    results = sql_conn.commit(sql)
    for row in results:
        print(row)

    # print(conn_dict.host)
    # connect_and_execute(conn_dict)









