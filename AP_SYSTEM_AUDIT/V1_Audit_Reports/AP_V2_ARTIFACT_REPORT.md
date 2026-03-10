# ARCHON_PRIME — V2 Artifact Content Report

**Generated:** 2026-03-10 00:11 UTC  
**Scope:** Full repository read-only scan  
**Route:** `AP_SYSTEM_CONFIG/CLAUDE/V2_Overview/`  
**Governance:** NON-DELETION enforced — report only

---

## Repository Summary

| Metric | Value |
|---|---|
| Total files (excl. venv/.git) | 455 |
| `.json` files | 179 |
| `.md` files | 135 |
| `.py` files | 112 |
| `.yml` files | 8 |
| `.docx` files | 6 |
| `none` files | 4 |
| `.txt` files | 4 |
| `.yaml` files | 4 |
| Spec-defined modules (M00–M96) | 39 |
| Spec modules PRESENT_CORRECT | 4 |
| Spec modules MISSING | 35 |
| Non-spec Python modules | 109 |
| Phase-1 remediation targets | 35 |
| Remediation completion | 10.3% |

---

## Directory Structure — Top Level

```
.devcontainer/  (1 children)
.github/  (4 children)
.vscode/  (3 children)
ALL_ARTIFACTS_P1/  (6 children)
AP_SYSTEM_AUDIT/  (39 children)
AP_SYSTEM_CONFIG/  (7 children)
AUDIT_LOGS/  (0 children)
AUDIT_SYSTEM/  (6 children)
Designs_and_Guides/  (17 children)
STAGING_ARTIFACTS/  (2 children)
config/  (3 children)
configs/  (4 children)
controllers/  (7 children)
crawler/  (6 children)
logos_analysis/  (3 children)
logs/  (0 children)
orchestration/  (4 children)
registry/  (4 children)
repair/  (2 children)
schemas/  (4 children)
simulation/  (5 children)
targets/  (1 children)
tests/  (1 children)
tools/  (9 children)
utils/  (1 children)
.gitignore  [402 B]
AP_PHASE1_REPO_SNAPSHOT.zip  [959.2 KB]
MASTER_SYSTEM_DESIGN_SPEC.md  [22.5 KB]
README.md  [14 B]
pyproject.toml  [322 B]
requirements.txt  [115 B]
```

---

## Artifact Content Report

Each section covers a functional group of artifacts.


### Root

#### `MASTER_SYSTEM_DESIGN_SPEC.md`

**Status:** ✓ | **Size:** 22.5 KB | **Lines:** 376 lines  
**Purpose:** Master design specification for ARCHON_PRIME  
**Content snapshot:** # ARCHON_PRIME — MASTER SYSTEM DESIGN SPECIFICATION **Version:** 1.0.0 | **Date:** 2026-03-08 | **Status:** AUTHORITATIVE — DO NOT MODIFY WITHOUT ARCHITECT APPROVAL  ---  ## DELIVERABLE 1 — MASTER SYSTEM DESIGN SPEC  ### A. System Purpose  ARCHON_PRIME is a deterministic, single-


#### `README.md`

**Status:** ✓ | **Size:** 14 B | **Lines:** 1 lines  
**Purpose:** Repository readme and onboarding  
**Content snapshot:** # ARCHON_PRIME


#### `pyproject.toml`

**Status:** ✓ | **Size:** 322 B | **Lines:** 19 lines  
**Purpose:** Python project build and tool configuration  
**Content snapshot:** [tool.black] line-length = 88 target-version = ["py312"]  [tool.ruff] target-version = "py312" line-length = 88 select = ["E", "F", "B", "I"] ignore = [] fix = true  [tool.mypy] python_version = "3.12" strict = true warn_unused_configs = true warn_return_any = true warn_unused_ig


#### `requirements.txt`

**Status:** ✓ | **Size:** 115 B | **Lines:** 10 lines  
**Purpose:** Python package dependencies  
**Content snapshot:** jsonschema>=4.0 PyYAML>=6.0 GitPython>=3.1 pytest>=7.0 pytest-cov>=4.0 black>=24.0 ruff>=0.4 mypy>=1.0 bandit>=1.7



