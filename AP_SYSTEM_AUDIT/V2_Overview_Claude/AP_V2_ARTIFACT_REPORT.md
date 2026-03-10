# ARCHON_PRIME — V2 Artifact Content Report

**Scope:** `AP_SYSTEM_CONFIG/CLAUDE/V2/`  
**Generated:** 2026-03-10 02:00 UTC  
**Artifacts analyzed:** 30  
**Governance:** NON-DELETION enforced — read-only scan  

---

## Directory Summary

| Metric | Value |
|---|---|
| Total artifacts | 30 |
| Markdown (`.md`) files | 24 |
| JSON (`.json`) files | 6 |
| Total directory size | 282.1 KB |
| Largest artifact | `AP_DESIGN_SPEC_SCHEMA.json` (34.5 KB) |
| Smallest artifact | `CONCEPT_ARTIFACT_SCHEMA.json` |

### Artifacts by Group

| Group | Count |
|---|---|
| Core Identity | 1 |
| Governance | 3 |
| Operational Protocols | 7 |
| Session & Handoff | 4 |
| Workflows | 2 |
| Output Formats | 2 |
| Templates | 4 |
| Schemas | 6 |
| Specifications | 1 |

---

## Directory Tree

```
AP_SYSTEM_CONFIG/CLAUDE/V2/
  [Core Identity]
    CLAUDE_SYSTEM_PROMPT.md  (8.2 KB, OPS-001)
  [Governance]
    CLAUDE_GOVERNANCE_PROTOCOL.md  (6.6 KB, GOV-001)
    CLAUDE_OPERATIONAL_CONSTRAINTS.md  (5.0 KB, CON-001)
    CLAUDE_ROLE_DEFINITION.md  (7.0 KB, ROL-001)
  [Operational Protocols]
    CLAUDE_CONCEPT_AUDIT_PROTOCOL.md  (6.4 KB, OPS-005)
    CLAUDE_DRIFT_TRIAGE_PROTOCOL.md  (12.8 KB, OPS-010)
    CLAUDE_FORMALIZATION_PROTOCOL.md  (12.4 KB, OPS-003)
    CLAUDE_MODULE_HEADER_PROTOCOL.md  (8.6 KB, OPS-008)
    CLAUDE_OUTPUT_PREFLIGHT_CHECKLIST.md  (9.7 KB, OPS-006)
    CLAUDE_RESEARCH_PROTOCOL.md  (4.7 KB, OPS-REX)
    CLAUDE_VALIDATION_REPORT_PROTOCOL.md  (11.9 KB, OPS-009)
  [Session & Handoff]
    ARCHON_PRIME_SESSION_HANDOFF.md  (5.3 KB, OPS-000)
    CLAUDE_CONCEPT_HANDOFF_FORMAT.md  (3.5 KB, FMT-002)
    CLAUDE_SESSION_INITIALIZATION.md  (11.6 KB, OPS-002)
    CLAUDE_SPEC_TO_GPT_HANDOFF_FORMAT.md  (11.1 KB, OPS-007)
  [Workflows]
    CLAUDE_CONCEPT_REFINEMENT_WORKFLOW.md  (3.9 KB, WFL-001)
    CLAUDE_PHASE_PARTICIPATION.md  (4.5 KB, OPS-004)
  [Output Formats]
    CLAUDE_FEEDBACK_REPORT_FORMAT.md  (3.8 KB, FMT-001)
    CLAUDE_RESPONSE_STYLE_GUIDE.md  (3.9 KB, STY-001)
  [Templates]
    ALGORITHM_MODEL_TEMPLATE.md  (3.7 KB, TPL-003)
    DESIGN_SPEC_TEMPLATE.md  (18.9 KB, TPL-001)
    FORMAL_MODEL_TEMPLATE.md  (3.2 KB, TPL-002)
    IMPLEMENTATION_GUIDE_TEMPLATE.md  (16.3 KB, TPL-004)
  [Schemas]
    ANALOG_DISCOVERY_SCHEMA.json  (2.5 KB, SCH-003)
    AP_DESIGN_SPEC_SCHEMA.json  (34.5 KB, SCH-001)
    AP_IMPLEMENTATION_GUIDE_SCHEMA.json  (26.7 KB, SCH-002)
    ARTIFACT_SCHEMA.json  (3.2 KB, SCH-000)
    CONCEPT_ARTIFACT_SCHEMA.json  (2.5 KB, SCH-004)
    TOOL_ENFORCEMENT_SCHEMA.json  (3.7 KB, SCH-005)
  [Specifications]
    SPEC-004_Architecture_Validator_v1.md  (25.7 KB, SPEC-004)
```

