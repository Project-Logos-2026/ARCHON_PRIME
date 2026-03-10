# ARCHON_PRIME — Design Specification
# Repair, Validation, and Phase Control Layer

---

## Specification Identity

| Field | Value |
|---|---|
| Artifact ID | SPEC-003 |
| System | ARCHON_PRIME |
| Platform | Python 3.11 / Codespaces |
| Artifact Type | Design Specification |
| Version | v1 |
| Status | Final Draft |
| Authority Source | Architect |
| Source Artifacts | SPEC-001, SPEC-002, Claude Audit Report, GPT Analysis (revised) |
| Phase | Phase 2 — Specification Production (active) |
| DRAC Status | Deferred — not targeted by this spec |

---

## Purpose

This specification defines the repair, validation, and phase control layer for ARCHON_PRIME. It incorporates findings from the Claude concept audit and the GPT analysis pass, with four schema corrections applied before this document was approved. It is the authoritative design reference for the following subsystems:

- Phase Gate framework
- CrawlMutationRecord artifact
- Quarantine subsystem
- Repair Sequencer
- Repair Checkpoint Manager
- AuditDeltaRecord and Re-Audit Loop
- Validation Manifest
- Post-Repair Boot Simulation
- Severity Routing (escalation architecture)
- Supporting audit expansions (Type Contract, Dead Code, Governance Execution Path)

This specification is written for GPT Prompt_Engineer consumption. Every schema, module, and integration contract defined here is precise enough to derive VS Code implementation prompts from directly.

---

## Governance Constraints

| Constraint | Source | Effect |
|---|---|---|
| Governance-first | CLAUDE_GOVERNANCE_PROTOCOL.md §3 | Phase gates enforce before any mutation executes |
| Fail-closed | CLAUDE_GOVERNANCE_PROTOCOL.md §3 | Pipeline halts on gate failure or escalation artifact presence |
| No source_snapshot mutation | AI_FAILURE_PROTOCOL.md §1A | All mutations in sandbox only |
| Four-layer separation | CLAUDE_OPERATIONAL_CONSTRAINTS.md §7 | Reports separate conceptual / spec / integration / priority |
| Deferment obedience | CLAUDE_GOVERNANCE_PROTOCOL.md §8 | DRAC excluded from all active targets |
| Phase constraint | CLAUDE_PHASE_PARTICIPATION.md §2 | Crawler not authorized until Phase Gates C-001 and C-002 implemented |

---

## Schema Corrections Applied (Pre-Authorization)

The following four corrections were required by Claude's review of the GPT analysis before STEP 4 prompts could be authorized. They are incorporated into every schema below.

| Correction | Finding | Change Applied |
|---|---|---|
| CrawlMutationRecord | F-001 | Added `source_audit_ids[]` field |
| PhaseGate | F-002 | Added `on_failure_action` field with enum values |
| QuarantineRecord | F-003 | Changed `exit_condition` from string to structured object |
| AuditDeltaRecord | F-004 | New artifact defined for re-audit loop comparison |

---

## Section 1 — Phase Gate Framework

### 1.1 Purpose

The Phase Gate framework enforces deterministic transition conditions between ARCHON_PRIME's four operational phases. Without gates, phase advancement depends on developer judgment, which violates the governance enforcement model.

### 1.2 Phases and Gate Names

```
Phase 1: Audit
    ↓  [gate: Audit_to_Simulation]
Phase 2: Simulation
    ↓  [gate: Simulation_to_Crawl]
Phase 3: Crawl / Mutation
    ↓  [gate: Crawl_to_Repair]
Phase 4: Repair / Validation
    ↓  [gate: Repair_to_Validated]
Validated State
```

### 1.3 PhaseGate Artifact Schema

```json
{
  "gate_name": "string",
  "from_phase": "Audit | Simulation | Crawl | Repair",
  "to_phase": "Simulation | Crawl | Repair | Validated",
  "required_artifacts": ["string"],
  "max_severity_allowed": {
    "Critical": 0,
    "Major": 5,
    "Minor": null
  },
  "gate_evaluator_module": "orchestration.phase_gates.phase_gate_evaluator",
  "on_failure_action": "halt_pipeline | quarantine_blocking_modules | escalate_to_architect | retry_after_n",
  "retry_after_n": null,
  "evaluated_at": "ISO8601 timestamp | null",
  "gate_status": "pending | open | blocked | failed"
}
```

