import pm4py
import random
from pm4py.objects.petri.petrinet import PetriNet, Marking
from pm4py.objects.petri import utils
from pm4py.simulation.playout import simulator
from pm4py.objects.random_variables.random_variable import RandomVariable
from pm4py.objects.random_variables.uniform.random_variable import Uniform
import matplotlib.pyplot as plt

# create new petrinet
net = PetriNet("PN")

# create places
start = PetriNet.Place("start")
end = PetriNet.Place("end")
p2 = PetriNet.Place("p2")
p3 = PetriNet.Place("p3")
p4 = PetriNet.Place("p4")
p5 = PetriNet.Place("p5")

# add places to petrinet
places = [start, end, p2, p3, p4, p5]
for p in places:
    net.places.add(p)

# create transitions
t1 = PetriNet.Transition("t1", "a")
t2 = PetriNet.Transition("t2", "b")
t3 = PetriNet.Transition("t3", "c")
t4 = PetriNet.Transition("t4", "d")
t5 = PetriNet.Transition("t5", None)
t6 = PetriNet.Transition("t6", "e")

# add transitions to petrinet
transitions = [t1, t2, t3, t4, t5, t6]
for t in transitions:
    net.transitions.add(t)

# add arcs
utils.add_arc_from_to(start, t1, net)
utils.add_arc_from_to(t1, p2, net)
utils.add_arc_from_to(t1, p3, net)
utils.add_arc_from_to(p2, t2, net)
utils.add_arc_from_to(p2, t3, net)
utils.add_arc_from_to(p3, t4, net)
utils.add_arc_from_to(p3, t5, net)
utils.add_arc_from_to(t2, p4, net)
utils.add_arc_from_to(t3, p4, net)
utils.add_arc_from_to(t4, p5, net)
utils.add_arc_from_to(t5, p5, net)
utils.add_arc_from_to(p4, t6, net)
utils.add_arc_from_to(p5, t6, net)
utils.add_arc_from_to(t6, end, net)

# defining initiam and final marking
im = Marking()
im[start] = 1
fm = Marking()
fm[end] = 1

    # visualizing the petrinet
    #from pm4py.objects.petri.exporter import exporter as pnml_exporter

    #pnml_exporter.apply(net, im, "createdPetriNet1.pnml", final_marking=fm)

    #from pm4py.visualization.petrinet import visualizer as pn_visualizer

    #gviz = pn_visualizer.apply(net, im, fm)
    #pn_visualizer.view(gviz)


#by using the extensive variant, we obtain the set of all possible runs
#there are 6 possible traces
simulated_log = simulator.apply(net, im, variant=simulator.Variants.EXTENSIVE, parameters={simulator.Variants.EXTENSIVE.value.Parameters.MAX_TRACE_LENGTH: 5})

#saving possible traces in a dictionary
possible_traces = {}
possible_traces[0] = ['a', 'b', 'e']
possible_traces[1] = ['a', 'b', 'd', 'e']
possible_traces[2] = ['a', 'd', 'b', 'e']
possible_traces[3] = ['a', 'c', 'e']
possible_traces[4] = ['a', 'c', 'd', 'e']
possible_traces[5] = ['a', 'd', 'c', 'e']

#creating stochastic map assigning probabilities to transitions
smap = {}
for t in transitions:
    rand = RandomVariable()
    #we do not use the uniform distribution, but we need some kind of distribution to initialize
    #the random_variable of the RandomVariable() object, so that we can call set_weight and get_weight later
    rand.random_variable = Uniform()
    smap[t] = rand
    if t.label == "b":
        rand.set_weight(0.9)
    elif t.label == "c":
        rand.set_weight(0.1)
    elif t.label == "d":
        rand.set_weight(0.2)
    elif t.label == None:
        rand.set_weight(0.8)
    else:
        rand.set_weight(1)


simulated_log2 = simulator.apply(
    net,
    initial_marking = im,
    final_marking = fm,
    variant=simulator.Variants.STOCHASTIC_PLAYOUT,
    parameters={simulator.Variants.STOCHASTIC_PLAYOUT.value.Parameters.STOCHASTIC_MAP: smap,
                simulator.Variants.STOCHASTIC_PLAYOUT.value.Parameters.MAX_TRACE_LENGTH: 5,
                simulator.Variants.STOCHASTIC_PLAYOUT.value.Parameters.NO_TRACES: 100000
})


#all traces have length 4, there are 6 possible traces
simulated_traces = []
for i,trace in enumerate(simulated_log2):
    activities = []
    n = len(trace)
    for j in range(n):
        activities.append(trace[j]['concept:name'])
    simulated_traces += [activities]



