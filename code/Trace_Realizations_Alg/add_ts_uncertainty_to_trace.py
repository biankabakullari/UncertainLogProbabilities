import proved
from proved.simulation.bewilderer.add_timestamps import add_uncertain_timestamp_to_log
from proved.artifacts.uncertain_log.uncertain_log import UncertainLog

def add_ts_uncertainty_to_trace(prob, one_trace_log):

    add_uncertain_timestamp_to_log(p=prob, log=one_trace_log, u_timestamp_min_key='t_min', u_timestamp_max_key='t_max')