# Copilot Instructions for Pet Adoption & Rescue API

## Architecture Overview

This is a **Django REST Framework (5.0) + SQLite backend** for a pet adoption and rescue platform. Core structure:

- **Project Root**: `root/` (settings, URL routing, ASGI/WSGI)
- **Apps**: 7 independent Django apps in app-per-feature pattern
- **API**: All endpoints under `/api/v1/` with automatic routing via ViewSets
- **Authentication**: JWT (simplejwt) + custom User model with email-based auth

## App Structure & Responsibilities

| App | Purpose | Key Pattern |
|-----|---------|-------------|
| `users` | Custom User model, auth (register/login/logout) | Custom UserManager, email as USERNAME_FIELD |
| `adopt` | Pet listings for adoption | ModelViewSet + image upload, "my-listings" custom action |
| `missing_pets` | Lost pet reports | Same pattern as adopt, includes reporter relationship |
| `rescue` | Shelters & veterinary contacts (read-only) | ReadOnlyModelViewSet, no user ownership |
| `donate` | Donation system with payment gateway prep | Supports anonymous donations, multiple payment methods |
| `contact` | User feedback/bug reports | Supports anonymous submissions, status workflow |
| `terms` | T&C versioning & acceptance tracking | Only one active version at a time (enforced in save()) |

## Critical Developer Workflows

### Running Django Commands
```bash
# Activate venv first
python manage.py runserver          # Dev server on 0.0.0.0:8000
python manage.py migrate           # Apply pending migrations
python manage.py makemigrations    # Create migration files
python manage.py createsuperuser   # Create admin user
python manage.py shell             # Interactive Python shell
```

### Making Database Changes
1. Edit model in `{app}/models.py`
2. Run `python manage.py makemigrations {app}` → creates migration file
3. Review generated migration file (in `{app}/migrations/`)
4. Run `python manage.py migrate` to apply
5. Update serializers & viewsets if needed

### Adding API Endpoints
- **Use ViewSets**: All endpoints use `viewsets.ModelViewSet` or `ReadOnlyModelViewSet`
- **Custom actions**: Decorate with `@action(detail=True/False, methods=['get'/'post'/etc])`
- **Example**: `@action(detail=False, methods=['get'], permission_classes=[...])` → GET `/api/v1/pets/my-listings/`
- **Register in `{app}/urls.py`** via `DefaultRouter().register()`

## Patterns & Conventions

### Permission & Authentication
- **Default**: `IsAuthenticatedOrReadOnly` (REST_FRAMEWORK config)
- **Custom permissions** in `core/permissions.py`:
  - `IsOwnerOrAdmin`: Owner-based + admin override (checks `owner`, `reporter`, `user`, `donor` fields)
  - `HasAcceptedTerms`: Enforces user.terms_accepted=True for write operations
  - `IsAdminUser`: Staff or role='ADMIN'
- **Public endpoints** explicitly use `permissions.AllowAny()`

### Serializer Hierarchy
- **List serializer**: Minimal fields, related names as read-only (e.g., `owner_name` from `owner.full_name`)
- **Detail serializer**: Full data + nested relationships
- **Create/Update serializer**: Write-enabled fields only, nested image handling
- **SerializerMethodField** for computed values (e.g., `primary_image` URL building)

### Image Handling Pattern (adopt, missing_pets)
- Max 5 images per listing, max 5MB each
- `is_primary=True` enforced unique per item (ensured in PetImage/MissingPetImage.save())
- Upload via ListField in create serializer, bulk via custom `upload_images` action
- Images deleted via custom `delete_image` action with validation (prevent last image deletion)

### Status & State Management
- Models use CharField with CHOICES (not separate model)
- Methods like `mark_as_adopted()`, `mark_as_found()` update status + timestamp in one transaction
- Filtering: list view defaults to AVAILABLE/MISSING; query param `status` overrides

### Anonymous User Data
- `donate`: Donor can be NULL (anonymous donations)
- `contact`: User can be NULL (anonymous feedback)
- Both provide `get_*_display()` methods respecting anonymity

## Configuration & Integrations

### JWT Settings (simplejwt)
- Access token: 30 min lifetime, blacklist rotation enabled
- Refresh token: 7 day lifetime
- Use `RefreshToken.for_user(user)` to generate tokens on login (see `users/views.py`)

### CORS Settings
- Only `localhost:3000` and `127.0.0.1:3000` allowed in dev
- Change in `root/settings.py` → `CORS_ALLOWED_ORIGINS`

### Payment Gateway Stubs
- `donate/payment_handlers/` has shell implementations (esewa, paypal, bank_transfer)
- Not integrated yet—marked with TODO comments
- Expected flow: `Donation.initiate()` → generate payment URL → verify webhook

### Terms & Conditions
- `User.terms_accepted` boolean tracks acceptance
- `TermsAcceptance` model logs version, IP, user-agent
- Only one `TermsAndConditions.is_active=True` at a time (enforced in save())

## Common Code Locations

| Task | File |
|------|------|
| Add auth endpoint | `users/views.py` UserViewSet |
| Add permission | `core/permissions.py` |
| Modify pet listing logic | `adopt/models.py` Pet + `adopt/views.py` PetViewSet |
| Add donation payment method | `donate/payment_handlers/` |
| Customize response format | Edit serializers, ViewSet.perform_create() |
| Add filtering/search | `{app}/views.py` filter_backends, filterset_fields, search_fields |

## Testing & Validation

- Test files exist but are mostly empty (`{app}/tests.py`)
- Serializer validation in Meta.validators or validate() method (see PetCreateUpdateSerializer.validate_age)
- Admin actions for bulk operations (see `adopt/admin.py` mark_as_adopted)

## Quick Gotchas

1. **Custom User Model**: Username is `email`, not username field. Auth via `authenticate(email=..., password=...)`
2. **Image URLs**: Use `request.build_absolute_uri()` in serializers to return full URLs (see PetListSerializer.get_primary_image)
3. **Timestamps auto-managed**: `created_at` (auto_now_add), `updated_at` (auto_now)—don't manually set
4. **Related names**: Use underscore (e.g., `related_name='pet_listings'`) for reverse queries
5. **Terms acceptance**: Enforced by `HasAcceptedTerms` permission—affects adopt & missing_pets creation, not rescue/donations
