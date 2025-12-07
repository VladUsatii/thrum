# Thrum Detector Reference
This page enumerates detector IDs and their descriptions. Every detector on our list supports direct fragment navigation, e.g., `#D007`. When you run a Thrum scan, you are getting access to every single one of these detectors. We've also built a proprietary model to selectively run detectors based on your unique repo so that you can get your scan back with speed, accuracy, completeness, and relevance.

## Category legend
| Abbrev. | Category |
|---|---|
| `AC` | access control |
| `UPG` | upgrades/proxies |
| `MATH` | numeric/precision |
| `CALL` | external calls/callbacks |
| `ORCL` | oracles/MEV |
| `TOK` | token standards |
| `DEFI` | DeFi math/economics |
| `XCH` | cross-chain |
| `AA` | account abstraction |
| `EVM` | new EVM/compiler surfaces |
| `UNI4` | Uniswap v4 hooks |
| `GEN` | general logic/DoS |
| `L2` | L2/rollup-specific surfaces |
| `WLT` | wallet standards/delegation |
| `STORE` | storage namespace/layout |
| `REST` | restaking/LST/validator ops |
| `ZK` | zero-knowledge/verifier |
| `MRK` | Merkle/claim trees |

## Detectors
> Query by `thrum.sh/docs/detectors#XXXX`, where `XXXX` is the UID.

<a id="D001"></a><a id="d001"></a>
### D001
- **Category:** `AC`
- **Description:** Missing or incorrect access control on privileged functions (owner/role checks).

<a id="D002"></a><a id="d002"></a>
### D002
- **Category:** `AC`
- **Description:** Role-admin misuse (DEFAULT ADMIN ROLE can grant/revoke itself without delay).

<a id="D003"></a><a id="d003"></a>
### D003
- **Category:** `AC`
- **Description:** Privilege escalation via role renouncement or role reconfiguration.

<a id="D004"></a><a id="d004"></a>
### D004
- **Category:** `AC`
- **Description:** Unprotected initialization/initializer front-run (initialize() callable by anyone).

<a id="D005"></a><a id="d005"></a>
### D005
- **Category:** `AC`
- **Description:** Reinitialization vulnerability (reinitializer callable multiple times).

<a id="D006"></a><a id="d006"></a>
### D006
- **Category:** `AC`
- **Description:** Two-step ownership transfer missing (no acceptOwnership pattern).

<a id="D007"></a><a id="d007"></a>
### D007
- **Category:** `AC`
- **Description:** Authorization via tx.origin (phishing/contract-call bypass).

<a id="D008"></a><a id="d008"></a>
### D008
- **Category:** `AC`
- **Description:** EOA-only checks via EXTCODESIZE==0 (bypassable; breaks with delegation).

<a id="D009"></a><a id="d009"></a>
### D009
- **Category:** `AC`
- **Description:** Incomplete access control on emergency functions (pause/unpause/rescue/skim).

<a id="D010"></a><a id="d010"></a>
### D010
- **Category:** `AC`
- **Description:** Unbounded admin power without timelock/delay window (risk posture flag).

<a id="D011"></a><a id="d011"></a>
### D011
- **Category:** `AC`
- **Description:** Inconsistent access control across overloaded functions (e.g., setX vs setX(uint)).

<a id="D012"></a><a id="d012"></a>
### D012
- **Category:** `AC`
- **Description:** Modifier order bug (auth after state change/external call).

<a id="D013"></a><a id="d013"></a>
### D013
- **Category:** `AC`
- **Description:** Delegatecall-based auth bypass (msg.sender semantics confusion).

<a id="D014"></a><a id="d014"></a>
### D014
- **Category:** `AC`
- **Description:** Signature-based auth replay (missing nonce/domain separation).

<a id="D015"></a><a id="d015"></a>
### D015
- **Category:** `AC`
- **Description:** EIP-1271 signature validation misuse (accepts invalid contract signature).

<a id="D016"></a><a id="d016"></a>
### D016
- **Category:** `AC`
- **Description:** Permit misuse (EIP-2612/permit2 allowance escalation).

<a id="D017"></a><a id="d017"></a>
### D017
- **Category:** `AC`
- **Description:** Misconfigured multisig threshold/owners set (single-owner disguised multisig).

<a id="D018"></a><a id="d018"></a>
### D018
- **Category:** `AC`
- **Description:** Critical parameter setters lack bounds (fee, LTV, oracle staleness, limits).

<a id="D019"></a><a id="d019"></a>
### D019
- **Category:** `AC`
- **Description:** Governance action can reduce timelock delay below safe minimum.

<a id="D020"></a><a id="d020"></a>
### D020
- **Category:** `AC`
- **Description:** Upgrade admin and protocol admin conflation (same key controls logic and funds).

<a id="D021"></a><a id="d021"></a>
### D021
- **Category:** `UPG`
- **Description:** Transparent/UUPS proxy pattern mis-detection (false immutability).

<a id="D022"></a><a id="d022"></a>
### D022
- **Category:** `UPG`
- **Description:** Proxy admin slot collision/incorrect EIP-1967 slot usage.

<a id="D023"></a><a id="d023"></a>
### D023
- **Category:** `UPG`
- **Description:** UUPS upgradeTo/upgradeToAndCall missing onlyProxy/proxiableUUID checks.

<a id="D024"></a><a id="d024"></a>
### D024
- **Category:** `UPG`
- **Description:** Upgradeable implementation exposes initialize() after deployment (uninitialized impl).

<a id="D025"></a><a id="d025"></a>
### D025
- **Category:** `UPG`
- **Description:** Initializer does not call parent initializers (partial init -> privilege bugs).

<a id="D026"></a><a id="d026"></a>
### D026
- **Category:** `UPG`
- **Description:** Storage layout collision across upgrades (struct packing/inherited state reorder).

