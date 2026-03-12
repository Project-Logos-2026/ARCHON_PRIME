# ARCHON_PRIME — Implementation Guide
# Repair, Validation, and Phase Control Layer

---

## Guide Identity

| Field | Value |
|---|---|
| Artifact ID | IMPL-002 |
| System | ARCHON_PRIME |
| Platform | Python 3.11 / Codespaces |
| Artifact Type | Implementation Guide |
| Version | v1 |
| Status | Final Draft |
| Authority Source | Architect |
| Source Specification | SPEC-003 v1 |
| Phase | Phase 2 — Specification Production (active) |
| DRAC Status | Deferred — not targeted by this guide |

---

## 1. Implementation Overview

This guide translates SPEC-003 into sequenced, independently executable implementation stages. It covers the Phase Gate framework, CrawlMutationRecord, Quarantine subsystem, Repair Sequencer, Repair Checkpoint Manager, Re-Audit Loop with AuditDeltaRecord, Validation Manifest, Post-Repair Boot Simulator, Severity Routing, and the three audit expansions.

The guide is written for GPT Prompt_Engineer consumption. Each stage contains exact file paths, precise implementation steps, and a testable exit gate. No stage may be skipped or reordered without Architect authorization.

**Critical prerequisite:** Stages 1–3 (Phase Gate infrastructure, CrawlMutationRecord, Quarantine) must be complete before the crawler is authorized to execute mutations against LOGOS. This is the minimum safe threshold per SPEC-003 §1 and the Claude audit findings C-001, C-002, C-003.

---

## 2. Prerequisites

| Prerequisite | Status | Notes |
|---|---|---|
| SPEC-001 modules exist | Required | All 18 modules from IMPL-001 must be scaffolded |
| IMPL-001 Stage 2 complete | Required | CIH infrastructure must be in place before new modules are added |
| `logos_analysis/sandbox/` exists | Required | Repair staging writes adjacent to this directory |
| `AUDIT_LOGS/` directory exists | Required | All artifact writers target this directory |
| `ap_config.yaml` includes new keys | Required | file_size thresholds and coverage threshold added in Stage 9 |

---

## 3. Directory Structure — New Paths

The following directories are created by this implementation pass. None existed in IMPL-001.

```
orchestration/
    phase_gates/
        __init__.py
        phase_gate_evaluator.py
        gate_configs/
            audit_to_simulation.json
            simulation_to_crawl.json
            crawl_to_repair.json
            repair_to_validated.json
    validation_manifest_evaluator.py

crawler/
    quarantine/
        __init__.py
        quarantine_manager.py
        quarantine_registry.py

repair/
    __init__.py
    repair_sequencer.py
    repair_checkpoint_manager.py
    re_audit_engine.py

simulation/
    post_repair_boot_simulator.py

tools/
    audit_tools/
        type_contract_audit.py
        dead_code_audit.py
        governance_execution_path_audit.py
        config_schema_audit.py
        test_coverage_audit.py

logos_analysis/
    repair_staging/          ← created at runtime, excluded from snapshot
    escalation/              ← subdirectory of AUDIT_LOGS/
    quarantine/              ← subdirectory of AUDIT_LOGS/
```

---

## 4. Implementation Stages

---

### Stage 1 — Phase Gate Infrastructure

**Objective:** Implement the PhaseGate artifact schema, gate configuration files, and the phase_gate_evaluator module. After this stage, pipeline_orchestrator can evaluate gate conditions before every phase transition.

**Files to create:**

| Path | Action | Description |
|---|---|---|
| `orchestration/phase_gates/__init__.py` | Create | Package init |
| `orchestration/phase_gates/gate_configs/audit_to_simulation.json` | Create | Gate config per SPEC-003 §1.4 |
| `orchestration/phase_gates/gate_configs/simulation_to_crawl.json` | Create | Strictest gate — zero Critical and Major |
| `orchestration/phase_gates/gate_configs/crawl_to_repair.json` | Create | Validates CrawlMutationRecords exist and are well-formed |
| `orchestration/phase_gates/gate_configs/repair_to_validated.json` | Create | Reads AuditDeltaRecords and ValidationManifest |
| `orchestration/phase_gates/phase_gate_evaluator.py` | Create | Core evaluator module |

**Implementation steps:**

1. Create `orchestration/phase_gates/__init__.py` as empty package init with CIH header. ARTIFACT_ID: OPS-024. FUNCTION: Phase gate package root.

2. Write the four gate configuration JSON files exactly as specified in SPEC-003 §1.4. Each file is a PhaseGate artifact with all required fields populated. Set `gate_status: "pending"` and `evaluated_at: null` in all four files at creation time.

3. Implement `phase_gate_evaluator.py` with the following structure:

```python
class PhaseGateEvaluator:

    def evaluate(self, gate_name: str) -> GateResult:
        """
        Load gate config from gate_configs/{gate_name}.json.
        Verify all required_artifacts exist in AUDIT_LOGS/.
        Count severity levels across those artifacts.
        Compare against max_severity_allowed thresholds.
        If thresholds exceeded: execute on_failure_action.
        Update gate_status in the config file.
        Return GateResult(status, blocking_findings, action_taken).
        """

    def _check_required_artifacts(self, required: list[str]) -> list[str]:
        """Return list of missing artifact types. Empty list = all present."""

    def _count_severities(self, artifact_types: list[str]) -> dict:
        """Read AUDIT_LOGS/ for named artifact types. Return severity counts."""

    def _execute_failure_action(self, gate: dict, blocking_findings: list) -> str:
        """
        halt_pipeline: write GateFailureRecord to AUDIT_LOGS/escalation/, return "halted"
        quarantine_blocking_modules: call quarantine_manager.enter() for each blocking module
        escalate_to_architect: write GateFailureRecord to escalation/, return "paused"
        retry_after_n: schedule re-evaluation after N minutes, return "retry_scheduled"
        """
```

