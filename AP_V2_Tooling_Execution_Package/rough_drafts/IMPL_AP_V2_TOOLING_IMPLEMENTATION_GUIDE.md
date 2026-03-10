# IMPL_AP_V2_TOOLING_IMPLEMENTATION_GUIDE
## Implementation Guide: ARCHON_PRIME V2 Tooling Architecture

---

## Guide Identity

| Field | Value |
|---|---|
| Artifact ID | IMPL-010 |
| System | ARCHON_PRIME |
| Platform | Python 3.11 / Codespaces |
| Artifact Type | Implementation Guide |
| Version | v1 |
| Status | Draft |
| Schema | AP_IMPLEMENTATION_GUIDE_V2_SCHEMA.json |
| Source Specification | SPEC-010 SPEC_AP_V2_TOOLING_ARCHITECTURE.md v1 |
| Source Spec Status | Draft |
| Author | Claude / Formalization_Expert |
| Date | 2026-03-10 |
| Approved By | |
| Phase | Phase 2 — Specification Production (active) |

---

## Lineage

| Field | Value |
|---|---|
| Source Spec | SPEC-010 |
| Prior Version | null |
| Supersedes | null |

---

## 1. Implementation Overview

This guide provides the deterministic build sequence for the ARCHON_PRIME V2 tooling layer as defined in SPEC-010. It is organized into 10 implementation phases that map directly to the SPEC-010 pipeline stage model (S0–S10).

**Key principle:** Every phase is a gate. A phase does not begin until its predecessor's exit condition is confirmed by the architecture validator. Phase ordering is non-negotiable.

**Repo root for all paths:** `/workspaces/ARCHON_PRIME/`

**Canonical domain constraint (all paths must begin with one of):**
```
WORKFLOW_MUTATION_TOOLING/
WORKFLOW_TARGET_AUDITS/
WORKFLOW_TARGET_PROCESSING/
```

**Read-only directories (no writes permitted):**
```
AP_SYSTEM_CONFIG/
AP_SYSTEM_AUDIT/
```

---

## 2. Prerequisites

| # | Prerequisite | Blocking | Verification |
|---|---|---|---|
| P-001 | SPEC-010 approved by Architect | Yes | Spec status field = 'approved' |
| P-002 | SPEC-004 (Architecture Validator) approved and `validate_architecture.py` implemented | Yes | Validator executable at `WORKFLOW_MUTATION_TOOLING/tools/validation/validate_architecture.py` |
| P-003 | V2 module registry pre-populated with all 72 module entries | Yes | `WORKFLOW_MUTATION_TOOLING/registry/module_registry.json` validates against AP_MASTER_SPEC_V2_SCHEMA.json |
| P-004 | CL-G1 schema naming resolved (AP_MASTER_SPEC_V2_SCHEMA.json canonical name confirmed) | Yes | Architect declaration on file |
| P-005 | OQ-004 mutation_allowed default confirmed | Yes | `crawl_config.json` template finalized |
| P-006 | Python 3.11 available in Codespaces environment | Yes | `python3 --version` ≥ 3.11 |
| P-007 | `pyproject.toml` present and dependency list confirmed | No | Manual check |

---

## 3. Deterministic Build Sequence

Phases must execute in the order defined below. No phase may begin before its predecessor's exit condition is confirmed.

```
PHASE_0 — Foundation + Config
    └─► PHASE_1 — Audit Migration
            └─► PHASE_2 — Repo Analysis Subsystem (AP_TOOL_PROP_01)
                    └─► PHASE_3 — Analysis Tools
                            └─► PHASE_4 — Simulation + Planning
                                    ├─► PHASE_5 — Validators + Mutation Ops (parallel with PHASE_4 in progress)
                                    └─► PHASE_6 — Crawl Execution
                                            └─► PHASE_7 — Repair + Quarantine
                                                    └─► PHASE_8 — Reporting + Commit
                                                            └─► PHASE_9 — Orchestration
```

Phases 4 and 5 may proceed in parallel once Phase 3 is complete. All others are strictly sequential.

---

## 4. Header Injection Rules

Every module written during this implementation MUST carry the following V2 AP header at the top of the file, before all imports.

```python
# ARCHON PRIME MODULE HEADER
# module_id: [M-ID from module registry]
# module_name: [filename without .py]
# subsystem: [subsystem ID from SPEC-010]
# canonical_path: WORKFLOW_MUTATION_TOOLING/[path/to/module.py]
# responsibility: [one-sentence description]
# runtime_stage: [initialization|analysis|processing|validation|repair|audit|reporting|utility]
# allowed_imports: [list of stdlib modules and internal AP subsystems]
# forbidden_imports: [list of forbidden modules — always includes target repo runtime]
# spec_reference: SPEC-010.section.[N]
# implementation_phase: PHASE_[N]
# authoring_authority: ARCHON_PRIME
# version: 1.0
# status: canonical
```