---

## Artifact Details

Each artifact is described with its identity, purpose, key features, and content snapshot.


---

### Core Identity

#### `CLAUDE_SYSTEM_PROMPT.md`

| Field | Value |
|---|---|
| **Artifact ID** | `OPS-001` |
| **Type** | System Prompt / Base Operating Instructions |
| **Group** | Core Identity |
| **Size** | 8.2 KB |
| **Lines** | 177 |
| **Extension** | `.md` |

**Purpose:** The base operating instructions and system prompt loaded at Claude session start. Defines fundamental operating mode, identity, and baseline constraints.

**Key Features:**
- 177 lines
- Artifact ID: OPS-001 — root of the operational stack
- Base identity and mode definitions
- Fundamental operating constraints
- Priority ordering of instructions
- Context loading order specification
- Override and escalation paths

**Content Snapshot:**
> ## Document Identity | Field | Value | |---|---| | Artifact ID | OPS-001 | | System | ARCHON_PRIME | | Platform | Claude | | Artifact Type | System Prompt / Base Operating Instructions | | Version | v2 | | Status | Draft | | Authority Source | Architect | | Intent | Define Claude



---

### Governance

#### `CLAUDE_OPERATIONAL_CONSTRAINTS.md`

| Field | Value |
|---|---|
| **Artifact ID** | `CON-001` |
| **Type** | Operational Constraint Specification |
| **Group** | Governance |
| **Size** | 5.0 KB |
| **Lines** | 142 |
| **Extension** | `.md` |

**Purpose:** Defines the explicit allowed actions, prohibited actions, and scope limitations for Claude across all operational modes.

**Key Features:**
- 142 lines
- Explicit allowed-action list (creation, config correction, header injection, import rewriting)
- Explicit prohibited-action list (deletion, mutation of existing files outside scope)
- Per-mode scope table
- Override escalation conditions

**Content Snapshot:**
> ## Document Identity * **System:** ARCHON_PRIME * **Platform:** Claude * **Artifact Type:** Operational Constraint Specification * **Status:** Draft v1 * **Intent:** Define the explicit allowed actions, prohibited actions, and scope limitations for Claude across all operational m


#### `CLAUDE_GOVERNANCE_PROTOCOL.md`

| Field | Value |
|---|---|
| **Artifact ID** | `GOV-001` |
| **Type** | Governance Protocol |
| **Group** | Governance |
| **Size** | 6.6 KB |
| **Lines** | 228 |
| **Extension** | `.md` |

**Purpose:** Defines the authority hierarchy, interaction rules, conflict resolution, and governance constraints binding Claude within the ARCHON_PRIME system.

**Key Features:**
- 228 lines
- Authority hierarchy definition (Architect > ARCHON_PRIME > Claude)
- Interaction rules between AI agents
- Conflict resolution decision tree
- Non-deletion policy reference
- Scope limitations on Claude autonomous operations
- Escalation triggers

**Content Snapshot:**
> ## Document Identity * **System:** ARCHON_PRIME * **Platform:** Claude * **Artifact Type:** Governance Protocol * **Status:** Draft v1 * **Intent:** Define the authority hierarchy, interaction rules, conflict resolution, and governance constraints binding Claude within the ARCHON


#### `CLAUDE_ROLE_DEFINITION.md`

| Field | Value |
|---|---|
| **Artifact ID** | `ROL-001` |
| **Type** | Role Definition Specification |
| **Group** | Governance |
| **Size** | 7.0 KB |
| **Lines** | 224 |
| **Extension** | `.md` |

**Purpose:** Authoritative definition of Claude's role structure, activation triggers, allowed actions, prohibited actions, and output expectations across all operational modes inside ARCHON_PRIME.

**Key Features:**
- 224 lines
- Role taxonomy: Formalization_Expert, Concept_Auditor, Research_Specialist, Execution_Agent
- Per-role activation triggers
- Per-role allowed and prohibited actions
- Output expectations and quality gates per role
- Cross-role interaction rules

**Content Snapshot:**
> ## Document Identity * **System:** ARCHON_PRIME * **Platform:** Claude * **Artifact Type:** Role Definition Specification * **Status:** Draft v1 * **Intent:** Define the authoritative role structure, activation triggers, allowed actions, prohibited actions, and output expectation



---

### Operational Protocols

#### `CLAUDE_FORMALIZATION_PROTOCOL.md`

| Field | Value |
|---|---|
| **Artifact ID** | `OPS-003` |
| **Type** | Operational Protocol — Formalization_Expert Mode |
| **Group** | Operational Protocols |
| **Size** | 12.4 KB |
| **Lines** | 287 |
| **Extension** | `.md` |

