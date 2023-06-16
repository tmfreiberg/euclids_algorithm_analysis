## AN ANALYSIS OF EUCLID'S ALGORITHM
##
## BY TRISTAN FREIBERG
##
##See
##
##https://github.com/tmfreiberg/euclids_algorithm_analysis/blob/main/README.md
##
##for an exposition with examples, plots, and much more.

# LIBRARIES/PACKAGES/MODULES

import numpy as np                              # Naturally, we'll need to do some numerics.
import pandas as pd                             # We'll want to put data in data frames to import and export it, and to display it nicely.
from timeit import default_timer as timer       # We'll want to see how long certain computations take.
import scipy.stats as stats                     # We'll want to plot normal curves and so on.
from scipy.optimize import curve_fit            # We'll want to do some curve-fitting.
from scipy.special import zeta                  # For certain constants involving the Riemann zeta function.
import matplotlib.pyplot as plt                 # We'll want to plot our data.
from matplotlib import animation                # We'll even make animations to display our data.
from matplotlib import rc                       # For animations.
from IPython.display import HTML                # For displaying and saving animations.
from matplotlib.animation import PillowWriter   # To save animated gifs.

# CODE FOR EUCLID'S ALGORITHM

# Let's code Euclid's algorithm in a few different ways.
# No special libraries are required for this code block.
# If we just want gcd(a,b), this is about the most straightforward way. 

def gcd(a,b):
    if b == 0:
        return abs(a)
    return gcd(b,a%b)

# As a side-note, the definition of gcd extends in an obvious way to gcd of an n-tuple of integer, n >= 2.
# Namely, gcd(a_1,...,a_n) is the unique nonnegative integer with the following property.
# For any integer d, d divides every a_i if and only if d divides gcd(a_1,...,a_n).
# Thus, gcd(a_1,...,a_n) = gcd(a_1,gcd(a_2,...,a_n)), and we can use recursion to compute the gcd of an n-tuple, as below.

def gcdn(*ntuple): # arbitrary number of arguments
    if len(ntuple) == 2:
        return gcd(ntuple[0], ntuple[1])
    return gcd(ntuple[0],gcdn(*ntuple[1:]))

# If we want gcd(a,b) and the number of steps (T(a,b)), we can use this.

def gcd_steps(a,b,i): # Input i = 0
    if b == 0:
        return abs(a), i # Output gcd(a,b) and i = T(a,b)
    i += 1
    return gcd_steps(b,a%b,i)

# If we want the sequence of remainders 
# [r_0,r_1,r_2,...,r_n] (a = r_0, b = r_1, r_{n + 1} = 0, r_1 > r_2 > ... > r_n > 0),
# we can use this.

def rem(a,b,r): # Input r = []
    r.append(a)
    if b == 0:
        return r
    return rem(b,a%b,r) # gcd(a,b) = abs(r[-1]), gcd_steps = len(r) - 1

# If we want to record both remainders and quotients [q_1,...,q_n], we can use this.

def quot_rem(a,b,q,r): # Input r = [] and q = []
    r.append(a)
    if b == 0:
        return q, r
    (Q, R) = divmod(a,b)
    q.append(Q)
    return quot_rem(b,R,q,r) # rem(a,b,r) = quot_rem(a,b,q,r)[1]

# If we want to write out the entire process, we can use this.

