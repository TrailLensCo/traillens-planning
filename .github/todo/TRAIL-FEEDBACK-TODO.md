# TrailPulse Feature Documentation TODO

## Task Overview

Add TrailPulse trail feedback and usage tracking feature to MVP documentation. This is a **DOCUMENTATION ONLY** task - no backend implementation, no infrastructure deployment, no database creation.

**Scope:** Three files only:
1. `planning/docs/MVP_IMPLEMENTATION_PROMPT.md` - Add TrailPulse feature section
2. `planning/docs/MVP_PROJECT_PLAN.md` - Add TrailPulse to project plan
3. `web/src/data/features.js` - Add TrailPulse feature entry to website

**Source Material:** `planning/.github/prompts/trail-feedback-prompt.md`

---

## TODO Items

### 1. Update MVP_IMPLEMENTATION_PROMPT.md with TrailPulse Feature Section

**File:** `planning/docs/MVP_IMPLEMENTATION_PROMPT.md`

**Task Description:**
Add a comprehensive TrailPulse feature section to the MVP implementation prompt document. This section should follow the existing structure and formatting of the document.

**Detailed Steps:**

1. **Read the existing MVP_IMPLEMENTATION_PROMPT.md file completely** to understand:
   - Document structure and formatting patterns
   - Section numbering scheme
   - Writing style and tone
   - How other features are documented
   - Location where new feature should be inserted (likely after existing feature sections)

2. **Create TrailPulse feature section** with the following subsections:
   - **Feature Overview**: Brief introduction to TrailPulse (2-3 paragraphs)
     - What it does: Trail feedback and usage tracking via GPS
     - Why it matters: Software-based trail counting, rider feedback for trail conditions
     - Key benefit: Privacy-first, subscription-based tracking

   - **1. Mobile App - GPS Tracking and Ride Detection** (Reference: R1.1-R1.4 from prompt)
     - Location tracking within subscribed trail systems only
     - Geofencing for entry/exit detection
     - Privacy controls and opt-out settings
     - Ride event recording (start/end timestamps)

   - **2. Post-Ride Feedback Collection** (Reference: R2.1-R2.3 from prompt)
     - Push notification triggers
     - Trail condition reporting options
     - Additional custom questions
     - Frequency-based question logic
     - Free-text comment field

   - **3. Trail System Owner Configuration** (Reference: R3.1-R3.3 from prompt)
     - Trail condition customization
     - Additional question management (CRUD operations)
     - Notification customization

   - **4. Feedback Data Management Interface** (Reference: R4.1-R4.6 from prompt)
     - Feedback data viewing (table/list format with pagination)
     - Search and filter capabilities (date, condition, user, text search)
     - Feedback management (delete, bulk delete, soft delete)
     - User feedback statistics and crew member identification
     - Data usage for trail condition management
     - Crew member management system

   - **5. Trail System Geofence Management** (Reference: Section 5 from prompt)
     - Geofence data model (GeoJSON format)
     - Admin interface for geofence definition
     - API for geofence data retrieval
     - Geofence validation logic

   - **6. Usage Counting System** (Reference: Section 6 from prompt)
     - Trail usage metrics (ride counts per trail system)
     - Count accuracy requirements
     - Usage analytics display

   - **7. Data Model** (Reference: R5.1-R5.2 from prompt)
     - Database schema tables:
       - TrailConditions
       - AdditionalQuestions
       - RideEvents (with 90-day TTL)
       - FeedbackResponses (with soft delete support)
       - UsageCounts
       - UserPreferences
       - QuestionResponseTracker
       - TrailSystemGeofences
       - CrewMembers
       - FeedbackDeletionAudit
     - Data retention policies

   - **8. Push Notification Integration** (Reference: R6.1-R6.3 from prompt)
     - SNS mobile integration
     - Notification triggers
     - Notification content and deeplink format

   - **9. API Endpoints** (Reference: R7.1-R7.4 from prompt)
     - Mobile app endpoints (8 endpoints listed)
     - Web endpoints (2 endpoints)
     - Admin configuration endpoints (8 endpoints)
     - Admin feedback management endpoints (10 endpoints)

   - **10. Integration Points**
     - Existing systems (Cognito, SNS, DynamoDB)
     - New infrastructure needed
     - Backend-mobile integration flow

   - **11. MVP Scope**
     - Must Have features for this repo (backend & web)
     - Must Have features for mobile team
     - Should Have (post-MVP)
     - Nice to Have (future)