**Purpose:** Defines Claude's operation in Formalization_Expert mode — converting informal concepts into formal mathematical system definitions.

**Key Features:**
- 287 lines
- Formalization_Expert mode activation conditions
- Formal model structure requirements
- Mathematical notation standards
- Derivation chain documentation rules
- Algorithm model generation workflow
- Output validation against FORMAL_MODEL_TEMPLATE.md

**Content Snapshot:**
> ## Document Identity | Field | Value | |---|---| | Artifact ID | OPS-003 | | System | ARCHON_PRIME | | Platform | Claude | | Artifact Type | Operational Protocol — Formalization_Expert Mode | | Version | v2 | | Status | Draft | | Authority Source | Architect | | Schema References


#### `CLAUDE_CONCEPT_AUDIT_PROTOCOL.md`

| Field | Value |
|---|---|
| **Artifact ID** | `OPS-005` |
| **Type** | Operational Protocol — Concept_Auditor Mode |
| **Group** | Operational Protocols |
| **Size** | 6.4 KB |
| **Lines** | 197 |
| **Extension** | `.md` |

**Purpose:** Defines how Claude critiques, hardens, and refines concepts received from GPT/Architect brainstorming sessions. Activates Claude in Concept_Auditor role.

**Key Features:**
- 197 lines
- Concept_Auditor mode activation criteria
- Critique framework: feasibility, spec alignment, drift detection
- Hardening workflow steps
- Output format: structured feedback artifact
- Escalation rules for unresolvable concepts

**Content Snapshot:**
> ## Document Identity * **System:** ARCHON_PRIME * **Platform:** Claude * **Artifact Type:** Operational Protocol — Concept_Auditor Mode * **Status:** Draft v1 * **Intent:** Define how Claude critiques, hardens, and refines concepts received from GPT/Architect brainstorming sessio


#### `CLAUDE_OUTPUT_PREFLIGHT_CHECKLIST.md`

| Field | Value |
|---|---|
| **Artifact ID** | `OPS-006` |
| **Type** | Self-Verification Checklist |
| **Group** | Operational Protocols |
| **Size** | 9.7 KB |
| **Lines** | 180 |
| **Extension** | `.md` |

**Purpose:** A mandatory pre-output self-verification checklist Claude must run before emitting any artifact. Ensures governance compliance, schema conformance, and completeness.

**Key Features:**
- 180 lines
- Artifact ID: OPS-006
- Mandatory pre-output checklist (12+ checks)
- Schema compliance verification step
- Governance constraint verification step
- Spec alignment verification
- Completeness and format validation
- Signature requirement check

**Content Snapshot:**
> ## Document Identity | Field | Value | |---|---| | Artifact ID | OPS-006 | | System | ARCHON_PRIME | | Platform | Claude | | Artifact Type | Self-Verification Checklist | | Version | v1 | | Status | Draft | | Authority Source | Architect | | Schema Reference | AP_MASTER_SPEC_V2_S


#### `CLAUDE_MODULE_HEADER_PROTOCOL.md`

| Field | Value |
|---|---|
| **Artifact ID** | `OPS-008` |
| **Type** | Operational Protocol — Module Header Generation and Validation |
| **Group** | Operational Protocols |
| **Size** | 8.6 KB |
| **Lines** | 211 |
| **Extension** | `.md` |

**Purpose:** Defines the canonical module header format, required fields, and validation procedure Claude must apply to all generated Python modules.

**Key Features:**
- 211 lines
- Canonical header field taxonomy
- Required fields: module_id, subsystem, spec_ref, status
- Header injection procedure
- Validation checklist for header completeness
- Diff rules for header updates vs injection

**Content Snapshot:**
> ## Document Identity | Field | Value | |---|---| | Artifact ID | OPS-008 | | System | ARCHON_PRIME | | Platform | Claude | | Artifact Type | Operational Protocol — Module Header Generation and Validation | | Version | v1 | | Status | Draft | | Authority Source | Architect | | Sch


#### `CLAUDE_VALIDATION_REPORT_PROTOCOL.md`

| Field | Value |
|---|---|
| **Artifact ID** | `OPS-009` |
| **Type** | Operational Protocol — Architecture Validation Report Interpretation |
| **Group** | Operational Protocols |
| **Size** | 11.9 KB |
| **Lines** | 287 |
| **Extension** | `.md` |

**Purpose:** Defines how Claude interprets, processes, and acts on architecture validation reports. Governs the validation report consumption workflow.

