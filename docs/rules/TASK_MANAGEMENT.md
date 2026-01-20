# Standard: Fractal Project Plan & Agent Protocols

## 1. Structure & Naming Convention (The Container Rule)
*   **Rule of Container**: If a directory exists, it **MUST** have an `index.md` (Roadmap). The root `.planning/` directory follows this rule too.
*   **Rule of Leaf**: If a file has no children directories, give it a `DescriptiveName.md`.
*   **Hybrid Model**: A directory can contain BOTH sub-directories (complex features) AND leaf files (simple tasks).

```text
.planning/
├── index.md                        # [ROOT MAP] Project Roadmap
├── auth/                           # Domain Directory
│   ├── index.md                    # [Container Map]
│   ├── password_reset.md           # [LEAF] Simple task
│   └── oauth/                      # [SUB-DIR] Complex feature
│       ├── index.md                # [Container Map]
│       └── google.md               # [LEAF] Specific task
└── database/
    ├── index.md                    # [Container Map] REQUIRED
    └── schema.md                   # [LEAF] Specific task
```

## 2. File Format & Metadata
**MANDATORY HEADER (For every task file):**
```markdown
<!-- METADATA
Status: [PENDING | IN_PROGRESS | DONE | BLOCKED]
Context: "Concise intent description"
Strategy: @REQUIRE_CONTEXT_CHAIN
-->
# [Title]
[<< UPLINK (Parent)](../index.md)
```

## 3. Protocol: Context Chain (@REQUIRE_CONTEXT_CHAIN)
**CRITICAL**: Agent **MUST** reconstruct the full context path **BEFORE** any action.
1.  **Trace**: Follow `[<< UPLINK]` from Leaf -> Root (`.planning/index.md`).
2.  **Load Stack**: Read Root -> Domain Index -> Feature Index -> Current File.
3.  **Scope**: Ignore sibling files (only load the vertical chain).

## 4. Execution Protocol (The 3-Flight Phases)
**Phase 1: Pre-Flight (Before Coding)**
1.  **Context**: Do I have the full Chain loaded?
2.  **Docs Check**: Check `/docs`. Do I understand the library/API?
3.  **Plan**: Do I have a concrete plan for this specific file?

**Phase 2: Flight (Execution)**
*   **DoD (Definition of Done)**: Task is `[x]` ONLY if verified (Test Passed / UI Checked).
*   **Atomic Steps**: Small changes, frequent verification.

**Phase 3: Post-Flight (Knowledge Propagation)**
*   **Elevator Rule**: If you learned something crucial, add a note to the `index.md` (Elevator Rule).
*   **Archive**: If task is DONE, move logs to archive.

## 5. Error Handling & Recovery Protocols
**The "Anti-Loop" Mechanism (2-Strikes Rule)**
1.  **Strike 1**: Attempt fix.
2.  **Strike 2**: Log entry in `## Troubleshooting Log`. Attempt different fix.
3.  **Strike 3**: **STOP**. Trigger **Creative Reboot**.

**Protocol: Creative Reboot (Before Giving Up)**
*   **Lateral Thinking**: Don't fix the code, fix the approach. Is the library wrong?
*   **Expert Knowledge**: How is this solved in industry standards?
*   **Docs Deep Dive**: Re-read the manual.

**Protocol: Spec Freeze (Red Line)**
*   If fixing a bug requires changing the agreed spec/architecture: **STOP**.
*   **ESCALATE**: Mark as `@blocked(spec_change_needed)` and ask User.

**Log Archiving Strategy (Cleanup)**
*   While Debugging: Keep logs in `## Troubleshooting Log` (at bottom of task file).
*   When Done (`[x]`):
    1.  **CUT** the log content.
    2.  **APPEND** it to `docs/archive/issues_log.md`.
    3.  **LEAVE** a marker: `(Issues archived: #ID...)` in the task file.

## 8. Dynamic Plan Updates (The Zero-Unplanned-Work Policy)
Jeśli podczas pracy wyniknie potrzeba wykonania zadania, którego nie ma w planie (np. brakujący ficzer, naprawa długu technologicznego, awaria):

**Algorithm: The Fit-Check Loop** (Gdzie wstrzyknąć zadanie?)
1.  **Check 1: Current Leaf (Lokalnie)**
    *   Czy to zadanie jest logicznym pod-krokiem obecnego pliku?
    *   *Akcja*: Dopisz w bieżącym pliku. **Tag: `[INJECTED]`**.
2.  **Check 2: Parent Module (Sąsiedztwo)**
    *   Otwórz plik rodzica (`../index.md`).
    *   Czy to zadanie pasuje do tego modułu?
    *   *Akcja*: Dopisz w `index.md` jako nowe zadanie-rodzeństwo. **Tag: `[INJECTED]`**.
3.  **Check 3: Root (Globalnie)**
    *   Otwórz `.planning/index.md`.
    *   Czy to zupełnie nowy obszar?
    *   *Akcja*: Dopisz w Root. **Tag: `[INJECTED]`**.
4.  **Fallback: Pure Ad-Hoc (Awaria)**
    *   Jeśli to "wypadek" (np. konflikt, awaria IDE) i nie pasuje nigdzie:
    *   *Akcja*: Dopisz na końcu aktywnego pliku w sekcji `## Ad-Hoc / Recovery`. **Tag: `[ADHOC]`**.
