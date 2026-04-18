# Karpathy Coding Guard — Example Anti-Patterns

> **Source:** Adapted from [forrestchang/andrej-karpathy-skills/EXAMPLES.md](https://github.com/forrestchang/andrej-karpathy-skills)
> (Apache-2.0). Examples are generic Python; see the parent SKILL.md for
> project-specific Go/Fiber + React/FSD anti-patterns.

---

## 1. Think Before Coding

### Hidden Assumptions

**User request:** "Add a feature to export user data"

**Wrong — silent assumptions:**

```python
def export_users(format='json'):
    users = User.query.all()          # assumed ALL users
    if format == 'json':
        with open('users.json', 'w') as f:   # assumed file location
            json.dump([u.to_dict() for u in users], f)
    elif format == 'csv':
        with open('users.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'email', 'name'])  # assumed fields
            writer.writeheader()
            writer.writerows([u.to_dict() for u in users])
    return f"Exported {len(users)} users"
```

**Right — surface assumptions first:**

```
Before implementing, I need to clarify:

1. Scope: Export all users or filtered subset? (privacy implications)
2. Format: Download file? Background job? API endpoint?
3. Fields: Which user fields? (some might be sensitive)
4. Volume: How many users typically? (affects approach)

Simplest approach: Add an API endpoint that returns paginated JSON.
```

### Multiple Interpretations

**User request:** "Make the search faster"

**Wrong — pick silently and over-engineer:**

```python
@lru_cache(maxsize=1000)
async def search(query: str) -> List[Result]:
    # 200 lines of optimization without asking which "faster" matters
```

**Right — present options:**

```
"Make the search faster" could mean:

1. Faster response time (< 100ms) → database indexes, caching
2. Higher throughput → async/await, connection pooling
3. Faster perceived speed (UX) → partial results, progressive loading

Current search takes ~500ms. Which aspect matters most?
```

---

## 2. Simplicity First

### Over-Abstraction

**User request:** "Add a function to calculate discount"

**Wrong — strategy pattern for a single calculation:**

```python
from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float: ...

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        self.percentage = percentage
    def calculate(self, amount: float) -> float:
        return amount * (self.percentage / 100)

class FixedDiscount(DiscountStrategy):
    def __init__(self, fixed_amount: float):
        self.fixed_amount = fixed_amount
    def calculate(self, amount: float) -> float:
        return min(self.fixed_amount, amount)

# ... 40+ more lines of DiscountConfig, DiscountCalculator ...
```

**Right — solve the actual problem:**

```python
def calculate_discount(amount: float, percent: float) -> float:
    """Calculate discount amount. percent should be 0-100."""
    return amount * (percent / 100)
```

Add complexity only when you actually need multiple discount types.

### Speculative Features

**User request:** "Save user preferences to database"

**Wrong — cache, validation, merge, notifications nobody asked for:**

```python
class PreferenceManager:
    def __init__(self, db, cache=None, validator=None):
        self.db = db
        self.cache = cache or InMemoryCache()
        self.validator = validator or DefaultValidator()

    def save(self, user_id, prefs, merge=True, validate=True, notify=False):
        if validate:
            errors = self.validator.validate(prefs)
            # ... 40+ lines of speculative features
```

**Right — just what was asked:**

```python
def save_preferences(db, user_id: int, preferences: dict):
    db.execute(
        "UPDATE users SET preferences = ? WHERE id = ?",
        (json.dumps(preferences), user_id)
    )
```

---

## 3. Surgical Changes

### Drive-By Refactoring

**User request:** "Fix the bug where empty emails crash the validator"

**Wrong — "improve" unrelated code while fixing a bug:**

```diff
  def validate_user(user_data):
-     if not user_data.get('email'):
+     """Validate user data."""                          # added docstring
+     email = user_data.get('email', '').strip()
+     if not email:
          raise ValueError("Email required")
-     if '@' not in user_data['email']:
+     if '@' not in email or '.' not in email.split('@')[1]:  # changed validation
          raise ValueError("Invalid email")
-     if not user_data.get('username'):
+     username = user_data.get('username', '').strip()   # refactored username
+     if not username:
          raise ValueError("Username required")
+     if len(username) < 3:                              # added new check
+         raise ValueError("Username too short")
```

**Right — only fix the reported bug:**

```diff
  def validate_user(user_data):
-     if not user_data.get('email'):
+     email = user_data.get('email', '')
+     if not email or not email.strip():
          raise ValueError("Email required")
-     if '@' not in user_data['email']:
+     if '@' not in email:
          raise ValueError("Invalid email")
      if not user_data.get('username'):
          raise ValueError("Username required")
      return True
```

### Style Drift

**User request:** "Add logging to the upload function"

**Wrong — reformat quotes, add type hints, change boolean logic:**

```diff
- def upload_file(file_path, destination):
+ def upload_file(file_path: str, destination: str) -> bool:  # added types
+     """Upload file to destination with logging."""           # added docstring
      try:
-         with open(file_path, 'rb') as f:
+         with open(file_path, "rb") as f:                    # changed quotes
```

**Right — match existing style, only add logging:**

```diff
+ import logging
+ logger = logging.getLogger(__name__)
+
  def upload_file(file_path, destination):
+     logger.info(f'Starting upload: {file_path}')
      try:
          with open(file_path, 'rb') as f:              # kept single quotes
              data = f.read()
          response = requests.post(destination, files={'file': data})
          if response.status_code == 200:
+             logger.info(f'Upload successful: {file_path}')
              return True
          else:
+             logger.error(f'Upload failed: {file_path}, status={response.status_code}')
              return False
      except Exception as e:
-         print(f"Error: {e}")
+         logger.exception(f'Upload error: {file_path}')
          return False
```

---

## 4. Goal-Driven Execution

### Vague vs. Verifiable

**User request:** "Fix the authentication system"

**Wrong — vague plan without success criteria:**

```
I'll fix the authentication system by:
1. Reviewing the code
2. Identifying issues
3. Making improvements
4. Testing the changes
```

**Right — define verifiable goals first:**

```
What specific issue are we solving?

If "users stay logged in after password change":

1. Write test: Change password → verify old session invalidated
   Verify: Test fails (reproduces bug)
2. Implement: Invalidate sessions on password change
   Verify: Test passes
3. Edge cases: Multiple active sessions, concurrent changes
   Verify: Additional tests pass
4. Regression: Existing auth tests still pass
   Verify: Full test suite green
```

### Reproduce Before Fixing

**User request:** "The sorting breaks when there are duplicate scores"

**Wrong — fix without reproducing:**

```python
def sort_scores(scores):
    return sorted(scores, key=lambda x: (-x['score'], x['name']))
```

**Right — reproduce first, then fix:**

```python
# 1. Write a test that reproduces the issue
def test_sort_with_duplicate_scores():
    scores = [
        {'name': 'Alice', 'score': 100},
        {'name': 'Bob', 'score': 100},
        {'name': 'Charlie', 'score': 90},
    ]
    result = sort_scores(scores)
    assert result[0]['score'] == 100
    assert result[1]['score'] == 100
    assert result[2]['score'] == 90
# Verify: Run 10 times → fails with inconsistent ordering

# 2. Fix with stable sort
def sort_scores(scores):
    return sorted(scores, key=lambda x: (-x['score'], x['name']))
# Verify: Test passes consistently
```

---

## Anti-Patterns Summary

| Principle | Anti-Pattern | Fix |
|-----------|-------------|-----|
| Think Before Coding | Silently assumes format, fields, scope | List assumptions explicitly, ask |
| Simplicity First | Strategy pattern for single calculation | One function until complexity needed |
| Surgical Changes | Reformats quotes, adds type hints during bugfix | Only change lines that fix the issue |
| Goal-Driven | "I'll review and improve the code" | "Write test → make it pass → verify" |

## Key Insight

The "overcomplicated" examples follow valid design patterns — the problem is **timing**.
Adding complexity before it's needed makes code harder to understand, introduces bugs,
takes longer to implement, and is harder to test.

Simple code that solves today's problem can always be refactored later when
complexity is actually needed.

> **Good code solves today's problem simply, not tomorrow's problem prematurely.**
