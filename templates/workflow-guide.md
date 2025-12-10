# Workflow Guide

## Minimalist Two-Tag System

### Quick Reference

| Tag | Purpose | Dashboard Section |
|-----|---------|------------------|
| `#working` | Active work, inbox items | Inbox / Active Work |
| `#completed` | Finished notes, archive | Archive / Completed |

### How to Use

**Starting a new note:**
```markdown
#developer #working

Your content here...
```

**Finishing a note:**
```markdown
#developer #completed

Your content here...
```

### Tag Combinations

The workflow tags (`#working`, `#completed`) work with organization tags:

- `#developer #working` - Active development note → stays in developer/
- `#ideas #working` - Active idea → stays in brain/
- `#art #completed` - Completed art note → stays in art/
- `#auditoria #completed` - Completed audit research → stays in auditoria-gubernamental/

### Dashboard

View [Dashboard.md](../Dashboard.md) to see:
- All `#working` notes across all folders (sorted by recent)
- All `#completed` notes for reference (sorted by recent)

### Dataview Queries

**Inbox / Active Work:**
```dataview
LIST
FROM #working
SORT file.mtime DESC
```

**Archive / Completed:**
```dataview
LIST
FROM #completed
SORT file.mtime DESC
```

### Tips

- **Keep it simple:** Only use these two tags for workflow tracking
- **No extra metadata:** No fields, no complex properties needed
- **Works everywhere:** Tags work across all folders automatically
- **Recent first:** Most recently modified notes appear at the top
- **Independent systems:** Workflow tags don't interfere with organization tags
