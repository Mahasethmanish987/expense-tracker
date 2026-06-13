# 🐛 BUGS FOUND & FIXES

---

## 🔐 01. Data Isolation Vulnerability (Multi-User Safety)
**Commit:** `8bf511b0b87538967cdbf3d0a91a69f14e82a897`

### ❌ Issue
Categories and expenses were visible across different users.

### 🔍 Root Cause
Missing user-level filtering in queryset and model relationships.

### ✅ Fix
- Added `user` field in Category and Expense models  
- Scoped all queries using `request.user`

---

## 🧾 02. Serializer Field Mismatch
**Commit:** `4c9757cc0d70c9f28fea2af65ef9677bd7b62c02`

### ❌ Issue
API requests failed due to incorrect serializer field mapping.

### 🔍 Root Cause
Mismatch between serializer fields and model fields.

### ✅ Fix
Corrected serializer fields to match model structure.

---

## ⚙️ 03. Serializer Processing Issue
**Commit:** `6b1fe03df23f9507f553e0dee9cba4a002ba7c04`

### ❌ Issue
Expense data was not being saved or validated properly.

### 🔍 Root Cause
Incorrect serializer initialization in views.

### ✅ Fix
Fixed serializer instantiation and validation flow.

---

## 📊 04. Missing Aggregation Import
**Commit:** `45778e367af61e370916ec57696837f17115602c`

### ❌ Issue
Summary endpoint crashed due to missing import.

### 🔍 Root Cause
Missing `Sum` import from Django ORM.

### ✅ Fix
## 📸 Bot Alert Proof

![Bot Alert](https://github.com/user-attachments/assets/c82aacfd-2af3-486a-9e02-3019be186745)


## 🧠 Design Decisions

### 🔐 Authentication & Security
- Used DRF’s `IsAuthenticated` permission to secure all endpoints.
- Ensured all API access requires a valid authenticated user.
- Prevented cross-user data leakage by enforcing `request.user` filtering at the queryset level.
- Adopted object-level ownership (each `Category` and `Expense` is tied to a specific user).

---

### 🗂️ Data Modeling
- Designed a simple relational structure:
  - User → Category → Expense
- Each expense belongs to a category and user, ensuring strict ownership separation.
- Added `currency` field in `Expense` to support multi-currency tracking without altering original amount.

---

### 💱 Currency Conversion Strategy
- Stored original transaction amount with its currency (no loss of original data).
- Performed conversion dynamically in the summary endpoint using live exchange rates.
- Kept conversion logic separate from models to maintain clean architecture.

---

### 📊 Aggregation & Reporting
- Used Django ORM `prefetch_related` to optimize database queries.
- Calculated category-wise totals in base currency (USD) at runtime.
- Designed summary endpoint to be frontend-ready without extra API calls.

---

### 🤖 Budget Alert System
- Implemented threshold-based alerts using category-wise monthly limits.
- Triggered alert immediately after expense creation when limit exceeded.
- Used external bot API (Telegram/Slack) for notifications.

---

### ⚙️ API Design Philosophy
- Followed RESTful conventions (GET, POST, PUT, DELETE).
- Maintained consistent response structures across endpoints.
- Kept API responses minimal but frontend-ready.
- Prioritized readability and maintainability over complexity.

---

### 🚧 Trade-offs & Limitations
- Currency conversion depends on external API availability.
- No caching for exchange rates implemented.
- Bot alerts are synchronous (no retry/background queue).
- No pagination implemented for large datasets.
