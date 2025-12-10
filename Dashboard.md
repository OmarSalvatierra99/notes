## Inbox / Active Work

```dataview
LIST
FROM #working
SORT file.mtime DESC
```

## Archive / Completed

```dataview
LIST
FROM #completed
SORT file.mtime DESC
```

---

**Workflow:**
- Tag notes with `#working` when actively working on them
- Tag notes with `#completed` when finished (for reference)