4. Define `GateResult` dataclass:

```python
@dataclass
class GateResult:
    gate_name: str
    status: str          # "open" | "blocked" | "failed"
    blocking_findings: list[dict]
    action_taken: str | None
    evaluated_at: str    # ISO8601
```

5. Define `GateFailureRecord` dataclass and writer. Writes to `AUDIT_LOGS/escalation/gate_failure_{gate_name}_{timestamp}.json`.

6. Add CIH header to `phase_gate_evaluator.py`. ARTIFACT_ID: OPS-024. MUTATION_POLICY: NONE. GOVERNANCE_GATES: phase_transition_enforcement.

7. Modify `pipeline_orchestrator.py` to call `phase_gate_evaluator.evaluate(gate_name)` before each phase transition. If result.status is not "open", halt the transition and log the GateResult.

**Validation:**
- All four gate config files parse as valid JSON
- `phase_gate_evaluator.evaluate("Audit_to_Simulation")` returns a GateResult without raising
- Unit test: inject zero-finding audit logs → gate returns status "open"
- Unit test: inject one Critical finding → gate returns status "blocked", action_taken matches on_failure_action

**Exit gate:** `phase_gate_evaluator.evaluate()` callable from pipeline_orchestrator for all four gate names without error.

**Dependencies:** None. This stage has no dependencies on other new stages.

---

### Stage 2 — CrawlMutationRecord

**Objective:** Define the CrawlMutationRecord schema and artifact writer. Integrate intake routing into the repair system entry point. After this stage, crawler mutations produce machine-readable records that the repair system can consume.

**Files to create/modify:**

| Path | Action | Description |
|---|---|---|
| `crawler/crawl_mutation_record.py` | Create | Dataclass and writer for CrawlMutationRecord |
| `repair/repair_intake.py` | Create | Unified intake router for AuditIssueRecord and CrawlMutationRecord |

**Implementation steps:**

1. Implement `CrawlMutationRecord` as a dataclass matching the schema in SPEC-003 §2.2 exactly. All fields required. `source_audit_ids` must validate non-empty at construction time — raise `ValueError` if empty list provided.

2. Implement `CrawlMutationRecordWriter`:

```python
class CrawlMutationRecordWriter:

    def write(self, record: CrawlMutationRecord) -> Path:
        """
        Serialize record to JSON.
        Write to AUDIT_LOGS/crawl_mutations/cmr_{record_id}.json.
        If mutation_status is "partial" or "failed":
            call severity_router to write EscalationReference (severity: Critical).
        Return path written.
        """

    def _generate_record_id(self, module_path: str, timestamp: str) -> str:
        """Return CMR-{timestamp}-{sha256(module_path)[:8]}"""
```

3. Implement `repair/repair_intake.py` with routing logic from SPEC-003 §2.3:

```python
class RepairIntake:

    def ingest(self, record: AuditIssueRecord | CrawlMutationRecord) -> IntakeResult:
        """
        Dispatch by record type.
        AuditIssueRecord: route to standard repair handler by issue_type.
        CrawlMutationRecord:
            success: close linked source_audit_ids, return IntakeResult(action="closed")
            partial: call repair_checkpoint_manager.restore(), re-queue source_audit_ids
            failed + rollback_available: execute rollback, re-queue
            failed + not rollback_available: call quarantine_manager.enter()
        """
```

4. Add CIH headers to both new files. MUTATION_POLICY for CrawlMutationRecordWriter: REPORT_ONLY. MUTATION_POLICY for repair_intake: REPORT_ONLY.

**Validation:**
- `CrawlMutationRecord(source_audit_ids=[])` raises ValueError
- CrawlMutationRecord with all fields serializes to valid JSON matching SPEC-003 schema
- Unit test: ingest success record → linked audit IDs marked closed
- Unit test: ingest failed record with rollback_available=False → quarantine_manager.enter() called

**Exit gate:** `RepairIntake.ingest()` handles both record types without raising for all three mutation_status values.

**Dependencies:** Stage 3 (quarantine_manager) must exist as a stub with an `enter()` method before this stage's unit tests pass. Implement Stage 3 stub before running Stage 2 tests.

---

### Stage 3 — Quarantine Subsystem

**Objective:** Implement the full quarantine subsystem including registry, entry/exit logic, and the structured exit condition evaluator. After this stage, modules that cannot be safely mutated have a defined isolation and release path.

**Files to create:**

| Path | Action | Description |
|---|---|---|
| `crawler/quarantine/__init__.py` | Create | Package init |
| `crawler/quarantine/quarantine_registry.py` | Create | Persistent registry of all QuarantineRecords |
| `crawler/quarantine/quarantine_manager.py` | Create | Entry, evaluation, and release logic |

**Implementation steps:**

1. Implement `QuarantineRecord` dataclass matching the schema in SPEC-003 §3.2. The `exit_condition` field is a nested `ExitCondition` dataclass:

```python
@dataclass
class ExitCondition:
    condition_type: str    # "re_audit_passes" | "manual_architect_release" | "repair_category_complete"
    condition_params: ExitConditionParams

@dataclass
class ExitConditionParams:
    required_audit_types: list[str] | None
    max_severity: dict | None          # {"Critical": 0, "Major": 0}
    repair_category: str | None
```

