# System Tree Relocation Plan

SYSTEM: ARCHON_PRIME
REPORT_TYPE: Structural Audit — Deterministic Artifact Relocation Plan
AUDIT_PASS: System Tree Structural Audit
AUDIT_DATE: 2026-03-11
AUTHORITY: Architect
STATUS: Audit Only — Repository NOT Mutated

---

## Overview

This document provides a deterministic move plan for all artifacts detected as misplaced within the SYSTEM tree. Moves are listed in execution order with full source path, destination path, and rationale.

**Total moves required:** 12 artifact moves + 5 empty directory deletions + 1 REPORTS tree teardown

---

## Execution Prerequisites

Before executing any moves:

1. Complete the current audit pass (all STRUCTURE/ report files generated)
2. Archive the STRUCTURE/ audit outputs to a durable location outside SYSTEM
3. Verify destination directories exist in WORKFLOW_TARGET_AUDITS/
4. Stage all moves as a single atomic commit

---

## Phase 1 — Structural Analysis Reports (3 moves)

These artifacts are structural inventory and analysis outputs from the AP V2 tooling pass. Destination: `WORKFLOW_TARGET_AUDITS/MODULES/reports/structural_reports/`

---

**MOVE 1**
```
FROM:  AP_SYSTEM_CONFIG/SYSTEM/REPORTS/TOOLING/ap_v2_artifact_inventory.md
TO:    WORKFLOW_TARGET_AUDITS/MODULES/reports/structural_reports/ap_v2_artifact_inventory.md
```
RATIONALE: Artifact inventory is a structural analysis output of the V2 tooling pass against a workflow target. Not a system configuration artifact. The structural_reports/ directory in WORKFLOW_TARGET_AUDITS/MODULES/reports/ is the canonical home for this artifact class.

---

**MOVE 2**
```
FROM:  AP_SYSTEM_CONFIG/SYSTEM/REPORTS/TOOLING/ap_v2_dependency_graph.md
TO:    WORKFLOW_TARGET_AUDITS/MODULES/reports/structural_reports/ap_v2_dependency_graph.md
```
RATIONALE: Dependency graph is a structural analysis output documenting module relationships in the workflow target. Not a system configuration artifact.

---

**MOVE 3**
```
FROM:  AP_SYSTEM_CONFIG/SYSTEM/REPORTS/TOOLING/ap_v2_structure_analysis.md
TO:    WORKFLOW_TARGET_AUDITS/MODULES/reports/structural_reports/ap_v2_structure_analysis.md
```
RATIONALE: Structure analysis is a structural evaluation report of the workflow target. Not a system configuration artifact.

---

## Phase 2 — Runtime Execution Reports (7 moves)

These artifacts are runtime execution outputs from mutation, simulation, and validation passes. Destination: `WORKFLOW_TARGET_AUDITS/MODULES/reports/runtime_reports/`

---

**MOVE 4**
```
FROM:  AP_SYSTEM_CONFIG/SYSTEM/REPORTS/TOOLING/ap_v2_mutation_plan.md
TO:    WORKFLOW_TARGET_AUDITS/MODULES/reports/runtime_reports/ap_v2_mutation_plan.md
```
RATIONALE: Mutation plan is an execution-phase planning artifact produced by the tooling pass. Belongs in runtime reports.

---

**MOVE 5**
```
FROM:  AP_SYSTEM_CONFIG/SYSTEM/REPORTS/TOOLING/ap_v2_mutation_results.md
TO:    WORKFLOW_TARGET_AUDITS/MODULES/reports/runtime_reports/ap_v2_mutation_results.md
```
RATIONALE: Mutation results document the outcome of a tooling execution pass. Belongs in runtime reports.

---

**MOVE 6**
```
FROM:  AP_SYSTEM_CONFIG/SYSTEM/REPORTS/TOOLING/ap_v2_simulation_results.md
TO:    WORKFLOW_TARGET_AUDITS/MODULES/reports/runtime_reports/ap_v2_simulation_results.md
```
RATIONALE: Simulation results are direct execution outputs of a simulation pass. Belongs in runtime reports.

---