**Header Validation Rules:**
- HVR-001: Header block must be the first content in the file (before docstrings and imports)
- HVR-002: All 13 fields must be present
- HVR-003: `canonical_path` must begin with `WORKFLOW_MUTATION_TOOLING/`
- HVR-004: `module_id` must match the registry entry exactly
- HVR-005: `forbidden_imports` MUST always include all LOGOS target repo modules

---

## 5. Spec Compliance Checks

Before each phase begins, the following checks are run:

| Check | Tool | Pass Condition |
|---|---|---|
| Architecture validation | `validate_architecture.py --spec SPEC-010` | `architecture_valid: true` |
| Module registry validation | `schema_registry.py` | Registry validates against AP_MASTER_SPEC_V2_SCHEMA.json |
| Canonical domain check | Architecture validator AVR-001 | All modules under WORKFLOW_MUTATION_TOOLING/ |
| Header compliance check | Architecture validator AVR-003 | All modules carry valid V2 headers |

If any check fails, the phase does not begin. A `halt_diagnostic.json` is produced.

---

## 6. Module Generation Contract

For every new module created during this implementation:

1. Registry entry exists before VS Code prompt is issued
2. V2 header is the first content in the file
3. Module produces structured JSON output (no stdout-only output — see VF-003)
4. Module accepts target repo root as runtime parameter (no hardcoded paths — see VF-008)
5. Module supports dry-run mode (for all mutation-stage modules)
6. Module does not write to AP_SYSTEM_CONFIG/ or AP_SYSTEM_AUDIT/
7. Module does not import from target repo runtime modules

---

## 7. Analog Reconciliation Process

Analog modules (legacy modules that partially implement a spec module) must be reconciled before the spec module is built.

**Process per analog:**

1. Read analog module in full
2. Identify reusable logic (algorithm, data structure, utility function)
3. Identify non-compliant elements (hardcoded paths, stdout output, missing header, passthrough logic)
4. Decision: migrate (reuse and V2-header-inject) or rebuild (analog is too far from spec to refactor)
5. If migrate: copy to canonical path, inject V2 header, fix non-compliant elements
6. If rebuild: preserve analog in `WORKFLOW_TARGET_AUDITS/logs/legacy/[module_name]_v1.py` before overwriting
7. Register canonical module in module_registry.json

**Rebuild threshold:** If the analog requires >40% of its logic to change to meet the spec, rebuild is preferred. Migrating a fundamentally broken module (e.g., `dependency_graph.py` passthrough) creates technical debt.

---

## 8. Enhancement Integration Rules

Any enhancement not defined in SPEC-010 follows the enhancement lifecycle:

1. Enhancement proposal submitted to Architect
2. Architect decision obtained
3. SPEC-010 updated with new module entry
4. IMPL-010 updated with new phase step
5. Module registry updated
6. Implementation proceeds

**Blocking rule:** No enhancement may be coded before the spec and registry are updated. GPT prompt compiler may not issue a prompt for an unregistered module.

---

## 9. Artifact Directory Rules

| Artifact Type | Canonical Output Path |
|---|---|
| Stage reports | `WORKFLOW_TARGET_AUDITS/reports/[stage_name]_report.json` |
| Audit logs | `WORKFLOW_TARGET_AUDITS/logs/[audit_name].json` |
| Gap analysis | `WORKFLOW_TARGET_AUDITS/reports/AP_REPOSITORY_GAP_ANALYSIS.json` |
| Simulation report | `WORKFLOW_MUTATION_TOOLING/simulation/simulation_report.json` |
| Pre-crawl checklist | `WORKFLOW_MUTATION_TOOLING/configs/pre_crawl_checklist.json` |
| Architecture validation report | `WORKFLOW_TARGET_AUDITS/reports/architecture_validation_report.json` |
| Halt diagnostic | `WORKFLOW_TARGET_AUDITS/logs/halt_diagnostic.json` |
| Pipeline execution manifest | `WORKFLOW_TARGET_AUDITS/reports/pipeline_execution_manifest.json` |
| Repair plan | `WORKFLOW_TARGET_AUDITS/reports/repair_plan.json` |
| Commit manifest | `WORKFLOW_TARGET_AUDITS/reports/commit_manifest.json` |
| Legacy module archive | `WORKFLOW_TARGET_AUDITS/logs/legacy/` |

---

## 10. Drift Detection Audit

At the end of each phase, before proceeding to the next:

1. Run `validate_architecture.py` against WORKFLOW_MUTATION_TOOLING/
2. Confirm no unexpected modules have been created
3. Confirm all new modules appear in module_registry.json
4. Confirm no modules exist outside canonical domain
5. Confirm all headers pass HVR-001 through HVR-005

If any drift is detected: halt, produce `halt_diagnostic.json`, escalate to Architect.

---

## 11. Architecture Validation Gate