2. Implement `quarantine_registry.py`:

```python
class QuarantineRegistry:

    REGISTRY_PATH = Path("AUDIT_LOGS/quarantine/registry.json")

    def add(self, record: QuarantineRecord) -> None:
        """Append record to registry. Never overwrite existing records."""

    def get_active(self) -> list[QuarantineRecord]:
        """Return all records where resolution_status == "pending"."""

    def get_by_module_path(self, path: str) -> list[QuarantineRecord]:

    def get_by_source_stage(self, stage: str) -> list[QuarantineRecord]:

    def update_status(self, quarantine_id: str, status: str, resolved_at: str | None) -> None:
        """Update resolution_status. Does not delete records."""
```

3. Implement `quarantine_manager.py`:

```python
class QuarantineManager:

    def enter(self, module_path: str, reason: str, source_stage: str,
              source_record_id: str, exit_condition: ExitCondition) -> QuarantineRecord:
        """
        Create QuarantineRecord with resolution_status: "pending".
        Write to quarantine_registry.
        Write QuarantineRecord JSON to AUDIT_LOGS/quarantine/.
        Return record.
        """

    def evaluate_exits(self) -> list[QuarantineRecord]:
        """
        Called by pipeline_orchestrator between cycles.
        For each active QuarantineRecord, evaluate exit_condition:
            re_audit_passes: run specified audit types, check severity thresholds
            manual_architect_release: check for release artifact in AUDIT_LOGS/architect_releases/
            repair_category_complete: check repair system completion log for this module + category
        Release modules that pass. Return list of released records.
        """

    def release(self, quarantine_id: str) -> None:
        """
        Update registry: resolution_status = "resolved", resolved_at = now.
        Write resolution event to AUDIT_LOGS/quarantine/.
        Re-queue module for its original repair category via repair_intake.
        """

    def permanent_exclusion(self, quarantine_id: str, reason: str) -> None:
        """
        Update registry: resolution_status = "permanent_exclusion".
        Write EscalationReference to AUDIT_LOGS/escalation/.
        """
```

4. Add the `quarantine_resolution` repair category handler to `repair_intake.py` (created in Stage 2). When a module exits quarantine, repair_intake re-queues it at its original repair category with crawl_cycle incremented.

5. Add CIH headers to all three files. ARTIFACT_ID: OPS-025 (quarantine_manager), OPS-026 (quarantine_registry). MUTATION_POLICY: REPORT_ONLY for both. GOVERNANCE_GATES: quarantine_entry_authorization.

**Validation:**
- QuarantineRecord with condition_type "re_audit_passes" releases when mock audit returns clean
- QuarantineRecord with condition_type "manual_architect_release" stays pending without release artifact
- `quarantine_registry.get_active()` never returns resolved records
- Records written to AUDIT_LOGS/quarantine/ are valid JSON matching SPEC-003 schema
- Unit test: permanent_exclusion writes EscalationReference to escalation/

**Exit gate:** `quarantine_manager.enter()` and `evaluate_exits()` callable without error. Registry persists across Python process restarts (reads from file on init).

**Dependencies:** Stage 1 (severity_router for EscalationReference writes — see Stage 8). Implement Stage 8 severity_router stub before running quarantine escalation path tests.

---

### Stage 4 — Repair Sequencer

**Objective:** Implement the topological sort engine for repair operations. After this stage, the repair system cannot execute operations in the wrong order or against the same module in parallel.

**Files to create/modify:**

| Path | Action | Description |
|---|---|---|
| `repair/repair_sequencer.py` | Create | Topological sort engine for RepairTasks |

**Implementation steps:**

1. Define `RepairTask` dataclass matching schema in SPEC-003 §4.3.

2. Define the canonical dependency order as a module-level constant:

```python
REPAIR_DEPENDENCY_ORDER = [
    "import_rewrite",
    "dependency_normalization",
    "module_relocation",
    "namespace_disambiguation",
    "header_injection",
    "quarantine_resolution",
]

CATEGORY_RANK = {cat: i for i, cat in enumerate(REPAIR_DEPENDENCY_ORDER)}
```

3. Implement `RepairSequencer`:

```python
class RepairSequencer:

    def sequence(self, tasks: list[RepairTask]) -> list[RepairTask]:
        """
        Step 1 — Deduplication: group tasks by module_path.
            For each module with multiple tasks, merge into single node
            with subtasks ordered by CATEGORY_RANK.
        Step 2 — Graph construction: build directed graph.
            For each task, add edge from all tasks of lower CATEGORY_RANK
            against the same module to this task.
        Step 3 — Cycle detection: if cycle detected, raise GovernanceViolation
            with category "A" (hallucinated repair state).
        Step 4 — Topological sort: return sorted task list.
            Set sequence_position on each task before returning.
        """

    def _detect_cycles(self, graph: dict) -> bool:
        """Standard DFS cycle detection. Return True if cycle present."""

    def _merge_module_tasks(self, tasks: list[RepairTask]) -> list[RepairTask]:
        """
        Group by module_path. For each group, keep one RepairTask per category.
        If duplicates exist for same module + category, merge source_record_ids.
        """
```

4. Add CIH header. ARTIFACT_ID: OPS-027. MUTATION_POLICY: NONE. CALLS: GovernanceViolation (from governance exceptions module).

**Validation:**
- Tasks for same module sorted by CATEGORY_RANK regardless of input order
- Circular dependency raises GovernanceViolation with category "A"
- Tasks for different modules interleaved correctly (all import_rewrites before any dependency_normalizations)
- Duplicate tasks for same module+category merged with combined source_record_ids
- Unit test: 6-task sequence across 2 modules returns correct topological order

