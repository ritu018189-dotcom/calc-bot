# Running the webhook example behind TLS

`examples/flask_webhook.py` (see [architecture.md](../architecture.md) for
why this isn't the default) needs an HTTPS URL — Telegram refuses to send
updates to a plain HTTP webhook. Flask's dev server doesn't terminate TLS
itself, so put it behind a reverse proxy that does:

1. Get a certificate for your domain (e.g. `certbot certonly --nginx -d bot.example.com`).
2. Use `examples/nginx-reverse-proxy.conf` as a starting point — it
   terminates TLS on 443 and forwards `/webhook` to `127.0.0.1:8080`, where
   `flask_webhook.py` listens.
3. Set `WEBHOOK_URL=https://bot.example.com/webhook` and run
   `python examples/flask_webhook.py`.

If you'd rather not manage a reverse proxy and certificate yourself, stick
with `main.py`'s default long-polling mode — it needs no public URL at all.
