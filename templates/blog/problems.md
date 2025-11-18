# Current problems in crypto security

Thank you to [] and [] for your help with this article. Your ongoing support means the world to me as I build this business from the ground up.

Current Web3 infrastructure is buggy, slow, and incredibly hard to follow. One simple thought experiment to prove this line of reasoning:

* Consider you have Token A.
* You want to stake it with the ability to be rewarded money from a Pool with Token B.
* Token B may run out, so you have an overflow that spills into Token C.
* Token C must be "yanked" from Account N.
* If Account N doesn't have sufficient Token C, it must be taken out of Account M.
* If Token A is proven not to be staked, or the staking was "cheated," there must be robust resolution mechanisms to handle the flow of undeserved fortunes.

The number of guards, requires, possible timing exploits (from Pool drips), and mix-and-match confusion derived from such a setup is beyond the scope of most crypto security companies. Most autonomous audit software doesn't have sufficient resources to monitor the every which way that an attack surface may be found. Many research articles *do* exist, though, which brings us..

..to some structural bugs (and features) in the world of crypto.

### Cross-domain state

Bridges and oracles are the new systemic single-point-of-failure for the majority of modern protocols. Crypto is no longer one-chain, one-state. As much as I hate generalizing to large swaths of the ecosystem, almost everything now spans L1-to-L2 rollups, Chain A- to- Chain B bridges, and on-chain protocols- to- off-chain data.

We know from [here](https://dl.acm.org/doi/full/10.1145/3696429) that cross-chain bridges historically produce the largest individual hacks in crypto. Recent SoK's treat them as systemic risk and not just bad implementations. Cross-chain interoperability articles now frame bridges as high-risk PoF's where mitigation steps can save companies their hard-earned investors' trust and millions of dollars.

[Central banks and regulators are now flagging oracles as system-level risk](https://www.bis.org/publ/bisbull76.pdf), where a failure in DeFi can propagate shocks into TradFi and result in something that we used to deem beyond the pale.

You're trying to maintain cross-domain invariants when each domain has

* different finality
* different validator sets
* different failure modes
* no global consensus
* a bunch of weakly-coupled ledgers

Bridges and oracles are also multi-tenant, so one severe bug could cascade across every protocol and ruin an ecosystem overnight. The threat models here are heterogeneous, so one side might be BFT, the other Nakamoto. One side might roll back final blocks while the other can't.

The invariant you actually care about is global.

A lot of research still treats bridge contracts and oracle feeds as interfaces, not as state machines whose safety conditions need to be proven across various domains.

This hole in a research-focused industry brings us to the biggest problem..

# Tooling can't see the whole machine yet

Most of today's crypto security stack is optimized for local bugs like single-contract reentrancy, access-control misconfigurations, and price-oracle manipulations.

Existing tools target headline bug classes like simple reentrancy, flash loans, and oracle manipulation, while only a minority, and usually cloudy/hard-to-follow papers touch on state-level or cross-chain bugs/failures.

The tooling is also fragmented and not found in **one place.**

Static analyzers like Slither reason about code, but not production flows.

Fuzzers generate traces but don't lift them back into understandable invariants.

Metric monitors don't know why the state machine behaves strangely; they only see investor-friendly numbers like TVL, prices, and liquidation spikes.

And recent research is doing a good job moving towards richer static reasoning, like in the case of detecting transaction conflicts by analyzing state access patterns and variable dependencies, but these tools mostly live in papers without public prototypes, and many big crypto companies don't spare the resources to implement these ground-breaking ideas.

You end up with a really weird paradox:

**the invariants that matter are global and cross-domain, but the tooling is local and siloed.**

Raw detection is no longer the hard part. The community is slowly building new detectors for every bug class in tandem. What *is* scarce is:

* allocated compute for running heavy static and dynamic analyses over realistic codebases, multiple chains, and transaction traces without blowing the budget
* triage to turn hundreds of plausible lightweight, heuristic-based alerts into a set of *N* workable and mitigable issues with documented financial impact.
* the context to connect suspicious patterns in Repo X Contract A to behavior in Repo Y Contract B.

## Thrum

I built this because the bottleneck in crypto security has moved from research to execution at scale. The mission is quite simple:

```
Solve crypto security while delivering workable, research-grade insights on vulnerabilities.
```

This means we must implement and aggregate the world's best detectors while building our own pipelines for the most accurate analysis in the industry. The goal is a unified pipeline where research-grade analyses can be conducted at scale without sacrificing wait-time or latency in the process.

That last sentence implies the need for better hardware and low-level software. Serious security work in crypto is computationally ugly and slow.

* You want to check deep invariants over large state spaces, obviously without state space explosion, but within a reasonable time constraint.
* You want to replay and perturb real transaction histories without sacrificing legibility.
* You definitely want to prove certain safety properties or generate counterexamples without sacrificing security in delivery and responsibility in disclosure.

So as a second-class mission, Thrum will engineer efficient infrastructure:

* GPU-optimized zk/graph compute.
* Batching and amortization.

As a third-class mission, in tandem with our mission of accuracy, Thrum will introduce state-of-the-art reasoning models (TRN and LLM) to better classify bugs, give mitigation steps, answer user confusion regarding a finding, and as a graph-level view over large codebases.

## Let's bring it back

If near-perfect auditing is TradFi's most robust engineering solution, why isn't this true in crypto as well?

Crypto is handling unauthorized, uncleared user flows from pseudonymous parties in ways we should classify trustless, and we haven't built robust solutions to prevent bad actors from exploiting common bug patterns?

It's time for a change, and Thrum is here to deliver the future of crypto security.

### The business model

What are we even selling? Good question you've probably been floating for the last 10 minutes.

We break our plan into 3 parts:

1. Command
2. Understand
3. Expand

During (1), we'll release a CLI tool that runs a large, parallelized suite of detectors. These range from cross-contract, multi-variable state-inconsistency to dynamic exploit generation. Our cloud does the heavy lifting and returns a clean, near-perfect audit of your code using tiny recursive models and large-language-models for legibility and mitigation steps.

(2) and (3) will be announced soon.

< to be continued >