**Exit gate:** `RepairSequencer.sequence()` returns deterministically ordered list for all valid input configurations.

**Dependencies:** None beyond existing GovernanceViolation exception class from SPEC-001.

---

### Stage 5 — Repair Checkpoint Manager

**Objective:** Implement per-module snapshot capability so individual repair failures can be rolled back without discarding progress on other modules.

**Files to create:**

| Path | Action | Description |
|---|---|---|
| `repair/repair_checkpoint_manager.py` | Create | Per-module pre-repair snapshot and restore |

**Implementation steps:**

1. Define `CheckpointRecord` dataclass:

```python
@dataclass
class CheckpointRecord:
    task_id: str
    module_path: str
    checkpoint_path: str     # path in logos_analysis/repair_staging/
    pre_state_hash: str      # SHA-256 of module at checkpoint time
    created_at: str          # ISO8601
    committed: bool          # True after successful repair confirmed
```

2. Implement `RepairCheckpointManager`:

```python
class RepairCheckpointManager:

    STAGING_ROOT = Path("logos_analysis/repair_staging")

    def validate_path_safety(self, path: Path) -> None:
        """
        Identical gate to header_normalizer and import_canonicalizer.
        Raise GovernanceViolation(category="C") if path is inside source_snapshot.
        """

    def write_checkpoint(self, module_path: Path) -> CheckpointRecord:
        """
        validate_path_safety(module_path).
        Compute SHA-256 of current module content.
        Copy module to STAGING_ROOT/{sha256(module_path)[:16]}/module_name.py.bak
        Write CheckpointRecord to STAGING_ROOT/{hash}/checkpoint.json.
        Return CheckpointRecord.
        """

    def commit(self, task_id: str) -> None:
        """
        Mark CheckpointRecord.committed = True.
        This signals that the repair succeeded and the checkpoint can be cleared.
        Does not delete checkpoint immediately — clear_completed handles cleanup.
        """

    def restore(self, module_path: Path) -> RestoreResult:
        """
        Load CheckpointRecord for module_path where committed == False.
        Copy .bak file back to module_path.
        Verify post-restore SHA-256 matches pre_state_hash.
        Return RestoreResult(success, verified_hash_match).
        """

    def clear_completed(self, module_path: Path) -> None:
        """Remove staging directory for module after repair cycle completes."""
```

3. Define `RestoreResult` dataclass:

```python
@dataclass
class RestoreResult:
    success: bool
    verified_hash_match: bool
    module_path: str
    restored_from: str
```

4. Add CIH header. ARTIFACT_ID: OPS-028. MUTATION_POLICY: SANDBOX_ONLY. GOVERNANCE_GATES: snapshot_path_exclusion.

5. Update `crawl_engine.py` to call `repair_checkpoint_manager.write_checkpoint()` before each mutation and update `CrawlMutationRecord.rollback_available` and `rollback_path` based on the result.

**Validation:**
- `write_checkpoint()` raises GovernanceViolation when passed source_snapshot path
- `restore()` returns `verified_hash_match: True` when checkpoint matches restored content
- `restore()` returns `verified_hash_match: False` and does not leave partial state on hash mismatch
- Unit test: write checkpoint, mutate file, restore, verify file matches original
- STAGING_ROOT never contains paths overlapping with source_snapshot

**Exit gate:** Full write → mutate → restore cycle completes with verified hash match.

**Dependencies:** Stage 2 (CrawlMutationRecord.rollback_path field populated here).

---

### Stage 6 — Re-Audit Engine and AuditDeltaRecord

**Objective:** Implement the comparison layer that determines whether a repair cycle made progress. After this stage, the pipeline can accept or retry repair cycles based on machine-evaluable evidence.

**Files to create:**

| Path | Action | Description |
|---|---|---|
| `repair/re_audit_engine.py` | Create | Post-repair audit runner and delta comparator |

**Implementation steps:**

1. Define `AuditDeltaRecord` dataclass matching schema in SPEC-003 §6.2 exactly.

2. Implement `ReAuditEngine`:

```python
class ReAuditEngine:

    def run(self, module_path: str, original_audit_types: list[str],
            crawl_cycle: int) -> AuditDeltaRecord:
        """
        Load pre_repair_issue_ids: read all AuditIssueRecords in AUDIT_LOGS/
            for this module_path from crawl_cycle - 1 (or initial audit).
        Run each audit type in original_audit_types against sandbox state.
        Collect post_repair_issue_ids from new audit output.
        Compute:
            issues_resolved = pre_repair_issue_ids - post_repair_issue_ids
            issues_introduced = post_repair_issue_ids - pre_repair_issue_ids
            net_delta = len(issues_resolved) - len(issues_introduced)
        Set cycle_verdict per SPEC-003 §6.2 rules.
        Set accept_status:
            accepted: net_delta > 0 and no new Critical in issues_introduced
            escalate: any Critical in issues_introduced
            retry: all other cases
        Write AuditDeltaRecord to AUDIT_LOGS/audit_deltas/delta_{module_hash}_{cycle}.json
        If accept_status == "escalate": write EscalationReference to AUDIT_LOGS/escalation/
        Auto-acknowledge any EscalationReferences whose primary issue appears in issues_resolved.
        Return AuditDeltaRecord.
        """

    def _auto_acknowledge_resolved(self, resolved_ids: list[str]) -> None:
        """
        Scan AUDIT_LOGS/escalation/ for EscalationReferences
        where primary_artifact_id in resolved_ids.
        Set acknowledged: True, acknowledged_at: now() for each.
        """
```

