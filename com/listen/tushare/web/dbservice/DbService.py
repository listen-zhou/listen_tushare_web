# -*- coding: utf-8 -*-
import datetime
import pymysql
import configparser
import os
import traceback
import sys

class DbService(object):
    def __init__(self):
        # charset必须设置为utf8，而不能为utf-8
        config = configparser.ConfigParser()
        os.chdir('../config')
        config.read('database.cfg')
        mysql_section = config['mysql']
        print("mysql连接配置信息")
        print(mysql_section)
        if mysql_section:
            host = mysql_section['db.host']
            port = int(mysql_section['db.port'])
            username = mysql_section['db.username']
            password = mysql_section['db.password']
            dbname = mysql_section['db.dbname']
            charset = mysql_section['db.charset']
            self.conn = pymysql.connect(host=host, port=port, user=username, passwd=password, db=dbname, charset=charset)
            self.conn.autocommit(True)
            self.cursor = self.conn.cursor()
        else:
            raise FileNotFoundError('配置文件[database.cfg]mysql区块配置信息没有找到!!!')

    # 数据库连接关闭
    def close(self):
        if self.cursor:
            self.cursor.close()
            print('---> 关闭游标')
        if self.conn:
            self.conn.close()
            print('---> 关闭连接')

    def insert(self, upsert_sql):
        try:
            if upsert_sql:
                self.cursor.execute(upsert_sql)
                return True
            else:
                return False
        except Exception:
            print('error sql:', upsert_sql)
            traceback.print_exc()

    def check_exist_id(self, dict_data, table_name, list_unique_fields):
        check_sql = ""
        try:
            check_sql = "select id from " + table_name + " where "
            where_sql = ""
            for field_name in list_unique_fields:
                where_sql += field_name + " = " + dict_data[field_name] + " and "
            check_sql = check_sql + where_sql[0:len(where_sql) - 4]
            ids = self.query(check_sql)
            if ids is not None and len(ids) > 0:
                id = ids[0][0]
                return id
            return 0
        except Exception:
            print('error sql:', check_sql)
            traceback.print_exc()

    def upsert(self, dict_data, table_name, list_unique_fields):
        try:
            id = self.check_exist_id(dict_data, table_name, list_unique_fields)
            if id is not None and id > 0:
                # update
                sql = "update " + table_name + " set"
                for field_name in dict_data.keys():
                    sql += " " + field_name + " = {" + field_name + "},"
                sql = sql[0:len(sql) - 1]
                sql += " where id = " + str(id)
            else:
                # insert
                sql = "insert into " + table_name + " ("
                field_names_sql = ""
                field_values_sql = ""
                for field_name in dict_data.keys():
                    field_names_sql += " " + field_name + ","
                    field_values_sql += " {" + field_name + "},"
                field_names_sql = field_names_sql[0:len(field_names_sql) - 1]
                field_values_sql = field_values_sql[0:len(field_values_sql) - 1]
                sql += field_names_sql
                sql += ") values ("
                sql += field_values_sql + ")"
            sql = sql.format_map(dict_data)
            self.cursor.execute(sql)
        except Exception:
            print('error sql', sql)
            self.conn.rollback()
            traceback.print_exc()

    def upsert_many(self, list_dict_data, table_name, list_unique_fields):
        sql = ""
        try:
            for dict_data in list_dict_data:
                self.upsert(dict_data, table_name, list_unique_fields)
        except Exception:
            print('error sql', sql)
            self.conn.rollback()
            traceback.print_exc()


    def insert_many(self, upsert_sql_list):
        try:
            if upsert_sql_list:
                for upsert_sql in upsert_sql_list:
                    try:
                        self.cursor.execute(upsert_sql)
                    except Exception:
                        print('error sql:', upsert_sql)
                        self.conn.rollback()
                        traceback.print_exc()
                        return False
                return True
            return False
        except Exception:
            self.conn.rollback()
            traceback.print_exc()

    def query(self, query_sql):
        try:
            if query_sql:
                self.cursor.execute(query_sql)
                stock_tuple_tuple = self.cursor.fetchall()
                return stock_tuple_tuple
            else:
                return None
        except Exception:
            traceback.print_exc()
            print('sql error:', query_sql)
            return None

    def query_table(self, table_name, field_names, where_sql):
        sql = ""
        try:
            sql = "select "
            for name in field_names:
                sql += name + ","
            sql = sql[0:len(sql)-1]
            sql += " from " + table_name + " " + where_sql
            tuple_datas = self.query(sql)
            if tuple_datas is not None and len(tuple_datas) > 0:
                dict_list = []
                for i in range(len(tuple_datas)):
                    tuple_data = tuple_datas[i]
                    # print(tuple_data)
                    dict_data = {}
                    for j in range(len(field_names)):
                        dict_data[field_names[j]] = tuple_data[j]
                    dict_list.append(dict_data)
                return dict_list
            return None
        except Exception:
            traceback.print_exc()
            print('sql error:', sql)
            return None