3. **Format the section** following document conventions:
   - Use consistent heading levels (likely ### or #### based on document structure)
   - Use bullet points for lists
   - Use code formatting for API endpoints and technical terms
   - Include notes about mobile team separation where relevant

4. **Insert the section** in the appropriate location:
   - Likely after existing feature sections
   - Before any implementation timeline or dependency sections
   - Maintain document flow and logical organization

**Acceptance Criteria:**
- [ ] TrailPulse section added to MVP_IMPLEMENTATION_PROMPT.md
- [ ] All 11 subsections included with complete content
- [ ] Section follows existing document formatting and style
- [ ] All requirements from trail-feedback-prompt.md are documented
- [ ] API endpoints documented with proper formatting
- [ ] Database schema tables documented
- [ ] Integration points clearly described
- [ ] Mobile team vs. backend team responsibilities clarified
- [ ] MVP scope clearly defined
- [ ] No implementation details added - documentation only
- [ ] Document structure and numbering maintained
- [ ] Copyright header preserved (if present)

**Dependencies:**
- Must read existing MVP_IMPLEMENTATION_PROMPT.md structure first
- Must reference trail-feedback-prompt.md for complete requirements

**Estimated Complexity:** High (comprehensive documentation with multiple subsections)

---

### 2. Update MVP_PROJECT_PLAN.md with TrailPulse Implementation Phase

**File:** `planning/docs/MVP_PROJECT_PLAN.md`

**Task Description:**
Add TrailPulse as a new implementation phase in the MVP project plan with timeline, tasks, dependencies, and success criteria.

**Detailed Steps:**

1. **Read the existing MVP_PROJECT_PLAN.md file completely** to understand:
   - Current phase numbering (appears to be 14 phases from TOC)
   - Phase structure and formatting
   - How tasks are numbered within phases
   - Timeline estimation approach
   - Dependency notation format
   - Success criteria format
   - Risk assessment format (if present)

2. **Determine TrailPulse phase number:**
   - Count existing phases in the document
   - TrailPulse should be added as a new phase (likely Phase 15 or insert earlier if logical)
   - Consider logical placement: After authentication/PII phases, before or alongside mobile app phase

3. **Create TrailPulse implementation phase** with the following structure:

   **Phase Header:**
   - Phase number and title: "Phase X: TrailPulse - Trail Feedback and Usage Tracking"
   - Brief description (1-2 sentences)
   - Timeline estimate (suggest 10-15 days for backend/web, separate mobile timeline)
   - Dependencies on other phases

   **Phase Overview:**
   - Feature description and business value
   - Key components (backend API, web interface, mobile integration)
   - Separation of responsibilities (this repo vs. mobile team)

   **Tasks by Component:**

   **Backend API Tasks (api-dynamo/):**
   - Task X.1: Implement TrailPulse DynamoDB schema
     - Create tables: RideEvents, FeedbackResponses, UsageCounts, TrailSystemGeofences, CrewMembers, etc.
     - Configure TTL for RideEvents (90 days)
     - Set up GSI indexes for querying
   - Task X.2: Implement mobile app API endpoints
     - POST /api/trailpulse/rides/start
     - POST /api/trailpulse/rides/end
     - GET /api/trailpulse/geofences
     - GET /api/trailpulse/trail-systems/{id}/feedback-config
     - POST /api/trailpulse/feedback
     - GET /api/trailpulse/user/ride-count/{trail_system_id}
     - PUT /api/trailpulse/user/preferences
     - POST /api/trailpulse/device-token
   - Task X.3: Implement web feedback endpoints
     - GET /api/trailpulse/trail-systems/subscribed
     - POST /api/trailpulse/feedback/web
   - Task X.4: Implement admin configuration endpoints (8 endpoints)
   - Task X.5: Implement admin feedback management endpoints (10 endpoints)
   - Task X.6: Implement ride detection and validation logic
   - Task X.7: Implement usage counting aggregation
   - Task X.8: Implement SNS push notification triggers

   **Infrastructure Tasks (infra/):**
   - Task X.9: Deploy TrailPulse DynamoDB tables via Pulumi
   - Task X.10: Configure SNS topics for mobile push notifications
   - Task X.11: Add API Gateway endpoints for TrailPulse APIs
   - Task X.12: Configure Lambda functions for TrailPulse handlers
   - Task X.13: Set up DynamoDB TTL for ride event expiration

   **Web Interface Tasks (web/):**
   - Task X.14: Build web feedback submission form
   - Task X.15: Build admin TrailPulse configuration interface
     - Trail condition management (CRUD)
     - Additional question management (CRUD)
     - Notification settings
   - Task X.16: Build admin feedback data management interface
     - Feedback viewing with pagination
     - Search and filter UI
     - Delete/bulk delete functionality
     - Crew member management UI
     - Feedback statistics display
   - Task X.17: Build geofence management interface
     - Map-based geofence editor or coordinate input
     - Geofence preview and validation
   - Task X.18: Build usage analytics dashboard
     - Display ride counts and trends
     - Export functionality
   - Task X.19: Update features.js with TrailPulse entry

   **Testing Tasks:**
   - Task X.20: Test ride detection API with geofence validation
   - Task X.21: Test feedback submission and retrieval
   - Task X.22: Test admin configuration and data management
   - Task X.23: Test SNS notification delivery
   - Task X.24: Test usage count accuracy
   - Task X.25: Test data retention (TTL, soft delete)

4. **Add Dependencies section:**
   - Depends on Phase 3 (Authentication) - needs Cognito integration
   - Depends on Phase 5 (Trail System Data Model) - needs trail system boundaries
   - Depends on SNS infrastructure from earlier phases
   - Mobile team coordination required (separate timeline)

5. **Add Success Criteria:**
   - All backend API endpoints implemented and tested
   - DynamoDB schema deployed with proper indexes and TTL
   - Web feedback form functional with authentication
   - Admin configuration interface complete
   - Admin feedback management interface complete
   - Geofence boundaries can be defined and managed
   - Push notifications triggered correctly on ride end
   - Usage counts accurate and aggregated
   - Integration tested with mobile team APIs
   - Documentation complete

6. **Add Risk Assessment (if document includes this):**
   - Risk: Mobile team coordination delays
     - Mitigation: Backend APIs ready early, mock mobile integration for testing
   - Risk: Geofence accuracy issues
     - Mitigation: Proper validation logic, coordinate with mobile team on GPS accuracy
   - Risk: SNS push notification delivery failures
     - Mitigation: Graceful handling, logging, retry logic
   - Risk: Data privacy concerns with GPS tracking
     - Mitigation: Privacy-first design, opt-out available, clear consent

7. **Update Table of Contents:**
   - Add new phase to TOC with proper numbering
   - Update section references if needed

8. **Update Executive Summary (if needed):**
   - Add TrailPulse to list of features if summary includes feature list
   - Update phase count (14 → 15 or whatever new total is)

**Acceptance Criteria:**
- [ ] TrailPulse phase added to MVP_PROJECT_PLAN.md
- [ ] Phase number and title follow document conventions
- [ ] All tasks numbered and described clearly (suggest 20-25 tasks)
- [ ] Tasks organized by component (backend, infra, web, testing)
- [ ] Timeline estimate provided
- [ ] Dependencies on other phases documented
- [ ] Success criteria listed
- [ ] Risk assessment included (if document has this section)
- [ ] Table of Contents updated with new phase
- [ ] Executive Summary updated if needed
- [ ] Document formatting and style maintained
- [ ] No breaking changes to existing phase numbering if possible
- [ ] Copyright header preserved (if present)

**Dependencies:**
- Must read existing MVP_PROJECT_PLAN.md structure first
- Must reference trail-feedback-prompt.md for task breakdown
- Should align with TODO item #1 (implementation prompt)

**Estimated Complexity:** High (comprehensive phase with 20+ tasks)

---

### 3. Update web/src/data/features.js with TrailPulse Feature Entry

**File:** `web/src/data/features.js` (in web submodule)

**Task Description:**
Add TrailPulse feature object to the features array and create new "trail-engagement" category in the feature categories array.

**Detailed Steps:**

1. **Read the existing web/src/data/features.js file** to verify:
   - Current structure and formatting
   - Existing feature IDs (should be 1-7, so TrailPulse will be ID 8)
   - Copyright header format
   - Code style conventions
   - featureCategories array structure

2. **Add TrailPulse feature object** to the features array:
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

3. **Add new category** to featureCategories array:
   ```javascript
   { id: 'trail-engagement', name: 'Trail Engagement' }
   ```
   - Insert in logical order (alphabetical or grouped by theme)

4. **Verify formatting:**
   - Proper indentation (2 spaces per level, matching existing code)
   - Comma placement consistent with existing code
   - Quote style consistent (single quotes for strings)
   - Array formatting matches existing benefits arrays
   - Escaped apostrophes in benefit text (e.g., "you\'re")

5. **Verify no breaking changes:**
   - No duplicate IDs
   - No duplicate category IDs
   - All existing features remain unchanged
   - Export statements unchanged

**Acceptance Criteria:**
- [ ] TrailPulse feature object added with ID 8
- [ ] All required properties present (id, title, description, category, icon, image, benefits)
- [ ] Benefits array has 6 items as specified
- [ ] "trail-engagement" category added to featureCategories
- [ ] Code formatting matches existing style
- [ ] Copyright header preserved
- [ ] No breaking changes to existing features
- [ ] No syntax errors
- [ ] Feature will display correctly on Features page
- [ ] Category filter will work correctly

**Dependencies:**
- Must reference trail-feedback-prompt.md Section 8 (R8.1-R8.4)
- Must verify current feature.js structure first

**Estimated Complexity:** Low (straightforward code addition)

**Notes:**
- Image file `/img/features/trailpulse.png` is a placeholder - actual image generation is separate task
- Icon `fa-heartbeat` represents pulse/heartbeat theme
- Description is user-focused (rider benefit, not technical)

---

## Questions

### Questions for Clarification

1. **Phase Numbering in MVP_PROJECT_PLAN.md:**
   - Current document has 14 phases. Should TrailPulse be Phase 15?
   - Or should it be inserted earlier (e.g., after mobile app phase)?
   - **Recommendation:** Add as Phase 15 to avoid renumbering existing phases

2. **Timeline Estimates:**
   - What timeline format is used in the project plan? (days, weeks, person-days?)
   - Should we estimate based on AI-assisted development speeds mentioned in the plan?
   - **Recommendation:** Use days, suggest 10-15 days backend/web + separate mobile team timeline

3. **Mobile Team Coordination:**
   - Is there a separate timeline/phase for mobile team TrailPulse work?
   - Should we note dependencies on mobile team in the backend phase?
   - **Recommendation:** Note in Dependencies section that mobile team implements client features separately

4. **Feature Image Asset:**
   - The trail-feedback-prompt.md includes image generation specifications. Should we create the image?
   - **Recommendation:** No - image generation is out of scope for this TODO. Use placeholder path.

5. **Testing Section in Project Plan:**
   - Does the project plan include testing tasks within each phase or separate testing phase?
   - **Recommendation:** Include testing tasks (X.20-X.25) within TrailPulse phase

### Unknowns to Address

1. **MVP_IMPLEMENTATION_PROMPT.md Section Placement:**
   - Need to read full document to determine best location for TrailPulse section
   - May need to match section numbering scheme used in document

2. **Project Plan Phase Structure:**
   - Need to read full MVP_PROJECT_PLAN.md to understand:
     - Exact task numbering format
     - Whether risks are assessed per phase
     - Timeline estimation methodology

3. **Existing TrailLens Features:**
   - Need to verify current feature count in features.js
   - Need to verify if there are any unpublished features with ID 8 already

---

## Summary

This TODO breaks down the work into three clear, actionable items:

1. **Documentation task (HIGH complexity):** Add comprehensive TrailPulse feature section to MVP implementation prompt with 11 subsections covering all requirements
2. **Planning task (HIGH complexity):** Add TrailPulse as new implementation phase in project plan with 20-25 tasks organized by component
3. **Code task (LOW complexity):** Update features.js with TrailPulse feature object and new category

**Total Estimated Effort:** 4-6 hours
- Item 1: 2-3 hours (comprehensive documentation writing)
- Item 2: 1.5-2 hours (detailed task breakdown and phase creation)
- Item 3: 0.5-1 hour (code addition with verification)

**Critical Path:** Items 1 and 2 can be done in parallel. Item 3 is independent.

**Success Criteria:** All three files updated with TrailPulse information, no implementation code written, copyright headers preserved, no breaking changes.
