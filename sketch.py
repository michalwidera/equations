#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

hh = (3 ** 0.5) / 2.0
span = 20

def get_delta(first_ls):
    prev_elem = None
    delta_ls = []
    for one_elem in first_ls:
        if prev_elem is not None:
            if one_elem is None:
                diff_value = None
            else:
                diff_value = one_elem - prev_elem
            delta_ls.append(diff_value)
        prev_elem = one_elem
    delta_ls.append(None)
    return delta_ls



def kot(line_nr):  
    first_ls = []
    if line_nr % 2:
        horiz_start = 0.5
    else:
        horiz_start = 0.0
    for i in range(-span, span):
        elem = (line_nr * line_nr * 3) / 4.0 + (i + horiz_start) ** 2
        first_ls.append(elem)
    return first_ls


def display_result():
    line_nr = 2
    first_ls = kot(line_nr)
    delta_ls = get_delta(first_ls)
    sec_ls = get_delta(delta_ls)
    tri_ls = get_delta(sec_ls)
    for a, b, c, d in zip(first_ls, delta_ls, sec_ls, tri_ls):
        print(a ** 0.5, a, b, c, d)


display_result()
