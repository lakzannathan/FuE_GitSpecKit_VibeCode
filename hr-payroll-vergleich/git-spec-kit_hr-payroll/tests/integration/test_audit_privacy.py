import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
from src.main import app
from src.database import get_session
from src.models import AuditLog, Employee
from decimal import Decimal

# Setup in-memory database for testing
sqlite_file_name = "database_privacy.db"
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
        first_name="Privacy",
        last_name="Test",
        email="privacy@example.com",
        iban="DE9999999999",
        tax_id="999999999",
        gross_salary=Decimal("9999.99"),
        tax_class="I",
        has_children=False,
        is_church_member=False,
        state="NRW"
    )
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee

def test_audit_log_no_pii(client: TestClient, session: Session, employee: Employee):
    # T012: Integration test verifying details field does not contain IBAN/Salary
    
    # Trigger action
    client.get(f"/hr/employees/{employee.id}")
    
    # Check log
    logs = session.exec(select(AuditLog).where(AuditLog.action == "VIEW_DETAILS")).all()
    assert len(logs) > 0
    log = logs[0]
    
    # Verify NO PII in details
    if log.details:
        assert employee.iban not in log.details
        assert str(employee.gross_salary) not in log.details
        assert employee.tax_id not in log.details

def test_audit_log_payroll_no_pii(client: TestClient, session: Session, employee: Employee):
    # Trigger payroll
    client.post(f"/hr/payroll/calculate/{employee.id}")
    
    logs = session.exec(select(AuditLog).where(AuditLog.action == "CALC_PAYROLL")).all()
    assert len(logs) > 0
    log = logs[0]
    
    if log.details:
        assert employee.iban not in log.details
        assert str(employee.gross_salary) not in log.details