<a id="D027"></a><a id="d027"></a>
### D027
- **Category:** `UPG`
- **Description:** Storage gap mismanagement (incorrect gap sizing).

<a id="D028"></a><a id="d028"></a>
### D028
- **Category:** `UPG`
- **Description:** Delegatecall to untrusted implementation (implementation pointer mutable by attacker).

<a id="D029"></a><a id="d029"></a>
### D029
- **Category:** `UPG`
- **Description:** Beacon proxy: beacon upgrade auth missing/beacon address changeable.

<a id="D030"></a><a id="d030"></a>
### D030
- **Category:** `UPG`
- **Description:** Diamond selector collision across facets (EIP-2535).

<a id="D031"></a><a id="d031"></a>
### D031
- **Category:** `UPG`
- **Description:** Diamond function shadowing/selector overwrite introduced by diamondCut plan.

<a id="D032"></a><a id="d032"></a>
### D032
- **Category:** `UPG`
- **Description:** DiamondCut access control weakness (diamondCut callable by non-admin).

<a id="D033"></a><a id="d033"></a>
### D033
- **Category:** `UPG`
- **Description:** Diamond init delegatecall hazard (init can be swapped/re-run/reenter).

<a id="D034"></a><a id="d034"></a>
### D034
- **Category:** `UPG`
- **Description:** Diamond loupe inconsistency (facet mapping incomplete -> monitoring blind spots).

<a id="D035"></a><a id="d035"></a>
### D035
- **Category:** `UPG`
- **Description:** Metamorphic CREATE2 upgrade trick reliance (incompatible with post-6780 semantics).

<a id="D036"></a><a id="d036"></a>
### D036
- **Category:** `UPG`
- **Description:** Upgrade introduces new external call edge (call graph diff risk).

<a id="D037"></a><a id="d037"></a>
### D037
- **Category:** `UPG`
- **Description:** Upgrade introduces new privileged function (ABI surface diff risk).

<a id="D038"></a><a id="d038"></a>
### D038
- **Category:** `UPG`
- **Description:** Upgrade removes safety check/invariant (semantic regression).

<a id="D039"></a><a id="d039"></a>
### D039
- **Category:** `UPG`
- **Description:** Upgradeable ERC-20/4626: decimals/asset changes across upgrade (economic break).

<a id="D040"></a><a id="d040"></a>
### D040
- **Category:** `UPG`
- **Description:** Storage type-change across upgrades (e.g., uint->address) even if slot preserved.

<a id="D041"></a><a id="d041"></a>
### D041
- **Category:** `UPG`
- **Description:** Proxy selfdestruct/kill-switch reachable (fund lock/bricking risk).

<a id="D042"></a><a id="d042"></a>
### D042
- **Category:** `UPG`
- **Description:** Admin key can bypass pause or circuit breaker (guardrail bypass risk).

<a id="D043"></a><a id="d043"></a>
### D043
- **Category:** `UPG`
- **Description:** Initialization parameter injection via upgradeToAndCall (unsafe init calldata parsing).

<a id="D044"></a><a id="d044"></a>
### D044
- **Category:** `UPG`
- **Description:** Differential upgrade regression (diff fuzz) between old/new implementations.

<a id="D045"></a><a id="d045"></a>
### D045
- **Category:** `UPG`
- **Description:** Hidden proxy detection in unverified bytecode (proxy collision/shadow proxy).

<a id="D046"></a><a id="d046"></a>
### D046
- **Category:** `MATH`
- **Description:** Integer overflow/underflow in unchecked blocks (semantic bug).

<a id="D047"></a><a id="d047"></a>
### D047
- **Category:** `MATH`
- **Description:** Signed/unsigned cast truncation (int256->uint256) leading to negative bypass.

<a id="D048"></a><a id="d048"></a>
### D048
- **Category:** `MATH`
- **Description:** Downcast truncation (uint256->uint128/uint64) losing high bits.

<a id="D049"></a><a id="d049"></a>
### D049
- **Category:** `MATH`
- **Description:** Precision loss in division before multiplication (a/bc) vs (a*c/b).

<a id="D050"></a><a id="d050"></a>
### D050
- **Category:** `MATH`
- **Description:** Rounding direction bug (ceil vs floor) in share/asset conversions.

<a id="D051"></a><a id="d051"></a>
### D051
- **Category:** `MATH`
- **Description:** Unchecked return of SafeCast/custom cast helpers (silent wrap).

<a id="D052"></a><a id="d052"></a>
### D052
- **Category:** `MATH`
- **Description:** Fixed-point scaling mismatch (1e18 vs 1e27 vs token decimals).

<a id="D053"></a><a id="d053"></a>
### D053
- **Category:** `MATH`
- **Description:** Fee computation overflow (feeRate * amount) before division.

<a id="D054"></a><a id="d054"></a>
### D054
- **Category:** `MATH`
- **Description:** Interest accrual overflow/exponentiation blowup.

<a id="D055"></a><a id="d055"></a>
### D055
- **Category:** `MATH`
- **Description:** TWAP accumulator overflow/uint32 timestamp wrap misuse.

<a id="D056"></a><a id="d056"></a>
### D056
- **Category:** `MATH`
- **Description:** Double-counting in cumulative indices (integral updated twice per block).

<a id="D057"></a><a id="d057"></a>
### D057
- **Category:** `MATH`
- **Description:** Division by zero on supply/totalAssets/totalSupply edge cases.

<a id="D058"></a><a id="d058"></a>
### D058
- **Category:** `MATH`
- **Description:** Slippage checks missing or inverted (minOut/maxIn misuse).

<a id="D059"></a><a id="d059"></a>
### D059
- **Category:** `MATH`
- **Description:** Precision mismatch in sqrt/exp/log approximations (AMM math).

