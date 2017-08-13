# conding: utf-8
import calendar
import decimal
from decimal import Decimal
from decimal import getcontext
import copy

import datetime


class Utils():

    @staticmethod
    def format_log_message(list):
        if list is not None and len(list) > 0:
            length = len(list)
            i = 0
            message = ''
            while i < length:
                message += '{0[' + str(i) + ']} '
                i += 1
            message = message.format(list)
            return message
        else:
            return None

    @staticmethod
    def quotes_surround(str):
        if str is not None:
            return "'" + str + "'"
        return str

    @staticmethod
    def base_round(val, n):
        if val is not None:
            val = Decimal(val, getcontext())
            return val.__round__(n)
        return None
    @staticmethod
    def base_round_zero(val, n):
        if val is not None:
            val = Decimal(val, getcontext())
        else:
            val = Decimal(0, getcontext())
        return val.__round__(n)

    @staticmethod
    def division(divisor, dividend):
        if divisor is not None and dividend is not None and dividend != 0 and dividend != Decimal(0):
            return divisor / dividend
        return None

    @staticmethod
    def division_zero(divisor, dividend):
        if divisor is not None:
            if dividend is not None and dividend != 0 and dividend != Decimal(0):
                return divisor / dividend
        return Decimal(0)

    @staticmethod
    def sum(list):
        if list is not None and len(list) > 0:
            total = Decimal(0)
            for item in list:
                if item is not None:
                    total += item
            return total
        return None

    @staticmethod
    def sum_zero(list):
        if list is not None and len(list) > 0:
            total = Decimal(0)
            for item in list:
                if item is not None:
                    total += item
            return total
        return Decimal(0)

    @staticmethod
    def average(list):
        if list is not None and len(list) > 0:
            total = Utils.sum(list)
            if total is not None:
                average = total / Decimal(len(list))
                return average
        return None

    @staticmethod
    def average_zero(list):
        if list is not None and len(list) > 0:
            total = Utils.sum(list)
            if total is not None:
                average = total / Decimal(len(list))
                return average
        return Decimal(0)

    @staticmethod
    def deepcopy_list(list):
        return copy.deepcopy(list)

    @staticmethod
    def get_week_day_num(the_date):
        if the_date is not None:
            year = the_date.year
            month = the_date.month
            day = the_date.day
            return calendar.weekday(year, month, day) + 1

    @staticmethod
    def get_amount_flow_css(price_avg_chg):
        if price_avg_chg is not None:
            if price_avg_chg >= 0:
                return 'm0'
            else:
                return 'l0'
        else:
            return ''

    @staticmethod
    def get_amount_flow_arrow(val, price_avg_chg):
        if val is not None and price_avg_chg is not None:
            if price_avg_chg > 0:
                if val > 100 and val < 150:
                    return '../static/img/stop2.gif'
                elif val >= 150 and val < 200:
                    return '../static/img/up2.gif'
                elif val >= 200:
                    return '../static/img/up1.gif'
                elif val == 100:
                    return ''
                elif val < 70 and val > 50:
                    return '../static/img/down4.gif'
                elif val <= 50 and val > 0:
                    return '../static/img/down3.gif'
                else:
                    return ''
            elif price_avg_chg < 0:
                if val > 100 and val < 150:
                    return '../static/img/stop3.gif'
                elif val >= 150 and val < 200:
                    return '../static/img/up4.gif'
                elif val >= 200:
                    return '../static/img/up3.gif'
                elif val == 100:
                    return ''
                elif val < 70 and val > 50:
                    return '../static/img/down2.gif'
                elif val <= 50 and val > 0:
                    return '../static/img/down1.gif'
                else:
                    return ''
            else:
                return ''

    @staticmethod
    def get_diff_arrow(val):
        if val is None or val == '':
            return ''
        if val > 0:
            return '../static/img/up2.gif'
        elif val < 0:
            return '../static/img/down2.gif'
        else:
            return '../static/img/stop2.gif'

    @staticmethod
    def get_css(val):
        if val is None or val == '':
            return ''
        elif val >= 3:
            return 'm3'
        elif val >= 2:
            return 'm2'
        elif val >= 1:
            return 'm1'
        elif val > 0:
            return 'm0'
        elif val <= -3:
            return 'l3'
        elif val <= -2:
            return 'l2'
        elif val <= -1:
            return 'l1'
        elif val < 0:
            return 'l0'
        else:
            return ''

    @staticmethod
    def json_default(val):
        if isinstance(val, datetime.date):
            return val.strftime('%Y-%m-%d')
        return val

    @staticmethod
    def format_mm_dd(val):
        if val is not None and isinstance(val, datetime.date):
            return val.strftime('%m-%d')
        return val

    @staticmethod
    def tuple_to_dict(tuple_data, list_keys):
        if tuple_data is not None and list_keys is not None and len(tuple_data) == len(list_keys):
            result = {}
            i = 0
            for key in list_keys:
                result[key] = tuple_data[i]
                i += 1
            return result
        else:
            return None

    @staticmethod
    def tuples_to_dicts(tuple_datas, list_keys):
        if tuple_datas is not None and len(tuple_datas) > 0 and list_keys is not None:
            result = []
            for tuple_data in tuple_datas:
                dict_data = Utils.tuple_to_dict(tuple_data, list_keys)
                if dict_data is not None:
                    result.append(dict_data)
            return result
        else:
            return None

    @staticmethod
    def format_yyyy_mm_dd(val):
        if val is not None:
            return val.strftime('%Y-%m-%d')
        return val

    @staticmethod
    def format_week_day(val):
        if isinstance(val, datetime.date) or isinstance(val, datetime.datetime):
            return val.weekday() + 1
        return val

    @staticmethod
    def append_week_day(result):
        if result is not None and len(result) > 0:
            for i in range(len(result)):
                result[i]['week_day'] = Utils.format_week_day(result[i]['the_date'])
        return result

    @staticmethod
    def str_to_decimal(str, n):
        return Utils.base_round(Decimal(str), n)

    @staticmethod
    def get_diff_days(the_date1, the_date2):
        if the_date1 is None or the_date2 is None:
            return 0
        else:
            if (isinstance(the_date1, datetime.date) or isinstance(the_date1, datetime.datetime)) \
                    and (isinstance(the_date2, datetime.date) or isinstance(the_date2, datetime.datetime)):
                the_date1 = datetime.datetime.now().replace(the_date1.year, the_date1.month, the_date1.day, 0, 0, 0, 0)
                the_date2 = datetime.datetime.now().replace(the_date2.year, the_date2.month, the_date2.day, 0, 0, 0, 0)
                diff_days = the_date2 - the_date1
                return diff_days.days
            else:
                return 0

    @staticmethod
    def get_day_kline_list_keys():
        list_keys = ['the_date', 'week_day',
                     'close', 'close_chg', 'close_open_chg',
                     'open', 'open_chg', 'high', 'high_chg', 'low', 'low_chg',
                     'amount', 'amount_chg', 'vol', 'vol_chg',
                     'price_avg_1', 'price_avg_1_chg', 'price_avg_1_chg_diff', 'close_price_avg_1_chg',
                     'price_avg_3', 'price_avg_3_chg', 'price_avg_3_chg_diff', 'close_price_avg_3_chg',
                     'price_avg_5', 'price_avg_5_chg', 'price_avg_5_chg_diff', 'close_price_avg_5_chg',
                     'price_avg_10', 'price_avg_10_chg', 'price_avg_10_chg_diff', 'close_price_avg_10_chg'
                     ]
        return list_keys