### Architecture

#### `Designs_and_Guides/AP_REMEDIATION_SOURCES/Architecture_Spec/MODULE_INVENTORY.md`

**Status:** ✓ | **Size:** 23.7 KB | **Lines:** 538 lines  
**Purpose:** Authoritative spec of all 39 modules across 11 subsystems (M00–M96)  
**Content snapshot:** # ARCHON_PRIME — COMPLETE MODULE INVENTORY **Deliverable 3** | Version 1.0.0 | 2026-03-08 | AUTHORITATIVE  ---  ## MODULE REGISTRY — ALL SUBSYSTEMS  Grouped by subsystem. Each module fully specified: path, purpose, inputs, outputs, dependencies, blocking/supporting classification


#### `Designs_and_Guides/AP_REMEDIATION_SOURCES/Architecture_Spec/IMPLEMENTATION_SEQUENCE.md`

**Status:** ✓ | **Size:** 17.3 KB | **Lines:** 403 lines  
**Purpose:** Sequential build plan across 10 stages with validation gates  
**Content snapshot:** # ARCHON_PRIME — SEQUENTIAL IMPLEMENTATION PLAN **Deliverable 5** | Version 1.0.0 | 2026-03-08 | AUTHORITATIVE  ---  ## SEQUENCING PRINCIPLES  1. **No implicit wiring.** Every module that is built assumes its dependencies are already built and frozen. 2. **Freeze before downstrea


#### `Designs_and_Guides/AP_REMEDIATION_SOURCES/Architecture_Spec/MASTER_SYSTEM_DESIGN_SPEC.md`

**Status:** ✓ | **Size:** 22.5 KB | **Lines:** 376 lines  
**Purpose:** Full architectural design specification document  
**Content snapshot:** # ARCHON_PRIME — MASTER SYSTEM DESIGN SPECIFICATION **Version:** 1.0.0 | **Date:** 2026-03-08 | **Status:** AUTHORITATIVE — DO NOT MODIFY WITHOUT ARCHITECT APPROVAL  ---  ## DELIVERABLE 1 — MASTER SYSTEM DESIGN SPEC  ### A. System Purpose  ARCHON_PRIME is a deterministic, single-



### Remediation

#### `Designs_and_Guides/AP_REMEDIATION_SOURCES/phase1_remediation_plan.json`

**Status:** ✓ | **Size:** 25.5 KB | **Lines:** 835 lines  
**Purpose:** Phase-1 remediation plan with governance patch — 35 remediation targets, classification schema, non-deletion policy  
**Content snapshot:** Top-level keys: phase, generated_at, repo_root, spec_source, audit_source, sequence_source, artifact_integrity, total_modules, present_correct, missing_modules, misplaced_modules, completion_score_pct


#### `AP_SYSTEM_AUDIT/phase2_audit_snapshot.json`

**Status:** ✓ | **Size:** 61.8 KB | **Lines:** 1,846 lines  
**Purpose:** Phase-2 audit snapshot — live repo surface scan, 112 Python files, 35 targets, dependency graph 92 edges  
**Content snapshot:** Top-level keys: phase, generated_at, repo_root, source_plan, scan_stats, targets_summary, present_modules, missing_modules, misplaced_modules, non_spec_modules, dependency_graph, subsystem_completion


#### `AP_SYSTEM_AUDIT/manual_review_candidates.json`

**Status:** ✓ | **Size:** 16.3 KB | **Lines:** 371 lines  
**Purpose:** Manual review list of 50 non-spec modules with classification and spec mapping  
**Content snapshot:** Top-level keys: schema_version, generated_at, source_artifact, governance_policy, authority, review_required, summary, modules



### Audit

#### `AP_SYSTEM_AUDIT/phase1_remediation_report.json`

**Status:** ✓ | **Size:** 6.6 KB | **Lines:** 198 lines  
**Purpose:** Phase-1 remediation report generated by prior pipeline run  
**Content snapshot:** Top-level keys: remediation_metadata, venv_removed, interpreter_path, interpreter_path_update, pyproject_created, tool_versions, git_hygiene_status, environment_status, environment_status_detail, ready_for_freeze, freeze_blockers, phase1_actions_completed


