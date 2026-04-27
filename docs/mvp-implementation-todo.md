<!--
=========================================================================================
CEO'S DIRECTIVE (January 17, 2026)
=========================================================================================

"Let's start over.

Execute the MVP doc to generate a TODO file based on the prompt-to-todo-prompt file from the root .github/prompt/ directory (exact filenames are in the MVP document in directions to AI section).

You are to only create a TODO file. No other files may be changed.

Some files have already been generated. However, you never finished the task. If a file already exists, you may use it to start with, but create a new version to continue.

For the MVP_PROJECT_PLAN.md, ALL 14 phases MUST be done. All items you add to the table of contents must be included.

Do not take shortcuts. You have unlimited time. You are to work 24/7 until the TODO file and associated documents are complete and finalized.

The CEO is counting on you. Your job depends on it.

Save this prompt in a comments section to the top of the generate TODO file."

=========================================================================================
END CEO DIRECTIVE
=========================================================================================

=========================================================================================
CTO'S CLARIFICATION (January 17, 2026)
=========================================================================================

"Be more explicit when referencing code. Any references in the todo file that refers to code must Action item to DOCUMENT the changes.

For example:
Break down Phase 1 into detailed tasks and document what needs to change

Would be appropriate. No check is changed in the task during execution.

Review the TODO file and update the tasks that refer to code to explicit

Put this prompt into the command section of the file."

=========================================================================================
END CTO CLARIFICATION
=========================================================================================
-->

# MVP Implementation TODO

**Document Version:** 1.0
**Created:** 2026-01-17
**Status:** Ready for Execution
**CTO Directive:** Complete documentation updates and create comprehensive MVP project plan with ALL 14 phases fully detailed

---

## Overview

This TODO list guides the complete MVP implementation process in two major sections:

**Section A: Documentation Updates**
- Backup and update existing CEO-facing documentation to reflect MVP v1.13 changes
- Ensure all documentation is consistent with MVP scope and decisions

**Section B: MVP Project Plan Creation**
- Create comprehensive `MVP_PROJECT_PLAN.md` with all 14 implementation phases
- Detail every task, dependency, acceptance criteria, and timeline estimate
- Account for existing codebase and AI-assisted development approach

**CRITICAL REQUIREMENT:** For MVP_PROJECT_PLAN.md, ALL 14 phases MUST be fully detailed. Every item added to the table of contents MUST be included with complete content. No shortcuts, no placeholders, no "TBD" sections.

---

## Section A: Documentation Updates

### Phase A1: Backup Existing Documentation Files

**Objective:** Preserve current versions of all documentation before making MVP updates.

#### Task A1.1: Backup PRODUCT_OVERVIEW_FOR_CEO.md
- [ ] **Action:** Copy `docs/PRODUCT_OVERVIEW_FOR_CEO.md` to `docs/PRODUCT_OVERVIEW_FOR_CEO_v2.md`
- [ ] **Verification:** Confirm backup file exists and is identical to source
- [ ] **Files Affected:**
  - Source: `docs/PRODUCT_OVERVIEW_FOR_CEO.md`
  - Backup: `docs/PRODUCT_OVERVIEW_FOR_CEO_v2.md`
- [ ] **Acceptance Criteria:**
  - Backup file created with `_v2` suffix
  - Backup file is byte-for-byte identical to source
  - Original file remains unchanged

#### Task A1.2: Backup SYSTEM_ARCHITECTURE.md
- [ ] **Action:** Copy `docs/SYSTEM_ARCHITECTURE.md` to `docs/SYSTEM_ARCHITECTURE_v3.md`
- [ ] **Verification:** Confirm backup file exists and is identical to source
- [ ] **Files Affected:**
  - Source: `docs/SYSTEM_ARCHITECTURE.md`
  - Backup: `docs/SYSTEM_ARCHITECTURE_v3.md`
- [ ] **Acceptance Criteria:**
  - Backup file created with `_v3` suffix
  - Backup file is byte-for-byte identical to source
  - Original file remains unchanged

#### Task A1.3: Backup SECURITY_REPORT_FOR_CEO.md
- [ ] **Action:** Copy `docs/SECURITY_REPORT_FOR_CEO.md` to `docs/SECURITY_REPORT_FOR_CEO_v2.md`
- [ ] **Verification:** Confirm backup file exists and is identical to source
- [ ] **Files Affected:**
  - Source: `docs/SECURITY_REPORT_FOR_CEO.md`
  - Backup: `docs/SECURITY_REPORT_FOR_CEO_v2.md`
- [ ] **Acceptance Criteria:**
  - Backup file created with `_v2` suffix
  - Backup file is byte-for-byte identical to source
  - Original file remains unchanged

#### Task A1.4: Backup MARKETING_PLAN.md
- [ ] **Action:** Copy `docs/MARKETING_PLAN.md` to `docs/MARKETING_PLAN_v2.md`
- [ ] **Verification:** Confirm backup file exists and is identical to source
- [ ] **Files Affected:**
  - Source: `docs/MARKETING_PLAN.md`
  - Backup: `docs/MARKETING_PLAN_v2.md`
- [ ] **Acceptance Criteria:**
  - Backup file created with `_v2` suffix
  - Backup file is byte-for-byte identical to source
  - Original file remains unchanged

**Dependencies:** None (this is the first phase)
**Complexity:** Small (S)
**Estimated Duration:** 10 minutes

---

### Phase A2: Update PRODUCT_OVERVIEW_FOR_CEO.md

**Objective:** Update product overview to reflect MVP v1.13 scope, focusing on trail systems (not individual trails), Trail Care Reports, tag-based status organization, and all MVP clarifications.

#### Task A2.1: Update Executive Summary
- [ ] **Action:** Revise executive summary to emphasize MVP scope
- [ ] **Key Changes:**
  - Confirm MVP v1.13 status (not v1.12)
  - Emphasize trail systems model (NOT individual trails)
  - Highlight Trail Care Reports as core MVP feature
  - Mention all three authentication methods (passkey, magic link, email/password)
  - Reference 14 implementation phases
- [ ] **Files Affected:** `docs/PRODUCT_OVERVIEW_FOR_CEO.md` (lines 28-35)
- [ ] **Acceptance Criteria:**
  - MVP version updated to v1.13
  - Trail systems clearly defined
  - Q2 2026 launch date confirmed
  - Pilot organizations (Hydrocut, GORBA) with 3 trail systems mentioned

#### Task A2.2: Update Core Features Section
- [ ] **Action:** Update core features to reflect MVP scope
- [ ] **Key Changes:**
  - **Trail System Management:** Update to tag-based status organization (max 10 tags per org), NOT fixed status groups
  - **Trail Care Reports:** Add complete Trail Care Reports section with:
    - P1-P5 priority system
    - Public/private visibility flag
    - Type tags (max 25 per org)
    - Assignment workflow
    - Comments and activity log
    - Multiple photos (up to 5)
    - Status-based retention policy
    - Offline report creation support
  - **Authentication:** Emphasize all three methods required (passkey, magic link, email/password)
  - **Security Hardening:** List MVP security gaps (CloudTrail, WAF, secrets rotation, incident response, API rate limiting, MFA); Security Hub and GuardDuty moved to post-MVP
- [ ] **Files Affected:** `docs/PRODUCT_OVERVIEW_FOR_CEO.md` (lines 188-241)
- [ ] **Acceptance Criteria:**
  - Tag-based status organization clearly explained
  - Trail Care Reports section comprehensive and accurate
  - All three authentication methods listed as required
  - All 7 security gaps documented

#### Task A2.3: Update iPhone Apps Section
- [ ] **Action:** Update iPhone apps section with MVP requirements
- [ ] **Key Changes:**
  - User app features: view trail systems, submit/view care reports, offline report creation
  - Admin app features: manage trail systems, full care report CRUD, work logs
  - Offline capabilities: 7-day status caching + offline report creation with local queueing
  - TestFlight distribution for MVP
  - iOS 15+ requirement
- [ ] **Files Affected:** `docs/PRODUCT_OVERVIEW_FOR_CEO.md` (lines 120-144)
- [ ] **Acceptance Criteria:**
  - User app features complete (including offline report creation)
  - Admin app features complete (including full care report CRUD)
  - Offline mode clearly explained (status caching + report queueing)
  - TestFlight distribution documented

#### Task A2.4: Update Brand Messaging Section
- [ ] **Action:** Update brand messaging to reflect MVP requirement
- [ ] **Key Changes:**
  - Move brand messaging from "post-MVP" to "REQUIRED for MVP"
  - Add section explaining "Building communities, one trail at a time" byline
  - Note this is Phase 1 of implementation
- [ ] **Files Affected:** `docs/PRODUCT_OVERVIEW_FOR_CEO.md` (lines 692-709)
- [ ] **Acceptance Criteria:**
  - Brand messaging clearly marked as MVP requirement
  - Byline "Building communities, one trail at a time" documented
  - Note that website and marketing materials must be updated

#### Task A2.5: Update DynamoDB Tables Inventory
- [ ] **Action:** Update table inventory to reflect MVP v1.13 data model
- [ ] **Key Changes:**
  - Update to 21 tables (was 14 or 16)
  - Add trail_systems table (replaces trails)
  - Add trail_system_history table
  - Add status_tags table
  - Add scheduled_status_changes table
  - Add trail_care_reports table
  - Add trail_care_report_comments table
  - Add care_report_type_tags table
- [ ] **Files Affected:** Referenced in product overview
- [ ] **Acceptance Criteria:**
  - All 21 tables documented
  - Trail systems model clearly explained
  - Care report tables documented

#### Task A2.6: Update Pilot Organizations Section
- [ ] **Action:** Update pilot organizations details
- [ ] **Key Changes:**
  - Confirm Hydrocut: 1 trail system (includes Glasgow and Synders areas)
  - Confirm GORBA: Guelph Lake + Akell trail systems
  - Total: 3 trail systems for MVP
  - White-glove onboarding approach
- [ ] **Files Affected:** `docs/PRODUCT_OVERVIEW_FOR_CEO.md` (lines 643-659)
- [ ] **Acceptance Criteria:**
  - All 3 trail systems documented
  - White-glove onboarding explained
  - Free Enterprise tier for 6-12 months mentioned

#### Task A2.7: Update Revision History
- [ ] **Action:** Add revision history entry for MVP v1.13 updates
- [ ] **Key Changes:**
  - Add entry: "Version 2.0 | 2026-01-17 | Product Management | Updated to reflect MVP v1.13: documentation updates per MVP implementation prompt, all 14 phases documented, Trail Care Reports fully specified, tag-based status organization, brand messaging in MVP"
- [ ] **Files Affected:** `docs/PRODUCT_OVERVIEW_FOR_CEO.md` (bottom of file)
- [ ] **Acceptance Criteria:**
  - Revision entry added with correct version, date, author
  - All major changes documented in revision entry

**Dependencies:** Task A1.1 (backup) must be complete
**Complexity:** Large (L)
**Estimated Duration:** 2-3 hours

---

### Phase A3: Update SYSTEM_ARCHITECTURE.md

**Objective:** Update architecture documentation to reflect MVP v1.13 technical decisions, DynamoDB schema changes, and iPhone app requirements.

#### Task A3.1: Update Executive Summary
- [ ] **Action:** Update executive summary with MVP cost targets
- [ ] **Key Changes:**
  - Confirm development environment: $75-150/month
  - Confirm production environment: $200-400/month
  - Note serverless architecture benefits for MVP
- [ ] **Files Affected:** `docs/SYSTEM_ARCHITECTURE.md` (lines 26-40)
- [ ] **Acceptance Criteria:**
  - Cost estimates match MVP requirements
  - Serverless benefits clearly stated

#### Task A3.2: Update DynamoDB Tables Section
- [ ] **Action:** Update DynamoDB tables to 21 tables for MVP v1.13
- [ ] **Key Changes:**
  - **Core Trail System Management (4 tables):**
    1. trail_systems - Trail system data (replaces individual trails concept)
    2. trail_system_history - Status change audit trail (2-year retention)
    3. status_tags - Status categorization tags (max 10 per org)
    4. scheduled_status_changes - Pre-scheduled status changes with cron automation
  - **Trail Care Reports (3 tables):**
    5. trail_care_reports - Unified issue tracking (P1-P5, public/private, type tags)
    6. trail_care_report_comments - Crew update comments with optional photos
    7. care_report_type_tags - Report categorization tags (max 25 per org)
  - **User Management (2 tables):**
    8. users - User profiles with email lowercase index
    9. devices - Device registration for push notifications (APNS/FCM)
  - **Community Features (9 tables):**
    10. trail_reviews
    11. trail_photos
    12. forum_topics
    13. forum_replies
    14. events
    15. event_rsvps
    16. volunteer_opportunities
    17. volunteer_signups
    18. (2 more from existing)
  - **Business Operations (4 tables):**
    19. demo_requests
    20. partner_applications
    21. testimonials
    22. case_studies (may exist)
- [ ] **Files Affected:** `docs/SYSTEM_ARCHITECTURE.md` (DynamoDB section)
- [ ] **Acceptance Criteria:**
  - All 21 tables documented
  - Each table has description of purpose and key attributes
  - GSI (Global Secondary Indexes) documented where applicable
  - Retention policies documented (2-year history, 180-day photos)

