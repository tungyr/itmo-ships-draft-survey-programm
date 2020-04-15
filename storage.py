#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path as Path
import sqlite3


SQL_SELECT_DIST_BY_AFT_DRAFT = 'SELECT * FROM AFT_DRAUGHT WHERE DRAUGHT<=?'
SQL_SELECT_HYDROSTATIC_BY_MOMC = 'SELECT * FROM HYDROSTATIC WHERE DRAUGHT>=?'


def connect(db_name=None):
    """Функция подключения к БД"""
    if db_name is None:
        db_name = ':memory:'

    conn = sqlite3.connect(db_name)
    return conn


def get_fm_db(*args) -> tuple:
    """Функция выборки соответствующих данных из БД"""

    # выборка данных кормового отстояния из БД по средней кормовой осадке
    if args[0] == "a_mean":
        with connect('hydrostatic.sqlite') as conn:
            aft_dist = conn.execute(SQL_SELECT_DIST_BY_AFT_DRAFT, (args[1],))
            return aft_dist.fetchone()

    elif args[0] == "a_mean_rounded":
        with connect('hydrostatic.sqlite') as conn:
            cursor = conn.execute(SQL_SELECT_DIST_BY_AFT_DRAFT, (args[1],))
            return cursor.fetchmany(2)

    # выборка гидростатических данных из БД по осадке
    elif args[0] == "hydrostatic":
        with connect('hydrostatic.sqlite') as conn:
            cursor = conn.execute(SQL_SELECT_HYDROSTATIC_BY_MOMC, (args[1],))
            return cursor.fetchone()

    elif args[0] == "hydrostatic_rounded":
        with connect('hydrostatic.sqlite') as conn:
            cursor = conn.execute(SQL_SELECT_HYDROSTATIC_BY_MOMC, (args[1],))
            return cursor.fetchmany(2)

def aft_dist_data(a_mean) -> (tuple, int, int, tuple):
    """Функция определения кормового отстояния по средней кормовой осадке"""

    # проверка на значение в начале таблицы и передача в функцию интерполлирования
    if 1 < a_mean < 4.8:
        db_query = [(4.8, -1.84), (1, 4.82)]
        return interpolation(db_query, a_mean, db_column=1)

    # проверка на значение в конце таблицы и выдача результата без интерполирования
    elif 7.05 <= a_mean <= 8.0:
        db_draught_dist = -2.4
        return db_draught_dist

    # проверка на значение кормовой осадки без сотых и выборка результата из БД без интерполирования
    elif len(str(a_mean)) <= 3:
        return get_fm_db('a_mean', a_mean)[1]

    # выборка двух значений отстояния кормовой осадки из БД и их интерполляция
    else:
        a_mean_rounded = round(a_mean + 0.05, 1)
        db_query = get_fm_db("a_mean_rounded", a_mean_rounded)
        # проверка на корректный диапазон данных для интерполяции для A_mean
        if db_query[0][0] < a_mean:
            a_mean_rounded += 0.05
            db_query = get_fm_db("a_mean_rounded", a_mean_rounded)
        return interpolation(db_query, a_mean, db_column=1)


def hydrostatic_data(momc, db_column) -> float:
    """Функция определения гидростатических данных"""

    # подготовка входных данных для выборки из базы данных
    if momc < 2:
        momc_outbound = 2 + (2 - momc)
        momc_round = float(str(momc_outbound)[:4])

        if momc_round * 100 % 2 != 0:
            momc_round = round(momc_round - 0.01, 2)

        # выбираем ближайшее значение к momc_outbound из БД для интерполяции
        table_result_outbound = get_fm_db("hydrostatic_rounded", momc_round)

        # интерполируем значение momc_outbound к оригинальному и по нему находим истинный item
        item_interp_result = interpolation(table_result_outbound, momc_outbound, db_column)

        # собираем данные в список и отправляем в функцию интерполирования
        temp_list = list(range(0, 8))
        table_result = []
        table_result.append(get_fm_db("hydrostatic", 2.0))
        temp_list[0], temp_list[db_column]= momc_outbound, item_interp_result
        table_result.append(temp_list)
        return interpolation(table_result, momc, db_column)

    elif momc > 7.8:
        momc_outbound = 7.8 - (momc - 7.8)
        momc_round = float(str(momc_outbound)[:4])

        if momc_round * 100 % 2 != 0:
            momc_round = momc_round - 0.01
            momc_round = float(str(momc_round)[:4])

        # выбираем ближайшее значение к momc_outbound из БД для интерполяции
        table_result_outbound = get_fm_db("hydrostatic_rounded", momc_round)

        # интерполируем значение momc_outbound к оригинальному и по нему находим истинный item
        item_interp_result = interpolation(table_result_outbound, momc_outbound, db_column)

        # собираем данные в список и отправляем в функцию интерполирования
        temp_list = list(range(0, 8))
        temp_list[0], temp_list[db_column]= momc_outbound, item_interp_result
        table_result = [temp_list,]
        table_result.append(get_fm_db("hydrostatic", 7.8))
        return interpolation(table_result, momc, db_column)

    else:
        momc_round = float(str(momc)[:4])
        if momc_round * 100 % 2 != 0:
            momc_round = round(momc_round - 0.01, 2)
        table_result = get_fm_db("hydrostatic_rounded", momc_round)
        return interpolation(table_result, momc, db_column)


def interpolation(db_data, draught_value, db_column) -> float:
    """Функция интерполирования кормового отстояния и гидростатических данных"""

    first_db_value, second_db_value = db_data[0], db_data[1]
    draught_entry_db_diff = draught_value - first_db_value[0]
    draughts_db_diff = second_db_value[0] - first_db_value[0]
    db_column_values_diff = second_db_value[db_column] - first_db_value[db_column]

    # определение кормового отстояния
    if db_column == 1:
        draught_dist = ((db_column_values_diff / draughts_db_diff) * draught_entry_db_diff + first_db_value[1])
        return draught_dist

    # определение гидростатических данных
    result = ((db_column_values_diff / draughts_db_diff) * draught_entry_db_diff + first_db_value[db_column])
    return result

if __name__ == "__main__":

    pass