**Key Features:**
- 287 lines
- Artifact ID: OPS-009
- Validation report taxonomy (PASS / WARN / FAIL / CRITICAL)
- Action decision tree per severity
- Remediation workflow for FAIL/CRITICAL findings
- Escalation path for unresolvable findings
- Report acknowledgement format

**Content Snapshot:**
> ## Document Identity | Field | Value | |---|---| | Artifact ID | OPS-009 | | System | ARCHON_PRIME | | Platform | Claude | | Artifact Type | Operational Protocol — Architecture Validation Report Interpretation | | Version | v1 | | Status | Draft | | Authority Source | Architect |


#### `CLAUDE_DRIFT_TRIAGE_PROTOCOL.md`

| Field | Value |
|---|---|
| **Artifact ID** | `OPS-010` |
| **Type** | Operational Protocol — Drift Triage |
| **Group** | Operational Protocols |
| **Size** | 12.8 KB |
| **Lines** | 289 |
| **Extension** | `.md` |

**Purpose:** Defines how Claude detects, classifies, and triages architectural drift. One of the largest operational protocols (289 lines).

**Key Features:**
- 289 lines — largest operational protocol
- Artifact ID: OPS-010
- Drift detection taxonomy (structural, semantic, surface-level)
- Triage decision tree
- Severity classification (CRITICAL / MAJOR / MINOR)
- Remediation assignment rules
- Escalation protocol for unresolvable drift

**Content Snapshot:**
> ## Document Identity | Field | Value | |---|---| | Artifact ID | OPS-010 | | System | ARCHON_PRIME | | Platform | Claude | | Artifact Type | Operational Protocol — Drift Triage | | Version | v1 | | Status | Draft | | Authority Source | Architect | | Extends | AI_FAILURE_PROTOCOL.


#### `CLAUDE_RESEARCH_PROTOCOL.md`

| Field | Value |
|---|---|
| **Artifact ID** | `OPS-REX` |
| **Type** | Operational Protocol — Research_Specialist Mode |
| **Group** | Operational Protocols |
| **Size** | 4.7 KB |
| **Lines** | 156 |
| **Extension** | `.md` |

**Purpose:** Defines how Claude performs analog discovery and mathematical model search in Research_Specialist mode.

**Key Features:**
- 156 lines
- Research_Specialist mode activation
- Analog discovery search procedure
- Mathematical model source taxonomy
- Scoring rubric for analog candidates
- Output format: ANALOG_DISCOVERY artifact
- Quality gate before handoff to Formalization_Expert

**Content Snapshot:**
> ## Document Identity * **System:** ARCHON_PRIME * **Platform:** Claude * **Artifact Type:** Operational Protocol — Research_Specialist Mode * **Status:** Draft v1 * **Intent:** Define how Claude performs analog discovery and mathematical model search. ---



---

### Session & Handoff

#### `CLAUDE_CONCEPT_HANDOFF_FORMAT.md`

| Field | Value |
|---|---|
| **Artifact ID** | `FMT-002` |
| **Type** | Handoff Format Specification |
| **Group** | Session & Handoff |
| **Size** | 3.5 KB |
| **Lines** | 132 |
| **Extension** | `.md` |

**Purpose:** Defines the standardized format for concept submissions from GPT/Architect to Claude. Platform: Claude (receiving) / GPT (sending).

**Key Features:**
- 132 lines
- Standard concept submission envelope
- Required metadata fields for valid handoff
- Concept body structure and type taxonomy
- Acceptance/rejection criteria for received concepts

**Content Snapshot:**
> ## Document Identity * **System:** ARCHON_PRIME * **Platform:** Claude (receiving) / GPT (sending) * **Artifact Type:** Handoff Format Specification * **Status:** Draft v1 * **Intent:** Define the standardized format for concept submissions from GPT/Architect to Claude. ---


#### `ARCHON_PRIME_SESSION_HANDOFF.md`

| Field | Value |
|---|---|
| **Artifact ID** | `OPS-000` |
| **Type** | Session Handoff Protocol |
| **Group** | Session & Handoff |
| **Size** | 5.3 KB |
| **Lines** | 245 |
| **Extension** | `.md` |

**Purpose:** Governs context transfer between AI sessions in the ARCHON_PRIME system. Ensures zero workflow loss and deterministic session initialization for all Claude instances.

**Key Features:**
- 245 lines
- Zero-loss context transfer specification
- Deterministic session initialization rules
- Handoff artifact structure definition
- Cross-session state preservation protocol

#### `CLAUDE_SESSION_INITIALIZATION.md`