Per SPEC-004, the architecture validator runs at:
- Start of each phase (pre-build gate)
- End of each phase (post-build gate)
- At S5→S6 pipeline transition (pre-crawl gate)
- At S9 (pre-commit gate)

CLI invocation:
```
python validate_architecture.py \
  --spec SPEC-010 \
  --registry WORKFLOW_MUTATION_TOOLING/registry/module_registry.json \
  --output WORKFLOW_TARGET_AUDITS/reports/architecture_validation_report.json
```

Exit codes: 0 = clean, 1 = blocking findings, 2 = non-blocking findings only.

---

## 12. Implementation Stages

---

### PHASE_0 — Foundation + Config

**Entry condition:** SPEC-010 approved; SPEC-004 validator running.

**Exit condition:** All foundation modules present; all config files at canonical paths; module registry validated; architecture validator passes.

**Modules to build:**

| Module ID | Module | Path | Action | Header Required |
|---|---|---|---|---|
| M00 | schema_registry.py | WORKFLOW_MUTATION_TOOLING/tools/normalization_tools/ | Add V2 header | Yes |
| M01 | routing_table_loader.py | WORKFLOW_MUTATION_TOOLING/orchestration/task_router/ | Validate analog; add V2 header | Yes |
| M01-A | config_loader.py | WORKFLOW_MUTATION_TOOLING/controllers/ | Validate analog; add V2 header | Yes |
| M02 | repair_registry_loader.py | WORKFLOW_MUTATION_TOOLING/tools/audit_tools/ | Create new | Yes |

**Config files to create:**

| File | Path | Source |
|---|---|---|
| crawl_config.json | WORKFLOW_MUTATION_TOOLING/configs/crawl_configs/ | Template from SPEC-010 + OQ-004 resolution |
| logos_targets.yaml | WORKFLOW_MUTATION_TOOLING/configs/crawl_configs/ | Architect-facing; LOGOS repo path |
| ap_config.yaml | WORKFLOW_MUTATION_TOOLING/configs/crawl_configs/ | Architect-override YAML |
| routing_table.json | WORKFLOW_MUTATION_TOOLING/orchestration/task_router/ | Derived from OUTPUT_ROUTING_TABLE.md |
| repair_registry.json (canonical) | WORKFLOW_MUTATION_TOOLING/configs/repair_configs/ | Expand existing registry |

**Registry update:** Populate `module_registry.json` with all 72 V2 canonical module entries before Phase 1 begins.

**Build sequence:**
1. Validate existing `schema_registry.py` — inject V2 header; no logic changes required
2. Validate existing `routing_table_loader.py` analog — inject V2 header; verify it loads from `routing_table.json` (not hardcoded)
3. Validate existing `config_loader.py` analog — inject V2 header; add validation for all required config fields
4. Create `repair_registry_loader.py` — load `configs/repair_configs/repair_registry.json`; expose `get_operator(issue_type)` and `list_operators()` functions
5. Create all 5 config files at canonical paths
6. Populate full V2 module registry
7. Run architecture validator — confirm PHASE_0 exit condition

---

### PHASE_1 — Audit Migration

**Entry condition:** PHASE_0 complete; architecture validator clean.

**Exit condition:** All 18 audit modules at canonical paths under `WORKFLOW_MUTATION_TOOLING/tools/audit_tools/`; all have V2 headers; `run_audit_suite.py` and `run_governance_audit.py` accept `target_path` parameter.

**Critical fix required (addresses VF-003 pattern):** `run_audit_suite.py` and `run_governance_audit.py` currently do not accept a configurable target path — they operate on the local repo only. Both must be modified to accept a `target_path` argument.

**Modules to migrate:**

| Module | Current Location | Target Location | Action |
|---|---|---|---|
| audit_utils.py | (various) | WORKFLOW_MUTATION_TOOLING/tools/audit_tools/ | Migrate + V2 header |
| circular_dependency_audit.py | tools/audit_tools/ | WORKFLOW_MUTATION_TOOLING/tools/audit_tools/ | Confirm path + V2 header |
| cross_package_dependency_audit.py | tools/audit_tools/ | WORKFLOW_MUTATION_TOOLING/tools/audit_tools/ | Confirm path + V2 header |
| duplicate_module_audit.py | tools/audit_tools/ | WORKFLOW_MUTATION_TOOLING/tools/audit_tools/ | Confirm path + V2 header |
| facade_bypass_audit.py | tools/audit_tools/ | WORKFLOW_MUTATION_TOOLING/tools/audit_tools/ | Confirm path + V2 header |
| header_schema_audit.py | tools/audit_tools/ | WORKFLOW_MUTATION_TOOLING/tools/audit_tools/ | Confirm path + V2 header |
| import_surface_audit.py | tools/audit_tools/ | WORKFLOW_MUTATION_TOOLING/tools/audit_tools/ | Confirm path + V2 header |
| module_path_ambiguity_audit.py | tools/audit_tools/ | WORKFLOW_MUTATION_TOOLING/tools/audit_tools/ | Confirm path + V2 header |
| namespace_shadow_audit.py | tools/audit_tools/ | WORKFLOW_MUTATION_TOOLING/tools/audit_tools/ | Confirm path + V2 header |
| orphan_module_audit.py | tools/audit_tools/ | WORKFLOW_MUTATION_TOOLING/tools/audit_tools/ | Confirm path + V2 header |
| run_audit_suite.py | tools/audit_tools/ | WORKFLOW_MUTATION_TOOLING/tools/audit_tools/ | Add target_path param + V2 header |
| run_governance_audit.py | tools/audit_tools/ | WORKFLOW_MUTATION_TOOLING/tools/audit_tools/ | Add target_path param + V2 header |

