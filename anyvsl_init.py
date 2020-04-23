#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys


def calc_momc(params):

    F_mean = round((params['fwd_ps'] + params['fwd_ss']) / 2, 3)
    M_mean = round((params['mid_ps'] + params['mid_ss']) / 2, 3)
    A_mean = round((params['aft_ps'] + params['aft_ss']) / 2, 3)

    app_trim = round((A_mean - F_mean), 3)

    dF = round(app_trim * params['fwd_delta'] / params['lbp'], 3)
    dM = round(app_trim * params['mid_delta'] / params['lbp'], 3)
    dA = round(app_trim * params['aft_delta'] / params['lbp'], 3)

    Fc = round(F_mean + dF, 3)
    Mc = round(M_mean + dM, 3)
    Ac = round(A_mean + dA, 3)

    true_trim = round(Ac - Fc, 3)

    defl = (abs((Mc - (Fc + Ac) / 2)) * 100)  # hog / sag ???????????
    print('defl: ', defl)

    if (Mc - (Fc + Ac) / 2) > 0:
        defl_mean = "Sagging"
    else:
        defl_mean = "Hogging"

    MOMC = round((Fc + 6 * Mc + Ac) / 8, 3)

    # вычисленные результаты плюс пробрасываем значения из словаря params обратно чтобы использовать
    # их все вмесе в экспорте
    result = (F_mean, M_mean, A_mean, params['fwd_delta'], params['mid_delta'], params['aft_delta'],  app_trim, dF,
               dM, dA, Fc, Mc, Ac, true_trim, defl_mean, MOMC)

    return result


def calc_displ(params):

    print('D_momc: ', params['displ_momc'])
    print('TPC: ', params['tpc'])
    print('LCF: ', params['lcf'])

    FTC = round((abs(params['true_trim'] * params['tpc'] * (params['lbp'] / 2 - params['lcf']) / params['lbp'] * 100)), 3)

    print('FTC: ', FTC)

    if params['lbp']/2 < params['lcf'] and ['true_trim'] > 0:
        FTC = FTC * -1
    elif params['lbp']/2 > params['lcf'] and params['true_trim'] < 0:
        FTC = FTC * -1
    else:
        FTC = FTC  # ?

    dM_dZ = round(params['mtc_plus'] - params['mtc_minus'], 3)

    print('dM_dZ: ', dM_dZ)

    STC = round(((params['true_trim'] * params['true_trim'] * dM_dZ * 50.0) / params['lbp']), 3)

    print('STC: ', STC)

    D_trim = round(params['displ_momc'] + FTC + STC, 3)

    print('D_trim: ', D_trim)

    D_corr = round(D_trim * params['dens'] / 1.025, 3)

    print('D_corr: ', D_corr)

    total = params['ballast'] + params['fw'] + params['hfo'] + params['mgo'] + params['lo'] + params['slops'] + params['sludge'] + params['other']

    print('total: ', total)

    constant = 0

    if D_corr == 0:
        constant == 0
    else:
        constant = round(D_corr - params['light_ship'] - total, 3)
    # вычисленные результаты плюс пробрасываем значения из словаря params обратно чтобы использовать
    # их все вмесе в экспорте
    result = (params['displ_momc'], params['tpc'], params['lcf'], FTC, params['mtc'], params['mtc_plus'], params['mtc_minus'], dM_dZ, STC, D_trim, constant, D_corr)

    return result


if __name__ == '__main__':
    calc_momc()
    calc_displ()
