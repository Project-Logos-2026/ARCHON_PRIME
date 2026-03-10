# SPEC_AP_V2_TOOLING_ARCHITECTURE
## ARCHON PRIME — V2 Tooling Architecture Design Specification

---

## Specification Identity

| Field | Value |
|---|---|
| Artifact ID | SPEC-010 |
| System | ARCHON_PRIME |
| Platform | Python 3.11+ / Codespaces |
| Artifact Type | Design Specification |
| Version | v1 |
| Status | Draft |
| Schema | AP_DESIGN_SPEC_SCHEMA.json |
| Authority Source | Architect |
| Source Concepts | RPT-002, GPT_TOOLING_AUDIT_V2, AP_TOOL_PROP_01, MASTER_SYSTEM_DESIGN_SPEC v1.0.0, AP_SYSTEM_AUDIT V1 failure corpus |
| Author | Claude / Formalization_Expert |
| Date | 2026-03-10 |
| Approved By | |
| Phase | Phase 2 — Specification Production (active) |
| DRAC Status | Deferred — not targeted by this spec |

---

## Lineage

| Field | Value |
|---|---|
| Concept Origin | Multi-source synthesis: RPT-002, GPT_TOOLING_AUDIT_V2, AP_TOOL_PROP_01, V1 failure corpus |
| Analog Origin | null |
| Prior Version | null |
| Supersedes | IMPLEMENTATION_SEQUENCE.md (V1 build guide) |

---

## 1. Purpose

This specification defines the complete V2 tooling architecture for ARCHON_PRIME. It establishes the canonical directory structure, module inventory, subsystem contracts, artifact routing rules, pipeline execution model, and validation gate requirements for the V2 tooling build.

ARCHON_PRIME's V2 tooling objective is a deterministic, single-pass crawl-mutation-validation engine capable of operating on both the ARCHON_PRIME repository (self-repair and architecture validation) and arbitrary external target repositories (specifically LOGOS). The V1 tooling pass produced a 455-file repository at approximately 10.3% spec-module completion with 35 of 39 required canonical modules missing and a structural dispersion problem: runtime code scattered across root-level directories rather than consolidated into canonical workflow domains.

This spec integrates all design inputs — V1 audit failure corpus, GPT V2 tooling architecture proposal, previous Claude formalization session (RPT-002), and the AP_TOOL_PROP_01 repo analysis subsystem concept — and is sufficient to drive deterministic implementation of the entire tooling layer.

---

## 2. V1 Failure Analysis — Design Spec Inclusions

The following failures are extracted from the AP_SYSTEM_AUDIT V1 corpus. Each failure is converted directly to a V2 design requirement.

### 2.1 Structural Dispersion (Critical)

**V1 failure:** Runtime modules scattered across 9+ root-level directories (`controllers/`, `crawler/`, `repair/`, `schemas/`, `simulation/`, `orchestration/`, `tools/`, `registry/`, `AUDIT_SYSTEM/`), all outside any canonical workflow domain. The GPT V2 audit identified that `AP_MUTATION_TOOLING` consolidation was partial — many modules were not migrated.

**V2 requirement FR-001:** All runtime modules must reside in exactly one of three canonical workflow domains:
- `WORKFLOW_MUTATION_TOOLING/` — AP runtime engine and mutation tooling
- `WORKFLOW_TARGET_AUDITS/` — audit modules operating on external target repos
- `WORKFLOW_TARGET_PROCESSING/` — target repo staging, design specs, IGs, processing workspace

No module may be generated or migrated outside these domains. Domain assignment is determined at design-spec time. Root-level directories (`controllers/`, `crawler/`, `repair/`, `simulation/`, `AUDIT_SYSTEM/`, `AUDIT_LOGS/`) are legacy structures consolidated before or during V2 implementation. Non-deletion policy applies throughout.

### 2.2 Missing Canonical Modules (Critical)

**V1 failure:** 35 of 39 spec-required modules absent. Subsystem completion at time of V1 audit:

| Subsystem | Required | Present | Functional | Completion |
|---|---|---|---|---|
| S0_FOUNDATION | 3 | 0 | 0 | 0% |
| S1_AUDIT_REGENERATION | 8 | 0 | 0 | 0% |
| S2_REPO_ANALYSIS | 6 | 0 | 0 | 0% |
| S3_SIMULATION | 3 | 3 | 2 | 66.7% (1 skeleton) |
| S4_CRAWL_PLANNING | 2 | 0 | 0 | 0% |
| S5_MUTATION_OPERATORS | 2 | 0 | 0 | 0% |
| S6_CRAWL_EXECUTION | 6 | 1 | 0 | partial skeleton |
| S7_ERROR_REPAIR | 3 | 0 | 0 | 0% |
| S8_QUARANTINE | 1 | 0 | 0 | 0% |
| S9_ARTIFACT_REPORTING | 3 | 0 | 0 | 0% |
| S10_ORCHESTRATION | 2 | 0 | 0 | 0% |

**V2 requirement FR-002:** All 39 canonical modules must be built in dependency order per the implementation sequence in Section 14. SPEC-004 (`validate_architecture.py`) must be approved and implemented before any gated pipeline stage proceeds.

### 2.3 Analog Module Proliferation (Major)

**V1 failure:** 109 non-spec Python modules exist. Of 50 reviewed, approximately 18 are functional analog implementations of spec modules (same purpose, wrong name or path), and approximately 31 are enhancement or unknown modules.

**V2 requirement FR-003:** Every analog module must be classified before replacement or migration. Classification categories: MIGRATE (functional, correct path), MIGRATE_AND_RENAME (functional, wrong name/path), REFACTOR (functional, wrong structure), REBUILD (skeleton or partial), PRESERVE_AS_ENHANCEMENT (non-spec utility, keep), DEPRECATE (duplicate or obsolete). No analog module may be silently overwritten.

**Key analog modules for V2 migration:**

