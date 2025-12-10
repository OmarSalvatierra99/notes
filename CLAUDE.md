# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is an Obsidian vault for personal knowledge management with automated organization. The vault combines semantic folder structure with tag-based routing, Python automation scripts, and Anki flashcard synchronization. It's version-controlled via Git with automated commits through the obsidian-git plugin.

## Vault Architecture

### Folder Structure

```
notas/
├── developer/          # Development and programming notes (#developer)
├── brain/              # Ideas and concepts (#ideas)
├── art/                # Art-related content (#art)
├── anki/               # Flashcard notes for Anki export (#anki)
├── auditoria-gubernamental/  # Government auditing research (#auditoria)
├── diary/              # Daily dated notes (YYYY-MM-DD.md, git-ignored)
├── media/              # Images and visual assets
├── pdf/                # PDF documents for reference
├── scripts/            # Python automation scripts
│   ├── organized-vault.py  # Auto-organizes files by type and tags
│   ├── anki.py            # Syncs notes to Anki via AnkiConnect
│   └── logs/              # Operation logs with timestamps
├── templates/          # Obsidian templates
├── Dashboard.md        # Main productivity hub (Dataview-powered)
└── Budget.md           # Personal finances tracker
```

### Organization Pattern

The vault uses **automated tag-based routing**:

1. Files with specific tags are automatically moved to corresponding folders
2. PDFs automatically move to `pdf/`, images to `media/`
3. Tag priority order: `#developer` > `#art` > `#ideas` > `#auditoria` > `#anki`
4. First matching tag wins (files are not duplicated)

### Workflow Tags

The vault uses a **minimalist two-tag productivity system**:

- `#working` - Active/inbox notes tracked in Dashboard
- `#completed` - Archived/reference notes

