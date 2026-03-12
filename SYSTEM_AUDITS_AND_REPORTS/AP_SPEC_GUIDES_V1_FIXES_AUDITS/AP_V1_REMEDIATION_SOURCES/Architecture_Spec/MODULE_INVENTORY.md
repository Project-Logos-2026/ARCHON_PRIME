# ARCHON_PRIME — COMPLETE MODULE INVENTORY
**Deliverable 3** | Version 1.0.0 | 2026-03-08 | AUTHORITATIVE

---

## MODULE REGISTRY — ALL SUBSYSTEMS

Grouped by subsystem. Each module fully specified: path, purpose, inputs, outputs, dependencies,
blocking/supporting classification, and crawl phase.

Legend:
- **Phase:** `PRE` = pre-crawl | `IN` = in-crawl | `POST` = post-crawl | `FOUND` = foundation (built first, not run as part of crawl)
- **Class:** `BLOCKING` = crawl cannot proceed without this | `SUPPORTING` = assists but crawl continues if unavailable

---

## SUBSYSTEM 0 — FOUNDATION / SCHEMA LAYER

### M00 — `schema_registry.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/tools/normalization_tools/schema_registry.py` |
| **Purpose** | Central registry of all JSON schema definitions; validates any artifact against its schema on demand |
| **Inputs** | JSON schema files from `ARCHON_PRIME/orchestration/json_drivers/` |
| **Outputs** | Validation results (pass/fail + validation errors) |
| **Dependencies** | None (foundation module) |
| **Class** | BLOCKING |
| **Phase** | FOUND |
| **Notes** | All other modules MUST import validation logic from here. No inline schema validation. |

### M01 — `routing_table_loader.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/orchestration/task_router/routing_table_loader.py` |
| **Purpose** | Load and expose the canonical output routing table from config; all artifact writes use this |
| **Inputs** | `ARCHON_PRIME/configs/crawl_configs/routing_table.json` |
| **Outputs** | Dict: artifact_type → canonical_path |
| **Dependencies** | M00 (schema validation) |
| **Class** | BLOCKING |
| **Phase** | FOUND |

### M02 — `repair_registry_loader.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/tools/audit_tools/repair_registry_loader.py` |
| **Purpose** | Load the repair registry (failure class → remediation behavior) before crawl begins |
| **Inputs** | `ARCHON_PRIME/configs/repair_registry/repair_registry.json` |
| **Outputs** | Dict: failure_class → {action, retry_limit, escalation_policy} |
| **Dependencies** | M00 |
| **Class** | BLOCKING |
| **Phase** | FOUND |

---

## SUBSYSTEM 1 — PRE-CRAWL AUDIT REGENERATION

### M10 — `repo_directory_scanner.py`
| Field | Value |
|-------|-------|
| **Path** | `AUDIT_SYSTEM/scripts/repo_scanners/repo_directory_scanner.py` |
| **Purpose** | Walk the LOGOS repo root, produce complete directory tree with metadata |
| **Inputs** | LOGOS repo root path (config) |
| **Outputs** | `repo_directory_tree.json` |
| **Dependencies** | M00 (schema validation), M01 (routing) |
| **Class** | BLOCKING |
| **Phase** | PRE |
| **Routing** | `ARCHON_PRIME/sources/baseline_analysis/repo_directory_tree.json` + `AUDIT_SYSTEM/reports/structural_reports/` |

### M11 — `python_file_collector.py`
| Field | Value |
|-------|-------|
| **Path** | `AUDIT_SYSTEM/scripts/repo_scanners/python_file_collector.py` |
| **Purpose** | Enumerate all `.py` files in LOGOS; record path, size, last-modified, module dotpath |
| **Inputs** | `repo_directory_tree.json` |
| **Outputs** | `repo_python_files.json` |
| **Dependencies** | M10 |
| **Class** | BLOCKING |
| **Phase** | PRE |
| **Routing** | `ARCHON_PRIME/sources/baseline_analysis/` + `AUDIT_SYSTEM/analysis/repo_maps/` |

