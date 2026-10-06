"""Build a Happ profile from RoscomVPN and local domain overrides."""
import base64
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = "https://raw.githubusercontent.com/hydraponique/roscomvpn-routing/refs/heads/main/HAPP/DEFAULT.DEEPLINK"
PREFIX = "happ://routing/onadd/"


def build():
    with urllib.request.urlopen(SOURCE, timeout=60) as response:
        upstream = response.read().decode().strip()
    if not upstream.startswith(PREFIX):
        raise ValueError("Unexpected upstream deeplink format")
    profile = json.loads(base64.b64decode(upstream[len(PREFIX):], validate=True))
    overrides = json.loads((ROOT / "custom-rules.json").read_text(encoding="utf-8"))
    keys = ("ProxySites", "DirectSites", "BlockSites")
    if set(overrides) != set(keys):
        raise ValueError("custom-rules.json must contain exactly the three site lists")
    owners = {}
    for key in keys:
        if not isinstance(overrides[key], list):
            raise ValueError(f"{key} must be a list")
        for rule in overrides[key]:
            if not isinstance(rule, str) or not rule.strip() or rule != rule.strip():
                raise ValueError(f"Invalid rule in {key}: {rule!r}")
            if rule in owners and owners[rule] != key:
                raise ValueError(f"Conflicting custom rule: {rule}")
            owners[rule] = key
    for key in keys:
        # Move identical upstream entries to the explicitly selected route.
        profile[key] = list(dict.fromkeys(
            [rule for rule in profile.get(key, []) if rule not in owners]
            + overrides[key]
        ))
    profile["Name"] = "AbobikPopik routing"
    output = ROOT / "HAPP"
    output.mkdir(exist_ok=True)
    target = output / "DEFAULT.JSON"
    if target.exists():
        previous = json.loads(target.read_text(encoding="utf-8"))
        current = dict(profile)
        previous.pop("LastUpdated", None)
        current.pop("LastUpdated", None)
        if previous == current:
            return
    profile["LastUpdated"] = str(int(time.time()))
    payload = json.dumps(profile, ensure_ascii=False, separators=(",", ":")).encode()
    target.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "DEFAULT.DEEPLINK").write_text(PREFIX + base64.b64encode(payload).decode() + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
