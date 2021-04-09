from Trace_Realizations_Alg.one_trace_log_generator import generate_one_trace_log
from Trace_Realizations_Alg.add_ts_uncertainty_to_trace import add_ts_uncertainty_to_trace
from Trace_Realizations_Alg.get_EventType_set import get_EventType_set
from Trace_Realizations_Alg.ValidPermutations import ValidPermutations
from Trace_Realizations_Alg.NaivePermutations import NaivePermutations
from proved.artifacts.uncertain_log.utils import realization_set
import time
import gc
import matplotlib.pyplot as plt

gc.disable()
elapsed_novel = []
elapsed_naive = []
elapsed_rs = []
for i in range(1,11):

    p = i * 0.1
    #add_ts_uncertainty_to_trace(p, simulated_log)
    #E = get_EventType_set(simulated_log[0])
    simulated_log = generate_one_trace_log(9)

    elapsed_i_novel = 0
    elapsed_i_naive = 0
    elapsed_i_rs = 0
    gc.collect()
    for j in range(10):
        print(f"p={p}, j={j}")

        add_ts_uncertainty_to_trace(p, simulated_log)
        trace = simulated_log[0]
        E = get_EventType_set(trace)
        start_j_novel = time.perf_counter()
        novel = ValidPermutations(E)
        elapsed_j_novel = time.perf_counter()  - start_j_novel
        elapsed_i_novel += elapsed_j_novel

        start_j_naive = time.perf_counter()
        naive = NaivePermutations(E)
        elapsed_j_naive = time.perf_counter()  - start_j_naive
        elapsed_i_naive += elapsed_j_naive

        #start_j_rs = time.time()
        #realizations = realization_set(trace)
        #elapsed_j_rs = time.time() - start_j_rs
        #elapsed_i_rs += elapsed_j_rs

    elapsed_novel.append(elapsed_i_novel/10)
    elapsed_naive.append(elapsed_i_naive/10)
    #elapsed_rs.append(elapsed_i_rs/1000)

#print(elapsed_novel)
#print(elapsed_naive)

x = [i*0.1 for i in range(1,11)]
y1 = elapsed_novel
y2 = elapsed_naive
plt.plot(x, y1, label = "novel", linestyle='-', marker='s', color='b')
plt.plot(x, y2, label = "naive", linestyle='-', marker='d', color='r')
plt.yscale('log')
plt.xlabel("Probability p")
plt.ylabel("Time (seconds)")
plt.legend()
plt.show()