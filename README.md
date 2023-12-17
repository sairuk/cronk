# cronk
crappy little monitor (cron wannabe), completely unecessary in its
current state, code is garbage

supposed to be extended to monitor repos and build things with a webui
but for now it'll just run scripts with pycron

runs on a 60s loop, reviewing the cron data and run scripts, launch in 
user context from systemd or however you like

```
TDIR=~/.local/share/systemd/user
mkdir -p $TDIR
cp cronk.service.example $TDIR/cronk.service
systemctl --user daemon-reload
systemctl --user start cronk.service
systemctl --user enable cronk.service
```

see the config example and save it as `~/cronk.yaml`

pycron is packaged in this repo, main project is python-cron
