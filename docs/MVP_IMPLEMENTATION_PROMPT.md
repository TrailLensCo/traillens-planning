# TrailLensHQ MVP Implementation Prompt

<!--
=========================================================================================
PROMPT HISTORY - All CTO Prompts in Chronological Order
=========================================================================================

PROMPT 1 - ORIGINAL MVP DEFINITION (January 15, 2026):

"Create a prompt file in the docs directory using the .github/prompts/prompt_template.md that describes the MVP using the documentation in the docs directory.

As the CTO, I am not satisfied with the reports. They miss the mark for MVP. The current codebase does not represent the MVP, but some ideas tossed together to see if this project was possible.

The mvp includes:
- status update changing
- status type update
 - status type groups (open, close, etc)
 - individual status tied to a group
  - each status can have a photo
   - each status can have a season (fall, winter, etc)
- the above is per trail org
- we will target the Hydrocut and GORBA to start
- status updates can be sent to users who have subscribed to the trail org
- users, trail admin, etc have to be able to login to their dashboard
- users have to update their own data and methods of contact
- initially, status can be via email and SMS
- next, phone apps will allow people to login and see status and get update notifications
- an additional phone app will allow trail org admins to set the status
- the admin app will allow traillens status to change anything when logged in

Make suggestion along those lines as for things related to above based on the reports in the docs directory to include. For example, we want to tackle security risks for PII data now while we can at the start.

Additionally items we want to include are passkey logins and logins via a link (fill in email and we sent you a link to click on) to eliminate.

Organize my thoughts into a prompt I can edit. Make reference to any reports you use. Eventually, we will be updating all reports with this new information."

---

PROMPT 2 - CLARIFICATIONS AND CORRECTIONS (January 15, 2026):

"Update the prompt with the original prompt that created it. Place that at the top of the file.

A few things from the summary above:
- we are not signing a DPA at this point
- the user types/groups in the code are fine and we will not be changing or reducing them
- auth requirements are required for MVP
- suggested items (5) are required for MVP
- admin/traillens super admin apps are the same thing - one app for both
- iphone app for users and for admins (so status can be set) are required for MVP. Android to follow later

Update the question section with any ambiguities.

Modify the MVP implementation prompt only and reference the prompt_template.md if required."

---

PROMPT 3 - QUESTIONS AND DECISIONS (January 15, 2026):

"Use the AskUserQuestion tool to ask the questions in the attached prompt, and update the prompt file accordingly. Keep the questions section and mark my decisions. Make recommended answers for each question."

[36 questions answered via AskUserQuestion tool - see "MVP Implementation Decisions" section below]

---

PROMPT 4 - TRAIL SYSTEMS CLARIFICATION (January 15, 2026):

"The documentation and the prompt seem to the notion we are working with Trails. We are working with trail systems. One trail system has many trails. For MVP, we will only be concerned with trail systems. That said, each trail organization can have multiple trail systems. The Hydrocut has Glasgow and Synders. GORBA has Guelph Lake and Akell. Each trail system can have a status. So, the product and interface must support many trail systems per trail org which each trail system having a status as already defined.

Update the prompt with all current typed in prompts thus far at the top of the file.

Review the prompt and my current request and ask any questions about ambiguity using the AskUserQuestion too."

---

PROMPT 5 - TAG-BASED STATUS ORGANIZATION (January 16, 2026):

"Items 1.2 and 1.3 talk about trail status organizaton. As the CTO, I think this is tool cumbsome. Replace this notion with the concept of tags. Tags can be created/updated/delete with anyone access to status, and assigned to a status. It will be a way of sorting the status in the interface and allow uses to decide how they are sorted. Therefore, along with being able to do CRUD on statuses, we need code to do CRUD on status tags. Then, the interface to create statuses can be used to assign tags, and the view status page can allow tags to be assigned to status. The change status page should alllow tags to be sticky such that a set of tags can be applied to the change status so, for example, a winter statuses would appear when selected allowing the user to view those only when changing the status. The tag set should be updatable.

Use the AskUserQuestion tool to ask questions about abiguity about this change, then update the MVP document with the new feeature. Also, add this prompt to the comments to the top of the document."

CTO DECISIONS (via AskUserQuestion):
- Tag scope: Per-organization (each organization manages their own tag set)
- Multiple tags: Yes, statuses can have multiple tags simultaneously
- Tag limit: 10 tags maximum per organization
- Tag permissions: Anyone with status access can create/update/delete tags

---

PROMPT 6 - WORK LOGS AND TRAIL CARE REPORTS (January 16, 2026):

"We have the concept of work logs in the system, but really this nothing more the trail care reports with view of who can see it. Care reports would be viewable by anyone including regular users and generally submited by users. Work logs are care reports that are submitted by trail crew and only viewable by trail crew or better users. We need to combine the system with some kind of tagging system limit who views what, as well as, tags for what kind of work it has.

Add this prompt to the top of the MVP doc, but explore the idea here. Do not adjust anything. Just save the prompt."

---

PROMPT 7 - TRAIL CARE REPORT ATTRIBUTES (January 16, 2026):

"Lets review the full attributes of the trail care report system from the above, and add photos, priority (P1-P5) (only trail crew and above can set priority - regular users get it set to P3 by default), user submitted, currently assigned to (which needs a assigned to trail crew item to suggest anyone on the crew can take the ticket), time/date submitted, status (open, deferred, in-progress, cancelled, closed - suggest others), days open (not canceled or closed), title, description - suggest other attributes to a normal ticket system.

Add this prompt to the MVP file, and add our trail care system to the document.

Use AskUserQuestion tool to ask me about any ambiguities about the system."

CTO DECISIONS (via AskUserQuestion):
- Photo limit: Multiple photos (up to 5 photos per report)
- Assignment system: Flexible assignment (unassigned pool + specific assignment + self-assignment)
- Submitter notifications: Optional per submitter (user can opt-in to notifications)
- Comments: Support comments system for crew updates

---

PROMPT 8 - TRAIL CARE REPORT RETENTION AND IPHONE APP FEATURES (January 16, 2026):

"We didn't talk about trail report retention or trail report photo retention. Check the other items in the MVP file and the security report, and use the AskUserQuestion tool to ask any questions about ambiguities about retention (help me define it), and update the MVP doc.

Also, we didn't touch on how the iphone apps would change. Ask me quesitons about that."

CTO DECISIONS (via AskUserQuestion):
- Report data retention: 2 years after closed/cancelled (open reports kept indefinitely)
- Report photo retention: 180 days after report closed/cancelled (active report photos kept indefinitely)
- Status-based retention: Yes, open/in-progress/deferred/resolved reports kept indefinitely, closed/cancelled deleted after 2 years
- iPhone app features: All four options selected:
  - User app: View public reports
  - User app: Submit new reports with camera integration
  - Admin app: Full report management (CRUD, comments, priority, assignment)
  - Admin app: Quick work log creation from field

---

PROMPT 9 - OFFLINE TRAIL CARE REPORT CREATION (January 17, 2026):

"The doc says:

5. **Offline capability:** ✅ **DECISION: Cache last-known trail system status only** (show stale data when offline with warning banner, helps in low-signal areas)

That said, I think users must be able to create a trail care report offline, and have it upload when signal is available.

Add this prompt to the top of the file, and use the AskUserQuestion tool to answer any ambiguities about the new feature."

CTO DECISIONS (via AskUserQuestion):
- Offline photos: Yes, store photos locally and upload when online (up to 5 photos per report)
- Queue duration: 7 days with warnings (warning after 48 hours offline, offer retry/delete after 7 days)
- UI indicators: All selected:
  - Show pending badge/icon on report list
  - Separate "Pending Sync" section in app
  - Allow users to edit pending reports before sync
  - Allow users to delete pending reports before sync
- Retry behavior: Auto-retry with exponential backoff (3 attempts: 30s, 2min, 10min), then manual retry with error details

---

PROMPT 10 - BRAND MESSAGING UPDATE IN MVP (January 17, 2026):

"From the marketing plan:

**Update brand messaging** - Use "Building communities, one trail at a time" byline (marketing, not technical)

This update is in MVP. It is low hanging fruit to be able to change the website for this byline and other data.

Add this prompt to the document, and update the MVP doc to include the marketing update in MVP."

---

PROMPT 11 - PHASE LIST REVIEW AND UPDATE (January 17, 2026):

"This section seems to spell out how to create the todo. But, the phases may not represent the current MVP changes. Review the MVP doc, and update the phase list. Additionally, it should be mentioned this is only a recommendation, and the exact phases will require review of the referenced documentation.

Add this prompt to the top of the doc, and conduct your review."

---

PROMPT 12 - MOVE BRAND MESSAGING TO PHASE 1 (January 17, 2026):

"Update the MVP prompt to move Phase 12 - brand messaging to phase 1.

Add this prompt to the top comment."

=========================================================================================
END PROMPT HISTORY
=========================================================================================
-->

<!--
IMPORTANT: This prompt defines the TRUE MVP for TrailLensHQ.
The current codebase represents exploratory work to validate feasibility.
This document defines what we will actually build and ship as MVP.

Based on:
- CTO Vision (January 2026)
- docs/PRODUCT_OVERVIEW_FOR_CEO.md
- docs/SYSTEM_ARCHITECTURE.md
- docs/SECURITY_REPORT_FOR_CEO.md
- docs/MARKETING_PLAN.md
-->

## Task Overview

**Build the TrailLensHQ Minimum Viable Product (MVP)** - a focused **trail system** status management platform targeting two pilot organizations (Hydrocut and GORBA) with emphasis on security, user management, and real-time status notifications.

**CRITICAL CONTEXT:** The current codebase is exploratory prototype code to validate technical feasibility. It does NOT represent the MVP. This prompt defines what we will actually build and ship.

**IMPORTANT DATA MODEL CLARIFICATION:**

- We manage **trail systems**, NOT individual trails
- A **trail system** contains many individual trails (e.g., Hydrocut trail system includes Glasgow and Synders areas)
- Individual trails in a trail system are OUT OF SCOPE - we only manage trail systems
- Each **trail organization** has one or more **trail systems**:
  - **Hydrocut** → Hydrocut trail system (includes Glasgow and Synders areas)
  - **GORBA** → Guelph Lake trail system, Akell trail system
- Each **trail system** has a status (not individual trails within the system)

---

## Context

### Current State

- **Exploratory codebase exists** - Various ideas tested to prove viability
- **Infrastructure operational** - AWS dev environment (`dev.traillenshq.com`) fully deployed
- **No production-ready MVP** - Current code needs focused rebuild for MVP
- **Target launch** - Q1 2026 with two pilot organizations (Hydrocut, GORBA)
- **Pilot trail systems** - 3 total trail systems (Hydrocut: 1 trail system with Glasgow and Synders areas, GORBA: Guelph Lake + Akell)

### MVP Philosophy

**"Do one thing exceptionally well"** - **Trail system** status management with bulletproof security and delightful UX for trail organizations and their communities.

### Related Documentation

- **Product Vision:** [docs/PRODUCT_OVERVIEW_FOR_CEO.md](PRODUCT_OVERVIEW_FOR_CEO.md)
  - Full platform vision (many features beyond MVP scope)
  - Market positioning and competitive analysis
  - Long-term roadmap (NOT for MVP)

- **Infrastructure:** [docs/SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md)
  - AWS serverless architecture (Lambda, DynamoDB, Cognito, S3)
  - Multi-tenant design patterns
  - Cost projections ($75-150/month dev, $200-400/month production)

- **Security Requirements:** [docs/SECURITY_REPORT_FOR_CEO.md](SECURITY_REPORT_FOR_CEO.md)
  - PII data inventory (16 DynamoDB tables with sensitive user data)
  - Access controls and encryption requirements
  - **CRITICAL GAPS identified:** CloudTrail, DPAs, incident response plan
  - Compliance requirements (GDPR, CCPA, PIPEDA)

- **Marketing & Positioning:** [docs/MARKETING_PLAN.md](MARKETING_PLAN.md)
  - Brand messaging: "Building communities, one trail at a time"
  - Target audience personas
  - Go-to-market strategy

### Constraints

- **Timeline:** Q2 2026 launch
- **Pilot Organizations:** Hydrocut and GORBA only
- **Team:** 1-2 developers with Claude Code assistance
- **Budget:** $75-150/month infrastructure during MVP development
- **Security:** Must address PII protection from day one (non-negotiable)

---

## Requirements

### 1. Core Trail System Status Management

**Entity: Trail System**

- A trail system is a named collection of individual trails managed as a single unit
- Examples: Hydrocut trail system (includes Glasgow and Synders areas), Guelph Lake trail system (GORBA), Akell trail system (GORBA)
- Each trail system belongs to exactly one trail organization
- Each trail system has ONE status at any given time (applies to the entire system)
- Individual trails within a system are NOT managed.

#### 1.1 Trail System Attributes

**Core Attributes (Required):**

- **Name** - Trail system name (e.g., "Hydrocut Trail System", "Guelph Lake Trail System")
- **Status** - Current status of the trail system (see Status Type System below)
- **Organization ID** - Which trail organization owns this trail system

**Standard Attributes:**

- **Description** - Text description of the trail system
- **Location** - GPS coordinates or physical address of trail system
- **Cover Photo** - Representative image of the trail system (not status photo)

**Metadata:**

- **Created by** - User who created the trail system
- **Last modified by** - User who last updated the trail system
- **Created at** - Timestamp
- **Updated at** - Timestamp

#### 1.2 Tag-Based Status Organization

**Status Tags** provide flexible categorization and organization of trail system statuses.

- **Tag Scope:** Per trail organization
  - Each organization manages their own set of tags
  - Hydrocut tags are separate from GORBA tags
  - All trail systems within an organization share the same tag pool

- **Tag Limit:** Maximum 10 tags per organization
  - Prevents UI clutter and encourages focused categorization
  - Organizations must be thoughtful about tag creation

- **Multiple Tags per Status:** Statuses can have multiple tags assigned
  - Examples:
    - Status "Icy Conditions" could be tagged: ["Winter", "Weather-Related", "Caution"]
    - Status "Closed - Snow Removal" could be tagged: ["Winter", "Maintenance", "Temporary"]
  - Enables rich, flexible categorization schemes
  - Supports complex filtering and sorting in interfaces

