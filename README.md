## Analysis of Euclid's Algorithm

<a id='introduction'></a>
### § 1. Introduction

<sup>Jump to: ↓ [Some plots](#pictures) | ↓ [Table of Contents](#toc) </sup>

Euclid's algorithm "might be called the grandaddy of all algorithms", as Knuth aptly put it [[5]](#references). Countless modern-day students know the joy of performing the algorithm by hand, essentially in the form set down by Euclid in his _Elements_ over two thousand years ago. Analyses of the algorithm go back as far as the 18th century, when it was understood (at least implicitly) that consecutive Fibonacci numbers give rise to the worst-case in terms of the number of divisions performed, relative to the size of the inputs. Average-case analyses and finer points received surprisingly little attention until the latter half of the last century. (See Knuth [[5]](#references) and Shallit [[9]](#references) for superlatively detailed accounts of the algorithm's fascinating history.) Only in recent decades has Euclid's algorithm been put into a general framework for the analysis of algorithms (by Baladi and Vallée [[1]](#references) et al.), in which certain algorithms are viewed as dynamical systems: the mathematics is as beautiful as it is deep. Although the current state-of-the-art paints a fairly detailed picture with respect to the distributional analysis of Euclid's algorithm, it still tantalises us with open questions, and these questions remain focal points of some exciting research programmes. 

![SegmentLocal](images/euclid_steps_distribution_loop.gif)

