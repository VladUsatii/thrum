# Router

The first crucial step of Thrum's pipeline is the Router.

```
This turns an arbitrary Solidity repo - that a protocol submits for a scan - into its compiled, analyzed version, or gives you instructions to make it compilable.
```

## What does Router do?

The user's first step is to run `thrum scan .`. After this is run, your repo will be passed into a pipeline that compiles and prepares your repo for our detection suite.

When compilation succeeds, Thrum Router will emit:

- a selected project (or possibly a collection of monorepos)
- a compile plan describing:
    * the working directory to run from,
    * dependency install intent,
    * compilation commands,
    * entrypoints required by the toolchain,
    * and any other info usable to compile.
- compiler outputs suitable for downstream analysis
- diagnostics suitable for CI logs in case of a failure, explaining what you need to build to get from a `failed -> working` compilation.

For Solidity repos, Thrum compiles via framework-native commands (e.g. npx hardhat compile), but we built some extra magic in case that fails (i.e. we're framework-agnostic).

## Determinism on success

Thrum treats compilation as a deterministic pipeline step. This is because we're fundamentally an autonomous tool, so if users run into errors from *our* side, we must have robust solutions in place for every edge case. Administratively, supplying the user with instructions on how to correctly compile their program *could be* the difference between a satisfied, trialed user, and a dissatisfied, confused user.

* Given the same repository snapshot, the same toolchain, and the same dependence graph, we aim to produce the same compile and the same outputs every time.
* When reproducibility is expected, Thrum prefers lockfile-respecting installs (e.g. `yarn`'s `--frozen-lockfile` and `pnpm`'s `--frozen-lockfile`).
* When npm is used, CI-style installs are expected to be lockfile-driven (e.g., `npm ci`).

## Determinism on failure

Thrum will refuse to compile when the repo is incomplete in a way that would make results non-reproducible or misleading. This is a deliberate brake pedal. Failing fast is preferable to producing partial artifacts which downstream detectors might treat as authoritative. We want to be deterministically correct on our outputs.

To help you make your program compilable and deterministic, we mark your repo incomplete if, at compile time, it lacks one or more of the following:

| Requirement | Description |
| ----------- | ----------- |
| Source inputs | No meaningful compile targets specified |
| Dependency inputs | Missing vendored dependencies, missing lockfile or manifest consistency, or missing submodules |
| Toolchain inputs | Configuration or pinned versions needed for reproduction |
| Integrity inputs |  Placeholder files, truncated dependencies, or missing content |

## Rejection Log

We list all canonical reasons for a rejected Router submission.

> Again, we want to re-iterate our goal of delivering a satisfying user experience, and allowing teams to continuously assure that their program is compilable and free of critical, financial-loss-grade vulnerabilities. In so doing, we've constructed this canonical list. We hope you find it helpful when debugging your scan submissions.

| Code | Category | Outcome | What it means (externally observable) | Typical remediation |
|---|---|---:|---|---|
| `missing_manifest` | Structure | Block | A detected project has no required manifest/config for its toolchain (e.g., package manifest missing). | Add/restore the expected manifest file(s) for the selected project root. |
| `missing_sources` | Inputs | Block | The expected source directory exists but contains no compile targets (e.g., no `.sol` where the tool expects them). | Ensure the repo includes contract sources in the expected location(s). |
| `missing_dependency_graph` | Dependencies | Block | Dependencies cannot be resolved from the repo snapshot (e.g., required vendor dirs absent and install cannot be made reproducible). | Vendor deps, include lockfiles, or ensure the dependency manager can install deterministically. |
| `missing_lockfile` | Reproducibility | Block/Warn (policy) | A dependency manager is detected but no lockfile is present where reproducibility is required. | Commit the lockfile (e.g., `yarn.lock`, `pnpm-lock.yaml`, `package-lock.json`). :contentReference[oaicite:3]{index=3} |
| `lockfile_out_of_sync` | Reproducibility | Block | The lockfile would need to change to satisfy the manifest, which breaks determinism expectations. | Regenerate lockfile and commit changes; keep manifest/lockfile consistent. :contentReference[oaicite:4]{index=4} |
| `missing_submodules` | Integrity | Block | The repo references submodules that are not present in the working tree. | Initialize/update submodules (e.g., `git submodule update --init --recursive`) and re-run. :contentReference[oaicite:5]{index=5} |
| `placeholder_content_present` | Integrity | Block | The repo contains placeholder content instead of real sources/deps (common with LFS-managed content not fetched). | Ensure the full content is present in the snapshot used for compilation. |
| `unresolved_imports` | Inputs | Block | Solidity imports cannot be resolved using the repo snapshot + declared dependency layout. | Add missing dependencies or correct import paths/remappings. |
| `missing_node_modules` | Dependencies | Block/Warn (policy) | A Node-based toolchain is detected but dependencies are not installed in the execution environment. | Run the deterministic install step for the detected package manager (CI-style). :contentReference[oaicite:6]{index=6} |
| `requires_network_access` | Environment | Block (strict) | Compilation would depend on fetching remote inputs at runtime, making results non-reproducible in a sealed environment. | Provide vendored deps or allow networked compilation explicitly (policy-dependent). |
| `unsupported_toolchain` | Capability | Block | The repo requires a compiler/framework version or stack not supported by the current runtime. | Pin supported versions or provide an alternative compilation pathway. |
| `ambiguous_project_root` | Selection | Block/Warn (policy) | Multiple candidate projects exist and none can be selected without risking incorrect compilation. | Specify the intended project root or restructure the repo. |
| `repo_too_large` | Resource | Block (strict) | Repo exceeds configured size/file limits for safe deterministic compilation. | Reduce scope (target a subdir), or use enterprise limits. |
| `environment_required` | Configuration | Block/Warn (policy) | The build expects required environment variables/secrets that are not provided in the compile context. | Provide required env vars via approved secret injection mechanisms (never commit secrets). |
| `interactive_build` | Automation | Block | The build requires interactive prompts. | Provide non-interactive configuration or scripts suitable for CI. |