- **Tag Management (CRUD Operations):**
  - **Create:** Anyone with status access can create new tags
  - **Read:** All users can view tags assigned to statuses
  - **Update:** Anyone with status access can rename tags
  - **Delete:** Anyone with status access can delete tags
    - Deleting a tag removes it from all statuses
    - Requires confirmation (destructive operation)

- **Tag Assignment:**
  - **During Status Creation:** Interface allows assigning tags when creating a new status type
  - **View Status Page:** Tags can be added/removed from existing statuses
  - **Bulk Operations:** Multiple statuses can be tagged simultaneously

- **Sticky Tag Filtering (Change Status Interface):**
  - Tag filters persist across status changes within a session
  - Example use case:
    - Trail crew selects "Winter" tag filter
    - Only statuses tagged with "Winter" appear in status dropdown
    - Filter remains active until manually cleared or session ends
  - Enables focused status management (e.g., viewing only winter-related statuses when changing status in winter months)

- **Tag Use Cases:**
  - **Seasonal organization:** "Winter", "Spring", "Summer", "Fall"
  - **Severity categorization:** "Open", "Caution", "Closed"
  - **Cause classification:** "Weather", "Maintenance", "Wildlife", "Events"
  - **Temporal markers:** "Temporary", "Permanent", "Scheduled"
  - **Custom organizational schemes:** Organizations define tags that match their workflow

#### 1.3 Status Attributes

- **Tags** (optional, multiple allowed)
  - Assigned from organization's tag pool (max 20 tags per organization)
  - Multiple tags can be applied to a single status
  - Used for filtering, sorting, and organizing statuses in interfaces
  - Examples: ["Winter", "Weather-Related"], ["Maintenance", "Temporary"]

- **Photo attachment** (optional)
  - Each status update can include one photo
  - Stored in S3, optimized for web/mobile display
  - Max 5MB file size

- ~~**Season assignment** (optional)~~ — **REMOVED per docs-mvp-backend-features pass.** Season state is communicated via org-defined `condition_tags` (e.g. `Winter Closure`, `Spring Mud Season`). No dedicated season entity, no season attribute on the status record. The catalog (Phase 7.5) can include season-themed entries that admins apply when seasons change.

- **Status metadata**
  - Timestamp (when status was set)
  - Set by (which user/admin made the change)
  - Reason/notes (free text explanation)
  - Duration (estimated time in this status, if known)

#### 1.4 Trail System Status Updates

- **Quick status change** - Trail admins can change trail system status in <30 seconds
- **Status history** - Complete audit trail of all status changes (visible to users and admins)
  - Who made the change
  - When the change occurred
  - Previous status → New status
  - Reason/notes provided
  - Photo attached (if any)
  - 2-year retention (matches user data retention policy)
- **Bulk updates** - Update multiple trail systems to same status simultaneously (e.g., "Close all Hydrocut trail systems due to storm")
- **Scheduled status changes** - Pre-schedule multiple future status changes per trail system
  - Example: Hydrocut trail system scheduled to "Close Nov 1", "Reopen Apr 1", "Close for maintenance Feb 15"
  - Stored in separate `scheduled_status_changes` table
  - Users receive reminder notifications before scheduled changes
  - Automated cron job applies scheduled changes at specified time

---

### 2. Trail Care Reports (Issue Tracking System)

**Trail Care Reports** unify work logs and user-submitted issue reports into a single flexible ticketing system for tracking trail system maintenance, hazards, and observations.

#### 2.1 Core Concept

- **Single unified system** replacing separate "work logs" and "problem reports"
- **Visibility control** via `is_public` boolean flag (not tags)
  - `is_public = true`: Viewable by all users including regular users (community reports)
  - `is_public = false`: Viewable only by trailsystem-crew and above (internal work logs)
- **Flexible categorization** via type tags
- **Assignment and workflow** for crew task management

#### 2.2 Report Attributes

**Core Fields (Required):**

- **Title** - Short summary of the issue/report (max 100 chars)
- **Description** - Detailed explanation of the issue, work performed, or observation
- **Trail System** - Which trail system this report relates to (required association)
- **Submitted by** - User who created the report
- **Submitted at** - Timestamp of report creation
- **Status** - Current state of the report (see workflow below)
- **is_public** - Boolean flag controlling visibility

**Priority (Required, Restricted Editing):**

- **P1 (Critical)** - Immediate safety hazard, trail closure required
- **P2 (High)** - Significant issue, should be addressed within days
- **P3 (Normal)** - Standard maintenance or minor issue (DEFAULT)
- **P4 (Low)** - Nice-to-have improvements
- **P5 (Deferred)** - Long-term wishlist items
- **Permission model:**
  - Regular users: Reports auto-set to P3, cannot change priority
  - Trail-crew and above: Can set/change priority to any level
  - Priority affects sorting in crew dashboards (P1 at top)

**Photos (Optional, Multiple Allowed):**

- Up to 5 photos per report
- Stored in S3, optimized for web/mobile display
- Max 5MB per photo
- Useful for showing multiple angles of issues (tree damage, erosion, etc.)
- Each photo can have optional caption

**Type Tags (Optional, Multiple Allowed):**

- Assigned from organization's **care report type tag pool** (separate from status tags)
- Multiple type tags can be applied to categorize the report
- Examples: "maintenance", "hazard", "tree-down", "erosion", "observation", "winter", "urgent", "signage"
- Maximum 15 type tags per organization
- Created/managed by trailsystem-crew and above
- Used for filtering and sorting reports in interfaces

**Assignment (Optional):**

- **Unassigned** - Default state, any crew member can self-assign
- **Assigned to specific crew member** - Org-admin or trailsystem-owner can assign to individual
- **Crew member self-assignment** - Any crew member can claim an unassigned report
- **Reassignment** - Org-admin, trailsystem-owner, or current assignee can reassign

**Calculated Fields:**

- **Days open** - Days since submission, excluding cancelled/closed reports
- **Last updated** - Timestamp of most recent change (status, comment, assignment)
- **Last updated by** - User who made the most recent change

**Optional Fields:**

- **Location** - GPS coordinates (auto-captured from mobile app or manually entered)
- **Estimated resolution time** - How long crew thinks this will take (trailsystem-crew+ only)

#### 2.3 Report Status Workflow

**Status Options:**

- **Open** - New report, not yet triaged or assigned
- **In Progress** - Crew member actively working on the issue
- **Deferred** - Issue acknowledged but postponed (low priority or seasonal)
- **Resolved** - Work completed, awaiting verification
- **Closed** - Report fully resolved and closed
- **Cancelled** - Report duplicate, invalid, or no action needed

**Status Workflow Rules:**

- Any status can transition to any other status (flexible workflow)
- Closing a report requires **resolution notes** (required field, trailsystem-crew+ only)
- Cancelled reports require **cancellation reason** (required field)
- Days open counter shows that day the report is any report is anything other than closed or cancelled. Once closed or cancelled, the count stops.

**Resolution Notes (Required when closing/cancelling):**

- Free text field explaining how the issue was resolved or why it was cancelled
- Visible to all users who can view the report
- Examples: "Tree removed, trail cleared", "Duplicate of report #123", "Not a real issue"

#### 2.4 Comments and Updates

**Comment System:**

- Trail-crew and above can add text comments to reports
- Comments create audit trail of progress
- Each comment includes:
  - Comment text
  - Author (crew member name)
  - Timestamp
  - Optional photo attachment
- Examples: "Inspected today, will fix next week", "Ordered new signage", "Waiting for weather to improve"
- Comments visible to anyone who can view the report (respects is_public flag)

**Activity Log:**

- Automatic audit trail of all changes:
  - Status changes
  - Priority changes
  - Assignment changes
  - Tag additions/removals
  - Resolution notes
- Each log entry includes: what changed, who made the change, timestamp
- Full history visible to trailsystem-crew and above

#### 2.5 Submission and Permissions

**Who Can Submit:**

- **Regular users** - Can submit reports, automatically set to `is_public = true`, priority P3
- **Trail-crew and above** - Can submit reports, can choose public or private, can set priority

**Who Can View:**

- **Public reports** (`is_public = true`) - Visible to all users
- **Private reports** (`is_public = false`) - Visible only to trailsystem-crew and above for that organization

**Who Can Edit:**

- **Submitter** - Can edit title, description, and photos within 24 hours of submission
- **Trail-crew and above** - Can edit all fields, change status, add comments, assign
- **Org-admin** - Full control over all reports in their organization

**Who Can Close:**

- **Trail-crew and above** - Can mark reports as resolved, closed, or cancelled with resolution notes

#### 2.6 Notifications (Optional per Submitter)

**Submitter Notification Preferences:**

- Users can opt-in to receive notifications about their submitted reports
- Preference set in user profile: "Notify me about my care report updates"
- Default: Enabled for all users

**Notification Triggers (if opted-in):**

- Report status changed (e.g., open → in-progress)
- Report priority changed by crew
- Crew member adds comment to report
- Report assigned to crew member
- Report resolved or closed

**Notification Channels:**

- Email (always)
- Push notification (if mobile app installed)
- SMS (if high-priority report P1/P2 and user has SMS enabled)

**Crew Notifications:**

- Trail-crew members notified of new reports in their organization
- Assignee notified when report is assigned to them
- Org-admin notified of high-priority (P1/P2) reports

#### 2.7 Care Report Type Tags

**Separate Tag Pool:**

- Care report type tags are **separate** from report status (P1-P5)
- Each organization manages their own care report type tag pool
- Maximum 25 type tags per organization

**Tag Management:**

- **Create** - Org-admin can create new type tags
- **Update** - Org-admin can rename type tags
- **Delete** - Org-admin can delete type tags (removes tag from all reports)
- **Assignment** - Anyone submitting a report can assign existing type tags

**Common Type Tag Examples:**

- Work type: "maintenance", "repair", "inspection", "cleanup"
- Issue type: "hazard", "tree-down", "erosion", "flooding", "signage", "bridge"
- Season: "winter", "spring", "summer", "fall"
- Urgency: "urgent", "routine"
- Location: "trailhead", "bridge", "parking", "signage"

**Tag Use in Interface:**

- Filter reports by type tags
- Sort reports by tag combinations
- Sticky filtering (like status tags - persist across sessions)

#### 2.8 Dashboard Views

**User Dashboard (Regular Users):**

- **My Reports** - List of reports submitted by user
- **Community Reports** - All public reports for subscribed trail systems
- **Submit New Report** - Button to create new report (auto-set to public, P3)

**Trail Crew Dashboard:**

- **Assigned to Me** - Reports assigned to logged-in crew member
- **Unassigned** - Reports available for self-assignment
- **All Open Reports** - All open/in-progress reports for their organization
- **Filter by:**
  - Priority (P1-P5)
  - Status (open, in-progress, deferred, etc.)
  - Type tags
  - Trail system
  - Days open
- **Bulk actions:**
  - Assign multiple reports to crew member
  - Apply type tags to multiple reports
  - Change priority on multiple reports

**Org-Admin Dashboard:**

- All trail crew features PLUS:
- **All Reports** - View all reports (public and private) for organization
- **Analytics:**
  - Reports by status
  - Average resolution time
  - Reports by trail system
  - Reports by type tag
  - Top submitters

#### 2.9 Integration with Trail System Status

**Optional Link:**

- Care reports can optionally trigger status changes
- Example: P1 hazard report → crew can immediately change trail system status to "Closed - Hazard"
- Link in report UI: "Change trail system status based on this report"
- Creates association between report and status change in audit log

**Report Categories That May Affect Status:**

- Hazard reports (P1/P2) → May require trail closure
- Maintenance reports → May trigger "Maintenance" status
- Condition reports → May trigger "Caution" status
- Resolution reports → May trigger status back to "Open"

#### 2.10 Trail Care Report Retention Policy

**Data Retention Strategy:**

Trail care reports follow a status-based retention policy that balances historical value with storage costs:

**Active Reports (No Auto-Deletion):**

- **Open** - Kept indefinitely (ongoing issues require permanent visibility)
- **In Progress** - Kept indefinitely (active work in progress)
- **Deferred** - Kept indefinitely (known issues that may need future action)
- **Resolved** - Kept indefinitely until manually closed

**Rationale:** Active reports represent ongoing or unresolved issues. Auto-deleting these would lose critical information about trail system problems that may require future attention.

**Closed/Cancelled Reports (2-Year Retention):**

- **Closed** - Deleted 2 years after closure date
- **Cancelled** - Deleted 2 years after cancellation date

**Rationale:** Matches user data and status history retention policy (2 years). Resolved reports have historical value but do not require permanent storage. Two years provides sufficient time for trend analysis and liability protection.

**Photo Retention (180 Days After Closure):**

- Photos attached to **closed** reports: Deleted 180 days after report closure
- Photos attached to **cancelled** reports: Deleted 180 days after report cancellation
- Photos attached to **active** reports (open, in-progress, deferred, resolved): Retained indefinitely with report

**Rationale:** Photos are valuable during active issue resolution and for short-term historical reference (6 months). After 180 days, report text/data remains but photos are deleted to save S3 storage costs. This aggressive photo cleanup balances cost with utility.

**Report Text/Data vs. Photos:**

- Report text, title, description, comments, activity log: Retained per status rules above
- Photos: More aggressive deletion (180 days after closure) regardless of report text retention
- After photo deletion, report shows "Photo no longer available (deleted per retention policy)"

**Retention Implementation:**

- **Automated cleanup job** - Daily cron job identifies reports/photos eligible for deletion
- **Soft delete** - Reports marked as deleted (not hard deleted from DynamoDB) for 90 days
- **Hard delete** - After 90-day grace period, reports permanently removed from database
- **Audit logging** - All deletions logged in CloudTrail for compliance

**Manual Deletion:**

- Org-admins can manually delete reports immediately (bypasses retention policy)
- Manual deletion requires confirmation and reason
- Deleted reports enter 90-day soft-delete grace period before hard deletion

**User Notification:**

