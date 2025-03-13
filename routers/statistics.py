from datetime import datetime, date
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy import and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import coalesce

from core.session import get_db
from dal.dao import RequestDAO, InvoiceDAO, ContractDAO, FileDAO, LogDAO
from schemas.requests import Requests, Request, UpdateRequest, CreateRequest
from utils.utils import PermissionChecker



statistics_router = APIRouter()




@statistics_router.get("/statistics")
async def get_statistics(
        start_date: date,
        finish_date: date,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Requests": ["read"]}))
):
    requests_statuses = db.query(
        RequestDAO.model.status, func.count(RequestDAO.model.id)
    ).filter(
        RequestDAO.model.created_at.between(start_date, finish_date)
    ).group_by(
        RequestDAO.model.status
    ).all()
    # print("requests_statuses: ", requests_statuses)

    today_paying_requests = db.query(
        func.count(RequestDAO.model.id)
    ).filter(
        and_(
            RequestDAO.model.status == 2,
            func.date(RequestDAO.model.created_at) == datetime.now().date()
        )
    ).all()
    # print("today_paying_requests: ", today_paying_requests)

    expense_statistics = db.query(
        coalesce(func.sum(RequestDAO.model.sum), 0)
    ).filter(
        and_(
            RequestDAO.model.status == 2,
            RequestDAO.model.created_at.between(start_date, finish_date)
        )
    ).all()
    # print("expense_statistics: ", expense_statistics)

    data = {
        "Статус заявок": {status: count for status, count in requests_statuses},
        "Заявки на оплату": today_paying_requests[0][0],
        "Статистика расходов": expense_statistics[0][0],
    }
    return data
