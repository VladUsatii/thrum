# 1CPU1V vs. 1P1V


#### Published Sun Nov 30 2025
----

Satoshi's [Bitcoin](https://bitcoin.org/bitcoin.pdf) reduced reliance on [institutional trust](https://www.bankofengland.co.uk/-/media/boe/files/news/2008/october/recapitalisation-of-the-uk-banking-system.pdf) by making [protocol validity](https://bitcoin.stackexchange.com/questions/78148/how-is-bitcoin-governed-by-mathematics) publicly verifiable under shared consensus rules. [Social control over money](https://files.libcom.org/files/Seeing%20Like%20a%20State%20-%20James%20C.%20Scott.pdf) depends on which institutions can render transactions and counterparties legible and enforceable, and on the interfaces through which users access monetary utility. I formalize this as a capability [partial order](https://dspace.mit.edu/bitstream/handle/1721.1/104426/6-042j-spring-2010/contents/readings/MIT6_042JS10_chap07.pdf) over monetary regimes and a graph-theoretic coercion bound. Under mild concentration and interface-dependence assumptions, a state can achieve high suppression of targeted monetary uses by applying [coercion to a small set of identifiable nodes](https://www.stlouisfed.org/publications/review/2023/02/03/tornado-cash-and-blockchain-privacy-a-primer-for-economists-and-policymakers) without owning the asset or dominating consensus. The government has a monopoly on legitimacy of force, which raises eyebrows when something claimed to be "socially robust" lands on the market in the form of digital signatures and proof-of-work consensus.

Bitcoin was designed so you don't need centralized banks to vouch that a payment is real. Instead, a peer-to-peer network like Bitcoin Core accepts the history (a global ledger) with the most accumulated proof-of-work. This creates a generalization we can use in economic theory, namely the idea of ["1 CPU 1 vote."](https://bitcoin.stackexchange.com/questions/5638/what-is-the-motivation-behind-one-cpu-one-vote-rule)

In real life, money outcomes are enforced through courts, police, taxes, licenses, firm regulation, and even top-secret campaigns intended to round up people of influence in times of severe state impact.

![my photo](/static/blog/Reserve-Index.jpg)

> See Section A of the Reserve Index: people to be rounded up in times of national emergency that may have more impact than those with state power.

