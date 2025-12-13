import uvicorn
from fastapi import FastAPI, APIRouter, Depends
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from routers import *
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
main_router.include_router(countries_router, tags=['Countries'])
main_router.include_router(cities_router, tags=['Cities'])
main_router.include_router(departments_router, tags=['Departments'])
main_router.include_router(payer_companies_router, tags=['Payer Companies'])
main_router.include_router(currencies_router, tags=['Currencies'])
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
main_router.include_router(invoice_router, tags=['Requests with receipts'])
main_router.include_router(purchase_router, tags=['Purchase'])
main_router.include_router(checker_router, tags=['Checkable requests'])
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
