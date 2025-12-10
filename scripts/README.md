# Vault Automation Scripts

Python scripts for automating Obsidian vault organization and Anki flashcard synchronization.

## organized-vault.py

Automatically organizes vault files by type and tags.

### Usage

```bash
# Run immediately (non-interactive, perfect for automation)
python scripts/organized-vault.py

# Preview changes without moving files
python scripts/organized-vault.py --dry-run

# Silent mode - only logs to file (for Shell Commands plugin)
python scripts/organized-vault.py --silent

# Legacy interactive mode with prompts
python scripts/organized-vault.py --interactive
```

### Features

- **Automatic file organization** based on type (PDF, images) and tags
- **Tag-based routing** with priority order: #developer → #art → #ideas → #auditoria → #anki
- **Comprehensive logging** to `scripts/logs/organization_TIMESTAMP.log`
- **Duplicate handling** with automatic renaming (file_1.md, file_2.md)
- **Skip protection** for organized folders, hidden folders, and system directories
- **UTF-8 console support** for Windows emoji display
- **Exit codes** for automation: 0 = success, 1 = errors

### Configuration

No configuration needed! The script automatically detects the vault path.

### Log Files

All operations are logged to `scripts/logs/` with:
- Timestamp for each operation
- DEBUG level details (which folders/files were processed)
- INFO level summaries (files moved, errors encountered)
- Full error tracebacks for troubleshooting

## anki.py

Syncs markdown flashcards to Anki via AnkiConnect API.

### Prerequisites

1. Install AnkiConnect add-on in Anki (Code: 2055492159)
2. Ensure Anki is running
3. Place flashcard notes in the `anki/` folder

### Usage

```bash
python scripts/anki.py
```

### Card Format

```markdown
---
id: optional-custom-id
---

Front:
Your question here

Back:
Your answer here
```

## Shell Commands Plugin Integration

For the **obsidian-shellcommands** plugin, use these commands:

**Organize vault (silent mode):**
```bash
python {{vault_path}}/scripts/organized-vault.py --silent
```

**Organize vault with preview:**
```bash
python {{vault_path}}/scripts/organized-vault.py --dry-run
```

**Sync to Anki:**
```bash
python {{vault_path}}/scripts/anki.py
```

The silent mode ensures the plugin doesn't hang waiting for user input, and all output is logged to files for later review.

## Troubleshooting

1. **Check log files** in `scripts/logs/` for detailed error information
2. **Run with --dry-run** first to preview changes
3. **Verify tags** are correctly formatted (#tagname or YAML frontmatter)
4. **Ensure Python 3.8+** is installed

## Recent Improvements (2025-12-10)

- ✅ Added non-interactive mode by default (perfect for automation)
- ✅ Created centralized `scripts/logs/` folder for all log files
- ✅ Added `--silent` mode for Shell Commands plugin integration
- ✅ Fixed Windows console Unicode/emoji encoding issues
- ✅ Automatic vault path detection (no manual configuration)
- ✅ Enhanced error handling with proper exit codes
- ✅ Removed unused variables and optimized code
- ✅ Added comprehensive logging at DEBUG and INFO levels
- ✅ Added `templates/` to skip folders list