<a id="D060"></a><a id="d060"></a>
### D060
- **Category:** `MATH`
- **Description:** Overflow/underflow in bitwise packing/unpacking of state (e.g., ticks).

<a id="D061"></a><a id="d061"></a>
### D061
- **Category:** `CALL`
- **Description:** Reentrancy: state update after external call (classic checks-effects-interactions violation).

<a id="D062"></a><a id="d062"></a>
### D062
- **Category:** `CALL`
- **Description:** Cross-function reentrancy (reenter via different entrypoint).

<a id="D063"></a><a id="d063"></a>
### D063
- **Category:** `CALL`
- **Description:** Read-only reentrancy (view reentrancy affecting price/oracle/limits).

<a id="D064"></a><a id="d064"></a>
### D064
- **Category:** `CALL`
- **Description:** Reentrancy via ERC-777/token hooks (tokensReceived).

<a id="D065"></a><a id="d065"></a>
### D065
- **Category:** `CALL`
- **Description:** Reentrancy via ERC-721 receiver hooks (onERC721Received).

<a id="D066"></a><a id="d066"></a>
### D066
- **Category:** `CALL`
- **Description:** Reentrancy via fallback/receive function on ETH transfer.

<a id="D067"></a><a id="d067"></a>
### D067
- **Category:** `CALL`
- **Description:** Reentrancy via delegatecall into attacker-controlled code.

<a id="D068"></a><a id="d068"></a>
### D068
- **Category:** `CALL`
- **Description:** Missing reentrancy guard on multicall/batch execution entrypoint.

<a id="D069"></a><a id="d069"></a>
### D069
- **Category:** `CALL`
- **Description:** Reentrancy guard incorrectly scoped (nonReentrant on internal, bypass via external).

<a id="D070"></a><a id="d070"></a>
### D070
- **Category:** `CALL`
- **Description:** Reentrancy guard cleared too early (before function end).

<a id="D071"></a><a id="d071"></a>
### D071
- **Category:** `CALL`
- **Description:** Unchecked low-level call success (call/delegatecall/staticcall).

<a id="D072"></a><a id="d072"></a>
### D072
- **Category:** `CALL`
- **Description:** Unchecked external call return value for ERC-20 transfers (non-standard tokens).

<a id="D073"></a><a id="d073"></a>
### D073
- **Category:** `CALL`
- **Description:** External call in loop (n untrusted callees -> gas griefing/reentrancy).

<a id="D074"></a><a id="d074"></a>
### D074
- **Category:** `CALL`
- **Description:** Callback origin not validated (hook/callback callable by anyone).

<a id="D075"></a><a id="d075"></a>
### D075
- **Category:** `CALL`
- **Description:** Cross-contract invariants broken by external call between reads/writes.

<a id="D076"></a><a id="d076"></a>
### D076
- **Category:** `ORCL`
- **Description:** Price oracle manipulation (spot price used; no TWAP).

<a id="D077"></a><a id="d077"></a>
### D077
- **Category:** `ORCL`
- **Description:** Oracle source centralization (single feed; admin updatable without delay).

<a id="D078"></a><a id="d078"></a>
### D078
- **Category:** `ORCL`
- **Description:** Oracle stale price usage (heartbeat/updatedAt not checked).

<a id="D079"></a><a id="d079"></a>
### D079
- **Category:** `ORCL`
- **Description:** Oracle decimal mismatch (feed decimals vs token decimals).

<a id="D080"></a><a id="d080"></a>
### D080
- **Category:** `ORCL`
- **Description:** Chainlink-like aggregator answeredInRound misuse (stale round).

<a id="D081"></a><a id="d081"></a>
### D081
- **Category:** `ORCL`
- **Description:** Uniswap v2/v3 TWAP misuse (observation cardinality/period too short).

<a id="D082"></a><a id="d082"></a>
### D082
- **Category:** `ORCL`
- **Description:** AMM price used during same block as swap (sandwichable).

<a id="D083"></a><a id="d083"></a>
### D083
- **Category:** `ORCL`
- **Description:** Front-running vulnerability in commit-less auctions/order submissions.

<a id="D084"></a><a id="d084"></a>
### D084
- **Category:** `ORCL`
- **Description:** Sandwich attack susceptibility due to missing slippage bounds.

<a id="D085"></a><a id="d085"></a>
### D085
- **Category:** `ORCL`
- **Description:** Block timestamp dependence in price selection (timestamp manipulation).

<a id="D086"></a><a id="d086"></a>
### D086
- **Category:** `ORCL`
- **Description:** Miner/validator extractable liquidation path (liquidation bonus exploit).

<a id="D087"></a><a id="d087"></a>
### D087
- **Category:** `ORCL`
- **Description:** Flash-loan aided oracle manipulation (single-tx pump and dump).

<a id="D088"></a><a id="d088"></a>
### D088
- **Category:** `ORCL`
- **Description:** Cross-chain oracle message finality not validated (optimistic relay abuse).

<a id="D089"></a><a id="d089"></a>
### D089
- **Category:** `ORCL`
- **Description:** Price circuit breaker missing (oracle jump not bounded).

<a id="D090"></a><a id="d090"></a>
### D090
- **Category:** `ORCL`
- **Description:** Min-out computed from stale oracle but executed against AMM (mismatch exploit).

<a id="D091"></a><a id="d091"></a>
### D091
- **Category:** `TOK`
- **Description:** ERC-20 transfer/transferFrom return value not checked (non-standard tokens).

<a id="D092"></a><a id="d092"></a>
### D092
- **Category:** `TOK`
- **Description:** ERC-20 approve race condition (IERC20 approve front-running).