| Field | Value |
|---|---|
| **Artifact ID** | `OPS-002` |
| **Type** | Session Initialization Protocol |
| **Group** | Session & Handoff |
| **Size** | 11.6 KB |
| **Lines** | 292 |
| **Extension** | `.md` |

**Purpose:** Defines the protocol Claude must execute at the start of every session to verify system state, load context, and reach operational readiness.

**Key Features:**
- 292 lines — one of the largest operational protocols
- Artifact ID: OPS-002
- Session state verification checklist
- Context loading sequence (priority-ordered)
- Handoff artifact consumption procedure
- Operational readiness gate conditions
- Failure recovery steps for incomplete context

**Content Snapshot:**
> ## Document Identity | Field | Value | |---|---| | Artifact ID | OPS-002 | | System | ARCHON_PRIME | | Platform | Claude | | Artifact Type | Session Initialization Protocol | | Version | v2 | | Status | Draft | | Authority Source | Architect | | Supersedes | CLAUDE_SESSION_INITIA


#### `CLAUDE_SPEC_TO_GPT_HANDOFF_FORMAT.md`

| Field | Value |
|---|---|
| **Artifact ID** | `OPS-007` |
| **Type** | Handoff Format Specification |
| **Group** | Session & Handoff |
| **Size** | 11.1 KB |
| **Lines** | 208 |
| **Extension** | `.md` |

**Purpose:** Defines the standardized format for Claude→GPT handoffs of validated spec artifacts. Platform: Claude → GPT.

**Key Features:**
- 208 lines
- Artifact ID: OPS-007
- Claude→GPT handoff envelope structure
- Required pre-handoff validation steps
- Artifact package manifest format
- Recipient context injection specification
- Handoff acknowledgement protocol

**Content Snapshot:**
> ## Document Identity | Field | Value | |---|---| | Artifact ID | OPS-007 | | System | ARCHON_PRIME | | Platform | Claude → GPT | | Artifact Type | Handoff Format Specification | | Version | v1 | | Status | Draft | | Authority Source | Architect | | Schema References | AP_MASTER_S



---

### Workflows

#### `CLAUDE_PHASE_PARTICIPATION.md`

| Field | Value |
|---|---|
| **Artifact ID** | `OPS-004` |
| **Type** | Phase Operations Specification |
| **Group** | Workflows |
| **Size** | 4.5 KB |
| **Lines** | 142 |
| **Extension** | `.md` |

**Purpose:** Defines how Claude participates in each project phase and what its specific responsibilities are per phase (Phase-0 through Phase-6+).

**Key Features:**
- 142 lines
- Per-phase responsibility matrix
- Phase entry criteria Claude must verify
- Phase exit deliverables Claude owns
- Mode activation mapping per phase
- Boundary conditions between phases

**Content Snapshot:**
> ## Document Identity * **System:** ARCHON_PRIME * **Platform:** Claude * **Artifact Type:** Phase Operations Specification * **Status:** Draft v1 * **Intent:** Define how Claude participates in each project phase and what its responsibilities are per phase. ---


#### `CLAUDE_CONCEPT_REFINEMENT_WORKFLOW.md`

| Field | Value |
|---|---|
| **Artifact ID** | `WFL-001` |
| **Type** | Workflow Specification |
| **Group** | Workflows |
| **Size** | 3.9 KB |
| **Lines** | 155 |
| **Extension** | `.md` |

**Purpose:** Defines the iterative refinement loop between GPT/Architect and Claude for concept hardening. Specifies loop termination conditions and escalation paths.

**Key Features:**
- 155 lines
- Iterative refinement loop specification
- Loop entry and exit conditions
- GPT→Claude→GPT feedback cycle
- Convergence criteria
- Escalation path for non-converging concepts

**Content Snapshot:**
> ## Document Identity * **System:** ARCHON_PRIME * **Platform:** Claude * **Artifact Type:** Workflow Specification * **Status:** Draft v1 * **Intent:** Define the iterative refinement loop between GPT/Architect and Claude for concept hardening. ---



---

### Output Formats

#### `CLAUDE_FEEDBACK_REPORT_FORMAT.md`

| Field | Value |
|---|---|
| **Artifact ID** | `FMT-001` |
| **Type** | Output Format Specification |
| **Group** | Output Formats |
| **Size** | 3.8 KB |
| **Lines** | 145 |
| **Extension** | `.md` |

**Purpose:** Defines the standardized structure for Claude's feedback, critique, and analysis reports. All Claude feedback outputs must conform.

**Key Features:**
- 145 lines
- Required report sections definition
- Severity labeling taxonomy
- Pass/Fail/Warning classification system
- Structured findings format
- Signature and version fields

