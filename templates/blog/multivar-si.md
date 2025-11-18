# crushing state-of-the-art in state inconsistency bug analysis

wrote a paper this semester that does the work of state-of-the-art dynamic SI detectors but without expensive multiplex symbolic execution and SMT. i'll break it down in simple terms without spoiling our (best) detector -- we need to sell a product after all.

smart-contract security detectors have historically taken 2 paths:

1. shallow static scans that catch **surface-level issues only**
2. heavy dynamic engines powered by MSE, fuzzing, or SMT solvers that **formally prove valid issues** but take forever

this semester, we decided to achieve perf present in (2), but with (1). and it worked.

here is a benchmark of our results compared to other tools on the market.

<< to be continued >>