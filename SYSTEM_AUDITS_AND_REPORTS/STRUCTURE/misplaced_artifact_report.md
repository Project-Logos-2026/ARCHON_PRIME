# Misplaced Artifact Report

SYSTEM: ARCHON_PRIME
REPORT_TYPE: Structural Audit — Misplaced Artifact Detection
AUDIT_PASS: System Tree Structural Audit
AUDIT_DATE: 2026-03-11
AUTHORITY: Architect
STATUS: Audit Only — Repository NOT Mutated

---

## Summary

| Metric                          | Count |
|---------------------------------|-------|
| Total artifacts analyzed        | 41    |
| Correctly placed artifacts      | 29    |
| Misplaced artifacts detected    | 12    |
| Misplacement categories         | 1 (EXECUTION_OUTPUT in SYSTEM config tree) |

---

## Domain Classification Framework

Artifacts in the SYSTEM tree must belong to one of the following domains:

| Domain                     | Description                                                      |
|----------------------------|------------------------------------------------------------------|
| SYSTEM_CONFIG              | Core configuration for the ARCHON_PRIME system itself            |
| EXECUTION_CONTEXT          | Interface contracts and context specifications                   |
| EXECUTION_ENVELOPE_CONFIG  | Execution attribute rules and enforcement definitions            |
| VALIDATION_SCHEMA          | JSON schemas and validation rule specifications                  |
| GOVERNANCE_RULE            | Pipeline governance contracts and execution state definitions     |
| WORKFLOW_ARTIFACT          | System-level pipeline phase models                               |

The following domain is **NOT permitted** within SYSTEM:

| Disallowed Domain    | Reason                                                              |
|----------------------|---------------------------------------------------------------------|
| EXECUTION_OUTPUT     | Output artifacts produced by workflow execution belong in workflow execution surfaces, not in system configuration |

---

## Misplaced Artifact Registry

### Group 1 — SYSTEM/REPORTS/TOOLING/ (6 artifacts)

All six artifacts are workflow execution outputs produced by the AP V2 tooling run.
They document the results of tooling analysis passes against a target repository.
They are NOT configuration artifacts and MUST NOT reside in the SYSTEM config tree.

| # | Artifact                          | Detected Domain    | Correct Domain      |
|---|-----------------------------------|--------------------|---------------------|
| 1 | ap_v2_artifact_inventory.md       | EXECUTION_OUTPUT   | Workflow Audit Surface |
| 2 | ap_v2_dependency_graph.md         | EXECUTION_OUTPUT   | Workflow Audit Surface |
| 3 | ap_v2_mutation_plan.md            | EXECUTION_OUTPUT   | Workflow Audit Surface |
| 4 | ap_v2_mutation_results.md         | EXECUTION_OUTPUT   | Workflow Audit Surface |
| 5 | ap_v2_simulation_results.md       | EXECUTION_OUTPUT   | Workflow Audit Surface |
| 6 | ap_v2_structure_analysis.md       | EXECUTION_OUTPUT   | Workflow Audit Surface |

**Misplacement Rationale:**
These artifacts were produced by running the AP V2 tooling mutation pass against a workflow target. Their filenames (`ap_v2_*`) encode a workflow pass prefix and version tag. They describe results — dependency graphs, mutation results, simulation outputs — none of which constitute system configuration. Their presence in SYSTEM/REPORTS/TOOLING/ conflates execution output with system configuration, violating the separation of concerns mandated by the ARCHON_PRIME architecture.

---

### Group 2 — SYSTEM/REPORTS/VALIDATION_RESULTS/ (6 artifacts)

All six artifacts are execution validation and simulation reports from workflow passes.
They document pre-tooling states, simulation runs, and execution outcomes.
They are NOT configuration artifacts and MUST NOT reside in the SYSTEM config tree.

| # | Artifact                              | Detected Domain    | Correct Domain      |
|---|---------------------------------------|--------------------|---------------------|
| 7 | ap_v2_simulation_validation.md        | EXECUTION_OUTPUT   | Workflow Audit Surface |
| 8 | ap_v2_tooling_execution_report.md     | EXECUTION_OUTPUT   | Workflow Audit Surface |
| 9 | ap_v2_tooling_resimulation_report.md  | EXECUTION_OUTPUT   | Workflow Audit Surface |
|10 | ap_v2_tooling_simulation_report.md    | EXECUTION_OUTPUT   | Workflow Audit Surface |
|11 | pre_tooling_artifact_install_report.md| EXECUTION_OUTPUT   | Workflow Audit Surface |
|12 | pre_tooling_remediation_report.md     | EXECUTION_OUTPUT   | Workflow Audit Surface |

**Misplacement Rationale:**
The `pre_tooling_*` artifacts represent a pre-execution baseline snapshot produced before the AP V2 tooling pass. The `ap_v2_tooling_*` artifacts represent execution validation reports. Neither type constitutes system configuration. Their namespace prefix (`ap_v2_tooling_`, `pre_tooling_`) are execution-phase identifiers, not system component identifiers.

---

## Structural Anomaly — The REPORTS Directory Itself

The REPORTS directory and its subdirectory structure within SYSTEM constitutes a structural violation:

```
SYSTEM/REPORTS/
├── EXECUTION_LOGS/       ← empty — intended for live execution logs
├── SIMULATION_RESULTS/   ← empty — intended for simulation output
├── TOOLING/              ← contains 6 execution output files
└── VALIDATION_RESULTS/   ← contains 6 execution output files
```

The presence of subdirectories named `EXECUTION_LOGS/` and `SIMULATION_RESULTS/` inside SYSTEM confirms that this directory was originally scaffolded to accumulate runtime execution outputs during workflow passes. This architectural intent is incompatible with the SYSTEM tree's role as a static system configuration store.

**The entire REPORTS directory tree must be relocated.**

---

## Correctly Placed Artifact Confirmation

The following artifact groups are correctly classified and correctly placed within SYSTEM:

| Directory                             | Artifact Count | Domain                     |
|---------------------------------------|----------------|----------------------------|
| SYSTEM/CONFIG/                        | 2              | SYSTEM_CONFIG, VALIDATION_SCHEMA |
| SYSTEM/DESIGN_SPEC/                   | 1              | SYSTEM_CONFIG              |
| SYSTEM/EXECUTION_CONTEXT/             | 6              | EXECUTION_CONTEXT          |
| SYSTEM/EXECUTION_ENVELOPES/EA_CONFIG/ | 10             | EXECUTION_ENVELOPE_CONFIG  |
| SYSTEM/EXECUTION_ENVELOPES/EE_SCHEMAS/| 4              | VALIDATION_SCHEMA          |
| SYSTEM/EXECUTION_ENVELOPES/VALIDATION/| 2              | VALIDATION_SCHEMA          |
| SYSTEM/GOVERNANCE/                    | 2              | GOVERNANCE_RULE            |
| SYSTEM/SCHEMAS/                       | 1              | VALIDATION_SCHEMA          |
| SYSTEM/WORKFLOW/                      | 1              | WORKFLOW_ARTIFACT          |

---

*End of Report — Audit Only — No repository mutations performed.*
