import logging as lg

def is_metastable(_syst, _time):
    sum_res = 0
    length_res = 0
    lg.info(f"FFFFFFFFFFFFFFFFFFFFFFFFFFFF - failure time is: {_time}")
    for t in range(_time, len(_syst.responded_reqs)):
        sum_res += _syst.responded_reqs[t] - _syst.responded_reqs[t - 1]
        length_res += 1
    lg.warning(f"The average slope of responded_reqs is: {sum_res / length_res}")
    sum_ret = 0
    length_ret = 0
    for t in range(_time, len(_syst.retried_reqs)):
        sum_ret += _syst.retried_reqs[t] - _syst.retried_reqs[t - 1]
        length_ret += 1
    lg.warning(f"The average slope of retried_reqs is: {sum_ret / length_ret}")
    return sum_res / length_res, sum_ret / length_ret
