#!/usr/bin/env python3
"""Slack slash-command handler for hex code generation."""

from __future__ import annotations

import hmac
import os
import time
from hashlib import sha256

from flask import Flask, jsonify, request

from hex_tool import generate_hex_code

MAX_CODES = 50
MAX_LENGTH = 64

app = Flask(__name__)


def verify_slack_signature(signing_secret: str, body: bytes) -> bool:
    timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
    signature = request.headers.get("X-Slack-Signature", "")
    if not timestamp or not signature:
        return False
    try:
        timestamp_value = int(timestamp)
    except ValueError:
        return False
    if abs(time.time() - timestamp_value) > 60 * 5:
        return False
    sig_basestring = f"v0:{timestamp}:{body.decode('utf-8')}"
    digest = hmac.new(signing_secret.encode("utf-8"), sig_basestring.encode("utf-8"), sha256).hexdigest()
    expected = f"v0={digest}"
    return hmac.compare_digest(expected, signature)


def parse_text(text: str) -> tuple[int, int]:
    parts = [part for part in text.split() if part]
    count = 1
    length = 8
    if parts and parts[0].isdigit():
        count = int(parts[0])
    if len(parts) > 1 and parts[1].isdigit():
        length = int(parts[1])
    if count <= 0 or count > MAX_CODES:
        raise ValueError(f"count must be between 1 and {MAX_CODES}")
    if length <= 0 or length > MAX_LENGTH:
        raise ValueError(f"length must be between 1 and {MAX_LENGTH}")
    return count, length


@app.post("/slack/hex")
def handle_hex() -> tuple[str, int] | tuple[dict[str, str], int]:
    signing_secret = os.environ.get("SLACK_SIGNING_SECRET", "")
    body = request.get_data()
    if not signing_secret or not verify_slack_signature(signing_secret, body):
        return "Unauthorized", 401

    text = request.form.get("text", "")
    try:
        count, length = parse_text(text)
    except ValueError as exc:
        return jsonify({"response_type": "ephemeral", "text": str(exc)}), 200

    codes = [generate_hex_code(length) for _ in range(count)]
    return jsonify({"response_type": "in_channel", "text": "\n".join(codes)}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
