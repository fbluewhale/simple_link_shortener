import pytest
import secrets
import string


class TestRedirectUser:

    @pytest.fixture(autouse=True)
    def setup(self, client, test_db):
        self.client = client
        self.test_db = test_db

    def test_redirect_user_valid_path(self):
        original_link = "https://example.com/"
        response = self.client.post(
            "/api/v1/link/",
            json={
                "original_link": original_link,
                "name": "test"
                + "".join(
                    secrets.choice(string.ascii_letters + string.digits)
                    for _ in range(5)
                ),
            },
        )
        assert response.status_code == 200
        data = response.json()

        response_forward = self.client.get("/" + data.get("shorten_path"))
        assert response_forward.status_code == 200

    def test_redirect_user_invalid_path_404(self):
        response = self.client.get("/avcds")
        assert response.status_code == 404
        assert response.json() == {"detail": "Shorten link not found"}

    def test_redirect_user_invalid_path_422(self):
        response = self.client.get("/avcdsdasdqewq")
        assert response.status_code == 422
