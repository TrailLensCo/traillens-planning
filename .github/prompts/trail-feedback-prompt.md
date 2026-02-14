# TrailPulse - Trail Feedback and Usage Tracking Feature

## Feature Name: TrailPulse

**Selected Feature Name**: **TrailPulse**

This name best captures the real-time nature, usage tracking ("pulse" of trail activity), and condition monitoring in a memorable, branded term that aligns with the TrailLens product family.

### Alternative Names Considered

For reference, other names that were considered:

1. **TrailPulse** ✓ SELECTED
2. RideReport - Simple, action-oriented name focused on post-ride reporting
3. TrailSense - Suggests intelligent trail condition awareness and sensing
4. TrailWatch - Monitoring-focused, implies continuous observation
5. ConditionCheck - Direct, functional name focused on trail conditions
6. TrailTelemetry - Technical term that encompasses both feedback and usage data
7. RideInsight - Emphasizes the value derived from rider feedback
8. TrailMetrics - Data-focused name for condition and usage tracking
9. RideTrace - Suggests GPS tracking and post-ride reporting
10. TrailMonitor - Comprehensive monitoring of both conditions and usage

---

## IMPORTANT: Documentation Only

**This prompt is for adding TrailPulse feature to MVP documentation only.**

**Scope of Work - Three Files Only:**

1. **`docs/MVP_IMPLEMENTATION_PROMPT.md`** - Add TrailPulse feature section
2. **`docs/MVP_PROJECT_PLAN.md`** - Add TrailPulse to project plan
3. **`web/src/data/features.js`** - Add TrailPulse feature entry to website

**NOT in Scope:**

- No backend API implementation
- No database schema creation
- No infrastructure deployment
- No admin interface implementation
- No feedback management interface implementation
- Mobile app development (separate team handles this)

**Purpose:** This document defines the TrailPulse feature requirements for documentation purposes. The only code changes are the three files listed above.

---

## Task Overview

**Document** the TrailPulse trail feedback and usage tracking feature for TrailLens MVP.

**Features to Document:**

- Users to report trail conditions after riding subscribed trail systems
- Automated GPS-based ride detection within subscribed trail systems only
- Software-based trail usage counting to replace hardware counter devices
- Configurable feedback questions and frequency by trail system owners
- Trail admins to view, search, filter, and manage collected feedback data
- Crew member identification and management for better feedback context
- Privacy-first location tracking (opt-out available, only within subscribed systems)

**Current Task**: Add TrailPulse to three documentation/code files only. No implementation.

## Context

### Current State

- TrailLens has web interface and separate mobile app (developed independently)
- User authentication system exists (Cognito)
- Trail system subscription model is in place
- GPS capabilities available in mobile app (managed by mobile team)
- SNS infrastructure exists but needs mobile push integration
- Partial admin interface exists for trail system owners (needs extension)
- DynamoDB infrastructure available for application data

### Related Components

- **Mobile App** (Separate Team): GPS tracking, location services, push notifications
- **Web Interface** (This Repo - web/): Feedback submission form (login required)
- **Backend API** (This Repo - api-dynamo/): Data collection, ride detection logic, notification triggers, mobile endpoints
- **Database** (DynamoDB): Trail conditions, user responses, usage counts, configuration
- **Trail System Admin** (This Repo - web/): Extend existing admin interface for TrailPulse configuration
- **Infrastructure** (This Repo - infra/): SNS setup, DynamoDB tables, API Gateway endpoints

### Dependencies

- Mobile location services (GPS) - handled by mobile team
- Push notification service (SNS) - exists, needs mobile integration
- User authentication (Cognito) - already implemented
- Trail system geofence data (boundary definitions) - **NEEDS TO BE ADDED**
- Time-series data storage (DynamoDB with TTL)

### Constraints

- **Privacy First**: No tracking outside subscribed trail systems
- **Opt-Out Required**: Users must be able to disable GPS tracking
- **Performance**: GPS tracking should not drain battery excessively (mobile team responsibility)
- **Accuracy**: Geofence detection must be reliable to avoid false triggers
- **Scale**: System must handle multiple trail systems and concurrent users
- **MVP Scope**: Focus on core functionality, avoid over-engineering
- **No Feature Flag**: TrailPulse will be always enabled in MVP (no gradual rollout)
- **Mobile Separation**: This repo provides backend APIs; mobile team implements client features

