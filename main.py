import uvicorn
from fastapi import FastAPI, APIRouter, Depends
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from routers.life_span import combined_lifespan
from routers.roles import roles_router
from routers.users import users_router
from routers.permissions import permissions_router
from routers.departments import departments_router
from routers.expense_types import expense_types_router
from routers.payment_types import payment_types_router
from routers.clients import clients_router
from routers.buyers import buyers_router
from routers.suppliers import suppliers_router
from routers.requests import requests_router
from routers.files import files_router
from routers.contracts import contracts_router
from routers.logs import logs_router
from routers.statistics import statistics_router
from routers.accounting import accounting_router
from routers.settings import settings_router
from routers.budgets import budgets_router
from routers.transactions import transactions_router
from routers.transfers import transfers_router
from routers.payer_companies import payer_companies_router
from routers.limits import limits_router
from routers.purchase import purchase_router
from utils.utils import get_current_user_for_docs


app = FastAPI(
    lifespan=combined_lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui(current_user: str = Depends(get_current_user_for_docs)):
    return get_swagger_ui_html(
        openapi_url="/docs/openapi.json",
        title="Finance System ...",
        swagger_ui_parameters={"docExpansion": "none"}
    )


@app.get("/docs/openapi.json", include_in_schema=False)
def get_open_api_endpoint(username: str = Depends(get_current_user_for_docs)):
    return JSONResponse(get_openapi(title="Secure API", version="1.0.0", routes=app.routes))


main_router = APIRouter()


main_router.include_router(permissions_router, tags=['Permissions'])
main_router.include_router(roles_router, tags=['Roles'])
main_router.include_router(users_router, tags=['Users'])
main_router.include_router(clients_router, tags=['Clients'])
main_router.include_router(departments_router, tags=['Departments'])
main_router.include_router(payer_companies_router, tags=['Payer Companies'])
main_router.include_router(budgets_router, tags=['Budgets'])
main_router.include_router(limits_router, tags=['Limits'])
main_router.include_router(transactions_router, tags=['Transactions'])
main_router.include_router(expense_types_router, tags=['Expense Types'])
main_router.include_router(payment_types_router, tags=['Payment Types'])
main_router.include_router(buyers_router, tags=['Buyers'])
main_router.include_router(suppliers_router, tags=['Suppliers'])
main_router.include_router(requests_router, tags=['Requests'])
main_router.include_router(statistics_router, tags=['Statistics'])
main_router.include_router(accounting_router, tags=['Accounting'])
main_router.include_router(purchase_router, tags=['Purchase'])
main_router.include_router(transfers_router, tags=['Transfers'])
main_router.include_router(logs_router, tags=['Logs'])
main_router.include_router(files_router, tags=['Files'])
main_router.include_router(contracts_router, tags=['Contracts'])
main_router.include_router(settings_router, tags=['Settings'])



app.include_router(main_router)

add_pagination(app)


app.mount("/files", StaticFiles(directory="files"), name="files")



origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