| Analog Module | Current Path | Classification | V2 Target Path |
|---|---|---|---|
| `pipeline_controller.py` | `controllers/` | MIGRATE+RENAME → `controller_main.py` | `WORKFLOW_MUTATION_TOOLING/orchestration/controllers/` |
| `audit_controller.py` | `controllers/` | MIGRATE | `WORKFLOW_MUTATION_TOOLING/orchestration/controllers/` |
| `analysis_controller.py` | `controllers/` | MIGRATE | `WORKFLOW_MUTATION_TOOLING/orchestration/controllers/` |
| `repair_controller.py` | `controllers/` | MIGRATE | `WORKFLOW_MUTATION_TOOLING/crawler/repair/` |
| `config_loader.py` | `controllers/` | MIGRATE | `WORKFLOW_MUTATION_TOOLING/tools/audit_tools/` |
| `crawl_engine.py` | `crawler/core/` | REBUILD (skeletal) | `WORKFLOW_MUTATION_TOOLING/crawler/engine/crawl_executor.py` |
| `repo_scanner.py` | `tools/repo_mapping/` | MIGRATE+RENAME → `repo_directory_scanner.py` | `WORKFLOW_MUTATION_TOOLING/tools/repo_mapping/` |
| `header_validator.py` | `tools/normalization_tools/` | MIGRATE+RENAME → `header_schema_scanner.py` | `WORKFLOW_MUTATION_TOOLING/tools/normalization_tools/` |
| `governance_scanner.py` | `tools/governance_analysis/` | MIGRATE+RENAME → `governance_contract_scanner.py` | `WORKFLOW_MUTATION_TOOLING/tools/governance_analysis/` |
| `dependency_graph.py` | `tools/runtime_analysis/` | MIGRATE+RENAME → `dependency_graph_builder.py` | `WORKFLOW_MUTATION_TOOLING/tools/import_analysis/` |
| `runtime_simulator.py` | `simulation/runtime_simulator/` | PRESENT functional — keep in place | `WORKFLOW_MUTATION_TOOLING/simulation/runtime_simulator/` |
| `import_simulator.py` | `simulation/import_simulator/` | PRESENT functional — keep in place | `WORKFLOW_MUTATION_TOOLING/simulation/import_simulator/` |
| `repo_simulator.py` | `simulation/repo_simulator/` | REBUILD (166B, no JSON output) | `WORKFLOW_MUTATION_TOOLING/simulation/repo_simulator/` |
| `routing_table_loader.py` | `orchestration/task_router/` | EXPAND (reference-only implementation) | Stay in place |
| `schema_registry.py` | `tools/normalization_tools/` | PRESENT functional — keep in place | Stay in place |
| `header_injection_operator.py` | `repair/operators/` | MIGRATE → `header_injector.py` | `WORKFLOW_MUTATION_TOOLING/crawler/mutation/` |
| `import_rewrite_operator.py` | `repair/operators/` | MIGRATE → `import_rewriter.py` | `WORKFLOW_MUTATION_TOOLING/crawler/mutation/` |
| `dependency_normalizer.py` | `repair/operators/` | MIGRATE | `WORKFLOW_MUTATION_TOOLING/crawler/repair/` |
| `module_relocation_operator.py` | `repair/operators/` | MIGRATE | `WORKFLOW_MUTATION_TOOLING/crawler/repair/` |
| `namespace_disambiguator.py` | `repair/operators/` | MIGRATE | `WORKFLOW_MUTATION_TOOLING/crawler/repair/` |
| `repo_mapper.py` | `AUDIT_SYSTEM/scripts/repo_scanners/` | MIGRATE to target audits domain | `WORKFLOW_TARGET_AUDITS/modules/repo_mapping/` |
| 18x `audit_tools/*.py` | `tools/audit_tools/` | PRESENT functional — wire to pipeline, add target_path | Stay in place |

### 2.4 Missing Configuration Files (Major)

**V1 failure:** 6 required configuration files absent. Pipeline stalls at initialization because config loaders have no files to consume.

**V2 requirement FR-004:** All 6 config files must exist at canonical paths before pipeline initialization. They are source files, not generated artifacts. They must be created as part of PHASE_0.

| Config File | V2 Canonical Path | Purpose |
|---|---|---|
| `crawl_config.json` | `WORKFLOW_MUTATION_TOOLING/configs/crawl_configs/` | Runtime crawl parameters, mutation policy, worker config |
| `logos_targets.yaml` | `WORKFLOW_TARGET_PROCESSING/targets/` | Target repo definitions (path, branch, language) |
| `ap_config.yaml` | `WORKFLOW_MUTATION_TOOLING/configs/` | Architect-editable override layer |
| `repair_registry.json` | `WORKFLOW_MUTATION_TOOLING/registry/` | Operator-to-failure-type mapping |
| `routing_table.json` | `WORKFLOW_MUTATION_TOOLING/orchestration/task_router/` | Artifact output routing (rebuild — current version routes to legacy paths) |
| `header_schema.json` | `WORKFLOW_MUTATION_TOOLING/tools/normalization_tools/` | Canonical header field definitions |

### 2.5 Pipeline Wiring Absent (Critical)

**V1 failure:** 18 audit tool modules are functionally implemented but isolated. Each runs independently with no common invocation interface, no standardized JSON output contract, and no artifact routing.

**V2 requirement FR-005:** All audit tools must be invocable through the audit controller via a standardized `run(target: str) -> dict` interface returning `{"status": "ok|error", "artifact_output": "<path>", "findings": [...]}`. All outputs must be routed per `routing_table.json`. The audit controller must aggregate results and write a consolidated audit report.

### 2.6 Routing Table Legacy References (Major)

**V1 failure:** `routing_table.json` routes artifacts to `AUDIT_SYSTEM/` paths — a legacy directory dissolved in V2. Artifact routing does not match V2 canonical structure.

**V2 requirement FR-006:** `routing_table.json` must be rebuilt to route all target-repo audit outputs to `WORKFLOW_TARGET_AUDITS/` paths, and all self-audit outputs to `WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/`. No legacy path references permitted.