<a id="D093"></a><a id="d093"></a>
### D093
- **Category:** `TOK`
- **Description:** Permit (EIP-2612) domain separator misuse (chainId replay/forks).

<a id="D094"></a><a id="d094"></a>
### D094
- **Category:** `TOK`
- **Description:** Permit nonce reuse (replay)/missing deadline checks.

<a id="D095"></a><a id="d095"></a>
### D095
- **Category:** `TOK`
- **Description:** Permit2 integration misconfiguration (unbounded allowance/expiration).

<a id="D096"></a><a id="d096"></a>
### D096
- **Category:** `TOK`
- **Description:** ERC-777 hooks incompatibility (reentrancy/denial via hook revert).

<a id="D097"></a><a id="d097"></a>
### D097
- **Category:** `TOK`
- **Description:** Fee-on-transfer/deflationary token incompatibility (amount received != amount sent).

<a id="D098"></a><a id="d098"></a>
### D098
- **Category:** `TOK`
- **Description:** Rebasing token incompatibility (balance changes break accounting).

<a id="D099"></a><a id="d099"></a>
### D099
- **Category:** `TOK`
- **Description:** ERC-4626 share inflation/donation attack surface (totalAssets manipulation).

<a id="D100"></a><a id="d100"></a>
### D100
- **Category:** `TOK`
- **Description:** ERC-4626 rounding edge cases (preview vs actual mismatch).

<a id="D101"></a><a id="d101"></a>
### D101
- **Category:** `TOK`
- **Description:** ERC-4626 totalAssets reported incorrectly (includes/excludes fees).

<a id="D102"></a><a id="d102"></a>
### D102
- **Category:** `TOK`
- **Description:** ERC-3156 flash loan callback origin not validated.

<a id="D103"></a><a id="d103"></a>
### D103
- **Category:** `TOK`
- **Description:** ERC-721 safeMint/transferToReceiver reentrancy via onERC721Received.

<a id="D104"></a><a id="d104"></a>
### D104
- **Category:** `TOK`
- **Description:** ERC-721 approval logic error (operator approvals overly broad).

<a id="D105"></a><a id="d105"></a>
### D105
- **Category:** `TOK`
- **Description:** ERC-1155 batch transfer receiver hook misuse and reentrancy.

<a id="D106"></a><a id="d106"></a>
### D106
- **Category:** `TOK`
- **Description:** EIP-712 typed data hash mismatch (struct encoding bug).

<a id="D107"></a><a id="d107"></a>
### D107
- **Category:** `TOK`
- **Description:** EIP-1271 signature validation accepts arbitrary magic value.

<a id="D108"></a><a id="d108"></a>
### D108
- **Category:** `TOK`
- **Description:** EIP-3009 transferWithAuthorization replay (nonce/validAfter/validBefore).

<a id="D109"></a><a id="d109"></a>
### D109
- **Category:** `TOK`
- **Description:** ERC-20 decimals assumption hardcoded (must not assume 18).

<a id="D110"></a><a id="d110"></a>
### D110
- **Category:** `TOK`
- **Description:** Unsafe token rescue function can drain user funds (sweep transfers all).

<a id="D111"></a><a id="d111"></a>
### D111
- **Category:** `DEFI`
- **Description:** AMM invariant violation: k not preserved due to rounding or fee bug.

<a id="D112"></a><a id="d112"></a>
### D112
- **Category:** `DEFI`
- **Description:** AMM fee accounting mismatch (fees not applied consistently).

<a id="D113"></a><a id="d113"></a>
### D113
- **Category:** `DEFI`
- **Description:** AMM lp share minting uses wrong reserve snapshot (front-runnable).

<a id="D114"></a><a id="d114"></a>
### D114
- **Category:** `DEFI`
- **Description:** AMM sync()/skim() misuse enabling reserve manipulation.

<a id="D115"></a><a id="d115"></a>
### D115
- **Category:** `DEFI`
- **Description:** Tick math overflow/underflow in concentrated liquidity (sqrtPriceX96).

<a id="D116"></a><a id="d116"></a>
### D116
- **Category:** `DEFI`
- **Description:** Liquidity position accounting double-count/missing update in burn/mint.

<a id="D117"></a><a id="d117"></a>
### D117
- **Category:** `DEFI`
- **Description:** Lending market collateral factor/LTV setter lacks bounds.

<a id="D118"></a><a id="d118"></a>
### D118
- **Category:** `DEFI`
- **Description:** Lending: liquidation calculation uses stale index (over/under-liquidation).

<a id="D119"></a><a id="d119"></a>
### D119
- **Category:** `DEFI`
- **Description:** Lending: repay can underflow debt due to rounding.

<a id="D120"></a><a id="d120"></a>
### D120
- **Category:** `DEFI`
- **Description:** Lending: interest accrual not called on state-changing paths (stale debt).

<a id="D121"></a><a id="d121"></a>
### D121
- **Category:** `DEFI`
- **Description:** Lending: borrow allowed when market paused (pause bypass).

<a id="D122"></a><a id="d122"></a>
### D122
- **Category:** `DEFI`
- **Description:** Vault: deposit/withdraw uses incorrect asset decimals scaling.

<a id="D123"></a><a id="d123"></a>
### D123
- **Category:** `DEFI`
- **Description:** Vault: donation/inflation attack (pre-mint shares then donate assets).

<a id="D124"></a><a id="d124"></a>
### D124
- **Category:** `DEFI`
- **Description:** Vault: totalAssets includes pending rewards incorrectly (double count).

<a id="D125"></a><a id="d125"></a>
### D125
- **Category:** `DEFI`
- **Description:** Vault: share price manipulation via flash loan + donation.

<a id="D126"></a><a id="d126"></a>
### D126
- **Category:** `DEFI`
- **Description:** Staking rewards: per-user integral update order bug (steal rewards).

