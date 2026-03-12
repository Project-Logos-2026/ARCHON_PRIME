# SYSTEM Tree Artifact Inventory

SYSTEM: ARCHON_PRIME
REPORT_TYPE: Structural Audit — Tree Inventory
AUDIT_PASS: System Tree Structural Audit
AUDIT_DATE: 2026-03-11
AUTHORITY: Architect
STATUS: Audit Only — Repository NOT Mutated

---

## Scan Target

```
/workspaces/ARCHON_PRIME/AP_SYSTEM_CONFIG/SYSTEM
```

---

## Summary Counts

| Metric                     | Count |
|----------------------------|-------|
| Total directories scanned  | 19    |
| Total artifacts scanned    | 41    |
| Empty directories          | 5     |
| Populated directories      | 14    |

---

## Full Artifact Inventory

### SYSTEM/CONFIG/

| Artifact                            | Type | Size (bytes) | Detected Category |
|-------------------------------------|------|--------------|-------------------|
| AP_CONFIG_README.md                 | .md  | 4,410        | SYSTEM_CONFIG     |
| AP_PIPELINE_AUDIT_LOG_SCHEMA.json   | .json| 366          | VALIDATION_SCHEMA |

---

### SYSTEM/DESIGN_SPEC/

| Artifact                        | Type | Size (bytes) | Detected Category |
|---------------------------------|------|--------------|-------------------|
| MASTER_SYSTEM_DESIGN_SPEC.md    | .md  | 23,240       | SYSTEM_CONFIG     |

---

### SYSTEM/EXECUTION_CONTEXT/

| Artifact                                 | Type | Size (bytes) | Detected Category   |
|------------------------------------------|------|--------------|---------------------|
| ARTIFACT_ROUTER_CONTRACT.md              | .md  | 1,445        | EXECUTION_CONTEXT   |
| CRAWLER_ENVELOPE_INTERFACE_CONTRACT.md   | .md  | 1,710        | EXECUTION_CONTEXT   |
| EXECUTION_ENVIRONMENT.md                 | .md  | 1,453        | EXECUTION_CONTEXT   |
| PROMPT_COMPILER_INTERFACE.md             | .md  | 1,470        | EXECUTION_CONTEXT   |
| PROMPT_TO_ARTIFACT_TRACEABILITY_MAP.md   | .md  | 821          | EXECUTION_CONTEXT   |
| VS_CODE_ENVELOPE_LOADER_SPEC.md          | .md  | 709          | EXECUTION_CONTEXT   |

---

### SYSTEM/EXECUTION_ENVELOPES/DS_CONFIG/

| Artifact | Type | Size (bytes) | Detected Category |
|----------|------|--------------|-------------------|
| *(empty)*| —    | —            | —                 |

---

### SYSTEM/EXECUTION_ENVELOPES/EA_CONFIG/

| Artifact                                      | Type | Size (bytes) | Detected Category          |
|-----------------------------------------------|------|--------------|----------------------------|
| EA-001_ENVELOPE_TARGET_INTEGRITY.md           | .md  | 1,539        | EXECUTION_ENVELOPE_CONFIG  |
| EA-002_ARTIFACT_ROUTER_ENFORCEMENT.md         | .md  | 1,505        | EXECUTION_ENVELOPE_CONFIG  |
| EA-003_DETERMINISTIC_EXECUTION_ORDERING.md    | .md  | 1,427        | EXECUTION_ENVELOPE_CONFIG  |
| EA-004_SIMULATION_FIRST_RULE.md               | .md  | 1,373        | EXECUTION_ENVELOPE_CONFIG  |
| EA-005_GOVERNANCE_CONSISTENCY_CHECK.md        | .md  | 1,540        | EXECUTION_ENVELOPE_CONFIG  |
| EA-006_EXECUTION_LOGGING_REQUIREMENTS.md      | .md  | 1,495        | EXECUTION_ENVELOPE_CONFIG  |
| EA-007_ARTIFACT_METADATA_SCHEMA_ENFORCEMENT.md| .md  | 1,387        | EXECUTION_ENVELOPE_CONFIG  |
| EA-008_ENVELOPE_MANIFEST_CONTRACT.md          | .md  | 1,405        | EXECUTION_ENVELOPE_CONFIG  |
| EA-009_PROMPT_COMPILER_INTEGRATION.md         | .md  | 1,440        | EXECUTION_ENVELOPE_CONFIG  |
| EA-010_FAILURE_ROLLBACK_PROTOCOL.md           | .md  | 1,418        | EXECUTION_ENVELOPE_CONFIG  |

---

### SYSTEM/EXECUTION_ENVELOPES/EE_SCHEMAS/

> NOTE: This directory is not listed in the canonical EXECUTION_ENVELOPES subdirectory spec (DS_CONFIG, EA_CONFIG, EP_CONFIG, IG_CONFIG). It is an undocumented addition and represents a structural inconsistency.

| Artifact                          | Type  | Size (bytes) | Detected Category   |
|-----------------------------------|-------|--------------|---------------------|
| DESIGN_SPEC_SCHEMA.json           | .json | 35,349       | VALIDATION_SCHEMA   |
| EXECUTION_APPEND.json             | .json | 799          | VALIDATION_SCHEMA   |
| EXECUTION_ENVELOPE_SCHEMA.json    | .json | 1,125        | VALIDATION_SCHEMA   |
| IMPLEMENTATION_GUIDE_SCHEMA.json  | .json | 27,373       | VALIDATION_SCHEMA   |

---

### SYSTEM/EXECUTION_ENVELOPES/EP_CONFIG/