#### `Designs_and_Guides/AP_REMEDIATION_SOURCES/Audit_Artifacts/ARCHON_PRIME_FUNCTIONALITY_AUDIT_V2.json`

**Status:** ✓ | **Size:** 11.5 KB | **Lines:** 320 lines  
**Purpose:** V2 functionality audit — 39 spec modules, 4 present, 35 missing, 50 non-spec modules documented  
**Content snapshot:** Top-level keys: schema_version, generated_at, audit_id, data_source, spec_source, invalidation_notice, global_stats, subsystem_results, non_spec_functional_layers, config_file_status, empty_subsystem_directories


#### `Designs_and_Guides/AP_REMEDIATION_SOURCES/Audit_Artifacts/ARCHON_PRIME_SUBSYSTEM_MAP.json`

**Status:** ✓ | **Size:** 11.2 KB | **Lines:** 396 lines  
**Purpose:** Subsystem-level completion map across S0–S10  
**Content snapshot:** Top-level keys: S0_FOUNDATION, S1_AUDIT_REGEN, S2_REPO_ANALYSIS, S3_SIMULATION, S4_CRAWL_PLANNING, S5_MUTATION, S6_CRAWL_EXECUTION, S7_ERROR_REPAIR, S8_QUARANTINE, S9_ARTIFACT_REPORTING, S10_ORCHESTRATION


#### `Designs_and_Guides/AP_REMEDIATION_SOURCES/Audit_Artifacts/ARCHON_PRIME_MODULE_INVENTORY.json`

**Status:** ✓ | **Size:** 16.2 KB | **Lines:** 488 lines  
**Purpose:** Full module inventory list with spec status for all 54 Python files found  
**Content snapshot:** JSON array — 54 items



### Control

#### `Designs_and_Guides/AP_REMEDIATION_SOURCES/Control_Dataset/AP_ARTIFACT_INDEX.json`

**Status:** ✓ | **Size:** 102.9 KB | **Lines:** 2,378 lines  
**Purpose:** Control dataset artifact index for Phase-1  
**Content snapshot:** JSON array — 198 items


#### `Designs_and_Guides/AP_REMEDIATION_SOURCES/Control_Dataset/AP_DIRECTORY_TREE_CURRENT.json`

**Status:** ✓ | **Size:** 35.2 KB | **Lines:** 1,084 lines  
**Purpose:** Snapshot directory tree captured at Phase-1 baseline  
**Content snapshot:** Top-level keys: schema_version, generated_at, repo_root, tree


#### `Designs_and_Guides/AP_REMEDIATION_SOURCES/Control_Dataset/step_failures.json`

**Status:** ✓ | **Size:** 2 B | **Lines:** 1 lines  
**Purpose:** Step failure records from pipeline runs  
**Content snapshot:** JSON array — 0 items



### Workflow

#### `Designs_and_Guides/AP_REMEDIATION_SOURCES/Workflow_Context/AP_WORKFLOW_CONTEXT.md`

**Status:** ✓ | **Size:** 33.0 KB | **Lines:** 709 lines  
**Purpose:** Workflow context snapshot — describes pipeline state and artifact surfaces  
**Content snapshot:** # ARCHON_PRIME — WORKFLOW CONTEXT SNAPSHOT **Document Type:** Operational Context Reference **Version:** v1 **Status:** draft **Date:** 2026-03-08 **Author:** Claude (Formalization_Expert) — merged from Claude SPEC-004/IMPL-003 analysis and GPT Environment Audit Report **Authorit


#### `Designs_and_Guides/AP_REMEDIATION_SOURCES/Workflow_Context/AP_WORKFLOW_OVERVIEW.md`

**Status:** ✓ | **Size:** 13.0 KB | **Lines:** 307 lines  
**Purpose:** High-level workflow overview for remediation phases  
**Content snapshot:** # AP_WORKFLOW_OVERVIEW.md  ## Document Identity  | Field | Value | |---|---| | Artifact ID | OPS-SYS-001 | | System | ARCHON_PRIME | | Platform | Cross-Platform | | Artifact Type | System Workflow Overview | | Version | v1 | | Status | Final Draft | | Authority Source | Architect