**Field definitions:**

| Field | Required | Description |
|---|---|---|
| `gate_name` | Yes | Unique identifier matching the transition name |
| `from_phase` | Yes | Phase this gate closes |
| `to_phase` | Yes | Phase this gate opens |
| `required_artifacts` | Yes | Artifact types that must exist in AUDIT_LOGS before gate evaluates |
| `max_severity_allowed` | Yes | Per-severity thresholds. null = no limit |
| `gate_evaluator_module` | Yes | Dot-path to the evaluator module |
| `on_failure_action` | Yes | What phase_gate_evaluator executes when threshold exceeded |
| `retry_after_n` | Conditional | Required when on_failure_action is retry_after_n. Integer minutes. |
| `evaluated_at` | Set at runtime | Timestamp of last evaluation |
| `gate_status` | Set at runtime | Current gate state |

**`on_failure_action` enum behavior:**

| Value | Behavior |
|---|---|
| `halt_pipeline` | pipeline_orchestrator stops all execution. Writes GateFailureRecord to AUDIT_LOGS/escalation/. Requires Architect manual restart. |
| `quarantine_blocking_modules` | Modules producing Critical findings are quarantined. Gate re-evaluates against remaining modules. |
| `escalate_to_architect` | Writes GateFailureRecord to escalation/. Pipeline pauses. Resumes on Architect confirmation artifact. |
| `retry_after_n` | Gate re-evaluates after N minutes. Fails permanently after 3 retries. |

### 1.4 Defined Gate Configurations

#### Gate: Audit_to_Simulation

```json
{
  "gate_name": "Audit_to_Simulation",
  "from_phase": "Audit",
  "to_phase": "Simulation",
  "required_artifacts": ["import_surface_audit", "circular_dependency_audit", "governance_coverage_map"],
  "max_severity_allowed": { "Critical": 0, "Major": null, "Minor": null },
  "on_failure_action": "escalate_to_architect"
}
```

#### Gate: Simulation_to_Crawl

```json
{
  "gate_name": "Simulation_to_Crawl",
  "from_phase": "Simulation",
  "to_phase": "Crawl",
  "required_artifacts": ["dependency_resolution_simulator", "import_rewrite_simulator", "runtime_boot_simulator", "mutation_dryrun_engine"],
  "max_severity_allowed": { "Critical": 0, "Major": 0, "Minor": null },
  "on_failure_action": "halt_pipeline"
}
```

**Note:** Simulation_to_Crawl is the strictest gate. Zero Critical and zero Major predicted failures are required before mutation is authorized. This is the primary safeguard for LOGOS integrity.

#### Gate: Crawl_to_Repair

```json
{
  "gate_name": "Crawl_to_Repair",
  "from_phase": "Crawl",
  "to_phase": "Repair",
  "required_artifacts": ["crawl_mutation_records"],
  "max_severity_allowed": { "Critical": null, "Major": null, "Minor": null },
  "on_failure_action": "quarantine_blocking_modules"
}
```

**Note:** Crawl_to_Repair does not block on severity counts — crawl will always produce mutation records including failures. The gate validates that CrawlMutationRecords exist and are well-formed before repair is authorized to consume them.

#### Gate: Repair_to_Validated

```json
{
  "gate_name": "Repair_to_Validated",
  "from_phase": "Repair",
  "to_phase": "Validated",
  "required_artifacts": ["audit_delta_records", "validation_manifest"],
  "max_severity_allowed": { "Critical": 0, "Major": 0, "Minor": null },
  "on_failure_action": "retry_after_n",
  "retry_after_n": 0
}
```

**Note:** retry_after_n is 0 here meaning immediate retry — the re-audit loop drives this gate, not a timer.

### 1.5 Module: phase_gate_evaluator

**Location:** `orchestration/phase_gates/phase_gate_evaluator.py`