### M12 — `import_extractor.py`
| Field | Value |
|-------|-------|
| **Path** | `AUDIT_SYSTEM/scripts/import_scanners/import_extractor.py` |
| **Purpose** | Parse each `.py` file via AST; extract all `import` and `from ... import` statements |
| **Inputs** | `repo_python_files.json` |
| **Outputs** | `repo_imports.json` |
| **Dependencies** | M11 |
| **Class** | BLOCKING |
| **Phase** | PRE |
| **Routing** | `ARCHON_PRIME/sources/baseline_analysis/` + `AUDIT_SYSTEM/analysis/repo_maps/` |

### M13 — `symbol_import_extractor.py`
| Field | Value |
|-------|-------|
| **Path** | `AUDIT_SYSTEM/scripts/import_scanners/symbol_import_extractor.py` |
| **Purpose** | From `repo_imports.json`, resolve which specific symbols are imported from each module |
| **Inputs** | `repo_imports.json`, `repo_python_files.json` |
| **Outputs** | `repo_symbol_imports.json` |
| **Dependencies** | M12 |
| **Class** | SUPPORTING |
| **Phase** | PRE |
| **Routing** | `AUDIT_SYSTEM/analysis/repo_maps/` |

### M14 — `header_schema_scanner.py`
| Field | Value |
|-------|-------|
| **Path** | `AUDIT_SYSTEM/scripts/header_scanners/header_schema_scanner.py` |
| **Purpose** | Scan every `.py` file for presence and compliance of canonical module header |
| **Inputs** | `repo_python_files.json`, `header_schema.json` |
| **Outputs** | `header_schema_compliance.json`, `modules_missing_headers.json` |
| **Dependencies** | M11, header_schema.json (config) |
| **Class** | BLOCKING |
| **Phase** | PRE |
| **Routing** | `AUDIT_SYSTEM/reports/governance_reports/` |

### M15 — `governance_contract_scanner.py`
| Field | Value |
|-------|-------|
| **Path** | `AUDIT_SYSTEM/scripts/governance_scanners/governance_contract_scanner.py` |
| **Purpose** | Scan all modules for governance contract declarations; check against expected contract registry |
| **Inputs** | `repo_python_files.json`, governance contract schema (config) |
| **Outputs** | `governance_contract_map.json`, `missing_governance_modules.json` |
| **Dependencies** | M11 |
| **Class** | BLOCKING |
| **Phase** | PRE |
| **Routing** | `ARCHON_PRIME/sources/governance_artifacts/` + `AUDIT_SYSTEM/reports/governance_reports/` |

### M16 — `runtime_phase_scanner.py`
| Field | Value |
|-------|-------|
| **Path** | `AUDIT_SYSTEM/scripts/runtime_scanners/runtime_phase_scanner.py` |
| **Purpose** | Scan all modules for declared runtime phase markers; extract phase assignments |
| **Inputs** | `repo_python_files.json` |
| **Outputs** | `raw_phase_assignments.json` (intermediate; consumed by M23) |
| **Dependencies** | M11 |
| **Class** | BLOCKING |
| **Phase** | PRE |
| **Routing** | `AUDIT_SYSTEM/analysis/runtime_maps/` |

### M17 — `concept_spec_gap_detector.py`
| Field | Value |
|-------|-------|
| **Path** | `AUDIT_SYSTEM/scripts/repo_scanners/concept_spec_gap_detector.py` |
| **Purpose** | Compare module inventory against declared LOGOS concepts and specs; surface unimplemented or orphaned modules |
| **Inputs** | `repo_python_files.json`, `module_index.json` (after M20), concept registry (config) |
| **Outputs** | `concept_spec_gap_report.json` |
| **Dependencies** | M11, M20 |
| **Class** | SUPPORTING |
| **Phase** | PRE |
| **Routing** | `AUDIT_SYSTEM/reports/concept_reports/` |

---

## SUBSYSTEM 2 — REPO ANALYSIS TOOLS

### M20 — `module_index_builder.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/tools/repo_mapping/module_index_builder.py` |
| **Purpose** | Build complete module index: maps every dotpath to file path, declared phase, governance class, imports |
| **Inputs** | `repo_python_files.json`, `repo_imports.json`, `raw_phase_assignments.json`, `governance_contract_map.json` |
| **Outputs** | `module_index.json` |
| **Dependencies** | M11, M12, M15, M16 |
| **Class** | BLOCKING |
| **Phase** | PRE |
| **Routing** | `ARCHON_PRIME/sources/baseline_analysis/` + `AUDIT_SYSTEM/reports/structural_reports/` |

