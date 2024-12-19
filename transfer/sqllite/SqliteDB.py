import sqlite3


class DB:
    def __init__(self, db_path, table_name,create_table_sql):
        self.db_path = db_path
        self.table_name = table_name
        self.create_table_sql = create_table_sql
        self.conn = None
        self.cursor = None
        self.open = False

        self.select_all_sql = ''' select * from {};'''
    def create_table(self):
        # try:
        if not self.open:
            self.start()
        self.cursor.execute(self.create_table_sql)
        self.close()
        print(f"crete table success:{self.table_name}")
        return 1
        # except Exception as e:
        #     print(f"crete table error:{e}")

    def start(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.open = True
        except Exception as e:
            print(f"close conn error:{e}")



    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
            self.open = False
        except Exception as e:
            print(f"close conn error:{e}")


    def query_all(self):
        try:
            if not self.open:
                self.start()
            sql = self.select_all_sql.format(self.table_name)
            # print(sql)
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            self.close()
            return res
        except Exception as e:
            print(e)

if __name__ == '__main__':
    pass