**Function:** Reads the PhaseGate artifact for the requested transition. Counts severity levels across all required artifact types present in AUDIT_LOGS. Compares against thresholds. Executes `on_failure_action` if thresholds exceeded. Writes gate_status to the PhaseGate artifact. Returns open or blocked to pipeline_orchestrator.

**Called by:** `pipeline_orchestrator` at each phase transition attempt.

**Calls:** `AUDIT_LOGS` reader, `quarantine_manager` (if action is quarantine), `escalation_writer`.

**Must not:** Advance the phase if any required artifact is missing. A missing artifact is treated as a Critical finding for gate evaluation purposes.

---

## Section 2 — CrawlMutationRecord

### 2.1 Purpose

Bridges the crawler and repair systems. Represents a single mutation event — what was attempted, what the outcome was, and whether recovery is possible. The repair system accepts this record type alongside AuditIssueRecords.

### 2.2 CrawlMutationRecord Schema

```json
{
  "record_id": "string",
  "module_path": "string",
  "mutation_type": "import_rewrite | header_injection | module_relocation | dependency_normalization | namespace_disambiguation | quarantine_resolution",
  "source_audit_ids": ["string"],
  "pre_state_hash": "string",
  "post_state_hash": "string | null",
  "mutation_status": "success | partial | failed",
  "failure_point": "string | null",
  "failure_detail": "string | null",
  "rollback_available": "boolean",
  "rollback_path": "string | null",
  "timestamp": "ISO8601",
  "crawl_cycle": "integer"
}
```

**Field definitions:**

| Field | Required | Description |
|---|---|---|
| `record_id` | Yes | Unique ID for this mutation event. Format: CMR-{timestamp}-{hash} |
| `module_path` | Yes | Absolute path to the target module in sandbox |
| `mutation_type` | Yes | Category of mutation attempted. Enum enforced. |
| `source_audit_ids` | Yes | Array of AuditIssueIDs that triggered this mutation. Minimum one entry. Empty array is invalid. |
| `pre_state_hash` | Yes | SHA-256 of module content before mutation |
| `post_state_hash` | Conditional | SHA-256 after mutation. Null if mutation never began. |
| `mutation_status` | Yes | success: completed and verified. partial: started but incomplete. failed: did not execute or was rolled back. |
| `failure_point` | Conditional | Required when status is partial or failed. Names the operation that failed. |
| `failure_detail` | Conditional | Required when status is partial or failed. Human-readable description. |
| `rollback_available` | Yes | True if repair_checkpoint_manager has a pre-mutation snapshot available. |
| `rollback_path` | Conditional | Required when rollback_available is true. Path to the checkpoint snapshot. |
| `crawl_cycle` | Yes | Integer counter of which crawl pass this mutation belongs to. Enables re-audit loop comparison. |

### 2.3 Repair System Integration

The repair intake layer must accept both record types and route them to appropriate handlers:

```
intake(record):
    if isinstance(record, AuditIssueRecord):
        route to standard repair handler by issue_type
    if isinstance(record, CrawlMutationRecord):
        if record.mutation_status == "success":
            close linked source_audit_ids, no repair needed
        if record.mutation_status == "partial":
            route to repair_checkpoint_manager for rollback, then re-queue
        if record.mutation_status == "failed":
            if record.rollback_available:
                execute rollback, re-queue source_audit_ids for next cycle
            else:
                route to quarantine with source_stage: "crawl"
```

---

## Section 3 — Quarantine Subsystem

### 3.1 Purpose

Quarantine isolates modules that cannot be safely mutated or repaired in the current cycle. It is not a dead end — every quarantined module has a defined exit path.

### 3.2 QuarantineRecord Schema

```json
{
  "quarantine_id": "string",
  "module_path": "string",
  "reason": "string",
  "source_stage": "audit | simulation | crawl",
  "source_record_id": "string",
  "entry_timestamp": "ISO8601",
  "exit_condition": {
    "condition_type": "re_audit_passes | manual_architect_release | repair_category_complete",
    "condition_params": {
      "required_audit_types": ["string"],
      "max_severity": { "Critical": 0, "Major": 0 },
      "repair_category": "string | null"
    }
  },
  "resolution_status": "pending | resolved | permanent_exclusion",
  "resolved_at": "ISO8601 | null",
  "resolution_record_id": "string | null"
}
```

