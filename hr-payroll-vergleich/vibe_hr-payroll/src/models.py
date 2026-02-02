from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from decimal import Decimal

class AuditLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    employee_id: int
    action: str
    details: Optional[str] = None

class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str
    
    # Sensible Daten!
    iban: str 
    tax_id: str
    
    # Gehaltsdaten
    gross_salary: Decimal = Field(max_digits=10, decimal_places=2)
    tax_class: str = "I"
    has_children: bool = False
    is_church_member: bool = False
    state: str = "NRW"

# Hier fehlt das AuditLog Modell!