**Build sequence:**
1. Confirm all audit_tools modules are under WORKFLOW_MUTATION_TOOLING/tools/audit_tools/ (may already be correct)
2. Inject V2 headers into all 18 modules
3. Modify `run_audit_suite.py`: add `target_path: str` parameter to `run()` entry function; all audit modules receive target_path at invocation
4. Modify `run_governance_audit.py`: same modification
5. Verify all audit modules produce JSON output to declared artifact paths (not stdout)
6. Run architecture validator — confirm PHASE_1 exit condition

---

### PHASE_2 — Repo Analysis Subsystem (AP_TOOL_PROP_01)

**Entry condition:** PHASE_1 complete; architecture validator clean.

**Exit condition:** All four AP_TOOL_PROP_01 modules operational; pipeline produces `AP_STRUCTURE_ANALYSIS.json`, `AP_SUBSYSTEM_ANALYSIS.json`, `AP_REPOSITORY_GAP_ANALYSIS.json` against synthetic test fixture.

**This phase formalizes AP_TOOL_PROP_01 from rough draft to spec-compliant implementation.**

**Modules to create:**

| Module ID | Module | Path | Inputs | Outputs |
|---|---|---|---|---|
| M-RSA-01 | ap_repo_scanner.py | WORKFLOW_MUTATION_TOOLING/tools/repo_mapping/ | target_path (runtime) | AP_ARTIFACT_INDEX.json, AP_DIRECTORY_TREE_CURRENT.json, AP_EMPTY_DIRECTORIES.json |
| M-RSA-02 | ap_structure_analyzer.py | WORKFLOW_MUTATION_TOOLING/tools/repo_mapping/ | AP_ARTIFACT_INDEX.json, AP_DIRECTORY_TREE_CURRENT.json | AP_STRUCTURE_ANALYSIS.json |
| M-RSA-03 | ap_subsystem_analyzer.py | WORKFLOW_MUTATION_TOOLING/tools/repo_mapping/ | AP_STRUCTURE_ANALYSIS.json, AP_ARTIFACT_INDEX.json | AP_SUBSYSTEM_ANALYSIS.json |
| M-RSA-04 | ap_gap_analysis_engine.py | WORKFLOW_MUTATION_TOOLING/tools/repo_mapping/ | AP_SUBSYSTEM_ANALYSIS.json, design_specs (optional) | AP_REPOSITORY_GAP_ANALYSIS.json |

**ap_repo_scanner.py functional contract:**
- Full repository traversal with configurable target_path
- Exclusion filtering (venv, .git, __pycache__, test fixtures)
- File classification (python_module, config_json, config_yaml, documentation, schema, unknown)
- Artifact mirroring (optional copy of files to staging area)
- Directory tree generation (hierarchical JSON)
- Empty directory detection
- Artifact indexing (flat list with path, size, type, line_count)
- Output: AP_ARTIFACT_INDEX.json, AP_DIRECTORY_TREE_CURRENT.json, AP_EMPTY_DIRECTORIES.json

**ap_structure_analyzer.py functional contract:**
- Module clustering (group modules by directory proximity and naming convention)
- Subsystem boundary detection (identify directories that constitute functional subsystems)
- Directory hierarchy analysis (depth distribution, naming patterns)
- Orphan directory detection (directories with no Python files in subtree)
- Abnormal file placement detection (Python files in docs/config/test directories)
- Configuration vs. runtime separation check
- Structural anomaly reporting (unexpected directory names, flat vs. hierarchical mismatches)
- Output: AP_STRUCTURE_ANALYSIS.json

**ap_subsystem_analyzer.py functional contract:**
- Empty subsystem directory detection
- Missing module group detection (subsystem present but all modules missing)
- Incomplete subsystem detection (some modules present, others missing)
- Stub module detection (module present but below functional threshold — e.g., <20 lines)
- Partial runtime surface detection (subsystem has interface but no implementation)
- Incomplete configuration layer detection (configs referenced but not present)
- Output: AP_SUBSYSTEM_ANALYSIS.json with per-subsystem completeness score and status