**MOVE 7**
```
FROM:  AP_SYSTEM_CONFIG/SYSTEM/REPORTS/VALIDATION_RESULTS/ap_v2_simulation_validation.md
TO:    WORKFLOW_TARGET_AUDITS/MODULES/reports/runtime_reports/ap_v2_simulation_validation.md
```
RATIONALE: Simulation validation is a runtime verification artifact. Belongs in runtime reports.

---

**MOVE 8**
```
FROM:  AP_SYSTEM_CONFIG/SYSTEM/REPORTS/VALIDATION_RESULTS/ap_v2_tooling_execution_report.md
TO:    WORKFLOW_TARGET_AUDITS/MODULES/reports/runtime_reports/ap_v2_tooling_execution_report.md
```
RATIONALE: Tooling execution report documents the runtime outcome of a tooling execution pass. Belongs in runtime reports.

---

**MOVE 9**
```
FROM:  AP_SYSTEM_CONFIG/SYSTEM/REPORTS/VALIDATION_RESULTS/ap_v2_tooling_resimulation_report.md
TO:    WORKFLOW_TARGET_AUDITS/MODULES/reports/runtime_reports/ap_v2_tooling_resimulation_report.md
```
RATIONALE: Re-simulation report is a re-execution pass output. Belongs in runtime reports.

---

**MOVE 10**
```
FROM:  AP_SYSTEM_CONFIG/SYSTEM/REPORTS/VALIDATION_RESULTS/ap_v2_tooling_simulation_report.md
TO:    WORKFLOW_TARGET_AUDITS/MODULES/reports/runtime_reports/ap_v2_tooling_simulation_report.md
```
RATIONALE: Simulation report is a direct simulation pass output. Belongs in runtime reports.

---

## Phase 3 — Pre-Tooling Baseline Artifacts (2 moves)

These artifacts represent the pre-execution state captured before the V2 tooling pass. Destination: `WORKFLOW_TARGET_AUDITS/AUDIT_LOGS/baselines/`

---

**MOVE 11**
```
FROM:  AP_SYSTEM_CONFIG/SYSTEM/REPORTS/VALIDATION_RESULTS/pre_tooling_artifact_install_report.md
TO:    WORKFLOW_TARGET_AUDITS/AUDIT_LOGS/baselines/pre_tooling_artifact_install_report.md
```
RATIONALE: Pre-tooling installation report is a baseline state snapshot taken before execution began. The AUDIT_LOGS/baselines/ directory is the canonical home for pre-execution snapshots.

---

**MOVE 12**
```
FROM:  AP_SYSTEM_CONFIG/SYSTEM/REPORTS/VALIDATION_RESULTS/pre_tooling_remediation_report.md
TO:    WORKFLOW_TARGET_AUDITS/AUDIT_LOGS/baselines/pre_tooling_remediation_report.md
```
RATIONALE: Pre-tooling remediation report is a baseline remediation record captured before tooling execution. Belongs with other baseline artifacts.

---

## Phase 4 — Audit Output Relocation (this audit's own outputs)

The STRUCTURE/ directory and its contents are themselves execution outputs of this audit pass. They must be archived before the REPORTS directory is deleted.

