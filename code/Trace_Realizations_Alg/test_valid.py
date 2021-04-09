from Trace_Realizations_Alg.Event import Event
from Trace_Realizations_Alg.ValidPermutations import ValidPermutations

e1 = Event(1, 2, 2)
e2 = Event(2, 1, 3)
e3 = Event(3, 4, 5)
e4 = Event(4, 6, 7)
e5 = Event(5, 9, 9)
e6 = Event(6, 8, 10)
e7 = Event(7, 4, 10)
e8 = Event(8, 13, 13)

E = set([e1, e2, e3, e4, e5, e6, e7, e8])

valids = ValidPermutations(E)
print(len(valids))