**ap_gap_analysis_engine.py functional contract:**
- Missing module identification with priority ranking
- Missing subsystem identification
- Architectural drift detection (module at wrong path, wrong name convention)
- Unused directory identification
- Orphan file identification (files not referenced by any import)
- Incomplete implementation identification
- If design specs provided: spec-vs-actual gap computation
- Output: AP_REPOSITORY_GAP_ANALYSIS.json with remediation_priority per finding

**Build sequence:**
1. Create ap_repo_scanner.py — build as standalone with clear public API (`scan(target_path) → (index, tree, empty_dirs)`)
2. Unit test against synthetic fixture (10-dir, 20-file test repo)
3. Create ap_structure_analyzer.py — consumes scanner outputs
4. Create ap_subsystem_analyzer.py — consumes structure analysis
5. Create ap_gap_analysis_engine.py — consumes subsystem analysis
6. Integration test: run full M-RSA-01 → M-RSA-04 chain against AP_SYSTEM_AUDIT test data
7. Verify AP_REPOSITORY_GAP_ANALYSIS.json schema matches expected structure
8. Run architecture validator — confirm PHASE_2 exit condition

---

### PHASE_3 — Analysis Tools

**Entry condition:** PHASE_2 complete; architecture validator clean.

**Exit condition:** All S2 artifact contracts producible (`module_index.json`, `dependency_graph.json`, `circular_dependencies.json`, `runtime_phase_map.json`, `canonical_import_registry.json`) against test fixture.

**Critical rebuild required:** `dependency_graph.py` analog is a passthrough (VF-006). It must be rebuilt as a proper graph builder.

**Modules to create/rebuild:**

| Module ID | Module | Action | Critical Notes |
|---|---|---|---|
| M10 | repo_directory_scanner.py | Replace analog (repo_scanner.py) | Must accept target_path param |
| M11 | python_file_collector.py | Create new | Produces structured file metadata |
| M12 | import_extractor.py | Migrate analog | AST-based import extraction |
| M13 | symbol_import_extractor.py | Create new | Symbol-level (from X import Y) extraction |
| M14 | header_schema_scanner.py | Migrate analog (header_validator.py) | Must scan all modules, not validate one |
| M15 | governance_contract_scanner.py | Create new | Detect presence and compliance of governance contracts |
| M16 | runtime_phase_scanner.py | Create new | Extract runtime_phase from module headers |
| M17 | concept_spec_gap_detector.py | Create new | Compare concept artifacts vs. spec artifacts |
| M20 | module_index_builder.py | Create new | Builds comprehensive module index |
| M21 | dependency_graph_builder.py | Rebuild — replace passthrough analog | MUST construct actual graph, not copy input |
| M22 | circular_dependency_detector.py | Migrate analog | Detect cycles in dependency graph |
| M23 | runtime_phase_mapper.py | Create new | Map modules to phases using phase scanner output |
| M24 | runtime_boot_sequencer.py | Create new | Topological sort of dependency graph for boot order |
| M25 | canonical_import_registry_builder.py | Create new | Build lockable canonical import registry |

**dependency_graph_builder.py — functional contract (VF-006 fix):**
- Input: `repo_imports.json` (line-level import map)
- Process: construct directed graph where nodes = modules, edges = import relationships
- Output: `dependency_graph.json` with nodes[], edges[], metrics{avg_in_degree, avg_out_degree, total_edges}
- Must NOT be a passthrough copy of input

**Build sequence:**
1. Rebuild `repo_directory_scanner.py` (replace `repo_scanner.py` analog)
2. Create `python_file_collector.py`
3. Migrate `import_extractor.py`
4. Create `symbol_import_extractor.py`
5. Migrate `header_schema_scanner.py` (from `header_validator.py` analog)
6. Create `governance_contract_scanner.py`
7. Create `runtime_phase_scanner.py`
8. Rebuild `dependency_graph_builder.py` (CRITICAL — replace passthrough)
9. Migrate `circular_dependency_detector.py`
10. Create `module_index_builder.py`
11. Create `runtime_phase_mapper.py`
12. Create `runtime_boot_sequencer.py`
13. Create `canonical_import_registry_builder.py`
14. Create `concept_spec_gap_detector.py`
15. Run full S2 pipeline against test fixture — confirm all artifact contracts
16. Run architecture validator — confirm PHASE_3 exit condition

---

### PHASE_4 — Simulation + Planning

**Entry condition:** PHASE_3 complete.

**Exit condition:** `simulation_report.json` with `crawl_permitted` field produced; `crawl_planner.py` produces ordered execution graph.

**Rebuild required:** `repo_simulator.py` is a skeleton (VF-005). It must be rebuilt.

**Modules:**

