"""Verify downloaded wheels against the authoritative PyPI release metadata."""

import hashlib
import json
from pathlib import Path
from urllib.request import urlopen


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    records = []
    wheels = sorted((root / "wheelhouse").glob("*.whl"))
    if not wheels:
        raise RuntimeError("No wheels to verify")
    for wheel in wheels:
        name, version = wheel.name.split("-")[:2]
        url = f"https://pypi.org/pypi/{name}/{version}/json"
        with urlopen(url, timeout=30) as response:
            release = json.load(response)
        matches = [item for item in release["urls"] if item["filename"] == wheel.name]
        if len(matches) != 1:
            raise RuntimeError(f"Wheel absent or ambiguous on PyPI: {wheel.name}")
        expected = matches[0]["digests"]["sha256"]
        actual = hashlib.sha256(wheel.read_bytes()).hexdigest()
        if actual != expected:
            raise RuntimeError(f"SHA-256 mismatch: {wheel.name}")
        records.append(
            {"filename": wheel.name, "sha256": actual, "metadata": url,
             "canonical_url": matches[0]["url"]}
        )
        print(f"VERIFIED {wheel.name}", flush=True)
    output = root / "results" / "wheel-provenance.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
