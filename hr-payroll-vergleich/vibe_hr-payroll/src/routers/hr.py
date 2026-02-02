from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import Employee, AuditLog
from ..legacy_engine import legacy_calculate_net_salary

router = APIRouter(prefix="/hr", tags=["hr"])

@router.post("/employees/", response_model=Employee)
def create_employee(employee: Employee, session: Session = Depends(get_session)):
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee

@router.get("/employees/{employee_id}", response_model=Employee)
def get_employee_details(employee_id: int, session: Session = Depends(get_session)):
    """
    CRITICAL: Gibt IBAN und Steuer-ID zurück.
    MUSS auditiert werden! (Aktuell: Kein Log)
    """
    employee = session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Audit Log
    log_entry = AuditLog(
        employee_id=employee_id,
        action="VIEW_DETAILS",
        details=f"Accessed sensitive data for employee {employee_id}"
    )
    session.add(log_entry)
    session.commit()
    
    return employee

@router.post("/payroll/calculate/{employee_id}")
async def run_payroll(employee_id: int, session: Session = Depends(get_session)):
    """
    Ruft die langsame Legacy-Engine auf.
    MUSS auditiert werden! (Aktuell: Kein Log)
    """
    employee = session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Audit Log
    log_entry = AuditLog(
        employee_id=employee_id,
        action="CALC_PAYROLL",
        details=f"Payroll calculation triggered for employee {employee_id}"
    )
    session.add(log_entry)
    session.commit()
    
    # Aufruf der synchronen Legacy Engine (Blockiert!)
    result = legacy_calculate_net_salary(
        gross_amount=employee.gross_salary,
        tax_class=employee.tax_class,
        has_children=employee.has_children,
        is_church_member=employee.is_church_member,
        state=employee.state
    )
    
    return result