---
name: refactoring
description: Use when improving code structure without changing behavior. Trigger on phrases like "refactor", "clean up", "code smell", "technical debt", "simplify", "extract method", "rename", "reorganize", "DRY", "SOLID", or when code is duplicated, complex, or poorly structured.
---

# Refactoring Skill

Improve code quality through systematic structural changes.

## Code Smells Checklist

| Smell | Detection | Fix |
|-------|-----------|-----|
| Long method | > 50 lines | Extract methods |
| Large class | > 300 lines | Split into smaller classes |
| Duplicated code | Same logic in 2+ places | Extract to shared function |
| Long parameter list | > 4 parameters | Use dataclass/dict |
| Deep nesting | > 3 levels | Extract early returns |
| Magic numbers | Raw numbers in code | Extract to named constants |
| God object | One class does everything | Split responsibilities |
| Feature envy | Method uses another class's data | Move method |
| Primitive obsession | Using primitives for complex concepts | Create value objects |

## Refactoring Techniques

### Extract Method
```python
# BEFORE
def process_order(order):
    total = 0
    for item in order.items:
        if item.quantity > 0:
            price = item.price * item.quantity
            if item.discount:
                price *= (1 - item.discount)
            total += price
    tax = total * 0.08
    return total + tax

# AFTER
def calculate_item_price(item):
    price = item.price * item.quantity
    if item.discount:
        price *= (1 - item.discount)
    return price

def calculate_tax(amount, rate=0.08):
    return amount * rate

def process_order(order):
    subtotal = sum(calculate_item_price(item) for item in order.items)
    tax = calculate_tax(subtotal)
    return subtotal + tax
```

### Replace Magic Numbers
```python
# BEFORE
if len(password) < 8:
    raise ValueError("Too short")

# AFTER
MIN_PASSWORD_LENGTH = 8

if len(password) < MIN_PASSWORD_LENGTH:
    raise ValueError(f"Password must be at least {MIN_PASSWORD_LENGTH} characters")
```

### Decompose Conditional
```python
# BEFORE
if date.before(summer_start) or date.after(summer_end):
    charge = quantity * winter_rate + winter_service_charge
else:
    charge = quantity * summer_rate

# AFTER
def is_winter(date):
    return date.before(summer_start) or date.after(summer_end)

def calculate_charge(quantity, date):
    if is_winter(date):
        return quantity * winter_rate + winter_service_charge
    return quantity * summer_rate
```

### Introduce Parameter Object
```python
# BEFORE
def create_user(name, email, phone, address, city, state, zip_code):
    ...

# AFTER
@dataclass
class UserAddress:
    street: str
    city: str
    state: str
    zip_code: str

def create_user(name: str, email: str, address: UserAddress):
    ...
```

## Refactoring Workflow

1. **Identify** the smell (use checklist above)
2. **Ensure tests pass** before refactoring
3. **Make one change at a time**
4. **Run tests after each change**
5. **Commit** after each successful refactor
6. **Document** why the change was made

## When NOT to Refactor

- Code is about to be deleted
- No tests exist and you can't add them
- It's a temporary workaround (document it instead)
- The gain doesn't justify the risk

## Rules

- NEVER refactor and add features in the same commit
- ALWAYS run tests before and after refactoring
- ONE refactoring technique per commit
- Keep refactoring small and incremental
- Don't refactor dead code — delete it
