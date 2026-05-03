# Basis Path Testing: Create Post Use Case

## Control Flow Graph

```
create_post(user_id, data)
    │
    ├─> Create Post object
    │
    ├─> D1: Is text provided?
    │   ├─ NO  → post.text = None
    │   └─ YES → post.text = data.text
    │
    ├─> D2: Is workout_id provided?
    │   ├─ NO  → post.workout_id = None
    │   └─ YES → post.workout_id = data.workout_id
    │
    ├─> D3: Is club_id provided?
    │   ├─ NO  → post.club_id = None
    │   └─ YES → post.club_id = data.club_id
    │
    ├─> save_post(post, session)
    │
    ├─> session.refresh(post)
    │
    └─> return post
```

## Decision Points

1. **D1** (implicit in data validation): Is text provided and not None?
   - Post has textual content?
   
2. **D2** (implicit in data validation): Is workout_id provided and not None?
   - Post is associated with a workout?
   
3. **D3** (implicit in data validation): Is club_id provided and not None?
   - Post is associated with a club?

## Cyclomatic Complexity

V(G) = 2^(decision branches) = **4 independent paths**

## Independent Basis Paths

### Path 1: Minimal Post (Text Only)
- **Flow:** D1=True, D2=False, D3=False
- **Scenario:** Create a basic text-only post without workout or club context
- **Input:**
  - user_id: 1
  - text: "Just had a great workout session!"
  - workout_id: None
  - club_id: None
- **Expected:** Post created with text, user_id set, workout_id and club_id are None

### Path 2: Workout Post (Text + Workout)
- **Flow:** D1=True, D2=True, D3=False
- **Scenario:** Create a post tied to a specific workout session
- **Input:**
  - user_id: 1
  - text: "Crushed my leg day!"
  - workout_id: 42
  - club_id: None
- **Expected:** Post created with text and workout_id set, club_id is None

### Path 3: Club Post (Text + Club)
- **Flow:** D1=True, D2=False, D3=True
- **Scenario:** Create a post for a specific gym club
- **Input:**
  - user_id: 1
  - text: "Amazing workout with the crew!"
  - workout_id: None
  - club_id: 15
- **Expected:** Post created with text and club_id set, workout_id is None

### Path 4: Full Post (Text + Workout + Club)
- **Flow:** D1=True, D2=True, D3=True
- **Scenario:** Create a post with all contextual information
- **Input:**
  - user_id: 1
  - text: "Logged a new personal record!"
  - workout_id: 42
  - club_id: 15
- **Expected:** Post created with text, workout_id, and club_id all set

## Test Coverage

All 4 basis paths are covered in [test_create_post_basis_path.py](test_create_post_basis_path.py):

- `test_path1_minimal_post_text_only()` - Path 1
- `test_path2_workout_post()` - Path 2  
- `test_path3_club_post()` - Path 3
- `test_path4_full_post_all_fields()` - Path 4

Additional integration tests verify the route endpoint behavior.

## Running Tests

```bash
cd backend
python -m pytest tests/test_create_post_basis_path.py -v
```

## Dependencies Required

Ensure these are in requirements.txt:
```
pytest>=7.0.0
pytest-mock>=3.10.0
```
