import datetime

from transfer.sqllite.SqliteDB import DB
from pprint import pprint


class DBDemo1(DB):
    def __init__(self, db_path, table_name):
        create_table_sql = '''
                          CREATE TABLE IF NOT EXISTS `{}`(
                              `id` INTEGER PRIMARY KEY,
                              `user` VARCHAR(100) NOT NULL,
                              `score` INTEGER UNSIGNED NOT NULL,
                              `update_time` TIMESTAMP
                          );
                      '''.format(table_name)

        super(DBDemo1,self).__init__(db_path, table_name, create_table_sql)

        self.insert_table_sql = '''
               INSERT INTO {} (id, user, score, update_time)
               VALUES
               (NULL, ?, ?, ?);
           '''.format(self.table_name)

        self.select_table_by_user_sql = '''
            SELECT * from {} WHERE user=(?);
        '''.format(table_name)

        self.delete_table_by_user_sql = '''
            DELETE from {} WHERE user=(?);
        '''.format(table_name)

    def insert_data(self,user,score):
        try:
            if not self.open:
                self.start()
            self.cursor.execute(self.insert_table_sql,
                                (user,score,datetime.datetime.now()))
            self.conn.commit()
            self.close()
            print(f"insert data success:{user},{score}")
            return 1
        except Exception as e:
            print(f"insert data error:{e}")

    def select_by_user(self,user):
        try:
            if not self.open:
                self.start()
            self.cursor.execute(self.select_table_by_user_sql,(user,))
            # print(sql)
            res = self.cursor.fetchall()
            self.close()
            return res
        except Exception as e:
            print(f"insert data error:{e}")

    def delete_by_user(self,user):
        try:
            if not self.open:
                self.start()
            self.cursor.execute(self.delete_table_by_user_sql,(user,))
            self.conn.commit()
            self.close()
            print(f"delete data success:{user}")
            return 1
            # print(sql)
            # res = self.cursor.fetchall()
            # self.close()
            return res
        except Exception as e:
            print(f"insert data error:{e}")


if __name__ == '__main__':
    db_path = './db/demo1.db'
    table_name = 'demo'


    db = DBDemo1(db_path=db_path, table_name=table_name)
    # db.create_table()
    # db.insert_data(user="user1",score='100')
    # db.insert_data(user="user2", score='200')
    #
    #select
    # res = db.query_all()
    # pprint(res)
    #

    # res = db.select_by_user(user="user2")
    # pprint(res)

    # delete
    # db.delete_by_user(user="user2")
    # res = db.select_by_user(user="user2")
    # pprint(res)

    #update







