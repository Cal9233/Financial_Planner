# Frontend to Backend Route Mapping

## Database Routes
| Frontend Call | Backend Route | Status |
|--------------|---------------|---------|
| GET /api/database/status | GET /api/database/status | ✅ Implemented |
| POST /api/database/connect | POST /api/database/connect | ✅ Implemented |
| POST /api/database/disconnect | POST /api/database/disconnect | ✅ Implemented |
| POST /api/database/test | POST /api/database/test | ✅ Implemented |

## Auth Routes
| Frontend Call | Backend Route | Status |
|--------------|---------------|---------|
| POST /api/auth/login | POST /api/auth/login | ✅ Implemented |
| POST /api/auth/register | POST /api/auth/register | ✅ Implemented |
| POST /api/auth/logout | POST /api/auth/logout | ✅ Implemented |
| POST /api/auth/refresh | POST /api/auth/refresh | ✅ Implemented |
| GET /api/auth/me | GET /api/auth/me | ✅ Implemented |
| GET /api/users/profile | GET /api/users/profile | ✅ Implemented |

## Dashboard Routes
| Frontend Call | Backend Route | Status |
|--------------|---------------|---------|
| GET /api/transactions/summary | GET /api/transactions/summary | ✅ Implemented |
| GET /api/accounts | GET /api/accounts | ✅ Implemented |
| GET /api/transactions?per_page=5 | GET /api/transactions | ✅ Implemented |
| GET /api/budgets/performance | GET /api/budgets/performance | ✅ Implemented |
| GET /api/goals?include_completed=false | GET /api/goals | ✅ Implemented |

## Transaction Routes
| Frontend Call | Backend Route | Status |
|--------------|---------------|---------|
| GET /api/transactions | GET /api/transactions | ✅ Implemented |
| POST /api/transactions | POST /api/transactions | ✅ Implemented |
| PUT /api/transactions/:id | PUT /api/transactions/:id | ✅ Implemented |
| DELETE /api/transactions/:id | DELETE /api/transactions/:id | ✅ Implemented |
| GET /api/categories | GET /api/categories | ✅ Implemented |

## Reports Routes
| Frontend Call | Backend Route | Status |
|--------------|---------------|---------|
| GET /api/reports/monthly/:year/:month | GET /api/reports/monthly/:year/:month | ✅ Implemented |

## Missing/Placeholder Routes
| Frontend Call | Backend Route | Status |
|--------------|---------------|---------|
| Accounts CRUD | /api/accounts/* | ❌ Need full CRUD |
| Budgets CRUD | /api/budgets/* | ❌ Need full CRUD |
| Goals CRUD | /api/goals/* | ❌ Need full CRUD |
| Reports (other than monthly) | /api/reports/* | ❌ Need implementation |