- No user notification for automatic report/photo deletion (expected behavior per policy)
- Users can see retention policy in help documentation
- Report interface shows "This report will be auto-deleted on [date]" for closed/cancelled reports

**Compliance Notes:**

- Retention policy disclosed in Privacy Policy
- Users can export their report data before deletion (GDPR Article 20)
- Manual deletion available on request (GDPR Article 17)
- CloudTrail logs retention/deletion actions for audit trail (1 year retention)

---

### 3. User Management & Authentication

#### 3.1 User Roles (All 8 Roles - As Designed in Current Codebase)

- **superadmin** - Platform super admin (TrailLens staff)
- **admin** - Site administrator
- **org-admin** - Organization administrator (full org control)
- **trailsystem-owner** - Can manage specific trails
- **trailsystem-crew** - Can update trail status and submit work logs
- **trailsystem-status** - Can only update trail status (limited crew)
- **content-moderator** - Moderate user-generated content
- **org-member** - Basic organization member access

**Note:** All 8 roles from current implementation remain unchanged. These provide the granular permissions needed for proper trail organization management.

#### 3.2 Authentication Methods (REQUIRED FOR MVP - Security Focus)

**REQUIRED 1: Passkey Login (Passwordless, Phishing-Resistant)**

- **What:** WebAuthn/FIDO2 passkeys (Touch ID, Face ID, security keys)
- **Why:** Most secure authentication method (no passwords to steal/phish)
- **Implementation:**
  - AWS Cognito passkey support (if available) OR custom WebAuthn integration
  - Primary authentication method for all users
- **Reference:** [docs/SECURITY_REPORT_FOR_CEO.md](SECURITY_REPORT_FOR_CEO.md) - Addresses PII security risks
- **Status:** REQUIRED FOR MVP ✅

**REQUIRED 2: Magic Link Login (Email-Based, No Passwords)**

- **What:** User enters email, receives time-limited login link
- **Why:** Eliminates password management, reduces credential theft risk
- **Implementation:**
  - Generate short-lived JWT token (5-15 minute expiration)
  - Send via AWS SES with link to auth endpoint
  - Single-use token (invalidated after first use)
- **Use Case:** Users without passkey-capable devices, or as backup method
- **Status:** REQUIRED FOR MVP ✅

**REQUIRED 3: Traditional Email/Password (Fallback Only)**

- **What:** Standard username/password with strong requirements
- **Why:** Compatibility for older systems/browsers
- **Implementation:**
  - AWS Cognito User Pool with strong password policy
  - MFA required for org-admin, trailsystem-owner, and superadmin roles
  - Password rotation encouraged (not enforced for MVP)
- **Status:** REQUIRED FOR MVP ✅

**Rationale:** Passkeys + Magic Links eliminate 90%+ of credential-based attacks while maintaining excellent UX. All three methods are required for MVP to ensure broad compatibility and maximum security.

#### 3.3 User Profile Management

- **Users can update their own data:**
  - Name, email address
  - Contact preferences (email, SMS, push notifications)
  - Preferred notification channels
  - Profile photo (optional)

- **Users can manage notification methods:**
  - Add/remove email addresses
  - Add/remove phone numbers for SMS
  - Enable/disable notification types
  - Set quiet hours (e.g., no notifications 10pm-7am)

#### 3.4 User Dashboard (Simplified for MVP)

- **For regular users:**
  - View subscribed trails and current status
  - Notification history (last 30 days)
  - Update profile and contact methods
  - Manage notification preferences

- **For trailsystem-crew:**
  - All user features PLUS:
  - Quick status update interface for trail systems they manage
  - View trail systems they manage
  - Upload status photos to trail systems
  - View status history for their trail systems

- **For org-admin:**
  - All trailsystem-crew features PLUS:
  - Manage organization members
  - Invite new users
  - Create/edit/delete trail systems for their organization
  - Manage organization's status types (customize from templates)
  - View organization analytics (basic: status changes, notifications sent, subscriber counts)
  - Bulk update multiple trail systems

- **For superadmin:**
  - Full access to all organizations
  - Create/edit status type templates
  - Create new organizations and trail systems
  - Platform-wide analytics
  - View all trail systems across all organizations

---

### 4. Notification System

#### 4.1 Notification Channels (MVP: Email + SMS)

**Email Notifications**

- **Trigger:** Trail status changes to subscribed trails
- **Delivery:** AWS SES (verified domain: traillenshq.com)
- **Content:**
  - Trail name
  - New status (with status group)
  - Reason/notes from trail crew
  - Photo (if attached)
  - Link to trail details
- **Frequency options:**
  - Immediate (real-time, within 1 minute) - Only option for MVP
  - ~~Daily digest~~ - REMOVED: Status updates are event-driven, not batched
  - ~~Weekly summary~~ - REMOVED: Not needed for real-time trail status

**SMS Notifications**

- **Trigger:** Urgent status changes only (Closed, Caution)
- **Delivery:** AWS SNS → Twilio OR Pinpoint
- **Content:** Concise text-only (160 chars max)
  - "🚨 [Trail Name] is now CLOSED: [Reason]. Details: [short link]"
- **Cost consideration:** ~$0.0075 per SMS, so optional/opt-in for users
- **Rationale:** SMS for critical alerts only, email for routine updates

#### Push Notifications (REQUIRED FOR MVP - iPhone Apps)

- **Trigger:** Trail status changes to subscribed trails
- **Delivery:** AWS SNS → APNS (Apple Push Notification Service)
- **Content:**
  - Trail name, new status, reason
  - Optional photo thumbnail
  - Deep link to trail details in app
- **Platform:** iPhone apps only (iOS 15+)
- **Status:** REQUIRED FOR MVP ✅

#### Future (Post-MVP)

- Android push notifications (FCM)
- In-app notifications (badge counts, notification center)

#### 4.2 Subscription Management

**Subscription Options:**

- **Individual trail systems** - Subscribe to specific trail systems (e.g., Hydrocut trail system only, not Guelph Lake)
- **Entire organization** - Subscribe to ALL trail systems in an organization (e.g., all Hydrocut trail systems)

**Subscription Limits (MVP):**

- Free tier: 5 trail system subscriptions per user
- Pro tier: Unlimited trail system subscriptions

**Notifications Received:**

- **Status changes** - When trail system status changes (required, core feature)
- **Scheduled change reminders** - Notification before scheduled status change (e.g., "Hydrocut trail system closing Nov 1 in 3 days")

**Unsubscribe:**

- One-click unsubscribe link in every email
- Granular control (unsubscribe from specific trail system, not all)

---

### 5. Target Organizations (Pilot Program)

#### 5.1 Hydrocut

- **Location:** Kitchener-Waterloo, Ontario, Canada
- **Trail Systems:**
  - **Hydrocut** trail system (mountain biking focus, includes Glasgow and Synders areas)
- **User Base:** 500-1000 active trail users
- **Pain Points:**
  - Manual Facebook posts for every trail system status change
  - Users don't know which trail system is open/closed until they arrive
  - Volunteer coordination via email/spreadsheets

#### 5.2 GORBA (Grand River Off-Road Association of Bikers)

- **Location:** Cambridge/Guelph, Ontario, Canada
- **Trail Systems:**
  - **Guelph Lake** trail system (mountain biking)
  - **Akell** trail system (mountain biking)
- **User Base:** 300-500 active trail users
- **Pain Points:**
  - Similar to Hydrocut
  - Limited communication tools
  - Seasonal trail system management complexity (winter closures)

#### 5.3 Pilot Success Criteria

- **Onboarding:** Both organizations fully set up within 2 weeks
  - All 3 trail systems created (Hydrocut, Guelph Lake, Akell)
  - Status types configured for each organization
  - Key admins and trail crew trained
- **Adoption:** 70%+ of trail users subscribe to trail system notifications
- **Engagement:** 90%+ of trail system status changes include photo and reason
- **Reliability:** 99.9% notification delivery rate
- **Performance:** Trail system status updates propagate to users within 2 minutes

---

### 6. Security Requirements (From Security Report)

**Reference:** [docs/SECURITY_REPORT_FOR_CEO.md](SECURITY_REPORT_FOR_CEO.md) - Section 3: Current Security Posture

#### 6.1 Address Critical Security Gaps (MUST DO for MVP)

**GAP 1: Enable CloudTrail Audit Logging**

- **What:** Enable AWS CloudTrail on production account
- **Why:** Required to detect insider threats, investigate breaches, meet compliance
- **Implementation:**
  - CloudTrail logs to dedicated S3 bucket
  - 90-day retention (GDPR requirement)
  - Log all API calls: DynamoDB, S3, Cognito, Secrets Manager
- **Cost:** ~$2-5/month
- **Status:** NOT CURRENTLY ENABLED ⚠️

**GAP 2: Data Processing Agreement (DPA) with AWS**

- **What:** Sign AWS GDPR Data Processing Addendum
- **Why:** Legal requirement for GDPR/CCPA compliance (future production requirement)
- **Implementation:**
  - AWS account admin signs DPA in AWS console
  - Document signed agreement
- **Cost:** Free
- **Status:** NOT REQUIRED FOR MVP (defer to production launch) ⏸️

**GAP 3: Create Incident Response Plan**

- **What:** Documented runbook for security incidents
- **Why:** GDPR requires 72-hour breach notification
- **Implementation:**
  - Define escalation procedures
  - Create security contact (<security@traillenshq.com>)
  - Document breach notification process
  - Assign security lead
- **Cost:** Internal time only
- **Status:** NO PLAN EXISTS ⚠️

**GAP 4: Enable API Rate Limiting**

- **What:** API Gateway throttling (100 requests/min per user)
- **Why:** Prevent DDoS, credential stuffing, brute force attacks
- **Implementation:**
  - Enable API Gateway throttling policies
  - Per-user rate limits via JWT claims
  - IP-based rate limiting for public endpoints
- **Cost:** Included in API Gateway pricing
- **Status:** CONFIGURED BUT NOT ENABLED ⚠️

**GAP 5: Deploy AWS WAF (Web Application Firewall)**

- **What:** WAF rules to block OWASP Top 10 exploits
- **Why:** Protect against XSS, SQL injection (mitigated by DynamoDB), DDoS
- **Implementation:**
  - AWS WAF with managed rule sets
  - CloudFront + API Gateway integration
- **Cost:** $5-20/month
- **Status:** NOT DEPLOYED ⚠️

**GAP 6: Rotate Secrets and Remove Placeholders**

- **What:** Replace `"CHANGE_ME_IN_PRODUCTION"` with real secrets
- **Why:** Hardcoded placeholders are security vulnerabilities
- **Implementation:**
  - Generate strong random secrets (32+ chars)
  - Store in AWS Secrets Manager
  - Enable 90-day automatic rotation
- **Cost:** $0.40 per secret per month
- **Status:** PLACEHOLDER SECRETS EXIST ⚠️

**GAP 7: Enable Security Hub and GuardDuty** (MOVED TO POST-MVP)

- **What:** AWS threat detection and continuous compliance monitoring
- **Why:** Detect anomalous access patterns, insider threats, compromised credentials
- **Implementation:**
  - Enable AWS Security Hub (compliance dashboards)
  - Enable AWS GuardDuty (threat detection)
  - Configure CloudWatch alarms for security findings
- **Cost:** ~$54/month (Security Hub: ~$50/month, GuardDuty: ~$4/month)
- **Status:** MOVED TO POST-MVP DUE TO COST ⏸️

#### 6.2 PII Data Protection (REQUIRED FOR MVP)

- **Encryption at rest:** All DynamoDB tables, S3 buckets (already implemented ✅)
- **Encryption in transit:** HTTPS/TLS 1.2+ only (already implemented ✅)
- **Data minimization:** Only collect PII necessary for service (implement during build)
- **Data retention policy:** Delete inactive user data after 2 years (REQUIRED FOR MVP ✅)
- **User data export API:** Endpoint for users to download their data (GDPR Article 20) (REQUIRED FOR MVP ✅)
- **User data deletion API:** Endpoint for users to delete their account (GDPR Article 17) (REQUIRED FOR MVP ✅)
- **MFA for admin accounts:** Required for org-admin, trailsystem-owner, and superadmin roles (REQUIRED FOR MVP ✅)

#### 6.3 Compliance Documentation (Legal Review Required)

- **Privacy Policy** - Disclose what PII we collect, how we use it, who we share with
- **Terms of Service** - Liability waiver for outdated trail information
- **Cookie Policy** - Disclose cookies used on website
- **Data Processing Agreements (DPAs)** - With AWS, Twilio (SMS), any third parties

**Recommendation:** Engage legal counsel to draft/review before production launch.

---

### 7. iPhone Apps (REQUIRED FOR MVP)

**CRITICAL:** iPhone apps are REQUIRED for MVP. Android apps to follow post-MVP.

#### 7.1 User iPhone App (REQUIRED FOR MVP)

- **Purpose:** Trail users can view status, get push notifications, submit and view trail care reports
- **Platform:** iOS (Swift) - Native app
- **Features:**
  - **View trail systems** - Grouped by organization (Hydrocut → Hydrocut trail system)
  - **Real-time status viewing** - See current status of each trail system
  - **Status history** - View past status changes with photos and reasons
  - **View public trail care reports** - See community-submitted reports for subscribed trail systems
    - Filter by trail system, priority, status, type tags
    - View report details: title, description, photos, priority, status, days open
    - View report comments and activity log (trail crew updates)
  - **Submit new trail care reports** - Report issues, hazards, or observations from the field
    - Camera integration for capturing issue photos (up to 5 photos per report)
    - Auto-set to public visibility, P3 priority
    - Assign type tags from organization's tag pool
    - GPS location auto-capture (with permission)
    - Quick submission workflow optimized for field use
  - **My Reports dashboard** - View all reports submitted by user
    - Track report status changes
    - Receive notifications when crew updates reports
    - View crew comments and resolution notes
  - **Push notifications** (APNS via AWS SNS) - Status changes, scheduled reminders, and care report updates
  - **Subscription management** - Subscribe to individual trail systems or entire organizations
  - **Login** via passkey, magic link, or email/password
  - **Profile and notification preferences**
  - **Offline mode** - Cache last-known trail system status with staleness warning
