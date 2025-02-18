import pytest

from fastapi.testclient import TestClient
from backend.database import get_db, Base, engine
from sqlalchemy.orm import sessionmaker
from backend.config import start_app

app = start_app()

# Configuração do banco de dados de testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def test_db():
    return override_get_db()


@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)  # Cria as tabelas no banco de testes
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)  # Limpa o banco após os testes