## Requirements

### Scope Clarification

**This Repo's Scope (Backend & Web)**:

- Backend API endpoints in `api-dynamo/` submodule (FastAPI/Lambda)
- DynamoDB schema and infrastructure in `infra/` submodule (Pulumi)
- Web feedback form in `web/` submodule (React)
- Web admin configuration interface in `web/` submodule
- SNS push notification infrastructure in `infra/` submodule
- Feature list update in `web/src/data/features.js`

**Mobile Team's Scope (Separate Repo)**:

- GPS tracking implementation
- Geofence detection and ride start/end logic
- Push notification client (receiving and displaying)
- Mobile UI for feedback forms
- Device token registration
- Calling backend APIs from mobile app

**Note**: Requirements below describe the full feature. Implementation in this repo focuses on backend APIs, infrastructure, and web interfaces only.

---

### 1. Mobile App - GPS Tracking and Ride Detection (Mobile Team Implementation)

**R1.1 Location Tracking**
- Track GPS coordinates ONLY when user is within a subscribed trail system
- Implement geofencing to detect entry/exit from trail system boundaries
- Default: GPS tracking enabled (but only within subscribed systems)
- Provide opt-out setting in user preferences
- No tracking of users who opt out (still count usage via other means if possible)

**R1.2 Privacy Controls**
- Clear user consent during onboarding about location tracking
- Visible indicator when GPS tracking is active
- Easy access to disable tracking in settings
- No location data stored outside subscribed trail systems
- No tracking of individual user routes (only entry/exit and usage count)

**R1.3 Ride Detection**
- Detect when user enters a subscribed trail system
- Detect when user exits a subscribed trail system
- Calculate ride duration (entry to exit time)
- Increment usage count for both user and trail system
- Handle edge cases (app backgrounded, GPS signal loss, etc.)

**R1.4 Post-Ride Notification**
- Send push notification when user exits trail system
- Notification content: "How were the trails today?" (customizable by trail owner)
- Deeplink to feedback form in app
- Allow user to dismiss or complete feedback
- Respect notification preferences (DND, quiet hours)

### 2. Feedback Collection

**R2.1 Trail Condition Feedback (Every Ride)**
- Present trail condition options configured by trail system owner
- Default conditions: Dry, Muddy, Wet, Icy, Snowy, Rocky, Dusty
- Single or multiple selection based on owner configuration
- Optional free-text comment field
- Quick submit (< 30 seconds to complete)

**R2.2 Additional Questions (Configurable Frequency)**
- Trail system owner defines additional questions
- Owner sets frequency threshold (e.g., every 10 rides)
- Questions can be:
  - Multiple choice
  - Rating scale (1-5 stars)
  - Yes/No
  - Free text
- Track question response count to determine when to ask next

**R2.3 Web Interface Feedback**
- Login required (authenticated users only)
- Manual feedback submission (not tied to GPS ride detection)
- Select trail system from subscribed list
- Same question flow as mobile app
- Timestamp and user ID recorded

### 3. Trail System Owner Configuration

**R3.1 Condition Configuration**
- Define list of trail conditions to track
- Set condition types (single vs. multiple selection)
- Enable/disable condition tracking
- Preview how conditions appear to users

**R3.2 Additional Questions Configuration**
- Create custom questions
- Set question type (multiple choice, rating, yes/no, text)
- Define response options for multiple choice
- Set frequency threshold (e.g., ask every N rides)
- Enable/disable specific questions
- Reorder questions

**R3.3 Notification Customization**
- Customize exit notification message
- Set notification timing (immediate, 5 min delay, etc.)
- Enable/disable notifications

### 4. Feedback Data Management Interface

**R4.1 Feedback Data Viewing**

Trail admins need web interface to view and analyze collected feedback:

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

**R4.2 Search and Filter Capabilities**

Comprehensive search and filtering to help admins find relevant feedback:

- **Date Range Filter**: Filter feedback by date range (last 7 days, last 30 days, custom range)
- **Condition Filter**: Filter by specific trail conditions (e.g., show only "Muddy" reports)
- **User Filter**: Filter by specific user or user type (crew members, regular users, frequent reporters)
- **Question Filter**: Filter by responses to specific additional questions
- **Text Search**: Search within free-text comments
- **Feedback Count Filter**: Show users who have submitted N+ feedback entries
- **Combined Filters**: Apply multiple filters simultaneously
- **Save Filter Presets**: Save commonly used filter combinations