Indeed, one of our goals here is to shed some light (numerically) on a certain "obscure" constant that arises in the analysis of Euclid's algorithm. Our main goal, though, is simply to demonstrate how fun and instructive it can be to study introductory discrete mathematics and statistics alongside basic Python. We'll code Euclid's algorithm, apply it to almost five billion pairs of integers to produce some data, then tabulate and visualise the results (the above animation is just one example). Along the way, we'll discuss the Fibonacci numbers and touch on **dynamic programming**, among other things like **random walks**... [Libraries](#libraries) we'll use include **NumPy**, **SciPy**, **Matplotlib**, and **pandas**. 

There are various ways of analysing Euclid's algorithm. Here is one example. Let $X$ be the random variable whose value is the number divisions performed in the computation of $\gcd(a,b)$ via Euclid's algorithm, with $(a,b)$ chosen uniformly at random from the region $1 \le b < a \le N$. It is known that $X$ is asymptotically normal (as $N \to \infty$), with mean close to $\lambda\log N + \nu - \frac{1}{2}$ and variance close to $\eta\log N + \kappa$, for certain constants $\lambda, \nu, \eta, \kappa$. While the constants associated with the mean can be written in closed form and easily calculated to any desired degree of accuracy ($\lambda = 0.8427659\ldots$ and $\nu = 0.0653514\ldots$), those associated with the variance cannot. Nevertheless, $\eta$ and $\kappa$ are polynomial-time computable, and the first seven digits of $\eta$ have been determined: $\eta = 0.5160524\ldots$. The "subdominant" constant $\kappa$ is even more mysterious, and our numerics will lead us to guess an approximate value for it (we believe it is around $-0.1$). 

In the above animation, the distribution of $X$ is shown for various $N$ up to $10^5$ (starting with $N = 1000$ and going up by $1000$ in each frame). The large blue dots give the probability that $X$ equals a given number on the horizontal axis. The dotted blue curve is normal with mean $\mu = \mathbb{E}[X]$ and variance $\sigma^2 = \mathrm{Var}(X)$, while the light blue curve is normal with mean $\mu_* = \lambda\log N + \nu - \frac{1}{2}$ and variance $\sigma_*^2 = \eta \log N - 0.1$. The red dots and curves are analagous, but only coprime pairs $(a,b)$ are considered. See [Two-dimensional analysis: distribution](#2d-distribution) for more detail and context.

<a id='pictures'></a>
#### Some plots

<sup>Jump to: ↑ [§ 1. Introduction](#introduction) | ↓ [Table of Contents](#toc)</sup>

Is this a _random walk?_ See [One-dimensional analysis: mean and error term](#1d-investigation-mean) for the answer.

![SegmentLocal](images/sum_sign_error_term_porter_1000.png)

See [One-dimensional analysis: mean and error term](#1d-investigation-mean) for the context of this instance of _square-root-cancellation_.

![SegmentLocal](images/error_term_porter_650.png)

See [One-dimensional analysis: variance](#1d-investigation-variance) for more about the next two plots.

![SegmentLocal](images/second_moment_1d_1000.png)

![SegmentLocal](images/variance_error_1d_1000.png)

See [One-dimensional analysis: distribution](#1d-investigation) for an explanation of the animation below.

![SegmentLocal](images/euclid_steps_distribution_1d_10001_loop.gif)

See [Two-dimensional analysis: error terms & subdominant constant in the variance](#2d-investigation) for an explanation of the plots below.

![SegmentLocal](images/error_term_in_mean_and_variance_no_constant_100000.png)

<a id='toc'></a>
#### Table of Contents

<sup>Jump to: ↑ [Some plots](#pictures) | ↓ [Libraries](#libraries) </sup>

 § 1... [Introduction](#introduction) [Maths/Visuals] <br>
 ............... [Some plots](#pictures) [Visuals] <br>
 § 2... [Libraries](#libraries) [Code] <br>
 § 3... [A quick recap of the GCD and Euclid's algorithm](#definitions) [Maths]<br>
    ............... [Code for Euclid's algorithm](#codeEuclid) [Code] <br>
 § 4... [Worst-case analysis](#worst-case) [Maths/Code] <br>
    ............... [The Fibonacci numbers and dynamic programming](#fibonacci) [Code] <br>
 § 5... [Constants](#constants) [Maths/Code] <br>
 § 6... [One-dimensional analysis](#1d-analysis) [Maths] <br>
    ............... [Average-case analysis](#1d-average-case) [Maths] <br>
    ............... [Error term, variance, and distribution](#1d-higher-moments) [Maths] <br>
 § 7... [Two-dimensional analysis](#2d-analysis) [Maths] <br> 
    ............... [Average-case analysis](#average-case) [Maths] <br>
    ............... [Variance and distribution](#distribution) [Maths] <br>
 § 8... [Code for analysing Euclid's algorithm](#code-for-analysing) [Code] <br>
 § 9... [Generating and exporting/importing the raw data](#raw-data) [Code] <br>
 § 10... [Numerical investigation & data visualisation](#numerical-investigation) <br>
     ............... [One-dimensional analysis: distribution](#1d-investigation) [Maths/Code/Visuals] <br>
     ............... [One-dimensional analysis: mean and error term](#1d-investigation-mean) [Maths/Code/Visuals] <br>
     ............... [One-dimensional analysis: variance](#1d-investigation-variance) [Maths/Code/Visuals] <br>
     ............... [Two-dimensional analysis: error terms & subdominant constant in the variance](#2d-investigation) [Maths/Code/Visuals] <br>
     ............... [Two-dimensional analysis: distribution](#2d-distribution) [Maths/Code/Visuals] <br>
[References](#references) 

<a id='libraries'></a>
### § 2. Libraries

<sup>Jump to: [Table of Contents](#toc) | ↓ [A quick recap of the GCD and Euclid's algorithm](#definitions)</sup>

```python
# We'll use the following libraries (by the end of this Notebook).

import numpy as np # Naturally, we'll need to do some numerics.
import pandas as pd # We'll want to put data in data frames to import and export it, and to display it nicely.
from timeit import default_timer as timer # We'll want to see how long certain computations take.
import scipy.stats as stats # We'll want to plot normal curves and so on.
from scipy.optimize import curve_fit # We'll want to do some curve-fitting.
from scipy.special import zeta # For certain constants involving the Riemann zeta function.
import matplotlib.pyplot as plt # We'll want to plot our data.
from matplotlib import animation # We'll even make animations to display our data.
from matplotlib import rc # For animations.
from IPython.display import HTML # For displaying and saving animations.
from matplotlib.animation import PillowWriter # To save animated gifs.
```

<a id='definitions'></a>
### § 3. A quick recap of the GCD and Euclid's algorithm

<sup>Jump to: [Table of Contents](#toc) | ↑ [Libraries](#libraries) | ↓ [Code for Euclid's algorithm](#codeEuclid)</sup>

---
**Proposition 3.1.** Let $a,b \in \mathbb{Z}$. There exists a unique nonnegative $g \in \mathbb{Z}$ such that, for any $d \in \mathbb{Z}$, $d \mid a$ and $d \mid b$ if and only if $d \mid g$. 

---
**Definition 3.2.** The integer $g$ is the _greatest common divisor_ of $a$ and $b$, denoted $\gcd(a,b)$. The common divisors of $a$ and $b$ are precisely the divisors of $\gcd(a,b)$.

---
The divisors of $g$ are the divisors of $-g$, so $-\gcd(a,b)$ satisfies the definition of greatest common divisor sans nonnegativity. Were we to generalize the notion of gcd to commutative rings, we would say that $g$ is _a_ gcd of $a$ and $b$ if the common divisors of $a$ and $b$ are precisely the divisors of $g$. Then, coming back to the integers, we would say that $g$ and $-g$ are both gcds of $a$ and $b$, but that gcds (in $\mathbb{Z}$) are unique _up to multiplcation by a unit_ ($\pm 1$).

Note that, for all $a \in \mathbb{Z}$, $\gcd(a,0) = |a|$ as all integers divide $0$ (hence the common divisors of $a$ and $0$ are the divisors of $a$). In particular, $\gcd(0,0) = 0$.

How can we compute $\gcd(a,b)$ when $a$ and $b$ are nonzero?

**Euclid's algorithm.** If $b \ge 1$, the division algorithm gives unique integers $q$ and $r$ such that $a = qb + r$ and $0 \le r < b$. It is straightforward to verify that the common divisors of $a$ and $b$ are precisely the common divisors of $b$ and $r$. Hence $\gcd(a,b) = \gcd(b,r)$. If $r > 0$ we may apply the division algorithm again: $b = q_2r + r_3$ with $0 \le r_3 < r$ and $\gcd(b,r) = \gcd(r,r_3)$. Repeating the process as many times as necessary, we obtain a sequence 

<a id='eq:rem_seq'></a>
$$a = r_0, b = r_1 > r = r_2 > r_3 > \cdots > r_n > r_{n + 1} = 0 \tag{3.1}$$ 

with the property that $\gcd(r_{i-1},r_{i}) = \gcd(r_{i},r_{i + 1})$ for $i = 1,\ldots,n$, because

<a id='eq:rem_seq2'></a>
$$r_{i - 1} = q_ir_i + r_{i + 1} \quad (i = 1,\ldots,n). \tag{3.2}$$

But $\gcd(r_n,r_{n + 1}) = \gcd(r_n,0) = r_n$, and so in this way we find the gcd of $a$ and $b$ (and of $\gcd(r_{i},r_{i + 1})$ for $i = 1,\ldots,n$). The case $b \le -1$ is similar, but instead of $(3.1)$ we have

<a id='eq:rem_seq_neg'></a>
$$a = r_0, b = r_1 < r_2 < r_3 < \cdots < r_{n} < r_{n + 1} = 0 \tag{3.3}$$

and $\gcd(a,b) = -r_n$. However, since $\gcd(a,b) = \gcd(|a|,|b|)$, we will typically assume that $a$ and $b$ are nonnegative.

---
**Definition 3.3.** Given $a,b \in \mathbb{Z}$, let $T(a,b) = n$ with $n$ as in [$(3.1)$](#eq:rem_seq) (if $b \ge 0$) or [$(3.3)$](#eq:rem_seq_neg) (if $b \le 0$). Thus, $T(a,b)$ is the number of "steps" or "divisions" in Euclid's algorithm for computing $\gcd(a,b)$. 

---

<a id='codeEuclid'></a>
#### Code for Euclid's algorithm

<sup>Jump to: [Table of Contents](#toc) | ↑ [A quick recap of the GCD and Euclid's algorithm](#definitions) | ↓ [Worst-case analysis](#worst-case)</sup>

```python
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
```
```python
# Try out some of the above code.

write_euclid(1011,69)
```
```
1011 = 14*69 + 45 	 ∴ gcd(1011,69) = gcd(69,45)
  69 =  1*45 + 24 	 ∴   gcd(69,45) = gcd(45,24)
  45 =  1*24 + 21 	 ∴   gcd(45,24) = gcd(24,21)
  24 =  1*21 +  3 	 ∴   gcd(24,21) = gcd(21,3) 
  21 =  7* 3 +  0 	 ∴    gcd(21,3) = gcd(3,0)  

gcd(1011,69) = 3, T(1011,69) = 5
```

```python
write_euclid(-1011,-69)
```

```
-1011 = 14*(-69) - 45 	 ∴ gcd(-1011,-69) = gcd(-69,-45)
  -69 =  1*(-45) - 24 	 ∴   gcd(-69,-45) = gcd(-45,-24)
  -45 =  1*(-24) - 21 	 ∴   gcd(-45,-24) = gcd(-24,-21)
  -24 =  1*(-21) -  3 	 ∴   gcd(-24,-21) = gcd(-21,-3) 
  -21 =  7* (-3) +  0 	 ∴    gcd(-21,-3) = gcd(-3,0)   

gcd(-1011,-69) = 3, T(-1011,-69) = 5
```

<a id='worst-case'></a>
### § 4. Worst-case analysis

<sup>Jump to: [Table of Contents](#toc) | ↑ [Code for Euclid's algorithm](#codeEuclid) | ↓ [The Fibonacci numbers and dynamic programming](#fibonacci)</sup>

First let's record a result that will be useful in the sequel.

---
<a id='prop:4.1'></a>
**Proposition 4.1.** We have the following for $a \ge b \ge 1$. <br>
(a) $T(a,b) = 1$ if and only if $b \mid a$. <br>
(b) If $a > b$, $T(b,a) = T(a,b) + 1$. <br>
(c) For all positive integers $d$, $T(da,db) = T(a,b)$.

---
>_Proof._ (a) Simply note that $b \mid a$ if and only if there exists an integer $q$ such that $a = qb + 0$.
>
>(b) If $1 \le b < a$ then the first two divisions of the Euclidean algorithm for $\gcd(b,a)$ are: $b = 0a + b$ and $a = qb + r$, $0 \le r < b$. The second division is the first done in the Euclidean algorithm for $\gcd(a,b)$.
>
>(c) If [$(3.1)$](#eq:rem_seq) is the remainder sequence given by Euclid's algorithm for $\gcd(a,b)$, then for any positive integer $d$, 
>
>$$da = dr_0, db = dr_1 > dr_2 > \cdots > dr_n > dr_{n + 1} = 0$$
>
>is the remainder sequence given by Euclid's algorithm for $\gcd(da,db)$ (the quotients $q_i$ in [$(3.2)$](#eq:rem_seq2) won't change).
