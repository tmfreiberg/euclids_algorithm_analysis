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


