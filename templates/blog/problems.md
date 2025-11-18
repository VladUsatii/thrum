# Current problems in crypto security

Thank you to [] and [] for your help with this article. Your ongoing support means the world to me as I build this business from the ground up.

Current Web3 infrastructure is buggy, slow, and incredibly hard to follow. One simple thought experiment to prove this line of reasoning:

* Consider you have Token A.
* You want to stake it with the ability to be rewarded money from a Pool with Token B.
* Token B may run out, so you have an overflow that spills into Token C.
* Token C must be "yanked" from Account N.
* If Account N doesn't have sufficient Token C, it must be taken out of Account M.
* If Token A is proven not to be staked, or the staking was "cheated," there must be robust resolution mechanisms to handle the flow of undeserved fortunes.

The number of guards, requires, possible timing exploits (from Pool drips), and mix-and-match confusion derived from such a setup is beyond me. I don't have the sufficient resources to monitor the every which way that an attack surface may be found.

This brings us to some structural problems in the world of crypto.

### Cross-domain state

Bridges and oracles are the new systemic single-point-of-failure for the majority of modern protocols. Crypto is no longer one-chain, one-state. As much as I hate generalizing to large swaths of the ecosystem, almost everything now spans L1-to-L2 rollups, Chain A- to- Chain B bridges, and on-chain protocols- to- off-chain data.

We know from [here](https://dl.acm.org/doi/full/10.1145/3696429) that cross-chain bridges historically produce the largest individual hacks in crypto. Recent SoK's treat them as systemic risk and not just bad implementations. Cross-chain interoperability articles now frame bridges as high-risk PoF's where mitigation steps can save companies their hard-earned investors' trust, millions of dollars, and a huge group of angry whales.

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

<< to be continued >>