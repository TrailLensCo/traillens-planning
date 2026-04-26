---
title: "TrailLensHQ MVP Implementation Project Plan"
author: "Chief Development Manager"
date: "January 2026"
abstract: "Comprehensive implementation plan for TrailLensHQ MVP v1.13 covering 14 phases, dependencies, timelines, and success criteria with AI-assisted development approach. V4: Android-first mobile, single-table DynamoDB, webui/ greenfield rewrite."
---

<!--
CTO DIRECTIVE - DOCUMENT GENERATION REQUIREMENTS:

As the CTO, I reviewed the MVP_PROJECT_PLAN and it has wording and tasks that suggest someone has to do research. For example:

Task 3.1: Research Cognito Passkey Support

This is not good enough. The CTO requires the project plan to be fully vetted.

Create a V2 version of the document as a backup and regenerate the base document. Create a new version by going through the plan ONCE TASK AT A TIME, and copying the tasks to the new file one task at a time making sure anything that requires research or has some unknowns is researched with references. You must do the research by searching relevant documentation and updating the task to indicate the research has been done and what changes are required to the plan. You must update task at a time to avoid running out of context.

At the end, re-review the new document to make sure you have fully completed the task, no shortcuts, no laziness. You are to work 24/7 until the update is done with no breaks or complaining about time limits or resources.

Add this prompt to the top of the file in the comments section.

---

CTO DIRECTIVE V3 - PASSKEY MFA CORRECTION:

"*Passkeys NOT compatible with required MFA**: If MFA is required in user pool, users cannot sign in with passkeys. Make MFA OPTIONAL for passkey users."

Not sure where this idea came from. Passkey is a form of MFA. Therefore, MFA IS enabled if passkey setup. Update the document accordingly.

Make a backup of the current plan before making changes.

Add this prompt to to the top of the new file.

---

DOCUMENT STATUS: V4 - Android Priority, Single-Table DynamoDB, WebUI Rewrite

V2 RESEARCH SUMMARY:
- Task 3.1: AWS Cognito native passkey support confirmed (Nov 2024 launch)
- Task 3.2: Passkey implementation using Cognito APIs (no custom crypto needed)
- Task 3.3: Magic link requires custom implementation (EMAIL_OTP alternative available)
- Task 3.4: Password policy and history fully supported in Cognito
- Task 12.1: AWS SDK for iOS EOL Aug 2026 - MUST use AWS Amplify for Swift
- Task 12.5: Core Data selected for offline report queue (vs UserDefaults)
- Task 12.7: Core Data selected for offline caching (consistency)
- Risk Section: Updated with resolution of authentication and iOS SDK risks

V3 CORRECTIONS:
- CRITICAL CLARIFICATION: Passkeys ARE multi-factor authentication (inherently)
- AWS Cognito's "MFA required" setting refers to ADDITIONAL factors beyond primary authentication
- When using passkeys, Cognito MFA must be set to "optional" - this is a Cognito implementation detail
- Passkey authentication (something you have + something you are/know) is already multi-factor
- Document updated to clarify that setting MFA to "optional" does NOT disable multi-factor security
- Passkeys provide stronger authentication than password + SMS/TOTP MFA

All technical unknowns have been researched and resolved with authoritative AWS documentation references.