- **Status:** REQUIRED FOR MVP ✅
- **Target:** iOS 15+ (supports passkeys/WebAuthn)

#### 7.2 Admin/TrailLens iPhone App (REQUIRED FOR MVP - Single Unified App)

- **Purpose:** Trail org admins AND TrailLens super admins can manage trails and trail care reports from the field
- **Platform:** iOS (Swift) - Native app
- **Architecture:** Single app with role-based UI
  - Trail org admins see their organization only
  - TrailLens admins (when logged in) see all organizations
- **Features:**
  - **Quick status update** - Change trail system status in <30 seconds (camera integration for photos)
  - **View status history** - Complete audit log of trail system status changes
  - **Manage trail systems** - Create, view, edit, delete trail systems (org-admin only)
  - **Bulk status update** - Update multiple trail systems at once (org-admin only)
  - **Schedule status changes** - Pre-schedule future status changes for trail systems
  - **Trail Care Reports - Full Management** - Complete CRUD operations for reports
    - **View all reports** - Public and private reports for organization
    - **Create work logs** - Quick private report creation (camera integration)
      - Fast workflow for crew field work logs
      - Set as private (is_public = false) by default
      - Set priority (P1-P5), assign to crew, add type tags
      - Camera integration for work documentation (up to 5 photos)
      - GPS location auto-capture
    - **Manage reports** - Change priority, status, assignment, type tags
    - **Add comments** - Update reports with progress notes and photos
    - **Close/cancel reports** - Add resolution notes when completing work
    - **Assign reports** - Assign to specific crew members or self-assign
    - **Dashboard views:**
      - Assigned to Me (for trailsystem-crew)
      - Unassigned Pool (for self-assignment)
      - All Open Reports (org-wide view for admins)
      - Filter by priority, status, type tags, trail system, days open
    - **Link reports to status changes** - Change trail system status based on report
  - **Dashboard access** - Role-specific UI (org-admin sees their org, superadmin sees all orgs)
  - **Login** via passkey, magic link, or email/password
  - **Photo upload** from camera or photo library with geolocation and metadata
- **Status:** REQUIRED FOR MVP ✅
- **Target:** iOS 15+

**Note:** Admin and TrailLens super admin functionality combined into ONE app. Role-based access control determines which features/organizations are visible.

**Android Apps:** Post-MVP. iOS apps must be fully functional for pilot program (Hydrocut, GORBA).

---

### 8. TrailPulse - Trail Feedback and Usage Tracking

**TrailPulse** is a privacy-first trail feedback and usage tracking system that enables trail system owners to gather rider feedback and track trail usage through GPS-based ride detection.

#### Feature Overview

TrailPulse transforms trail system management by providing software-based trail counting and real-time condition feedback from the riding community. The system uses GPS technology to detect when users visit subscribed trail systems, prompting them for post-ride feedback while maintaining strict privacy controls.

**What it does:**
- Automatically detects trail system visits via GPS geofencing
- Prompts users for post-ride feedback on trail conditions
- Tracks trail system usage counts (replaces hardware counters)
- Provides trail system owners with actionable feedback data

**Why it matters:**
- **Software-based counting**: Eliminates need for expensive hardware trail counters
- **Community-driven conditions**: Real-time feedback from actual riders
- **Data-driven decisions**: Trail system owners can prioritize maintenance based on user feedback

**Key benefits:**
- **Privacy-first design**: Only tracks within subscribed trail systems, easy opt-out available
- **Subscription-based**: Users must subscribe to a trail system before any tracking occurs
- **Rider-focused**: Quick, simple feedback collection (< 30 seconds)
- **Cost-effective**: No hardware infrastructure required

#### 8.1 Mobile App - GPS Tracking and Ride Detection

**Mobile Team Implementation** (separate mobile repository handles all GPS functionality)

**Location Tracking (R1.1)**

GPS tracking operates ONLY within subscribed trail systems:
- Geofencing detects trail system entry/exit
- No tracking outside subscribed boundaries
- Default: GPS tracking enabled (but only within subscribed systems)
- User opt-out available in preferences
- Users who opt out are not tracked (usage still counted via other means if possible)

**Privacy Controls (R1.2)**

Clear privacy protections and user control:
- User consent during onboarding about location tracking
- Visible indicator when GPS tracking is active
- Easy access to disable tracking in settings
- No location data stored outside subscribed trail systems
- No individual route tracking (only entry/exit and usage count)

**Ride Detection (R1.3)**

Automated detection of trail system visits:
- Detect user entry into subscribed trail system
- Detect user exit from subscribed trail system
- Calculate ride duration (entry to exit time)
- Increment usage count for user and trail system
- Handle edge cases (app backgrounded, GPS signal loss, etc.)

**Post-Ride Notification (R1.4)**

Push notification triggers feedback collection:
- Send push notification when user exits trail system
- Notification content: "How were the trails today?" (customizable by trail owner)
- Deeplink to feedback form in app
- Allow user to dismiss or complete feedback
- Respect notification preferences (DND, quiet hours)

#### 8.2 Post-Ride Feedback Collection

**Trail Condition Feedback - Every Ride (R2.1)**

Simple, quick condition reporting:
- Present trail condition options configured by trail system owner
- Default conditions: Dry, Muddy, Wet, Icy, Snowy, Rocky, Dusty
- Single or multiple selection based on owner configuration
- Optional free-text comment field
- Quick submit (< 30 seconds to complete)

**Additional Questions - Configurable Frequency (R2.2)**

Customizable questions asked periodically:
- Trail system owner defines additional questions
- Owner sets frequency threshold (e.g., every 10 rides)
- Question types supported:
  - Multiple choice
  - Rating scale (1-5 stars)
  - Yes/No
  - Free text
- Track question response count to determine when to ask next

**Web Interface Feedback (R2.3)**

Manual feedback submission via web:
- Login required (authenticated users only)
- Manual feedback submission (not tied to GPS ride detection)
- Select trail system from subscribed list
- Same question flow as mobile app
- Timestamp and user ID recorded

#### 8.3 Trail System Owner Configuration

**Condition Configuration (R3.1)**

Customize trail condition tracking:
- Define list of trail conditions to track
- Set condition types (single vs. multiple selection)
- Enable/disable condition tracking
- Preview how conditions appear to users

**Additional Questions Configuration (R3.2)**

Create custom feedback questions:
- Create custom questions
- Set question type (multiple choice, rating, yes/no, text)
- Define response options for multiple choice
- Set frequency threshold (e.g., ask every N rides)
- Enable/disable specific questions
- Reorder questions

**Notification Customization (R3.3)**

Configure post-ride notifications:
- Customize exit notification message
- Set notification timing (immediate, 5 min delay, etc.)
- Enable/disable notifications

#### 8.4 Feedback Data Management Interface

**Feedback Data Viewing (R4.1)**

Comprehensive feedback viewing for trail admins:
- View all feedback responses for their trail system(s)
- Display feedback in table/list format with key columns:
  - Date/time of ride
  - User identification (name, email, or anonymous ID)
  - Trail conditions reported
  - Responses to additional questions
  - Free-text comments
  - User metadata (crew member status, feedback count)
- Paginated results for large datasets
- Default sort by most recent first
- Visual indicators for different condition types
- Expandable rows for detailed view

**Search and Filter Capabilities (R4.2)**

Comprehensive filtering for feedback analysis:
- **Date Range Filter**: Filter feedback by date range (last 7 days, last 30 days, custom range)
- **Condition Filter**: Filter by specific trail conditions (e.g., show only "Muddy" reports)
- **User Filter**: Filter by specific user or user type (crew members, regular users, frequent reporters)
- **Question Filter**: Filter by responses to specific additional questions
- **Text Search**: Search within free-text comments
- **Feedback Count Filter**: Show users who have submitted N+ feedback entries
- **Combined Filters**: Apply multiple filters simultaneously
- **Save Filter Presets**: Save commonly used filter combinations

**Feedback Management (R4.3)**

Data quality and relevance management:
- **Delete Single Feedback**: Remove individual feedback entry with confirmation
- **Bulk Delete**: Select multiple feedback entries and delete together
- **Delete by Filter**: Delete all feedback matching current filter criteria (with confirmation)
- **Soft Delete Option**: Mark feedback as deleted without permanent removal (for audit trail)
- **Deletion Reason**: Optional field to note why feedback was deleted
- **Deletion Audit Log**: Track who deleted what and when

**User Feedback Statistics (R4.4)**

Aggregate user statistics for pattern identification:
- **User Feedback Count**: Total number of feedback submissions per user
- **Crew Member Identification**: Visual badge or indicator for trail crew members
- **Feedback Frequency**: Average time between feedback submissions per user
- **Most Active Contributors**: Leaderboard or list of top feedback providers
- **User Feedback History**: Click user to see all their feedback submissions
- **Reliability Score**: Optional metric based on feedback consistency (post-MVP)

**Data Usage for Trail Condition Management (R4.5)**

Integration with trail condition workflow:
- **Quick Condition Update**: Set trail condition based on recent feedback with one click
- **Feedback Summary View**: Aggregate view showing condition distribution (e.g., "70% reported Muddy")
- **Suggested Conditions**: System suggests trail condition based on recent feedback patterns
- **Feedback Context**: When setting conditions manually, show recent feedback as reference
- **Decision Support**: Show trend of conditions over past week/month

**Crew Member Management (R4.6)**

Track and manage crew member status:
- **Crew Member Flag**: Admin can mark users as crew members
- **Crew Feedback Weighting**: Option to give more visibility to crew member feedback
- **Crew Activity Tracking**: See which crew members are actively providing feedback
- **Bulk Crew Assignment**: Add/remove crew status for multiple users
- **Crew Member Notes**: Add notes about crew members (roles, responsibilities)

#### 8.5 Trail System Geofence Management

**Geofence Data Model (R5.1)**

Trail system boundary definitions:
- Store trail system boundary coordinates in DynamoDB
- Support GeoJSON format or simple polygon coordinates
- Each trail system must have defined boundaries for ride detection
- Boundaries define where GPS tracking is active

**Admin Interface for Geofences (R5.2)**

Geofence management UI:
- Trail system owners can define/edit geofence boundaries
- Map-based interface for drawing boundaries (or coordinate input)
- Preview geofence coverage on map
- Validate boundary data (closed polygon, reasonable size)

**API for Geofence Data (R5.3)**

