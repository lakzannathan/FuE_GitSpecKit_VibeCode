from fastapi import APIRouter, HTTPException
from src.database import SessionDep
from src.schemas.order import OrderCreate, OrderRead
from src.services.sales import SalesService

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("", response_model=OrderRead, status_code=201)
def create_order(order_in: OrderCreate, session: SessionDep):
    service = SalesService(session)
    try:
        return service.create_order(order_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
