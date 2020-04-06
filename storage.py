#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path as Path
import sqlite3



SQL_SELECT_DIST_BY_AFT_DRAFT = 'SELECT DRAUGHT_DIST FROM AFT_DRAUGHT WHERE DRAUGHT=?'
SQL_SELECT_DIST_BY_AFT_DRAFT_INTERP = 'SELECT DRAUGHT, DRAUGHT_DIST FROM AFT_DRAUGHT WHERE DRAUGHT<=?'
SQL_SELECT_HYDROSTATIC_BY_MOMC = 'SELECT * FROM HYDROSTATIC WHERE DRAUGHT=?'
SQL_SELECT_HYDROSTATIC_BY_MOMC_INTERP = 'SELECT * FROM HYDROSTATIC WHERE DRAUGHT>=?'


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
            cursor = conn.execute(SQL_SELECT_DIST_BY_AFT_DRAFT_INTERP, (args[1],))
            return cursor.fetchmany(2)

    elif args[0] == "hydrostatic":
        # выборка из БД по округленной осадке
        with connect('hydrostatic.sqlite') as conn:
            cursor = conn.execute(SQL_SELECT_HYDROSTATIC_BY_MOMC, (args[1],))
            return cursor.fetchone()

    elif args[0] == "hydrostatic_rounded":
        # выборка из БД по округленной осадке
        with connect('hydrostatic.sqlite') as conn:
            cursor = conn.execute(SQL_SELECT_HYDROSTATIC_BY_MOMC_INTERP, (args[1],))
            return cursor.fetchmany(2)

# выборка двух значений отстояния кормовой осадки для интерполляции
# def get_aft_dist_interp(A_mean):
#         A_mean_rounded = round(A_mean + 0.05, 1)  # округление в большую сторону
#         return get_fm_db(["A_mean_rounded", A_mean_rounded])



def get_hydrostatic(conn, MOMC):
        with conn:  # выборка из БД по округленной осадке
                cursor = conn.execute(SQL_SELECT_HYDROSTATIC_BY_MOMC, (MOMC,))
                return cursor.fetchmany(2)



# выборка двух значений гидростатических данных для интерполляции
def get_hydrostatic_interp(conn, MOMC):
    with conn:
        MOMC_rounded = MOMC - 0.01
        with conn:
            cursor = conn.execute(SQL_SELECT_HYDROSTATIC_BY_MOMC_INTERP, (round(MOMC_rounded, 4),))
            return cursor.fetchmany(2)



def aft_dist_find(A_mean) -> (tuple, int, int, tuple):
    if 1 < A_mean < 4.8:  # проверка на значение в начале таблицы и передача в
                            #  функцию интерполлирования aft_interp
        table_result = [(4.8, -1.84), (1, 4.82)]
        return aft_interp(A_mean, table_result)

    elif 7.05 <= A_mean <= 8.0:  # проверка на значение в конце таблицы и выдача результата сразу
        dist_draught = -2.4
        return dist_draught

    elif len(str(A_mean)) <= 3:  # проверка на значение без сотых и выборка результата без интерполирования
        return get_fm_db('A_mean', A_mean)

    else:  # значение с сотыми и обращение к базе и
           # последующая передача результата выборки в функцию интерполлирования aft_interp
           # выборка двух значений отстояния кормовой осадки для интерполляции
        A_mean_rounded = round(A_mean + 0.05, 1)  # округление в большую сторону
        table_result = get_fm_db("A_mean_rounded", A_mean_rounded)
        print(table_result)
        return aft_interp(A_mean, table_result)





# def aft_dist_find(conn, A_mean):
#     if 1 < A_mean < 4.8:  # проверка на значение в начале таблицы и передача в
#                             #  функцию интерполлирования aft_interp
#         table_result = [(4.8, -1.84), (1, 4.82)]
#         return aft_interp(A_mean, table_result)
#     elif 7.05 <= A_mean <= 8.0:  # проверка на значение в конце таблицы и выдача результата сразу
#         dist_draught = -2.4
#         return dist_draught
#     elif len(str(A_mean)) <= 3:  # проверка на значение без сотых и выборка результата сразу
#         with conn:
#             aft_dist = conn.execute(SQL_SELECT_DIST_BY_AFT_DRAFT, (A_mean,))
#             return aft_dist.fetchone()
#
#     else:  # значение с сотыми и обращение к базе через функцию get_aft_dist_interp и
#            # последующая передача результата выборки в функцию интерполлирования aft_interp
#         table_result = get_aft_dist_interp(conn, A_mean)
#         return aft_interp(A_mean, table_result)


