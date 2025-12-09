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

Both scripts require updating the `VAULT_PATH` constant to match your local path before execution:

```python
VAULT_PATH = r"C:\Users\Usuario\Documents\Personal\notas"
```

Run scripts using:
```bash
python scripts/organized-vault.py
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
- Only the first matching tag moves the file
- Hidden folders and `.obsidian/` are skipped
- Duplicate filenames are auto-renamed with counters
- Supports both inline tags (`#tag`) and YAML frontmatter tags
- Interactive mode with dry-run option and debug mode

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
- **obsidian-git** - Git version control integration
- **obsidian-excalidraw-plugin** - Drawing and diagrams
- **templater-obsidian** - Advanced templating
- **pdf-plus** - Enhanced PDF handling
- **oz-clear-unused-images** - Cleanup unused media
- **background-image** - Customization

## Templates

**anki.md** - Basic Anki flashcard template with Front/Back structure

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
