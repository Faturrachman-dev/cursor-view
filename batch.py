import os

# --- Define your MDC file data here ---
# Add an entry for each .mdc file you want to create/update.
# I'll start with the two visual-map files we just refined as examples.
# You will need to meticulously copy the refined content for each file.

MDC_FILES_DATA = [
    {
        "path": ".cursor/rules/isolation_rules/visual-maps/archive-mode-map.mdc",
        "description": "Orchestrates the ARCHIVE mode process for the Memory Bank system, focusing on creating comprehensive documentation, archiving files, and updating Memory Bank for task completion. To be fetched when ARCHIVE process is initiated.",
        "globs": "**/visual-maps/archive-mode-map.mdc",
        "alwaysApply": False,
        "body": """
# ARCHIVE MODE: TASK DOCUMENTATION PROCESS MAP (AI Instructions)

> **TL;DR:** Your role is to finalize task documentation, create an archive record, and update the Memory Bank. Use `edit_file` for all document creation and updates.

## 🧭 ARCHIVE MODE PROCESS FLOW (AI Actions)

1.  **Acknowledge & Gather Context:**
    a.  State: "Initiating ARCHIVE process for [Task Name - infer from activeContext.md or tasks.md]."
    b.  Use `read_file` to load `memory-bank/tasks.md`. Identify the completed task and its complexity level.
    c.  Use `read_file` to load `memory-bank/reflection/reflect-[task_id_or_feature_name]-[date].md` (determine filename from `tasks.md` or `activeContext.md`).
    d.  Use `read_file` to load `memory-bank/progress.md`.
    e.  Use `read_file` to load `memory-bank/activeContext.md` for any final implementation notes or links to creative documents.

2.  **Determine Archiving Detail (Based on Complexity from `tasks.md`):**
    *   **Level 1 (Quick Bug Fix):**
        i.  Use `fetch_rules` to load and follow instructions from `.cursor/rules/isolation_rules/Level1/archive-minimal.mdc`.
    *   **Level 2 (Simple Enhancement):**
        i.  Use `fetch_rules` to load and follow instructions from `.cursor/rules/isolation_rules/Level2/archive-basic.mdc`.
    *   **Level 3 (Intermediate Feature):**
        i.  Use `fetch_rules` to load and follow instructions from `.cursor/rules/isolation_rules/Level3/archive-intermediate.mdc`.
    *   **Level 4 (Complex System):**
        i.  Use `fetch_rules` to load and follow instructions from `.cursor/rules/isolation_rules/Level4/archive-comprehensive.mdc`.

3.  **Create Archive Document (Guided by Level-Specific Rule):**
    a.  The fetched level-specific rule will instruct you on the path and content for the archive document.
    b.  Use `edit_file` to create and populate this document.

4.  **Final Memory Bank Updates (Guided by Level-Specific Rule):**
    a.  **`tasks.md`**: Use `edit_file` to mark the main task as `[x] COMPLETED & ARCHIVED: [path_to_archive_document]`.
    b.  **`progress.md`**: Use `edit_file` to add a final entry summarizing completion and linking to the archive document.
    c.  **`activeContext.md`**: Use `edit_file` to reset its content:
        ```markdown
        # Active Context
        ## Current Mode: ARCHIVE (Completed)
        ## Focus: Ready for new task.
        ## Previous Task: [Task Name] - Archived at [path_to_archive_document]
        ## Next Steps: Suggest VAN mode for new task.
        ```

5.  **Notify User of Completion:**
    State: "ARCHIVING COMPLETE for [Task Name]. Archive created at: `[path_to_archive_document]`. Suggest VAN mode for new task."

## 📊 REQUIRED FILE STATE VERIFICATION (AI Self-Check before Archiving)
1.  Is `tasks.md` marked with "Reflection complete" for the current task?
2.  Does `memory-bank/reflection/reflect-[task_id_or_feature_name]-[date].md` exist?
3.  Is `progress.md` updated?
*(If checks fail, state the issue and suggest returning to REFLECT mode.)*
"""
    },
    {
        "path": ".cursor/rules/isolation_rules/visual-maps/creative-mode-map.mdc",
        "description": "Orchestrates the CREATIVE mode process for the Memory Bank system, guiding design decisions for components flagged during planning. To be fetched by the main PLAN mode instructions.",
        "globs": "**/visual-maps/creative-mode-map.mdc",
        "alwaysApply": False,
        "body": """
# CREATIVE MODE: DESIGN PROCESS MAP (AI Instructions)

> **TL;DR:** Your role is to facilitate structured design decision-making for components flagged in `tasks.md`. Use `fetch_rules` for specific design-type guidance and `edit_file` for all documentation.

## 🧭 CREATIVE MODE PROCESS FLOW (AI Actions)

1.  **Acknowledge & Gather Context:**
    a.  State: "OK CREATIVE. Identifying components requiring creative design."
    b.  Use `read_file` to load `memory-bank/tasks.md`. Look for sub-tasks like "- [ ] CREATIVE: Design [component_name] - Type: [Architecture/Algorithm/UI-UX]".
    c.  Use `read_file` to load `memory-bank/activeContext.md` for overall project context.
    d.  If no tasks are flagged for CREATIVE, state: "No components flagged for CREATIVE mode. Recommend IMPLEMENT or update PLAN." Await user instruction.

2.  **Iterate Through Flagged Creative Tasks:** For each "CREATIVE: Design..." sub-task:
    a.  **Announce Focus:** "Entering CREATIVE phase for: [Component Name] - Design Type: [Type]."
    b.  **Fetch Design-Type Specific Rules:**
        *   Architecture: `fetch_rules` for `.cursor/rules/isolation_rules/Phases/CreativePhase/creative-phase-architecture.mdc`.
        *   Algorithm: `fetch_rules` for `.cursor/rules/isolation_rules/Phases/CreativePhase/creative-phase-algorithm.mdc`.
        *   UI/UX: `fetch_rules` for `.cursor/rules/isolation_rules/Phases/CreativePhase/creative-phase-uiux.mdc`.
    c.  **Follow Fetched Rule to Generate Design Document:**
        i.  The fetched rule guides defining requirements, exploring options, analysis, decision, and implementation guidelines.
        ii. Use `edit_file` to create/update `memory-bank/creative/creative-[component_name].md`.
        iii. Use the template from `.cursor/rules/isolation_rules/Phases/CreativePhase/optimized-creative-template.mdc` (which you can `read_file`) for structure.
    d.  **Update `activeContext.md`:** Use `edit_file` to append summary to "Creative Decisions": "- [Component]: Design complete. Recommended [Approach]. See `creative/creative-[component_name].md`."
    e.  **Update `tasks.md`:** Use `edit_file` to mark sub-task: `[x] CREATIVE: Design [component_name] - Decision in creative/creative-[component_name].md`.

3.  **Overall Verification & Transition:**
    a.  State: "CREATIVE mode complete. All designated components have design documentation."
    b.  Recommend: "Recommend transitioning to IMPLEMENT mode." (Or VAN QA if applicable).

## 📊 REQUIRED FILE STATE VERIFICATION (AI Self-Check before starting CREATIVE)
1.  Does `tasks.md` show "Planning complete" for the parent feature?
2.  Are sub-tasks in `tasks.md` marked for "CREATIVE: Design..."?
*(If checks fail, state issue and suggest PLAN mode.)*
"""
    },
    # --- ADD MORE FILE DICTIONARIES HERE FOR EACH REFINED MDC ---
    # Example for a Core rule we refined:
    {
        "path": ".cursor/rules/isolation_rules/Core/command-execution.mdc",
        "description": "Core guidelines for AI command execution, emphasizing tool priority (edit_file, fetch_rules, run_terminal_cmd), platform awareness, and result documentation within the Memory Bank system.",
        "globs": "**/Core/command-execution.mdc",
        "alwaysApply": False, # Or True if you decide it should always be implicitly available
        "body": """
# COMMAND EXECUTION SYSTEM

> **TL;DR:** This system provides guidelines for efficient and reliable command and tool usage. Prioritize `edit_file` for file content, `fetch_rules` for loading `.mdc` rules, and `run_terminal_cmd` for execution tasks. Always document actions and results in `memory-bank/activeContext.md`.

## 🛠️ TOOL PRIORITY & USAGE
# ... (rest of the refined content for command-execution.mdc) ...
"""
    },
    # Add all other refined Core, LevelX, Phases, visual-maps/*.mdc files here
]