### M21 — `dependency_graph_builder.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/tools/import_analysis/dependency_graph_builder.py` |
| **Purpose** | Build directed dependency graph from import relationships; nodes are module dotpaths, edges are import relationships |
| **Inputs** | `repo_imports.json`, `module_index.json` |
| **Outputs** | `dependency_graph.json` |
| **Dependencies** | M12, M20 |
| **Class** | BLOCKING |
| **Phase** | PRE |
| **Routing** | `ARCHON_PRIME/sources/baseline_analysis/` + `AUDIT_SYSTEM/analysis/dependency_graphs/` |

### M22 — `circular_dependency_detector.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/tools/import_analysis/circular_dependency_detector.py` |
| **Purpose** | Run cycle detection (Tarjan's SCC or equivalent) on dependency graph; classify cycles by severity (boot chain vs post-boot) |
| **Inputs** | `dependency_graph.json`, `runtime_phase_map.json` |
| **Outputs** | `circular_dependency_groups.json` |
| **Dependencies** | M21, M23 |
| **Class** | BLOCKING |
| **Phase** | PRE |
| **Routing** | `AUDIT_SYSTEM/analysis/dependency_graphs/` + `AUDIT_SYSTEM/reports/import_reports/` |
| **Notes** | Boot-chain circular deps are HALT-class; must be resolved before crawl is permitted |

### M23 — `runtime_phase_mapper.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/tools/runtime_analysis/runtime_phase_mapper.py` |
| **Purpose** | Merge raw phase assignments with module index; resolve conflicts; produce authoritative phase map |
| **Inputs** | `raw_phase_assignments.json`, `module_index.json` |
| **Outputs** | `runtime_phase_map.json` |
| **Dependencies** | M16, M20 |
| **Class** | BLOCKING |
| **Phase** | PRE |
| **Routing** | `ARCHON_PRIME/sources/baseline_analysis/` + `AUDIT_SYSTEM/reports/runtime_reports/` |

### M24 — `runtime_boot_sequencer.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/tools/runtime_analysis/runtime_boot_sequencer.py` |
| **Purpose** | From runtime phase map and dependency graph, produce topologically-sorted boot sequence for phase 0 and phase 1 modules |
| **Inputs** | `runtime_phase_map.json`, `dependency_graph.json` |
| **Outputs** | `runtime_boot_sequence.json` |
| **Dependencies** | M21, M23 |
| **Class** | BLOCKING |
| **Phase** | PRE |
| **Routing** | `ARCHON_PRIME/sources/baseline_analysis/` + `AUDIT_SYSTEM/reports/runtime_reports/` |

### M25 — `canonical_import_registry_builder.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/tools/import_analysis/canonical_import_registry_builder.py` |
| **Purpose** | Build the canonical import registry: maps every allowed import dotpath to its facade-compliant form; identifies all deep import violations |
| **Inputs** | `repo_imports.json`, `module_index.json`, Canonical Import Facade module list (config) |
| **Outputs** | `canonical_import_registry.json`, `canonical_import_rewrite_plan.json` |
| **Dependencies** | M12, M20 |
| **Class** | BLOCKING |
| **Phase** | PRE |
| **Routing** | `ARCHON_PRIME/tools/normalization_tools/` (registry) + `AUDIT_SYSTEM/analysis/dependency_graphs/` (rewrite plan) |
| **Notes** | Registry is LOCKED before crawl begins. No in-crawl modifications. |

---

## SUBSYSTEM 3 — SIMULATION LAYER

### M30 — `repo_simulator.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/simulation/repo_simulator/repo_simulator.py` |
| **Purpose** | Simulate repo state after full crawl completes; apply hypothetical mutations to module index and validate structural integrity |
| **Inputs** | `module_index.json`, `crawl_plan.json`, `canonical_import_rewrite_plan.json`, `header_schema.json` |
| **Outputs** | `simulation_report.json` (partial — repo section) |
| **Dependencies** | M20, M25, M38, header_schema.json |
| **Class** | BLOCKING |
| **Phase** | PRE |
| **Routing** | `ARCHON_PRIME/logs/simulation_logs/` |

### M31 — `runtime_simulator.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/simulation/runtime_simulator/runtime_simulator.py` |
| **Purpose** | Simulate runtime boot sequence after mutations; verify no boot chain violations are introduced |
| **Inputs** | `runtime_boot_sequence.json`, `crawl_plan.json`, `runtime_phase_map.json` |
| **Outputs** | `simulation_report.json` (partial — runtime section) |
| **Dependencies** | M24, M38 |
| **Class** | BLOCKING |
| **Phase** | PRE |
| **Routing** | `ARCHON_PRIME/logs/simulation_logs/` |

### M32 — `import_simulator.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/simulation/import_simulator/import_simulator.py` |
| **Purpose** | Simulate import resolution after all import rewrites; verify no broken imports or unresolvable dotpaths remain |
| **Inputs** | `dependency_graph.json`, `canonical_import_rewrite_plan.json`, `module_index.json` |
| **Outputs** | `simulation_report.json` (partial — import section) |
| **Dependencies** | M21, M25 |
| **Class** | BLOCKING |
| **Phase** | PRE |
| **Routing** | `ARCHON_PRIME/logs/simulation_logs/` |

---

## SUBSYSTEM 4 — CRAWL PLANNING

### M38 — `crawl_planner.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/crawler/engine/crawl_planner.py` |
| **Purpose** | Produce ordered module processing list; respects dependency graph topological sort, runtime phase order, and governance priority |
| **Inputs** | `module_index.json`, `dependency_graph.json`, `runtime_phase_map.json`, `runtime_boot_sequence.json`, `circular_dependency_groups.json` |
| **Outputs** | `crawl_plan.json` |
| **Dependencies** | M20, M21, M22, M23, M24 |
| **Class** | BLOCKING |
| **Phase** | PRE |
| **Routing** | `ARCHON_PRIME/orchestration/execution_graphs/crawl_plan.json` |
| **Notes** | Boot-chain modules are processed first. Circular deps in boot chain BLOCK plan generation. |

### M39 — `execution_graph_builder.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/orchestration/execution_graphs/execution_graph_builder.py` |
| **Purpose** | Transform crawl plan into a structured execution graph with explicit stage gates, checkpoints, and rollback points |
| **Inputs** | `crawl_plan.json` |
| **Outputs** | `execution_graph.json` |
| **Dependencies** | M38 |
| **Class** | BLOCKING |
| **Phase** | PRE |
| **Routing** | `ARCHON_PRIME/orchestration/execution_graphs/execution_graph.json` |

---

## SUBSYSTEM 5 — MUTATION OPERATORS

### M50 — `header_injector.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/crawler/mutation/header_injector.py` |
| **Purpose** | Replace existing module header or inject canonical header into modules that lack one; uses locked header_schema.json |
| **Inputs** | Module source (string), `header_schema.json`, module metadata from `module_index.json` |
| **Outputs** | Mutated module source (string), mutation event record |
| **Dependencies** | M00, header_schema.json |
| **Class** | BLOCKING |
| **Phase** | IN |
| **Notes** | Pure function: takes source in, returns source out. Does not write files directly — called by module_processor.py |

### M51 — `import_rewriter.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/crawler/mutation/import_rewriter.py` |
| **Purpose** | Rewrite deep imports to facade-compliant canonical forms per `canonical_import_rewrite_plan.json` |
| **Inputs** | Module source (string), `canonical_import_registry.json`, `canonical_import_rewrite_plan.json` |
| **Outputs** | Mutated module source (string), list of rewrites applied |
| **Dependencies** | M00, M25 |
| **Class** | BLOCKING |
| **Phase** | IN |
| **Notes** | Pure function. Operates on AST then re-serializes. Does not write files. |

---

## SUBSYSTEM 6 — CRAWL EXECUTION + PIPELINE

### M60 — `crawl_executor.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/crawler/engine/crawl_executor.py` |
| **Purpose** | Main crawl loop: iterate execution graph, invoke module_processor for each module, collect results, update crawl_status |
| **Inputs** | `execution_graph.json`, initialized instances of all pipeline modules |
| **Outputs** | `crawl_status.json` (live updates), `crawl_execution_log.json` (append) |
| **Dependencies** | M39, M61, M70, M71, M01, M02 |
| **Class** | BLOCKING |
| **Phase** | IN |
| **Notes** | Enforces one-module-at-a-time semantics. Single entry point for crawl execution. |

### M61 — `module_processor.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/crawler/pipeline/module_processor.py` |
| **Purpose** | Execute full processing pipeline for a single module: load → pre-validate → mutate → post-validate → route artifacts |
| **Inputs** | Module file path, module metadata, all mutation operators (M50, M51), all validators (M62, M63, M64) |
| **Outputs** | `ProcessingResult`: {status, mutations_applied, validation_results, errors} |
| **Dependencies** | M50, M51, M62, M63, M64 |
| **Class** | BLOCKING |
| **Phase** | IN |
| **Notes** | Stateless per call. Orchestrates: syntax_check → header_inject → import_rewrite → governance_validate → phase_validate → syntax_recheck |

### M62 — `syntax_validator.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/crawler/pipeline/syntax_validator.py` |
| **Purpose** | Validate Python syntax using `ast.parse()`; return structured error on failure |
| **Inputs** | Module source (string), module path |
| **Outputs** | `ValidationResult`: {pass/fail, errors[]} |
| **Dependencies** | None (stdlib only) |
| **Class** | BLOCKING |
| **Phase** | IN |

### M63 — `governance_validator.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/crawler/pipeline/governance_validator.py` |
| **Purpose** | Validate post-mutation module against its governance contract from `governance_contract_map.json` |
| **Inputs** | Module source (string), `governance_contract_map.json`, module dotpath |
| **Outputs** | `ValidationResult`: {pass/fail, violations[]} |
| **Dependencies** | M15 outputs |
| **Class** | BLOCKING |
| **Phase** | IN |

### M64 — `phase_validator.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/crawler/pipeline/phase_validator.py` |
| **Purpose** | Validate that module's phase assignment in its header matches `runtime_phase_map.json` |
| **Inputs** | Module source (string), `runtime_phase_map.json`, module dotpath |
| **Outputs** | `ValidationResult`: {pass/fail, phase_declared, phase_expected} |
| **Dependencies** | M23 outputs |
| **Class** | BLOCKING |
| **Phase** | IN |

### M65 — `crawl_monitor.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/crawler/monitor/crawl_monitor.py` |
| **Purpose** | Real-time crawl monitoring: tracks progress, detects stalls, mirrors status to AUDIT_SYSTEM/runtime_monitor/ |
| **Inputs** | `crawl_status.json` (live) |
| **Outputs** | `AUDIT_SYSTEM/runtime_monitor/live_status/crawl_status_mirror.json`, `AUDIT_SYSTEM/runtime_monitor/progress_tracking/progress_tracker.json` |
| **Dependencies** | M60 (reads its output) |
| **Class** | SUPPORTING |
| **Phase** | IN |

---

## SUBSYSTEM 7 — ERROR CLASSIFICATION + REPAIR

### M70 — `error_classifier.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/crawler/repair/error_classifier.py` |
| **Purpose** | Classify any processing failure into a known failure class from the failure taxonomy; return structured failure record |
| **Inputs** | Raw exception or `ValidationResult`, module context |
| **Outputs** | `FailureRecord`: {failure_class, severity, module_path, context, timestamp} |
| **Dependencies** | Failure taxonomy (loaded from repair_registry.json via M02) |
| **Class** | BLOCKING |
| **Phase** | IN |
| **Notes** | Unknown failure class → severity = HALT. No silent failures. |

### M71 — `repair_router.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/crawler/repair/repair_router.py` |
| **Purpose** | Given a classified failure, route to the correct repair action and enforce retry limits |
| **Inputs** | `FailureRecord`, repair registry (via M02), module retry counter |
| **Outputs** | Repair action directive: {action_type, retry_allowed, escalate_to_quarantine} |
| **Dependencies** | M02, M70 |
| **Class** | BLOCKING |
| **Phase** | IN |

### M72 — `repair_executor.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/crawler/repair/repair_executor.py` |
| **Purpose** | Execute the repair action directed by repair_router; apply fix; append to repair_event_log.json |
| **Inputs** | Repair action directive, module source, module context |
| **Outputs** | Repaired module source (string), `repair_event_log.json` (append) |
| **Dependencies** | M50, M51, M71 |
| **Class** | BLOCKING |
| **Phase** | IN |

---

## SUBSYSTEM 8 — QUARANTINE MANAGEMENT

### M80 — `quarantine_manager.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/crawler/quarantine/quarantine_manager.py` |
| **Purpose** | Generate governance-compliant quarantine stub; write stub to module path; update quarantine_registry.json |
| **Inputs** | Module path, `FailureRecord`, original source, quarantine stub template |
| **Outputs** | Written stub file, `quarantine_registry.json` (append) |
| **Dependencies** | M70 |
| **Class** | BLOCKING |
| **Phase** | IN |
| **Notes** | Original source is backed up before stub is written. Backup stored in `ARCHON_PRIME/sources/repo_snapshots/quarantine_backups/`. |

---

## SUBSYSTEM 9 — ARTIFACT ROUTING + REPORTING + COMMIT

### M90 — `artifact_router.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/crawler/commit/artifact_router.py` |
| **Purpose** | Route any generated artifact to its canonical location per routing table; validate destination exists before writing |
| **Inputs** | Artifact (data), artifact type key, routing table (via M01) |
| **Outputs** | Artifact written to canonical path; routing event logged |
| **Dependencies** | M01 |
| **Class** | BLOCKING |
| **Phase** | IN + POST |

### M91 — `report_generator.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/crawler/commit/report_generator.py` |
| **Purpose** | Produce human-readable and machine-readable post-crawl reports: summary, quarantine list, repair summary, validation summary |
| **Inputs** | `crawl_execution_log.json`, `repair_event_log.json`, `quarantine_registry.json`, `mutation_log.json`, `validation_report.json` |
| **Outputs** | `post_crawl_summary_report.json`, `post_crawl_summary_report.md` |
| **Dependencies** | M60, M72, M80, all log outputs |
| **Class** | BLOCKING |
| **Phase** | POST |
| **Routing** | `AUDIT_SYSTEM/reports/` (summary copies) |

### M92 — `commit_finalizer.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/crawler/commit/commit_finalizer.py` |
| **Purpose** | Verify all artifacts are at canonical locations; verify post-crawl summary exists; produce clean git commit |
| **Inputs** | `post_crawl_summary_report.json`, routing table verification pass, `quarantine_registry.json` |
| **Outputs** | Git commit (or list of pre-commit failures if not clean) |
| **Dependencies** | M91, M90 |
| **Class** | BLOCKING |
| **Phase** | POST |
| **Notes** | Does NOT force-commit. If pre-commit checks fail, outputs failure list and holds. |

---

## SUBSYSTEM 10 — ORCHESTRATION + CONTROLLER

### M95 — `task_router.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/orchestration/task_router/task_router.py` |
| **Purpose** | Route control-plane tasks (pre-crawl, crawl, post-crawl stages) to correct subsystems; enforce stage gates |
| **Inputs** | Stage directive, stage gate status from each subsystem |
| **Outputs** | Stage execution results; gate PASS/FAIL records |
| **Dependencies** | M01, M02, all subsystem entry points |
| **Class** | BLOCKING |
| **Phase** | PRE + IN + POST |

### M96 — `controller_main.py`
| Field | Value |
|-------|-------|
| **Path** | `ARCHON_PRIME/orchestration/controllers/controller_main.py` |
| **Purpose** | Top-level entry point for ARCHON_PRIME; parses config, initializes all subsystems, invokes task_router, handles HALT signals |
| **Inputs** | `crawl_config.json`, CLI args |
| **Outputs** | Exit code (0 = success, non-zero = failure or quarantine present) |
| **Dependencies** | ALL subsystems |
| **Class** | BLOCKING |
| **Phase** | PRE + IN + POST |
| **Notes** | If any HALT-class failure is raised anywhere in the system, controller_main catches it, emits diagnostic, and exits non-zero. |

---

## MODULE COUNT SUMMARY

| Subsystem | Module Count |
|-----------|-------------|
| S0 Foundation | 3 |
| S1 Audit Regeneration | 8 |
| S2 Repo Analysis | 6 |
| S3 Simulation | 3 |
| S4 Crawl Planning | 2 |
| S5 Mutation Operators | 2 |
| S6 Execution + Pipeline | 6 |
| S7 Error + Repair | 3 |
| S8 Quarantine | 1 |
| S9 Reporting + Commit | 3 |
| S10 Orchestration | 2 |
| **TOTAL** | **39** |
