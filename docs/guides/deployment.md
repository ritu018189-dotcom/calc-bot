# Deployment

The bot polls Telegram (no inbound webhook needed) and also runs a tiny
Flask server on port 8080 so host platforms that require an HTTP health
check don't kill the process for "not listening on a port."

## Docker

```bash
docker build -t calc-bot .
docker run --env-file .env -p 8080:8080 calc-bot
```

Or with `deploy/docker-compose.yml`:

```bash
docker compose -f deploy/docker-compose.yml up --build
```

## Render

`deploy/render.yaml` defines a background worker. Push the repo, connect it
on [render.com](https://render.com), and set `BOT_TOKEN` in the service's
environment variables — never commit it.

## Railway

`deploy/railway.json` gives Railway the start command. Set `BOT_TOKEN` under
the project's Variables tab.

## Bare metal / VPS (systemd)

Copy `deploy/systemd/calc-bot.service` to `/etc/systemd/system/`, edit the
`WorkingDirectory`/`EnvironmentFile` paths, then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now calc-bot
```