#counting how often each trace appears
counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

counts_abe = []
counts_abde = []
counts_adbe = []
counts_ace = []
counts_acde = []
counts_adce = []

runs = 0

for trace in simulated_traces:
    runs += 1
    for key in possible_traces.keys():
        if trace == possible_traces[key]:
            counts[key] +=1
    counts_abe.append(counts[0]/runs)
    counts_abde.append(counts[1]/runs)
    counts_adbe.append(counts[2] / runs)
    counts_ace.append(counts[3] / runs)
    counts_acde.append(counts[4] / runs)
    counts_adce.append(counts[5] / runs)

for key in counts:
    print(key, possible_traces[key], counts[key]/100000)


#x = [x for x in range(1,100001)]
#plt.plot(x, [0.72]*100000, color='b', linestyle='-', label="Estimate for <a,b,e>")
#plt.plot(x, counts_abe, color='r', label="Simulation for <a,b,e>")
#plt.yticks([0, 0.5, 0.72, 1])
#plt.legend()
#plt.show()

#x = [x for x in range(1,100001)]
#plt.plot(x, [0.09]*100000, color='b', linestyle='-', label="Estimate for <a,b,d,e>")
#plt.plot(x, counts_abde, color='r', label="Simulation for <a,b,d,e>")
#plt.yticks([0.09, 0.5, 1])
#plt.legend()
#plt.show()

#x = [x for x in range(1,100001)]
#plt.plot(x, [0.09]*100000, color='b', linestyle='-', label="Estimate for <a,d,b,e>")
#plt.plot(x, counts_adbe, color='r', label="Simulation for <a,d,b,e>")
#plt.yticks([0.09, 0.5, 1])
#plt.legend()
#plt.show()

#x = [x for x in range(1,100001)]
#plt.plot(x, [0.08]*100000, color='b', linestyle='-', label="Estimate for <a,c,e>")
#plt.plot(x, counts_ace, color='r', label="Simulation for <a,c,e>")
#plt.yticks([0.08, 0.5, 1])
#plt.legend()
#plt.show()

#x = [x for x in range(1,100001)]
#plt.plot(x, [0.01]*100000, color='b', linestyle='-', label="Estimate for <a,c,d,e>")
#plt.plot(x, counts_acde, color='r', label="Simulation for <a,c,d,e>")
#plt.yticks([-0.02, 0.01, 0.5, 1])
#plt.legend()
#plt.show()

#x = [x for x in range(1,100001)]
#plt.plot(x, [0.01]*100000, color='b', linestyle='-', label="Estimate for <a,d,c,e>")
#plt.plot(x, counts_adce, color='r', label="Simulation for <a,d,c,e>")
#plt.yticks([-0.02, 0.01, 0.5, 1])
#plt.legend()
#plt.show()

fig, axs = plt.subplots(6, 1)
axs[0].axhline(y=0.72, color='b', linestyle='-', label="Estimate for <a,b,e>")
axs[0].plot(counts_abe, color='r', label="Simulation for <a,b,e>")
axs[0].set_yticks([0, 0.5, 0.72, 1])
axs[0].legend()

axs[1].axhline(y=0.09, color='b', linestyle='-', label="Estimate for <a,b,d,e>")
axs[1].plot(counts_abde, color='r', label="Simulation for <a,b,d,e>")
axs[1].set_yticks([0.09, 0.5, 1])
axs[1].legend()

axs[2].axhline(y=0.09, color='b', linestyle='-', label="Estimate for <a,d,b,e>")
axs[2].plot(counts_adbe, color='r', label="Simulation for <a,d,b,e>")
axs[2].set_yticks([0.09, 0.5, 1])
axs[2].legend()

axs[3].axhline(y=0.08, color='b', linestyle='-', label="Estimate for <a,c,e>")
axs[3].plot(counts_ace, color='r', label="Simulation for <a,c,e>")
axs[3].set_yticks([0.08, 0.5, 1])
axs[3].legend()

axs[4].axhline(y=0.01, color='b', linestyle='-', label="Estimate for <a,c,d,e>")
axs[4].plot(counts_acde, color='r', label="Simulation for <a,c,d,e>")
axs[4].set_yticks([-0.2, 0.01, 0.5, 1])
axs[4].legend()

axs[5].axhline(y=0.01, color='b', linestyle='-', label="Estimate for <a,d,c,e>")
axs[5].plot(counts_adce, color='r', label="Simulation for <a,d,c,e>")
axs[5].set_yticks([-0.2, 0.01, 0.5, 1])
axs[5].legend()

fig.subplots_adjust(hspace=0.5)
plt.show()