| Module ID | Module | Action | Critical Notes |
|---|---|---|---|
| M30 | repo_simulator.py | Rebuild skeleton | MUST model full mutation plan; MUST produce simulation_report.json with crawl_permitted field |
| M31 | runtime_simulator.py | V2 header injection | Present and functional |
| M32 | import_simulator.py | V2 header injection | Present and functional |
| M33 | simulation_coordinator.py | Create new | Orchestrates M30–M32; aggregates results |
| M38 | crawl_planner.py | Create new | Produces ordered execution graph from dependency data |
| M39 | execution_graph_builder.py | Create new | Builds execution graph as dependency-ordered module list |

**repo_simulator.py functional contract (VF-005 fix):**
- Input: S2 analysis artifacts (module_index.json, dependency_graph.json, runtime_phase_map.json)
- Input: mutation plan (from crawl_planner.py)
- Process: model full mutation sequence — for each planned mutation, simulate the state change without executing it
- Output: `simulation_report.json` with fields: `crawl_permitted`, `simulated_mutations[]`, `predicted_conflicts[]`, `risk_assessment`, `estimated_module_count`, `blocking_issues[]`
- `crawl_permitted: false` if ANY predicted conflict or blocking issue is CRITICAL severity
- MUST produce JSON output — no stdout (VF-003)

**Build sequence:**
1. Rebuild `repo_simulator.py`
2. Inject V2 headers into `runtime_simulator.py` and `import_simulator.py`
3. Create `simulation_coordinator.py`
4. Create `crawl_planner.py`
5. Create `execution_graph_builder.py`
6. Integration test: run simulation pipeline against Phase 3 test fixture outputs
7. Verify simulation_report.json contains crawl_permitted field
8. Run architecture validator — confirm PHASE_4 exit condition

---

### PHASE_5 — Validators + Mutation Operators

**Entry condition:** PHASE_3 complete. (Can run in parallel with PHASE_4.)

**Exit condition:** All validator and mutation modules pass unit tests against synthetic error fixtures.

**Modules:**

| Module ID | Module | Action | Notes |
|---|---|---|---|
| M50 | header_injector.py | Create new (refactor from repair/operators/header_injection_operator.py analog) | Must support simulation mode |
| M51 | import_rewriter.py | Create new (refactor from repair/operators/import_rewrite_operator.py analog) | Must support simulation mode |
| M62 | syntax_validator.py | Create new | AST parse; catch SyntaxError |
| M63 | governance_validator.py | Create new | Validates governance contract compliance |
| M64 | phase_validator.py | Create new | Validates runtime phase assignments |

**Simulation mode contract for M50, M51:**
- All mutation operators MUST accept `dry_run: bool` parameter
- When `dry_run=True`: compute the mutation plan; do NOT write to filesystem; return plan as structured JSON
- When `dry_run=False`: execute mutation; return result as structured JSON
- This directly addresses VF-007 and supports LEVEL_2 (dry-run) safety mode

**Analog preservation rule for M50, M51:** Before replacing the analogs in `repair/operators/`, copy them to `WORKFLOW_TARGET_AUDITS/logs/legacy/` (non-deletion policy).

**Build sequence:**
1. Archive `repair/operators/header_injection_operator.py` → `WORKFLOW_TARGET_AUDITS/logs/legacy/`
2. Archive `repair/operators/import_rewrite_operator.py` → `WORKFLOW_TARGET_AUDITS/logs/legacy/`
3. Create `header_injector.py` — refactor from analog; add dry_run support; V2 header
4. Create `import_rewriter.py` — refactor from analog; add dry_run support; V2 header
5. Create `syntax_validator.py`, `governance_validator.py`, `phase_validator.py`
6. Unit test each module against synthetic fixtures with both dry_run=True and dry_run=False
7. Run architecture validator — confirm PHASE_5 exit condition

---

### PHASE_6 — Crawl Execution

**Entry condition:** PHASE_4 and PHASE_5 both complete.

**Exit condition:** `crawl_executor.py` (M60) accepts configurable target repo root; produces structured JSON output; processes at least 100 modules without error against test fixture.

**Rebuild required:** `crawl_engine.py` is non-functional for V2 purposes (VF-003, VF-008).

**Modules:**

| Module ID | Module | Action | Critical Notes |
|---|---|---|---|
| M60 | crawl_engine.py | V2 rebuild | MUST accept target_path param; MUST produce JSON output; no stdout; configurable root |
| M61 | module_processor.py | Create new | Processes individual module through validator chain → mutation operator chain |
| M65 | crawl_monitor.py | Replace skeleton (VF-004) | MUST poll actual filesystem/in-memory state; no sleep-and-print |

**crawl_engine.py functional contract (VF-003, VF-008 fix):**
- Entry point: `execute_crawl(target_path: str, execution_graph: dict, config: dict) → dict`
- Process: iterate execution_graph module list in declared order; pass each module to module_processor.py; collect results
- Output: `crawl_execution_report.json` with per-module results, timing, error count, halt_reason (if halted)
- HALT on any CRITICAL error from module_processor
- mutation_allowed flag checked before any write operation

