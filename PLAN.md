# Plan: Integrate Prompt Templates into thinktank-wrapper

## Chosen Approach (One‑liner)

Rewrite `thinktank-wrapper` in Python as a modular CLI application, embedding prompt templates as package resources and loading them by name, thereby eliminating cross-repository symlinks and temporary file management in calling scripts.

## Architecture Blueprint

-   **Modules / Packages**
    -   `thinktank_wrapper/` (Root package)
        -   `__main__.py`: Entry point for the CLI application.
        -   `cli.py`: Handles command-line argument parsing using `argparse`. Defines all flags, positional arguments, and template selection logic.
        -   `templates/`: Directory containing prompt template files (e.g., `plan.md`, `review.md`) bundled as package data.
        -   `template_loader.py`: Logic for discovering, loading, and potentially rendering embedded prompt templates using `importlib.resources`.
        -   `context_finder.py`: Logic for finding context files (`glance.md`, `DEVELOPMENT_PHILOSOPHY*.md`) based on flags and working directory/explicit paths.
        -   `config.py`: Defines static configuration like model sets (`MODELS_ALL`, `MODELS_HIGH_CTX`) and the default synthesis model (`MODEL_SYNTH`).
        -   `command_builder.py`: Constructs the final `thinktank` command list based on parsed arguments, selected template, model set, and context files.
        -   `executor.py`: Executes the constructed `thinktank` command using `subprocess`, handling output streaming and error propagation.
        -   `logging_config.py`: Configures structured logging.
    -   `tests/`: Contains unit and integration tests.

-   **Public Interfaces / Contracts**
    -   **CLI:** `thinktank-wrapper [OPTIONS] --template <template_name> [CONTEXT_FILES...]`
        -   `--template <n>`: (New, Required unless listing) Name of the prompt template (e.g., `plan`).
        -   `--list-templates`: (New) List available embedded templates and exit.
        -   `--model-set <set_name>`: Select model set (e.g., `all`, `high-ctx`). Defaults defined in `config.py`.
        -   `--include-glance`: Find `glance.md` context files.
        -   `--include-philosophy`: Find `DEVELOPMENT_PHILOSOPHY*.md` context files relative to `$CODEX_DIR/docs/`.
        -   `--dry-run`: Print the final `thinktank` command instead of executing.
        -   `--instructions <file_path>`: (Existing, Overrides `--template`) Explicitly provide an instructions file path.
        -   Other `--*` flags: Pass-through unknown flags directly to `thinktank`.
        -   Positional `[CONTEXT_FILES...]`: Explicit file/directory paths to include as context.
    -   **Internal APIs (Python):**
        -   `template_loader.list_templates() -> List[str]`
        -   `template_loader.load_template(name: str) -> str`
        -   `context_finder.find_context_files(include_glance: bool, include_philosophy: bool, explicit_paths: List[str]) -> List[str]`
        -   `command_builder.build_command(args: argparse.Namespace, template_content: Optional[str]) -> List[str]`
        -   `executor.run_command(cmd: List[str], dry_run: bool) -> int`

-   **Data Flow Diagram** (mermaid)

    ```mermaid
    graph TD
        A[User runs thinktank-wrapper] --> B(cli.py: Parse Args);
        B --> C{Mode?};
        C -- --list-templates --> D(template_loader.py: List Templates);
        D --> Exit;
        C -- Default --> E{Check --instructions};
        E -- Yes --> F[Use provided instructions path];
        E -- No --> G{Check --template};
        G -- Yes --> H(template_loader.py: Load Template);
        G -- No --> ErrorExit[ERROR: Must provide --template or --instructions];
        H --> I[Write Template Content to Temp File];
        F --> J(command_builder.py: Build Command);
        I --> J;
        B --> K(context_finder.py: Find Context Files);
        B --> L(config.py: Get Model Set);
        K --> J;
        L --> J;
        J --> M{Dry Run?};
        M -- Yes --> N[Print Command];
        M -- No --> O(executor.py: Run thinktank via subprocess);
        N --> Cleanup[Cleanup Temp File if created];
        O --> Cleanup;
        Cleanup --> ExitCode[Propagate Exit Code];
    ```

