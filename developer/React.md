#developer #working 

```bash
npm create vite
```

## Run the vite development server with host exposed

Vite by default binds to `localhost`, so you must expose it:

```bash
npm run dev -- --host 0.0.0.0
```

If you need to change the port, add:

```bash
-- port 3000
```

Is a reference for
```js
"scripts": {

    "dev": "vite",

    "build": "tsc && vite build",

    "preview": "vite preview"

  },
```