**`exit_condition.condition_type` behavior:**

| Value | Evaluator Behavior |
|---|---|
| `re_audit_passes` | quarantine_manager runs specified audit types against the module. If results are within max_severity thresholds, module is released. |
| `manual_architect_release` | Module stays quarantined until Architect writes a release artifact with matching quarantine_id. This is the escape hatch for judgment cases. |
| `repair_category_complete` | Module is released when the repair system marks the specified repair_category as complete for this module_path. |

### 3.3 Quarantine Module Structure

```
crawler/quarantine/
    __init__.py
    quarantine_manager.py     — entry, evaluation, release logic
    quarantine_registry.py    — persistent registry of all QuarantineRecords
```

**quarantine_manager.py responsibilities:**
- Accept quarantine entry requests from phase_gate_evaluator, crawl_engine, and repair intake
- Write QuarantineRecord to quarantine_registry and AUDIT_LOGS/quarantine/
- Periodically evaluate exit conditions (called by pipeline_orchestrator between cycles)
- Write resolution record when exit condition is met
- Update QuarantineRecord.resolution_status

**quarantine_registry.py responsibilities:**
- Maintain the canonical list of all active and resolved QuarantineRecords
- Provide query interface: get_active(), get_by_module_path(), get_by_source_stage()
- Never delete records — resolved records are retained for traceability

### 3.4 Repair Category: quarantine_resolution

A new repair category is added to the repair system to handle quarantine exit:

```
quarantine_resolution:
    trigger: quarantine exit_condition met
    action: re-queue module for its original repair category
    on_success: update QuarantineRecord.resolution_status to resolved
    on_failure: update to permanent_exclusion, write to AUDIT_LOGS/escalation/
```

---

## Section 4 — Repair Sequencer

### 4.1 Purpose

The repair system has five categories that must execute in a strict dependency order. The repair_sequencer topologically sorts all pending repair operations before any execution begins. Executing repairs in the wrong order or in parallel causes compounding failures.

### 4.2 Required Execution Order

```
1. import_rewrite
       ↓  (imports must be clean before dependency analysis is accurate)
2. dependency_normalization
       ↓  (dependency graph must be clean before module moves are safe)
3. module_relocation
       ↓  (modules must be in final locations before namespace is evaluated)
4. namespace_disambiguation
       ↓  (namespace clean before header contracts are finalized)
5. header_injection
       ↓
6. quarantine_resolution   (always last — re-queues to prior categories)
```

### 4.3 RepairTask Schema

```json
{
  "task_id": "string",
  "module_path": "string",
  "repair_category": "import_rewrite | dependency_normalization | module_relocation | namespace_disambiguation | header_injection | quarantine_resolution",
  "source_record_ids": ["string"],
  "dependencies": ["task_id"],
  "sequence_position": "integer",
  "status": "pending | in_progress | complete | failed | skipped",
  "assigned_cycle": "integer"
}
```

### 4.4 Module: repair_sequencer

**Location:** `repair/repair_sequencer.py`

**Function:** Accepts a list of RepairTasks. Builds a directed acyclic graph where edges represent the dependency order in Section 4.2. Runs topological sort. Returns an ordered execution queue. Detects and rejects circular repair dependencies (which would indicate a Category A governance failure — hallucinated repair state).

**Deduplication:** Before building the graph, repair_sequencer groups all tasks by module_path. Multiple tasks against the same module are merged into a single node with ordered subtasks. This resolves the m-004 multi-audit deduplication gap.

**Called by:** `pipeline_orchestrator` at the start of Repair phase, after Crawl_to_Repair gate opens.

---

## Section 5 — Repair Checkpoint Manager

### 5.1 Purpose

Provides single-module recovery without requiring full sandbox rollback. The rollback_automator in SPEC-001 restores the entire sandbox. The repair_checkpoint_manager targets individual modules, preserving progress on modules that repaired successfully.

### 5.2 Checkpoint Workflow

