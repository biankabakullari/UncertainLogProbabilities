import pm4py
from pm4py.objects.petri.petrinet import PetriNet, Marking
from pm4py.objects.petri import utils
from pm4py.simulation.playout import simulator
import string

def generate_one_trace_log(n):

    # here we create a petri net with n transitions and n+1 places, which can replay a single trace of length n
    def create_PetriNet(n):
        # label_set[0] = 'a',...,label_set[26]=z
        label_set = dict(enumerate(string.ascii_lowercase))
        if n >= 26:
            print("N is >= 26 but there are only 26 unique letters.")

        # create new petrinet
        net = PetriNet("PN")

        place_list = []
        # create start and end place
        start = PetriNet.Place("start")
        end = PetriNet.Place("end")
        net.places.add(start)
        net.places.add(end)
        place_list.insert(0, start)
        place_list.insert(n + 1, end)

        # create the rest of n-2 places (n+1 places are needed for a length n trace)
        for i in range(n - 1):
            p = PetriNet.Place(f"p{i}")
            net.places.add(p)
            place_list.insert(i + 1, p)

        transitions_list = []
        # create n transitions
        for i in range(n):
            t = PetriNet.Transition(f"t{i}", label_set[i])
            net.transitions.add(t)
            transitions_list.insert(i, t)

        for i, t in enumerate(transitions_list):
            utils.add_arc_from_to(place_list[i], t, net)
            utils.add_arc_from_to(t, place_list[i + 1], net)

        # defining initial and final marking
        im = Marking()
        im[start] = 1
        fm = Marking()
        fm[end] = 1

        return net, im

    petrinet, im = create_PetriNet(n)
    # by using the extensive variant, we obtain the set of all possible runs
    # there is only one trace with length <27 (can only generate trace with up to 26 distinct letters as transition labels)
    simulated_log = simulator.apply(petrinet, initial_marking=im, variant=simulator.Variants.EXTENSIVE, parameters={simulator.Variants.EXTENSIVE.value.Parameters.MAX_TRACE_LENGTH: 30})

    return simulated_log