#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path as Path
import sqlite3


SQL_SELECT_DIST_BY_AFT_DRAFT = 'SELECT * FROM AFT_DRAUGHT WHERE DRAUGHT<=?'
SQL_SELECT_HYDROSTATIC_BY_MOMC = 'SELECT * FROM HYDROSTATIC WHERE DRAUGHT>=?'


#  подключение к БД
def connect(db_name=None):
    if db_name is None:
        db_name = ':memory:'

    conn = sqlite3.connect(db_name)
    return conn


def get_fm_db(*args):
    if args[0] == "A_mean":
        with connect('hydrostatic.sqlite') as conn:
            aft_dist = conn.execute(SQL_SELECT_DIST_BY_AFT_DRAFT, (args[1],))
            return aft_dist.fetchone()

    elif args[0] == "A_mean_rounded":
        with connect('hydrostatic.sqlite') as conn:
            cursor = conn.execute(SQL_SELECT_DIST_BY_AFT_DRAFT, (args[1],))
            return cursor.fetchmany(2)

    elif args[0] == "hydrostatic":
        # выборка из БД по округленной осадке
        with connect('hydrostatic.sqlite') as conn:
            cursor = conn.execute(SQL_SELECT_HYDROSTATIC_BY_MOMC, (args[1],))
            return cursor.fetchone()

    elif args[0] == "hydrostatic_rounded":
        # выборка из БД по округленной осадке
        with connect('hydrostatic.sqlite') as conn:
            cursor = conn.execute(SQL_SELECT_HYDROSTATIC_BY_MOMC, (args[1],))
            return cursor.fetchmany(2)




def aft_dist_find(A_mean) -> (tuple, int, int, tuple):
    if 1 < A_mean < 4.8:  # проверка на значение в начале таблицы и передача в
                            #  функцию интерполлирования aft_interp
        db_query = [(4.8, -1.84), (1, 4.82)]
        # return aft_interp(A_mean, table_result)
        return interpolation(db_query, A_mean, db_column=1)

    elif 7.05 <= A_mean <= 8.0:  # проверка на значение в конце таблицы и выдача результата сразу
        db_draught_dist = -2.4
        return db_draught_dist

    elif len(str(A_mean)) <= 3:  # проверка на значение без сотых и выборка результата без интерполирования
        return get_fm_db('A_mean', A_mean)[1]

    else:  ''' значение с сотыми и обращение к базе и
           последующая передача результата выборки в функцию интерполлирования interpolation
           выборка двух значений отстояния кормовой осадки для интерполляции'''
        A_mean_rounded = round(A_mean + 0.05, 1)  # округление в большую сторону
        db_query = get_fm_db("A_mean_rounded", A_mean_rounded)
        # проверка на правильный диапазон данных для интерполяции для A_mean
        if db_query[0][0] < A_mean:
            A_mean_rounded += 0.05
            db_query = get_fm_db("A_mean_rounded", A_mean_rounded)
        return interpolation(db_query, A_mean, db_column=1)



# def aft_interp(A_mean, table_result):
#         first_pair, second_pair = table_result[0], table_result[1]
#         A_mean_diff = first_pair[0] - A_mean  # вычитание полученной осадки и первоначальной
#         draught_diff = first_pair[0] - second_pair[0]  # разница осадок
#         draught_dist_diff = first_pair[1] - second_pair[1]  # разница draught_dist по выбранным осадкам
#         if second_pair[1] != 4.82:  # проверка на значение из начала таблицы с положительными draught_dist
#             draught_dist = ((draught_dist_diff / draught_diff) * A_mean_diff - first_pair[1]) * (-1)
#         else:
#             draught_dist = ((draught_dist_diff / draught_diff) * A_mean_diff - first_pair[1]) * (-1)
#         return draught_dist


