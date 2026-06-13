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
```python
from django.db.models import Sum


<img width="1913" height="920" alt="Screenshot 2026-06-13 230931" src="https://github.com/user-attachments/assets/c82aacfd-2af3-486a-9e02-3019be186745" />