-   **Error & Edge‑Case Strategy**
    -   Argument validation: Handled by `argparse` (required flags, types). Specific validation for `--template` (must exist if specified), `--model-set` (must be in `config.py`).
    -   Missing template: `TemplateNotFoundError` raised by `template_loader`, caught in `__main__`, print clear error listing available templates, exit(1).
    -   Missing context files: Warn if `--include-*` flags used but no files found. Error if explicit paths don't exist.
    -   `thinktank` executable not found: `FileNotFoundError` caught by `executor`, print clear error, exit(1).
    -   `thinktank` execution failure: `executor` captures non-zero exit code and stderr from `subprocess.run`, logs error, propagates exit code.
    -   Precedence: `--instructions` explicitly provided by user always overrides `--template`.
    -   Temporary file errors: Use `tempfile` module with context managers (`with tempfile.NamedTemporaryFile(...)`) for robust creation and automatic cleanup. Catch I/O errors during write.

## Detailed Build Steps

1.  **Project Setup:** Initialize a Python project (`pyproject.toml`, `src/thinktank_wrapper/`). Use `hatch` or `poetry`. Define dependencies (minimal, e.g., potentially `python-json-logger`). Configure package data inclusion for `templates/`.
2.  **Configuration:** Implement `src/thinktank_wrapper/config.py`. Port model set definitions (`MODELS_ALL`, `MODELS_HIGH_CTX`, `MODEL_SYNTH`) from Bash script into Python constants (e.g., `Dict[str, List[str]]`).
3.  **Embed Templates:** Create `src/thinktank_wrapper/templates/` and copy existing prompt files (`docs/prompts/*.md`) into it. Ensure `pyproject.toml` includes `templates/*`.
4.  **Template Loading:** Implement `src/thinktank_wrapper/template_loader.py`. Use `importlib.resources.files()` and `.iterdir()` to list templates, `.read_text()` to load content. Implement `load_template(name)` and `list_templates()`. Handle `FileNotFoundError` gracefully, converting to a custom `TemplateNotFoundError`. *Initially, do not add template rendering logic (e.g., Jinja2) - only load raw content (Simplicity/YAGNI).*
5.  **CLI Parsing:** Implement `src/thinktank_wrapper/cli.py` using `argparse`. Define all arguments: `--template`, `--list-templates`, `--model-set` (with choices from `config.py`), `--include-*`, `--dry-run`, `--instructions`, positional `context_files`, and handle unknown args for pass-through using `parse_known_args()`.
6.  **Context Finding:** Implement `src/thinktank_wrapper/context_finder.py`. Port Bash logic for finding `glance.md` (relative to CWD or explicit paths) and `DEVELOPMENT_PHILOSOPHY*.md` (relative to `$CODEX_DIR/docs/`). Use `pathlib` and environment variables (`$CODEX_DIR` is critical - ensure `install.sh` sets this). Handle non-existence gracefully.
7.  **Command Building:** Implement `src/thinktank_wrapper/command_builder.py`. Create `build_command` function taking parsed args and optional template content.
    -   Resolve model flags from `config.py` based on `--model-set`.
    -   Aggregate unique context file paths (explicit + discovered).
    -   If template content provided (from `--template`), write to a temporary file using `tempfile.NamedTemporaryFile(delete=False)` and get its path. Pass this path via `--instructions`.
    -   If `--instructions` was provided by user, use that path directly.
    -   Assemble the final command list (`['thinktank', '--model', '...', '--synthesis-model', '...', '--instructions', temp_file_path_or_user_path, context_file1, ...]`). Include pass-through arguments.
    -   Return the command list *and* the path to the temporary file if one was created.