def write_euclid(a,b): 
    q, r = quot_rem(a,b,[],[])  
    R = r[2:] # The next few lines are largely to facilitate the formatting of the output (alignment etc.)
    R.append(0)
    A, B, Q = r, r[1:], q 
    GCDcol = [f'gcd({a},{b})', f'gcd({b},{R[0]})']
    for i in range(len(R) - 1):
        GCDcol.append(f'gcd({R[i]},{R[i + 1]})')
    for i in range(len(B)): # For display, put parentheses around negative integers.
        if B[i] < 0:
            B[i] = f'({B[i]})'
    for i in range(len(Q)): # For display, put parentheses around negative integers.
        if Q[i] < 0:
            Q[i] = f'({Q[i]})' 
    pm = [] # Next few lines are so we display a = bq - r instead of a = bq + -r in the case where r < 0.
    for i in range(len(R)): 
        if R[i] < 0:
            R[i] = -R[i]
            pm.append('-')
        else:
            pm.append('+')
    colA = max([len(str(i)) for i in A]) # For alignment.
    colB = max([len(str(i)) for i in B])
    colQ = max([len(str(i)) for i in Q])
    colR = max([len(str(i)) for i in R])
    colGCDl = max([len(i) for i in GCDcol[:-2]])
    colGCDr = max([len(i) for i in GCDcol[1:]])
    if len(A) > 1:
        for i in range(len(R)):
            print(f'{A[i]:>{colA}} = {Q[i]:>{colQ}}*{B[i]:>{colB}} {pm[i]} {R[i]:>{colR}} \t ∴ {GCDcol[i]:>{colGCDl}} = {GCDcol[i + 1]:<{colGCDr}}')
    print(f'\ngcd({a},{b}) = {abs(r[-1])}, T({a},{b}) = {len(r) - 1}\n')

# THE FIBONACCI NUMBERS AND DYNAMIC PROGRAMMING

# Let's take a detour and compute some Fibonacci numbers.
# Computing f_n naively takes time exponential in n.
# E.g. to compute f_5 naively we do this: 
# f_5 = f_4 + f_3 
#     = f_3 + f_2 + f_2 + f_1 
#     = f_2 + f_1 + f_1 + f_0 + f_1 + f_0 + 1
#     = f_1 + 1 + 1 + 0 + 1 + 0 + 1
#     = 1 + 1 + 1 + 0 + 1 + 0 + 1
#     = 5
# We can think of this as a tree with f_5 at the top, 
# and where each parent node has two children until the node corresponds to f_1 or f_0. 
# We end up having to sum a sequence of 1's and 0's of length f_n, 
# and we know f_n is of order phi^n, where phi is the golden ratio.

def naive_fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n > 1:
        return naive_fib(n - 1) + naive_fib(n - 2)
    if n < 0:
        return naive_fib(-n) # Why not?

# Of course it is very silly to compute fib(n) from scratch if you've just computed f_0,f_1,...,f_{n-1}.
# Let's compute f_n the way a human might do it: by starting at the beginning.

FIB = []
list_time = []
for n in range(101):
    start = timer()
    if (n == 0 or n == 1):
        FIB.append(n)
    else:
        FIB.append(FIB[n - 1] + FIB[n - 2])
    end = timer()
    list_time.append(end - start)

# Now if we want to compute f_n but don't want to have to maintain an ever-expanding list 
# of all previous Fibonacci numbers, we can do the following.
# This algorithm computes f_n in O(n) time for n >= 1 
# (a unit of time being the time taken to do an addition and update a couple of variables).
# There are only about n additions needed in this algorithm.
# This is the archetypal example of dynamic programming, specifically memoization.
# a and b in the code below essentially constitute a hash table, which is updated in each iteration. 
# Perhaps the previous code (generating a list of all Fibonacci numbers) up to f_n, is an example 
# of tabulation.

def fib(n):
    a, b = 0, 1 # a and b will be placeholders for fib(n - 2) and fib(n - 1)
    if n == 0:
        return a
    if n == 1:
        return b
    if n < 0: 
        return fib(-n) # Why not?
    for k in range(n-1):
        c = a + b # c will be fib(n) ultimately. 
        a = b # First, k = 0, c = 0 + 1 = 1, a -> 1, b -> 1.
        b = c # Then, k = 1, c -> 1 + 1 = 2, a -> 1, b -> 2. And so on.
    return c

#CONSTANTS