**R4.3 Feedback Management**

Admins can manage feedback data quality and relevance:

- **Delete Single Feedback**: Remove individual feedback entry with confirmation
- **Bulk Delete**: Select multiple feedback entries and delete together
- **Delete by Filter**: Delete all feedback matching current filter criteria (with confirmation)
- **Soft Delete Option**: Mark feedback as deleted without permanent removal (for audit trail)
- **Deletion Reason**: Optional field to note why feedback was deleted
- **Deletion Audit Log**: Track who deleted what and when

**R4.4 User Feedback Statistics**

Display aggregate user statistics to help admins identify patterns:

- **User Feedback Count**: Total number of feedback submissions per user
- **Crew Member Identification**: Visual badge or indicator for trail crew members
- **Feedback Frequency**: Average time between feedback submissions per user
- **Most Active Contributors**: Leaderboard or list of top feedback providers
- **User Feedback History**: Click user to see all their feedback submissions
- **Reliability Score**: Optional metric based on feedback consistency (post-MVP)

**R4.5 Data Usage for Trail Condition Management**

Integration with trail condition setting workflow:

- **Quick Condition Update**: Set trail condition based on recent feedback with one click
- **Feedback Summary View**: Aggregate view showing condition distribution (e.g., "70% reported Muddy")
- **Suggested Conditions**: System suggests trail condition based on recent feedback patterns
- **Feedback Context**: When setting conditions manually, show recent feedback as reference
- **Decision Support**: Show trend of conditions over past week/month

**R4.6 Crew Member Management**

Track and manage crew member status for better feedback context:

- **Crew Member Flag**: Admin can mark users as crew members
- **Crew Feedback Weighting**: Option to give more visibility to crew member feedback
- **Crew Activity Tracking**: See which crew members are actively providing feedback
- **Bulk Crew Assignment**: Add/remove crew status for multiple users
- **Crew Member Notes**: Add notes about crew members (roles, responsibilities)

### 5. Trail System Geofence Management

**R4.1 Geofence Data Model**

- Store trail system boundary coordinates in DynamoDB
- Support GeoJSON format or simple polygon coordinates
- Each trail system must have defined boundaries for ride detection
- Boundaries define where GPS tracking is active

**R4.2 Admin Interface for Geofences**

- Trail system owners can define/edit geofence boundaries
- Map-based interface for drawing boundaries (or coordinate input)
- Preview geofence coverage on map
- Validate boundary data (closed polygon, reasonable size)

**R4.3 API for Geofence Data**