8.  **Execution Logic:** Implement `src/thinktank_wrapper/executor.py`. Create `run_command` taking the command list. Use `subprocess.run(cmd, check=False, text=True, capture_output=False)` (stream output directly). Return the `returncode`. Handle `FileNotFoundError` if `thinktank` isn't in PATH.
9.  **Logging Setup:** Implement `src/thinktank_wrapper/logging_config.py` to configure standard `logging` with a structured formatter (e.g., JSON).
10. **Main Orchestration:** Implement `src/thinktank_wrapper/__main__.py`.
    -   Setup logging.
    -   Parse args using `cli.parse_args()`.
    -   Handle `--list-templates`.
    -   Load template via `template_loader` if `--template` used.
    -   Find context files via `context_finder`.
    -   Build command via `command_builder`, getting back command list and temporary file path (if any).
    -   Handle `--dry-run` (print command).
    -   Execute command via `executor.run_command`.
    -   **Crucially:** Use a `try...finally` block to ensure the temporary instructions file is deleted if created.
    -   Exit with the code from `executor`.
11. **Testing:** Implement comprehensive unit and integration tests (see Testing Strategy).
12. **Documentation:** Update `README.md`, `bin/README.md`. Add docstrings and type hints.
13. **Replace & Update:** Remove old Bash wrapper. Update `install.sh` to install the Python package and ensure `$CODEX_DIR` is reliably set. Update all `claude-commands/*.md` scripts to use `thinktank-wrapper --template <n>` instead of manual temp file creation.

## Testing Strategy

-   **Test Layers:**
    -   **Unit Tests (`pytest`):** Isolate and test individual modules/functions.
        -   `cli.py`: Verify parsing of various argument combinations, including pass-through args.
        -   `template_loader.py`: Mock `importlib.resources`. Test listing templates, loading known templates, error on loading unknown templates.
        -   `context_finder.py`: Mock `os.environ`, `pathlib.Path` methods (`exists`, `glob`, `walk`). Test finding files under different conditions (flags on/off, files present/absent, `$CODEX_DIR` set/unset).
        -   `command_builder.py`: Test construction of the command list with different inputs (templates vs instructions, model sets, context files). Verify temporary file creation logic (mock `tempfile`). Assert correct argument order and content.
        -   `config.py`: Simple tests ensuring data structures are correct.
    -   **Integration Tests (`pytest`):** Test the collaboration between modules, focusing on the flow from CLI args to the final command execution call.
        -   Use `pytest.MonkeyPatch` to set environment variables (`$CODEX_DIR`).
        -   Use `tmp_path` fixture to create temporary directory structures for context file finding tests.
        -   Mock `subprocess.run` to assert the correct command list is passed for execution under various scenarios (including `--dry-run`). Verify temporary file content and cleanup.
-   **What to Mock:**
    -   **True Externals:** `importlib.resources` (package data access), Filesystem (`pathlib`, `os`), Environment Variables (`os.environ`), `subprocess.run` (the `thinktank` execution).
    -   **Why:** Focus tests on the wrapper's logic, isolating it from the environment and the external `thinktank` process itself. Adheres to DEVELOPMENT_PHILOSOPHY.md (Testability - minimal mocking).
-   **Coverage Targets & Edge‑Case Notes:**
    -   Aim for >95% line/branch coverage for core logic modules (`cli`, `template_loader`, `context_finder`, `command_builder`).
    -   Test edge cases: template not found, context files not found (with/without flags), invalid model set, `--instructions` overriding `--template`, no context files provided, `thinktank` not found error, `thinktank` execution failure propagation, temporary file errors, pass-through argument handling.

## Logging & Observability

-   Use Python's standard `logging` module configured for structured JSON output (`logging_config.py`).
-   Log key events: Wrapper start, Parsed arguments (excluding potentially sensitive context), Template selected, Context files found, Model set resolved, Final `thinktank` command constructed (DEBUG level, potentially excluding sensitive args), `thinktank` execution start/end, `thinktank` exit code (INFO/ERROR), Any exceptions caught.
-   Structured fields: `timestamp`, `level`, `name` (module), `message`, `correlation_id` (generate UUID per run), `template_name`, `model_set`, `num_context_files`, `thinktank_exit_code`.
-   Correlation ID: Generate a UUID at the start of `__main__.py` and include it in all log records for tracing a single invocation.

