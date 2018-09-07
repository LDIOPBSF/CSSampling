# Sequential Pattern Sampling with Norm Constraints

The CSSampling repository contains the materials concerning our paper : Sequential Pattern Sampling with Norm Constraints. There are essentially three folders and six python files.
- Data : contains the synthetic datasets built with the IBM Generator.
- Samples : contains some results of the output sampling with the synthetic datasets
- DistributionMotifsFrequence : contains the experimental results of the distribution of the patterns produced by CSSampling according to frequency
- The python files are the project code
- cmdrun.txt contains the command line to use when you want to run the application

# Abstract
In recent years, the field of pattern mining has shifted to user-centered methods. In such a context, it is necessary
to have a thigh coupling between the system and the user where mining techniques provide results at any time or within a short
response time of only few seconds. Pattern sampling is a nonexhaustive method for instantly discovering relevant patterns that
ensures a good interactivity while providing strong statistical guarantees due to its random nature. Curiously, such an approach
investigated for itemsets and subgraphs has not yet been applied to sequential patterns, which are useful for a wide range of mining
tasks and application fields. In this paper, we propose the first method for sequential pattern sampling. In addition to address sequential data, the originality of our approach is to introduce a constraint on the norm to control the length of the drawn patterns
and to avoid the pitfall of the “long tail” where the rarest patterns flood the user. We propose a new constrained two-step random
procedure, named CSSampling, that randomly draws sequential patterns according to frequency with an interval constraint on the norm. We demonstrate that this method performs an exact sampling. Moreover, despite the use of rejection sampling, the experimental study shows that CSSampling remains efficient and the constraint helps to draw general patterns of the “head”. We also illustrate how to benefit from these sampled patterns to instantly build an associative classifier dedicated to sequences. This classification approach rivals state of the art proposals showing the interest of constrained sequential pattern sampling.

# Keywords
Pattern Mining, Pattern Sampling, Sequential Data
