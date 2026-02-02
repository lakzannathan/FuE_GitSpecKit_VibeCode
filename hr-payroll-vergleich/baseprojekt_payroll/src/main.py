from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from decimal import Decimal
from .database import create_db_and_tables, engine
from .models import Employee
from .routers import hr

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    # Seed Data: Ein Test-Mitarbeiter
    with Session(engine) as session:
        if not session.exec(select(Employee)).first():
            emp = Employee(
                first_name="Max", last_name="Mustermann", email="max@firma.de",
                iban="DE12 3456 7890 0000", tax_id="99 888 777",
                gross_salary=Decimal("4500.00"), tax_class="III",
                has_children=True, is_church_member=True
            )
            session.add(emp)
            session.commit()
    yield

app = FastAPI(title="HR Payroll System (Legacy)", lifespan=lifespan)

app.include_router(hr.router)

@app.get("/")
def root():
    return {"status": "System Online", "version": "1.0.0"}