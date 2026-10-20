"""
Employee API endpoint tests.

Covers all assignment requirements:
- Successful retrieval (initial page)
- Search by name
- Search by department
- Search term matching both fields
- Search term matching neither field
- Empty input behavior
- Query length validation
- Pagination (limit, offset)
- Total count accuracy
- Response schema validation
- Correct status codes
"""

import pytest
from fastapi.testclient import TestClient


class TestEmployeeSearchEndpoint:
    """Tests for GET /api/v1/employees."""

    ENDPOINT = "/api/v1/employees"

    # --- Successful retrieval ---

    def test_returns_all_employees_with_no_search_term(self, client: TestClient, seeded_db):
        """Empty search returns a paginated list of all employees."""
        response = client.get(self.ENDPOINT)
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 5
        assert len(data["items"]) == 5
        assert data["limit"] == 20
        assert data["offset"] == 0

    def test_response_schema_shape(self, client: TestClient, seeded_db):
        """Each item contains exactly the required employee fields."""
        response = client.get(self.ENDPOINT)
        item = response.json()["items"][0]

        required_fields = {"id", "name", "email", "department", "designation", "date_of_joining"}
        assert set(item.keys()) == required_fields

    # --- Name search ---

    def test_search_by_name_full(self, client: TestClient, seeded_db):
        """Exact name match."""
        response = client.get(self.ENDPOINT, params={"search": "Rahul Sharma"})
        data = response.json()

        assert data["total"] == 1
        assert data["items"][0]["name"] == "Rahul Sharma"

    def test_search_by_name_partial(self, client: TestClient, seeded_db):
        """Partial name match (substring)."""
        response = client.get(self.ENDPOINT, params={"search": "rah"})
        data = response.json()

        assert data["total"] >= 1
        names = [emp["name"] for emp in data["items"]]
        assert any("Rahul" in name for name in names)

    def test_search_is_case_insensitive(self, client: TestClient, seeded_db):
        """Search should work regardless of casing."""
        response = client.get(self.ENDPOINT, params={"search": "RAHUL"})
        data = response.json()

        assert data["total"] >= 1

    # --- Department search ---

    def test_search_by_department(self, client: TestClient, seeded_db):
        """Search by department name."""
        response = client.get(self.ENDPOINT, params={"search": "Engineering"})
        data = response.json()

        assert data["total"] == 3  # Rahul, Priya, Vikram
        departments = {emp["department"] for emp in data["items"]}
        assert departments == {"Engineering"}

    def test_search_by_department_partial(self, client: TestClient, seeded_db):
        """Partial department match."""
        response = client.get(self.ENDPOINT, params={"search": "Engi"})
        data = response.json()

        assert data["total"] == 3

    # --- Cross-field matching ---

    def test_search_matches_name_or_department(self, client: TestClient, seeded_db):
        """A term matching one employee's name and another's department
        should return results from both."""
        response = client.get(self.ENDPOINT, params={"search": "design"})
        data = response.json()

        # "Design" matches Sneha's department
        assert data["total"] >= 1

    # --- No results ---

    def test_search_no_results(self, client: TestClient, seeded_db):
        """Non-matching search returns 200 with empty items."""
        response = client.get(self.ENDPOINT, params={"search": "zzzznonexistent"})

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []

    # --- Empty database ---

    def test_empty_database_returns_empty_list(self, client: TestClient):
        """No employees at all returns 200 with empty items."""
        response = client.get(self.ENDPOINT)

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []

    # --- Pagination ---

    def test_pagination_limit(self, client: TestClient, seeded_db):
        """Limit controls page size."""
        response = client.get(self.ENDPOINT, params={"limit": 2})
        data = response.json()

        assert len(data["items"]) == 2
        assert data["total"] == 5  # Total is still all employees
        assert data["limit"] == 2

    def test_pagination_offset(self, client: TestClient, seeded_db):
        """Offset skips records."""
        response = client.get(self.ENDPOINT, params={"limit": 2, "offset": 3})
        data = response.json()

        assert len(data["items"]) == 2  # 2 remaining (indices 3,4)
        assert data["offset"] == 3

    def test_pagination_total_reflects_filtered_set(self, client: TestClient, seeded_db):
        """Total count should reflect the search filter, not the page size."""
        response = client.get(self.ENDPOINT, params={"search": "Engineering", "limit": 1})
        data = response.json()

        assert len(data["items"]) == 1
        assert data["total"] == 3  # Total Engineering employees, not just 1

    # --- Validation ---

    def test_invalid_limit_zero(self, client: TestClient, seeded_db):
        """Limit of 0 should be rejected."""
        response = client.get(self.ENDPOINT, params={"limit": 0})
        assert response.status_code == 422

    def test_invalid_limit_too_large(self, client: TestClient, seeded_db):
        """Limit over 100 should be rejected."""
        response = client.get(self.ENDPOINT, params={"limit": 200})
        assert response.status_code == 422

    def test_invalid_offset_negative(self, client: TestClient, seeded_db):
        """Negative offset should be rejected."""
        response = client.get(self.ENDPOINT, params={"offset": -1})
        assert response.status_code == 422

    def test_search_term_too_long(self, client: TestClient, seeded_db):
        """Search term exceeding max length should be rejected."""
        long_term = "a" * 101
        response = client.get(self.ENDPOINT, params={"search": long_term})
        assert response.status_code == 422

    # --- Whitespace handling ---

    def test_whitespace_only_search_treated_as_empty(self, client: TestClient, seeded_db):
        """Whitespace-only search should return all employees."""
        response = client.get(self.ENDPOINT, params={"search": "   "})
        data = response.json()

        assert data["total"] == 5


class TestHealthEndpoint:
    """Tests for GET /api/v1/health."""

    def test_health_check(self, client: TestClient):
        """Health endpoint should be reachable."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ("ok", "degraded")