# Constants needed to define other subsequent constants...
euler_mascheroni = 0.57721566490153286060   # Approximate value of Euler-Mascheroni constant.
zeta_der_2 = -0.93754825431584375370        # Approximate value of zeta'(2)
zeta_dder_2 = 1.98928                       # Approximation to zeta''(2)

# The constants we actually need...
# For the mean in the one- and two-dimensional analyses

# This is the reciprocal of Levy's constant. We'll name it here in honour of Dixon.
lambda_dixon = 2*np.log(2)/zeta(2) 
# Porter's constant
porter_constant = ((np.log(2))/zeta(2))*(3*np.log(2) + 4*euler_mascheroni - 4*zeta_der_2/zeta(2) - 2) - (1/2) 

# For the mean in the two-dimensional analysis (subdominant constants)

# Norton's refinement of the mean. (Counting all pairs, not just a > b.)
nu_norton = -1 + lambda_dixon*(2*euler_mascheroni + 1.5*np.log(2) - 1.5 - zeta_der_2/zeta(2)) 
# Norton's constant for case of coprime pairs. (Counting all coprime pairs, not just a > b.)
nu_norton_coprime = nu_norton - lambda_dixon*zeta_der_2/zeta(2) 

# For the variance in the two-dimensional analysis

# Hensley's constant in the variance, as given by Lhote.
eta_hensley = 0.5160524 

# Subdominant constants in the variance for the two-dimensional analysis

# Our "guesstimate" of the subdominant constant in a certain variance
kappa_var = -0.1 
delta_kappa = np.around(eta_hensley*zeta_der_2/zeta(2) + (lambda_dixon**2)*((zeta_dder_2/zeta(2)) - (zeta_der_2/zeta(2))**2),3)
# Our "guesstimate" of the subdominant constant in another variance
kappa_var_coprime = np.around(kappa_var - delta_kappa,3) 

# CODE FOR ANALYSING EUCLID'S ALGORITHM

# Input a dictionary and output a new dictionary, sorted by keys (if the keys are sortable).
def dictionary_sort(dictionary):  
    L = list(dictionary.keys()) 
    L.sort() 
    sorted_dictionary = {}  
    for k in L: 
        sorted_dictionary[k] = dictionary[k] 
    return sorted_dictionary 

# ONE-DIMENSIONAL CASE

# Input gcdlist and list 1, output two dictionaries, both of whose keys are the elements a of list1, 
# and whose corresponding values are themselves dictionaries, the keys of which are positive integers s, 
# s being the number of divisions performed in the Euclidean algorithm in computing gcd(a,b) for some b in [1,a]. 
# The corresponding values are frequencies (the number of b for which T(a,b) = s).
# In the first dictionary, we restrict to b for which gcd(a,b) is in gcdlist (primarily interested in gcdlist = [1]).
# In the second output dictionary, we count all b in [1,a].
# Thus, the second output dictionary items take the form a : {1 : x, 2 : y, ...}, where x is the number of b in [1,a] such that
# T(a,b) = 1, y is the number of b in [1,a] such that T(a,b) = 2, and so on. 
# First output dictionary similar but b is restricted by gcdlist.

def heilbronn(gcdlist, list1):
    list1.sort()
    output_dictionary_restricted = {}
    output_dictionary_all = {}
    for a in list1:
        output_dictionary_restricted[a] = {}
        output_dictionary_all[a] = {}
        for b in range(1,a+1):
            g, s = gcd_steps(a,b,0)
            if (g in gcdlist):
                if s in output_dictionary_restricted[a].keys():
                    output_dictionary_restricted[a][s] += 1
                else:
                    output_dictionary_restricted[a][s] = 1
            if s in output_dictionary_all[a].keys():
                output_dictionary_all[a][s] += 1
            else:
                output_dictionary_all[a][s] = 1
    return output_dictionary_restricted, output_dictionary_all

# TWO-DIMENSIONAL CASE