| Artifact | Type | Size (bytes) | Detected Category |
|----------|------|--------------|-------------------|
| *(empty)*| —    | —            | —                 |

---

### SYSTEM/EXECUTION_ENVELOPES/IG_CONFIG/

| Artifact | Type | Size (bytes) | Detected Category |
|----------|------|--------------|-------------------|
| *(empty)*| —    | —            | —                 |

---

### SYSTEM/EXECUTION_ENVELOPES/VALIDATION/

> NOTE: This directory is not listed in the canonical EXECUTION_ENVELOPES subdirectory spec. It is an undocumented addition alongside EE_SCHEMAS.

| Artifact                          | Type | Size (bytes) | Detected Category   |
|-----------------------------------|------|--------------|---------------------|
| ENVELOPE_VALIDATION_CLI_SPEC.md   | .md  | 956          | VALIDATION_SCHEMA   |
| VALIDATION_RULES.md               | .md  | 1,380        | VALIDATION_SCHEMA   |

---

### SYSTEM/GOVERNANCE/

| Artifact                            | Type | Size (bytes) | Detected Category |
|-------------------------------------|------|--------------|-------------------|
| AP_EXECUTION_STATE_MACHINE.md       | .md  | 639          | GOVERNANCE_RULE   |
| AP_PIPELINE_RUNTIME_CONTRACT.md     | .md  | 702          | GOVERNANCE_RULE   |

---

### SYSTEM/REPORTS/EXECUTION_LOGS/

| Artifact | Type | Size (bytes) | Detected Category |
|----------|------|--------------|-------------------|
| *(empty)*| —    | —            | —                 |

---

### SYSTEM/REPORTS/SIMULATION_RESULTS/

| Artifact | Type | Size (bytes) | Detected Category |
|----------|------|--------------|-------------------|
| *(empty)*| —    | —            | —                 |

---

### SYSTEM/REPORTS/TOOLING/

> ⚠ MISPLACED DOMAIN: These are EXECUTION_OUTPUT artifacts present inside the SYSTEM configuration tree.

| Artifact                          | Type | Size (bytes) | Detected Category  |
|-----------------------------------|------|--------------|---------------------|
| ap_v2_artifact_inventory.md       | .md  | 6,275        | EXECUTION_OUTPUT    |
| ap_v2_dependency_graph.md         | .md  | 8,008        | EXECUTION_OUTPUT    |
| ap_v2_mutation_plan.md            | .md  | 5,522        | EXECUTION_OUTPUT    |
| ap_v2_mutation_results.md         | .md  | 5,480        | EXECUTION_OUTPUT    |
| ap_v2_simulation_results.md       | .md  | 7,131        | EXECUTION_OUTPUT    |
| ap_v2_structure_analysis.md       | .md  | 7,704        | EXECUTION_OUTPUT    |

---

### SYSTEM/REPORTS/VALIDATION_RESULTS/

> ⚠ MISPLACED DOMAIN: These are EXECUTION_OUTPUT artifacts present inside the SYSTEM configuration tree.

| Artifact                              | Type | Size (bytes) | Detected Category  |
|---------------------------------------|------|--------------|---------------------|
| ap_v2_simulation_validation.md        | .md  | 7,431        | EXECUTION_OUTPUT    |
| ap_v2_tooling_execution_report.md     | .md  | 12,119       | EXECUTION_OUTPUT    |
| ap_v2_tooling_resimulation_report.md  | .md  | 16,824       | EXECUTION_OUTPUT    |
| ap_v2_tooling_simulation_report.md    | .md  | 24,165       | EXECUTION_OUTPUT    |
| pre_tooling_artifact_install_report.md| .md  | 1,900        | EXECUTION_OUTPUT    |
| pre_tooling_remediation_report.md     | .md  | 13,063       | EXECUTION_OUTPUT    |

---

### SYSTEM/SCHEMAS/

| Artifact                        | Type  | Size (bytes) | Detected Category   |
|---------------------------------|-------|--------------|---------------------|
| HEADER_POLICY_REGISTRY.json     | .json | 459          | VALIDATION_SCHEMA   |

---

### SYSTEM/WORKFLOW/

| Artifact                        | Type | Size (bytes) | Detected Category   |
|---------------------------------|------|--------------|---------------------|
| AP_PIPELINE_PHASE_MODEL.md      | .md  | 1,094        | WORKFLOW_ARTIFACT   |

---

## Artifact Category Distribution

| Category                   | Count |
|----------------------------|-------|
| SYSTEM_CONFIG              | 3     |
| EXECUTION_CONTEXT          | 6     |
| EXECUTION_ENVELOPE_CONFIG  | 10    |
| VALIDATION_SCHEMA          | 9     |
| GOVERNANCE_RULE            | 2     |
| WORKFLOW_ARTIFACT          | 1     |
| EXECUTION_OUTPUT           | 12    |
| **Total**                  | **41**|

---

## Empty Directory Registry

| Directory Path                                     | Status |
|----------------------------------------------------|--------|
| SYSTEM/EXECUTION_ENVELOPES/DS_CONFIG/              | EMPTY  |
| SYSTEM/EXECUTION_ENVELOPES/EP_CONFIG/              | EMPTY  |
| SYSTEM/EXECUTION_ENVELOPES/IG_CONFIG/              | EMPTY  |
| SYSTEM/REPORTS/EXECUTION_LOGS/                     | EMPTY  |
| SYSTEM/REPORTS/SIMULATION_RESULTS/                 | EMPTY  |

---

*End of Inventory — Audit Only — No repository mutations performed.*
