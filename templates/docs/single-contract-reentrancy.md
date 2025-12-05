# Single-Contract Reentrancy

This detector module implements single-contract reentrancy, the classic "interaction before effects" failure mode. This occurs when:

1. A public or external function performs an external call.
2. That call can transfer control to untrusted code.
3. The attacker re-enters the victim contract before the critical state update happens, allowing state-dependent logic to execute on stale assumptions.

We scope this detector to basic single-contract class. The entrypoint is public/external functions. The signal is every "read-before external call" combined with "write-after external call." The goal is to pinpoint CEI violations that enable simple reentrancy paths.

## What is a finding here?

A finding is emitted when the detector observes all of the following:

* State is read before the call
* The same state is written after the call
* That state wasn't already written before the call.

Formally:

```
overlap = (read_before - written_before) and written_after
return overlap if overlap ≠ ∅ else None
```

## What is an external call here?