```
repair_sequencer emits next RepairTask
        ↓
repair_checkpoint_manager.write_checkpoint(module_path)
        ↓
repair handler executes mutation
        ↓
if success:
    repair_checkpoint_manager.commit(task_id)
    update CrawlMutationRecord.mutation_status = success
        ↓
if partial or failed:
    repair_checkpoint_manager.restore(module_path)
    update CrawlMutationRecord.mutation_status = failed, rollback_available = false
    re-queue or quarantine per repair intake logic
```

### 5.3 Checkpoint Storage

**Location:** `logos_analysis/repair_staging/{module_path_hash}/`

This is a separate directory from sandbox. It is not the source_snapshot. It is a per-module pre-repair snapshot. It is cleared when the module's repair cycle completes successfully.

**Must not** write to source_snapshot. Path safety validation identical to header_normalizer and import_canonicalizer entry gates.

### 5.4 Module: repair_checkpoint_manager

**Location:** `repair/repair_checkpoint_manager.py`

**Public methods:**
```python
def write_checkpoint(self, module_path: Path) -> CheckpointRecord
def commit(self, task_id: str) -> None
def restore(self, module_path: Path) -> RestoreResult
def validate_path_safety(self, path: Path) -> None  # raises GovernanceViolation if snapshot path
def clear_completed(self, module_path: Path) -> None
```

---

## Section 6 — AuditDeltaRecord and Re-Audit Loop

### 6.1 Purpose

After repair executes, the system must re-audit to verify repair succeeded and did not introduce new issues. The AuditDeltaRecord is the comparison artifact that makes this determination machine-evaluable and traceable.

### 6.2 AuditDeltaRecord Schema

```json
{
  "delta_id": "string",
  "module_path": "string",
  "crawl_cycle": "integer",
  "pre_repair_issue_ids": ["string"],
  "post_repair_issue_ids": ["string"],
  "issues_resolved": ["string"],
  "issues_introduced": ["string"],
  "net_delta": "integer",
  "cycle_verdict": "progress | regression | no_change",
  "accept_status": "accepted | retry | escalate",
  "timestamp": "ISO8601"
}
```

**Field definitions:**

| Field | Description |
|---|---|
| `pre_repair_issue_ids` | AuditIssueIDs present before this repair cycle for this module |
| `post_repair_issue_ids` | AuditIssueIDs present after re-audit for this module |
| `issues_resolved` | IDs present in pre but not post |
| `issues_introduced` | IDs present in post but not pre |
| `net_delta` | len(issues_resolved) - len(issues_introduced). Positive = progress. |
| `cycle_verdict` | progress: net_delta > 0. regression: net_delta < 0. no_change: net_delta == 0. |
| `accept_status` | accepted: net_delta > 0 and no new Critical issues. retry: regression or no_change. escalate: new Critical introduced. |

### 6.3 Re-Audit Loop Flow

```
Repair phase completes for a module
        ↓
re_audit_engine runs the same audit types that originally flagged this module
        ↓
AuditDeltaRecord written comparing pre and post issue sets
        ↓
if accept_status == "accepted":
    module marked repair_complete
    Repair_to_Validated gate re-evaluates
        ↓
if accept_status == "retry":
    module re-queued in repair_sequencer for next cycle
    crawl_cycle incremented
        ↓
if accept_status == "escalate":
    module quarantined with source_stage: "repair"
    CrawlMutationRecord written with mutation_status: failed
    AuditDeltaRecord written to AUDIT_LOGS/escalation/
```

### 6.4 Module: re_audit_engine

**Location:** `repair/re_audit_engine.py`

**Function:** Accepts a module_path and the list of audit types that originally flagged it. Re-runs those audits against the post-repair sandbox state. Collects new issue IDs. Writes AuditDeltaRecord. Returns accept_status to pipeline_orchestrator.

**Called by:** `pipeline_orchestrator` after each repair cycle completes.

---

## Section 7 — Validation Manifest

### 7.1 Purpose

Defines the formal machine-evaluable end state that ARCHON_PRIME must reach before the Validated phase is declared. Without this, the system cannot programmatically determine whether it has succeeded.

### 7.2 ValidationManifest Schema