**crawl_monitor.py functional contract (VF-004 fix):**
- Must accept a shared state object (progress_state dict or threading.Event)
- Must poll actual crawl progress (modules_processed, modules_total, current_module, errors_encountered)
- Must produce periodic `crawl_progress.json` snapshots (not stdout prints)
- Must respond to HALT signal

**Build sequence:**
1. Archive `crawler/core/crawl_engine.py` original → `WORKFLOW_TARGET_AUDITS/logs/legacy/`
2. Archive `crawler/monitor/crawl_monitor.py` original → `WORKFLOW_TARGET_AUDITS/logs/legacy/`
3. Build `module_processor.py` — processes single module through: syntax_validator → governance_validator → phase_validator → [mutation operators if mutation_allowed]
4. Rebuild `crawl_engine.py` — iterate execution graph; invoke module_processor per module
5. Rebuild `crawl_monitor.py` — poll state object; write progress JSON
6. Integration test: run crawl pipeline against 50-module synthetic fixture
7. Verify JSON output structure; verify no stdout-only output
8. Run architecture validator — confirm PHASE_6 exit condition

---

### PHASE_7 — Repair + Quarantine

**Entry condition:** PHASE_6 complete.

**Exit condition:** Error classification, routing, and repair execution operational. Quarantine manager produces valid stub for any quarantined module.

**Modules:**

| Module ID | Module | Action | Notes |
|---|---|---|---|
| M70 | error_classifier.py | Create new | Classify crawl errors by type and severity |
| M71 | repair_router.py | Create new (refactor from module_relocation_operator analog) | Route error to correct repair operator |
| M72 | repair_executor.py | Create new | Execute repairs from repair_registry; enforce dry_run contract |
| M80 | quarantine_manager.py | Create new (refactor from namespace_disambiguator analog) | Produce syntax-valid stub; preserve original in legacy/ |

**error_classifier.py functional contract:**
- Input: `crawl_execution_report.json`
- Classification taxonomy (from FAILURE_TAXONOMY.md):
  - `import_error` → repair operator: ImportRewriteOperator
  - `header_violation` → repair operator: HeaderInjectionOperator
  - `syntax_error` → quarantine (not repairable by AP)
  - `dependency_inconsistency` → repair operator: DependencyNormalizerOperator
  - `module_misplacement` → repair operator: ModuleRelocationOperator
  - `namespace_collision` → quarantine
  - `unclassified` → manual review queue
- Output: `error_classification_report.json` with per-module classification and assigned operator

**quarantine_manager.py functional contract:**
- Input: module path + reason for quarantine
- Process:
  1. Copy original module to `WORKFLOW_TARGET_AUDITS/logs/legacy/quarantine/[module_name]_original.py`
  2. Generate syntax-valid stub (header + docstring + `raise NotImplementedError` placeholder)
  3. Stub MUST pass syntax_validator before being written to canonical path
  4. Log quarantine event to `quarantine_manifest.json`
- Output: stub at original module path; quarantine_manifest entry

**Build sequence:**
1. Archive analogs for M71, M80 → `WORKFLOW_TARGET_AUDITS/logs/legacy/`
2. Create `error_classifier.py`
3. Create `repair_router.py` (consumes error_classifier output; maps to repair_registry)
4. Create `repair_executor.py` (invokes operators; enforces dry_run contract)
5. Create `quarantine_manager.py`
6. Wire existing repair operators (ImportRewriteOperator, HeaderInjectionOperator, DependencyNormalizerOperator, ModuleRelocationOperator) into repair_registry at canonical path
7. Integration test: inject known errors into synthetic fixture; run full repair pipeline; verify repairs applied or quarantined
8. Run architecture validator — confirm PHASE_7 exit condition

---

### PHASE_8 — Reporting + Commit

**Entry condition:** PHASE_7 complete.

**Exit condition:** All canonical artifact paths populated; pipeline_report.json produced; commit_finalizer confirms clean state.

**Modules:**

| Module ID | Module | Action |
|---|---|---|
| M90 | artifact_router.py | Create new |
| M91 | report_generator.py | Create new |
| M92 | commit_finalizer.py | Create new |

**artifact_router.py functional contract:**
- Single authority for all pipeline output writes
- Input: output artifact + artifact_type + stage
- Routes to canonical path per artifact type (see §9 Artifact Directory Rules)
- Rejects any write attempt to AP_SYSTEM_CONFIG/ or AP_SYSTEM_AUDIT/
- Produces `artifact_routing_manifest.json` entry per write

**report_generator.py functional contract:**
- Consumes all stage artifacts
- Produces `pipeline_report.json` (machine-readable) and `pipeline_summary.md` (human-readable)
- Includes per-stage status, total modules processed, errors, repairs, quarantines, timing

**commit_finalizer.py functional contract:**
- Verifies all canonical artifact paths are populated
- Verifies `artifact_routing_manifest.json` completeness
- Produces `commit_manifest.json` with final state
- Does NOT perform git operations directly — produces commit-ready state report for Architect/GPT