**Content Snapshot:**
> ## Document Identity * **System:** ARCHON_PRIME * **Platform:** Claude * **Artifact Type:** Output Format Specification * **Status:** Draft v1 * **Intent:** Define the standardized structure for Claude's feedback, critique, and analysis reports. ---


#### `CLAUDE_RESPONSE_STYLE_GUIDE.md`

| Field | Value |
|---|---|
| **Artifact ID** | `STY-001` |
| **Type** | Style Guide |
| **Group** | Output Formats |
| **Size** | 3.9 KB |
| **Lines** | 133 |
| **Extension** | `.md` |

**Purpose:** Defines consistent formatting, language, and structural standards for all Claude outputs within ARCHON_PRIME.

**Key Features:**
- 133 lines
- Markdown formatting standards
- Section ordering conventions
- Prohibited language patterns
- Terminology standards
- Table and code block formatting rules

**Content Snapshot:**
> ## Document Identity * **System:** ARCHON_PRIME * **Platform:** Claude * **Artifact Type:** Style Guide * **Status:** Draft v1 * **Intent:** Define consistent formatting, language, and structural standards for all Claude outputs. ---



---

### Templates

#### `DESIGN_SPEC_TEMPLATE.md`

| Field | Value |
|---|---|
| **Artifact ID** | `TPL-001` |
| **Type** | Template — Design Specification V2 |
| **Group** | Templates |
| **Size** | 18.9 KB |
| **Lines** | 527 |
| **Extension** | `.md` |

**Purpose:** Standardized structure for all ARCHON_PRIME Design Specification documents. V2 aligned with AP_DESIGN_SPEC_SCHEMA.json.

**Key Features:**
- 527 lines — largest template
- V2, schema reference: AP_MASTER_SPEC_V2_SCHEMA.json
- Full module identity block
- Subsystem boundary definition section
- Interface surface specification
- Enhancement governance section
- Header schema definition fields
- Implementation sequencing section
- Artifact isolation rules

**Content Snapshot:**
> ## Document Identity * **System:** ARCHON_PRIME * **Platform:** Claude * **Artifact Type:** Template — Design Specification * **Version:** v2 * **Status:** Draft * **Schema Reference:** AP_MASTER_SPEC_V2_SCHEMA.json * **Supersedes:** DESIGN_SPEC_TEMPLATE.md v1 * **Intent:** Provi


#### `FORMAL_MODEL_TEMPLATE.md`

| Field | Value |
|---|---|
| **Artifact ID** | `TPL-002` |
| **Type** | Template — Formal Model |
| **Group** | Templates |
| **Size** | 3.2 KB |
| **Lines** | 130 |
| **Extension** | `.md` |

**Purpose:** Standardized structure for formal mathematical system definitions produced by Claude in Formalization_Expert mode.

**Key Features:**
- 130 lines
- Mathematical notation standards section
- State space definition block
- Transition function specification
- Invariant and property definitions
- Derivation provenance section

**Content Snapshot:**
> ## Document Identity * **System:** ARCHON_PRIME * **Platform:** Claude * **Artifact Type:** Template — Formal Model * **Status:** Draft v1 * **Intent:** Provide the standardized structure for formal mathematical system definitions produced by Claude. ---


#### `ALGORITHM_MODEL_TEMPLATE.md`

| Field | Value |
|---|---|
| **Artifact ID** | `TPL-003` |
| **Type** | Template |
| **Group** | Templates |
| **Size** | 3.7 KB |
| **Lines** | 158 |
| **Extension** | `.md` |

**Purpose:** Standardized structure for algorithmic representations derived from formal mathematical models. Produced by Claude in Formalization_Expert mode.

**Key Features:**
- Structured algorithm identity block
- Pseudocode + complexity sections
- Input/output specification schema
- Derivation chain from formal model
- Implementation notes section

**Content Snapshot:**
> ## Document Identity * **System:** ARCHON_PRIME * **Platform:** Claude * **Artifact Type:** Template — Algorithm Model * **Status:** Draft v1 * **Intent:** Provide the standardized structure for algorithmic representations derived from formal models. ---


#### `IMPLEMENTATION_GUIDE_TEMPLATE.md`

| Field | Value |
|---|---|
| **Artifact ID** | `TPL-004` |
| **Type** | Template — Implementation Guide V2 |
| **Group** | Templates |
| **Size** | 16.3 KB |
| **Lines** | 417 |
| **Extension** | `.md` |

**Purpose:** Standardized structure for ARCHON_PRIME Implementation Guide documents. V2 enforces build sequencing, header injection, and spec compliance gates.

