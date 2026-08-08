# softwareVerse-shared-python-utils

Shared Pydantic models for Userverse services, clients, and downstream Python integrations.

## What This Package Is For

Use this package when you want one source of truth for:

- Userverse request payloads
- Userverse response payloads
- Pagination wrappers
- Reusable validators such as phone number validation

This keeps API services, SDKs, and app integrations aligned on the same schema.

## Installation

Install from GitHub:

```bash
pip install git+https://github.com/SoftwareVerse/softwareVerse-shared-python-utils.git@v0.1.11
```

With `uv`:

```bash
uv add git+https://github.com/SoftwareVerse/softwareVerse-shared-python-utils.git@v0.1.11
```

Editable local install:

```bash
git clone https://github.com/SoftwareVerse/softwareVerse-shared-python-utils.git
cd softwareVerse-shared-python-utils
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Python And Dependency Support

- Python: `>=3.12`
- Pydantic: `>=2`

## Package Layout

- `userverse_models.user`: user auth, profile, password, and token models
- `userverse_models.company`: company, company-user, and company-role models
- `userverse_models.permissions`: global and company-scoped RBAC permission models
- `sverse_generic_models`: generic API response and pagination wrappers
- `sverse_validators`: shared validation helpers

## Typical Usage

### User models

```python
from userverse_models.user.user import (
    UserCreateModel,
    UserLoginModel,
    UserReadModel,
    RefreshTokenRequestModel,
)
from userverse_models.user.password import PasswordResetRequest

user = UserCreateModel(
    first_name="Ada",
    last_name="Lovelace",
    phone_number="+27821234567",
)

credentials = UserLoginModel(
    email="ada@example.com",
    password="strong-password",
)

refresh = RefreshTokenRequestModel(refresh_token="refresh-token")
reset = PasswordResetRequest(email="ada@example.com")
```

### Company models

```python
from userverse_models.company.address import CompanyAddressModel
from userverse_models.company.company import CompanyCreateModel
from userverse_models.company.user import CompanyUserAddModel
from userverse_models.company.roles import RoleCreateModel

company = CompanyCreateModel(
    name="Acme",
    email="info@acme.co.za",
    address=CompanyAddressModel(
        street="123 Main St",
        city="Cape Town",
        country="South Africa",
    ),
)

membership = CompanyUserAddModel(
    email="member@acme.co.za",
    role="Viewer",
)

role = RoleCreateModel(
    name="Supervisor",
    description="Can manage approvals",
)
```

### Permission models

```python
from userverse_models.permissions import (
    PermissionCreateModel,
    PermissionQueryParamsModel,
    PermissionReadModel,
    PermissionUpdateModel,
)

permission = PermissionCreateModel(
    name="invoice.approve",
    description="Approve company invoices",
)
filters = PermissionQueryParamsModel(name="invoice", page=1, limit=25)
```

### Generic API wrappers

```python
from sverse_generic_models.generic_response import GenericResponseModel
from sverse_generic_models.generic_pagination import PaginatedResponse
from userverse_models.user.user import UserReadModel

response: GenericResponseModel[UserReadModel]
page: GenericResponseModel[PaginatedResponse[UserReadModel]]
```

## Best Practices

- Pin a release tag in downstream apps instead of tracking the repo head.
- Reuse these models in both client code and tests so API drift is caught early.
- Prefer the typed request models over ad hoc dict payloads.
- Treat UUID ids as strings at the transport boundary unless your app needs `UUID` objects directly.
- Keep this package schema-focused. Avoid putting service logic here.

## When To Update This Repo

Update this package whenever Userverse changes:

- endpoint request bodies
- endpoint response bodies
- authentication token shapes
- pagination wrappers
- shared validation rules

If the API changes first, update this repo before or alongside SDK changes.

## Development

Run tests:

```bash
uv run pytest
```

Target the model tests directly:

```bash
PYTHONPATH=src uv run python -m pytest tests/userverse_models
```