### Foundation Config

#### `configs/crawl_configs/crawl_config.json`

**Status:** ✓ | **Size:** 387 B | **Lines:** 14 lines  
**Purpose:** Crawl runtime config — workers, depth, target & registry paths  
**Content snapshot:** Top-level keys: version, mutation_allowed, repair, crawler, targets_file, routing_table, repair_registry


#### `configs/crawl_configs/logos_targets.yaml`

**Status:** ✓ | **Size:** 234 B | **Lines:** 14 lines  
**Purpose:** LOGOS target repository definition with extension and exclusion filters  
**Content snapshot:** targets:   - name: LOGOS     repository_path: ../LOGOS     include_extensions:       - ".py"       - ".json"       - ".yaml"       - ".yml"       - ".md"     exclude_paths:       - "__pycache__"       - ".git"       - ".pytest_cache"


#### `configs/crawl_configs/ap_config.yaml`

**Status:** ✓ | **Size:** 70 B | **Lines:** 5 lines  
**Purpose:** ARCHON_PRIME default runtime behavioural settings  
**Content snapshot:** defaults:   mutation_allowed: false   repair:     max_retry_cycles: 3


#### `configs/repair_registry/repair_registry.json`

**Status:** ✓ | **Size:** 183 B | **Lines:** 8 lines  
**Purpose:** Repair registry mapping failure classes to repair operators  
**Content snapshot:** Top-level keys: version, repair_types


#### `orchestration/task_router/routing_table.json`

**Status:** ✓ | **Size:** 314 B | **Lines:** 7 lines  
**Purpose:** Artifact routing table — maps artifact types to canonical destination paths  
**Content snapshot:** Top-level keys: repo_python_files, module_index, dependency_graph, simulation_report, validation_report



### Foundation Modules

#### `tools/normalization_tools/schema_registry.py`

**Status:** ✓ | **Size:** 3.1 KB | **Lines:** 104 lines  
**Purpose:** M00 — Central JSON schema registry with get_schema(), validate(), register_schema()  
**Content snapshot:** # ARCHON_PRIME MODULE # Created by remediation stage AP-REM-001 # Purpose: Foundation configuration loader  """ schema_registry.py — Central registry for JSON schema definitions.  Loads JSON schemas from the orchestration/json_drivers/ directory and validates configuration struct


#### `tools/audit_tools/repair_registry_loader.py`

**Status:** ✓ | **Size:** 2.5 KB | **Lines:** 89 lines  
**Purpose:** M02 — Loads repair_registry.json, exposes load_repair_registry() and get_repair_action()  
**Content snapshot:** # ARCHON_PRIME MODULE # Created by remediation stage AP-REM-001 # Purpose: Foundation configuration loader  """ repair_registry_loader.py — Load and expose the repair registry (M02).  Loads configs/repair_registry/repair_registry.json and returns its parsed content as a dictionar


#### `orchestration/task_router/routing_table_loader.py`

**Status:** ✓ | **Size:** 2.6 KB | **Lines:** 94 lines  
**Purpose:** M01 — Loads routing_table.json, exposes load_routing_table() and resolve_destination()  
**Content snapshot:** # ARCHON_PRIME MODULE # Created by remediation stage AP-REM-001 # Purpose: Foundation configuration loader  """ routing_table_loader.py — Load and expose the canonical artifact routing table (M01).  Loads orchestration/task_router/routing_table.json and returns its parsed content



### Simulation (S3)

#### `simulation/repo_simulator/repo_simulator.py`

**Status:** ✓ | **Size:** 166 B | **Lines:** 9 lines  
**Purpose:** M30 — SPEC_PRESENT: Repo state simulator  
**Content snapshot:** from pathlib import Path  def simulate():     files=list(Path(".").rglob("*.py"))     print("Simulated modules:",len(files))  if __name__=="__main__":     simulate()


#### `simulation/runtime_simulator/runtime_simulator.py`

