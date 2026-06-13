Bugs Found and Fixed
Bug 1: Model ownership missing (data isolation issue)
Description: Categories and expenses were not scoped to the authenticated user.
Root Cause: Missing user-level filtering in models/views.
Fix: Added user ownership and enforced request.user scoping.
Commit Hash: 8bf511b0b87538967cdbf3d0a91a69f14e82a897
Bug 2: Serializer typo issue
Description: Category serializer had incorrect field naming causing API issues.
Root Cause: Typo in serializer field definition.
Fix: Corrected serializer field mapping.
Commit Hash: 4c9757cc0d70c9f28fea2af65ef9677bd7b62c02
Bug 3: Serializer variable misuse in view
Description: Expense API was not properly validating/saving data.
Root Cause: Incorrect serializer instance usage in view logic.
Fix: Fixed serializer initialization and validation flow.
Commit Hash: 6b1fe03df23f9507f553e0dee9cba4a002ba7c04
Bug 4: Missing aggregation import in summary endpoint
Description: Summary endpoint crashed due to missing Sum import.
Root Cause: Django ORM aggregation function not imported.
Fix: Added missing import from django.db.models import Sum.
Commit Hash: 45778e367af61e370916ec57696837f17115602c
Bug 5: Date filtering not inclusive
Description: End date was excluded from results in filtering.
Root Cause: Incorrect date range logic in queryset filtering.
Fix: Updated filter to include both start and end dates.
Commit Hash: 2edad36c54f39d9780b75e5a9e742b03ee1afcc2
Bug 6: Negative expense validation missing
Description: API allowed creation of expenses with negative amounts.
Root Cause: No validation on expense amount field.
Fix: Added validation to prevent negative values in serializer/model.
Commit Hash: ba74670d20feb4dfe7820984296da796af839588