<a id="D127"></a><a id="d127"></a>
### D127
- **Category:** `DEFI`
- **Description:** Staking rewards: missing checkpoint on transfer (reward theft).

<a id="D128"></a><a id="d128"></a>
### D128
- **Category:** `DEFI`
- **Description:** Fee module: fee recipient can be set to zero or attacker.

<a id="D129"></a><a id="d129"></a>
### D129
- **Category:** `DEFI`
- **Description:** Fee module: fee-on-fee compounding bug (fee charged on already-fee’d value).

<a id="D130"></a><a id="d130"></a>
### D130
- **Category:** `DEFI`
- **Description:** Options/derivatives: settlement uses manipulable oracle at expiry.

<a id="D131"></a><a id="d131"></a>
### D131
- **Category:** `DEFI`
- **Description:** Options: exercise/withdraw ordering bug (withdraw before settle).

<a id="D132"></a><a id="d132"></a>
### D132
- **Category:** `DEFI`
- **Description:** Perp funding: funding rate sign bug (pays wrong side).

<a id="D133"></a><a id="d133"></a>
### D133
- **Category:** `DEFI`
- **Description:** Stablecoin peg: redemption rounding bug drains collateral.

<a id="D134"></a><a id="d134"></a>
### D134
- **Category:** `DEFI`
- **Description:** Aggregator routers: arbitrary external call/swap data injection risk.

<a id="D135"></a><a id="d135"></a>
### D135
- **Category:** `DEFI`
- **Description:** Fee distribution: division remainder accumulates to attacker address.

<a id="D136"></a><a id="d136"></a>
### D136
- **Category:** `XCH`
- **Description:** Bridge message replay (nonce/domain not enforced).

<a id="D137"></a><a id="d137"></a>
### D137
- **Category:** `XCH`
- **Description:** Bridge message origin not authenticated (anyone can call receiveMessage).

<a id="D138"></a><a id="d138"></a>
### D138
- **Category:** `XCH`
- **Description:** Bridge finality assumption wrong (accepts optimistic message without challenge window).

<a id="D139"></a><a id="d139"></a>
### D139
- **Category:** `XCH`
- **Description:** Bridge multisig signer-set update insecure (threshold lowered/signer added).

<a id="D140"></a><a id="d140"></a>
### D140
- **Category:** `XCH`
- **Description:** Bridge rate limits missing (infinite mint per time window).

<a id="D141"></a><a id="d141"></a>
### D141
- **Category:** `XCH`
- **Description:** Bridge guardian pause bypass (pause not checked on receive).

<a id="D142"></a><a id="d142"></a>
### D142
- **Category:** `XCH`
- **Description:** Cross-chain token decimals mismatch (mint wrong amount).

<a id="D143"></a><a id="d143"></a>
### D143
- **Category:** `XCH`
- **Description:** Cross-chain fee calculation mismatch leading to underpayment/DoS.

<a id="D144"></a><a id="d144"></a>
### D144
- **Category:** `XCH`
- **Description:** Cross-domain reentrancy via message callback into protocol.

<a id="D145"></a><a id="d145"></a>
### D145
- **Category:** `XCH`
- **Description:** Bridge refund logic exploitable (double refund/refund to attacker).

<a id="D146"></a><a id="d146"></a>
### D146
- **Category:** `AA`
- **Description:** ERC-4337 validateUserOp missing signature check (auth bypass).

<a id="D147"></a><a id="d147"></a>
### D147
- **Category:** `AA`
- **Description:** ERC-4337 nonce management bug (replay across bundles).

<a id="D148"></a><a id="d148"></a>
### D148
- **Category:** `AA`
- **Description:** ERC-4337 paymaster validation allows free gas (sponsor drain).

<a id="D149"></a><a id="d149"></a>
### D149
- **Category:** `AA`
- **Description:** ERC-4337 paymaster postOp accounting mismatch (sponsor loss).

<a id="D150"></a><a id="d150"></a>
### D150
- **Category:** `AA`
- **Description:** ERC-4337 UserOperation packing/hashing bug (different ops same hash).

<a id="D151"></a><a id="d151"></a>
### D151
- **Category:** `AA`
- **Description:** ERC-7562 validation-scope rule violations (bundler DoS/mempool rejection).

<a id="D152"></a><a id="d152"></a>
### D152
- **Category:** `AA`
- **Description:** AA validation reads mutable state not permitted (state-dependent validation).

<a id="D153"></a><a id="d153"></a>
### D153
- **Category:** `AA`
- **Description:** ERC-6900 module install authorization weak (anyone can install validation module).

<a id="D154"></a><a id="d154"></a>
### D154
- **Category:** `AA`
- **Description:** ERC-6900 module uninstall leaves account without validation (fail-open).

<a id="D155"></a><a id="d155"></a>
### D155
- **Category:** `AA`
- **Description:** ERC-6900 hook ordering conflict (pre/post hooks can bypass checks).

<a id="D156"></a><a id="d156"></a>
### D156
- **Category:** `AA`
- **Description:** ERC-6900 shared storage collisions among modules (corrupt module state).

<a id="D157"></a><a id="d157"></a>
### D157
- **Category:** `AA`
- **Description:** ERC-7579 module type confusion (validator vs executor vs hook mis-registered).

<a id="D158"></a><a id="d158"></a>
### D158
- **Category:** `AA`
- **Description:** ERC-7579 fallback handler authorization bypass.

<a id="D159"></a><a id="d159"></a>
### D159
- **Category:** `AA`
- **Description:** EOA delegation (EIP-7702): whitelist/EOA-only gating bypass risk.

<a id="D160"></a><a id="d160"></a>
### D160
- **Category:** `AA`
- **Description:** Session key/spending limit module bypass (limit checked after call).