3. Add CIH header. ARTIFACT_ID: OPS-029. MUTATION_POLICY: REPORT_ONLY. CALLS: all original audit modules (dynamic dispatch by audit type name), severity_router.

4. Update `pipeline_orchestrator.py` to call `re_audit_engine.run()` after each repair cycle completes for a module.

5. Update `pipeline_orchestrator.py` to route AuditDeltaRecord outcomes:
   - `accepted` → mark module repair_complete, trigger Repair_to_Validated gate re-evaluation
   - `retry` → re-queue module in repair_sequencer with cycle incremented
   - `escalate` → call quarantine_manager.enter() with source_stage: "repair"

**Validation:**
- net_delta computed correctly for all combinations of resolved/introduced
- accept_status "escalate" fires when any Critical in issues_introduced regardless of net_delta
- `_auto_acknowledge_resolved` sets acknowledged on matching EscalationReferences
- Unit test: 3 resolved, 1 introduced non-Critical → accepted
- Unit test: 1 resolved, 1 introduced Critical → escalate
- Unit test: 0 resolved, 0 introduced → no_change, retry

**Exit gate:** `ReAuditEngine.run()` returns AuditDeltaRecord with correct accept_status for all three outcome cases.

**Dependencies:** Stage 8 (severity_router) for EscalationReference writes. Stage 3 (quarantine_manager) for escalate routing.

---

### Stage 7 — Validation Manifest and Post-Repair Boot Simulator

**Objective:** Implement the formal end-state definition and the post-repair boot chain verification. After this stage, the system can declare Validated state with machine-evaluable evidence.

**Files to create:**

| Path | Action | Description |
|---|---|---|
| `orchestration/validation_manifest_evaluator.py` | Create | Evaluates all ValidationManifest criteria |
| `simulation/post_repair_boot_simulator.py` | Create | Boot chain simulation against post-repair sandbox |

**Implementation steps:**

1. Write `AUDIT_LOGS/validation_manifest.json` as the runtime ValidationManifest instance. Initialize with all `current_state: null` and `manifest_status: "pending"`. This file is updated in place by validation_manifest_evaluator at runtime.

2. Implement `ValidationManifestEvaluator`:

```python
class ValidationManifestEvaluator:

    MANIFEST_PATH = Path("AUDIT_LOGS/validation_manifest.json")

    def evaluate(self) -> str:
        """
        Load manifest from MANIFEST_PATH.
        Set manifest_status: "evaluating", write to file.
        For each criterion in manifest.criteria:
            call the named evaluator module against sandbox
            write result to criterion.current_state or current_count
        Determine manifest_status:
            "passed" if all required criteria pass
            "failed" if any required criterion fails
        Write final manifest to file.
        Return manifest_status.
        """

    def _evaluate_criterion(self, criterion_name: str, criterion: dict) -> bool:
        """
        Dispatch to named evaluator module.
        Return True if pass_condition met, False otherwise.
        Each evaluator called with sandbox path as argument.
        """
```

3. Implement `PostRepairBootSimulator` in `simulation/post_repair_boot_simulator.py`:

```python
class PostRepairBootSimulator:

    def simulate(self, sandbox_path: Path) -> BootSimulationRecord:
        """
        Mirror runtime_boot_simulator logic targeting sandbox_path.
        Identify entry points (modules with if __name__ == "__main__" or
            registered in logos_targets.yaml as entry points).
        For each entry point:
            attempt to trace initialization sequence via AST import graph
            detect any unresolvable imports, missing modules, circular init deps
        Write BootSimulationRecord to AUDIT_LOGS/boot_simulation_post_repair_{timestamp}.json
        If boot_success is False:
            write EscalationReference to AUDIT_LOGS/escalation/
        Return BootSimulationRecord.
        """
```

4. `BootSimulationRecord` dataclass per SPEC-003 §8.2. `simulation_type` set to `"post_repair"`.

5. Add `post_repair_boot_simulator` as the evaluator for `stable_runtime_boot_chain` criterion in the ValidationManifest JSON file.

6. Add CIH headers. ValidationManifestEvaluator: ARTIFACT_ID OPS-030, MUTATION_POLICY: REPORT_ONLY. PostRepairBootSimulator: ARTIFACT_ID OPS-031, MUTATION_POLICY: NONE.

7. Update `pipeline_orchestrator.py` to call `validation_manifest_evaluator.evaluate()` before the Repair_to_Validated gate is evaluated. Gate reads ValidationManifest; evaluator must run first to populate it.

**Validation:**
- ValidationManifest with all criteria passing returns `manifest_status: "passed"`
- ValidationManifest with one failing required criterion returns `manifest_status: "failed"`
- PostRepairBootSimulator detects unresolvable import in sandbox and sets `boot_success: False`
- BootSimulationRecord written to AUDIT_LOGS with simulation_type: "post_repair"
- Unit test: mock all criteria as passing → evaluator returns "passed"
- Unit test: mock one criterion failing → evaluator returns "failed" regardless of others

**Exit gate:** `ValidationManifestEvaluator.evaluate()` returns "passed" against a clean sandbox, "failed" against a sandbox with known issues. Both BootSimulationRecord and ValidationManifest written to AUDIT_LOGS.

**Dependencies:** All audit modules named as evaluators in ValidationManifest must exist (from SPEC-001 / IMPL-001 and Stage 10 of this guide). Stage 8 (severity_router) for boot simulation escalation path.

---

### Stage 8 — Severity Routing

**Objective:** Implement the escalation reference system. After this stage, all Critical and High findings produce EscalationReferences in AUDIT_LOGS/escalation/ that block phase gate evaluation until acknowledged.

