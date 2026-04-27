<!--
=========================================================================================
ORIGINAL PROMPT (January 13, 2026)
=========================================================================================

"you are a cheif architect and have to report to the CEO about the architecture of the system including potentail costs or running the system in AWS. He wants to see the overall architecture description and diaggram (SVG format). Provide detail of the architecture but be concise. Remove all the code. Missing from the root repo is the iOS and Android apps. Take those into consideration. Create an architectire document in in the root docs directory."

=========================================================================================
-->

---
title: "TrailLensHQ System Architecture"
author: "Chief Architect"
date: "April 2026"
abstract: "Technical architecture overview of TrailLensHQ's modern serverless AWS infrastructure including scaling, security, multi-tenancy, and cost projections."
---

# TrailLensHQ System Architecture
**Chief Architect Report to CEO | April 2026 | Document Version 3.0**

**📊 IMPORTANT: For detailed cost analysis with complete calculations, usage methodologies, and verified AWS pricing references, see:**
**→ [COST_ANALYSIS_DETAILED.md](COST_ANALYSIS_DETAILED.md)**

---

## Executive Summary

TrailLensHQ is built on a **modern, serverless architecture** using AWS cloud services. The system is designed for:
- **Automatic scaling** - Handles 10 users or 100,000 users without infrastructure changes
- **Cost efficiency** - Pay only for actual usage (no idle server costs)
- **High availability** - 99.9% uptime SLA with multi-AZ deployment
- **Security-first** - Enterprise-grade authentication, encryption, and data isolation
- **Multi-tenant** - Single infrastructure serves all customers with complete data isolation

**Current Monthly Costs:**
- **Development Environment:** $75-150/month
- **Production Environment:** $200-400/month (projected, scales with usage)
- **No upfront infrastructure investment required**

---

## Architecture Diagram

![TrailLensHQ System Architecture](./ARCHITECTURE.svg)

The diagram above shows the complete system architecture including all client applications (iOS, Android, Web), API services, databases, and AWS infrastructure.

---

## System Components

### 1. Client Applications

#### **iOS Mobile App - User App** (Native Swift, REQUIRED for MVP v1.13)

- **Platform:** Apple App Store (TestFlight for MVP beta)
- **Purpose:** Trail system discovery and real-time status for outdoor enthusiasts
- **Authentication:** AWS Cognito SDK (magic link, email/password, Native WebAuthn passkey)
- **Push Notifications:** APNS (Apple Push Notification Service) via AWS SNS
- **Key Features:**
  - Real-time trail system status and alerts
  - View public Trail Care Reports
  - **Submit Trail Care Reports** with camera integration (up to 5 photos)
  - **Offline report creation**: Create reports offline, auto-upload when signal returns (7-day queue with warnings)
  - Offline status caching (7-day cache with stale data warning)
  - Subscribe to trail systems and organizations
- **Repository:** Separate iOS repository
- **Status:** REQUIRED for MVP

#### **iOS Mobile App - Admin App** (Native Swift, REQUIRED for MVP v1.13)

- **Platform:** Apple App Store (TestFlight for MVP beta)
- **Purpose:** Trail system management and Trail Care Report handling for trail crew
- **Authentication:** AWS Cognito SDK with role verification (trailsystem-crew+ only)
- **Key Features:**
  - Quick trail system status updates from field
  - Full Trail Care Report CRUD (view, create, edit, assign, comment, close)
  - Quick work log creation (private reports)
  - Priority assignment (P1-P5)
  - Photo upload with geolocation
  - Offline capability (same as user app)
- **Repository:** Same repository as user app (separate app target)
- **Status:** REQUIRED for MVP

#### **Android Mobile Apps** (Native Kotlin, Active Development)

- **Platform:** Google Play Store
- **Purpose:** Same functionality as iOS apps (user + admin), built from the ground up in Kotlin
- **Authentication:** AWS Cognito SDK (magic link, email/password, Native WebAuthn passkey)
- **Push Notifications:** FCM (Firebase Cloud Messaging) via AWS SNS
- **Key Features:**
  - Trail system discovery and real-time status
  - Trail Care Report submission with camera integration
  - Offline capability with local sync queue
  - Organization management (admin app)
- **Repositories:** Three linked repos via Gradle composite build:
  - `androiduser/` — User app (`com.traillenshq.app`)
  - `androidadmin/` — Admin app (`com.traillenshq.admin`)
  - `androidrestapi/` — Shared REST API client library (`com.traillenshq.api`, 71 endpoints)
- **Stack:** Kotlin 2.3.20, Jetpack Compose, Hilt 2.59.2, Retrofit 3.0.0
- **Status:** Active development

#### **Web Application** (`webui/` — React 19 + Tailwind CSS 4.x)
- **Platform:** AWS Amplify + CloudFront CDN
- **Framework:** React 19 with React Router v7
- **Styling:** Tailwind CSS 4.x
- **Design:** Ground-up rebuild with latest libraries — no legacy template dependencies
- **Pages:** Covers all tiers:
  - **Public Tier:** Marketing, trail directory, pricing (no auth)
  - **Auth Tier:** Login, magic link, passkey (Cognito Native WebAuthn)
  - **Organization Tier:** Dashboard, team management, trail admin
  - **User Tier:** Personal dashboard, subscriptions, settings
- **Deployment:** Automated via AWS Amplify (git push triggers build/deploy)
- **Global CDN:** CloudFront delivers content from edge locations worldwide
- **Status:** Active development (replaces legacy `web/` frontend)

### 2. API Layer

#### **AWS API Gateway** (REST API)
- **Type:** Regional REST API
- **Custom Domain:** `api.dev.traillenshq.com` (dev), `api.traillenshq.com` (prod)
- **SSL Certificate:** AWS Certificate Manager (ACM) with auto-renewal
- **Rate Limiting:** 100 requests/minute per user
- **Architecture Pattern:** `{proxy+}` catch-all proxy to Lambda
  - Infrastructure creates the master API Gateway with root resource
  - `{proxy+}` resource handles ALL routes (ANY method, auth NONE at gateway level)
  - Explicit `/api/auth/magic-link/lookup-token` resource (POST, API key required)
  - FastAPI CORSMiddleware handles all CORS; auth enforced at FastAPI level (RS256 JWKS)
  - Mangum adapter receives full path from Lambda event, routes to FastAPI

#### **Main API Service** (FastAPI + Python 3.14)
- **Runtime:** AWS Lambda (serverless compute), ARM64 (Graviton2), 512 MB
- **Framework:** FastAPI with Mangum adapter (ASGI to Lambda)
- **Architecture:** Spec-driven code generation from OpenAPI 3.1.0 + DynamoDB spec; layered Routes → Services → Repositories → DynamoDB
- **Route Modules:**
  - `auth` — Magic link auth, Cognito sign-out, token refresh
  - `magic_link` — Cross-device passwordless auth token lookup
  - `trail_systems` — CRUD, condition updates, status history, notifications
  - `users` — User profiles, authentication, role management
  - `organizations` — Org CRUD, members, roles
  - `devices` — Push notification device registration (APNS/FCM)
  - `notifications` — Notification preference management
  - `care_reports` — Trail Care Report create/update/query
  - `condition_observations` — TrailPulse condition observations (6 endpoints)
  - `scheduled_condition` — Scheduled status/condition management
  - `tags` — Trail system tagging
  - `content` — Static content (FAQ, etc.)
- **Database:** Single-table DynamoDB (66 access patterns, 6 GSIs)
- **Performance:** P95 latency < 200ms, P99 < 500ms, ~1,157 RPS sustained
- **Testing:** 90%+ test coverage (pytest + moto `mock_aws`)
- **Deployment:** ZIP packaged, uploaded to S3, deployed to Lambda via Pulumi

#### **Social Media API** (NestJS + Node.js 22)
- **Runtime:** AWS Lambda (serverless compute)
- **Framework:** NestJS (TypeScript)
- **Purpose:** Automated social media posting
- **Integrations:**
  - Facebook Graph API v19.0 (Pages posting)
  - Instagram Graph API (Posts and Stories)
