# Basis Path Testing: Login Use Case

## Control Flow Graph

```
login_user(credentials)
    │
    ├─> authenticate_user(email, password)
    │       │
    │       ├─> get_user_by_email(email)
    │       │       │
    │       │       ├─> D1: user exists?
    │       │       │   ├─ NO  → verify_password(dummy) → return False
    │       │       │   └─ YES ↓
    │       │       │
    │       │       └─> D2: verify_password(password, user.password)?
    │       │           ├─ NO  → return False
    │       │           └─ YES → return user
    │       │
    │       └─> return user or False
    │
    └─> D3: user is truthy?
        ├─ NO  → return None
        └─ YES → create_access_token() → return LoginResponse
```

## Decision Points

1. **D1** (line 15 in auth_service.py): `if not user:`
   - User exists in database?
   
2. **D2** (line 19 in auth_service.py): `if not verify_password(...)`
   - Password verification succeeds?
   
3. **D3** (line 38 in auth_service.py): `if not user:`
   - Authentication result is valid?

## Cyclomatic Complexity

V(G) = E - N + 2P
V(G) = 3 decisions + 1 = **4 independent paths**

## Independent Basis Paths

### Path 1: User Not Found
- **Flow:** D1=False
- **Scenario:** Email does not exist in database
- **Input:**
  - email: "nonexistent@example.com"
  - password: "any_password"
- **Expected:** authenticate_user returns False → login_user returns None → 401 HTTPException

### Path 2: Wrong Password
- **Flow:** D1=True, D2=False
- **Scenario:** User exists but password is incorrect
- **Input:**
  - email: "user@example.com" (exists)
  - password: "wrong_password"
- **Expected:** verify_password returns False → authenticate_user returns False → login_user returns None → 401 HTTPException

### Path 3: Authentication Returns Falsy
- **Flow:** D1=True, D2=True, D3=False
- **Scenario:** User authenticated but returns falsy value
- **Input:**
  - Mock authenticate_user to return False/None
- **Expected:** login_user returns None → 401 HTTPException
- **Note:** This path is theoretically possible if authenticate_user is modified to return None/False despite password matching

### Path 4: Successful Login
- **Flow:** D1=True, D2=True, D3=True
- **Scenario:** Valid credentials, user authenticated successfully
- **Input:**
  - email: "user@example.com" (exists)
  - password: "correct_password" (matches hash)
- **Expected:** Returns LoginResponse with access_token, token_type="bearer", and user object

## Test Coverage

All 4 basis paths are covered in [test_login_basis_path.py](test_login_basis_path.py):

- `test_path1_user_not_found()` - Path 1
- `test_path2_wrong_password()` - Path 2  
- `test_path3_authentication_returns_falsy()` - Path 3
- `test_path4_successful_login()` - Path 4

Additional integration tests verify the route endpoint behavior.

## Running Tests

```bash
cd backend
pytest tests/test_login_basis_path.py -v
```

## Dependencies Required

Ensure these are in requirements.txt:
```
pytest>=7.0.0
pytest-mock>=3.10.0
```