### 2.7 No Architecture Validation Gate (Critical)

**V1 failure:** No architecture validator exists. All pipeline stages ran without confirming valid architectural state. Structural drift accumulated through all V1 stages without detection.

**V2 requirement FR-007:** SPEC-004 (`validate_architecture.py`) must be implemented and passing before any gated pipeline stage proceeds. It is the first module built after PHASE_0. Validation gate VG-001 blocks all subsequent stages.

### 2.8 Repo Analysis Subsystem Gap (AP_TOOL_PROP_01)

**New requirement:** Analyzing LOGOS — which is significantly larger and more complex than the AP repo — requires structural intelligence beyond a flat file index. The V1 artifact collection module (`ap_artifact_collection_p1.py`) produces raw indexes but no analysis layer.

**V2 requirement FR-008:** The artifact collection module becomes Stage 0 of a four-stage repo analysis pipeline resident in `WORKFLOW_TARGET_AUDITS/modules/`. This pipeline provides the primary analysis capability for external target repositories.

---

## 3. Canonical Directory Architecture

### 3.1 Domain Assignment Rule

Every module, config, schema, and artifact in the AP system belongs to exactly one of five root directories. Two are immutable; three are mutable:

```
ARCHON_PRIME/
├── AP_SYSTEM_CONFIG/             [IMMUTABLE — platform configs, design specs, governance]
├── AP_SYSTEM_AUDIT/              [IMMUTABLE — V1 audit artifacts, historical reports]
├── WORKFLOW_MUTATION_TOOLING/    [MUTABLE — AP runtime engine]
├── WORKFLOW_TARGET_AUDITS/       [MUTABLE — audit modules for external repos]
└── WORKFLOW_TARGET_PROCESSING/   [MUTABLE — target repo staging and processing]
```

### 3.2 WORKFLOW_MUTATION_TOOLING — Full V2 Tree

```
WORKFLOW_MUTATION_TOOLING/
│
├── orchestration/
│   ├── controllers/
│   │   ├── controller_main.py             [M96 — pipeline orchestrator]
│   │   ├── audit_controller.py            [analog migrate]
│   │   ├── analysis_controller.py         [analog migrate]
│   │   └── simulation_controller.py       [analog migrate]
│   ├── task_router/
│   │   ├── task_router.py                 [M95]
│   │   └── routing_table.json             [config — rebuild V2 paths]
│   └── execution_graphs/
│       └── execution_graph_builder.py     [M39]
│
├── tools/
│   ├── repo_mapping/
│   │   ├── repo_directory_scanner.py      [M10 — migrate+rename from repo_scanner.py]
│   │   ├── python_file_collector.py       [M11 — build]
│   │   └── module_index_builder.py        [M20 — build]
│   ├── import_analysis/
│   │   ├── import_extractor.py            [M12 — migrate+rename from import_scanner.py]
│   │   ├── symbol_import_extractor.py     [M13 — build]
│   │   ├── dependency_graph_builder.py    [M21 — migrate+rename from dependency_graph.py]
│   │   ├── circular_dependency_detector.py [M22 — build]
│   │   └── canonical_import_registry_builder.py [M25 — build]
│   ├── governance_analysis/
│   │   └── governance_contract_scanner.py [M15 — migrate+rename from governance_scanner.py]
│   ├── runtime_analysis/
│   │   ├── runtime_phase_mapper.py        [M23 — build]
│   │   └── runtime_boot_sequencer.py      [M24 — build]
│   ├── normalization_tools/
│   │   ├── schema_registry.py             [M00 — PRESENT functional]
│   │   ├── header_schema_scanner.py       [M14 — migrate+rename from header_validator.py]
│   │   └── header_schema.json             [config — build]
│   ├── audit_tools/
│   │   ├── repair_registry_loader.py      [M02 — build]
│   │   ├── audit_utils.py                 [PRESENT — keep]
│   │   ├── circular_dependency_audit.py   [PRESENT — wire to controller]
│   │   ├── cross_package_dependency_audit.py [PRESENT — wire]
│   │   ├── duplicate_module_audit.py      [PRESENT — wire]
│   │   ├── facade_bypass_audit.py         [PRESENT — wire]
│   │   ├── header_schema_audit.py         [PRESENT — wire]
│   │   ├── import_surface_audit.py        [PRESENT — wire]
│   │   ├── module_path_ambiguity_audit.py [PRESENT — wire]
│   │   ├── namespace_shadow_audit.py      [PRESENT — wire]
│   │   ├── orphan_module_audit.py         [PRESENT — wire]
│   │   ├── run_audit_suite.py             [PRESENT — modify: add target_path param]
│   │   ├── run_governance_audit.py        [PRESENT — modify: add target_path param]
│   │   └── unused_import_audit.py         [PRESENT — wire]
│   └── validation/
│       └── validate_architecture.py       [M-VAL-01 — SPEC-004]
│
├── crawler/
│   ├── engine/
│   │   ├── crawl_planner.py               [M38 — build]
│   │   ├── crawl_executor.py              [M60 — rebuild from crawl_engine.py skeleton]
│   │   └── checklist_evaluator.py         [pre-crawl gate — build]
│   ├── pipeline/
│   │   ├── module_processor.py            [M61 — build]
│   │   ├── syntax_validator.py            [M62 — build]
│   │   ├── governance_validator.py        [M63 — build]
│   │   └── phase_validator.py             [M64 — build]
│   ├── mutation/
│   │   ├── header_injector.py             [M50 — migrate from repair/operators/]
│   │   └── import_rewriter.py             [M51 — migrate from repair/operators/]
│   ├── repair/
│   │   ├── error_classifier.py            [M70 — build]
│   │   ├── repair_router.py               [M71 — build]
│   │   ├── repair_executor.py             [M72 — build]
│   │   ├── dependency_normalizer.py       [analog migrate]
│   │   ├── module_relocation_operator.py  [analog migrate]
│   │   └── namespace_disambiguator.py     [analog migrate]
│   ├── monitor/
│   │   └── crawl_monitor.py               [M65 — rebuild from skeleton]
│   ├── quarantine/
│   │   └── quarantine_manager.py          [M80 — build]
│   └── commit/
│       ├── artifact_router.py             [M90 — build]
│       ├── report_generator.py            [M91 — build]
│       └── commit_finalizer.py            [M92 — build]
│
├── simulation/
│   ├── repo_simulator/
│   │   └── repo_simulator.py              [M30 — rebuild skeleton, add JSON output]
│   ├── runtime_simulator/
│   │   └── runtime_simulator.py           [M31 — PRESENT functional]
│   ├── import_simulator/
│   │   └── import_simulator.py            [M32 — PRESENT functional]
│   └── simulation_coordinator.py          [orchestrates all three — build]
│
├── registry/
│   ├── module_registry.json               [PRESENT — expand to full 39-module inventory]
│   ├── audit_registry.json                [PRESENT — keep]
│   └── repair_registry.json               [PRESENT — update paths, confirm canonical]
│
├── configs/
│   ├── crawl_configs/
│   │   ├── crawl_config.json              [config — build]
│   │   └── logos_targets.yaml             [config — already present in WORKFLOW_TARGET_PROCESSING/targets/]
│   ├── phase_maps/
│   │   └── phase_map_config.json          [config — build]
│   └── ap_config.yaml                     [config — build]
│
├── schemas/
│   ├── CrawlMutationRecord.schema.json    [PRESENT]
│   ├── ValidationManifest.schema.json     [PRESENT]
│   ├── PhaseGate.schema.json              [PRESENT]
│   └── QuarantineRecord.schema.json       [PRESENT]
│
└── utils/
    └── logger.py                          [PRESENT — functional JSON event logger]
```