The modern state is commonly [defined](https://www.balliol.ox.ac.uk/sites/default/files/politics_as_a_vocation_extract.pdf) by its claim to the legitimate physical force used over a designated territory. So even if a transaction is valid on-chain, what matters socially is whether it is usable off-chain in a pseudonymous manner while leaving no paper trail or analytic surface for the state to capture.

Most people reach cryptocurrencies through [identifiable interfaces](https://coinmarketcap.com/rankings/exchanges/) like centralized, regulated crypto exchanges and custodians, payment processors, stablecoin issuers, and infrastructure providers. Regulation and sanction frameworks target these sectors, which tend to accumulate the majority of crypto ownership, rather than trying to rewrite or attack the base protocol and its deployments/issuing parties.

What is a capability partial order over monetary regimes?

I define "who wins" by comparing compatibilities like

1. Who sets the dominant unit prices are quoted in.
2. Who can legally finalize and undo obligations.
3. Who can compel tax and fee payments.

This produces the notion of a **partial order**. That is, regime \\(A\\) is stronger than \\(B\\) if \\(A \geq B\\) on all chosen capabilities. Formally:

\\[
\text{Let } \mathcal{R} \text{ be a set of monetary regimes.}
\\]

\\[\text{ Choose } k \text{ capabilities (e.g., unit-of-account control, legal finality, interface censorship). } \\]

\\[\text{ Define a capability map } C: \mathcal{R} \to \{0,1\}^k \text{ (or }[0,1]^k\text{ for degrees).}
\\]

\\[
\text{Define a partial order } \succeq \text{ on regimes by:}
\\]

\\[
A \succeq B \;\Longleftrightarrow\; \forall i \in \{1, \dots, k\},\; C_i(A) \ge C_i(B).
\\]

\\[
\text{Then } A \text{ is “at least as powerful as” } B \text{ w.r.t. }  \mathcal{R}.
\\]


Let's extend this even more.

Treat the whole crypto economy as a network graph.

```
Users --> Services --> Utility
```

A coercion bound says that if the network is concentrated at a few key nodes, which Satoshi said already happened in his most recent, seemingly unverified communications, then a government can get large control effects by pressuring only the few nodes with the most network capture. They can do this without [owning a significant portion of the asset](https://en.wikipedia.org/wiki/U.S._Strategic_Bitcoin_Reserve) or controlling consensus.

The tension I aim at in this article is that Bitcoin *can be robust* at validating blocks and signatures mathematically via a "protocol invariant," but society runs on *binding enforcement against people and firms,* an omniscient legal truth with more capture than a distributed, trustless protocol. The state's coercive and legal toolkit applies to the interface layer even when the protocol is permissionless, trustless, and implies freedom within its usage and applications.

In this article, I plan to expose why Bitcoin failed socially and how a better money can be made in the future.

## Separating protocol validity from monetary finality

A Bitcoin transaction answers the question:

> Given a public set of rules, is this state transition function valid?

A monetary transaction in traditional society poses differently:

> Will this state transition bind together real agents, survive security and administrative disputes, and remain spendable across the interfaces converting asset ownership into life outcomes?

The gap between these questions is in the mismatch between voting mechanisms. Satoshi posed 1 CPU 1 vote and the federal government poses 1 person 1 vote. 1CPU1V is unique in that ordering and inclusion in the ledger are decided by who generates the most hashes, thereby using the most compute. This is done within a protocol-defined validity region and any attempts at using that value statement outside of the network poses as a useless mathematical puzzle. Within the federal government, 1P1V dominates. It is the idea that obligations and life outcomes are determined by institutions who have the ability to compel behavior, adjudicate disputes, and attach penalties to rigorously defined, ultimate social identities.

Bitcoin's security model is formal. If you follow the rules which govern every CPU, you can verify and append to the ledger. But money isn't only a ledger. It is a system of enforceable obligations embedded in law, social identity and construct, and our institutions. Validity of a hash is necessary for a cryptosystem dealing with finances and proof-of-work, but it isn't sufficient for a monetary regime which enforces inescapably.

On-chain signatures and off-chain work can simultaneously be mathematically final and socially non-final. Socially, nobody *has* to accept the interface, custody funds, and convertibility. If you want a sound monetary system that doesn't rely on centralized institutions, you can't stop at consensus.

## Censorable interfaces

Let's sidetrack to discuss what interfaces are shaped like in my model. This path leads a user from a private key to utility:

```
Key custody --> connectivity --> liquidity & conversion --> unit of account --> settlement & compliance --> dispute and enforcement
```

* **Key custody**. Self-custody, e.g. writing your private and public keys on a sheet of paper and hiding it so that nobody can find it in a feasible period of time, is the only available solution to irrevocable self-ownership. Hosted wallets, exchange custody, brokerage custody, and even atomic swaps still touch layers that are censorable to the extent of the law.
* **Connectivity**. Wallet software, node providers, RPC endpoints, and relays are all stalkable and in some cases, writeable and routable by authorities.
* **Liquidity and conversion**. On and off-ramps, exchanges, OTC desks, payment processors. These are all recognized by traditional finance outlets and thus are heavily governed by the state, both in price and in utility.
* **Unit of account**. Wages, taxes, rent, legal damages, accounting standards. As long as payments are made anonymously, this interface remains pseudonymous. But as long as nodes are censored from risk to be OPAC compliant, the cryptocurrency ecosystem remains heavily skewed towards centralized regulatory capture.
* **Settlement and compliance**. Banks, card networks, stablecoin issuers, and merchant acquirers, all of which can be assumed to have full centralized regulatory capture.
* **Dispute and enforcement**. Cryptocurrency transactions are mediated logically by "who sent what and when and who accepted the transaction as legible."

Bitcoin removes the need for bank approval to avoid the double-spending problem, but it doesn't remove the need for an ownership-utility route - which is never pure peer-to-peer all the way down due to the attribute of rivalry. ThePirateBay, for instance, is non-rivalrous: if I have a book and I give you the book, I still have the book. Bitcoin is rivalrous: if I have 1 satoshi and I give you 1 satoshi, I have 0 satoshis and you have 1 new satoshi. Due to Bitcoin's rivalrous nature, some portion of the path from private key to utility involves a mediated, legible, and governable layer. Recall that money is also a kind of game with its own set of unique rules, unlike a distributed p2p network like ThePirateBay.

There is a clean split between the protocol layer and the interface layer: validity, consensus, and data are separate from identity, convertibility, permissionful usability, and enforceability.

You can have a permissionless protocol sitting under a permissioned interface stack, giving the illusion of pure pseudonymity, privacy, and utility. To achieve the best configuration, users must (a) mine their own coins, (b) self-custody, (c) transact privately or through back-channels when converting to fiat, and (d) obtain stable, spendable utility (if currency remains native) without touching regulated chokepoints.

<0.1% of users can enact the scenario listed above without an interface. So far, the protocol reeks of insecurity.

## Capability partial order

What does "stronger" mean?

We defined a comparison of regimes across their respective capabilities. Let's build on our abstract ideas with rigor:

Let the capability vector \\(C\\) be defined as

\\(C(R) = (C_{\text{unit}}(R), C_{\text{final}}(R), C_{\text{tax}}(R), C_{\text{license}}(R), C_{\text{censorship}}(R), C_{\text{surveillance}}(R), C_{\text{seizure}}(R))\\),

where each component maps cleanly to \\([0,1]\\), representing the monetary regime's ability to do the named action at scale. I use the term "scale" hand-wavey to mean "at a considerably large magnitude within its operational bounds." For the federal government, this means enacting the above to its population. For cryptocurrency, this means enacting the above to its constituents and actors.

Some examples of each term:

* \\(C_{\text{unit}}\\): can make price and debt denominate in the regime's unit (unit-of-account)
* \\(C_{\text{final}}\\): can finalize or undo obligations via law (legal finality)
* \\(C_{\text{tax}}\\): can compel payments to itself (tax)
* \\(C_{\text{censorship}}\\): can block targeted usage (censorship)
* \\(C_{\text{surveillance}}\\): can map flow to identity (legibility)
* \\(C_{\text{seizure}}\\): can seize or freeze assets (seizure)

Then the following formalizes a more realistic situation, namely that regimes are often comparable:

\\[
A \succeq B \;\Longleftrightarrow\; \forall i \in \{1, \dots, k\},\; C_i(A) \ge C_i(B).
\\]

Bitcoin can be larger on protocol finality while being smaller on tax, license, or seizure at scale. The state regime is larger on enforceability and identity-binding as they have both a monopoly on social control, physical violence, and justice. Bitcoin is a strong regime for validity, but the state is a strong regime for binding outcomes.

So who wins? The actual question to ask: on which coordinates do real outcomes depend? My answer? Most outcomes depend on the state.

## The crypto economy: a graph-theoretic spin

Model the economy as a directed graph.

Nodes \\(V\\) as entities (users, exchanges, custudians, merchants, employers, banks, bridges to real-world utility). Directed edges \\(M: u \leadsto v\\) mean that \\(u\\) can route value through \\(v\\) in the form of access, settlement, service, or liquidity. \\(u\\) can be a user from a subset of users and \\(v\\) can be a utility sink from a subset of utility sinks (e.g. merchants, payroll, banks).

A user has monetary utility if there exists a directed path from \\(u\\) to \\(v\\).

Let \\(T \subseteq U\\) be targeted users/use patterns. The state applies coercion at nodes \\(S \subseteq V\\) by forcing \\(s \in S \subseteq V\\) by forcing those nodes to deny service to \\(T\\), to then report, freeze, or break them.

Define a suppression ratio \\(\text{Supp}(S, T) = 1 - \frac{|{t \in T: \exists t \leadsto w \text{ in } G \backslash S}|}{|T|} \\), so \\(\text{Supp} = 1\\) is perfect suppression, where targeted users/use patterns can't reach utility without crossing coerced or censored nodes.

| A quick graph theory primer |
| - |
| A minimum separation cut \\(\kappa(A, B)\\) is any set of edges whose removal makes it impossible to reach any node in \\(B\\) from any node in \\(A\\) by any path in the graph. \\( \kappa (A, B) = \min\\{ \|C\| : C \text{ separates } A \text{ and } B \\} \\). In other words, it is the smallest number of edges you must remove to completely block every path from any node in \\(A\\) to any node in \\(B\\). |

Define the minimum separation cut between \\(T\\) and \\(W\\): \\( \kappa(T, W) = \min\\{ \| S \| : \text{removing } S \text{ breaks all paths } T \leadsto W\\}\\), so the smallest set of intermediaries whose coercion disconnects targeted users from utility in the real world. If we plug in different values and graph representations, we can deduce that \\( \text{if } \kappa(T, W) \text{ is small, coercion is cheap} \\).

With all of this in mind, we can now set up the scenario where the economy routes through a small number of high-betweenness intermediaries, such as exchanges, custodians, processors, RPCs, banks, which then leads to \\(\kappa(T,W)\\) collapsing into a handful of nodes. Coercion produces a control effect and the "interface layer dominates."

Finally, lets define a concentration parameter for the interface layer, where a tiny \\( \phi \\) means a tiny fraction of the ecosystem can be coerced to block a large fraction of utility routes:

\\[ \phi = \frac{\kappa(U, W)}{\| V \|} \\]

One key point: Bitcoin Core remains untouched while \\(\phi \text{ ~ } 0 \\) because the concentration is not at the protocol layer. Rather, it is at the access and settlement layer. You can then view decentralization as a spectrum and view the attack surface through a minimum separation cut set.

## Unwrapping interface dominance

A few things to consider before I continue:

* A protocol can be uncensorable as a ledger while being censorable as money if utility routes pass through a small number of coercible intermediaries.
* Treat “spendability” as a routing problem on a graph representing our previously-defined interfaces, and treat “state pressure” as removing a small set of nodes from the graph.
* For a monetary regime \\(R\\), I build a directed graph \\(G_R=(V,E)\\) where nodes \\(V\\) are users, services, and utility endpoints and edges \\(u \to v\\) represent routing value via access, settlement, conversion, and services.
* Let's create a super-source \\(s: \text{a typical user holding value}\\) and a super-sink \\(t: \text{a real world utility}\\).
* Put capacities on edges to represent throughput or substitutability. Alternatively, we can simply set \\(1\\) for every independent way to get utility instead of using complicated capacities.

Now we can do a few things:

Define the baseline utility capacity of a regime to be:

\\[
    F_R := \operatorname{maxflow}(G_R, s, t)
\\]

> The best an economy can route value from ```users --> utility``` given its current interface structure.

Let coercible nodes \\(C\subseteq V\\) be specified as identifiable, jurisdictionally reachable institutions that can be compelled to deny a service.

Assign each \\(v \in C\\) a coercion cost \\(w(v) \ge 0\\). If you want the simplest model, \\(\forall \text{ coercible institutions, } w(v) = 1\\).

Given a coercion set \\(S\subseteq C\\), define the residual utility:
\\[
F_R(S) := \operatorname{maxflow}(G_R\setminus S, s,t)
\\]

Define suppression as \\( \sigma_R(S) := 1-\frac{F_R(S)}{F_R} \\).

Now I introduce the state's optimization problem:

Given a coercion budget \\(B\\), the state chooses:
\\[
S_R^\*(B)\in \arg\min_{S\subseteq C}\ F_R(S)\quad \text{s.t.}\quad \sum_{v\in S} w(v)\le B.
\\]

> A network interdiction where an attacker removes nodes and the network reroutes flow.

Define the minimum coercible vertex cut cost:

\\[
\kappa_C(R) := \min\Big\\{\sum_{v\in S} w(v)\ :\ S\subseteq C,\ \text{removing }S\text{ disconnects }s\text{ from }t\Big\\}.
\\]

> The cheapest set of coercible institutions that can fully block typical users from reaching utility when under pressure.

| **Interface Dominance Theorem** |
| - |
| If \\(\kappa_C(R)\\) is small, then there exists a small, identifiable coercion set \\(S\\) that achieves near-total suppression of monetary utility—even if the base protocol remains permissionless and consensus is not dominated. |

| **Corollary** |
| - |
| In the unweighted case \\(w(v)\equiv 1\\), \\(\kappa_C(R)\\) equals the maximum number of internally vertex-disjoint \\(s \leadsto t\\) paths through the interface graph: i.e., the number of independent institutional escape routes. |

Social robustness can then be seen as how large the coercible cut between users and utility is.

## How this ties to Effective Monetary Autonomy

A bit of economics is needed to grasp the graph-theoretic formulation of routing I've laid out. In fact, one can even argue that a theorem needs a dial. EMA is the proverbial dial, measuring how quickly real monetary utility collapses as coercion budget increases.

## Owning Bitcoin ⊭ controlling outcomes

2 control channels dominate in Bitcoin, and more generally, the cryptocurrency ecosystem:

1. Consensus control. That is, the ability to reorder, censor, and rewrite the chain.
2. Utility control. The ability to block conversion, freeze balances, sanction use patterns, seize endpoints, impose KYC, and deny settlement of funds.

Bitcoin hardens its protocol channel against unilateral control, but the state dominates the utility channel via law and legitimacy. A state can therefore be framed as the layers above the protocol, sometimes framed as L1, L2, and L3. A state wins without owning the asset, controlling the mining, rewriting and creating shared consensus over the protocol, or even understanding the protocol (apart from its nodes). As shown in graph-theoretic terms, a government simply demands a small \\(\kappa(T, W)\\) and enough widespread legitimacy to coerce. Even perfect censorship resistance at L1 doesn't imply utility in the real economy.

## Bitcoin failed?

Failed does not mean that the protocol broke, was hacked, or the price fell to 0. Rather, it didn't deliver robust monetary autonomy for the typical user under realistic interface dependence. Bitcoin failed socially when the coercion bound became small. In such a world, the protocol is permissionless and trustless, usable access becomes permissioned and sanctioned, and privacy becomes stigmatized, outlawed, or expensive at the interface.