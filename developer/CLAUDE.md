# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is an Obsidian vault for personal knowledge management with automated organization. The vault includes Python automation scripts for organizing files and exporting notes to Anki flashcards.

## Repository Structure

The vault uses a tag-based organization system with dedicated folders:

- **anki/** - Flashcard notes intended for Anki export
- **brain/** - Ideas and concepts (`#ideas` tag)
- **developer/** - Development and programming notes (`#developer` tag)
- **art/** - Art-related notes (`#art` tag)
- **auditoria-gubernamental/** - Government audit content (`#auditoria` tag)
- **diary/** - Daily notes
- **media/** - Images and visual assets
- **pdf/** - PDF documents
- **scripts/** - Python automation scripts
- **templates/** - Obsidian templates

## Python Scripts

### Running the Scripts

The scripts automatically detect the vault path from their location (`Path(__file__).parent.parent`), so no configuration is needed.

**organized-vault.py** - Run with command-line arguments:
```bash
# Non-interactive mode (default) - runs immediately with logging
python scripts/organized-vault.py

# Dry run mode - preview changes without moving files
python scripts/organized-vault.py --dry-run

# Silent mode - only log to file, no console output (for Shell Commands plugin)
python scripts/organized-vault.py --silent

# Interactive mode (legacy) - prompts for confirmation
python scripts/organized-vault.py --interactive
```

**anki.py** - Run with:
```bash
python scripts/anki.py
```

### organized-vault.py

Automatically organizes vault files based on file type and tags.

**Organization rules:**
- PDFs → `pdf/`
- Images (jpg, png, gif, webp, bmp, svg) → `media/`
- Files with `#developer` → `developer/`
- Files with `#art` → `art/`
- Files with `#ideas` → `brain/`
- Files with `#auditoria` → `auditoria-gubernamental/`
- Files with `#anki` → `anki/`

**Important behaviors:**
- **Tag priority**: Only the first matching tag moves the file (order: #developer, #art, #ideas, #auditoria, #anki)
- Hidden folders (`.obsidian/`, `.git/`, `.trash/`) and `scripts/`, `templates/` folders are automatically skipped
- Duplicate filenames are auto-renamed with numeric suffixes (e.g., `file_1.md`, `file_2.md`)
- Supports both inline tags (`#tag`) and YAML frontmatter tags (converted to hashtag format)
- Non-interactive by default (perfect for Shell Commands plugin automation)
- All operations logged to `scripts/logs/organization_TIMESTAMP.log` with DEBUG level details
- Files already in organized folders are not moved again
- Exit code 0 on success, 1 on errors (for automation scripting)

### anki.py

Syncs markdown notes from the `anki/` folder directly to Anki via AnkiConnect API with smart update/create logic.

**Prerequisites:**
1. Install AnkiConnect add-on in Anki (Code: 2055492159)
2. Anki must be running during sync
3. AnkiConnect listens on http://localhost:8765

**Card template format:**
Notes must use the Front:/Back: template structure:
```markdown
Front:
Your question here

Back:
Your answer here
```

Optional YAML frontmatter for custom ID:
```markdown
---
id: my-custom-id
---
Front:
...
```

**Features:**
- **Direct sync**: No manual import needed, cards added directly to Anki
- **Smart updates**: Syncing the same note updates the existing card instead of creating duplicates
- **Unique ID tracking**: Each note tracked by ID (from YAML `id:` field or auto-generated from file path)
- **Obsidian image support**: Both `![[image.png]]` (wiki-style) and `![alt](image.png)` (markdown) formats
- **Template parsing**: Extracts Front/Back content from structured markdown
- **HTML conversion**: Markdown formatting converted to HTML (bold, italic, lists, links, etc.)
- **Auto-tagging**: Cards tagged with "obsidian" and unique ID tag (`obsidian-id-{id}`)

**Image handling:**
- Supports Obsidian wiki-style links: `![[image.png]]`
- Supports standard markdown: `![alt](image.png)`
- Looks for images in `media/` folder first
- Falls back to vault root for relative paths
- Supports: jpg, png, gif, webp, bmp, svg
- Images are base64 encoded and uploaded to Anki's media collection

**Update mechanism:**
1. Each note gets a unique ID (YAML `id:` or MD5 hash of file path)
2. ID stored as Anki tag: `obsidian-id-{id}`
3. On sync:
   - If card with ID exists → updates fields and images
   - If card doesn't exist → creates new card
4. No duplicates are ever created from the same source note

**Usage:**
```bash
python scripts/anki.py
```

The script will:
1. Test AnkiConnect connection
2. Create/verify the deck exists
3. Scan all .md files in `anki/` folder
4. Parse Front:/Back: sections and extract/generate ID
5. Upload images
6. Create new cards or update existing ones based on ID

## Obsidian Configuration

### Core Plugins Enabled
- Daily notes, templates, graph view, backlinks, command palette
- Canvas, bookmarks, properties, page preview
- File explorer, global search, tag pane

### Community Plugins
- **obsidian-git** - Git version control integration (automated commits)
- **obsidian-excalidraw-plugin** - Drawing and diagrams
- **templater-obsidian** - Advanced templating
- **pdf-plus** - Enhanced PDF handling
- **oz-clear-unused-images** - Cleanup unused media
- **background-image** - Customization
- **obsidian-shellcommands** - Execute shell commands from Obsidian
- **obsidian-reminder-plugin** - Reminder and task management

## Script Architecture

### organized-vault.py Key Functions
- `setup_logging()` - Configures dual logging (file + optional console) with UTF-8 support for Windows (lines 56-93)
- `find_tags_in_file()` - Extracts tags from both inline format and YAML frontmatter with error handling (lines 101-137)
- `should_skip_folder()` - Determines if a folder should be excluded from organization (lines 169-195)
- `move_file()` - Handles file movement with duplicate name resolution and detailed logging (lines 140-166)
- `organize_vault()` - Main orchestrator that walks the vault and applies organization rules with comprehensive error handling (lines 198-339)
- `main()` - CLI entry point with argparse for --dry-run, --silent, --interactive modes (lines 342-414)

### anki.py Key Functions
- `invoke_anki_connect()` - Low-level API wrapper for AnkiConnect requests (lines 31-56)
- `parse_card_from_template()` - Extracts Front:/Back: content from markdown files (lines 236-272)
- `extract_note_id()` - Generates or extracts unique ID from YAML or file path hash (lines 217-233)
- `process_images()` - Converts Obsidian image links to Anki format and uploads media (lines 102-147)
- `clean_markdown()` - Converts markdown formatting to HTML for Anki display (lines 150-214)
- `find_note_by_id()` - Searches Anki for existing notes by custom ID tag (lines 275-286)
- `sync_or_update_note()` - Smart sync logic that updates existing cards or creates new ones (lines 343-368)

**AnkiConnect API**: The script communicates with Anki via HTTP requests to `http://localhost:8765`. Key API calls include `addNote`, `updateNoteFields`, `findNotes`, and `storeMediaFile`.

## Templates

Located in [templates/](templates/) folder:
- **anki-template.md** - Basic Anki flashcard template with Front:/Back: structure for creating new cards

## Development Workflow

1. Create notes in the root or appropriate tagged folders
2. Tag notes with relevant tags (`#developer`, `#ideas`, etc.)
3. Run `organized-vault.py` in dry-run mode first to preview changes
4. Confirm and execute organization
5. For Anki exports, place notes in `anki/` folder and run `anki.py`
6. Git commits are automated via obsidian-git plugin

## Tag System

Tags can be added in two ways:
- Inline: `#developer #ideas #anki`
- YAML frontmatter:
  ```yaml
  ---
  tags: [developer, ideas]
  ---
  ```

The organization script recognizes both formats and converts YAML tags to hashtag format automatically.
