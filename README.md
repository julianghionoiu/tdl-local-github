# tdl-local-github

Simulate the Github API locally

To run:
```bash
python github-server-wrapper.py start
```

```
Will run and detach from CLI and return to prompt...
Process running as pid: 7997
Is application listening on port 9556?
No. Retrying in 5 seconds
Sun Mar 24 08:27:28 2019 [INFO] Server Starts - localhost:9556
Is application listening on port 9556?
Yes
```

Console mode (blocking):
```bash
python github-server-wrapper.py console
```

```
Entered console mode (blocking, Ctrl-C to breakout)...
Sun Mar 24 08:28:39 2019 [INFO] Server Starts - localhost:9556
```

To stop:
```bash
python github-server-wrapper.py stop
```

```
Kill process with pid: 7997
Is application listening on port 9556?
Yes. Retrying in 5 seconds
Is application listening on port 9556?
No
```