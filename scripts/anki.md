## Anki Sync via AnkiConnect

### Setup
1. Install AnkiConnect add-on in Anki
   - Tools > Add-ons > Get Add-ons
   - Code: **2055492159**
   - Restart Anki
2. Keep Anki running when syncing
3. Run: `python scripts/anki.py`

### Card Template Format
Create notes in `anki/` folder using this structure:

```markdown
Front:
Your question here

Back:
Your answer here
```

Optional: Add a unique ID in YAML frontmatter (recommended for consistent tracking):
```markdown
---
id: my-unique-id
---
Front:
Your question here

Back:
Your answer here
```

If no ID is provided, one will be auto-generated based on the file path.

### Features
✅ Direct sync to Anki (no manual import)
✅ **Smart updates** - syncing the same file twice updates the card instead of creating duplicates
✅ **Unique ID tracking** - each note tracked by ID (YAML or auto-generated)
✅ **Obsidian image support** - both `![[image.png]]` and `![alt](image.png)` formats work
✅ Markdown formatting (bold, italic, lists, code)
✅ Auto-tagged with "obsidian" and unique ID tag

### Image Usage
- Put images in `media/` folder
- Obsidian wiki-style: `![[image-name.png]]` ✅
- Standard markdown: `![description](image-name.png)` ✅
- Supported: jpg, png, gif, webp, bmp, svg
- Images are automatically uploaded to Anki

### How Updates Work
1. Each note gets a unique ID (from YAML `id:` field or auto-generated from file path)
2. ID is stored as an Anki tag: `obsidian-id-{id}`
3. When syncing:
   - If card with that ID exists → **updates** the existing card
   - If card doesn't exist → **creates** a new card
4. You can edit your Obsidian notes and re-sync to update cards in Anki!

### Example Files
See `anki/Sample Card.md` and `anki/Example with Image.md` for examples.