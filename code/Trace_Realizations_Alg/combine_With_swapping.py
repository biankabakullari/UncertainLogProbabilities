import itertools as it

def interweave(sb, s, start_pos=0):
    if not sb:  # if sb is empty, you are done
        return [s]

    sequences = []
    event = sb[0]
    for pos in range(start_pos, len(s) + 1):
        s_new = s.copy()
        s_new.insert(pos, event)
        sequences += interweave(sb[1:], s_new, pos + 1)
    return sequences


# In[114]:


def combine_With_swapping(Pi_lists):
    k = len(Pi_lists)
    if k == 1:
        # Input is [P], return P
        return Pi_lists[0]

        # input is [P1,...,Pk] with k > 1
    full_sequences = []

    # stays true if all sets have only a sequence with one single element
    all_singletons = True
    # indices of sets with only one element which is a singleton list
    singleton_sets = []

    for i in range(k):
        Pi_size = len(Pi_lists[i])
        for j in range(Pi_size):
            if len(Pi_lists[i][j]) == 1:
                if i not in singleton_sets:
                    singleton_sets.append(i)
            else:
                all_singletons = False
                # the index of the only set with longer sequence(s), if there is one
                non_singleton = i

    if all_singletons == True:
        Pi_singletons = Pi_lists
    else:
        Pi_singletons = [Pi_lists[x] for x in singleton_sets]
    # save here all sequences emerging from concatenating only singleton sets
    singleton_sequences = []
    # if all sets are indeed only singleton sets, any order between them is valid
    index_permutations = it.permutations(range(len(Pi_singletons)))
    for permutation in index_permutations:
        sequence = []
        for index in permutation:
            # accessing the index-th list of form [x], get x
            sequence += Pi_singletons[index][0]
        singleton_sequences.append(sequence)

    if all_singletons == True:
        # since there is no non-singleton set, singleton sequences are already the full sequences
        return singleton_sequences
    else:
        big_set = Pi_lists[non_singleton]
        # go through each sequence in the single big component (big component could contain many sequences)
        for sb in big_set:
            for s in singleton_sequences:
                interweavings = interweave(sb, s)
                for sequence in interweavings:
                    full_sequences.append(sequence)
        return full_sequences