**Status:** ✓ | **Size:** 2.6 KB | **Lines:** 93 lines  
**Purpose:** M31 — SPEC_PRESENT: Runtime boot sequence simulator  
**Content snapshot:** """ ARCHON PRIME — Runtime Boot Simulator Stage 3: Simulation System Activation  Reads dependency graph and structure map artifacts produced by Stage-2 and simulates repository runtime boot sequence. Read-only — no mutations performed. """  import json import os from pathlib impo


#### `simulation/import_simulator/import_simulator.py`

**Status:** ✓ | **Size:** 1.9 KB | **Lines:** 66 lines  
**Purpose:** M32 — SPEC_PRESENT: Import resolution simulator  
**Content snapshot:** """ ARCHON PRIME — Import Simulator Stage 3: Simulation System Activation  Reads import topology artifacts produced by Stage-2 analysis and simulates import resolution across the repository. Read-only — no mutations performed. """  import json import os from pathlib import Path  



### Crawler

#### `crawler/monitor/crawl_monitor.py`

**Status:** ✓ | **Size:** 142 B | **Lines:** 10 lines  
**Purpose:** M65 — SPEC_PRESENT: Real-time crawl monitor  
**Content snapshot:** import time  def monitor():     while True:         print("Crawler running...")         time.sleep(5)  if __name__=="__main__":     monitor()



### Controllers

#### `controllers/pipeline_controller.py`

**Status:** ✓ | **Size:** 20.4 KB | **Lines:** 539 lines  
**Purpose:** ANALOG: Pipeline controller — analog to M96 controller_main  
**Content snapshot:** """ ARCHON PRIME — Pipeline Controller Stage 6: Pipeline Controller Implementation  Orchestrates the full AP workflow pipeline in strict deterministic order:      audit → analysis → simulation → crawl → repair  Responsibilities:   - Initialize and sequence all sub-controllers   -


#### `controllers/crawler_controller.py`

**Status:** ✓ | **Size:** 9.1 KB | **Lines:** 264 lines  
**Purpose:** ANALOG: Crawler controller — analog to M60 crawl_executor  
**Content snapshot:** """ ARCHON PRIME — Crawler Controller Stage 4: Crawler System Implementation  Responsibilities:   - Load crawl_config.json and targets/logos_targets.yaml via ConfigLoader   - Instantiate CrawlEngine and CrawlMonitor   - Execute deterministic repository traversal   - Route travers


#### `controllers/repair_controller.py`

**Status:** ✓ | **Size:** 15.7 KB | **Lines:** 414 lines  
**Purpose:** ANALOG: Repair controller — analog to M71/M72 repair subsystem  
**Content snapshot:** """ ARCHON PRIME — Repair Controller Stage 5: Repair System Implementation  Responsibilities:   - Load repair registry from registry/repair_registry.json   - Dynamically import repair operator classes   - Consume upstream audit artifacts from AP_SYSTEM_AUDIT/   - Map detected iss



### Repair Operators

#### `repair/operators/header_injection_operator.py`

**Status:** ✓ | **Size:** 3.3 KB | **Lines:** 110 lines  
**Purpose:** ANALOG: Header injection — analog to M50, at wrong path  
**Content snapshot:** """ ARCHON PRIME — Header Injection Operator Stage 5: Repair System Implementation  Plans and applies canonical header block injection into Python modules that are missing required governance/metadata headers.  SAFETY CONTRACT:   - plan_repair() is always safe — read-only analysi


#### `repair/operators/import_rewrite_operator.py`

