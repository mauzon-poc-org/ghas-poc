import pytest
import sqlite3
from unittest.mock import patch, MagicMock
from src.app import app


@pytest.fixture
def client():
    """Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# -------------------------------------------------------
# /user endpoint
# -------------------------------------------------------

def test_get_user_returns_200(client):
    """Endpoint /user responde com sucesso quando id é fornecido."""
    with patch("src.app.sqlite3.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchall.return_value = [(1, "alice")]
        mock_connect.return_value = mock_conn

        response = client.get("/user?id=1")
        assert response.status_code == 200


def test_get_user_missing_id(client):
    """Endpoint /user sem parâmetro id não deve causar crash inesperado."""
    with patch("src.app.sqlite3.connect") as mock_connect:
        mock_conn = MagicMock()
        # SQL injection com None — simula comportamento real da vuln
        mock_conn.execute.side_effect = sqlite3.OperationalError("near 'None'")
        mock_connect.return_value = mock_conn

        response = client.get("/user")
        # Esperamos um erro (500) — a vuln existe propositalmente na PoC
        assert response.status_code == 500


def test_get_user_sql_injection_vector(client):
    """
    Documenta o vetor de SQL Injection presente propositalmente.
    Este teste NÃO valida que a injeção foi bloqueada —
    ele serve para deixar explícito no CI que a vuln existe e é monitorada pelo CodeQL.
    """
    with patch("src.app.sqlite3.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchall.return_value = []
        mock_connect.return_value = mock_conn

        # Vetor clássico de SQL Injection
        response = client.get("/user?id=1 OR 1=1--")
        # Passa pelo endpoint (vuln ativa) — CodeQL detecta no SAST
        assert response.status_code == 200


# -------------------------------------------------------
# /ping endpoint
# -------------------------------------------------------

def test_ping_returns_200(client):
    """Endpoint /ping responde com sucesso quando host é fornecido."""
    with patch("src.app.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)

        response = client.get("/ping?host=127.0.0.1")
        assert response.status_code == 200


def test_ping_command_injection_vector(client):
    """
    Documenta o vetor de Command Injection presente propositalmente.
    Assim como o SQL Injection, este teste serve para deixar explícito
    no CI que a vuln existe e é coberta pelo CodeQL.
    """
    with patch("src.app.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)

        # Vetor clássico de Command Injection
        response = client.get("/ping?host=127.0.0.1; whoami")
        # Passa pelo endpoint (vuln ativa) — CodeQL detecta no SAST
        assert response.status_code == 200


def test_ping_missing_host(client):
    """Endpoint /ping sem parâmetro host não deve causar crash inesperado."""
    with patch("src.app.subprocess.run") as mock_run:
        mock_run.side_effect = TypeError("expected str, got NoneType")

        response = client.get("/ping")
        assert response.status_code == 500