def aft_interp(A_mean, table_result):
        first_pair = table_result[0]  # значение
        second_pair = table_result[1]
        A_mean_diff = first_pair[0] - A_mean  # вычитание полученной осадки и первоначальной
        draught_diff = first_pair[0] - second_pair[0]  # разница осадок
        draught_dist_diff = first_pair[1] - second_pair[1]  # разница draught_dist по выбранным осадкам
        if second_pair[1] != 4.82:  # проверка на значение из начала таблицы с положительными draught_dist
            draught_dist = ((draught_dist_diff / draught_diff) * A_mean_diff - first_pair[1]) * (-1)
        else:
            draught_dist = ((draught_dist_diff / draught_diff) * A_mean_diff - first_pair[1]) * (-1)
        return draught_dist


def hydrostatic_find(MOMC, item):
    # проверка необходимости интерполляции гидростатических данных
    # выборка одного прямого значения гидростатических данных без интерполяции
    # MOMC_round = round(MOMC - 0.005, 2)
    MOMC_round = float(str(MOMC)[:4])

    if MOMC_round < 2:
        MOMC_outbound = 2.0 + (2.0 - MOMC_round)

        MOMC_round = MOMC_outbound

        table_result = []
        if MOMC_round * 100 % 2 == 0:
            table_result.append(get_fm_db("hydrostatic", 2.0))
            table_result.append(get_fm_db("hydrostatic", MOMC_round))
            return hydrostatic_interp(table_result, MOMC, item)
        else:
            # TODO: check values like 2,9
            MOMC_round -= 0.01
            table_result.append(get_fm_db("hydrostatic", 2.0))
            table_result.append(get_fm_db("hydrostatic", MOMC_round))
            return hydrostatic_interp(table_result, MOMC, item)

    if MOMC_round * 100 % 2 == 0:
        table_result = get_fm_db("hydrostatic", MOMC_round)
        return table_result[item]
    else:
        # TODO: check values like 2,9
        MOMC_round -= 0.01
        table_result = get_fm_db("hydrostatic_rounded", MOMC_round)
        return hydrostatic_interp(table_result, MOMC, item)


    #
    # MOMC_outbound = round(2.0 + (2.0 - MOMC), 2)
    #     if MOMC_outbound * 100 % 2 == 0:
    #         table_result = get_fm_db("hydrostatic", MOMC_outbound)
    #         print(table_result[0], table_result[0][item])
    #         return table_result[0][item]
    #     else:
    #         MOMC_outbound -= 0.01
    #         table_result = get_fm_db("hydrostatic_rounded", MOMC_outbound)
    #         return hydrostatic_interp(table_result, MOMC, item)
    #
    # if MOMC > 7.8:
    # MOMC_outbound = round(2.0 + (2.0 - MOMC), 2)
    #     if MOMC_outbound * 100 % 2 == 0:
    #         table_result = get_fm_db("hydrostatic", MOMC_outbound)
    #         print(table_result[0], table_result[0][item])
    #         return table_result[0][item]
    #     else:
    #         MOMC_outbound -= 0.01
    #         table_result = get_fm_db("hydrostatic_rounded", MOMC_outbound)
    #         return hydrostatic_interp(table_result, MOMC, item)

    # table_result[1], table_result[2],  = get_fm_db("hydrostatic", 2.0)
    # table_result = get_fm_db("hydrostatic", 2.0 + (2.0 - MOMC))










# def hydrostatic_find(conn, MOMC, item):
#     # проверка необходимости интерполляции гидростатических данных
#
#     try:
#         print('get_hydrostatic_check: ', get_hydrostatic(conn, MOMC)[1])
#     except IndexError:
#         with conn:
#             # выборка двух значений для интерполляции
#             # table_result = get_hydrostatic_interp(conn, MOMC)
#             MOMC_rounded = round((MOMC - 0.01), 4)
#             table_result = get_fm_db("hydrostatic", MOMC_rounded)
#             return hydrostatic_interp(table_result, MOMC, item)
#     else:
#         # выборка одного прямого значения гидростатических данных
#         return get_hydrostatic(MOMC)[item]


#  функция интерполляции для гидростатических данных
def hydrostatic_interp(table_result, MOMC, item):
    first_pair = table_result[0]
    second_pair = table_result[1]
    draught_diff = MOMC - first_pair[0]   # вычитание полученной осадки и первоначальной
    draught_table_diff = second_pair[0] - first_pair[0]   # разница осадок
    item_table_diff = second_pair[item] - first_pair[item]  # разница draught_dist по выбранным осадкам
    item_result = ((item_table_diff / draught_table_diff) * draught_diff + first_pair[item])
    return item_result