<a id="D161"></a><a id="d161"></a>
### D161
- **Category:** `EVM`
- **Description:** Transient storage used as long-lived state (assumes persists beyond tx).

<a id="D162"></a><a id="d162"></a>
### D162
- **Category:** `EVM`
- **Description:** Transient storage not cleared on revert path (cleanup missing on error).

<a id="D163"></a><a id="d163"></a>
### D163
- **Category:** `EVM`
- **Description:** Transient storage keying collision (same slot reused across independent flows).

<a id="D164"></a><a id="d164"></a>
### D164
- **Category:** `EVM`
- **Description:** Transient storage used for access control without end-of-call clear.

<a id="D165"></a><a id="d165"></a>
### D165
- **Category:** `EVM`
- **Description:** Transient storage read-before-write (uninitialized transient slot assumption).

<a id="D166"></a><a id="d166"></a>
### D166
- **Category:** `EVM`
- **Description:** SELFDESTRUCT used as access control (kill-switch) but semantics changed (EIP-6780).

<a id="D167"></a><a id="d167"></a>
### D167
- **Category:** `EVM`
- **Description:** Compiler-version vulnerable range detector (known solc bugs; ABIEncoderV2, etc.).

<a id="D168"></a><a id="d168"></a>
### D168
- **Category:** `EVM`
- **Description:** abi.encodePacked collision in hashing/signatures.

<a id="D169"></a><a id="d169"></a>
### D169
- **Category:** `EVM`
- **Description:** Uncheckedassembly return(...)skipping invariants/access control.

<a id="D170"></a><a id="d170"></a>
### D170
- **Category:** `EVM`
- **Description:** ecrecover malleability/s-value not enforced.

<a id="D171"></a><a id="d171"></a>
### D171
- **Category:** `UNI4`
- **Description:** Uniswap v4 hook not PoolKey-bound (hook callable from arbitrary pool).

<a id="D172"></a><a id="d172"></a>
### D172
- **Category:** `UNI4`
- **Description:** Hook initialization lacks token-pair validation (fake token pools exploit).

<a id="D173"></a><a id="d173"></a>
### D173
- **Category:** `UNI4`
- **Description:** Hook callback origin not validated (external direct calls to callbacks).

<a id="D174"></a><a id="d174"></a>
### D174
- **Category:** `UNI4`
- **Description:** Hook reentrancy: external calls inside before/afterSwap without guard.

<a id="D175"></a><a id="d175"></a>
### D175
- **Category:** `UNI4`
- **Description:** Hook DoS: hook can revert and brick swaps/liquidity operations.

<a id="D176"></a><a id="d176"></a>
### D176
- **Category:** `UNI4`
- **Description:** Hook fee manipulation bug (dynamic fee logic exploitable).

<a id="D177"></a><a id="d177"></a>
### D177
- **Category:** `UNI4`
- **Description:** Hook custom accounting mismatch (credits without deposits).

<a id="D178"></a><a id="d178"></a>
### D178
- **Category:** `UNI4`
- **Description:** Hook donation/claim mechanism allows unbacked mint (callback spoofing).

<a id="D179"></a><a id="d179"></a>
### D179
- **Category:** `UNI4`
- **Description:** Hook statefulness across pools leaks accounting (shared state cross-pool).

<a id="D180"></a><a id="d180"></a>
### D180
- **Category:** `UNI4`
- **Description:** Hook uses transient storage without strict cleanup (tx-composability bug).

<a id="D181"></a><a id="d181"></a>
### D181
- **Category:** `GEN`
- **Description:** Denial of service via unbounded iteration over dynamic arrays/mappings.

<a id="D182"></a><a id="d182"></a>
### D182
- **Category:** `GEN`
- **Description:** Denial of service via unexpected revert in external dependency (no fallback path).

<a id="D183"></a><a id="d183"></a>
### D183
- **Category:** `GEN`
- **Description:** Gas griefing via storage writes in loop (attacker-controlled length).

<a id="D184"></a><a id="d184"></a>
### D184
- **Category:** `GEN`
- **Description:** Block gas limit assumption (function becomes uncallable as state grows).

<a id="D185"></a><a id="d185"></a>
### D185
- **Category:** `GEN`
- **Description:** DoS via forced Ether (selfdestruct/coinbase payment) affecting invariants.

<a id="D186"></a><a id="d186"></a>
### D186
- **Category:** `GEN`
- **Description:** DoS via revert-on-receive ETH (pull vs push payments).

<a id="D187"></a><a id="d187"></a>
### D187
- **Category:** `GEN`
- **Description:** Unchecked arithmetic in loop index leading to infinite loop.

<a id="D188"></a><a id="d188"></a>
### D188
- **Category:** `GEN`
- **Description:** Timestamp dependence for critical logic (auction end, vesting) without tolerance.

<a id="D189"></a><a id="d189"></a>
### D189
- **Category:** `GEN`
- **Description:** Block.number dependence for time (L2 reorg/variable block times).

<a id="D190"></a><a id="d190"></a>
### D190
- **Category:** `GEN`
- **Description:** Front-running in commit-reveal missing (reveal can be copied).

<a id="D191"></a><a id="d191"></a>
### D191
- **Category:** `GEN`
- **Description:** Improper error handling: assert used for user-controlled condition.

<a id="D192"></a><a id="d192"></a>
### D192
- **Category:** `GEN`
- **Description:** Missing input validation: zero address, zero amount, same-token pairs.

<a id="D193"></a><a id="d193"></a>
### D193
- **Category:** `GEN`
- **Description:** Unvalidated array length mismatch across parallel arrays.

<a id="D194"></a><a id="d194"></a>
### D194
- **Category:** `GEN`
- **Description:** Type confusion via abi.decode with wrong tuple layout.