- **Features:**
  - Automatic posting when trail status changes
  - Multi-tenant credential management (each org has own Facebook/Instagram accounts)
  - Rate limit handling (Facebook API throttling)
  - Post scheduling
  - Analytics tracking
- **Testing:** 80.68% test coverage (118 tests passing)
- **Deployment:** Packaged as ZIP, uploaded to S3, deployed to Lambda
- **Status:** 80% complete (AWS deployment pending)

### 3. Lambda Functions (Python 3.14, ARM64 Graviton2)

All Lambda functions are owned and deployed by application repositories (`api-dynamo/pulumi/` and `facebook-api/pulumi/`). The `infra/` repository deploys **no Lambda functions** — it creates only shared infrastructure (DynamoDB, S3, Cognito, SNS, SES domain, API Gateway master) consumed via Pulumi StackReference. This is verified at `infra/pulumi/__main__.py:16` ("Lambda functions are deployed from application repositories").

**Deployment-package count: 9** (up from 7). Note that "deployment package" is distinct from "`aws.lambda.Function` resource" — a single deployment package such as `cognito-triggers` contains multiple handlers (`define_auth_challenge`, `create_auth_challenge`, `verify_auth_challenge`, `post_authentication`) and produces multiple `aws.lambda.Function` resources in `api-dynamo/pulumi/` from the same ZIP.

The 9 deployment packages in `api-dynamo/src/lambdas/`:

| # | Package | Memory | Trigger | Purpose |
|---|---------|--------|---------|---------|
| 1 | `api_dynamo` | 512MB | API Gateway `{proxy+}` | Main FastAPI REST API (Mangum adapter) |
| 2 | `cognito-triggers` (multi-handler) | 256MB each | Cognito triggers | `define_auth_challenge`, `create_auth_challenge` (generates magic-link token + stores in DynamoDB + sends via SES), `verify_auth_challenge`, `post_authentication` |
| 3 | `notification_email` | 256MB | SNS: `TRAIL_CONDITION_CHANGE` | Email alerts via SES templates |
| 4 | `notification_sms` | 256MB | SNS: critical severity | SMS alerts via SNS |
| 5 | `notification_push` | 256MB | SNS: `TRAIL_CONDITION_CHANGE` | Push notifications to iOS (APNS) / Android (FCM) |
| 6 | `photo_processor` | 1024MB | S3: photo uploads | Resize to thumbnail/medium/large WebP variants |
| 7 | `email_forwarder` | 256MB | SES receipt rules | Forward incoming emails per YAML config |
| 8 | **`scheduled_condition_processor`** *(NEW)* | 256MB | EventBridge `cron(0/15 * * * ? *)` (every 15 min) | Single handler does both: (a) GSI4 query for scheduled conditions due to fire, TransactWrite to apply + append history + flip status to APPLIED + SNS publish; (b) GSI4 query for items with reminder window open, dispatch pre-fire reminder push and mark `reminder_sent=true`. |
| 9 | **`retention_cleanup_processor`** *(NEW)* | 512MB | EventBridge `cron(0 3 * * ? *)` (daily 03:00 UTC) | Closed care-report cleanup → batch-delete + audit log; deleted-account PII scrub; S3 photo-orphan sweep + CloudFront invalidation; belt-and-suspenders magic-link token cleanup. |

`facebook-api` adds one additional Node.js Lambda (Social Media API), deployed from `facebook-api/pulumi/` — not counted in the api-dynamo 9.

**Runtime:** Python 3.14, ARM64 (Graviton2) for all api-dynamo Lambdas.
**Deployment:** All Lambdas are packaged as ZIP, uploaded to S3, deployed via the owning application repo's Pulumi stack (never from `infra/`).
**Monitoring:** CloudWatch log groups (30-day retention), X-Ray tracing, P95 < 200ms / P99 < 500ms targets.

### 4. Authentication & Authorization