```
FROM:  AP_SYSTEM_CONFIG/SYSTEM/REPORTS/STRUCTURE/system_tree_inventory.md
TO:    WORKFLOW_TARGET_AUDITS/MODULES/reports/structural_reports/system_tree_inventory.md

FROM:  AP_SYSTEM_CONFIG/SYSTEM/REPORTS/STRUCTURE/misplaced_artifact_report.md
TO:    WORKFLOW_TARGET_AUDITS/MODULES/reports/structural_reports/misplaced_artifact_report.md

FROM:  AP_SYSTEM_CONFIG/SYSTEM/REPORTS/STRUCTURE/execution_envelope_structure_analysis.md
TO:    WORKFLOW_TARGET_AUDITS/MODULES/reports/structural_reports/execution_envelope_structure_analysis.md

FROM:  AP_SYSTEM_CONFIG/SYSTEM/REPORTS/STRUCTURE/empty_directory_population_strategy.md
TO:    WORKFLOW_TARGET_AUDITS/MODULES/reports/structural_reports/empty_directory_population_strategy.md

FROM:  AP_SYSTEM_CONFIG/SYSTEM/REPORTS/STRUCTURE/reports_directory_relocation_strategy.md
TO:    WORKFLOW_TARGET_AUDITS/MODULES/reports/structural_reports/reports_directory_relocation_strategy.md

FROM:  AP_SYSTEM_CONFIG/SYSTEM/REPORTS/STRUCTURE/system_domain_boundary_validation.md
TO:    WORKFLOW_TARGET_AUDITS/MODULES/reports/structural_reports/system_domain_boundary_validation.md

FROM:  AP_SYSTEM_CONFIG/SYSTEM/REPORTS/STRUCTURE/system_tree_relocation_plan.md
TO:    WORKFLOW_TARGET_AUDITS/MODULES/reports/structural_reports/system_tree_relocation_plan.md

FROM:  AP_SYSTEM_CONFIG/SYSTEM/REPORTS/STRUCTURE/system_tree_normalization_report.md
TO:    WORKFLOW_TARGET_AUDITS/MODULES/reports/structural_reports/system_tree_normalization_report.md
```

---

## Phase 5 — Empty Directory and REPORTS Tree Deletion

After all moves are confirmed, delete the now-empty REPORTS directory tree:

```
DELETE: AP_SYSTEM_CONFIG/SYSTEM/REPORTS/STRUCTURE/
DELETE: AP_SYSTEM_CONFIG/SYSTEM/REPORTS/TOOLING/
DELETE: AP_SYSTEM_CONFIG/SYSTEM/REPORTS/VALIDATION_RESULTS/
DELETE: AP_SYSTEM_CONFIG/SYSTEM/REPORTS/EXECUTION_LOGS/
DELETE: AP_SYSTEM_CONFIG/SYSTEM/REPORTS/SIMULATION_RESULTS/
DELETE: AP_SYSTEM_CONFIG/SYSTEM/REPORTS/
```

---

## Move Summary Table

| Move # | Phase | Artifact                                  | Destination Surface                                      |
|--------|-------|-------------------------------------------|----------------------------------------------------------|
| 1      | 1     | ap_v2_artifact_inventory.md               | WORKFLOW_TARGET_AUDITS/MODULES/reports/structural_reports/ |
| 2      | 1     | ap_v2_dependency_graph.md                 | WORKFLOW_TARGET_AUDITS/MODULES/reports/structural_reports/ |
| 3      | 1     | ap_v2_structure_analysis.md               | WORKFLOW_TARGET_AUDITS/MODULES/reports/structural_reports/ |
| 4      | 2     | ap_v2_mutation_plan.md                    | WORKFLOW_TARGET_AUDITS/MODULES/reports/runtime_reports/  |
| 5      | 2     | ap_v2_mutation_results.md                 | WORKFLOW_TARGET_AUDITS/MODULES/reports/runtime_reports/  |
| 6      | 2     | ap_v2_simulation_results.md               | WORKFLOW_TARGET_AUDITS/MODULES/reports/runtime_reports/  |
| 7      | 2     | ap_v2_simulation_validation.md            | WORKFLOW_TARGET_AUDITS/MODULES/reports/runtime_reports/  |
| 8      | 2     | ap_v2_tooling_execution_report.md         | WORKFLOW_TARGET_AUDITS/MODULES/reports/runtime_reports/  |
| 9      | 2     | ap_v2_tooling_resimulation_report.md      | WORKFLOW_TARGET_AUDITS/MODULES/reports/runtime_reports/  |
| 10     | 2     | ap_v2_tooling_simulation_report.md        | WORKFLOW_TARGET_AUDITS/MODULES/reports/runtime_reports/  |
| 11     | 3     | pre_tooling_artifact_install_report.md    | WORKFLOW_TARGET_AUDITS/AUDIT_LOGS/baselines/             |
| 12     | 3     | pre_tooling_remediation_report.md         | WORKFLOW_TARGET_AUDITS/AUDIT_LOGS/baselines/             |

---

*End of Report — Audit Only — No repository mutations performed.*