def hydrostatic_find(MOMC, item):
    # подготовка входных данных для выборки из базы данных
    MOMC_round = float(str(MOMC)[:4])

    if MOMC_round < 2:
        MOMC_outbound = 2 + (2 - MOMC_round)

        table_result = []
        if MOMC_outbound * 100 % 2 == 0:
            table_result.append(get_fm_db("hydrostatic", 2.0))
            table_result.append(get_fm_db("hydrostatic", MOMC_outbound))
            return hydrostatic_interp(table_result, MOMC, item)
        else:
            MOMC_outbound -= 0.01
            MOMC_outbound = float('%.2f' % (MOMC_outbound))
            # выбираем ближайшее значение к MOMC_outbound из БД для интерполяции
            table_result_outbound = get_fm_db("hydrostatic_rounded", MOMC_outbound)
            # интерполируем значение MOMC_outbound к оригинальному и по нему находим истинный item
            item_interp_result = hydrostatic_interp(table_result=table_result_outbound, MOMC=MOMC_outbound + 0.01, item=item)
            # подготовка данных для расчета интерполированого значения item
            table_result.append(get_fm_db("hydrostatic", 2.0))
            # временный список для выборки данных из него функцией hydrostatic_interp
            temp_list = list(range(0, 8))
            temp_list[0], temp_list[item]= MOMC_outbound + 0.01, item_interp_result
            table_result.append(temp_list)
            return hydrostatic_interp(table_result, MOMC, item)

    elif MOMC_round > 7.8:
        MOMC_outbound = 7.8 - (MOMC_round - 7.8)
        MOMC_outbound = float('%.2f' % (MOMC_outbound))

        table_result = []
        if MOMC_outbound * 100 % 2 == 0:
            table_result.append(get_fm_db("hydrostatic", MOMC_outbound))
            table_result.append(get_fm_db("hydrostatic", 7.8))
            return hydrostatic_interp(table_result, MOMC, item)
        else:
            MOMC_outbound -= 0.01
            MOMC_outbound = float('%.2f' % (MOMC_outbound))
            # выбираем ближайшее значение к MOMC_outbound из БД для интерполяции
            table_result_outbound = get_fm_db("hydrostatic_rounded", MOMC_outbound)
            # интерполируем значение MOMC_outbound к оригинальному и по нему находим истинный item
            item_interp_result = hydrostatic_interp(table_result=table_result_outbound, MOMC=MOMC_outbound + 0.01, item=item)
            # подготовка данных для расчета интерполированого значения item
            # временный список для выборки данных из него функцией hydrostatic_interp
            temp_list = list(range(0, 8))
            temp_list[0], temp_list[item]= MOMC_outbound + 0.01, item_interp_result
            table_result.append(temp_list)
            table_result.append(get_fm_db("hydrostatic", 7.8))
            return hydrostatic_interp(table_result, MOMC, item)

    else:
        if MOMC * 100 % 2 == 0:
            table_result = get_fm_db("hydrostatic", MOMC)
            return table_result[item]
        else:
            MOMC_round -= 0.01
            MOMC_round = round(MOMC_round, 2)
            table_result = get_fm_db("hydrostatic_rounded", MOMC_round)
            return interpolation(table_result, MOMC, item)


#  функция интерполляции для гидростатических данных
def hydrostatic_interp(table_result, MOMC, item):
    first_pair, second_pair = table_result[0], table_result[1]
    draught_diff = MOMC - first_pair[0]   # вычитание полученной осадки и первоначальной
    draught_table_diff = second_pair[0] - first_pair[0]   # разница осадок
    item_table_diff = second_pair[item] - first_pair[item]  # разница draught_dist по выбранным осадкам
    item_result = ((item_table_diff / draught_table_diff) * draught_diff + first_pair[item])
    return item_result

def interpolation(db_data, draught_value, db_column):
    first_db_value, second_db_value = db_data[0], db_data[1]
    draught_entry_db_diff = draught_value - first_db_value[0]
    draughts_db_diff = second_db_value[0] - first_db_value[0]
    db_column_values_diff = second_db_value[db_column] - first_db_value[db_column]
    if db_column == 1:
        # проверка на значение из начала таблицы с положительными draught_dist
        draught_dist = ((db_column_values_diff / draughts_db_diff) * draught_entry_db_diff + first_db_value[1])
        return draught_dist
    db_column_values_diff = second_db_value[db_column] - first_db_value[db_column]
    result = ((db_column_values_diff / draughts_db_diff) * draught_entry_db_diff + first_db_value[db_column])
    return result

if __name__ == "__main__":

    # print(hydrostatic_find(2.01, 4))
    print(aft_dist_find(6.99))
    # print(aft_dist_find(6.3))
    # print(aft_dist_find(8))
    # print(aft_dist_find(5.55))

# a = 4 - 1.651
# 2.349 -109.70
# 109.70 - 106.77 =2.93
# 2.93/0.35 = 8.371
# 106.77-2,93=103,84
# data_prev = None
# i = 7.8
# while i > 2.0:
#     data_new = get_fm_db('hydrostatic', i)
#     if data_prev == None:
#         data_prev = data_new
#     result = data_prev[4] - data_new[4]
#     data_prev = data_new
#     i -= 0.02
#     i = float('%.2f' %(i))
#
#     print(f'i : {i} --- diff : {result:.2f}')