- Mobile app retrieves geofence boundaries for subscribed trail systems
- Efficient boundary queries (don't send all geofences, only subscribed)
- Cache geofence data on mobile device
- Update geofences when trail system boundaries change

**R4.4 Geofence Validation**

- Backend validates ride start/end coordinates are within geofence
- Prevent false positives from GPS drift
- Reject ride events from non-subscribed trail systems
- Log geofence violations for debugging

### 5. Usage Counting System

**R4.1 Trail Usage Metrics**
- Count total rides for each trail system (all users combined)
- Count rides per user per trail system
- Store counts with timestamp for trend analysis
- No personally identifiable route data stored
- Aggregate counts visible to trail system owners

**R4.2 Count Accuracy**
- Count users who opt out of GPS (if app is open during ride)
- Deduplicate multiple entries/exits within short time window
- Handle offline scenarios (sync counts when connection restored)

**R4.3 Reporting for Trail Owners**
- Daily/weekly/monthly usage counts
- Trend graphs over time
- Export usage data (CSV)
- Software-based alternative to hardware trail counters

### 5. Data Model

**R5.1 Database Schema**

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

**R5.2 Data Retention**

- Individual ride events: 90 days (use DynamoDB TTL for automatic deletion)
- Aggregated usage counts: indefinite
- Feedback responses: indefinite
- User preferences: until account deletion
- Geofence boundary data: indefinite (part of trail system configuration)

### 6. Push Notification Integration

**R6.1 SNS Mobile Integration**

Extend existing SNS infrastructure for mobile push notifications:

- Extend existing SNS infrastructure for mobile push notifications
- Mobile team will provide device tokens for registered users
- Backend stores device tokens in DynamoDB (UserPreferences or separate table)
- Send post-ride notification via SNS to user's registered device(s)

**R6.2 Notification Triggers**

Configure when and how notifications are sent:

- Trigger notification when ride end event is recorded
- Include trail system name and feedback link in notification payload
- Respect user notification preferences (can opt out of feedback notifications)
- Handle notification failures gracefully (log but don't block ride recording)

**R6.3 Notification Content**

Define notification message format:

- Default message: "How were the trails at [Trail System Name] today?"
- Trail owners can customize notification message (optional)
- Include deeplink to feedback form: `traillens://feedback/{ride_id}`
- 24-hour expiration for feedback link

### 7. API Endpoints

**R7.1 Mobile App Endpoints (for separate mobile team)**

Endpoints for mobile app integration:

- `POST /api/trailpulse/rides/start` - Record ride entry
- `POST /api/trailpulse/rides/end` - Record ride exit, trigger notification
- `GET /api/trailpulse/geofences` - Get geofence boundaries for subscribed trail systems
- `GET /api/trailpulse/trail-systems/{id}/feedback-config` - Get questions for feedback
- `POST /api/trailpulse/feedback` - Submit feedback response
- `GET /api/trailpulse/user/ride-count/{trail_system_id}` - Get user ride count
- `PUT /api/trailpulse/user/preferences` - Update GPS/notification settings
- `POST /api/trailpulse/device-token` - Register device for push notifications

**R7.2 Web Endpoints**

Web interface feedback endpoints (all require authentication):

- `GET /api/trailpulse/trail-systems/subscribed` - Get user's subscribed trail systems
- `POST /api/trailpulse/feedback/web` - Submit web-based feedback
- All endpoints require authentication

**R7.3 Admin Endpoints (Trail System Owners)**

Trail system owner configuration endpoints:

- `GET /api/trailpulse/admin/trail-systems/{id}/config` - Get current configuration
- `PUT /api/trailpulse/admin/trail-systems/{id}/conditions` - Update trail conditions
- `POST /api/trailpulse/admin/trail-systems/{id}/questions` - Create additional question
- `PUT /api/trailpulse/admin/trail-systems/{id}/questions/{question_id}` - Update question
- `DELETE /api/trailpulse/admin/trail-systems/{id}/questions/{question_id}` - Delete question
- `GET /api/trailpulse/admin/trail-systems/{id}/usage` - Get usage statistics
- `PUT /api/trailpulse/admin/trail-systems/{id}/geofence` - Update geofence boundaries
- `GET /api/trailpulse/admin/trail-systems/{id}/geofence` - Get geofence boundaries

**R7.4 Admin Feedback Management Endpoints**

Feedback data viewing, searching, and management endpoints:

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
- `GET /api/trailpulse/admin/trail-systems/{id}/feedback/suggested-condition` - Get AI-suggested trail condition based on recent feedback

### 8. Web Feature List Update

**R8.1 Update Features Data**

Add TrailPulse feature to web project features list:

- File location: `web/src/data/features.js`
- Add new feature object with the following properties:
  - `id`: Next sequential ID (currently 8)
  - `title`: "TrailPulse"
  - `description`: "Share your trail experience and help improve conditions for the entire riding community" (user-focused, rider benefit)
  - `category`: "trail-engagement" (new category)
  - `icon`: "fa-heartbeat" (represents pulse/heartbeat)
  - `image`: "/img/features/trailpulse.png" (placeholder path)
  - `benefits`: Array of 4-6 key benefits highlighting **user/rider value**:
    - "Quick post-ride feedback on trail conditions"
    - "Help other riders know what to expect"
    - "Privacy-first - only tracks when you're on subscribed trails"
    - "Contribute to trail improvements with your input"
    - "Easy opt-out if you prefer not to share"
    - "Make your voice heard on trail maintenance priorities"

**R8.2 Update Feature Categories**

Add new category to `featureCategories` array:

- File location: `web/src/data/features.js`
- Category object:
  - `id`: "trail-engagement"
  - `name`: "Trail Engagement"

**R8.3 Feature Image Placeholder**

TrailPulse feature image specifications (for future generation):

- Image path: `/img/features/trailpulse.png` (placeholder for now)
- Specifications:
  - Dimensions: 1200x675px (16:9 aspect ratio)
  - Style: Modern, clean, professional
  - Visual elements: GPS/location icon, trail/mountain silhouette, heartbeat/pulse line
  - Color scheme: Consistent with TrailLens brand
  - Mobile-friendly composition

**R8.4 Acceptance Criteria**

Feature list update validation:

- TrailPulse feature appears on Features page when "All Features" or "Trail Engagement" category is selected
- Feature card displays correctly with icon, title, description, and benefits
- Feature integrates seamlessly with existing features list
- No breaking changes to features.js structure
- Follows existing code style and copyright header requirements

## Expected Behavior

### User Journey - Mobile App (GPS Enabled)
1. User subscribes to a trail system
2. User arrives at trail system → App detects geofence entry
3. GPS tracking begins (only within trail boundaries)
4. User rides trails (app tracks presence, not route)
5. User exits trail system → App detects geofence exit
6. System increments usage count
7. Push notification sent: "How were the trails today?"
8. User taps notification → Feedback form opens
9. User selects trail conditions (e.g., "Muddy", "Wet")
10. If ride count threshold met, additional questions shown
11. User submits feedback
12. Data saved, confirmation shown

### User Journey - Web Interface
1. User logs into TrailLens web app
2. User navigates to "Trail Feedback" section
3. User selects trail system from subscribed list
4. Feedback form loads with configured questions
5. User answers condition questions and any additional questions
6. User submits feedback
7. Confirmation displayed

### Trail Owner Journey - Configuration
1. Trail owner logs into admin interface
2. Navigates to "Feedback Settings" for their trail system
3. Configures trail conditions (add/remove/reorder)
4. Creates additional questions with frequency settings
5. Sets notification message and timing
6. Saves configuration
7. Preview feedback form as users will see it

### Trail Admin Journey - Feedback Data Management

1. Trail admin logs into admin interface
2. Navigates to "TrailPulse Data" section for their trail system
3. **Viewing Feedback Data**:
   - Table displays all submitted feedback with columns: Date, User, Conditions, Responses, Comments
   - User metadata visible: feedback count badge, crew member indicator
   - Click row to expand for full details
   - Paginated results (50 per page default)
4. **Filtering and Searching**:
   - Apply date range filter (last 7 days, last 30 days, custom)
   - Filter by specific trail conditions (e.g., show only "Muddy" reports)
   - Filter by user type (all, crew members, frequent reporters)
   - Search within free-text comments
   - Filter by users with N+ feedback submissions
   - Combine multiple filters
5. **Using Feedback to Set Trail Conditions**:
   - View feedback summary card showing condition distribution (e.g., "70% Muddy, 20% Wet, 10% Dry")
   - System suggests trail condition based on recent patterns
   - "Set Condition from Feedback" quick action button
   - Recent feedback shown as reference when manually updating conditions
6. **Managing Data Quality**:
   - Identify spam, duplicate, or inappropriate feedback
   - Select single feedback entry and click "Delete" button
   - Provide optional deletion reason
   - Choose soft delete (hide from view, keep in database) or permanent delete
   - Confirmation dialog before deletion
   - Deletion logged in audit trail with admin name and timestamp
7. **Bulk Management**:
   - Select multiple feedback entries with checkboxes
   - Bulk delete selected entries
   - Delete all feedback matching current filters with confirmation
8. **Crew Member Management**:
   - View user feedback history by clicking username
   - Identify valuable contributors
   - Click "Mark as Crew Member" button
   - Add optional crew notes (role, responsibilities)
   - View list of all crew members with activity stats
   - Bulk add/remove crew status for multiple users
9. **Feedback Statistics**:
   - View top contributors leaderboard
   - See feedback frequency trends
   - Export filtered feedback data to CSV

### Usage Count Display
- Trail owner dashboard shows:
  - Total rides this week/month/year
  - Usage trends graph
  - Peak usage days/times
  - Export button for raw data

## Additional Notes

### Edge Cases to Consider

**GPS and Network**
- User loses GPS signal mid-ride → Handle gracefully, don't count as exit
- User's phone dies during ride → Sync entry/exit on next app open
- Geofence boundary overlap with multiple trail systems → Use most specific/smallest boundary
- User enters trail system offline → Queue ride event, sync when online

**Notification Scenarios**
- User has notifications disabled → Store feedback opportunity, show in-app prompt next time
- User dismisses notification → Don't re-notify for same ride
- User exits/re-enters quickly → Deduplicate, treat as single ride if < 10 min apart

**Feedback Timing**
- User delays responding to feedback → Feedback remains available for 24 hours post-ride
- User rides multiple times in one day → Separate feedback for each ride (conditions may change)

**Privacy and Opt-Out**
- User opts out mid-ride → Stop tracking immediately, count ride up to opt-out point
- User opts back in → Start tracking on next ride
- User deletes account → Delete all ride events and feedback, keep anonymized usage counts

**Configuration Changes**
- Owner changes conditions while user has pending feedback → Use conditions from ride time, not current
- Owner deletes question → Mark as deprecated, don't show in new feedback, keep historical responses
- Frequency threshold changes → Apply to future rides only, don't retroactively trigger

### Technical Considerations

**Battery Optimization**
- Use geofencing APIs (not continuous GPS polling)
- Coarse location when outside trail systems (to detect entry)
- Fine location only when inside trail system
- Background location services with minimal updates

**Scalability**
- Usage counts should be aggregated asynchronously
- Consider time-series database for usage metrics (DynamoDB with TTL)
- Cache frequently accessed configuration data

**Security**
- Validate geofence boundaries on backend (don't trust client)
- Rate limit feedback submissions (prevent spam)
- Sanitize free-text responses
- Authenticate all API calls

**Testability**
- Mock location services for testing
- Simulate geofence entry/exit in dev environment
- Test notification delivery
- Test frequency logic with various ride counts

### Integration Points

**Existing Systems**

- User authentication (Cognito) - both web and mobile use this
- Subscription management (must check active subscription)
- Push notification service (SNS) - exists, needs mobile integration
- Trail system boundary data (geofence coordinates) - **NEW, needs to be added**

**New Infrastructure Needed**

- DynamoDB tables for TrailPulse data
- SNS topic for push notifications (mobile device endpoints)
- API Gateway endpoints for TrailPulse APIs
- Lambda functions for API handlers
- DynamoDB TTL configuration for ride event expiration
- Background job for aggregating usage counts (optional - can be done on-demand)

**Backend-Mobile Integration Flow**:

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

### MVP Scope Recommendations

**Note**: These scope recommendations are for **documentation purposes only**. No implementation is being done at this time.

**Must Have (MVP) - For Documentation (This Repo)**:

- DynamoDB schema for ride events, feedback, usage counts, geofences, preferences, crew members, audit logs
- Backend API endpoints for mobile app (ride start/end, feedback, geofences, preferences)
- Backend API endpoints for web (feedback submission)
- Admin API endpoints (configuration, usage stats, geofence management)
- Admin API endpoints for feedback management (view, search, filter, delete, crew member management)
- SNS integration for push notifications
- Web feedback form (manual feedback entry)
- Admin configuration interface (trail conditions, questions, geofences)
- Admin feedback data management interface (view, search, filter, delete feedback)
- Crew member management interface (assign/remove crew status)
- Usage counting and aggregation logic
- Data retention (90-day TTL on ride events, soft delete for feedback)
- Web feature list update with TrailPulse entry
- Infrastructure deployment (DynamoDB tables, API Gateway, SNS topics)

**Must Have (MVP) - For Documentation (Mobile Team)**:

- GPS tracking within subscribed trail systems
- Geofence detection (entry/exit)
- Ride start/end event recording (call backend API)
- Push notification client
- Mobile feedback form UI
- User preferences for GPS opt-out
- Device token registration

**Should Have (Post-MVP)**:

- Advanced question types (rating scales, multi-select)
- Frequency-based additional questions
- Usage analytics dashboard with graphs (web)
- Export functionality (CSV)
- In-app feedback history for users (mobile)
- Map-based geofence editor (web admin)

**Nice to Have (Future)**:

- Real-time condition map (aggregated user reports)
- Weather integration for condition predictions
- Social features (share ride stats)
- Gamification (badges for ride counts)
- ML-based condition predictions

### TrailPulse Feature Image Requirements

The documentation should include a comprehensive prompt for generating the TrailPulse feature image. This prompt will be used separately to create the feature image asset.

**Image Generation Prompt Specifications:**

The prompt should request an image with these characteristics:

- **Dimensions**: 1200x675px (16:9 aspect ratio, optimized for web display)
- **File Format**: PNG with transparency support
- **Style**: Modern, clean, professional design that matches TrailLens brand aesthetic
- **Color Palette**:
  - Primary: Blues and greens (trail/nature theme)
  - Accent: Vibrant pulse/heartbeat color (orange or bright green)
  - Background: Light, neutral tones or subtle gradient
- **Visual Elements**:
  - GPS/location pin or marker icon
  - Trail or mountain silhouette in background
  - Heartbeat/pulse line graphic (representing "pulse" in TrailPulse)
  - Optional: Mobile device showing feedback interface
  - Optional: Subtle trail map or topographic pattern
- **Composition**:
  - Focal point in center or slightly left of center
  - Leave space for text overlay if needed
  - Mobile-friendly (important elements visible at small sizes)
  - High contrast for readability
- **Mood/Tone**: Active, engaging, tech-forward, outdoorsy
- **Usage Context**: Will be displayed on Features page alongside other feature images

**Prompt Template:**

```markdown
Generate a feature image for TrailPulse, a trail feedback and usage tracking system.

Image Requirements:
- Size: 1200x675px (16:9 aspect ratio)
- Format: PNG
- Style: Modern, clean, professional

Visual Elements:
- GPS/location icon or pin marker
- Trail/mountain silhouette backdrop
- Heartbeat or pulse line graphic (central theme)
- Color scheme: Blues, greens, with vibrant accent color
- Optional: Mobile device mockup showing feedback form

Composition:
- Center or center-left focal point
- High contrast, mobile-friendly
- Space for potential text overlay
- Professional outdoor tech aesthetic

Context: This image represents a system that tracks trail usage via GPS and collects rider feedback on trail conditions. The "pulse" theme represents the heartbeat of trail activity.
```

**Note**: The image will be saved to `web/public/img/features/trailpulse.png` after generation.

## Instructions for AI Assistant

**CRITICAL - THREE FILES ONLY**:

This prompt adds TrailPulse feature to documentation. The scope is:

**Three Files to Update:**

1. **`docs/MVP_IMPLEMENTATION_PROMPT.md`** - Add a "TrailPulse" section describing the feature, its requirements, API endpoints, database schema, and implementation details
2. **`docs/MVP_PROJECT_PLAN.md`** - Add TrailPulse to the project plan with timeline, milestones, and dependencies
3. **`web/src/data/features.js`** - Add TrailPulse feature object (ID 8) and "trail-engagement" category

**DO NOT IMPLEMENT**:

- ❌ No backend API code
- ❌ No database schema creation
- ❌ No infrastructure deployment
- ❌ No admin interface implementation
- ❌ No feedback management interface
- ❌ No TODO file creation

The requirements documented here are for **reference only**. The three file updates are the complete scope.

**Process**:

1. Read and understand all requirements above
2. Update `docs/MVP_IMPLEMENTATION_PROMPT.md` with TrailPulse feature section
3. Update `docs/MVP_PROJECT_PLAN.md` with TrailPulse in project plan
4. Update `web/src/data/features.js` with TrailPulse feature entry
5. Present changes for review

**Success Criteria**:

- [ ] `docs/MVP_IMPLEMENTATION_PROMPT.md` updated with TrailPulse feature section
- [ ] `docs/MVP_PROJECT_PLAN.md` updated with TrailPulse in project plan
- [ ] `web/src/data/features.js` updated with TrailPulse feature entry (ID 8)
- [ ] New "trail-engagement" category added to featureCategories
- [ ] Copyright headers preserved in all files
- [ ] No breaking changes to existing code
- [ ] Only three files modified - no other changes

**Questions Clarified**:

1. ✓ Mobile app is developed separately (different team/repo) - this repo provides backend APIs
2. ✓ DynamoDB will be used for all TrailPulse data
3. ✓ Partial admin interface exists - extend it for TrailPulse configuration
4. ✓ SNS exists but needs mobile push integration
5. ✓ Data retention: 90 days for ride events (DynamoDB TTL), indefinite for aggregates and feedback
6. ✓ Geofence boundaries need to be added (new requirement)
7. ✓ No feature flag - always enabled in MVP
8. ✓ Web feature description should be user-focused (rider benefits)

**Remaining Questions for Mobile Team Coordination**:

1. What is the mobile app's deeplink URL scheme? (assumed `traillens://` but needs confirmation)
2. How will the mobile team provide device tokens for push notifications? (API endpoint? Separate system?)
3. What geolocation library/framework does the mobile app use? (to ensure compatible geofence format)
4. Does the mobile app already have a subscription data sync mechanism, or do we need to design one?