```json
{
  "manifest_id": "string",
  "target_repository": "string",
  "evaluated_at": "ISO8601 | null",
  "manifest_status": "pending | evaluating | passed | failed",
  "criteria": {
    "normalized_imports": {
      "required": true,
      "current_state": "boolean | null",
      "evaluator": "import_surface_audit",
      "pass_condition": "zero Critical findings"
    },
    "circular_dependencies": {
      "required": true,
      "current_count": "integer | null",
      "pass_condition": 0,
      "evaluator": "circular_dependency_audit"
    },
    "namespace_collisions": {
      "required": true,
      "current_count": "integer | null",
      "pass_condition": 0,
      "evaluator": "symbol_collision_audit"
    },
    "governance_enforcement_reachable": {
      "required": true,
      "current_state": "boolean | null",
      "evaluator": "governance_execution_path_audit",
      "pass_condition": "all governance gates reachable from runtime entry points"
    },
    "consistent_module_headers": {
      "required": true,
      "current_state": "boolean | null",
      "evaluator": "header_schema_audit",
      "pass_condition": "zero Critical findings"
    },
    "stable_runtime_boot_chain": {
      "required": true,
      "current_state": "boolean | null",
      "evaluator": "post_repair_boot_simulation",
      "pass_condition": "boot simulation exits without failure"
    },
    "deterministic_repo_structure": {
      "required": true,
      "current_state": "boolean | null",
      "evaluator": "module_path_ambiguity_audit",
      "pass_condition": "zero Critical findings"
    }
  }
}
```

### 7.3 Module: validation_manifest_evaluator

**Location:** `orchestration/validation_manifest_evaluator.py`

**Function:** Reads the ValidationManifest. For each criterion, calls the named evaluator module against the current sandbox state. Writes the result into the criterion's current_state/current_count field. Sets manifest_status. Returns passed or failed to pipeline_orchestrator for Repair_to_Validated gate evaluation.

---

## Section 8 — Post-Repair Boot Simulation

### 8.1 Purpose

The existing `runtime_boot_simulator` tests the pre-mutation boot chain. The `post_repair_boot_simulation` runs the equivalent test against the post-repair sandbox state. It is the final verification before the Validated phase is declared.

### 8.2 Module: post_repair_boot_simulator

**Location:** `simulation/post_repair_boot_simulator.py`

**Function:** Mirrors runtime_boot_simulator's logic but targets logos_analysis/sandbox/ after all repair cycles have completed. Attempts to trace the module initialization sequence. Reports any boot chain failures as Critical findings. Writes a BootSimulationRecord to AUDIT_LOGS/.

**Called by:** `validation_manifest_evaluator` as the evaluator for `stable_runtime_boot_chain`.

**BootSimulationRecord schema:**
```json
{
  "simulation_id": "string",
  "simulation_type": "pre_mutation | post_repair",
  "target_path": "string",
  "entry_points_tested": ["string"],
  "boot_success": "boolean",
  "failure_point": "string | null",
  "failure_detail": "string | null",
  "timestamp": "ISO8601"
}
```

---

## Section 9 — Severity Routing

### 9.1 Architecture Decision

Claude's review (F-005) identified that artifact duplication in the escalation directory creates stale-artifact risk. The resolution adopted here is the **reference model**: the escalation directory contains EscalationReference artifacts that point to primary artifacts by ID. It does not contain copies.

### 9.2 EscalationReference Schema

```json
{
  "escalation_id": "string",
  "primary_artifact_id": "string",
  "primary_artifact_path": "string",
  "severity": "Critical | High",
  "source_module": "string",
  "escalation_timestamp": "ISO8601",
  "acknowledged": "boolean",
  "acknowledged_at": "ISO8601 | null"
}
```

### 9.3 Routing Logic

```
Any module writes an artifact with severity Critical or High:
        ↓
severity_router (called by all audit/crawl/repair modules post-write)
        ↓
writes EscalationReference to AUDIT_LOGS/escalation/
        ↓
pipeline_orchestrator checks AUDIT_LOGS/escalation/ before each phase transition
        ↓
if unacknowledged EscalationReferences exist:
    phase_gate_evaluator treats them as active Critical findings
        ↓
Architect acknowledges by setting acknowledged: true and acknowledged_at
    (or via GitHub Issue closure if integrated)
```