Mobile app geofence retrieval:
- Mobile app retrieves geofence boundaries for subscribed trail systems
- Efficient boundary queries (don't send all geofences, only subscribed)
- Cache geofence data on mobile device
- Update geofences when trail system boundaries change

**Geofence Validation (R5.4)**

Backend validation and security:
- Backend validates ride start/end coordinates are within geofence
- Prevent false positives from GPS drift
- Reject ride events from non-subscribed trail systems
- Log geofence violations for debugging

#### 8.6 Usage Counting System

**Trail Usage Metrics (R6.1)**

Comprehensive usage tracking:
- Count total rides for each trail system (all users combined)
- Count rides per user per trail system
- Store counts with timestamp for trend analysis
- No personally identifiable route data stored
- Aggregate counts visible to trail system owners

**Count Accuracy (R6.2)**

Accurate usage counting:
- Count users who opt out of GPS (if app is open during ride)
- Deduplicate multiple entries/exits within short time window
- Handle offline scenarios (sync counts when connection restored)

**Reporting for Trail Owners (R6.3)**

Usage analytics and reporting:
- Daily/weekly/monthly usage counts
- Trend graphs over time
- Export usage data (CSV)
- Software-based alternative to hardware trail counters

#### 8.7 Data Model

**Database Schema (R7.1)**

TrailPulse DynamoDB tables:
- **TrailConditions**: condition options per trail system
- **AdditionalQuestions**: custom questions per trail system
- **RideEvents**: entry/exit timestamps, user, trail system (TTL: 90 days)
- **FeedbackResponses**: user responses to conditions and questions (includes soft_delete flag, deleted_at, deleted_by, deletion_reason)
- **UsageCounts**: aggregated ride counts per trail system
- **UserPreferences**: GPS opt-out, notification settings
- **QuestionResponseTracker**: count responses to trigger frequency logic
- **TrailSystemGeofences**: boundary coordinates for each trail system (GeoJSON or polygon)
- **CrewMembers**: user_id, trail_system_id, is_crew flag, crew_notes, assigned_at, assigned_by
- **FeedbackDeletionAudit**: audit log for deleted feedback (feedback_id, deleted_at, deleted_by, deletion_reason, was_soft_delete)

**Data Retention (R7.2)**

TrailPulse data retention policy:
- **Individual ride events**: 90 days (use DynamoDB TTL for automatic deletion)
- **Aggregated usage counts**: indefinite
- **Feedback responses**: indefinite
- **User preferences**: until account deletion
- **Geofence boundary data**: indefinite (part of trail system configuration)

#### 8.8 Push Notification Integration

**SNS Mobile Integration (R8.1)**

Extend SNS infrastructure for TrailPulse:
- Extend existing SNS infrastructure for mobile push notifications
- Mobile team will provide device tokens for registered users
- Backend stores device tokens in DynamoDB (UserPreferences or separate table)
- Send post-ride notification via SNS to user's registered device(s)

**Notification Triggers (R8.2)**

Configure notification sending:
- Trigger notification when ride end event is recorded
- Include trail system name and feedback link in notification payload
- Respect user notification preferences (can opt out of feedback notifications)
- Handle notification failures gracefully (log but don't block ride recording)

**Notification Content (R8.3)**

Notification message format:
- Default message: "How were the trails at [Trail System Name] today?"
- Trail owners can customize notification message (optional)
- Include deeplink to feedback form: `traillens://feedback/{ride_id}`
- 24-hour expiration for feedback link

#### 8.9 API Endpoints

**Mobile App Endpoints (R9.1)**

Endpoints for mobile app integration (8 endpoints):
- `POST /api/trailpulse/rides/start` - Record ride entry
- `POST /api/trailpulse/rides/end` - Record ride exit, trigger notification
- `GET /api/trailpulse/geofences` - Get geofence boundaries for subscribed trail systems
- `GET /api/trailpulse/trail-systems/{id}/feedback-config` - Get questions for feedback
- `POST /api/trailpulse/feedback` - Submit feedback response
- `GET /api/trailpulse/user/ride-count/{trail_system_id}` - Get user ride count
- `PUT /api/trailpulse/user/preferences` - Update GPS/notification settings
- `POST /api/trailpulse/device-token` - Register device for push notifications

**Web Endpoints (R9.2)**

Web interface feedback endpoints (2 endpoints):
- `GET /api/trailpulse/trail-systems/subscribed` - Get user's subscribed trail systems
- `POST /api/trailpulse/feedback/web` - Submit web-based feedback
- All endpoints require authentication

**Admin Configuration Endpoints (R9.3)**

Trail system owner configuration endpoints (8 endpoints):
- `GET /api/trailpulse/admin/trail-systems/{id}/config` - Get current configuration
- `PUT /api/trailpulse/admin/trail-systems/{id}/conditions` - Update trail conditions
- `POST /api/trailpulse/admin/trail-systems/{id}/questions` - Create additional question
- `PUT /api/trailpulse/admin/trail-systems/{id}/questions/{question_id}` - Update question
- `DELETE /api/trailpulse/admin/trail-systems/{id}/questions/{question_id}` - Delete question
- `GET /api/trailpulse/admin/trail-systems/{id}/usage` - Get usage statistics
- `PUT /api/trailpulse/admin/trail-systems/{id}/geofence` - Update geofence boundaries
- `GET /api/trailpulse/admin/trail-systems/{id}/geofence` - Get geofence boundaries

**Admin Feedback Management Endpoints (R9.4)**

Feedback data viewing, searching, and management endpoints (10 endpoints):
- `GET /api/trailpulse/admin/trail-systems/{id}/feedback` - Get feedback with pagination and filters
  - Query params: `page`, `limit`, `start_date`, `end_date`, `condition`, `user_id`, `user_type`, `question_id`, `search_text`, `min_feedback_count`
- `GET /api/trailpulse/admin/trail-systems/{id}/feedback/{feedback_id}` - Get single feedback detail
- `DELETE /api/trailpulse/admin/trail-systems/{id}/feedback/{feedback_id}` - Delete single feedback
  - Body: `{ "reason": "optional deletion reason", "soft_delete": true/false }`
- `POST /api/trailpulse/admin/trail-systems/{id}/feedback/bulk-delete` - Delete multiple feedback entries
  - Body: `{ "feedback_ids": [...], "reason": "optional", "soft_delete": true/false }`
- `POST /api/trailpulse/admin/trail-systems/{id}/feedback/delete-by-filter` - Delete all feedback matching filters
  - Body: Same filter params as GET endpoint, plus `reason` and `soft_delete`
- `GET /api/trailpulse/admin/trail-systems/{id}/feedback/statistics` - Get aggregated feedback statistics
  - Response: condition distribution, user feedback counts, crew member activity, trends
- `GET /api/trailpulse/admin/trail-systems/{id}/users/{user_id}/feedback` - Get all feedback from specific user
- `PUT /api/trailpulse/admin/trail-systems/{id}/users/{user_id}/crew-status` - Set user as crew member
  - Body: `{ "is_crew": true/false, "notes": "optional crew notes" }`
- `GET /api/trailpulse/admin/trail-systems/{id}/crew-members` - Get list of crew members
- `POST /api/trailpulse/admin/trail-systems/{id}/crew-members/bulk` - Set crew status for multiple users
  - Body: `{ "user_ids": [...], "is_crew": true/false }`

#### 8.10 Integration Points

**Existing Systems**

TrailPulse integrates with:
- **Cognito**: User authentication (both web and mobile)
- **Subscription management**: Must check active subscription before tracking
- **SNS**: Push notification service (existing infrastructure, needs mobile integration)
- **DynamoDB**: Application data storage
- **Trail system data**: Geofence coordinates for boundaries

**New Infrastructure Needed**

TrailPulse requires:
- DynamoDB tables for TrailPulse data (10 new tables)
- SNS topic for push notifications (mobile device endpoints)
- API Gateway endpoints for TrailPulse APIs (28 new endpoints)
- Lambda functions for API handlers
- DynamoDB TTL configuration for ride event expiration (90 days)
- Background job for aggregating usage counts (optional - can be done on-demand)

**Backend-Mobile Integration Flow**

1. **Initial Setup**:
   - Backend: Deploy DynamoDB tables, API endpoints, SNS topics
   - Mobile: Implement authentication, obtain user subscription list
   - Mobile: Call `GET /api/trailpulse/geofences` to fetch geofence boundaries
   - Mobile: Register device token via `POST /api/trailpulse/device-token`

2. **Ride Detection**:
   - Mobile: Detect geofence entry (client-side)
   - Mobile: Call `POST /api/trailpulse/rides/start` with coordinates and trail system ID
   - Backend: Validate subscription, validate coordinates within geofence, record ride start
   - Mobile: Track presence in trail system (no continuous API calls)
   - Mobile: Detect geofence exit (client-side)
   - Mobile: Call `POST /api/trailpulse/rides/end` with exit coordinates
   - Backend: Record ride end, increment usage count, trigger SNS notification

3. **Feedback Collection**:
   - Mobile: Receive push notification with deeplink
   - Mobile: User taps notification, opens feedback form
   - Mobile: Call `GET /api/trailpulse/trail-systems/{id}/feedback-config` to get questions
   - Mobile: Display questions to user
   - Mobile: Call `POST /api/trailpulse/feedback` to submit responses
   - Backend: Store feedback responses

4. **Admin Configuration**:
   - Web: Trail owner logs in, navigates to TrailPulse settings
   - Web: Call admin endpoints to configure conditions, questions, geofences
   - Backend: Store configuration
   - Mobile: Fetch updated configuration on next sync

#### 8.11 MVP Scope

**Must Have for MVP - This Repo (Backend & Web)**

Documentation scope for this repository:
- DynamoDB schema for ride events, feedback, usage counts, geofences, preferences, crew members, audit logs
- Backend API endpoints for mobile app (8 endpoints: ride start/end, feedback, geofences, preferences)
- Backend API endpoints for web (2 endpoints: feedback submission)
- Admin API endpoints (8 endpoints: configuration, usage stats, geofence management)
- Admin API endpoints for feedback management (10 endpoints: view, search, filter, delete, crew member management)
- SNS integration for push notifications
- Web feedback form (manual feedback entry)
- Admin configuration interface (trail conditions, questions, geofences)
- Admin feedback data management interface (view, search, filter, delete feedback)
- Crew member management interface (assign/remove crew status)
- Usage counting and aggregation logic
- Data retention (90-day TTL on ride events, soft delete for feedback)
- Web feature list update with TrailPulse entry
- Infrastructure deployment (DynamoDB tables, API Gateway, SNS topics)

**Must Have for MVP - Mobile Team (Separate Repository)**

Mobile team implements:
- GPS tracking within subscribed trail systems
- Geofence detection (entry/exit)
- Ride start/end event recording (call backend API)
- Push notification client
- Mobile feedback form UI
- User preferences for GPS opt-out
- Device token registration

**Should Have (Post-MVP)**

Future enhancements:
- Advanced question types (rating scales, multi-select)
- Frequency-based additional questions
- Usage analytics dashboard with graphs (web)
- Export functionality (CSV)
- In-app feedback history for users (mobile)
- Map-based geofence editor (web admin)

**Nice to Have (Future)**

Long-term features:
- Real-time condition map (aggregated user reports)
- Weather integration for condition predictions
- Social features (share ride stats)
- Gamification (badges for ride counts)
- ML-based condition predictions

---

## Expected Behavior

### User Stories (MVP Acceptance Criteria)

**As a trail user, I want to:**

1. Subscribe to my favorite trail systems so I get notified when status changes
2. Subscribe to entire organizations to get updates for all their trail systems
3. Receive email/SMS/push notifications within 2 minutes of trail system status changes
4. View current status and history for trail systems I care about
5. Get reminders before scheduled trail system closures
6. Update my contact information and notification preferences
7. Log in securely without passwords (passkey or magic link)
8. **Submit trail care reports** - Report hazards, issues, or observations I encounter on the trail
9. **View public trail care reports** - See what issues other users and crew have reported for my subscribed trail systems
10. **Track my submitted reports** - See status updates, crew comments, and resolution notes for reports I've submitted
11. **Receive notifications** - Get notified when crew updates or resolves my submitted reports (opt-in)

**As a trail crew member, I want to:**

1. Update trail system status in <30 seconds from my phone (iPhone app or web)
2. Upload a photo with each status update showing current conditions
3. Add a reason/note explaining the status change
4. See the complete history of status changes for trail systems I manage
5. Schedule future status changes (e.g., "Close Hydrocut trail system Nov 1 for winter")
6. Log in quickly and securely to make urgent updates
7. **View all trail care reports** - See public and private reports for my organization
8. **Create work care report** - Quickly submit private reports documenting trail work from the field
9. **Manage report priority** - Triage reports by setting P1-P5 priority levels
10. **Self-assign reports** - Claim unassigned reports from the pool to work on
11. **Add comments to reports** - Update reports with progress notes and photos as work progresses
12. **Close reports** - Mark reports as resolved with resolution notes when work is complete
13. **Filter reports** - View reports by priority, status, type tags, trail system, or days open
14. **Link reports to status changes** - Change trail system status directly from a hazard report

**As an organization admin, I want to:**

1. Create and manage trail systems for my organization (add Hydrocut trail system, Guelph Lake trail system, etc.)
2. Invite new trail crew members via email
3. Customize my organization's status types (based on templates)
4. View analytics on status changes, notifications sent, subscriber counts per trail system
5. Update multiple trail systems to the same status simultaneously (e.g., "Close all Hydrocut systems due to storm")
6. Manage user roles and permissions (promote crew to admin, etc.)
7. View which trail systems are most popular (subscriber counts)
8. **All trail crew features** - Full access to trail care reports (view, create, manage, assign, comment, close)
9. **Manage care report type tags** - Create, update, and delete type tags for categorizing reports
10. **Assign reports to crew** - Assign reports to specific crew members for resolution
11. **View all reports** - See all public and private reports for the organization
12. **Analytics on reports** - View reports by status, priority, trail system, average resolution time, top submitters

**As a TrailLens admin, I want to:**

1. Access any organization's trail systems when logged in
2. Create new organizations (onboard Hydrocut, GORBA) and their trail systems
3. View platform-wide analytics (total trail systems, organizations, users, status changes)
4. Manage status type templates that organizations can use
5. Provide support to organization admins
6. Monitor system health and notification delivery rates

### Success Metrics (Pilot Program)

- **Reliability:** 99.9% uptime (API Gateway + Lambda)
- **Performance:** <500ms API response time (p95)
- **Notification latency:** <2 minutes from status change to user notification
- **Delivery rate:** 99%+ email delivery, 98%+ SMS delivery
- **User satisfaction:** NPS score 50+ from pilot organizations
- **Engagement:** 70%+ of trail users subscribe within first month

---

## Additional Notes

### What's In Scope for MVP

✅ **Trail system status management** (status types, tag-based organization, updates, photos, seasons)
✅ **Trail system entity** (name, description, location, cover photo, status, metadata)
✅ **Trail Care Reports** (unified issue tracking system with public/private visibility, P1-P5 priority, type tags, assignment, comments, photo attachments, status-based retention, iPhone app integration)
✅ **User authentication** (passkey, magic link, email/password - ALL THREE REQUIRED)
✅ **User profile and notification preference management**
✅ **Email, SMS, and push notifications** (push via iPhone apps)
✅ **User subscriptions** (subscribe to trail systems or entire organizations)
✅ **Subscription limits** (free tier: 5 trail systems, pro tier: unlimited)
✅ **Status history** (2-year retention, visible to users and admins)
✅ **Scheduled status changes** (multiple future changes per trail system)
✅ **Bulk status updates** (update multiple trail systems simultaneously)
✅ **Dashboards** (web-based for all 8 user roles)
✅ **iPhone apps** (User app + Admin/TrailLens unified app - REQUIRED)
✅ **Security hardening** (CloudTrail, WAF, incident response, secrets rotation)
✅ **PII protection** (data retention, export API, deletion API, MFA for admins)
✅ **Pilot onboarding** (Hydrocut with 1 trail system, GORBA with 2 trail systems)
✅ **All 8 user roles** (as designed in current codebase)
✅ **Tag-based status organization** (flexible per-organization tags, max 20 status tags, max 15 care report type tags)

### What's Out of Scope for MVP

❌ **Individual trail management** (MVP only manages trail systems, not individual trails within systems)
❌ **Social media automation** (Facebook/Instagram posting)
❌ **Android apps** (iOS only for MVP, Android post-MVP)
❌ **Forums and community features**
❌ **Events and volunteer management**
❌ **Advanced analytics and reporting** (only basic metrics for MVP)
❌ **Search and discovery** (beyond simple trail system list grouped by organization)
❌ **Reviews and ratings** (for trail systems)
❌ **Photo galleries** (beyond status photos and cover photos)
❌ **Multi-language support** (English only for MVP)
❌ **White-labeling for enterprise**
❌ **API partner program**
❌ **AWS DPA signing** (defer to production launch)
❌ **Trail difficulty ratings** (defer to post-MVP)
❌ **Trail system metadata** beyond core attributes (e.g., trail count, amenities, rules)
❌ **Recurring scheduled changes** (e.g., "Close every winter Nov-Apr" - manual scheduling only for MVP)
❌ **Multi-organization ownership** of trail systems (each trail system belongs to exactly one org)

### Additional Features from Reports (All REQUIRED for MVP)

**From SECURITY_REPORT_FOR_CEO.md (ALL REQUIRED):**

- ✅ **Implement passkey authentication** - Phishing-resistant, no passwords (REQUIRED)
- ✅ **Implement magic link authentication** - Eliminate password management (REQUIRED)
- ✅ **Implement email/password authentication** - Fallback compatibility (REQUIRED)
- ✅ **Enable CloudTrail** - Audit logging for compliance (REQUIRED)
- ✅ **Create incident response plan** - GDPR 72-hour breach notification (REQUIRED)
- ✅ **Enable API rate limiting** - Prevent DDoS and brute force attacks (REQUIRED)
- ✅ **Deploy AWS WAF** - Block OWASP Top 10 exploits (REQUIRED)
- ✅ **Rotate secrets and remove placeholders** - Eliminate hardcoded secrets (REQUIRED)
- ⏸️ **Enable Security Hub and GuardDuty** - Threat detection and compliance monitoring (MOVED TO POST-MVP DUE TO COST: ~$54/month)
- ✅ **Enable MFA for admin accounts** - Required for org-admin, trailsystem-owner, superadmin (REQUIRED)
- ✅ **Implement data retention policy** - Auto-delete inactive users after 2 years (REQUIRED)
- ✅ **Implement user data export feature** - GDPR Article 20 right to data portability via dashboard UI (REQUIRED)
- ✅ **Implement account deletion feature** - GDPR Article 17 right to be forgotten via user settings (REQUIRED)

**From MARKETING_PLAN.md:**

- ✅ **Update brand messaging** - Use "Building communities, one trail at a time" byline on website and marketing materials (REQUIRED)

**From SYSTEM_ARCHITECTURE.md (Deferred Post-MVP):**

- ⏸️ **Enable Redis caching** - Only if API response times >500ms (not needed for 2 orgs)
- ⏸️ **Implement ElasticSearch** - Only if >500 trails (not needed for MVP with 2 orgs)
- ⏸️ **Blue/Green Lambda deployments** - Zero-downtime deployments (nice to have, not critical)
- ⏸️ **Multi-region deployment** - Only if international expansion (not MVP)

**From MARKETING_PLAN.md (Deferred Post-MVP):**

- ⏸️ **Create case studies** - Document Hydrocut and GORBA pilot success (post-launch)
- ⏸️ **Blog content** - Trail management best practices (post-MVP marketing)

### MVP Implementation Decisions (Answered by CTO)

**Authentication:**

1. **AWS Cognito passkey support:** ✅ **DECISION: Use Cognito native passkey support** (if available as of Q1 2026, otherwise custom WebAuthn integration with Cognito user directory)
2. **Magic link expiration time:** ✅ **DECISION: 15 minutes** (better UX while maintaining security)
3. **Magic link delivery method:** ✅ **DECISION: Email only** (simpler, no SMS cost for auth)
4. **MFA enforcement timing:** ✅ **DECISION: 7-day grace period** (allow admin users to explore platform before MFA enforcement with reminder emails)

**Notifications:**

1. **SMS provider:** ✅ **DECISION: AWS Pinpoint** (native AWS integration, simpler setup, lower cost at $0.00645/SMS in Canada)
2. **SMS cost model:** Pay-per-message (default for Pinpoint)
3. **Daily digest email:** ✅ **DECISION: REMOVED FROM MVP** - CTO feedback: "No daily digest emails. No idea why we would need them. Status are a one time shot thing on change." Status updates are event-driven, not batched.
4. **Push notification delivery priority:** ✅ **DECISION: Normal priority for all** (consistent delivery, no special handling for urgent vs. non-urgent)
5. **Push notification sound:** ✅ **DECISION: Default iOS sound** (familiar to users, simple implementation)

**Status Types:**

1. **Status types:** Per organization (CONFIRMED by CTO earlier)
2. **Pre-population:** ✅ **DECISION: Pre-populate with templates** (provide "Mountain Biking Trail Org Template" for faster onboarding, orgs can customize)
3. **Status type limits:** ✅ **DECISION: 30 status types maximum** per organization (prevents UI clutter)
4. **Status group editing:** ✅ **DECISION: Fixed groups (no editing)** (5 groups are platform-wide standards: Open, Closed, Caution, Maintenance, Seasonal)

**Data Model:**

1. **Status history retention:** ✅ **DECISION: 2 years** (matches user retention policy, consistent data lifecycle)
2. **Photo storage lifecycle:** ✅ **DECISION: Delete after 90 days if trail system deleted** (aggressive cleanup saves storage, removes photos when trail system no longer exists)
3. **Inactive user deletion:** ✅ **DECISION: No login for 2 years** (simple to implement via last_login timestamp check)
4. **User data export format:** ✅ **DECISION: Both JSON and CSV** (JSON for machine-readable/migrations, CSV for human-readable/Excel)
5. **Scheduled status changes:** ✅ **DECISION: Separate scheduled_status_changes table** (clean separation, supports multiple scheduled changes per trail system)
6. **Trail system ownership:** ✅ **DECISION: One organization per trail system** (each trail system belongs to exactly one org, simplest data model)
7. **Status type scope:** ✅ **DECISION: Per organization** (all trail systems in an org share the same status types)
8. **Trail system subscriptions:** ✅ **DECISION: Subscribe to individual trail systems OR entire organization** (users can choose granularity)
9. **UI display:** ✅ **DECISION: Grouped by organization** (show "Hydrocut" with nested trail system: Hydrocut trail system)
10. **Status history visibility:** ✅ **DECISION: Show history publicly** (display "Hydrocut trail system was Open, changed to Closed on Jan 14 by Jane Doe")
11. **Scheduled changes:** ✅ **DECISION: Multiple concurrent scheduled changes** (full calendar of future statuses per trail system)

**iPhone Apps:**

1. **App Store deployment:** ✅ **DECISION: TestFlight beta only for MVP** (faster iteration, easier updates, no App Store review delays for pilot orgs)
2. **App naming:** ✅ **DECISION: "TrailLensHQ" and "TrailLensHQ Admin"** (clear differentiation, descriptive naming)
3. **Minimum iOS version:** ✅ **DECISION: iOS 15+** (supports passkeys/WebAuthn, covers 95%+ of devices)
4. **Deep linking:** ✅ **DECISION: Yes, deep link to trail system details** (tap notification → opens app to specific trail system page, better UX)
5. **Offline capability:** ✅ **DECISION: Cache trail system status + offline trail care report creation** (cache status for 7 days with staleness warning; allow full offline report creation with photos, local queueing, auto-upload when online, 7-day queue limit with warnings)

**Pilot Onboarding:**

1. **Historical trail system data:** ✅ **DECISION: Start fresh with current trail systems only** (clean slate, create 3 trail systems from scratch: Hydrocut trail system, Guelph Lake, Akell)
2. **User migration:** ✅ **DECISION: Hybrid approach** (invite/migrate key users like trail crew and admins, require new signups for general users)
3. **Onboarding support:** ✅ **DECISION: White-glove onboarding** (TrailLens staff sets up orgs, creates trail systems, configures status types, trains admins)
4. **Training:** ✅ **DECISION: Live training sessions + written documentation** (real-time training for onboarding, docs for reference)

**Performance Targets:**

1. **API response time target:** ✅ **DECISION: <500ms (p95)** (achievable without caching for 2 orgs, standard for serverless APIs)
2. **Notification latency target:** ✅ **DECISION: <2 minutes** (near real-time, feels instant to users, achievable with SNS/SES)
3. **Email delivery SLA:** ✅ **DECISION: 99%** (industry standard for transactional email, 1 in 100 may fail)
4. **Push notification delivery SLA:** ✅ **DECISION: 95% (APNS best-effort)** (track delivery rates but no guarantee given APNS limitations)
5. **iPhone app launch time:** ✅ **DECISION: <2 seconds cold start** (modern iOS standard, requires optimized networking and lazy loading)

**Security:**

1. **CloudTrail retention:** ✅ **DECISION: 1 year** (better for forensics and long-term compliance, industry standard)
2. **Secrets rotation frequency:** ✅ **DECISION: 180 days** (moderate rotation, balances security with operational overhead)
3. **Session timeout:** ✅ **DECISION: 1 hour** (balances security and UX, standard for web apps)
4. **Failed login lockout:** ✅ **DECISION: 5 attempts** (standard security, protects against brute force while allowing typo forgiveness)

---

## MVP Implementation Clarifications (January 16, 2026)

The following clarifications were provided by the CTO to resolve ambiguities in the MVP specification before implementation begins.

### Data Model Clarifications

**Status Model (Three-Tier Architecture):**

- **Status TYPE**: Template/definition created by organization (e.g., "Open", "Closed - Snow", "Caution - Icy Conditions")
  - Organizations create custom status types (max 30 per org)
  - Each status type has a name, optional default photo, optional season assignment, and optional tags
  - Status types can be pre-populated from templates for faster onboarding
- **Status UPDATE**: Applying a status type to a trail system at a specific point in time
  - Crew selects a status type and applies it to a trail system
  - Can override the default photo with current conditions photo
  - Must provide reason/notes explaining the change
  - Creates historical record
- **Tags**: Categorize status types for filtering and organization
  - Multiple tags per status type (e.g., ["Winter", "Weather-Related", "Caution"])
  - Used for sticky filtering in change status interface

**Status Photos (Two-Level System):**

- **Status type default photo**: Representative image for the status type definition (optional)
- **Status update photo**: Current conditions photo attached when applying status (optional, overrides default)
- Both photos stored in S3, status update photos retained in history for 2 years

**Trail System Management:**

- **Renaming**: Org-admins can rename trail systems. Historical records retain old name with timestamp.
- **Soft Delete (Archiving)**: Trail systems can be archived instead of hard-deleted. Archived systems hidden from public but visible in admin interface for potential restoration.
- **No transfers**: Trail systems cannot be transferred between organizations (out of scope for MVP)
- **Immutable ownership**: Each trail system belongs to exactly one organization

**Care Report Days Open Counter:**

- Starts at 0 on submission date
- Increments daily while status is: open, in-progress, deferred, or resolved
- Stops incrementing permanently when status changes to closed or cancelled
- Shows "days since submission" not "days in current status"

### Permission Clarifications

**Status Tags Management:**

- **Who can manage**: trailsystem-status role and above (trailsystem-status, trailsystem-crew, trailsystem-owner, org-admin, superadmin)
- **Operations**: Create, rename, delete tags; assign tags to status types
- **Limit**: Maximum 20 tags per organization

**Care Report Type Tags Management:**

- **Who can manage**: trailsystem-owner and above ONLY (trailsystem-owner, org-admin, superadmin)
- **Operations**: Create, rename, delete type tags
- **Who can assign**: Anyone submitting a report can assign existing type tags
- **Limit**: Maximum 25 type tags per organization
- **Rationale**: More restrictive than status tags for better tag governance

**Care Report Editing:**

- **Within 24 hours**: Submitters can edit title, description, and photos
- **After 24 hours**: Submitters lose edit access but can add comments to their own reports
- **Trail crew**: Can always edit all report fields, change status, add comments

### Phase 7.5 Condition Catalog Implementation Guidance

**Tag-reuse rationale:** The Condition Catalog reuses the existing `condition_tags` taxonomy (per-org, max 20). No new tag entity is introduced — the catalog references existing `condition_tag_ids` and denormalizes their names for read efficiency (mirrors the existing `condition_observation` pattern). Single source of truth for tag naming and color across catalog entries, observations, and trail-system condition history.

**Optimistic locking:** All catalog `PATCH` operations MUST use a `version` field on the `ConditionCatalogEntry` entity (matches the existing `condition_tag` and `trail_system` pattern). The DynamoDB `UpdateItem` call uses `ConditionExpression: #version = :expected_version` and increments `version` atomically. Concurrent edit collisions surface as `ConditionalCheckFailedException` and are returned to the client as HTTP 409 Conflict so the UI can prompt re-fetch.

**S3 key convention:** Catalog images live at `orgs/{org_id}/catalog/{catalog_id}.jpg` with WebP variants written by the existing `photo_processor` Lambda (mirrors the existing trail-photo flow exactly — no new S3 bucket, no new IAM policies, no new lifecycle rules). The original is at `.jpg`; the processor emits `{catalog_id}-thumb.webp`, `{catalog_id}-medium.webp`, `{catalog_id}-full.webp` in the same prefix.

**Presigned PUT via CloudFront OAC:** `POST /api/organizations/{org_id}/condition-catalog/upload-url` returns a presigned S3 PUT URL using the same CloudFront Origin Access Control pattern already in production for trail-system photos. The client PUTs directly to S3; no bytes traverse the api-dynamo Lambda. Reuses `s3_service.py` helpers verbatim.

**TransactWrite for "apply catalog → trail system + history + usage_count":** The `POST /api/trail-systems/{trail_system_id}/condition/apply-catalog/{catalog_id}` endpoint MUST execute a single DynamoDB `TransactWriteItems` call covering: (a) update the trail-system entity's denormalized `condition_type_id`, `condition_type_name`, `condition_color`, `condition_updated_at` fields; (b) `Put` a new condition-history item under `PK=TRAILSYSTEM#{ts_id}`; (c) `Update` the catalog entry's `usage_count` (`ADD usage_count :one`) and `last_used_at` fields. SNS publish to `TRAIL_CONDITION_CHANGE` happens AFTER the transaction commits. Atomic — either all four mutations succeed or none.

**`save_to_catalog: bool` flag on `PATCH /condition`:** When the existing `PATCH /api/trail-systems/{trail_system_id}/condition` request body carries `save_to_catalog: true` AND no `catalog_entry_id` is referenced, the server creates a new `ConditionCatalogEntry` from the same payload in the same TransactWrite (trail-system condition update + history APPEND + catalog PUT). When `false` or omitted, behavior is unchanged. Backwards-compatible — existing free-form `PATCH /condition` calls work without modification.

**Lambda performance targets:** All catalog routes MUST meet the platform-wide Python Lambda performance contract: P95 latency < 200ms, P99 latency < 500ms (per High-Performance Coding Standards). The catalog list endpoint stays single-partition (GSI1 with `ORG#{org_id}#CATALOG#ACTIVE` partition key) so it serves O(1) regardless of org size up to 100K DAU. Tag-filter intersection happens at the application layer (no per-tag adjacency item in MVP).

**Tag-cap validation (max 20):** The `tags_service.py` validation constant for `condition_tags` MUST enforce 20 server-side. `POST /api/organizations/{org_id}/condition-tags` returns HTTP 400 if the request would push the org's tag count over 20. The check is read-modify-write protected by either an `attribute_not_exists` ConditionExpression or a transactional read of the org's current tag count. Existing tests asserting the prior limit of 10 must be updated.

### Phase 9.6 Care Report `is_public` Field

The care-report request and response schemas in `openapi.json` MUST include `is_public: bool` (default `false`). The `CareReportEntity` in `traillens_db` adds the same field. Visibility-gating rule: when `is_public=true`, any authenticated user (not just org members) can list/get the care report; when `false`, only org members can. `GET /api/care-reports` query semantics: org members see all care reports for the org; non-org-members see only `is_public=true` care reports.

### Phase 9.10 Care Report Photo Cap (max 5)

Add `maxItems: 5` to both the photo upload request schema and the care-report response `photos` array in `openapi.json`. Server-side enforcement: `care_reports_service.py` MUST return HTTP 400 if a `POST /api/care-reports/{care_report_id}/photos` request would push the report's photo count over 5.

### Phase 10.5 Notification Preferences (2-axis matrix)

Notification preferences are a 2-axis matrix: channels (email / SMS / push) × event types. The `NotificationPreferences` schema in `openapi.json` becomes:

```text
{
  channels: { email: bool, sms: bool, push: bool },
  events: {
    condition_change:                { email, sms, push },
    care_report_created:             { email, sms, push },
    care_report_assigned:            { email, sms, push },
    care_report_comment:             { email, sms, push },
    scheduled_condition_reminder:    { email, sms, push },
    observation_received:            { email, sms, push }
  }
}
```

`notifications_service.py` is rewritten to evaluate the per-event-type per-channel matrix at dispatch time.

### Phase 11.4 Analytics Routes (8 new)

Add 8 new analytics routes under a new `analytics` tag. All return pre-aggregated data (never raw rows) backed by daily DynamoDB rollups (`ANALYTICS_ROLLUP#{org_id}#{metric}#{date}`). Routes accept `start_date`, `end_date` query params; bucketed routes accept `bucket=day|week|month`:

1. `GET /api/organizations/{org_id}/analytics/overview` — Org-Admin landing snapshot (`org-admin`+).
2. `GET /api/organizations/{org_id}/analytics/trail-systems` — status-change frequency, average time per condition, bucketed (`org-admin`+).
3. `GET /api/organizations/{org_id}/analytics/care-reports` — count by priority/status/type-tag, average resolution time, bucketed (`org-admin`+ for whole org; `trailsystem-crew` may filter).
4. `GET /api/organizations/{org_id}/analytics/users` — total / 30d-active / subscriptions / notification engagement (`org-admin`+).
5. `GET /api/organizations/{org_id}/analytics/activity-feed` — paginated org-wide timeline (any authenticated org member; rows filtered by membership).
6. `GET /api/organizations/{org_id}/analytics/export` — CSV export with `metric=` and date range; returns `text/csv` (`org-admin`+).
7. `GET /api/trail-systems/{ts_id}/analytics/condition-history` — per-trail-system timeline, bucketed (`trailsystem-owner`+).
8. `GET /api/trail-systems/{ts_id}/analytics/views` — per-trail-system view counts; depends on view-tracking middleware (`trailsystem-owner`+).

### Subscriptions Endpoints

Three new subscriptions endpoints under the existing `users` tag: `POST /api/users/me/subscriptions`, `GET /api/users/me/subscriptions`, `DELETE /api/users/me/subscriptions/{trailsystem_id}`. Existing `AP-SUB01–AP-SUB03` access patterns (`USER#{user_id}` + `SUBSCRIPTION#{trailsystem_id}`) already match the new route shape.

### Care Report Activity-Log Endpoint

`GET /api/care-reports/{id}/activity` is an aggregate-on-read endpoint: a single `Query(PK=CAREREPORT#{id})` reads the care-report core + comments + assignment-history + status-history items already co-located under that PK; the service merges them into a chronological feed. No new entity, no extra writes. New access pattern AP-CR14.

### URL Renames (Greenfield Breaking Changes)

Three URL renames land in the same `openapi.json` MAJOR version bump (1.1.3 → 2.0.0):

- `/api/devices` → `/api/users/me/devices` (and `/api/devices/{id}` → `/api/users/me/devices/{id}`)
- `/api/users/phone/verify`, `/api/users/phone/confirm` → `/api/users/me/phone/verify`, `/api/users/me/phone/confirm`
- `/api/organizations/{org_id}/tags/condition` → `/api/organizations/{org_id}/condition-tags`

Greenfield (zero production users) permits breaking URL changes; both REST client libs (`webui/packages/jsrestapi`, `androidrestapi`) regenerate from `openapi.json` so they pick up new paths automatically.

### Backup Password Authentication (Cognito SRP)

Email + password is a **backup** auth path alongside passkey and magic-link. Wire protocol: Cognito `USER_SRP_AUTH` (Secure Remote Password). Password is never sent in plaintext. **No** account creation via password (Cognito `allow_admin_create_user_only=True` already configured). **No** forgot-password endpoint in `api-dynamo` (deferred to webui Phase 11). Mobile apps (androiduser, androidadmin) expose the username+password login screen **only in DEBUG builds** (`BuildConfig.DEBUG`).

### Background-Worker Lambdas (2 new)

Two new Lambda deployment packages with EventBridge schedules:

- **`scheduled_condition_processor`** (Architecture A) — `cron(0/15 * * * ? *)` every 15 minutes; 256 MB memory; 60s timeout; ARM64. Handles both fire-due-scheduled-conditions and pre-fire reminder dispatch. New DynamoDB GSI4 (`GSI4PK = SCHEDULED#{status}`).
- **`retention_cleanup_processor`** (Architecture B) — `cron(0 3 * * ? *)` daily at 03:00 UTC; 512 MB memory; 900s timeout; ARM64. Closed care reports (>90d), deleted-account PII scrub (>30d), S3 photo orphan sweep, magic-link belt-and-suspenders. Adds new audit entities: `CareReportDeletionAudit`, `PIIDeletionAudit`.

Pulumi ComponentResource `EventBridgeScheduledLambda` (in `infra/`) provisions the EventBridge rule + target + IAM role + CloudWatch log group (30-day retention) for each. CloudWatch alarms recalibrated for the 15-min interval (1 invocation per 15-min window).

### Cognito Threat Protection Enablement

Upgrade Cognito `user_pool_tier` from `ESSENTIALS` to `PLUS` and add `user_pool_add_ons=aws.cognito.UserPoolUserPoolAddOnsArgs(advanced_security_mode="AUDIT")` initially (then `ENFORCED` after 2-week soak). Caveat: Cognito's compromised-credentials check only runs on `USER_PASSWORD_AUTH`, not on `USER_SRP_AUTH` — adaptive auth (risk scoring) still applies to both. AWS WAF rules on the Cognito endpoint and API Gateway are the correct path for volumetric/brute-force protection (separate infra task).

### Privacy-First TrailPulse Ride Tracking

The backend stores **only** anonymous per-trail-system aggregates — no per-user ride records. Two ride-tracking entities, both co-located under `PK=TRAILSYSTEM#{ts_id}`:

- `TrailSystemRideCount` (anonymous daily aggregate): `SK=RIDECOUNT#{YYYY-MM-DD}`, `total_rides` atomic counter, TTL 3 years (1095 days).
- `RideCompletion` (anonymous idempotency marker): `SK=RIDECOMPLETION#{ride_id}`, `completed_at` only (no `user_id`), TTL 30 days.

`PUT /api/trailpulse/trail-systems/{trail_system_id}/ride-completion` body `{ ride_id, completed_at }` does a single-partition TransactWrite: (a) `Put RIDECOMPLETION#{ride_id}` with `attribute_not_exists(SK)` for idempotency, (b) `Update RIDECOUNT#{today}` with `ADD total_rides :one`. Per-user "you've ridden here N times" UX is mobile-local Room DB only — backend never sees per-user ride history. Unique-users-per-day, if needed, derives from `FeedbackResponses.user_id` (which IS user-attributed by Task 15.5/15.9 design).

### Security Implementation Details

**CloudTrail Configuration:**

- **Retention**: 1 year (not 90 days as listed in Section 6.1)
- **Logs to**: Dedicated S3 bucket
- **Tracks**: All API calls to DynamoDB, S3, Cognito, Secrets Manager
- **Cost**: ~$2-5/month

**Secrets Rotation:**

- **Frequency**: 180 days (not 90 days as listed in Section 6.1)
- **Scope**: All secrets in AWS Secrets Manager
- **Automation**: AWS Secrets Manager automatic rotation enabled

**MFA Enforcement:**

- **Timing**: 7-day grace period after first login for admin roles (org-admin, trailsystem-owner, superadmin)
- **Reminders**: Daily email reminders during grace period
- **Enforcement**: After 7 days, account access restricted until MFA enabled
- **Rationale**: Allows admin exploration without friction while maintaining security

**Passkey Implementation:**

- **Primary approach**: Research AWS Cognito passkey support (as of January 2026)
- **If supported**: Use native Cognito passkey features
- **If not supported**: Build custom WebAuthn/FIDO2 integration while using Cognito for user directory
- **Fallback**: Magic link and email/password always available regardless of passkey implementation

### Subscription Model

**MVP Subscription Tiers:**

- **Free tier only**: All users get 5 trail system subscriptions
- **No Pro tier**: Unlimited subscriptions and payment processing deferred to post-MVP
- **Rationale**: Pilot orgs have only 4 trail systems total, so 5 free subscriptions is sufficient

### Notification and Communication

**Bulk Status Updates:**

- **Scope**: Update multiple trail systems to same status simultaneously
- **Reason**: Single reason applies to all trail systems in bulk update
- **Photo**: Single photo applies to all trail systems in bulk update
- **Rationale**: Simpler implementation and UI. Admins can do individual updates if customization needed.

**Seasonal Status Behavior:**

- **No auto-revert**: Status persists until manually changed, even when season ends
- **Rationale**: Prevents unexpected automated changes that could inappropriately open trails
- **Season assignment**: Informational only, helps predict future closures but does not trigger automated actions

### iPhone App Details

**TestFlight Distribution (MVP):**

- **Phased rollout approach**:
  1. Phase 1: Invite admins and trail crew (5-10 people per org)
  2. Phase 2: Expand to active community members (50-100 per org)
  3. Phase 3: Open to all pilot org users
- **Rationale**: Controlled growth, allows bug fixes before full rollout
- **Limit**: Well under 10K TestFlight user limit (pilot orgs ~1500 users total)

**Offline Mode:**

- **Trail system status**: Cached for up to 7 days with staleness warning
- **Care reports - Creation**: Full offline support with local queueing
  - Users can create reports offline with title, description, and photos (up to 5)
  - Reports stored locally and auto-upload when connection restored
  - Photos stored on device, uploaded with report
  - Pending reports shown with badge/icon and in dedicated "Pending Sync" section
  - Users can edit or delete pending reports before sync
  - 7-day queue limit with warning after 48 hours offline
  - Auto-retry with exponential backoff (30s, 2min, 10min), then manual retry
- **Care reports - Viewing**: NO offline support (requires online connection to fetch)
- **Rationale**: Status viewing is read-only and cacheable. Report creation is write-only and can queue locally. Report viewing requires real-time data and is too complex for offline caching.

**App Naming:**

- **User app**: "TrailLensHQ" (status viewing, subscriptions, submit care reports)
- **Admin app**: "TrailLensHQ Admin" (trail system management, full care report CRUD)

### Data Export and Retention

**User Data Export API:**

- **Formats**: Both JSON (machine-readable) and CSV (human-readable)
- **PII included**: Name, email, phone, notification preferences, profile photo, account creation date, last login
- **Activity included**: Trail system subscriptions, care reports submitted, comments on reports, notification history (last 30 days)
- **Access**: Users trigger export via dashboard UI, download link sent via email

**Data Retention Consistency:**

- **User data**: 2 years after account becomes inactive (no login for 2 years)
- **Status history**: 2 years after status change
- **Care reports**: Status-based retention (open/in-progress/deferred/resolved kept indefinitely, closed/cancelled deleted after 2 years)
- **Care report photos**: 180 days after report closed/cancelled
- **CloudTrail logs**: 1 year retention

---

## Instructions for AI Assistant

**CRITICAL CONTEXT**: This TODO list is for **documentation updates and project planning**, NOT for implementing MVP features directly. The actual implementation will be documented in a separate project plan.

**IMPORTANT**:

- [ ] Create a TODO list for this task - DO NOT implement any changes yet
- [ ] Save the TODO list as a markdown file in `docs` directory (e.g., `docs/mvp-implementation-todo.md`)
- [ ] The TODO should break down the work into very detailed, logical, trackable steps
- [ ] Each TODO item should have a clear description and acceptance criteria
- [ ] Wait for confirmation before proceeding with implementation
- [ ] Follow Constitution standards (see `.github/CONSTITUTION.md`)
- [ ] Any unknowns should be asked as questions rather than making assumptions, but recommendations should be made for each recommendation

**What the TODO List Will Accomplish**:

1. **Update existing documentation files** in `docs/` directory with MVP changes:
   - `PRODUCT_OVERVIEW_FOR_CEO.md` - Update product overview to reflect MVP scope and features
   - `SYSTEM_ARCHITECTURE.md` - Update architecture to reflect MVP technical decisions
   - `SECURITY_REPORT_FOR_CEO.md` - Update security requirements based on MVP clarifications
   - `MARKETING_PLAN.md` - Update marking plan based on MVP clarifications
   - For each file:
     - Back up current version with revision suffix (e.g., `PRODUCT_OVERVIEW_FOR_CEO_v1.md`)
     - Create new version incorporating MVP changes from this document
     - Update version numbers and revision history in each file
     - Reference the original prompt in each file for content

2. **Create a new project plan document** based on this prompt from the Chief Development Manager:

   > "As the chief development manager and project manager, I want to document the implementation plan for all features in the MVP document taking into account the codebase that already exists and the documents from others in the senior team. I want to document each phase of the set of changes and the tasks involved. Document the updates and new feature changes as detailed as possible so my development staff can create working code. Keep in mind, we are using AI assistance, so timelines will be shorter."

   - Create `docs/MVP_PROJECT_PLAN.md`
   - Reference the 14 recommended phases below as a starting point
   - Account for existing codebase (exploratory prototype in `api-dynamo/`, `web/`, `infra/`)
   - Detail each task with enough specificity for developers with AI assistance
   - Include dependencies, critical path, and acceptance criteria
   - Shorter timelines due to AI-assisted development

**Process**:

1. **Read and understand all requirements above**
   - Review all referenced documentation (PRODUCT_OVERVIEW_FOR_CEO, SYSTEM_ARCHITECTURE, SECURITY_REPORT, MARKETING_PLAN)
   - Understand the difference between MVP scope and full product vision
   - Note critical security gaps that MUST be addressed
   - Review existing codebase to understand what exists vs. what needs to be built

2. **Ask clarifying questions** if needed
   - Documentation backup strategy
   - Project plan format preferences
   - Level of detail required for tasks

3. **Create a comprehensive TODO list** using the TodoWrite tool with two main sections:

   **Section A: Documentation Updates**
   - Back up and update PRODUCT_OVERVIEW_FOR_CEO.md
   - Back up and update SYSTEM_ARCHITECTURE.md
   - Back up and update SECURITY_REPORT_FOR_CEO.md
   - Update MARKETING_PLAN.md if needed

   **Section B: Project Plan Creation**
   - Create MVP_PROJECT_PLAN.md based on chief development manager's requirements
   - Use the 14 recommended phases below as foundation
   - Detail tasks for each phase accounting for existing codebase
   - Include dependencies, acceptance criteria, and AI-assisted timeline estimates

   **IMPORTANT:** The phases below are RECOMMENDATIONS based on logical implementation order. The exact phases, dependencies, and sequencing will require thorough review of all referenced documentation (PRODUCT_OVERVIEW_FOR_CEO.md, SYSTEM_ARCHITECTURE.md, SECURITY_REPORT_FOR_CEO.md, MARKETING_PLAN.md) and existing codebase before finalizing the project plan.

   **Recommended Implementation Phases** (for project plan reference):

   - **Phase 1:** Brand messaging (update website and marketing materials with "Building communities, one trail at a time" byline)
   - **Phase 2:** Security hardening (CloudTrail, WAF, secrets rotation, incident response plan; Security Hub and GuardDuty moved to post-MVP)
   - **Phase 3:** Authentication system (passkey via Cognito or WebAuthn, magic link, email/password - ALL THREE required)
   - **Phase 4:** PII protection (data retention policies, user data export feature, account deletion feature, MFA enforcement for admins with 7-day grace period)
   - **Phase 5:** Trail system data model (trail systems table, attributes, relationships to organizations, cover photos, metadata)
   - **Phase 6:** Tag-based status organization (condition tags max 20 per org, CRUD operations, sticky filtering, permissions: trailsystem-status+)
   - **Phase 7:** Status management (status types max 30 per org, status updates with photos, two-level photo system, seasons, history with 2-year retention, bulk updates, templates)
   - **Phase 8:** Scheduled status changes (separate scheduled_status_changes table, cron job automation, reminder notifications before changes)
   - **Phase 9:** Trail Care Reports system (P1-P5 priority, public/private visibility flag, type tags max 25 per org, assignment workflow, comments, activity log, multiple photos up to 5, status-based retention, integration with trail system status)
   - **Phase 10:** Notification system (email via SES, SMS via Pinpoint, push notifications via SNS→APNS for iPhone apps, subscriptions to individual trail systems or entire organizations)
   - **Phase 11:** Web dashboards (role-specific interfaces for all 8 roles, trail system CRUD, care report management, analytics, bulk operations)
   - **Phase 12:** iPhone apps (User app: view trail systems + submit/view care reports + offline report creation; Admin app: manage trail systems + full care report CRUD + work logs; iOS 15+, TestFlight distribution, offline status caching 7 days, deep linking)
   - **Phase 13:** Pilot onboarding (Hydrocut with 1 trail system including Glasgow and Synders areas, GORBA with Guelph Lake + Akell trail systems, white-glove setup, live training)
   - **Phase 14:** Testing and validation (end-to-end testing, security testing, performance testing, user acceptance testing with pilot orgs)

4. **Reference the prompt-to-todo-prompt.md format** (`.github/prompts/prompt-to-todo-prompt.md`)

5. **Save the TODO list** to `docs/mvp-implementation-todo.md`

6. **Present the TODO list for review**
   - Section A: Documentation update tasks
   - Section B: Project plan creation tasks
   - Highlight critical path items
   - Identify dependencies between tasks
   - Estimate relative complexity (T-shirt sizes: S, M, L, XL)

7. **Wait for explicit approval** before making any changes

8. **Execute TODO items one at a time**, marking each complete as you go
   - Commit frequently with clear messages
   - Review changes with CTO before proceeding
   - Update TODO list status as work progresses

---

## Success Criteria

**Documentation Update Success Criteria:**

- [ ] TODO list created and saved to `docs/mvp-implementation-todo.md`
- [ ] TODO list has Section A (Documentation Updates) and Section B (Project Plan Creation)
- [ ] Backup strategy defined for existing documentation files (PRODUCT_OVERVIEW_FOR_CEO.md, SYSTEM_ARCHITECTURE.md, SECURITY_REPORT_FOR_CEO.md)
- [ ] Plan for updating each documentation file to reflect MVP v1.11 changes
- [ ] No documentation changes made until TODO list approved by CTO

**Project Plan Success Criteria:**

- [ ] Project plan creation tasks defined in TODO list Section B
- [ ] Project plan will be saved as `docs/MVP_PROJECT_PLAN.md`
- [ ] Project plan will reference the 14 recommended implementation phases
- [ ] Project plan will account for existing codebase in api-dynamo/, web/, infra/
- [ ] Project plan will detail tasks with enough specificity for AI-assisted development
- [ ] Project plan will include dependencies, critical path, and acceptance criteria
- [ ] Project plan will include AI-assisted timeline estimates (shorter than traditional)

**MVP Requirements Captured:**

- [ ] All requirements understood (trail systems model, trail care reports, iPhone apps, all 8 roles, all auth methods)
- [ ] All MVP security gaps identified (CloudTrail, WAF, secrets rotation, incident response, MFA; Security Hub and GuardDuty moved to post-MVP)
- [ ] Trail system data model clearly defined (vs individual trails - OUT OF SCOPE)
- [ ] Trail Care Reports system included (P1-P5 priority, public/private, type tags max 25, assignment, comments, offline creation)
- [ ] Tag-based status organization included (condition tags max 20, care report type tags max 25, separate permission models)
- [ ] 3 pilot trail systems identified (Hydrocut trail system with Glasgow and Synders areas, Guelph Lake, Akell)
- [ ] Subscription model clarified (trail systems + organizations, free tier only for MVP)
- [ ] iPhone app requirements clearly defined (2 apps: User app with care reports + offline creation, Admin app with full care report CRUD + work logs)
- [ ] Brand messaging update included (website and marketing materials with "Building communities, one trail at a time" byline)
- [ ] All 14 implementation phases documented with disclaimer about requiring documentation review

---

## Revision History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-01-15 | CTO + Claude Code | Initial MVP prompt based on CTO vision and documentation analysis |
| 1.1 | 2026-01-15 | CTO + Claude Code | Updated per CTO feedback: DPA deferred, all 8 roles kept, auth required, suggested items now required, iPhone apps required, admin apps unified, questions expanded |
| 1.2 | 2026-01-15 | CTO + Claude Code | All 36 implementation questions answered by CTO. Key decisions: iOS 15+, TestFlight only, AWS Pinpoint, daily digest removed, 2-year retention, white-glove onboarding |
| 1.3 | 2026-01-15 | CTO + Claude Code | CRITICAL DATA MODEL CHANGE: Replaced "trails" with "trail systems" throughout. MVP manages trail systems (Hydrocut trail system, Guelph Lake, Akell), NOT individual trails. Added trail system attributes, subscription model, 11 new data model decisions. 11 implementation phases (was 9). |
| 1.4 | 2026-01-16 | CTO + Claude Code | MAJOR ARCHITECTURAL CHANGE: Replaced fixed Status Type Groups (sections 1.2-1.3) with flexible tag-based system. Tags are per-organization, max 10 per org, multiple tags per status, managed by anyone with status access. Includes sticky tag filtering for change status interface. Enables custom organizational schemes vs. rigid 5-group structure. |
| 1.5 | 2026-01-16 | CTO + Claude Code | NEW FEATURE: Added comprehensive Trail Care Reports system (Section 2) - unified issue tracking replacing work logs and problem reports. Features: P1-P5 priority, public/private visibility flag, type tags (max 25 per org, org-admin only), flexible assignment, comments, activity log, multiple photos (up to 5), optional submitter notifications. Renumbered sections 3-7 (was 2-6). |
| 1.6 | 2026-01-16 | CTO + Claude Code | TRAIL CARE REPORTS ENHANCEMENT: Added retention policy (Section 2.10) - status-based retention with open/in-progress/deferred/resolved reports kept indefinitely, closed/cancelled deleted after 2 years, photos deleted 180 days after closure. Updated iPhone apps (Section 7) with full care report support: User app can view/submit reports with camera integration, Admin app has full CRUD, comments, assignment, and quick work log creation. Updated user stories with trail care report workflows. |
| 1.7 | 2026-01-16 | CTO + Claude Code | AMBIGUITY RESOLUTION: Added comprehensive "MVP Implementation Clarifications" section documenting 16 CTO decisions via AskUserQuestion tool. Clarified: Status model (types vs updates vs tags), permission model (status tags: trailsystem-status+, care report tags: trailsystem-owner+), security config (CloudTrail 1yr, secrets 180d), MFA timing (7-day grace), passkey implementation (research Cognito first), subscription model (free tier only), bulk updates (same reason/photo), seasonal behavior (no auto-revert), TestFlight rollout (phased), offline mode (7-day cache), data export (JSON+CSV with PII+activity), trail system management (rename+archive), care report editing (24hr window), days open counter (submission to close). Fixed line 740: traillens-admin \u2192 superadmin. |
| 1.8 | 2026-01-16 | CTO + Claude Code | WORDING CLARIFICATION: Updated GDPR requirements (lines 1164-1165) from technical "Create API" language to user-facing feature language. Changed "Create user data export API" to "Implement user data export feature" and "Create user data deletion API" to "Implement account deletion feature" to emphasize UI-accessible features per GDPR requirements, not technical REST endpoints requiring programming knowledge. |
| 1.9 | 2026-01-17 | CTO + Claude Code | OFFLINE TRAIL CARE REPORTS: Added full offline support for creating trail care reports. Users can now create reports offline with photos (up to 5), stored locally and auto-uploaded when connection restored. Features: pending badge/icon on reports, dedicated "Pending Sync" section, edit/delete pending reports before sync, 7-day queue with warnings after 48 hours, auto-retry with exponential backoff (30s, 2min, 10min) then manual. Updated offline mode clarifications section and iPhone app decision. Report viewing still requires online connection. |
| 1.10 | 2026-01-17 | CTO + Claude Code | BRAND MESSAGING IN MVP: Moved brand messaging update from post-MVP marketing to required MVP features. Added requirement to update website and marketing materials with "Building communities, one trail at a time" byline. Low-hanging fruit that improves brand consistency from launch. |
| 1.11 | 2026-01-17 | CTO + Claude Code | PHASE LIST UPDATE: Comprehensive review and update of implementation phases (lines 1484-1503) to reflect all MVP changes through v1.10. Updated from 11 to 14 phases to include: Trail Care Reports system (Phase 8), separated tag-based status organization from status management (Phases 5-6), expanded iPhone apps to include offline report creation and care report features (Phase 11), added brand messaging phase (Phase 12). Added disclaimer that phases are recommendations requiring documentation review. Updated Success Criteria to reflect 14 phases and new features (care reports, tag systems, offline creation). Key changes: Phase 5 now tag-based (not fixed groups), Phase 8 is new Trail Care Reports system, Phase 11 includes offline report creation from v1.9, Phase 12 is brand messaging from v1.10. |
| 1.12 | 2026-01-17 | CTO + Claude Code | INSTRUCTIONS CLARIFICATION: Rewrote "Instructions for AI Assistant" section (lines 1459-1557) to clarify TODO list purpose and scope. **CRITICAL CHANGE**: TODO list is for documentation updates and project plan creation, NOT direct MVP implementation. Added "What the TODO List Will Accomplish" section detailing: (1) Backup and update existing documentation files (PRODUCT_OVERVIEW_FOR_CEO.md, SYSTEM_ARCHITECTURE.md, SECURITY_REPORT_FOR_CEO.md) with revision suffixes, (2) Create new MVP_PROJECT_PLAN.md based on Chief Development Manager's prompt accounting for existing codebase and AI-assisted development timelines. Updated process to include two TODO sections: Section A (Documentation Updates) and Section B (Project Plan Creation). Reorganized Success Criteria into three categories: Documentation Update, Project Plan, and MVP Requirements. Added requirement to review existing codebase in api-dynamo/, web/, infra/ before planning. |
| 1.13 | 2026-01-17 | CTO + Claude Code | PHASE REORDERING: Moved brand messaging from Phase 12 to Phase 1 per CTO request. **RATIONALE**: Brand messaging is low-hanging fruit and should be the first priority. Renumbered all subsequent phases: Security hardening (Phase 2), Authentication (Phase 3), PII protection (Phase 4), Trail system data model (Phase 5), Tag-based status (Phase 6), Status management (Phase 7), Scheduled changes (Phase 8), Trail Care Reports (Phase 9), Notifications (Phase 10), Web dashboards (Phase 11), iPhone apps (Phase 12), Pilot onboarding (Phase 13), Testing (Phase 14). Added PROMPT 12 to prompt history documenting the phase reordering request. |

---

**Prepared by:** CTO + Claude Code AI Assistant
**Last Updated:** 2026-01-17
**Status:** Ready for Documentation Updates and Project Planning