**Files to create/modify:**

| Path | Action | Description |
|---|---|---|
| `tools/core/severity_router.py` | Create | EscalationReference writer and acknowledgement manager |

**Implementation steps:**

1. Define `EscalationReference` dataclass matching schema in SPEC-003 §9.2.

2. Implement `SeverityRouter`:

```python
class SeverityRouter:

    ESCALATION_PATH = Path("AUDIT_LOGS/escalation")

    def route(self, artifact_id: str, artifact_path: str,
              severity: str, source_module: str) -> None:
        """
        Called by any module after writing an artifact with severity Critical or High.
        Create EscalationReference with acknowledged: False.
        Write to AUDIT_LOGS/escalation/esc_{artifact_id}_{timestamp}.json.
        """

    def acknowledge(self, escalation_id: str) -> None:
        """
        Set acknowledged: True, acknowledged_at: now().
        Write updated EscalationReference back to file.
        Only re_audit_engine (auto) and Architect (manual) may call this.
        Enforce caller identity via call stack inspection or explicit caller parameter.
        """

    def get_unacknowledged(self) -> list[EscalationReference]:
        """
        Read all files in AUDIT_LOGS/escalation/.
        Return those with acknowledged: False.
        Used by phase_gate_evaluator to check for blocking escalations.
        """

    def auto_acknowledge_resolved(self, resolved_issue_ids: list[str]) -> int:
        """
        Called by re_audit_engine when issues are resolved.
        Find EscalationReferences where primary_artifact_id in resolved_issue_ids.
        Call acknowledge() for each.
        Return count acknowledged.
        """
```

3. Add CIH header. ARTIFACT_ID: OPS-032. MUTATION_POLICY: REPORT_ONLY. GOVERNANCE_GATES: escalation_acknowledgement_authorization. CALLED_BY: all audit modules, crawl_engine, repair modules, phase_gate_evaluator.

4. Update `phase_gate_evaluator.py` to call `severity_router.get_unacknowledged()` at the start of every gate evaluation. If unacknowledged escalations exist from previous phases, treat each as an active Critical finding before evaluating artifact-level thresholds.

5. Update all existing audit modules that produce Critical findings to call `severity_router.route()` after writing their finding to AUDIT_LOGS. This is a retrofit to SPEC-001 modules — add to each audit module that has Critical-severity output paths.

**Validation:**
- `severity_router.route()` creates EscalationReference JSON in AUDIT_LOGS/escalation/
- `get_unacknowledged()` returns only records with acknowledged: False
- `auto_acknowledge_resolved()` correctly sets acknowledged on matching records
- Phase gate evaluation counts unacknowledged escalations as Critical findings
- Unit test: write 2 escalations, acknowledge 1, verify get_unacknowledged() returns 1

**Exit gate:** `SeverityRouter.route()` and `get_unacknowledged()` callable. Phase gate evaluator reads escalation directory before threshold evaluation.

**Dependencies:** None. This stage can be implemented before the stages that call it; stubs calling severity_router will resolve once this stage completes.

---

### Stage 9 — Configuration Updates

**Objective:** Add all new configuration keys to ap_config.yaml required by new modules. After this stage, all new modules read their thresholds from config rather than hardcoded values.

**Files to modify:**

| Path | Action | Description |
|---|---|---|
| `config/ap_config.yaml` | Modify | Add new config sections |

**Implementation steps:**

1. Add the following sections to `ap_config.yaml`:

```yaml
file_size:
  major_threshold_lines: 1500
  critical_threshold_lines: 3000

coverage:
  min_threshold: 70          # percent, per-module
  coverage_xml_path: "coverage.xml"

phase_gates:
  configs_dir: "orchestration/phase_gates/gate_configs"
  escalation_dir: "AUDIT_LOGS/escalation"

repair:
  staging_dir: "logos_analysis/repair_staging"
  max_retry_cycles: 3        # OQ-005: max re-audit retries before permanent quarantine

quarantine:
  registry_path: "AUDIT_LOGS/quarantine/registry.json"
  releases_dir: "AUDIT_LOGS/architect_releases"

validation_manifest:
  path: "AUDIT_LOGS/validation_manifest.json"

severity_routing:
  escalation_dir: "AUDIT_LOGS/escalation"
```

2. Update `packet_validator.py` to validate these new sections exist and have correct types when it validates `ap_config.yaml`.

3. Update each new module to read its configuration from `ap_config.yaml` via the existing config loader rather than hardcoded paths or values.

**Note on OQ-005:** `repair.max_retry_cycles: 3` is the default answer to OQ-005 (maximum retry cycles before permanent quarantine). This value is Architect-configurable. If the Architect specifies a different value, update this key. The re_audit_engine reads this value when determining whether to retry or permanently quarantine.

**Validation:**
- `packet_validator.py` fails on ap_config.yaml missing any new required key
- All new modules read their paths and thresholds from config, not hardcoded values
- Unit test: remove `repair.staging_dir` key, verify packet_validator returns Critical finding

**Exit gate:** `packet_validator` passes on updated ap_config.yaml. All new modules instantiate without hardcoded path constants.

**Dependencies:** All prior stages. Run this stage after scaffolding all modules so config keys can be referenced.

---

### Stage 10 — Audit Expansions

**Objective:** Implement the three new audit modules (type_contract_audit, dead_code_audit, governance_execution_path_audit) and the two minor audits (config_schema_audit, test_coverage_audit).

**Files to create:**