def create_or_update_mdc_file(filepath, description, globs, always_apply, body_content):
    """Creates or updates an .mdc file with the given frontmatter and body."""
    
    # Construct frontmatter
    # Ensure boolean is lowercase 'true' or 'false' for YAML
    always_apply_str = 'true' if always_apply else 'false'
    frontmatter = f"""---
description: {description}
globs: "{globs}"
alwaysApply: {always_apply_str}
---
"""
    
    full_content = frontmatter + body_content.strip() #.strip() to remove leading/trailing whitespace from body

    try:
        # Ensure directory exists
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
    if not MDC_FILES_DATA:
        print("No file data provided. Please populate the MDC_FILES_DATA list.")
    else:
        # Create the .cursor/rules/isolation_rules base path if it doesn't exist
        # This ensures relative paths in MDC_FILES_DATA work correctly
        # if the script is run from the project root.
        base_rules_path = ".cursor/rules/isolation_rules"
        if not os.path.exists(base_rules_path):
            os.makedirs(base_rules_path, exist_ok=True)
            print(f"Ensured base directory exists: {base_rules_path}")

        for file_data in MDC_FILES_DATA:
            create_or_update_mdc_file(
                file_data["path"],
                file_data["description"],
                file_data["globs"],
                file_data["alwaysApply"], # Corrected key name
                file_data["body"]
            )
        print("\n--- MDC file generation process complete. ---")
        print("NOTE: This script overwrites existing files with the defined content.")