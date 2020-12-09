#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from draft_survey import storage
# функция связи с БД
get_connection = lambda: storage.connect('hydrostatic.sqlite')

LBP = 123.175


def aft_dist(a_mean) -> float:
    """Функция поиска отстояния для поправки кормовой осадки"""

    aft_distance = storage.aft_dist_data(a_mean)
    if type(aft_distance) is tuple:
        aft_distance = aft_distance[0]
    aft_distance = round(aft_distance, 3)
    return aft_distance


def calculation(parameters):
    """Основная функция расчета программы"""

    #  определение средних осадок
    F_mean = round((parameters['fwd_ps'] + parameters['fwd_ss']) / 2, 3)
    M_mean = round((parameters['mid_ps'] + parameters['mid_ss']) / 2, 3)
    A_mean = round((parameters['aft_ps'] + parameters['aft_ss']) / 2, 3)

    # определение отстояний для поправок осадок
    f_delta = -2.095
    m_delta = 1.078
    # обращение к функции поиска отстояния кормовой поправки
    a_delta = aft_dist(A_mean)

    # вычисление дифферента
    app_trim = round((A_mean - F_mean), 3)

    # вычисление поправок осадок
    dF = round(app_trim * f_delta / LBP, 3)
    dM = round(app_trim * m_delta / LBP, 3)
    dA = round(app_trim * a_delta / LBP, 3)

    # скорректированные осадки
    Fc = round(F_mean + dF, 3)
    Mc = round(M_mean + dM, 3)
    Ac = round(A_mean + dA, 3)

    # вычисление дифферента по скорректированным осадкам
    true_trim = round(Ac - Fc, 3)

    #  определение прогиба/выгиба
    defl = (abs((Mc - (Fc + Ac) / 2)) * 100)

    if (Mc - (Fc + Ac) / 2) > 0:
        defl_mean = "Sagging - Прогиб"
    else:
        defl_mean = "Hogging - Выгиб"

    #  вычисление средней осадки судна
    MOMC = round((Fc + 6 * Mc + Ac) / 8, 3)

    #  вычисление гидростатических значений
    D_momc = round(storage.hydrostatic_data(MOMC, 2), 2)
    TPC = storage.hydrostatic_data(MOMC, 3)
    LCF = storage.hydrostatic_data(MOMC, 6)

    #  первая поправка за дифферент
    FTC = round(abs(true_trim * TPC * (LBP / 2 - LCF) / LBP * 100), 3)

    #TODO: test
    #  определение знака первой поправки
    if LBP/2 < LCF and true_trim > 0:
        FTC *= -1

    #  величина разброса для интерполляции в БД
    increm = 0.50

     # выборка тонн на см
    MTC_momc = round(storage.hydrostatic_data(MOMC, 4), 2)  # fm DB with interpolation by MOMC

    #  выборка момент изменения дифферента +
    MTC_plus = round(storage.hydrostatic_data(MOMC + increm, 4), 2) # fm DB with interpolation by MTC + increm

    #  выборка момент изменения дифферента -
    MTC_minus = round(storage.hydrostatic_data(MOMC - increm, 4), 2)  # fm DB with interpolation by MTC - increm

    #  разница моментов изменения дифферента
    dM_dZ = round(MTC_plus - MTC_minus, 3)

    #  вторая поправка за дифферент
    STC = round((true_trim * true_trim * dM_dZ * 50) / LBP, 3)

    # водоизмещение скорректированное за дифферент
    D_trim = round(D_momc + FTC + STC, 3)

    #  корреция за плотность воды
    D_corr = round(D_trim * parameters['density'] / 1.025, 3)

    #  судно порожнем
    lihgt_ship = 3269.367

    #  общее количество судовых запасов
    total = parameters['ballast'] + parameters['fw'] + parameters['hfo'] + parameters['mgo'] + parameters['lo'] + \
             parameters['slops'] + parameters['sludge'] + parameters['other']

    constant = 0
    #  постоянный мертвый вес судна
    constant = round(D_corr - lihgt_ship - total, 3)

    #  возвращение результатов расчетов в форму программы
    result = (F_mean, M_mean, A_mean, f_delta, m_delta, a_delta, app_trim, dF,
               dM, dA, Fc, Mc, Ac, true_trim, defl_mean, MOMC, D_momc, TPC,
               LCF, FTC, MTC_momc, MTC_plus, MTC_minus, dM_dZ, STC, D_trim,
               constant, D_corr)

    return result


if __name__ == '__main__':
    calculation()
    aft_dist()