<a id="D195"></a><a id="d195"></a>
### D195
- **Category:** `GEN`
- **Description:** Storage pointer aliasing bug (Solidity older patterns)/uninitialized storage ref.

<a id="D196"></a><a id="d196"></a>
### D196
- **Category:** `GEN`
- **Description:** Unsafe cast from bytes to address (truncation) in parsing calldata.

<a id="D197"></a><a id="d197"></a>
### D197
- **Category:** `GEN`
- **Description:** Signature replay across function selectors (missing function binding).

<a id="D198"></a><a id="d198"></a>
### D198
- **Category:** `GEN`
- **Description:** Replay across chains (missing chainId in signed message).

<a id="D199"></a><a id="d199"></a>
### D199
- **Category:** `GEN`
- **Description:** Fee recipient can be griefed (set to contract that reverts on receive).

<a id="D200"></a><a id="d200"></a>
### D200
- **Category:** `GEN`
- **Description:** Emergency withdrawal bypasses accounting (steal funds/breaks invariants).

<a id="D201"></a><a id="d201"></a>
### D201
- **Category:** `L2`
- **Description:** Missing L2 sequencer-uptime gating before using oracle data (downtime -> stale prices, unsafe liqui- dations).

<a id="D202"></a><a id="d202"></a>
### D202
- **Category:** `L2`
- **Description:** Missing post-recovery grace period after sequencer resumes (operations immediately resume on “up”).

<a id="D203"></a><a id="d203"></a>
### D203
- **Category:** `L2`
- **Description:** Sequencer check implemented but wrong condition (inverted “up/down”, wrong timestamp field, or wrong comparison).

<a id="D204"></a><a id="d204"></a>
### D204
- **Category:** `L2`
- **Description:** Sequencer check exists but not applied to all sensitive paths (e.g., applied to swap, not to liqui- date/settle).

<a id="D205"></a><a id="d205"></a>
### D205
- **Category:** `L2`
- **Description:** Cross-domain auth: contract trusts L1 sender but fails to enforcemsg.sender == CrossDomainMessenger (OP-style).

<a id="D206"></a><a id="d206"></a>
### D206
- **Category:** `L2`
- **Description:** Cross-domain auth: contract readsmsg.senderinstead ofxDomainMessageSender()/ equivalent (sender spoof risk).

<a id="D207"></a><a id="d207"></a>
### D207
- **Category:** `L2`
- **Description:** Rollup address-aliasing bug: uses rawmsg.senderfor L1-originated calls without un-aliasing (Arbitrum- style).

<a id="D208"></a><a id="d208"></a>
### D208
- **Category:** `L2`
- **Description:** Bridge replay: missing “spent”/nonce consumption check on finalized messages (same withdrawal/message can be executed twice).

<a id="D209"></a><a id="d209"></a>
### D209
- **Category:** `L2`
- **Description:** Finality/challenge-window not enforced for optimistic bridges (accepts messages/withdrawals before finalization).

<a id="D210"></a><a id="d210"></a>
### D210
- **Category:** `L2`
- **Description:** L2 gas/refund-path reentrancy: refunds /call{value:...}("")to user assumed safe (breaks under delegated-code EOAs).

<a id="D211"></a><a id="d211"></a>
### D211
- **Category:** `WLT`
- **Description:** ERC-6492 counterfactual signature not supported (auth DoS/incompatible with modern wallet flows).

<a id="D212"></a><a id="d212"></a>
### D212
- **Category:** `WLT`
- **Description:** ERC-6492 validation executes attacker-controlled deployment calldata or calls (reentrancy/arbitrary side effects during “isValidSignature”).

<a id="D213"></a><a id="d213"></a>
### D213
- **Category:** `WLT`
- **Description:** ERC-6492 accepted without factory/deployer allowlist (counterfactual “wallet” can be spoofed).

<a id="D214"></a><a id="d214"></a>
### D214
- **Category:** `WLT`
- **Description:** EIP-7702: “EOA-only” gating viatx.origin==msg.sender(or variants) used for security (bypass- able).

<a id="D215"></a><a id="d215"></a>
### D215
- **Category:** `WLT`
- **Description:** EIP-7702:tx.origin-based “anti-reentrancy” is relied upon (now broken; reentrancy feasible with delegated code).

<a id="D216"></a><a id="d216"></a>
### D216
- **Category:** `WLT`
- **Description:** EIP-7702: refund-to-EOA/ETH-send assumed non-reentrant; delegated fallback enables reentry into protocol.

<a id="D217"></a><a id="d217"></a>
### D217
- **Category:** `WLT`
- **Description:** Missing nested EIP-712 binding (ERC-7739-style) for signatures used across multiple consumers (cross-app/relayer replay).

<a id="D218"></a><a id="d218"></a>
### D218
- **Category:** `WLT`
- **Description:** Signature digest useskeccak256(abi.encodePacked(...))with multiple dynamic types (collision -> forged authorization).

<a id="D219"></a><a id="d219"></a>
### D219
- **Category:** `STORE`
- **Description:** ERC-7201 namespace slot computed incorrectly (not following the spec formula/masking; silent state corruption).

<a id="D220"></a><a id="d220"></a>
### D220
- **Category:** `STORE`
- **Description:** Duplicate ERC-7201 namespace IDs across inheritance/libs (distinct modules share storage; cor- ruption/collision risk).

<a id="D221"></a><a id="d221"></a>
### D221
- **Category:** `REST`
- **Description:** Withdrawal-credentials capture: first-deposit/registration sets withdrawal creds without strict ownership/auth checks (front-runnable).

<a id="D222"></a><a id="d222"></a>
### D222
- **Category:** `REST`
- **Description:** Withdrawal-credential validation incomplete (accepts malformed prefixes/lengths; wrong credential type accepted).

