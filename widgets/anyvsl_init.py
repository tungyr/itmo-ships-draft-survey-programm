#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys


def calc_momc(fwd_ps, fwd_ss, mid_ps, mid_ss, aft_ps, aft_ss, lbp,
              fwd_delta, mid_delta, aft_delta):

    print('mid_ps: ', mid_ps)
    print('mid_ss: ', mid_ss)
    print('aft_ps: ', aft_ps)
    print('aft_ss: ', aft_ss)

    F_mean = round((fwd_ps + fwd_ss) / 2, 3)
    M_mean = round((mid_ps + mid_ss) / 2, 3)
    A_mean = round((aft_ps + aft_ss) / 2, 3)

    print('F_mean: ', F_mean)
    print('M_mean: ', M_mean)
    print('A_mean: ', A_mean)

    print('a_delta: ', aft_delta, type(aft_delta))

    app_trim = round((A_mean - F_mean), 3)

    print('app_trim: ', app_trim)

    dF = round(app_trim * fwd_delta / lbp, 3)
    dM = round(app_trim * mid_delta / lbp, 3)
    dA = round(app_trim * aft_delta / lbp, 3)

    print('dF: ', dF)
    print('dM: ', dM)
    print('dA: ', dA)

    Fc = round(F_mean + dF, 3)
    Mc = round(M_mean + dM, 3)
    Ac = round(A_mean + dA, 3)

    print('Fc: ', Fc)
    print('Mc: ', Mc)
    print('Ac: ', Ac)

    true_trim = round(Ac - Fc, 3)

    print('true_trim: ', true_trim)

    defl = (abs((Mc - (Fc + Ac) / 2)) * 100)  # hog / sag ???????????
    print('defl: ', defl)

    if (Mc - (Fc + Ac) / 2) > 0:
        defl_mean = "Sagging - Прогиб"
        print("Sagging - Прогиб")
    else:
        defl_mean = "Hogging - Выгиб"
        print("Hogging - Выгиб")

    MOMC = round((Fc + 6 * Mc + Ac) / 8, 3)

    evrthng = (F_mean, M_mean, A_mean, app_trim, dF,
               dM, dA, Fc, Mc, Ac, true_trim, defl_mean, MOMC)

    return evrthng


def calc_displ(lbp, true_trim, dens, displ_momc, tpc, lcf, mtc, mtc_plus,
                    mtc_minus, light_ship, ballast, fw, hfo,
                    mgo, lo, slops, sludge, other):



    print('D_momc: ', displ_momc)
    print('TPC: ', tpc)
    print('LCF: ', lcf)

    FTC = round((abs(true_trim * tpc * (lbp / 2 - lcf) / lbp * 100)), 3)

    print('FTC: ', FTC)

    if lbp/2 < lcf and true_trim > 0:
        FTC = FTC * -1
    elif lbp/2 > lcf and true_trim < 0:
        FTC = FTC * -1
    else:
        FTC = FTC  # ?

    dM_dZ = round(mtc_plus - mtc_minus, 3)

    print('dM_dZ: ', dM_dZ)

    STC = round(((true_trim * true_trim * dM_dZ * 50.0) / lbp), 3)

    print('STC: ', STC)

    D_trim = round(displ_momc + FTC + STC, 3)

    print('D_trim: ', D_trim)

    D_corr = round(D_trim * dens / 1.025, 3)

    print('D_corr: ', D_corr)

    total = ballast + fw + hfo + mgo + lo + slops + sludge + other

    print('total: ', total)

    constant = 0

    if D_corr == 0:
        constant == 0
    else:
        constant = round(D_corr - light_ship - total, 3)

    evrthng = (FTC, dM_dZ, STC, D_trim, constant, D_corr)

    return evrthng


if __name__ == '__main__':
    calc_momc()
    calc_displ()
