from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel import Session, select
from ..database import get_session
from ..models import Employee, AuditLog
from ..legacy_engine import legacy_calculate_net_salary
from sqlmodel import create_engine

router = APIRouter(prefix="/hr", tags=["hr"])

import re

def create_audit_log_entry(employee_id: int, action: str, details: str = None):
    """
    Helper function to create an audit log entry.
    This function is intended to be run in a background task.
    It creates its own session to ensure thread safety and independence from the main request session.
    """
    # Re-import engine to avoid circular imports or context issues if needed,
    # but typically we can import from database.py.
    # For safety in background tasks, we create a new session.
    from ..database import engine
    
    # PII Stripping Logic
    if details:
        # Regex for IBAN (simplified: DE followed by digits/spaces)
        details = re.sub(r'DE\d{2}\s?(\d{4}\s?){4}\d{2}', '[REDACTED IBAN]', details)
        # Regex for Salary (simplified: numbers with decimal/comma)
        details = re.sub(r'\d+[\.,]\d{2}', '[REDACTED SALARY]', details)
        
    with Session(engine) as session:
        log_entry = AuditLog(
            employee_id=employee_id,
            action=action,
            details=details
        )
        session.add(log_entry)
        session.commit()

@router.post("/employees/", response_model=Employee)
def create_employee(employee: Employee, session: Session = Depends(get_session)):
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee

@router.get("/employees/{employee_id}", response_model=Employee)
def get_employee_details(employee_id: int, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    """
    CRITICAL: Gibt IBAN und Steuer-ID zurück.
    MUSS auditiert werden! (Aktuell: Kein Log)
    """
    employee = session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Audit Log (Async)
    background_tasks.add_task(create_audit_log_entry, employee_id, "VIEW_DETAILS", f"Accessed details for {employee.email}")
    
    return employee

@router.post("/payroll/calculate/{employee_id}")
async def run_payroll(employee_id: int, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    """
    Ruft die langsame Legacy-Engine auf.
    MUSS auditiert werden! (Aktuell: Kein Log)
    """
    employee = session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Aufruf der synchronen Legacy Engine (Blockiert!)
    result = legacy_calculate_net_salary(
        gross_amount=employee.gross_salary,
        tax_class=employee.tax_class,
        has_children=employee.has_children,
        is_church_member=employee.is_church_member,
        state=employee.state
    )
    
    # Audit Log (Async)
    background_tasks.add_task(create_audit_log_entry, employee_id, "CALC_PAYROLL", f"Payroll run for {employee.gross_salary}")
    
    return result