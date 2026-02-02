import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool
from src.main import app
from src.database import get_session
from src.models import Employee, AuditLog
from decimal import Decimal

# Setup in-memory database for testing
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_audit_log_view_details(client: TestClient, session: Session):
    # Create a test employee
    employee = Employee(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        iban="DE123456789",
        tax_id="123456789",
        gross_salary=Decimal("3000.00"),
        tax_class="I",
        has_children=False,
        is_church_member=False,
        state="NRW"
    )
    session.add(employee)
    session.commit()
    session.refresh(employee)

    # Access the employee details
    response = client.get(f"/hr/employees/{employee.id}")
    assert response.status_code == 200

    # Verify audit log
    logs = session.exec(select(AuditLog)).all()
    assert len(logs) == 1
    assert logs[0].employee_id == employee.id
    assert logs[0].action == "VIEW_DETAILS"
    assert "Accessed sensitive data" in logs[0].details

def test_audit_log_calc_payroll(client: TestClient, session: Session):
    # Create a test employee
    employee = Employee(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        iban="DE123456789",
        tax_id="123456789",
        gross_salary=Decimal("3000.00"),
        tax_class="I",
        has_children=False,
        is_church_member=False,
        state="NRW"
    )
    session.add(employee)
    session.commit()
    session.refresh(employee)

    # Trigger payroll calculation
    response = client.post(f"/hr/payroll/calculate/{employee.id}")
    assert response.status_code == 200

    # Verify audit log
    logs = session.exec(select(AuditLog)).all()
    assert len(logs) == 1
    assert logs[0].employee_id == employee.id
    assert logs[0].action == "CALC_PAYROLL"
    assert "Payroll calculation triggered" in logs[0].details
