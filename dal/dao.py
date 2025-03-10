from dal.base import BaseDAO
from models.roles import Roles
from models.permission_groups import PermissionGroups
from models.permissions import Permissions
from models.users import Users
from models.accesses import Accesses
from models.departments import Departments
from models.clients import Clients
from models.expense_types import ExpenseTypes
from models.payment_types import PaymentTypes
from models.buyers import Buyers
from models.suppliers import Suppliers
from models.requests import Requests
from models.contracts import Contracts
from models.invoices import Invoices
from models.files import Files
from models.logs import Logs



class PermissionGroupDAO(BaseDAO):
    model = PermissionGroups


class PermissionDAO(BaseDAO):
    model = Permissions


class RoleDAO(BaseDAO):
    model = Roles


class AccessDAO(BaseDAO):
    model = Accesses


class UserDAO(BaseDAO):
    model = Users


class DepartmentDAO(BaseDAO):
    model = Departments


class ClientDAO(BaseDAO):
    model = Clients


class ExpenseTypeDAO(BaseDAO):
    model = ExpenseTypes


class PaymentTypeDAO(BaseDAO):
    model = PaymentTypes


class BuyerDAO(BaseDAO):
    model = Buyers


class SupplierDAO(BaseDAO):
    model = Suppliers


class RequestDAO(BaseDAO):
    model = Requests


class ContractDAO(BaseDAO):
    model = Contracts


class InvoiceDAO(BaseDAO):
    model = Invoices


class FileDAO(BaseDAO):
    model = Files


class LogDAO(BaseDAO):
    model = Logs