### 9.4 Stale-Reference Prevention

The primary artifact is the source of truth. If a finding is resolved (removed from primary audit output in a re-audit), severity_router marks the corresponding EscalationReference.acknowledged = true automatically when re_audit_engine writes a clean AuditDeltaRecord for that issue_id.

---

## Section 10 — Audit Expansions

### 10.1 type_contract_audit

**Location:** `tools/audit_tools/type_contract_audit.py`

**Purpose:** Detects function signature drift, return type mismatches, and dataclass contract drift across module boundaries. These failures are invisible to import and dependency audits.

**Method:** AST parsing of all module exports. Cross-reference against call sites within crawl scope. Flag argument count mismatches, type annotation conflicts, and dataclass field access against non-existent fields.

**Output fields (per finding):**
```json
{
  "id": "string",
  "file": "string",
  "line": "integer",
  "issue_type": "signature_mismatch | return_type_conflict | dataclass_field_missing",
  "defined_in": "string",
  "called_from": "string",
  "expected_signature": "string",
  "actual_call": "string",
  "severity": "Major"
}
```

### 10.2 dead_code_audit

**Location:** `tools/audit_tools/dead_code_audit.py`

**Purpose:** Identifies defined symbols (functions, methods, classes) with no call sites within the crawl scope.

**Severity rules:**

| Context | Severity |
|---|---|
| Governance or core modules | Major |
| Utility or helper modules | Minor |
| Test files | Not reported |

**Note:** Dead code in governance modules is Major because an enforcement point that is defined but never called is not enforced at runtime — this overlaps with and reinforces `governance_execution_path_audit`.

### 10.3 governance_execution_path_audit

**Location:** `tools/audit_tools/governance_execution_path_audit.py`

**Purpose:** Verifies that governance enforcement points in the code are reachable from runtime entry points. Governance checks that exist in unreachable functions are not enforced.

**Method:**
1. `runtime_entry_audit` provides the list of entry point functions
2. Build a call graph from each entry point (depth-limited to prevent infinite traversal)
3. Collect all reachable function names
4. Cross-reference against governance enforcement points identified by `governance_coverage_map`
5. Flag governance points not present in reachable set as Critical findings

**Output fields (per finding):**
```json
{
  "id": "string",
  "file": "string",
  "line": "integer",
  "issue_type": "unreachable_governance_gate",
  "gate_function": "string",
  "nearest_entry_point": "string | null",
  "reachability_distance": "null",
  "severity": "Critical"
}
```

### 10.4 Minor Audit Completions

#### config_schema_audit

**Location:** `tools/audit_tools/config_schema_audit.py`

Validates `ap_config.yaml` and `logos_targets.yaml` against their JSON schemas before pipeline execution. Findings written to AUDIT_LOGS before phase gates evaluate. Missing or invalid config is a Critical finding.

#### test_coverage_audit

**Location:** `tools/audit_tools/test_coverage_audit.py`

Reads `coverage.xml` produced by pytest. Flags modules below coverage threshold as Minor findings. Threshold defined in `ap_config.yaml` under `coverage.min_threshold` (default: 70).

#### file_size_thresholds

Applied in existing `file_size_audit`. Add threshold configuration to `ap_config.yaml`:

```yaml
file_size:
  major_threshold_lines: 1500
  critical_threshold_lines: 3000
```

---

## Section 11 — Functional Requirements

| ID | Requirement | Module | Testable |
|---|---|---|---|
| FR-013 | Phase transitions require gate evaluation; no phase advance without gate open | phase_gate_evaluator | Yes |
| FR-014 | CrawlMutationRecord.source_audit_ids must be non-empty for all mutation records | crawl_engine | Yes |
| FR-015 | Quarantine exit conditions are machine-evaluable for all condition_types except manual_architect_release | quarantine_manager | Yes |
| FR-016 | Repair operations execute in topologically sorted order per Section 4.2 | repair_sequencer | Yes |
| FR-017 | repair_checkpoint_manager writes checkpoint before every repair operation | repair_checkpoint_manager | Yes |
| FR-018 | AuditDeltaRecord written for every module after each repair cycle | re_audit_engine | Yes |
| FR-019 | ValidationManifest evaluates all seven criteria before Validated state is declared | validation_manifest_evaluator | Yes |
| FR-020 | Escalation directory contains only EscalationReferences, never artifact copies | severity_router | Yes |
| FR-021 | EscalationReferences auto-acknowledged when linked issue resolved in re-audit | re_audit_engine + severity_router | Yes |
| FR-022 | post_repair_boot_simulator runs against sandbox after all repair cycles complete | post_repair_boot_simulator | Yes |

