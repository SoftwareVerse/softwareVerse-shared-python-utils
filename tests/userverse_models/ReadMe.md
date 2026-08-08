# Userverse Models Tests

These tests cover the shared Pydantic models in `src/userverse_models`:
- `user/user.py`: login, create/update/read, token response, and query params
- `user/password.py`: password reset and OTP models
- `company/address.py`: address model
- `company/company.py`: company create/update/read and query params
- `company/user.py`: company user add/read models
- `company/roles.py`: role enums and role models
- `permissions.py`: global and company-scoped RBAC permission models

## How to run
From the repository root:

```bash
pytest tests/userverse_models
```

From the module folder:

```bash
cd tests/userverse_models
pytest .
```