**Build sequence:**
1. Create `artifact_router.py`
2. Create `report_generator.py`
3. Create `commit_finalizer.py`
4. Integration test: run full pipeline through reporting stage; verify all output artifacts at canonical paths
5. Run architecture validator — confirm PHASE_8 exit condition

---

### PHASE_9 — Orchestration Controller

**Entry condition:** PHASE_8 complete; architecture validator clean on all prior phases.

**Exit condition:** Full pipeline run completes against LOGOS fixture (in LEVEL_0 analysis mode) without halt. All 12 pre-crawl checklist items evaluate correctly.

**Modules:**

| Module ID | Module | Action | Notes |
|---|---|---|---|
| M95 | task_router.py | Create new | Route tasks between subsystems |
| M96 | pipeline_controller.py | V2 rebuild | Single entry point; orchestrate S0→S9 |

**pipeline_controller.py functional contract (VF-001 fix):**
- Single entry point: `run(target_path: str, config_path: str, mutation_allowed: bool = False)`
- Orchestrates stages S0 → S9 in strict order
- Enforces all stage artifact gates (HALT on gate failure)
- Enforces all architecture validation gates
- Evaluates pre-crawl checklist (PCL-001 through PCL-012) before Stage 6
- Enforces mutation_allowed flag at Stage 6
- On HALT: writes `halt_diagnostic.json` with stage, reason, failing gate
- On completion: writes `pipeline_execution_manifest.json`

**Pre-crawl checklist evaluator:**
- Evaluates PCL-001 through PCL-012
- Produces `pre_crawl_checklist.json` with per-item GREEN/RED status and blocking flag
- Pipeline halts if any BLOCKING item is RED

**Build sequence:**
1. Archive existing `pipeline_controller.py` analog → `WORKFLOW_TARGET_AUDITS/logs/legacy/`
2. Create `task_router.py`
3. Rebuild `pipeline_controller.py` — wire all stage controllers; implement full gate logic
4. Implement pre-crawl checklist evaluator within pipeline_controller or as a separate module
5. Integration test against synthetic 50-module fixture: full S0→S9 run in LEVEL_0 mode
6. System test against LOGOS repo snapshot in LEVEL_0 mode
7. Verify no halts; verify `pipeline_execution_manifest.json` produced
8. Run architecture validator — confirm PHASE_9 exit condition

---

## 13. Governance Enforcement Points

| Enforcement Point | Rule | Action on Violation |
|---|---|---|
| Phase start | Architecture validator must pass before phase begins | halt |
| Module creation | Module ID must be in registry before VS Code prompt issued | halt |
| Module creation | V2 header must be first content in new module | halt |
| Module creation | canonical_path must begin with WORKFLOW_MUTATION_TOOLING/ | halt |
| Analog replacement | Original must be archived to WORKFLOW_TARGET_AUDITS/logs/legacy/ before overwrite | halt |
| Stage 6 entry | mutation_allowed flag must be explicitly present in config | halt |
| Stage 6 entry | simulation_report.crawl_permitted must be true | halt |
| Stage 6 entry | pre_crawl_checklist.json all BLOCKING items GREEN | halt |
| Write operation | No write to AP_SYSTEM_CONFIG/ or AP_SYSTEM_AUDIT/ | halt |
| Write operation | All writes routed through artifact_router.py | escalate_to_architect |
| Enhancement | No enhancement coded without spec and registry update | halt |
| Deletion | No module deleted without explicit Architect authorization | halt |

---

## 14. Ambiguity Log

| ID | Context | Question | Blocking Module | Recommendation | Escalation Required | Resolution |
|---|---|---|---|---|---|---|
| A1 | Schema naming | CL-G1: AP_MASTER_SPEC_V2_SCHEMA.json vs AP_DESIGN_SPEC_SCHEMA.json | All DS validation | Architect to declare canonical name | Yes | |
| A2 | Config naming | OQ-004: mutation_allowed default — confirm analysis-only for initial LOGOS run | M96 pipeline_controller | Architect to confirm false is default | Yes | |
| A3 | Controller structure | OQ-002: controllers/ as separate dir vs. collapsed into orchestration/ | M95, M96 | Recommend keeping separate | No | |
| A4 | Audit registry scope | OQ-003: WORKFLOW_TARGET_AUDITS/ shares or separates registry from WORKFLOW_MUTATION_TOOLING/ | M-RSA-01 through M-RSA-04 | Recommend separate registries | No | |
| A5 | AP_TOOL_PROP_01 module ID | OQ-005: Confirm AP_REPO_SCANNER maps to M-RSA-01 canonical identity | M-RSA-01 | Recommend confirming | No | |

---

## 15. Revision History

| Version | Date | Change | Author |
|---|---|---|---|
| v1 | 2026-03-10 | Initial implementation guide — paired with SPEC-010 | Claude / Formalization_Expert |

---

*End of IMPL-010*