### 3.3 WORKFLOW_TARGET_AUDITS — Full V2 Tree

Replaces legacy `AUDIT_SYSTEM/` and `AUDIT_LOGS/`. Houses the AP_TOOL_PROP_01 repo analysis pipeline.

```
WORKFLOW_TARGET_AUDITS/
│
├── modules/
│   ├── repo_mapping/
│   │   └── repo_mapper.py                 [migrate from AUDIT_SYSTEM/scripts/repo_scanners/]
│   ├── collection/
│   │   └── artifact_collector.py          [AP_TOOL_PROP_01 Stage 0 — repo traversal + indexing]
│   ├── structure_analysis/
│   │   └── structure_analyzer.py          [AP_TOOL_PROP_01 Stage 1 — structural intelligence]
│   ├── subsystem_analysis/
│   │   └── subsystem_analyzer.py          [AP_TOOL_PROP_01 Stage 2 — subsystem completeness]
│   └── gap_analysis/
│       └── gap_analysis_engine.py         [AP_TOOL_PROP_01 Stage 3 — remediation guidance]
│
├── configs/
│   └── audit_module_config.json           [file type filters, exclusion rules]
│
├── logs/
│   [runtime logs from audit module execution — replaces empty AUDIT_LOGS/]
│
└── reports/
    [per-repo audit reports, timestamped]
```

### 3.4 WORKFLOW_TARGET_PROCESSING — V2 Structure (Existing + Clarified)

```
WORKFLOW_TARGET_PROCESSING/
├── incoming/             [drop zone for external repos and archives]
├── targets/
│   ├── repos/            [top-level clones of target repos]
│   └── subsystems/       [subsystem-focused work directories]
├── design_specs/         [authoritative DS for target repo subsystems]
├── implementation_guides/ [IGs for target repo mutation work]
├── processing/           [active workspace where mutation tooling operates]
└── validated/            [output of validated processing passes]
```

**Constraint:** `incoming/Designs_and_Guides/` contains V1-format LOGOS DS/IGs. Do not process these during V2 AP tooling build — they require V2 schema upgrade, which is a separate workstream.

---

## 4. Repo Analysis Subsystem (AP_TOOL_PROP_01 Integration)

The repo analysis subsystem extends V1 artifact collection into a four-stage pipeline resident in `WORKFLOW_TARGET_AUDITS/modules/`. It is the primary analysis engine for external target repositories, and is required before AP can operate on LOGOS.

### 4.1 Pipeline Architecture

```
Stage 0: ARTIFACT_COLLECTOR
  Inputs:  target repo root path
  Outputs: AP_ARTIFACT_INDEX.json, AP_DIRECTORY_TREE.json, AP_EMPTY_DIRECTORIES.json
  Function: full traversal, exclusion filtering, file classification, indexing
  Source:   extends ap_artifact_collection_p1.py logic

Stage 1: STRUCTURE_ANALYZER
  Inputs:  Stage 0 outputs
  Outputs: AP_STRUCTURE_ANALYSIS.json
  Analysis: module clustering, subsystem boundaries, hierarchy, orphan dirs,
            abnormal placement, config/runtime separation, structural anomalies

Stage 2: SUBSYSTEM_ANALYZER
  Inputs:  Stage 1 outputs + AP_ARTIFACT_INDEX.json
  Outputs: AP_SUBSYSTEM_ANALYSIS.json
  Detection: empty subsystem dirs, missing module groups, incomplete implementations,
             stub modules, partial runtime surfaces, incomplete config layers

Stage 3: GAP_ANALYSIS_ENGINE
  Inputs:  Stage 2 outputs, Design Specifications (optional)
  Outputs: AP_REPOSITORY_GAP_ANALYSIS.json
  Gaps:    missing modules, missing subsystems, architectural drift,
           unused dirs, orphan files, incomplete implementations
```

### 4.2 Output Schema Contracts

**AP_ARTIFACT_INDEX.json:**
```json
{
  "schema_version": "2.0",
  "generated_at": "<ISO>",
  "repo_root": "<path>",
  "total_files": 0,
  "files": [{ "path": "<rel>", "type": "<classification>", "size_bytes": 0 }]
}
```