# Input three lists and three dictionaries (gcdlist, list1, list2, gcd_dictionary, steps_dictionary, steps_dictionary_all). 
# Usually, list1 and the three dictionaries will be empty (unless we're building upon data we've already produced).
# Output will be three "meta" dictionaries, each containing dictionaries whose keys are the integers in list2.
# Say the output dictionaries are A, B, C, and N is a key.
# In A, the value corresponding to N will be a dictionary itself, where each item is of the form 
# g : #{0 < b < a < N : gcd(a,b) = g}.
# In B, the value corresponding to N will be a dictionary itself, where each item is of the form 
# s : #{0 < b < a < N and gcd(a,b) is in gcdlist: T(a,b) = s}.
# In C, the value corresponding to N will be a dictionary itself, where each item is of the form 
# s : #{0 < b < a < N : T(a,b) = s}.
# If we've already spent a long time to create A, B, and C, we will not want to re-do the computation when we want to
# extend them. If we want to extend A, B, and C, we should input A, B, and C as the three dictionary inputs.
# list1 should be the keys of A, B, and C, although all that really matters is that list1[-1] == list2[0].
# list2[1:] should list of keys we want to add to A, B, and C. 

def euclid_alg_frequencies(gcdlist, list1, list2, gcd_dictionary, steps_dictionary, steps_dictionary_all):
    list2.sort()    
    gcd_frequencies = {}
    steps_frequencies = {}
    steps_frequencies_all = {}
    updated_gcd_dictionary = dictionary_sort(gcd_dictionary)
    updated_steps_dictionary = dictionary_sort(steps_dictionary)
    updated_steps_dictionary_all = dictionary_sort(steps_dictionary_all) 
    if list1 == []:
        b_0 = list2[0]
    else:
        list1.sort()
        b_0 = list1[0]
        for k in updated_gcd_dictionary[list1[-1]].keys():
            gcd_frequencies[k] = updated_gcd_dictionary[list1[-1]][k]
        for k in updated_steps_dictionary[list1[-1]].keys():
            steps_frequencies[k] = updated_steps_dictionary[list1[-1]][k]
        for k in updated_steps_dictionary_all[list1[-1]].keys():
            steps_frequencies_all[k] = updated_steps_dictionary_all[list1[-1]][k]
    for k in range(len(list2)-1):
        for b in range(list2[k], list2[k + 1]):
            for a in range(b + 1, list2[k + 1]):
                g, s = gcd_steps(a,b,0)
                if g in gcd_frequencies.keys():
                    gcd_frequencies[g] += 1
                else:
                    gcd_frequencies[g] = 1
                if s in steps_frequencies_all.keys():
                    steps_frequencies_all[s] += 1
                else:
                    steps_frequencies_all[s] = 1
                if (g in gcdlist or gcdlist == []):
                    if s in steps_frequencies.keys():
                        steps_frequencies[s] += 1
                    else:
                        steps_frequencies[s] = 1
        for b in range(b_0,list2[k]): 
            for a in range(list2[k], list2[k + 1]): 
                g, s = gcd_steps(a,b,0)
                if g in gcd_frequencies.keys():
                    gcd_frequencies[g] += 1
                else:
                    gcd_frequencies[g] = 1
                if s in steps_frequencies_all.keys():
                    steps_frequencies_all[s] += 1
                else:
                    steps_frequencies_all[s] = 1
                if (g in gcdlist or gcdlist == []):
                    if s in steps_frequencies.keys():
                        steps_frequencies[s] += 1
                    else:
                        steps_frequencies[s] = 1
        updated_gcd_dictionary[list2[k+1]] = dictionary_sort(gcd_frequencies) 
        updated_steps_dictionary[list2[k+1]] = dictionary_sort(steps_frequencies)
        updated_steps_dictionary_all[list2[k+1]] = dictionary_sort(steps_frequencies_all)
    return updated_gcd_dictionary, updated_steps_dictionary, updated_steps_dictionary_all