## Security & Config

-   **Input Validation:**
    -   `argparse` handles basic type checks.
    -   Validate `--template` name against `list_templates()`.
    -   Validate `--model-set` against keys in `config.MODEL_SETS`.
    -   `context_finder` should validate that explicit paths exist.
    -   No path traversal risk from template names as they are loaded via `importlib.resources` from within the package.
-   **Secrets Handling:** The wrapper itself handles no secrets. It relies on `thinktank`'s own mechanisms (likely environment variables referenced in `models.yaml`). The temporary instructions file should have default restricted permissions (handled by `tempfile`). Avoid logging file contents or sensitive arguments.
-   **Least‑Privilege:** Runs as the user invoking it. Requires read access to context files and templates, write access to `/tmp` (or equivalent), execute permission for `thinktank`. Use `subprocess.run(..., shell=False)` to avoid shell injection vulnerabilities.

## Documentation

-   **Code Self‑Doc:** PEP 8 compliant. Type hints (`typing`) for all functions/methods. Docstrings explaining purpose, arguments, return values, and exceptions raised for all public modules, classes, and functions.
-   **README Updates:** Update `README.md` and `bin/README.md`. Detail the Python implementation, installation (`pip install .`, `install.sh` for `$CODEX_DIR`), new usage (`--template`, `--list-templates`), argument precedence (`--instructions` > `--template`), and how to add new templates (add file to `templates/`, reinstall).
-   **Template Docs:** Consider adding a comment header block within each template file (`templates/*.md`) briefly explaining its purpose or required context variables (if any are introduced later).
-   **CLI Help:** Ensure `argparse` generates clear and comprehensive help messages (`--help`).

## Risk Matrix

| Risk                                                     | Severity | Mitigation                                                                                                                               |
| :------------------------------------------------------- | :------- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| Regression: Python script behaves differently than Bash  | High     | Comprehensive integration tests verifying command construction (using `--dry-run` and mocking `subprocess`) against known Bash script outputs. |
| `$CODEX_DIR` not set or incorrect                        | Medium   | Make `$CODEX_DIR` the primary mechanism. Ensure `install.sh` sets it reliably. Add clear error message if needed directories aren't found. |
| Template Loading Fails (packaging issue)                 | Medium   | Use standard `importlib.resources`. Test template loading in integration tests after a local build/install (`pip install -e .`).          |
| `thinktank` command construction errors (arg order, etc.) | Medium   | Thorough integration tests using `--dry-run` and `subprocess` mocking to assert the exact command list for various argument combinations.  |
| Temporary file handling errors (creation, cleanup)       | Low      | Use `tempfile.NamedTemporaryFile` within `try...finally` block or context manager for robust creation and automatic cleanup.             |
| Breaking existing `claude-commands/*.md` scripts         | Medium   | Manually review and update all command scripts. Test key command scripts after implementing the new wrapper.                               |
| Increased complexity managing Python environment         | Low      | Use standard tools (`poetry`/`hatch`). Keep dependencies minimal. Provide clear installation instructions.                               |

## Open Questions

-   What is the minimum required Python version? (Recommend 3.8+ for `importlib.resources` and typing features).
-   Confirm `$CODEX_DIR` is the acceptable method for locating `DEVELOPMENT_PHILOSOPHY*.md`. Is any fallback needed? (Decision: Prioritize env var strongly).
-   Will templates *ever* require variable substitution (parameterization)? (Decision: No, not in this iteration - YAGNI. If needed later, consider `str.format` or Jinja2 and update plan).
-   Are there any subtle behaviors of the Bash wrapper's file finding or argument handling that must be precisely replicated? (Requires careful review of the Bash source during implementation).