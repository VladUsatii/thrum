# Labs: Ready for Fusaka

> To learn what Thrum Labs is, consult our [Labs primer](https://thrum.sh/blog/labs).
>
> **This is a Labs build for Enterprise clients only.** The Fusaka detectors below are delivered as a private, Enterprise rule set and integrated with your rollup stack + CI/release gates. They are not enabled by default in the standard Thrum Scan.

![Fusaka upgrade has finalized on-chain](https://pbs.twimg.com/media/G7Lgf5XXoAAMEiV?format=jpg&name=medium)

Congratulations, Ethereum, on completing finalization of the Fusaka upgrade into mainnet. At Thrum, we've conducted pedantic reviews of various EIP's/merges. Research covers the Fulu/Osaka hardfork and its immediate changes that were activated/scheduled inside Ethereum during the last 30 days. We used the Meta-EIP as the inclusion list. Upgrades include:

1. Resource/limit changes
2. Cryptographic primitive additions
3. Blob/data availability economics and networking changes
4. Operator/infra correctness requirements

At Thrum, we build crypto security tools to help protocol developers build faster, safer, and (hopefully) unexploitable code. After taking some time to understand the following EIP's, we've built new tooling in **Thrum Labs** that we can add to Thrum Scan for our Enterprise partners:

- EIP-7594
- EIP-7823
- EIP-7825
- EIP-7883
- EIP-7917
- EIP-7918
- EIP-7934
- EIP-7939
- EIP-7951
- Associated items in EIP-7892, 7642, 7910, 7935.

Let's go over new failure modes for applications, rollups, infra, and auditors that need our immediate tooling:

### Hard caps on worst-case blocks/transactions

* The new transaction gas cap: 16,777,216 (2^24).
* RLP-encoded execution block size cap: 10 MiB + 2 MiB safety margin.
* Default gas limit guidance moves to 60M by default to scale L1 execution.

### Cryptography changes

* New pre-compile P256VERIFY at 0x100
* Fixed gas cost 6900
* Input ABI 160 bytes
* Returns 32-byte 1 on success, empty on fail

### MODEXP changes affecting on-chain cryptography and ZK/RSA verification

* MODEXP input lengths are bounded so that base/modulus/exponent bit-lengths must be ≤ 8192.
* MODEXP minimum rises 200 to 500, and general cost increases to avoid underpricing.

### Blob/data-availability

* Reserve price dynamic: blob base fee is bounded by execution cost, which prevents blob fees from collapsing near-zero when execution fees dominate.
* PeerDAS changes how blob data is disseminated/validated to scale rollup data availability.
* BPO (Blob Parameter Only) forks normalize changing blob schedule params without full forks.

### Consensus predictability

* Deterministic proposer lookahead is precomputed and stored, making proposer schedules reliably derivable for upcoming epochs, enabling certain preconfirmation designs.
* This creates new “trust schedule correctly” requirements.

### General tooling

* JSON-RPC method eth_config exposes current and next-fork configuration, motivated by real incidents causing consensus divergence.
* P2P eth/69 changes: history serving windows and simplified receipts transport removing the bloom field.

## Detectors we added for Fusaka support (Thrum Labs)

Thrum treats Fusaka as a constraint-tightening fork, not an extreme-new-addition fork. Thus, it is simply reducing a lot of extreme cases from earlier versions. In addition, detectors must enforce post-fork reality, not pre-fork assumptions.

Because these are **L2 posting + infra correctness** checks (not just Solidity lint), we are shipping them via **Thrum Labs**: we integrate them into your repo boundaries (batcher/poster, fee model, monitoring, configs), validate with your workflow, and turn them into CI “fork readiness” gates.

Thus, each detector we built is written as:

1. The new failure mode
2. What Thrum detects
3. How it proves it
4. Recommended remediation/mitigation
5. Autonomous heuristics for continuous auditing

These detectors are fork-aware, L2-oriented security/correctness checks that are focused on the boundary between L-1 and -2, specifically within the fields of blob transaction construction, posting economics, and parameter drift handling.

Common questions before you read our spec:

1. Why is this security and not just compatibility checks?

Security in L2's involve liveness security (inability to post or derive data can halt the chain or force an unsafe operating mode), economic security (wrong fee models can be exploited to force the chain into subsidizing posting or experience downtime), and correctness under consensus rules (invalid txs or invalid sidecars cause systemic failure at the posting layer).

2. What *aren't* our goals?

We are not auditing Ethereum implementations. We are also not proving protocol-wide safety. These detectors are risk reducers and fork readiness gates, not formal verifiers.

Here are the new detectors we've added:

### `DET-FUS-L2-7594` — Blob Transaction Proof-Format Readiness (Cell Proofs)

Protocol anchor: `EIP-7594` (PeerDAS).

Core fork change: Proof format for blobs changes from “blob proofs” to “cell proofs.” Ethereum Foundation urges all blob originators to update software to create cell proofs.

What it detects:

* L2 posting codepaths that construct or assume legacy blob proofs rather than cell proofs.
* “Signed blob tx” workflows that fail to recompute cell proofs post-fork (signatures remain valid but proofs must be recomputed).
* Operational risk patterns around the fork boundary, given implementations may drop or convert txpool entries at the fork.

Why it matters:

* If an L2’s batch submitter sends the wrong proof format, L1 posting can fail after Fusaka. This is a practical halt-risk for rollups and is treated as a readiness requirement by major L2 stacks.

Severity:

* Blocker if the repo contains L1 posting logic that cannot produce cell proofs.
* High if it relies on node-side conversion rather than producing correct proofs.

Mitigations:

* Upgrade blob-transaction construction to produce cell proofs natively.
* Add post-fork “resend strategy” for transactions that were in-flight at activation.
* Include CI checks that exercise a blob tx build on a Fusaka-configured environment.

Verification steps:

* Demonstrate passing end-to-end posting of a blob transaction after Fusaka activation.
* Confirm the batcher’s proof construction path is cell-proof producing (not relying on node conversion).

### `DET-FUS-L2-7825` — Per-Transaction Gas Limit Cap Violations

Protocol anchor: `EIP-7825`.

Core fork change: Any tx with gasLimit > 16,777,216 is rejected; blocks containing such a transaction are invalid.

What it detects:

* Offchain tx builders that set gas limits above the cap.
* “Single huge tx” operational procedures (upgrade, recovery, mass action) that require gas above the cap in worst-case conditions.

Why it matters:

* One invalid posting tx can stall critical operations.
* Post-fork, “just set gas very high” patterns become invalid by protocol rule.

Severity:

* Blocker for any L2 critical path tx construction that can exceed the cap.
* High for admin/emergency procedures that may fail when needed.

Mitigations:

* Clamp gas limits to the cap.
* Split large ops into multiple txs.
* Implement batch-size limits and retry logic that does not exceed protocol limits.

Verification steps:

* Construct “largest” txs and validate they remain ≤ cap.

### `DET-FUS-L2-7918` — Blob Fee Floor/Reserve-Price Coupling Blind Spots

Protocol anchor: `EIP-7918`.

Core fork change:

* Introduces a reserve price below which the blob base fee cannot fall, tied to execution base fee by a fixed ratio.

What it detects:

* Fee estimators that treat blob fees as independent and allow them to collapse below the reserve floor implied by execution costs.
* Posting policies that subsidize L1 posting without dynamic throttles/circuit breakers under rising execution fees.

Why it matters:

* If your estimator assumes blob posting will remain extremely cheap during periods when execution fees are high, you can end up undercharging users, burning treasury, or throttling posting too late—creating downtime or exploitable subsidization dynamics.

Severity:

* High if the L2 pays posting costs or provides fixed-fee guarantees.
* Medium if all posting costs are passed through with strong backpressure.

Mitigations:

* Model blob cost as having a floor linked to execution base fee (EIP-7918’s reserve mechanism).
* Add backpressure by reducing batch frequency, adjusting compression, raising L2 fees, or pausing subsidization when costs exceed thresholds.

Verification steps:

* Simulate scenarios with high execution base fees and confirm the estimator/policy remains stable and does not produce unsafe underpricing.

### `DET-FUS-L2-7892` — Blob Parameter Drift and BPO Fork Resilience

Protocol anchor: `EIP-7892`.

Core fork change:

* Blob capacity parameters (target, max, baseFeeUpdateFraction) can be adjusted via BPO forks to scale blob capacity with demand.

What it detects:

* Hardcoded blob parameters (targets/limits/update fractions) in: fee estimators, posting schedulers, monitoring/alerting thresholds, config files assumed immutable after Fusaka.
* Logic that assumes blob capacity changes only arrive in “major forks,” not parameter-only forks.

Why it matters:

* If your L2 hardcodes blob capacity assumptions, your cost models, batching behavior, and monitoring can become wrong after a BPO fork.

Severity:

* High if blob parameters are used for cost controls or safety-critical rate limiting.
* Medium if used only for telemetry or approximate dashboards.

Mitigations:

* Make blob param ingestion config-driven rather than constant literals.
* Add “parameter change detection” to monitoring to automatically re-baseline alerts around BPO activations.

Verification steps:

* Changing target/max/update fraction shouldn't require code changes and shouldn't break batching/fee estimation.

---

If you operate an L2 / rollup stack and want these Fusaka readiness gates integrated into your posting pipeline and CI, this is a **Thrum Labs** engagement. Start at the Labs primer above, and we’ll scope the exact boundary surfaces (batcher/poster, fee model, config ingestion, monitoring) where these detectors should attach.