# Now some code that will take a dictionary as input.
# Assume the keys are numbers and each key's value is the number of times (frequency of) the key occurs in some data.
# The output is a dictionary, whose first item is itself a dictionary, whose keys are the same as the input dictionary, 
# and for which each key's value is the _proportion_ of occurrences (_relative_ frequency) of the key among the data.
# The other items in the output dictionary are mean, variance, median, mode, etc., of the original data.

def dictionary_statistics(dictionary): 
    frequencies = dictionary_sort(dictionary)
    relative_frequencies = {} 
    number_of_objects_counted = 0 
    mean = 0 
    median = 0 
    mode = [] 
    second_moment = 0 
    variance = 0 
    standard_deviation = 0 
    M = max(frequencies.values()) 
    for s in frequencies.keys(): 
        number_of_objects_counted += frequencies[s] 
        mean += s*frequencies[s]  
        second_moment += (s**2)*frequencies[s] 
        if frequencies[s] == M:
            mode.append(s) 
    mean = mean/number_of_objects_counted
    second_moment = second_moment/number_of_objects_counted
    variance = second_moment - mean**2 
    standard_deviation = np.sqrt(variance)
    
# A little subroutine for computing the median... 

    temp_counter = 0 
    if number_of_objects_counted%2 == 1: 
        for s in frequencies.keys():
            if temp_counter < number_of_objects_counted/2:
                temp_counter += frequencies[s]
                if temp_counter > number_of_objects_counted/2:
                    median = s
    if number_of_objects_counted%2 == 0: 
        for s in frequencies.keys():
            if temp_counter < number_of_objects_counted/2:
                temp_counter += frequencies[s]
                if temp_counter >= number_of_objects_counted/2:
                    median = s 
        temp_counter = 0 
        for s in frequencies.keys():
            if temp_counter < 1 + (number_of_objects_counted/2):
                temp_counter += frequencies[s]
                if temp_counter >= 1 + (number_of_objects_counted/2):
                    median = (median + s)/2     

# Finally, let's get the relative frequencies.

    for s in frequencies.keys(): 
        relative_frequencies[s] = frequencies[s]/number_of_objects_counted

    output_dictionary = {} 
    output_dictionary["dist"] = relative_frequencies
    output_dictionary["mean"] = mean
    output_dictionary["2ndmom"] = second_moment
    output_dictionary["var"] = variance
    output_dictionary["sdv"] = standard_deviation
    output_dictionary["med"] = median
    output_dictionary["mode"] = mode

    return output_dictionary 

# It will be convenient to just input a dictionary of dictionaries for which each key's value is the frequency of that key, 
# and output a dictionary with the same keys, but the values replaced by the _relative_ frequency of its key.

def basic_stats(meta_dictionary):
    output_dictionary = {}
    for k in meta_dictionary.keys():
        output_dictionary[k] = dictionary_statistics(meta_dictionary[k])
    return output_dictionary

def dists(meta_dictionary):
    output_dictionary = {}
    for k in meta_dictionary.keys():
        output_dictionary[k] = dictionary_statistics(meta_dictionary[k])["dist"]
    return output_dictionary

# We may want to display the data in a readable format, etc. 
# The next bit of code is convenient. 
# We assume the input is a dictionary of dictionaries whose values are all either floats or integers.

def tabulate(meta_dictionary):
    type_indicator = 1 # 1 means all values are integers; 0 means some are floats.
    for v in meta_dictionary.values():
        for w in v.values():
            if type(w) == float:
                type_indicator *= 0
    if type_indicator == 1:
        return pd.DataFrame.from_dict(meta_dictionary).fillna(0).apply(np.int64) # Fill empty cells with 0. Not really necessary, but anyway. np.int64 is probably overkill as well.
    if type_indicator == 0:
        return pd.DataFrame.from_dict(meta_dictionary).fillna(0).apply(np.float64) # Fill empty cells with 0. Not really necessary. np.float64 is probably overkill.