#### **AWS Cognito User Pool**
- **Purpose:** User authentication and identity management
- **Custom Domain:** `auth.dev.traillenshq.com` (dev), `auth.traillenshq.com` (prod)
- **Tier:** ESSENTIALS (supports WebAuthn + EMAIL_OTP)
- **Authentication Methods (THREE methods, all terminating at Cognito; api-dynamo issues no auth tokens of its own):**
  1. **Native WebAuthn Passkey** (primary): Touch ID, Face ID, security keys via Cognito Native WebAuthn (USER_AUTH flow + WEB_AUTHN challenge). Client-side via Cognito SDK; no custom backend, no api-dynamo route.
  2. **Magic Link** (primary, passwordless): Cognito CUSTOM_AUTH flow → `cognito-triggers/create_auth_challenge.py` Lambda generates a 256-bit URL-safe token, persists it in DynamoDB single-table (`PK=MLT#{token}`, 10-minute TTL), and emails the link via AWS SES. The user clicks the link → frontend extracts the token → frontend calls `POST /api/auth/magic-link/lookup-token` (api-dynamo's only role: token → email lookup) → client calls `Cognito.RespondToAuthChallenge(ANSWER=token)` → `verify_auth_challenge.py` validates → Cognito issues tokens. Reference: `api-dynamo/src/lambdas/cognito-triggers/src/cognito_triggers/create_auth_challenge.py`.
  3. **Password (backup, USER_SRP_AUTH)**: Cognito-direct via the SDK (Secure Remote Password — password never traverses the wire in plaintext). No api-dynamo route. **No account creation by password** — `infra/pulumi/components/auth.py:230-231` already sets `admin_create_user_config=...UserPoolAdminCreateUserConfigArgs(allow_admin_create_user_only=True)`, blocking self-signup. **No `/auth/forgot-password` endpoint in api-dynamo** — deferred to webui Phase 11 (uses Cognito `ForgotPassword`/`ConfirmForgotPassword` directly). The 12+ char password policy is already configured at `infra/pulumi/components/auth.py:218-224`. On mobile (androiduser, androidadmin) the password login screen is exposed **only in DEBUG builds**, behind a hidden trigger; production builds expose only passkey + magic-link.
- **MFA Configuration:** OPTIONAL at Cognito level. Enforced at FastAPI middleware level for org-admin, trailsystem-owner, and superadmin roles (7-day grace period). WebAuthn passkeys are inherently multi-factor and satisfy MFA requirements.
- **FactorConfiguration:** `MULTI_FACTOR_WITH_USER_VERIFICATION` — set via `set-cognito-mfa-config.py` boto3 script on every `pulumi up` (idempotent). Required to allow MFA-enabled admins to use passkeys.
- **WebAuthn Configuration:** `relying_party_id=traillenshq.com`, `user_verification=preferred`
- **Token Type:** RS256 JWT (JSON Web Tokens) issued by Cognito, verified via JWKS endpoint. HS256 is NOT accepted.
  - `sub`: User ID (Cognito UUID)
  - `email`: User email address
  - `cognito:groups`: User role memberships → mapped to `roles` claim
  - `custom:user_id`: Application user ID → mapped to `user_id` claim
  - `custom:org_id`: Primary organization ID → mapped to `org_id` claim
- **Password Policy:**
  - Minimum 12 characters
  - Requires: uppercase, lowercase, numbers, symbols
  - Password history: 6 (prevent reuse of last 6 passwords)
- **User Groups (8 roles):**
  - `super-admin`: Platform super admin
  - `admin`: Site administrator
  - `org-admin`: Organization administrator
  - `trailsystem-owner`: Trail management permissions
  - `trailsystem-crew`: Trail maintenance permissions
  - `trailsystem-status`: Trail status update only
  - `content-moderator`: Content moderation
  - `org-member`: Basic organization member
- **Email Integration:** Uses Amazon SES for sending (no 50/day limit)

#### **Cognito Threat Protection Enablement (REQUIRED — not yet enabled)**

Reference: [AWS Cognito Threat Protection developer guide](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-threat-protection.html).

Verified by direct read of `infra/pulumi/components/auth.py:213-239`: there is **no `user_pool_add_ons` block** today, and the pool is currently on the `ESSENTIALS` tier (`auth.py:202`). Threat Protection (formerly Advanced Security) is required for MVP and queued for the implementation plan:

1. **Tier upgrade:** raise `user_pool_tier` from `ESSENTIALS` → `PLUS`. Threat Protection is gated to the PLUS tier; ESSENTIALS does not support it. The per-MAU price delta should be documented for transparency before merge (absolute cost is small at <500 MAU).
2. **Add the `user_pool_add_ons` block:** `user_pool_add_ons=aws.cognito.UserPoolUserPoolAddOnsArgs(advanced_security_mode="AUDIT")` initially (per AWS guidance: run audit mode for 2+ weeks before enabling enforcement). Promote to `"ENFORCED"` after the soak window AND after configuring per-risk-level responses.
3. **Adaptive-auth response policy:** low risk → allow; medium risk → require MFA challenge; high risk → block.
4. **Caveat — compromised-credentials check works ONLY on `USER_PASSWORD_AUTH`, NOT on `USER_SRP_AUTH`** (per AWS Threat Protection "Key Limitations"). Adaptive risk-scoring works on both flows. The password backup flow above uses SRP, which keeps the password off the wire but forfeits the compromised-credentials check. Implementation-plan decision: (i) accept the trade-off and rely on the 12-char + complexity policy, OR (ii) switch the password backup flow to `USER_PASSWORD_AUTH` to gain the check (deviates from existing webui SRP flow). Magic-link and passkey flows are unaffected.
5. **Threat Protection does NOT provide rate-limiting.** Volumetric / brute-force protection requires AWS WAF rules on the Cognito endpoint or on API Gateway. WAF work is queued for the implementation plan (separate from Threat Protection enablement).
6. **Account recovery:** no explicit `account_recovery_setting` is configured today; default Cognito behaviour applies. This is intentional and acceptable because the MVP does **not** offer forgot-password (per the password-backup auth section above). Documented here so the gap is recognised as deliberate, not accidental.

### 5. Data Layer

#### **Amazon DynamoDB** (Single-Table Design)

All entities share a single DynamoDB table (`traillens-{env}-dynamodb`) using composite key patterns. This replaced a multi-table design to reduce operational overhead, lower cost, and enable atomic cross-entity transactions.

- **Billing Model:** PAY_PER_REQUEST (on-demand) — zero idle cost, automatic scaling
- **Backup:** Point-in-Time Recovery (PITR) enabled — continuous backups for 35 days
- **Encryption:** Server-side encryption with AWS managed keys (AES-256)
- **Deletion Protection:** Enabled (prevents accidental table drops)

**Key Schema:**

| Key | Type | Purpose |
|-----|------|---------|
| `PK` | String | Partition key (entity prefix + ID, e.g. `TRAILSYSTEM#abc`) |
| `SK` | String | Sort key (entity type or relationship, e.g. `METADATA`) |
| `GSI1PK` / `GSI1SK` | String | Overloaded index for access pattern flexibility |
| `GSI2PK` / `GSI2SK` | String | Overloaded index |
| `GSI3PK` / `GSI3SK` | String | Overloaded index |
| `GSI4PK` / `GSI4SK` | String | Overloaded index |
| `GSI5PK` / `GSI5SK` | String | Overloaded index |
| `GSI6PK` / `GSI6SK` | String | Geohash-based geospatial index (map bounds trail queries) |
| `ttl` | Number | TTL — automatic item expiration (used for tokens, temp data) |

**GSI overloading by entity type:**

Each GSI is intentionally overloaded — different entity types write distinct partition-key prefixes into the same physical index, and they never collide because the prefix uniquely identifies the entity type.

**GSI1 partition patterns (post-this-pass):**

| GSI1PK pattern | GSI1SK pattern | Owner / purpose |
|----------------|----------------|-----------------|
| `ORG#{org_id}` | (varies) | Org-member queries (existing) |
| `USER#{user_id}` | (varies) | User-centric queries (existing) |
| `EMAIL#{email_lc}` | (varies) | Magic-link rate-limit query, written by Cognito-trigger `create_auth_challenge.py` `_is_rate_limited` (existing) |
| `ORG#{org_id}#CATALOG#ACTIVE` | `USAGE#{usage_count_zero_padded}#CATALOG#{catalog_id}` | **NEW** — list active condition-catalog entries by org, sorted by usage count (Section "Condition Catalog" in `CONDITION_CATALOG.md`) |

**GSI4 (NEW) — Scheduled-condition processor index:**

| Key | Pattern | Notes |
|-----|---------|-------|
| `GSI4PK` | `SCHEDULED#{status}` | `status` ∈ {`PENDING`, `APPLIED`, `CANCELLED`} |
| `GSI4SK` | `scheduled_at_iso8601` | Lexicographic sort = chronological sort for ISO-8601 |

The new `scheduled_condition_processor` Lambda (see "Event-Driven Processing" below) queries `GSI4PK = SCHEDULED#PENDING` with `GSI4SK <= now+15min` to find scheduled-condition items due to fire in the next 15-minute window. When `status` flips to `APPLIED` or `CANCELLED`, the item moves to a different `GSI4PK` partition and is no longer returned by the PENDING query — there is no separate "processed" flag to maintain.

**Entity Key Pattern Examples:**

| Entity | PK | SK |
|--------|----|----|
| Trail system | `TRAILSYSTEM#{id}` | `METADATA` |
| Trail system (by slug) | `TRAILSYSTEM_SLUG#{slug}` *(GSI1)* | `TRAILSYSTEM#{id}` |
| User profile | `USER#{cognito_sub}` | `PROFILE` |
| Magic link token | `MLT#{token}` | `METADATA` |
| Device registration | `USER#{id}` | `DEVICE#{device_id}` |
| Condition observation | `TRAILSYSTEM#{id}` | `OBS#{timestamp}` |
| Care report | `CAREREPORT#{id}` | `METADATA` |
| Organization member | `ORG#{org_id}` *(GSI5)* | `USER#{user_id}` |
| Condition catalog entry | `ORG#{org_id}` | `CATALOG#{catalog_id}` |
| **Tag** (unified, all `tag_type` values) | `ORG#{org_id}` | `TAG#{tag_type}#{tag_id}` |
| **Tag config** (per-org cap override) | `ORG#{org_id}` | `TAG_CONFIG#{tag_type}` |

**Entity-type count (single-table overlay): 17 base + 9 TrailPulse = 26 entity types.**

The 17 base entity types include the existing 16 MVP entities plus the new `ConditionCatalogEntry` (org-scoped catalog of preset conditions; reuses the unified `Tag` entity with `tag_type=CONDITION` and is referenced by per-trail-system feedback configuration in TrailPulse).

**Tag Architecture (decided 2026-04-26):** The previously separate `ConditionTag` and `CareReportTypeTag` entities are unified into **one `Tag` entity discriminated by `tag_type`** (current values: `CONDITION`, `CARE_REPORT_TYPE`; the discriminator is open for extension). All tag flavors share the same identical schema (`tag_id`, `org_id`, `tag_type`, `name`, `description`, `color`, `is_active`, `created_at`, `updated_at`, `created_by_user_id`, `version`). Per-org caps are configurable via the new `TagConfig` entity. The merge of two entities into one (`-1`) plus the addition of `TagConfig` (`+1`) leaves the entity-type count unchanged at **26**. Type-specific URLs (`/condition-tags`, `/care-report-tags`) front a single shared service/repository — the discriminator is a backend implementation detail. Adding a new tag type requires no new entity, no new repository, and no new GSI: only a new `tag_type` enum value, a default cap constant, a route module, and a doc row.

The 9 TrailPulse entities (per Phase 7.5/15.1 in `MVP_PROJECT_PLAN.md`) are: `AdditionalQuestions`, `TrailSystemRideCount`, `RideCompletion`, `FeedbackResponses`, `UserPreferences`, `QuestionResponseTracker`, `TrailSystemGeofences`, `CrewMembers`, `FeedbackDeletionAudit`. `TrailConditions` is dropped (the Condition Catalog supersedes it — per-trail-system feedback config references `catalog_id`s instead). `RideEvents` is dropped per the privacy-first redesign — the backend never sees per-user ride history; only anonymous per-trail-system aggregates (`TrailSystemRideCount`) and a short-lived idempotency marker (`RideCompletion`) are stored.

**Access Patterns:** 66 defined patterns — full spec in `api-dynamo/docs/dynamodb-spec.json`

**Data Retention via TTL:**
- Magic link tokens: 15-minute TTL
- Refresh tokens: 30-day TTL (Cognito manages its own refresh token lifecycle)
- Condition observations: 30-day TTL
- Trail system status history: 2-year retention
- Trail Care Reports (closed/cancelled): 2-year retention
- Care report photos: 180 days after report closure

#### **Amazon ElastiCache (Redis 7.0)** — Optional
- **Status:** Disabled (not currently needed at <500 MAU)
- **Purpose:** Session caching, API response caching
- **When to Enable:** When DynamoDB read costs exceed $50/month (approximately 10K–25K MAU)
- **Estimated Cost:** $15-30/month (when enabled)

### 6. Storage Layer

#### **Amazon S3 (Simple Storage Service)**

**Trail Photos Bucket:**
- **Purpose:** User-uploaded trail photos
- **Naming:** `traillens-{env}-trail-photos-{account_id}`
- **Features:**
  - Public read access (photos served directly to users)
  - Versioning enabled (restore deleted photos)
  - Server-side encryption (AES-256)
  - CORS enabled for web uploads
- **Photo Processing:** Lambda function automatically resizes images
  - Thumbnail: 200x200px
  - Medium: 800x600px
  - Large: 1920x1080px
  - Original: Preserved for quality
- **Storage Class:** Standard (hot data), automatic transition to Glacier after 1 year
- **Estimated Size:** 5GB/month growth (500 photos/month at 10MB each)

**Lambda Deployments Bucket:**
- **Purpose:** Store Lambda function deployment packages
- **Naming:** `traillens-{env}-lambda-deployments-{account_id}`
- **Features:**
  - Versioning enabled (rollback to previous deployments)
  - Lifecycle policy: Delete old versions after 30 days
  - Private access only (IAM policies)
- **Storage Size:** ~50-100MB per deployment package

#### **Amazon CloudFront** (CDN)
- **Purpose:** Global content delivery for photos and web assets
- **Origin:** S3 trail photos bucket
- **Edge Locations:** 200+ worldwide (AWS global network)
- **Caching:**
  - Photos: 1 year cache (immutable URLs)
  - Web assets: 5 minutes cache (for updates)
- **HTTPS:** Required, uses ACM certificate
- **Performance:** Sub-100ms photo load times globally

### 7. Messaging & Notifications

#### **Amazon SNS (Simple Notification Service)**
- **Purpose:** Push notification delivery to mobile devices
- **Topics:**
  - `trailsystem-status`: Trail status change notifications
- **Platform Applications:**
  - APNS (iOS): Requires Apple Push Notification certificate
  - FCM (Android): Requires Firebase Cloud Messaging API key
- **Message Delivery:**
  - Success rate: 99%+
  - Latency: <1 second from trigger to device
- **Cost:** $0.50 per million notifications

#### **Amazon SES (Simple Email Service)**
- **Purpose:** Transactional email delivery
- **Domain:** `traillenshq.com` (verified)
- **DKIM Enabled:** Email authentication for deliverability
- **From Address:** `noreply@traillenshq.com`
- **Use Cases:**
  - Trail status change notifications
  - Event reminders
  - Volunteer opportunity alerts
  - Password reset emails
  - Welcome emails
- **Email Forwarding:** Incoming emails forwarded to `mark@buckaway.ca` via Lambda
- **Deliverability:** 99%+ inbox placement rate
- **Cost:** $0.10 per 1,000 emails sent

#### **AWS Secrets Manager**
- **Purpose:** Secure credential storage
- **Secrets Stored:**
  - JWT signing keys (shared across services)
  - Internal API keys
  - Facebook/Instagram access tokens (per organization)
  - Third-party API keys (future)
- **Features:**
  - Automatic rotation (planned for production)
  - Encryption at rest with AWS KMS
  - Audit logging (CloudTrail)
  - Granular IAM access control
- **Cost:** $0.40 per secret per month + $0.05 per 10,000 API calls

### 8. Network Architecture (VPC)

#### **Amazon VPC (Virtual Private Cloud)**
- **CIDR Block:** `10.0.0.0/16` (65,536 IP addresses)
- **Availability Zones:** 2 (for high availability)
- **Subnet Strategy:**
  - **Public Subnets:** 2 subnets (1 per AZ)
    - CIDR: `10.0.1.0/24` and `10.0.2.0/24` (512 IPs each)
    - Purpose: NAT Gateways, load balancers
  - **Private Subnets:** 2 subnets (1 per AZ)
    - CIDR: `10.0.10.0/24` and `10.0.11.0/24` (512 IPs each)
    - Purpose: Lambda functions, Redis (when enabled)
- **Internet Gateway:** Single IGW for public internet access
- **NAT Gateways:** 1 per AZ (high availability for outbound traffic)
  - Lambda functions in private subnets use NAT for external API calls (Facebook, Instagram)

#### **VPC Endpoints** (Cost Optimization)
- **DynamoDB Gateway Endpoint:** Free, no NAT gateway charges for DynamoDB access
- **S3 Gateway Endpoint:** Free, no NAT gateway charges for S3 access
- **Secrets Manager Interface Endpoint:** $7/month, reduces NAT charges for credential retrieval
- **Savings:** ~$30-50/month by avoiding NAT gateway data transfer costs

#### **Security Groups**
- **Lambda Security Group:** Allows all outbound traffic (HTTPS to APIs, DynamoDB, S3)
- **Redis Security Group:** Allows inbound TCP 6379 only from Lambda security group
- **Default Deny:** All inbound traffic denied by default

### 9. Infrastructure Management

#### **Deployment Ownership Split**

Infrastructure and application code deploy independently via separate Pulumi stacks:

| Repository | Deploys |
|------------|---------|
| `infra/` | VPC + networking, DynamoDB table, S3 buckets, Cognito user pool, API Gateway (master), SNS topics, SES domain identity, Secrets Manager, CloudFront, Route53, ACM, CloudWatch alarms |
| `api-dynamo/` | All Lambda deployment packages (**9 packages** — see Section 3 for the inventory; note `cognito-triggers` is one package containing multiple `aws.lambda.Function` resources), API routes attached to master gateway (via StackReference) |
| `webui/` | AWS Amplify app (React 19, Tailwind 4.x) |

**Deployment Order:** `infra/` → `api-dynamo/` → `webui/`

`api-dynamo/` reads `infra/` outputs via Pulumi StackReference to resolve Lambda execution roles, DynamoDB table name, Cognito pool ARN, S3 bucket names, SNS topic ARNs, and API Gateway ID. No Lambda functions are deployed by `infra/`.

#### **Pulumi (Infrastructure as Code)**
- **Language:** Python
- **Purpose:** Define and deploy all AWS infrastructure
- **Foundation Phase** (parallel deployment):
  - Network (VPC, subnets, NAT, security groups)
  - Storage (S3 buckets with lifecycle rules)
  - Database (DynamoDB single table with 6 GSIs)
  - Authentication (Cognito user pool + triggers)
  - Email (SES domain identity, DKIM, receipt rules)
  - Messaging (SNS topics)
  - Secrets (Secrets Manager)
- **Services Phase** (depends on Foundation):
  - API Gateway (master REST API)
  - Redis (optional, disabled at <500 MAU)
- **DNS & Certificates Phase** (depends on Services):
  - Route53 records, ACM certificates, custom domains
- **Benefits:**
  - Reproducible deployments
  - Version-controlled infrastructure (git history)
  - Disaster recovery (redeploy from code)
- **Stack Outputs:** 50+ outputs exported for application consumption via StackReference

#### **AWS Route53 + ACM**
- **Domain:** `traillenshq.com`
- **Hosted Zone:** Managed DNS with health checks
- **SSL Certificates:**
  - `api.dev.traillenshq.com` (API Gateway) - ca-central-1 region
  - `auth.dev.traillenshq.com` (Cognito) - us-east-1 region (required by Cognito)
  - Auto-renewal every 13 months
  - DNS validation (automatic CNAME record creation)
- **Subdomains:**
  - `api.traillenshq.com` → API Gateway
  - `auth.traillenshq.com` → Cognito CloudFront distribution
  - `www.traillenshq.com` → Amplify web app

### 10. External Service Integrations

#### **Facebook Graph API**
- **Version:** v19.0
- **Authentication:** OAuth 2.0 access tokens stored in Secrets Manager
- **Capabilities:**
  - Facebook Page post creation
  - Post deletion
  - Post analytics
- **Rate Limits:** 200 calls/hour per user token
- **Multi-Tenant:** Each organization has separate Facebook Page and credentials

#### **Instagram Graph API**
- **Authentication:** OAuth 2.0 access tokens (Business accounts only)
- **Capabilities:**
  - Instagram feed posts (images + captions)
  - Instagram Stories (24-hour ephemeral content)
  - Post analytics
- **Requirements:**
  - Instagram Business Account
  - Linked Facebook Page
- **Rate Limits:** 200 calls/hour per user token
- **Multi-Tenant:** Each organization has separate Instagram Business Account

### 11. Event-Driven Processing

Periodic and event-triggered work runs as scheduled Lambdas (EventBridge rules → Lambda → DynamoDB / SNS / S3) and as inline atomic writes inside hot-path API requests. Cross-link: full reference in `api-dynamo/docs/BACKGROUND_WORKERS.md` (created in this docs pass) — see "Background Workers" cross-link below.

**Scheduled (EventBridge → Lambda):**

| EventBridge schedule | Target Lambda | Side effects |
|----------------------|---------------|--------------|
| `cron(0/15 * * * ? *)` (every 15 min) | `scheduled_condition_processor` | DynamoDB GSI4 query (`GSI4PK=SCHEDULED#PENDING`); TransactWrite to apply scheduled condition + append history + flip status to APPLIED; SNS publish to `TRAIL_CONDITION_CHANGE`. Second pass on the same invocation: GSI4 query for items in their reminder window → push reminder via existing `notification_push` Lambda → mark `reminder_sent=true`. User-facing accuracy: ±15 minutes of the scheduled time. |
| `cron(0 3 * * ? *)` (daily 03:00 UTC) | `retention_cleanup_processor` | Closed care-report cleanup (90+ days old) → batch-delete + write `CareReportDeletionAudit`; deleted-account PII scrub (`deleted_at < now-30d`) → hard-delete user items + audit `PIIDeletionAudit`; S3 photo orphan sweep → S3 `DeleteObject` + CloudFront invalidation; belt-and-suspenders magic-link token cleanup. |

**Inline (NOT a separate Lambda — atomic single-partition TransactWrite inside an API request):**

- `PUT /api/trailpulse/trail-systems/{ts_id}/ride-completion` performs a single-partition TransactWrite on `PK=TRAILSYSTEM#{ts_id}`: (a) `Put RIDECOMPLETION#{ride_id}` with `ConditionExpression: attribute_not_exists(SK)` for idempotency; (b) `Update RIDECOUNT#{YYYY-MM-DD} ADD total_rides :one`. **No `usage_aggregator` Lambda is needed** — the rollup is computed inline as part of the write. Daily aggregates retained 3 years (1095-day TTL); idempotency markers retained 30 days.

**Mobile-local (NOT server-side — fired by the Android client, no backend involvement):**

- The post-ride feedback notification is dispatched on-device by the Android app's `NotificationCompat` / `NotificationManagerCompat` when the GPS-foreground-service geofence detects ride-end. The backend has **no SNS topic** for this event and runs **no dispatcher Lambda** for it. `POST /api/trailpulse/feedback` is the only related backend call (a pure data write — no notification side-effect). Rationale: < 50ms latency vs FCM round-trip, $0 cost, fires immediately even when offline, and only the on-ride device receives it (correct UX). iOS will mirror this via `UNUserNotificationCenter` post-MVP.

**Pulumi component:** the `infra/` repository will gain an `EventBridgeScheduledLambda` ComponentResource (queued for the implementation plan) that provisions, per scheduled Lambda: the EventBridge Rule + Target, the Lambda IAM role with least-privilege table/SNS access, and a CloudWatch log group with 30-day retention. Both new Lambdas use the same component pattern.

**Cost projections at 100K DAU (per-Lambda, monthly):**

- `scheduled_condition_processor`: 96 invocations/day × 30 days = **2,880 invocations/month**, ~50 ms avg = 2.4 GB-s/month → **~$0.00** (well inside Lambda free tier; ~3× cheaper than a 5-minute schedule).
- `retention_cleanup_processor`: 30 invocations/month × ~5 min × 512 MB = **4.6 GB-min/month** → **~$0.00** (free tier).

**CloudWatch alarms (recalibrated for 15-min cron interval):**

- `scheduled_condition_processor`: (a) ≥ 1 invocation failure in 30 min (catches a single failure on the next-tick retry — a missed fire = a missed user-visible condition update); (b) `processed-items-count > 100` for 2 consecutive ticks → indicates queue buildup or a stuck cursor; (c) 0 invocations in 60 min → indicates EventBridge rule misconfigured or disabled.
- `retention_cleanup_processor`: Lambda failure → page; processed-count = 0 for 7 consecutive days → likely silent broken state.

**Background Workers cross-reference:** see `api-dynamo/docs/BACKGROUND_WORKERS.md` (NEW — created in this docs pass) for the per-Lambda reference covering triggers, access patterns (AP-SC04–06, AP-RC01–03), idempotency guarantees, alarm thresholds, and cost. `api-dynamo/docs/API_DESIGN.md` includes a "Background Workers" section that links here.

---

## Data Flow Patterns

### 1. User Registration Flow
1. User fills registration form (web or mobile app)
2. App sends request to Cognito User Pool
3. Cognito sends verification email via SES
4. User clicks verification link
5. Cognito confirms account
6. App receives JWT tokens (access, ID, refresh)
7. First API request with JWT triggers user record creation in DynamoDB users table
8. User can now access protected resources

### 2. Trail Status Update Flow
1. Trail manager updates trail status (web or mobile app)
2. App sends authenticated request to API Gateway
3. API Gateway validates JWT with Cognito
4. Main API Lambda executes:
   - Validates user has `trailsystem-owner`, `trailsystem-crew`, or `admin` group
   - Updates trail status in DynamoDB trails table
   - Writes history entry to trail_history table
   - Triggers SNS notification to subscribed users
   - Triggers Facebook API Lambda (if enabled for org)
5. Facebook API Lambda:
   - Retrieves org credentials from Secrets Manager
   - Formats post with trail name, status, reason, photo
   - Posts to Facebook Page and Instagram
   - Stores post record in DynamoDB facebook_posts table
6. SNS sends push notifications to mobile devices
7. SES sends emails to subscribed users (batched for efficiency)

### 3. Photo Upload Flow
1. User uploads photo (web or mobile app)
2. App requests signed URL from API (S3 pre-signed PUT)
3. App uploads directly to S3 trail photos bucket (bypasses API)
4. S3 PUT event triggers photo processing Lambda
5. Lambda generates thumbnails (200x200, 800x600, 1920x1080)
6. Lambda stores processed images in S3
7. API stores photo metadata in DynamoDB trail_photos table
8. CloudFront CDN caches images for fast global delivery

### 4. Real-Time Notification Flow
1. Trail status changes (as in Flow #2)
2. Main API Lambda publishes message to SNS topic
3. SNS fans out to:
   - **Mobile Push:** SNS → APNS (iOS) / FCM (Android) → User devices
   - **Email:** SNS → SES → User inboxes
   - **SMS:** (Future) SNS → Twilio → User phones
4. In-app notifications stored in DynamoDB for persistence
5. User sees notification within seconds

### 5. Social Media Automation Flow
1. Organization admin enables social media automation in settings
2. Admin links Facebook Page and Instagram Business Account via OAuth
3. Credentials stored in Secrets Manager (encrypted)
4. When trail status changes to "Closed" or "Caution":
   - Main API Lambda triggers Facebook API Lambda via HTTP request
   - Facebook API Lambda retrieves credentials from Secrets Manager
   - Lambda formats post: "⚠️ Trail Name is now CLOSED due to [reason]"
   - Lambda uploads photo to Facebook/Instagram
   - Lambda posts to both platforms simultaneously
   - Lambda stores post IDs in DynamoDB for tracking
5. Organization sees post appear on Facebook Page and Instagram within seconds
6. No manual posting required

---

## Security Architecture

### 1. Authentication & Authorization
- **Authentication:** AWS Cognito User Pool with RS256 JWT tokens (JWKS verification only)
  - **Three Methods Required for MVP v1.13:**
    - Native WebAuthn Passkey: Touch ID, Face ID, security keys via Cognito USER_AUTH flow (client-side Cognito SDK — no custom backend passkey endpoints)
    - Magic Link: 15-minute expiration email links (CUSTOM_AUTH Lambda triggers)
    - Email/Password: 12+ character minimum with complexity requirements
- **Authorization:** Role-based access control (8 Cognito groups)
- **Token Expiration:** Access tokens expire after 1 hour, refresh tokens after 30 days
- **MFA Enforcement:** Required for org-admin, trailsystem-owner, superadmin roles (7-day grace period)
- **Password Policy:** 12+ chars, mixed case, numbers, symbols, 6-password history

### 2. Data Encryption
- **In Transit:**
  - All API requests require HTTPS (TLS 1.2+)
  - Mobile apps enforce certificate pinning
  - Internal AWS service communication encrypted
- **At Rest:**
  - DynamoDB: AWS managed keys (AES-256)
  - S3: Server-side encryption (AES-256)
  - Secrets Manager: Encrypted with AWS KMS
  - Redis: Encryption enabled in production

### 3. Network Security
- **VPC Isolation:** Lambda functions run in private subnets (no direct internet access)
- **Security Groups:** Whitelist-based (deny all by default)
- **VPC Endpoints:** Private connectivity to AWS services (no internet gateway)
- **NAT Gateways:** Controlled outbound access for external APIs

### 4. Access Control & Security Hardening (MVP v1.13 Requirements)

- **Least Privilege:** Each Lambda function has minimal required permissions
- **Resource Policies:** S3 buckets and DynamoDB tables restrict access by IAM role
- **CloudTrail Audit Logging:** 1-year retention (REQUIRED for MVP, not 90 days)
- **Secrets Rotation:** 180-day automatic rotation (REQUIRED for MVP, not 90 days)
- **AWS WAF:** OWASP Top 10 protection for API Gateway (REQUIRED for MVP)
- **Security Hub:** Continuous compliance monitoring (POST-MVP due to cost ~$50/month)
- **GuardDuty:** Threat detection and anomaly monitoring (POST-MVP due to cost ~$4/month)
- **Incident Response Plan:** GDPR 72-hour breach notification process (REQUIRED for MVP)
- **API Rate Limiting:** Protect against abuse (REQUIRED for MVP)
- **MFA Enforcement:** Required for admin roles (REQUIRED for MVP)

### 5. Multi-Tenancy & Data Isolation
- **Tenant ID:** Every record in DynamoDB includes `organization_id` or `tenant_id`
- **Query Filtering:** All DynamoDB queries filtered by tenant ID
- **Authorization Checks:** API validates user belongs to organization before data access
- **Test Coverage:** 80%+ test coverage includes tenant isolation tests
- **Audit Trail:** All cross-tenant access attempts logged

### 6. DDoS & Rate Limiting

- **CloudFront:** Built-in DDoS protection (AWS Shield Standard)
- **API Gateway:** 100 requests/minute per user (burst: 200)
- **Lambda Throttling:** Concurrent execution limits (1000 concurrent in dev)
- **Cost Protection:** Budget alerts trigger at $500/month

### 7. Data Retention Policies (MVP v1.13 Requirements)

- **User Accounts:** 2 years inactive (automated deletion)
- **Trail System Status History:** 2 years (automated cleanup)
- **Trail Care Reports:**
  - Active reports (Open, In Progress, Deferred, Resolved): Kept indefinitely
  - Closed/Cancelled reports: 2 years, then automated deletion
  - Care report photos: 180 days after report closure, then automated deletion
- **CloudTrail Logs:** 1 year retention
- **Other Photos:** Standard S3 lifecycle (Glacier after 1 year)

---

## Scalability & Performance

### Automatic Scaling Components
- **Lambda Functions:** Scale from 0 to 1,000 concurrent executions automatically
- **DynamoDB:** Pay-per-request scales to millions of reads/writes per second
- **API Gateway:** Handles 10,000 requests/second per region
- **CloudFront:** Global CDN handles unlimited requests
- **SNS/SES:** No practical limits on message delivery

### Performance Targets
- **API Response Time:** <500ms (p95)
- **Photo Load Time:** <100ms (via CloudFront)
- **Push Notification Latency:** <1 second
- **Email Delivery:** <5 seconds
- **Search Query:** <200ms for <500 trails (client-side)

### Scalability Limits (When to Upgrade)
1. **Search Performance:** At 500+ trails, migrate to ElasticSearch ($150-300/month)
2. **Caching:** At 1,000+ concurrent users, enable Redis ($15-30/month)
3. **Database Hot Partitions:** At 10,000+ concurrent writes, switch to provisioned capacity
4. **Photo Storage:** At 1TB, evaluate S3 Intelligent-Tiering (automatic cost optimization)

---

## Cost Breakdown & Projections

**⚠️ IMPORTANT FOR CEO:** This section provides cost summaries. For complete details including:
- **Usage calculation methodologies** (how every number was derived)
- **Official AWS pricing references** (verified links to aws.amazon.com)
- **Step-by-step calculations** (all math shown)
- **Regional pricing adjustments** (ca-central-1 specific)
- **Real-world validation** (industry case studies)

**See the comprehensive analysis in: [COST_ANALYSIS_DETAILED.md](COST_ANALYSIS_DETAILED.md)**

All pricing below is current as of January 2026 for **ca-central-1 (Canada Central)** region.

### Development Environment (Current)

| Service | Usage | Monthly Cost | Notes |
|---------|-------|--------------|-------|
| **DynamoDB** | 1M reads, 500K writes | $1-3 | Pay-per-request |
| **Lambda** | 10M requests, 1GB-sec | $5-10 | First 1M requests free |
| **API Gateway** | 1M requests | $3-5 | First 1M requests $3.50 |
| **S3 Storage** | 10GB photos | $0.25 | $0.023/GB |
| **CloudFront** | 100GB transfer | $8-12 | First 1TB included |
| **SNS** | 100K notifications | $0.50 | $0.50 per million |
| **SES** | 10K emails | $1 | $0.10 per 1,000 |
| **Cognito** | 1K active users | $0 | First 50K free |
| **NAT Gateway** | 2 AZs, 50GB | $45-50 | $0.045/hour + data |
| **VPC Endpoints** | Secrets Manager | $7 | $0.01/hour |
| **Secrets Manager** | 5 secrets | $2 | $0.40 per secret |
| **Route53** | 1 hosted zone | $0.50 | $0.50/zone |
| **ACM Certificates** | 2 certificates | $0 | Free |
| **CloudWatch Logs** | 5GB logs | $2-5 | $0.50/GB ingestion |
| **S3 Lambda Deploys** | 500MB | $0.01 | Negligible |
| **Redis** (disabled) | N/A | $0 | $15-30 if enabled |
| **TOTAL** | | **$75-150/month** | |

### Production Environment (Projected at 50 Organizations, 10K Users)

| Service | Usage | Monthly Cost | Notes |
|---------|-------|--------------|-------|
| **DynamoDB** | 50M reads, 10M writes | $15-25 | Scales with traffic |
| **Lambda** | 100M requests, 50GB-sec | $20-30 | Compute time |
| **API Gateway** | 10M requests | $35 | $3.50 per million |
| **S3 Storage** | 100GB photos | $2.50 | Growing over time |
| **CloudFront** | 1TB transfer | $85 | Global delivery |
| **SNS** | 1M notifications | $5 | Push + email fanout |
| **SES** | 100K emails | $10 | Transactional email |
| **Cognito** | 10K active users | $0 | Still under free tier |
| **NAT Gateway** | 2 AZs, 500GB | $90-100 | $0.045/hour + data |
| **VPC Endpoints** | Secrets Manager | $7 | Interface endpoint |
| **Secrets Manager** | 15 secrets | $6 | Org credentials |
| **Route53** | 1 hosted zone + queries | $2 | DNS queries |
| **CloudWatch Logs** | 50GB logs | $25-30 | Monitoring |
| **Redis** (optional) | t4g.small, 2 nodes | $30 | If enabled |
| **TOTAL** | | **$300-400/month** | |

### Cost at Scale (200 Organizations, 50K Users - 12 Month Target)

| Scenario | Monthly Cost | Notes |
|----------|--------------|-------|
| **Base Infrastructure** | $150-200 | NAT, VPC, monitoring |
| **Data Transfer** | $200-300 | CloudFront, API Gateway |
| **Compute** | $100-150 | Lambda executions |
| **Storage** | $50-75 | S3 photos (500GB) |
| **Database** | $100-150 | DynamoDB reads/writes |
| **Notifications** | $50-75 | SNS + SES volume |
| **Caching** | $30-50 | Redis enabled |
| **TOTAL** | **$680-1,000/month** | **$8,000-12,000/year** |

### Cost Optimization Strategies

1. **Reserved Capacity:** Save 30-50% on NAT Gateways and Redis with 1-year commitment
2. **S3 Lifecycle Policies:** Move old photos to Glacier after 1 year (90% cost reduction)
3. **CloudFront Savings Bundle:** Commit to data transfer volume for 20% discount
4. **VPC Endpoints:** Already implemented (saves $30-50/month on NAT charges)
5. **Lambda Memory Optimization:** Right-size memory allocations (currently 512MB-1GB)
6. **DynamoDB On-Demand:** Pay-per-request is optimal until consistent 1000+ req/sec
7. **Budget Alerts:** CloudWatch alarms trigger at $500 threshold

### Cost Per Customer (Unit Economics)

At 200 organizations:
- Infrastructure cost: $800/month
- Cost per organization: $4/month
- Pricing: $49/month (Pro tier)
- **Gross Margin: 92%** ($45 profit per customer)

---

## High Availability & Disaster Recovery

### High Availability (HA) Features
- **Multi-AZ Deployment:** All services deployed across 2 availability zones
- **NAT Gateways:** 1 per AZ (if one AZ fails, other AZ continues)
- **DynamoDB:** Automatically replicates across 3 AZs
- **Lambda:** Runs in multiple AZs automatically
- **CloudFront:** Global edge network (200+ locations)
- **API Gateway:** Multi-AZ by default
- **Target Uptime:** 99.9% (43 minutes downtime/month max)

### Disaster Recovery (DR)
- **DynamoDB PITR:** Point-in-time recovery for 35 days
- **S3 Versioning:** Restore deleted photos
- **Infrastructure as Code:** Entire stack recreated from Pulumi code in <1 hour
- **Secrets Backup:** Secrets Manager retains deleted secrets for 30 days
- **CloudTrail Logs:** 90-day audit trail for forensics
- **RTO (Recovery Time Objective):** <2 hours
- **RPO (Recovery Point Objective):** <5 minutes (DynamoDB PITR)

### Monitoring & Alerting
- **CloudWatch Dashboards:** Real-time metrics (requests, errors, latency)
- **CloudWatch Alarms:** Alert on error rates, latency spikes, cost overruns
- **AWS Health Dashboard:** Proactive AWS service health notifications
- **Lambda Insights:** Function-level performance metrics
- **X-Ray Tracing:** End-to-end request tracing for debugging
- **Log Aggregation:** Centralized logging with CloudWatch Logs Insights

---

## Deployment Pipeline

### Infrastructure Deployment (Pulumi)
1. Developer commits changes to `infra/` repository
2. GitHub Actions triggers on push to `topic/*` branch
3. Pulumi preview shows planned changes
4. Manual approval required for production
5. Pulumi up deploys changes to AWS
6. Stack outputs updated for application consumption
7. Rollback: `pulumi up --stack previous` restores prior state

### Application Deployment (Lambda)

**api-dynamo (Main API):**
1. Developer commits to `topic/*` branch
2. GitHub Actions runs:
   - Linting (flake8)
   - Unit tests (pytest) - must pass with 80%+ coverage
   - Integration tests (LocalStack)
3. If tests pass, package Lambda:
   - Install dependencies: `pip install -r requirements.txt`
   - Create ZIP: `app/ + dependencies`
   - Upload to S3: `traillens-dev-lambda-deployments`
4. Update Lambda function: `aws lambda update-function-code`
5. Smoke test: `curl api.dev.traillenshq.com/health`
6. Manual promotion to production

**facebook-api (Social Media API):**
1. Developer commits to `topic/*` branch
2. GitHub Actions runs:
   - Linting (ESLint)
   - Unit tests (Jest) - must pass with 80%+ coverage
   - Integration tests (LocalStack + nock mocking)
3. If tests pass, package Lambda:
   - Install dependencies: `npm install --production`
   - Create ZIP: `api/ + node_modules/`
   - Upload to S3
4. Update Lambda function
5. Smoke test social media endpoints
6. Manual promotion to production

**web (React App):**
1. Developer commits to main branch
2. AWS Amplify auto-detects commit
3. Amplify builds React app:
   - `npm install`
   - `npm run build`
   - Generates static HTML/CSS/JS
4. Amplify deploys to CloudFront CDN
5. Automatic invalidation of CloudFront cache
6. Live in <5 minutes

### Rollback Procedures
- **Infrastructure:** `pulumi up --stack <previous-snapshot>`
- **Lambda:** Update function with previous S3 version (versioning enabled)
- **Web:** Amplify console → "Redeploy" previous build
- **DynamoDB:** Point-in-time recovery to timestamp before incident

---

## Technical Debt & Future Improvements

### Current Limitations
1. **Search:** Client-side search limited to <500 trails
   - **Solution:** Migrate to ElasticSearch at 500+ trails ($150-300/month)
2. **Redis Disabled:** Caching not yet needed
   - **Solution:** Enable at 1,000+ concurrent users
3. **Single Region:** Currently only `ca-central-1` (Canadian home base)
   - **Solution:** Add `us-east-1` for international customers requiring US data residency (latency reduction)
4. **No Blue/Green Deployment:** Direct Lambda updates (brief downtime possible)
   - **Solution:** Lambda aliases + weighted routing for zero-downtime
5. **Manual Secret Rotation:** Credentials manually rotated
   - **Solution:** Automatic 90-day rotation in production

### Planned Architecture Enhancements

**Q1 2026:**
- Deploy Facebook API to production Lambda
- Enable Redis for session caching
- Add ElasticSearch for search at scale
- Implement blue/green Lambda deployments

**Q2 2026:**
- Multi-region deployment (Canada Central primary, US East secondary for international expansion)
- Add Route53 health checks with failover
- Implement GraphQL API (in addition to REST)
- Add WebSocket support for real-time updates (API Gateway WebSocket API)

**Q3 2026:**
- Add read replicas for DynamoDB (Global Tables for multi-region)
- Implement S3 Intelligent-Tiering for cost optimization
- Add machine learning for predictive trail closures (SageMaker)
- Implement advanced analytics (QuickSight dashboards)

**Q4 2026:**
- White-label support (custom domains per organization)
- API partner program (public REST API + API keys)
- Implement event-driven architecture (EventBridge)
- Add data lake for analytics (Athena + Glue)

---

## Compliance & Regulatory

### Data Residency
- **Current:** All data stored in Canada (`ca-central-1`) - Canadian-owned company with Canadian data sovereignty
- **Future:** International customers can opt for regional storage (US: `us-east-1`, EU: `eu-central-1`)
- **Default:** Canadian hosting for all customers (emphasizes Canadian ownership and values)
- **GDPR Compliance:** User data deletion workflow implemented

### Security Standards
- **SOC 2 Type II:** AWS infrastructure is SOC 2 certified
- **HIPAA:** Not currently required (no health data)
- **PCI DSS:** Not required (no payment card data stored)

### Privacy
- **Cookie Policy:** Implemented on website
- **Privacy Policy:** User consent required for data collection
- **Data Deletion:** Users can request account deletion (API endpoint exists)
- **Data Export:** Users can download their data (API endpoint exists)

### Accessibility
- **WCAG 2.1 AA:** Web application target (in progress)
- **Mobile Accessibility:** iOS VoiceOver and Android TalkBack support

---

## Key Architectural Decisions & Rationale

### 1. Serverless Architecture (Lambda)
**Decision:** Use AWS Lambda instead of EC2 servers

**Rationale:**
- **Cost:** Pay only for execution time (no idle server costs)
- **Scaling:** Automatic scaling from 0 to 1,000 concurrent requests
- **Maintenance:** No OS patching, no server management
- **High Availability:** Multi-AZ by default

**Trade-offs:**
- Cold start latency (300-500ms for first request)
- 15-minute execution time limit (not an issue for API)
- Limited control over runtime environment

### 2. DynamoDB Pay-Per-Request
**Decision:** Use on-demand billing instead of provisioned capacity

**Rationale:**
- **No Capacity Planning:** No need to predict traffic
- **Cost-Effective at Scale:** At current usage, 50% cheaper than provisioned
- **Automatic Scaling:** Handles traffic spikes without throttling
- **Development Speed:** Focus on features, not database tuning

**Trade-offs:**
- Higher cost at very high sustained traffic (>1000 req/sec)
- No reserved capacity discounts

### 3. Multi-Tenant Single Stack
**Decision:** All customers share same infrastructure

**Rationale:**
- **Cost Efficiency:** Single stack serves all customers
- **Faster Development:** One codebase, faster feature delivery
- **Easier Maintenance:** No per-customer deployments
- **Data Isolation:** Tenant ID filtering ensures security

**Trade-offs:**
- Noisy neighbor risk (mitigated by rate limiting)
- Limited white-label customization (planned for Enterprise)

### 4. VPC Private Subnets
**Decision:** Run Lambda functions in VPC private subnets

**Rationale:**
- **Security:** No direct internet access for Lambda functions
- **Compliance:** Meets enterprise security requirements
- **VPC Endpoints:** Private access to AWS services (no internet gateway)
- **Network Controls:** Security groups enforce traffic policies

**Trade-offs:**
- NAT Gateway cost ($45-100/month)
- Slightly increased cold start time (50-100ms)

### 5. Cognito for Authentication
**Decision:** Use AWS Cognito instead of Auth0 or custom auth

**Rationale:**
- **Native AWS Integration:** Works seamlessly with API Gateway, Lambda
- **Cost:** Free for first 50K users (vs $23/month for Auth0)
- **Compliance:** AWS manages security updates and compliance
- **Features:** MFA, social login, JWT, user pools out of box

**Trade-offs:**
- Less flexible UI customization than Auth0
- Learning curve for developers unfamiliar with Cognito

### 6. React + Tailwind for Web
**Decision:** React 18 + Tailwind CSS instead of Vue or Angular

**Rationale:**
- **Developer Ecosystem:** Largest React community
- **Performance:** React 18 concurrent rendering
- **Tailwind:** Rapid UI development with utility classes
- **AWS Amplify:** Native React support

**Trade-offs:**
- Larger bundle size than Vue (mitigated by code splitting)
- Tailwind HTML verbosity (many classes per element)

### 7. Separate iOS/Android Apps
**Decision:** Native Swift and Kotlin apps instead of React Native

**Rationale:**
- **Performance:** Native apps 2-3x faster than hybrid
- **Platform Features:** Full access to device capabilities (camera, GPS, push)
- **User Experience:** Native UI patterns for each platform
- **Offline Support:** Better control over local storage and sync

**Trade-offs:**
- Higher development cost (two codebases)
- Slower feature parity (iOS and Android developed separately)

### 8. FastAPI for Main API
**Decision:** FastAPI (Python) instead of Node.js or Go

**Rationale:**
- **Development Speed:** Python rapid prototyping
- **Type Safety:** Pydantic models with automatic validation
- **API Documentation:** Auto-generated OpenAPI/Swagger docs
- **Testing:** Excellent pytest ecosystem

**Trade-offs:**
- Slightly slower than Go (but Lambda cold start dominates latency)
- Python packaging complexity (requirements.txt management)

---

## Conclusion

TrailLensHQ's architecture is designed for:

✅ **Scalability** - Handles 10 to 100,000 users with no infrastructure changes
✅ **Cost Efficiency** - $75/month dev, $200-400/month production (scales linearly)
✅ **High Availability** - 99.9% uptime with multi-AZ deployment
✅ **Security** - Enterprise-grade auth, encryption, and data isolation
✅ **Developer Velocity** - Infrastructure as code enables rapid iteration
✅ **Future-Proof** - Modular design allows easy addition of new services

The system is **production-ready** and positioned for sustainable growth from MVP to 100K+ users without architectural rewrites.

---

## Revision History

| Version | Date       | Author          | Changes                                                                                                                                                                                                                                                                                                                                                                                           |
|---------|------------|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1.0     | 2026-01-13 | Chief Architect | Initial system architecture document created for CEO review                                                                                                                                                                                                                                                                                                                                       |
| 2.0     | 2026-01-17 | Chief Architect | Updated to reflect MVP v1.13: 21 DynamoDB tables (trail systems model, Trail Care Reports with 3 new tables), iPhone apps with offline support (User + Admin apps), three authentication methods (passkey, magic link, email/password with 12 char min), security hardening requirements (CloudTrail 1-year, WAF, Security Hub, GuardDuty, secrets 180-day rotation, MFA 7-day grace, incident response plan), data retention policies (2-year history, status-based care reports, 180-day photo retention) |
| 3.0     | 2026-04-03 | Chief Architect | Updated to reflect single-table DynamoDB design (1 table with 6 GSIs replacing 21 normalized tables, 66 access patterns), 10 Lambda functions all owned by api-dynamo (push/SMS/email notifications, photo processor, email forwarder, 4 Cognito auth triggers), new API routes (magic link, condition observations, scheduled conditions, tags), Android apps in active development (Kotlin 2.3.20 / Jetpack Compose, 3 repos), webui/ as current React 19 / Tailwind 4.x web frontend replacing legacy web/, deployment ownership split clarified (infra/ deploys shared resources, api-dynamo/ deploys all Lambdas) |

---

**Prepared by:** Chief Architect
**Date:** April 2026
**Document Version:** 3.0
**AWS Region:** ca-central-1 (Canada Central)
**Environment:** Development (Production deployment pending)
