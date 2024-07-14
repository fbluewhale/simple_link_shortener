import pytest
import secrets
import string
from bson import ObjectId


@pytest.mark.asyncio
async def test_get_shorten_links(client, test_db):
    link1 = {"original_link": "https://example.com/", "name": "abcde"}
    link2 = {"original_link": "https://example.org/", "name": "vwxyz"}
    collection = test_db.shorten_link  # Assuming 'links' is your collection name

    collection.insert_many([link1, link2])

    response = client.get("/api/v1/link/")
    assert response.status_code == 200
    data = response.json()

    assert len(data.get("data")) == 2
    assert data.get("total") == 2
    assert data.get("data")[0]["original_link"] == link1["original_link"]
    assert data.get("data")[1]["original_link"] == link2["original_link"]


@pytest.mark.asyncio
async def test_create_shorten_link(client, test_db):
    original_link = "https://example.com/"
    response = client.post(
        "/api/v1/link/",
        json={
            "original_link": original_link,
            "name": "test"
            + "".join(
                secrets.choice(string.ascii_letters + string.digits) for _ in range(5)
            ),
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["original_link"] == original_link
    assert len(data["shorten_path"]) == 5
    collection = test_db.shorten_link
    assert collection.find_one({"_id": ObjectId(data["_id"])}) is not None


@pytest.mark.asyncio
async def test_wrong_shorten_link_creation(client, test_db):
    original_link = "abjdpijds[sak,l;dkwp]"
    response = client.post(
        "/api/v1/link/",
        json={
            "original_link": original_link,
            "name": "test"
            + "".join(
                secrets.choice(string.ascii_letters + string.digits) for _ in range(5)
            ),
        },
    )
    assert response.status_code == 422
    data = response.json()
    assert "original_link" in data["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_wrong_shorten_link_creation(client, test_db):
    original_link = "abjdpijds[sak,l;dkwp]"
    response = client.post(
        "/api/v1/link/",
        json={
            "original_link": original_link,
            "name": "ab"
            + "".join(
                secrets.choice(string.ascii_letters + string.digits) for _ in range(5)
            ),
        },
    )
    assert response.status_code == 422
    data = response.json()
    assert "original_link" in data["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_delete_shorten_link(client, test_db):
    link_to_delete = {"original_link": "https://example.com/", "name": "abcde"}
    collection = test_db.shorten_link
    result = collection.insert_one(link_to_delete)
    link_id = str(result.inserted_id)

    response = client.delete(f"/api/v1/link/{link_id}/")
    assert response.status_code == 200, link_id
    assert response.json() == {"msg": f"Link with id {link_id} has been deleted"}
    assert collection.find_one({"_id": ObjectId(link_id)}) is None


@pytest.mark.asyncio
async def test_wrong_delete_shorten_link(client, test_db):
    link_id = str("6693608a650ed878602a8e33")
    response = client.delete(f"/api/v1/link/{link_id}/")
    assert response.status_code == 404
