import pytest
import time
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
from src.main import app
from src.database import get_session
from src.models import AuditLog, Employee
from decimal import Decimal

# Setup in-memory database for testing
sqlite_file_name = "database_perf.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session_override():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = get_session_override

@pytest.fixture(name="session")
def session_fixture():
    create_db_and_tables()
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    from unittest.mock import patch
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    with patch("src.database.engine", engine):
        client = TestClient(app)
        yield client
    app.dependency_overrides.clear()

@pytest.fixture(name="employee")
def employee_fixture(session: Session):
    employee = Employee(
        first_name="Perf",
        last_name="Test",
        email="perf@example.com",
        iban="DE1111111111",
        tax_id="111111111",
        gross_salary=Decimal("1000.00"),
        tax_class="I",
        has_children=False,
        is_church_member=False,
        state="NRW"
    )
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee

def test_async_logging_performance(client: TestClient, session: Session, employee: Employee):
    # T016: Performance/async verification test
    # Note: TestClient runs background tasks synchronously after the response is sent.
    # To truly test async behavior, we would need a live server or mock the background task execution.
    # However, we can verify that the response is successful and fast enough.
    
    start_time = time.time()
    response = client.get(f"/hr/employees/{employee.id}")
    end_time = time.time()
    
    assert response.status_code == 200
    duration = end_time - start_time
    
    # This is a very loose check because TestClient is synchronous for background tasks
    # But it ensures no massive blocking overhead is added by the task definition itself.
    assert duration < 1.0 # Should be very fast
    
    # Verify log was created (TestClient executes tasks)
    logs = session.exec(select(AuditLog).where(AuditLog.action == "VIEW_DETAILS")).all()
    assert len(logs) == 1