**AP_STRUCTURE_ANALYSIS.json:**
```json
{
  "schema_version": "2.0",
  "generated_at": "<ISO>",
  "module_clusters": [],
  "subsystem_boundaries": [],
  "orphan_directories": [],
  "structural_anomalies": []
}
```

**AP_SUBSYSTEM_ANALYSIS.json:**
```json
{
  "schema_version": "2.0",
  "subsystems": [{ "name": "<str>", "status": "complete|partial|empty", "missing": [] }]
}
```

**AP_REPOSITORY_GAP_ANALYSIS.json:**
```json
{
  "schema_version": "2.0",
  "gap_summary": { "critical": 0, "major": 0, "minor": 0 },
  "gaps": [{ "id": "<str>", "severity": "Critical|Major|Minor", "description": "<str>", "remediation": "<str>" }]
}
```

---

## 5. Canonical Module Registry (V2 Complete Inventory)

All 39 canonical modules plus the architecture validator and repo analysis subsystem modules.

### Stage 0 — Foundation

| Module ID | Module Name | Path | Status | Action |
|---|---|---|---|---|
| M00 | schema_registry.py | tools/normalization_tools/ | PRESENT | Keep |
| M01 | routing_table_loader.py | orchestration/task_router/ | PRESENT (ref impl) | Expand |
| M02 | repair_registry_loader.py | tools/audit_tools/ | MISSING | Build |

### Stage 1 — Audit Regeneration

| Module ID | Module Name | Path | Status | Action |
|---|---|---|---|---|
| M10 | repo_directory_scanner.py | tools/repo_mapping/ | ANALOG | Migrate+Rename |
| M11 | python_file_collector.py | tools/repo_mapping/ | MISSING | Build |
| M12 | import_extractor.py | tools/import_analysis/ | ANALOG | Migrate+Rename |
| M13 | symbol_import_extractor.py | tools/import_analysis/ | MISSING | Build |
| M14 | header_schema_scanner.py | tools/normalization_tools/ | ANALOG | Migrate+Rename |
| M15 | governance_contract_scanner.py | tools/governance_analysis/ | ANALOG | Migrate+Rename |
| M16 | runtime_phase_scanner.py | tools/runtime_analysis/ | MISSING | Build |
| M17 | concept_spec_gap_detector.py | tools/audit_tools/ | MISSING | Build |

### Stage 2 — Repo Analysis

| Module ID | Module Name | Path | Status | Action |
|---|---|---|---|---|
| M20 | module_index_builder.py | tools/repo_mapping/ | MISSING | Build |
| M21 | dependency_graph_builder.py | tools/import_analysis/ | ANALOG | Migrate+Rename |
| M22 | circular_dependency_detector.py | tools/import_analysis/ | MISSING | Build |
| M23 | runtime_phase_mapper.py | tools/runtime_analysis/ | MISSING | Build |
| M24 | runtime_boot_sequencer.py | tools/runtime_analysis/ | MISSING | Build |
| M25 | canonical_import_registry_builder.py | tools/import_analysis/ | MISSING | Build |

### Stage 3 — Simulation

| Module ID | Module Name | Path | Status | Action |
|---|---|---|---|---|
| M30 | repo_simulator.py | simulation/repo_simulator/ | SKELETON (166B) | Rebuild |
| M31 | runtime_simulator.py | simulation/runtime_simulator/ | FUNCTIONAL | Keep |
| M32 | import_simulator.py | simulation/import_simulator/ | FUNCTIONAL | Keep |
| — | simulation_coordinator.py | simulation/ | MISSING | Build |

### Stage 4 — Crawl Planning

| Module ID | Module Name | Path | Status | Action |
|---|---|---|---|---|
| M38 | crawl_planner.py | crawler/engine/ | MISSING | Build |
| M39 | execution_graph_builder.py | orchestration/execution_graphs/ | MISSING | Build |

### Stage 5 — Mutation Operators

| Module ID | Module Name | Path | Status | Action |
|---|---|---|---|---|
| M50 | header_injector.py | crawler/mutation/ | ANALOG at repair/operators/ | Migrate |
| M51 | import_rewriter.py | crawler/mutation/ | ANALOG at repair/operators/ | Migrate |

### Stage 6 — Crawl Execution

| Module ID | Module Name | Path | Status | Action |
|---|---|---|---|---|
| M60 | crawl_executor.py | crawler/engine/ | ANALOG skeletal | Rebuild |
| M61 | module_processor.py | crawler/pipeline/ | MISSING | Build |
| M62 | syntax_validator.py | crawler/pipeline/ | MISSING | Build |
| M63 | governance_validator.py | crawler/pipeline/ | MISSING | Build |
| M64 | phase_validator.py | crawler/pipeline/ | MISSING | Build |
| M65 | crawl_monitor.py | crawler/monitor/ | SKELETON (142B) | Rebuild |

### Stage 7 — Error Repair

| Module ID | Module Name | Path | Status | Action |
|---|---|---|---|---|
| M70 | error_classifier.py | crawler/repair/ | MISSING | Build |
| M71 | repair_router.py | crawler/repair/ | MISSING | Build |
| M72 | repair_executor.py | crawler/repair/ | MISSING | Build |

### Stage 8 — Quarantine

| Module ID | Module Name | Path | Status | Action |
|---|---|---|---|---|
| M80 | quarantine_manager.py | crawler/quarantine/ | MISSING | Build |

### Stage 9 — Artifact Reporting

| Module ID | Module Name | Path | Status | Action |
|---|---|---|---|---|
| M90 | artifact_router.py | crawler/commit/ | MISSING | Build |
| M91 | report_generator.py | crawler/commit/ | MISSING | Build |
| M92 | commit_finalizer.py | crawler/commit/ | MISSING | Build |

### Stage 10 — Orchestration