| Path | Action | Description |
|---|---|---|
| `tools/audit_tools/type_contract_audit.py` | Create | Function signature and return type mismatch detection |
| `tools/audit_tools/dead_code_audit.py` | Create | Unused symbol detection |
| `tools/audit_tools/governance_execution_path_audit.py` | Create | Governance gate reachability from runtime entry |
| `tools/audit_tools/config_schema_audit.py` | Create | Config file validation against schemas |
| `tools/audit_tools/test_coverage_audit.py` | Create | Coverage threshold checking |

**Implementation steps:**

1. Implement `type_contract_audit.py`:

```python
class TypeContractAudit:

    def run(self, crawl_records: list[CrawlRecord]) -> list[AuditFinding]:
        """
        For each function exported by a module:
            collect its signature (argument names, type annotations, return type)
        For each call site of that function in other modules:
            compare call argument count and types to definition
            flag mismatches as Major findings
        For each dataclass:
            collect field definitions
            scan all attribute accesses in other modules
            flag access to undefined fields as Major findings
        Return findings list.
        """
```

Finding `issue_type` values: `"signature_mismatch"`, `"return_type_conflict"`, `"dataclass_field_missing"`. All severity: Major.

2. Implement `dead_code_audit.py`:

```python
class DeadCodeAudit:

    def run(self, crawl_records: list[CrawlRecord]) -> list[AuditFinding]:
        """
        Build symbol definition map: {symbol_name: {defined_in, line, symbol_type}}
        Build call graph from all CrawlRecords.
        For each defined symbol not appearing in any call site:
            determine module classification (governance/core → Major, utility → Minor)
            skip test files entirely
            emit finding
        """
```

3. Implement `governance_execution_path_audit.py`:

```python
class GovernanceExecutionPathAudit:

    MAX_CALL_DEPTH = 50      # prevents infinite traversal in recursive codebases

    def run(self, crawl_records: list[CrawlRecord],
            entry_points: list[str],
            governance_gates: list[str]) -> list[AuditFinding]:
        """
        Build call graph from crawl_records.
        From each entry_point, perform DFS up to MAX_CALL_DEPTH.
        Collect all reachable function names.
        For each governance_gate function:
            if not in reachable set: emit Critical finding
        Return findings.
        """
```

`governance_gates` list is sourced from `governance_coverage_map` output (existing module OPS-019).

4. Implement `config_schema_audit.py`:

```python
class ConfigSchemaAudit:

    def run(self) -> list[AuditFinding]:
        """
        Load ap_config.yaml, validate against config schema.
        Load logos_targets.yaml, validate against targets schema.
        Emit Critical finding for any missing required key or type violation.
        Called by packet_validator at pipeline start.
        """
```

5. Implement `test_coverage_audit.py`:

```python
class TestCoverageAudit:

    def run(self, coverage_xml_path: Path, min_threshold: int) -> list[AuditFinding]:
        """
        Parse coverage.xml using xml.etree.ElementTree.
        For each <class> element:
            if line-rate * 100 < min_threshold: emit Minor finding
        Return findings.
        """
```

6. Add CIH headers to all five modules. ARTIFACT_IDs: OPS-033 through OPS-037. All MUTATION_POLICY: NONE.

7. Register all five new audit types in `logos_targets.yaml` audit_types list and in pipeline_orchestrator's audit dispatch table.

8. Update `ValidationManifest` criteria to reference `governance_execution_path_audit` as the evaluator for `governance_enforcement_reachable`. This replaces the placeholder left in Stage 7.

**Validation:**
- `type_contract_audit` detects argument count mismatch between definition and call site
- `dead_code_audit` correctly skips test files and classifies by module type
- `governance_execution_path_audit` flags unreachable governance gate as Critical
- `config_schema_audit` returns Critical on missing required config key
- `test_coverage_audit` parses coverage.xml and flags modules below threshold
- All five modules produce findings in standard AuditFinding format compatible with existing AUDIT_LOGS writers

**Exit gate:** All five audit modules callable with appropriate inputs and return `list[AuditFinding]` without error.

**Dependencies:** Stage 9 (config keys for coverage threshold and max_call_depth). Existing `runtime_entry_audit` output available for governance path audit entry points.

---

## 5. Integration Points

| Integration Point | Target | Method | Stage |
|---|---|---|---|
| phase_gate_evaluator → pipeline_orchestrator | pipeline_orchestrator | Called before each phase transition | 1 |
| repair_intake → quarantine_manager | quarantine_manager | Called on failed mutation with no rollback | 2, 3 |
| re_audit_engine → severity_router | severity_router | Called on escalate outcome | 6, 8 |
| validation_manifest_evaluator → all audit modules | each audit module | Dynamic dispatch by evaluator name | 7 |
| post_repair_boot_simulator → severity_router | severity_router | Called on boot_success: False | 7, 8 |
| repair_sequencer → repair_checkpoint_manager | checkpoint_manager | Called before each RepairTask | 4, 5 |
| all audit modules → severity_router | severity_router | Called on Critical/High finding write | 8, 10 |

---

## 6. Governance Enforcement Points

| Enforcement Point | Stage | Mechanism |
|---|---|---|
| Phase transition blocked without gate open | 1 | phase_gate_evaluator returns blocked; pipeline_orchestrator does not advance |
| Crawler blocked until Simulation_to_Crawl gate open | 1 | gate config: max_severity Critical: 0, Major: 0 |
| Mutation blocked from source_snapshot | 5 | repair_checkpoint_manager.validate_path_safety() raises GovernanceViolation |
| CrawlMutationRecord must have non-empty source_audit_ids | 2 | ValueError at dataclass construction |
| Escalation directory blocks phase gates | 8 | phase_gate_evaluator reads unacknowledged escalations before threshold check |
| Circular repair dependency rejected | 4 | repair_sequencer raises GovernanceViolation category "A" |
| Max retry cycles enforced before permanent quarantine | 6, 9 | re_audit_engine reads max_retry_cycles from config |