---

## Section 12 — Constraints

| ID | Constraint | Rationale |
|---|---|---|
| C-009 | Crawler may not execute mutations until Simulation_to_Crawl gate is open | Safety — zero predicted failures required before mutation |
| C-010 | CrawlMutationRecord.source_audit_ids must reference existing AuditIssueIDs | Traceability — mutations must be traceable to audit findings |
| C-011 | repair_staging/ must never write to source_snapshot/ | Safety — identical to sandbox mutation constraint |
| C-012 | Repair operations must not execute in parallel on the same module | Safety — sequencer enforces single-module serial execution |
| C-013 | ValidationManifest criteria evaluators must be the same audit modules used in Audit phase | Consistency — validated state uses same measurement as initial state |
| C-014 | EscalationReference.acknowledged must not be set to true by any module other than re_audit_engine (auto) or Architect (manual) | Governance — escalation acknowledgement is an authority-level action |

---

## Section 13 — Verification Criteria

| ID | Criterion | Method |
|---|---|---|
| V-009 | Phase gate blocks transition when Critical findings exceed threshold | Unit test: inject Critical finding, assert gate returns blocked |
| V-010 | on_failure_action halt_pipeline causes pipeline_orchestrator to stop | Unit test: configure gate with halt, trigger failure, assert no further stage executes |
| V-011 | CrawlMutationRecord with empty source_audit_ids is rejected at intake | Unit test: submit record with source_audit_ids: [], assert validation error |
| V-012 | Quarantine exit condition re_audit_passes releases module when audit clean | Unit test: quarantine module, mock clean re-audit, assert resolution_status: resolved |
| V-013 | repair_sequencer rejects circular repair dependencies | Unit test: create circular RepairTask graph, assert rejection |
| V-014 | repair_checkpoint_manager raises GovernanceViolation on snapshot path | Unit test: pass source_snapshot path, assert exception |
| V-015 | AuditDeltaRecord net_delta correctly computed for mixed resolution/introduction | Unit test: 3 resolved, 1 introduced → net_delta: 2, verdict: progress |
| V-016 | ValidationManifest fails when any single criterion is not met | Unit test: set one criterion to failing state, assert manifest_status: failed |
| V-017 | EscalationReference auto-acknowledged when issue resolved in re-audit | Integration test: resolve issue, run re_audit_engine, assert acknowledged: true |
| V-018 | post_repair_boot_simulator detects broken boot chain in mutated sandbox | Integration test: introduce boot failure in sandbox, assert simulation reports it |

---

## Section 14 — Open Questions for Architect Resolution

| ID | Question | Impact if Unresolved |
|---|---|---|
| OQ-005 | What is the maximum number of re-audit retry cycles before a module is permanently quarantined? | Without a limit, the re-audit loop could cycle indefinitely on pathological modules |
| OQ-006 | Should the Architect confirmation artifact for escalate_to_architect gate action be a GitHub Issue closure, a file written to the repo, or a separate CLI command? | Affects how quarantine_manager and phase_gate_evaluator detect Architect authorization |
| OQ-007 | Should repair_staging/ be committed to git or excluded via .gitignore? | Committed: provides recovery point across sessions. Excluded: prevents large intermediate state from bloating repo. |
| OQ-008 | Is the coverage threshold for test_coverage_audit a per-module threshold or a system-wide aggregate? | Per-module is stricter and more targeted; aggregate allows critical modules to be under-covered if utilities are high |

---

*Artifact ID: SPEC-003 | ARCHON_PRIME | Platform: Python 3.11 / Codespaces | Version: v1 | Status: Final Draft*