| Module ID | Module Name | Path | Status | Action |
|---|---|---|---|---|
| M95 | task_router.py | orchestration/task_router/ | MISSING | Build |
| M96 | controller_main.py | orchestration/controllers/ | ANALOG | Migrate+Rename |
| — | checklist_evaluator.py | crawler/engine/ | MISSING | Build |

### Architecture Validator

| Module ID | Module Name | Path | Status | Action |
|---|---|---|---|---|
| M-VAL-01 | validate_architecture.py | tools/validation/ | SPEC-ONLY (SPEC-004 Draft) | Build after SPEC-004 approved |

### WORKFLOW_TARGET_AUDITS (AP_TOOL_PROP_01)

| Module ID | Module Name | Path | Status | Action |
|---|---|---|---|---|
| TA-01 | artifact_collector.py | WORKFLOW_TARGET_AUDITS/modules/collection/ | MISSING | Build (extends ap_artifact_collection_p1.py) |
| TA-02 | structure_analyzer.py | WORKFLOW_TARGET_AUDITS/modules/structure_analysis/ | MISSING | Build |
| TA-03 | subsystem_analyzer.py | WORKFLOW_TARGET_AUDITS/modules/subsystem_analysis/ | MISSING | Build |
| TA-04 | gap_analysis_engine.py | WORKFLOW_TARGET_AUDITS/modules/gap_analysis/ | MISSING | Build |

---

## 6. Pipeline Execution Model

### 6.1 Full Pipeline Sequence

```
[INITIALIZATION]
  Load: crawl_config.json, routing_table.json, repair_registry.json
  Run: checklist_evaluator.py → PRE_CRAWL_CHECKLIST.json must be GREEN
       │
       ▼ GATE VG-001: architecture_valid == true (SPEC-004)
       ▼ GATE VG-002: checklist PASS

[STAGE 1: AUDIT REGENERATION]
  Run all M10–M17 against target repo
  Outputs: repo_directory_tree.json, repo_python_files.json, repo_imports.json,
           header_schema_compliance.json, governance_contract_map.json
       │
       ▼ GATE: all S1 artifacts present, schema-valid

[STAGE 2: REPO ANALYSIS]
  Run M20–M25: module_index, dependency_graph, circular deps, phase map, boot sequence
  Outputs: module_index.json, dependency_graph.json, runtime_phase_map.json
       │
       ▼ GATE: all S2 artifacts present, dependency_graph non-empty

[STAGE 3: SIMULATION]
  Run simulation_coordinator → repo_simulator → runtime_simulator → import_simulator
  Output: simulation_report.json
       │
       ▼ GATE VG-004: simulation_report.status == "PASS"

[STAGE 4: CRAWL PLANNING]
  Run crawl_planner → execution_graph_builder
  Output: crawl_plan.json (dependency-ordered module list)
       │
       ▼ GATE: crawl_plan.json valid, order_length > 0

[STAGES 5+6: CRAWL EXECUTION — one module at a time]
  For each module in crawl_plan:
    module_processor:
      syntax_validator →
      header_injector [MUTATION — simulate or execute] →
      import_rewriter  [MUTATION — simulate or execute] →
      governance_validator →
      phase_validator →
      syntax_validator (post-mutation re-run) →
    if PASS: route artifacts → advance
    if FAIL: → [STAGE 7: REPAIR]
       │
[STAGE 7: REPAIR LOOP]
  error_classifier → repair_router → repair_executor
  On success: back to validation
  On fail (threshold exceeded): → [STAGE 8: QUARANTINE]
       │
[STAGE 8: QUARANTINE]
  quarantine_manager → stub module, update quarantine_registry.json, advance
       │
[STAGE 9: REPORTING + COMMIT]
  artifact_router → report_generator → commit_finalizer
  Outputs: validation_report.json, repair_event_log.json, mutation_log.json,
           crawl_execution_log.json, crawl_status.json
```

### 6.2 Simulation Mode Contract

All mutation-capable modules (header_injector, import_rewriter, repair_executor, module_relocation_operator) must support a `--simulate` flag. Simulation mode: all reads and computation execute; no files written to target repo; artifacts produced with `"simulation": true`. The `--simulate` flag is the default. `--execute` requires explicit invocation and must be authorized by VG-004 passing.

### 6.3 CLI Contract (All Pipeline Modules)

```
python <module>.py --target <repo_root> [--simulate|--execute] [--spec <SPEC-ID>] [--output <path>]
```

| Flag | Required | Default | Behavior |
|---|---|---|---|
| `--target` | Yes | — | Path to target repo root |
| `--simulate` | No | Yes (default) | Dry run, no mutations |
| `--execute` | No | No | Live mutations, requires VG-004 pass |
| `--spec` | Validator only | — | Design spec to validate against |
| `--output` | No | routing_table.json value | Override output artifact path |

---

## 7. Module Identity Rules

Every canonical module must satisfy all three conditions simultaneously:

| Condition ID | Condition | Enforcement Point |
|---|---|---|
| IC-001 | Module exists at canonical path declared in registry | path_validation |
| IC-002 | Module carries a valid V2 header block with all 13 fields populated | header_validation |
| IC-003 | Module registered in module_registry.json with matching module_id and canonical_path | registry_check |

**Violation classification:**

| Category | Description | Severity |
|---|---|---|
| MISPLACED | Module present at non-canonical path | blocking |
| HEADER_INVALID | Module present, header missing or incomplete | blocking |
| UNREGISTERED | Module present at correct path but absent from registry | blocking |
| DEFERRED | Module absent but subsystem marked deferred | non-blocking |

---

## 8. Artifact Surface Definition

| Surface ID | Name | Canonical Directories | Permitted Content |
|---|---|---|---|
| S-001 | runtime_surface | WORKFLOW_MUTATION_TOOLING/tools/, crawler/, simulation/, orchestration/ | Python modules only |
| S-002 | audit_surface | WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/, WORKFLOW_TARGET_AUDITS/logs/, reports/ | JSON artifacts, logs |
| S-003 | config_surface | WORKFLOW_MUTATION_TOOLING/configs/, registry/ | JSON configs, YAML |
| S-004 | design_surface | AP_SYSTEM_CONFIG/, WORKFLOW_TARGET_PROCESSING/design_specs/, implementation_guides/ | Markdown, JSON schemas |
| S-005 | target_audit_surface | WORKFLOW_TARGET_AUDITS/modules/ | Python modules only |
| S-006 | test_surface | tests/ | Python test modules |