**Status:** ✓ | **Size:** 3.3 KB | **Lines:** 101 lines  
**Purpose:** ANALOG: Import rewrite — analog to M51, at wrong path  
**Content snapshot:** """ ARCHON PRIME — Import Rewrite Operator Stage 5: Repair System Implementation  Plans and applies corrections to broken or malformed import statements.  SAFETY CONTRACT:   - plan_repair() is always safe — read-only analysis only.   - apply_repair() MUST NOT be called while muta



### Audit Tools

#### `tools/audit_tools/run_audit_suite.py`

**Status:** ✓ | **Size:** 979 B | **Lines:** 38 lines  
**Purpose:** ENHANCEMENT: Orchestrates full audit tool suite  
**Content snapshot:** import sys  import import_surface_audit import circular_dependency_audit import header_schema_audit import unused_import_audit import duplicate_module_audit import file_size_audit import runtime_entry_audit import orphan_module_audit import symbol_collision_audit import cross_pac


#### `tools/audit_tools/governance_contract_audit.py`

**Status:** ✓ | **Size:** 979 B | **Lines:** 50 lines  
**Purpose:** ENHANCEMENT: Governance contract scanner, analog to M15  
**Content snapshot:** import re from pathlib import Path from audit_utils import write_log,generate_id  GOV_TERMS = [     "governance",     "contract",     "policy",     "protocol",     "rule",     "constraint",     "spec",     "design" ]  def run(target):      issues=[]      for p in Path(target).rgl



### Remediation Scripts

#### `tools/ap_phase2_audit.py`

**Status:** ✓ | **Size:** 16.3 KB | **Lines:** 405 lines  
**Purpose:** Phase-2 audit script — scans repo, compares against 35 targets, writes phase2_audit_snapshot.json  
**Content snapshot:** # ARCHON_PRIME MODULE # Created by remediation stage AP-REM-002 # Purpose: Phase-2 pre-crawl audit snapshot generator  """ ap_phase2_audit.py — Phase-2 Pre-Crawl Audit Regeneration  Read-only scan of the repository surface.  Produces AP_SYSTEM_AUDIT/phase2_audit_snapshot.json.  G



### Schemas

#### `schemas/CrawlMutationRecord.schema.json`

**Status:** ✓ | **Size:** 496 B | **Lines:** 21 lines  
**Purpose:** JSON schema for crawl mutation records  
**Content snapshot:** Top-level keys: type, properties, required


#### `schemas/ValidationManifest.schema.json`

**Status:** ✓ | **Size:** 292 B | **Lines:** 11 lines  
**Purpose:** JSON schema for validation manifests  
**Content snapshot:** Top-level keys: type, properties


#### `schemas/PhaseGate.schema.json`

**Status:** ✓ | **Size:** 306 B | **Lines:** 14 lines  
**Purpose:** JSON schema for phase gate records  
**Content snapshot:** Top-level keys: type, properties


#### `schemas/QuarantineRecord.schema.json`

**Status:** ✓ | **Size:** 324 B | **Lines:** 14 lines  
**Purpose:** JSON schema for quarantine records  
**Content snapshot:** Top-level keys: type, properties



### Registry

#### `registry/repair_registry.json`

**Status:** ✓ | **Size:** 1.8 KB | **Lines:** 50 lines  
**Purpose:** Legacy repair registry at non-spec path (registry/)  
**Content snapshot:** Top-level keys: repairs


#### `registry/module_registry.json`

**Status:** ✓ | **Size:** 1.9 KB | **Lines:** 53 lines  
**Purpose:** Module registry data  
**Content snapshot:** Top-level keys: modules



### System Config

#### `AP_SYSTEM_CONFIG/AP_WORKFLOW_CONTEXT.md`

**Status:** ✓ | **Size:** 33.0 KB | **Lines:** 709 lines  
**Purpose:** Workflow context reference copy  
**Content snapshot:** # ARCHON_PRIME — WORKFLOW CONTEXT SNAPSHOT **Document Type:** Operational Context Reference **Version:** v1 **Status:** draft **Date:** 2026-03-08 **Author:** Claude (Formalization_Expert) — merged from Claude SPEC-004/IMPL-003 analysis and GPT Environment Audit Report **Authorit


#### `AP_SYSTEM_CONFIG/AP_WORKFLOW_OVERVIEW.md`

**Status:** ✓ | **Size:** 13.0 KB | **Lines:** 307 lines  
**Purpose:** Workflow overview reference copy  
**Content snapshot:** # AP_WORKFLOW_OVERVIEW.md  ## Document Identity  | Field | Value | |---|---| | Artifact ID | OPS-SYS-001 | | System | ARCHON_PRIME | | Platform | Cross-Platform | | Artifact Type | System Workflow Overview | | Version | v1 | | Status | Final Draft | | Authority Source | Architect