These workflow tags are **independent** from organization tags. A note can have both:
- Example: `#developer #working` (a development note you're currently working on)
- Example: `#ideas #completed` (a completed idea note for reference)

**Dashboard.md** uses Dataview queries to display:
- **Inbox / Active Work:** All notes tagged `#working` across all folders
- **Archive / Completed:** All notes tagged `#completed` for reference

## Commands

### Organize Vault Files

```bash
# Non-interactive mode (default) - runs immediately with logging
python scripts/organized-vault.py

# Dry run - preview changes without moving files
python scripts/organized-vault.py --dry-run

# Silent mode - only log to file (for Shell Commands plugin)
python scripts/organized-vault.py --silent

# Interactive mode - prompts for confirmation
python scripts/organized-vault.py --interactive
```

**What it does:**
- Moves PDFs to `pdf/`, images to `media/`
- Routes tagged markdown files to appropriate folders based on tags
- Handles duplicate filenames with numeric suffixes (`file_1.md`, `file_2.md`)
- Logs all operations to `scripts/logs/organization_TIMESTAMP.log`
- Skips `.obsidian/`, `.git/`, `scripts/`, `templates/`, and files already in organized folders

### Calculate Budget Totals

```bash
python scripts/budget-calculator.py
```

**What it does:**
- Scans Budget.md for sections (## headers)
- Extracts numeric values from all bullet points
- Calculates and updates totals automatically
- Preserves all formatting and emojis
- Outputs formatted totals: `- **Total: $X,XXX.XX MXM**`

### Sync Notes to Anki

```bash
python scripts/anki.py
```

**Prerequisites:**
- AnkiConnect add-on installed in Anki (Code: 2055492159)
- Anki running during sync
- Notes in `anki/` folder with Front:/Back: template structure

**What it does:**
- Parses Front:/Back: sections from markdown files
- Creates new Anki cards or updates existing ones based on unique IDs
- Uploads embedded images to Anki's media collection
- Converts markdown formatting to HTML
- Tracks cards via unique IDs to prevent duplicates

## Key Implementation Details

### Tag Recognition

The organization script recognizes tags in two formats:

**Inline tags:**
```markdown
#developer #working

Your content here...
```

**YAML frontmatter:**
```yaml
---
tags: [developer, working]
---

Your content here...
```

Both formats are automatically processed and converted to hashtag format internally.

### Anki Card Template

Notes in the `anki/` folder should use this structure:

```markdown
---
id: optional-custom-id
---

Front:
Your question or prompt here

Back:
Your answer or explanation here
```

- Optional YAML `id:` field for custom IDs (otherwise auto-generated from file path)
- Supports Obsidian wiki-style images: `![[image.png]]`
- Supports standard markdown images: `![alt](image.png)`
- Images are automatically uploaded to Anki's media collection

### Python Script Architecture

**organized-vault.py** (420 lines):
- `setup_logging()` - Dual logging (file + console) with UTF-8 support for Windows
- `find_tags_in_file()` - Extracts tags from inline and YAML frontmatter
- `should_skip_folder()` - Determines if folder should be excluded
- `move_file()` - Handles file movement with duplicate resolution
- `organize_vault()` - Main orchestrator that walks vault and applies rules
- `main()` - CLI entry point with argparse for modes

**budget-calculator.py** (173 lines):
- `extract_amount()` - Extracts numeric values from lines with regex pattern matching
- `format_amount()` - Formats numbers as `$X,XXX.XX` with comma separators
- `calculate_budget_totals()` - Parses sections, sums amounts, regenerates totals
- `main()` - Entry point with UTF-8 console support and change detection

**anki.py** (509 lines):
- `invoke_anki_connect()` - AnkiConnect API wrapper
- `extract_note_id()` - Generates/extracts unique ID from YAML or file hash
- `parse_card_from_template()` - Extracts Front:/Back: content
- `process_images()` - Converts Obsidian image links to Anki format
- `clean_markdown()` - Converts markdown to HTML for Anki
- `sync_or_update_note()` - Smart sync logic (update existing or create new)

**Log Files:**
All automation operations logged to `scripts/logs/` with:
- Timestamp for each operation
- DEBUG level details (folders/files processed)
- INFO level summaries (files moved, errors)
- Full error tracebacks for troubleshooting

## Obsidian Configuration

### Settings
- VIM mode enabled
- Auto-update links on file rename
- Media folder: `media/`
- Daily notes folder: `diary/`

### Core Plugins
Daily notes, templates, graph view, backlinks, command palette, canvas, bookmarks, properties, page preview, file explorer, global search, tag pane

### Community Plugins
- **dataview** - Powers the Dashboard with dynamic queries
- **obsidian-git** - Automated git commits ("vault backup" timestamps)
- **obsidian-shellcommands** - Execute Python scripts from Obsidian UI
- **templater-obsidian** - Advanced templating
- **obsidian-excalidraw-plugin** - Diagrams and drawings
- **pdf-plus** - Enhanced PDF handling
- **oz-clear-unused-images** - Cleanup unused media
- **background-image** - Visual customization
- **obsidian-reminder-plugin** - Task reminders

## Git Configuration

- Automated commits via obsidian-git plugin
- Commit message format: "vault backup: YYYY-MM-DD HH:MM:SS"
- `.gitignore` protects privacy: entire `diary/` folder excluded
- Excludes Obsidian system files (workspace, cache, appearance)
- Excludes Python artifacts and script logs
- Tracks PDFs and media files

## Productivity Dashboard Workflow

The vault uses a **minimalist two-tag system** for tracking work:

1. **Start working on a note:** Add `#working` tag (appears in Dashboard's "Inbox / Active Work")
2. **Finish the note:** Replace `#working` with `#completed` tag (moves to "Archive / Completed")

**Dashboard queries:**
- Both sections use simple `LIST FROM #tag` queries sorted by modification time
- Works across **all folders** - doesn't matter if note is in `developer/`, `brain/`, etc.
- No metadata fields required - just the two tags

**Combining with organization tags:**
- `#developer #working` - Active development note
- `#ideas #completed` - Completed idea for reference
- `#art #working` - Art project in progress

The workflow tags (`#working`, `#completed`) are **independent** from organization tags (`#developer`, `#art`, `#ideas`, `#auditoria`, `#anki`). Organization tags determine folder location, workflow tags determine dashboard visibility.

## Development Workflow

1. **Creating notes:** Create notes in root or appropriate folders, add relevant tags
2. **Track progress:** Add `#working` when actively working, `#completed` when done
3. **Organization:** Run `organized-vault.py --dry-run` to preview, then run without flag to execute
4. **Anki export:** Place notes in `anki/` folder with Front:/Back: structure, run `anki.py`
5. **Version control:** Git commits automated via obsidian-git plugin
6. **Dashboard:** View all active work and completed notes in [Dashboard.md](Dashboard.md)

## Important Notes

- **Vault path:** Scripts auto-detect vault path via `Path(__file__).parent.parent`
- **No configuration needed:** Scripts work out-of-box after installation
- **Windows compatibility:** UTF-8 console encoding handled for emoji display
- **Exit codes:** Scripts return 0 on success, 1 on errors (for automation)
- **Duplicate handling:** Files with same name get numeric suffixes automatically
- **Protected files:** `CLAUDE.md` files are never moved by organization script (preserved in place)
- **Privacy:** `diary/` folder excluded from git, logs excluded from version control
- **Media management:** Centralized in `media/` folder with auto-attachment configuration

## Additional Documentation

For detailed script internals and function documentation, see [developer/CLAUDE.md](developer/CLAUDE.md).
