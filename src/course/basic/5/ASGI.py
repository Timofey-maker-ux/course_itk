import json

import httpx

API_PROVIDER = "https://api.exchangerate-api.com/v4/latest/"


async def app(scope, receive, send):
    if scope["type"] != "http":
        return

    path = scope.get("path", "/")
    currency = path.strip("/").upper()

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(API_PROVIDER + currency)
            resp.raise_for_status()
            data = resp.json()
        status = 200
    except Exception as e:
        data = {"error": str(e)}
        status = 502

    body = json.dumps(data).encode()

    await send(
        {
            "type": "http.response.start",
            "status": status,
            "headers": [(b"content-type", b"application/json")],
        }
    )
    await send({"type": "http.response.body", "body": body})