---

## 7. Error Handling

| Error Type | Cause | Response | Recovery |
|---|---|---|---|
| GovernanceViolation(category="C") | repair_checkpoint_manager path safety gate triggered | Halt mutation, write to escalation, await Architect | Architect resolves path configuration |
| GovernanceViolation(category="A") | Circular repair dependency detected by repair_sequencer | Halt repair phase, write to escalation | Architect resolves repair task graph |
| GateFailureRecord written | Phase gate threshold exceeded | Execute on_failure_action per gate config | Depends on action: halt, quarantine, escalate, retry |
| QuarantineRecord.resolution_status = "permanent_exclusion" | Module failed quarantine exit after max retries | Write EscalationReference, exclude from active targets | Manual Architect release required |
| RestoreResult.verified_hash_match = False | Checkpoint file corrupted or wrong module restored | Log error, quarantine module, halt repair for that module | Full sandbox rollback via rollback_automator |
| ValidationManifest.manifest_status = "failed" | One or more end-state criteria not met | Repair_to_Validated gate remains blocked | Another repair cycle or Architect escalation |

---

## 8. Testing Strategy

| Test | Validates | Method |
|---|---|---|
| Gate blocks on Critical threshold exceeded | FR-013 | Unit: inject Critical finding → assert gate blocked |
| Gate advances on clean audit logs | FR-013 | Unit: empty AUDIT_LOGS → assert gate open |
| CrawlMutationRecord rejects empty source_audit_ids | FR-014 | Unit: assert ValueError on construction |
| Quarantine re_audit_passes exit releases module | FR-015 | Unit: mock clean audit → assert status resolved |
| Repair tasks execute in CATEGORY_RANK order | FR-016 | Unit: submit out-of-order tasks → assert sorted output |
| Checkpoint written before every repair operation | FR-017 | Integration: run one repair cycle → assert checkpoint file exists |
| AuditDeltaRecord written after each repair cycle | FR-018 | Integration: run repair cycle → assert delta file in AUDIT_LOGS |
| ValidationManifest fails on single failing criterion | FR-019 | Unit: mock one criterion failing → assert manifest_status: failed |
| Escalation dir contains only EscalationReferences | FR-020 | Integration: trigger Critical finding → assert only reference written, no artifact copy |
| Auto-acknowledge on issue resolution | FR-021 | Unit: resolve issue in re-audit → assert EscalationReference acknowledged |
| Post-repair boot sim detects broken import chain | FR-022 | Integration: introduce broken import in sandbox → assert boot_success: False |

---

## 9. Rollback Plan

If any stage fails and leaves modules in a partially implemented state:

1. All new modules introduced in this pass are additive — they do not modify existing SPEC-001 modules except for pipeline_orchestrator.py (which receives new gate evaluation calls) and existing audit modules (which receive severity_router calls).

2. `pipeline_orchestrator.py` changes: if a stage fails after pipeline_orchestrator was modified, revert to the IMPL-001 version. The new gate calls are isolated additions — remove them cleanly without affecting the rest of orchestrator logic.

3. `ap_config.yaml` changes (Stage 9): all new keys are additive. Removing them returns the file to IMPL-001 state without side effects.

4. Staging directory `logos_analysis/repair_staging/` is created at runtime. If Stage 5 fails, delete this directory entirely with no impact on other stages.

5. Gate config JSON files are static configuration. If Stage 1 fails partially, delete `orchestration/phase_gates/gate_configs/` and recreate from SPEC-003 §1.4.

---

## 10. Post-Implementation Checklist

- [ ] All four gate config JSON files present and parse without error
- [ ] `phase_gate_evaluator.evaluate()` callable for all four gate names
- [ ] `CrawlMutationRecord` raises ValueError on empty source_audit_ids
- [ ] `quarantine_registry` persists across process restarts
- [ ] `repair_sequencer` rejects circular dependency with GovernanceViolation
- [ ] `repair_checkpoint_manager.validate_path_safety()` raises on source_snapshot path
- [ ] `AuditDeltaRecord` written for every repair cycle in integration test
- [ ] `ValidationManifest` evaluates all seven criteria
- [ ] `SeverityRouter` creates EscalationReferences for all Critical findings
- [ ] All five new audit modules return AuditFinding list without error
- [ ] `ap_config.yaml` passes packet_validator with all new keys present
- [ ] OQ-005 resolved: max_retry_cycles set in config (default 3)
- [ ] OQ-006, OQ-007, OQ-008 flagged for Architect resolution before production run

---

## 11. Open Questions (Inherited from SPEC-003)

| ID | Question | Blocking? |
|---|---|---|
| OQ-005 | Maximum re-audit retry cycles before permanent quarantine | Non-blocking — default 3 applied in Stage 9 |
| OQ-006 | Architect confirmation artifact format for escalate_to_architect action | Blocking for escalate_to_architect gate action path |
| OQ-007 | Commit repair_staging/ to git or exclude via .gitignore | Non-blocking — exclude by default, Architect can override |
| OQ-008 | Coverage threshold: per-module or system-wide aggregate | Non-blocking — per-module applied as default in Stage 9 |

---

*Artifact ID: IMPL-002 | ARCHON_PRIME | Platform: Python 3.11 / Codespaces | Version: v1 | Status: Final Draft*
