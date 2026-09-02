"""Tests for GET /media?path= (Code changes §3).

No localhost-only restriction is expected/tested here — `/media` being
LAN-reachable and unrestricted to any allow-listed-extension file is an
explicit, accepted tradeoff (Deep Dive Q16), not a bug."""

from __future__ import annotations


def test_valid_image_path_returns_200_with_image_content_type(client, tmp_path):
    image_path = tmp_path / "banner.png"
    # Minimal valid-enough bytes; the endpoint streams the file back as-is,
    # it doesn't validate image contents.
    image_path.write_bytes(b"\x89PNG\r\n\x1a\n" + b"0" * 16)

    res = client.get("/media", params={"path": str(image_path)})
    assert res.status_code == 200
    assert res.headers["content-type"].startswith("image/")


def test_nonexistent_path_is_404(client, tmp_path):
    missing = tmp_path / "does-not-exist.png"
    res = client.get("/media", params={"path": str(missing)})
    assert res.status_code == 404


def test_non_image_extension_is_rejected(client, tmp_path):
    text_file = tmp_path / "notes.txt"
    text_file.write_text("hello")
    res = client.get("/media", params={"path": str(text_file)})
    assert res.status_code == 404


def test_directory_path_is_rejected(client, tmp_path):
    # A directory that happens to end in an allow-listed extension still
    # isn't a file, so it must be rejected gracefully rather than crashing.
    fake_dir = tmp_path / "fake.png"
    fake_dir.mkdir()
    res = client.get("/media", params={"path": str(fake_dir)})
    assert res.status_code == 404