V4 UPDATES - MARCH 2026:
- CRITICAL: Android apps now replace iOS as first mobile priority; both platforms in MVP
- Phase 12 renamed from "iPhone Apps" to "Mobile Apps (Android + iOS)" — Android-first with Kotlin/Compose
- Android User App: 36 screens (Kotlin 2.0+, Jetpack Compose, Material Design 3, Hilt DI, Room, FCM)
- Android Admin App: 42 screens (same stack, admin role gate, conditions/care reports/team management)
- Figma mockups accelerating design for both Android apps
- iOS remains in MVP as parallel track (Swift/SwiftUI) with same level of detail as Android
- Post-MVP: Consider consolidating User + Admin into single app per platform
- DynamoDB: Updated from 21-table multi-table to single-table design with entity prefixes (ORG#, USER#, TRAILSYSTEM#, REPORT#, etc.)
- Current production: 7-table multi-table design (ADR-001); single-table is scale target
- 5 overloaded GSIs, 78 access patterns, 16 MVP entity types, TTL for transient data
- WebUI: web/ replaced by webui/ — greenfield React 19 + TypeScript + Vite 6.x + Tailwind CSS 4.x
- WebUI stack: shadcn/ui + Tremor + Lucide React, Zustand 5.x + React Query 5.x
- Feature-based organization, 5-tier routing, 5 auth methods, all routes lazy-loaded
- Push notifications: SNS → FCM (Android) + SNS → APNS (iOS)
- Out of Scope updated: "Android apps" removed, "iOS/Android app consolidation" added
-->

# TrailLensHQ MVP Implementation Project Plan

**Chief Development Manager Report | January 2026 | Document Version 1.0**

---

## Executive Summary

This document provides a comprehensive implementation plan for **TrailLensHQ MVP v1.13**, targeting a **Q2 2026 launch** with pilot organizations Hydrocut and GORBA (3 trail systems total).

**Project Scope:**
- **14 Implementation Phases**: From brand messaging to testing and validation
- **Target Launch**: Q2 2026 (April-June 2026)
- **Pilot Organizations**: Hydrocut (1 trail system with Glasgow and Synders areas) and GORBA (Guelph Lake + Akell)
- **Development Approach**: AI-assisted development with Claude Sonnet 4.6 / Claude Opus 4.6 for accelerated delivery

**Key Context:**
- **Existing Codebase**: Exploratory prototype exists in `api-dynamo/`, `webui/`, and `infra/` repositories (`web/` deprecated, replaced by `webui/`)
- **Current State**: ~60-70% of core infrastructure and features implemented
- **Net-New Development**: Mobile apps — Android (User + Admin) and iOS (User + Admin), Trail Care Reports system, tag-based status, security hardening
- **AI-Assisted Timeline**: 45-75 days (vs. 83-122 days traditional development)

**Critical Success Factors:**
- All 14 phases MUST be completed before launch
- Security hardening (Phase 2) is REQUIRED before handling production data
- Mobile apps (Phase 12) are REQUIRED for MVP - cannot launch without them (Android-first, iOS parallel track)
- Pilot onboarding (Phase 13) must be white-glove quality

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Project Overview](#project-overview)
3. [Implementation Approach](#implementation-approach)
4. [Existing Codebase Assessment](#existing-codebase-assessment)
5. [Phase 1: Brand Messaging Update](#phase-1-brand-messaging-update)
6. [Phase 2: Security Hardening](#phase-2-security-hardening)
7. [Phase 3: Authentication System](#phase-3-authentication-system)
8. [Phase 4: PII Protection](#phase-4-pii-protection)
9. [Phase 5: Trail System Data Model](#phase-5-trail-system-data-model)
10. [Phase 6: Tag-Based Status Organization](#phase-6-tag-based-status-organization)
11. [Phase 7: Status Management](#phase-7-status-management)
12. [Phase 8: Scheduled Status Changes](#phase-8-scheduled-status-changes)
13. [Phase 9: Trail Care Reports System](#phase-9-trail-care-reports-system)
14. [Phase 10: Notification System](#phase-10-notification-system)
15. [Phase 11: Web Dashboards](#phase-11-web-dashboards)
16. [Phase 12: Mobile Apps (Android + iOS)](#phase-12-mobile-apps-android--ios)
17. [Phase 13: Pilot Onboarding](#phase-13-pilot-onboarding)
18. [Phase 14: Testing and Validation](#phase-14-testing-and-validation)
19. [Dependencies and Critical Path](#dependencies-and-critical-path)
20. [Timeline and Milestones](#timeline-and-milestones)
21. [Success Criteria](#success-criteria)
22. [Revision History](#revision-history)

---

## Project Overview

### MVP Definition and Scope

**TrailLensHQ MVP v1.13** is a comprehensive multi-tenant SaaS platform for real-time **trail system** status management and outdoor recreation area management.

**IMPORTANT DATA MODEL:** TrailLensHQ manages **trail systems** (collections of trails managed as one unit), NOT individual trails within those systems. Each organization has one or more trail systems (e.g., Hydrocut has one trail system with Glasgow and Synders areas, GORBA has Guelph Lake and Akell trail systems).

### Core MVP Features (In Scope)

**1. Trail System Management**
- Trail system CRUD (create, read, update, delete)
- Real-time status updates with tag-based organization (max 20 tags per org)
- Status history with 2-year retention
- Scheduled status changes with automated cron processing
- Bulk operations

**2. Trail Care Reports System**
- Unified issue tracking (replaces separate work logs and user reports)
- P1-P5 priority system
- Public/private visibility control
- Type tags (max 25 per org)
- Assignment workflow (unassigned pool, specific assignment, self-assignment)
- Comments system with photos
- Activity log and audit trail
- Status-based retention policy (active indefinitely, closed/cancelled 2 years)
- Multiple photos per report (up to 5)
- Offline report creation support (local queueing for 7 days)

**3. Authentication & Security**
- Three authentication methods (ALL REQUIRED):
  - Passkey (WebAuthn/FIDO2): Touch ID, Face ID, security keys - **inherently multi-factor**
  - Magic Link: 15-minute expiration email links
  - Email/Password: 12+ char minimum with complexity requirements
- MFA enforcement for admin roles using password-based login (7-day grace period)
  - Note: Passkey users exempt from traditional MFA (passkeys are already multi-factor)
- Security hardening (7 critical gaps):
  - CloudTrail (1-year retention)
  - AWS WAF (OWASP Top 10 protection)
  - Secrets rotation (180-day cycle)
  - Incident response plan
  - API rate limiting (100 req/min per user)
  - **Post-MVP**: Security Hub (compliance monitoring), GuardDuty (threat detection)

**4. Mobile Apps (REQUIRED)**
- **Android User App** (com.traillens.app): 36 screens — trail system discovery, status viewing, care report submission, TrailPulse observations, offline support (Kotlin 2.0+, Jetpack Compose, Material Design 3, Hilt DI, Room, FCM)
- **Android Admin App** (com.traillens.admin): 42 screens — trail system management, full care report CRUD, conditions management, team/user management, work logs, offline support (same tech stack, admin role validation gate)
- **iOS User App**: Same feature set as Android User App (Swift/SwiftUI, Core Data, APNS)
- **iOS Admin App**: Same feature set as Android Admin App (Swift/SwiftUI, Core Data, APNS)
- Figma mockups driving design for all mobile apps
- Android distribution: Google Play internal testing track for MVP
- iOS distribution: TestFlight for MVP
- Push notifications: FCM via AWS SNS (Android), APNS via AWS SNS (iOS)
- Offline status caching (7 days)
- Offline report creation with auto-upload
- Post-MVP: Consider consolidating User + Admin into single app per platform

**5. Web Dashboards**
- Role-specific dashboards (8 roles)
- Trail system management UI
- Care report management UI
- Analytics dashboards
- Tag management UI
- User management UI

**6. Notification System**
- Email notifications (AWS SES)
- SMS notifications (AWS Pinpoint)
- Push notifications (SNS → FCM for Android, SNS → APNS for iOS)
- Subscription management
- Notification preferences

**7. TrailPulse - User Condition Observations (REQUIRED)**
- User-submitted trail condition observations using org-defined condition tags
- Observation summary with tag distribution (24h/7d aggregation)
- Admin observation management (view, mark viewed/closed, delete)
- Rate limiting (1 observation per user per trail system per 24h)
- 30-day observation retention (DynamoDB TTL auto-cleanup)
- Organization membership enforcement on all user endpoints
- **MVP Scope**: 6 API endpoints for condition observations (subset of full TrailPulse spec)
- **Deferred**: GPS geofencing, ride detection, post-ride notifications, crew management, frequency-based questions

### Out of Scope for MVP

- iOS/Android app consolidation (User + Admin into single app per platform — post-MVP)
- Social media automation (Facebook/Instagram API)
- Community features (forums, events, volunteer hub)
- Reviews and ratings
- Advanced analytics and reporting
- Multi-region deployment (Canada only for MVP)
- Payment processing (pilot organizations get free Enterprise tier)

### Pilot Organization Details

**Confirmed Pilot Organizations:**

1. **Hydrocut** - 1 trail system
   - Hydrocut trail system (includes Glasgow and Synders areas)

2. **GORBA** - 2 trail systems
   - Guelph Lake trail system
   - Akell trail system

**Total**: 3 trail systems for MVP

**Pilot Approach:**
- Free Enterprise tier for 6-12 months
- White-glove onboarding with live training sessions
- Load historical trail system data and status updates
- Use as case studies for marketing after 90 days
- Provide dedicated support channel (Slack or email)

### Success Metrics

**Technical Metrics:**
- 99.9% API uptime
- <500ms API response time (p95)
- <2 minutes notification latency
- 99% email delivery rate
- 95% push notification delivery rate

**Pilot Metrics:**
- All 3 trail systems operational
- 70%+ of trail users subscribed within first month
- 90%+ of status changes include photo and reason
- 5+ trail crew members actively using admin app
- Zero critical bugs in production after 30 days

**Business Metrics:**
- Both pilot organizations renew after 6 months
- At least 2 referrals from pilot organizations
- Case studies completed for both organizations
- Product-market fit validated (NPS > 50)

---

## Implementation Approach

### AI-Assisted Development Methodology

This project leverages **Claude Sonnet 4.5** for AI-assisted development, significantly accelerating delivery timelines while maintaining high code quality.

**AI-Assisted Tasks:**
- Code generation (API endpoints, UI components, infrastructure code)
- Test writing (unit tests, integration tests)
- Documentation generation (API docs, user docs, inline comments)
- Code review and refactoring
- Bug fixing and debugging

**Human-Led Tasks:**
- Product decisions and requirements clarification
- UX/UI design review
- Manual testing and user acceptance
- Infrastructure deployment and monitoring
- Pilot organization communication

**Timeline Impact:**
- **Traditional Development**: 83-122 days (4-6 months)
- **AI-Assisted Development**: 45-75 days (1.5-2.5 months)
- **Acceleration Factor**: ~1.8x faster

### Agile Sprint Structure

**Sprint Duration**: 2 weeks (recommended)
**Sprint Cadence**:
- Sprint Planning: Monday morning (2 hours)
- Daily Standups: 15 minutes (async via Slack acceptable for AI pair)
- Sprint Review: Friday afternoon (1 hour)
- Sprint Retrospective: Friday afternoon (30 minutes)

**Sprint Team**:
- CTO (Product Owner + Technical Lead)
- AI Assistant (Claude Sonnet 4.5 - Development Partner)
- Additional developers as needed

### Code Review and Quality Assurance

**Code Review Process:**
1. All code changes via pull requests (no direct commits to main)
2. AI-generated code reviewed by human developer
3. Automated tests must pass before merge
4. Constitution linter must pass (no violations)
5. Manual QA testing for UI changes

**Quality Gates:**
- Unit test coverage: 80%+ for new code
- Integration tests for all API endpoints
- E2E tests for critical user flows
- Manual testing for mobile apps (Google Play internal track / TestFlight)
- Security scanning (no secrets in code)

### Testing Strategy

**Unit Testing:**
- Python: pytest with 80%+ coverage
- TypeScript: Jest/Vitest for React components
- Android: JUnit + Compose UI tests; iOS: XCTest for mobile apps

**Integration Testing:**
- API endpoint tests with real DynamoDB (LocalStack or dev environment)
- Authentication flow tests with Cognito
- Notification delivery tests

**End-to-End Testing:**
- Critical user workflows (trail system creation, status update, care report submission)
- Mobile app flows (Google Play internal track / TestFlight manual testing)
- Cross-browser testing for web (Chrome, Safari, Firefox)

**Performance Testing:**
- API response time benchmarking
- Load testing (100+ concurrent users)
- Notification latency testing

### Documentation Requirements

**Required Documentation:**
- API documentation (auto-generated from OpenAPI spec)
- User documentation (how to use web app and mobile apps)
- Admin documentation (trail crew and org-admin guides)
- Developer documentation (setup, architecture, deployment)
- Pilot onboarding guides (step-by-step for Hydrocut and GORBA)

### Constitution Compliance

All code must comply with TrailLens Constitution standards:
- Python: CONSTITUTION-PYTHON.md (imports, type hints, docstrings, error handling)
- Shell: CONSTITUTION-SHELL.md (safety, error handling, quoting)
- JavaScript: CONSTITUTION-JAVASCRIPT.md (no var, React hooks, PropTypes)
- Copyright headers required in all source files
- No AI advertising or promotional content in commits

---

## Existing Codebase Assessment

### Overview

The TrailLensHQ codebase consists of an **exploratory prototype** across three main repositories. Approximately **60-70% of core infrastructure and features are implemented**, but significant work remains to reach MVP quality.

### api-dynamo/ (FastAPI Backend)

**Current State:**
- FastAPI application with ~60+ REST endpoints
- DynamoDB integration with boto3
- AWS Cognito authentication (JWT verification)
- Multi-tenant architecture with tenant isolation
- Role-based access control (8 Cognito groups)
- ~80% test coverage

**Needs Updates For MVP:**
- **Trail Systems Model**: Currently uses individual trails, needs refactor to trail systems (collections)
- **Trail Care Reports**: Net-new entity types and endpoints (REPORT#, COMMENT#, TYPE_TAG# entities in single-table design)
- **Tag-Based Status**: New condition tag entity type (CONDITION_TAG#) and tag assignment logic
- **Scheduled Status Changes**: New scheduled change entity type (SCHEDULED_CHANGE#) and cron job for automated processing
- **Three Authentication Methods**: Add passkey and magic link support (currently only email/password)
- **API Rate Limiting**: Enable and test throttling configuration
- **Data Retention**: Implement automated cleanup jobs for 2-year retention policies

**Estimated Work**: 20-30 days (AI-assisted)

### web/ (React Frontend — DEPRECATED)

**Current State:**
- React 18 with Tailwind CSS 3.4.13 — **DEPRECATED, replaced by webui/**
- Significant technical debt from Notus React starter template (custom pixel values, CommonJS config, prop-types, gulp build tools, type-based organization)
- Retained as reference only; all new development in webui/

**Estimated Work**: 0 days (no further development on web/)

### webui/ (React Frontend — ACTIVE)

**Current State:**
- Greenfield rewrite of web/ — React 19 + TypeScript strict mode + Vite 6.x + Tailwind CSS 4.x
- UI libraries: shadcn/ui (Radix primitives + Tailwind), Tremor (charts/dashboards), Lucide React (icons)
- State: Zustand 5.x (client state) + React Query 5.x (server state)
- Auth: AWS Amplify 6.x, amazon-cognito-identity-js, @github/webauthn-json (passkeys)
- Feature-based organization (auth/, admin/, organization/, user/, trails/, public/)
- 5-tier routing: Public, Auth, Admin, Organization, User
- 5 auth methods: Passwordless, Magic Link, Passkey, Social Login, Admin Login (hidden)
- All routes lazy-loaded with React.lazy() and Suspense boundaries
- Testing: Vitest 3.x + React Testing Library 16.x + Playwright 1.57

**Needs Updates For MVP:**
- **Trail Systems UI**: Complete trail system management pages (CRUD, status updates, history timeline)
- **Care Reports UI**: Create complete care report management interface (list, detail, create, edit, assign, comment)
- **Tag Management UI**: Create tag CRUD interfaces (condition tags and care report type tags)
- **Dashboard Updates**: Implement dashboards for all 8 roles with trail systems and care reports
- **Analytics**: Implement analytics dashboards with Tremor charts
- **Bulk Operations**: Implement bulk status update and bulk report management interfaces

**Estimated Work**: 15-25 days (AI-assisted)

### infra/ (Pulumi Infrastructure)

**Current State:**
- VPC, subnets, security groups configured
- AWS Cognito User Pool with 8 groups
- DynamoDB tables (7 tables currently in multi-table design per ADR-001; single-table design with 16 entity types is scale target)
- Lambda functions for API deployment
- API Gateway with custom domain
- S3 buckets for photos and deployments
- SNS topics for notifications
- SES for email delivery
- Infrastructure as Code (Pulumi + Python)

**Needs Updates For MVP:**

- **Security Hardening**: Enable CloudTrail (1-year retention), deploy AWS WAF (Security Hub and GuardDuty moved to post-MVP)
- **DynamoDB Entity Types**: Current 7-table design supports MVP entities. Single-table migration (16 entity types with ORG#, USER#, TRAILSYSTEM#, REPORT#, DEVICE#, PASSKEY# prefixes, 5 overloaded GSIs) deferred per ADR-001 until DynamoDB costs exceed $100/month or traffic reaches 10K DAU
- **Secrets Rotation**: Configure 180-day automatic rotation
- **Cognito Updates**: Configure MFA enforcement, passkey support (if available)
- **Lambda Cron Job**: Add scheduled status changes processor
- **Data Retention Jobs**: Add Lambda crons for 2-year retention cleanup

**Estimated Work**: 10-15 days (AI-assisted)

### Android Apps (ACTIVE — FIRST PRIORITY)

**Current State:**
- **Android User App** (com.traillens.app): In active development with Figma mockups
  - 36 screens defined in `androiduser/docs/MOBILEAPP_SCREENS.md`
  - Kotlin 2.0+, Jetpack Compose, Material Design 3, Hilt DI
  - Sections: Onboarding/Auth (9), Main Tab Bar (4), Trail Discovery (7), Care Reports (5), Notifications (2), Profile/Settings (5), Offline/Error (4), TrailPulse (2)
- **Android Admin App** (com.traillens.admin): In active development with Figma mockups
  - 42 screens defined in `androidadmin/docs/MOBILEAPP_SCREENS.md`
  - Same tech stack as User app, admin role validation gate
  - Sections: Onboarding/Auth (7), Main Tab Bar (5), Conditions Mgmt (6), TrailPulse (3), Care Reports Admin (6), Users/Team (5), Settings Admin (8), Notifications (2), Offline/Error (3)

**Required For MVP:**
- **Auth**: All five authentication methods (Passwordless, Magic Link, Passkey via Android Credential Manager, Social Login, Admin Login)
- **Push Notifications**: FCM via AWS SNS
- **Offline Mode**: Room database for offline caching and offline report queue (7-day TTL)
- **Distribution**: Google Play internal testing track
- **Performance**: Cold start <1.5s, 60fps scrolling, <15MB APK

**Estimated Work**: 30-45 days (AI-assisted, longest single phase)

### iOS Apps (PARALLEL TRACK)

**Current State:**
- **Do not exist** - will be created after Android apps reach beta

**Required For MVP:**
- **User App**: Swift/SwiftUI with same feature set as Android User App
- **Admin App**: Swift/SwiftUI with same feature set as Android Admin App
- **TestFlight**: Distribution channel for pilot organizations
- **Cognito Integration**: All authentication methods via AWS Amplify for Swift
- **Push Notifications**: APNS via SNS
- **Offline Mode**: Core Data for offline caching and offline report queue (7-day TTL)

**Estimated Work**: 20-30 days (AI-assisted, leveraging Android patterns and shared API)

---

## Phase 1: Brand Messaging Update

**Objective**: Update all public-facing content with new brand byline, messaging, and official brand assets

**Duration**: 2-3 days
**Priority**: HIGH (low-hanging fruit, can be done immediately)
**Dependencies**: None

**Reference Documentation**:
- **Detailed Implementation Guide**: `docs/WEBSITE_CONTENT_UPDATES_MVP.md` - Comprehensive brand asset specifications and implementation details
- **Authentication Implementation**: `docs/AUTH_REPORT.md` - Social authentication setup for Google/Facebook/Apple (Google only for MVP)

### Task 1.1: Update Website Homepage Byline

**Objective**: Change homepage hero section byline from "Connecting users to trail maintainers" to "Building communities, one trail at a time"

**Files to Modify**:
- `webui/src/features/public/pages/Landing.tsx` (line ~143 or hero section)
- `webui/src/features/public/pages/Home.tsx` (if exists)

**Implementation Steps**:
1. Read Landing.jsx or Home.jsx to locate current byline
2. Replace old byline with new: "Building communities, one trail at a time."
3. Verify h1 tag styling is consistent
4. Update any supporting hero copy to align with community-building theme
5. Run tests to ensure no regressions
6. Visual QA in browser (localhost:3000)

**Testing**:
- Unit tests pass for Landing component
- Manual visual inspection of homepage
- Mobile responsive check

**Acceptance Criteria**:
- New byline "Building communities, one trail at a time" visible on homepage
- No broken styling or layout issues
- Tests pass

**AI-Assisted Timeline**: 1 hour

---

### Task 1.2: Update Marketing Materials and Documentation

**Objective**: Ensure all documentation references the new brand messaging

**Files to Modify**:
- `docs/PRODUCT_OVERVIEW_FOR_CEO.md` (already updated)
- `docs/MARKETING_PLAN.md` (already updated with MVP requirement note)
- Any README files that mention the byline
- Email templates (if they exist in codebase)

**Implementation Steps**:
1. Search codebase for old byline text: "Connecting users to trail maintainers"
2. Replace all occurrences with new byline
3. Update any brand positioning language in docs
4. Verify consistency across all files

**Testing**:
- Grep search confirms no old byline remains
- Documentation review for consistency

**Acceptance Criteria**:
- All instances of old byline replaced
- Brand messaging consistent across all materials
- Documentation updated

**AI-Assisted Timeline**: 2 hours

---

### Task 1.3: Update Metadata and SEO

**Objective**: Update website metadata with new brand messaging

**Files to Modify**:
- `webui/index.html` (meta description tag)
- `webui/src/features/public/components/SEO.tsx` (if exists)
- Any OpenGraph/Twitter card metadata

**Implementation Steps**:
1. Update meta description to include new byline or community theme
2. Update og:description for social media sharing
3. Update twitter:description
4. Verify no other metadata needs updating

**Testing**:
- View page source to confirm meta tags updated
- Test social media card preview (Facebook/Twitter debugger tools)

**Acceptance Criteria**:
- Meta description updated
- Social media previews show new messaging
- SEO tags consistent

**AI-Assisted Timeline**: 1 hour

---

### Task 1.4: Create Brand Messaging Guidelines Document

**Objective**: Document brand voice and messaging for future content creation

**Files to Create**:
- `docs/BRAND_MESSAGING_GUIDELINES.md` (optional but recommended)

**Content to Include**:
- Official byline: "Building communities, one trail at a time"
- Brand voice: Friendly, accessible, outdoor-enthusiast (not corporate)
- Key messaging themes: community, stewardship, empowerment
- Tone guidelines for user-facing copy
- Examples of good vs. bad messaging

**Acceptance Criteria**:
- Guidelines document created and clear
- Team can reference for future content

**AI-Assisted Timeline**: 2 hours (optional)

---

### Task 1.5: Update App Store and Play Store Badges with Official Branding

**Objective**: Replace placeholder app store buttons with official Apple App Store and Google Play Store badges that comply with brand guidelines

**Reference Documentation**: `docs/WEBSITE_CONTENT_UPDATES_MVP.md` - Section 8.9 "Official App Store and Play Store Badges"

**Background**: The website currently references app store buttons in the landing page but does not use official branded badges from Apple and Google. Each provider has strict branding requirements that must be followed to comply with their terms of service and pass app review.

**Files to Modify**:
- `webui/src/features/public/pages/Landing.tsx` (or wherever app download CTAs are shown)
- `webui/index.html` (if app badges are in static HTML)

**Assets to Download and Add**:

**Apple App Store Badge**:
- Download from: [Apple App Store Marketing Tools](https://tools.applemediaservices.com/app-store/)
- Badge Type: "Download on the App Store" (black badge preferred)
- Formats: SVG (primary), PNG (fallback)
- Save to: `webui/src/assets/badges/Download_on_App_Store_Badge_US-UK_RGB_blk_092917.svg`
- Minimum height: 40px (screen), 10mm (print)
- Clear space: 1/4 badge height on all sides

**Google Play Store Badge**:
- Download from: [Google Play Badges Tool](https://play.google.com/intl/en_us/badges/)
- Badge Type: "Get it on Google Play" (standard badge)
- Formats: SVG (primary), PNG (fallback)
- Save to: `webui/src/assets/badges/google-play-badge.svg`
- Size: Same height or larger than Apple badge when displayed together
- Clear space: 1/4 badge height on all sides

**Implementation Steps**:
1. Download official badge assets from Apple and Google (see Section 8.9 Download Checklist)
2. Create `webui/src/assets/badges/` directory if it doesn't exist
3. Save SVG and PNG versions for both badges
4. Update landing page component to use official badges with proper markup:
   - Use semantic `<a>` links with `target="_blank"` and `rel="noopener noreferrer"`
   - Add proper `alt` text and `aria-label` for accessibility
   - Implement hover effects (scale-105 transition)
   - Use Tailwind classes for consistent sizing: `h-14 w-auto` (56px height)
   - Add `loading="lazy"` for performance
5. Implement conditional rendering for Android app availability (set to false for MVP, true post-MVP)
6. Ensure both badges have identical height when displayed together
7. Add proper spacing (gap-4 between badges)
8. Add legal credit lines in footer or about page:
   - Apple: "Apple and the Apple logo are trademarks of Apple Inc."
   - Google: "Google Play and the Google Play logo are trademarks of Google LLC."

**Example Implementation (from Section 8.9)**:
```jsx
const ANDROID_APP_AVAILABLE = false; // Set to true when Android app launches

<div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center items-center">
  {/* iOS App Store Badge - Always show */}
  <a
    href="https://apps.apple.com/app/traillenshq/id[YOUR_APP_ID]"
    target="_blank"
    rel="noopener noreferrer"
    className="inline-block transition-transform hover:scale-105"
    aria-label="Download TrailLensHQ on the App Store"
  >
    <img
      src="/assets/badges/Download_on_App_Store_Badge_US-UK_RGB_blk_092917.svg"
      alt="Download on the App Store"
      className="h-14 w-auto"
      style={{ minHeight: '40px' }}
      loading="lazy"
    />
  </a>

  {/* Google Play Badge - Conditional (post-MVP) */}
  {ANDROID_APP_AVAILABLE && (
    <a
      href="https://play.google.com/store/apps/details?id=com.traillenshq"
      target="_blank"
      rel="noopener noreferrer"
      className="inline-block transition-transform hover:scale-105"
      aria-label="Get TrailLensHQ on Google Play"
    >
      <img
        src="/assets/badges/google-play-badge.svg"
        alt="Get it on Google Play"
        className="h-14 w-auto"
        style={{ minHeight: '40px' }}
        loading="lazy"
      />
    </a>
  )}
</div>
```

**Testing**:
- Visual verification: Both badges render correctly with proper sizing and spacing
- Accessibility: Screen reader announces badge purpose correctly
- Responsive: Badges stack vertically on mobile, side-by-side on desktop
- Links: Verify URLs point to correct app store pages (update with actual app IDs before production)
- Brand compliance: Compare against official guidelines (see Section 8.9)
- Performance: Verify lazy loading works, no layout shift

**Acceptance Criteria**:
- Official badge assets downloaded and stored in `webui/src/assets/badges/`
- Landing page displays Apple App Store badge with proper branding
- Google Play badge conditionally rendered (hidden for MVP, shown post-MVP)
- Both badges are identical height (56px / h-14)
- Proper accessibility attributes present (alt text, aria-label)
- Hover effects work smoothly
- Mobile responsive behavior correct (stack vertically)
- Legal credit lines added to footer or about page
- All brand guideline requirements met (minimum size, clear space, aspect ratio)

**AI-Assisted Timeline**: 3-4 hours

**Notes**:
- Apple App Store badge MUST be displayed (iOS app is part of MVP)
- Google Play badge should be conditionally rendered but hidden for MVP (no Android app yet)
- DO NOT modify, recolor, or alter official badges - use as-is per brand guidelines
- Replace `[YOUR_APP_ID]` placeholder with actual App Store ID before production
- Android package ID `com.traillenshq` is a placeholder - confirm actual package name

---

### Task 1.6: Update Social Sign-In Buttons with Official Provider Branding

**Objective**: Replace generic FontAwesome icons on login page with official branded buttons that comply with Google, Facebook, and Apple branding requirements

**Reference Documentation**: `docs/WEBSITE_CONTENT_UPDATES_MVP.md` - Section 8.10 "Login Page Social Sign-In Buttons"

**Background**: The current login page (`webui/src/features/auth/pages/Login.tsx`, lines 116-144) uses generic FontAwesome icons for social sign-in buttons. This does NOT comply with official branding guidelines from Google, Facebook, and Apple, and may cause app review failures or violate terms of service.

**Current Implementation Issues**:
1. Uses `<i className="fab fa-google">` instead of official Google "G" logo
2. Button text says "Google" instead of required "Sign in with Google"
3. Uses generic button styling instead of brand-specific colors and fonts
4. Does not follow Apple's "Sign in with Apple" Human Interface Guidelines
5. Does not follow Facebook's Platform Policy 8.3 for Login buttons
6. Does not use required typography (Roboto for Google, San Francisco for Apple)

**Files to Modify**:
- `webui/src/features/auth/pages/Login.tsx` (lines 115-145 - replace social button section)
- `webui/src/features/auth/pages/Register.tsx` (if social buttons exist there - same updates)
- `webui/index.html` or `webui/src/index.css` (add Roboto font import)

**Assets to Download and Add**:

**Google Sign-In Assets**:
- Download from: [Google Identity Branding Guidelines](https://developers.google.com/identity/branding-guidelines)
- Asset: `signin-assets.zip` containing official Google "G" logo
- Save to: `webui/src/assets/auth/google-g-logo.svg`
- Required text: "Sign in with Google" (NOT just "Google")
- Font: Roboto Medium, 14px
- Colors: Light theme - white fill, gray stroke; Dark theme - dark fill

**Facebook Login Assets**:
- Download from: [Facebook Brand Resource Center](https://en.facebookbrand.com/facebookapp/)
- Asset: Facebook logo pack with white 'f' logo
- Save to: `webui/src/assets/auth/facebook-f-logo-white.svg`
- Required text: "Continue with Facebook" or "Login with Facebook"
- Background color: #1877F2 (Facebook Blue)
- Text color: White (#FFFFFF)

**Apple Sign In Assets**:
- Download from: [Apple HIG Sign in with Apple](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple)
- Asset: Official Apple logo in SVG format
- Save to: `webui/src/assets/auth/apple-logo-white.svg` and `apple-logo-black.svg`
- Required text: "Sign in with Apple" (NOT just "Apple")
- Styles: Black background with white logo, OR white background with black logo
- Font: San Francisco (system font fallback: `-apple-system, BlinkMacSystemFont`)

**Font Requirements**:
Add Roboto font for Google Sign-In button. Add to `webui/index.html`:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@500&display=swap" rel="stylesheet">
```

Or add to `webui/src/index.css`:
```css
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@500&display=swap');
```

**Implementation Steps**:
1. Download all official logo assets (see Section 8.10 Asset Download Checklist)
2. Create `webui/src/assets/auth/` directory if it doesn't exist
3. Save all logo SVG files to assets directory
4. Add Roboto font import to HTML head or CSS
5. **REPLACE lines 115-145 in Login.js** with new implementation (see code below)
6. **REMOVE lines 98-101** (isAppleDevice function) - show Apple button on all platforms
7. Update Register.js with same changes if social buttons exist there
8. Change button layout from inline to stacked full-width for better mobile UX
9. Add proper accessibility attributes (aria-label, aria-hidden on images)
10. Use brand-specific colors and typography
11. Test on all three providers (Google for MVP, Facebook/Apple post-MVP)

**Complete Replacement Code for Login.js (Lines 115-145)**:

**BEFORE (Current - Lines 115-145)**:
```jsx
<div className="btn-wrapper text-center">
  <button className="bg-white ... " onClick={() => handleSocialSignIn('Google')}>
    <i className="fab fa-google text-lg mr-1"></i>
    Google
  </button>
  {/* Similar for Facebook and Apple with FontAwesome icons */}
</div>
```

**AFTER (New - Replace Lines 115-145)**:
```jsx
<div className="btn-wrapper text-center space-y-3">
  {/* Google Sign-In Button */}
  <button
    className="w-full bg-white border border-gray-300 text-gray-700 px-4 py-3 rounded-lg shadow hover:shadow-md inline-flex items-center justify-center font-medium text-sm ease-linear transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed"
    type="button"
    onClick={() => handleSocialSignIn('Google')}
    disabled={isSubmitting || loading}
    aria-label="Sign in with Google"
  >
    <img
      src="/assets/auth/google-g-logo.svg"
      alt=""
      className="w-5 h-5 mr-3"
      aria-hidden="true"
    />
    <span className="font-medium" style={{ fontFamily: 'Roboto, sans-serif' }}>
      Sign in with Google
    </span>
  </button>

  {/* Facebook Login Button */}
  <button
    className="w-full text-white px-4 py-3 rounded-lg shadow hover:shadow-md inline-flex items-center justify-center font-medium text-sm ease-linear transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed"
    style={{ backgroundColor: '#1877F2' }}
    type="button"
    onClick={() => handleSocialSignIn('Facebook')}
    disabled={isSubmitting || loading}
    aria-label="Continue with Facebook"
  >
    <img
      src="/assets/auth/facebook-f-logo-white.svg"
      alt=""
      className="w-5 h-5 mr-3"
      aria-hidden="true"
    />
    <span className="font-medium">
      Continue with Facebook
    </span>
  </button>

  {/* Apple Sign In Button - Show on all platforms (removed device detection) */}
  <button
    className="w-full bg-black text-white px-4 py-3 rounded-lg shadow hover:shadow-md inline-flex items-center justify-center font-medium text-sm ease-linear transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed"
    type="button"
    onClick={() => handleSocialSignIn('Apple')}
    disabled={isSubmitting || loading}
    aria-label="Sign in with Apple"
  >
    <img
      src="/assets/auth/apple-logo-white.svg"
      alt=""
      className="w-5 h-5 mr-3"
      aria-hidden="true"
    />
    <span className="font-medium" style={{ fontFamily: '-apple-system, BlinkMacSystemFont, sans-serif' }}>
      Sign in with Apple
    </span>
  </button>
</div>
```

**Key Changes**:
1. **Full-width buttons**: Changed from inline (`mr-2 mb-1`) to stacked (`w-full`, `space-y-3`)
2. **Official logos**: Replaced FontAwesome icons with official brand SVG assets
3. **Proper branding**:
   - Google: "Sign in with Google" with Roboto font
   - Facebook: "Continue with Facebook" with #1877F2 background
   - Apple: "Sign in with Apple" with black background, system font
4. **Accessibility**: Added `aria-label` on buttons, `aria-hidden="true"` on decorative images
5. **Consistency**: All buttons same height and padding for visual harmony
6. **Removed device detection**: Apple button now shows on all platforms (not just Apple devices)
7. **Typography**: Uses brand-specific fonts (Roboto for Google, San Francisco for Apple)

**Also Remove (Lines 98-101)**:
```jsx
// DELETE THIS FUNCTION - No longer needed
const isAppleDevice = () => {
  const ua = navigator.userAgent;
  return /iPhone|iPad|iPod|Macintosh|Mac OS X/i.test(ua);
};
```

**Testing**:
- Visual verification: All three buttons display with official logos and correct colors
- Brand compliance: Compare against official guidelines (Section 8.10)
  - Google: White background, gray border, colored "G" logo, Roboto font
  - Facebook: #1877F2 background, white text and logo
  - Apple: Black background, white logo and text
- Accessibility: Screen reader announces button purpose correctly
- Responsive: Buttons stack vertically and are full-width on all screen sizes
- Disabled state: Buttons show reduced opacity and cursor changes when disabled
- Font rendering: Verify Roboto loads for Google button
- Functionality: Click each button and verify `handleSocialSignIn()` is called
- Cross-browser: Test on Chrome, Safari, Firefox, Edge
- Mobile devices: Test on actual iOS and Android devices

**Acceptance Criteria**:
- Official logo assets downloaded and stored in `webui/src/assets/auth/`
- Roboto font added to project (via HTML link or CSS import)
- Login.js lines 115-145 replaced with new implementation
- isAppleDevice() function removed (lines 98-101)
- All three buttons use official branding:
  - Google: "Sign in with Google" with official "G" logo
  - Facebook: "Continue with Facebook" with official 'f' logo, #1877F2 background
  - Apple: "Sign in with Apple" with official Apple logo, black background
- Buttons are full-width and stacked vertically
- All buttons have consistent height and spacing
- Accessibility attributes present (aria-label, aria-hidden)
- Disabled state styling works correctly
- Brand fonts render correctly (Roboto for Google, system font for Apple)
- No brand guideline violations
- All tests pass (Login.test.js)

**AI-Assisted Timeline**: 4-5 hours

**Notes**:
- DO NOT modify or recolor official logos - use as-is per brand guidelines
- The buttons are UI-only for now - actual OAuth functionality configured in Task 1.7
- All three providers will be visually displayed but only Google will function for MVP
- Facebook and Apple authentication will be enabled post-MVP
- Consider adding a visual indicator or tooltip for non-functional buttons during MVP

---

### Task 1.7: Enable Google Social Authentication (MVP Only)

**Objective**: Configure AWS Cognito User Pool to enable Google Sign-In authentication for MVP users (Facebook and Apple post-MVP)

**Reference Documentation**: `docs/AUTH_REPORT.md` - Complete social authentication implementation guide

**Background**: The login page has Google, Facebook, and Apple sign-in buttons (updated in Task 1.6), but they are currently non-functional because AWS Cognito is only configured with `supported_identity_providers=["COGNITO"]`. For MVP, we will ONLY enable Google Sign-In. Facebook and Apple will remain as UI-only buttons and be enabled post-MVP.

**Why Google First**:
- Simplest implementation (2-4 hours)
- Highest user adoption rate
- Free to implement (no developer program fees)
- Low risk
- Strong step toward passwordless authentication

**Why Facebook and Apple are Post-MVP**:
- Facebook: Medium complexity, API versioning risks, same cost (free)
- Apple: High complexity, requires Apple Developer Program ($99 USD/year), App Store dependency
- Focus MVP scope on core functionality with one working social provider

**Files to Modify**:
- `infra/pulumi/components/auth.py` (Cognito User Pool Client configuration)
- `infra/pulumi/components/cognito_identity_provider.py` (new file - Google identity provider)
- Environment configuration files (add Google OAuth credentials)

**Prerequisites**:
1. **Google Cloud Console Setup** (2-3 hours):
   - Create Google Cloud project (or use existing)
   - Enable Google+ API
   - Create OAuth 2.0 credentials (Web application type)
   - Configure authorized redirect URIs:
     - `https://auth.dev.traillenshq.com/oauth2/idpresponse` (dev)
     - `https://auth.traillenshq.com/oauth2/idpresponse` (prod - future)
   - Obtain Client ID and Client Secret
   - Configure OAuth consent screen with app name, logo, privacy policy, terms of service
   - Add test users for development/testing

**Implementation Steps**:

**Step 1: Create Google OAuth 2.0 Application**:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing: "TrailLensHQ"
3. Navigate to "APIs & Services" > "Credentials"
4. Click "Create Credentials" > "OAuth client ID"
5. Application type: "Web application"
6. Name: "TrailLensHQ Web Application"
7. Authorized JavaScript origins:
   - `https://traillenshq.com`
   - `https://auth.dev.traillenshq.com`
8. Authorized redirect URIs:
   - `https://auth.dev.traillenshq.com/oauth2/idpresponse`
   - `https://auth.traillenshq.com/oauth2/idpresponse` (future prod)
9. Click "Create" and save Client ID and Client Secret
10. Configure OAuth consent screen:
    - App name: "TrailLensHQ"
    - User support email: support@traillenshq.com
    - App logo: Upload TrailLens logo (120x120px minimum)
    - App domain: traillenshq.com
    - Privacy policy: https://traillenshq.com/privacy
    - Terms of service: https://traillenshq.com/terms
11. Add scopes: `email`, `profile`, `openid`
12. Add test users for development

**Step 2: Store Google OAuth Credentials in AWS Secrets Manager**:
```bash
# Create secret for Google OAuth credentials
aws secretsmanager create-secret \
  --name traillens/dev/google-oauth \
  --description "Google OAuth credentials for Cognito" \
  --secret-string '{"client_id":"YOUR_GOOGLE_CLIENT_ID","client_secret":"YOUR_GOOGLE_CLIENT_SECRET"}' \
  --region ca-central-1
```

**Step 3: Update Cognito Infrastructure (auth.py)**:

Create new file `infra/pulumi/components/cognito_google_provider.py`:
```python
"""Google identity provider for AWS Cognito."""
import pulumi
import pulumi_aws as aws
from pulumi import Output, ResourceOptions

class CognitoGoogleProvider(pulumi.ComponentResource):
    """Configure Google as identity provider for Cognito."""

    def __init__(self, name: str, user_pool_id: Output[str], opts: ResourceOptions = None):
        super().__init__("traillens:auth:CognitoGoogleProvider", name, None, opts)

        # Retrieve Google OAuth credentials from Secrets Manager
        google_secret = aws.secretsmanager.get_secret_version(
            secret_id="traillens/dev/google-oauth"
        )

        # Parse secret JSON
        google_creds = Output.secret(google_secret.secret_string).apply(lambda s: json.loads(s))

        # Create Google identity provider
        self.google_provider = aws.cognito.IdentityProvider(
            f"{name}-google",
            user_pool_id=user_pool_id,
            provider_name="Google",
            provider_type="Google",
            provider_details={
                "client_id": google_creds.apply(lambda c: c["client_id"]),
                "client_secret": google_creds.apply(lambda c: c["client_secret"]),
                "authorize_scopes": "email openid profile",
            },
            attribute_mapping={
                "email": "email",
                "username": "sub",  # Google's unique user ID
                "name": "name",
                "picture": "picture",
            },
            opts=ResourceOptions(parent=self),
        )

        self.register_outputs({
            "provider_name": self.google_provider.provider_name,
        })
```

Update `infra/pulumi/components/auth.py` (around line 152):
```python
# BEFORE:
supported_identity_providers=["COGNITO"],

# AFTER:
supported_identity_providers=["COGNITO", "Google"],
```

Update `infra/pulumi/__main__.py` or `index.ts`:
```python
from components.cognito_google_provider import CognitoGoogleProvider

# After creating auth component:
google_provider = CognitoGoogleProvider(
    "traillens-google-auth",
    user_pool_id=auth.user_pool.id,
)
```

**Step 4: Deploy Infrastructure Changes**:
```bash
cd infra/pulumi
pulumi up --stack dev
# Review changes, confirm deployment
```

**Step 5: Update Frontend Environment Variables** (if needed):
Verify `web/.env.production` has correct Cognito domain:
```bash
REACT_APP_COGNITO_DOMAIN=auth.dev.traillenshq.com
```

**Step 6: Test Google Sign-In Flow**:
1. Navigate to https://traillenshq.com/auth/login (or localhost:3000/auth/login for dev)
2. Click "Sign in with Google" button
3. Should redirect to Google OAuth consent screen
4. Sign in with Google test account
5. Grant permissions (email, profile, openid)
6. Should redirect back to TrailLens app, logged in
7. Verify user created in Cognito User Pool with Google sub as username
8. Verify email and profile attributes populated from Google

**Testing Checklist**:
- [ ] Google OAuth app created in Google Cloud Console
- [ ] OAuth credentials stored in AWS Secrets Manager
- [ ] Cognito Google identity provider created successfully
- [ ] User Pool Client updated with "Google" in supported providers
- [ ] Infrastructure deployment successful (pulumi up)
- [ ] Click "Sign in with Google" redirects to Google OAuth
- [ ] Google sign-in completes successfully
- [ ] User redirected back to TrailLens app
- [ ] User authenticated and session created
- [ ] Cognito User Pool shows new user with Google identity
- [ ] User attributes (email, name, picture) populated from Google
- [ ] Sign-out and re-sign-in works correctly
- [ ] Error handling works (user denies permissions, network failure)
- [ ] Privacy policy and terms of service links work on OAuth consent screen

**Acceptance Criteria**:
- Google OAuth 2.0 application created and configured in Google Cloud Console
- OAuth credentials securely stored in AWS Secrets Manager
- Cognito User Pool configured with Google identity provider
- `supported_identity_providers` includes both "COGNITO" and "Google"
- Attribute mapping configured (email, username, name, picture)
- Infrastructure deployed to dev environment successfully
- Google Sign-In button functional on login page
- Users can successfully authenticate via Google
- User data correctly synced from Google to Cognito
- Error handling works for failed authentication attempts
- Documentation updated with Google OAuth setup instructions
- **Facebook and Apple buttons remain visible but non-functional** (to be enabled post-MVP)

**AI-Assisted Timeline**: 3-4 hours (after Google Cloud Console setup)

**Post-MVP Tasks** (NOT included in MVP):
- Task 1.7.1: Enable Facebook Login (3-5 hours) - See AUTH_REPORT.md Section 4.2
- Task 1.7.2: Enable Apple Sign In (4-8 hours, requires Apple Developer Program $99/year) - See AUTH_REPORT.md Section 4.3
- Task 1.7.3: Configure attribute mapping for Facebook and Apple
- Task 1.7.4: Test all three providers end-to-end

**Security Considerations**:
- Store OAuth credentials in AWS Secrets Manager (NEVER in code or environment files)
- Use HTTPS for all redirect URIs (required by Google)
- Implement CSRF protection (handled by Cognito automatically)
- Configure OAuth consent screen with privacy policy and terms of service
- Limit OAuth scopes to minimum required (email, profile, openid)
- Set up monitoring for failed authentication attempts
- Document OAuth credential rotation process (manual for now, automate post-MVP)

**Cost Impact**: Free (Google OAuth is free, no additional AWS costs)

**Notes**:
- Google OAuth credentials are sensitive - store in Secrets Manager, never commit to code
- OAuth consent screen requires privacy policy and terms of service URLs
- Test users can be added in Google Cloud Console for development
- Production OAuth consent screen requires Google verification process (can take 1-2 weeks)
- For MVP, use "Testing" mode in OAuth consent screen (allows up to 100 test users)
- Move to "Production" mode post-MVP after verification complete

---

**Phase 1 Total Duration**: 2-3 days
**Phase 1 Success Criteria**:
- Website homepage displays new byline
- All documentation updated
- No references to old byline remain
- Brand messaging consistent and documented
- **Official App Store and Play Store badges displayed with proper branding** (NEW)
- **Social sign-in buttons updated with official provider logos and text** (NEW)
- **Google Sign-In authentication functional for MVP users** (NEW)
- **Facebook and Apple buttons displayed but non-functional** (post-MVP)

---

## Phase 2: Security Hardening

**Objective**: Address 5 critical security gaps to make platform production-ready for MVP

**Duration**: 3-5 days
**Priority**: CRITICAL (must complete before handling production data)
**Dependencies**: None (can start immediately)

**5 Critical Gaps to Address (MVP)**:

1. Enable CloudTrail with 1-year retention
2. Deploy AWS WAF for API Gateway
3. Implement secrets rotation (180-day cycle)
4. Create incident response plan
5. Enable API rate limiting
6. Implement MFA enforcement for admin roles

**Moved to Post-MVP** (due to cost considerations):

- Security Hub (~$50/month ongoing cost)
- GuardDuty (~$4.40/month ongoing cost)

---

### Task 2.1: Enable AWS CloudTrail with 1-Year Retention

**Objective**: Enable audit logging for all AWS API calls to detect and investigate security incidents

**Files to Modify**:
- `infra/components/monitoring.py` (new file or existing monitoring module)
- `infra/index.ts` or `infra/__main__.py` (import CloudTrail stack)
- `infra/components/s3.ts` or `s3.py` (CloudTrail logs bucket)

**Implementation Steps**:
1. Create S3 bucket for CloudTrail logs with versioning and encryption
2. Configure bucket lifecycle policy for 1-year retention (365 days)
3. Enable CloudTrail trail with multi-region support
4. Enable log file validation (integrity checking)
5. Configure CloudTrail to log all management events and data events (DynamoDB, S3)
6. Set up SNS topic for CloudTrail log delivery notifications (optional)
7. Deploy to dev environment first, then prod
8. Verify logs are being delivered to S3

**Cost Impact**: $2-5/month for log storage and API calls

**Testing**:
- Perform test API call (e.g., create DynamoDB item)
- Verify CloudTrail log shows the event within 15 minutes
- Confirm S3 bucket contains log files
- Verify log file validation works

**Acceptance Criteria**:
- CloudTrail enabled in all regions
- 1-year retention policy configured
- Log file validation enabled
- Logs successfully delivered to S3
- No errors in CloudTrail console

**AI-Assisted Timeline**: 4 hours

---

### Task 2.2: Deploy AWS WAF for API Gateway

**Objective**: Protect API Gateway from OWASP Top 10 exploits and common web attacks

**Files to Modify**:
- `infra/components/waf.py` (new file)
- `infra/components/api_gateway.py` (associate WAF with API Gateway)
- `infra/index.ts` or `__main__.py` (import WAF stack)

**Implementation Steps**:
1. Create WAF Web ACL with AWS managed rule sets:
   - AWSManagedRulesCommonRuleSet (OWASP Top 10)
   - AWSManagedRulesKnownBadInputsRuleSet (malicious patterns)
   - AWSManagedRulesAmazonIpReputationList (known bad IPs)
   - AWSManagedRulesSQLiRuleSet (SQL injection)
   - AWSManagedRulesLinuxRuleSet (Linux-specific exploits)
2. Configure rate limiting rule (100 requests/5 minutes per IP)
3. Associate WAF with API Gateway regional endpoint
4. Set up CloudWatch metrics for WAF (blocked requests, allowed requests)
5. Deploy to dev environment first, test thoroughly, then prod
6. Monitor WAF logs for false positives

**Cost Impact**: $5-20/month ($5 base + $1/rule + $0.60/million requests)

**Testing**:
- Perform normal API request (should be allowed)
- Attempt SQL injection in query parameter (should be blocked)
- Attempt excessive requests from single IP (should be rate limited)
- Review WAF logs in CloudWatch

**Acceptance Criteria**:
- WAF associated with API Gateway
- Managed rule sets active
- Rate limiting functional
- Legitimate traffic not blocked
- Attack traffic successfully blocked

**AI-Assisted Timeline**: 6 hours

---

### Task 2.3: Implement Secrets Rotation (180-Day Cycle)

**Objective**: Configure automatic rotation for all secrets to minimize exposure window

**Files to Modify**:
- `infra/components/secrets.py` (configure rotation)
- Lambda function for rotation handler (if needed for custom secrets)

**Secrets to Rotate**:
- JWT signing keys (if stored in Secrets Manager)
- Facebook API tokens (post-MVP, but set up rotation infrastructure)
- Database credentials (if any)
- API keys for third-party services

**Implementation Steps**:
1. Review current secrets in AWS Secrets Manager
2. Configure 180-day automatic rotation for applicable secrets
3. Create Lambda rotation function (if not using AWS-managed rotation)
4. Test rotation manually (trigger rotation, verify new secret works)
5. Set up CloudWatch alarms for rotation failures
6. Document rotation process in runbook

**Testing**:
- Manually trigger secret rotation
- Verify application continues to work with new secret
- Confirm old secret is invalidated
- Check CloudWatch logs for rotation events

**Acceptance Criteria**:
- All secrets have 180-day rotation configured
- Rotation tested and successful
- Alarms configured for failures
- Documentation updated

**AI-Assisted Timeline**: 4 hours

---

### Task 2.4: Create Incident Response Plan

**Objective**: Document formal process for responding to security incidents, especially GDPR 72-hour breach notification

**Files to Create**:
- `docs/INCIDENT_RESPONSE_PLAN.md` (new file)

**Content to Include**:
1. **Incident Classification** (P1-P5 severity levels)
2. **Notification Timeline** (GDPR requires 72-hour notification for breaches)
3. **Response Team** (roles and responsibilities)
4. **Escalation Procedures** (when to notify CEO, when to notify customers)
5. **Communication Templates** (breach notification email, public statement)
6. **Forensics Procedures** (how to investigate using CloudTrail logs)
7. **Containment Steps** (disable compromised accounts, rotate secrets, etc.)
8. **Recovery Procedures** (restore from backups, verify system integrity)
9. **Post-Incident Review** (lessons learned, process improvements)

**GDPR 72-Hour Breach Notification Requirements**:
- Notify supervisory authority within 72 hours of becoming aware
- Notify affected data subjects "without undue delay" if high risk
- Document all breaches (even if not reported)

**Acceptance Criteria**:
- Comprehensive incident response plan documented
- GDPR 72-hour notification process clear
- Response team roles assigned
- Templates ready for use
- Plan reviewed by CEO and legal (if available)

**AI-Assisted Timeline**: 6 hours (AI can draft, human reviews)

---

### Task 2.5: Enable API Rate Limiting

**Objective**: Protect API from abuse and DDoS attacks by enforcing rate limits

**Files to Modify**:
- `infra/components/api_gateway.py` (enable throttling)
- API Gateway usage plans configuration

**Implementation Steps**:
1. Configure API Gateway throttling limits:
   - Rate limit: 100 requests/minute per user (JWT sub claim)
   - Burst limit: 200 requests
2. Create usage plans for different tiers (if needed)
3. Configure Lambda concurrency limits (1000 concurrent executions in dev)
4. Set up CloudWatch alarms for throttling events
5. Test rate limiting with load testing tool
6. Document rate limits in API documentation

**Testing**:
- Send 100 requests/minute from single user (should succeed)
- Send 101st request (should be throttled with 429 status)
- Verify different users have independent rate limits
- Check CloudWatch metrics for throttling

**Acceptance Criteria**:
- Rate limiting configured and active
- 100 req/min limit enforced per user
- Burst limit working
- Throttling returns 429 status with Retry-After header
- Documentation updated

**AI-Assisted Timeline**: 3 hours

---

### Task 2.6: Implement MFA Enforcement for Admin Roles

**Objective**: Require multi-factor authentication for org-admin, trailsystem-owner, and superadmin roles with 7-day grace period

**IMPORTANT CLARIFICATION**: This task applies to admin users who authenticate with **password-based login**. Admin users who authenticate with **passkeys DO NOT need traditional MFA** because passkeys are inherently multi-factor (something you have + something you are/know). Passkey authentication is more secure than password + SMS/TOTP.

**Files to Modify**:
- `infra/components/cognito.py` (Cognito MFA configuration)
- `api-dynamo/middleware/auth.py` (MFA enforcement logic - skip MFA check for passkey-authenticated users)
- `webui/src/features/auth/pages/Login.tsx` (MFA setup UI)

**Implementation Steps**:
1. Configure Cognito User Pool MFA settings:
   - MFA configuration: OPTIONAL (required setting for passkey compatibility - allows both passkey users and password+MFA users)
   - Allowed MFA methods: SMS and TOTP authenticator apps (for password-based logins)
2. Implement API middleware to check MFA status:
   - **CRITICAL**: Skip MFA check if user authenticated via passkey (passkeys are already MFA)
   - For password-based logins: On first admin login, set `mfa_grace_period_end = current_time + 7 days`
   - For password-based logins: On subsequent logins, if user is in admin group AND MFA not enabled AND grace period expired, force MFA setup
3. Create MFA setup flow in web UI:
   - QR code for TOTP setup
   - SMS verification option
   - Recovery codes generation
4. Update user documentation with MFA setup instructions
5. Test MFA flow end-to-end

**Grace Period Logic**:
- Admin users get 7 days from first login to set up MFA
- After 7 days, login is blocked until MFA is configured
- Grace period tracked in user attributes (custom:mfa_grace_period_end)

**Testing**:
- Create new org-admin user
- Login (grace period starts)
- Verify can access system for 7 days without MFA
- Wait for grace period to expire (or manually expire)
- Verify login is blocked with MFA setup prompt
- Complete MFA setup
- Verify login succeeds with MFA code

**Acceptance Criteria**:
- MFA enforcement active for admin roles
- 7-day grace period working
- MFA setup UI functional
- SMS and TOTP both supported
- Documentation updated

**AI-Assisted Timeline**: 8 hours

---

**Phase 2 Total Duration**: 3-5 days
**Phase 2 Success Criteria**:
- All 5 critical security gaps addressed
- CloudTrail and WAF enabled
- Secrets rotation configured
- Incident response plan documented
- API rate limiting and MFA enforcement active
- Security audit passes (excluding Security Hub/GuardDuty which are post-MVP)

---

## Phase 3: Authentication System

**Objective**: Implement three required authentication methods (passkey, magic link, email/password)

**Duration**: 7-10 days
**Priority**: CRITICAL (required for MVP)
**Dependencies**: Phase 2 complete (Cognito configured with MFA)

**Three Authentication Methods (ALL REQUIRED)**:

1. **Passkey Authentication**: WebAuthn/FIDO2 (Touch ID, Face ID, security keys) - **inherently multi-factor authentication**
2. **Magic Link**: Email-based passwordless login (15-minute expiration)
3. **Email/Password**: Traditional authentication (12+ char, complexity, 6-password history) - **requires MFA for admin roles**

---

### Task 3.1: Configure Cognito for Native Passkey Support ✅ COMPLETE

**Status: IMPLEMENTED** — Cognito Essentials tier with Native WebAuthn configured and deployed.

**Objective**: Enable AWS Cognito's native passkey (WebAuthn/FIDO2) authentication support launched November 2024

**Implementation Summary**:
- Cognito user pool upgraded to `ESSENTIALS` tier
- `web_authn_configuration`: `relying_party_id=traillenshq.com`, `user_verification=preferred`
- `sign_in_policy`: `allowed_first_auth_factors=["PASSWORD", "WEB_AUTHN"]`
- `mfa_configuration` changed from `ON` to `OPTIONAL` (WebAuthn is inherently MFA; admin MFA enforced at FastAPI middleware)
- `FactorConfiguration=MULTI_FACTOR_WITH_USER_VERIFICATION` set via `infra/scripts/set-cognito-mfa-config.py` boto3 script on every `pulumi up`

**Key References**:

- [AWS Cognito Passwordless Launch Announcement](https://aws.amazon.com/about-aws/whats-new/2024/11/amazon-cognito-passwordless-authentication-low-friction-secure-logins/)
- [Authentication Flows Documentation](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-authentication-flow-methods.html)
- [StartWebAuthnRegistration API](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_StartWebAuthnRegistration.html)
- [CompleteWebAuthnRegistration API](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CompleteWebAuthnRegistration.html)

**Files to Modify**:

- `infra/cognito.py` (User Pool configuration)
- `infra/cognito_app_client.py` (App Client configuration)

**Implementation Steps**:

**1. Update Cognito User Pool Configuration (Pulumi)**:

```python
# Enable passkey in sign-in policy
sign_in_policy = {
    "AllowedFirstAuthFactors": [
        "PASSWORD",
        "WEB_AUTHN",
        "EMAIL_OTP"  # Magic link
    ]
}

# Configure WebAuthn settings
web_authn_config = {
    "RelyingPartyId": "auth.dev.traillenshq.com",  # Cognito custom domain
    "UserVerification": "preferred"  # Allows authenticators without verification
}
```

**2. Update App Client Configuration**:

```python
# Enable USER_AUTH flow for passkey support
explicit_auth_flows = [
    "ALLOW_USER_AUTH",  # Required for passkey authentication
    "ALLOW_REFRESH_TOKEN_AUTH"
]
```

**3. Deploy Infrastructure**:

```bash
cd infra/
pulumi up --stack dev
```

**Critical Constraints (from AWS documentation)**:

- **IMPORTANT - Passkeys ARE Multi-Factor Authentication**: Passkeys combine "something you have" (device) + "something you are" (biometric) or "something you know" (PIN), making them inherently multi-factor. When using passkeys, you do NOT need additional MFA factors like SMS/TOTP.

- **AWS Cognito MFA Setting Constraint**: AWS Cognito's "MFA required" setting refers to ADDITIONAL factors beyond primary authentication (e.g., password + SMS code). According to AWS documentation: *"Passkey authentication isn't eligible for multi-factor authentication (MFA)"* and *"Passwordless authentication flows aren't compatible with required multi-factor authentication (MFA) in your user pool."* ([Source](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-authentication-flow-methods.html)). Therefore, when enabling passkeys, Cognito's MFA setting must be set to "optional" - but this does NOT mean authentication is single-factor. **The passkey itself provides multi-factor authentication.**

- **Security Clarification**: Setting Cognito MFA to "optional" for passkey users does NOT reduce security. Passkey authentication is more secure than password + SMS/TOTP MFA because passkeys are:
  - **Phishing-resistant** (cryptographic challenge-response cannot be intercepted)
  - **No shared secrets** (private key never leaves device)
  - **Biometric binding** (device security prevents credential theft)
  - **Immune to password attacks** (no password to steal or guess)

  Reference: [AWS Blog - Passkeys enhance security and usability](https://aws.amazon.com/blogs/security/passkeys-enhance-security-and-usability-as-aws-expands-mfa-requirements/)

- **User must sign in once before passkey registration**: Users must create account and sign in with password/magic link first, then register passkey.

- **Maximum 20 passkeys per user**

- **Supported algorithms**: ES256 (-7) and RS256 (-257)

- **Relying Party ID**: Must match Cognito custom domain. Changing RP ID requires all users to re-register passkeys.

- **Availability**: Only available with `ALLOW_USER_AUTH` flow, not available in Lite plan (we use Standard/Plus)

**Testing**:

- Verify User Pool has `WEB_AUTHN` in AllowedFirstAuthFactors
- Verify App Client has `ALLOW_USER_AUTH` in ExplicitAuthFlows
- Verify WebAuthnConfiguration has correct RelyingPartyId
- Verify MFA is OPTIONAL (Cognito implementation requirement for passkey support - passkeys themselves ARE multi-factor)

**Acceptance Criteria**:

- Cognito User Pool configured for passkey authentication
- App Client allows USER_AUTH flow
- WebAuthn configuration applied with correct Relying Party ID
- MFA configuration set to OPTIONAL (Cognito requirement - does NOT reduce security as passkeys are inherently MFA)
- Infrastructure deployment successful
- Documentation updated with passkey constraints and MFA clarification

**AI-Assisted Timeline**: 2-3 hours (configuration only, implementation in Tasks 3.2-3.4)

---

### Task 3.2: Implement Passkey Authentication (WebAuthn/FIDO2) ✅ ARCHITECTURE COMPLETE

**Status: BACKEND ARCHITECTURE COMPLETE** — Custom passkey backend removed; Cognito Native WebAuthn configured. Frontend client implementation deferred to separate PRs.

**Objective**: Enable biometric login using Touch ID, Face ID, or hardware security keys via Cognito Native WebAuthn.

**Architecture Decision (FINAL)**: All WebAuthn operations are **client-side only** via the Cognito SDK. There are **NO backend passkey proxy endpoints**. The 6 custom backend passkey endpoints previously planned (`/auth/passkey/register/start`, `/auth/passkey/register/complete`, `/auth/passkey/list`, `/auth/passkey/delete`, `/auth/login?auth_type=passkey`, `/auth/passkey/verify`) were implemented as a custom HS256 solution and have been **removed entirely** from the codebase. Cognito Native WebAuthn makes them unnecessary.

**Implemented (Backend/Infra)**:

- Cognito ESSENTIALS tier with `web_authn_configuration` and `sign_in_policy` (Task 3.1)
- Custom passkey/HS256 backend deleted: ~2,400 lines removed
- JWT verification is RS256-only via Cognito JWKS (no HS256 fallback)
- API Gateway simplified to `{proxy+}` catch-all (auth at FastAPI level only)

**Pending (Frontend — separate PRs)**:

**Registration flow (client-side Cognito SDK)**:
1. Call Cognito SDK `StartWebAuthnRegistration(AccessToken=access_token)`
2. Pass `CredentialCreationOptions` to `navigator.credentials.create()`
3. Call `CompleteWebAuthnRegistration(AccessToken=access_token, Credential=credential_data)`

**Authentication flow (client-side Cognito SDK)**:
1. Call `InitiateAuth` with `AuthFlow="USER_AUTH"`, `PREFERRED_CHALLENGE="WEB_AUTHN"`
2. Receive `WEB_AUTHN` challenge; call `navigator.credentials.get()`
3. Call `RespondToAuthChallenge` with assertion response
4. Receive RS256 IdToken/AccessToken/RefreshToken

**Credential management (client-side Cognito SDK)**:
- `ListWebAuthnCredentials(AccessToken=...)` — list registered passkeys
- `DeleteWebAuthnCredential(AccessToken=..., CredentialId=...)` — remove passkey

**Frontend files to create** (webui, androiduser — deferred):
- `webui/src/features/auth/components/PasskeySetup.tsx` (registration)
- `webui/src/features/auth/pages/Login.tsx` (add "Sign in with Passkey" button)
- `webui/src/features/user/pages/Settings.tsx` (passkey management)
- `androiduser/` — Credential Manager API integration with Cognito SDK

---

### Task 3.3: Implement Magic Link Authentication (Cognito Custom-Auth, NOT a REST route)

**Objective**: Enable email-based passwordless login with 10-minute expiration clickable links via Cognito Custom-Auth flow.

**ARCHITECTURE CORRECTION (docs-mvp-backend-features pass)**: The previously-claimed `POST /auth/magic-link/send` and `POST /auth/magic-link/verify` REST endpoints **do not exist** and **must not be added**. The "send" path is owned end-to-end by **Cognito Custom-Auth + the `cognito-triggers/create_auth_challenge.py` Lambda** (515 lines, verified). api-dynamo's only role in the magic-link flow is the single token-lookup endpoint.

**Verified end-to-end flow** (line citations refer to `api-dynamo/src/lambdas/cognito-triggers/src/cognito_triggers/create_auth_challenge.py`):

1. Client calls `Cognito.InitiateAuth(AuthFlow=CUSTOM_AUTH, AuthParameters={USERNAME: email})` directly via the Cognito SDK (no api-dynamo route).
2. Cognito invokes `create_auth_challenge.lambda_handler` (L426).
3. Lambda checks user existence (`_check_user_exists`, L117).
4. Silent-failure gate when `ALLOW_NEW_USERS=false` (L382).
5. Rate-limit check on GSI1 `EMAIL#{email_lc}` partition (`_is_rate_limited`, L138) — 60-second window.
6. Generate 256-bit URL-safe token (`_generate_token`, L112).
7. Send templated email via SES with `{FRONTEND_URL}/auth/verify-magic-link?token={token}` (`_send_magic_link_email`, L221).
8. Store token in DynamoDB single-table (`PK=MLT#{token}`, `SK=METADATA`, `GSI1PK=EMAIL#{email_lc}`, 10-minute TTL) (`_store_token`, L183).
9. User clicks email link → frontend extracts token → calls `POST /api/auth/magic-link/lookup-token` — **THIS is api-dynamo's only role: token → email lookup**.
10. Client then calls `Cognito.RespondToAuthChallenge(ANSWER=token)` → `verify_auth_challenge.py` checks → Cognito issues access + refresh + ID tokens.

**Files involved (verified)**:
- `api-dynamo/src/lambdas/cognito-triggers/src/cognito_triggers/create_auth_challenge.py` — owns the entire send path (rate-limit, token generation, SES dispatch, DynamoDB write).
- `api-dynamo/src/lambdas/cognito-triggers/src/cognito_triggers/verify_auth_challenge.py` — verifies the token and marks it used during `RespondToAuthChallenge`.
- `api-dynamo/src/lambdas/api_dynamo/src/api/routes/auth.py` — exposes **only** `POST /api/auth/magic-link/lookup-token` (frontend → email lookup); no `/send` and no `/verify`.

**Implementation Steps (this docs pass — no code changes)**:

1. Confirm `routes/auth.py` exposes `POST /api/auth/magic-link/lookup-token` and **only** that magic-link route.
2. Confirm openapi.json contains the lookup-token route and **does not** contain `/auth/magic-link/send` or `/auth/magic-link/verify`.
3. Cross-check `ACCESS_PATTERNS.md` AP-A08–AP-A10 use the actual `MLT#{token}` PK (not the stale `MAGIC_LINK#{token}`); add AP-A11 for the GSI1 `EMAIL#{email_lc}` rate-limit query.

**Acceptance Criteria**:
- No api-dynamo REST endpoint for `/send` or `/verify` (Cognito-direct).
- `POST /api/auth/magic-link/lookup-token` documented in openapi.json under tag `auth`.
- Token storage uses `PK=MLT#{token}`, 10-minute TTL.
- 60-second rate-limit per email enforced via GSI1.
- Sequence diagram added to `planning/docs/SYSTEM_ARCHITECTURE.md` (auth section) covering the 10 verified steps.

**AI-Assisted Timeline**: 0 hours additional code in this docs pass; audit + sequence-diagram drafting only.

---

### Task 3.4: Email/Password Authentication (Backup-Only via Cognito SRP, NO Signup, NO Forgot-Password)

**Objective**: Provide email + password as a **backup** authentication method alongside passkey and magic-link. Per docs-mvp-backend-features pass: NO account creation by password, NO forgot-password endpoint in api-dynamo.

**Wire protocol**: Cognito `USER_SRP_AUTH` (Secure Remote Password). Client talks **directly to Cognito** (same pattern as passkey and magic-link's challenge response). No api-dynamo route. Password never sent in plaintext to the network.

**Verified existing infra config (no infra change needed for these constraints)**:

- **`AllowAdminCreateUserOnly=True`** already set at `infra/pulumi/components/auth.py:230-231`. Self-signup via password is already blocked. New users onboard via magic-link or admin invite.
- **Password policy already configured** at `infra/pulumi/components/auth.py:218-224`: `minimum_length=12, require_lowercase=True, require_uppercase=True, require_numbers=True, require_symbols=True`. Matches MVP spec.

**Required infra changes (queued for implementation plan, NOT this docs pass)**:

1. **Upgrade Cognito `user_pool_tier`** from `ESSENTIALS` (`auth.py:202`) → **`PLUS`**. Threat Protection (formerly Advanced Security) is gated to PLUS.
2. **Add `user_pool_add_ons` block** to the `aws.cognito.UserPool(...)` constructor: `user_pool_add_ons=aws.cognito.UserPoolUserPoolAddOnsArgs(advanced_security_mode="AUDIT")` for the first 2 weeks; promote to `"ENFORCED"` after the soak window. Per [AWS Cognito Threat Protection docs](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-threat-protection.html).
3. **Configure adaptive-auth response policy**: low risk → allow; medium risk → require MFA; high risk → block.
4. **Caveat surfaced for implementation plan**: Threat Protection's compromised-credentials check **only runs on `USER_PASSWORD_AUTH`, NOT on `USER_SRP_AUTH`** (per AWS docs). The SRP choice forfeits the compromised-credentials check. Two viable resolutions for the implementation plan to pick: (i) keep SRP, accept the trade-off, rely on the 12-char + complexity policy; (ii) switch the password backup flow to `USER_PASSWORD_AUTH` (password traverses TLS in cleartext) to enable compromised-credentials checking.
5. **No rate-limiting from Threat Protection**. The earlier "Cognito has built-in lockout after 5 failed attempts" claim was inaccurate — that level of lockout is NOT a Threat Protection feature. AWS WAF rules on the Cognito endpoint or API Gateway are the correct path for volumetric / brute-force protection (queue WAF work for the implementation plan).

**Explicit non-goals (MVP)**:

- **NO account creation by password** — `allow_admin_create_user_only=True` enforces this; do not change.
- **NO forgot-password endpoint in api-dynamo** — Cognito's `ForgotPassword`/`ConfirmForgotPassword` API is **not** offered to clients in the MVP. Webui will add a UI for it later (see Phase 11 deferred task at end of phase). Admins reset via Cognito console or scripts.
- **NO `/auth/forgot-password` or `/auth/reset-password` REST routes**.

**Files involved (no code work in this docs pass)**:

- Existing webui SRP path: `webui/packages/jsrestapi/src/auth/AuthManager.ts` — public surface today is 9 methods; `signInWithSrp` is **NOT yet present** and must be added in the implementation plan.
- Existing Android SRP path: `androidrestapi/lib/src/main/kotlin/com/traillenshq/api/auth/CognitoAuthApi.kt` — SRP is reachable today via `initiateAuth(authFlow="USER_SRP_AUTH")`; no new method needed.

**Acceptance Criteria (docs-only this pass)**:

- Task body reflects backup-only SRP architecture.
- No `/auth/forgot-password` route is referenced anywhere in the MVP plan.
- Threat Protection enablement queued explicitly (PLUS tier + `advanced_security_mode`).
- SRP-vs-PASSWORD trade-off captured for the implementation plan to resolve.

**AI-Assisted Timeline**: 0 hours additional code in this docs pass.

---

### Task 3.5: Create Unified Login Experience

**Objective**: Design clean login page with all three authentication methods

**Files to Modify**:
- `webui/src/features/auth/pages/Login.tsx` (update with all three options)

**UI Design**:
```
+----------------------------------+
|       TrailLensHQ Logo           |
|                                  |
|   [ Sign in with Passkey ]       | <- Primary option (most secure)
|                                  |
|   --- OR ---                     |
|                                  |
|   [ Email me a magic link ]      | <- Secondary option (passwordless)
|                                  |
|   --- OR ---                     |
|                                  |
|   Email: [____________]          | <- Traditional option
|   Password: [____________]       |
|   [x] Remember me                |
|   [ Sign In ]                    |
|                                  |
|   Forgot password? | Sign up     |
+----------------------------------+
```

**Implementation Steps**:
1. Design clean, accessible login UI
2. Implement tabs or sections for each auth method
3. Add clear labels and instructions for each method
4. Ensure mobile responsive
5. Add loading states and error handling
6. Test all three methods work seamlessly

**Acceptance Criteria**:
- All three auth methods available on login page
- UI clean and intuitive
- Mobile responsive
- Loading states implemented
- Error handling graceful

**AI-Assisted Timeline**: 6 hours

---

### Task 3.6: Implement Mobile App Authentication (Production = Passkey + Magic-Link Only; Password = DEBUG Build Only)

**Objective**: Integrate authentication methods into mobile apps. **Production builds expose passkey + magic-link only.** Email/password login screens are **debug-build-only** behind a hidden trigger (per docs-mvp-backend-features pass).

**Production-build auth methods (Android user + admin apps)**:

1. **Passkey** (WebAuthn via Android Credential Manager API).
2. **Magic-link** (Cognito Custom-Auth via SDK; deep-link callback into the app).

**Debug-build-only auth method**:

3. **Email + password** (Cognito SRP via SDK). Gated by `BuildConfig.DEBUG`. Hidden entry point (exact UX TBD in implementation plan — candidates: tap-version-7x, long-press-logo, hidden menu item). Production users cannot reach this screen.

**Files involved (no code work in this docs pass)**:

- Existing Android SRP support via `androidrestapi/lib/src/main/kotlin/com/traillenshq/api/auth/CognitoAuthApi.kt` — `initiateAuth(authFlow="USER_SRP_AUTH")` already reachable.
- iOS deferred per project scope (no iOS work in MVP).

**Implementation Steps (queued for implementation plan, NOT this docs pass)**:

1. Wire passkey + magic-link login screens into the user app and admin app for **all** build types.
2. Wire password-login screen into both apps **only** under `BuildConfig.DEBUG`. Use Hilt module gating or compose conditional routes — exact pattern TBD.
3. Hide the password-login screen route + entry trigger when `BuildConfig.DEBUG == false`.
4. Add the new "Debug-Only Password Login" screen to both apps' MOBILEAPP_SCREENS.md (separate doc task).

**Testing**:

- Production build: confirm password login screen unreachable.
- Debug build: confirm password login screen reachable via the hidden trigger.
- Passkey + magic-link work in both build types.

**Acceptance Criteria**:

- Production APKs do not expose any password login UX.
- Debug APKs expose password login behind a hidden trigger.
- Passkey + magic-link supported in both build types.

**AI-Assisted Timeline**: 12 hours (included in Phase 12 Mobile Apps development)

---

### Task 3.7: Update User Documentation

**Objective**: Document all three authentication methods for users

**Files to Create**:
- `docs/USER_AUTH_GUIDE.md` (new file)

**Content to Include**:
- How to register with each method
- How to login with each method
- How to set up MFA (for admins)
- How to manage passkeys
- Troubleshooting common issues
- Browser/device compatibility

**Acceptance Criteria**:
- Comprehensive auth documentation
- Screenshots/GIFs for each flow
- Troubleshooting section

**AI-Assisted Timeline**: 4 hours

---

**Phase 3 Total Duration**: 7-10 days
**Phase 3 Success Criteria**:
- All three authentication methods functional
- Passkey login with biometrics working
- Magic link email delivery working
- Enhanced password requirements enforced
- Unified login experience implemented
- Mobile apps support all five methods
- User documentation complete

---

## Phase 4: PII Protection

**Objective**: Implement data retention policies, user data export, and account deletion features to comply with GDPR/CCPA

**Duration**: 3-5 days
**Priority**: HIGH (legal/compliance requirement)
**Dependencies**: Phase 3 complete (authentication working)

---

### Task 4.1: Implement Data Retention Policies

**Objective**: Create automated cleanup jobs for 2-year retention of inactive accounts and closed care reports

**Files to Modify**:
- `infra/lambda/data_retention_cleanup.py` (new Lambda function)
- `infra/components/lambda_crons.py` (schedule cleanup job)
- `api-dynamo/services/data_retention.py` (retention logic)

**Implementation Steps**:
1. Create Lambda function for data retention cleanup (runs daily)
2. Implement cleanup logic:
   - User accounts: Delete if inactive for 2 years (last_login > 730 days ago)
   - Trail system status history: Delete if created_at > 730 days ago
   - Trail Care Reports (closed/cancelled): Delete if status_updated_at > 730 days ago
   - Trail Care Report photos: Delete from S3 if report closed > 180 days ago
3. Add DynamoDB query to find records eligible for deletion
4. Implement batch deletion (max 25 items per batch)
5. Log all deletions to CloudWatch for audit trail
6. Add email notification to admins for mass deletions
7. Schedule Lambda to run daily at 2 AM UTC
8. Test with synthetic data

**Data Retention Policy Summary**:
- User accounts: 2 years inactive
- Trail system status history: 2 years
- Care reports (active): Indefinite
- Care reports (closed/cancelled): 2 years
- Care report photos: 180 days after closure
- CloudTrail logs: 1 year
- Other photos: 1 year to Glacier

**Testing**:
- Create test data with old timestamps
- Run Lambda function manually
- Verify old records deleted
- Verify audit logs created
- Confirm no active data deleted

**Acceptance Criteria**:
- Automated cleanup job running daily
- All retention policies enforced
- Audit logging complete
- No data loss for active records
- Email notifications working

**AI-Assisted Timeline**: 8 hours

---

### Task 4.2: Implement User Data Export Feature

**Objective**: Allow users to download all their personal data in machine-readable format (GDPR Article 20)

**Canonical endpoint path (docs-mvp-backend-features pass)**: `POST /api/users/me/export-data`. Note: `users` is **plural** per existing convention; `me` segment per the user-scoped pattern (Cat 3 #14/#15 in source plan). New access pattern: **AP-U15** (export-data query across user-scoped entity types).

**Files to Modify**:
- `api-dynamo/src/lambdas/api_dynamo/src/api/routes/users.py` (add `POST /api/users/me/export-data` endpoint)
- `webui/src/features/user/pages/Settings.tsx` (add "Download My Data" button)
- `api-dynamo/src/lambdas/api_dynamo/src/api/services/data_export_service.py` (new file for export logic)

**Implementation Steps**:
1. Create `POST /api/users/me/export-data` API endpoint (authenticated)
2. Query all tables for user's data:
   - User profile (users table)
   - Trail system history (where user_id = current user)
   - Care reports submitted (where submitted_by = current user)
   - Care report comments (where user_id = current user)
   - Forum posts and replies
   - Event RSVPs
   - Volunteer signups
   - Reviews submitted
3. Aggregate data into JSON structure
4. Include metadata (export_date, user_id, email)
5. Return JSON file for download
6. Add UI button "Download My Data" in Settings page
7. Show loading state while export generates
8. Trigger browser download of JSON file

**Export JSON Structure**:
```json
{
  "export_date": "2026-01-17T12:00:00Z",
  "user_id": "abc123",
  "email": "user@example.com",
  "profile": { ...user profile data... },
  "trail_care_reports": [ ...reports... ],
  "trail_care_comments": [ ...comments... ],
  "forum_activity": [ ...posts and replies... ],
  "events": [ ...RSVPs... ],
  "reviews": [ ...trail reviews... ]
}
```

**Testing**:
- Login as user
- Click "Download My Data"
- Verify JSON file downloaded
- Verify all user data included
- Test with user who has no data (empty arrays)

**Acceptance Criteria**:
- Export endpoint functional
- All user data included in export
- JSON format valid and readable
- UI button accessible
- Download triggers successfully

**AI-Assisted Timeline**: 6 hours

---

### Task 4.3: Implement Account Deletion Feature

**Objective**: Allow users to permanently delete their account and all associated data (GDPR Article 17)

**Canonical endpoint path (docs-mvp-backend-features pass)**: `POST /api/users/me/delete-account`. New access pattern: **AP-U16** (mark user `deleted_at = now`).

**Important architectural note**: The actual hard-delete is **NOT performed by this endpoint**. This endpoint marks the account as `deleted_at = now` (soft delete with 30-day grace period). The hard delete + PII scrub is performed by the `retention_cleanup_processor` Lambda 30 days after the `deleted_at` timestamp (see Task 4.4 + Section 11 Architecture B). This separation enables: (a) cancellation during the grace period, (b) batched cleanup at 03:00 UTC daily (lower DynamoDB cost than per-request cascade deletes), (c) audit-logging via `PIIDeletionAudit`.

**Files to Modify**:
- `api-dynamo/src/lambdas/api_dynamo/src/api/routes/users.py` (add `POST /api/users/me/delete-account` endpoint)
- `webui/src/features/user/pages/Settings.tsx` (add "Delete Account" section)
- `api-dynamo/src/lambdas/api_dynamo/src/api/services/account_deletion_service.py` (new file — soft-delete only; hard-delete lives in retention_cleanup_processor Lambda)

**Implementation Steps**:
1. Create `POST /api/users/me/delete-account` API endpoint (authenticated, requires password / passkey confirmation)
2. Implement account deletion logic (soft-delete only — hard delete deferred to Lambda):
   - **Soft delete here**: Mark account as `pending_deletion`, set `deleted_at = now()`, with 30-day grace period
   - After 30 days, **the `retention_cleanup_processor` Lambda** (Task 4.4 + Section 11 Architecture B) hard-deletes all user data:
     - Remove user from Cognito
     - Delete user record from users table
     - Anonymize trail care reports (replace user_id with "deleted_user")
     - Anonymize care report comments (replace user_id with "deleted_user")
     - Delete forum posts and replies (or anonymize)
     - Delete event RSVPs
     - Delete volunteer signups
     - Delete reviews
     - Delete photos uploaded by user (S3)
3. Send confirmation email before deletion
4. Send final confirmation email after deletion complete
5. Add UI for account deletion with multi-step confirmation:
   - Step 1: Click "Delete Account" button
   - Step 2: Show warning modal with consequences
   - Step 3: Require password confirmation
   - Step 4: Show 30-day grace period notice
   - Step 5: Confirm deletion
6. Add "Cancel Deletion" option during grace period

**Deletion Confirmation Flow**:
```
User clicks "Delete Account"
  ↓
Warning modal appears:
  "This will permanently delete your account and all data.
   You will have 30 days to change your mind.
   After 30 days, this action cannot be undone."
  ↓
User enters password to confirm
  ↓
Account marked as pending_deletion
Email sent: "Your account will be deleted in 30 days"
  ↓
After 30 days: Lambda function hard deletes all data
Email sent: "Your account has been permanently deleted"
```

**Testing**:
- Initiate account deletion
- Verify pending_deletion flag set
- Verify confirmation email sent
- Test cancellation during grace period
- Wait for grace period expiration (or manually expire)
- Verify hard deletion completes
- Verify all user data removed

**Acceptance Criteria**:
- Soft delete with 30-day grace period
- Hard delete after grace period
- Email notifications working
- UI confirmation flow clear
- Data anonymization or deletion complete

**AI-Assisted Timeline**: 8 hours

---

### Task 4.4: Create Automated Retention Cleanup Job (EventBridge → `retention_cleanup_processor` Lambda — Architecture B)

**Objective**: Daily background Lambda that performs scheduled cleanups for closed care reports, deleted-account PII scrub, S3 photo orphans, and belt-and-suspenders magic-link tokens. Per docs-mvp-backend-features pass Section 11 Architecture B.

**Architecture (verified, source-plan Section 11 Architecture B)**:

- **Trigger**: EventBridge scheduled rule, `cron(0 3 * * ? *)` (daily 03:00 UTC).
- **New Lambda deployment package**: `retention_cleanup_processor` in `api-dynamo/src/lambdas/retention_cleanup_processor/`.
- **Lambda spec**: Memory **512 MB**, timeout **900 s** (15-min Lambda max — paginate across multiple days or switch to Step Functions if work exceeds), architecture **ARM64** (Graviton2, 20% cheaper).

**Per-invocation work (in this order)**:

1. **Closed care reports** (Phase 9.11): query GSI for `status=CLOSED AND closed_at < now-90d` (configurable per-org policy in future) → batch-delete + write to **`CareReportDeletionAudit`** entity (mirrors `FeedbackDeletionAudit` from TrailPulse).
2. **Deleted-account PII scrub**: query GSI for `users` with `deleted_at < now-30d` → hard-delete remaining `USER#{id}` items, observations, subscriptions, devices. Audit-log to **`PIIDeletionAudit`**.
3. **Photo orphan sweep** (S3): paginated S3 list under `orgs/{org_id}/...`; for each key, check if the referenced parent (care-report id, trail-system id, catalog id, user id) still exists in DynamoDB. If not, delete from S3 + invalidate CloudFront cache.
4. **Belt-and-suspenders magic-link tokens**: scan items with `PK begins_with MLT#` and `ttl < now-300s` (only matters if DynamoDB TTL is delayed, which is rare).
5. **Emit CloudWatch metrics**: `RetentionCleanup.{CareReports,PIIScrub,PhotoOrphans,MagicLinkTokens}.Deleted`.

**New access patterns** (added to `api-dynamo/docs/ACCESS_PATTERNS.md`):

- **AP-RC01**: closed-care-report cleanup query.
- **AP-RC02**: deleted-user PII scrub query.
- **AP-RC03**: photo orphan parent-existence check.

**Pulumi infra additions (queued for implementation plan)**:

- `EventBridgeScheduledLambda` ComponentResource: EventBridge rule + target + Lambda IAM role + CloudWatch log group (30-day retention per project standard).

**CloudWatch alarms**:

- Lambda failure → page.
- Processed-count = 0 for 7 consecutive days → likely silent broken state; page.

**Cost at 100K DAU**: 30 invocations/month × ~5 min × 512 MB = **4.6 GB-min/month** → ~$0.00 (free tier).

**Acceptance Criteria**:

- `retention_cleanup_processor` Lambda runs daily at 03:00 UTC.
- All four cleanup steps execute and emit metrics.
- `CareReportDeletionAudit` and `PIIDeletionAudit` records written for every hard-delete.
- CloudWatch log group created with 30-day retention.
- AP-RC01–AP-RC03 documented in `ACCESS_PATTERNS.md`.

**AI-Assisted Timeline**: 6 hours (Lambda + EventBridge rule + tests).

---

**Phase 4 Total Duration**: 3-5 days
**Phase 4 Success Criteria**:
- Data retention policies automated
- User data export functional
- Account deletion with grace period working
- All GDPR Article 15, 17, 20 requirements met
- Cleanup job running daily

---

## Phase 5: Trail System Data Model

**Objective**: Refactor from individual trails to trail systems (collections of trails managed as one unit)

**Duration**: 5-7 days
**Priority**: CRITICAL (core data model)
**Dependencies**: Phase 3 complete (authentication working)

**DATA MODEL CHANGE**: This is a CRITICAL architectural change. The platform currently manages individual trails, but MVP requires managing trail systems (collections of trails). Example: Hydrocut organization has one trail system that includes Glasgow and Synders areas. Each trail system can contain multiple physical trails, but status is managed at the system level, not per-trail.

**DATABASE DESIGN**: Per `api-dynamo/docs/DYNAMO_DATABASE_DESIGN.md`, TrailLens uses a **single-table DynamoDB design** pattern (table name: `traillens-prod`) with entity type prefixes (ORG#, USER#, TRAILSYSTEM#, REPORT#, etc.), 5 overloaded GSIs (GSI1-GSI5), and 16 MVP entity types. **Current production** uses a 7-table multi-table design per ADR-001, optimized for cost at <500 DAU. Single-table migration is deferred until DynamoDB costs exceed $100/month or traffic reaches 10K DAU. See `api-dynamo/docs/ACCESS_PATTERNS.md` for 78 documented access patterns.

---

### Task 5.1: Create trail_systems DynamoDB Table

**Objective**: Create new table for trail system data

**Files to Modify**:
- `infra/components/dynamodb.py` (add trail_systems table)

**Table Schema**:
```python
trail_systems = Table(
    table_name="trail_systems",
    partition_key=Attribute(name="PK", type="S"),  # org_id
    sort_key=Attribute(name="SK", type="S"),       # trail_system_id
    attributes={
        "trail_system_id": str,      # UUID
        "org_id": str,               # Organization ID
        "name": str,                 # e.g., "Hydrocut Trail System"
        "description": str,          # Long description
        "location": dict,            # {lat, lng, address}
        "cover_photo_url": str,      # S3 URL
        "status": str,               # Current status (open, closed, etc.)
        "status_reason": str,        # Why this status
        "condition_tags": list,      # List of tag IDs (max 20)
        "status_updated_at": str,    # ISO timestamp
        "status_updated_by": str,    # user_id
        "visibility": str,           # public, organization, private
        "created_at": str,
        "updated_at": str,
    },
    global_secondary_indexes=[
        GSI(name="StatusIndex", partition_key="status", sort_key="updated_at"),
        GSI(name="LocationIndex", partition_key="location_region", sort_key="name"),
    ]
)
```

**Implementation Steps**:
1. Define table schema in Pulumi code
2. Deploy to dev environment
3. Verify table created in DynamoDB console
4. Test CRUD operations with boto3
5. Add seed data for Hydrocut and GORBA trail systems (Hydrocut: 1 trail system, GORBA: 2 trail systems)

**Testing**:
- Create trail system record
- Query by org_id
- Query by status
- Verify GSIs working

**Acceptance Criteria**:
- Table created successfully
- Schema matches requirements
- GSIs functional
- Seed data loaded

**AI-Assisted Timeline**: 2 hours

---

### Task 5.2: Create trail_system_history DynamoDB Table

**Objective**: Audit log of all status changes for trail systems (2-year retention)

**Files to Modify**:
- `infra/components/dynamodb.py` (add trail_system_history table)

**Table Schema**:
```python
trail_system_history = Table(
    table_name="trail_system_history",
    partition_key=Attribute(name="trail_system_id", type="S"),
    sort_key=Attribute(name="timestamp", type="S"),  # ISO timestamp
    attributes={
        "history_id": str,           # UUID
        "trail_system_id": str,
        "org_id": str,
        "old_status": str,
        "new_status": str,
        "old_status_reason": str,
        "new_status_reason": str,
        "changed_by": str,           # user_id
        "changed_at": str,           # ISO timestamp
        "tags_added": list,
        "tags_removed": list,
        "photos_added": list,        # S3 URLs
    },
    ttl_attribute="expires_at",  # 2-year retention
)
```

**Implementation Steps**:
1. Define table schema with TTL
2. Deploy table
3. Implement history recording logic in API
4. Test TTL expiration (create record with past expiration)

**Acceptance Criteria**:
- Table created with TTL
- History records created on status changes
- TTL deletes records after 2 years

**AI-Assisted Timeline**: 2 hours

---

### Task 5.3: Migrate API Endpoints from Trails to Trail Systems

**Objective**: Update all API endpoints to work with trail systems instead of individual trails

**Files to Modify**:
- `api-dynamo/routes/trail_systems.py` (rename from trails.py)
- `api-dynamo/models/trail_system.py` (new Pydantic model)
- `api-dynamo/services/trail_system_service.py` (business logic)

**Endpoints to Create/Update**:
1. `POST /trail-systems` - Create trail system
2. `GET /trail-systems/{id}` - Get trail system details
3. `PUT /trail-systems/{id}` - Update trail system
4. `DELETE /trail-systems/{id}` - Delete trail system
5. `GET /trail-systems` - List trail systems (with filters)
6. `PUT /trail-systems/{id}/status` - Update trail system status
7. `GET /trail-systems/{id}/history` - Get status change history
8. `POST /trail-systems/bulk-update` - Bulk status update

**Implementation Steps**:
1. Create Pydantic models for request/response validation
2. Implement CRUD endpoints
3. Add tenant isolation (filter by org_id)
4. Implement status update logic with history recording
5. Add authorization checks (org-admin, trailsystem-owner, trailsystem-crew)
6. Write unit tests for all endpoints
7. Write integration tests

**Testing**:
- Create trail system
- Update trail system
- Delete trail system
- Update status (verify history recorded)
- Bulk update multiple systems
- Test authorization (non-admin cannot update)
- Test tenant isolation (cannot access other org's systems)

**Acceptance Criteria**:
- All endpoints functional
- Tenant isolation enforced
- Authorization working
- History recording working
- Tests passing (80%+ coverage)

**AI-Assisted Timeline**: 12 hours

---

### Task 5.4: Update Web UI for Trail Systems

**Objective**: Update frontend to manage trail systems instead of individual trails

**Files to Modify**:
- `webui/src/features/trails/pages/TrailSystems.tsx` (rename from Trails.tsx)
- `webui/src/features/trails/pages/TrailSystemDetail.tsx`
- `webui/src/features/trails/pages/TrailSystemEdit.tsx`
- `webui/src/features/trails/components/TrailSystemCard.tsx`
- `webui/src/features/trails/components/StatusUpdateModal.tsx`

**UI Components to Update**:
1. Trail Systems List Page (org-admin view)
2. Trail System Detail Page (public view)
3. Trail System Edit Form
4. Status Update Modal
5. History Timeline Component
6. Bulk Update Interface

**Implementation Steps**:
1. Update API client calls to use /trail-systems endpoints
2. Update component prop types and state
3. Update forms to use trail system terminology
4. Update status update modal to show tags
5. Create history timeline component
6. Test all user flows end-to-end

**Testing**:
- Navigate to trail systems list
- Create new trail system
- Edit trail system
- Update status (verify history shows)
- Test mobile responsive
- Test accessibility

**Acceptance Criteria**:
- All pages updated to trail systems
- Forms functional
- Status update working
- History timeline displaying correctly
- Mobile responsive
- Tests passing

**AI-Assisted Timeline**: 10 hours

---

### Task 5.5: Seed Pilot Organization Data

**Objective**: Create trail systems for Hydrocut and GORBA with initial data

**Files to Modify**:
- `scripts/seed_pilot_data.py` (new script)

**Data to Seed**:

**Hydrocut Organization**:

- Trail System 1: "Hydrocut Trail System"
  - Location: Kitchener-Waterloo, ON
  - Status: Open
  - Description: "Mountain biking trail system featuring Glasgow and Synders areas with technical and flow trails"

**GORBA Organization**:
- Trail System 1: "Guelph Lake Trail System"
  - Location: Guelph, ON
  - Status: Open
  - Description: "Scenic lake trails..."
- Trail System 2: "Akell Trail System"
  - Location: Guelph, ON
  - Status: Closed for Maintenance
  - Description: "Technical mountain bike trails..."

**Implementation Steps**:
1. Create organizations (if not exist)
2. Create trail systems
3. Add initial status history
4. Upload cover photos to S3 (use placeholder images)
5. Verify data in DynamoDB console

**Acceptance Criteria**:
- All 3 trail systems created
- Organizations linked correctly
- Cover photos uploaded
- Data visible in web UI

**AI-Assisted Timeline**: 4 hours

---

**Phase 5 Total Duration**: 5-7 days
**Phase 5 Success Criteria**:
- Trail systems data model implemented
- API endpoints migrated
- Web UI updated
- History tracking working
- Pilot data seeded (3 trail systems)
- Tests passing

---

## Phase 6: Tag-Based Status Organization

**Objective**: Implement flexible condition tag system (max 20 tags per organization)

**Duration**: 3-5 days
**Priority**: MEDIUM (enhances status management)
**Dependencies**: Phase 5 complete (trail systems exist)

---

### Task 6.1: Create condition_tags DynamoDB Table

**Objective**: Store customizable condition tags for each organization

**Files to Modify**:
- `infra/components/dynamodb.py` (add condition_tags table)

**Table Schema**:
```python
condition_tags = Table(
    table_name="condition_tags",
    partition_key=Attribute(name="org_id", type="S"),
    sort_key=Attribute(name="tag_id", type="S"),
    attributes={
        "tag_id": str,               # UUID
        "org_id": str,
        "name": str,                 # e.g., "winter", "maintenance"
        "color": str,                # Hex color for UI display
        "description": str,
        "is_active": bool,
        "created_at": str,
        "created_by": str,
    }
)
```

**Implementation Steps**:
1. Define table schema
2. Deploy table
3. Add org-level constraint: max 20 active tags per org
4. Create default tags for new organizations:
   - "winter", "maintenance", "caution", "wet-conditions", "dry-conditions"

**Acceptance Criteria**:
- Table created
- Max 20 tags enforced
- Default tags created

**AI-Assisted Timeline**: 2 hours

---

### Task 6.2: Implement Condition Tag CRUD API Endpoints

**Objective**: Allow org-admins to manage tags

**Files to Modify**:
- `api-dynamo/routes/condition_tags.py` (new file)

**Endpoints** (URL canonical name is `condition-tags` per docs-mvp-backend-features rename; entity name is `condition_tag`):
1. `GET /api/organizations/{org_id}/condition-tags` - List organization's condition tags
2. `POST /api/organizations/{org_id}/condition-tags` - Create new tag (check max 20 limit per docs-mvp-backend-features)
3. `PUT /api/organizations/{org_id}/condition-tags/{tag_id}` - Update tag
4. `DELETE /api/organizations/{org_id}/condition-tags/{tag_id}` - Delete tag (if not in use)

**Implementation Steps**:
1. Implement CRUD endpoints
2. Add validation for **max 20 tags per organization** (raised from 10 in the docs-mvp-backend-features pass — `tags_service.py` validation constant)
3. Prevent deletion of tags in use
4. Add authorization (org-admin only)
5. Write tests

**Testing**:
- Create tag
- Try to create 21st tag (should fail)
- Update tag color
- Try to delete tag in use (should fail)
- Delete unused tag

**Acceptance Criteria**:
- CRUD operations functional
- Max 20 limit enforced
- Authorization working

**AI-Assisted Timeline**: 4 hours

---

### Task 6.3: Implement Tag Assignment to Status Types

**Objective**: Allow trailsystem-crew to tag status updates

**Files to Modify**:
- `api-dynamo/services/trail_system_service.py` (update status logic)
- `webui/src/features/trails/components/StatusUpdateModal.tsx` (add tag selector)

**Implementation Steps**:
1. Update status update endpoint to accept tags array
2. Validate tags exist and belong to organization
3. Store tags in trail_systems.condition_tags array
4. Record tag changes in history
5. Add tag selector UI to status update modal
6. Show current tags as filter chips

**Testing**:
- Update status with tags
- Verify tags saved to trail_system
- Verify history shows tag changes
- Test tag filter in list view

**Acceptance Criteria**:
- Tags assignable during status update
- Tags stored and queryable
- History tracking tag changes

**AI-Assisted Timeline**: 4 hours

---

### Task 6.4: Implement Sticky Tag Filtering

**Objective**: Remember last-used tags for quick status updates

**Files to Modify**:
- `webui/src/features/trails/components/StatusUpdateModal.tsx` (add sticky filter)

**Implementation Steps**:
1. Store last-used tags in localStorage per user
2. Pre-select last-used tags in status update modal
3. Show "Recently Used" section in tag selector
4. Allow easy clearing of selections

**Acceptance Criteria**:
- Last-used tags remembered
- Quick tag selection working

**AI-Assisted Timeline**: 2 hours

---

### Task 6.5: Update Web UI for Tag Management

**Objective**: Create tag management page for org-admins

**Files to Modify**:
- `webui/src/features/organization/pages/OrganizationSettings.tsx` (add Tags tab)
- `webui/src/features/organization/components/TagManager.tsx` (new component)

**UI Features**:
- List all tags with color chips
- Create new tag (name, color picker, description)
- Edit tag
- Delete tag (with confirmation if in use)
- Show "X/10 tags used" counter
- Drag-and-drop to reorder (optional)

**Testing**:
- Create tags up to limit
- Try to exceed limit
- Edit tag color
- Delete tag

**Acceptance Criteria**:
- Tag management UI functional
- Color picker working
- Limit displayed clearly

**AI-Assisted Timeline**: 6 hours

---

**Phase 6 Total Duration**: 3-5 days
**Phase 6 Success Criteria**:
- Condition tags table created
- CRUD API functional
- Tag assignment working
- Max 20 tags enforced
- Tag management UI complete

---

## Phase 7: Status Management

**Objective**: Implement comprehensive status management with history, photos, and bulk operations

**Duration**: 7-10 days
**Priority**: CRITICAL (core feature)
**Dependencies**: Phase 6 complete (tags exist)

### Task 7.1: Implement Status Type Management

**Objective**: Allow organizations to define custom status types (max 30 per org)

**Files to Modify**:
- `infra/components/dynamodb.py` (add status_types table or reuse configuration)
- `api-dynamo/routes/status_types.py`

**Predefined Condition Types** (seed data only — admins can rename, delete, or replace):

| Name | Color | Hex |
|------|-------|-----|
| OPEN | Green | #4CAF50 |
| GREAT CONDITIONS | Green | #4CAF50 |
| CAUTION (WET CONDITIONS) | Yellow | #FFC107 |
| CAUTION (ICY) | Yellow | #FFC107 |
| POOR CONDITIONS - DON'T RIDE | Red | #F44336 |
| MUDDY - DON'T RIDE | Red | #F44336 |
| CLOSED FOR EVENT | Red | #F44336 |

**NOTE**: "Closed" is NOT a condition. Conditions describe trail state for riders. These 7 are seed data only — trail system admins can customize freely.

**Implementation Steps**:
1. Create condition types configuration (may be in organization settings, not separate table)
2. Allow org-admin to create custom condition types (max 30)
3. Each condition type has: name, color (hex, admin-chosen), default_reason, default_tags
4. Implement API endpoints for condition type CRUD
5. Create UI for managing condition types

**Acceptance Criteria**:
- Custom status types supported
- Max 30 limit enforced
- Default status types available

**AI-Assisted Timeline**: 6 hours

---

### Task 7.2: Implement Status Update Workflow

**Objective**: Streamlined status update with photos, reason, and tags

**Files to Modify**:
- `api-dynamo/routes/trail_systems.py` (status update endpoint)
- `webui/src/features/trails/components/StatusUpdateModal.tsx` (complete modal)

**Workflow**:
1. User selects trail system(s)
2. Choose new status type
3. Add reason (required if closing)
4. Add tags (sticky filter from last use)
5. Upload photos (optional, max 5)
6. Preview changes
7. Confirm update

**Implementation Steps**:
1. Update PUT /trail-systems/{id}/status endpoint
2. Accept: new_status, reason, tags, photo_urls
3. Validate all fields
4. Update trail_systems record
5. Create history entry
6. Upload photos to S3 (if provided)
7. Implement bulk update endpoint
8. Create comprehensive status update modal UI

**Testing**:
- Update single trail system status
- Update with photos
- Bulk update multiple systems
- Verify history recorded

**Acceptance Criteria**:
- Status updates functional
- Photos upload to S3
- History tracking complete
- Bulk update working

**AI-Assisted Timeline**: 8 hours

---

### Task 7.3: Implement Two-Level Photo System

**Objective**: Support default photos per trail system plus update-specific photos

**Files to Modify**:
- `api-dynamo/models/trail_system.py` (add default_photos field)
- S3 bucket structure for photos

**Photo System**:
- **Default Photos**: Set on trail system (e.g., cover photo, trail map)
- **Update Photos**: Specific to status changes (e.g., "flooded trail photo")

**S3 Structure**:
```
traillens-{env}-photos/
  trail-systems/
    {trail_system_id}/
      default/
        cover.jpg
        map.png
      updates/
        {update_timestamp}/
          photo1.jpg
          photo2.jpg
```

**Implementation Steps**:
1. Update trail_systems schema with default_photos array
2. Implement photo upload endpoint
3. Store update photos with timestamp
4. Display logic: show default photos + recent update photos
5. Implement photo deletion (180-day retention for update photos)

**Acceptance Criteria**:
- Default photos settable
- Update photos upload successfully
- Photos display correctly
- Retention policy applied

**AI-Assisted Timeline**: 6 hours

---

### Task 7.4: Implement Season Assignment

**STATUS (docs-mvp-backend-features pass): NOT NEEDED — covered by `condition_tags`.**

Season state is communicated via org-defined `condition_tags` (e.g. `Winter Closure`, `Spring Mud Season`). No dedicated season entity or routes. The catalog (Phase 7.5) can include season-themed entries that admins apply when seasons change. This avoids inventing a parallel taxonomy when the existing tag system already covers the use case.

**No code work required.** Doc-only resolution.

---

### Task 7.5: Implement Status History with 2-Year Retention

**Objective**: Complete history tracking (already created in Phase 5)

**Files to Modify**:
- `webui/src/features/trails/components/HistoryTimeline.tsx` (display component)

**Implementation Steps**:
1. Create history timeline component
2. Display status changes chronologically
3. Show: timestamp, user, old status, new status, reason, tags, photos
4. Implement pagination (50 records per page)
5. Add filtering by date range

**Acceptance Criteria**:
- History displays correctly
- Pagination working
- Filtering functional

**AI-Assisted Timeline**: 4 hours

---

### Task 7.6: Implement Bulk Status Updates

**Objective**: Update multiple trail systems simultaneously

**Files to Modify**:
- `api-dynamo/routes/trail_systems.py` (bulk update endpoint)
- `webui/src/features/trails/components/BulkStatusUpdate.tsx` (new component)

**Bulk Update Flow**:
1. Select multiple trail systems (checkboxes)
2. Click "Bulk Update Status"
3. Choose new status (applies to all)
4. Add reason (applies to all)
5. Add tags (applies to all)
6. Upload photos (applies to all)
7. Preview affected systems
8. Confirm update

**Implementation Steps**:
1. Implement POST /trail-systems/bulk-update endpoint
2. Accept array of trail_system_ids and update payload
3. Update each system in transaction (or batch)
4. Create history entries for each
5. Return success/failure for each system
6. Create bulk update UI component
7. Show progress indicator during update
8. Display results (X successful, Y failed)

**Testing**:
- Select 5 trail systems
- Bulk update to "Closed for Maintenance"
- Verify all updated
- Verify individual histories created
- Test partial failure handling

**Acceptance Criteria**:
- Bulk update functional
- Progress indicator working
- Results displayed clearly
- History created for each system

**AI-Assisted Timeline**: 6 hours

---

### Task 7.7: Create Status Type Templates for Onboarding

**STATUS (docs-mvp-backend-features pass): DROPPED — not in MVP scope.**

New orgs are not auto-seeded with starter catalog entries. The condition catalog (Phase 7.5) is org-curated from scratch. The earlier suggestion to seed new orgs from a curated default set is reverted. No code work required.

---

**Phase 7 Total Duration**: 7-10 days
**Phase 7 Success Criteria**:
- Status type management functional
- Status update workflow complete
- Two-level photo system working
- Season state covered by `condition_tags` (no dedicated season entity)
- History with 2-year retention
- Bulk updates functional
- Onboarding starter-templates dropped (no auto-seed)

---

## Phase 7.5: Condition Catalog (Org-Scoped Preset Library)

**Objective**: Provide an org-scoped library of curated **condition presets** that admins can apply with one click to set a trail-system's current condition. Presets carry a name, description, optional reference photo, color, and references to existing org `condition_tags`. The catalog reuses the existing `condition_tags` taxonomy as its tag source — no new tag entity.

**Duration**: 3-5 days
**Priority**: HIGH (core admin UX, drives Phase 7 update flow + Phase 15 TrailPulse feedback configuration)
**Dependencies**: Phase 5 (trail systems exist), Phase 6 (`condition_tags` exist), Phase 7 (condition update flow exists), Phase 9 photo flow (S3 presigned-PUT pattern)

**Files to Create**:

- `api-dynamo/src/lambdas/api_dynamo/src/api/routes/condition_catalog.py` — 7 new routes under tag `condition-catalog`.
- `api-dynamo/src/lambdas/api_dynamo/src/api/services/condition_catalog_service.py` — business logic.
- `api-dynamo/src/packages/traillens_db/src/traillens_db/entities/condition_catalog_entry.py` — `ConditionCatalogEntry` entity.
- `api-dynamo/src/packages/traillens_db/src/traillens_db/repositories/condition_catalog.py` — repository.
- `api-dynamo/docs/CONDITION_CATALOG.md` — single-page reference doc (NEW).

**Entity: `ConditionCatalogEntry`** (verbatim from source-plan spec):

| Field | Type | Notes |
| --- | --- | --- |
| `catalog_id` | UUID | PK component |
| `org_id` | string | Tenancy scope |
| `name` | string (1–80) | Display label, e.g. "Wet & rideable" |
| `description` | string (0–500) | What this condition means; shown in picker |
| `image_s3_key` | string \| null | Optional reference image (presigned upload, same flow as trail photos) |
| `image_url` | string \| null (computed) | CloudFront URL derived from `image_s3_key` |
| `condition_tag_ids` | list[string] (0–5) | References existing `condition_tags` (reused taxonomy) |
| `condition_tag_names` | list[string] | Denormalized for read efficiency (mirrors `condition_observation` pattern) |
| `color` | string (hex) | Display color; defaults to first tag's color if blank |
| `is_active` | bool | Soft-disable without delete |
| `created_by_user_id` | string | Who first created this entry |
| `last_used_at` | string (ISO8601) \| null | For "recently used" sorting |
| `usage_count` | int | Increment on `apply` (eventually-consistent) |
| `created_at`, `updated_at`, `version` | standard | Optimistic-locking version field |

**DynamoDB single-table layout** (to be added to `dynamodb-spec.md` and `DYNAMO_DATABASE_DESIGN.md`):

```text
PK: ORG#{org_id}
SK: CATALOG#{catalog_id}

GSI1 — list active by org, sorted by usage (catalog overload):
  GSI1PK: ORG#{org_id}#CATALOG#ACTIVE
  GSI1SK: USAGE#{usage_count_zero_padded}#CATALOG#{catalog_id}

Tag-filter pattern (no new GSI needed):
  Filter at the application layer by intersecting condition_tag_ids;
  for >100 catalog entries per org consider a per-tag adjacency item later.
```

**GSI overloading note**: TrailLens single-table design intentionally overloads each GSI by entity type. GSI1 already serves `ORG#{id}` for org-member queries, `USER#{id}` for user-centric queries, `EMAIL#{email_lc}` for magic-link rate-limit queries. Adding `ORG#{id}#CATALOG#ACTIVE` is consistent with this pattern (different GSI1PK values per entity type — they never collide).

**Endpoints (7 new + 1 modified)** — under tag `condition-catalog`:

| Method + Path | Purpose | Auth/role |
| --- | --- | --- |
| `GET /api/organizations/{org_id}/condition-catalog` | List entries (paginated, filter by tag IDs, sort by `usage_count` / `last_used_at` / `name`) | Any org member |
| `GET /api/organizations/{org_id}/condition-catalog/{catalog_id}` | Get one entry | Any org member |
| `POST /api/organizations/{org_id}/condition-catalog` | Create entry directly (admin-curation flow — not the user save-to-catalog flow) | `trailsystem-status` or higher |
| `PATCH /api/organizations/{org_id}/condition-catalog/{catalog_id}` | Update entry (optimistic locking via `version`) | `trailsystem-status` or higher |
| `DELETE /api/organizations/{org_id}/condition-catalog/{catalog_id}` | Soft delete (sets `is_active=false`); hard delete restricted to `org-admin` | `trailsystem-status` (soft) / `org-admin` (hard) |
| `POST /api/organizations/{org_id}/condition-catalog/upload-url` | Presigned S3 PUT for catalog image (S3 key: `orgs/{org_id}/catalog/{catalog_id}.jpg` + WebP variants, mirrors existing trail-photo flow) | `trailsystem-status` |
| `POST /api/trail-systems/{trail_system_id}/condition/apply-catalog/{catalog_id}` | Apply a catalog entry as the current condition (allows per-call overrides for `name`, `color`, `description`, `image_s3_key`); updates denormalized fields on trail system, appends to history, fires SNS | `trailsystem-status` |

**Modified existing endpoint:**

- **`PATCH /api/trail-systems/{trail_system_id}/condition`** — add **two** optional fields:
  1. **`catalog_entry_id`** (optional): when present, the server hydrates defaults from the catalog entry, then applies any explicit field overrides in the body.
  2. **`save_to_catalog: bool`** (default `false`): when `true` AND the request did **not** reference an existing `catalog_entry_id`, the server creates a new catalog entry from the same payload in the same TransactWrite (per the user-facing UX: "create a new condition" with optional save-to-catalog checkbox).
  - Backwards-compatible (existing free-form path with both flags omitted keeps working).

**Save-to-catalog UX clarification**: there is **no** "copy from existing trail-system condition history" route. When a user creates a new condition (free-form or via `PATCH /condition`), the request body carries the optional `save_to_catalog: bool` flag. The catalog never gets seeded from past trail-system state.

**Access patterns** (added to `api-dynamo/docs/ACCESS_PATTERNS.md`):

| ID | Pattern | Index |
| --- | --- | --- |
| AP-CC01 | List active catalog entries by org, sortable by usage / recency / name | GSI1 (catalog-active) |
| AP-CC02 | Get catalog entry by ID | Main table |
| AP-CC03 | Filter catalog entries by `condition_tag_ids` (intersection) | App-layer filter on AP-CC01 |
| AP-CC04 | Apply catalog entry to a trail system (transactional: trail system PATCH + history APPEND + catalog `usage_count` UPDATE + `last_used_at` UPDATE + SNS publish) | TransactWrite |
| AP-CC05 | Create catalog entry from a `PATCH /condition` request that carries `save_to_catalog=true` (transactional: trail-system condition update + history APPEND + catalog PUT) | TransactWrite |
| AP-CC06 | Update catalog entry (optimistic-lock on `version`) | UpdateItem with ConditionExpression |
| AP-CC07 | Soft-delete catalog entry (sets `is_active=false`, removed from GSI1) | UpdateItem |

(Note: there is **no AP-CC08** — the from-trail-system route was removed per source-plan correction F-Q.)

**Implementation Steps**:

1. Define `ConditionCatalogEntry` entity + repository + service (TDD; tests first per project standards).
2. Add 7 new routes + 1 modified PATCH to `routes/condition_catalog.py` and update `routes/trail_systems.py`.
3. Add the routes to `openapi.json` under tag `condition-catalog` (tag bump as part of `2.0.0` semver MAJOR version bump).
4. Add GSI1 catalog overload spec to `dynamodb-spec.md` and `DYNAMO_DATABASE_DESIGN.md`.
5. Add AP-CC01–AP-CC07 to `ACCESS_PATTERNS.md` with `Status: IMPLEMENTED ❌` initially.
6. Reuse the existing presigned-S3-PUT + CloudFront-OAC photo flow (`s3_service.py`) for catalog images — same key/variant convention, new prefix `orgs/{org_id}/catalog/{catalog_id}.jpg` + WebP variants.
7. Reuse the existing SNS `TRAIL_CONDITION_CHANGE` topic on apply-catalog; add `catalog_entry_id` and `catalog_entry_name` to the payload for richer push messages.
8. Write unit + integration tests targeting 90% coverage per project standards.

**Acceptance Criteria**:

- 7 catalog routes + 1 modified PATCH live in openapi.json under tag `condition-catalog`.
- `ConditionCatalogEntry` entity + repository + service implemented with TDD.
- GSI1 catalog overload documented and queryable.
- `save_to_catalog: bool` flag on `PATCH /condition` creates a catalog entry in a single TransactWrite.
- `apply-catalog` endpoint atomically updates trail-system, appends history, increments usage_count, fires SNS.
- AP-CC01–AP-CC07 documented with Status column.
- Reference image S3 layout matches `orgs/{org_id}/catalog/{catalog_id}.jpg` + WebP variants.
- 90%+ test coverage on the new service + routes.

**AI-Assisted Timeline**: 14 hours (entity + repo + service + 7 routes + tests + docs).

---

## Phase 8: Scheduled Status Changes

**Objective**: Allow pre-scheduling of future status changes with automated processing

**Duration**: 3-5 days
**Priority**: MEDIUM (nice-to-have, not critical for launch)
**Dependencies**: Phase 7 complete (status management working)

### Task 8.1: Create scheduled_status_changes DynamoDB Table

**Objective**: Store future scheduled status changes

**Files to Modify**:
- `infra/components/dynamodb.py` (add table)

**Table Schema**:
```python
scheduled_status_changes = Table(
    table_name="scheduled_status_changes",
    partition_key=Attribute(name="trail_system_id", type="S"),
    sort_key=Attribute(name="scheduled_time", type="S"),  # ISO timestamp
    attributes={
        "schedule_id": str,
        "trail_system_id": str,
        "org_id": str,
        "scheduled_time": str,
        "new_status": str,
        "reason": str,
        "tags": list,
        "created_by": str,
        "created_at": str,
        "executed": bool,
        "executed_at": str,
    },
    global_secondary_indexes=[
        GSI(name="ExecutionIndex", partition_key="executed", sort_key="scheduled_time"),
    ]
)
```

**Acceptance Criteria**:
- Table created
- Schema supports multiple schedules per trail system

**AI-Assisted Timeline**: 2 hours

---

### Task 8.2: Implement Scheduled Changes CRUD API

**Objective**: Allow trailsystem-crew to schedule future status changes

**Files to Modify**:
- `api-dynamo/routes/scheduled_changes.py` (new file)

**Endpoints**:
1. `POST /scheduled-changes` - Create scheduled change
2. `GET /scheduled-changes` - List upcoming changes
3. `GET /scheduled-changes/{id}` - Get specific change
4. `DELETE /scheduled-changes/{id}` - Cancel scheduled change

**Implementation Steps**:
1. Implement endpoints with validation
2. Prevent scheduling in the past
3. Allow multiple schedules per trail system
4. Add authorization (trailsystem-crew+)
5. Write tests

**Acceptance Criteria**:
- CRUD operations functional
- Past dates rejected
- Authorization working

**AI-Assisted Timeline**: 4 hours

---

### Task 8.3 + 8.4: Scheduled-Condition Processor + Reminder Dispatcher (Single Lambda — Architecture A)

**MERGED (docs-mvp-backend-features pass)**: Tasks 8.3 and 8.4 are collapsed into a single design. **One** Lambda (`scheduled_condition_processor`) handles **both** the fire path **and** the reminder dispatch in the same handler. There is no separate reminder-notification Lambda.

**Architecture (verified, source-plan Section 11 Architecture A)**:

- **Trigger**: EventBridge scheduled rule, **`cron(0/15 * * * ? *)`** (every 15 minutes). User-facing accuracy ±15 minutes — acceptable for MVP. (If tighter is needed at scale, switch to per-item EventBridge Scheduler at >100 schedules/day.)
- **New Lambda deployment package**: `scheduled_condition_processor` in `api-dynamo/src/lambdas/scheduled_condition_processor/`.
- **Lambda spec**: Memory **256 MB**, timeout **60 s**, architecture **ARM64** (Graviton2, 20% cheaper).

**Per-invocation work**:

1. Query DynamoDB **GSI4** (`GSI4PK=SCHEDULED#PENDING`, `GSI4SK <= now+5min`) — items due to fire in this window.
2. For each due item: **TransactWrite** to (a) update trail-system denormalized condition fields, (b) append condition_history entry, (c) flip scheduled-condition `status=APPLIED, applied_at=now`. Publish SNS to `TRAIL_CONDITION_CHANGE` topic (reuses existing fanout).
3. Query GSI4 again for items with `notify_before_minutes` set AND `scheduled_at - now <= notify_before_minutes` AND `reminder_sent=false` — send pre-fire reminder push via existing `notification_push` Lambda or direct SNS.
4. Mark `reminder_sent=true` on those items.

**New DynamoDB GSI**: **GSI4** (`GSI4PK = SCHEDULED#PENDING`, `GSI4SK = scheduled_at_iso8601`). When `status` flips to `APPLIED` or `CANCELLED`, the item is removed from GSI4 (via `GSI4PK = SCHEDULED#{status}`) so the processor doesn't re-process. Documented in `dynamodb-spec.md` and `DYNAMO_DATABASE_DESIGN.md`.

**New access patterns**: AP-SC04 (query due-now), AP-SC05 (query reminder-window), AP-SC06 (mark applied/cancelled). Add to `ACCESS_PATTERNS.md`.

**Pulumi infra additions (queued for implementation plan)**: `EventBridgeScheduledLambda` ComponentResource — EventBridge rule + target + Lambda IAM role + CloudWatch log group (30-day retention). IAM permissions for trail-system / scheduled-condition / history table writes + SNS publish.

**CloudWatch alarms (recalibrated for 15-min interval — 1 invocation per 15-min window, 4/hour, 96/day)**:

- `≥ 1 invocation failure in 30min` → catches a single failure on the next-tick retry; pages on first sustained failure since a missed fire = a missed user-visible condition update.
- `processed-items-count > 100 per tick` for 2 consecutive ticks → indicates scheduled-condition queue buildup or a stuck cursor.
- `0 invocations in 60min` → indicates EventBridge rule misconfigured or disabled (no-fire is invisible without this alarm).

**Cost at 100K DAU** (recalculated for 15-min interval): 96 invocations/day × 30 = **2,880 invocations/month**, ~50ms avg = 2.4 GB-s/month → ~$0.00 (well inside free tier; ~3× cheaper than the original 5-min plan).

**Acceptance Criteria**:

- Single `scheduled_condition_processor` Lambda fires every 15 minutes.
- Both fire AND reminder paths handled in the same handler.
- GSI4 created and populated correctly.
- AP-SC04–AP-SC06 documented.
- CloudWatch alarms configured per the recalibrated thresholds.
- User-facing UI copy in webui + admin app surfaces "applied within 15 minutes of <time>".

**AI-Assisted Timeline**: 8 hours (Lambda + GSI4 + EventBridge rule + tests).

---

### Task 8.5: Update Web UI for Scheduling

**Objective**: Allow scheduling from status update modal

**Files to Modify**:
- `webui/src/features/trails/components/StatusUpdateModal.tsx` (add schedule option)
- `webui/src/features/trails/pages/ScheduledChanges.tsx` (new page to view/manage schedules)

**UI Features**:
- "Schedule for Later" checkbox in status update modal
- Date/time picker for scheduled time
- Upcoming schedules calendar view
- Cancel schedule button

**Acceptance Criteria**:
- Scheduling UI functional
- Date/time picker working
- Calendar view displays schedules

**AI-Assisted Timeline**: 6 hours

---

**Phase 8 Total Duration**: 3-5 days
**Phase 8 Success Criteria**:
- Scheduled changes table created
- API endpoints functional
- Cron job processing changes automatically
- Reminder notifications sent
- UI for scheduling complete

---

## Phase 9: Trail Care Reports System

**Objective**: Implement comprehensive issue tracking system with P1-P5 priority, public/private visibility, and offline support

**Duration**: 10-14 days
**Priority**: CRITICAL (key differentiator)
**Dependencies**: Phase 5 complete (trail systems exist)

**IMPORTANT**: This replaces separate work logs and user reports with a single unified system. Trail crew can create private reports (work logs), and regular users can submit public reports that trail crew can see and manage.

---

### Task 9.1: Create trail_care_reports DynamoDB Table

**Objective**: Store all care reports (issues, work logs, user reports)

**Files to Modify**:
- `infra/components/dynamodb.py` (add table)

**Table Schema**:
```python
trail_care_reports = Table(
    table_name="trail_care_reports",
    partition_key=Attribute(name="trail_system_id", type="S"),
    sort_key=Attribute(name="report_id", type="S"),
    attributes={
        "report_id": str,            # UUID
        "trail_system_id": str,
        "org_id": str,
        "title": str,                # Brief description
        "description": str,          # Full details
        "priority": str,             # P1-P5
        "status": str,               # Open, In Progress, Resolved, Closed, Deferred, Cancelled
        "type_tags": list,           # List of type tag IDs (max 25)
        "is_public": bool,           # Public (visible to all) or Private (crew only)
        "submitted_by": str,         # user_id
        "submitted_at": str,
        "assigned_to": str,          # user_id or null (unassigned pool)
        "assigned_at": str,
        "resolved_at": str,
        "closed_at": str,
        "photo_urls": list,          # Up to 5 photos
        "location": dict,            # {lat, lng} if reported from field
        "created_offline": bool,     # Submitted while offline
        "synced_at": str,            # When uploaded from offline queue
    },
    global_secondary_indexes=[
        GSI(name="StatusIndex", partition_key="status", sort_key="submitted_at"),
        GSI(name="PriorityIndex", partition_key="priority", sort_key="submitted_at"),
        GSI(name="AssignmentIndex", partition_key="assigned_to", sort_key="submitted_at"),
    ]
)
```

**Acceptance Criteria**:
- Table created with GSIs
- Schema supports all required fields

**AI-Assisted Timeline**: 2 hours

---

### Task 9.2: Create trail_care_report_comments Table

**Objective**: Allow crew to add update comments on reports

**Files to Modify**:
- `infra/components/dynamodb.py` (add table)

**Table Schema**:
```python
trail_care_report_comments = Table(
    table_name="trail_care_report_comments",
    partition_key=Attribute(name="report_id", type="S"),
    sort_key=Attribute(name="comment_id", type="S"),
    attributes={
        "comment_id": str,
        "report_id": str,
        "user_id": str,
        "comment_text": str,
        "photo_urls": list,          # Optional photos with comment
        "created_at": str,
    }
)
```

**Acceptance Criteria**:
- Table created

**AI-Assisted Timeline**: 1 hour

---

### Task 9.3: Create care_report_type_tags Table

**Objective**: Flexible categorization for reports (max 25 tags per org)

**Files to Modify**:
- `infra/components/dynamodb.py` (add table)

**Table Schema**:
```python
care_report_type_tags = Table(
    table_name="care_report_type_tags",
    partition_key=Attribute(name="org_id", type="S"),
    sort_key=Attribute(name="tag_id", type="S"),
    attributes={
        "tag_id": str,
        "org_id": str,
        "name": str,                 # e.g., "tree-down", "erosion", "hazard"
        "color": str,
        "description": str,
        "is_active": bool,
        "created_at": str,
    }
)
```

**Default Tags**:
- maintenance, hazard, tree-down, erosion, litter, signage, bridge-repair

**Acceptance Criteria**:
- Table created
- Max 25 tags per org enforced

**AI-Assisted Timeline**: 2 hours

---

### Task 9.4: Implement Care Report CRUD API Endpoints

**Objective**: Complete API for managing care reports

**Files to Modify**:
- `api-dynamo/routes/care_reports.py` (new file)
- `api-dynamo/models/care_report.py` (Pydantic models)
- `api-dynamo/services/care_report_service.py` (business logic)

**Endpoints**:
1. `POST /api/care-reports` - Create report (authenticated)
2. `GET /api/care-reports/{id}` - Get report details
3. `PUT /api/care-reports/{id}` - Update report (crew only)
4. `DELETE /api/care-reports/{id}` - Delete report (org-admin only)
5. `GET /api/care-reports` - List reports (filter by status, priority, assignment)
6. `PUT /api/care-reports/{id}/assign` - Assign to crew member
7. `PUT /api/care-reports/{id}/status` - Update status
8. `POST /api/care-reports/{id}/comments` - Add comment
9. `GET /api/care-reports/{id}/comments` - Get all comments
10. **`GET /api/care-reports/{id}/activity`** — Aggregated activity feed (status changes, assignment changes, comments-as-activity, status-history). **Implementation (per docs-mvp-backend-features pass)**: single `Query(PK=CAREREPORT#{id}, SK begins_with anything)` reads care-report core + comments + assignment-history + status-history items already co-located under that PK; service merges them into a chronological feed. No new entity, no extra writes. New access pattern **AP-CR14** added to `ACCESS_PATTERNS.md`.

**Authorization Rules**:
- Regular users: Can create public reports, view own reports
- Trail-crew: Can create private reports, view all reports, update/assign/comment
- Org-admin: Full access

**Implementation Steps**:
1. Implement all endpoints
2. Add validation (priority must be P1-P5, etc.)
3. Implement visibility filtering (public vs. private)
4. Add authorization checks
5. Implement activity log tracking
6. Write comprehensive tests

**Testing**:
- Create report as regular user (default P3 priority)
- Create private report as trailsystem-crew
- Assign report to crew member
- Update status through workflow (Open → In Progress → Resolved → Closed)
- Add comment with photo
- Verify activity log records all changes
- Test authorization (regular user cannot access private reports)

**Acceptance Criteria**:
- All endpoints functional
- Authorization working correctly
- Activity log tracking all changes
- Visibility filtering working

**AI-Assisted Timeline**: 12 hours

---

### Task 9.5: Implement P1-P5 Priority System

**Objective**: Priority levels with default P3 for regular users

**Priority Levels**:
- **P1 (Critical)**: Immediate danger, trail closed (crew only)
- **P2 (High)**: Significant hazard, needs urgent attention (crew only)
- **P3 (Normal)**: Standard maintenance needed (default for users)
- **P4 (Low)**: Minor issue, address when convenient
- **P5 (Wishlist)**: Enhancement or nice-to-have

**Implementation Steps**:
1. Default priority = P3 for regular user submissions
2. Trail-crew can set any priority (P1-P5)
3. Display priority badge with color coding (P1 red, P2 orange, P3 yellow, P4 green, P5 blue)
4. Sort reports by priority (P1 first)

**Acceptance Criteria**:
- Default P3 for users
- Crew can set any priority
- Priority sorting working

**AI-Assisted Timeline**: 2 hours (included in Task 9.4)

---

### Task 9.6: Implement Public/Private Visibility Flag

**Objective**: Control who can see reports via an explicit `is_public` flag.

**Schema additions (docs-mvp-backend-features pass)**:

- **openapi.json**: add `is_public: bool` (default `false`) to care-report request schema and response schema, and to the `photos` array's parent object.
- **Pydantic model** (`api-dynamo/src/lambdas/api_dynamo/src/api/routes/care_reports.py`): add `is_public: bool = Field(default=False)`.
- **DynamoDB entity** (`CareReportEntity`): add `is_public: bool` column.

**Visibility-gating semantics**:

- When `is_public=true`: any authenticated user (not just org members) can list and get the report.
- When `is_public=false`: only org members can list and get the report.

**Query semantics for `GET /api/care-reports`**:

- Org members: see all reports for their org regardless of `is_public`.
- Non-org-members: see only `is_public=true` reports.

**Implementation Steps**:
1. Add `is_public` field to openapi schema + Pydantic model + DynamoDB entity.
2. Filter queries in `care_reports_service.py` based on caller's org membership:
   - Org members: no `is_public` filter applied.
   - Non-members: `FilterExpression: is_public = :true`.
3. Add "Make Private" checkbox for crew when creating report (UI side; default to public for user submissions, private for crew work logs).
4. Document gating in `api-dynamo/docs/API_DESIGN.md`.

**Acceptance Criteria**:
- `is_public` field present in openapi schema, Pydantic model, and DynamoDB entity.
- Visibility-gating semantics enforced server-side in list and get endpoints.
- Default value `false` (private) when unspecified.

**AI-Assisted Timeline**: 4 hours (included in Task 9.4 implementation).

---

### Task 9.7: Implement Type Tag Management

**Objective**: Allow org-admin to manage report type tags (max 25 per org)

**Files to Modify**:
- `api-dynamo/routes/care_report_type_tags.py` (new file)
- `webui/src/features/organization/pages/OrganizationSettings.tsx` (add Type Tags tab)

**Implementation Steps**:
1. Implement CRUD API for type tags
2. Enforce max 25 tags per org
3. Create UI for managing type tags
4. Auto-create default tags for new orgs

**Acceptance Criteria**:
- CRUD operations functional
- Max 25 tags enforced
- Tag management UI complete

**AI-Assisted Timeline**: 4 hours

---

### Task 9.8: Implement Assignment Workflow

**Objective**: Allow assignment to specific crew members or self-assignment

**Assignment Options**:
1. **Unassigned Pool**: Report not assigned to anyone
2. **Specific Assignment**: Org-admin assigns to specific crew member
3. **Self-Assignment**: Crew member claims report from unassigned pool

**Implementation Steps**:
1. Implement PUT /care-reports/{id}/assign endpoint
2. Support assigning to user_id or setting to null (unassigned)
3. Add "Assign to Me" button for crew
4. Add "Assign to..." dropdown for org-admin
5. Send notification when assigned
6. Track assignment in activity log

**Testing**:
- Org-admin assigns report to crew member
- Crew member self-assigns from pool
- Unassign report

**Acceptance Criteria**:
- Assignment workflow functional
- Self-assignment working
- Notifications sent
- Activity log tracking assignments

**AI-Assisted Timeline**: 4 hours

---

### Task 9.9: Implement Comments and Activity Log

**Objective**: Allow crew to add update comments and track all changes

**Comments**:
- Crew can add comments to reports
- Comments can include photos
- Displayed chronologically

**Activity Log**:
- Track all changes: status, priority, assignment, tags
- Show: timestamp, user, action, old value, new value
- Display in timeline format

**Implementation Steps**:
1. Implement comment CRUD (create, get, delete)
2. Implement activity log recording for all report changes
3. Create ActivityTimeline component for UI
4. Display comments and activity log together

**Acceptance Criteria**:
- Comments functional
- Activity log tracking all changes
- Timeline display clear

**AI-Assisted Timeline**: 6 hours

---

### Task 9.10: Implement Multiple Photo Upload (Max 5)

**Objective**: Allow up to 5 photos per report. Schema-enforced via openapi `maxItems: 5` AND server-side validation.

**Schema enforcement (docs-mvp-backend-features pass)**:

- **openapi.json**: add `maxItems: 5` to the photo upload request schema AND to the care-report response `photos` array.
- **Server-side validation** (`care_reports_service.py`): if a `POST /api/care-reports/{id}/photos` request would cause the total count to exceed 5, return **400 Bad Request** with a clear error message (`{"error": "max_photos_exceeded", "message": "A care report may have at most 5 photos."}`).

**Implementation Steps**:
1. Update photo upload endpoint to accept array of photos.
2. **Validate max 5 photos per report (server-side)**: count existing photos + incoming photos before write; reject with 400 if total > 5.
3. Add `maxItems: 5` to openapi.json on both request and response schemas.
4. Store photos in S3: `care-reports/{report_id}/{photo_id}.jpg`.
5. Add photo URLs to report record.
6. Implement photo deletion (frees a slot for another upload).
7. Create photo upload UI component with preview.
8. Add photo captions (optional).

**Testing**:
- Upload 1 photo.
- Upload 5 photos (one request).
- Upload 5 photos in 5 separate requests (one at a time).
- Try to upload 6th photo (should fail with 400).
- Try to upload 3 photos when 4 already exist (should fail with 400 — would exceed 5).
- Delete a photo, then upload another (should succeed — 4 + 1 = 5).

**Acceptance Criteria**:
- openapi schema declares `maxItems: 5` on both request and response photo arrays.
- Server-side validation returns 400 when the write would exceed 5.
- Photos upload to S3.
- Preview working.
- Deletion functional.

**AI-Assisted Timeline**: 6 hours

---

### Task 9.11: Implement Status-Based Retention Policy

**Objective**: Active reports kept indefinitely; closed care-reports scrubbed after 90 days. **Cross-link to Task 4.4 / Section 11 Architecture B** — the actual scrubbing is done by the `retention_cleanup_processor` Lambda, NOT by per-request logic in this task.

**Retention Policy (docs-mvp-backend-features pass)**:

- **Active Reports** (Open, In Progress, Deferred, Resolved): Kept indefinitely.
- **Closed Reports**: scrubbed by the `retention_cleanup_processor` Lambda (Task 4.4) after **90 days** (configurable per-org policy in future). Audit-logged to **`CareReportDeletionAudit`** entity.
- **Photos**: photo orphan sweep performed by the same Lambda — any S3 key whose parent care-report is gone is deleted.

**Implementation Steps**:

1. Confirm closed-care-report cleanup is implemented in the `retention_cleanup_processor` Lambda (Task 4.4 + Architecture B step #1).
2. Confirm `CareReportDeletionAudit` entity exists in `DYNAMO_DATABASE_DESIGN.md` and `dynamodb-spec.md`.
3. Document the 90-day window in `api-dynamo/docs/CONDITION_CATALOG.md` adjacents and in `api-dynamo/docs/BACKGROUND_WORKERS.md`.
4. Document the configurability hook (per-org `closed_care_report_retention_days` field on the Organization entity) — deferred to a future PR; default to 90 today.

**Acceptance Criteria**:

- Closed care-reports scrubbed after 90 days by the daily Lambda (not per-request logic).
- Audit log written to `CareReportDeletionAudit` for every deletion.
- Photo orphan sweep deletes S3 keys whose parent care-report is gone.
- 90-day window documented; configurability hook noted for future work.

**AI-Assisted Timeline**: 0 hours additional (logic lives in Task 4.4 Lambda).

---

### Task 9.12: Implement Offline Report Creation Support

**Objective**: Allow mobile apps to create reports offline, queue locally, auto-upload when signal returns

**Implementation Steps** (mostly in Phase 12 Mobile Apps):
1. API supports batch upload of offline reports
2. Add `created_offline` and `synced_at` fields
3. Validate reports submitted from offline queue
4. Handle potential duplicates (idempotency)
5. Show "Syncing X offline reports..." in app

**Acceptance Criteria**:
- Offline reports can be uploaded
- Duplicate prevention working
- Sync status displayed

**AI-Assisted Timeline**: 4 hours (mostly in Phase 12)

---

### Task 9.13: Update Web UI for Care Report Management

**Objective**: Complete care report UI for web

**Files to Modify**:
- `webui/src/features/trails/pages/CareReports.tsx` (list view)
- `webui/src/features/trails/pages/CareReportDetail.tsx` (detail view)
- `webui/src/features/trails/pages/CareReportCreate.tsx` (create form)
- `webui/src/features/trails/components/CareReportCard.tsx`
- `webui/src/features/trails/components/CareReportFilters.tsx`

**UI Features**:
- List view with filters (status, priority, assignment, type tags)
- Detail view with comments and activity log
- Create form with photo upload, priority, visibility toggle
- Assignment interface
- Status update workflow
- Comment form

**Implementation Steps**:
1. Create all components
2. Implement filtering and sorting
3. Add pagination
4. Create photo gallery component
5. Implement mobile responsive design
6. Write tests

**Testing**:
- Navigate through all views
- Create report with photos
- Filter by status, priority
- Assign report
- Add comment
- Update status

**Acceptance Criteria**:
- All views functional
- Filtering working
- Mobile responsive
- Tests passing

**AI-Assisted Timeline**: 14 hours

---

**Phase 9 Total Duration**: 10-14 days
**Phase 9 Success Criteria**:
- All 3 DynamoDB tables created
- Care report API fully functional
- P1-P5 priority system working
- Public/private visibility control
- Type tags (max 25) implemented
- Assignment workflow complete
- Comments and activity log functional
- Multiple photo upload (max 5) working
- Status-based retention policy automated
- Offline support infrastructure ready
- Web UI complete and tested

---

## Phase 10: Notification System

**Objective**: Implement email, SMS, and push notifications for trail system status updates

**Duration**: 5-7 days
**Priority**: HIGH (key user engagement feature)
**Dependencies**: Phase 7 complete (status management working)

### Task 10.1: Implement Email Notifications via AWS SES

**Objective**: Send email notifications for status changes

**Files to Modify**:
- `api-dynamo/services/notification_service.py` (new file)
- `api-dynamo/templates/email/status_change.html` (email template)

**Implementation Steps**:
1. Configure AWS SES for email sending (already done in infra)
2. Create email template for status change notifications
3. Implement send_email function using boto3 SES client
4. Trigger email when trail system status updated
5. Query subscribers for affected trail system
6. Send personalized email to each subscriber
7. Track email delivery status (CloudWatch)
8. Implement unsubscribe link in email footer

**Email Template**:
```html
Subject: [TrailLensHQ] {Trail System Name} Status Updated

Hi {User Name},

The status of {Trail System Name} has been updated:

Previous Status: {Old Status}
New Status: {New Status}
Reason: {Reason}
Updated By: {User Name}
Updated At: {Timestamp}

View full details: {Link to trail system page}

---
Building communities, one trail at a time.
Unsubscribe | Notification Preferences
```

**Testing**:
- Update trail system status
- Verify email sent to subscribers
- Check email deliverability (not spam)
- Test unsubscribe link

**Acceptance Criteria**:
- Email notifications sent on status change
- Delivery rate >99%
- Unsubscribe working
- Email template professional

**AI-Assisted Timeline**: 6 hours

---

### Task 10.2: Implement SMS Notifications via AWS Pinpoint

**Objective**: Send SMS notifications for urgent status changes (P1-P2 care reports, closures)

**Files to Modify**:
- `api-dynamo/services/notification_service.py` (add SMS logic)
- `infra/components/pinpoint.py` (configure Pinpoint)

**Implementation Steps**:
1. Configure AWS Pinpoint for SMS
2. Implement send_sms function
3. Create SMS template (160 char limit):
   "TrailLensHQ Alert: {Trail System} is now {Status}. Reason: {Reason}. View details: {short URL}"
4. Trigger SMS only for urgent notifications:
   - Trail closures
   - P1-P2 care reports
   - User-configurable urgency preferences
5. Implement opt-in requirement (GDPR/TCPA compliance)
6. Add STOP/START keyword handling

**SMS Template**:
```
TrailLensHQ: {Trail System} now {Status}. {Reason}. Details: {URL}
Reply STOP to unsubscribe.
```

**Testing**:
- Close trail system
- Verify SMS sent
- Test STOP keyword
- Verify no non-urgent SMS sent

**Acceptance Criteria**:
- SMS sent for urgent notifications only
- 160 char limit enforced
- Opt-in requirement met
- STOP keyword working

**Cost Impact**: ~$0.00645/SMS (Canada)

**AI-Assisted Timeline**: 6 hours

---

### Task 10.3: Implement Push Notifications via SNS→FCM (Android) and SNS→APNS (iOS)

**Objective**: Send push notifications to Android app users (FCM) and iOS app users (APNS)

**Files to Modify**:
- `api-dynamo/services/notification_service.py` (add push logic)
- `infra/components/sns.py` (APNS configuration)

**Implementation Steps**:
1. Configure SNS with FCM credentials (Firebase Server Key) and APNS credentials (Apple Push Notification certificate)
2. Store device tokens in `devices` table when user logs in
3. Implement send_push function using SNS
4. Create push notification payload:
   ```json
   {
     "aps": {
       "alert": {
         "title": "Trail Status Update",
         "body": "{Trail System} is now {Status}"
       },
       "badge": 1,
       "sound": "default"
     },
     "trail_system_id": "{id}",
     "status": "{status}"
   }
   ```
5. Trigger push on status change
6. Handle device token expiration (remove invalid tokens)
7. Implement deep linking (tap notification → trail detail page)

**Testing**:
- Update trail system status
- Verify push notification received on Android (FCM) and iOS (APNS)
- Tap notification (verify deep link works)
- Test with invalid device token (should remove)

**Acceptance Criteria**:
- Push notifications sent on status change
- Deep linking working
- Invalid tokens cleaned up
- Delivery rate >95%

**AI-Assisted Timeline**: 8 hours

---

### Task 10.4: Implement Subscription Management

**Objective**: Allow users to subscribe to trail systems and organizations

**Files to Modify**:
- `api-dynamo/routes/subscriptions.py` (new file)
- DynamoDB table: `subscriptions` (new table)
- `webui/src/features/user/pages/Subscriptions.tsx` (manage subscriptions UI)

**Subscription Types**:
1. **Trail System Subscription**: Subscribe to specific trail system
2. **Organization Subscription**: Subscribe to all trail systems in organization

**Table Schema**:
```python
subscriptions = Table(
    table_name="subscriptions",
    partition_key=Attribute(name="user_id", type="S"),
    sort_key=Attribute(name="subscription_id", type="S"),
    attributes={
        "subscription_id": str,      # UUID
        "user_id": str,
        "subscription_type": str,    # "trail_system" or "organization"
        "trail_system_id": str,      # If trail_system subscription
        "org_id": str,               # If organization subscription
        "created_at": str,
    },
    global_secondary_indexes=[
        GSI(name="TrailSystemIndex", partition_key="trail_system_id", sort_key="created_at"),
        GSI(name="OrganizationIndex", partition_key="org_id", sort_key="created_at"),
    ]
)
```

**API Endpoints (canonical paths per docs-mvp-backend-features pass — under existing `users` tag, no new service facade)**:

1. **`POST /api/users/me/subscriptions`** — Subscribe to trail system. Body: `{trail_system_id}`. (AP-SUB01)
2. **`GET /api/users/me/subscriptions`** — List the authenticated user's subscriptions. (AP-SUB02)
3. **`DELETE /api/users/me/subscriptions/{trailsystem_id}`** — Unsubscribe from a trail system. (AP-SUB03)

Access patterns AP-SUB01–AP-SUB03 already exist in `api-dynamo/docs/ACCESS_PATTERNS.md` (verified at lines 196–198) using `USER#{user_id}` + `SUBSCRIPTION#{trailsystem_id}`. The new route shape matches the existing access-pattern shape — no new patterns needed.

**Implementation Steps**:

1. Add the three routes under the `users` tag in `openapi.json`.
2. Create `subscriptions_service.py` (new file under `api-dynamo/src/lambdas/api_dynamo/src/api/services/`).
3. Add "Subscribe" button on trail-system pages in webui + both mobile apps.
4. Query subscribers when sending notifications.
5. Respect subscription + notification preferences (Task 10.5).

**Testing**:

- Subscribe to trail system.
- Verify notification received when status changes.
- Unsubscribe.
- Verify notification not received.
- Confirm pagination on the LIST endpoint works for users with >50 subscriptions.

**Acceptance Criteria**:

- All three routes documented in openapi under `users` tag.
- Subscription CRUD functional.
- Notifications sent to subscribers only.
- Subscribe/unsubscribe UI working in webui + admin app + user app.

**AI-Assisted Timeline**: 6 hours

---

### Task 10.5: Implement Notification Preferences

**Objective**: Allow users to configure notification channels and types

**Files to Modify**:
- `api-dynamo/models/user.py` (add notification_preferences)
- `webui/src/features/user/pages/NotificationSettings.tsx` (new page)

**Preference Options (docs-mvp-backend-features pass — 2-axis matrix)**:

- **Channels (top-level on/off)**: Email, SMS, Push (checkboxes for each — global gate per channel).
- **Events × Channels (matrix)**: each of the **6 event types** below has independent per-channel toggles (email, sms, push):

  1. `condition_change` — trail-system condition changed.
  2. `care_report_created` — new care report submitted on a subscribed trail system.
  3. `care_report_assigned` — a care report was assigned to me.
  4. `care_report_comment` — new comment on a care report I'm watching.
  5. `scheduled_condition_reminder` — pre-fire reminder for a scheduled condition change.
  6. `observation_received` — a new condition observation submitted on a subscribed trail system.

- **Quiet Hours**: don't send notifications during specified times (per-user start/end + timezone).

**User Preferences Schema (docs-mvp-backend-features pass — 2-axis matrix replacing the legacy nested-by-channel shape)**:

```json
{
  "notification_preferences": {
    "channels": {
      "email": true,
      "sms": false,
      "push": true
    },
    "events": {
      "condition_change":              { "email": true,  "sms": false, "push": true  },
      "care_report_created":           { "email": true,  "sms": false, "push": true  },
      "care_report_assigned":          { "email": true,  "sms": true,  "push": true  },
      "care_report_comment":           { "email": false, "sms": false, "push": true  },
      "scheduled_condition_reminder":  { "email": false, "sms": false, "push": true  },
      "observation_received":          { "email": false, "sms": false, "push": false }
    },
    "quiet_hours": {
      "start": "22:00",
      "end": "08:00",
      "timezone": "America/Toronto"
    }
  }
}
```

**Resolution rule (server-side dispatch)**: a notification is delivered on channel X for event E **iff** `channels.X == true` AND `events.E.X == true` AND not in quiet hours.

**Endpoints**: `GET /api/users/me/notification-preferences` and `PATCH /api/users/me/notification-preferences` (existing routes; openapi schema is rewritten in this pass to the 2-axis shape above). Notifications service (`notifications_service.py`) is rewritten to consult the matrix per dispatch.

**Implementation Steps**:
1. Add notification_preferences to users table
2. Create NotificationSettings UI page
3. Implement preference saving
4. Update notification service to respect preferences
5. Implement quiet hours logic

**Testing**:
- Disable email notifications
- Verify no email sent on status change
- Enable SMS, verify SMS sent
- Set quiet hours, verify notifications delayed

**Acceptance Criteria**:
- All preference options functional
- Notifications respect preferences
- Quiet hours working
- Settings UI intuitive

**AI-Assisted Timeline**: 6 hours

---

### Task 10.6: Create Email Templates for Status Changes

**Objective**: Professional email templates for different notification types

**Files to Modify**:
- `api-dynamo/templates/email/` directory with multiple templates

**Templates to Create**:
1. `status_change.html` - Trail system status changed
2. `care_report_assigned.html` - Care report assigned to you
3. `care_report_comment.html` - New comment on your report
4. `care_report_resolved.html` - Your report was resolved
5. `welcome.html` - Welcome to TrailLensHQ
6. `password_reset.html` - Password reset link

**Template Standards**:
- Responsive HTML (works on mobile)
- Plain text fallback
- Consistent branding
- Clear call-to-action buttons
- Unsubscribe link in footer

**Acceptance Criteria**:
- All templates created
- Mobile responsive
- Brand consistent
- Tested across email clients

**AI-Assisted Timeline**: 4 hours

---

### Task 10.7: Create SMS Templates (160 Char Max)

**Objective**: Concise SMS templates

**Templates to Create**:
1. Trail closure: "TrailLensHQ: {Trail} CLOSED. {Reason}. {URL}"
2. Trail reopened: "TrailLensHQ: {Trail} OPEN. {URL}"
3. P1 care report: "TrailLensHQ URGENT: {Trail} hazard reported. {URL}"

**Acceptance Criteria**:
- All templates <160 chars
- URL shortener implemented (bit.ly or custom)

**AI-Assisted Timeline**: 2 hours

---

### Task 10.8: Update Web UI for Notification Preferences

**Objective**: Settings page for managing notifications

**Files to Modify**:
- `webui/src/features/user/pages/Settings.tsx` (add Notifications tab)
- `webui/src/features/user/components/NotificationPreferences.tsx`

**UI Features**:
- Toggle switches for email/SMS/push
- Checkboxes for notification types
- Frequency dropdown
- Quiet hours time pickers
- "Test Notification" button

**Acceptance Criteria**:
- Settings UI complete
- Test notification working
- Changes saved successfully

**AI-Assisted Timeline**: 6 hours

---

**Phase 10 Total Duration**: 5-7 days
**Phase 10 Success Criteria**:
- Email notifications functional (99%+ delivery)
- SMS notifications for urgent updates (opt-in)
- Push notifications to mobile apps (<2 min latency)
- Subscription management working
- Notification preferences configurable
- Email and SMS templates professional
- Settings UI complete

---

## Phase 11: Web Dashboards

**Objective**: Create role-specific dashboards for all 8 user roles

**Duration**: 10-14 days
**Priority**: CRITICAL (core user interface)
**Dependencies**: Phases 5-9 complete (all backend features ready)

**Tech Stack**: webui/ project — React 19 + TypeScript + Vite 6.x + Tailwind CSS 4.x + shadcn/ui + Tremor (charts) + Lucide React (icons) + Zustand 5.x + React Query 5.x. Feature-based organization with lazy-loaded routes.

**8 User Roles**:
1. super-admin (platform super admin)
2. admin (site administrator)
3. org-admin (organization administrator)
4. trailsystem-owner (trail management permissions)
5. trailsystem-crew (trail maintenance permissions)
6. trailsystem-status (trail status update only)
7. content-moderator (content moderation)
8. org-member (basic organization member)

---

### Task 11.1: Create Role-Specific Dashboard Layouts

**Objective**: Design and implement dashboard for each role with relevant metrics and quick actions

**Files to Modify**:
- `webui/src/features/admin/pages/Dashboard.tsx` (main dashboard router)
- `webui/src/features/admin/pages/dashboards/OrgAdminDashboard.tsx`
- `webui/src/features/admin/pages/dashboards/TrailCrewDashboard.tsx`
- `webui/src/features/admin/pages/dashboards/UserDashboard.tsx`
- (Similar for other roles)

**Dashboard Components by Role**:

**Org-Admin Dashboard**:
- Total trail systems count
- Active care reports count (by priority)
- Recent status changes
- Team member list
- Quick actions: Create trail system, Invite user, Bulk status update

**Trail-Crew Dashboard**:
- Assigned care reports
- Unassigned care reports (to claim)
- Recent activity
- Quick actions: Submit care report, Update trail status

**Regular User Dashboard**:
- Subscribed trail systems with current status
- Saved trail systems
- Recent care reports submitted
- Quick actions: Browse trails, Submit report

**Implementation Steps**:
1. Design dashboard layouts for each role
2. Create reusable dashboard components (StatCard, QuickActions, ActivityFeed)
3. Implement role detection and dashboard routing
4. Fetch relevant data for each dashboard
5. Add loading states and error handling
6. Ensure mobile responsive

**Testing**:
- Login as each role
- Verify correct dashboard displayed
- Test all quick actions
- Verify data accuracy

**Acceptance Criteria**:
- Dashboard for each of 8 roles
- Role-specific data displayed
- Quick actions functional
- Mobile responsive

**AI-Assisted Timeline**: 16 hours

---

### Task 11.2: Implement Trail System CRUD UI for Org-Admin

**Objective**: Complete interface for managing trail systems

**Files to Modify**:
- `webui/src/features/trails/pages/TrailSystems.tsx` (list)
- `webui/src/features/trails/pages/TrailSystemCreate.tsx` (create)
- `webui/src/features/trails/pages/TrailSystemEdit.tsx` (edit)

**UI Features**:
- List view with search and filters
- Create form with validation
- Edit form with photo upload
- Delete confirmation modal
- Bulk actions

**Acceptance Criteria**:
- CRUD operations functional
- Form validation working
- Photo upload working

**AI-Assisted Timeline**: 8 hours (completed in Phase 5, just verify)

---

### Task 11.3: Implement Care Report Management UI for Trail-Crew

**Objective**: Complete care report interface

**Files to Modify**:
- `webui/src/features/trails/pages/CareReports.tsx`
- `webui/src/features/trails/pages/CareReportDetail.tsx`
- `webui/src/features/trails/components/AssignmentModal.tsx`

**UI Features**:
- List view with filters (priority, status, assignment)
- Detail view with comments and activity log
- Assignment interface
- Status update workflow
- Comment form with photo upload

**Acceptance Criteria**:
- All features functional
- Filters working
- Assignment and status update working

**AI-Assisted Timeline**: 10 hours (completed in Phase 9, just verify)

---

### Task 11.4: Implement Analytics Dashboards

**Objective**: Show key metrics and trends

**Files to Modify**:
- `webui/src/features/admin/pages/Analytics.tsx` (new page)
- `webui/src/features/admin/components/charts/` (chart components)

**Analytics to Display**:

**Trail System Analytics**:
- Total views per trail system
- Status change frequency
- Average time in each status
- Peak usage times

**Care Report Analytics**:
- Reports by priority (P1-P5 breakdown)
- Average resolution time
- Reports by status
- Most common type tags

**User Analytics**:
- Total users
- Active users (30-day)
- Subscriptions count
- Notification engagement rate

**Charts to Implement**:
- Line chart: Status changes over time
- Pie chart: Care reports by priority
- Bar chart: Reports by trail system
- Timeline: Recent activity

**Implementation Steps**:
1. Use Tremor charting components (built on Recharts) per webui/ tech stack.
2. Implement the **8 dedicated `/api/.../analytics/*` routes** (per docs-mvp-backend-features pass — Section 8 row #10). All routes under new openapi tag **`analytics`**. Each route returns pre-aggregated data only — never raw rows. All routes accept `start_date`, `end_date` query params; bucketed routes also accept `bucket=day|week|month`. **AuthZ matrix detailed below.** New access patterns **AP-AN01–AP-AN08**.

   - **AP-AN01** — `GET /api/organizations/{org_id}/analytics/overview` — Org-Admin landing-page snapshot: total trail systems, active care-reports count by priority (P1–P5), total users, total subscriptions, last-30d activity count. AuthZ: `org-admin`+.
   - **AP-AN02** — `GET /api/organizations/{org_id}/analytics/trail-systems` — status-change frequency, average time in each condition. Bucketed. AuthZ: `org-admin`+.
   - **AP-AN03** — `GET /api/organizations/{org_id}/analytics/care-reports` — count by priority, by status, by type-tag, average resolution time. Bucketed. AuthZ: `org-admin`+ for whole org; `trailsystem-crew` may filter by trail system.
   - **AP-AN04** — `GET /api/organizations/{org_id}/analytics/users` — total, 30d-active, subscriptions count, notification engagement (sent / opened / clicked). AuthZ: `org-admin`+.
   - **AP-AN05** — `GET /api/organizations/{org_id}/analytics/activity-feed` — paginated timeline of status changes + care-report updates + comments + new observations across the whole org. Cursor-paginated, no aggregation. AuthZ: any authenticated org member (rows are filtered by membership).
   - **AP-AN06** — `GET /api/organizations/{org_id}/analytics/export` — CSV export. Query params: `metric=trail-systems|care-reports|users|activity`, plus date range. Returns `text/csv` with appropriate `Content-Disposition`. AuthZ: `org-admin`+.
   - **AP-AN07** — `GET /api/trail-systems/{ts_id}/analytics/condition-history` — per-trail-system condition timeline with peak-usage times. Bucketed. AuthZ: `trailsystem-owner`+.
   - **AP-AN08** — `GET /api/trail-systems/{ts_id}/analytics/views` — view counts per trail system over time. Requires view-tracking; flag for implementation plan as a dependency (likely a small writes-only `VIEW#{ts_id}#{date}` rollup updated by a non-blocking middleware on `GET /trail-systems/{id}`). AuthZ: `trailsystem-owner`+.

3. **Backed by daily DynamoDB rollups** written by the `retention_cleanup_processor` Lambda (Task 4.4 / Architecture B is extended to also compute rollups). Rollup entity: `ANALYTICS_ROLLUP#{org_id}#{metric}#{date}`. Each analytics route reads rollups, never raw rows.
4. Create chart components.
5. Implement date range selector.
6. Add export to CSV functionality (AP-AN06 endpoint above).
7. Ensure mobile responsive.

**Trail-Crew and Regular-User dashboards** (Phase 11.1) compose from existing endpoints (`/care-reports?assignee=me`, `/users/me/subscriptions`, etc.) — no additional analytics routes needed for them.

**Testing**:
- View analytics page
- Change date range
- Export data to CSV
- Verify calculations accurate

**Acceptance Criteria**:
- All charts displaying correctly
- Data accurate
- Export functional
- Mobile responsive

**AI-Assisted Timeline**: 12 hours

---

### Task 11.5: Implement Bulk Operations UI

**Objective**: Efficiently manage multiple trail systems

**Files to Modify**:
- `webui/src/features/trails/components/BulkActions.tsx`
- `webui/src/features/trails/components/TrailSystemTable.tsx` (add checkboxes)

**Bulk Operations**:
- Select multiple trail systems (checkboxes)
- Bulk status update
- Bulk delete
- Bulk export

**Acceptance Criteria**:
- Selection working
- Bulk update functional
- Progress indicators shown

**AI-Assisted Timeline**: 4 hours (completed in Phase 7, just verify)

---

### Task 11.6: Implement Tag Management UI

**Objective**: Manage status tags and care report type tags

**Files to Modify**:
- `webui/src/features/organization/pages/OrganizationSettings.tsx` (Tags section)
- `webui/src/features/organization/components/TagManager.tsx`
- `webui/src/features/organization/components/TypeTagManager.tsx`

**UI Features**:
- Create/edit/delete tags
- Color picker
- Usage count display
- "X/10 tags used" or "X/25 tags used" counter

**Acceptance Criteria**:
- Tag management functional
- Limits enforced and displayed
- Color picker working

**AI-Assisted Timeline**: 4 hours (completed in Phase 6, just verify)

---

### Task 11.7: Implement User Management UI for Org-Admin

**Objective**: Manage team members and roles

**Files to Modify**:
- `webui/src/features/admin/pages/TeamManagement.tsx` (new page)
- `webui/src/features/admin/components/UserRoleEditor.tsx`
- `webui/src/features/admin/components/InviteUserModal.tsx`

**UI Features**:
- List all team members
- Invite new user (email invitation)
- Change user role (dropdown)
- Remove user from organization
- View user activity

**Implementation Steps**:
1. Create team management page
2. Implement user list with filters
3. Create invite modal with email form
4. Implement role change dropdown
5. Add remove confirmation modal
6. Integrate with Cognito for role changes

**Testing**:
- Invite user
- Change user role
- Remove user
- Verify permissions updated

**Acceptance Criteria**:
- Team management UI functional
- Invitations sent via email
- Role changes applied in Cognito
- Remove working correctly

**AI-Assisted Timeline**: 8 hours

---

### Task 11.x: Password-Reset UI (Webui — Deferred)

**STATUS (docs-mvp-backend-features pass): Deferred backup-auth UX work for webui Phase 11.**

Implement password-reset UI in webui (uses Cognito `ForgotPassword` / `ConfirmForgotPassword` directly, client-side via the Cognito SDK). **Deferred from this docs pass; api-dynamo does not expose forgot-password in MVP** (per Section 9 of the source plan / Task 3.4 above). Recorded here so the work doesn't get lost.

- Implementation: webui-side only; talks directly to Cognito.
- No api-dynamo route involved.
- Triggered from the existing password login screen (a "Forgot password?" link).
- AI-Assisted Timeline: ~6 hours (deferred; not counted in MVP totals).

---

**Phase 11 Total Duration**: 10-14 days
**Phase 11 Success Criteria**:
- Dashboard for all 8 roles
- Trail system CRUD UI complete
- Care report management UI complete
- Analytics dashboards functional
- Bulk operations working
- Tag management UI complete
- User management UI complete
- All interfaces mobile responsive

---

## Phase 12: Mobile Apps (Android + iOS)

**Objective**: Create User and Admin mobile apps for both Android and iOS with offline support (REQUIRED for MVP)

**Duration**: 30-50 days (longest single phase — Android-first, then iOS parallel)
**Priority**: CRITICAL (cannot launch without mobile apps)
**Dependencies**: Phases 3, 7, 9, 10 complete (authentication, status management, care reports, notifications)

**FOUR APPS REQUIRED (Two per Platform)**:
1. **Android User App** (com.traillens.app): 36 screens — trail discovery, condition viewing, care reports, TrailPulse, offline support
2. **Android Admin App** (com.traillens.admin): 42 screens — condition management, care reports admin, team/user management
3. **iOS User App**: Feature parity with Android User App
4. **iOS Admin App**: Feature parity with Android Admin App

**Android Platform**: Android 12+ (API 31+), Kotlin 2.0+, Jetpack Compose, Material Design 3
**iOS Platform**: iOS 16+, Native Swift, SwiftUI
**Android Distribution**: Google Play internal testing track for MVP beta
**iOS Distribution**: TestFlight for MVP beta
**Repositories**: `androiduser/`, `androidadmin/` (Android), separate iOS repository (not in main workspace)
**Design**: Figma mockups driving all screen designs (see `docs/MOBILEAPP_SCREENS.md` in each repo)
**Post-MVP**: Consider consolidating User + Admin into single app per platform

---

### Task 12.1: Set Up Android Development Environment and Repositories

**Objective**: Initialize Android project structure (already in progress)

**Key References**:
- `androiduser/docs/MOBILEAPP_SCREENS.md` — 36 screens for User App
- `androidadmin/docs/MOBILEAPP_SCREENS.md` — 42 screens for Admin App
- `androiduser/app/CODE_STRUCTURE.md` — Architecture and file organization rules
- `androidadmin/app/CODE_STRUCTURE.md` — Architecture and file organization rules

**Tech Stack**:
- Kotlin 2.0+, Jetpack Compose, Material Design 3
- Hilt for dependency injection
- Retrofit + OkHttp for networking
- Room for offline database
- Firebase Cloud Messaging for push notifications
- Coil for image loading
- Gradle with version catalog (`gradle/libs.versions.toml`)
- Android Credential Manager for passkeys

**Implementation Steps**:
1. Android repositories already created (`androiduser/`, `androidadmin/`)
2. Gradle project structure configured with version catalog
3. CODE_STRUCTURE.md files in place for both apps
4. Figma connection configured (`docs/FIGMA_CONFIG.md`, `docs/FIGMA_CONNECTION.md`)
5. Configure CI/CD with GitHub Actions
6. Set up Google Play internal testing track

**Acceptance Criteria**:
- Both Android projects building successfully
- Figma mockups accessible for development
- CI/CD pipeline running

**AI-Assisted Timeline**: 4 hours

---

### Task 12.2: Implement Android User App - Trail System Discovery

**Objective**: Browse and view trail systems with current conditions (7 screens in Trail Discovery section)

**Screens**: Browse Trail Systems, Trail System Detail, Condition History, Search Filters, Map View, Subscribe Dialog, Subscription Confirmation

**UI Features**:
- LazyColumn list of trail systems (nearby or subscribed)
- Search and filter with Compose state management
- Trail system detail page with condition display
- Condition history timeline
- Photos gallery with Coil image loading
- Subscribe/unsubscribe with confirmation

**Implementation Steps**:
1. Create Compose screens following CODE_STRUCTURE.md feature-based organization
2. Implement ViewModels with Hilt injection
3. Integrate with API via Retrofit (/trail-systems endpoints)
4. Implement location-based sorting (nearby first)
5. Add pull-to-refresh with SwipeRefresh
6. Create detail page with all info
7. Test on emulator and device

**Acceptance Criteria**:
- List view functional with LazyColumn
- Detail view complete with condition display
- Search working
- Subscribe/unsubscribe working

**AI-Assisted Timeline**: 16 hours

---

### Task 12.3: Implement Android User App - Care Report Submission

**Objective**: Allow users to submit care reports with camera integration (5 screens in Care Reports section)

**Screens**: Create Report, Select Trail System, Add Photo, Report Detail, Add Comment

**UI Features**:
- Report submission form with Compose
- CameraX integration (take photos)
- PhotoPicker API for gallery selection
- Preview before submit
- Success confirmation

**Implementation Steps**:
1. Create report submission Compose screens
2. Integrate CameraX for camera capture
3. Implement photo selection (up to 5 photos) via PhotoPicker API
4. Add location capture (GPS via FusedLocationProviderClient)
5. Implement photo upload to S3 via presigned URLs
6. Call API POST /care-reports via Retrofit
7. Show loading state during upload
8. Display success message

**Acceptance Criteria**:
- Camera integration working via CameraX
- Photo upload functional
- Location capture working
- Report creation successful

**AI-Assisted Timeline**: 12 hours

---

### Task 12.4: Implement Android User App - Offline Support

**Objective**: Cache trail system conditions and create reports offline with auto-upload

**Storage**: Room database for offline queue and status caching (complex objects with relationships to photos)

**Offline Queue Logic**:
1. When offline, save report to local Room database
2. Mark as "pending_sync"
3. Show "Offline - will sync when online" message
4. When online, automatically upload pending reports via WorkManager
5. Update UI when sync completes
6. Show "Syncing X reports..." notification
7. Handle sync failures (retry with exponential backoff)
8. Delete successfully synced reports from queue
9. Warn user if queue older than 7 days

**Caching Logic**:
1. Cache trail system data in Room database
2. Include cached_at timestamp
3. When offline, load from cache
4. Show "Cached X hours ago" warning if data stale
5. Auto-refresh when online
6. Expire cache after 7 days (force refresh)

**Implementation Steps**:
1. Define Room entities and DAOs for offline reports and cached trail systems
2. Implement network reachability detection
3. Create WorkManager workers for background sync
4. Implement retry logic with exponential backoff
5. Show sync status in UI
6. Add 7-day warning for old queued reports
7. Test with airplane mode

**Acceptance Criteria**:
- Offline report creation working
- Auto-sync on connection restore via WorkManager
- 7-day cache expiration
- Stale data warning displayed

**AI-Assisted Timeline**: 16 hours

---

### Task 12.5: Implement Android User App - Push Notifications (FCM)

**Objective**: Receive push notifications via Firebase Cloud Messaging

**Implementation Steps**:
1. Configure Firebase project and add `google-services.json`
2. Implement `FirebaseMessagingService` for token registration
3. Register device token with API (POST /devices)
4. Create notification channels: Trail Conditions, Care Reports, Assignments
5. Handle notification receipt (app in foreground, background, closed)
6. Implement deep linking via Navigation Compose (tap notification → trail detail)
7. Show notification badge count
8. Handle notification settings

**Deep Link Schemas**:
- `traillenshq://trail-system/{id}` → Trail system detail
- `traillenshq://care-report/{id}` → Care report detail
- `traillenshq://notifications` → Notifications list

**Acceptance Criteria**:
- FCM push notifications received
- Notification channels configured
- Deep linking working via Navigation Compose
- Badge count accurate

**AI-Assisted Timeline**: 10 hours

---

### Task 12.6: Implement Android User App - Authentication

**Objective**: Support all five authentication methods

**Implementation Steps**:
1. Integrate AWS Amplify for Android (Cognito)
2. Implement passwordless (email-first) login
3. Implement magic link with deep linking
4. Implement passkey authentication via Android Credential Manager API
5. Implement social login (Google/Apple/Facebook)
6. Implement admin login (hidden, for testing)
7. Store tokens securely in EncryptedSharedPreferences
8. Implement token refresh with AuthInterceptor
9. Create unified login UI with Compose

**Acceptance Criteria**:
- All five auth methods working
- Biometric prompts functional via Credential Manager
- Tokens stored securely in EncryptedSharedPreferences
- Session persistence working

**AI-Assisted Timeline**: 16 hours

---

### Task 12.7: Implement Android Admin App - Conditions Management

**Objective**: Admin app for managing trail system conditions from field (6 screens in Conditions section)

**Screens**: Conditions List, Update Condition, Trail System Detail, Condition History, Schedule Changes, Manage Condition Types

**UI Features**:
- List trail systems for organization with current conditions
- Quick condition update (one-tap)
- Full condition update (reason, photos, tags)
- Schedule future condition changes
- Manage condition types for organization
- Admin role validation gate (requires `trail-admin`, `trailsystem-owner`, or `admin` Cognito group)

**Implementation Steps**:
1. Create admin-specific Compose screens
2. Implement RoleValidator for admin group check
3. Implement quick condition buttons (Open, Closed, Caution)
4. Implement full condition update form
5. Add condition type management CRUD
6. Verify role-based access on every screen

**Acceptance Criteria**:
- Admin UI distinct from user app
- Quick condition update working
- Full condition update working
- Role verification functional via RoleValidator

**AI-Assisted Timeline**: 12 hours

---

### Task 12.8: Implement Android Admin App - Care Reports Admin

**Objective**: Complete care report management for trail crew (6 screens in Care Reports Admin section)

**Screens**: Reports List, Report Detail, Create Report, Assign Report, Update Status, Add Comment

**UI Features**:
- List all care reports (public + private)
- Create private work log (quick form)
- View report detail
- Assign to crew member or self
- Update status (Open → In Progress → Resolved → Closed)
- Add comments with photos
- Change priority (P1-P5)
- View activity log

**Implementation Steps**:
1. Create all Compose screens
2. Implement filtering and sorting
3. Add assignment interface
4. Implement status workflow
5. Create comment form with photo upload
6. Add priority editor
7. Test all CRUD operations

**Acceptance Criteria**:
- Full CRUD functional
- Assignment working
- Status workflow complete
- Comments with photos working

**AI-Assisted Timeline**: 16 hours

---

### Task 12.9: Implement Android Admin App - Team/User Management

**Objective**: Manage team members and roles (5 screens in Users/Team section)

**Screens**: Members List, User Detail, Change Role, Remove User, Add User

**UI Features**:
- List organization members with roles
- Invite new users
- Change user roles (org-admin, trailsystem-crew, trailsystem-owner, etc.)
- Remove users from organization
- View user activity

**Implementation Steps**:
1. Create team management Compose screens
2. Implement user invitation flow
3. Add role management (dropdown with Cognito groups)
4. Implement user removal with confirmation
5. Role-gate all admin actions

**Acceptance Criteria**:
- Member list functional
- Invitation working
- Role management functional
- User removal working with confirmation

**AI-Assisted Timeline**: 8 hours

---

### Task 12.10: Android Testing and Internal Distribution

**Objective**: Test both Android apps and distribute via Google Play internal testing

**Implementation Steps**:
1. Run unit tests (90% coverage target)
2. Run Compose UI tests for critical flows
3. Performance testing: cold start <1.5s, 60fps scrolling, <15MB APK
4. Test on multiple device sizes (phone, tablet)
5. Create Google Play internal testing track listing
6. Upload signed APK/AAB to Play Console
7. Invite pilot testers via email
8. Create testing instructions document
9. Monitor crash reports via Firebase Crashlytics

**Acceptance Criteria**:
- Both apps passing all tests
- Performance targets met
- Apps on Google Play internal testing track
- Pilot users invited

**AI-Assisted Timeline**: 6 hours

---

### Task 12.11: Set Up iOS Development Environment and Repositories

**Objective**: Initialize iOS project structure

**Research Completed**: AWS SDK for iOS reaches End of Support on August 1, 2026. MUST use AWS Amplify for Swift (v2) instead. Amplify provides modern Swift APIs with async/await, better SwiftUI integration, and long-term support.

**Key References**:
- [AWS SDK for iOS End of Support Notice](https://github.com/aws-amplify/aws-sdk-ios)
- [AWS Amplify for Swift Documentation](https://docs.amplify.aws/gen1/swift/prev/build-a-backend/auth/existing-resources/)

**Critical Decision**: Use AWS Amplify for Swift (v2) instead of deprecated AWS SDK for iOS.

**Implementation Steps**:
1. Create new iOS repository (separate from main workspace)
2. Initialize Xcode project with two app targets:
   - TrailLensHQ (User App)
   - TrailLensHQ Admin (Admin App)
3. Configure Swift Package Manager for dependencies:
   - **AWS Amplify for Swift** (auth, storage, API, notifications) - REQUIRED
   - Kingfisher or SDWebImage (image loading/caching)
   - SwiftUI native components (preferred over third-party)
4. Set up project structure:
   - Shared code (Models, NetworkingManager, AuthenticationManager)
   - User app specific views
   - Admin app specific views
5. Configure build settings and signing
6. Set up TestFlight distribution
7. Add .gitignore for Xcode

**Acceptance Criteria**:
- iOS project initialized
- Two app targets configured
- Dependencies installed
- TestFlight ready

**AI-Assisted Timeline**: 4 hours

---

### Task 12.12: Implement iOS User App - Trail System Discovery

**Objective**: Browse and view trail systems with current conditions (feature parity with Android Task 12.2)

**UI Features**:
- SwiftUI List of trail systems (nearby or subscribed)
- Search and filter
- Trail system detail page with condition display
- Condition history timeline
- Photos gallery
- Subscribe/unsubscribe button

**Implementation Steps**:
1. Create SwiftUI views (leveraging Android patterns for API integration)
2. Integrate with API (/trail-systems endpoints) using Amplify/URLSession
3. Implement location-based sorting (nearby first) via CoreLocation
4. Add pull-to-refresh
5. Implement search
6. Create detail page with all info
7. Add photo gallery
8. Test on simulator and device

**Acceptance Criteria**:
- List view functional
- Detail view complete
- Search working
- Subscribe/unsubscribe working

**AI-Assisted Timeline**: 12 hours

---

### Task 12.13: Implement iOS User App - Care Report Submission

**Objective**: Allow users to submit care reports with camera integration (feature parity with Android Task 12.3)

**UI Features**:
- Report submission form in SwiftUI
- Camera integration via UIImagePickerController
- Photo library picker via PHPickerViewController
- Preview before submit
- Success confirmation

**Implementation Steps**:
1. Create report submission SwiftUI views
2. Integrate UIImagePickerController for camera
3. Implement photo selection (up to 5 photos)
4. Add location capture (GPS via CoreLocation)
5. Implement photo upload to S3
6. Call API POST /care-reports
7. Show loading state during upload
8. Display success message

**Acceptance Criteria**:
- Camera integration working
- Photo upload functional
- Location capture working
- Report creation successful

**AI-Assisted Timeline**: 10 hours

---

### Task 12.14: Implement iOS User App - Offline Support, Push Notifications, and Authentication

**Objective**: Complete iOS user app with offline, push, and auth (feature parity with Android Tasks 12.4-12.6)

**Storage Decision**: Use Core Data for offline report queue and status caching (consistency with iOS patterns, complex objects with relationships to photos)

**Offline Queue Logic**: Same as Android (Task 12.4) — save to Core Data, mark pending_sync, auto-upload on reconnect, 7-day warning

**Push Notifications**: APNS via AWS SNS
1. Request notification permissions on app launch
2. Register device token with API (POST /devices)
3. Handle notification receipt (foreground, background, closed)
4. Implement deep linking (tap notification → trail detail)

**Authentication**: All five methods
1. Integrate AWS Amplify for Swift (Cognito)
2. Implement passkey with ASAuthorizationController
3. Implement magic link with deep linking
4. Store tokens securely in iOS Keychain
5. Implement token refresh

**Deep Link Schemas**:
- `traillenshq://trail-system/{id}` → Trail system detail
- `traillenshq://care-report/{id}` → Care report detail
- `traillenshq://notifications` → Notifications list

**Acceptance Criteria**:
- Offline report creation working with Core Data
- Auto-sync on connection restore
- Push notifications received via APNS
- Deep linking working
- All five auth methods working
- Tokens stored securely in Keychain

**AI-Assisted Timeline**: 20 hours

---

### Task 12.15: Implement iOS Admin App

**Objective**: Complete iOS admin app with conditions management, care reports admin, and team management (feature parity with Android Tasks 12.7-12.9)

**UI Features (SwiftUI)**:
- Conditions management: quick update, full condition form, condition type management, schedule changes
- Care reports admin: full CRUD, assignment, status workflow, comments with photos
- Team management: member list, invite, role management, user removal
- Admin role validation gate (same logic as Android RoleValidator)

**Implementation Steps**:
1. Create admin-specific SwiftUI views (leveraging Android patterns)
2. Implement role validation for admin group check
3. Implement conditions management screens
4. Implement care report admin screens
5. Implement team/user management screens
6. Add push notification channels for admin-specific events
7. Test all admin workflows

**Acceptance Criteria**:
- Admin UI distinct from user app
- All conditions management working
- Full care report CRUD functional
- Team management functional
- Role verification working

**AI-Assisted Timeline**: 20 hours

---

### Task 12.16: Implement iOS Deep Linking and Notification Handling

**Objective**: Configure URL schemes and deep linking for iOS notifications

**Implementation Steps**:
1. Configure URL schemes in Xcode
2. Implement deep link routing via SwiftUI navigation
3. Handle links when app closed, background, foreground
4. Extract parameters from URL
5. Navigate to appropriate view
6. Test all link types

**Acceptance Criteria**:
- Deep linking functional
- Works in all app states
- Parameters extracted correctly

**AI-Assisted Timeline**: 4 hours

---

### Task 12.17: iOS Testing and TestFlight Distribution

**Objective**: Test both iOS apps and distribute via TestFlight

**Implementation Steps**:
1. Run unit tests (90% coverage target)
2. Run SwiftUI preview tests for critical flows
3. Performance testing: cold start <3s, smooth scrolling
4. Test on multiple device sizes (iPhone, iPad)
5. Create App Store Connect records for both apps
6. Configure app metadata (name, description, icons)
7. Set up TestFlight groups:
   - Internal Testing (development team)
   - External Testing (Hydrocut + GORBA)
8. Upload first build to TestFlight
9. Invite pilot users via email
10. Create testing instructions document
11. Monitor crash reports

**Acceptance Criteria**:
- Both apps passing all tests
- Both apps in TestFlight
- Pilot users invited
- Testing instructions sent

**AI-Assisted Timeline**: 6 hours

---

**Phase 12 Total Duration**: 30-50 days
**Phase 12 Success Criteria**:
- Android User App (36 screens) complete with:
  - Trail system discovery and condition viewing
  - Care report submission with camera (CameraX)
  - View public care reports
  - TrailPulse condition observations
  - Offline report creation (Room, 7-day queue)
  - Push notifications (FCM via AWS SNS)
  - Offline status caching (Room, 7 days)
- Android Admin App (42 screens) complete with:
  - Conditions management (quick update + full form)
  - Full care report CRUD with assignment workflow
  - Team/user management
  - TrailPulse observation management
  - Admin role validation gate
- iOS User App complete with feature parity (SwiftUI, Core Data, APNS)
- iOS Admin App complete with feature parity (SwiftUI, Core Data, APNS)
- Authentication with all five methods on both platforms (passwordless, magic link, passkey, social, admin login)
- Android: Google Play internal testing track distribution
- iOS: TestFlight distribution
- Deep linking functional on both platforms
- All apps available for pilot testing
- Performance: Android cold start <1.5s, 60fps, <15MB APK; iOS cold start <3s

---

## Phase 13: Pilot Onboarding

**Objective**: Onboard Hydrocut and GORBA organizations with white-glove support

**Duration**: 3-5 days
**Priority**: CRITICAL (validates MVP)
**Dependencies**: Phases 11-12 complete (webui dashboards and mobile apps ready)

### Task 13.1: Create Hydrocut Organization and Trail System

**Objective**: Set up Hydrocut in production

**Implementation Steps**:
1. Create organization record: Hydrocut
2. Create admin user account for Hydrocut primary contact
3. Create 1 trail system:
   - Hydrocut Trail System (Kitchener-Waterloo, ON - includes Glasgow and Synders areas)
4. Upload cover photo for trail system
5. Set initial status (Open)
6. Create default status tags and care report type tags
7. Invite 3-5 trail crew members
8. Assign roles (org-admin, trailsystem-crew)

**Acceptance Criteria**:
- Hydrocut org created
- 1 trail system configured
- Users invited and assigned roles

**AI-Assisted Timeline**: 4 hours

---

### Task 13.2: Create GORBA Organization and 2 Trail Systems

**Objective**: Set up GORBA in production

**Implementation Steps**:
1. Create organization record: GORBA
2. Create admin user account
3. Create 2 trail systems:
   - Guelph Lake Trail System (Guelph, ON)
   - Akell Trail System (Guelph, ON)
4. Upload cover photos
5. Set initial statuses
6. Create default tags
7. Invite 3-5 trail crew members
8. Assign roles

**Acceptance Criteria**:
- GORBA org created
- 2 trail systems configured
- Users invited

**AI-Assisted Timeline**: 4 hours

---

### Task 13.3: Configure Status Types for Each Organization

**Objective**: Set up custom status types matching each organization's needs

**Implementation Steps**:
1. Interview each organization about their status needs
2. Create custom status types (beyond defaults)
3. Configure default tags for common scenarios
4. Set up care report type tags based on common issues
5. Document status workflow for each org

**Acceptance Criteria**:
- Custom status types configured
- Tags set up
- Workflows documented

**AI-Assisted Timeline**: 4 hours

---

### Task 13.4: Invite and Train Key Admins and Trail Crew

**Objective**: Get pilot users set up and trained

**Implementation Steps**:
1. Send invitation emails to all pilot users
2. Schedule live training sessions (Zoom):
   - Session 1: Org-admin training (2 hours)
   - Session 2: Trail crew training (1.5 hours)
3. Provide training materials:
   - User guide PDFs
   - Video tutorials
   - Quick reference cards
4. Set up dedicated support channel (Slack or email)
5. Provide 1-on-1 onboarding for admins

**Acceptance Criteria**:
- All users invited
- Training sessions conducted
- Support channel active
- Materials distributed

**AI-Assisted Timeline**: 12 hours (including preparation and sessions)

---

### Task 13.5: Conduct Live Training Sessions

**Objective**: Hands-on training for pilot organizations

**Training Agenda - Org-Admin Session (2 hours)**:
1. Platform overview (15 min)
2. Trail system management (30 min)
   - Create, edit, delete
   - Status updates with photos
3. Team management (20 min)
   - Invite users
   - Assign roles
4. Care report management (30 min)
   - View reports
   - Assignment workflow
5. Analytics and reporting (15 min)
6. Q&A (10 min)

**Training Agenda - Trail Crew Session (1.5 hours)**:
1. Platform overview (10 min)
2. Status updates from field (20 min)
   - Quick status update
   - Add photos and reason
3. Care report submission (30 min)
   - Submit public report
   - Create private work log
4. Offline features (20 min)
   - Offline report creation
   - Offline status viewing
5. Q&A (10 min)

**Acceptance Criteria**:
- Both sessions conducted
- All attendees comfortable with platform
- Questions answered

**AI-Assisted Timeline**: 4 hours (delivery time)

---

### Task 13.6: Provide White-Glove Onboarding Support

**Objective**: Ensure smooth first 30 days

**Support Plan**:
- Week 1: Daily check-ins via Slack/email
- Week 2-4: Every other day check-ins
- Dedicated support response time: <2 hours
- Monthly feedback calls
- Bug fix priority: <24 hour response

**Implementation Steps**:
1. Set up Slack workspace for pilot organizations
2. Create #support, #feedback, #announcements channels
3. Monitor daily activity
4. Proactively reach out with tips
5. Collect feedback weekly
6. Address issues immediately
7. Celebrate wins (first status update, first care report, etc.)

**Acceptance Criteria**:
- Support channels active
- Daily check-ins first week
- All issues resolved quickly
- Feedback collected

**AI-Assisted Timeline**: Ongoing throughout pilot

---

### Task 13.7: Set Up TestFlight for Pilot Users

**Objective**: Distribute mobile apps to pilot users

**Implementation Steps**:
1. Add pilot user emails to TestFlight
2. Send TestFlight invitations
3. Provide installation instructions
4. Help users install apps on their devices (Android via Play Store internal track, iOS via TestFlight)
5. Verify all users successfully installed
6. Provide app usage guide

**Acceptance Criteria**:
- All pilot users invited to TestFlight
- Apps successfully installed
- Users comfortable with app

**AI-Assisted Timeline**: 2 hours

---

**Phase 13 Total Duration**: 3-5 days
**Phase 13 Success Criteria**:
- All 3 trail systems operational (Hydrocut: 1, GORBA: 2)
- All admins and trail crew trained
- TestFlight apps distributed
- Support channels active
- First status updates posted
- First care reports submitted
- Pilot organizations satisfied with onboarding

---

## Phase 14: Testing and Validation

**Objective**: Comprehensive testing before production launch

**Duration**: 7-10 days
**Priority**: CRITICAL (final quality gate)
**Dependencies**: Phase 13 complete (pilot setup done)

### Task 14.1: End-to-End Testing (Full User Workflows)

**Objective**: Test complete user journeys

**Workflows to Test**:

**Workflow 1: Trail User Journey**
1. Register account
2. Browse trail systems
3. Subscribe to trail system
4. Receive notification when status changes
5. Submit care report with photos
6. Track care report status

**Workflow 2: Trail Crew Journey**
1. Login with passkey
2. View assigned care reports
3. Update trail system status from field
4. Create private work log
5. Assign care report to colleague
6. Add comment to care report

**Workflow 3: Org-Admin Journey**
1. Create new trail system
2. Invite trail crew member
3. Bulk update multiple trail systems
4. View analytics dashboard
5. Manage status tags
6. Review care reports

**Implementation Steps**:
1. Create detailed test scripts for each workflow
2. Execute workflows in dev environment
3. Execute workflows in prod environment
4. Document any issues found
5. Verify all issues resolved
6. Re-test failed workflows

**Acceptance Criteria**:
- All workflows complete successfully
- No critical bugs found
- Performance acceptable

**AI-Assisted Timeline**: 16 hours

---

### Task 14.2: Security Testing (Penetration Testing, Vulnerability Scanning)

**Objective**: Verify security hardening

**Tests to Perform**:

1. CloudTrail log verification
2. Penetration testing (manual or automated)
3. OWASP Top 10 vulnerability scan
4. SQL injection testing
5. XSS testing
6. CSRF protection verification
7. Authorization bypass attempts
8. Secrets scanning (no credentials in code)

**Tools to Use**:

- OWASP ZAP or Burp Suite (manual pen testing)
- Trufflehog (secrets scanning)
- npm audit / pip-audit (dependency vulnerabilities)

**Implementation Steps**:
1. Run automated security scans
2. Conduct manual pen testing
3. Document all findings
4. Prioritize findings (Critical, High, Medium, Low)
5. Fix critical and high findings
6. Re-test after fixes
7. Create security report for CEO

**Acceptance Criteria**:

- No critical vulnerabilities
- High vulnerabilities addressed
- Security report prepared

**AI-Assisted Timeline**: 12 hours

---

### Task 14.3: Performance Testing (API Response Times, Notification Latency)

**Objective**: Verify performance targets

**Performance Targets**:
- API response time: <500ms (p95)
- Push notification latency: <2 minutes
- Email delivery: <5 seconds
- Photo load time: <100ms (via CloudFront)
- Search query: <200ms for <500 trail systems

**Tests to Perform**:
1. API endpoint benchmarking (all major endpoints)
2. Database query performance testing
3. Notification delivery time measurement
4. Photo load time testing
5. Web page load time testing
6. Mobile app responsiveness testing

**Tools to Use**:
- Artillery or k6 (load testing)
- AWS CloudWatch (latency metrics)
- Lighthouse (web page performance)
- Xcode Instruments (iOS app profiling)

**Implementation Steps**:
1. Set up load testing scripts
2. Run performance benchmarks
3. Identify slow endpoints
4. Optimize slow queries
5. Add caching where needed
6. Re-test after optimizations
7. Document performance results

**Acceptance Criteria**:
- All performance targets met
- No endpoints >500ms
- Notification latency <2 min
- Performance report prepared

**AI-Assisted Timeline**: 12 hours

---

### Task 14.4: Load Testing (Simulate 100+ Users)

**Objective**: Verify platform can handle concurrent users

**Load Tests**:
1. 100 concurrent users browsing trail systems
2. 50 users updating trail status simultaneously
3. 25 users submitting care reports with photos
4. 1000 push notifications sent simultaneously
5. 500 emails sent simultaneously

**Implementation Steps**:
1. Create load testing scenarios with Artillery
2. Run load tests against dev environment
3. Monitor CloudWatch metrics during tests
4. Identify bottlenecks (Lambda throttling, DynamoDB limits, etc.)
5. Increase concurrency limits if needed
6. Add caching or optimization
7. Re-run load tests

**Acceptance Criteria**:
- System handles 100+ concurrent users
- No throttling errors
- Response times remain <500ms under load

**AI-Assisted Timeline**: 8 hours

---

### Task 14.5: User Acceptance Testing with Pilot Organizations

**Objective**: Get real user feedback

**UAT Process**:
1. Ask pilot organizations to use platform for 1 week
2. Provide UAT checklist:
   - Create trail system ✓
   - Update status ✓
   - Submit care report ✓
   - Receive notification ✓
   - etc.
3. Collect feedback via:
   - Daily check-ins
   - Weekly survey
   - One-on-one interviews
4. Document all feedback
5. Prioritize feedback (Must-fix, Nice-to-have)
6. Address must-fix issues
7. Get sign-off from pilot organizations

**Acceptance Criteria**:
- UAT completed by both pilot orgs
- All must-fix issues addressed
- Pilot orgs satisfied (NPS >50)

**AI-Assisted Timeline**: 5 days (mostly pilot org time, not dev time)

---

### Task 14.6: Fix Critical Bugs and Issues

**Objective**: Zero critical bugs before launch

**Process**:
1. Collect all bugs from testing phases
2. Prioritize by severity:
   - P1 (Critical): Breaks core functionality, must fix
   - P2 (High): Significant issue, should fix
   - P3 (Medium): Minor issue, nice to fix
   - P4 (Low): Cosmetic, can defer
3. Fix all P1 bugs
4. Fix P2 bugs if time allows
5. Document P3/P4 bugs for post-launch
6. Retest all fixes
7. Verify no regressions

**Acceptance Criteria**:
- Zero P1 bugs
- <5 P2 bugs remaining
- All fixes tested
- Regression testing passed

**AI-Assisted Timeline**: Variable (depends on bug count, assume 20 hours)

---

**Phase 14 Total Duration**: 7-10 days
**Phase 14 Success Criteria**:
- End-to-end testing passed
- Security testing passed (>90% compliance score)
- Performance testing passed (all targets met)
- Load testing passed (100+ concurrent users)
- UAT completed and approved by pilot organizations
- All critical bugs fixed
- Zero P1 bugs remaining
- Platform ready for production launch

---

## Phase 15: TrailPulse - Trail Feedback and Usage Tracking (MVP-REQUIRED)

**Objective**: Implement trail feedback collection and GPS-based usage tracking system

**Duration**: 12-18 days
**Priority**: **MVP-REQUIRED** (user condition feedback is critical for trail management decisions)
**Dependencies**: Phases 5 (Trail System Model), 10 (Notifications), 12 (Mobile Apps for GPS)

**MVP Scope Note (docs-mvp-backend-features pass — REVISED)**: The MVP implements the **full 25 TrailPulse backend endpoints** (5 mobile + 2 web + 8 admin-config + 10 admin-feedback). Math: 8 mobile (original) − 2 ride start/end (mobile-local per F-AA) − 1 GET ride-count (mobile-local per F-BB) − 1 device-token (consolidated to `/api/users/me/devices` per F-CC) + 1 new `PUT /ride-completion` = **5 mobile**. iOS client deferred. Earlier "6 endpoints / 22 deferred" framing is superseded.

### Overview

TrailPulse is a privacy-first trail feedback and usage tracking system that enables trail system owners to gather rider feedback and track trail usage through GPS-based ride detection. The system uses GPS geofencing to detect when users visit subscribed trail systems, prompting them for post-ride feedback while maintaining strict privacy controls.

**Key Benefits:**
- Software-based trail counting (replaces expensive hardware counters)
- Real-time rider feedback on trail conditions
- Data-driven trail management decisions
- Privacy-first design with easy opt-out

**Scope for This Repo (docs-mvp-backend-features pass — REVISED)**:
- Backend API endpoints (**25 endpoints**: 5 mobile + 2 web + 8 admin-config + 10 admin-feedback)
- DynamoDB schema (**9 entity types** in single-table overlay; `TrailConditions` dropped per design overlap with Condition Catalog Phase 7.5; `RideEvents` dropped per privacy-first redesign)
- Web feedback submission form
- Admin configuration interface
- Admin feedback management interface
- **No** SNS push notification topic for post-ride feedback (mobile-local per F-Y); existing SNS used only for cross-user / admin events

**Mobile Team Scope (Separate Repository):**
- GPS tracking and geofence detection
- Mobile feedback form UI
- Device token registration
- Ride start/end event recording

---

### Task 15.1: Implement TrailPulse DynamoDB Schema (9 Entity Types — Privacy-First, Catalog-Driven)

**Objective**: Define **9 entity types** in the single-table overlay for TrailPulse data. **`TrailConditions` is dropped** per design overlap with Condition Catalog Phase 7.5 (per-trail-system feedback config now references `catalog_id`s instead of a standalone TrailConditions entity). **`RideEvents` is dropped** per privacy-first redesign (the backend never sees per-user ride records).

**The 9 entity types:**

1. **AdditionalQuestions** — Custom questions per trail system.
   - PK: `TRAILSYSTEM#{trail_system_id}`, SK: `QUESTION#{question_id}`
   - Attributes: question_text, question_type, options, frequency_threshold, is_enabled, display_order

2. **TrailSystemRideCount** — **Anonymous daily aggregate** (no user attribution).
   - PK: `TRAILSYSTEM#{trail_system_id}`, SK: `RIDECOUNT#{YYYY-MM-DD}`
   - Attributes: `total_rides` (atomic counter via `ADD`)
   - **TTL**: `now + 1095 days` (3-year retention per user direction). Long-term storage for analytics.

3. **RideCompletion** — **Anonymous idempotency marker**.
   - PK: `TRAILSYSTEM#{trail_system_id}`, SK: `RIDECOMPLETION#{ride_id}`
   - Attributes: `completed_at` only (no `user_id`, no `org_id` reverse lookup).
   - **TTL**: `now + 30 days` (short — only needed long enough to dedupe legitimate replays from offline-queued requests).
   - Co-located with the trail-system PK so the TransactWrite is a single-partition op.

4. **FeedbackResponses** — User responses to conditions and questions.
   - PK: `TRAILSYSTEM#{trail_system_id}`, SK: `FEEDBACK#{created_at}#{feedback_id}`
   - GSI1: `USER#{user_id}` for user feedback history (admins manage feedback per Tasks 15.5/15.9).
   - Attributes: `user_id`, `conditions[]` (catalog_id refs), `question_responses[]`, `comments`, `soft_deleted`, `deleted_at`, `deleted_by`, `deletion_reason`.
   - **No `ride_id` field** — backend has no per-user ride records per F-AA/BB; mobile keeps any local ride↔feedback linkage in its own Room DB.

5. **UserPreferences** — GPS opt-out and notification settings.
   - PK: `USER#{user_id}`, SK: `TRAILPULSE_PREFS`
   - Attributes: `gps_tracking_enabled`, `feedback_notifications_enabled`.
   - (Device tokens live in the existing `users/me/devices` entity, not here.)

6. **QuestionResponseTracker** — Count responses to trigger frequency logic.
   - PK: `USER#{user_id}#TRAILSYSTEM#{trail_system_id}`, SK: `QUESTION#{question_id}`
   - Attributes: `response_count`, `last_asked_at`.

7. **TrailSystemGeofences** — Boundary coordinates for each trail system.
   - PK: `TRAILSYSTEM#{trail_system_id}`, SK: `GEOFENCE`
   - Attributes: `geojson_boundaries`, `last_updated_at`, `updated_by`.

8. **CrewMembers** — Crew member status for feedback context.
   - PK: `TRAILSYSTEM#{trail_system_id}`, SK: `CREW#{user_id}`
   - GSI1: `USER#{user_id}` for user's crew memberships.
   - Attributes: `is_crew`, `crew_notes`, `assigned_at`, `assigned_by`.

9. **FeedbackDeletionAudit** — Audit log for deleted feedback.
   - PK: `FEEDBACK#{feedback_id}`, SK: `DELETED#{deleted_at}`
   - Attributes: `deleted_by`, `deletion_reason`, `was_soft_delete`.

**Per-trail-system feedback config (replaces the dropped `TrailConditions` entity)**: the `PUT /api/trailpulse/admin/trail-systems/{id}/conditions` endpoint stores an array of `{catalog_id, display_order, is_multiselect}` against the trail system. Single source of truth for "what conditions exist": the org `ConditionCatalogEntry` library (Phase 7.5).

**Single-partition TransactWrite for ride completion** (atomicity guarantee, 1 WCU effective):

1. `Put RIDECOMPLETION#{ride_id}` with `ConditionExpression: attribute_not_exists(SK)` (idempotency — duplicate ride_id aborts the txn cleanly with `ConditionalCheckFailed`, server returns 200 OK no-op).
2. `Update RIDECOUNT#{today}` with `ADD total_rides :one`.

**Implications for analytics**: per-trail-system daily totals are queryable for 3 years. **Unique-users-per-day is no longer derivable** from ride records (no user attribution at all). If the analytics dashboard wants "unique users", derive from distinct `FeedbackResponses.user_id` per day.

**Implementation Steps:**

1. Define DynamoDB single-table-overlay entities for all 9 types in `traillens_db`.
2. Configure TTL: 30 days on `RideCompletion`, 1095 days (3 years) on `TrailSystemRideCount`.
3. Set up GSI1 overloads for `FeedbackResponses` (user-history) and `CrewMembers` (user-memberships).
4. Configure on-demand capacity.
5. Deploy schema; verify creation and TTL config.
6. Run integration tests for the single-partition TransactWrite (ride-completion).

**Acceptance Criteria**:

- 9 entity types created (NOT 10 — `TrailConditions` and `RideEvents` dropped).
- TTL: 30 days on `RideCompletion`; 1095 days on `TrailSystemRideCount`.
- GSI1 overloads functional for user-history and user-memberships.
- Single-partition TransactWrite proven idempotent (duplicate `ride_id` returns no-op success).
- No `user_id` field on any ride-tracking entity (privacy-first verified).
- Per-trail-system feedback config references `catalog_id`s only (no embedded condition definitions).

**AI-Assisted Timeline**: 8 hours

---

### Task 15.2: Implement Mobile App API Endpoints (5 Endpoints — Privacy-First)

**Objective**: Create backend APIs for mobile feedback integration. **5 endpoints (was 8)** after the F-AA / F-BB / F-CC corrections.

**Endpoints to Implement (5):**

1. **`GET /api/trailpulse/geofences`** — geofence boundaries for the authenticated user's subscribed trail systems (mobile downloads once, matches on-device).
   - Returns: `{ trail_system_id, geojson_boundaries }[]`

2. **`GET /api/trailpulse/trail-systems/{id}/feedback-config`** — conditions (catalog-id refs) + questions for the feedback form. Checks question frequency logic for user.
   - Returns: `{ conditions: [{catalog_id, display_order, is_multiselect}, ...], additional_questions[] }`

3. **`POST /api/trailpulse/feedback`** — submit feedback (conditions[], question_responses[], comments). User-attributed for admin management per Tasks 15.5/15.9.
   - Body: `{ trail_system_id, conditions[], question_responses[], comments }` (**no `ride_id`** — backend doesn't track rides per F-AA/BB)
   - Creates FeedbackResponse record + updates QuestionResponseTracker.
   - Returns: `{ success, feedback_id }`

4. **`PUT /api/trailpulse/trail-systems/{trail_system_id}/ride-completion`** — **anonymous** ride-completion ping (NEW, replaces removed `/rides/start` and `/rides/end`).
   - Body: `{ ride_id: <client-uuid>, completed_at: <iso8601> }`
   - **Idempotent**: `ride_id` is the dedupe key (single-partition TransactWrite with `attribute_not_exists(SK)`).
   - **Auth**: any authenticated user (membership check required so we don't accept rides for trail systems the user isn't subscribed to, but the user's identity is **not stored** in the ride-completion record).
   - On success, single-partition TransactWrite: (a) put `RIDECOMPLETION#{ride_id}` marker with TTL=now+30d; (b) `ADD total_rides :one` on `RIDECOUNT#{YYYY-MM-DD}` with TTL=now+1095d.
   - Returns: `{ success: true }` (200 on first call, 200 no-op on duplicate).

5. **`PUT /api/trailpulse/user/preferences`** — GPS-tracking-enabled, feedback-notifications-enabled (this **is** user-scoped — preferences belong to the user).
   - Body: `{ gps_tracking_enabled, feedback_notifications_enabled }`
   - Returns: `{ success }`

**REMOVED endpoints (with rationale):**

- ~~`POST /api/trailpulse/rides/start`~~ — mobile-only via geofence entry detection (F-AA).
- ~~`POST /api/trailpulse/rides/end`~~ — mobile-only via geofence exit detection; local notification per F-Y.
- ~~`GET /api/trailpulse/user/ride-count/{trail_system_id}`~~ — mobile keeps any "you've ridden here N times" UX in local Room DB only (F-BB privacy-first).
- ~~`POST /api/trailpulse/device-token`~~ — duplicate of existing `/api/users/me/devices` route (F-CC); single canonical device-registration route used for ALL push paths.

**Implementation Steps:**

1. Create Lambda handlers in `api-dynamo/` for each of the 5 endpoints.
2. Implement input validation and authentication.
3. Implement subscription/membership check on `PUT /ride-completion` (without storing user identity in the record).
4. Configure API Gateway routes.
5. Add endpoint documentation.
6. Write unit tests for each endpoint.
7. Integration testing with focus on the anonymous ride-completion idempotency path.

**Acceptance Criteria**:

- All 5 mobile endpoints functional.
- Authentication required on all endpoints.
- `PUT /ride-completion` is idempotent (duplicate `ride_id` returns success no-op).
- No `user_id` written to `RIDECOMPLETION` or `TRAILSYSTEMRIDECOUNT` items (verified via DynamoDB inspection in tests).
- No `/rides/start`, `/rides/end`, `/user/ride-count`, or `/device-token` route exists (verified by openapi.json scan).

**AI-Assisted Timeline**: 12 hours

---

### Task 15.3: Implement Web Feedback Endpoints (2 Endpoints)

**Objective**: Create web interface for manual feedback submission

**Endpoints to Implement:**

1. `GET /api/trailpulse/trail-systems/subscribed`
   - Returns user's subscribed trail systems for feedback dropdown
   - Requires authentication
   - Returns: `{ trail_system_id, name, organization }[]`

2. `POST /api/trailpulse/feedback/web`
   - Body: `{ trail_system_id, conditions[], question_responses[], comments }`
   - Creates feedback response without ride_id (web submission)
   - Returns: `{ success, feedback_id }`

**Implementation Steps:**
1. Create Lambda handlers in `api-dynamo/`
2. Implement authentication middleware
3. Query user subscriptions from existing subscription table
4. Create feedback response logic (shared with mobile endpoint)
5. Configure API Gateway routes
6. Write unit tests
7. Integration testing

**Acceptance Criteria**:
- Both web endpoints functional
- Authentication working
- Feedback submissions recorded correctly
- Web feedback distinguishable from mobile feedback

**AI-Assisted Timeline**: 4 hours

---

### Task 15.4: Implement Admin Configuration Endpoints (8 Endpoints)

**Objective**: Trail system owner configuration APIs

**Endpoints to Implement:**

1. `GET /api/trailpulse/admin/trail-systems/{id}/config`
2. `PUT /api/trailpulse/admin/trail-systems/{id}/conditions`
3. `POST /api/trailpulse/admin/trail-systems/{id}/questions`
4. `PUT /api/trailpulse/admin/trail-systems/{id}/questions/{question_id}`
5. `DELETE /api/trailpulse/admin/trail-systems/{id}/questions/{question_id}`
6. `GET /api/trailpulse/admin/trail-systems/{id}/usage`
7. `PUT /api/trailpulse/admin/trail-systems/{id}/geofence`
8. `GET /api/trailpulse/admin/trail-systems/{id}/geofence`

**Implementation Steps:**
1. Create Lambda handlers for CRUD operations
2. Implement org-admin authorization checks
3. Implement condition and question management logic
4. Implement geofence CRUD with validation
5. Implement usage statistics aggregation
6. Configure API Gateway routes
7. Write unit tests
8. Integration testing

**Acceptance Criteria**:
- All 8 admin config endpoints functional
- Proper authorization (org-admin+ only)
- Geofence validation working
- Usage stats accurate

**AI-Assisted Timeline**: 12 hours

---

### Task 15.5: Implement Admin Feedback Management Endpoints (10 Endpoints)

**Objective**: Feedback viewing, filtering, and management APIs

**Endpoints to Implement:**

1. `GET /api/trailpulse/admin/trail-systems/{id}/feedback` - Paginated feedback with filters
2. `GET /api/trailpulse/admin/trail-systems/{id}/feedback/{feedback_id}` - Single feedback detail
3. `DELETE /api/trailpulse/admin/trail-systems/{id}/feedback/{feedback_id}` - Delete single
4. `POST /api/trailpulse/admin/trail-systems/{id}/feedback/bulk-delete` - Bulk delete
5. `POST /api/trailpulse/admin/trail-systems/{id}/feedback/delete-by-filter` - Filter-based delete
6. `GET /api/trailpulse/admin/trail-systems/{id}/feedback/statistics` - Aggregated stats
7. `GET /api/trailpulse/admin/trail-systems/{id}/users/{user_id}/feedback` - User feedback history
8. `PUT /api/trailpulse/admin/trail-systems/{id}/users/{user_id}/crew-status` - Crew member flag
9. `GET /api/trailpulse/admin/trail-systems/{id}/crew-members` - List crew members
10. `POST /api/trailpulse/admin/trail-systems/{id}/crew-members/bulk` - Bulk crew assignment

**Implementation Steps:**
1. Implement feedback query with pagination and filters
2. Implement soft delete and audit logging
3. Implement bulk delete operations
4. Implement feedback statistics aggregation
5. Implement crew member management
6. Configure API Gateway routes
7. Write unit tests for complex queries
8. Integration testing

**Acceptance Criteria**:
- All 10 feedback management endpoints functional
- Pagination working correctly
- Filters combining properly (date, condition, user, text search)
- Soft delete and audit trail working
- Crew member management functional

**AI-Assisted Timeline**: 16 hours

---

### Task 15.6: Implement Local Post-Ride Notification (Mobile) — REWRITTEN per F-Y

**Objective**: Fire the post-ride feedback notification **locally on the mobile device** when the on-device geofence detects ride-end. **This is mobile-app scope, NOT backend scope** (per docs-mvp-backend-features pass F-Y).

**ARCHITECTURE CORRECTION**: The previous "Implement SNS Push Notification Triggers" framing over-specified this. **No SNS topic. No backend dispatcher Lambda. No FCM round-trip.** Android `NotificationCompat` + `NotificationManagerCompat` post local notifications client-side with deeplink-bearing `PendingIntent`.

**Why local-notification is strictly better for this use case:**

| Dimension | Server-side push (old design) | Local notification (this design) |
| --- | --- | --- |
| Latency | 200ms–2s (FCM round-trip) | < 50ms (immediate) |
| Cost | SNS publish + Lambda invoke per ride | $0 |
| Offline behaviour | Push delayed until next sync | Fires immediately |
| Cross-device delivery | All registered devices | Only the device on the ride (correct UX) |
| Backend dependency | Required for notification path | None |
| Failure mode | Push API can fail | Local API doesn't fail in normal operation |

**Why this works on Android (the only client platform in MVP scope):**

- Ride detection requires GPS, which requires a foreground service with `foregroundServiceType="location"`. By definition, the app process is alive at ride-end.
- Android keeps `location`-typed foreground services alive over Doze mode and App Standby. If the user force-stopped the app, ride-end wasn't detected at all — neither local nor server notification can help.

**APIs (Android):**

```text
NotificationCompat.Builder(context, channelId)
  .setSmallIcon(R.drawable.ic_traillens)
  .setContentTitle("How were the trails today?")
  .setContentText(trailSystemName)
  .setContentIntent(deeplinkPendingIntent)  // Intent.ACTION_VIEW + Uri.parse("traillens://feedback/{ride_id}")
  .build()

NotificationManagerCompat.from(context).notify(notificationId, notification)
```

**Permissions / setup the mobile app must handle:**

- `POST_NOTIFICATIONS` runtime permission on Android 13+ (API 33+). Request once, at first run.
- `NotificationChannel` registration on Android 8+ (API 26+). Channel ID: `trailpulse_post_ride`, importance: `IMPORTANCE_DEFAULT`.
- `PendingIntent` flags: `FLAG_UPDATE_CURRENT or FLAG_IMMUTABLE`.

**Opt-out**: mobile reads the same `UserPreferences.feedback_notifications_enabled` field synced from `PUT /api/trailpulse/user/preferences` (Task 15.2 endpoint #5). If `false`, skip the local notify call.

**What stays server-side**: `POST /api/users/me/devices` (existing route, renamed from `/api/devices`) is still used for OTHER push paths (admin notifications, scheduled-condition fires, care-report assignments). The dispatcher for ride-end specifically is gone.

**What gets removed (verified vs source plan):**

- ~~`TRAILPULSE_RIDE_END` SNS topic~~ — drop.
- ~~Server-side dispatcher logic in `rides/end` handler~~ — N/A; `/rides/end` was removed entirely per F-AA.
- ~~SNS-publish failure-handling around the dispatcher~~ — drop.

**Acceptance Criteria**:

- Mobile app fires local notification within 50ms of geofence-detected ride-end.
- Notification deeplink opens the in-app feedback form for `{ride_id}`.
- `feedback_notifications_enabled=false` suppresses the local notification.
- No backend SNS topic created for ride-end.
- iOS deferred (`UNUserNotificationCenter` mirrors this pattern when iOS work resumes).

**AI-Assisted Timeline**: 4 hours (mobile-side only; was 6 hours backend).

Sources:

- [Android Notifications overview — NotificationCompat / NotificationManagerCompat](https://developer.android.com/develop/ui/views/notifications)

---

### Task 15.7: Build Web Feedback Submission Form

**Objective**: Manual feedback form for web users

**Implementation Steps:**
1. Create React component in `webui/src/features/trails/components/TrailPulse/`
2. Fetch subscribed trail systems dropdown
3. Fetch feedback config (conditions, questions)
4. Build form UI with:
   - Trail system selector
   - Condition checkboxes/radio buttons
   - Additional question inputs
   - Free-text comment field
   - Submit button
5. Implement form submission to web endpoint
6. Add success/error toast notifications
7. Require authentication (redirect if not logged in)
8. Add to user dashboard

**Acceptance Criteria**:
- Web feedback form functional
- User can submit feedback manually
- Form loads conditions and questions dynamically
- Success message displayed on submission
- Authentication required

**AI-Assisted Timeline**: 8 hours

---

### Task 15.8: Build Admin TrailPulse Configuration Interface

**Objective**: Trail system owner configuration UI

**Implementation Steps:**
1. Create React components in `webui/src/features/admin/components/TrailPulse/`
2. **Trail Condition Management:**
   - List current conditions
   - Add new condition (name, multiselect, display order)
   - Edit existing condition
   - Delete condition (with confirmation)
   - Reorder conditions (drag-and-drop)
   - Preview how conditions appear to users
3. **Additional Questions Management:**
   - List current questions
   - Create new question (type, options, frequency)
   - Edit existing question
   - Delete question (with confirmation)
   - Enable/disable questions
   - Reorder questions
4. **Notification Customization:**
   - Edit notification message
   - Set notification timing (immediate, 5 min delay)
   - Enable/disable notifications
5. **Geofence Management:**
   - Display current geofence on map
   - Edit geofence boundaries (coordinate input or map drawing)
   - Preview geofence coverage
   - Validate and save geofence
6. Add to admin dashboard navigation
7. Restrict access to org-admin+

**Acceptance Criteria**:
- Admin can manage trail conditions
- Admin can create/edit/delete questions
- Admin can set frequency thresholds
- Admin can customize notification message
- Admin can define/edit geofences
- All changes saved to backend
- Authorization enforced (org-admin+)

**AI-Assisted Timeline**: 20 hours

---

### Task 15.9: Build Admin Feedback Data Management Interface

**Objective**: Feedback viewing, filtering, and management UI

**Implementation Steps:**
1. Create React components in `webui/src/features/admin/components/TrailPulse/`
2. **Feedback Data Table:**
   - Display feedback in paginated table
   - Columns: Date, User, Conditions, Responses, Comments, Crew Status
   - Expandable rows for full details
   - Sort by date (most recent first)
3. **Search and Filters:**
   - Date range picker (last 7 days, last 30 days, custom)
   - Condition filter (dropdown, multi-select)
   - User type filter (all, crew, regular, frequent)
   - Text search (search comments)
   - Feedback count filter (N+ submissions)
   - Apply multiple filters simultaneously
   - Save filter presets (localStorage)
4. **Feedback Management:**
   - Select individual feedback (checkbox)
   - Delete single feedback (with confirmation)
   - Bulk delete selected (with confirmation)
   - Delete by filter (with confirmation)
   - Soft delete option (checkbox)
   - Deletion reason field (optional)
   - Deletion audit log display
5. **Crew Member Management:**
   - Click user to see feedback history
   - "Mark as Crew Member" button
   - Crew notes field
   - Bulk crew assignment
   - Crew member list view
6. **Feedback Statistics:**
   - Condition distribution pie chart
   - Top contributors leaderboard
   - Average feedback frequency
   - Crew vs. regular user breakdown
7. **Integration with Trail Condition Setting:**
   - "Feedback Summary" card showing condition distribution
   - "Set Condition from Feedback" quick action button
   - Display recent feedback when setting conditions manually
8. Add to admin dashboard navigation
9. Restrict access to org-admin+

**Acceptance Criteria**:
- Admin can view all feedback for their trail systems
- Pagination working (50 per page)
- All filters functional and combinable
- Delete operations working (single, bulk, by filter)
- Soft delete and audit trail visible
- Crew member management functional
- Feedback statistics displayed correctly
- Integration with condition setting working
- Authorization enforced (org-admin+)

**AI-Assisted Timeline**: 24 hours

---

### Task 15.10: Implement Usage Counting (Inline TransactWrite — NO Aggregator Lambda) — REWRITTEN per F-AA

**Objective**: Maintain per-trail-system daily ride aggregates with **zero background Lambda work**. Counts are updated inline by the new `PUT /api/trailpulse/trail-systems/{ts_id}/ride-completion` TransactWrite.

**ARCHITECTURE CORRECTION (F-AA)**: The original design queried `RideEvents` nightly to build `UsageCounts` rollups. Since `RideEvents` is dropped (backend doesn't see rides) and `TrailSystemRideCount` is updated inline by the `PUT /ride-completion` TransactWrite, **no aggregator Lambda is required**. `trailpulse_usage_aggregator` is dropped from the new-Lambdas list.

**How counting actually works (verified, source-plan Section 11 Architecture C.1)**:

- Each `PUT /ride-completion` call performs a single-partition TransactWrite:
  1. `Put RIDECOMPLETION#{ride_id}` with `attribute_not_exists(SK)` (idempotency).
  2. `Update RIDECOUNT#{today_iso_date}` with `ADD total_rides :one`.
- `TRAILSYSTEMRIDECOUNT` items have a 3-year TTL (1095 days) — long enough that historical analytics queries can read directly from these items without any rollup step.
- **Privacy-first note**: `TRAILSYSTEMRIDECOUNT` carries no user attribution. Unique-users-per-day is **not** derivable from ride records; if dashboards want unique-user signals, derive from distinct `FeedbackResponses.user_id` per day (which IS user-attributed per Tasks 15.5/15.9 admin requirements).

**Implementation Steps:**

1. Confirm the `PUT /ride-completion` handler uses a single-partition TransactWrite with the two operations above.
2. Confirm `RIDECOUNT#{date}` items are written with TTL=now+1095d.
3. Document the inline-aggregation pattern in `api-dynamo/docs/BACKGROUND_WORKERS.md` and `dynamodb-spec.md`.
4. Add admin analytics queries that read directly from `RIDECOUNT#{date}` items (no aggregator lookup).

**Acceptance Criteria**:

- No `trailpulse_usage_aggregator` Lambda exists.
- Counts update on every `PUT /ride-completion` call atomically.
- Daily totals queryable for 3 years.
- Unique-users-per-day documented as derived from `FeedbackResponses.user_id`, not from ride records.

**AI-Assisted Timeline**: 0 hours additional (logic lives in the Task 15.2 `PUT /ride-completion` handler).

---

### Task 15.11: Implement Data Retention and TTL — REVISED per F-AA / F-BB privacy-first redesign

**Objective**: Auto-expire short-lived ride-tracking entities. **`RideEvents` is dropped** per privacy-first redesign (the backend never sees per-user ride records).

**Implementation Steps:**

1. Configure DynamoDB TTL on **`RideCompletion`** items: `now + 30 days` (idempotency markers — only needed long enough to dedupe legitimate replays from offline-queued requests).
2. Configure DynamoDB TTL on **`TrailSystemRideCount`** items: `now + 1095 days` (3-year retention per user direction; long-term storage for analytics).
3. Verify automatic deletion working for both entity types.
4. Ensure `FeedbackResponses` retained indefinitely (no TTL).
5. Document retention policy in privacy policy.

**Acceptance Criteria**:

- `RideCompletion` items automatically deleted after 30 days.
- `TrailSystemRideCount` items automatically deleted after 3 years.
- `FeedbackResponses` retained indefinitely.
- TTL working correctly in prod.

**AI-Assisted Timeline**: 2 hours

---

### Task 15.12: Update Web Features List

**Objective**: Add TrailPulse to website features page

**Implementation Steps:**
1. Edit `webui/src/features/public/data/features.ts`
2. Add TrailPulse feature object (ID 8):
   ```javascript
   {
     id: 8,
     title: 'TrailPulse',
     description: 'Share your trail experience and help improve conditions for the entire riding community',
     category: 'trail-engagement',
     icon: 'fa-heartbeat',
     image: '/img/features/trailpulse.png',
     benefits: [
       'Quick post-ride feedback on trail conditions',
       'Help other riders know what to expect',
       'Privacy-first - only tracks when you\'re on subscribed trails',
       'Contribute to trail improvements with your input',
       'Easy opt-out if you prefer not to share',
       'Make your voice heard on trail maintenance priorities'
     ]
   }
   ```
3. Add new category to featureCategories:
   ```javascript
   { id: 'trail-engagement', name: 'Trail Engagement' }
   ```
4. Verify feature displays on Features page
5. Test category filter

**Acceptance Criteria**:
- TrailPulse feature visible on Features page
- "Trail Engagement" category filter working
- Feature card displays correctly
- No breaking changes to existing features

**AI-Assisted Timeline**: 1 hour

---

### Task 15.13: Testing and Integration

**Objective**: End-to-end testing of TrailPulse feature

**Test Scenarios:**

1. **Mobile App Flow:**
   - Simulate ride start/end via API calls
   - Verify notification sent
   - Submit feedback via mobile endpoint
   - Verify feedback stored correctly

2. **Web Feedback Flow:**
   - Login to web app
   - Submit manual feedback
   - Verify feedback stored

3. **Admin Configuration Flow:**
   - Create trail conditions
   - Create additional questions
   - Define geofence boundaries
   - Verify configuration saved

4. **Admin Feedback Management Flow:**
   - View feedback table
   - Apply filters
   - Delete feedback (single, bulk)
   - Assign crew member status
   - View feedback statistics

5. **Usage Counting:**
   - Simulate multiple rides
   - Verify counts accurate
   - Verify deduplication working

6. **Data Retention:**
   - Verify TTL configured
   - Test automatic deletion (simulate 90-day expiration)

**Implementation Steps:**
1. Write integration test suite
2. Execute all test scenarios
3. Document any issues found
4. Fix critical bugs
5. Retest after fixes

**Acceptance Criteria**:
- All test scenarios pass
- No critical bugs
- Feature ready for pilot testing

**AI-Assisted Timeline**: 12 hours

---

**Phase 15 Total Duration**: 12-18 days

**Phase 15 Success Criteria**:
- All 28 API endpoints implemented and tested
- All 10 DynamoDB tables deployed
- Web feedback form functional
- Admin configuration interface complete
- Admin feedback management interface complete
- Push notifications working on ride end
- Usage counting accurate
- Data retention (90-day TTL) configured
- Web features list updated
- End-to-end testing passed
- Feature ready for mobile team integration
- Documentation complete

**Phase 15 Dependencies**:
- Phase 5 (Trail System Model) - Required for trail system associations
- Phase 10 (Notification System) - Required for SNS push notification infrastructure
- Phase 12 (Mobile Apps) - Mobile team needs APIs for GPS integration

**Phase 15 Notes**:
- This phase focuses on backend and web implementation
- Mobile team implements GPS tracking separately
- Coordinate with mobile team on API contracts
- Test notifications require iOS devices
- Geofence validation critical for privacy
- Consider phased rollout (beta users first)

---


---

## Dependencies and Critical Path

### Phase Dependencies Matrix

| Phase | Phase Name                      | Direct Dependencies                          | Duration   | Can Start After              |
|-------|----------------------------------|---------------------------------------------|------------|------------------------------|
| 1     | Brand Messaging Update           | None                                        | 1-2 days   | Immediately                  |
| 2     | Security Hardening               | None                                        | 5-7 days   | Immediately                  |
| 3     | Authentication System            | Phase 2 (MFA enforcement requires Security) | 7-10 days  | Phase 2 complete             |
| 4     | PII Protection                   | Phase 2 (retention policies require audit)  | 3-5 days   | Phase 2 complete             |
| 5     | Trail System Data Model          | Phase 3 (auth needed for API testing)       | 5-7 days   | Phase 3 complete             |
| 6     | Tag-Based Status Organization    | Phase 5 (requires trail system model)       | 3-5 days   | Phase 5 complete             |
| 7     | Status Management                | Phases 5, 6 (requires model + tags)         | 7-10 days  | Phases 5, 6 complete         |
| 8     | Scheduled Status Changes         | Phase 7 (requires status system)            | 3-5 days   | Phase 7 complete             |
| 9     | Trail Care Reports System        | Phases 5, 6 (requires model + type tags)    | 10-14 days | Phases 5, 6 complete         |
| 10    | Notification System              | Phases 7, 9 (status changes + reports)      | 5-7 days   | Phases 7, 9 complete         |
| 11    | Web Dashboards                   | Phases 7, 9, 10 (all core features)         | 10-14 days | Phases 7, 9, 10 complete     |
| 12    | Mobile Apps (Android + iOS)      | Phases 3, 7, 9, 10 (auth + core features)  | 30-50 days | Phases 3, 7, 9, 10 complete  |
| 13    | Pilot Onboarding                 | Phases 11, 12 (webui + mobile apps ready)          | 3-5 days   | Phases 11, 12 complete       |
| 14    | Testing and Validation           | Phase 13 (all features + pilots)            | 7-10 days  | Phase 13 complete            |

### Critical Path Analysis

The **critical path** represents the longest sequence of dependent phases that determines the minimum project duration.

**Critical Path Sequence:**
```
Phase 2 (Security) → Phase 3 (Auth) → Phase 5 (Trail Model) → Phase 7 (Status) → 
Phase 10 (Notifications) → Phase 11 (Web Dashboards) → Phase 12 (Mobile Apps) → 
Phase 13 (Pilot) → Phase 14 (Testing)
```

**Critical Path Duration:**
- **AI-Assisted**: 5-7 + 7-10 + 5-7 + 7-10 + 5-7 + 10-14 + 30-50 + 3-5 + 7-10 = **79-120 days**
- **Critical Path Optimistic**: ~79 days (11 weeks)
- **Critical Path Realistic**: ~100 days (14 weeks)
- **Critical Path Pessimistic**: ~120 days (17 weeks)

### Parallelization Opportunities

Several phases can run in parallel to optimize timeline:

**Wave 1 (Immediate Start):**
- Phase 1: Brand Messaging (1-2 days) - Can complete before Wave 2
- Phase 2: Security Hardening (5-7 days) - Blocks Wave 2

**Wave 2 (After Security):**
- Phase 3: Authentication (7-10 days) - CRITICAL PATH
- Phase 4: PII Protection (3-5 days) - Can run parallel to Phase 3

**Wave 3 (After Auth):**
- Phase 5: Trail System Data Model (5-7 days) - CRITICAL PATH

**Wave 4 (After Trail Model):**
- Phase 6: Tag-Based Status (3-5 days) - Can run parallel to early Phase 7
- Phase 7: Status Management (7-10 days) - CRITICAL PATH

**Wave 5 (After Model + Tags):**
- Phase 8: Scheduled Status Changes (3-5 days) - Can run parallel to Phase 9
- Phase 9: Trail Care Reports (10-14 days) - Can run parallel to Phase 8

**Wave 6 (After Status + Reports):**
- Phase 10: Notifications (5-7 days) - CRITICAL PATH
- Phase 11: Web Dashboards (10-14 days) - Can start when Phase 10 starts
- Phase 12: Mobile Apps (30-50 days) - Android can start when Phase 10 starts; iOS starts after Android beta

**Wave 7 (After All Features):**
- Phase 13: Pilot Onboarding (3-5 days) - CRITICAL PATH
- Phase 14: Testing (7-10 days) - CRITICAL PATH

### Risk Mitigation

**High-Risk Dependencies:**

1. **Phase 12 (Mobile Apps) - 30-50 days**
   - **Risk 1**: Longest phase, blocks pilot launch
   - **Mitigation**: Start Android development as early as possible (after Phase 3), parallelize with Phases 7-11
   - **Contingency**: Consider phased mobile rollout (Android apps first, Admin App in Phase 2)
   - **Risk 2**: ~~AWS SDK for iOS dependency~~ **RESOLVED - Research Complete**
   - **Research Findings**: AWS SDK for iOS reaches End of Support on August 1, 2026 (during MVP timeframe). MUST use AWS Amplify for Swift instead.
   - **Updated Risk**: None - plan updated to use AWS Amplify for Swift (v2) with long-term support
   - **See**: Task 12.1 for full details and migration guidance

2. **Phase 3 (Authentication) - 7-10 days**
   - **Risk**: ~~Passkey implementation complexity~~ **RESOLVED - Research Complete**
   - **Research Findings**: AWS Cognito natively supports passkeys via StartWebAuthnRegistration/CompleteWebAuthnRegistration APIs (launched November 2024). No custom implementation needed.
   - **Updated Risk**: None - passkeys fully supported by Cognito, no contingency needed
   - **See**: Task 3.1 for full implementation details with references

3. **Phase 9 (Trail Care Reports) - 10-14 days**
   - **Risk**: Complex feature with many dependencies
   - **Mitigation**: Break into sub-phases, implement core features first (create, view, assign)
   - **Contingency**: Defer advanced features (bulk ops, offline sync) to post-MVP

4. **Phase 11 (Web Dashboards) - 10-14 days**
   - **Risk**: 8 role-specific dashboards require extensive UI work
   - **Mitigation**: Reuse dashboard components, implement highest-priority roles first
   - **Contingency**: Launch with 4 core roles (superadmin, org-admin, trailsystem-owner, trailsystem-crew), add others post-MVP

### Optimized Timeline Strategy

**Best-Case Scenario (79 days / 11 weeks):**
- Maximum parallelization
- No blockers or rework
- All AI estimates hit optimistic targets
- **Target Launch**: Early Q2 2026 (early April)

**Realistic Scenario (100 days / 14 weeks):**
- Standard parallelization
- Minor blockers and rework (10-15% overhead)
- AI estimates hit realistic targets
- **Target Launch**: Mid Q2 2026 (mid-April to early May)

**Pessimistic Scenario (120 days / 17 weeks):**
- Limited parallelization
- Significant blockers and rework (20-30% overhead)
- AI estimates hit pessimistic targets
- **Target Launch**: Late Q2 2026 (late May to early June)

**Recommended Approach**: Plan for **realistic scenario (100 days)** with built-in buffer for unexpected issues.


---

## Timeline and Milestones

### Project Timeline Overview

**Start Date**: January 20, 2026 (Week 1)
**Target Launch Date**: April 22, 2026 (Week 14) - Realistic Scenario
**Buffer Period**: 2 weeks for unexpected issues
**Hard Deadline**: May 6, 2026 (Week 16)

### Week-by-Week Breakdown

#### **Week 1: Foundation (Jan 20-26)**
- **Phase 1**: Brand Messaging Update (1-2 days) ✓
- **Phase 2**: Security Hardening START (Day 3-7)
- **Deliverables**: New brand byline live on website, CloudTrail enabled
- **Milestone**: M1 - Brand Launch

#### **Week 2: Security & Auth Foundation (Jan 27 - Feb 2)**
- **Phase 2**: Security Hardening COMPLETE (Day 1-2)
- **Phase 3**: Authentication System START (Day 2-7)
- **Phase 4**: PII Protection START (parallel, Day 3-7)
- **Deliverables**: AWS WAF deployed, secrets rotation configured, MFA enabled
- **Milestone**: M2 - Security Hardening Complete

#### **Week 3: Authentication & Data Model (Feb 3-9)**
- **Phase 3**: Authentication System COMPLETE (Day 1-3)
- **Phase 4**: PII Protection COMPLETE (Day 1-2)
- **Phase 5**: Trail System Data Model START (Day 4-7)
- **Deliverables**: Passkey + magic link + email/password working, data retention policies live
- **Milestone**: M3 - Authentication System Complete

#### **Week 4: Core Data Model (Feb 10-16)**
- **Phase 5**: Trail System Data Model COMPLETE (Day 1-4)
- **Phase 6**: Tag-Based Status Organization START (Day 5-7)
- **Deliverables**: 21 DynamoDB tables deployed, trail system CRUD working
- **Milestone**: M4 - Trail System Data Model Complete

#### **Week 5: Status System Foundation (Feb 17-23)**
- **Phase 6**: Tag-Based Status Organization COMPLETE (Day 1-2)
- **Phase 7**: Status Management START (Day 3-7)
- **Deliverables**: Tag system working (max 20 per org), status API endpoints live
- **Milestone**: M5 - Tag-Based Organization Complete

#### **Week 6: Status & Reports Start (Feb 24 - Mar 2)**
- **Phase 7**: Status Management CONTINUE (Day 1-5)
- **Phase 9**: Trail Care Reports System START (parallel, Day 3-7)
- **Deliverables**: Status history tracking, bulk updates working

#### **Week 7: Advanced Status & Reports (Mar 3-9)**
- **Phase 7**: Status Management COMPLETE (Day 1-2)
- **Phase 8**: Scheduled Status Changes START (Day 3-7)
- **Phase 9**: Trail Care Reports System CONTINUE (Day 1-7)
- **Deliverables**: Photo uploads working, scheduled status changes functional
- **Milestone**: M6 - Status Management Complete

#### **Week 8: Reports & Notifications (Mar 10-16)**
- **Phase 8**: Scheduled Status Changes COMPLETE (Day 1-2)
- **Phase 9**: Trail Care Reports System COMPLETE (Day 1-5)
- **Phase 10**: Notification System START (Day 6-7)
- **Deliverables**: P1-P5 reports working, type tags configured, assignments functional
- **Milestone**: M7 - Trail Care Reports Complete

#### **Week 9: Notifications & Dashboards (Mar 17-23)**
- **Phase 10**: Notification System COMPLETE (Day 1-4)
- **Phase 11**: Web Dashboards START (Day 5-7)
- **Phase 12**: Mobile Apps START — Android development (parallel, Day 1-7)
- **Deliverables**: Email/SMS/push working, subscription system live
- **Milestone**: M8 - Notification System Complete

#### **Week 10-11: Dashboards & Mobile Development (Mar 24 - Apr 6)**
- **Phase 11**: Web Dashboards CONTINUE (Week 10: Day 1-7, Week 11: Day 1-4)
- **Phase 12**: Android Apps CONTINUE (parallel, Week 10-11: Day 1-14)
- **Deliverables**: 8 role-specific dashboards, analytics pages, Android User + Admin basic UI

#### **Week 12: Dashboard Complete & Mobile Continue (Apr 7-13)**
- **Phase 11**: Web Dashboards COMPLETE (Day 1-3)
- **Phase 12**: Android Apps CONTINUE (Day 1-5), iOS Apps START (Day 3-7)
- **Deliverables**: All dashboards live, bulk operations working, Android offline support, iOS project initialized
- **Milestone**: M9 - Web Dashboards Complete

#### **Week 13-14: Mobile Apps & Pilot Prep (Apr 14-20)**
- **Phase 12**: Android Apps COMPLETE (Day 1-3), iOS Apps CONTINUE (Day 1-14)
- **Phase 13**: Pilot Onboarding START (Day 6-7)
- **Deliverables**: Android User + Admin on Google Play internal track, iOS User + Admin on TestFlight, push notifications working (FCM + APNS)
- **Milestone**: M10 - Mobile Apps Complete

#### **Week 14: Pilot Launch & Testing (Apr 21-27)**
- **Phase 13**: Pilot Onboarding COMPLETE (Day 1-2)
- **Phase 14**: Testing and Validation START (Day 3-7)
- **Deliverables**: Hydrocut Trail System + GORBA onboarded, training complete
- **Milestone**: M11 - Pilot Organizations Live

#### **Week 15-16: Final Testing & Launch (Apr 28 - May 6)**
- **Phase 14**: Testing and Validation COMPLETE (Day 1-9)
- **MVP LAUNCH**: May 6, 2026
- **Deliverables**: All critical bugs fixed, performance validated, security audit passed
- **Milestone**: M12 - MVP LAUNCH

### Major Milestones

| Milestone | Date         | Description                                                                 | Success Criteria                                                                                                  |
|-----------|--------------|-----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| M1        | Jan 22, 2026 | Brand Launch                                                                | New byline live on website, marketing materials updated                                                           |
| M2        | Feb 2, 2026  | Security Hardening Complete                                                 | CloudTrail (1-year), WAF, secrets rotation (180-day), incident response plan, API rate limiting                   |
| M3        | Feb 9, 2026  | Authentication System Complete                                              | Passkey (inherently MFA) + magic link + email/password working, admin MFA enforced for password logins           |
| M4        | Feb 16, 2026 | Trail System Data Model Complete                                            | DynamoDB entity types implemented (7-table multi-table per ADR-001), trail system CRUD APIs working                                                       |
| M5        | Feb 23, 2026 | Tag-Based Organization Complete                                             | Max 20 condition tags per org, tag CRUD working                                                                   |
| M6        | Mar 9, 2026  | Status Management Complete                                                  | Status types, history, photos, bulk updates, scheduled changes working                                            |
| M7        | Mar 16, 2026 | Trail Care Reports Complete                                                 | P1-P5 reports, type tags (max 25), assignments, comments, photo uploads working                                   |
| M8        | Mar 23, 2026 | Notification System Complete                                                | Email (SES), SMS (Pinpoint), Push (SNS→FCM + SNS→APNS), subscriptions, preferences working                                  |
| M9        | Apr 13, 2026 | Web Dashboards Complete                                                     | 8 role-specific dashboards, analytics, bulk operations live                                                       |
| M10       | Apr 20, 2026 | Mobile Apps Complete                                                        | Android + iOS apps on Play internal track and TestFlight, offline support, push notifications                                              |
| M11       | Apr 23, 2026 | Pilot Organizations Live                                                    | Hydrocut + GORBA onboarded, 3 trail systems operational (Hydrocut: 1, GORBA: 2), admins trained                  |
| M12       | May 6, 2026  | MVP LAUNCH                                                                  | All 14 phases complete, testing passed, pilots validated, ready for public launch                                 |

### AI-Assisted Development Impact

**Traditional Timeline (no AI assistance):**
- **Estimated Duration**: 120-150 days (17-21 weeks)
- **Launch Date**: Late June to mid-July 2026
- **Developer Effort**: 2-3 full-time engineers

**AI-Assisted Timeline (Claude Sonnet 4.6 / Claude Opus 4.6):**
- **Estimated Duration**: 74-110 days (10.5-15.5 weeks)
- **Target Launch**: Late March to early June 2026
- **Developer Effort**: 1-2 full-time engineers
- **Productivity Gain**: 1.8x faster (45% time reduction)

**Assumptions:**
- AI assists with code generation, boilerplate reduction, testing automation
- Engineers focus on architecture, business logic, complex features
- AI handles routine tasks (CRUD endpoints, UI components, test cases)
- Human oversight for critical security, performance, architecture decisions

### Timeline Risks and Contingencies

**Risk 1: Mobile Development Delays (Phase 12)**
- **Probability**: Medium (30%)
- **Impact**: High (30-50 day phase)
- **Mitigation**: Start Android development early (Week 9), parallelize with dashboards
- **Contingency**: Launch web-only MVP, add mobile apps in Phase 2 release

**Risk 2: Authentication Complexity (Phase 3)**
- **Probability**: Medium (25%)
- **Impact**: Medium (7-10 day phase)
- **Mitigation**: Research Cognito passkey support in Week 1
- **Contingency**: Drop passkey to post-MVP, launch with magic link + email/password

**Risk 3: Trail Care Reports Scope Creep (Phase 9)**
- **Probability**: High (40%)
- **Impact**: Medium (10-14 day phase)
- **Mitigation**: Strictly enforce MVP scope, defer advanced features
- **Contingency**: Launch with basic reports (create, view, assign), add comments/bulk ops post-MVP

**Risk 4: Pilot Organization Issues (Phase 13)**
- **Probability**: Low (15%)
- **Impact**: Low (3-5 day phase)
- **Mitigation**: Pre-validate pilot data, provide white-glove onboarding support
- **Contingency**: Launch with 1 pilot org (Hydrocut), add GORBA in Phase 2

### Launch Readiness Checklist

**2 Weeks Before Launch (Week 13):**
- [ ] All 14 phases code-complete
- [ ] Android apps on Play internal track, iOS apps on TestFlight
- [ ] Performance testing passed (<500ms API response, 99.9% uptime)
- [ ] Security audit complete (no P1/P2 vulnerabilities)
- [ ] Pilot organizations using system daily

**1 Week Before Launch (Week 14):**
- [ ] All critical bugs fixed (P1/P2 = 0)
- [ ] Documentation complete (user guides, admin guides, API docs)
- [ ] Training materials created (videos, tutorials, FAQs)
- [ ] Support system ready (email support, in-app chat)
- [ ] Monitoring and alerts configured (CloudWatch, PagerDuty)

**Launch Day (Week 15):**
- [ ] Final smoke tests passed
- [ ] Pilot organizations validated
- [ ] Marketing announcement ready
- [ ] Support team on standby
- [ ] Launch blog post published
- [ ] MVP v1.13 LIVE 🚀


---

## Success Criteria

### Functional Requirements

The MVP is considered **functionally complete** when ALL of the following requirements are met:

#### **1. Brand Messaging (Phase 1)**
- [ ] Website homepage displays "Building communities, one trail at a time." byline
- [ ] Marketing materials updated with new messaging
- [ ] SEO metadata reflects brand positioning
- [ ] Brand messaging guidelines documented

#### **2. Security Hardening (Phase 2)**
- [ ] CloudTrail enabled with 1-year (365-day) retention for all regions
- [ ] AWS WAF deployed with OWASP Top 10 rules
- [ ] Secrets Manager configured with 180-day automatic rotation
- [ ] Incident Response Plan documented and team trained
- [ ] API rate limiting enabled (100 req/min/user, 1000 req/min/org)
- [ ] AWS WAF deployed (Security Hub and GuardDuty moved to post-MVP due to costs)
- [ ] MFA enforcement for org-admin, trailsystem-owner, superadmin roles (7-day grace period)

#### **3. Authentication System (Phase 3)**
- [ ] Passkey authentication working (WebAuthn/FIDO2, Touch ID, Face ID, security keys)
- [ ] Magic link authentication working (15-minute expiration, AWS SES delivery)
- [ ] Email/password authentication working (12+ chars, mixed case, numbers, symbols, 6-password history)
- [ ] Unified login experience across all three methods
- [ ] Mobile app authentication integrated (all five methods: passwordless, magic link, passkey, social login, admin login)
- [ ] User documentation for all authentication methods

#### **4. PII Protection (Phase 4)**
- [ ] 2-year retention policy implemented for inactive accounts
- [ ] Data export tool working (JSON format, all user data)
- [ ] Account deletion tool working (7-day soft delete, then hard delete)
- [ ] Monthly automated cleanup job running (DynamoDB TTL + Lambda)

#### **5. Trail System Data Model (Phase 5)**
- [ ] DynamoDB entity types implemented — **Status: PRODUCTION**: 7-table multi-table design per ADR-001 (current production reality at <500 DAU, optimized for cost)
- [ ] DynamoDB entity types documented — **Status: TARGET (post-100K-DAU)**: single-table design with 16 entity types and 5 overloaded GSIs (documented future-scale design; migration deferred until DynamoDB costs exceed $100/month or traffic reaches 10K DAU). The two designs are **complementary**, not contradictory: production runs multi-table today; single-table is the documented forward path.
- [ ] Trail System CRUD APIs working (create, read, update, delete)
- [ ] Trail System edit history tracking (5-year retention)
- [ ] Legacy trail data migrated to trail system model
- [ ] Web UI updated to use trail system model
- [ ] Seed data loaded for pilot organizations (Hydrocut Trail System + GORBA)

#### **6. Tag-Based Status Organization (Phase 6)**
- [ ] Max 20 condition tags per organization enforced
- [ ] Tag CRUD working (create, edit, delete, reorder)
- [ ] Tag assignment to trail systems working
- [ ] Default tags created for new organizations (Open, Closed, Caution)

#### **7. Status Management (Phase 7)**
- [ ] 7 status types working (emergency, seasonal, temporary, scheduled, weather-related, maintenance, general)
- [ ] Status history tracking (who, when, what changed)
- [ ] Photo uploads working (up to 5 photos per status, geolocation tagged)
- [ ] Bulk status updates working (apply to multiple trail systems)
- [ ] Status change workflow (draft → published)
- [ ] Public status page accessible without login

#### **8. Scheduled Status Changes (Phase 8)**
- [ ] Schedule status changes (specific date/time or recurring)
- [ ] Automated cron job executing scheduled changes
- [ ] Email reminders 24 hours before scheduled change
- [ ] Schedule management UI (view, edit, cancel upcoming changes)

#### **9. Trail Care Reports System (Phase 9)**
- [ ] Report creation working (title, description, location, 5 photos, priority P1-P5)
- [ ] Public vs private visibility settings
- [ ] Type tags working (max 25 per org: Trail Damage, Safety Hazard, Maintenance Needed, etc.)
- [ ] Assignment system working (assign to trail crew members)
- [ ] Comments system working (threaded discussions)
- [ ] Report status workflow (Open → In Progress → Resolved → Closed)
- [ ] Photo uploads with geolocation and timestamps
- [ ] 2-year retention for closed reports (auto-archive after 2 years)
- [ ] 180-day retention for care report photos (auto-cleanup)
- [ ] Offline report creation working (7-day queue with warnings)
- [ ] Report history and audit trail

#### **10. Notification System (Phase 10)**
- [ ] Email notifications working (AWS SES, status changes + new reports)
- [ ] SMS notifications working (AWS Pinpoint, emergency status changes)
- [ ] Push notifications working (AWS SNS → FCM for Android + SNS → APNS for iOS, status + reports + assignments)
- [ ] Subscription system working (subscribe to trail systems, organizations, specific statuses)
- [ ] Notification preferences working (per channel, per type)
- [ ] Unsubscribe links in all emails
- [ ] Notification history and audit trail

#### **11. Web Dashboards (Phase 11)**
- [ ] 8 role-specific dashboards working:
  - Superadmin: System-wide analytics, all organizations
  - Org-Admin: Organization overview, user management, reports
  - Trail-Owner: Trail system status, care reports, analytics
  - Trail-Crew: Assigned care reports, quick status updates
  - Trail-Volunteer: Assigned reports, limited status view
  - Organization-Viewer: Read-only org view, analytics
  - Trail-Viewer: Read-only trail system view
  - Public: Public status page, public reports
- [ ] Analytics pages (usage stats, report trends, status change frequency)
- [ ] Bulk operations (bulk assign reports, bulk update statuses)

#### **12. Mobile Apps (Phase 12)**
- [ ] **Android User App** (36 screens): Trail system discovery, condition viewing, care reports, TrailPulse observations, offline support
- [ ] **Android Admin App** (42 screens): Conditions management, full care report CRUD, team/user management, admin role gate
- [ ] **iOS User App**: Feature parity with Android User App
- [ ] **iOS Admin App**: Feature parity with Android Admin App
- [ ] Android apps on Google Play internal testing track with 10+ beta testers
- [ ] iOS apps on TestFlight with 10+ beta testers
- [ ] Offline support working on both platforms (7-day queue, sync on reconnect)
- [ ] Push notifications working (FCM for Android, APNS for iOS)
- [ ] Photo uploads with camera integration on both platforms
- [ ] Android: Play Store listing ready; iOS: App Store submission ready
- [ ] Performance: Android cold start <1.5s, 60fps, <15MB APK

#### **13. Pilot Onboarding (Phase 13)**

- [ ] Hydrocut onboarded (1 trail system: Hydrocut Trail System with Glasgow and Synders areas)
- [ ] GORBA onboarded (organization-level access)
- [ ] All pilot admins trained (2-hour training sessions)
- [ ] Support channels established (email, phone, in-app chat)
- [ ] Pilot organizations using system daily

#### **14. Testing and Validation (Phase 14)**
- [ ] End-to-end testing passed (all critical user flows)
- [ ] Security testing passed (OWASP Top 10, penetration test)
- [ ] Performance testing passed (<500ms API response, <2s page load)
- [ ] Load testing passed (1000 concurrent users, 10,000 req/min)
- [ ] User acceptance testing passed (pilot organizations validated)
- [ ] All P1/P2 bugs fixed (0 critical/high severity bugs)

### Performance Requirements

- **API Response Time**: < 500ms for 95th percentile (all endpoints)
- **Page Load Time**: < 2 seconds for web app (initial load)
- **Mobile App Launch**: < 3 seconds (cold start)
- **Uptime**: 99.9% availability (< 43 minutes downtime per month)
- **Concurrent Users**: Support 1,000 concurrent users without degradation
- **API Throughput**: Support 10,000 requests/minute across all endpoints
- **Database Performance**: < 100ms query response time for 95th percentile
- **Photo Upload**: < 10 seconds for 5MB photo (mobile network)
- **Offline Sync**: < 30 seconds to sync 7 days of queued reports

### Quality Requirements

- **Code Coverage**: > 80% unit test coverage for critical paths
- **Bug Severity**: 0 P1/P2 bugs at launch
- **Security Vulnerabilities**: 0 high/critical severity vulnerabilities
- **Accessibility**: WCAG 2.1 Level AA compliance for web app
- **Browser Support**: Chrome, Safari, Firefox, Edge (latest 2 versions)
- **Mobile OS Support**: Android 12+ (API 31+), iOS 16+
- **Documentation**: 100% API documentation coverage
- **Code Quality**: Pass black, isort, flake8 linters (Python), ESLint (JavaScript)

### Pilot Organization Requirements

- **Minimum Pilot Organizations**: 2 organizations (Hydrocut, GORBA)
- **Minimum Trail Systems**: 3 trail systems (Hydrocut Trail System, Guelph Lake Trail System, Akell Trail System)
- **Minimum Active Users**: 10+ active users across pilot organizations
- **Daily Active Usage**: At least 5 users logging in daily
- **Care Reports Created**: At least 20 care reports created during pilot
- **Status Updates**: At least 50 status updates during pilot
- **Mobile App Usage**: At least 5 users using Android or iOS apps daily

### User Satisfaction Requirements

- **Training Completion**: 100% of pilot admins complete training
- **Onboarding Success**: 100% of pilot organizations successfully onboarded
- **Feature Adoption**: 80%+ of core features used by pilot organizations
- **User Feedback**: Average rating > 4.0/5.0 from pilot users
- **Support Tickets**: < 10 support tickets per week during pilot
- **Bug Reports**: < 5 bug reports per week during pilot

### Documentation Requirements

- **User Documentation**: Complete user guides for all 8 roles
- **Admin Documentation**: Complete admin guides for org-admin, trailsystem-owner
- **API Documentation**: Complete API reference with examples
- **Developer Documentation**: Complete setup guides, architecture docs
- **Training Materials**: Video tutorials, FAQs, troubleshooting guides
- **Marketing Materials**: Website copy, launch announcement, press release

### Compliance and Legal Requirements

- **Privacy Policy**: Updated to reflect PII handling and retention
- **Terms of Service**: Updated to reflect multi-tenant SaaS model
- **Data Processing Agreement**: Available for enterprise customers
- **GDPR Compliance**: Data export, deletion, consent management
- **Cookie Policy**: Cookie consent banner on website
- **Accessibility Statement**: WCAG compliance statement published

### Launch Readiness Checklist

**Technical Readiness:**
- [ ] All 14 phases code-complete
- [ ] All automated tests passing
- [ ] Performance benchmarks met
- [ ] Security audit passed
- [ ] Monitoring and alerts configured
- [ ] Backup and disaster recovery tested

**Business Readiness:**
- [ ] Pilot organizations validated
- [ ] Training materials complete
- [ ] Support team trained
- [ ] Marketing materials ready
- [ ] Pricing and billing configured
- [ ] Legal documents finalized

**Operational Readiness:**
- [ ] Support channels established
- [ ] Incident response plan tested
- [ ] On-call rotation established
- [ ] Runbooks documented
- [ ] Launch communication plan ready
- [ ] Post-launch monitoring plan ready

### Definition of "MVP Launch Ready"

The MVP is considered **launch ready** when:

1. **All functional requirements met** (100% of Phase 1-14 tasks complete)
2. **All performance requirements met** (API < 500ms, uptime 99.9%)
3. **All quality requirements met** (0 P1/P2 bugs, 0 high/critical vulnerabilities)
4. **Pilot organizations validated** (2+ orgs, 10+ users, 20+ reports, daily usage)
5. **All documentation complete** (user guides, API docs, training materials)
6. **Launch readiness checklist complete** (technical, business, operational)

When these criteria are met, the executive team will approve **MVP v1.13 public launch** and begin marketing and sales activities.


---

## Revision History

| Version | Date       | Author             | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|---------|------------|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1.0     | 2026-01-17 | Product Management | Initial comprehensive MVP implementation plan created. Detailed all 14 phases with 85+ tasks covering: Brand Messaging Update, Security Hardening (CloudTrail 1-year, WAF, secrets 180-day rotation, MFA), Authentication System (passkey, magic link, email/password), PII Protection (2-year retention), Trail System Data Model (21 DynamoDB tables), Tag-Based Status Organization (max 20 tags), Status Management (7 types, photos, history), Scheduled Status Changes, Trail Care Reports (P1-P5, type tags max 25, assignments, comments, offline support), Notification System (email/SMS/push), Web Dashboards (8 roles), iPhone Apps (User + Admin, offline queue), Pilot Onboarding (Hydrocut + GORBA), Testing and Validation. Includes dependencies matrix, critical path analysis (74-110 days), timeline (16-week roadmap), success criteria (functional, performance, quality, pilot requirements), and AI-assisted development impact (1.8x productivity gain). Target launch: Q2 2026 (April-May). |
| 1.1     | 2026-03-27 | Product Management | V4 Update: (1) Android apps replace iOS as first mobile priority — both platforms now in MVP. Android User App (36 screens, Kotlin 2.0+/Compose/MD3/Hilt) and Admin App (42 screens) with Figma-driven design. iOS as parallel track with same level of detail. (2) DynamoDB updated from 21-table multi-table to single-table design documentation (16 MVP entity types, 5 overloaded GSIs, 78 access patterns). Current production: 7-table per ADR-001. (3) web/ deprecated, replaced by webui/ greenfield rewrite (React 19 + TypeScript + Vite 6.x + Tailwind CSS 4.x + shadcn/ui + Tremor + Zustand 5.x + React Query 5.x). (4) Push notifications updated for both FCM (Android) and APNS (iOS). (5) Phase 12 duration 30-50 days. (6) All web/src/*.jsx references updated to webui/src/features/*.tsx. |

---

**Document Version**: 1.1  
**Last Updated**: 2026-03-27  
**Document Owner**: Product Management  
**Status**: V4 - Updated for Android-first mobile, single-table DynamoDB, webui/ rewrite

---

**END OF MVP PROJECT PLAN**