**Surface isolation invariant:** No runtime module may exist in design_surface or audit_surface. No design artifact may exist in runtime_surface. Violations are detected by AVR-008 in SPEC-004.

---

## 9. Subsystem Contracts

| Subsystem | Role | May Import From | Forbidden Imports |
|---|---|---|---|
| S0_FOUNDATION | Config loading, schema registry | stdlib only | All other AP subsystems |
| S1_AUDIT_REGEN | Target repo scanning | S0, stdlib | LOGOS runtime, S6+, S7+ |
| S2_REPO_ANALYSIS | Graph building, phase detection | S0, S1, stdlib | LOGOS runtime, S6+, S7+ |
| S3_SIMULATION | Pre-crawl simulation | S0, S1, S2, stdlib | LOGOS runtime, S6, S7, S8 |
| S4_CRAWL_PLANNING | Execution ordering | S0, S2, S3, stdlib | LOGOS runtime, S6+, S7+ |
| S5_MUTATION_OPERATORS | Header/import mutation | S0, stdlib | S7, S8, S9, LOGOS runtime |
| S6_CRAWL_EXECUTION | Per-module processing | S0, S4, S5, stdlib | S9 direct calls |
| S7_ERROR_REPAIR | Error classify + repair | S0, S5, stdlib | S9 direct calls |
| S8_QUARANTINE | Stub isolation | S0, stdlib | S6+, S9, LOGOS runtime |
| S9_ARTIFACT_REPORTING | Output routing, commit | S0, stdlib | LOGOS runtime |
| S10_ORCHESTRATION | Pipeline sequencing | All subsystems | LOGOS runtime |
| TARGET_AUDITS | External repo analysis | stdlib, S0 | All LOGOS modules, S5+ mutation |

---

## 10. Header Schema Definition

Every canonical Python module in `WORKFLOW_MUTATION_TOOLING/` must carry this header as the first content block, before all imports:

```python
# ARCHON PRIME MODULE HEADER
# module_id: <M-ID>
# module_name: <filename without .py>
# subsystem: <subsystem ID>
# canonical_path: WORKFLOW_MUTATION_TOOLING/<relative path>
# responsibility: <one sentence>
# runtime_stage: <initialization|analysis|processing|validation|repair|audit|reporting|utility>
# allowed_imports: [<stdlib modules>]
# forbidden_imports: [<forbidden modules>]
# spec_reference: SPEC-010.section.<N>
# implementation_phase: PHASE_<N>
# authoring_authority: ARCHON_PRIME
# version: 1.0
# status: canonical|draft|deprecated
```

---

## 11. Validation Gate Conditions

| Gate ID | Stage | Condition | Responsible Module |
|---|---|---|---|
| VG-001 | Pre-execution | architecture_valid == true | validate_architecture.py (M-VAL-01) |
| VG-002 | Pre-crawl | PRE_CRAWL_CHECKLIST.json status == GREEN | checklist_evaluator.py |
| VG-003 | Post-Stage-1 | All S1 output schemas valid, no missing artifacts | schema_registry.validate() |
| VG-004 | Post-Stage-2 | dependency_graph.json non-empty, module_index.json complete | M20, M21 |
| VG-005 | Post-Stage-3 | simulation_report.status == "PASS" | simulation_coordinator |
| VG-006 | Post-Stage-4 | crawl_plan.json valid, order_length > 0 | crawl_planner |
| VG-007 | Per-module | post-mutation syntax valid | syntax_validator |
| VG-008 | Post-crawl | crawl_status.json completion_rate == 100% (excl. quarantined) | report_generator |

---

## 12. Architecture Validation Rules (V2 Tooling Specific)

Additional checks beyond the 8 standard AVR checks defined in SPEC-004:

| Rule ID | Check | Blocking |
|---|---|---|
| AVR-V2-001 | No module exists at repo root outside canonical workflow domains | Yes |
| AVR-V2-002 | routing_table.json contains no legacy AUDIT_SYSTEM/ references | Yes |
| AVR-V2-003 | All analog modules classified in AP_LEGACY_MODULE_MIGRATION_LOG.json before pipeline runs | Yes |
| AVR-V2-004 | All 6 required config files present at canonical paths before initialization | Yes |
| AVR-V2-005 | module_registry.json contains complete 39-module inventory | Yes |

---

## 13. Governance Rules

**Non-Deletion Policy:** No module deleted without explicit Architect authorization. Analog modules preserved at original path until migration confirmed complete.

**Canonical Directory Enforcement (FR-001 binding):** No implementation prompt may place a module outside the three canonical workflow domains. Any prompt violating this rule is rejected by GPT before VS Code execution.

**Legacy Module Migration Policy:** All 22 identified analog modules must be catalogued in `AP_LEGACY_MODULE_MIGRATION_LOG.json` before migration begins. Each entry: original path, target path, classification, migration status.

**Simulation Enforcement:** `--simulate` is the default execution mode for all mutation operators. `--execute` requires VG-005 to have passed in the same session.

**Routing Table Enforcement:** routing_table.json must be rebuilt before PHASE_0 is complete. All references to legacy AUDIT_SYSTEM/ paths are invalid in V2.

**Schema Filename Resolution:** Per open risk CL-G1, `AP_DESIGN_SPEC_SCHEMA.json` and `AP_MASTER_SPEC_V2_SCHEMA.json` refer to the same artifact. All produced DS artifacts reference `AP_DESIGN_SPEC_SCHEMA.json` until the Architect resolves the canonical name.

---

## 14. Implementation Sequence

