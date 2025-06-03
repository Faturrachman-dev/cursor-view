import os

# --- Define your MDC file data here ---
# Each dictionary contains the file path and its complete, text-only content (including frontmatter).
MDC_FILES_DATA = [
    {
        "path": ".cursor/rules/isolation_rules/STRUCTURE.md",
        "content": """
```
└── 📁isolation_rules
    └── 📁Core
        └── command-execution.mdc
        └── complexity-decision-tree.mdc
        └── creative-phase-enforcement.mdc
        └── creative-phase-metrics.mdc
        └── file-verification.mdc
        └── hierarchical-rule-loading.mdc
        └── memory-bank-paths.mdc
        └── mode-transition-optimization.mdc
        └── optimization-integration.mdc
        └── platform-awareness.mdc
    └── 📁Level1
        └── optimized-workflow-level1.mdc
        └── quick-documentation.mdc
        └── workflow-level1.mdc
    └── 📁Level2
        └── archive-basic.mdc
        └── reflection-basic.mdc
        └── task-tracking-basic.mdc
        └── workflow-level2.mdc
    └── 📁Level3
        └── archive-intermediate.mdc
        └── implementation-intermediate.mdc
        └── planning-comprehensive.mdc
        └── reflection-intermediate.mdc
        └── task-tracking-intermediate.mdc
        └── workflow-level3.mdc
    └── 📁Level4
        └── architectural-planning.mdc
        └── archive-comprehensive.mdc
        └── phased-implementation.mdc
        └── reflection-comprehensive.mdc
        └── task-tracking-advanced.mdc
        └── workflow-level4.mdc
    └── 📁Phases
        └── 📁CreativePhase
            └── creative-phase-architecture.mdc
            └── creative-phase-uiux.mdc
            └── optimized-creative-template.mdc
    └── 📁visual-maps
        └── archive-mode-map.mdc
        └── creative-mode-map.mdc
        └── implement-mode-map.mdc
        └── plan-mode-map.mdc
        └── qa-mode-map.mdc
        └── reflect-mode-map.mdc
        └── 📁van_mode_split
            └── van-complexity-determination.mdc
            └── van-file-verification.mdc
            └── van-mode-map.mdc
            └── van-platform-detection.mdc
            └── 📁van-qa-checks
                └── build-test.mdc
                └── config-check.mdc
                └── dependency-check.mdc
                └── environment-check.mdc
                └── file-verification.mdc
            └── van-qa-main.mdc
            └── 📁van-qa-utils
                └── common-fixes.mdc
                └── mode-transitions.mdc
                └── reports.mdc
                └── rule-calling-guide.mdc
                └── rule-calling-help.mdc
            └── van-qa-validation.md.old
        └── van-mode-map.mdc
    └── main-optimized.mdc
    └── main.mdc
```
"""
    },
    {
        "path": ".cursor/rules/isolation_rules/visual-maps/van-mode-map.mdc",
        "content": """---
description: Visual process map for VAN mode (Initialization)
globs: van-mode-map.mdc
alwaysApply: false
---
# VAN MODE: INITIALIZATION PROCESS MAP

> **TL;DR:** This document defines the VAN mode process for project initialization, task analysis, and technical validation. It guides users through platform detection, file verification, complexity determination, and technical validation to ensure proper setup before implementation.

## 🧭 VAN MODE PROCESS FLOW (AI Actions)

This flow describes the sequential steps you will take when operating in VAN Mode.

1.  **Acknowledge & Determine Entry Point:**
    *   If user typed "VAN": Respond "OK VAN - Beginning Initialization Process." Proceed with step 2.
    *   If user typed "VAN QA": Respond "OK VAN QA - Beginning Technical Validation." Skip to **Step 7 (VAN QA)**.

2.  **Initial Problem Intake & Quick Triage:**
    a.  State: "Performing initial problem intake and quick triage."
    b.  `read_file` the user's prompt and any immediately provided context files (like `error-delete-chat.txt`).
    c.  `read_file` the 1-2 most directly implicated source files if obvious from the error/request (e.g., `server.py` if an API error is mentioned).
    d.  **Decision Point - Quick Fix Assessment:**
        *   Based on this *very limited initial review*, can you confidently identify:
            1.  A highly localized problem (e.g., affects only one function or a few lines in one file)?
            2.  A clear root cause?
            3.  A simple, low-risk fix (e.g., correcting a variable name, adjusting a simple conditional, fixing a property access path like in the delete_chat example)?
            4.  The fix requires no new dependencies or significant design changes?
        *   **If YES to all above (High Confidence, Simple Fix):**
            i.  State: "Initial analysis suggests a straightforward Level 0/1 fix for [brief problem description]."
            ii. `edit_file memory-bank/tasks.md` to create a task: "L0/1 Quick Fix: [Problem Description]".
            iii. `edit_file memory-bank/activeContext.md` to log: "Focus: L0/1 Quick Fix - [Problem]. Initial diagnosis: [Root Cause]. Proposed fix: [Brief Fix]."
            iv. `fetch_rules` to load and follow `.cursor/rules/isolation_rules/Level1/optimized-workflow-level1.mdc`.
                *   (This rule already guides: implement fix, verify, document concisely in `tasks.md`/`activeContext.md`, then state completion and readiness for a new task).
            v.  **After `Level1/optimized-workflow-level1.mdc` completes, the VAN mode for THIS SPECIFIC QUICK TASK is considered complete.** State this and await further user instruction (e.g., new VAN for another task, or switch to another mode).
            vi. **SKIP to Step 8 (QA Command Precedence Check & End of VAN for this task).**
        *   **If NO (Problem is not immediately obvious/simple, or any uncertainty):**
            i.  State: "Initial triage indicates further analysis is needed. Proceeding with standard VAN initialization."
            ii. Proceed to Step 3.

3.  **Platform Detection (Sub-Rule - Standard VAN Path):**
    a.  State: "Performing platform detection."
    b.  `fetch_rules` to load and follow `.cursor/rules/isolation_rules/visual-maps/van_mode_split/van-platform-detection.mdc`.
    c.  (This fetched rule will guide OS detection and logging to `activeContext.md`).

4.  **File Verification & Creation (Memory Bank Setup) (Sub-Rule - Standard VAN Path):**
    a.  State: "Performing Memory Bank file verification and setup."
    b.  `fetch_rules` to load and follow `.cursor/rules/isolation_rules/Core/file-verification.mdc`.
    c.  (This fetched rule guides creating/verifying `memory-bank/` structure and core files).

5.  **Full Context Analysis & Complexity Determination (Sub-Rule - Standard VAN Path):**
    a.  State: "Performing detailed context analysis and determining task complexity."
    b.  `read_file` relevant project files (README, main source files, etc.) as needed for a broader understanding.
    c.  `fetch_rules` to load and follow `.cursor/rules/isolation_rules/Core/complexity-decision-tree.mdc`.
    d.  (This fetched rule guides assessing Level 1-4 and updating `activeContext.md` and `tasks.md`).
    e.  `read_file memory-bank/activeContext.md` to confirm the determined complexity level.

6.  **Mode Transition based on Complexity (Standard VAN Path):**
    a.  **If Level 1 determined (and not handled by Quick Triage):**
        i.  State: "Task assessed as Level 1. Completing VAN initialization."
        ii. Use `edit_file` to update `memory-bank/activeContext.md` with: "VAN Process Status: Level 1 Initialization Complete. Task ready for IMPLEMENT mode."
        iii. State: "VAN Initialization Complete for Level 1 task [Task Name]. Recommend IMPLEMENT mode." Await user.
    b.  **If Level 2, 3, or 4 determined:**
        i.  State: "🚫 LEVEL [2/3/4] TASK DETECTED: [Task Name]. This task REQUIRES detailed planning."
        ii. State: "Transitioning to PLAN mode is necessary. Type 'PLAN' to proceed with planning." Await user.

7.  **VAN QA - Technical Validation (Entry point if "VAN QA" was typed, or if called after CREATIVE mode by user):**
    a.  State: "Initiating VAN QA Technical Validation."
    b.  `fetch_rules` to load and follow `.cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-main.mdc`.
    c.  (This rule handles the QA process). Await user action based on QA report.

8.  **QA COMMAND PRECEDENCE (If user types "QA" during steps 3-6 of Standard VAN Initialization):**
    a.  State: "General QA command received, pausing current VAN initialization step ([current step])."
    b.  `fetch_rules` to load and follow `.cursor/rules/isolation_rules/visual-maps/qa-mode-map.mdc`.
    c.  After general QA is complete: State "Resuming VAN initialization." Continue from paused step.

## 🌐 PLATFORM DETECTION PROCESS

This section describes the platform detection process.

**Process Flow:**
1.  **Platform Detection.**
2.  **Detect Operating System:** Branches to Windows, macOS, or Linux detection.
3.  **Windows, macOS, or Linux -> Adapt Commands for Platform.**
4.  **Adapt Commands -> Path Separator Detection.**
    *   Windows Path: Backslash (`\`).
    *   macOS Path: Forward Slash (`/`).
    *   Linux Path: Forward Slash (`/`).
5.  **Path Separator Detection -> Command Checkpoint.**
    *   Windows Command Adaptations: `dir`, `icacls`, etc.
    *   macOS Command Adaptations: `ls`, `chmod`, etc.
    *   Linux Command Adaptations: `ls`, `chmod`, etc.
6.  **Path Separator Checkpoint & Command Checkpoint -> Platform Detection Complete.**

## 📁 FILE VERIFICATION PROCESS

This section describes the file verification process.

**Process Flow:**
1.  **File Verification.**
2.  **Check Essential Files.**
3.  **Check Memory Bank Structure.**
4.  **Memory Bank Exists?**
    *   If "Yes": Verify Memory Bank Contents.
    *   If "No": Create Memory Bank Structure.
5.  **Check Essential Files -> Check Documentation Files.**
6.  **Docs Exist?**
    *   If "Yes": Verify Documentation Structure.
    *   If "No": Create Documentation Structure.
7.  **Verify/Create Memory Bank & Verify/Create Docs -> Memory Bank Checkpoint & Documentation Checkpoint.**
8.  **Memory Bank Checkpoint & Documentation Checkpoint -> File Verification Complete.**

## 🧩 COMPLEXITY DETERMINATION PROCESS

This section describes the complexity determination process.

**Process Flow:**
1.  **Complexity Determination.**
2.  **Analyze Task Requirements.**
3.  **Analyze Task Requirements -> Check Task Keywords.**
4.  **Check Task Keywords -> Assess Scope Impact.**
5.  **Assess Scope Impact -> Evaluate Risk Level.**
6.  **Evaluate Risk Level -> Estimate Implementation Effort.**
7.  **Estimate Implementation Effort -> Determine Complexity Level.**
    *   If "Level 1": Level 1: Quick Bug Fix.
    *   If "Level 2": Level 2: Simple Enhancement.
    *   If "Level 3": Level 3: Intermediate Feature.
    *   If "Level 4": Level 4: Complex System.
8.  **Level 1 -> Complexity Determination Complete.**
9.  **Level 2, 3, or 4 -> Force Mode Switch to PLAN.**

## 🔄 COMPLETE WORKFLOW WITH QA VALIDATION

This section describes the complete workflow, including QA validation.

**Workflow Flow:**
*   VAN MODE (Initial Analysis) -> PLAN MODE (Task Planning) -> CREATIVE MODE (Design Decisions) -> VAN QA MODE (Technical Validation) -> BUILD MODE (Implementation).

## 🔍 TECHNICAL VALIDATION OVERVIEW

This section provides an overview of the four-point technical validation process.

**Validation Flow:**
1.  **VAN QA MODE.**
2.  **FOUR-POINT VALIDATION.**
3.  **1️⃣ DEPENDENCY VERIFICATION:** Check all required packages.
4.  **2️⃣ CONFIGURATION VALIDATION:** Verify format & compatibility.
5.  **3️⃣ ENVIRONMENT VALIDATION:** Check build environment.
6.  **4️⃣ MINIMAL BUILD TEST:** Test core functionality.
7.  **MINIMAL BUILD TEST -> All Checks Passed?**
    *   If "Yes": GENERATE SUCCESS REPORT -> Proceed to BUILD MODE.
    *   If "No": GENERATE FAILURE REPORT -> Fix Technical Issues -> Re-validate.

## 📝 VALIDATION STATUS FORMAT

```
╔═════════════════ 🔍 QA VALIDATION STATUS ═════════════════╗
│ ✓ Design Decisions   │ Verified as implementable          │
│ ✓ Dependencies       │ All required packages installed    │
│ ✓ Configurations     │ Format verified for platform       │
│ ✓ Environment        │ Suitable for implementation        │
╚════════════════════════════════════════════════════════════╝
✅ VERIFIED - Clear to proceed to BUILD mode
```

## 🚨 MODE TRANSITION TRIGGERS

### VAN to PLAN Transition
For complexity levels 2-4:
```
🚫 LEVEL [2-4] TASK DETECTED
Implementation in VAN mode is BLOCKED
This task REQUIRES PLAN mode
You MUST switch to PLAN mode for proper documentation and planning
Type 'PLAN' to switch to planning mode
```

### CREATIVE to VAN QA Transition
After completing the CREATIVE mode:
```
⏭️ NEXT MODE: VAN QA
To validate technical requirements before implementation, please type 'VAN QA'
```

### VAN QA to BUILD Transition
After successful validation:
```
✅ TECHNICAL VALIDATION COMPLETE
All prerequisites verified successfully
You may now proceed to BUILD mode
Type 'BUILD' to begin implementation
```

## 🔒 BUILD MODE PREVENTION MECHANISM

This section describes how the system prevents moving to BUILD mode without passing QA validation.

**Process Flow:**
1.  **Start: User Types: BUILD.**
2.  **QA Validation Completed?**
    *   If "Yes and Passed": Allow BUILD Mode.
    *   If "No or Failed": BLOCK BUILD MODE.
3.  **BLOCK BUILD MODE -> Display: ⚠️ QA VALIDATION REQUIRED.**
4.  **Display -> Prompt: Type VAN QA.**

## 🔄 QA COMMAND PRECEDENCE

QA validation can be called at any point in the process flow, and takes immediate precedence over any other current steps, including forced mode switches.

**Process Flow:**
1.  **User Types: QA.**
2.  **⚠️ HIGH PRIORITY COMMAND.**
3.  **Pause Current Task/Process.**
4.  **Load QA Mode Map.**
5.  **Execute QA Validation Process.**
6.  **QA Results.**
    *   If "PASS": Resume Prior Process Flow.
    *   If "FAIL": Fix Identified Issues -> Re-run QA Validation.

### QA Interruption Rules

When a user types **QA** at any point:

1. **The QA command MUST take immediate precedence** over any current operation, including the "FORCE MODE SWITCH" triggered by complexity assessment.
2. The system MUST:
   - Immediately load the QA mode map
   - Execute the full QA validation process
   - Address any failures before continuing
3. **Required remediation steps take priority** over any pending mode switches or complexity rules
4. After QA validation is complete and passes:
   - Resume the previously determined process flow
   - Continue with any required mode switches

```
⚠️ QA OVERRIDE ACTIVATED
All other processes paused
QA validation checks now running...
Any issues found MUST be remediated before continuing with normal process flow
```

## 📋 CHECKPOINT VERIFICATION TEMPLATE

Each major checkpoint in VAN mode uses this format:

```
✓ SECTION CHECKPOINT: [SECTION NAME]
- Requirement 1? [YES/NO]
- Requirement 2? [YES/NO]
- Requirement 3? [YES/NO]

→ If all YES: Ready for next section
→ If any NO: Fix missing items before proceeding
```

## 🚀 VAN MODE ACTIVATION

When the user types "VAN", respond with a confirmation and start the process:

```
User: VAN

Response: OK VAN - Beginning Initialization Process
```

After completing CREATIVE mode, when the user types "VAN QA", respond:

```
User: VAN QA

Response: OK VAN QA - Beginning Technical Validation
```

This ensures clear communication about which phase of VAN mode is active. 

## 🔍 DETAILED QA VALIDATION PROCESS

### 1️⃣ DEPENDENCY VERIFICATION

This step verifies that all required packages are installed and compatible.

**Process Flow:**
1.  **Start: Dependency Verification.**
2.  **Read Required Dependencies:** From Creative Phase.
3.  **Check if Dependencies are Installed.**
4.  **All Dependencies Installed?**
    *   If "Yes": Verify Versions and Compatibility.
    *   If "No": Install Missing Dependencies -> Verify Versions.
5.  **Versions Compatible?**
    *   If "Yes": Dependencies Verified ✅ PASS.
    *   If "No": Upgrade/Downgrade as Needed -> Retry Verification.

#### Windows (PowerShell) Implementation:
```powershell
# Example: Verify Node.js dependencies for a React project
function Verify-Dependencies {
    $requiredDeps = @{
        "node" = ">=14.0.0"
        "npm" = ">=6.0.0"
    }
    
    $missingDeps = @()
    $incompatibleDeps = @()
    
    # Check Node.js version
    $nodeVersion = $null
    try {
        $nodeVersion = node -v
        if ($nodeVersion -match "v(\d+)\.(\d+)\.(\d+)") {
            $major = [int]$Matches[1]
            if ($major -lt 14) {
                $incompatibleDeps += "node (found $nodeVersion, required >=14.0.0)"
            }
        }
    } catch {
        $missingDeps += "node"
    }
    
    # Check npm version
    $npmVersion = $null
    try {
        $npmVersion = npm -v
        if ($npmVersion -match "(\d+)\.(\d+)\.(\d+)") {
            $major = [int]$Matches[1]
            if ($major -lt 6) {
                $incompatibleDeps += "npm (found $npmVersion, required >=6.0.0)"
            }
        }
    } catch {
        $missingDeps += "npm"
    }
    
    # Display results
    if ($missingDeps.Count -eq 0 -and $incompatibleDeps.Count -eq 0) {
        Write-Output "✅ All dependencies verified and compatible"
        return $true
    } else {
        if ($missingDeps.Count -gt 0) {
            Write-Output "❌ Missing dependencies: $($missingDeps -join ', ')"
        }
        if ($incompatibleDeps.Count -gt 0) {
            Write-Output "❌ Incompatible versions: $($incompatibleDeps -join ', ')"
        }
        return $false
    }
}
```

#### Mac/Linux (Bash) Implementation:
```bash
#!/bin/bash

# Example: Verify Node.js dependencies for a React project
verify_dependencies() {
    local missing_deps=()
    local incompatible_deps=()
    
    # Check Node.js version
    if command -v node &> /dev/null; then
        local node_version=$(node -v)
        if [[ $node_version =~ v([0-9]+)\.([0-9]+)\.([0-9]+) ]]; then
            local major=${BASH_REMATCH[1]}
            if (( major < 14 )); then
                incompatible_deps+=("node (found $node_version, required >=14.0.0)")
            fi
        fi
    else
        missing_deps+=("node")
    fi
    
    # Check npm version
    if command -v npm &> /dev/null; then
        local npm_version=$(npm -v)
        if [[ $npm_version =~ ([0-9]+)\.([0-9]+)\.([0-9]+) ]]; then
            local major=${BASH_REMATCH[1]}
            if (( major < 6 )); then
                incompatible_deps+=("npm (found $npm_version, required >=6.0.0)")
            fi
        fi
    else
        missing_deps+=("npm")
    fi
    
    # Display results
    if [ ${#missing_deps[@]} -eq 0 ] && [ ${#incompatible_deps[@]} -eq 0 ]; then
        echo "✅ All dependencies verified and compatible"
        return 0
    else
        if [ ${#missing_deps[@]} -gt 0 ]; then
            echo "❌ Missing dependencies: ${missing_deps[*]}"
        fi
        if [ ${#incompatible_deps[@]} -gt 0 ]; then
            echo "❌ Incompatible versions: ${incompatible_deps[*]}"
        fi
        return 1
    fi
}
```

### 2️⃣ CONFIGURATION VALIDATION

This step validates configuration files format and compatibility.

**Process Flow:**
1.  **Start: Configuration Validation.**
2.  **Identify Configuration Files.**
3.  **Read Configuration Files.**
4.  **Validate Syntax and Format.**
5.  **Syntax Valid?**
    *   If "Yes": Check Compatibility with Platform.
    *   If "No": Fix Syntax Errors -> Retry Validation.
6.  **Compatible with Platform?**
    *   If "Yes": Configurations Validated ✅ PASS.
    *   If "No": Adapt Configurations for Platform -> Retry Compatibility Check.

#### Configuration Validation Implementation:
```powershell
# Example: Validate configuration files for a web project
function Validate-Configurations {
    $configFiles = @(
        "package.json",
        "tsconfig.json",
        "vite.config.js"
    )
    
    $invalidConfigs = @()
    $incompatibleConfigs = @()
    
    foreach ($configFile in $configFiles) {
        if (Test-Path $configFile) {
            # Check JSON syntax for JSON files
            if ($configFile -match "\.json$") {
                try {
                    Get-Content $configFile -Raw | ConvertFrom-Json | Out-Null
                } catch {
                    $invalidConfigs += "$configFile (JSON syntax error: $($_.Exception.Message))"
                    continue
                }
            }
            
            # Specific configuration compatibility checks
            if ($configFile -eq "vite.config.js") {
                $content = Get-Content $configFile -Raw
                # Check for React plugin in Vite config
                if ($content -notmatch "react\(\)") {
                    $incompatibleConfigs += "$configFile (Missing React plugin for React project)"
                }
            }
        } else {
            $invalidConfigs += "$configFile (file not found)"
        }
    }
    
    # Display results
    if ($invalidConfigs.Count -eq 0 -and $incompatibleConfigs.Count -eq 0) {
        Write-Output "✅ All configurations validated and compatible"
        return $true
    } else {
        if ($invalidConfigs.Count -gt 0) {
            Write-Output "❌ Invalid configurations: $($invalidConfigs -join ', ')"
        }
        if ($incompatibleConfigs.Count -gt 0) {
            Write-Output "❌ Incompatible configurations: $($incompatibleConfigs -join ', ')"
        }
        return $false
    }
}
```

### 3️⃣ ENVIRONMENT VALIDATION

This step checks if the environment is properly set up for the implementation.

**Process Flow:**
1.  **Start: Environment Validation.**
2.  **Check Build Environment.**
3.  **Verify Build Tools.**
4.  **Build Tools Available?**
    *   If "Yes": Check Permissions and Access.
    *   If "No": Install Required Build Tools -> Retry Verification.
5.  **Permissions Sufficient?**
    *   If "Yes": Environment Validated ✅ PASS.
    *   If "No": Fix Permission Issues -> Retry Permission Check.

#### Environment Validation Implementation:
```powershell
# Example: Validate environment for a web project
function Validate-Environment {
    $requiredTools = @(
        @{Name = "git"; Command = "git --version"},
        @{Name = "node"; Command = "node --version"},
        @{Name = "npm"; Command = "npm --version"}
    )
    
    $missingTools = @()
    $permissionIssues = @()
    
    # Check build tools
    foreach ($tool in $requiredTools) {
        try {
            Invoke-Expression $tool.Command | Out-Null
        } catch {
            $missingTools += $tool.Name
        }
    }
    
    # Check write permissions in project directory
    try {
        $testFile = ".__permission_test"
        New-Item -Path $testFile -ItemType File -Force | Out-Null
        Remove-Item -Path $testFile -Force
    } catch {
        $permissionIssues += "Current directory (write permission denied)"
    }
    
    # Check if port 3000 is available (commonly used for dev servers)
    try {
        $listener = New-Object System.Net.Sockets.TcpListener([System.Net.IPAddress]::Loopback, 3000)
        $listener.Start()
        $listener.Stop()
    } catch {
        $permissionIssues += "Port 3000 (already in use or access denied)"
    }
    
    # Display results
    if ($missingTools.Count -eq 0 -and $permissionIssues.Count -eq 0) {
        Write-Output "✅ Environment validated successfully"
        return $true
    } else {
        if ($missingTools.Count -gt 0) {
            Write-Output "❌ Missing tools: $($missingTools -join ', ')"
        }
        if ($permissionIssues.Count -gt 0) {
            Write-Output "❌ Permission issues: $($permissionIssues -join ', ')"
        }
        return $false
    }
}
```

### 4️⃣ MINIMAL BUILD TEST

This step performs a minimal build test to ensure core functionality.

**Process Flow:**
1.  **Start: Minimal Build Test.**
2.  **Create Minimal Test Project.**
3.  **Attempt Build.**
4.  **Build Successful?**
    *   If "Yes": Run Basic Functionality Test.
    *   If "No": Fix Build Issues -> Retry Build.
5.  **Test Passed?**
    *   If "Yes": Minimal Build Test ✅ PASS.
    *   If "No": Fix Test Issues -> Retry Test.

#### Minimal Build Test Implementation:
```powershell
# Example: Perform minimal build test for a React project
function Perform-MinimalBuildTest {
    $buildSuccess = $false
    $testSuccess = $false
    
    # Create minimal test project
    $testDir = ".__build_test"
    if (Test-Path $testDir) {
        Remove-Item -Path $testDir -Recurse -Force
    }
    
    try {
        # Create minimal test directory
        New-Item -Path $testDir -ItemType Directory | Out-Null
        Push-Location $testDir
        
        # Initialize minimal package.json
        @"
{
  "name": "build-test",
  "version": "1.0.0",
  "description": "Minimal build test",
  "main": "index.js",
  "scripts": {
    "build": "echo Build test successful"
  }
}
"@ | Set-Content -Path "package.json"
        
        # Attempt build
        npm run build | Out-Null
        $buildSuccess = $true
        
        # Create minimal test file
        @"
console.log('Test successful');
"@ | Set-Content -Path "index.js"
        
        # Run basic test
        node index.js | Out-Null
        $testSuccess = $true
        
    } catch {
        Write-Output "❌ Build test failed: $($_.Exception.Message)"
    } finally {
        Pop-Location
        if (Test-Path $testDir) {
            Remove-Item -Path $testDir -Recurse -Force
        }
    }
    
    # Display results
    if ($buildSuccess -and $testSuccess) {
        Write-Output "✅ Minimal build test passed successfully"
        return $true
    } else {
        if (-not $buildSuccess) {
            Write-Output "❌ Build process failed"
        }
        if (-not $testSuccess) {
            Write-Output "❌ Basic functionality test failed"
        }
        return $false
    }
}
```

## 📋 COMPREHENSIVE QA REPORT FORMAT

After running all validation steps, a comprehensive report is generated:

```
╔═════════════════════ 🔍 QA VALIDATION REPORT ══════════════════════╗
│                                                                     │
│  PROJECT: [Project Name]                                            │
│  TIMESTAMP: [Current Date/Time]                                     │
│                                                                     │
│  1️⃣ DEPENDENCY VERIFICATION                                         │
│  ✓ Required: [List of required dependencies]                        │
│  ✓ Installed: [List of installed dependencies]                      │
│  ✓ Compatible: [Yes/No]                                            │
│                                                                     │
│  2️⃣ CONFIGURATION VALIDATION                                        │
│  ✓ Config Files: [List of configuration files]                      │
│  ✓ Syntax Valid: [Yes/No]                                          │
│  ✓ Platform Compatible: [Yes/No]                                   │
│                                                                     │
│  3️⃣ ENVIRONMENT VALIDATION                                          │
│  ✓ Build Tools: [Available/Missing]                                │
│  ✓ Permissions: [Sufficient/Insufficient]                          │
│  ✓ Environment Ready: [Yes/No]                                     │
│                                                                     │
│  4️⃣ MINIMAL BUILD TEST                                              │
│  ✓ Build Process: [Successful/Failed]                              │
│  ✓ Functionality Test: [Passed/Failed]                             │
│  ✓ Build Ready: [Yes/No]                                           │
│                                                                     │
│  🚨 FINAL VERDICT: [PASS/FAIL]                                      │
│  ➡️ [Success message or error details]                              │
╚═════════════════════════════════════════════════════════════════════╝
```

## ❌ FAILURE REPORT FORMAT

If any validation step fails, a detailed failure report is generated:

```
⚠️⚠️⚠️ QA VALIDATION FAILED ⚠️⚠️⚠️

The following issues must be resolved before proceeding to BUILD mode:

1️⃣ DEPENDENCY ISSUES:
- [Detailed description of dependency issues]
- [Recommended fix]

2️⃣ CONFIGURATION ISSUES:
- [Detailed description of configuration issues]
- [Recommended fix]

3️⃣ ENVIRONMENT ISSUES:
- [Detailed description of environment issues]
- [Recommended fix]

4️⃣ BUILD TEST ISSUES:
- [Detailed description of build test issues]
- [Recommended fix]

⚠️ BUILD MODE IS BLOCKED until these issues are resolved.
Type 'VAN QA' after fixing the issues to re-validate.
```

## 🔄 INTEGRATION WITH DESIGN DECISIONS

The VAN QA mode reads and validates design decisions from the CREATIVE phase.

**Process Flow:**
1.  **Start: Read Design Decisions.**
2.  **Parse Creative Phase Documentation.**
3.  **Extract Technology Choices.**
4.  **Extract Required Dependencies.**
5.  **Build Validation Plan.**
6.  **Start Four-Point Validation Process.**

### Technology Extraction Process:
```powershell
# Example: Extract technology choices from creative phase documentation
function Extract-TechnologyChoices {
    $techChoices = @{}
    
    # Read from systemPatterns.md
    if (Test-Path "memory-bank\systemPatterns.md") {
        $content = Get-Content "memory-bank\systemPatterns.md" -Raw
        
        # Extract framework choice
        if ($content -match "Framework:\s*(\w+)") {
            $techChoices["framework"] = $Matches[1]
        }
        
        # Extract UI library choice
        if ($content -match "UI Library:\s*(\w+)") {
            $techChoices["ui_library"] = $Matches[1]
        }
        
        # Extract state management choice
        if ($content -match "State Management:\s*([^\\n]+)") {
            $techChoices["state_management"] = $Matches[1].Trim()
        }
    }
    
    return $techChoices
}
```

## 🚨 IMPLEMENTATION PREVENTION MECHANISM

If QA validation fails, the system prevents moving to BUILD mode.

```powershell
# Example: Enforce QA validation before allowing BUILD mode
function Check-QAValidationStatus {
    $qaStatusFile = "memory-bank\.qa_validation_status"
    
    if (Test-Path $qaStatusFile) {
        $status = Get-Content $qaStatusFile -Raw
        if ($status -match "PASS") {
            return $true
        }
    }
    
    # Display block message
    Write-Output "`n`n"
    Write-Output "🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫"
    Write-Output "⛔️ BUILD MODE BLOCKED: QA VALIDATION REQUIRED"
    Write-Output "⛔️ You must complete QA validation before proceeding to BUILD mode"
    Write-Output "`n"
    Write-Output "Type 'VAN QA' to perform technical validation"
    Write-Output "`n"
    Write-Output "🚫 NO IMPLEMENTATION CAN PROCEED WITHOUT VALIDATION 🚫"
    Write-Output "🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫"
    
    return $false
}
```

## 🧪 COMMON QA VALIDATION FIXES

Here are common fixes for issues encountered during QA validation:

### Dependency Issues:
- **Missing Node.js**: Install Node.js from https://nodejs.org/
- **Outdated npm**: Run `npm install -g npm@latest` to update
- **Missing packages**: Run `npm install` or `npm install [package-name]`

### Configuration Issues:
- **Invalid JSON**: Use a JSON validator to check syntax
- **Missing React plugin**: Add `import react from '@vitejs/plugin-react'` and `plugins: [react()]` to vite.config.js
- **Incompatible TypeScript config**: Update `tsconfig.json` with correct React settings

### Environment Issues:
- **Permission denied**: Run terminal as administrator (Windows) or use sudo (Mac/Linux)
- **Port already in use**: Kill process using the port or change the port in configuration
- **Missing build tools**: Install required command-line tools

### Build Test Issues:
- **Build fails**: Check console for specific error messages
- **Test fails**: Verify minimal configuration is correct
- **Path issues**: Ensure paths use correct separators for the platform

## 🔒 FINAL QA VALIDATION CHECKPOINT

```
✓ SECTION CHECKPOINT: QA VALIDATION
- Dependency Verification Passed? [YES/NO]
- Configuration Validation Passed? [YES/NO]
- Environment Validation Passed? [YES/NO]
- Minimal Build Test Passed? [YES/NO]

→ If all YES: Ready for BUILD mode
→ If any NO: Fix identified issues before proceeding
```
"""
    },
    {
        "path": ".cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-checks/file-verification.mdc",
        "content": """---
description: VAN QA sub-rule for specific file/artifact verification post-build or during QA. Fetched by `van-qa-main.mdc` if deeper file checks are needed.
globs: **/visual-maps/van_mode_split/van-qa-checks/file-verification.mdc
alwaysApply: false
---
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
    {
        "path": ".cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-main.mdc",
        "content": """---
description: Main orchestrator for VAN QA technical validation. Fetched by `van-mode-map.mdc` when 'VAN QA' is triggered. Fetches specific check rules and utility rules.
globs: **/visual-maps/van_mode_split/van-qa-main.mdc
alwaysApply: false
---
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
    {
        "path": ".cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-utils/common-fixes.mdc",
        "content": """---
description: VAN QA utility providing common fixes for validation failures. Fetched by `van-qa-main.mdc` on QA fail.
globs: **/visual-maps/van_mode_split/van-qa-utils/common-fixes.mdc
alwaysApply: false
---
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
        "content": """---
description: VAN QA utility for handling mode transitions after QA. Fetched by `van-qa-main.mdc` on QA pass. Guides AI to recommend BUILD mode.
globs: **/visual-maps/van_mode_split/van-qa-utils/mode-transitions.mdc
alwaysApply: false
---
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
        "content": """---
description: VAN QA utility for generating success/failure reports. Fetched by `van-qa-main.mdc`. Guides AI to format and present QA results using `edit_file`.
globs: **/visual-maps/van_mode_split/van-qa-utils/reports.mdc
alwaysApply: false
---
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
    "@
    
    # Save validation status (used by BUILD mode prevention mechanism)
    "FAIL" | Set-Content -Path "memory-bank\.qa_validation_status"
    
    return $report
}
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
        "content": """---
description: VAN QA utility: A reference guide on how to call VAN QA rules. Fetched if AI needs clarification on rule invocation.
globs: **/visual-maps/van_mode_split/van-qa-utils/rule-calling-guide.mdc
alwaysApply: false
---
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
        "content": """---
description: VAN QA utility: Quick helper on `fetch_rules` syntax. Rarely fetched directly.
globs: **/visual-maps/van_mode_split/van-qa-utils/rule-calling-help.mdc
alwaysApply: false
---
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
    },
    {
        "path": ".cursor/rules/isolation_rules/visual-maps/van_mode_split/van-qa-validation.md.old",
        "content": """# VAN MODE: QA TECHNICAL VALIDATION (Pre-BUILD)

> **TL;DR:** This map details the technical validation process executed *after* CREATIVE mode and *before* BUILD mode, triggered by the `VAN QA` command. It ensures dependencies, configuration, environment, and basic build functionality are sound.

## 🚀 VAN QA MODE ACTIVATION

After completing CREATIVE mode, when the user types "VAN QA", respond:

```
User: VAN QA

Response: OK VAN QA - Beginning Technical Validation
Loading QA Validation map...
```

## 🔄 QA COMMAND PRECEDENCE (QA Override)

QA validation can be called at any point (`QA` command) and takes immediate precedence:

**Process Flow:**
1.  **User Types: QA.**
2.  **⚠️ HIGH PRIORITY COMMAND.**
3.  **Pause Current Task/Process.**
4.  **Load QA Validation Map (This File).**
5.  **Execute QA Validation Process.**
6.  **QA Results.**
    *   If "PASS": Resume Prior Process Flow.
    *   If "FAIL": Fix Identified Issues -> Re-run QA Validation.

### QA Interruption Rules

1. **Immediate Precedence:** `QA` command interrupts everything.
2. **Load & Execute:** Load this map (`van-qa-validation.mdc`) and run the full process.
3. **Remediation Priority:** Fixes take priority over pending mode switches.
4. **Resume:** On PASS, resume the previous flow.

```
⚠️ QA OVERRIDE ACTIVATED
All other processes paused
QA validation checks now running...
Any issues found MUST be remediated before continuing with normal process flow
```

## 🔍 TECHNICAL VALIDATION OVERVIEW

Four-point validation process:

**Validation Flow:**
1.  **VAN QA MODE.**
2.  **FOUR-POINT VALIDATION.**
3.  **1️⃣ DEPENDENCY VERIFICATION.**
4.  **2️⃣ CONFIGURATION VALIDATION.**
5.  **3️⃣ ENVIRONMENT VALIDATION.**
6.  **4️⃣ MINIMAL BUILD TEST.**
7.  **MINIMAL BUILD TEST -> All Checks Passed?**
    *   If "Yes": GENERATE SUCCESS REPORT -> Trigger BUILD Mode.
    *   If "No": GENERATE FAILURE REPORT -> Fix Technical Issues -> Re-validate.

## 🔄 INTEGRATION WITH DESIGN DECISIONS

Reads Creative Phase outputs (e.g., `memory-bank/systemPatterns.md`) to inform validation:

**Integration Flow:**
1.  **Start: Read Design Decisions.**
2.  **Parse Creative Phase Documentation.**
3.  **Extract Technology Choices.**
4.  **Extract Required Dependencies.**
5.  **Build Validation Plan.**
6.  **Start Four-Point Validation Process.**

### Example Technology Extraction (PowerShell):
```powershell
# Example: Extract technology choices from creative phase documentation
function Extract-TechnologyChoices {
    $techChoices = @{}
    # Read from systemPatterns.md
    if (Test-Path "memory-bank\systemPatterns.md") {
        $content = Get-Content "memory-bank\systemPatterns.md" -Raw
        if ($content -match "Framework:\s*(\w+)") { $techChoices["framework"] = $Matches[1] }
        if ($content -match "UI Library:\s*(\w+)") { $techChoices["ui_library"] = $Matches[1] }
        if ($content -match "State Management:\s*([^\n]+)") { $techChoices["state_management"] = $Matches[1].Trim() }
    }
    return $techChoices
}
```

## 🔍 DETAILED QA VALIDATION STEPS & SCRIPTS

### 1️⃣ DEPENDENCY VERIFICATION

**Mermaid graph for Dependency Verification (as in original file) - replaced by text:**
**Process Flow:**
1.  Start: Dependency Verification.
2.  Read Required Dependencies: From Creative Phase.
3.  Check if Dependencies are Installed.
4.  All Dependencies Installed?
    *   If "Yes": Verify Versions and Compatibility.
    *   If "No": Install Missing Dependencies -> Verify Versions.
5.  Versions Compatible?
    *   If "Yes": Dependencies Verified ✅ PASS.
    *   If "No": Upgrade/Downgrade as Needed -> Retry Verification.

#### Example Implementation (PowerShell):
```powershell
# Verify-Dependencies function (as in original file)
function Verify-Dependencies {
    $requiredDeps = @{ "node" = ">=14.0.0"; "npm" = ">=6.0.0" }
    $missingDeps = @(); $incompatibleDeps = @()
    try { $nodeVersion = node -v; if ($nodeVersion -match "v(\d+).*") { if ([int]$Matches[1] -lt 14) { $incompatibleDeps += "node" } } } catch { $missingDeps += "node" }
    try { $npmVersion = npm -v; if ($npmVersion -match "(\d+).*") { if ([int]$Matches[1] -lt 6) { $incompatibleDeps += "npm" } } } catch { $missingDeps += "npm" }
    if ($missingDeps.Count -eq 0 -and $incompatibleDeps.Count -eq 0) { Write-Output "✅ Deps OK"; return $true } else { Write-Output "❌ Deps FAIL"; return $false }
}
```

#### Example Implementation (Bash):
```bash
# verify_dependencies function (as in original file)
verify_dependencies() {
    local missing_deps=(); local incompatible_deps=()
    if command -v node &> /dev/null; then node_version=$(node -v); if [[ $node_version =~ v([0-9]+) ]]; then if (( ${BASH_REMATCH[1]} < 14 )); then incompatible_deps+=("node"); fi; fi; else missing_deps+=("node"); fi
    if command -v npm &> /dev/null; then npm_version=$(npm -v); if [[ $npm_version =~ ([0-9]+) ]]; then if (( ${BASH_REMATCH[1]} < 6 )); then incompatible_deps+=("npm"); fi; fi; else missing_deps+=("npm"); fi
    if [ ${#missing_deps[@]} -eq 0 ] && [ ${#incompatible_deps[@]} -eq 0 ]; then echo "✅ Deps OK"; return 0; else echo "❌ Deps FAIL"; return 1; fi
}
```

### 2️⃣ CONFIGURATION VALIDATION

**Mermaid graph for Configuration Validation (as in original file) - replaced by text:**
**Process Flow:**
1.  Start: Configuration Validation.
2.  Identify Configuration Files.
3.  Read Configuration Files.
4.  Validate Syntax.
5.  Syntax Valid?
    *   If "Yes": Check Compatibility.
    *   If "No": Fix Syntax -> Retry.
6.  Compatible?
    *   If "Yes": Configs Validated ✅ PASS.
    *   If "No": Adapt Configs -> Retry Check.

#### Example Implementation (PowerShell):
```powershell
# Validate-Configurations function (as in original file)
function Validate-Configurations {
    $configFiles = @("package.json", "tsconfig.json", "vite.config.js")
    $invalidConfigs = @(); $incompatibleConfigs = @()
    foreach ($configFile in $configFiles) {
        if (Test-Path $configFile) {
            if ($configFile -match "\.json$") { try { Get-Content $configFile -Raw | ConvertFrom-Json | Out-Null } catch { $invalidConfigs += "$configFile (JSON)"; continue } }
            if ($configFile -eq "vite.config.js") { $content = Get-Content $configFile -Raw; if ($content -notmatch "react\(\)") { $incompatibleConfigs += "$configFile (React)" } }
        } else { $invalidConfigs += "$configFile (missing)" }
    }
    if ($invalidConfigs.Count -eq 0 -and $incompatibleConfigs.Count -eq 0) { Write-Output "✅ Configs OK"; return $true } else { Write-Output "❌ Configs FAIL"; return $false }
}
```

### 3️⃣ ENVIRONMENT VALIDATION

**Mermaid graph for Environment Validation (as in original file) - replaced by text:**
**Process Flow:**
1.  Start: Environment Validation.
2.  Check Env.
3.  Verify Tools.
4.  Available?
    *   If "Yes": Check Permissions.
    *   If "No": Install Tools -> Retry.
5.  Sufficient?
    *   If "Yes": Environment Validated ✅ PASS.
    *   If "No": Fix Permissions -> Retry Check.

#### Example Implementation (PowerShell):
```powershell
# Validate-Environment function (as in original file)
function Validate-Environment {
    $requiredTools = @(@{Name='git';Cmd='git --version'},@{Name='node';Cmd='node --version'},@{Name='npm';Cmd='npm --version'})
    $missingTools = @(); $permissionIssues = @()
    foreach ($tool in $requiredTools) { try { Invoke-Expression $tool.Cmd | Out-Null } catch { $missingTools += $tool.Name } }
    try { $testFile = ".__perm_test"; New-Item $testFile -ItemType File -Force | Out-Null; Remove-Item $testFile -Force } catch { $permissionIssues += "CWD Write" }
    try { $L = New-Object Net.Sockets.TcpListener([Net.IPAddress]::Loopback, 3000); $L.Start(); $L.Stop() } catch { $permissionIssues += "Port 3000" }
    if ($missingTools.Count -eq 0 -and $permissionIssues.Count -eq 0) { Write-Output "✅ Env OK"; return $true } else { Write-Output "❌ Env FAIL"; return $false }
}
```

### 4️⃣ MINIMAL BUILD TEST

**Mermaid graph for Minimal Build Test (as in original file) - replaced by text:**
**Process Flow:**
1.  Start: Minimal Build Test.
2.  Create Test Proj.
3.  Attempt Build.
4.  Success?
    *   If "Yes": Run Basic Test.
    *   If "No": Fix Build Issues -> Retry Build.
5.  Passed?
    *   If "Yes": Build Test ✅ PASS.
    *   If "No": Fix Test Issues -> Retry Test.

#### Example Implementation (PowerShell):
```powershell
# Perform-MinimalBuildTest function (as in original file)
function Perform-MinimalBuildTest {
    $buildSuccess = $false; $testSuccess = $false; $testDir = ".__build_test"
    if (Test-Path $testDir) { Remove-Item $testDir -Recurse -Force }
    try {
        New-Item $testDir -ItemType Directory | Out-Null; Push-Location $testDir
        '{"name": "build-test","scripts": {"build": "echo Build test successful"}}' | Set-Content package.json
        npm run build | Out-Null; $buildSuccess = $true
        'console.log("Test successful");' | Set-Content index.js
        node index.js | Out-Null; $testSuccess = $true
    } catch { Write-Output "❌ Build test exception" } finally { Pop-Location; if (Test-Path $testDir) { Remove-Item $testDir -Recurse -Force } }
    if ($buildSuccess -and $testSuccess) { Write-Output "✅ Build Test OK"; return $true } else { Write-Output "❌ Build Test FAIL"; return $false }
}
```

## 📝 VALIDATION REPORT FORMATS

### Comprehensive Success Report:
```
╔═════════════════════ 🔍 QA VALIDATION REPORT ══════════════════════╗
│ PROJECT: [Project Name] | TIMESTAMP: [Current Date/Time]            │
├─────────────────────────────────────────────────────────────────────┤
│ 1️⃣ DEPENDENCIES: ✓ Compatible                                       │
│ 2️⃣ CONFIGURATION: ✓ Valid & Compatible                             │
│ 3️⃣ ENVIRONMENT: ✓ Ready                                             │
│ 4️⃣ MINIMAL BUILD: ✓ Successful & Passed                            │
├─────────────────────────────────────────────────────────────────────┤
│ 🚨 FINAL VERDICT: PASS                                              │
│ ➡️ Clear to proceed to BUILD mode                                   │
╚═════════════════════════════════════════════════════════════════════╝
```

### Detailed Failure Report:
```
⚠️⚠️⚠️ QA VALIDATION FAILED ⚠️⚠️⚠️
Issues must be resolved before BUILD mode:

1️⃣ DEPENDENCY ISSUES: [Details/Fix]
2️⃣ CONFIGURATION ISSUES: [Details/Fix]
3️⃣ ENVIRONMENT ISSUES: [Details/Fix]
4️⃣ BUILD TEST ISSUES: [Details/Fix]

⚠️ BUILD MODE BLOCKED. Type 'VAN QA' after fixing to re-validate.
```

## 🧪 COMMON QA VALIDATION FIXES

- **Dependencies:** Install Node/npm, run `npm install`, check versions.
- **Configuration:** Validate JSON, check required plugins (e.g., React for Vite), ensure TSConfig compatibility.
- **Environment:** Check permissions (Admin/sudo), ensure ports are free, install missing CLI tools (git, etc.).
- **Build Test:** Check logs for errors, verify minimal config, check path separators.

## 🔒 BUILD MODE PREVENTION MECHANISM

Logic to check QA status before allowing BUILD mode transition.

**Process Flow:**
1.  Start: User Types: BUILD.
2.  QA Validation Passed?
    *   If "Yes": Allow BUILD Mode.
    *   If "No": BLOCK BUILD MODE -> Display: ⚠️ QA VALIDATION REQUIRED -> Prompt: Type VAN QA.

### Example Implementation (PowerShell):
```powershell
# Example: Check QA status before allowing BUILD
function Check-QAValidationStatus {
    $qaStatusFile = "memory-bank\.qa_validation_status" # Assumes status is written here
    if (Test-Path $qaStatusFile) {
        if ((Get-Content $qaStatusFile -Raw) -match "PASS") { return $true }
    }
    Write-Output "🚫 BUILD MODE BLOCKED: QA VALIDATION REQUIRED. Type 'VAN QA'. 🚫"
    return $false
}
```

## 🚨 MODE TRANSITION TRIGGERS (Relevant to QA)

### CREATIVE to VAN QA Transition:
```
⏭️ NEXT MODE: VAN QA
To validate technical requirements before implementation, please type 'VAN QA'
```

### VAN QA to BUILD Transition (On Success):
```
✅ TECHNICAL VALIDATION COMPLETE
All prerequisites verified successfully
You may now proceed to BUILD mode
Type 'BUILD' to begin implementation
```

## 📋 FINAL QA VALIDATION CHECKPOINT

```
✓ SECTION CHECKPOINT: QA VALIDATION
- Dependency Verification Passed? [YES/NO]
- Configuration Validation Passed? [YES/NO]
- Environment Validation Passed? [YES/NO]
- Minimal Build Test Passed? [YES/NO]

→ If all YES: Ready for BUILD mode transition.
→ If any NO: Fix identified issues and re-run VAN QA.
```
"""
    }
]

def create_or_update_mdc_file(filepath, content):
    """Creates or updates an .mdc file with the given content."""
    try:
        dir_name = os.path.dirname(filepath)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
            print(f"Created directory: {dir_name}")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n") # Ensure a final newline
        print(f"Successfully created/updated: {filepath}")
    except Exception as e:
        print(f"Error writing file {filepath}: {e}")

if __name__ == "__main__":
    project_root = os.getcwd() 
    print(f"Running script from: {project_root}")
    print("Starting MDC file generation process...")

    for file_data in MDC_FILES_DATA:
        absolute_filepath = os.path.join(project_root, file_data["path"])
        create_or_update_mdc_file(absolute_filepath, file_data["content"])
    
    print("\n--- MDC file generation process complete. ---")
    print("All .mdc files in .cursor/rules/isolation_rules/ have been updated to their text-only versions.")
    print("Please ensure your Cursor custom modes are configured to use these updated rules for optimal AI performance.")