**Key Features:**
- 417 lines
- V2 aligned with AP_IMPLEMENTATION_GUIDE_SCHEMA.json
- Deterministic build step sequencing fields
- Header injection checklist section
- Spec compliance verification checkpoints
- Analog reconciliation section
- Enhancement integration gate fields
- Architecture drift detection notes

**Content Snapshot:**
> ## Document Identity | Field | Value | |---|---| | System | ARCHON_PRIME | | Platform | Claude | | Artifact Type | Template — Implementation Guide | | Version | v2 | | Status | Draft | | Schema Reference | AP_IMPLEMENTATION_GUIDE_V2_SCHEMA.json | | Supersedes | IMPLEMENTATION_GUI



---

### Schemas

#### `ARTIFACT_SCHEMA.json`

| Field | Value |
|---|---|
| **Artifact ID** | `SCH-000` |
| **Type** | JSON Schema (draft-07) |
| **Group** | Schemas |
| **Size** | 3.2 KB |
| **Lines** | 111 |
| **Extension** | `.json` |

**Purpose:** Base-level schema that validates design specification artifacts. Required fields: spec_identity, purpose.

**Key Features:**
- Required fields: spec_identity, purpose
- Foundational schema underpinning other schemas
- Compact (111 lines) — used as a base reference

#### `AP_DESIGN_SPEC_SCHEMA.json`

| Field | Value |
|---|---|
| **Artifact ID** | `SCH-001` |
| **Type** | JSON Schema (draft-07) V2 |
| **Group** | Schemas |
| **Size** | 34.5 KB |
| **Lines** | 985 |
| **Extension** | `.json` |

**Purpose:** Master schema for all ARCHON_PRIME Design Specification artifacts. V2 closes Phase-2 architectural drift gaps. Enforces module identity, subsystem boundaries, artifact surface separation, header schema definition, enhancement governance, and implementation sequencing.

**Key Features:**
- 985 lines — most comprehensive schema in V2
- version: 2.0, authority: ARCHON_PRIME_ARCHITECT
- Self-contained (references ARTIFACT_META_SCHEMA for shared defs)
- Enforces canonical module identity + subsystem boundaries
- Enhancement governance gates
- Artifact surface separation rules
- Implementation sequencing constraints

#### `AP_IMPLEMENTATION_GUIDE_SCHEMA.json`

| Field | Value |
|---|---|
| **Artifact ID** | `SCH-002` |
| **Type** | JSON Schema (draft-07) V2 |
| **Group** | Schemas |
| **Size** | 26.7 KB |
| **Lines** | 730 |
| **Extension** | `.json` |

**Purpose:** Master schema for ARCHON_PRIME Implementation Guide artifacts. V2 enforces deterministic build sequencing, header injection, spec compliance verification, analog reconciliation, enhancement integration gates, artifact isolation, and architecture drift detection.

**Key Features:**
- 730 lines
- version: 2.0, authority: ARCHON_PRIME_ARCHITECT
- Deterministic build sequencing enforcement
- Header injection validation
- Analog reconciliation section
- Enhancement integration gates
- Architecture drift detection constraints
- Guard: valid impl guide required before code generation

#### `ANALOG_DISCOVERY_SCHEMA.json`

| Field | Value |
|---|---|
| **Artifact ID** | `SCH-003` |
| **Type** | JSON Schema (draft-07) |
| **Group** | Schemas |
| **Size** | 2.5 KB |
| **Lines** | 88 |
| **Extension** | `.json` |

**Purpose:** Validates the structure of analog candidate report artifacts produced during research/analog discovery sessions.

**Key Features:**
- Required: report_identity, concept_summary
- Analog candidate list with scoring fields
- Source attribution fields
- JSON Schema draft-07 compliant

#### `CONCEPT_ARTIFACT_SCHEMA.json`

| Field | Value |
|---|---|
| **Artifact ID** | `SCH-004` |
| **Type** | JSON Schema (draft-07) |
| **Group** | Schemas |
| **Size** | 2.5 KB |
| **Lines** | 93 |
| **Extension** | `.json` |

**Purpose:** Validates the structure of concept draft and formal concept artifacts submitted into the ARCHON_PRIME pipeline.

**Key Features:**
- 93 lines
- Required: concept_identity, concept_summary
- Concept type taxonomy field
- Formal model attachment validation
- Status field enforcement

#### `TOOL_ENFORCEMENT_SCHEMA.json`

| Field | Value |
|---|---|
| **Artifact ID** | `SCH-005` |
| **Type** | JSON Schema (draft-07) |
| **Group** | Schemas |
| **Size** | 3.7 KB |
| **Lines** | 136 |
| **Extension** | `.json` |

