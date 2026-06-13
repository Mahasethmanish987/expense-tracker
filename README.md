╔══════════════════════════════════════════════════════════════════════╗
║                        🐛 BUGS FOUND & FIXES                         ║
╚══════════════════════════════════════════════════════════════════════╝


╔══════════════════════════════════════════════════════════════════════╗
║  🔐 01. DATA ISOLATION VULNERABILITY (MULTI-USER SAFETY)             ║
║  Commit: 8bf511b0b87538967cdbf3d0a91a69f14e82a897                    ║
╠══════════════════════════════════════════════════════════════════════╣
║ ❌ Issue                                                             ║
║ Categories and expenses were accessible across different users.      ║
║                                                                      ║
║ 🔍 Root Cause                                                       ║
║ Missing user-level filtering in queryset and model relationships.    ║
║                                                                      ║
║ ✅ Fix                                                              ║
║ - Added user relation to Category and Expense models                 ║
║ - Scoped all queries using request.user                              ║
╚══════════════════════════════════════════════════════════════════════╝


╔══════════════════════════════════════════════════════════════════════╗
║  🧾 02. SERIALIZER FIELD MISMATCH                                    ║
║  Commit: 4c9757cc0d70c9f28fea2af65ef9677bd7b62c02                    ║
╠══════════════════════════════════════════════════════════════════════╣
║ ❌ Issue                                                             ║
║ API requests failed due to incorrect serializer field mapping.       ║
║                                                                      ║
║ 🔍 Root Cause                                                       ║
║ Field name mismatch between serializer and model.                   ║
║                                                                      ║
║ ✅ Fix                                                              ║
║ Corrected serializer fields to match model structure.                ║
╚══════════════════════════════════════════════════════════════════════╝


╔══════════════════════════════════════════════════════════════════════╗
║  ⚙️ 03. SERIALIZER PROCESSING ISSUE                                  ║
║  Commit: 6b1fe03df23f9507f553e0dee9cba4a002ba7c04                    ║
╠══════════════════════════════════════════════════════════════════════╣
║ ❌ Issue                                                             ║
║ Expense data was not being saved or validated properly.              ║
║                                                                      ║
║ 🔍 Root Cause                                                       ║
║ Incorrect serializer initialization in views.                        ║
║                                                                      ║
║ ✅ Fix                                                              ║
║ Fixed serializer instantiation and validation flow.                  ║
╚══════════════════════════════════════════════════════════════════════╝


╔══════════════════════════════════════════════════════════════════════╗
║  📊 04. MISSING AGGREGATION IMPORT                                   ║
║  Commit: 45778e367af61e370916ec57696837f17115602c                    ║
╠══════════════════════════════════════════════════════════════════════╣
║ ❌ Issue                                                             ║
║ Summary endpoint was crashing.                                       ║
║                                                                      ║
║ 🔍 Root Cause                                                       ║
║ Missing Django ORM Sum import.                                       ║
║                                                                      ║
║ ✅ Fix                                                              ║
║ from django.db.models import Sum                                     ║
╚══════════════════════════════════════════════════════════════════════╝


╔══════════════════════════════════════════════════════════════════════╗
║  📅 05. DATE FILTERING ISSUE                                         ║
║  Commit: 2edad36c54f39d9780b75e5a9e742b03ee1afcc2                    ║
╠══════════════════════════════════════════════════════════════════════╣
║ ❌ Issue                                                             ║
║ End date was excluded from results.                                 ║
║                                                                      ║
║ 🔍 Root Cause                                                       ║
║ Incorrect date range filtering logic.                               ║
║                                                                      ║
║ ✅ Fix                                                              ║
║ Updated filter to include both start and end dates.                 ║
╚══════════════════════════════════════════════════════════════════════╝


╔══════════════════════════════════════════════════════════════════════╗
║  🚫 06. NEGATIVE EXPENSE VALIDATION                                  ║
║  Commit: ba74670d20feb4dfe7820984296da796af839588                    ║
╠══════════════════════════════════════════════════════════════════════╣
║ ❌ Issue                                                             ║
║ API allowed negative expense values.                                ║
║                                                                      ║
║ 🔍 Root Cause                                                       ║
║ Missing validation on amount field.                                 ║
║                                                                      ║
║ ✅ Fix                                                              ║
║ Added validation to reject negative numbers.                         ║
╚══════════════════════════════════════════════════════════════════════╝
