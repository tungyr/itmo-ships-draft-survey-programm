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
    if args[0] == "a_mean":
        with connect('hydrostatic.sqlite') as conn:
            aft_dist = conn.execute(SQL_SELECT_DIST_BY_AFT_DRAFT, (args[1],))
            return aft_dist.fetchone()

    elif args[0] == "a_mean_rounded":
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




def aft_dist_find(a_mean) -> (tuple, int, int, tuple):
    if 1 < a_mean < 4.8:  # проверка на значение в начале таблицы и передача в
                            #  функцию интерполлирования aft_interp
        db_query = [(4.8, -1.84), (1, 4.82)]
        # return aft_interp(A_mean, table_result)
        return interpolation(db_query, a_mean, db_column=1)

    elif 7.05 <= a_mean <= 8.0:  # проверка на значение в конце таблицы и выдача результата сразу
        db_draught_dist = -2.4
        return db_draught_dist

    elif len(str(a_mean)) <= 3:  # проверка на значение без сотых и выборка результата без интерполирования
        return get_fm_db('a_mean', a_mean)[1]

    # значение с сотыми и обращение к базе и
    # последующая передача результата выборки в функцию интерполлирования interpolation
    # выборка двух значений отстояния кормовой осадки для интерполляции
    else:
        a_mean_rounded = round(a_mean + 0.05, 1)  # округление в большую сторону
        db_query = get_fm_db("a_mean_rounded", a_mean_rounded)
        # проверка на правильный диапазон данных для интерполяции для A_mean
        if db_query[0][0] < a_mean:
            a_mean_rounded += 0.05
            db_query = get_fm_db("a_mean_rounded", a_mean_rounded)
        return interpolation(db_query, a_mean, db_column=1)


def hydrostatic_find(momc, db_column):
    # подготовка входных данных для выборки из базы данных
    momc_round = float(str(momc)[:4])

    if momc_round < 2:
        momc_outbound = 2 + (2 - momc_round)

        table_result = []
        if momc_outbound * 100 % 2 == 0:
            table_result.append(get_fm_db("hydrostatic", 2.0))
            table_result.append(get_fm_db("hydrostatic", momc_outbound))
            # return hydrostatic_interp(table_result, MOMC, item)
            return interpolation(table_result, momc, db_column)
        else:
            momc_outbound -= 0.01
            momc_outbound = float('%.2f' % (momc_outbound))

            # выбираем ближайшее значение к momc_outbound из БД для интерполяции
            table_result_outbound = get_fm_db("hydrostatic_rounded", momc_outbound)

            # интерполируем значение momc_outbound к оригинальному и по нему находим истинный item
            item_interp_result = hydrostatic_interp(table_result=table_result_outbound, momc=momc_outbound + 0.01, item=db_column)

            # подготовка данных для расчета интерполированого значения item
            table_result.append(get_fm_db("hydrostatic", 2.0))

            # временный список для выборки данных из него функцией hydrostatic_interp
            temp_list = list(range(0, 8))
            temp_list[0], temp_list[db_column]= momc_outbound + 0.01, item_interp_result
            table_result.append(temp_list)
            return hydrostatic_interp(table_result, momc, db_column)

    elif momc_round > 7.8:
        momc_outbound = 7.8 - (momc_round - 7.8)
        momc_outbound = float('%.2f' % (momc_outbound))

        table_result = []
        if momc_outbound * 100 % 2 == 0:
            table_result.append(get_fm_db("hydrostatic", momc_outbound))
            table_result.append(get_fm_db("hydrostatic", 7.8))
            return hydrostatic_interp(table_result, momc, db_column)
        else:
            momc_outbound -= 0.01
            momc_outbound = float('%.2f' % (momc_outbound))

            # выбираем ближайшее значение к momc_outbound из БД для интерполяции
            table_result_outbound = get_fm_db("hydrostatic_rounded", momc_outbound)

            # интерполируем значение momc_outbound к оригинальному и по нему находим истинный item
            item_interp_result = hydrostatic_interp(table_result=table_result_outbound, momc=momc_outbound + 0.01, item=db_column)

            # подготовка данных для расчета интерполированого значения item
            # временный список для выборки данных из него функцией hydrostatic_interp
            temp_list = list(range(0, 8))
            temp_list[0], temp_list[db_column]= momc_outbound + 0.01, item_interp_result
            table_result.append(temp_list)
            table_result.append(get_fm_db("hydrostatic", 7.8))
            return hydrostatic_interp(table_result, momc, db_column)

    else:
        if momc * 100 % 2 == 0:
            table_result = get_fm_db("hydrostatic", momc)
            return table_result[db_column]
        else:
            momc_round -= 0.01
            momc_round = round(momc_round, 2)
            table_result = get_fm_db("hydrostatic_rounded", momc_round)
            return interpolation(table_result, momc, db_column)


 # функция интерполляции для гидростатических данных
def hydrostatic_interp(table_result, momc, item):
    first_pair, second_pair = table_result[0], table_result[1]
    draught_diff = momc - first_pair[0]   # вычитание полученной осадки и первоначальной
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

    print(hydrostatic_find(1.635, 2))
    # print(aft_dist_find(6.99))
    # print(aft_dist_find(6.3))
    # print(aft_dist_find(8))
    # print(aft_dist_find(5.55))



