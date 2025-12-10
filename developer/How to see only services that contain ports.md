#developer #working 
Replace `500[0-9]` with whatever range you want:

```bash
grep -RniE ":[0-9]{4}" /etc/systemd/system/
```

This shows only lines that contain `:####` (addresses with ports).