#### `AP_SYSTEM_CONFIG/AP_VSCODE_PIPELINE_INTEGRATION.md`

**Status:** ✓ | **Size:** 1.7 KB | **Lines:** 80 lines  
**Purpose:** VS Code pipeline integration guide  
**Content snapshot:** # AP_VSCODE_PIPELINE_INTEGRATION  ## Document Identity  System: ARCHON_PRIME   Artifact Type: Pipeline Integration Specification   Status: Active  ## Purpose  This document defines how the VS Code execution agent integrates into the ARCHON PRIME workflow pipeline.  The execution 


#### `AP_SYSTEM_CONFIG/EXECUTION_AGENT_ROLE.md`

**Status:** ✓ | **Size:** 13.2 KB | **Lines:** 298 lines  
**Purpose:** Execution agent role definition for VS Code chat agent  
**Content snapshot:** # EXECUTION_AGENT_ROLE.md  ## Document Identity  | Field | Value | |---|---| | Artifact ID | OPS-SYS-002 | | System | ARCHON_PRIME | | Platform | VS Code / Codespaces | | Artifact Type | Execution Agent Role Specification | | Version | v1 | | Status | Final Draft | | Authority So


---

## Empty / Reserved Directories

These directories exist but contain no files. They are reserved for pipeline outputs:

- `crawler/pipeline/`
- `crawler/repair/`
- `crawler/mutation/`
- `crawler/quarantine/`
- `crawler/commit/`
- `orchestration/controllers/`
- `orchestration/execution_graphs/`
- `AUDIT_SYSTEM/scripts/import_scanners/`
- `AUDIT_SYSTEM/scripts/header_scanners/`
- `AUDIT_SYSTEM/scripts/governance_scanners/`
- `AUDIT_SYSTEM/scripts/runtime_scanners/`
- `AUDIT_SYSTEM/analysis/dependency_graphs/`
- `AUDIT_SYSTEM/analysis/runtime_maps/`
- `AUDIT_SYSTEM/reports/concept_reports/`
- `AUDIT_SYSTEM/reports/governance_reports/`
- `AUDIT_SYSTEM/reports/import_reports/`
- `AUDIT_SYSTEM/reports/runtime_reports/`
- `AUDIT_SYSTEM/reports/structural_reports/`
- `AUDIT_SYSTEM/baselines/initial_repo_snapshot/`
- `AUDIT_SYSTEM/runtime_monitor/live_status/`
- `AUDIT_SYSTEM/runtime_monitor/progress_tracking/`
- `AUDIT_LOGS/`
- `logs/`
- `STAGING_ARTIFACTS/incoming/`
- `STAGING_ARTIFACTS/sorted/`
- `logos_analysis/reports/`
- `logos_analysis/sandbox/`
- `logos_analysis/source_snapshot/`

---

## Remediation Pipeline State

| Phase | Status | Artifact |
|---|---|---|
| Phase-0 Bundle Load | COMPLETE | `AP_REMEDIATION_SOURCES/` (12 files) |
| Phase-1 Remediation Plan | COMPLETE | `AP_SYSTEM_AUDIT/phase1_remediation_plan.json` — 35 targets |
| Phase-1 Governance Patch | COMPLETE | Non-deletion policy + classification schema installed |
| Phase-1 Review Artifact | COMPLETE | `AP_SYSTEM_AUDIT/manual_review_candidates.json` — 50 non-spec modules |
| AP-REM-001 Stage 0 Foundation | COMPLETE | 5 configs + 3 Python modules created |
| Phase-2 Audit Snapshot | COMPLETE | `AP_SYSTEM_AUDIT/phase2_audit_snapshot.json` — 112 files scanned |
| Phase-3 Module Creation | **PENDING** | 32 missing spec modules to be created |
| Phase-4 Module Relocation | **PENDING** | 0 misplaced modules identified |
| Phase-5 Config Normalization | **PENDING** | 4 config files at wrong paths |
| Phase-6 Final Audit | **PENDING** | — |