#### Task A3.3: Update iPhone Apps Section
- [ ] **Action:** Update iPhone apps architecture details
- [ ] **Key Changes:**
  - Two apps required for MVP: User app + Admin app
  - User app: trail system viewing, care report submission/viewing, offline report creation
  - Admin app: trail system management, full care report CRUD
  - Authentication: AWS Cognito SDK with all three methods
  - Push notifications: APNS via AWS SNS
  - Offline mode: 7-day status caching + offline report queueing
  - TestFlight distribution for MVP
- [ ] **Files Affected:** `docs/SYSTEM_ARCHITECTURE.md` (iOS section)
- [ ] **Acceptance Criteria:**
  - Both apps documented
  - Offline architecture clearly explained
  - Push notification flow documented
  - TestFlight deployment strategy documented

#### Task A3.4: Update Authentication Section
- [ ] **Action:** Update authentication section with all three methods
- [ ] **Key Changes:**
  - Passkey authentication: WebAuthn/FIDO2 via Cognito (research native support first)
  - Magic link: 15-minute JWT tokens via SES
  - Email/password: Cognito User Pool with MFA for admins (7-day grace period)
  - All three methods required for MVP
- [ ] **Files Affected:** `docs/SYSTEM_ARCHITECTURE.md` (Authentication section)
- [ ] **Acceptance Criteria:**
  - All three methods documented
  - Passkey implementation approach documented
  - MFA enforcement policy documented (7-day grace)

#### Task A3.5: Update Security Controls Section
- [ ] **Action:** Update security controls with all 7 critical gaps
- [ ] **Key Changes:**
  - CloudTrail: 1-year retention (not 90 days)
  - AWS WAF: OWASP Top 10 protection
  - Secrets Manager: 180-day rotation (not 90 days)
  - Incident response plan: GDPR 72-hour breach notification
  - MFA enforcement: 7-day grace period for admins
  - API rate limiting: 100 req/min per user
  - Security Hub: POST-MVP (compliance monitoring)
  - GuardDuty: POST-MVP (threat detection)
- [ ] **Files Affected:** `docs/SYSTEM_ARCHITECTURE.md` (Security section)
- [ ] **Acceptance Criteria:**
  - All MVP security controls documented (excluding post-MVP Security Hub/GuardDuty)
  - Retention periods accurate (1 year CloudTrail, 180 days secrets)
  - MFA policy clearly stated

#### Task A3.6: Update Data Retention Policies Section
- [ ] **Action:** Add comprehensive data retention policies
- [ ] **Key Changes:**
  - User accounts: 2 years inactive
  - Trail system status history: 2 years
  - Trail Care Reports: Status-based (active kept indefinitely, closed/cancelled 2 years)
  - Care report photos: 180 days after closure
  - CloudTrail logs: 1 year
- [ ] **Files Affected:** `docs/SYSTEM_ARCHITECTURE.md` (Data Retention section)
- [ ] **Acceptance Criteria:**
  - All retention policies documented
  - Status-based retention for care reports explained
  - Photo retention policy clearly stated

#### Task A3.7: Update Revision History
- [ ] **Action:** Add revision history entry for MVP v1.13 updates
- [ ] **Key Changes:**
  - Add entry: "Version 2.0 | 2026-01-17 | Chief Architect | Updated to reflect MVP v1.13: 21 DynamoDB tables, trail systems model, Trail Care Reports architecture, iPhone apps with offline support, all three authentication methods, security hardening requirements"
- [ ] **Files Affected:** `docs/SYSTEM_ARCHITECTURE.md` (bottom of file)
- [ ] **Acceptance Criteria:**
  - Revision entry added with correct details
  - All major architectural changes documented

**Dependencies:** Task A1.2 (backup) must be complete
**Complexity:** Large (L)
**Estimated Duration:** 2-3 hours

---

### Phase A4: Update SECURITY_REPORT_FOR_CEO.md

**Objective:** Update security report to reflect MVP v1.13 security requirements, data retention policies, and compliance approach.

#### Task A4.1: Update PII Data Inventory
- [ ] **Action:** Update PII inventory to include trail systems and care reports data
- [ ] **Key Changes:**
  - Add trail_systems table PII (GPS coordinates, trail system names)
  - Add trail_care_reports table PII (submitter info, GPS locations, photos)
  - Add care_report_comments PII (crew member comments)
  - Update total table count to 21 tables
- [ ] **Files Affected:** `docs/SECURITY_REPORT_FOR_CEO.md` (Section 1)
- [ ] **Acceptance Criteria:**
  - All 21 tables included in PII inventory
  - Trail Care Reports PII documented
  - Risk levels assigned appropriately

#### Task A4.2: Update Current Security Posture Section
- [ ] **Action:** Update current security posture with MVP requirements
- [ ] **Key Changes:**
  - Document all three authentication methods (passkey, magic link, email/password)
  - Update CloudTrail to 1-year retention (required for MVP)
  - Update secrets rotation to 180 days (required for MVP)
  - Add MFA enforcement with 7-day grace period
  - Confirm WAF, API rate limiting, MFA as required for MVP; Security Hub and GuardDuty moved to post-MVP
- [ ] **Files Affected:** `docs/SECURITY_REPORT_FOR_CEO.md` (Section 3)
- [ ] **Acceptance Criteria:**
  - All three authentication methods documented
  - All MVP security gaps listed (excluding post-MVP Security Hub/GuardDuty)
  - Retention periods accurate (1 year CloudTrail, 180 days secrets)

#### Task A4.3: Update Compliance Requirements Section
- [ ] **Action:** Update compliance requirements for MVP
- [ ] **Key Changes:**
  - GDPR Article 20: User data export feature (via dashboard UI)
  - GDPR Article 17: Account deletion feature (via user settings)
  - Data retention: 2 years inactive users, 2 years status history, status-based care reports
  - Photo retention: 180 days after care report closure
  - MFA for admins: Required with 7-day grace period
- [ ] **Files Affected:** `docs/SECURITY_REPORT_FOR_CEO.md` (Section 4)
- [ ] **Acceptance Criteria:**
  - User data export feature documented (not just API)
  - Account deletion feature documented (not just API)
  - All retention policies documented
  - MFA policy clearly stated

#### Task A4.4: Update Recommendations Section
- [ ] **Action:** Update recommendations with MVP priorities
- [ ] **Key Changes:**
  - Priority 1: Enable CloudTrail (1-year retention)
  - Priority 2: Deploy AWS WAF
  - Priority 3: Rotate secrets (180-day cycle)
  - Priority 4: Create incident response plan
  - Priority 5: Enable API rate limiting (100 req/min per user)
  - POST-MVP: Enable Security Hub and GuardDuty (~$54/month ongoing cost)
  - Priority 6: Implement MFA enforcement (7-day grace)
  - Priority 7: Implement data retention automation
  - Priority 8: Implement user data export/deletion features
- [ ] **Files Affected:** `docs/SECURITY_REPORT_FOR_CEO.md` (Section 8)
- [ ] **Acceptance Criteria:**
  - Recommendations prioritized for MVP
  - All 7 critical gaps addressed in recommendations
  - Timeline estimates provided

#### Task A4.5: Update Revision History
- [ ] **Action:** Add revision history entry for MVP v1.13 updates
- [ ] **Key Changes:**
  - Add entry: "Version 2.0 | 2026-01-17 | Chief Security Executive | Updated to reflect MVP v1.13: Trail Care Reports PII, 21 tables, all three authentication methods, CloudTrail 1-year retention, secrets 180-day rotation, MFA 7-day grace period, user data export/deletion features"
- [ ] **Files Affected:** `docs/SECURITY_REPORT_FOR_CEO.md` (bottom of file)
- [ ] **Acceptance Criteria:**
  - Revision entry added with all major security changes

**Dependencies:** Task A1.3 (backup) must be complete
**Complexity:** Large (L)
**Estimated Duration:** 2-3 hours

---

### Phase A5: Update MARKETING_PLAN.md (If Needed)

**Objective:** Verify marketing plan reflects MVP brand messaging requirement.

#### Task A5.1: Verify Brand Messaging is MVP Requirement
- [ ] **Action:** Confirm marketing plan documents brand messaging as MVP requirement
- [ ] **Key Verification:**
  - "Building communities, one trail at a time" byline documented
  - Brand messaging noted as Phase 1 of MVP implementation
  - Website and marketing materials update required for MVP
- [ ] **Files Affected:** `docs/MARKETING_PLAN.md` (Brand Positioning section)
- [ ] **Acceptance Criteria:**
  - Brand byline clearly documented
  - MVP requirement status confirmed
  - No additional updates needed (marketing plan already comprehensive)

**Dependencies:** Task A1.4 (backup) must be complete
**Complexity:** Small (S)
**Estimated Duration:** 15 minutes

---

## Section B: MVP Project Plan Creation

**🚨 CRITICAL CLARIFICATION 🚨**

**THIS SECTION IS ABOUT CREATING DOCUMENTATION, NOT IMPLEMENTING CODE!**

All tasks in Section B are about **WRITING CONTENT** into the `docs/MVP_PROJECT_PLAN.md` file. This file will DESCRIBE how to implement the 14 phases of the MVP, but we are NOT implementing those phases yet.

**What Section B Does:**
- ✅ Create a new file: `docs/MVP_PROJECT_PLAN.md`
- ✅ Write detailed documentation describing all 14 implementation phases
- ✅ Document tasks, dependencies, timelines, and acceptance criteria for future implementation
- ✅ This is a PLANNING document for the development team

**What Section B Does NOT Do:**
- ❌ Modify any code files (`web/`, `api-dynamo/`, `infra/`)
- ❌ Create infrastructure (CloudTrail, WAF, etc.)
- ❌ Implement authentication features
- ❌ Build iPhone apps
- ❌ ANY actual MVP feature implementation

**Example:** Task B3.2 "Detail Phase 2 Task - Enable CloudTrail" means:
- ✅ READ infra project to discover current implementation
- ✅ WRITE documentation in MVP_PROJECT_PLAN.md that describes how to enable CloudTrail
- ❌ NOT: Actually create CloudTrail infrastructure
- ❌ NOT: Write any code

---

### Phase B1: Create MVP_PROJECT_PLAN.md Foundation

**Objective:** Create the comprehensive MVP project plan document structure and front matter.

#### Task B1.1: Create MVP_PROJECT_PLAN.md File
- [ ] **Action:** Create new file `docs/MVP_PROJECT_PLAN.md`
- [ ] **Content:** Initial document structure with YAML front matter
- [ ] **Files Created:** `docs/MVP_PROJECT_PLAN.md`
- [ ] **Acceptance Criteria:**
  - File created in docs directory
  - YAML front matter includes title, author, date, abstract
  - Document version set to 1.0

#### Task B1.2: Add Document Header and Executive Summary
- [ ] **Action:** Write executive summary for project plan
- [ ] **Key Content:**
  - Chief Development Manager perspective
  - MVP scope: 14 phases, Q2 2026 launch
  - Pilot organizations: Hydrocut and GORBA (3 trail systems)
  - AI-assisted development approach (shorter timelines)
  - Existing codebase context (exploratory prototype in api-dynamo/, web/, infra/)
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md`
- [ ] **Acceptance Criteria:**
  - Executive summary written
  - Scope clearly defined
  - Timeline targets documented
  - AI-assisted approach explained

#### Task B1.3: Add Table of Contents Structure
- [ ] **Action:** Create comprehensive table of contents for all 14 phases
- [ ] **Required TOC Sections:**
  - Executive Summary
  - Project Overview
  - Implementation Approach
  - Existing Codebase Assessment
  - **Phase 1: Brand Messaging Update**
  - **Phase 2: Security Hardening**
  - **Phase 3: Authentication System**
  - **Phase 4: PII Protection**
  - **Phase 5: Trail System Data Model**
  - **Phase 6: Tag-Based Status Organization**
  - **Phase 7: Status Management**
  - **Phase 8: Scheduled Status Changes**
  - **Phase 9: Trail Care Reports System**
  - **Phase 10: Notification System**
  - **Phase 11: Web Dashboards**
  - **Phase 12: iPhone Apps**
  - **Phase 13: Pilot Onboarding**
  - **Phase 14: Testing and Validation**
  - Dependencies and Critical Path
  - Timeline and Milestones
  - Success Criteria
  - Revision History
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md`
- [ ] **Acceptance Criteria:**
  - All 14 phases in TOC
  - All sections listed above included
  - No placeholders or "TBD" entries

#### Task B1.4: Write Project Overview Section
- [ ] **Action:** Write comprehensive project overview
- [ ] **Key Content:**
  - MVP definition and scope
  - Trail systems model (NOT individual trails)
  - Core features: trail systems, Trail Care Reports, tag-based status, notifications, iPhone apps
  - Out of scope items (social media, Android, forums, etc.)
  - Pilot organization details
  - Success metrics
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md`
- [ ] **Acceptance Criteria:**
  - Project overview complete
  - In-scope and out-of-scope clearly defined
  - Success metrics documented

#### Task B1.5: Write Implementation Approach Section
- [ ] **Action:** Document implementation approach
- [ ] **Key Content:**
  - AI-assisted development methodology
  - Agile sprint structure (2-week sprints recommended)
  - Code review and quality assurance process
  - Testing strategy (unit, integration, end-to-end)
  - Documentation requirements
  - Constitution compliance
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md`
- [ ] **Acceptance Criteria:**
  - Implementation approach documented
  - AI-assisted methodology explained
  - Quality assurance process defined