**Purpose:** Validates the structure of implementation guide artifacts. Required fields: guide_identity, overview.

**Key Features:**
- 136 lines
- Required: guide_identity, overview
- Tool enforcement constraint fields
- Implementation guide surface validation


---

### Specifications

#### `SPEC-004_Architecture_Validator_v1.md`

| Field | Value |
|---|---|
| **Artifact ID** | `SPEC-004` |
| **Type** | Design Specification |
| **Group** | Specifications |
| **Size** | 25.7 KB |
| **Lines** | 525 |
| **Extension** | `.md` |

**Purpose:** Full design specification for validate_architecture.py — the ARCHON_PRIME architecture validation module. One of the only completed individual module specs in the V2 directory.

**Key Features:**
- 525 lines — second largest artifact
- Artifact ID: SPEC-004
- Full module spec for validate_architecture.py
- Interface surface: inputs, outputs, error surface
- Validation algorithm description
- Test case matrix
- Implementation sequencing reference
- Schema compliance section

**Content Snapshot:**
> ## Design Specification: `validate_architecture.py` ---


---

## Operational Protocol Stack (OPS-001 → OPS-010)

Claude loads these protocols in order at session initialization:

| Load Order | Artifact ID | File | Purpose Summary |
|---|---|---|---|
| 1 | `OPS-001` | `CLAUDE_SYSTEM_PROMPT.md` | Base identity and operating instructions |
| 2 | `OPS-002` | `CLAUDE_SESSION_INITIALIZATION.md` | Session init and context loading sequence |
| 3 | `OPS-003` | `CLAUDE_FORMALIZATION_PROTOCOL.md` | Formalization_Expert mode — concept→formal model |
| 4 | `OPS-004` | `CLAUDE_PHASE_PARTICIPATION.md` | Per-phase responsibilities and boundary conditions |
| 5 | `OPS-005` | `CLAUDE_CONCEPT_AUDIT_PROTOCOL.md` | Concept_Auditor mode — critique and harden concepts |
| 6 | `OPS-006` | `CLAUDE_OUTPUT_PREFLIGHT_CHECKLIST.md` | Mandatory pre-output self-verification |
| 7 | `OPS-007` | `CLAUDE_SPEC_TO_GPT_HANDOFF_FORMAT.md` | Claude→GPT validated spec handoff format |
| 8 | `OPS-008` | `CLAUDE_MODULE_HEADER_PROTOCOL.md` | Header injection and validation for Python modules |
| 9 | `OPS-009` | `CLAUDE_VALIDATION_REPORT_PROTOCOL.md` | Validation report interpretation and action workflow |
| 10 | `OPS-010` | `CLAUDE_DRIFT_TRIAGE_PROTOCOL.md` | Drift detection, classification, and triage |

---

## Schema Hierarchy

| Schema | Validates | Size |
|---|---|---|
| `ARTIFACT_SCHEMA.json` | Base design specification artifacts | 3.2 KB |
| `CONCEPT_ARTIFACT_SCHEMA.json` | Concept draft and formal concept artifacts | 2.5 KB |
| `ANALOG_DISCOVERY_SCHEMA.json` | Analog candidate report artifacts | 2.5 KB |
| `AP_DESIGN_SPEC_SCHEMA.json` | Design Specification artifacts (V2 master) | 34.5 KB |
| `AP_IMPLEMENTATION_GUIDE_SCHEMA.json` | Implementation Guide artifacts (V2 master) | 26.7 KB |
| `TOOL_ENFORCEMENT_SCHEMA.json` | Implementation guide artifacts (enforcement) | 3.7 KB |

---

## Template Hierarchy

| Template | Artifact Type Produced | Paired Schema | Lines |
|---|---|---|---|
| `DESIGN_SPEC_TEMPLATE.md` | Design Specification | `AP_DESIGN_SPEC_SCHEMA.json` | 527 |
| `IMPLEMENTATION_GUIDE_TEMPLATE.md` | Implementation Guide | `AP_IMPLEMENTATION_GUIDE_SCHEMA.json` | 417 |
| `FORMAL_MODEL_TEMPLATE.md` | Formal Model | `CONCEPT_ARTIFACT_SCHEMA.json` | 130 |
| `ALGORITHM_MODEL_TEMPLATE.md` | Algorithm Model | `AP_DESIGN_SPEC_SCHEMA.json` | 158 |

---

*End of report. All data derived from read-only scan of `AP_SYSTEM_CONFIG/CLAUDE/V2/`. No files were modified.*
