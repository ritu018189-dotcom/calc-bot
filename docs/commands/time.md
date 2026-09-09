# `/time`

```
/time <city>
```

Example: `/time London`

Matches `<city>` (case-insensitive, spaces → underscores) against the last
segment of every zone in `pytz.all_timezones` (e.g. `Europe/London` →
`london`), either as an exact match or a substring match, and returns the
current time there.

If no zone matches, replies with an error — try a more specific or
differently-spelled city name.