| Phase ID | Phase Name | Scope | Entry Condition | Exit Condition |
|---|---|---|---|---|
| PHASE_0 | Legacy Migration + Config Creation | 22 analog migrations; 6 config files; migration log; rebuild routing_table.json | Architect approves SPEC-010 | All configs present; migration log complete; no modules at repo root outside domains |
| PHASE_1 | Architecture Validator | M-VAL-01 (SPEC-004) | SPEC-004 approved; PHASE_0 complete | Validator runs clean on known-good fixture |
| PHASE_2 | Foundation | M00 (expand), M01 (expand), M02 | PHASE_1 complete | Architecture validation passes |
| PHASE_3 | Audit Regeneration | M10–M17 | PHASE_2 complete | All S1 outputs produced against test fixture |
| PHASE_4 | Repo Analysis | M20–M25 | PHASE_3 complete | dependency_graph.json and module_index.json valid |
| PHASE_5 | Simulation + Planning | M30–M32, simulation_coordinator, M38, M39 | PHASE_4 complete | Simulation PASS on AP repo |
| PHASE_6 | Crawl Execution Engine | M50–M51, M60–M65, checklist_evaluator | PHASE_5 complete | Single-module crawl pass succeeds end-to-end |
| PHASE_7 | Repair + Quarantine | M70–M72, M80 | PHASE_6 complete | Seeded error resolved; unresolvable module quarantined |
| PHASE_8 | Reporting + Orchestration | M90–M92, M95–M96 | PHASE_7 complete | Full pipeline run produces all output artifacts |
| PHASE_9 | Target Repo Analysis Subsystem | TA-01 through TA-04 | PHASE_8 complete | Gap analysis report produced for AP repo self-analysis |
| PHASE_10 | LOGOS Integration | All modules | PHASE_9 complete; LOGOS present in targets/ | Simulation PASS on LOGOS snapshot; full crawl plan produced |

---

## 15. Enhancement Lifecycle

| Stage ID | Stage | Required Output |
|---|---|---|
| EL-001 | proposal | Enhancement proposal document |
| EL-002 | architect_review | Architect decision |
| EL-003 | spec_update | Updated SPEC-010 or new child spec |
| EL-004 | guide_update | Updated IMPL-010 |
| EL-005 | implementation | Code committed |

**Bypass Rule:** Not bypassable.

---

## 16. Integration Surfaces

| Adjacent System | Interface Type | Data Flow |
|---|---|---|
| LOGOS repository | Input — read-only during analysis | Target of audit regeneration and crawl operations |
| AP_SYSTEM_CONFIG | Input — immutable | Design specs, governance, schemas consumed at initialization |
| AP_SYSTEM_AUDIT | Output — append | Audit and pipeline execution reports |
| WORKFLOW_TARGET_AUDITS | Bidirectional | Gap analysis and audit outputs for external repos |
| SPEC-004 validate_architecture.py | CLI invocation | Called at each gated stage; produces architecture_validation_report.json |
| GPT Prompt Compiler | Downstream consumer | Consumes SPEC-010 + IMPL-010 to derive VS Code prompts |

---

## 17. Verification Criteria

| ID | Criterion | Method | Automated |
|---|---|---|---|
| V-001 | All 39 canonical modules present at canonical paths | validate_architecture.py | Yes |
| V-002 | All 6 config files present at canonical paths | Pre-crawl checklist | Yes |
| V-003 | routing_table.json contains no legacy AUDIT_SYSTEM/ paths | Schema validation | Yes |
| V-004 | Full pipeline completes without halting on clean AP repo | Integration test | Yes |
| V-005 | Simulation mode produces no file writes to target | Integration test: run --simulate, assert no file mutations | Yes |
| V-006 | Repair loop resolves a seeded header violation | Unit test | Yes |
| V-007 | Quarantine isolates a module after repair threshold | Unit test | Yes |
| V-008 | Gap analysis produces AP_REPOSITORY_GAP_ANALYSIS.json | Integration test | Yes |
| V-009 | validate_architecture.py passes on WORKFLOW_MUTATION_TOOLING after PHASE_8 | Run validator | Yes |
| V-010 | No module exists at repo root outside canonical domain directories | validate_architecture.py AVR-V2-001 | Yes |

---

## 18. Deferments

| Item | Rationale | Deferred To |
|---|---|---|
| LOGOS live crawl | Requires all tooling complete + LOGOS available | Post PHASE_9 |
| LOGOS DS/IG V2 schema upgrade | Separate workstream | After AP tooling complete |
| Incremental validation (changed files only) | Optimization; full-scan correctness prerequisite | Post PHASE_8 enhancement |
| Multi-spec registry merge | Requires registry federation design | Future enhancement |
| CI/CD GitHub Actions integration | Infrastructure concern | AP_SYSTEM_CONFIG phase |
| DRAC implementation | Architect standing deferment | Until canonical runtime exists |

---

## 19. Open Questions

| ID | Question | Blocking | Recommendation |
|---|---|---|---|
| OQ-001 | Resolve CL-G1: canonical schema filename AP_DESIGN_SPEC_SCHEMA.json vs. AP_MASTER_SPEC_V2_SCHEMA.json | Yes | Architect to confirm |
| OQ-002 | Architect approval of SPEC-004 (currently Draft) | Yes | Architect to approve or authorize IG production against Draft |
| OQ-003 | Should WORKFLOW_TARGET_AUDITS modules carry the same V2 header schema? | No | Recommend yes — single governance standard |
| OQ-004 | Should AP_TOOL_PROP_01 modules be formalized as SPEC-011 (child of SPEC-010) or remain in SPEC-010? | No | Recommend SPEC-011 for clean boundary separation; TA-01 through TA-04 are scoped here pending that decision |

---

## 20. Revision History

| Version | Date | Change | Author |
|---|---|---|---|
| v1 | 2026-03-10 | Initial specification — V2 tooling architecture | Claude / Formalization_Expert |

---

*End of SPEC-010*
