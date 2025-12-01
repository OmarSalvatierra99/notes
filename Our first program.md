```python
input('What is your name?')
```

```
- PythonError: Traceback (most recent call last): File "/lib/python312.zip/_pyodide/_base.py", line 596, in eval_code_async await CodeRunner( File "/lib/python312.zip/_pyodide/_base.py", line 410, in run_async coroutine = eval(self.code, globals, locals) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ File "<exec>", line 1, in <module> OSError: [Errno 29] I/O error
```

This error comes from Pyodide, not from the code itself.
[[Python in Obsidian]] execute Python inside a WebAssembly sandbox (Pyodide), which has several limitations:

- `**OSError: [Errno 29] I/O error**`
	- This error usually means you tried to do an operation Pyodide does NOT allow, such as:
		- Writing files to disk `open('file.txt','w')`
		- Reading local files without passing them through the virtual FS
		- Using libraries that require system-level access 