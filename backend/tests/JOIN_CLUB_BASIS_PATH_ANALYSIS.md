# Basis Path Testing: Join Club Use Case

## Control Flow Graph

```
join(club_id, member_id, user_id)
    │
    ├─> D1: Is member_id == user_id?
    │   ├─ NO  → raise 403 Forbidden (route guard)
    │   └─ YES → call service.join_club(user_id, club_id)
    │
    └─> join_club(user_id, club_id)
            │
            ├─> get_user(user_id, session)
            │
            ├─> get_club(club_id, session)
            │
            ├─> D2: Does the club exist?
            │   ├─ NO  → raise 404 Not Found
            │   └─ YES → continue
            │
            ├─> D3: Is user already a member?
            │   ├─ YES → raise 400 Bad Request
            │   └─ NO  → continue
            │
            ├─> club.members.append(user)
            │
            ├─> save_club(club, session)
            │
            ├─> session.refresh(club)
            │
            └─> return club
```

## Decision Points

1. **D1** (route layer): Is `member_id == user_id`?
   - Prevents a user from joining a club on behalf of someone else.
2. **D2** (service layer): Does the club exist in the database?
   - `get_club()` returns `None` if the club_id is not found.
3. **D3** (service layer): Is the user already a member of the club?
   - Checked by scanning `club.members` for a matching `id`.

## Cyclomatic Complexity

V(G) = number of decision points + 1 = 3 + 1 = **4 independent paths**

## Independent Basis Paths

### Path 1: Club Not Found

- **Flow:** D1=True, D2=False
- **Scenario:** The requested club does not exist in the database.
- **Input:**
  - user_id: 1
  - member_id: 1
  - club_id: 99
- **Expected:** HTTPException 404 with detail `"Club not found"`. `save_club` is never called.

### Path 2: User Already a Member

- **Flow:** D1=True, D2=True, D3=True
- **Scenario:** Club exists but the user is already listed as a member.
- **Input:**
  - user_id: 1
  - member_id: 1
  - club_id: 10
  - club.members already contains user with id=1
- **Expected:** HTTPException 400 with detail `"Already a member"`. `save_club` is never called.

### Path 3: Successful Join

- **Flow:** D1=True, D2=True, D3=False
- **Scenario:** Club exists and the user is not yet a member.
- **Input:**
  - user_id: 5
  - member_id: 5
  - club_id: 10
  - club.members is empty
- **Expected:** User is appended to `club.members`, `save_club` is called once, and the updated club is returned.

### Path 4: Join on Behalf of Another User (Route Guard)

- **Flow:** D1=False
- **Scenario:** Authenticated user attempts to join a club using a different user's member_id.
- **Input:**
  - user_id (authenticated): 1
  - member_id (in path): 2
  - club_id: 10
- **Expected:** HTTPException 403 with detail `"Cannot join a club on behalf of another user"`. The service layer is never reached.

## Test Coverage

All 4 basis paths are covered in [test_join_club.py](test_join_club.py):

- `test_path1_club_not_found()` — Path 1
- `test_path2_user_already_a_member()` — Path 2
- `test_path3_successful_join()` — Path 3
- `test_path4_join_on_behalf_of_another_user_is_forbidden()` — Path 4
  Additional tests cover edge cases and route pass-through behaviour:

- `test_owner_joins_as_member()` — owner joining their own club as a member
- `test_route_delegates_to_service_when_ids_match()` — verifies route calls service correctly

## Running Tests

```bash
cd backend
python -m pytest tests/test_join_club.py -v
```

## Dependencies Required

Ensure these are in requirements.txt:

```
pytest>=7.0.0
pytest-mock>=3.10.0
```
