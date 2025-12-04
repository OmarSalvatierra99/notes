Go to project folder
```bash
cd ~/reforzamiento
```

Allow port 
```bash
sudo ufw allow 5173/tcp
```

Run Vite 
```bash
npm run dev -- --host 0.0.0.0
```

Now you can see it in your local browser `http://<your_vps_ip>:5173/` 