---

## Spec Module Build Queue (Priority Order)

Modules listed by implementation stage and priority as defined in `phase1_remediation_plan.json`:

| Priority | Module ID | Module Name | Subsystem | Stage | Blocking |
|---|---|---|---|---|---|
| 1 | M00 | `schema_registry.py` | S0_FOUNDATION | 0 | YES |
| 2 | M01 | `routing_table_loader.py` | S0_FOUNDATION | 0 | YES |
| 3 | M02 | `repair_registry_loader.py` | S0_FOUNDATION | 0 | YES |
| 4 | M10 | `repo_directory_scanner.py` | S1_AUDIT_REGEN | 1 | YES |
| 5 | M11 | `python_file_collector.py` | S1_AUDIT_REGEN | 1 | YES |
| 6 | M12 | `import_extractor.py` | S1_AUDIT_REGEN | 1 | YES |
| 7 | M14 | `header_schema_scanner.py` | S1_AUDIT_REGEN | 1 | YES |
| 8 | M15 | `governance_contract_scanner.py` | S1_AUDIT_REGEN | 1 | YES |
| 9 | M16 | `runtime_phase_scanner.py` | S1_AUDIT_REGEN | 1 | YES |
| 10 | M13 | `symbol_import_extractor.py` | S1_AUDIT_REGEN | 1 | — |
| 11 | M17 | `concept_spec_gap_detector.py` | S1_AUDIT_REGEN | 1 | — |
| 12 | M20 | `module_index_builder.py` | S2_REPO_ANALYSIS | 2 | YES |
| 13 | M21 | `dependency_graph_builder.py` | S2_REPO_ANALYSIS | 2 | YES |
| 14 | M23 | `runtime_phase_mapper.py` | S2_REPO_ANALYSIS | 2 | YES |
| 15 | M22 | `circular_dependency_detector.py` | S2_REPO_ANALYSIS | 2 | YES |
| 16 | M24 | `runtime_boot_sequencer.py` | S2_REPO_ANALYSIS | 2 | YES |
| 17 | M25 | `canonical_import_registry_builder.py` | S2_REPO_ANALYSIS | 2 | YES |
| 18 | M50 | `header_injector.py` | S5_MUTATION | 3 | YES |
| 19 | M51 | `import_rewriter.py` | S5_MUTATION | 3 | YES |
| 20 | M62 | `syntax_validator.py` | S6_CRAWL_EXECUTION | 4 | YES |
| 21 | M63 | `governance_validator.py` | S6_CRAWL_EXECUTION | 4 | YES |
| 22 | M64 | `phase_validator.py` | S6_CRAWL_EXECUTION | 4 | YES |
| 23 | M38 | `crawl_planner.py` | S4_CRAWL_PLANNING | 5 | YES |
| 24 | M39 | `execution_graph_builder.py` | S4_CRAWL_PLANNING | 5 | YES |
| 25 | M61 | `module_processor.py` | S6_CRAWL_EXECUTION | 6 | YES |
| 26 | M60 | `crawl_executor.py` | S6_CRAWL_EXECUTION | 6 | YES |
| 27 | M70 | `error_classifier.py` | S7_ERROR_REPAIR | 7 | YES |
| 28 | M71 | `repair_router.py` | S7_ERROR_REPAIR | 7 | YES |
| 29 | M72 | `repair_executor.py` | S7_ERROR_REPAIR | 7 | YES |
| 30 | M80 | `quarantine_manager.py` | S8_QUARANTINE | 8 | YES |
| 31 | M90 | `artifact_router.py` | S9_ARTIFACT_REPORTING | 9 | YES |
| 32 | M91 | `report_generator.py` | S9_ARTIFACT_REPORTING | 9 | YES |
| 33 | M92 | `commit_finalizer.py` | S9_ARTIFACT_REPORTING | 9 | YES |
| 34 | M95 | `task_router.py` | S10_ORCHESTRATION | 10 | YES |
| 35 | M96 | `controller_main.py` | S10_ORCHESTRATION | 10 | YES |

---

*End of report. All data derived from read-only scan. No repository files were modified.*
