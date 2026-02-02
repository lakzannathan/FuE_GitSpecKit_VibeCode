from sqlmodel import SQLModel, Session, create_engine

sqlite_file_name = "payroll.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
# Check same thread false ist wichtig für SQLite in Async Apps
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    # Import models to ensure they are registered with SQLModel.metadata
    from .models import Employee, AuditLog
    SQLModel.metadata.create_all(engine)