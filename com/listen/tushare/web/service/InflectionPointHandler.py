# coding: utf-8
from datetime import datetime

from tornado.web import RequestHandler
import simplejson
from com.listen.tushare.web.dbservice.DbService import DbService
from com.listen.tushare.web.utils.Utils import Utils

class InflectionPointHandler(RequestHandler):
    dbService = DbService()
    table_tushare_stock_base_info = "tushare_stock_base_info"
    table_base_field_names = ['security_code', 'security_name']
    table_tushare_stock_hist_data = 'tushare_stock_hist_data'
    table_field_names = ['security_code', 'the_date', 'open', 'low', 'high', 'close', 'volume', 'amount',
                         'close_change', 'close_change_percent', 'high_change', 'high_change_percent',
                         'low_change', 'low_change_percent', 'amount_change', 'amount_change_percent',
                         'volume_change', 'volume_change_percent',
                         'price_average_1', 'price_average_change_1', 'price_average_change_percent_1',
                         'price_average_3', 'price_average_change_3', 'price_average_change_percent_3',
                         'price_average_5', 'price_average_change_5', 'price_average_change_percent_5',
                         'price_average_10', 'price_average_change_10', 'price_average_change_percent_10',
                         'week_day', 'close_change_diff', 'high_change_diff', 'low_change_diff',
                         'amount_change_diff', 'volume_change_diff', 'price_average_change_diff_1',
                         'price_average_change_diff_3', 'price_average_change_diff_5', 'price_average_change_diff_10']

    def post(self):
        security_code = self.get_argument('security_code', None)
        size = self.get_argument('size', 50)
        if security_code is not None:
            where_sql = "where security_code = {security_code} order by the_date desc limit {limit_size}"
            where_sql = where_sql.format(security_code=Utils.quotes_surround(security_code),
                                         limit_size=size)
            result = self.dbService.query_table(self.table_tushare_stock_hist_data, self.table_field_names, where_sql)
            # print('result', result)
            if result is None or len(result) == 0:
                self.write('[]')
            else:
                result = {"rows": result}
                result_json = simplejson.dumps(result, default=Utils.json_default)
                # print('get_stock_day_kline result: ', result_json)
                self.write(result_json)
        else:
            self.write('[]')

    def get(self):
        result = self.dbService.query_table(self.table_tushare_stock_base_info, self.table_base_field_names, "")
        result = {'rows': result}
        result_json = simplejson.dumps(result, default=Utils.json_default)
        # print('get_all_stock_info result: ', result_json)
        self.write(result_json)