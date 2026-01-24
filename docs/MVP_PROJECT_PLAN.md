---
title: "TrailLensHQ MVP Implementation Project Plan"
author: "Chief Development Manager"
date: "January 2026"
abstract: "Comprehensive implementation plan for TrailLensHQ MVP v1.13 covering 14 phases, dependencies, timelines, and success criteria with AI-assisted development approach."
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

DOCUMENT STATUS: V3 - Passkey MFA Misconception Corrected

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
- **Development Approach**: AI-assisted development with Claude Sonnet 4.5 for accelerated delivery

**Key Context:**
- **Existing Codebase**: Exploratory prototype exists in `api-dynamo/`, `web/`, and `infra/` repositories
- **Current State**: ~60-70% of core infrastructure and features implemented
- **Net-New Development**: iPhone apps (User + Admin), Trail Care Reports system, tag-based status, security hardening
- **AI-Assisted Timeline**: 45-75 days (vs. 83-122 days traditional development)

**Critical Success Factors:**
- All 14 phases MUST be completed before launch
- Security hardening (Phase 2) is REQUIRED before handling production data
- iPhone apps (Phase 12) are REQUIRED for MVP - cannot launch without them
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
16. [Phase 12: iPhone Apps](#phase-12-iphone-apps)
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
- Real-time status updates with tag-based organization (max 10 tags per org)
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

**4. iPhone Apps (REQUIRED)**
- **User App**: Trail system discovery, status viewing, care report submission, offline support
- **Admin App**: Trail system management, full care report CRUD, work logs, offline support
- TestFlight distribution for MVP
- Push notifications (APNS via AWS SNS)
- Offline status caching (7 days)
- Offline report creation with auto-upload

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
- Push notifications (SNS → APNS for iPhone)
- Subscription management
- Notification preferences

### Out of Scope for MVP

- Android apps (post-MVP)
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
- Manual testing for iPhone apps (TestFlight)
- Security scanning (no secrets in code)

### Testing Strategy

**Unit Testing:**
- Python: pytest with 80%+ coverage
- TypeScript: Jest/Vitest for React components
- Swift: XCTest for iPhone apps

**Integration Testing:**
- API endpoint tests with real DynamoDB (LocalStack or dev environment)
- Authentication flow tests with Cognito
- Notification delivery tests

**End-to-End Testing:**
- Critical user workflows (trail system creation, status update, care report submission)
- iPhone app flows (TestFlight manual testing)
- Cross-browser testing for web (Chrome, Safari, Firefox)

**Performance Testing:**
- API response time benchmarking
- Load testing (100+ concurrent users)
- Notification latency testing

### Documentation Requirements

**Required Documentation:**
- API documentation (auto-generated from OpenAPI spec)
- User documentation (how to use web app and iPhone apps)
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
- **Trail Care Reports**: Net-new tables and endpoints (trail_care_reports, trail_care_report_comments, care_report_type_tags)
- **Tag-Based Status**: New status_tags table and tag assignment logic
- **Scheduled Status Changes**: New table and cron job for automated processing
- **Three Authentication Methods**: Add passkey and magic link support (currently only email/password)
- **API Rate Limiting**: Enable and test throttling configuration
- **Data Retention**: Implement automated cleanup jobs for 2-year retention policies

**Estimated Work**: 20-30 days (AI-assisted)

### web/ (React Frontend)

**Current State:**
- React 18 with Tailwind CSS 3.4.13
- 26 implemented pages across 4 tiers
- 88% test coverage
- Responsive design
- AWS Amplify hosting configured

**Needs Updates For MVP:**
- **Brand Messaging**: Update homepage byline to "Building communities, one trail at a time"
- **Trail Systems UI**: Update trail management to trail system management
- **Care Reports UI**: Create complete care report management interface (list, detail, create, edit, assign, comment)
- **Tag Management UI**: Create tag CRUD interfaces (status tags and care report type tags)
- **Authentication UI**: Add passkey and magic link login options (currently only email/password)
- **Dashboard Updates**: Update dashboards for all 8 roles with trail systems and care reports
- **Offline Indicator**: Add UI indicators when using cached data

**Estimated Work**: 15-25 days (AI-assisted)

### infra/ (Pulumi Infrastructure)

**Current State:**
- VPC, subnets, security groups configured
- AWS Cognito User Pool with 8 groups
- DynamoDB tables (14 tables currently, needs 21 for MVP)
- Lambda functions for API deployment
- API Gateway with custom domain
- S3 buckets for photos and deployments
- SNS topics for notifications
- SES for email delivery
- Infrastructure as Code (Pulumi + Python)

**Needs Updates For MVP:**

- **Security Hardening**: Enable CloudTrail (1-year retention), deploy AWS WAF (Security Hub and GuardDuty moved to post-MVP)
- **New DynamoDB Tables**: Add 7 tables (trail_systems, trail_system_history, status_tags, scheduled_status_changes, trail_care_reports, trail_care_report_comments, care_report_type_tags)
- **Secrets Rotation**: Configure 180-day automatic rotation
- **Cognito Updates**: Configure MFA enforcement, passkey support (if available)
- **Lambda Cron Job**: Add scheduled status changes processor
- **Data Retention Jobs**: Add Lambda crons for 2-year retention cleanup

**Estimated Work**: 10-15 days (AI-assisted)

### iPhone Apps (iOS)

**Current State:**
- **Do not exist** - must be created from scratch

**Required For MVP:**
- **User App**: Swift app with trail system viewing, status alerts, care report submission, offline support
- **Admin App**: Same codebase, separate app target with admin features
- **TestFlight**: Distribution channel for pilot organizations
- **Cognito Integration**: All three authentication methods
- **Push Notifications**: APNS via SNS
- **Offline Mode**: 7-day status caching, offline report creation with auto-upload

**Estimated Work**: 25-40 days (AI-assisted, longest single phase)

### Android Apps

**Current State:**
- **Do not exist** and are **OUT OF SCOPE for MVP**

**Post-MVP**: Android version will follow after iOS MVP launch

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
- `web/src/pages/Landing.jsx` (line ~143 or hero section)
- `web/src/pages/Home.jsx` (if exists)

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
- `web/public/index.html` (meta description tag)
- `web/src/components/SEO.jsx` (if exists)
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
- `web/src/pages/Landing.jsx` (or wherever app download CTAs are shown)
- `web/public/index.html` (if app badges are in static HTML)

**Assets to Download and Add**:

**Apple App Store Badge**:
- Download from: [Apple App Store Marketing Tools](https://tools.applemediaservices.com/app-store/)
- Badge Type: "Download on the App Store" (black badge preferred)
- Formats: SVG (primary), PNG (fallback)
- Save to: `web/src/assets/badges/Download_on_App_Store_Badge_US-UK_RGB_blk_092917.svg`
- Minimum height: 40px (screen), 10mm (print)
- Clear space: 1/4 badge height on all sides

**Google Play Store Badge**:
- Download from: [Google Play Badges Tool](https://play.google.com/intl/en_us/badges/)
- Badge Type: "Get it on Google Play" (standard badge)
- Formats: SVG (primary), PNG (fallback)
- Save to: `web/src/assets/badges/google-play-badge.svg`
- Size: Same height or larger than Apple badge when displayed together
- Clear space: 1/4 badge height on all sides

**Implementation Steps**:
1. Download official badge assets from Apple and Google (see Section 8.9 Download Checklist)
2. Create `web/src/assets/badges/` directory if it doesn't exist
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
- Official badge assets downloaded and stored in `web/src/assets/badges/`
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

**Background**: The current login page (`web/src/views/auth/Login.js`, lines 116-144) uses generic FontAwesome icons for social sign-in buttons. This does NOT comply with official branding guidelines from Google, Facebook, and Apple, and may cause app review failures or violate terms of service.

**Current Implementation Issues**:
1. Uses `<i className="fab fa-google">` instead of official Google "G" logo
2. Button text says "Google" instead of required "Sign in with Google"
3. Uses generic button styling instead of brand-specific colors and fonts
4. Does not follow Apple's "Sign in with Apple" Human Interface Guidelines
5. Does not follow Facebook's Platform Policy 8.3 for Login buttons
6. Does not use required typography (Roboto for Google, San Francisco for Apple)

**Files to Modify**:
- `web/src/views/auth/Login.js` (lines 115-145 - replace social button section)
- `web/src/views/auth/Register.js` (if social buttons exist there - same updates)
- `web/public/index.html` or `web/src/index.css` (add Roboto font import)

**Assets to Download and Add**:

**Google Sign-In Assets**:
- Download from: [Google Identity Branding Guidelines](https://developers.google.com/identity/branding-guidelines)
- Asset: `signin-assets.zip` containing official Google "G" logo
- Save to: `web/src/assets/auth/google-g-logo.svg`
- Required text: "Sign in with Google" (NOT just "Google")
- Font: Roboto Medium, 14px
- Colors: Light theme - white fill, gray stroke; Dark theme - dark fill

**Facebook Login Assets**:
- Download from: [Facebook Brand Resource Center](https://en.facebookbrand.com/facebookapp/)
- Asset: Facebook logo pack with white 'f' logo
- Save to: `web/src/assets/auth/facebook-f-logo-white.svg`
- Required text: "Continue with Facebook" or "Login with Facebook"
- Background color: #1877F2 (Facebook Blue)
- Text color: White (#FFFFFF)

**Apple Sign In Assets**:
- Download from: [Apple HIG Sign in with Apple](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple)
- Asset: Official Apple logo in SVG format
- Save to: `web/src/assets/auth/apple-logo-white.svg` and `apple-logo-black.svg`
- Required text: "Sign in with Apple" (NOT just "Apple")
- Styles: Black background with white logo, OR white background with black logo
- Font: San Francisco (system font fallback: `-apple-system, BlinkMacSystemFont`)

**Font Requirements**:
Add Roboto font for Google Sign-In button. Add to `web/public/index.html`:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@500&display=swap" rel="stylesheet">
```

Or add to `web/src/index.css`:
```css
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@500&display=swap');
```

**Implementation Steps**:
1. Download all official logo assets (see Section 8.10 Asset Download Checklist)
2. Create `web/src/assets/auth/` directory if it doesn't exist
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
- Official logo assets downloaded and stored in `web/src/assets/auth/`
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

**Objective**: Require multi-factor authentication for org-admin, trail-owner, and superadmin roles with 7-day grace period

**IMPORTANT CLARIFICATION**: This task applies to admin users who authenticate with **password-based login**. Admin users who authenticate with **passkeys DO NOT need traditional MFA** because passkeys are inherently multi-factor (something you have + something you are/know). Passkey authentication is more secure than password + SMS/TOTP.

**Files to Modify**:
- `infra/components/cognito.py` (Cognito MFA configuration)
- `api-dynamo/middleware/auth.py` (MFA enforcement logic - skip MFA check for passkey-authenticated users)
- `web/src/pages/Login.jsx` (MFA setup UI)

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

### Task 3.1: Configure Cognito for Native Passkey Support

**Objective**: Enable AWS Cognito's native passkey (WebAuthn/FIDO2) authentication support launched November 2024

**Research Completed**: AWS Cognito has native passkey support as of November 22, 2024. No custom Lambda authentication flow needed.

**Implementation Approach**: Use Cognito's native `WEB_AUTHN` authentication flow with `USER_AUTH` flow type.

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

### Task 3.2: Implement Passkey Authentication (WebAuthn/FIDO2)

**Objective**: Enable biometric login using Touch ID, Face ID, or hardware security keys using Cognito's native passkey APIs

**Research Completed**: AWS Cognito has native passkey APIs (StartWebAuthnRegistration, CompleteWebAuthnRegistration, InitiateAuth with WEB_AUTHN challenge) that handle credential storage, verification, and security. No custom DynamoDB tables or crypto verification code needed.

**Key References**:

- [StartWebAuthnRegistration API Documentation](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_StartWebAuthnRegistration.html)
- [CompleteWebAuthnRegistration API Documentation](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CompleteWebAuthnRegistration.html)
- [Authentication Flows - Passkey Section](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-authentication-flow-methods.html)
- [AWS Passwordless Auth Sample Code](https://github.com/aws-samples/amazon-cognito-passwordless-auth)

**Files to Modify**:

- `api-dynamo/routes/auth.py` (add passkey registration/auth endpoints that call Cognito APIs)
- `web/src/pages/Login.jsx` (add "Sign in with Passkey" button)
- `web/src/pages/Settings.jsx` (add passkey management UI)
- `web/src/components/PasskeySetup.jsx` (new component for passkey registration)

**Implementation Steps**:

**Backend (API) - Proxy to Cognito APIs**:

1. Implement `/auth/passkey/register/start` endpoint:
   - Requires authenticated user (access token in Authorization header)
   - Call `cognito_client.start_web_authn_registration(AccessToken=access_token)`
   - Return `CredentialCreationOptions` from Cognito response
   - Example response includes: challenge, RP ID, user info, supported algorithms (ES256, RS256)

2. Implement `/auth/passkey/register/complete` endpoint:
   - Receives `CredentialCreationOptions` from frontend
   - Call `cognito_client.complete_web_authn_registration(AccessToken=access_token, Credential=credential_data)`
   - Return success/error status
   - Cognito handles credential storage automatically (max 20 per user)

3. Implement `/auth/passkey/list` endpoint:
   - Call `cognito_client.list_web_authn_credentials(AccessToken=access_token)`
   - Return list of registered passkeys with metadata (friendly name, creation date, last used)

4. Implement `/auth/passkey/delete` endpoint:
   - Call `cognito_client.delete_web_authn_credential(AccessToken=access_token, CredentialId=credential_id)`
   - Return success/error status

**Backend (API) - Passkey Sign-In Flow**:

1. Update existing `/auth/login` endpoint to support passkey option:
   - If `auth_type=passkey`, call `cognito_client.initiate_auth()` with:
     - `AuthFlow="USER_AUTH"`
     - `AuthParameters={"USERNAME": username, "PREFERRED_CHALLENGE": "WEB_AUTHN"}`
   - Receive `WEB_AUTHN` challenge from Cognito
   - Return challenge to frontend

2. Implement `/auth/passkey/verify` endpoint:
   - Receives assertion response from `navigator.credentials.get()`
   - Call `cognito_client.respond_to_auth_challenge()` with:
     - `ChallengeName="WEB_AUTHN"`
     - `ChallengeResponses={"USERNAME": username, "CREDENTIAL": credential_json}`
     - `Session` from previous challenge
   - Return JWT tokens (IdToken, AccessToken, RefreshToken) on success

**Frontend (Web) - Passkey Registration**:

1. Add "Set up Passkey" button in user settings (after user is logged in)
2. On button click:
   - Call backend `/auth/passkey/register/start` with user's access token
   - Receive `CredentialCreationOptions` from backend
   - Call `navigator.credentials.create()` with options:

     ```javascript
     const credential = await navigator.credentials.create({
       publicKey: credentialCreationOptions
     });
     ```

   - Send credential response to `/auth/passkey/register/complete`
   - Show success message: "Passkey registered successfully"

3. Display list of registered passkeys (call `/auth/passkey/list`):
   - Show friendly name (e.g., "MacBook Pro Touch ID")
   - Show creation date and last used date
   - Add "Delete" button for each passkey

**Frontend (Web) - Passkey Sign-In**:

1. Add "Sign in with Passkey" button to login page
2. On button click:
   - Prompt user to enter username OR implement autofill (conditional UI)
   - Call backend `/auth/login?auth_type=passkey&username={username}`
   - Receive WebAuthn challenge from backend
   - Call `navigator.credentials.get()` with challenge:

     ```javascript
     const assertion = await navigator.credentials.get({
       publicKey: challengeOptions
     });
     ```

   - Send assertion response to `/auth/passkey/verify`
   - Store returned JWT tokens in localStorage
   - Redirect to dashboard

3. Error handling:
   - User cancels: Show "Passkey sign-in cancelled" message
   - Passkey not supported: Hide passkey button, show fallback options
   - Invalid credential: Show "Passkey not recognized" error
   - Network error: Show retry option

**Browser Support Detection**:

```javascript
function isPasskeySupported() {
  return window.PublicKeyCredential !== undefined &&
         navigator.credentials !== undefined;
}
```

**Testing**:

- Register passkey with Touch ID on macOS Chrome/Safari
- Sign in with registered passkey (verify biometric prompt appears)
- Test passkey listing (verify metadata displayed correctly)
- Test passkey deletion and re-registration
- Test with hardware security key (YubiKey) if available
- Test error handling (user cancels, passkey not supported in old browsers)
- Verify maximum 20 passkeys per user enforced by Cognito
- Test cross-device passkey sync (iCloud Keychain, Google Password Manager)

**Acceptance Criteria**:

- Passkey registration working via Cognito's native APIs
- Passkey sign-in functional with biometrics (Touch ID, Face ID)
- Passkeys stored securely in Cognito (not custom DynamoDB table)
- Cognito handles replay attack prevention automatically
- List/delete passkey functionality working
- Error handling graceful with clear user messages
- Documentation updated with browser support matrix (Chrome 109+, Safari 16+, Edge 109+)
- No custom cryptography code (all handled by Cognito)

**AI-Assisted Timeline**: 10-14 hours (reduced from 12-16 since no custom crypto logic needed)

---

### Task 3.3: Implement Magic Link Authentication

**Objective**: Enable email-based passwordless login with 15-minute expiration clickable links

**Research Completed**: AWS Cognito has native EMAIL_OTP support (6-digit code sent via email) as of November 2024, but NOT native magic link support (clickable link). Magic links require custom implementation using Custom Authentication Flow with Lambda triggers.

**Decision**: Implement custom magic links instead of native EMAIL_OTP for better user experience (click link vs. copy/paste code).

**Key References**:

- [AWS Cognito Passwordless Authentication Announcement](https://aws.amazon.com/about-aws/whats-new/2024/11/amazon-cognito-passwordless-authentication-low-friction-secure-logins/)
- [AWS Sample: Custom Magic Link Implementation](https://github.com/aws-samples/amazon-cognito-passwordless-auth/blob/main/MAGIC-LINKS.md)
- [Implementing Magic Links with Cognito Guide](https://theburningmonk.com/2023/03/implementing-magic-links-with-amazon-cognito-a-step-by-step-guide/)
- [AWS Blog: Passwordless Email Authentication](https://aws.amazon.com/blogs/mobile/implementing-passwordless-email-authentication-with-amazon-cognito/)

**Implementation Approach**: Custom implementation storing tokens in DynamoDB + AWS SES for email delivery + custom verification endpoint.

**Alternative Considered**: Native EMAIL_OTP (requires user to copy/paste 6-digit code, less convenient than clickable link).

**Files to Modify**:
- `api-dynamo/auth/magic_link.py` (new file for magic link generation)
- `api-dynamo/routes/auth.py` (magic link endpoints)
- `web/src/pages/Login.jsx` (magic link login option)
- `web/src/pages/MagicLinkVerify.jsx` (new page for link verification)

**Implementation Steps**:

**Backend (API)**:
1. Create DynamoDB table `magic_link_tokens` (or reuse existing auth tokens table):
   - PK: token (UUID)
   - Attributes: user_email, expires_at, used (boolean)
2. Implement `/auth/magic-link/send` endpoint:
   - Validate email format
   - Check if user exists in Cognito
   - Generate secure random token (UUID v4)
   - Store token in DynamoDB with 15-minute expiration
   - Send email via AWS SES with magic link
   - Email subject: "Your TrailLensHQ Login Link"
   - Email body: "Click here to login: https://app.traillenshq.com/auth/verify?token=..."
3. Implement `/auth/magic-link/verify` endpoint:
   - Validate token exists and not expired
   - Verify token not already used
   - Mark token as used
   - Issue Cognito JWT tokens
   - Return access token and refresh token

**Frontend (Web)**:
1. Add "Email me a magic link" option to login page
2. Implement magic link send flow:
   - User enters email address
   - Call `/auth/magic-link/send`
   - Show success message: "Check your email for login link"
3. Create `/auth/verify` page:
   - Extract token from URL query parameter
   - Call `/auth/magic-link/verify` with token
   - Store tokens in localStorage
   - Redirect to dashboard
4. Handle error cases:
   - Token expired: Show message with "Request new link" button
   - Token already used: Show message with "Request new link"
   - Invalid token: Show error message

**Email Template**:
```
Subject: Your TrailLensHQ Login Link

Hi there,

Click the link below to sign in to TrailLensHQ:

https://app.traillenshq.com/auth/verify?token={token}

This link expires in 15 minutes and can only be used once.

If you didn't request this link, you can safely ignore this email.

---
TrailLensHQ
Building communities, one trail at a time.
```

**Testing**:
- Request magic link for existing user
- Verify email received
- Click link and verify automatic login
- Test link expiration (wait 15 minutes or manually expire)
- Test link reuse (should fail on second click)
- Test invalid token
- Test for non-existent email

**Acceptance Criteria**:
- Magic link sent via email successfully
- Link login functional within 15 minutes
- Expired links rejected with clear error
- Used links cannot be reused
- Email template professional and clear
- Error handling graceful

**AI-Assisted Timeline**: 8-10 hours

---

### Task 3.4: Update Email/Password Authentication

**Objective**: Enhance existing email/password authentication with 12+ char minimum, complexity requirements, and 6-password history

**Research Completed**: AWS Cognito supports password reuse prevention via `PasswordHistorySize` parameter (range: 0-24 passwords). This feature is available in Essentials and Plus tiers (we're using dev which has this). Cognito stores password hashes (not plaintext) with user-specific salts for security.

**Key References**:

- [Password Reuse Prevention Documentation](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-advanced-security-password-reuse.html)
- [PasswordPolicyType API Reference](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_PasswordPolicyType.html)
- [AWS Blog: Password Security Improvements](https://builder.aws.amazon.com/content/2kItyzuwvmbvwgIi8OG2DrOAzAe/improving-password-security-on-amazon-cognito-with-password-reuse-prevention)

**Configuration Values**:

- Minimum length: 12 characters (Cognito supports 6-99)
- Password history: 6 (Cognito supports 0-24, we're using 6)
- Complexity: uppercase, lowercase, numbers, symbols (all supported natively)

**Files to Modify**:
- `infra/components/cognito.py` (Cognito password policy)
- `web/src/pages/Register.jsx` (password validation UI)
- `web/src/pages/ChangePassword.jsx` (update password change flow)

**Implementation Steps**:

**Cognito Password Policy**:
1. Update Cognito User Pool password policy:
   - Minimum length: 12 characters (was 8)
   - Require uppercase letters: Yes
   - Require lowercase letters: Yes
   - Require numbers: Yes
   - Require symbols: Yes
   - Password history: 6 (prevent reuse of last 6 passwords)
2. Deploy updated Cognito configuration

**Frontend Validation**:
1. Update registration form to show password requirements
2. Add real-time password strength indicator
3. Show which requirements are met/not met as user types
4. Display error if password history check fails

**Testing**:
- Create user with weak password (should fail)
- Create user with strong password (should succeed)
- Change password to previously used password (should fail with history error)
- Verify all complexity requirements enforced

**Acceptance Criteria**:
- 12-character minimum enforced
- Complexity requirements enforced
- Password history prevents reuse of last 6 passwords
- UI shows clear password requirements
- Error messages helpful

**AI-Assisted Timeline**: 4 hours

---

### Task 3.5: Create Unified Login Experience

**Objective**: Design clean login page with all three authentication methods

**Files to Modify**:
- `web/src/pages/Login.jsx` (update with all three options)

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

### Task 3.6: Implement iPhone App Authentication

**Objective**: Integrate all three authentication methods into iPhone apps

**Files to Modify**:
- iOS app `AuthenticationManager.swift` (new file)
- iOS app `LoginView.swift` (login UI)

**Implementation Steps**:
1. Integrate AWS Cognito SDK for iOS
2. Implement passkey authentication with `ASAuthorizationController`
3. Implement magic link with deep linking
4. Implement email/password with Cognito
5. Store tokens securely in iOS Keychain
6. Handle token refresh

**Testing**:
- Test all three auth methods on iPhone
- Verify Face ID/Touch ID prompts for passkey
- Test magic link deep linking
- Verify secure token storage

**Acceptance Criteria**:
- All three auth methods work on iPhone
- Biometric prompts functional
- Tokens stored securely
- Session persistence working

**AI-Assisted Timeline**: 12 hours (included in Phase 12 iPhone Apps development)

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
- iPhone apps support all three methods
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

**Files to Modify**:
- `api-dynamo/routes/user.py` (add `/user/export-data` endpoint)
- `web/src/pages/Settings.jsx` (add "Download My Data" button)
- `api-dynamo/services/data_export.py` (new file for export logic)

**Implementation Steps**:
1. Create `/user/export-data` API endpoint (authenticated)
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

**Files to Modify**:
- `api-dynamo/routes/user.py` (add `/user/delete-account` endpoint)
- `web/src/pages/Settings.jsx` (add "Delete Account" section)
- `api-dynamo/services/account_deletion.py` (new file)

**Implementation Steps**:
1. Create `/user/delete-account` API endpoint (authenticated, requires password confirmation)
2. Implement account deletion logic:
   - **Soft delete first**: Mark account as `pending_deletion` with 30-day grace period
   - After 30 days, hard delete all user data:
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

### Task 4.4: Create Automated Retention Cleanup Job

**Objective**: Ensure Lambda function runs reliably on schedule

**Files to Modify**:
- `infra/components/lambda_crons.py` (EventBridge rule)

**Implementation Steps**:
1. Create EventBridge rule to trigger Lambda daily at 2 AM UTC
2. Configure Lambda timeout (15 minutes max)
3. Configure error handling and retries
4. Set up CloudWatch alarms for Lambda failures
5. Add dead letter queue (DLQ) for failed executions
6. Test scheduled execution

**Acceptance Criteria**:
- Lambda runs daily at 2 AM UTC
- Alarms configured for failures
- DLQ captures failed events

**AI-Assisted Timeline**: 2 hours

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
        "status_tags": list,         # List of tag IDs (max 10)
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
5. Add authorization checks (org-admin, trail-owner, trail-crew)
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
- `web/src/pages/TrailSystems.jsx` (rename from Trails.jsx)
- `web/src/pages/TrailSystemDetail.jsx`
- `web/src/pages/TrailSystemEdit.jsx`
- `web/src/components/TrailSystemCard.jsx`
- `web/src/components/StatusUpdateModal.jsx`

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

**Objective**: Implement flexible status tag system (max 10 tags per organization)

**Duration**: 3-5 days
**Priority**: MEDIUM (enhances status management)
**Dependencies**: Phase 5 complete (trail systems exist)

---

### Task 6.1: Create status_tags DynamoDB Table

**Objective**: Store customizable status tags for each organization

**Files to Modify**:
- `infra/components/dynamodb.py` (add status_tags table)

**Table Schema**:
```python
status_tags = Table(
    table_name="status_tags",
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
3. Add org-level constraint: max 10 active tags per org
4. Create default tags for new organizations:
   - "winter", "maintenance", "caution", "wet-conditions", "dry-conditions"

**Acceptance Criteria**:
- Table created
- Max 10 tags enforced
- Default tags created

**AI-Assisted Timeline**: 2 hours

---

### Task 6.2: Implement Status Tag CRUD API Endpoints

**Objective**: Allow org-admins to manage tags

**Files to Modify**:
- `api-dynamo/routes/status_tags.py` (new file)

**Endpoints**:
1. `GET /status-tags` - List organization's tags
2. `POST /status-tags` - Create new tag (check max 10 limit)
3. `PUT /status-tags/{id}` - Update tag
4. `DELETE /status-tags/{id}` - Delete tag (if not in use)

**Implementation Steps**:
1. Implement CRUD endpoints
2. Add validation for max 10 tags
3. Prevent deletion of tags in use
4. Add authorization (org-admin only)
5. Write tests

**Testing**:
- Create tag
- Try to create 11th tag (should fail)
- Update tag color
- Try to delete tag in use (should fail)
- Delete unused tag

**Acceptance Criteria**:
- CRUD operations functional
- Max 10 limit enforced
- Authorization working

**AI-Assisted Timeline**: 4 hours

---

### Task 6.3: Implement Tag Assignment to Status Types

**Objective**: Allow trail-crew to tag status updates

**Files to Modify**:
- `api-dynamo/services/trail_system_service.py` (update status logic)
- `web/src/components/StatusUpdateModal.jsx` (add tag selector)

**Implementation Steps**:
1. Update status update endpoint to accept tags array
2. Validate tags exist and belong to organization
3. Store tags in trail_systems.status_tags array
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
- `web/src/components/StatusUpdateModal.jsx` (add sticky filter)

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
- `web/src/pages/OrganizationSettings.jsx` (add Tags tab)
- `web/src/components/TagManager.jsx` (new component)

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
- Status tags table created
- CRUD API functional
- Tag assignment working
- Max 10 tags enforced
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

**Predefined Status Types**:
- Open
- Closed
- Closed for Maintenance
- Closed for Season
- Caution (Wet Conditions)
- Caution (Dry Conditions)
- Caution (Wildlife)

**Implementation Steps**:
1. Create status types configuration (may be in organization settings, not separate table)
2. Allow org-admin to create custom statuses (max 30)
3. Each status has: name, default_reason, default_tags
4. Implement API endpoints for status type CRUD
5. Create UI for managing status types

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
- `web/src/components/StatusUpdateModal.jsx` (complete modal)

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

**Objective**: Tag trail systems with seasons for scheduled closures

**Files to Modify**:
- `api-dynamo/models/trail_system.py` (add seasons field)
- `web/src/components/TrailSystemEdit.jsx` (add season selector)

**Seasons**:
- Spring, Summer, Fall, Winter
- Custom seasons (e.g., "Mud Season", "Hunting Season")

**Implementation Steps**:
1. Add seasons array to trail_systems
2. Allow multi-select (trail can be open multiple seasons)
3. Display seasons on trail system card
4. Filter trail systems by season

**Acceptance Criteria**:
- Seasons assignable
- Multi-select working
- Filter functional

**AI-Assisted Timeline**: 4 hours

---

### Task 7.5: Implement Status History with 2-Year Retention

**Objective**: Complete history tracking (already created in Phase 5)

**Files to Modify**:
- `web/src/components/HistoryTimeline.jsx` (display component)

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
- `web/src/components/BulkStatusUpdate.jsx` (new component)

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

**Objective**: Provide starter status types for new organizations

**Files to Modify**:
- `api-dynamo/services/organization_service.py` (onboarding logic)

**Default Status Types**:
1. Open (green) - "Trails are open and maintained"
2. Closed (red) - "Trails are closed to all users"
3. Closed for Maintenance (orange) - "Temporary closure for trail work"
4. Caution (yellow) - "Proceed with caution, conditions may be challenging"

**Implementation Steps**:
1. When new organization created, auto-create default status types
2. Also create default tags: "winter", "maintenance", "wet"
3. Add templates to organization settings for reference

**Acceptance Criteria**:
- New orgs get default statuses
- Defaults editable
- Templates documented

**AI-Assisted Timeline**: 2 hours

---

**Phase 7 Total Duration**: 7-10 days
**Phase 7 Success Criteria**:
- Status type management functional
- Status update workflow complete
- Two-level photo system working
- Season assignment implemented
- History with 2-year retention
- Bulk updates functional
- Status templates for onboarding

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

**Objective**: Allow trail-crew to schedule future status changes

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
4. Add authorization (trail-crew+)
5. Write tests

**Acceptance Criteria**:
- CRUD operations functional
- Past dates rejected
- Authorization working

**AI-Assisted Timeline**: 4 hours

---

### Task 8.3: Implement Cron Job for Automated Processing

**Objective**: Lambda function to execute scheduled changes automatically

**Files to Modify**:
- `infra/lambda/process_scheduled_changes.py` (new Lambda)
- `infra/components/lambda_crons.py` (schedule)

**Cron Job Logic**:
1. Run every 15 minutes
2. Query scheduled_status_changes where scheduled_time <= now AND executed = false
3. For each pending change:
   - Update trail_system status
   - Create history entry
   - Mark schedule as executed
   - Send notification to subscribers (if enabled)
4. Log all executions to CloudWatch

**Implementation Steps**:
1. Create Lambda function
2. Implement query and update logic
3. Schedule to run every 15 minutes (EventBridge)
4. Add error handling and retries
5. Set up alarms for failures
6. Test with synthetic data

**Testing**:
- Create scheduled change for 1 minute in future
- Wait for cron to run
- Verify status updated
- Verify schedule marked as executed
- Test failure handling

**Acceptance Criteria**:
- Cron runs every 15 minutes
- Scheduled changes execute automatically
- History created for automated changes
- Error handling robust

**AI-Assisted Timeline**: 8 hours

---

### Task 8.4: Implement Reminder Notifications

**Objective**: Notify admins before scheduled changes execute

**Files to Modify**:
- `infra/lambda/process_scheduled_changes.py` (add reminder logic)

**Reminder Logic**:
- Send email/SMS notification 24 hours before scheduled change
- Include: trail system name, new status, scheduled time
- Allow cancellation via link in email

**Implementation Steps**:
1. Query schedules where scheduled_time = now + 24 hours
2. Send notification to trail-crew members
3. Include cancellation link
4. Mark reminder as sent (add reminder_sent boolean to schema)

**Acceptance Criteria**:
- Reminder sent 24 hours before
- Cancellation link working

**AI-Assisted Timeline**: 4 hours

---

### Task 8.5: Update Web UI for Scheduling

**Objective**: Allow scheduling from status update modal

**Files to Modify**:
- `web/src/components/StatusUpdateModal.jsx` (add schedule option)
- `web/src/pages/ScheduledChanges.jsx` (new page to view/manage schedules)

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
1. `POST /care-reports` - Create report (authenticated)
2. `GET /care-reports/{id}` - Get report details
3. `PUT /care-reports/{id}` - Update report (crew only)
4. `DELETE /care-reports/{id}` - Delete report (org-admin only)
5. `GET /care-reports` - List reports (filter by status, priority, assignment)
6. `PUT /care-reports/{id}/assign` - Assign to crew member
7. `PUT /care-reports/{id}/status` - Update status
8. `POST /care-reports/{id}/comments` - Add comment
9. `GET /care-reports/{id}/comments` - Get all comments
10. `GET /care-reports/{id}/activity` - Get activity log

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
- Create private report as trail-crew
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

**Objective**: Control who can see reports

**Visibility Rules**:
- **Public Reports**: Viewable by anyone (authenticated users)
- **Private Reports**: Viewable only by organization members (crew-only work logs)

**Implementation Steps**:
1. Add is_public field to reports
2. Filter queries based on user role:
   - Regular users: Only see public reports
   - Org members: See public + private reports for their org
3. Add "Make Private" checkbox for crew when creating report
4. Default to public for user submissions, private for crew work logs

**Acceptance Criteria**:
- Public reports visible to all
- Private reports visible only to org members
- Visibility toggle working

**AI-Assisted Timeline**: 2 hours (included in Task 9.4)

---

### Task 9.7: Implement Type Tag Management

**Objective**: Allow org-admin to manage report type tags (max 25 per org)

**Files to Modify**:
- `api-dynamo/routes/care_report_type_tags.py` (new file)
- `web/src/pages/OrganizationSettings.jsx` (add Type Tags tab)

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

**Objective**: Allow up to 5 photos per report

**Implementation Steps**:
1. Update photo upload endpoint to accept array of photos
2. Validate max 5 photos per report
3. Store photos in S3: `care-reports/{report_id}/{photo_id}.jpg`
4. Add photo URLs to report record
5. Implement photo deletion
6. Create photo upload UI component with preview
7. Add photo captions (optional)

**Testing**:
- Upload 1 photo
- Upload 5 photos
- Try to upload 6th photo (should fail)
- Delete photo

**Acceptance Criteria**:
- Max 5 photos enforced
- Photos upload to S3
- Preview working
- Deletion functional

**AI-Assisted Timeline**: 6 hours

---

### Task 9.11: Implement Status-Based Retention Policy

**Objective**: Active reports kept indefinitely, closed/cancelled deleted after 2 years

**Retention Policy**:
- **Active Reports** (Open, In Progress, Deferred, Resolved): Kept indefinitely
- **Closed/Cancelled Reports**: 2-year retention, then deleted
- **Photos**: 180 days after report closure, then deleted from S3

**Implementation Steps**:
1. Add TTL logic to data retention Lambda (from Phase 4)
2. Query closed/cancelled reports older than 2 years
3. Delete reports and associated comments
4. Delete photos from S3 for reports closed > 180 days
5. Log all deletions to CloudWatch

**Acceptance Criteria**:
- Active reports never deleted
- Closed reports deleted after 2 years
- Photos deleted 180 days after closure
- Audit logging complete

**AI-Assisted Timeline**: 4 hours

---

### Task 9.12: Implement Offline Report Creation Support

**Objective**: Allow iPhone apps to create reports offline, queue locally, auto-upload when signal returns

**Implementation Steps** (mostly in Phase 12 iPhone Apps):
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
- `web/src/pages/CareReports.jsx` (list view)
- `web/src/pages/CareReportDetail.jsx` (detail view)
- `web/src/pages/CareReportCreate.jsx` (create form)
- `web/src/components/CareReportCard.jsx`
- `web/src/components/CareReportFilters.jsx`

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

### Task 10.3: Implement Push Notifications via SNS→APNS for iPhone

**Objective**: Send push notifications to iPhone app users

**Files to Modify**:
- `api-dynamo/services/notification_service.py` (add push logic)
- `infra/components/sns.py` (APNS configuration)

**Implementation Steps**:
1. Configure SNS with APNS credentials (Apple Push Notification certificate)
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
- Verify push notification received on iPhone
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
- `web/src/pages/Subscriptions.jsx` (manage subscriptions UI)

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

**API Endpoints**:
1. `POST /subscriptions` - Subscribe to trail system or organization
2. `DELETE /subscriptions/{id}` - Unsubscribe
3. `GET /subscriptions` - Get user's subscriptions

**Implementation Steps**:
1. Create subscriptions table
2. Implement API endpoints
3. Add "Subscribe" button on trail system pages
4. Query subscribers when sending notifications
5. Respect subscription preferences

**Testing**:
- Subscribe to trail system
- Verify notification received when status changes
- Unsubscribe
- Verify notification not received

**Acceptance Criteria**:
- Subscription CRUD functional
- Notifications sent to subscribers only
- Subscribe/unsubscribe UI working

**AI-Assisted Timeline**: 6 hours

---

### Task 10.5: Implement Notification Preferences

**Objective**: Allow users to configure notification channels and types

**Files to Modify**:
- `api-dynamo/models/user.py` (add notification_preferences)
- `web/src/pages/NotificationSettings.jsx` (new page)

**Preference Options**:
- **Channels**: Email, SMS, Push (checkboxes for each)
- **Types**: Status changes, Care reports, Events, Forums
- **Frequency**: Immediate, Daily digest, Weekly summary
- **Quiet Hours**: Don't send notifications during specified times

**User Preferences Schema**:
```json
{
  "notification_preferences": {
    "email": {
      "enabled": true,
      "status_changes": true,
      "care_reports": false,
      "frequency": "immediate"
    },
    "sms": {
      "enabled": false
    },
    "push": {
      "enabled": true,
      "status_changes": true,
      "care_reports": true
    },
    "quiet_hours": {
      "start": "22:00",
      "end": "08:00",
      "timezone": "America/Toronto"
    }
  }
}
```

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
- `web/src/pages/Settings.jsx` (add Notifications tab)
- `web/src/components/NotificationPreferences.jsx`

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
- Push notifications to iPhone apps (<2 min latency)
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

**8 User Roles**:
1. traillenshq-admin (platform super admin)
2. admin (site administrator)
3. org-admin (organization administrator)
4. trail-owner (trail management permissions)
5. trail-crew (trail maintenance permissions)
6. trail-status (trail status update only)
7. content-moderator (content moderation)
8. org-member (basic organization member)

---

### Task 11.1: Create Role-Specific Dashboard Layouts

**Objective**: Design and implement dashboard for each role with relevant metrics and quick actions

**Files to Modify**:
- `web/src/pages/Dashboard.jsx` (main dashboard router)
- `web/src/pages/dashboards/OrgAdminDashboard.jsx`
- `web/src/pages/dashboards/TrailCrewDashboard.jsx`
- `web/src/pages/dashboards/UserDashboard.jsx`
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
- `web/src/pages/TrailSystems.jsx` (list)
- `web/src/pages/TrailSystemCreate.jsx` (create)
- `web/src/pages/TrailSystemEdit.jsx` (edit)

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
- `web/src/pages/CareReports.jsx`
- `web/src/pages/CareReportDetail.jsx`
- `web/src/components/AssignmentModal.jsx`

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
- `web/src/pages/Analytics.jsx` (new page)
- `web/src/components/charts/` (chart components)

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
1. Choose charting library (Chart.js or Recharts)
2. Implement analytics API endpoints
3. Create chart components
4. Implement date range selector
5. Add export to CSV functionality
6. Ensure mobile responsive

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
- `web/src/components/BulkActions.jsx`
- `web/src/components/TrailSystemTable.jsx` (add checkboxes)

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
- `web/src/pages/OrganizationSettings.jsx` (Tags section)
- `web/src/components/TagManager.jsx`
- `web/src/components/TypeTagManager.jsx`

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
- `web/src/pages/TeamManagement.jsx` (new page)
- `web/src/components/UserRoleEditor.jsx`
- `web/src/components/InviteUserModal.jsx`

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

## Phase 12: iPhone Apps

**Objective**: Create User and Admin iPhone apps with offline support (REQUIRED for MVP)

**Duration**: 25-40 days (longest single phase)
**Priority**: CRITICAL (cannot launch without iPhone apps)
**Dependencies**: Phases 3, 7, 9, 10 complete (authentication, status management, care reports, notifications)

**TWO APPS REQUIRED**:
1. **User App**: Trail system viewing, care report submission, offline support
2. **Admin App**: Trail system management, full care report CRUD, work logs

**Platform**: iOS 15+, Native Swift, SwiftUI
**Distribution**: TestFlight for MVP beta
**Repository**: Separate iOS repository (not in main workspace)

---

### Task 12.1: Set Up iOS Development Environment and Repositories

**Objective**: Initialize iOS project structure

**Research Completed**: AWS SDK for iOS reaches End of Support on August 1, 2026. MUST use AWS Amplify for Swift (v2) instead. Amplify provides modern Swift APIs with async/await, better SwiftUI integration, and long-term support.

**Key References**:

- [AWS SDK for iOS End of Support Notice](https://github.com/aws-amplify/aws-sdk-ios)
- [AWS Amplify for Swift Documentation](https://docs.amplify.aws/gen1/swift/prev/build-a-backend/auth/existing-resources/)
- [AWS Blog: Using Cognito with Swift](https://aws.amazon.com/blogs/mobile/using-amazon-cognito-with-swift-sample-app-developer-guide-and-more/)
- [Migration Guide: AWS SDK → Amplify Swift](https://aws.amazon.com/blogs/developer/announcing-new-aws-sdk-for-swift-alpha-release/)

**Critical Decision**: Use AWS Amplify for Swift (v2) instead of deprecated AWS SDK for iOS.

**Implementation Steps**:

1. Create new iOS repository (separate from main workspace)
2. Initialize Xcode project with two app targets:
   - TrailLensHQ (User App)
   - TrailLensHQ Admin (Admin App)
3. Configure Swift Package Manager for dependencies:
   - **AWS Amplify for Swift** (auth, storage, API, notifications) - REQUIRED, replaces legacy SDK
   - Alamofire (optional, for non-AWS API calls) or use URLSession directly
   - Kingfisher or SDWebImage (image loading/caching)
   - SwiftUI native components (preferred over third-party)
4. Set up project structure:
   - Shared code (Models, NetworkingManager, AuthenticationManager)
   - User app specific views
   - Admin app specific views
5. Configure build settings and signing
6. Set up TestFlight distribution
7. Add .gitignore for Xcode
8. Create README with setup instructions

**Acceptance Criteria**:
- iOS project initialized
- Two app targets configured
- Dependencies installed
- TestFlight ready

**AI-Assisted Timeline**: 4 hours

---

### Task 12.2: Implement User App - View Trail Systems

**Objective**: Browse and view trail systems with current status

**Files to Create**:
- `TrailSystemListView.swift`
- `TrailSystemDetailView.swift`
- `TrailSystemCard.swift`
- `StatusBadge.swift`

**UI Features**:
- List of trail systems (nearby or subscribed)
- Search and filter
- Trail system detail page
- Current status display with badge
- Status history timeline
- Photos gallery
- Subscribe/unsubscribe button

**Implementation Steps**:
1. Create SwiftUI views
2. Integrate with API (/trail-systems endpoints)
3. Implement location-based sorting (nearby first)
4. Add pull-to-refresh
5. Implement search
6. Create detail page with all info
7. Add photo gallery
8. Test on simulator and device

**Testing**:
- Browse trail systems
- View detail page
- Subscribe to trail system
- Pull to refresh
- Search for trail system

**Acceptance Criteria**:
- List view functional
- Detail view complete
- Search working
- Subscribe/unsubscribe working

**AI-Assisted Timeline**: 16 hours

---

### Task 12.3: Implement User App - Submit Trail Care Reports

**Objective**: Allow users to submit care reports with camera integration

**Files to Create**:
- `SubmitReportView.swift`
- `CameraView.swift`
- `PhotoPickerView.swift`

**UI Features**:
- "Submit Report" button
- Form with title, description, location
- Camera integration (take photos)
- Photo library picker
- Preview before submit
- Success confirmation

**Implementation Steps**:
1. Create report submission form
2. Integrate UIImagePickerController for camera
3. Implement photo selection (up to 5 photos)
4. Add location capture (GPS)
5. Implement photo upload to S3
6. Call API POST /care-reports
7. Show loading state during upload
8. Display success message

**Testing**:
- Submit report with photos from camera
- Submit report with photos from library
- Submit report with location
- Verify report appears in web UI

**Acceptance Criteria**:
- Camera integration working
- Photo upload functional
- Location capture working
- Report creation successful

**AI-Assisted Timeline**: 12 hours

---

### Task 12.4: Implement User App - View Public Care Reports

**Objective**: View care reports submitted by others

**Files to Create**:
- `CareReportListView.swift`
- `CareReportDetailView.swift`
- `CareReportCard.swift`

**UI Features**:
- List of public care reports
- Filter by trail system
- Filter by status
- Detail view with photos and comments
- Report status updates (read-only for users)

**Acceptance Criteria**:
- List view functional
- Filters working
- Detail view complete

**AI-Assisted Timeline**: 8 hours

---

### Task 12.5: Implement User App - Offline Report Creation

**Objective**: Create reports offline, auto-upload when signal returns

**Research Completed**: Core Data vs UserDefaults comparison. **Decision: Use Core Data** for offline report queue because reports have complex structure (title, description, multiple photos, location, metadata, timestamps). UserDefaults is only suitable for simple preferences and small data.

**Key References**:

- [Core Data vs UserDefaults Best Practices](https://cocoacasts.com/ud-10-should-you-use-core-data-or-user-defaults)
- [iOS Data Storage Comparison](https://fluffy.es/persist-data/)
- [SwiftUI Core Data Integration](https://livsycode.com/best-practices/userdefaults-vs-filemanager-vs-keychain-vs-core-data-vs-swiftdata/)

**Storage Decision**: Core Data for offline queue (complex objects with relationships to photos), NOT UserDefaults (performance issues with large data).

**Files to Create**:

- `OfflineQueueManager.swift`
- `SyncManager.swift`
- `OfflineReport.xcdatamodeld` (Core Data model)

**Offline Queue Logic**:

1. When offline, save report to local Core Data
2. Mark as "pending_sync"
3. Show "Offline - will sync when online" message
4. When online, automatically upload pending reports
5. Update UI when sync completes
6. Show "Syncing X reports..." notification
7. Handle sync failures (retry with exponential backoff)
8. Delete successfully synced reports from queue
9. Warn user if queue older than 7 days

**Implementation Steps**:
1. Implement network reachability detection
2. Create offline queue with Core Data or UserDefaults
3. Implement SyncManager to upload queued reports
4. Add retry logic with exponential backoff
5. Show sync status in UI
6. Add 7-day warning for old queued reports
7. Test with airplane mode

**Testing**:
- Enable airplane mode
- Create report (should queue)
- Disable airplane mode
- Verify report auto-syncs
- Test sync failure handling

**Acceptance Criteria**:
- Offline report creation working
- Auto-sync on connection restore
- 7-day warning implemented
- Sync status visible

**AI-Assisted Timeline**: 12 hours

---

### Task 12.6: Implement User App - Push Notifications

**Objective**: Receive push notifications via APNS

**Files to Create**:
- `NotificationManager.swift`
- `PushNotificationHandler.swift`

**Implementation Steps**:
1. Request notification permissions on app launch
2. Register device token with API (POST /devices)
3. Handle notification receipt (app in foreground, background, closed)
4. Implement deep linking (tap notification → trail detail)
5. Show notification badge count
6. Handle notification settings

**Testing**:
- Receive notification when app in foreground
- Receive notification when app in background
- Tap notification (verify deep link)
- Verify badge count updates

**Acceptance Criteria**:
- Push notifications received
- Deep linking working
- Badge count accurate

**AI-Assisted Timeline**: 8 hours

---

### Task 12.7: Implement User App - Offline Status Caching

**Objective**: Cache trail system status for 7 days, show stale data warning

**Storage Decision**: Use Core Data for consistency with offline reports (Task 12.5) and because trail systems have complex structure (photos, status history, metadata). Leverages existing Core Data stack.

**Files to Create**:

- `CacheManager.swift`
- `CachedTrailSystem.xcdatamodeld` (Core Data model, shared with offline queue)

**Caching Logic**:

1. Cache trail system data in Core Data
2. Include cached_at timestamp
3. When offline, load from cache
4. Show "Cached X hours ago" warning if data stale
5. Auto-refresh when online
6. Expire cache after 7 days (force refresh)

**Implementation Steps**:
1. Implement caching layer
2. Add cached_at timestamp to all cached data
3. Create UI warning for stale data
4. Implement auto-refresh logic
5. Add manual refresh button
6. Test with airplane mode

**Testing**:
- View trail system offline (should load from cache)
- Verify stale data warning appears
- Go online, verify auto-refresh
- Test 7-day expiration

**Acceptance Criteria**:
- Offline caching working
- 7-day cache expiration
- Stale data warning displayed
- Auto-refresh on reconnect

**AI-Assisted Timeline**: 8 hours

---

### Task 12.8: Implement Admin App - Trail System Management

**Objective**: Admin app for managing trail systems from field

**Files to Create** (in Admin app target):
- `AdminDashboard.swift`
- `AdminTrailSystemList.swift`
- `QuickStatusUpdate.swift`

**UI Features**:
- List trail systems for organization
- Quick status update (one-tap)
- Full status update (reason, photos, tags)
- Create new trail system
- Edit trail system

**Implementation Steps**:
1. Create admin-specific views
2. Implement quick status buttons (Open, Closed, Caution)
3. Implement full status update form
4. Add trail system creation form
5. Verify role-based access (trail-crew+ only)

**Acceptance Criteria**:
- Admin UI distinct from user app
- Quick status update working
- Full status update working
- Role verification functional

**AI-Assisted Timeline**: 12 hours

---

### Task 12.9: Implement Admin App - Full Care Report CRUD

**Objective**: Complete care report management for trail crew

**Files to Create**:
- `AdminCareReportList.swift`
- `AdminCareReportDetail.swift`
- `CareReportAssignment.swift`
- `CareReportCommentForm.swift`

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
1. Create all views
2. Implement filtering and sorting
3. Add assignment interface
4. Implement status workflow
5. Create comment form
6. Add priority editor
7. Test all CRUD operations

**Testing**:
- View all reports
- Assign report to self
- Update status through workflow
- Add comment with photo
- Change priority

**Acceptance Criteria**:
- Full CRUD functional
- Assignment working
- Status workflow complete
- Comments with photos working

**AI-Assisted Timeline**: 16 hours

---

### Task 12.10: Implement Admin App - Work Logs (Quick Private Report Creation)

**Objective**: Quick form for trail crew to log maintenance work

**Files to Create**:
- `QuickWorkLogForm.swift`

**UI Features**:
- Quick form: title, description, photos
- Auto-set: is_public = false, priority = P3
- Auto-assign: assigned_to = current user
- One-tap submit

**Implementation Steps**:
1. Create quick form
2. Pre-fill default values
3. Implement fast photo capture
4. Auto-submit on completion

**Acceptance Criteria**:
- Quick form functional
- Defaults correct
- Fast submission working

**AI-Assisted Timeline**: 4 hours

---

### Task 12.11: Implement Authentication (Cognito SDK with All Three Methods)

**Objective**: Support passkey, magic link, and email/password login

**Files to Create**:
- `AuthenticationManager.swift`
- `LoginView.swift`
- `PasskeyLoginView.swift`
- `MagicLinkLoginView.swift`

**Implementation Steps**:
1. Integrate AWS Cognito SDK for iOS
2. Implement passkey authentication with ASAuthorizationController
3. Implement magic link with deep linking
4. Implement email/password with Cognito
5. Store tokens securely in iOS Keychain
6. Implement token refresh
7. Create unified login UI

**Testing**:
- Login with passkey (Face ID/Touch ID)
- Login with magic link (tap email)
- Login with email/password
- Verify session persistence

**Acceptance Criteria**:
- All three auth methods working
- Biometric prompts functional
- Tokens stored securely in Keychain
- Session persistence working

**AI-Assisted Timeline**: 16 hours

---

### Task 12.12: Set Up TestFlight Distribution

**Objective**: Distribute apps to pilot organizations via TestFlight

**Implementation Steps**:
1. Create App Store Connect records for both apps
2. Configure app metadata (name, description, icons)
3. Set up TestFlight groups:
   - Internal Testing (development team)
   - External Testing (Hydrocut + GORBA)
4. Upload first build to TestFlight
5. Invite pilot users via email
6. Create testing instructions document
7. Monitor crash reports

**Acceptance Criteria**:
- Both apps in TestFlight
- Pilot users invited
- Testing instructions sent

**AI-Assisted Timeline**: 4 hours

---

### Task 12.13: Implement Deep Linking for Notifications

**Objective**: Tap notification → open relevant page in app

**Files to Create**:
- `DeepLinkHandler.swift`

**Deep Link Schemas**:
- `traillenshq://trail-system/{id}` → Trail system detail
- `traillenshq://care-report/{id}` → Care report detail
- `traillenshq://notifications` → Notifications list

**Implementation Steps**:
1. Configure URL schemes in Xcode
2. Implement deep link routing
3. Handle links when app closed, background, foreground
4. Extract parameters from URL
5. Navigate to appropriate view
6. Test all link types

**Testing**:
- Tap notification for trail system
- Verify app opens to correct detail page
- Test when app closed
- Test when app in background

**Acceptance Criteria**:
- Deep linking functional
- Works in all app states
- Parameters extracted correctly

**AI-Assisted Timeline**: 6 hours

---

**Phase 12 Total Duration**: 25-40 days
**Phase 12 Success Criteria**:
- User App complete with:
  - Trail system viewing
  - Care report submission with camera
  - View public care reports
  - Offline report creation (7-day queue)
  - Push notifications (APNS)
  - Offline status caching (7 days)
- Admin App complete with:
  - Trail system management
  - Full care report CRUD
  - Work log creation (private reports)
  - All admin features
- Authentication with all three methods (passkey, magic link, email/password)
- TestFlight distribution setup
- Deep linking functional
- Both apps in TestFlight for pilot testing

---

## Phase 13: Pilot Onboarding

**Objective**: Onboard Hydrocut and GORBA organizations with white-glove support

**Duration**: 3-5 days
**Priority**: CRITICAL (validates MVP)
**Dependencies**: Phases 11-12 complete (web dashboards and iPhone apps ready)

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
8. Assign roles (org-admin, trail-crew)

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

**Objective**: Distribute iPhone apps to pilot users

**Implementation Steps**:
1. Add pilot user emails to TestFlight
2. Send TestFlight invitations
3. Provide installation instructions
4. Help users install apps on their iPhones
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
| 12    | iPhone Apps                      | Phases 3, 7, 9, 10 (auth + core features)   | 25-40 days | Phases 3, 7, 9, 10 complete  |
| 13    | Pilot Onboarding                 | Phases 11, 12 (web + mobile ready)          | 3-5 days   | Phases 11, 12 complete       |
| 14    | Testing and Validation           | Phase 13 (all features + pilots)            | 7-10 days  | Phase 13 complete            |

### Critical Path Analysis

The **critical path** represents the longest sequence of dependent phases that determines the minimum project duration.

**Critical Path Sequence:**
```
Phase 2 (Security) → Phase 3 (Auth) → Phase 5 (Trail Model) → Phase 7 (Status) → 
Phase 10 (Notifications) → Phase 11 (Web Dashboards) → Phase 12 (iPhone Apps) → 
Phase 13 (Pilot) → Phase 14 (Testing)
```

**Critical Path Duration:**
- **AI-Assisted**: 5-7 + 7-10 + 5-7 + 7-10 + 5-7 + 10-14 + 25-40 + 3-5 + 7-10 = **74-110 days**
- **Critical Path Optimistic**: ~74 days (10.5 weeks)
- **Critical Path Realistic**: ~92 days (13 weeks)
- **Critical Path Pessimistic**: ~110 days (15.5 weeks)

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
- Phase 12: iPhone Apps (25-40 days) - Can start when Phase 10 starts

**Wave 7 (After All Features):**
- Phase 13: Pilot Onboarding (3-5 days) - CRITICAL PATH
- Phase 14: Testing (7-10 days) - CRITICAL PATH

### Risk Mitigation

**High-Risk Dependencies:**

1. **Phase 12 (iPhone Apps) - 25-40 days**
   - **Risk 1**: Longest phase, blocks pilot launch
   - **Mitigation**: Start iPhone development as early as possible (after Phase 3), parallelize with Phases 7-11
   - **Contingency**: Consider phased iPhone rollout (User App first, Admin App in Phase 2)
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
   - **Contingency**: Launch with 4 core roles (superadmin, org-admin, trail-owner, trail-crew), add others post-MVP

### Optimized Timeline Strategy

**Best-Case Scenario (74 days / 10.5 weeks):**
- Maximum parallelization
- No blockers or rework
- All AI estimates hit optimistic targets
- **Target Launch**: End of Q1 2026 (late March)

**Realistic Scenario (92 days / 13 weeks):**
- Standard parallelization
- Minor blockers and rework (10-15% overhead)
- AI estimates hit realistic targets
- **Target Launch**: Mid Q2 2026 (mid-April to early May)

**Pessimistic Scenario (110 days / 15.5 weeks):**
- Limited parallelization
- Significant blockers and rework (20-30% overhead)
- AI estimates hit pessimistic targets
- **Target Launch**: Late Q2 2026 (late May to early June)

**Recommended Approach**: Plan for **realistic scenario (92 days)** with built-in buffer for unexpected issues.


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
- **Deliverables**: Tag system working (max 10 per org), status API endpoints live
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
- **Phase 12**: iPhone Apps START (parallel, Day 1-7)
- **Deliverables**: Email/SMS/push working, subscription system live
- **Milestone**: M8 - Notification System Complete

#### **Week 10-11: Dashboards & iPhone Development (Mar 24 - Apr 6)**
- **Phase 11**: Web Dashboards CONTINUE (Week 10: Day 1-7, Week 11: Day 1-4)
- **Phase 12**: iPhone Apps CONTINUE (parallel, Week 10-11: Day 1-14)
- **Deliverables**: 8 role-specific dashboards, analytics pages, iPhone basic UI

#### **Week 12: Dashboard Complete & iPhone Continue (Apr 7-13)**
- **Phase 11**: Web Dashboards COMPLETE (Day 1-3)
- **Phase 12**: iPhone Apps CONTINUE (Day 1-7)
- **Deliverables**: All dashboards live, bulk operations working, iPhone offline support
- **Milestone**: M9 - Web Dashboards Complete

#### **Week 13: iPhone Apps & Pilot Prep (Apr 14-20)**
- **Phase 12**: iPhone Apps COMPLETE (Day 1-5)
- **Phase 13**: Pilot Onboarding START (Day 6-7)
- **Deliverables**: User + Admin apps on TestFlight, push notifications working
- **Milestone**: M10 - iPhone Apps Complete

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
| M4        | Feb 16, 2026 | Trail System Data Model Complete                                            | 21 DynamoDB tables deployed, trail system CRUD APIs working                                                       |
| M5        | Feb 23, 2026 | Tag-Based Organization Complete                                             | Max 10 status tags per org, tag CRUD working                                                                      |
| M6        | Mar 9, 2026  | Status Management Complete                                                  | Status types, history, photos, bulk updates, scheduled changes working                                            |
| M7        | Mar 16, 2026 | Trail Care Reports Complete                                                 | P1-P5 reports, type tags (max 25), assignments, comments, photo uploads working                                   |
| M8        | Mar 23, 2026 | Notification System Complete                                                | Email (SES), SMS (Pinpoint), Push (SNS→APNS), subscriptions, preferences working                                  |
| M9        | Apr 13, 2026 | Web Dashboards Complete                                                     | 8 role-specific dashboards, analytics, bulk operations live                                                       |
| M10       | Apr 20, 2026 | iPhone Apps Complete                                                        | User + Admin apps on TestFlight, offline support, push notifications                                              |
| M11       | Apr 23, 2026 | Pilot Organizations Live                                                    | Hydrocut + GORBA onboarded, 3 trail systems operational (Hydrocut: 1, GORBA: 2), admins trained                  |
| M12       | May 6, 2026  | MVP LAUNCH                                                                  | All 14 phases complete, testing passed, pilots validated, ready for public launch                                 |

### AI-Assisted Development Impact

**Traditional Timeline (no AI assistance):**
- **Estimated Duration**: 120-150 days (17-21 weeks)
- **Launch Date**: Late June to mid-July 2026
- **Developer Effort**: 2-3 full-time engineers

**AI-Assisted Timeline (Claude Sonnet 4.5):**
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

**Risk 1: iPhone Development Delays (Phase 12)**
- **Probability**: Medium (30%)
- **Impact**: High (25-40 day phase)
- **Mitigation**: Start iPhone development early (Week 9), parallelize with dashboards
- **Contingency**: Launch web-only MVP, add iPhone apps in Phase 2 release

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
- [ ] iPhone apps on TestFlight with 10+ beta testers
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
- [ ] MFA enforcement for org-admin, trail-owner, superadmin roles (7-day grace period)

#### **3. Authentication System (Phase 3)**
- [ ] Passkey authentication working (WebAuthn/FIDO2, Touch ID, Face ID, security keys)
- [ ] Magic link authentication working (15-minute expiration, AWS SES delivery)
- [ ] Email/password authentication working (12+ chars, mixed case, numbers, symbols, 6-password history)
- [ ] Unified login experience across all three methods
- [ ] iPhone app authentication integrated (all three methods)
- [ ] User documentation for all authentication methods

#### **4. PII Protection (Phase 4)**
- [ ] 2-year retention policy implemented for inactive accounts
- [ ] Data export tool working (JSON format, all user data)
- [ ] Account deletion tool working (7-day soft delete, then hard delete)
- [ ] Monthly automated cleanup job running (DynamoDB TTL + Lambda)

#### **5. Trail System Data Model (Phase 5)**
- [ ] 21 DynamoDB tables deployed with proper indexes
- [ ] Trail System CRUD APIs working (create, read, update, delete)
- [ ] Trail System edit history tracking (5-year retention)
- [ ] Legacy trail data migrated to trail system model
- [ ] Web UI updated to use trail system model
- [ ] Seed data loaded for pilot organizations (Hydrocut Trail System + GORBA)

#### **6. Tag-Based Status Organization (Phase 6)**
- [ ] Max 10 status tags per organization enforced
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
- [ ] Push notifications working (AWS SNS → APNS, status + reports + assignments)
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

#### **12. iPhone Apps (Phase 12)**
- [ ] **User App**: Trail system discovery, status alerts, public reports, submit reports with camera
- [ ] **Admin App**: Status updates, full report CRUD, assignments, offline work logs
- [ ] Both apps on TestFlight with 10+ beta testers
- [ ] Offline support working (7-day queue, sync on reconnect)
- [ ] Push notifications working (APNS integration)
- [ ] Photo uploads with camera integration
- [ ] App Store submission ready (screenshots, descriptions, metadata)

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
- **Mobile OS Support**: iOS 16+, Android 12+ (post-MVP)
- **Documentation**: 100% API documentation coverage
- **Code Quality**: Pass black, isort, flake8 linters (Python), ESLint (JavaScript)

### Pilot Organization Requirements

- **Minimum Pilot Organizations**: 2 organizations (Hydrocut, GORBA)
- **Minimum Trail Systems**: 3 trail systems (Hydrocut Trail System, Guelph Lake Trail System, Akell Trail System)
- **Minimum Active Users**: 10+ active users across pilot organizations
- **Daily Active Usage**: At least 5 users logging in daily
- **Care Reports Created**: At least 20 care reports created during pilot
- **Status Updates**: At least 50 status updates during pilot
- **Mobile App Usage**: At least 5 users using iPhone apps daily

### User Satisfaction Requirements

- **Training Completion**: 100% of pilot admins complete training
- **Onboarding Success**: 100% of pilot organizations successfully onboarded
- **Feature Adoption**: 80%+ of core features used by pilot organizations
- **User Feedback**: Average rating > 4.0/5.0 from pilot users
- **Support Tickets**: < 10 support tickets per week during pilot
- **Bug Reports**: < 5 bug reports per week during pilot

### Documentation Requirements

- **User Documentation**: Complete user guides for all 8 roles
- **Admin Documentation**: Complete admin guides for org-admin, trail-owner
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
| 1.0     | 2026-01-17 | Product Management | Initial comprehensive MVP implementation plan created. Detailed all 14 phases with 85+ tasks covering: Brand Messaging Update, Security Hardening (CloudTrail 1-year, WAF, secrets 180-day rotation, MFA), Authentication System (passkey, magic link, email/password), PII Protection (2-year retention), Trail System Data Model (21 DynamoDB tables), Tag-Based Status Organization (max 10 tags), Status Management (7 types, photos, history), Scheduled Status Changes, Trail Care Reports (P1-P5, type tags max 25, assignments, comments, offline support), Notification System (email/SMS/push), Web Dashboards (8 roles), iPhone Apps (User + Admin, offline queue), Pilot Onboarding (Hydrocut + GORBA), Testing and Validation. Includes dependencies matrix, critical path analysis (74-110 days), timeline (16-week roadmap), success criteria (functional, performance, quality, pilot requirements), and AI-assisted development impact (1.8x productivity gain). Target launch: Q2 2026 (April-May). |

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-17  
**Document Owner**: Product Management  
**Status**: FINAL - Ready for Executive Review

---

**END OF MVP PROJECT PLAN**