<a id="D223"></a><a id="d223"></a>
### D223
- **Category:** `REST`
- **Description:** Slashing not reflected in exchange rate/share accounting (derivative token becomes undercollat- eralized).

<a id="D224"></a><a id="d224"></a>
### D224
- **Category:** `REST`
- **Description:** Reward index monotonicity trap: index only increases + precision/rounding -> eventual claim DoS/unclaimable rewards.

<a id="D225"></a><a id="d225"></a>
### D225
- **Category:** `REST`
- **Description:** Withdrawal queue accounting bug: shares not burned/locked before assets transfer (double-withdraw window).

<a id="D226"></a><a id="d226"></a>
### D226
- **Category:** `REST`
- **Description:** Delegation switch not checkpointed: user can claim rewards from old+new operator (double count- ing).

<a id="D227"></a><a id="d227"></a>
### D227
- **Category:** `REST`
- **Description:** Rebase mismatch: uses LSTbalanceOfwhere “shares” should be used (extractable via rebase timing).

<a id="D228"></a><a id="d228"></a>
### D228
- **Category:** `REST`
- **Description:** msg.value(or deposit amount) reused inside loops for multiple validator ops (over/under-deposit; replayed value bug).

<a id="D229"></a><a id="d229"></a>
### D229
- **Category:** `REST`
- **Description:** Deterministic vault/address derivation bug (CREATE2 inputs wrong -> funds stuck or credited to wrong vault).

<a id="D230"></a><a id="d230"></a>
### D230
- **Category:** `REST`
- **Description:** Fee-recipient/distributor callback reentrancy in reward distribution paths (repeat-claim/withdraw).

<a id="D231"></a><a id="d231"></a>
### D231
- **Category:** `ZK`
- **Description:** Missing public-input field/range checks (inputs not reduced mod field; invalid inputs pass or break soundness assumptions).

<a id="D232"></a><a id="d232"></a>
### D232
- **Category:** `ZK`
- **Description:** Missing “point on curve/subgroup” checks for elliptic-curve points supplied as public inputs or proof elements.

<a id="D233"></a><a id="d233"></a>
### D233
- **Category:** `ZK`
- **Description:** Proof verification return value ignored (verify called but not required for state transition).

<a id="D234"></a><a id="d234"></a>
### D234
- **Category:** `ZK`
- **Description:** Proof verifies, but contract fails to bind critical public inputs to execution context (e.g., recipi- ent/amount not checked vsmsg.sender).

<a id="D235"></a><a id="d235"></a>
### D235
- **Category:** `ZK`
- **Description:** Nullifier replay: contract lacks “seen nullifier” storage/bitmap (reused proof spends twice).

<a id="D236"></a><a id="d236"></a>
### D236
- **Category:** `ZK`
- **Description:** Root replay: accepts arbitrary/old Merkle roots (no valid-root set or epoch restriction).

<a id="D237"></a><a id="d237"></a>
### D237
- **Category:** `ZK`
- **Description:** Cross-chain/domain replay: proof not bound to chainId/contract domain (same proof valid elsewhere).

<a id="D238"></a><a id="d238"></a>
### D238
- **Category:** `ZK`
- **Description:** Known-vulnerable verifier template fingerprint (gnark/circom versions with documented issues; byte- pattern detection).

<a id="D239"></a><a id="d239"></a>
### D239
- **Category:** `ZK`
- **Description:** Precompile call failure not checked (pairing/EC ops viastaticcallwithout verifying success -> false positives).

<a id="D240"></a><a id="d240"></a>
### D240
- **Category:** `ZK`
- **Description:** Verifier uses unsafe assembly with missing calldata-length validation (reads garbage/malleability surface).

<a id="D241"></a><a id="d241"></a>
### D241
- **Category:** `MRK`
- **Description:** Leaf-vs-node collision: pre-hash leaf is 64 bytes and uses same hash as internal nodes (internal node can be “proven” as leaf).

<a id="D242"></a><a id="d242"></a>
### D242
- **Category:** `MRK`
- **Description:** Leaf hashing usesabi.encodePackedwith multiple dynamic args (hash collisions -> forged leaf).

<a id="D243"></a><a id="d243"></a>
### D243
- **Category:** `MRK`
- **Description:** Bitmap/index bug in claim tracking (wrong word/bit math -> double-claim or permanent lockout).

<a id="D244"></a><a id="d244"></a>
### D244
- **Category:** `MRK`
- **Description:** Multiproof misuse: proofFlags/leaves mismatch not validated (crafted multiproof accepted or claims bricked).

<a id="D245"></a><a id="d245"></a>
### D245
- **Category:** `MRK`
- **Description:** Leaf constructed fromlivemutable state (e.g., current token balance) instead of static entitlement (breaks claims/manipulable).

<a id="D246"></a><a id="d246"></a>
### D246
- **Category:** `MRK`
- **Description:** Missing domain separation in leaf (no “airdrop id”/contract binding) enabling cross-distribution proof reuse.

<a id="D247"></a><a id="d247"></a>
### D247
- **Category:** `MRK`
- **Description:** Merkle root update allowed after claims start without timelock/epoch rules (silent rug/clawback vector).

<a id="D248"></a><a id="d248"></a>
### D248
- **Category:** `MRK`
- **Description:** Claim verifies signature over one payload but Merkle leaf derived from another payload (inconsistent auth -> bypass/DoS).

<a id="D249"></a><a id="d249"></a>
### D249
- **Category:** `MRK`
- **Description:** Sorted-vs-unsorted Merkle mismatch (on-chain assumes sorted pairs; off-chain tree not) causing systemic claim failure.

<a id="D250"></a><a id="d250"></a>
### D250
- **Category:** `MRK`
- **Description:** Leaf includes variable-length strings/bytes viaabi.encodePacked.