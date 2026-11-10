import io


def test_login_rejects_bad_password(client):
    r = client.post("/api/auth/login", json={"email": "alice@example.com", "password": "wrong"})
    assert r.status_code == 401


def test_me_requires_token(client):
    assert client.get("/api/documents").status_code == 401


def test_create_rename_and_reopen(client, alice):
    created = client.post(
        "/api/documents", json={"title": "My doc", "content": "<p>hello</p>"}, headers=alice
    )
    assert created.status_code == 201
    doc_id = created.json()["id"]

    client.patch(f"/api/documents/{doc_id}", json={"title": "Renamed"}, headers=alice)

    reopened = client.get(f"/api/documents/{doc_id}", headers=alice).json()
    assert reopened["title"] == "Renamed"
    assert reopened["content"] == "<p>hello</p>"
    assert reopened["is_owner"] is True
    assert reopened["role"] == "owner"


def test_sharing_grants_and_scopes_access(client, alice, bob):
    doc_id = client.post(
        "/api/documents", json={"title": "Secret", "content": "<p>x</p>"}, headers=alice
    ).json()["id"]

    assert client.get(f"/api/documents/{doc_id}", headers=bob).status_code == 404

    share = client.post(
        f"/api/documents/{doc_id}/shares",
        json={"email": "bob@example.com", "permission": "view"},
        headers=alice,
    )
    assert share.status_code == 201

    seen = client.get(f"/api/documents/{doc_id}", headers=bob).json()
    assert seen["is_owner"] is False
    assert seen["role"] == "view"

    assert client.patch(
        f"/api/documents/{doc_id}", json={"content": "<p>hacked</p>"}, headers=bob
    ).status_code == 403

    assert client.delete(f"/api/documents/{doc_id}", headers=bob).status_code in (403, 404)

    bob_list = client.get("/api/documents", headers=bob).json()
    match = [d for d in bob_list if d["id"] == doc_id]
    assert len(match) == 1 and match[0]["is_owner"] is False


def test_editor_share_can_edit_but_not_delete(client, alice, bob):
    doc_id = client.post(
        "/api/documents", json={"title": "Doc", "content": "<p>v1</p>"}, headers=alice
    ).json()["id"]
    client.post(
        f"/api/documents/{doc_id}/shares",
        json={"email": "bob@example.com", "permission": "edit"},
        headers=alice,
    )
    assert client.patch(
        f"/api/documents/{doc_id}", json={"content": "<p>v2</p>"}, headers=bob
    ).status_code == 200
    assert client.delete(f"/api/documents/{doc_id}", headers=bob).status_code == 403


def test_upload_markdown_becomes_rich_text(client, alice):
    md = b"# Title\n\nSome **bold** and a list:\n\n- one\n- two\n"
    r = client.post(
        "/api/documents/upload",
        files={"file": ("notes.md", io.BytesIO(md), "text/markdown")},
        headers=alice,
    )
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == "notes"
    assert "<h1>" in body["content"] and "<strong>" in body["content"] and "<li>" in body["content"]


def test_upload_rejects_unsupported_type(client, alice):
    r = client.post(
        "/api/documents/upload",
        files={"file": ("image.png", io.BytesIO(b"\x89PNG..."), "image/png")},
        headers=alice,
    )
    assert r.status_code == 400


def test_script_is_stripped_on_save(client, alice):
    r = client.post(
        "/api/documents",
        json={"title": "XSS", "content": "<p>ok</p><script>alert(1)</script>"},
        headers=alice,
    )
    assert r.status_code == 201
    assert "<script>" not in r.json()["content"]
    assert "<p>ok</p>" in r.json()["content"]