#### Task B1.6: Write Existing Codebase Assessment Section
- [ ] **Action:** Document existing codebase and what needs to change
- [ ] **Key Content:**
  - **api-dynamo/**: FastAPI backend exists, needs updates for trail systems model, Trail Care Reports, tag-based status
  - **web/**: React frontend exists (26 pages), needs updates for MVP features
  - **infra/**: Infrastructure exists (DynamoDB, Cognito, S3, API Gateway), needs security hardening
  - **iPhone apps**: Do not exist, must be created from scratch
  - **Android apps**: Out of scope for MVP
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md`
- [ ] **Acceptance Criteria:**
  - Existing codebase documented
  - Required changes identified
  - Net-new development identified (iPhone apps)

**Dependencies:** Phase A2, A3, A4 (documentation updates) should be complete for reference
**Complexity:** Medium (M)
**Estimated Duration:** 1-2 hours

---

### Phase B2: Detail Phase 1 - Brand Messaging Update

**Objective:** Fully document Phase 1 implementation tasks.

#### Task B2.1: Write Phase 1 Overview
- [ ] **Action:** Document Phase 1 overview
- [ ] **Key Content:**
  - **Objective:** Update website and marketing materials with "Building communities, one trail at a time" byline
  - **Duration:** 1-2 days
  - **Priority:** HIGH (CTO's first priority)
  - **Dependencies:** None
  - **Rationale:** Low-hanging fruit, improves brand consistency from launch
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 1 section)
- [ ] **Acceptance Criteria:**
  - Phase overview complete
  - Objective clearly stated
  - Duration estimated

#### Task B2.2: Detail Phase 1 Tasks and Document What Needs to Change
- [ ] **Action:** Break down Phase 1 into detailed tasks and DOCUMENT what code changes will be required (write this documentation in MVP_PROJECT_PLAN.md)
- [ ] **Required Documentation Tasks:**
  1. **Document website homepage byline change**
     - File to document: `web/src/pages/Home.jsx` (or equivalent)
     - Change to document: Replace current byline with "Building communities, one trail at a time"
     - Testing to document: Verify homepage displays new byline
     - Acceptance criteria to document: New byline visible on homepage

  2. **Document website footer update**
     - File to document: `web/src/components/Footer.jsx` (or equivalent)
     - Change to document: Update footer tagline if present
     - Testing to document: Verify footer displays correctly across all pages
     - Acceptance criteria to document: Footer consistent with new brand messaging

  3. **Document About page update**
     - File to document: `web/src/pages/About.jsx` (or equivalent)
     - Change to document: Update mission/vision statements to align with new byline
     - Testing to document: Verify About page content consistency
     - Acceptance criteria to document: About page reflects "building communities" messaging

  4. **Document marketing materials update (if any exist)**
     - Files to document: Any PDFs, presentations, or marketing collateral in docs/ or assets/
     - Change to document: Update byline references
     - Testing to document: Review all materials for consistency
     - Acceptance criteria to document: All materials use new byline

  5. **Document PRODUCT_OVERVIEW_FOR_CEO.md brand section verification** (already done in Phase A2.4)
     - Documentation note: Section 11 (Company Positioning) reflects new byline
     - Acceptance: Document updated

  6. **Document MARKETING_PLAN.md brand section verification** (already done in Phase A5.1)
     - Documentation note: Section 1.2 documents new byline as MVP requirement
     - Acceptance: Document updated

  7. **Document codebase search for other byline references**
     - Action to document: Grep entire codebase for old byline text
     - Files to search: web/, docs/, api-dynamo/, facebook-api/
     - Change to document: Update any other references found
     - Acceptance criteria to document: No old byline references remain
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 1 tasks)
- [ ] **Acceptance Criteria:**
  - All 7 tasks documented in detail
  - Each task has file references, changes, testing, acceptance criteria
  - No vague or incomplete task descriptions

#### Task B2.3: Define Phase 1 Success Criteria
- [ ] **Action:** Document Phase 1 success criteria
- [ ] **Required Criteria:**
  - [ ] Website homepage displays "Building communities, one trail at a time" byline
  - [ ] Website footer updated (if applicable)
  - [ ] About page messaging aligned with new byline
  - [ ] All marketing materials updated
  - [ ] Documentation (PRODUCT_OVERVIEW, MARKETING_PLAN) updated
  - [ ] No old byline references found in codebase
  - [ ] Changes committed to git with clear commit message
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 1 success criteria)
- [ ] **Acceptance Criteria:**
  - All success criteria documented
  - Criteria are measurable and verifiable

#### Task B2.4: Estimate Phase 1 Timeline
- [ ] **Action:** Provide AI-assisted timeline estimate
- [ ] **Content:**
  - **Traditional Development:** 2-3 days (search/replace, testing, review)
  - **AI-Assisted Development:** 1-2 days (AI can quickly find/replace text, generate consistent messaging)
  - **Critical Path:** Not on critical path (can be done in parallel with other phases)
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 1 timeline)
- [ ] **Acceptance Criteria:**
  - Timeline estimate provided
  - AI-assisted benefits explained
  - Critical path status documented

**Dependencies:** Task B1.6 (existing codebase assessment) complete
**Complexity:** Medium (M)
**Estimated Duration:** 1 hour

---

### Phase B3: Detail Phase 2 - Security Hardening

**Objective:** Fully document Phase 2 implementation tasks for all 7 critical security gaps.

#### Task B3.1: Write Phase 2 Overview
- [ ] **Action:** Document Phase 2 overview
- [ ] **Key Content:**
  - **Objective:** Address all 7 critical security gaps identified in SECURITY_REPORT_FOR_CEO.md
  - **Duration:** 5-7 days (AI-assisted)
  - **Priority:** CRITICAL (required before production launch)
  - **Dependencies:** None (can start immediately)
  - **Rationale:** Security must be hardened before handling real user data
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 2 section)
- [ ] **Acceptance Criteria:**
  - Phase overview complete
  - All 7 security gaps listed
  - Duration estimated with AI-assisted context

#### Task B3.2: Detail Phase 2 Task - Document CloudTrail Enablement
- [ ] **Action:** Write documentation in MVP_PROJECT_PLAN.md describing how to enable CloudTrail (NOT actually enable it)
- [ ] **Required Documentation Content:**
  - **Task ID:** 2.1
  - **Task Name:** Enable AWS CloudTrail with 1-Year Retention
  - **Objective:** Enable audit logging for all AWS API calls
  - **Files to Document (that future developers will modify):**
    - `infra/cloudtrail.ts` (new file to create)
    - `infra/index.ts` (import CloudTrail stack)
    - `infra/s3.ts` (CloudTrail logs bucket configuration)
  - **Implementation Steps to Document:**
    1. Create dedicated S3 bucket for CloudTrail logs with versioning and encryption
    2. Configure CloudTrail to log all management events (read + write)
    3. Configure CloudTrail to log data events for DynamoDB, S3, Lambda
    4. Set 1-year (365-day) retention policy
    5. Enable log file validation for integrity checking
    6. Configure SNS topic for log file delivery notifications (optional)
    7. Test CloudTrail logging by performing API operations and verifying logs
  - **Testing:**
    - Verify CloudTrail is enabled in AWS Console
    - Perform test API operations (DynamoDB query, S3 upload, Lambda invoke)
    - Verify log files appear in S3 bucket within 15 minutes
    - Verify log file integrity validation works
    - Verify 1-year retention policy is set
  - **Acceptance Criteria:**
    - CloudTrail enabled for ca-central-1 region (dev environment)
    - All management and data events logged
    - Logs stored in encrypted S3 bucket
    - 1-year retention policy configured
    - Log file validation enabled
    - Test operations successfully logged
  - **Cost Impact:** ~$2-5/month
  - **AI-Assisted Timeline:** 4-6 hours (AI can generate Pulumi code, testing takes time)
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 2 Task 2.1)
- [ ] **Acceptance Criteria:**
  - Task documented in full detail
  - All implementation steps listed
  - Testing procedure defined
  - Acceptance criteria measurable

#### Task B3.3: Detail Phase 2 Task - Document AWS WAF Deployment
- [ ] **Action:** Write documentation in MVP_PROJECT_PLAN.md describing how to deploy AWS WAF (NOT actually deploy it)
- [ ] **Required Documentation Content:**
  - **Task ID:** 2.2
  - **Task Name:** Deploy AWS WAF for API Gateway and CloudFront
  - **Objective:** Protect against OWASP Top 10 exploits (XSS, SQL injection, etc.)
  - **Files to Document (that future developers will modify):**
    - `infra/waf.ts` (new file to create)
    - `infra/apigateway.ts` (associate WAF with API Gateway)
    - `infra/cloudfront.ts` (associate WAF with CloudFront, if exists)
  - **Implementation Steps to Document:**
    1. Create AWS WAF WebACL for API Gateway (Regional WAF)
    2. Add AWS Managed Rule Sets:
       - AWSManagedRulesCommonRuleSet (OWASP Top 10)
       - AWSManagedRulesKnownBadInputsRuleSet (malicious payloads)
       - AWSManagedRulesSQLiRuleSet (SQL injection prevention)
       - AWSManagedRulesLinuxRuleSet (Linux-specific exploits)
    3. Configure rate limiting rule: 100 requests per 5 minutes per IP
    4. Associate WAF WebACL with API Gateway
    5. Create CloudFront WAF WebACL if CloudFront exists
    6. Configure CloudWatch alarms for blocked requests
    7. Test WAF by simulating attacks (XSS, SQL injection)
  - **Testing:**
    - Send benign request → should succeed
    - Send XSS payload in query parameter → should be blocked
    - Send SQL injection attempt → should be blocked
    - Send 101 requests in 5 minutes → should be rate limited
    - Verify CloudWatch metrics show blocked requests
  - **Acceptance Criteria:**
    - AWS WAF enabled for API Gateway
    - All 4 managed rule sets enabled
    - Rate limiting rule configured (100 req/5min per IP)
    - Test attacks successfully blocked
    - CloudWatch alarms configured
  - **Cost Impact:** ~$5-20/month
  - **AI-Assisted Timeline:** 6-8 hours (AI generates WAF rules, testing requires manual attack simulation)
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 2 Task 2.2)
- [ ] **Acceptance Criteria:**
  - Task documented in full detail
  - All managed rule sets listed
  - Testing includes attack simulation
  - Acceptance criteria measurable

#### Task B3.4: Detail Phase 2 Task - Document Secrets Rotation
- [ ] **Action:** Write documentation in MVP_PROJECT_PLAN.md describing how to rotate secrets (NOT actually rotate them)
- [ ] **Required Documentation Content:**
  - **Task ID:** 2.3
  - **Task Name:** Rotate Secrets and Remove "CHANGE_ME_IN_PRODUCTION" Placeholders
  - **Objective:** Replace placeholder secrets with strong random values and enable automatic rotation
  - **Files to Document (that future developers will modify):**
    - `infra/secrets.ts` (update all secrets)
    - `api-dynamo/.env.example` (update with secret references)
    - `web/.env.example` (update with secret references)
    - Any hardcoded secrets in codebase (search for "CHANGE_ME")
  - **Implementation Steps to Document:**
    1. Identify all secrets in codebase:
       - Search for "CHANGE_ME_IN_PRODUCTION"
       - Search for "password", "secret", "key", "token" in env files
       - Review Secrets Manager entries in AWS Console
    2. Generate strong random secrets (32+ characters, cryptographically secure)
    3. Store secrets in AWS Secrets Manager:
       - Database passwords
       - JWT signing keys
       - API keys for third-party services (Twilio/Pinpoint, Mapbox)
       - OAuth client secrets
    4. Enable automatic 180-day rotation for all secrets
    5. Update application code to retrieve secrets from Secrets Manager (not env files)
    6. Test application with new secrets
    7. Document secret retrieval process for developers
  - **Testing:**
    - Verify no "CHANGE_ME" strings exist in codebase
    - Verify all secrets stored in AWS Secrets Manager
    - Verify 180-day rotation enabled for all secrets
    - Verify application starts and connects to database with new secrets
    - Verify API endpoints work with new JWT signing keys
  - **Acceptance Criteria:**
    - All placeholder secrets removed
    - All secrets stored in AWS Secrets Manager
    - 180-day automatic rotation enabled
    - Application functions correctly with new secrets
    - Secret retrieval documented in CLAUDE.md or README
  - **Cost Impact:** ~$0.40 per secret per month (~$5-10/month total)
  - **AI-Assisted Timeline:** 4-6 hours (AI can search for secrets, generate strong values)
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 2 Task 2.3)
- [ ] **Acceptance Criteria:**
  - Task documented in full detail
  - All secret types listed
  - Testing verifies no placeholders remain
  - Acceptance criteria measurable

#### Task B3.5: Detail Phase 2 Task - Document Incident Response Plan Creation
- [ ] **Action:** Write documentation in MVP_PROJECT_PLAN.md describing how to create incident response plan (NOT actually create it)
- [ ] **Required Documentation Content:**
  - **Task ID:** 2.4
  - **Task Name:** Create Incident Response Plan and Runbook
  - **Objective:** Document procedures for handling security incidents and GDPR breach notifications
  - **Files to Document (that future developers will create):**
    - `docs/INCIDENT_RESPONSE_PLAN.md`
    - `docs/SECURITY_CONTACTS.md`
  - **Implementation Steps to Document:**
    1. Define incident severity levels (P1: Critical, P2: High, P3: Medium, P4: Low)
    2. Document escalation procedures:
       - Who gets notified for each severity level
       - Escalation timeline (P1: immediate, P2: 1 hour, etc.)
       - Contact information for security team
    3. Create GDPR breach notification process:
       - 72-hour notification requirement
       - Breach assessment checklist
       - User notification templates
       - Regulatory authority contacts (Privacy Commissioner of Canada)
    4. Create security contact email: security@traillenshq.com
    5. Document incident response runbook:
       - Initial assessment steps
       - Containment procedures
       - Evidence preservation
       - Communication templates
       - Post-incident review process
    6. Assign security lead (CTO for MVP)
    7. Train team on incident response procedures
  - **Testing:**
    - Conduct tabletop exercise (simulate breach scenario)
    - Verify all contacts are reachable
    - Verify email alias security@traillenshq.com works
    - Time the exercise to ensure 72-hour notification is achievable
  - **Acceptance Criteria:**
    - Incident response plan document created and reviewed
    - GDPR breach notification process documented
    - Security contact email configured
    - Security lead assigned
    - Team trained (at least CTO and one developer)
    - Tabletop exercise conducted
  - **Cost Impact:** $0 (internal time only)
  - **AI-Assisted Timeline:** 4-6 hours (AI can generate plan template, team training takes time)
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 2 Task 2.4)
- [ ] **Acceptance Criteria:**
  - Task documented in full detail
  - All runbook sections listed
  - Tabletop exercise included in testing
  - Acceptance criteria measurable

#### Task B3.6: Detail Phase 2 Task - Document API Rate Limiting Enablement
- [ ] **Action:** Write documentation in MVP_PROJECT_PLAN.md describing how to enable API rate limiting (NOT actually enable it)
- [ ] **Required Documentation Content:**
  - **Task ID:** 2.5
  - **Task Name:** Enable API Gateway Rate Limiting and Throttling
  - **Objective:** Prevent DDoS attacks, credential stuffing, and brute force attempts
  - **Files to Document (that future developers will modify):**
    - `infra/apigateway.ts` (enable throttling)
    - `api-dynamo/middleware/rate-limit.ts` (per-user rate limiting, may need to create)
  - **Implementation Steps to Document:**
    1. Enable API Gateway throttling:
       - Burst limit: 200 requests
       - Steady-state limit: 100 requests/second (account-level)
    2. Implement per-user rate limiting (100 requests/minute per user):
       - Extract user_id from JWT token
       - Track request counts in Redis (or DynamoDB if Redis not enabled)
       - Return HTTP 429 (Too Many Requests) when limit exceeded
    3. Implement per-IP rate limiting for unauthenticated endpoints:
       - Login endpoint: 5 attempts per 15 minutes per IP
       - Password reset: 3 attempts per hour per IP
       - Registration: 10 attempts per hour per IP
    4. Configure API Gateway usage plans and API keys for partner integrations (future)
    5. Add rate limit headers to responses:
       - X-RateLimit-Limit
       - X-RateLimit-Remaining
       - X-RateLimit-Reset
    6. Configure CloudWatch alarms for rate limit violations
  - **Testing:**
    - Send 101 requests/minute from single user → verify 429 response
    - Send 6 failed login attempts in 15 minutes → verify lockout
    - Verify rate limit headers in response
    - Verify CloudWatch alarms trigger on excessive requests
  - **Acceptance Criteria:**
    - API Gateway throttling enabled (200 burst, 100/sec steady)
    - Per-user rate limiting implemented (100 req/min)
    - Per-IP rate limiting for auth endpoints
    - Rate limit headers in responses
    - CloudWatch alarms configured
    - Test scenarios all pass
  - **Cost Impact:** $0 (included in API Gateway pricing)
  - **AI-Assisted Timeline:** 6-8 hours (AI generates middleware, testing requires multiple API calls)
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 2 Task 2.5)
- [ ] **Acceptance Criteria:**
  - Task documented in full detail
  - All rate limit types listed (account, user, IP)
  - Testing includes multiple scenarios
  - Acceptance criteria measurable

#### Task B3.7: Detail Phase 2 Task - Document Security Hub and GuardDuty Enablement (POST-MVP)

- [ ] **Action:** **TASK MOVED TO POST-MVP** due to ongoing cost (~$54/month). This task is documentation-only and will be written for post-MVP implementation.
- [ ] **Required Documentation Content:**
  - **Task ID:** 2.6
  - **Task Name:** Enable AWS Security Hub and GuardDuty
  - **Objective:** Continuous compliance monitoring and threat detection
  - **Files to Document (that future developers will create):**
    - `infra/security-hub.ts` (new file to create)
    - `infra/guardduty.ts` (new file to create)
  - **Implementation Steps to Document:**
    1. Enable AWS Security Hub:
       - Enable Security Hub in ca-central-1
       - Enable security standards:
         - AWS Foundational Security Best Practices
         - CIS AWS Foundations Benchmark (if applicable)
       - Configure SNS topic for high/critical findings
       - Create CloudWatch dashboard for security findings
    2. Enable AWS GuardDuty:
       - Enable GuardDuty in ca-central-1
       - Configure S3 protection (monitors S3 access patterns)
       - Configure SNS topic for high/critical findings
       - Configure automated remediation for common threats (optional)
    3. Configure CloudWatch alarms:
       - Alarm on critical Security Hub findings
       - Alarm on high-severity GuardDuty findings
       - Alarm on failed compliance checks
    4. Create security monitoring dashboard:
       - Security Hub compliance score
       - GuardDuty findings summary
       - CloudTrail event volume
       - WAF blocked requests
    5. Document security monitoring procedures:
       - Daily review of security findings
       - Weekly compliance score review
       - Monthly security posture report
  - **Testing:**
    - Verify Security Hub enabled in AWS Console
    - Verify GuardDuty enabled in AWS Console
    - Generate test GuardDuty finding (simulate suspicious activity)
    - Verify SNS notifications sent for findings
    - Verify CloudWatch alarms trigger
    - Verify security dashboard displays findings
  - **Acceptance Criteria:**
    - Security Hub enabled with AWS Foundational Security Best Practices standard
    - GuardDuty enabled with S3 protection
    - SNS notifications configured for high/critical findings
    - CloudWatch alarms configured
    - Security dashboard created
    - Test finding generates notification
    - Monitoring procedures documented
  - **Cost Impact:** ~$5-10/month
  - **AI-Assisted Timeline:** 4-6 hours (AI generates infrastructure code, testing requires simulated threats)
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 2 Task 2.6)
- [ ] **Acceptance Criteria:**
  - Task documented in full detail
  - All security tools listed (Security Hub, GuardDuty)
  - Monitoring procedures documented
  - Acceptance criteria measurable

#### Task B3.8: Detail Phase 2 Task - Document MFA Enforcement Implementation
- [ ] **Action:** Write documentation in MVP_PROJECT_PLAN.md describing how to implement MFA enforcement (NOT actually implement it)
- [ ] **Required Documentation Content:**
  - **Task ID:** 2.7
  - **Task Name:** Implement MFA Enforcement with 7-Day Grace Period
  - **Objective:** Require MFA for org-admin, trailsystem-owner, and superadmin roles
  - **Files to Document (that future developers will modify/create):**
    - `infra/cognito.ts` (update Cognito User Pool configuration)
    - `api-dynamo/middleware/mfa-enforcement.ts` (new file to create)
    - `web/src/pages/SetupMFA.jsx` (new page to create)
  - **Implementation Steps to Document:**
    1. Enable MFA in Cognito User Pool:
       - Optional MFA for all users (SMS or TOTP)
       - Require MFA for org-admin, trailsystem-owner, superadmin groups
    2. Implement 7-day grace period logic:
       - Track user first login date
       - Allow 7 days from first login before enforcing MFA
       - Send daily email reminders during grace period
       - After 7 days, redirect to MFA setup page on login
       - Block access to app until MFA configured
    3. Create MFA setup page in web app:
       - QR code for TOTP app (Google Authenticator, Authy)
       - SMS option (backup method)
       - Verification step (user must enter code to confirm)
    4. Update login flow:
       - Check if user is admin role (org-admin, trailsystem-owner, superadmin)
       - Check if MFA enabled for user
       - If not enabled, check grace period
       - If grace period expired, redirect to MFA setup
    5. Create email reminder templates:
       - Day 1: "Welcome! Please enable MFA within 7 days"
       - Day 3: "Reminder: Enable MFA within 4 days"
       - Day 6: "Final reminder: Enable MFA by tomorrow"
       - Day 7: "MFA required: Your access is now restricted"
    6. Test MFA enforcement:
       - Create test admin user
       - Verify 7-day grace period
       - Verify email reminders sent
       - Verify MFA setup page
       - Verify access blocked after 7 days without MFA
  - **Testing:**
    - Create test org-admin user
    - Login and verify grace period starts
    - Verify email reminder received on Day 1
    - Wait 7 days (or simulate by changing user's first_login date)
    - Verify login redirects to MFA setup page
    - Verify access blocked until MFA enabled
    - Enable MFA and verify access restored
    - Verify non-admin users not affected
  - **Acceptance Criteria:**
    - MFA enabled in Cognito for optional use
    - 7-day grace period implemented for admin roles
    - Email reminders sent daily during grace period
    - MFA setup page created and functional
    - Access blocked after 7 days without MFA
    - Non-admin users not affected
    - Test scenarios all pass
  - **Cost Impact:** ~$0.50/month (SMS costs for MFA verification, minimal)
  - **AI-Assisted Timeline:** 8-10 hours (AI generates MFA setup UI, testing requires time-based verification)
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 2 Task 2.7)
- [ ] **Acceptance Criteria:**
  - Task documented in full detail
  - Grace period logic clearly explained
  - Email reminder flow documented
  - Testing includes time-based scenarios
  - Acceptance criteria measurable

#### Task B3.9: Define Phase 2 Success Criteria
- [ ] **Action:** Document Phase 2 success criteria
- [ ] **Required Criteria:**
  - [ ] CloudTrail enabled with 1-year retention
  - [ ] AWS WAF deployed and blocking test attacks
  - [ ] All placeholder secrets replaced with strong random values
  - [ ] 180-day automatic secrets rotation enabled
  - [ ] Incident response plan created and team trained
  - [ ] Security contact email configured
  - [ ] API rate limiting enabled (100 req/min per user)
  - [ ] Security Hub and GuardDuty **moved to POST-MVP** (cost: ~$54/month)
  - [ ] MFA enforcement implemented with 7-day grace period
  - [ ] All CloudWatch alarms configured
  - [ ] All security tasks committed to git
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 2 success criteria)
- [ ] **Acceptance Criteria:**
  - All success criteria documented
  - Criteria are measurable and verifiable

#### Task B3.10: Estimate Phase 2 Timeline
- [ ] **Action:** Provide AI-assisted timeline estimate
- [ ] **Content:**
  - **Traditional Development:** 10-14 days (infrastructure setup, testing, documentation)
  - **AI-Assisted Development:** 5-7 days (AI generates infrastructure code, policies, testing procedures)
  - **Critical Path:** On critical path (must complete before production deployment)
  - **Parallelization:** Tasks 2.1-2.3 can be done in parallel; Tasks 2.4-2.7 can be done in parallel after 2.1-2.3
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 2 timeline)
- [ ] **Acceptance Criteria:**
  - Timeline estimate provided
  - AI-assisted benefits explained
  - Parallelization opportunities identified
  - Critical path status documented

**Dependencies:** Phase B1 complete
**Complexity:** Extra Large (XL)
**Estimated Duration:** 3-4 hours to document fully

---

### Phase B4: Detail Phase 3 - Authentication System

**Objective:** Fully document Phase 3 implementation for all three authentication methods (passkey, magic link, email/password).

#### Task B4.1: Write Phase 3 Overview
- [ ] **Action:** Document Phase 3 overview
- [ ] **Key Content:**
  - **Objective:** Implement all three authentication methods (passkey, magic link, email/password)
  - **Duration:** 7-10 days (AI-assisted)
  - **Priority:** HIGH (required for MVP)
  - **Dependencies:** Phase 2 (Cognito User Pool configured, MFA ready)
  - **Rationale:** Triple authentication approach maximizes security and compatibility
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 3 section)
- [ ] **Acceptance Criteria:**
  - Phase overview complete
  - All three methods listed
  - Duration estimated

#### Task B4.2: Detail Phase 3 Task - Document Passkey Authentication
- [ ] **Action:** Write documentation in MVP_PROJECT_PLAN.md describing how to implement passkey authentication (NOT actually implement it)
- [ ] **Required Documentation Content:**
  - **Task ID:** 3.1
  - **Task Name:** Implement Passkey Authentication (WebAuthn/FIDO2)
  - **Objective:** Enable passwordless authentication via biometrics (Touch ID, Face ID, security keys)
  - **Research Required:** Determine if AWS Cognito supports passkeys natively (as of Q1 2026)
  - **Files to Document (that future developers will modify/create):**
    - `infra/cognito.ts` (passkey configuration if native support)
    - `web/src/auth/passkey.ts` (WebAuthn client-side implementation)
    - `api-dynamo/auth/passkey.py` (WebAuthn server-side implementation if custom)
    - `web/src/pages/RegisterPasskey.jsx` (passkey registration page)
    - `web/src/pages/LoginPasskey.jsx` (passkey login page)
  - **Implementation Steps to Document:**
    1. Research AWS Cognito passkey support:
       - If supported: Use Cognito native passkey features
       - If not supported: Implement custom WebAuthn integration
    2. If custom WebAuthn required:
       - Add WebAuthn library: py_webauthn (Python) or @simplewebauthn/server (Node)
       - Add client library: @simplewebauthn/browser
       - Create registration ceremony:
         - Generate challenge (server)
         - Request credential creation (browser)
         - Verify attestation (server)
         - Store credential public key in users table
       - Create authentication ceremony:
         - Generate challenge (server)
         - Request credential assertion (browser)
         - Verify assertion (server)
         - Issue JWT token
    3. If Cognito native:
       - Enable passkey authentication in Cognito User Pool
       - Configure relying party ID (traillenshq.com)
       - Configure passkey options (platform authenticators, cross-platform authenticators)
    4. Create passkey registration UI:
       - "Register with Passkey" button
       - Browser compatibility check (WebAuthn API support)
       - Error handling (no authenticator, registration failed)
    5. Create passkey login UI:
       - "Login with Passkey" button
       - Email input (to identify user)
       - Passkey authentication prompt
       - Error handling (passkey not found, authentication failed)
    6. Test passkey flows:
       - Registration on macOS (Touch ID)
       - Registration on iOS (Face ID)
       - Registration with hardware security key (YubiKey)
       - Login with Touch ID, Face ID, YubiKey
       - Cross-device passkeys (if supported)
  - **Testing:**
    - Register passkey on macOS with Touch ID → should succeed
    - Login with Touch ID → should succeed and issue JWT
    - Register passkey on iOS with Face ID → should succeed
    - Login with Face ID → should succeed
    - Register passkey with YubiKey → should succeed
    - Login with YubiKey → should succeed
    - Try passkey on unsupported browser → should show error message
    - Verify JWT token contains correct user_id and claims
  - **Acceptance Criteria:**
    - Passkey registration flow implemented
    - Passkey login flow implemented
    - Works with Touch ID, Face ID, security keys
    - JWT token issued on successful authentication
    - Error handling for unsupported browsers/devices
    - All test scenarios pass
  - **Cost Impact:** $0 (if Cognito native), minimal if custom
  - **AI-Assisted Timeline:** 12-16 hours (AI can generate WebAuthn implementation, testing requires multiple devices)
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 3 Task 3.1)
- [ ] **Acceptance Criteria:**
  - Task documented in full detail
  - Research step included
  - Both Cognito native and custom paths documented
  - Testing includes multiple device types
  - Acceptance criteria measurable

#### Task B4.3: Detail Phase 3 Task - Document Magic Link Authentication
- [ ] **Action:** Write documentation in MVP_PROJECT_PLAN.md describing how to implement magic link authentication (NOT actually implement it)
- [ ] **Required Documentation Content:**
  - **Task ID:** 3.2
  - **Task Name:** Implement Magic Link Authentication (Email-Based Passwordless)
  - **Objective:** Enable passwordless authentication via time-limited email links
  - **Files to Document (that future developers will modify/create):**
    - `api-dynamo/auth/magic-link.py` (magic link generation and verification)
    - `web/src/pages/LoginMagicLink.jsx` (magic link request page)
    - `web/src/pages/VerifyMagicLink.jsx` (magic link verification page)
    - `api-dynamo/templates/magic-link-email.html` (email template)
  - **Implementation Steps to Document:**
    1. Create magic link request endpoint:
       - Accept email address
       - Check if user exists (if not, optionally auto-create)
       - Generate short-lived JWT token (15-minute expiration)
       - Create magic link URL: https://traillenshq.com/auth/verify?token=<JWT>
       - Send email via AWS SES with magic link
       - Return success response (do not leak if user exists or not)
    2. Create magic link verification endpoint:
       - Accept JWT token from URL query parameter
       - Verify token signature
       - Check token expiration (15 minutes)
       - Check token is single-use (mark as used in database or cache)
       - Issue long-lived JWT token for app authentication
       - Redirect to dashboard
    3. Create magic link email template:
       - Subject: "Your TrailLensHQ login link"
       - Body:
         - Greeting
         - "Click here to login: [Magic Link Button]"
         - "This link expires in 15 minutes"
         - "If you didn't request this, ignore this email"
       - HTML + plain text versions
    4. Implement single-use token logic:
       - Store used tokens in Redis (if enabled) or DynamoDB
       - TTL: 15 minutes (auto-delete after expiration)
       - Check token is not in "used tokens" set before issuing auth JWT
    5. Create UI flows:
       - Login page: "Login with Magic Link" button
       - Magic link request page: Email input + "Send Link" button
       - Success message: "Check your email for login link"
       - Verification page: Auto-redirect after token verification
    6. Test magic link flows:
       - Request magic link
       - Receive email
       - Click link
       - Verify redirect to dashboard
       - Verify JWT issued
       - Try using link twice → should fail second time
       - Try using expired link → should fail
  - **Testing:**
    - Request magic link for existing user → email received
    - Click link within 15 minutes → successfully logged in
    - Request magic link, wait 16 minutes → link expired
    - Click link twice → second attempt fails (single-use)
    - Request magic link for non-existent user → handle gracefully (optional: auto-create or error)
    - Verify JWT token contains correct user_id
    - Verify email template renders correctly (HTML + plain text)
  - **Acceptance Criteria:**
    - Magic link request endpoint implemented
    - Magic link verification endpoint implemented
    - 15-minute token expiration enforced
    - Single-use token logic implemented
    - Email template created (HTML + plain text)
    - UI flows implemented
    - All test scenarios pass
  - **Cost Impact:** ~$0.10 per 1000 emails (AWS SES)
  - **AI-Assisted Timeline:** 8-10 hours (AI generates JWT logic and email templates)
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 3 Task 3.2)
- [ ] **Acceptance Criteria:**
  - Task documented in full detail
  - Single-use token logic clearly explained
  - Email template documented
  - Testing includes expiration and reuse scenarios
  - Acceptance criteria measurable

#### Task B4.4: Detail Phase 3 Task - Document Email/Password Authentication
- [ ] **Action:** Write documentation in MVP_PROJECT_PLAN.md describing how to implement email/password authentication (NOT actually implement it)
- [ ] **Required Documentation Content:**
  - **Task ID:** 3.3
  - **Task Name:** Implement Email/Password Authentication with Strong Password Policy
  - **Objective:** Traditional authentication with strong password requirements
  - **Files to Document (that future developers will modify/create):**
    - `infra/cognito.ts` (password policy configuration)
    - `web/src/pages/Register.jsx` (registration form)
    - `web/src/pages/Login.jsx` (login form)
    - `web/src/pages/ForgotPassword.jsx` (password reset flow)
  - **Implementation Steps to Document:**
    1. Configure Cognito password policy:
       - Minimum length: 12 characters
       - Require uppercase letter
       - Require lowercase letter
       - Require number
       - Require special character
       - Password history: 6 (prevent reuse of last 6 passwords)
       - Temporary password validity: 7 days
    2. Create registration flow:
       - Email input (validated)
       - Password input (strength indicator)
       - Confirm password input (must match)
       - Terms of service checkbox
       - Submit button
       - Email verification required before account activation
    3. Create login flow:
       - Email input
       - Password input
       - "Remember me" checkbox (optional)
       - "Forgot password" link
       - Submit button
       - Handle errors (invalid credentials, account not verified)
    4. Create password reset flow:
       - Email input
       - Send verification code to email
       - Code input (6-digit code)
       - New password input (must meet policy)
       - Confirm new password
       - Submit button
    5. Implement password strength indicator:
       - Weak (red): < 8 chars or missing requirements
       - Fair (orange): 8-11 chars, meets some requirements
       - Good (yellow): 12-15 chars, meets all requirements
       - Strong (green): 16+ chars, meets all requirements
    6. Test email/password flows:
       - Register new user
       - Verify email
       - Login with email/password
       - Logout
       - Forgot password flow
       - Reset password
       - Login with new password
  - **Testing:**
    - Register with weak password → should be rejected
    - Register with strong password → should succeed
    - Verify email verification required
    - Login with unverified account → should fail
    - Verify email and login → should succeed
    - Login with wrong password → should fail
    - Request password reset → code sent to email
    - Reset password with code → should succeed
    - Login with new password → should succeed
    - Verify JWT token contains correct user_id and roles
  - **Acceptance Criteria:**
    - Cognito password policy configured (12 char min, complexity requirements)
    - Registration flow implemented with password strength indicator
    - Login flow implemented
    - Password reset flow implemented
    - Email verification required
    - All test scenarios pass
  - **Cost Impact:** $0 (included in Cognito pricing)
  - **AI-Assisted Timeline:** 6-8 hours (AI generates forms and validation logic)
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 3 Task 3.3)
- [ ] **Acceptance Criteria:**
  - Task documented in full detail
  - Password policy requirements listed
  - Password strength indicator documented
  - Testing includes verification flow
  - Acceptance criteria measurable

#### Task B4.5: Detail Phase 3 Task - Document Unified Login Experience
- [ ] **Action:** Write documentation in MVP_PROJECT_PLAN.md describing how to create unified login experience (NOT actually create it)
- [ ] **Required Documentation Content:**
  - **Task ID:** 3.4
  - **Task Name:** Create Unified Login Page with All Three Methods
  - **Objective:** Single login page offering all three authentication options
  - **Files to Document (that future developers will modify/create):**
    - `web/src/pages/Login.jsx` (unified login page)
    - `web/src/components/AuthMethodSelector.jsx` (method selection component)
  - **Implementation Steps to Document:**
    1. Create unified login page layout:
       - Header: "Login to TrailLensHQ"
       - Three sections:
         - "Login with Passkey" button (primary, recommended)
         - "Login with Magic Link" button (secondary)
         - "Login with Email/Password" section (traditional)
       - Visual hierarchy: Passkey most prominent, email/password least prominent
    2. Implement method selection:
       - Default: Show all three options
       - Remember user's preferred method (localStorage)
       - Show preferred method first on return visit
    3. Add browser compatibility detection:
       - If WebAuthn not supported, hide passkey option
       - Show message: "Your browser doesn't support passkeys. Try magic link or email/password."
    4. Add helpful messaging:
       - "Passkey (Recommended): Fastest and most secure"
       - "Magic Link: No password needed, check your email"
       - "Email/Password: Traditional login method"
    5. Implement seamless flow:
       - User selects method
       - Authenticate
       - Redirect to dashboard on success
       - Show appropriate error messages on failure
    6. Test unified login page:
       - Test all three methods from single page
       - Verify method preference is remembered
       - Verify browser compatibility detection
       - Verify error handling for each method
  - **Testing:**
    - Login with passkey → should work
    - Login with magic link → should work
    - Login with email/password → should work
    - Select passkey, close browser, return → passkey option shown first
    - Test on browser without WebAuthn → passkey option hidden
    - Test error scenarios for each method
  - **Acceptance Criteria:**
    - Unified login page created
    - All three methods accessible from one page
    - Browser compatibility detection working
    - Method preference remembered
    - All test scenarios pass
  - **Cost Impact:** $0
  - **AI-Assisted Timeline:** 4-6 hours (AI generates unified UI)
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 3 Task 3.4)
- [ ] **Acceptance Criteria:**
  - Task documented in full detail
  - UI layout described
  - Browser compatibility handling documented
  - Acceptance criteria measurable

#### Task B4.6: Define Phase 3 Success Criteria
- [ ] **Action:** Document Phase 3 success criteria
- [ ] **Required Criteria:**
  - [ ] Passkey authentication implemented and tested (Touch ID, Face ID, security keys)
  - [ ] Magic link authentication implemented and tested (15-min expiration, single-use)
  - [ ] Email/password authentication implemented with strong password policy (12 char min)
  - [ ] Unified login page created with all three methods
  - [ ] Browser compatibility detection working
  - [ ] JWT tokens issued correctly for all three methods
  - [ ] Error handling implemented for all failure scenarios
  - [ ] All test scenarios pass
  - [ ] Changes committed to git
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 3 success criteria)
- [ ] **Acceptance Criteria:**
  - All success criteria documented
  - Criteria measurable and verifiable

#### Task B4.7: Estimate Phase 3 Timeline
- [ ] **Action:** Provide AI-assisted timeline estimate
- [ ] **Content:**
  - **Traditional Development:** 14-18 days (WebAuthn research, implementation, testing across devices)
  - **AI-Assisted Development:** 7-10 days (AI generates auth flows, testing still requires devices)
  - **Critical Path:** On critical path (required for user login)
  - **Parallelization:** Passkey, magic link, email/password can be developed in parallel by different devs
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 3 timeline)
- [ ] **Acceptance Criteria:**
  - Timeline estimate provided
  - AI-assisted benefits explained
  - Parallelization opportunities noted

**Dependencies:** Phase B3 complete (Phase 2 security hardening must finish first)
**Complexity:** Extra Large (XL)
**Estimated Duration:** 3-4 hours to document fully

---

### Phase B5: Detail Phases 4-14

**Objective:** Fully document all remaining phases (4-14) with same level of detail as Phases 1-3.

#### Task B5.1: Detail Phase 4 - PII Protection (DOCUMENTATION ONLY)
- [ ] **Action:** Write Phase 4 section in MVP_PROJECT_PLAN.md with comprehensive task breakdown (NOT implement the tasks)
- [ ] **Required Documentation Content:**
  - Phase overview (objective, duration, priority, dependencies)
  - **Document Task 4.1:** Implement data retention policies (describe how future developers will do this)
  - **Document Task 4.2:** Implement user data export feature (UI-accessible, not just API)
  - **Document Task 4.3:** Implement account deletion feature (UI-accessible, not just API)
  - **Document Task 4.4:** Create automated retention cleanup job
  - Success criteria
  - Timeline estimate (AI-assisted)
- [ ] **Each Task Documentation Must Include:**
  - Task ID and name
  - Objective
  - Files to document (specific file paths that future developers will modify/create)
  - Implementation steps to document (detailed, numbered)
  - Testing procedures to document (specific test cases)
  - Acceptance criteria to document (measurable)
  - Cost impact (if applicable)
  - AI-assisted timeline
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 4 section)
- [ ] **Acceptance Criteria:**
  - Phase 4 fully documented with all tasks
  - No placeholders or "TBD" entries
  - All tasks have implementation steps, testing, acceptance criteria

#### Task B5.2: Detail Phase 5 - Trail System Data Model (DOCUMENTATION ONLY)
- [ ] **Action:** Write Phase 5 section in MVP_PROJECT_PLAN.md with comprehensive task breakdown (NOT implement the tasks)
- [ ] **Required Documentation Content:**
  - Phase overview
  - **Document Task 5.1:** Create trail_systems DynamoDB table (describe schema, GSIs, etc.)
  - **Document Task 5.2:** Create trail_system_history DynamoDB table
  - **Document Task 5.3:** Implement trail system CRUD API endpoints
  - **Document Task 5.4:** Implement trail system cover photo upload to S3
  - **Document Task 5.5:** Update web UI for trail system management
  - Success criteria
  - Timeline estimate
- [ ] **Each Task Documentation Must Include:** Files to document (that future developers will modify/create), implementation steps to document, testing to document, acceptance criteria to document
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 5 section)
- [ ] **Acceptance Criteria:**
  - Phase 5 fully documented
  - Trail systems model clearly explained (NOT individual trails)
  - All tasks detailed

#### Task B5.3: Detail Phase 6 - Tag-Based Status Organization (DOCUMENTATION ONLY)
- [ ] **Action:** Write Phase 6 section in MVP_PROJECT_PLAN.md (NOT implement the tasks)
- [ ] **Required Documentation Content:**
  - Phase overview
  - **Document Task 6.1:** Create status_tags DynamoDB table
  - **Document Task 6.2:** Implement status tag CRUD API endpoints
  - **Document Task 6.3:** Implement tag assignment to status types
  - **Document Task 6.4:** Implement sticky tag filtering in change status interface
  - **Document Task 6.5:** Update web UI for tag management
  - Success criteria (max 10 tags per org enforced)
  - Timeline estimate
- [ ] **Each Task Documentation Must Include:** Files to document, implementation steps to document, testing to document
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 6 section)
- [ ] **Acceptance Criteria:**
  - Phase 6 fully documented
  - Tag system clearly explained
  - 10-tag limit enforcement documented

#### Task B5.4: Detail Phase 7 - Status Management (DOCUMENTATION ONLY)
- [ ] **Action:** Write Phase 7 section in MVP_PROJECT_PLAN.md (NOT implement the tasks)
- [ ] **Required Documentation Content:**
  - Phase overview
  - **Document Task 7.1:** Implement status type management (CRUD, max 30 per org)
  - **Document Task 7.2:** Implement status update workflow (apply status to trail system)
  - **Document Task 7.3:** Implement two-level photo system (default + update photos)
  - **Document Task 7.4:** Implement season assignment
  - **Document Task 7.5:** Implement status history (2-year retention)
  - **Document Task 7.6:** Implement bulk status updates
  - **Document Task 7.7:** Create status type templates for onboarding
  - Success criteria
  - Timeline estimate
- [ ] **Each Task Documentation Must Include:** Files to document, implementation steps to document, testing to document
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 7 section)
- [ ] **Acceptance Criteria:**
  - Phase 7 fully documented
  - Status model clearly explained (types vs updates vs tags)
  - All features detailed

#### Task B5.5: Detail Phase 8 - Scheduled Status Changes (DOCUMENTATION ONLY)
- [ ] **Action:** Write Phase 8 section in MVP_PROJECT_PLAN.md (NOT implement the tasks)
- [ ] **Required Documentation Content:**
  - Phase overview
  - **Document Task 8.1:** Create scheduled_status_changes DynamoDB table
  - **Document Task 8.2:** Implement scheduled changes CRUD API endpoints
  - **Document Task 8.3:** Implement cron job for automated status changes
  - **Document Task 8.4:** Implement reminder notifications before changes
  - **Document Task 8.5:** Update web UI for scheduling
  - Success criteria
  - Timeline estimate
- [ ] **Each Task Documentation Must Include:** Files to document, implementation steps to document, testing to document
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 8 section)
- [ ] **Acceptance Criteria:**
  - Phase 8 fully documented
  - Cron job architecture explained
  - Multiple scheduled changes per trail system supported

#### Task B5.6: Detail Phase 9 - Trail Care Reports System (DOCUMENTATION ONLY)
- [ ] **Action:** Write Phase 9 section in MVP_PROJECT_PLAN.md (NOT implement the tasks)
- [ ] **Required Documentation Content:**
  - Phase overview
  - **Document Task 9.1:** Create trail_care_reports DynamoDB table
  - **Document Task 9.2:** Create trail_care_report_comments DynamoDB table
  - **Document Task 9.3:** Create care_report_type_tags DynamoDB table
  - **Document Task 9.4:** Implement care report CRUD API endpoints
  - **Document Task 9.5:** Implement P1-P5 priority system
  - **Document Task 9.6:** Implement public/private visibility flag
  - **Document Task 9.7:** Implement type tag management (max 25 per org)
  - **Document Task 9.8:** Implement assignment workflow
  - **Document Task 9.9:** Implement comments and activity log
  - **Document Task 9.10:** Implement multiple photo upload (max 5)
  - **Document Task 9.11:** Implement status-based retention policy
  - **Document Task 9.12:** Implement offline report creation support (local queueing)
  - **Document Task 9.13:** Update web UI for care report management
  - Success criteria
  - Timeline estimate
- [ ] **Each Task Documentation Must Include:** Files to document, implementation steps to document, testing to document
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 9 section)
- [ ] **Acceptance Criteria:**
  - Phase 9 fully documented
  - Care report system comprehensively detailed
  - Offline support clearly explained
  - All 13 tasks detailed

#### Task B5.7: Detail Phase 10 - Notification System (DOCUMENTATION ONLY)
- [ ] **Action:** Write Phase 10 section in MVP_PROJECT_PLAN.md (NOT implement the tasks)
- [ ] **Required Documentation Content:**
  - Phase overview
  - **Document Task 10.1:** Implement email notifications via AWS SES
  - **Document Task 10.2:** Implement SMS notifications via AWS Pinpoint
  - **Document Task 10.3:** Implement push notifications via SNS→APNS for iPhone apps
  - **Document Task 10.4:** Implement subscription management (trail systems + organizations)
  - **Document Task 10.5:** Implement notification preferences (email, SMS, push)
  - **Document Task 10.6:** Create email templates for status changes
  - **Document Task 10.7:** Create SMS templates (160 char max)
  - **Document Task 10.8:** Update web UI for notification preferences
  - Success criteria (99% email delivery, <2 min latency)
  - Timeline estimate
- [ ] **Each Task Documentation Must Include:** Files to document, implementation steps to document, testing to document
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 10 section)
- [ ] **Acceptance Criteria:**
  - Phase 10 fully documented
  - All three notification channels detailed
  - Subscription model clearly explained

#### Task B5.8: Detail Phase 11 - Web Dashboards (DOCUMENTATION ONLY)
- [ ] **Action:** Write Phase 11 section in MVP_PROJECT_PLAN.md (NOT implement the tasks)
- [ ] **Required Documentation Content:**
  - Phase overview
  - **Document Task 11.1:** Create role-specific dashboard layouts (all 8 roles)
  - **Document Task 11.2:** Implement trail system CRUD UI for org-admin
  - **Document Task 11.3:** Implement care report management UI for trailsystem-crew
  - **Document Task 11.4:** Implement analytics dashboards
  - **Document Task 11.5:** Implement bulk operations UI
  - **Document Task 11.6:** Implement tag management UI
  - **Document Task 11.7:** Implement user management UI for org-admin
  - Success criteria
  - Timeline estimate
- [ ] **Each Task Documentation Must Include:** Files to document, implementation steps to document, testing to document
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 11 section)
- [ ] **Acceptance Criteria:**
  - Phase 11 fully documented
  - All 8 role dashboards detailed
  - UI components specified

#### Task B5.9: Detail Phase 12 - iPhone Apps (DOCUMENTATION ONLY)
- [ ] **Action:** Write Phase 12 section in MVP_PROJECT_PLAN.md (NOT implement the tasks)
- [ ] **Required Documentation Content:**
  - Phase overview
  - **Document Task 12.1:** Set up iOS development environment and repositories
  - **Document Task 12.2:** Implement User App - view trail systems
  - **Document Task 12.3:** Implement User App - submit trail care reports with camera
  - **Document Task 12.4:** Implement User App - view public care reports
  - **Document Task 12.5:** Implement User App - offline report creation with local queueing
  - **Document Task 12.6:** Implement User App - push notifications (APNS via SNS)
  - **Document Task 12.7:** Implement User App - offline status caching (7 days)
  - **Document Task 12.8:** Implement Admin App - trail system management
  - **Document Task 12.9:** Implement Admin App - full care report CRUD
  - **Document Task 12.10:** Implement Admin App - work logs (quick private report creation)
  - **Document Task 12.11:** Implement authentication (Cognito SDK with all three methods)
  - **Document Task 12.12:** Set up TestFlight distribution
  - **Document Task 12.13:** Implement deep linking for notifications
  - Success criteria (iOS 15+, TestFlight ready)
  - Timeline estimate
- [ ] **Each Task Documentation Must Include:** Files to document, implementation steps to document, testing to document
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 12 section)
- [ ] **Acceptance Criteria:**
  - Phase 12 fully documented
  - Both apps (User + Admin) detailed
  - Offline support clearly explained
  - All 13 tasks detailed

#### Task B5.10: Detail Phase 13 - Pilot Onboarding (DOCUMENTATION ONLY)
- [ ] **Action:** Write Phase 13 section in MVP_PROJECT_PLAN.md (NOT implement the tasks)
- [ ] **Required Documentation Content:**
  - Phase overview
  - **Document Task 13.1:** Create Hydrocut organization and 1 trail system (includes Glasgow and Synders areas)
  - **Document Task 13.2:** Create GORBA organization and 2 trail systems (Guelph Lake, Akell)
  - **Document Task 13.3:** Configure status types for each organization
  - **Document Task 13.4:** Invite and train key admins and trail crew
  - **Document Task 13.5:** Conduct live training sessions
  - **Document Task 13.6:** Provide white-glove onboarding support
  - **Document Task 13.7:** Set up TestFlight for pilot users
  - Success criteria (all 3 trail systems operational, admins trained)
  - Timeline estimate
- [ ] **Each Task Documentation Must Include:** Files to document, implementation steps to document, testing to document
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 13 section)
- [ ] **Acceptance Criteria:**
  - Phase 13 fully documented
  - All 4 pilot trail systems specified
  - White-glove onboarding process detailed

#### Task B5.11: Detail Phase 14 - Testing and Validation (DOCUMENTATION ONLY)
- [ ] **Action:** Write Phase 14 section in MVP_PROJECT_PLAN.md (NOT implement the tasks)
- [ ] **Required Documentation Content:**
  - Phase overview
  - **Document Task 14.1:** End-to-end testing (full user workflows)
  - **Document Task 14.2:** Security testing (penetration testing, vulnerability scanning)
  - **Document Task 14.3:** Performance testing (API response times, notification latency)
  - **Document Task 14.4:** Load testing (simulate 100+ users)
  - **Document Task 14.5:** User acceptance testing with pilot organizations
  - **Document Task 14.6:** Fix critical bugs and issues
  - Success criteria (99.9% uptime, <500ms API, 99% email delivery)
  - Timeline estimate
- [ ] **Each Task Documentation Must Include:** Files to document, implementation steps to document, testing to document
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Phase 14 section)
- [ ] **Acceptance Criteria:**
  - Phase 14 fully documented
  - All testing types detailed
  - Success metrics clearly stated

**Dependencies:** Phase B4 complete
**Complexity:** Extra Extra Large (XXL)
**Estimated Duration:** 8-12 hours to document all 11 phases fully

---

### Phase B6: Add Dependencies and Critical Path

**Objective:** Document dependencies between phases and identify critical path.

#### Task B6.1: Create Dependency Matrix
- [ ] **Action:** Document all dependencies between phases
- [ ] **Required Content:**
  - Phase 1 (Brand Messaging): No dependencies
  - Phase 2 (Security): No dependencies (can start immediately)
  - Phase 3 (Authentication): Depends on Phase 2 (Cognito configured)
  - Phase 4 (PII Protection): Depends on Phase 3 (users can login)
  - Phase 5 (Trail Systems): Depends on Phase 3 (authentication required)
  - Phase 6 (Tag-Based Status): Depends on Phase 5 (trail systems exist)
  - Phase 7 (Status Management): Depends on Phase 6 (tags exist)
  - Phase 8 (Scheduled Changes): Depends on Phase 7 (statuses exist)
  - Phase 9 (Care Reports): Depends on Phase 5 (trail systems exist)
  - Phase 10 (Notifications): Depends on Phase 7 (status changes to notify about)
  - Phase 11 (Web Dashboards): Depends on Phases 5-9 (all features to display)
  - Phase 12 (iPhone Apps): Depends on Phases 3-10 (all backend APIs ready)
  - Phase 13 (Pilot Onboarding): Depends on Phases 11-12 (web + mobile ready)
  - Phase 14 (Testing): Depends on Phase 13 (pilot setup complete)
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Dependencies section)
- [ ] **Acceptance Criteria:**
  - All dependencies documented
  - Dependency matrix clear and accurate

#### Task B6.2: Identify Critical Path
- [ ] **Action:** Identify critical path through 14 phases
- [ ] **Required Content:**
  - **Critical Path:** Phases 2 → 3 → 5 → 7 → 10 → 11 → 12 → 13 → 14
  - **Rationale:**
    - Security must be first (Phase 2)
    - Authentication required for all features (Phase 3)
    - Trail systems core data model (Phase 5)
    - Status management core feature (Phase 7)
    - Notifications core feature (Phase 10)
    - Web dashboards required for admins (Phase 11)
    - iPhone apps required for MVP (Phase 12)
    - Pilot onboarding required (Phase 13)
    - Testing final gate (Phase 14)
  - **Non-Critical Phases:**
    - Phase 1 (Brand Messaging): Can be done anytime
    - Phase 4 (PII Protection): Can be done in parallel with Phase 5
    - Phase 6 (Tag-Based Status): Can be done in parallel with Phase 7 development
    - Phase 8 (Scheduled Changes): Can be done in parallel with Phase 9
    - Phase 9 (Care Reports): Can be done in parallel with Phase 10 development
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Critical Path section)
- [ ] **Acceptance Criteria:**
  - Critical path identified
  - Parallelization opportunities documented
  - Total duration estimated

**Dependencies:** Phase B5 complete (all phases detailed)
**Complexity:** Medium (M)
**Estimated Duration:** 1-2 hours

---

### Phase B7: Add Timeline and Milestones

**Objective:** Create comprehensive timeline with milestones and deliverables.

#### Task B7.1: Calculate Total Timeline
- [ ] **Action:** Calculate total MVP implementation timeline
- [ ] **Required Content:**
  - **Phase 1:** 1-2 days
  - **Phase 2:** 5-7 days
  - **Phase 3:** 7-10 days
  - **Phase 4:** 3-5 days
  - **Phase 5:** 5-7 days
  - **Phase 6:** 3-5 days
  - **Phase 7:** 7-10 days
  - **Phase 8:** 3-5 days
  - **Phase 9:** 10-14 days
  - **Phase 10:** 5-7 days
  - **Phase 11:** 10-14 days
  - **Phase 12:** 14-21 days
  - **Phase 13:** 3-5 days
  - **Phase 14:** 7-10 days
  - **Total Sequential:** ~83-122 days (4-6 months)
  - **With Parallelization:** ~60-90 days (2-3 months)
  - **AI-Assisted Target:** ~45-75 days (1.5-2.5 months)
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Timeline section)
- [ ] **Acceptance Criteria:**
  - Total timeline calculated
  - Parallelization benefits quantified
  - AI-assisted target realistic

#### Task B7.2: Define Milestones
- [ ] **Action:** Define major milestones with dates
- [ ] **Required Content:**
  - **Milestone 1:** Security Hardened (End of Phase 2) - Week 1
  - **Milestone 2:** Authentication Complete (End of Phase 3) - Week 3
  - **Milestone 3:** Core Data Model Complete (End of Phase 5) - Week 5
  - **Milestone 4:** Status System Complete (End of Phase 7) - Week 8
  - **Milestone 5:** Trail Care Reports Complete (End of Phase 9) - Week 10
  - **Milestone 6:** Notifications Live (End of Phase 10) - Week 11
  - **Milestone 7:** Web Dashboards Complete (End of Phase 11) - Week 13
  - **Milestone 8:** iPhone Apps Beta (End of Phase 12) - Week 17
  - **Milestone 9:** Pilot Launch (End of Phase 13) - Week 18
  - **Milestone 10:** MVP Complete (End of Phase 14) - Week 20
  - **Target Launch:** Q2 2026 (April-June 2026)
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Milestones section)
- [ ] **Acceptance Criteria:**
  - All 10 milestones defined
  - Dates estimated
  - Q2 2026 launch feasible

#### Task B7.3: Create Gantt Chart or Timeline Visualization
- [ ] **Action:** Create visual timeline (optional, markdown table acceptable)
- [ ] **Required Content:**
  - Week-by-week breakdown
  - Phases shown in parallel where applicable
  - Milestones highlighted
  - Critical path emphasized
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Timeline visualization)
- [ ] **Acceptance Criteria:**
  - Timeline visualized (table or chart)
  - Parallel phases shown
  - Critical path clear

**Dependencies:** Phase B6 complete (dependencies and critical path identified)
**Complexity:** Medium (M)
**Estimated Duration:** 1-2 hours

---

### Phase B8: Add Success Criteria and Revision History

**Objective:** Define overall MVP success criteria and document creation history.

#### Task B8.1: Define Overall MVP Success Criteria
- [ ] **Action:** Document comprehensive success criteria for entire MVP
- [ ] **Required Content:**
  - **Functional Requirements:**
    - [ ] All 14 phases completed
    - [ ] All 8 user roles implemented
    - [ ] All 3 authentication methods working
    - [ ] Trail systems model implemented (NOT individual trails)
    - [ ] Trail Care Reports system fully functional
    - [ ] Tag-based status organization working
    - [ ] iPhone apps (User + Admin) in TestFlight
    - [ ] Web dashboards for all roles
    - [ ] Notification system (email, SMS, push) operational
    - [ ] Security hardening complete (all 7 gaps addressed)
    - [ ] PII protection complete (retention, export, deletion)
  - **Performance Requirements:**
    - [ ] 99.9% API uptime
    - [ ] <500ms API response time (p95)
    - [ ] <2 minutes notification latency
    - [ ] 99% email delivery rate
    - [ ] 95% push notification delivery rate
  - **Pilot Requirements:**
    - [ ] Hydrocut organization created (1 trail system with Glasgow and Synders areas)
    - [ ] GORBA organization created (Guelph Lake + Akell trail systems)
    - [ ] All 3 trail systems operational
    - [ ] Admins and crew trained
    - [ ] 70%+ of trail users subscribed within first month
    - [ ] 90%+ of status changes include photo and reason
  - **Quality Requirements:**
    - [ ] All critical bugs fixed
    - [ ] Security testing passed
    - [ ] Load testing passed (100+ concurrent users)
    - [ ] User acceptance testing passed
  - **Documentation Requirements:**
    - [ ] All documentation updated (PRODUCT_OVERVIEW, SYSTEM_ARCHITECTURE, SECURITY_REPORT)
    - [ ] User documentation created
    - [ ] Admin documentation created
    - [ ] API documentation created
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Success Criteria section)
- [ ] **Acceptance Criteria:**
  - All success criteria documented
  - Criteria measurable and verifiable
  - MVP definition clear

#### Task B8.2: Add Revision History
- [ ] **Action:** Create revision history section
- [ ] **Required Content:**
  - Version 1.0 | 2026-01-17 | Chief Development Manager + Claude Code | Initial MVP project plan created per CEO directive. All 14 phases fully detailed with tasks, dependencies, timelines, success criteria. Based on MVP_IMPLEMENTATION_PROMPT.md v1.13.
- [ ] **Files Affected:** `docs/MVP_PROJECT_PLAN.md` (Revision History section)
- [ ] **Acceptance Criteria:**
  - Revision history created
  - Initial entry documented

**Dependencies:** Phase B7 complete (timeline and milestones)
**Complexity:** Small (S)
**Estimated Duration:** 30 minutes

---

## Summary

**Total Tasks:** 85+ detailed tasks across 2 sections

**Section A Summary (Documentation Updates):**
- Phase A1: Backup 4 documentation files
- Phase A2: Update PRODUCT_OVERVIEW_FOR_CEO.md (7 tasks)
- Phase A3: Update SYSTEM_ARCHITECTURE.md (7 tasks)
- Phase A4: Update SECURITY_REPORT_FOR_CEO.md (5 tasks)
- Phase A5: Update MARKETING_PLAN.md (1 task)

**Section B Summary (MVP Project Plan Creation):**
- Phase B1: Create foundation (6 tasks)
- Phase B2: Detail Phase 1 - Brand Messaging (4 tasks)
- Phase B3: Detail Phase 2 - Security Hardening (10 tasks)
- Phase B4: Detail Phase 3 - Authentication (7 tasks)
- Phase B5: Detail Phases 4-14 (11 phase documentation tasks)
- Phase B6: Dependencies and critical path (2 tasks)
- Phase B7: Timeline and milestones (3 tasks)
- Phase B8: Success criteria and revision history (2 tasks)

**Critical Success Factors:**
- ALL 14 phases MUST be fully detailed in MVP_PROJECT_PLAN.md
- Every section in table of contents MUST have complete content
- No shortcuts, no placeholders, no "TBD" entries
- All tasks include: objective, files affected, implementation steps, testing, acceptance criteria
- Timeline estimates account for AI-assisted development (faster than traditional)
- Q2 2026 launch target must be achievable

**Estimated Total Duration to Complete TODO:**
- Documentation updates (Section A): 6-8 hours
- Project plan creation (Section B): 20-30 hours
- **Total: 26-38 hours of focused work**

---

## Section C: Backend MVP Feature Additions (post-docs-mvp-backend-features pass)

The tasks below were surfaced by the `topic/docs-mvp-backend-features` documentation pass (source: planning audit `i-just-discovered-you-golden-kite.md`). Each entry is an implementation task to be picked up after the docs land. Sub-sections group by feature.

### Phase 7.5: Condition Catalog (Org-Scoped Preset Library)

- [ ] Define `ConditionCatalogEntry` entity in `traillens_db` (`api-dynamo/src/packages/traillens_db/src/traillens_db/entities/condition_catalog.py`)
- [ ] Define `condition_catalog_repository` (org-scoped repository pattern, mirrors `condition_tag` and `type_tag` repos)
- [ ] Define `condition_catalog_service` (CRUD + apply-to-trail-system + save-from-condition orchestration)
- [ ] Add 7 new routes under tag `condition-catalog` to `api-dynamo/docs/openapi.json` and implement in `api-dynamo/src/lambdas/api_dynamo/src/api/routes/condition_catalog.py`:
  - [ ] `GET    /api/organizations/{org_id}/condition-catalog`
  - [ ] `GET    /api/organizations/{org_id}/condition-catalog/{catalog_id}`
  - [ ] `POST   /api/organizations/{org_id}/condition-catalog`
  - [ ] `PATCH  /api/organizations/{org_id}/condition-catalog/{catalog_id}`
  - [ ] `DELETE /api/organizations/{org_id}/condition-catalog/{catalog_id}`
  - [ ] `POST   /api/organizations/{org_id}/condition-catalog/upload-url`
  - [ ] `POST   /api/trail-systems/{trail_system_id}/condition/apply-catalog/{catalog_id}`
- [ ] Modify existing `PATCH /api/trail-systems/{trail_system_id}/condition` to accept optional `catalog_entry_id` and `save_to_catalog: bool` flags (TransactWrite path covers both)
- [ ] Add GSI1 catalog overload to DynamoDB single-table schema (`GSI1PK = ORG#{org_id}#CATALOG#ACTIVE`, `GSI1SK = USAGE#{usage_count_zero_padded}#CATALOG#{catalog_id}`)
- [ ] Add S3 key prefix `orgs/{org_id}/catalog/{catalog_id}.jpg` plus WebP variants to `photo_processor` Lambda (mirrors existing trail-photo flow)
- [ ] Add 7 access patterns AP-CC01–AP-CC07 to `api-dynamo/docs/ACCESS_PATTERNS.md` (Status: IMPLEMENTED ❌ initially)
- [ ] Integration tests for the apply-catalog TransactWrite (race-condition coverage on `usage_count` increments and concurrent apply)
- [ ] Integration tests for `save_to_catalog=true` flag on `PATCH /condition`
- [ ] Documentation propagation across REST client libs (jsrestapi + androidrestapi) and UI flow docs (already done in this docs pass — verify checked in)

### Tag Consolidation — Unified `Tag` Entity (plan `wse-did-alot-of-snuggly-volcano`)

This block supersedes the earlier "Tag-Cap Raise" task list. The cap raise is folded into the consolidation work since the unified service handles both flavors with type-keyed default caps and per-org `TagConfig` overrides.

- [ ] Define unified `TagEntity` and `TagType` enum in `api-dynamo/src/packages/traillens_db/src/traillens_db/entities/tag.py`; delete `condition_tag.py` + `type_tag.py`
- [ ] Implement single `TagRepository` in `api-dynamo/src/packages/traillens_db/src/traillens_db/repositories/tag.py` with type-keyed methods; delete `condition_tag.py` + `type_tag.py` repos
- [ ] Define `TagConfigEntity` in `entities/tag_config.py` (fields: `org_id`, `tag_type`, `max_count` (1–500), `created_at`, `updated_at`, `version`)
- [ ] Implement `TagConfigRepository` (PK=`ORG#{org_id}`, SK=`TAG_CONFIG#{tag_type}`)
- [ ] Rewrite `api/services/tags_service.py` — type-keyed methods that share the unified repository; introduce `_MAX_BY_TAG_TYPE: dict[TagType, int]` constants (defaults: CONDITION=20, CARE_REPORT_TYPE=25); read `TagConfig` (or default) on every create; reject with `409 TAG_CAP_EXCEEDED` if cap would breach
- [ ] **Net-new** cap enforcement on create — current `create_condition_tag` (line 87) and `create_care_report_type_tag` (line 225) **do not enforce caps today**; this is new work
- [ ] Split route module into two thin handlers + one config module: `routes/condition_tags.py`, `routes/care_report_tags.py`, `routes/tag_config.py`
- [ ] Rename URL `/api/organizations/{org_id}/tags/care-report-types` → `/api/organizations/{org_id}/care-report-tags` for symmetry with `/condition-tags`
- [ ] Add new routes `GET /api/organizations/{org_id}/tag-config` and `PUT /api/organizations/{org_id}/tag-config/{tag_type}` (org-admin for write, any org member for read)
- [ ] Implement cap-lowering safety rule: `PUT /tag-config/{tag_type}` rejects with `409 TAG_CAP_BELOW_CURRENT_USAGE` if new `max_count` is below current active tag count
- [ ] Implement org-bootstrap default-tag seeding: `Open`, `Closed`, `Caution` for CONDITION; `Maintenance`, `Hazard`, `Tree-down`, `Erosion`, `Litter`, `Signage`, `Bridge-repair` for CARE_REPORT_TYPE
- [ ] Add `description` to `Tag` schema as **required, may be empty string** (was absent on `ConditionTag`, optional/nullable on `TypeTag`); ensures identical schema across all `tag_type` values
- [ ] Server-side validation of `condition_tag_ids[]` (on `ConditionObservation`, `ConditionCatalogEntry`, `TrailSystem`) — every element must resolve to `Tag` with `tag_type=CONDITION`, same org, `is_active=true`; reject with `400 INVALID_TAG_REFERENCE` otherwise
- [ ] Server-side validation of `type_tag_id` (on `CareReport`) — when non-null, must resolve to `Tag` with `tag_type=CARE_REPORT_TYPE`, same org, `is_active=true`; reject with `400 INVALID_TAG_REFERENCE` otherwise
- [ ] Server-side denormalization on write: populate `condition_tag_names[]` from loaded `Tag.name` values in the same TransactWrite as the parent record
- [ ] Rewrite tag-related tests: cap enforcement (default and per-org override), optimistic locking, BOLA prevention, `TagConfig` upsert, cap-lowering safety rule, default-tag seeding
- [ ] Add 5 access patterns AP-TAG01–AP-TAG05 (List by org + type, List all by org, Create, Update, Soft-delete) and 2 access patterns AP-TC01–AP-TC02 (List configs, Upsert config) to `ACCESS_PATTERNS.md`
- [ ] Mark `AP-O04` and `AP-O05` as `**SUPERSEDED →** AP-TAG01 (parameterized by tag_type)`
- [ ] Update field-description prose in `dynamodb-spec.json`/`.md` and `DYNAMO_DATABASE_DESIGN.md` for `condition_tag_ids`, `condition_tag_names`, `type_tag_id` to point at the unified `Tag` entity

### Backup Password Authentication (Cognito SRP)

- [ ] Add `signInWithSrp(email, password)` method to `webui/packages/jsrestapi/src/auth/AuthManager.ts` (currently exposes 9 public methods, no SRP method)
- [ ] Document the existing `initiateAuth(authFlow="USER_SRP_AUTH")` pattern in `androidrestapi/lib/src/main/kotlin/com/traillenshq/api/auth/CognitoAuthApi.kt` README/docs (no new method — already reachable via the request `authFlow` parameter)
- [ ] Add debug-build-only password login screens to `androiduser` (gated by `BuildConfig.DEBUG`)
- [ ] Add debug-build-only password login screens to `androidadmin` (gated by `BuildConfig.DEBUG`)
- [ ] Cognito infra: upgrade `user_pool_tier` from `ESSENTIALS` to `PLUS` in `infra/pulumi/components/auth.py`
- [ ] Cognito infra: add `user_pool_add_ons=aws.cognito.UserPoolUserPoolAddOnsArgs(advanced_security_mode="AUDIT")`, then promote to `"ENFORCED"` after 2-week soak
- [ ] Configure adaptive-auth response policy (low → allow, medium → MFA, high → block)
- [ ] Add AWS WAF rules on the Cognito endpoint and on API Gateway for volumetric/brute-force protection (Threat Protection does NOT cover this)

### Background-Worker Lambdas

- [ ] Implement `scheduled_condition_processor` Lambda (Architecture A) in `api-dynamo/src/lambdas/scheduled_condition_processor/`
  - [ ] EventBridge rule `cron(0/15 * * * ? *)` (every 15 minutes)
  - [ ] Memory 256 MB, timeout 60s, ARM64
  - [ ] Handles fire-due-scheduled-conditions AND pre-fire reminder dispatch in the same handler
- [ ] Add GSI4 (`GSI4PK = SCHEDULED#{status}`, `GSI4SK = scheduled_at_iso8601`) to DynamoDB schema; on status flip the item is removed from `SCHEDULED#PENDING` partition
- [ ] Add 3 access patterns AP-SC04 (query due-now), AP-SC05 (query reminder-window), AP-SC06 (mark applied/cancelled) to `ACCESS_PATTERNS.md`
- [ ] CloudWatch alarms for scheduled-condition processor (recalibrated for 15-min interval): ≥1 failure in 30min; processed-items > 100/tick for 2 ticks; 0 invocations in 60min
- [ ] Implement `retention_cleanup_processor` Lambda (Architecture B) in `api-dynamo/src/lambdas/retention_cleanup_processor/`
  - [ ] EventBridge rule `cron(0 3 * * ? *)` (daily 03:00 UTC)
  - [ ] Memory 512 MB, timeout 900s (Lambda max), ARM64
  - [ ] Closed care reports >90d → batch-delete + audit
  - [ ] Deleted-account PII scrub >30d → hard-delete + audit
  - [ ] S3 photo orphan sweep (paginated S3 list + parent-existence DynamoDB check)
  - [ ] Magic-link belt-and-suspenders cleanup (`PK begins_with MLT#` AND `ttl < now-300s`)
- [ ] Add `CareReportDeletionAudit` and `PIIDeletionAudit` entity types to `traillens_db`
- [ ] Add 3 access patterns AP-RC01 (closed-care-report cleanup), AP-RC02 (deleted-user PII scrub), AP-RC03 (photo orphan parent-existence check) to `ACCESS_PATTERNS.md`
- [ ] CloudWatch alarms for retention cleanup: Lambda failure → page; processed-count = 0 for 7 consecutive days → likely silent broken state
- [ ] Implement Pulumi `EventBridgeScheduledLambda` ComponentResource in `infra/` (EventBridge Rule + Target + Lambda IAM role + CloudWatch log group with 30-day retention) — used by both new Lambdas

### TrailPulse (Full Backend per Section 10)

- [ ] Implement 9 entity types in `traillens_db` (NOT 10 — `TrailConditions` and `RideEvents` dropped per privacy-first redesign): `AdditionalQuestions`, `TrailSystemRideCount`, `RideCompletion`, `FeedbackResponses`, `UserPreferences`, `QuestionResponseTracker`, `TrailSystemGeofences`, `CrewMembers`, `FeedbackDeletionAudit`
- [ ] Implement 25 endpoints (5 mobile + 2 web + 8 admin-config + 10 admin-feedback) under sub-tags `trailpulse-mobile`, `trailpulse-web`, `trailpulse-admin-config`, `trailpulse-admin-feedback`
- [ ] Implement `PUT /api/trailpulse/trail-systems/{ts_id}/ride-completion` with idempotency via client-uuid `ride_id` (single-partition TransactWrite: `Put RIDECOMPLETION#{ride_id}` with `attribute_not_exists` + `Update RIDECOUNT#{today}` with `ADD total_rides :one`)
- [ ] Implement mobile-local post-ride feedback notification (Android `NotificationCompat` + `NotificationManagerCompat`) — NOT a server-side push. Channel `trailpulse_post_ride`; deeplink `traillens://feedback/{ride_id}`; `POST_NOTIFICATIONS` runtime permission on Android 13+
- [ ] Add 27 access patterns AP-TP01–AP-TP27 to `ACCESS_PATTERNS.md` (one per query type for each of the 9 entity types) — Status: IMPLEMENTED ❌ initially
- [ ] Document the two design-overlap decisions: (a) feedback config references `catalog_id`s (no standalone `TrailConditions` entity); (b) `/feedback` and `/observations` both kept (UNION on read for admin dashboards)

### Other openapi.json Changes (Categories 1–4)

- [ ] Add `GET /api/users/me` to openapi.json (currently missing — sync gap; route exists in `routes/users.py:90`)
- [ ] Add `PUT /api/users/me` to openapi.json (currently missing — sync gap; route exists in `routes/users.py:113`)
- [ ] Add `POST /api/users/me/export-data` route (Phase 4.2) + access pattern AP-U15
- [ ] Add `POST /api/users/me/delete-account` route (Phase 4.3) + access pattern AP-U16
- [ ] Add `GET /api/care-reports/{id}/activity` aggregate-on-read endpoint + access pattern AP-CR14
- [ ] Add 3 subscriptions routes under existing `users` tag: `POST /api/users/me/subscriptions`, `GET /api/users/me/subscriptions`, `DELETE /api/users/me/subscriptions/{trailsystem_id}`
- [ ] Add `is_public: bool` (default `false`) to care-report request and response schemas in openapi.json
- [ ] Add `is_public: bool` to `CareReportEntity` Pydantic model in `routes/care_reports.py`
- [ ] Add `is_public: bool` to `CareReportEntity` in `traillens_db`
- [ ] Implement visibility-gating semantics in `care_reports_service.py`: `is_public=true` visible to any authenticated user; `is_public=false` only to org members
- [ ] Add `maxItems: 5` to care-report photo upload request schema in openapi.json
- [ ] Add `maxItems: 5` to care-report response `photos` array in openapi.json
- [ ] Add server-side photo-cap enforcement in `care_reports_service.py` (HTTP 400 if request would exceed 5)
- [ ] Rewrite notification preferences as 2-axis matrix `{ channels, events: { event_type: { email, sms, push } } }` in openapi.json `NotificationPreferences` schema
- [ ] Itemise the 6 event types in planning Task 10.5 (`condition_change`, `care_report_created`, `care_report_assigned`, `care_report_comment`, `scheduled_condition_reminder`, `observation_received`)
- [ ] Rewrite `notifications_service.py` to evaluate the per-event-type per-channel matrix at dispatch time
- [ ] Add 8 analytics routes under new tag `analytics` (overview, trail-systems, care-reports, users, activity-feed, export, condition-history per ts, views per ts) + AP-AN01–AP-AN08 access patterns
- [ ] Bump `info.version` in openapi.json from `1.1.3` to `2.0.0` (MAJOR — breaking URL renames)
- [ ] Rename `/api/devices` → `/api/users/me/devices` (and `/{device_id}` variant) in openapi.json + `routes/devices.py`
- [ ] Rename `/api/users/phone/verify`, `/api/users/phone/confirm` → `/api/users/me/phone/verify`, `/api/users/me/phone/confirm` in openapi.json + `routes/users.py:258, 318`
- [ ] Rename `/api/organizations/{org_id}/tags/condition` (+`/{tag_id}`) → `/api/organizations/{org_id}/condition-tags` (+`/{tag_id}`) in openapi.json + `routes/tags.py` + `traillens_db.repositories.condition_tag` URL constants

### Embedded openapi.json Sync (Both REST Client Libs)

- [ ] Replace `webui/packages/jsrestapi/docs/openapi.json` with the updated `api-dynamo/docs/openapi.json`
- [ ] Regenerate TypeScript types via `@hey-api/openapi-ts` in `webui/packages/jsrestapi`
- [ ] Add new service facades to `webui/packages/jsrestapi`: `ConditionCatalogService`, `AnalyticsService`, `TrailPulseMobileService`, `TrailPulseWebService`, `TrailPulseAdminConfigService`, `TrailPulseAdminFeedbackService`
- [ ] Replace `androidrestapi/docs/openapi.json` with the updated `api-dynamo/docs/openapi.json`
- [ ] Regenerate Kotlin services in `androidrestapi/lib`
- [ ] Add the same 6 new service facades (Kotlin equivalents) to `androidrestapi`
- [ ] Add CI step in `androidrestapi/CI_INTEGRATION.md` to validate `androidrestapi/docs/openapi.json` matches `api-dynamo/docs/openapi.json` (file equality check) before running codegen — prevents future drift

---

**Prepared by:** AI Assistant per CEO Directive
**Last Updated:** 2026-01-17
**Status:** Ready for execution (no shortcuts, work 24/7 until complete)
