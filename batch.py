import os

# --- Define your MDC file data here ---
MDC_FILES_DATA = [
    # We will populate this list
]

def create_or_update_mdc_file(filepath, description, globs, always_apply, body_content):
    """Creates or updates an .mdc file with the given frontmatter and body."""
    
    always_apply_str = 'true' if always_apply else 'false'
    
    frontmatter = f"""---
description: {description}
globs: {globs}
alwaysApply: {always_apply_str}
---
"""
    
    full_content = frontmatter + body_content.strip()

    try:
        dir_name = os.path.dirname(filepath)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
            print(f"Created directory: {dir_name}")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_content)
        print(f"Successfully created/updated: {filepath}")
    except Exception as e:
        print(f"Error writing file {filepath}: {e}")

if __name__ == "__main__":
    # Add refined Core rules first
    MDC_FILES_DATA.extend([
        {
            "path": ".cursor/rules/isolation_rules/Core/command-execution.mdc",
            "description": "Core guidelines for AI command execution, emphasizing tool priority (edit_file, fetch_rules, run_terminal_cmd), platform awareness, and result documentation within the Memory Bank system.",
            "globs": "**/Core/command-execution.mdc",
            "alwaysApply": False,
            "body": """
# COMMAND EXECUTION SYSTEM

> **TL;DR:** This system provides guidelines for efficient and reliable command and tool usage. Prioritize `edit_file` for file content, `fetch_rules` for loading `.mdc` rules, and `run_terminal_cmd` for execution tasks. Always document actions and results in `memory-bank/activeContext.md`.

## 🛠️ TOOL PRIORITY & USAGE

1.  **`edit_file` (Primary for Content):**
    *   Use for ALL creation and modification of `.md` files in `memory-bank/` and `documentation/`.
    *   Use for ALL source code modifications.
    *   `edit_file` can create a new file if it doesn't exist and populate it.
    *   Provide clear instructions or full content blocks for `edit_file`.
2.  **`fetch_rules` (Primary for `.mdc` Rules):**
    *   Use to load and follow instructions from other `.mdc` rule files within `.cursor/rules/isolation_rules/`.
    *   Specify the full path to the target `.mdc` file.
3.  **`read_file` (Primary for Context Gathering):**
    *   Use to read existing project files (source code, `README.md`), `memory-bank/*.md` files for context, or `.mdc` files if `fetch_rules` is not appropriate for the specific need (e.g., just extracting a template).
4.  **`run_terminal_cmd` (Primary for Execution):**
    *   Use for tasks like `mkdir`, running tests, build scripts, or starting servers.
    *   **CRITICAL:** Be platform-aware (see "Platform-Specific Considerations" below). If unsure of the OS, state your default command (e.g., for Linux) and ask for the Windows PowerShell equivalent if needed.
5.  **`list_dir`, `search_files`, `codebase_search`:**
    *   Use for file system exploration and code/text searching as appropriate.

## 🔍 COMMAND EFFICIENCY & PLANNING WORKFLOW (Conceptual for AI)
```mermaid
graph TD
    Start["Command Planning"] --> Analyze["Analyze Requirements"]
    Analyze --> ToolSelect["Select Correct Tool<br>(edit_file, fetch_rules, run_terminal_cmd, etc.)"]
    ToolSelect --> Complexity{"Action Complexity?"}
    Complexity -->|"Simple File Edit"| SingleEdit["Use `edit_file` directly"]
    Complexity -->|"Simple Terminal Cmd"| SingleCmd["Use `run_terminal_cmd`"]
    Complexity -->|"Complex Sequence"| GroupedSteps["Break into Logical Textual Steps<br>using appropriate tools for each step"]
    SingleEdit & SingleCmd & GroupedSteps --> Verify["Verify Results<br>(e.g., `read_file` back, check terminal output)"]
    Verify --> Document["Document Action & Result<br>in `activeContext.md` using `edit_file`"]
    Document --> Next["Next Action"]
```
**Textual Guide for AI:**
1.  **Analyze Requirements:** Understand what needs to be achieved.
2.  **Select Correct Tool:** Choose `edit_file` for content, `fetch_rules` for rules, `run_terminal_cmd` for execution, etc.
3.  **Execute:** Perform the action. For complex sequences, break it down into clear, tool-specific steps.
4.  **Verify Results:** If you used `edit_file`, consider using `read_file` to confirm the content. If `run_terminal_cmd`, examine the output.
5.  **Document Action & Result:** Use `edit_file` to append a summary of the command/tool call and its outcome to the "Build Log" or relevant section in `memory-bank/activeContext.md`.

## 🚦 DIRECTORY VERIFICATION (for `run_terminal_cmd`)
**Textual Guide for AI:**
1.  Before running build scripts or package manager commands (npm, pip) via `run_terminal_cmd`, verify you are in the correct project root directory.
2.  Use `list_dir` to check for key files like `package.json` or `requirements.txt`.
3.  If not in the correct directory, use `run_terminal_cmd` with `cd [path_to_project_root]` to navigate.

## 📋 COMMAND DOCUMENTATION TEMPLATE (for `activeContext.md` "Build Log")
When documenting your actions, use `edit_file` to append entries like this to `memory-bank/activeContext.md`:
```markdown
### Action: [Purpose of the action]
- **Tool Used:** `[edit_file | fetch_rules | run_terminal_cmd | etc.]`
- **Target/Command:** `[file_path | rule_path | actual_terminal_command]`
- **Parameters (if applicable):** `[e.g., content for edit_file, search query]`
- **Expected Outcome:** `[Briefly what you expected]`
- **Actual Result:**
  \`\`\`
  [Output from run_terminal_cmd, or confirmation of file edit/read]
  \`\`\`
- **Effect:** `[Brief description of what changed in the system or Memory Bank]`
- **Next Steps:** `[What you plan to do next]`
```

## 🔍 PLATFORM-SPECIFIC CONSIDERATIONS (for `run_terminal_cmd`)
**Textual Guide for AI:**
*   **Windows (PowerShell):** Path separator: `\`, Dir creation: `mkdir my_dir` or `New-Item -ItemType Directory -Path my_dir`.
*   **Unix/Linux/Mac (Bash/Zsh):** Path separator: `/`, Dir creation: `mkdir -p my_dir`.
*   **Action:** If unsure of OS, state default (Linux) and ask for Windows PowerShell equivalent or user OS specification.

## 📝 COMMAND EXECUTION CHECKLIST (AI Self-Correction)
- Purpose clear? Correct tool chosen? Platform considerations for `run_terminal_cmd`? Action/result documented in `activeContext.md` via `edit_file`? Outcome verified?

## 🚨 WARNINGS
*   Avoid `run_terminal_cmd` with `echo > file` or `Add-Content` for multi-line content. **Always use `edit_file`**.
*   For destructive `run_terminal_cmd` (e.g., `rm`), seek user confirmation.
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/Core/complexity-decision-tree.mdc",
            "description": "Core rule for AI to determine task complexity (Level 1-4) and initiate appropriate workflow using Memory Bank principles.",
            "globs": "**/Core/complexity-decision-tree.mdc",
            "alwaysApply": False,
            "body": """
# TASK COMPLEXITY DETERMINATION

> **TL;DR:** This rule guides you to determine task complexity (Level 1-4). Based on the level, you will then be instructed to `fetch_rules` for the corresponding primary mode map.

## 🌳 COMPLEXITY DECISION TREE (Conceptual for AI)
**Textual Guide for AI:**
Based on user's request and initial analysis (e.g., from `read_file` on `README.md`):

1.  **Bug fix/error correction?**
    *   **Yes:** Single, isolated component? -> **Level 1 (Quick Bug Fix)**
    *   **Yes:** Multiple components, straightforward fix? -> **Level 2 (Simple Enhancement/Refactor)**
    *   **Yes:** Complex interactions, architectural impact? -> **Level 3 (Intermediate Feature/Bug)**
    *   **No (new feature/enhancement):**
        *   Small, self-contained addition? -> **Level 2 (Simple Enhancement)**
        *   Complete new feature, multiple components, needs design? -> **Level 3 (Intermediate Feature)**
        *   System-wide, major subsystem, deep architectural design? -> **Level 4 (Complex System)**

## 📝 ACTION: DOCUMENT & ANNOUNCE COMPLEXITY

1.  **Determine Level:** Decide Level 1, 2, 3, or 4.
2.  **Document in `activeContext.md`:** Use `edit_file` to update `memory-bank/activeContext.md`:
    ```markdown
    ## Task Complexity Assessment
    - Task: [User's request]
    - Determined Complexity: Level [1/2/3/4] - [Name]
    - Rationale: [Justification]
    ```
3.  **Update `tasks.md`:** Use `edit_file` to update `memory-bank/tasks.md` with the level, e.g., `Level 3: Implement user auth`.
4.  **Announce & Next Step:**
    *   State: "Assessed as Level [N]: [Name]."
    *   **Level 1:** "Proceeding with Level 1 workflow. Will `fetch_rules` for `.cursor/rules/isolation_rules/Level1/workflow-level1.mdc` (or directly to IMPLEMENT map if simple enough, e.g., `visual-maps/implement-mode-map.mdc` which might then fetch a Level 1 implement rule)."
    *   **Level 2-4:** "Requires detailed planning. Transitioning to PLAN mode. Will `fetch_rules` for `.cursor/rules/isolation_rules/visual-maps/plan-mode-map.mdc`."
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/Core/creative-phase-enforcement.mdc",
            "description": "Core rule for enforcing Creative Phase completion for Level 3-4 tasks before allowing IMPLEMENT mode.",
            "globs": "**/Core/creative-phase-enforcement.mdc",
            "alwaysApply": False,
            "body": """
# CREATIVE PHASE ENFORCEMENT

> **TL;DR:** For L3/L4 tasks, if `tasks.md` flags items for "CREATIVE Phase", they MUST be completed before IMPLEMENT.

## 🔍 ENFORCEMENT WORKFLOW (AI Actions)
(Typically invoked by IMPLEMENT mode orchestrator for L3/L4 tasks, or by PLAN mode before suggesting IMPLEMENT)

1.  **Check Task Level & Creative Flags:**
    a.  `read_file` `memory-bank/activeContext.md` (for task level).
    b.  `read_file` `memory-bank/tasks.md`. Scan current feature's sub-tasks for incomplete "CREATIVE: Design..." entries.
2.  **Decision:**
    *   **If uncompleted CREATIVE tasks for L3/L4 feature:**
        a.  State: "🚨 IMPLEMENTATION BLOCKED for [feature]. Creative designs needed for: [list uncompleted creative tasks]."
        b.  Suggest: "Initiate CREATIVE mode (e.g., 'CREATIVE design [component]')." Await user.
    *   **Else (No uncompleted creative tasks or not L3/L4):**
        a.  State: "Creative phase requirements met/not applicable. Proceeding."
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/Core/creative-phase-metrics.mdc",
            "description": "Core reference on metrics and quality assessment for Creative Phase outputs. For AI understanding of quality expectations.",
            "globs": "**/Core/creative-phase-metrics.mdc",
            "alwaysApply": False, 
            "body": """
# CREATIVE PHASE METRICS & QUALITY ASSESSMENT (AI Guidance)

> **TL;DR:** This outlines quality expectations for `creative-*.md` documents. Use this as a guide when generating or reviewing creative outputs.

## 📊 QUALITY EXPECTATIONS FOR `memory-bank/creative/creative-[feature_name].md` (AI Self-Guide)
A good creative document (created/updated via `edit_file`) should cover:
1.  **Problem & Objectives:** Clearly defined. What problem is this design solving? What are the goals?
2.  **Requirements & Constraints:** List functional and non-functional requirements. Note any technical or business constraints.
3.  **Options Explored:** At least 2-3 viable design options should be considered and briefly described.
4.  **Analysis of Options:** For each option:
    *   Pros (advantages).
    *   Cons (disadvantages).
    *   Feasibility (technical, time, resources).
    *   Impact (on other system parts, user experience).
5.  **Recommended Design & Justification:** Clearly state the chosen design option and provide a strong rationale for why it was selected over others, referencing the analysis.
6.  **Implementation Guidelines:** High-level steps or considerations for implementing the chosen design. This is not a full plan, but key pointers for the IMPLEMENT phase.
7.  **Visualizations (if applicable):** Reference or describe any diagrams (e.g., flowcharts, component diagrams) that clarify the design. (Actual diagram creation might be a separate step or user-provided).
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/Core/file-verification.mdc",
            "description": "Core rule for AI to verify and create Memory Bank file structures, prioritizing `edit_file` for content and `run_terminal_cmd` for `mkdir`.",
            "globs": "**/Core/file-verification.mdc",
            "alwaysApply": False,
            "body": """
# OPTIMIZED FILE VERIFICATION & CREATION SYSTEM (Memory Bank Setup)

> **TL;DR:** Verify/create essential Memory Bank directories and files. Use `edit_file` to create/populate files, `run_terminal_cmd` (platform-aware) for `mkdir`. Log actions.

## ⚙️ AI ACTIONS FOR MEMORY BANK SETUP (Typically during early VAN)

1.  **Acknowledge:** State: "Performing Memory Bank file verification and setup."
2.  **Reference Paths:** Mentally (or by `read_file` if necessary) refer to `.cursor/rules/isolation_rules/Core/memory-bank-paths.mdc` for canonical paths.
3.  **Verify/Create `memory-bank/` Root Directory:**
    a.  Use `list_dir .` (project root) to check if `memory-bank/` exists.
    b.  If missing:
        i.  `run_terminal_cmd` (platform-aware, e.g., `mkdir memory-bank` or `New-Item -ItemType Directory -Path memory-bank`).
        ii. Verify creation (e.g., `list_dir .` again).
4.  **Verify/Create Core Subdirectories in `memory-bank/`:**
    a.  The subdirectories are: `creative/`, `reflection/`, `archive/`.
    b.  For each (e.g., `creative`):
        i.  `list_dir memory-bank/` to check if `memory-bank/creative/` exists.
        ii. If missing: `run_terminal_cmd` (e.g., `mkdir memory-bank/creative`). Verify.
5.  **Verify/Create Core `.md` Files in `memory-bank/` (Using `edit_file`):**
    a.  The core files are: `tasks.md`, `activeContext.md`, `progress.md`, `projectbrief.md`, `productContext.md`, `systemPatterns.md`, `techContext.md`, `style-guide.md`.
    b.  For each file (e.g., `tasks.md`):
        i.  Attempt to `read_file memory-bank/tasks.md`.
        ii. If it fails (file doesn't exist) or content is empty/default placeholder:
            Use `edit_file memory-bank/tasks.md` to write an initial template. Example for `tasks.md`:
            ```markdown
            # Memory Bank: Tasks

            ## Current Task
            - Task ID: T000
            - Name: [Task not yet defined]
            - Status: PENDING_INITIALIZATION
            - Complexity: Not yet assessed
            - Assigned To: AI

            ## Backlog
            (Empty)
            ```
            *(Provide similar minimal templates for other core files if creating them anew. `activeContext.md` could start with `# Active Context - Initialized [Timestamp]`).*
        iii. Optionally, `read_file memory-bank/tasks.md` again to confirm content.
6.  **Log Verification Actions:**
    a.  Use `edit_file` to append a summary to `memory-bank/activeContext.md` under a "File Verification Log" heading. List directories/files checked, created, or found existing. Note any errors.
    b.  Example log entry:
        ```markdown
        ### File Verification Log - [Timestamp]
        - Checked/Created `memory-bank/` directory.
        - Checked/Created `memory-bank/creative/` directory.
        - Checked/Created `memory-bank/tasks.md` (initial template written).
        - ... (other files/dirs) ...
        - Status: All essential Memory Bank structures verified/created.
        ```
7.  **Completion:** State: "Memory Bank file structure verification and setup complete."
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/Core/hierarchical-rule-loading.mdc",
            "description": "Core design principle for Memory Bank: hierarchical/lazy loading of `.mdc` rules via `fetch_rules`.",
            "globs": "**/Core/hierarchical-rule-loading.mdc",
            "alwaysApply": False, 
            "body": """
# HIERARCHICAL RULE LOADING SYSTEM (Design Principle for AI)

> **TL;DR:** You achieve hierarchical/lazy rule loading by following instructions in main mode prompts or other `.mdc` rules that direct you to use `fetch_rules` to load specific `.mdc` rule files only when needed.

## 🧠 HOW YOU EXECUTE HIERARCHICAL LOADING:
1.  **Mode Activation:** Your main custom prompt for a mode (e.g., VAN) tells you to `fetch_rules` for its primary orchestrating `.mdc` (e.g., `visual-maps/van_mode_split/van-mode-map.mdc`).
2.  **Following Instructions:** That `.mdc` guides you. Some steps might instruct: "If [condition], then `fetch_rules` to load and follow `[specific_sub_rule.mdc]`." For example, `van-mode-map.mdc` might tell you to `fetch_rules` for `Core/complexity-decision-tree.mdc`.
3.  **Current Rule Focus:** Always operate based on the instructions from the most recently fetched and relevant rule. Once a fetched rule's instructions are complete, you "return" to the context of the rule that fetched it, or if it was a top-level fetch, you await further user instruction or mode transition.
4.  **Acknowledge Fetches:** When you `fetch_rules` for an `.mdc`, briefly state: "Fetched `.cursor/rules/isolation_rules/[rule_path]`. Now proceeding with its instructions."
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/Core/memory-bank-paths.mdc",
            "description": "Defines canonical paths for core Memory Bank files and directories. CRITICAL reference for all file operations.",
            "globs": "**/Core/memory-bank-paths.mdc",
            "alwaysApply": True, 
            "body": """
# CORE MEMORY BANK FILE & DIRECTORY LOCATIONS

**CRITICAL REFERENCE:** Adhere strictly to these paths for all file operations (`edit_file`, `read_file`, `list_dir`, `run_terminal_cmd` for `mkdir`).

## Root Memory Bank Directory:
*   `memory-bank/` (at project root)

## Core `.md` Files (in `memory-bank/`):
*   Tasks: `memory-bank/tasks.md`
*   Active Context: `memory-bank/activeContext.md`
*   Progress: `memory-bank/progress.md`
*   Project Brief: `memory-bank/projectbrief.md`
*   Product Context: `memory-bank/productContext.md`
*   System Patterns: `memory-bank/systemPatterns.md`
*   Tech Context: `memory-bank/techContext.md`
*   Style Guide: `memory-bank/style-guide.md`

## Subdirectories in `memory-bank/`:
*   Creative: `memory-bank/creative/` (Files: `creative-[feature_or_component_name]-[YYYYMMDD].md`)
*   Reflection: `memory-bank/reflection/` (Files: `reflect-[task_id_or_feature_name]-[YYYYMMDD].md`)
*   Archive: `memory-bank/archive/` (Files: `archive-[task_id_or_feature_name]-[YYYYMMDD].md`)

## Project Documentation Directory (Separate from Memory Bank, but related):
*   `documentation/` (at project root, for final, polished, user-facing docs)

## AI Verification Mandate:
*   Before using `edit_file` on Memory Bank artifacts, confirm the path starts with `memory-bank/` or one of its specified subdirectories.
*   When creating new core files (e.g., `tasks.md`), use `edit_file` with the exact path (e.g., `memory-bank/tasks.md`).
*   For `run_terminal_cmd mkdir`, ensure correct target paths (e.g., `mkdir memory-bank/creative`).
*   Filenames for creative, reflection, and archive documents should include a descriptive name and a date (YYYYMMDD format is good practice).
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/Core/mode-transition-optimization.mdc",
            "description": "Core design principles for optimized mode transitions using `activeContext.md` as the handover document.",
            "globs": "**/Core/mode-transition-optimization.mdc",
            "alwaysApply": False, 
            "body": """
# MODE TRANSITION OPTIMIZATION (AI Actions)

> **TL;DR:** Efficient mode transitions are achieved by updating `memory-bank/activeContext.md` (via `edit_file`) before a transition. The next mode's orchestrator rule then reads this file for context.

## 🔄 CONTEXT TRANSFER PROCESS (AI Actions):

1.  **Before Current Mode Exits (or suggests exiting):**
    a.  Your current instructions (from main prompt or an `.mdc` via `fetch_rules`) will guide you to use `edit_file` to update `memory-bank/activeContext.md`.
    b.  This update should include a section like:
        ```markdown
        ## Mode Transition Prepared - [Timestamp]
        - **From Mode:** [Current Mode, e.g., PLAN]
        - **To Mode Recommended:** [Target Mode, e.g., CREATIVE or IMPLEMENT]
        - **Current Task Focus:** [Specific task name or ID from tasks.md]
        - **Key Outputs/Decisions from [Current Mode]:**
            - [Summary of what was achieved, e.g., "Plan for user authentication feature is complete."]
            - [Reference to key artifacts created/updated, e.g., "See `memory-bank/tasks.md` for detailed sub-tasks. Creative design needed for UI components."]
        - **Primary Goal for [Target Mode]:** [What the next mode should focus on, e.g., "Design UI mockups for login and registration pages."]
        ```
2.  **When New Mode Starts:**
    a.  The new mode's main custom prompt (in Cursor's Advanced Settings) will instruct you to `fetch_rules` for its primary orchestrating `.mdc` file (e.g., `visual-maps/creative-mode-map.mdc`).
    b.  That orchestrating `.mdc` will (as an early step) instruct you to `read_file memory-bank/activeContext.md` to understand the incoming context, task focus, and goals.

**Key Principle:** `memory-bank/activeContext.md` is the primary "handover document" between modes, managed by `edit_file`. Keep its "Mode Transition Prepared" section concise and actionable for the next mode.
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/Core/optimization-integration.mdc",
            "description": "Design overview of Memory Bank optimization strategies. For AI understanding of system goals.",
            "globs": "**/Core/optimization-integration.mdc",
            "alwaysApply": False, 
            "body": """
# MEMORY BANK OPTIMIZATION INTEGRATION (AI Understanding)

> **TL;DR:** You enact Memory Bank optimizations by following specific instructions from other rule files that guide hierarchical rule loading, adaptive complexity, and progressive documentation. This is not a standalone process you run, but a result of adhering to the CMB framework.

## 🔄 HOW YOU ACHIEVE OPTIMIZATIONS:
You don't "run" an optimization integration flow. You achieve system optimizations by:
1.  **Hierarchical Rule Loading:** Following `fetch_rules` instructions in main prompts and other `.mdc` files to load only necessary rules when they are needed. This keeps your immediate context focused and relevant. (See `Core/hierarchical-rule-loading.mdc`).
2.  **Adaptive Complexity Model:** Following `Core/complexity-decision-tree.mdc` (when fetched in VAN mode) to assess task complexity. Then, loading level-specific rules (from `LevelX/` directories) as directed by subsequent instructions. This tailors the process to the task's needs.
3.  **Dynamic Context Management:** Diligently using `read_file` to get context from, and `edit_file` to update, key Memory Bank files like `memory-bank/activeContext.md`, `memory-bank/tasks.md`, and `memory-bank/progress.md`. This ensures context is current and progressively built.
4.  **Transition Optimization:** Following the process in `Core/mode-transition-optimization.mdc` (i.e., updating `activeContext.md` before a mode switch to ensure smooth handover).
5.  **Creative Phase Optimization:** Using templates and structured guidance like `Phases/CreativePhase/optimized-creative-template.mdc` (when fetched in CREATIVE mode) to ensure thorough but efficient design exploration.
6.  **Tool Prioritization:** Consistently using the right tool for the job (e.g., `edit_file` for content, `run_terminal_cmd` for execution) as outlined in `Core/command-execution.mdc`. This avoids inefficient or error-prone methods.

**This document explains the *design goals* of the CMB system. Your role is to execute the specific, actionable instructions in other `.mdc` files. By following those rules, you are inherently participating in and enabling these optimizations.**
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/Core/platform-awareness.mdc",
            "description": "Core guidelines for platform-aware command execution with `run_terminal_cmd`.",
            "globs": "**/Core/platform-awareness.mdc",
            "alwaysApply": True, 
            "body": """
# PLATFORM AWARENESS SYSTEM (for `run_terminal_cmd`)

> **TL;DR:** When using `run_terminal_cmd`, be aware of OS differences (paths, common commands). If unsure, state your default command (Linux-style) and ask the user to confirm or provide the platform-specific version (e.g., for Windows PowerShell).

## 🔍 AI ACTION FOR PLATFORM AWARENESS:

1.  **Identify Need for `run_terminal_cmd`:** This tool is for tasks like `mkdir`, running scripts (e.g., `npm run build`, `python manage.py test`), installing packages (`pip install`, `npm install`), or other shell operations. **Do NOT use it for creating or editing file content; use `edit_file` for that.**
2.  **Consider Platform Differences:**
    *   **Path Separators:** `/` (common for Linux, macOS, and often works in modern Windows PowerShell) vs. `\` (traditional Windows). When constructing paths for commands, be mindful.
    *   **Common Commands:**
        *   Directory Creation: `mkdir -p path/to/dir` (Linux/macOS) vs. `New-Item -ItemType Directory -Path path\to\dir` or `mkdir path\to\dir` (Windows PowerShell).
        *   Listing Directory Contents: `ls -la` (Linux/macOS) vs. `Get-ChildItem` or `dir` (Windows PowerShell).
        *   File Deletion: `rm path/to/file` (Linux/macOS) vs. `Remove-Item path\to\file` (Windows PowerShell).
        *   Environment Variables: `export VAR=value` (Linux/macOS) vs. `$env:VAR="value"` (Windows PowerShell).
3.  **Execution Strategy with `run_terminal_cmd`:**
    a.  **Check Context:** `read_file memory-bank/techContext.md` or `memory-bank/activeContext.md` to see if the OS has been previously identified.
    b.  **If OS is Known:** Use the appropriate command syntax for that OS.
    c.  **If OS is Unknown or Unsure:**
        i.  State your intended action and the command you would typically use (default to Linux-style if no other info). Example: "To create the directory `my_app/src`, I would use `run_terminal_cmd` with `mkdir -p my_app/src`."
        ii. Ask for Confirmation/Correction: "Is this command correct for your operating system? If you are on Windows, please provide the PowerShell equivalent."
        iii. Await user confirmation or correction before proceeding with `run_terminal_cmd`.
    d.  **Clearly State Command:** Before execution, always state the exact command you are about to run with `run_terminal_cmd`.
4.  **Document Action and Outcome:**
    a.  After `run_terminal_cmd` completes, use `edit_file` to log the command, its full output (or a summary if very long), and success/failure status in `memory-bank/activeContext.md` under a "Terminal Command Log" or similar section. (Refer to `Core/command-execution.mdc` for the log template).

**This is a guiding principle. The key is to be *aware* of potential differences, default to a common standard (like Linux commands), and proactively seek clarification from the user when unsure to ensure `run_terminal_cmd` is used safely and effectively.**
"""
        }
    ])

    MDC_FILES_DATA.extend([
        {
            "path": ".cursor/rules/isolation_rules/visual-maps/archive-mode-map.mdc",
            "description": "Orchestrates ARCHIVE mode. Fetched when ARCHIVE process starts. Guides AI to finalize task documentation, create archive record, and update Memory Bank using level-specific rules and `edit_file`.",
            "globs": "**/visual-maps/archive-mode-map.mdc",
            "alwaysApply": False,
            "body": """
# ARCHIVE MODE: TASK DOCUMENTATION PROCESS MAP (AI Instructions)

> **TL;DR:** Finalize task documentation, create an archive record, and update Memory Bank. Use `edit_file` for all document interactions. This rule orchestrates by fetching level-specific archive rules.

## 🧭 ARCHIVE MODE PROCESS FLOW (AI Actions)

1.  **Acknowledge & Context Gathering:**
    a.  State: "Initiating ARCHIVE mode for the current task."
    b.  `read_file memory-bank/activeContext.md` to identify the current task name/ID and its determined complexity level.
    c.  `read_file memory-bank/tasks.md` to confirm task details and status (especially if REFLECT phase is marked complete).
    d.  `read_file memory-bank/reflection/` (specifically the reflection document related to the current task, e.g., `reflect-[task_name_or_id]-[date].md`).
    e.  `read_file memory-bank/progress.md` for any relevant final notes.
2.  **Pre-Archive Check (AI Self-Correction):**
    a.  Verify from `tasks.md` that the REFLECT phase for the current task is marked as complete.
    b.  Verify that the corresponding reflection document (e.g., `memory-bank/reflection/reflect-[task_name_or_id]-[date].md`) exists and appears finalized.
    c.  If checks fail: State "ARCHIVE BLOCKED: Reflection phase is not complete or reflection document is missing/incomplete for task [task_name]. Please complete REFLECT mode first." Await user.
3.  **Fetch Level-Specific Archive Rule:**
    a.  Based on the complexity level identified in `activeContext.md` or `tasks.md`:
        *   **Level 1:** `fetch_rules` for `.cursor/rules/isolation_rules/Level1/archive-minimal.mdc`.
        *   **Level 2:** `fetch_rules` for `.cursor/rules/isolation_rules/Level2/archive-basic.mdc`.
        *   **Level 3:** `fetch_rules` for `.cursor/rules/isolation_rules/Level3/archive-intermediate.mdc`.
        *   **Level 4:** `fetch_rules` for `.cursor/rules/isolation_rules/Level4/archive-comprehensive.mdc`.
4.  **Follow Fetched Rule:**
    a.  The fetched level-specific `.mdc` rule will provide detailed instructions for:
        i.  Creating the main archive document (e.g., `memory-bank/archive/archive-[task_name_or_id]-[date].md`) using `edit_file`. This includes summarizing the task, requirements, implementation, testing, and lessons learned (drawing from reflection docs).
        ii.  Potentially archiving other relevant documents (e.g., creative phase documents for L3/L4) by copying their content or linking to them within the main archive document.
        iii. Updating `memory-bank/tasks.md` to mark the task as "ARCHIVED" or "COMPLETED" using `edit_file`.
        iv. Updating `memory-bank/progress.md` with a final entry about archiving using `edit_file`.
        v.  Updating `memory-bank/activeContext.md` to clear the current task focus and indicate readiness for a new task, using `edit_file`.
5.  **Notify Completion:**
    a.  Once the fetched rule's instructions are complete, state: "ARCHIVING COMPLETE for task [task_name]. The archive document is located at `[path_to_archive_doc]`."
    b.  Recommend: "The Memory Bank is ready for the next task. Suggest using VAN mode to initiate a new task." Await user.
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/visual-maps/creative-mode-map.mdc",
            "description": "Orchestrates CREATIVE mode. Fetched by PLAN mode when design is needed. Guides AI to facilitate design for components flagged in `tasks.md`, using `fetch_rules` for design-type guidance and `edit_file` for documentation.",
            "globs": "**/visual-maps/creative-mode-map.mdc",
            "alwaysApply": False,
            "body": """
# CREATIVE MODE: DESIGN PROCESS MAP (AI Instructions)

> **TL;DR:** Facilitate design for components flagged in `tasks.md` as needing creative input. Use `fetch_rules` to get specific design-type guidance (Arch, UI/UX, Algo) and `edit_file` to create/update `memory-bank/creative/creative-[component_name]-[date].md` documents.

## 🧭 CREATIVE MODE PROCESS FLOW (AI Actions)

1.  **Acknowledge & Context Gathering:**
    a.  State: "Initiating CREATIVE mode. Identifying components requiring design."
    b.  `read_file memory-bank/tasks.md`. Look for sub-tasks under the current main task that are marked like "CREATIVE: Design [Component Name] ([Design Type: Architecture/UI-UX/Algorithm])" and are not yet complete.
    c.  `read_file memory-bank/activeContext.md` for overall project context and the current main task focus.
    d.  If no active "CREATIVE: Design..." sub-tasks are found for the current main task, state: "No pending creative design tasks found for [main_task_name]. Please specify a component and design type, or transition to another mode." Await user.
2.  **Iterate Through Pending Creative Sub-Tasks:**
    a.  For each pending "CREATIVE: Design [Component Name] ([Design Type])" sub-task:
        i.  Announce: "Starting CREATIVE phase for: [Component Name] - Design Type: [Architecture/UI-UX/Algorithm]."
        ii. Update `memory-bank/activeContext.md` using `edit_file` to set current focus: "Creative Focus: Designing [Component Name] ([Design Type])."
        iii. **Fetch Specific Design-Type Rule:**
            *   If Design Type is Architecture: `fetch_rules` for `.cursor/rules/isolation_rules/Phases/CreativePhase/creative-phase-architecture.mdc`.
            *   If Design Type is UI/UX: `fetch_rules` for `.cursor/rules/isolation_rules/Phases/CreativePhase/creative-phase-uiux.mdc`.
            *   If Design Type is Algorithm: `fetch_rules` for `.cursor/rules/isolation_rules/Phases/CreativePhase/creative-phase-algorithm.mdc`.
            *   (If design type is other/generic, fetch `Phases/CreativePhase/optimized-creative-template.mdc` and adapt general design principles).
        iv. **Follow Fetched Rule:** The fetched rule will guide you through:
            *   Defining the problem for that component.
            *   Exploring options.
            *   Analyzing trade-offs.
            *   Making a design decision.
            *   Outlining implementation guidelines.
        v.  **Document Design:**
            *   The fetched rule will instruct you to use `edit_file` to create or update the specific creative document: `memory-bank/creative/creative-[component_name]-[date].md`.
            *   It will likely reference `.cursor/rules/isolation_rules/Phases/CreativePhase/optimized-creative-template.mdc` (which you can `read_file` if not fetched directly) for the structure of this document.
        vi. **Update `memory-bank/activeContext.md`:** Use `edit_file` to append a summary of the design decision for [Component Name] to a "Creative Decisions Log" section.
        vii. **Update `memory-bank/tasks.md`:** Use `edit_file` to mark the "CREATIVE: Design [Component Name]..." sub-task as complete.
3.  **Overall Verification & Transition:**
    a.  After all identified creative sub-tasks for the main task are complete, state: "All CREATIVE design phases for [main_task_name] are complete. Design documents are located in `memory-bank/creative/`."
    b.  Recommend next mode: "Recommend transitioning to IMPLEMENT mode to build these components, or VAN QA mode for technical pre-flight checks if applicable." Await user.

## 📊 PRE-CREATIVE CHECK (AI Self-Correction):
1.  `read_file memory-bank/tasks.md`: Is there a main task currently in a state that expects creative design (e.g., PLAN phase completed, and specific "CREATIVE: Design..." sub-tasks are listed and pending)?
2.  If not, or if PLAN phase is not complete for the main task, state: "CREATIVE mode requires a planned task with identified components for design. Please ensure PLAN mode is complete for [main_task_name] and creative sub-tasks are defined in `tasks.md`." Await user.
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/visual-maps/implement-mode-map.mdc",
            "description": "Orchestrates IMPLEMENT mode. Fetched after PLAN/CREATIVE. Guides AI to implement features/fixes using level-specific rules, `edit_file` for code, `run_terminal_cmd` for builds/tests, and `Core/command-execution.mdc` for tool usage.",
            "globs": "**/visual-maps/implement-mode-map.mdc",
            "alwaysApply": False,
            "body": """
# IMPLEMENT MODE: CODE EXECUTION PROCESS MAP (AI Instructions)

> **TL;DR:** Implement the planned and designed features or bug fixes. Use `edit_file` for all code and documentation changes. Use `run_terminal_cmd` for builds, tests, etc. Fetch level-specific implementation rules and `Core/command-execution.mdc` for detailed tool guidance.

## 🧭 IMPLEMENT MODE PROCESS FLOW (AI Actions)

1.  **Acknowledge & Context Gathering:**
    a.  State: "Initiating IMPLEMENT mode for the current task."
    b.  `read_file memory-bank/activeContext.md` to identify the current task, its complexity level, and any outputs from PLAN/CREATIVE modes.
    c.  `read_file memory-bank/tasks.md` for the detailed sub-tasks, implementation plan, and references to creative design documents.
    d.  `read_file memory-bank/progress.md` for any ongoing implementation status.
    e.  If L3/L4 task, `read_file` relevant `memory-bank/creative/creative-[component]-[date].md` documents.
2.  **Pre-Implementation Checks (AI Self-Correction):**
    a.  **PLAN Complete?** Verify in `tasks.md` that the planning phase for the current task is marked complete.
    b.  **CREATIVE Complete (for L3/L4)?** `fetch_rules` for `.cursor/rules/isolation_rules/Core/creative-phase-enforcement.mdc` to check. If it blocks, await user action (e.g., switch to CREATIVE mode).
    c.  **VAN QA Passed (if applicable)?** Check `activeContext.md` or a dedicated status file if VAN QA was run. If VAN QA failed, state: "IMPLEMENTATION BLOCKED: VAN QA checks previously failed. Please resolve issues and re-run VAN QA." Await user.
    d.  If any critical pre-check fails, state the blockage and await user instruction.
3.  **Fetch General Command Execution Guidelines:**
    a.  `fetch_rules` for `.cursor/rules/isolation_rules/Core/command-execution.mdc`. Keep these guidelines in mind for all tool usage.
4.  **Fetch Level-Specific Implementation Rule:**
    a.  Based on the complexity level:
        *   **Level 1:** `fetch_rules` for `.cursor/rules/isolation_rules/Level1/workflow-level1.mdc` (or a more specific L1 implement rule if it exists, e.g., `Level1/implement-quick-fix.mdc`).
        *   **Level 2:** `fetch_rules` for `.cursor/rules/isolation_rules/Level2/workflow-level2.mdc` (or `Level2/implement-basic.mdc`).
        *   **Level 3:** `fetch_rules` for `.cursor/rules/isolation_rules/Level3/implementation-intermediate.mdc`.
        *   **Level 4:** `fetch_rules` for `.cursor/rules/isolation_rules/Level4/phased-implementation.mdc`.
5.  **Follow Fetched Rule (Iterative Implementation):**
    a.  The level-specific rule will guide you through the implementation steps, which will involve:
        i.  Identifying the next specific sub-task from `tasks.md`.
        ii. Creating/modifying source code files using `edit_file`.
        iii. Creating/modifying documentation (e.g., code comments, README sections) using `edit_file`.
        iv. Running build scripts or compilers using `run_terminal_cmd` (platform-aware).
        v.  Running tests using `run_terminal_cmd`.
        vi. Verifying file creation/modification (e.g., using `read_file` or `list_dir`).
        vii. Documenting each significant action (tool used, command, outcome) in `memory-bank/activeContext.md` (in a "Build Log" section) using `edit_file`.
        viii. Updating `memory-bank/progress.md` with detailed progress for each sub-task using `edit_file`.
        ix. Updating `memory-bank/tasks.md` to mark sub-tasks as complete using `edit_file`.
    b.  This is an iterative process. Continue until all implementation sub-tasks in `tasks.md` are complete.
6.  **Notify Completion:**
    a.  Once all implementation sub-tasks are complete, state: "IMPLEMENTATION COMPLETE for task [task_name]."
    b.  Update `memory-bank/tasks.md` to mark the main IMPLEMENT phase as complete.
    c.  Update `memory-bank/activeContext.md`: "Implementation phase complete for [task_name]. Ready for REFLECT mode."
    d.  Recommend: "Recommend transitioning to REFLECT mode for review and lessons learned." Await user.
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/visual-maps/plan-mode-map.mdc",
            "description": "Orchestrates PLAN mode. Fetched by VAN for L2+ tasks. Guides AI to create detailed plans in `tasks.md` using level-specific rules, `edit_file`, and identifies needs for CREATIVE mode.",
            "globs": "**/visual-maps/plan-mode-map.mdc",
            "alwaysApply": False,
            "body": """
# PLAN MODE: TASK PLANNING PROCESS MAP (AI Instructions)

> **TL;DR:** Create a detailed implementation plan for Level 2-4 tasks. Update `tasks.md` extensively using `edit_file`. Identify components needing CREATIVE design. Fetch level-specific planning rules for detailed guidance.

## 🧭 PLAN MODE PROCESS FLOW (AI Actions)

1.  **Acknowledge & Context Gathering:**
    a.  State: "Initiating PLAN mode for the current task."
    b.  `read_file memory-bank/activeContext.md` to understand the task name, determined complexity level (should be L2, L3, or L4), and any initial notes from VAN mode.
    c.  `read_file memory-bank/tasks.md` for the current state of the task entry.
    d.  `read_file memory-bank/projectbrief.md`, `productContext.md`, `systemPatterns.md`, `techContext.md` for broader project understanding.
2.  **Pre-Planning Check (AI Self-Correction):**
    a.  Verify from `activeContext.md` or `tasks.md` that the task complexity is indeed Level 2, 3, or 4.
    b.  If complexity is Level 1 or not assessed, state: "PLAN mode is intended for Level 2-4 tasks. Current task is [Level/Status]. Please clarify or run VAN mode for complexity assessment." Await user.
3.  **Fetch Level-Specific Planning Rule:**
    a.  Based on the complexity level:
        *   **Level 2:** `fetch_rules` for `.cursor/rules/isolation_rules/Level2/task-tracking-basic.mdc` (or a dedicated L2 planning rule like `Level2/planning-basic.mdc` if it exists).
        *   **Level 3:** `fetch_rules` for `.cursor/rules/isolation_rules/Level3/planning-comprehensive.mdc`.
        *   **Level 4:** `fetch_rules` for `.cursor/rules/isolation_rules/Level4/architectural-planning.mdc`.
4.  **Follow Fetched Rule (Detailed Planning):**
    a.  The fetched level-specific rule will guide you through the detailed planning steps, which will involve extensive updates to `memory-bank/tasks.md` using `edit_file`. This includes:
        i.  Breaking down the main task into smaller, actionable sub-tasks.
        ii. Defining requirements, acceptance criteria for each sub-task.
        iii. Identifying affected components, files, or modules.
        iv. Estimating effort/dependencies for sub-tasks (qualitatively).
        v.  **Crucially for L3/L4:** Identifying specific components or aspects that require a dedicated CREATIVE design phase (e.g., "CREATIVE: Design User Authentication UI", "CREATIVE: Design Database Schema for Orders"). These should be added as specific sub-tasks in `tasks.md`.
        vi. Outlining a high-level implementation sequence.
        vii. Documenting potential challenges and mitigation strategies.
    b.  Throughout this process, use `edit_file` to meticulously update the relevant sections in `memory-bank/tasks.md`.
    c.  Update `memory-bank/activeContext.md` periodically with planning progress notes using `edit_file`.
5.  **Technology Validation (Conceptual - AI doesn't run code here but plans for it):**
    a.  The fetched planning rule might instruct you to consider and document the technology stack, any new dependencies, or build configurations needed. This is documented in `tasks.md` or `techContext.md` using `edit_file`.
    b.  If significant new technologies or complex configurations are involved, add a sub-task in `tasks.md` for "VAN QA: Technical Validation" to be performed before IMPLEMENT.
6.  **Notify Completion & Recommend Next Mode:**
    a.  Once the detailed plan is formulated in `tasks.md` as per the fetched rule, state: "PLANNING COMPLETE for task [task_name]. Detailed plan and sub-tasks are updated in `memory-bank/tasks.md`."
    b.  Update `memory-bank/tasks.md` to mark the main PLAN phase as complete.
    c.  Update `memory-bank/activeContext.md`: "Planning phase complete for [task_name]."
    d.  **Recommendation:**
        *   If "CREATIVE: Design..." sub-tasks were identified: "Recommend transitioning to CREATIVE mode to address design requirements."
        *   If no CREATIVE sub-tasks (e.g., simpler L2 task) and no VAN QA flagged: "Recommend transitioning to IMPLEMENT mode."
        *   If VAN QA was flagged as needed: "Recommend transitioning to VAN QA mode for technical pre-flight checks."
    e.  Await user instruction.
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/visual-maps/qa-mode-map.mdc",
            "description": "Orchestrates general QA mode (distinct from VAN QA). Fetched when user invokes 'QA'. Guides AI to perform context-aware validation of Memory Bank consistency, task tracking, and phase-specific checks.",
            "globs": "**/visual-maps/qa-mode-map.mdc",
            "alwaysApply": False,
            "body": """
# QA MODE: GENERAL VALIDATION PROCESS MAP (AI Instructions)

> **TL;DR:** Perform comprehensive validation of Memory Bank consistency, task tracking, and current phase status. This is a general QA mode, callable anytime, distinct from the pre-build VAN QA. Use `read_file` extensively and `edit_file` to log QA findings.

## 🧭 QA MODE PROCESS FLOW (AI Actions)

1.  **Acknowledge & Context Gathering:**
    a.  State: "Initiating general QA MODE. Analyzing current project state."
    b.  `read_file memory-bank/activeContext.md` to determine the current task, its perceived phase (VAN, PLAN, CREATIVE, IMPLEMENT, REFLECT, ARCHIVE), and complexity.
    c.  `read_file memory-bank/tasks.md` for task statuses and details.
    d.  `read_file memory-bank/progress.md` for activity log.
2.  **Universal Validation Checks (AI Self-Correction & Reporting):**
    a.  **Memory Bank Core File Integrity:**
        i.  `fetch_rules` for `.cursor/rules/isolation_rules/Core/memory-bank-paths.mdc` to get list of core files.
        ii. For each core file: Attempt `read_file`. Report if any are missing or seem corrupted (e.g., empty when they shouldn't be).
    b.  **`tasks.md` Consistency:**
        i.  Is there a clearly defined current task?
        ii. Are statuses (PENDING, IN_PROGRESS, COMPLETE, BLOCKED, CREATIVE_NEEDED, QA_NEEDED, REFLECT_NEEDED, ARCHIVE_NEEDED) used consistently?
        iii. Do sub-tasks roll up logically to the main task's status?
    c.  **`activeContext.md` Relevance:**
        i.  Does the `activeContext.md` accurately reflect the current focus apparent from `tasks.md` and `progress.md`?
        ii. Is the "Last Updated" timestamp recent relative to `progress.md`?
    d.  **`progress.md` Completeness:**
        i.  Are there entries for recent significant activities?
        ii. Do entries clearly state actions taken and outcomes?
    e.  **Cross-Reference Check (Conceptual):**
        i.  Do task IDs in `progress.md` or `activeContext.md` match those in `tasks.md`?
        ii. Do references to creative/reflection/archive documents seem plausible (e.g., filenames match task names)?
3.  **Phase-Specific Validation (Based on perceived current phase from `activeContext.md`):**
    *   **If VAN phase:** Are `projectbrief.md`, `techContext.md` populated? Is complexity assessed in `tasks.md`?
    *   **If PLAN phase:** Is `tasks.md` detailed with sub-tasks, requirements? Are creative needs identified for L3/L4?
    *   **If CREATIVE phase:** Do `memory-bank/creative/` documents exist for components marked in `tasks.md`? Are decisions logged in `activeContext.md`?
    *   **If IMPLEMENT phase:** Is there a "Build Log" in `activeContext.md`? Is `progress.md` being updated with code changes and test results? Are sub-tasks in `tasks.md` being marked complete?
    *   **If REFLECT phase:** Does `memory-bank/reflection/reflect-[task_name]-[date].md` exist and seem complete? Is `tasks.md` updated for reflection?
    *   **If ARCHIVE phase:** Does `memory-bank/archive/archive-[task_name]-[date].md` exist? Is `tasks.md` marked fully complete/archived?
4.  **Report Generation:**
    a.  Use `edit_file` to create a new QA report in `memory-bank/qa_reports/qa-report-[date]-[time].md`.
    b.  **Structure of the report:**
        ```markdown
        # General QA Report - [Date] [Time]
        - Perceived Current Task: [Task Name/ID]
        - Perceived Current Phase: [Phase]
        - Perceived Complexity: [Level]

        ## Universal Validation Findings:
        - Memory Bank Core Files: [OK/Issues found: list them]
        - `tasks.md` Consistency: [OK/Issues found: list them]
        - `activeContext.md` Relevance: [OK/Issues found: list them]
        - `progress.md` Completeness: [OK/Issues found: list them]
        - Cross-References: [OK/Issues found: list them]

        ## Phase-Specific ([Phase]) Validation Findings:
        - [Check 1]: [OK/Issue]
        - [Check 2]: [OK/Issue]

        ## Summary & Recommendations:
        - Overall Status: [GREEN/YELLOW/RED]
        - [Specific recommendations for fixes or areas to improve]
        ```
    c.  Announce: "General QA validation complete. Report generated at `memory-bank/qa_reports/qa-report-[date]-[time].md`."
    d.  Present a summary of key findings (especially any RED/YELLOW status items) directly to the user.
5.  **Await User Action:** Await user instructions for addressing any reported issues or proceeding.
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/visual-maps/reflect-mode-map.mdc",
            "description": "Orchestrates REFLECT mode. Fetched after IMPLEMENT. Guides AI to review implementation, document lessons in `reflection/...md`, and update Memory Bank using level-specific rules and `edit_file`.",
            "globs": "**/visual-maps/reflect-mode-map.mdc",
            "alwaysApply": False,
            "body": """
# REFLECT MODE: TASK REVIEW PROCESS MAP (AI Instructions)

> **TL;DR:** Review the completed implementation, document insights and lessons learned in `memory-bank/reflection/reflect-[task_name]-[date].md`. Use `edit_file` for all documentation. Fetch level-specific reflection rules for detailed guidance.

## 🧭 REFLECT MODE PROCESS FLOW (AI Actions)

1.  **Acknowledge & Context Gathering:**
    a.  State: "Initiating REFLECT mode for the current task."
    b.  `read_file memory-bank/activeContext.md` to identify the current task, its complexity level, and confirmation that IMPLEMENT phase is complete.
    c.  `read_file memory-bank/tasks.md` for the original plan, sub-tasks, and requirements.
    d.  `read_file memory-bank/progress.md` to review the implementation journey and any challenges logged.
    e.  `read_file` any relevant `memory-bank/creative/creative-[component]-[date].md` documents (for L3/L4) to compare design with implementation.
2.  **Pre-Reflection Check (AI Self-Correction):**
    a.  Verify from `tasks.md` or `activeContext.md` that the IMPLEMENT phase for the current task is marked as complete.
    b.  If not, state: "REFLECT BLOCKED: Implementation phase is not yet complete for task [task_name]. Please complete IMPLEMENT mode first." Await user.
3.  **Fetch Level-Specific Reflection Rule:**
    a.  Based on the complexity level:
        *   **Level 1:** `fetch_rules` for `.cursor/rules/isolation_rules/Level1/reflection-basic.mdc`. (If not present, use L2)
        *   **Level 2:** `fetch_rules` for `.cursor/rules/isolation_rules/Level2/reflection-basic.mdc`. (Note: `rules-visual-maps.txt` refers to `reflection-standard.md` for L2, I'll use `reflection-basic` as per `STRUCTURE.md` or assume they are similar. If a specific `reflection-standard.mdc` exists, use that).
        *   **Level 3:** `fetch_rules` for `.cursor/rules/isolation_rules/Level3/reflection-intermediate.mdc`.
        *   **Level 4:** `fetch_rules` for `.cursor/rules/isolation_rules/Level4/reflection-comprehensive.mdc`.
4.  **Follow Fetched Rule (Structured Reflection):**
    a.  The fetched level-specific `.mdc` rule will guide you through the reflection process, which involves creating/updating `memory-bank/reflection/reflect-[task_name_or_id]-[date].md` using `edit_file`. Key sections to populate (guided by the fetched rule):
        i.  **Summary of Task & Outcome:** What was built, did it meet goals?
        ii. **What Went Well:** Successful aspects, efficient processes.
        iii. **Challenges Encountered:** Difficulties, roadblocks, unexpected issues. How were they overcome?
        iv. **Lessons Learned:** Key takeaways, new knowledge gained (technical, process-wise).
        v.  **Comparison with Plan/Design:** Deviations from original plan/design and why.
        vi. **Process Improvements:** Suggestions for future tasks.
        vii. **Technical Improvements/Alternatives:** Better technical approaches for similar future tasks.
        viii. **Code Quality/Maintainability Assessment (if applicable).**
    b.  Use `edit_file` to meticulously populate the reflection document.
    c.  Update `memory-bank/activeContext.md` with notes like "Reflection in progress for [task_name]."
5.  **Notify Completion:**
    a.  Once the reflection document is complete as per the fetched rule, state: "REFLECTION COMPLETE for task [task_name]. Reflection document created/updated at `memory-bank/reflection/reflect-[task_name_or_id]-[date].md`."
    b.  Use `edit_file` to update `memory-bank/tasks.md`, marking the REFLECT phase as complete for the task.
    c.  Use `edit_file` to update `memory-bank/activeContext.md`: "Reflection phase complete for [task_name]. Ready for ARCHIVE mode."
    d.  Recommend: "Recommend transitioning to ARCHIVE mode to finalize and store task documentation." Await user.
"""
        },
        # --- VAN Mode Split Files ---
        {
            "path": ".cursor/rules/isolation_rules/visual-maps/van_mode_split/van-mode-map.mdc",
            "description": "Main orchestrator for VAN mode: platform detection, file verification, complexity determination, and optional QA. Fetched when VAN mode starts.",
            "globs": "**/visual-maps/van_mode_split/van-mode-map.mdc",
            "alwaysApply": False,
            "body": """
# VAN MODE: INITIALIZATION PROCESS MAP (AI Instructions)

> **TL;DR:** Initialize project: platform detection, file verification, complexity determination. For L2+ tasks, transition to PLAN. For L1, complete initialization. If 'VAN QA' is called, perform technical validation. This rule orchestrates by fetching specific sub-rules.

## 🧭 VAN MODE PROCESS FLOW (AI Actions)

1.  **Acknowledge & Determine Entry Point:**
    *   If user typed "VAN": Respond "OK VAN - Beginning Initialization Process." Proceed with step 2.
    *   If user typed "VAN QA": Respond "OK VAN QA - Beginning Technical Validation." Skip to step 6.
2.  **Platform Detection (Sub-Rule):**
    a.  State: "Performing platform detection."
    b.  `fetch_rules` to load and follow `.cursor/rules/isolation_rules/visual-maps/van_mode_split/van-platform-detection.mdc`.
    c.  (The fetched rule will guide OS detection and logging to `activeContext.md` via `edit_file`).
3.  **File Verification & Creation (Memory Bank Setup) (Sub-Rule):**
    a.  State: "Performing Memory Bank file verification and setup."
    b.  `fetch_rules` to load and follow `.cursor/rules/isolation_rules/Core/file-verification.mdc`.
    c.  (The fetched rule guides checking/creating `memory-bank/` dir, subdirs, and core `.md` files using `edit_file` and `run_terminal_cmd`).
4.  **Early Complexity Determination (Sub-Rule):**
    a.  State: "Determining task complexity."
    b.  `fetch_rules` to load and follow `.cursor/rules/isolation_rules/Core/complexity-decision-tree.mdc`.
    c.  (The fetched rule guides assessing Level 1-4 and updating `activeContext.md` and `tasks.md` via `edit_file`).
    d.  `read_file memory-bank/activeContext.md` to confirm the determined complexity level.
5.  **Mode Transition based on Complexity:**
    a.  **If Level 1 determined:**
        i.  State: "Task assessed as Level 1. Completing VAN initialization."
        ii. Use `edit_file` to update `memory-bank/activeContext.md` with: "VAN Process Status: Level 1 Initialization Complete. Task ready for IMPLEMENT mode."
        iii. State: "VAN Initialization Complete for Level 1 task [Task Name]. Recommend IMPLEMENT mode." Await user.
    b.  **If Level 2, 3, or 4 determined:**
        i.  State: "🚫 LEVEL [2/3/4] TASK DETECTED: [Task Name]. This task REQUIRES detailed planning."
        ii. State: "Transitioning to PLAN mode is necessary. Type 'PLAN' to proceed with planning." Await user.
        iii. (VAN mode is effectively paused here for L2-4 tasks. The user will initiate PLAN mode, which has its own orchestrator).
6.  **VAN QA - Technical Validation (Entry point if "VAN QA" was typed, or if called after CREATIVE mode by user):**
    a.  State: "Initiating VAN QA Technical Validation."
    b.  `fetch_rules` to load and follow `.cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-main.mdc`.
    c.  (The `van-qa-main.mdc` will orchestrate the entire QA process, fetching further sub-rules for specific checks and reporting).
    d.  After `van-qa-main.mdc` completes, it will have provided a summary and recommended next steps (e.g., proceed to BUILD or fix issues). Await user action based on that QA report.

## 🔄 QA COMMAND PRECEDENCE (If user types "QA" during steps 2-4 of VAN Initialization)
1.  State: "General QA command received, pausing current VAN initialization step ([current step])."
2.  `fetch_rules` to load and follow `.cursor/rules/isolation_rules/visual-maps/qa-mode-map.mdc` (the general QA orchestrator).
3.  After general QA is complete (and any issues potentially addressed by the user):
    a.  State: "Resuming VAN initialization."
    b.  Re-evaluate or continue from the paused VAN initialization step. For example, if paused during complexity determination, complete it, then proceed to step 5.
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/visual-maps/van_mode_split/van-platform-detection.mdc",
            "description": "VAN sub-rule for platform detection. Fetched by `van-mode-map.mdc`. Guides AI to detect OS and document in `activeContext.md`.",
            "globs": "**/visual-maps/van_mode_split/van-platform-detection.mdc",
            "alwaysApply": False,
            "body": """
# VAN MODE: PLATFORM DETECTION (AI Instructions)

> **TL;DR:** Detect the Operating System. Document the detected OS and path separator style in `memory-bank/activeContext.md` and `memory-bank/techContext.md` using `edit_file`. This rule is typically fetched by `van-mode-map.mdc`.

## ⚙️ AI ACTIONS FOR PLATFORM DETECTION:

1.  **Acknowledge:** State: "Attempting to determine Operating System."
2.  **Attempt Detection (via `run_terminal_cmd` - carefully):**
    *   **Strategy:** Use a simple, non-destructive command that has distinct output or behavior across OSes.
    *   Example 1 (Check for `uname`):
        *   `run_terminal_cmd uname`
        *   If output is "Linux", "Darwin" (macOS), or similar: OS is Unix-like. Path separator likely `/`.
        *   If command fails or output is unrecognized: OS might be Windows.
    *   Example 2 (Check PowerShell specific variable, if assuming PowerShell might be present):
        *   `run_terminal_cmd echo $PSVersionTable.PSVersion` (PowerShell)
        *   If successful with version output: OS is Windows (with PowerShell). Path separator likely `\`.
        *   If fails: Not PowerShell, or not Windows.
    *   **If still unsure after one attempt, DO NOT run many speculative commands.**
3.  **Decision & User Interaction if Unsure:**
    a.  **If Confident:** (e.g., `uname` returned "Linux")
        i.  Detected OS: Linux. Path Separator: `/`.
    b.  **If Unsure:**
        i.  State: "Could not definitively determine the OS automatically."
        ii. Ask User: "Please specify your Operating System (e.g., Windows, macOS, Linux) and preferred path separator (`/` or `\\`)."
        iii. Await user response.
        iv. Detected OS: [User's response]. Path Separator: [User's response].
4.  **Document Findings:**
    a.  Use `edit_file` to update `memory-bank/activeContext.md` with a section:
        ```markdown
        ## Platform Detection Log - [Timestamp]
        - Detected OS: [Windows/macOS/Linux/User-Specified]
        - Path Separator Style: [/ or \\]
        - Confidence: [High/Medium/Low/User-Provided]
        ```
    b.  Use `edit_file` to update (or create if not exists) `memory-bank/techContext.md` with:
        ```markdown
        # Technical Context
        ## Operating System
        - OS: [Windows/macOS/Linux/User-Specified]
        - Path Separator: [/ or \\]
        ## Key Command Line Interface (if known)
        - CLI: [Bash/Zsh/PowerShell/CMD/User-Specified]
        ```
5.  **Completion:** State: "Platform detection complete. OS identified as [OS_Name]. Proceeding with VAN initialization."
    (Control returns to the fetching rule, likely `van-mode-map.mdc`).
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/visual-maps/van_mode_split/van-file-verification.mdc",
            "description": "VAN sub-rule for initial Memory Bank file structure verification (DEPRECATED - Logic moved to Core/file-verification.mdc). This file is a placeholder.",
            "globs": "**/visual-maps/van_mode_split/van-file-verification.mdc",
            "alwaysApply": False,
            "body": """
# VAN MODE: FILE VERIFICATION (Placeholder - Logic Moved)

> **TL;DR:** This rule is a placeholder. The primary Memory Bank file verification and creation logic has been consolidated into `.cursor/rules/isolation_rules/Core/file-verification.mdc`.

## ⚙️ AI ACTION:

1.  **Acknowledge:** State: "Note: `van_mode_split/van-file-verification.mdc` is a placeholder. The main file verification logic is in `Core/file-verification.mdc`."
2.  **Guidance:** If you were instructed to perform initial Memory Bank file verification, you should have been (or should be) directed to `fetch_rules` for `.cursor/rules/isolation_rules/Core/file-verification.mdc`.

(Control returns to the fetching rule, likely `van-mode-map.mdc` which should fetch the Core rule directly).
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/visual-maps/van_mode_split/van-complexity-determination.mdc",
            "description": "VAN sub-rule for task complexity determination (DEPRECATED - Logic moved to Core/complexity-decision-tree.mdc). This file is a placeholder.",
            "globs": "**/visual-maps/van_mode_split/van-complexity-determination.mdc",
            "alwaysApply": False,
            "body": """
# VAN MODE: COMPLEXITY DETERMINATION (Placeholder - Logic Moved)

> **TL;DR:** This rule is a placeholder. The primary task complexity determination logic has been consolidated into `.cursor/rules/isolation_rules/Core/complexity-decision-tree.mdc`.

## ⚙️ AI ACTION:

1.  **Acknowledge:** State: "Note: `van_mode_split/van-complexity-determination.mdc` is a placeholder. The main complexity determination logic is in `Core/complexity-decision-tree.mdc`."
2.  **Guidance:** If you were instructed to determine task complexity, you should have been (or should be) directed to `fetch_rules` for `.cursor/rules/isolation_rules/Core/complexity-decision-tree.mdc`.

(Control returns to the fetching rule, likely `van-mode-map.mdc` which should fetch the Core rule directly).
"""
        },
        # --- VAN QA Main Orchestrator ---
        {
            "path": ".cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-main.mdc",
            "description": "Main orchestrator for VAN QA technical validation. Fetched by `van-mode-map.mdc` when 'VAN QA' is triggered. Fetches specific check rules and utility rules.",
            "globs": "**/visual-maps/van_mode_split/van-qa-main.mdc",
            "alwaysApply": False,
            "body": """
# VAN QA: TECHNICAL VALIDATION - MAIN ORCHESTRATOR (AI Instructions)

> **TL;DR:** Orchestrate the four-point technical validation (Dependencies, Configuration, Environment, Minimal Build Test) by fetching specific check rules. Then, fetch reporting and mode transition rules based on results. Use `edit_file` for logging to `activeContext.md`.

## 🧭 VAN QA PROCESS FLOW (AI Actions)

1.  **Acknowledge & Context:**
    a.  State: "VAN QA Main Orchestrator activated. Starting technical validation process."
    b.  `read_file memory-bank/activeContext.md` for current task, complexity, and any relevant tech stack info from CREATIVE phase.
    c.  `read_file memory-bank/tasks.md` for task details.
    d.  `read_file memory-bank/techContext.md` (if it exists and is populated).
    e.  Use `edit_file` to add to `memory-bank/activeContext.md`: "VAN QA Log - [Timestamp]: Starting technical validation."
2.  **Perform Four-Point Validation (Fetch sub-rules sequentially):**
    a.  **Dependency Verification:**
        i.  State: "Performing Dependency Verification."
        ii. `fetch_rules` for `.cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-checks/dependency-check.mdc`.
        iii. (This rule will guide checks and log results to `activeContext.md`). Let `pass_dep_check` be true/false based on its outcome.
    b.  **Configuration Validation (if `pass_dep_check` is true):**
        i.  State: "Performing Configuration Validation."
        ii. `fetch_rules` for `.cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-checks/config-check.mdc`.
        iii. Let `pass_config_check` be true/false.
    c.  **Environment Validation (if `pass_config_check` is true):**
        i.  State: "Performing Environment Validation."
        ii. `fetch_rules` for `.cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-checks/environment-check.mdc`.
        iii. Let `pass_env_check` be true/false.
    d.  **Minimal Build Test (if `pass_env_check` is true):**
        i.  State: "Performing Minimal Build Test."
        ii. `fetch_rules` for `.cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-checks/build-test.mdc`.
        iii. Let `pass_build_check` be true/false.
3.  **Consolidate Results & Generate Report:**
    a.  Overall QA Status: `pass_qa = pass_dep_check AND pass_config_check AND pass_env_check AND pass_build_check`.
    b.  State: "Technical validation checks complete. Overall QA Status: [PASS/FAIL]."
    c.  `fetch_rules` for `.cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-utils/reports.mdc`.
    d.  Follow instructions in `reports.mdc` to use `edit_file` to:
        i.  Generate the full QA report (success or failure format) and display it to the user.
        ii. Write "PASS" or "FAIL" to `memory-bank/.qa_validation_status` (a hidden file for programmatic checks).
4.  **Determine Next Steps:**
    a.  **If `pass_qa` is TRUE:**
        i.  State: "All VAN QA checks passed."
        ii. `fetch_rules` for `.cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-utils/mode-transitions.mdc`.
        iii. (This rule will guide recommending BUILD mode).
    b.  **If `pass_qa` is FALSE:**
        i.  State: "One or more VAN QA checks failed. Please review the report."
        ii. `fetch_rules` for `.cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-utils/common-fixes.mdc`.
        iii. (This rule will provide general fix guidance).
        iv. State: "Please address the issues and then re-type 'VAN QA' to re-run the validation."
5.  **Completion of this Orchestrator:**
    a.  Use `edit_file` to add to `memory-bank/activeContext.md`: "VAN QA Log - [Timestamp]: Technical validation process orchestrated. Outcome: [PASS/FAIL]."
    b.  (Control returns to `van-mode-map.mdc` or awaits user input based on QA outcome).

## 🧰 Utility Rule Reminder:
*   For detailed guidance on how to structure `fetch_rules` calls, you can (if necessary for your own understanding) `read_file` `.cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-utils/rule-calling-guide.mdc` or `rule-calling-help.mdc`. However, this orchestrator explicitly tells you which rules to fetch.
"""
        },
        # --- VAN QA Checks ---
        {
            "path": ".cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-checks/dependency-check.mdc",
            "description": "VAN QA sub-rule for dependency verification. Fetched by `van-qa-main.mdc`. Guides AI to check required dependencies and log results.",
            "globs": "**/visual-maps/van_mode_split/van-qa-checks/dependency-check.mdc",
            "alwaysApply": False,
            "body": """
# VAN QA: DEPENDENCY VERIFICATION (AI Instructions)

> **TL;DR:** Verify project dependencies (e.g., Node.js, npm, Python, pip, specific libraries) are installed and versions are compatible. Log findings to `activeContext.md` using `edit_file`. This rule is fetched by `van-qa-main.mdc`.

## ⚙️ AI ACTIONS FOR DEPENDENCY VERIFICATION:

1.  **Acknowledge & Context:**
    a.  State: "Starting Dependency Verification."
    b.  `read_file memory-bank/techContext.md` and `memory-bank/tasks.md` (or `activeContext.md` if it has tech stack info from CREATIVE phase) to identify key technologies and expected dependencies (e.g., Node.js version, Python version, package manager, specific libraries).
2.  **Define Checks (Based on Context):**
    *   **Example for Node.js project:**
        *   Check Node.js installed and version (e.g., `node -v`).
        *   Check npm installed and version (e.g., `npm -v`).
        *   Check `package.json` exists (e.g., `list_dir .`).
        *   If `package-lock.json` or `yarn.lock` exists, consider running `npm ci` or `yarn install --frozen-lockfile` (or just `npm install`/`yarn install` if less strict) to verify/install packages.
    *   **Example for Python project:**
        *   Check Python installed and version (e.g., `python --version` or `python3 --version`).
        *   Check pip installed (usually comes with Python).
        *   Check `requirements.txt` exists.
        *   Consider creating a virtual environment and `pip install -r requirements.txt`.
3.  **Execute Checks (Using `run_terminal_cmd`):**
    a.  For each defined check:
        i.  Clearly state the command you are about to run.
        ii. `run_terminal_cmd` with the command.
        iii. Record the output.
4.  **Evaluate Results & Log:**
    a.  Based on command outputs, determine if dependencies are met.
    b.  Use `edit_file` to append detailed findings to the "VAN QA Log" in `memory-bank/activeContext.md`:
        ```markdown
        #### Dependency Check Log - [Timestamp]
        - Check: Node.js version
          - Command: `node -v`
          - Output: `v18.12.0`
          - Status: PASS (meets requirement >=16)
        - Check: npm install
          - Command: `npm install`
          - Output: `... up to date ...` or error messages
          - Status: [PASS/FAIL - with error summary if FAIL]
        - ... (other checks) ...
        - Overall Dependency Status: [PASS/FAIL]
        ```
5.  **Completion:**
    a.  State: "Dependency Verification complete. Overall Status: [PASS/FAIL]."
    b.  (The `van-qa-main.mdc` orchestrator will use this outcome).
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-checks/config-check.mdc",
            "description": "VAN QA sub-rule for configuration validation. Fetched by `van-qa-main.mdc`. Guides AI to check project configuration files.",
            "globs": "**/visual-maps/van_mode_split/van-qa-checks/config-check.mdc",
            "alwaysApply": False,
            "body": """
# VAN QA: CONFIGURATION VALIDATION (AI Instructions)

> **TL;DR:** Validate project configuration files (e.g., `package.json` syntax, `tsconfig.json`, linters, build tool configs). Log findings to `activeContext.md` using `edit_file`. This rule is fetched by `van-qa-main.mdc`.

## ⚙️ AI ACTIONS FOR CONFIGURATION VALIDATION:

1.  **Acknowledge & Context:**
    a.  State: "Starting Configuration Validation."
    b.  `read_file memory-bank/techContext.md` and `memory-bank/tasks.md` to identify relevant configuration files based on the project type and technology stack.
2.  **Define Checks (Based on Context):**
    *   **Example for a TypeScript/React project:**
        *   `package.json`: `read_file package.json`. Check for valid JSON structure (conceptually, AI doesn't parse JSON strictly but looks for malformations). Check for essential scripts (`build`, `start`, `test`).
        *   `tsconfig.json`: `read_file tsconfig.json`. Check for valid JSON. Check for key compiler options like `jsx`, `target`, `moduleResolution`.
        *   `.eslintrc.js` or `eslint.config.js`: `read_file [config_name]`. Check for basic structural integrity.
        *   `vite.config.js` or `webpack.config.js`: `read_file [config_name]`. Check for presence of key plugins (e.g., React plugin).
3.  **Execute Checks (Primarily using `read_file` and analysis):**
    a.  For each configuration file:
        i.  `read_file [config_filepath]`.
        ii. Analyze its content against expected structure or key settings.
        iii. For linting/formatting configs, note their presence. Actual linting runs are usually part of build/test steps.
4.  **Evaluate Results & Log:**
    a.  Based on file content analysis, determine if configurations seem correct and complete.
    b.  Use `edit_file` to append detailed findings to the "VAN QA Log" in `memory-bank/activeContext.md`:
        ```markdown
        #### Configuration Check Log - [Timestamp]
        - File: `package.json`
          - Check: Valid JSON structure, presence of `build` script.
          - Status: PASS
        - File: `tsconfig.json`
          - Check: Presence of `jsx: react-jsx`.
          - Status: FAIL (jsx option missing or incorrect)
        - ... (other checks) ...
        - Overall Configuration Status: [PASS/FAIL]
        ```
5.  **Completion:**
    a.  State: "Configuration Validation complete. Overall Status: [PASS/FAIL]."
    b.  (The `van-qa-main.mdc` orchestrator will use this outcome).
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-checks/environment-check.mdc",
            "description": "VAN QA sub-rule for environment validation. Fetched by `van-qa-main.mdc`. Guides AI to check build tools, permissions, etc.",
            "globs": "**/visual-maps/van_mode_split/van-qa-checks/environment-check.mdc",
            "alwaysApply": False,
            "body": """
# VAN QA: ENVIRONMENT VALIDATION (AI Instructions)

> **TL;DR:** Validate the development/build environment (e.g., required CLI tools available, necessary permissions, environment variables). Log findings to `activeContext.md` using `edit_file`. This rule is fetched by `van-qa-main.mdc`.

## ⚙️ AI ACTIONS FOR ENVIRONMENT VALIDATION:

1.  **Acknowledge & Context:**
    a.  State: "Starting Environment Validation."
    b.  `read_file memory-bank/techContext.md` to identify expected environment characteristics (e.g., OS, required CLIs like Git, Docker).
2.  **Define Checks (Based on Context):**
    *   **General Checks:**
        *   Git CLI: `run_terminal_cmd git --version`.
        *   Network connectivity (if external resources needed for build): (Conceptual check, or a simple `ping google.com` if allowed and relevant).
    *   **Example for Web Development:**
        *   Build tool (e.g., Vite, Webpack if used globally): `run_terminal_cmd vite --version` (if applicable).
        *   Port availability (e.g., for dev server): (Conceptual, AI can't directly check. Note if a common port like 3000 or 8080 is usually needed).
    *   **Permissions:**
        *   (Conceptual) Does the AI anticipate needing to write files outside `memory-bank/` or project dir during build? If so, note potential permission needs. Actual permission checks are hard for AI.
3.  **Execute Checks (Using `run_terminal_cmd` where appropriate):**
    a.  For each defined check:
        i.  State the command or check being performed.
        ii. If using `run_terminal_cmd`, record the output.
4.  **Evaluate Results & Log:**
    a.  Based on command outputs and conceptual checks, determine if the environment seems suitable.
    b.  Use `edit_file` to append detailed findings to the "VAN QA Log" in `memory-bank/activeContext.md`:
        ```markdown
        #### Environment Check Log - [Timestamp]
        - Check: Git CLI availability
          - Command: `git --version`
          - Output: `git version 2.30.0`
          - Status: PASS
        - Check: Port 3000 availability for dev server
          - Method: Conceptual (not directly testable by AI)
          - Assumption: Port 3000 should be free.
          - Status: NOTE (User should ensure port is free)
        - ... (other checks) ...
        - Overall Environment Status: [PASS/WARN/FAIL]
        ```
5.  **Completion:**
    a.  State: "Environment Validation complete. Overall Status: [PASS/WARN/FAIL]."
    b.  (The `van-qa-main.mdc` orchestrator will use this outcome).
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-checks/build-test.mdc",
            "description": "VAN QA sub-rule for minimal build test. Fetched by `van-qa-main.mdc`. Guides AI to attempt a basic build/compilation.",
            "globs": "**/visual-maps/van_mode_split/van-qa-checks/build-test.mdc",
            "alwaysApply": False,
            "body": """
# VAN QA: MINIMAL BUILD TEST (AI Instructions)

> **TL;DR:** Attempt a minimal or dry-run build of the project to catch early integration or setup issues. Log findings to `activeContext.md` using `edit_file`. This rule is fetched by `van-qa-main.mdc`.

## ⚙️ AI ACTIONS FOR MINIMAL BUILD TEST:

1.  **Acknowledge & Context:**
    a.  State: "Starting Minimal Build Test."
    b.  `read_file package.json` (or equivalent like `Makefile`, `pom.xml`) to identify build commands.
    c.  `read_file memory-bank/techContext.md` for info on build tools.
2.  **Define Build Command:**
    a.  Identify the primary build script (e.g., `npm run build`, `mvn package`, `make`).
    b.  Consider if a "dry run" or "lint-only" or "compile-only" version of the build command exists to test the toolchain without full artifact generation (e.g., `tsc --noEmit` for TypeScript). If so, prefer it for a *minimal* test. If not, use the standard build command.
3.  **Execute Build Command (Using `run_terminal_cmd`):**
    a.  State the exact build command you are about to run.
    b.  Ensure you are in the correct directory (usually project root). `list_dir .` to confirm presence of `package.json` etc. If not, use `cd` via `run_terminal_cmd`.
    c.  `run_terminal_cmd [build_command]`.
    d.  Capture the full output.
4.  **Evaluate Results & Log:**
    a.  Analyze the output for success messages or error codes/messages.
    b.  Use `edit_file` to append detailed findings to the "VAN QA Log" in `memory-bank/activeContext.md`:
        ```markdown
        #### Minimal Build Test Log - [Timestamp]
        - Command: `npm run build`
        - Output:
          \`\`\`
          [Full or summarized build output]
          \`\`\`
        - Status: [PASS/FAIL - with key error if FAIL]
        - Overall Minimal Build Test Status: [PASS/FAIL]
        ```
5.  **Completion:**
    a.  State: "Minimal Build Test complete. Overall Status: [PASS/FAIL]."
    b.  (The `van-qa-main.mdc` orchestrator will use this outcome).
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-checks/file-verification.mdc",
            "description": "VAN QA sub-rule for specific file/artifact verification post-build or during QA. Fetched by `van-qa-main.mdc` if deeper file checks are needed.",
            "globs": "**/visual-maps/van_mode_split/van-qa-checks/file-verification.mdc",
            "alwaysApply": False,
            "body": """
# VAN QA: DETAILED FILE VERIFICATION (AI Instructions)

> **TL;DR:** Verify existence, content, or structure of specific project files or build artifacts, beyond initial Memory Bank setup. Log findings to `activeContext.md`. This rule is typically fetched by `van-qa-main.mdc` if specific file checks are part of the QA plan.

## ⚙️ AI ACTIONS FOR DETAILED FILE VERIFICATION:

1.  **Acknowledge & Context:**
    a.  State: "Starting Detailed File Verification."
    b.  `read_file memory-bank/tasks.md` or `activeContext.md` to understand which specific files or artifact locations need verification as part of the current QA scope (e.g., "ensure `dist/bundle.js` is created after build", "check `config.yaml` has specific keys").
    c.  If no specific files are targeted for this QA check, state so and this check can be considered trivially PASS.
2.  **Define Checks (Based on QA Scope):**
    *   **Existence Check:** `list_dir [path_to_dir]` to see if `[filename]` is present.
    *   **Content Snippet Check:** `read_file [filepath]` and then search for a specific string or pattern within the content.
    *   **File Size Check (Conceptual):** If a build artifact is expected, `list_dir -l [filepath]` (Unix-like) or `Get-ChildItem [filepath] | Select-Object Length` (PowerShell) might give size. AI notes if it's unexpectedly zero or very small.
    *   **Structure Check (Conceptual for complex files like XML/JSON):** `read_file [filepath]` and describe if it generally conforms to expected structure (e.g., "appears to be valid JSON with a root object containing 'data' and 'errors' keys").
3.  **Execute Checks (Using `list_dir`, `read_file`, or `run_terminal_cmd` for file system info):**
    a.  For each defined file check:
        i.  State the file and the check being performed.
        ii. Execute the appropriate tool/command.
        iii. Record the observation/output.
4.  **Evaluate Results & Log:**
    a.  Based on observations, determine if file verifications pass.
    b.  Use `edit_file` to append findings to the "VAN QA Log" in `memory-bank/activeContext.md`:
        ```markdown
        #### Detailed File Verification Log - [Timestamp]
        - File: `dist/app.js`
          - Check: Existence after build.
          - Observation: File exists.
          - Status: PASS
        - File: `src/config/settings.json`
          - Check: Contains key `"api_url"`.
          - Observation: `read_file` content shows `"api_url": "https://example.com"`.
          - Status: PASS
        - ... (other checks) ...
        - Overall Detailed File Verification Status: [PASS/FAIL]
        ```
5.  **Completion:**
    a.  State: "Detailed File Verification complete. Overall Status: [PASS/FAIL]."
    b.  (The `van-qa-main.mdc` orchestrator will use this outcome).
"""
        },
        # --- VAN QA Utils ---
        {
            "path": ".cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-utils/common-fixes.mdc",
            "description": "VAN QA utility providing common fixes for validation failures. Fetched by `van-qa-main.mdc` on QA fail.",
            "globs": "**/visual-maps/van_mode_split/van-qa-utils/common-fixes.mdc",
            "alwaysApply": False,
            "body": """
# VAN QA: COMMON VALIDATION FIXES (AI Guidance)

> **TL;DR:** Provides common troubleshooting steps and fix suggestions when VAN QA checks fail. This rule is fetched by `van-qa-main.mdc` after a QA failure is reported.

## ⚙️ AI ACTIONS (Present this information to the user):

State: "Here are some common troubleshooting steps based on the type of QA failure. Please review the detailed failure report and attempt these fixes:"

### 1. Dependency Issues:
*   **Missing Tools (Node, Python, Git, etc.):**
    *   "Ensure the required tool ([Tool Name]) is installed and available in your system's PATH. You might need to download it from its official website or install it via your system's package manager."
*   **Incorrect Tool Version:**
    *   "The version of [Tool Name] found is [Found Version], but [Required Version] is expected. Consider using a version manager (like nvm for Node, pyenv for Python) to switch to the correct version, or update/downgrade the tool."
*   **Project Dependencies (`npm install` / `pip install` failed):**
    *   "Check the error messages from the package manager (`npm`, `pip`). Common causes include network issues, permission problems, or incompatible sub-dependencies."
    *   "Try deleting `node_modules/` and `package-lock.json` (or `venv/` and `requirements.txt` conflicts) and running the install command again."
    *   "Ensure your `package.json` or `requirements.txt` is correctly formatted and specifies valid package versions."

### 2. Configuration Issues:
*   **File Not Found:**
    *   "The configuration file `[filepath]` was not found. Ensure it exists at the correct location in your project."
*   **Syntax Errors (JSON, JS, etc.):**
    *   "The file `[filepath]` appears to have syntax errors. Please open it and check for typos, missing commas, incorrect brackets, etc. Using a code editor with linting can help."
*   **Missing Key Settings:**
    *   "The configuration file `[filepath]` is missing an expected setting: `[setting_name]`. Please add it according to the project's requirements (e.g., add `jsx: 'react-jsx'` to `tsconfig.json`)."

### 3. Environment Issues:
*   **Command Not Found (for build tools like `vite`, `tsc`):**
    *   "The command `[command_name]` was not found. If it's a project-local tool, ensure you've run `npm install` (or equivalent) and try prefixing with `npx` (e.g., `npx vite build`). If it's a global tool, ensure it's installed globally."
*   **Permission Denied:**
    *   "An operation failed due to insufficient permissions. You might need to run your terminal/IDE as an administrator (Windows) or use `sudo` (macOS/Linux) for specific commands, but be cautious with `sudo`."
    *   "Check file/folder permissions if trying to write to a restricted area."
*   **Port in Use:**
    *   "The build or dev server tried to use port `[port_number]`, which is already in use. Identify and stop the process using that port, or configure your project to use a different port."

### 4. Minimal Build Test Issues:
*   **Build Script Fails:**
    *   "The command `[build_command]` failed. Examine the full error output from the build process. It often points to missing dependencies, configuration errors, or code syntax issues."
    *   "Ensure all dependencies from `dependency-check.mdc` are resolved first."
*   **Entry Point Errors / Module Not Found:**
    *   "The build process reported it couldn't find a key file or module. Check paths in your configuration files (e.g., `vite.config.js`, `webpack.config.js`) and in your import statements in code."

**General Advice to User:**
"After attempting fixes, please type 'VAN QA' again to re-run the technical validation process."

(Control returns to `van-qa-main.mdc` which awaits user action).
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-utils/mode-transitions.mdc",
            "description": "VAN QA utility for handling mode transitions after QA. Fetched by `van-qa-main.mdc` on QA pass. Guides AI to recommend BUILD mode.",
            "globs": "**/visual-maps/van_mode_split/van-qa-utils/mode-transitions.mdc",
            "alwaysApply": False,
            "body": """
# VAN QA: MODE TRANSITIONS (AI Instructions)

> **TL;DR:** Handles mode transition recommendations after VAN QA validation. If QA passed, recommend BUILD mode. This rule is fetched by `van-qa-main.mdc` after a successful QA.

## ⚙️ AI ACTIONS FOR MODE TRANSITION (POST QA SUCCESS):

1.  **Acknowledge:** State: "VAN QA validation passed successfully."
2.  **Update `activeContext.md`:**
    a.  Use `edit_file` to update `memory-bank/activeContext.md` with:
        ```markdown
        ## VAN QA Status - [Timestamp]
        - Overall Result: PASS
        - Next Recommended Mode: BUILD
        ```
3.  **Recommend BUILD Mode:**
    a.  State: "All technical pre-flight checks are green. The project appears ready for implementation."
    b.  State: "Recommend transitioning to BUILD mode. Type 'BUILD' to begin implementation."
4.  **Await User Confirmation:** Await the user to type 'BUILD' or another command.

## 🔒 BUILD MODE ACCESS (Conceptual Reminder for AI):
*   The system is designed such that if a user tries to enter 'BUILD' mode directly without VAN QA having passed (for tasks requiring it), the BUILD mode orchestrator (or a preceding check) should ideally verify the `.qa_validation_status` file or `activeContext.md` and block if QA was needed but not passed. This current rule (`mode-transitions.mdc`) focuses on the *recommendation* after a *successful* QA.

(Control returns to `van-qa-main.mdc` which awaits user input).
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-utils/reports.mdc",
            "description": "VAN QA utility for generating success/failure reports. Fetched by `van-qa-main.mdc`. Guides AI to format and present QA results using `edit_file`.",
            "globs": "**/visual-maps/van_mode_split/van-qa-utils/reports.mdc",
            "alwaysApply": False,
            "body": """
# VAN QA: VALIDATION REPORTS (AI Instructions)

> **TL;DR:** Generate and present a formatted success or failure report based on the outcomes of the VAN QA checks. Update `activeContext.md` and `.qa_validation_status`. This rule is fetched by `van-qa-main.mdc`.

## ⚙️ AI ACTIONS FOR GENERATING REPORTS:

You will be told by `van-qa-main.mdc` whether the overall QA passed or failed, and will have access to the detailed logs in `activeContext.md`.

1.  **Acknowledge:** State: "Generating VAN QA Report."
2.  **Gather Data from `activeContext.md`:**
    a.  `read_file memory-bank/activeContext.md`.
    b.  Extract the findings from the "VAN QA Log" sections for:
        *   Dependency Check Status & Details
        *   Configuration Check Status & Details
        *   Environment Check Status & Details
        *   Minimal Build Test Status & Details
3.  **Format the Report:**

    **If Overall QA Status is PASS:**
    ```markdown
    ╔═════════════════════ 🔍 QA VALIDATION REPORT ══════════════════════╗
    │ PROJECT: [Project Name from activeContext.md/projectbrief.md]
    │ TIMESTAMP: [Current Date/Time]
    ├─────────────────────────────────────────────────────────────────────┤
    │ 1️⃣ DEPENDENCIES:   ✓ PASS. [Brief summary, e.g., "Node & npm OK"]
    │ 2️⃣ CONFIGURATION:  ✓ PASS. [Brief summary, e.g., "package.json & tsconfig OK"]
    │ 3️⃣ ENVIRONMENT:    ✓ PASS. [Brief summary, e.g., "Git found, permissions assumed OK"]
    │ 4️⃣ MINIMAL BUILD:  ✓ PASS. [Brief summary, e.g., "npm run build script executed successfully"]
    ├─────────────────────────────────────────────────────────────────────┤
    │ 🚨 FINAL VERDICT: PASS                                              │
    │ ➡️ Clear to proceed to BUILD mode.                                  │
    ╚═════════════════════════════════════════════════════════════════════╝
    ```

    **If Overall QA Status is FAIL:**
    ```markdown
    ⚠️⚠️⚠️ QA VALIDATION FAILED ⚠️⚠️⚠️

    Project: [Project Name]
    Timestamp: [Current Date/Time]

    The following issues must be resolved before proceeding to BUILD mode:

    1️⃣ DEPENDENCY ISSUES: [Status: FAIL/WARN]
       - Details: [Extracted from activeContext.md log for dependencies]
       - Recommended Fix: (Refer to common-fixes.mdc or specific error messages)

    2️⃣ CONFIGURATION ISSUES: [Status: FAIL/WARN]
       - Details: [Extracted from activeContext.md log for configurations]
       - Recommended Fix: (Refer to common-fixes.mdc or specific error messages)

    3️⃣ ENVIRONMENT ISSUES: [Status: FAIL/WARN]
       - Details: [Extracted from activeContext.md log for environment]
       - Recommended Fix: (Refer to common-fixes.mdc or specific error messages)

    4️⃣ MINIMAL BUILD TEST ISSUES: [Status: FAIL/WARN]
       - Details: [Extracted from activeContext.md log for build test]
       - Recommended Fix: (Refer to common-fixes.mdc or specific error messages)

    ⚠️ BUILD MODE IS BLOCKED until these issues are resolved.
    Type 'VAN QA' after fixing the issues to re-validate.
    ```
4.  **Present Report to User:**
    a.  Display the formatted report directly to the user in the chat.
5.  **Update `.qa_validation_status` File:**
    a.  Use `edit_file` to write "PASS" or "FAIL" to `memory-bank/.qa_validation_status`. This file acts as a simple flag for other rules.
        *   Example content for PASS: `QA_STATUS: PASS - [Timestamp]`
        *   Example content for FAIL: `QA_STATUS: FAIL - [Timestamp]`
6.  **Log Report Generation in `activeContext.md`:**
    a.  Use `edit_file` to append to `memory-bank/activeContext.md`:
        ```markdown
        #### VAN QA Report Generation - [Timestamp]
        - Overall QA Status: [PASS/FAIL]
        - Report presented to user.
        - `.qa_validation_status` file updated.
        ```
7.  **Completion:** State: "VAN QA Report generated and presented."
    (Control returns to `van-qa-main.mdc`).
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-utils/rule-calling-guide.mdc",
            "description": "VAN QA utility: A reference guide on how to call VAN QA rules. Fetched if AI needs clarification on rule invocation.",
            "globs": "**/visual-maps/van_mode_split/van-qa-utils/rule-calling-guide.mdc",
            "alwaysApply": False,
            "body": """
# VAN QA: COMPREHENSIVE RULE CALLING GUIDE (AI Reference)

> **TL;DR:** This is a reference for understanding how VAN QA rules are structured to be called using `fetch_rules`. You typically won't fetch this rule directly unless you are trying to understand the system's design or if explicitly told to by a higher-level debugging instruction.

## 🔍 RULE CALLING BASICS for CMB System:

1.  **`fetch_rules` is Key:** All `.mdc` rule files in this system are designed to be loaded and executed via the `fetch_rules` tool.
2.  **Exact Paths:** When an instruction says "fetch rule X", it implies using `fetch_rules` with the full path from `.cursor/rules/isolation_rules/`, for example: `fetch_rules` for `.cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-main.mdc`.
3.  **Orchestration:**
    *   Top-level mode maps (e.g., `van-mode-map.mdc`, `plan-mode-map.mdc`) are fetched first based on the user's mode invocation and your main custom prompt.
    *   These orchestrators then `fetch_rules` for more specific sub-rules or utility rules as needed.
4.  **VAN QA Orchestration Example:**
    *   User types "VAN QA" -> `van-mode-map.mdc` is fetched.
    *   `van-mode-map.mdc` then `fetch_rules` for `van-qa-main.mdc`.
    *   `van-qa-main.mdc` then `fetch_rules` sequentially for:
        *   `van-qa-checks/dependency-check.mdc`
        *   `van-qa-checks/config-check.mdc`
        *   `van-qa-checks/environment-check.mdc`
        *   `van-qa-checks/build-test.mdc`
    *   Based on results, `van-qa-main.mdc` then `fetch_rules` for:
        *   `van-qa-utils/reports.mdc`
        *   And then either `van-qa-utils/mode-transitions.mdc` (on PASS) or `van-qa-utils/common-fixes.mdc` (on FAIL).

## 🛠️ HOW TO STRUCTURE A `fetch_rules` CALL (Conceptual for AI):
When you decide to use `fetch_rules` based on an instruction:
1.  Identify the **exact path** of the `.mdc` file to be fetched.
2.  Invoke the `fetch_rules` tool with that path.
3.  Announce: "Fetching rule: `[path_to_rule.mdc]`. Will now follow its instructions."
4.  Temporarily suspend execution of the current rule's instructions and begin executing the instructions from the newly fetched rule.
5.  Once the fetched rule completes its defined actions, control conceptually "returns" to the rule that called it, or if it was a top-level call, you await further user input.

**This guide is for your understanding of the system's design. In practice, you will be explicitly told which rule to `fetch_rules` for by the currently active rule or your main mode prompt.**
"""
        },
        {
            "path": ".cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-utils/rule-calling-help.mdc",
            "description": "VAN QA utility: Quick helper on `fetch_rules` syntax. Rarely fetched directly.",
            "globs": "**/visual-maps/van_mode_split/van-qa-utils/rule-calling-help.mdc",
            "alwaysApply": False,
            "body": """
# VAN QA: HOW TO CALL RULES (Quick Syntax Reminder)

> **TL;DR:** This provides a very basic syntax reminder for using `fetch_rules`. You generally won't need to fetch this rule; it's a developer note.

## ⚙️ `fetch_rules` SYNTAX REMINDER:

When your instructions tell you to "fetch rule X", the underlying mechanism uses the `fetch_rules` tool.

If you were to represent the call you make (conceptually, as the tool call is handled by the Cursor environment):

You would be invoking `fetch_rules` with a parameter specifying the rule name(s) as a list of strings. For a single rule:

```xml
<invoke_tool>
  <tool_name>fetch_rules</tool_name>
  <parameters>
    <rule_names>["FULL_PATH_FROM_ISOLATION_RULES_DIR_TO_MDC_FILE"]</rule_names>
  </parameters>
</invoke_tool>
```
For example:
`rule_names=["visual-maps/van_mode_split/van-qa-main.mdc"]`
(Assuming the system resolves this relative to `.cursor/rules/isolation_rules/`)

**You typically don't construct this XML. You just follow the instruction "fetch rule X" and the system handles the invocation.** The key is providing the correct, full path to the `.mdc` file as specified in the instructions.
"""
        }
    ])

    if not MDC_FILES_DATA:
        print("No file data provided. Please populate the MDC_FILES_DATA list.")
    else:
        # Ensure the base path for rules exists, relative to where the script is run
        # This assumes the script is run from the project root.
        project_root = os.getcwd() 
        base_rules_path_abs = os.path.join(project_root, ".cursor", "rules", "isolation_rules")

        if not os.path.exists(base_rules_path_abs):
            # This case should ideally not happen if Core rules were already made,
            # but it's a safeguard if only visual-maps are being generated by a modified script.
            print(f"Base directory {base_rules_path_abs} does not exist. Please ensure Core rules are generated first or the path is correct.")
            # os.makedirs(base_rules_path_abs, exist_ok=True) # Optionally create it

        for file_data in MDC_FILES_DATA:
            # Construct absolute path for file operations
            absolute_filepath = os.path.join(project_root, file_data["path"])
            
            create_or_update_mdc_file(
                absolute_filepath, # Use absolute path for writing
                file_data["description"],
                file_data["globs"], # Globs are relative to .cursor/rules/ for Cursor's matching
                file_data["alwaysApply"],
                file_data["body"]
            )
        print("\n--- MDC file generation process complete. ---")
        print(f"NOTE: This script overwrites existing files with the defined content in their respective paths, relative to project root: {project_root}")
        print("Ensure that the 'globs' in the .mdc files are correctly specified for Cursor's rule matching (usually relative to the .cursor/rules/ directory).")