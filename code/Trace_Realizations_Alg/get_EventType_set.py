import datetime
from Trace_Realizations_Alg.Event import Event
import proved.xes_keys as xes_keys


def get_EventType_set(trace):

    n = len(trace)
    ts_pairs = []
    for j in range(n):
        if xes_keys.DEFAULT_U_TIMESTAMP_MIN_KEY in trace[j].keys() and xes_keys.DEFAULT_U_TIMESTAMP_MAX_KEY in trace[j].keys():
            t_min = trace[j][xes_keys.DEFAULT_U_TIMESTAMP_MIN_KEY]
            t_max = trace[j][xes_keys.DEFAULT_U_TIMESTAMP_MAX_KEY]
            ts_pairs.append((('MIN', t_min), ('MAX', t_max)))
        else:
            t = trace[j]['time:timestamp']
            ts_pairs.append((('C', t), ('C', t)))

    E = []
    epoch = datetime.datetime(1970, 1, 1)
    for i, pair in enumerate(ts_pairs):
        ts_left = pair[0][1]
        ts_right = pair[1][1]
        tmin = (ts_left - epoch).total_seconds()
        tmax = (ts_right - epoch).total_seconds()
        event = Event(i, tmin, tmax)
        E.append(event)

    return E