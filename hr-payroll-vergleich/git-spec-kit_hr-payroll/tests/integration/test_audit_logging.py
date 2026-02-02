import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
from src.main import app
from src.database import get_session
from src.models import AuditLog, Employee
from decimal import Decimal

# Setup in-memory database for testing
sqlite_file_name = "database.db"
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
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    
    # Patch the engine so background tasks use the test database
    # We need to patch where it is imported in the router
    # Since src.routers.hr imports engine from ..database, we patch src.database.engine
    # But wait, src.routers.hr does: from ..database import engine (inside the function)
    # So we need to patch src.database.engine because that's where it comes from.
    # However, if it was imported at module level, we'd patch src.routers.hr.engine.
    # The implementation does:
    # def create_audit_log_entry(...):
    #     from ..database import engine
    # So we must patch src.database.engine
    
    with patch("src.database.engine", engine):
        client = TestClient(app)
        yield client
    app.dependency_overrides.clear()

@pytest.fixture(name="employee")
def employee_fixture(session: Session):
    employee = Employee(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        iban="DE1234567890",
        tax_id="123456789",
        gross_salary=Decimal("5000.00"),
        tax_class="I",
        has_children=False,
        is_church_member=False,
        state="NRW"
    )
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee

def test_view_details_logging(client: TestClient, session: Session, employee: Employee):
    # T005: Integration test for VIEW_DETAILS logging
    response = client.get(f"/hr/employees/{employee.id}")
    assert response.status_code == 200
    
    # Verify log entry exists
    # Note: In TestClient, BackgroundTasks run synchronously by default unless configured otherwise,
    # but we are testing the outcome. If they run async in test, we might need to wait or force execution.
    # Starlette TestClient runs background tasks.
    
    logs = session.exec(select(AuditLog).where(AuditLog.action == "VIEW_DETAILS")).all()
    assert len(logs) == 1
    assert logs[0].employee_id == employee.id
    assert logs[0].action == "VIEW_DETAILS"

def test_calc_payroll_logging(client: TestClient, session: Session, employee: Employee):
    # T006: Integration test for CALC_PAYROLL logging
    response = client.post(f"/hr/payroll/calculate/{employee.id}")
    assert response.status_code == 200
    
    logs = session.exec(select(AuditLog).where(AuditLog.action == "CALC_PAYROLL")).all()
    assert len(logs) == 1
    assert logs[0].employee_id == employee.id
    assert logs[0].action == "CALC_PAYROLL"
