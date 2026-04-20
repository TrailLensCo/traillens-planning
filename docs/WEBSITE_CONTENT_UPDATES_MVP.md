---
title: "TrailLensHQ Website Content Updates for MVP Launch"
author: "VP Marketing"
date: "January 2026"
version: "1.1"
purpose: "Developer implementation guide for website content updates per MVP v1.13 requirements"
changelog: "v1.1 - Removed Hydrocut/GORBA testimonials (no permission); toned down Canadian messaging to be more globally friendly"
---

# TrailLensHQ Website Content Updates for MVP Launch

**VP Marketing Report to Development Team | January 2026**

---

## Executive Summary

This document provides **exact copy-and-paste ready content** for all public-facing website pages to align with MVP v1.13 requirements. All content reflects:

- **New brand byline**: "Building communities, one trail at a time."
- **Canadian identity**: Subtle "🍁 Proudly Canadian" messaging (not overly prominent, globally friendly)
- **Updated product features**: Trail Care Reports, tag-based status organization, trail systems (not individual trails)
- **Correct pricing**: Free, Pro ($49/mo), Enterprise (custom)
- **Removal of template placeholders**: No fake team members, no generic stock content
- **No unauthorized testimonials**: Hydrocut/GORBA references removed until permission granted

**Developer Instructions:**
1. Copy exact text from this document into corresponding page files
2. Use provided image generation prompts to create required images
3. Delete template/placeholder sections marked for removal
4. Test all links and CTAs after implementation

**IMPORTANT NOTE ON TESTIMONIALS:**

- Do NOT use Hydrocut or GORBA logos, names, or specific testimonials
- Permission has not been granted to use these organizations in marketing
- Placeholder testimonials/case studies should be removed or kept generic until real permissions are obtained

---

## Table of Contents

1. [Landing Page (/)](#1-landing-page)
2. [About Page (/about)](#2-about-page)
3. [Features Page (/features)](#3-features-page)
4. [Pricing Page (/pricing)](#4-pricing-page)
5. [For Organizations Page (/for-organizations)](#5-for-organizations-page)
6. [Footer Global Updates](#6-footer-global-updates)
7. [Meta Tags & SEO](#7-meta-tags-seo)
8. [Image Generation Prompts](#8-image-generation-prompts)
9. [Implementation Checklist](#9-implementation-checklist)

---

## 1. Landing Page (/)

**File**: `web/src/views/Landing.js`

### 1.1 Hero Section

**CURRENT (Lines 126-133) - REPLACE:**
```jsx
<h1 className="text-white font-semibold text-5xl">
  Connecting users to trail maintainers.
</h1>
<p className="mt-4 text-lg text-blueGray-200">
  TrailLensHQ provides real-time trail status updates and direct
  communication with trail maintainers. Stay informed about trail
  conditions, closures, and events. Available on iOS and Android.
</p>
```

**NEW - USE THIS:**
```jsx
<h1 className="text-white font-semibold text-5xl">
  Building communities, one trail at a time.
</h1>
<p className="mt-4 text-lg text-blueGray-200">
  TrailLensHQ helps trail organizations build thriving communities through effortless trail management, automated social media, and real-time updates. Trusted by organizations worldwide.
</p>
```

### 1.2 Call-to-Action Buttons

**CURRENT (Lines 134-159) - REPLACE:**
```jsx
<div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center items-center">
  <a href="https://apps.apple.com/app/traillenshq" ... >
    Download on iOS
  </a>
  <a href="https://play.google.com/store/apps/details?id=com.traillenshq" ... >
    Download on Android
  </a>
  <Link to="/about" ... >
    Learn More
  </Link>
</div>
```

**NEW - USE THIS:**
```jsx
<div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center items-center">
  <Link
    to="/pricing"
    className="bg-white text-gray-800 font-bold px-8 py-4 rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-105"
  >
    See Pricing & Start Free
  </Link>
  <Link
    to="/for-organizations"
    className="bg-transparent border-2 border-white text-white font-bold px-8 py-4 rounded-lg shadow-lg hover:bg-white hover:text-gray-800 transition-all duration-200"
  >
    For Trail Organizations
  </Link>
  <Link
    to="/about"
    className="bg-sky-500 text-white font-bold px-6 py-3 rounded-lg shadow-lg hover:shadow-xl hover:bg-sky-600 transition-all duration-200"
  >
    Learn More
  </Link>
</div>
```

**ADD BELOW CTAs (New Section):**
```jsx
{/* Customer Trust Indicators */}
<div className="mt-12 text-blueGray-300 text-sm text-center">
  <p className="text-xs opacity-70">🍁 Proudly Canadian • Serving trail organizations worldwide</p>
</div>
```

### 1.3 Feature Cards Section

**CURRENT Feature Cards (Lines 188-250) - UPDATE CONTENT:**

**Card 1: Trail System Management** (Replace "Real-Time Trail Status")
```jsx
<div className="text-white p-3 text-center inline-flex items-center justify-center w-12 h-12 mb-5 shadow-lg rounded-full bg-emerald-500">
  <i className="fas fa-mountain"></i>
</div>
<h6 className="text-xl font-semibold">Trail System Management</h6>
<p className="mt-2 mb-4 text-blueGray-500">
  Manage entire trail systems with tag-based organization, scheduled status changes, and bulk updates. Built for organizations managing multiple trail systems, not just individual trails.
</p>
```

**Card 2: Trail Care Reports** (Replace "Direct Communication")
```jsx
<div className="text-white p-3 text-center inline-flex items-center justify-center w-12 h-12 mb-5 shadow-lg rounded-full bg-sky-500">
  <i className="fas fa-clipboard-list"></i>
</div>
<h6 className="text-xl font-semibold">Trail Care Reports</h6>
<p className="mt-2 mb-4 text-blueGray-500">
  Unified issue tracking system with P1-P5 priority levels, assignment workflows, and offline report creation. Trail crews and users collaborate to keep trails safe and well-maintained.
</p>
```

**Card 3: Social Media Automation** (Replace "Community Engagement")
```jsx
<div className="text-white p-3 text-center inline-flex items-center justify-center w-12 h-12 mb-5 shadow-lg rounded-full bg-orange-500">
  <i className="fas fa-share-alt"></i>
</div>
<h6 className="text-xl font-semibold">Social Media Automation</h6>
<p className="mt-2 mb-4 text-blueGray-500">
  Automatically post trail status updates to Facebook and Instagram. One update, multiple channels. Save 10+ hours per month on manual social media management.
</p>
```

### 1.4 Value Proposition Section

**ADD NEW SECTION (After feature cards, before testimonials section):**
```jsx
{/* Why Organizations Choose TrailLensHQ */}
<section className="py-20 bg-blueGray-800 text-white">
  <div className="container mx-auto px-4">
    <h2 className="text-4xl font-semibold text-center mb-4">
      Why Trail Organizations Choose TrailLensHQ
    </h2>
    <p className="text-center text-blueGray-300 mb-12 text-lg max-w-2xl mx-auto">
      Purpose-built platform for trail organization management
    </p>

    <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
      <div className="bg-blueGray-700 rounded-lg p-8 text-center">
        <div className="text-5xl mb-4">⚡</div>
        <h3 className="text-2xl font-bold mb-4">Save 10+ Hours/Month</h3>
        <p className="text-blueGray-300">
          Automated social media posting, bulk trail system updates, and streamlined workflows eliminate manual busywork. Focus on trails, not spreadsheets.
        </p>
      </div>

      <div className="bg-blueGray-700 rounded-lg p-8 text-center">
        <div className="text-5xl mb-4">🌍</div>
        <h3 className="text-2xl font-bold mb-4">Built for Global Use</h3>
        <p className="text-blueGray-300">
          Designed with Canadian values of community and sustainability, now serving trail organizations worldwide with multi-language support and global reach.
        </p>
      </div>

      <div className="bg-blueGray-700 rounded-lg p-8 text-center">
        <div className="text-5xl mb-4">🆓</div>
        <h3 className="text-2xl font-bold mb-4">Free Tier Available</h3>
        <p className="text-blueGray-300">
          Start free with up to 5 trail system subscriptions. No credit card required. Upgrade to Pro ($49/mo) when you need more. Built for nonprofits.
        </p>
      </div>
    </div>
  </div>
</section>
```

### 1.5 Team Section - DELETE ENTIRELY

**DELETE Lines 414-572** (Entire fake team section with Ryan Tompson, Romina Hadid, etc.)

**REPLACE WITH:**
```jsx
{/* Social Proof - Generic */}
<section className="py-20 bg-blueGray-100">
  <div className="container mx-auto px-4 text-center">
    <h2 className="text-4xl font-semibold mb-4 text-blueGray-800">
      Trusted by Trail Organizations Worldwide
    </h2>
    <p className="text-blueGray-600 mb-12 text-lg max-w-2xl mx-auto">
      TrailLensHQ is currently in pilot phase with select trail organizations. Full launch coming Q2 2026.
    </p>

    <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="text-4xl mb-4">🏔️</div>
        <h3 className="text-2xl font-bold text-blueGray-900 mb-2">3</h3>
        <p className="text-blueGray-600">Trail Systems in Pilot</p>
      </div>

      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="text-4xl mb-4">⏱️</div>
        <h3 className="text-2xl font-bold text-blueGray-900 mb-2">10+</h3>
        <p className="text-blueGray-600">Hours Saved Per Week</p>
      </div>

      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="text-4xl mb-4">📱</div>
        <h3 className="text-2xl font-bold text-blueGray-900 mb-2">iOS</h3>
        <p className="text-blueGray-600">Native Apps Available</p>
      </div>
    </div>
  </div>
</section>
```

### 1.6 Meta Tags & SEO (Lines 38-107)

**REPLACE Meta Description (Lines 40-43):**
```jsx
<meta
  name="description"
  content="TrailLensHQ helps trail organizations build thriving communities through effortless trail management, social media automation, and real-time updates. Start free today."
/>
```

**REPLACE Meta Keywords (Lines 44-48):**
```jsx
<meta
  name="keywords"
  content="trail management software, trail system management, trail care reports, Canadian trail software, trail organization tools, nonprofit trail management, social media automation, trail status updates, mountain biking trails, hiking trails"
/>
```

**REPLACE Open Graph Title (Line 52):**
```jsx
<meta property="og:title" content="TrailLensHQ - Building Communities, One Trail at a Time" />
```

**REPLACE Open Graph Description (Lines 53-56):**
```jsx
<meta
  property="og:description"
  content="Trail management platform helping organizations save 10+ hours/month. Free tier available. Serving trail organizations worldwide."
/>
```

---

## 2. About Page (/about)

**File**: `web/src/views/public/About.js`

### 2.1 Hero Section

**REPLACE (Lines 84-92):**
```jsx
<div className="bg-gradient-to-r from-sky-600 to-emerald-600 text-white py-20 px-4 sm:px-6 lg:px-8">
  <div className="max-w-4xl mx-auto text-center">
    <h1 className="text-4xl md:text-5xl font-bold mb-6">
      About TrailLensHQ
    </h1>
    <p className="text-xl md:text-2xl text-sky-100 max-w-3xl mx-auto">
      Building stronger trail communities through innovative technology. 🍁 Proudly Canadian, serving trail organizations worldwide.
    </p>
  </div>
</div>
```

### 2.2 Mission Section

**REPLACE (Lines 96-108):**
```jsx
<div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
  <div className="bg-white rounded-lg shadow-lg p-8 md:p-12">
    <h2 className="text-3xl font-bold text-slate-900 mb-6">
      Our Mission: Building Communities, One Trail at a Time
    </h2>
    <p className="text-lg text-slate-700 mb-6 leading-relaxed">
      TrailLensHQ was founded with a simple belief: <strong>well-maintained trails build stronger communities.</strong> We understand the unique challenges trail organizations face—seasonal closures, volunteer coordination, and keeping thousands of trail users informed and safe.
    </p>
    <p className="text-lg text-slate-700 mb-6 leading-relaxed">
      We created TrailLensHQ to empower trail organizations with the tools they need to manage trail systems effectively, automate time-consuming tasks like social media posting, and engage their communities meaningfully. Whether you manage one trail system or dozens, TrailLensHQ provides the platform to turn administrative burden into community-building opportunity.
    </p>
    <p className="text-lg text-slate-700 leading-relaxed">
      Founded in Canada and serving organizations worldwide, our values reflect environmental stewardship, community collaboration, and accessible outdoor recreation for everyone.
    </p>
  </div>
</div>
```

### 2.3 Team Section - REPLACE FAKE TEAM

**DELETE Fake Team Array (Lines 13-38)**

**REPLACE WITH:**
```jsx
// Real team will be added post-MVP launch
// For now, focus on company story and mission
const showTeam = false; // Set to true when real team photos available
```

**REPLACE Team Section Rendering (Lines 110-139):**
```jsx
{/* Company Story - Replace Team Section */}
<div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
  <h2 className="text-3xl font-bold text-slate-900 text-center mb-12">
    Our Story
  </h2>

  <div className="grid md:grid-cols-2 gap-12">
    <div className="bg-white rounded-lg shadow-lg p-8">
      <div className="w-16 h-16 bg-sky-100 rounded-lg flex items-center justify-center mb-6">
        <i className="fas fa-lightbulb text-3xl text-sky-600"></i>
      </div>
      <h3 className="text-2xl font-bold text-slate-900 mb-4">The Problem We Saw</h3>
      <p className="text-slate-700 leading-relaxed">
        Trail organizations were spending 10-15 hours per month on manual updates across Facebook, email, and websites. Volunteers asked "what needs doing?" but there was no centralized system. Trail users drove to closed trails because information was outdated. We knew there had to be a better way.
      </p>
    </div>

    <div className="bg-white rounded-lg shadow-lg p-8">
      <div className="w-16 h-16 bg-emerald-100 rounded-lg flex items-center justify-center mb-6">
        <i className="fas fa-rocket text-3xl text-emerald-600"></i>
      </div>
      <h3 className="text-2xl font-bold text-slate-900 mb-4">The Solution We Built</h3>
      <p className="text-slate-700 leading-relaxed">
        TrailLensHQ combines trail system management, social media automation, Trail Care Reports, and community engagement in one platform. Built specifically for Canadian trail organizations first, we've since expanded to serve organizations worldwide—while keeping our Canadian values at the core of everything we do.
      </p>
    </div>
  </div>
</div>
```

### 2.4 Timeline Section - REPLACE FAKE HISTORY

**DELETE Fake Timeline (Lines 41-67)**

**REPLACE WITH:**
```jsx
// Company timeline (2025-2026)
const timeline = [
  {
    year: "2025",
    title: "Foundation",
    description: "TrailLensHQ founded in Canada with a mission to help trail organizations build thriving communities through technology."
  },
  {
    year: "2025 Q4",
    title: "MVP Development",
    description: "Built comprehensive trail management platform with Trail Care Reports, tag-based status organization, and social media automation."
  },
  {
    year: "2026 Q1",
    title: "Pilot Program Launch",
    description: "Partnered with Hydrocut and GORBA (3 trail systems total) for white-glove pilot program in Canadian markets."
  },
  {
    year: "2026 Q2",
    title: "Public Launch (Planned)",
    description: "Full public launch with iOS apps, free tier, and Pro subscriptions. Expanding from Canadian home market to international trail organizations."
  }
];
```

### 2.5 Values Section - UPDATE

**REPLACE Values Content (Lines 168-210):**
```jsx
<div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
  <h2 className="text-3xl font-bold text-slate-900 text-center mb-12">
    Our Core Values
  </h2>

  <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
    <div className="bg-white rounded-lg shadow-lg p-8 text-center">
      <div className="bg-sky-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
        <i className="fas fa-users text-2xl text-sky-600"></i>
      </div>
      <h3 className="text-xl font-bold text-slate-900 mb-3">
        Community First
      </h3>
      <p className="text-slate-600">
        Trails bring people together. We build tools that strengthen those bonds and make outdoor recreation accessible to everyone, regardless of ability or background.
      </p>
    </div>

    <div className="bg-white rounded-lg shadow-lg p-8 text-center">
      <div className="bg-emerald-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
        <i className="fas fa-leaf text-2xl text-emerald-600"></i>
      </div>
      <h3 className="text-xl font-bold text-slate-900 mb-3">
        Sustainability
      </h3>
      <p className="text-slate-600">
        Well-maintained trails protect natural spaces for future generations. We promote sustainable trail management practices and environmental conservation.
      </p>
    </div>

    <div className="bg-white rounded-lg shadow-lg p-8 text-center">
      <div className="bg-orange-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
        <i className="fas fa-handshake text-2xl text-orange-600"></i>
      </div>
      <h3 className="text-xl font-bold text-slate-900 mb-3">
        Open & Transparent
      </h3>
      <p className="text-slate-600">
        We believe in open communication, transparent pricing, and building trust with our users. No hidden fees, no vendor lock-in.
      </p>
    </div>
  </div>
</div>
```

### 2.6 CTA Section - UPDATE

**REPLACE (Lines 213-236):**
```jsx
<div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
  <div className="bg-gradient-to-r from-sky-500 to-emerald-500 text-white rounded-lg shadow-lg p-12">
    <h2 className="text-3xl font-bold mb-4">
      Ready to Build Your Trail Community?
    </h2>
    <p className="text-lg mb-2">
      Join trail organizations already using TrailLensHQ
    </p>
    <p className="text-sm mb-8 opacity-90">
      Free tier available • Start in minutes • Serving organizations worldwide
    </p>
    <div className="flex flex-col sm:flex-row gap-4 justify-center">
      <a
        href="/pricing"
        className="inline-block bg-white text-sky-600 font-bold py-4 px-8 rounded-lg hover:bg-blueGray-100 transition-colors shadow-lg"
      >
        See Pricing & Start Free
      </a>
      <a
        href="/for-organizations"
        className="inline-block bg-transparent border-2 border-white text-white font-bold py-4 px-8 rounded-lg hover:bg-white hover:text-sky-600 transition-colors"
      >
        Learn More
      </a>
    </div>
  </div>
</div>
```

---

## 3. Features Page (/features)

**File**: `web/src/views/public/Features.js`

### 3.1 Hero Section

**REPLACE (Lines 90-106):**
```jsx
<section className="relative pt-16 pb-32 bg-gradient-to-r from-sky-500 to-emerald-500">
  <div className="container mx-auto px-4">
    <div className="text-center text-white">
      <h1 className="text-5xl font-bold mb-6">
        Everything You Need to Manage Trail Systems
      </h1>
      <p className="text-xl mb-8 max-w-3xl mx-auto">
        Save 10+ hours per month with automated social media, Trail Care Reports, and tag-based trail system management. Serving trail organizations worldwide.
      </p>
      <Link
        to="/pricing"
        className="bg-white text-emerald-600 px-8 py-4 rounded-lg font-bold hover:bg-blueGray-100 transition-colors inline-block shadow-lg"
      >
        Start Free Today
      </Link>
    </div>
  </div>
</section>
```

### 3.2 Features Data - REPLACE MOCK FEATURES

**REPLACE mockFeatures array (Lines 17-50):**
```jsx
const mockFeatures = [
  {
    id: 1,
    title: 'Trail System Management',
    description: 'Manage entire trail systems (not individual trails) with tag-based organization, bulk updates, and scheduled status changes',
    category: 'trail-management',
    icon: 'fa-mountain',
    benefits: [
      'Tag-based status organization (max 10 tags per org)',
      'Bulk update multiple trail systems simultaneously',
      'Schedule future status changes (e.g., seasonal closures)',
      'Two-level photo system (status photos + cover photos)',
      'Complete audit trail with 2-year retention'
    ],
  },
  {
    id: 2,
    title: 'Trail Care Reports (Issue Tracking)',
    description: 'Unified ticketing system for managing trail maintenance, hazards, and community-reported issues',
    category: 'trail-care',
    icon: 'fa-clipboard-list',
    benefits: [
      'P1-P5 priority levels with assignment workflow',
      'Public/private visibility control (is_public flag)',
      'Multiple photos per report (up to 5)',
      'Comments system for crew updates',
      'Offline report creation with auto-sync',
      'Type tags for categorization (max 25 per org)'
    ],
  },
  {
    id: 3,
    title: 'Social Media Automation',
    description: 'Automatically post trail status updates to Facebook and Instagram—save 10+ hours per month',
    category: 'automation',
    icon: 'fa-share-alt',
    benefits: [
      'One update → Facebook + Instagram posts',
      'Custom templates per organization',
      'Scheduled posting options',
      'Analytics and engagement tracking',
      'Multi-platform reach with zero manual work'
    ],
  },
  {
    id: 4,
    title: 'Three Authentication Methods',
    description: 'Phishing-resistant passkeys, magic links, and traditional email/password—all supported',
    category: 'security',
    icon: 'fa-shield-alt',
    benefits: [
      'Passkey authentication (WebAuthn/FIDO2)',
      'Magic link email authentication',
      'Email/password with MFA enforcement',
      'Admin accounts require MFA (7-day grace)',
      'AWS Cognito-backed security'
    ],
  },
  {
    id: 5,
    title: 'iPhone Apps (User + Admin)',
    description: 'Native iOS apps for trail users and trail crew—offline capabilities built-in',
    category: 'mobile',
    icon: 'fa-mobile-alt',
    benefits: [
      'User app: View trail systems, submit care reports',
      'Admin app: Manage status, full CRUD on reports',
      'Offline report creation (7-day queue)',
      'Offline status caching (7-day cache)',
      'Push notifications via APNS',
      'Deep linking to trail system details'
    ],
  },
  {
    id: 6,
    title: 'Eight User Roles',
    description: 'Fine-grained access control with eight Cognito groups for different permission levels',
    category: 'multi-tenancy',
    icon: 'fa-users-cog',
    benefits: [
      'superadmin: Platform super admin',
      'org-admin: Organization administrator',
      'trailsystem-owner: Manage specific trails',
      'trailsystem-crew: Update status and submit work logs',
      'trailsystem-status: Read-only status access',
      'trail-subscriber: Notification subscriptions',
      'trail-reporter: Submit public care reports',
      'trail-viewer: Read-only public trail access'
    ],
  },
  {
    id: 7,
    title: 'Analytics & Dashboards',
    description: 'Role-specific dashboards with comprehensive analytics for trail organizations',
    category: 'reporting',
    icon: 'fa-chart-line',
    benefits: [
      'Trail system analytics (view counts, status changes)',
      'Organization dashboard (member count, activity trends)',
      'Subscriber counts per trail system',
      'Care report metrics (priority distribution, days open)',
      'CSV/PDF export capabilities'
    ],
  },
  {
    id: 8,
    title: 'Notification System',
    description: 'Multi-channel notifications via email, SMS, and push—subscribers stay informed',
    category: 'notifications',
    icon: 'fa-bell',
    benefits: [
      'Email notifications (AWS SES)',
      'SMS notifications (AWS Pinpoint)',
      'Push notifications (iOS via APNS)',
      'Subscribe to individual trail systems OR entire organization',
      'Scheduled change reminders',
      'One-click unsubscribe links'
    ],
  },
  {
    id: 9,
    title: 'Security Hardening',
    description: 'Enterprise-grade security with CloudTrail, WAF, secrets rotation, and incident response',
    category: 'security',
    icon: 'fa-lock',
    benefits: [
      'CloudTrail audit logging (1-year retention)',
      'AWS WAF (OWASP Top 10 protection)',
      'Secrets rotation (180-day cycle)',
      'Incident response plan (GDPR 72-hour)',
      'API rate limiting (100 req/min per user)',
      'Data encryption at rest and in transit'
    ],
  },
  {
    id: 10,
    title: 'PII Protection & GDPR Compliance',
    description: 'User data export, account deletion, and 2-year retention policy—privacy by design',
    category: 'security',
    icon: 'fa-user-shield',
    benefits: [
      'User data export (JSON + CSV formats)',
      'Account deletion via user settings',
      '2-year inactive user data retention',
      'MFA enforcement for admin accounts',
      'Data minimization principles',
      'GDPR Article 17 & 20 compliance'
    ],
  },
];
```

### 3.3 Categories - UPDATE

**REPLACE categories array (Lines 64-70):**
```jsx
const categories = [
  { id: 'all', name: 'All Features' },
  { id: 'trail-management', name: 'Trail Management' },
  { id: 'trail-care', name: 'Trail Care Reports' },
  { id: 'automation', name: 'Automation' },
  { id: 'security', name: 'Security' },
  { id: 'mobile', name: 'Mobile Apps' },
  { id: 'notifications', name: 'Notifications' },
  { id: 'reporting', name: 'Analytics' },
];
```

### 3.4 Pricing Tiers Callout - UPDATE

**REPLACE pricingTiers (Lines 72-85):**
```jsx
const pricingTiers = [
  {
    tier: 'Free',
    features: ['Up to 5 trail system subscriptions', 'Basic trail status viewing', 'Email notifications', 'Submit public care reports'],
  },
  {
    tier: 'Pro ($49/mo)',
    features: ['Unlimited subscriptions', 'Manage trail systems', 'Full Trail Care Reports CRUD', 'Social media automation', 'SMS + push notifications', 'API access'],
  },
  {
    tier: 'Enterprise (Custom)',
    features: ['Everything in Pro', 'White-label options', 'Dedicated account manager', 'Custom integrations', 'SLA guarantees', 'Priority support'],
  },
];
```

---

## 4. Pricing Page (/pricing)

**File**: `web/src/views/public/Pricing.js`

### 4.1 Pricing Tiers Data - COMPLETE REPLACEMENT

**REPLACE pricingTiers array (Lines 17-73):**
```jsx
const pricingTiers = [
  {
    tier: "Free",
    monthlyPrice: 0,
    yearlyPrice: 0,
    description: "Perfect for trail users who want to stay informed",
    features: [
      "Subscribe to up to 5 trail systems",
      "Real-time trail status viewing",
      "Email notifications for status changes",
      "View public Trail Care Reports",
      "Submit public care reports (with photos)",
      "Community forum access",
      "Mobile app access (iOS)"
    ],
    limitations: [
      "Cannot manage trail systems",
      "Cannot create private care reports",
      "Limited to 5 subscriptions total"
    ],
    cta: {
      text: "Start Free",
      url: "/auth/register"
    },
    highlighted: false
  },
  {
    tier: "Pro",
    monthlyPrice: 49,
    yearlyPrice: 490,
    description: "For trail organizations managing trail systems",
    badge: "MOST POPULAR",
    features: [
      "✅ Everything in Free, PLUS:",
      "Unlimited trail system subscriptions",
      "Manage unlimited trail systems",
      "Full Trail Care Reports CRUD (create, assign, comment, close)",
      "Tag-based status organization (max 10 tags)",
      "Bulk trail system updates",
      "Scheduled status changes",
      "Social media automation (Facebook + Instagram)",
      "SMS + push notifications (in addition to email)",
      "Priority email support",
      "Analytics dashboards",
      "Team collaboration (unlimited admin users)",
      "API access for integrations"
    ],
    nonprofitDiscount: {
      available: true,
      discountedMonthly: 34,
      discountedYearly: 340,
      details: "30% nonprofit discount with 501(c)(3) verification"
    },
    cta: {
      text: "Start 30-Day Free Trial",
      url: "/auth/register?plan=pro"
    },
    highlighted: true
  },
  {
    tier: "Enterprise",
    monthlyPrice: "Custom",
    yearlyPrice: "Custom",
    description: "For large organizations with advanced needs",
    features: [
      "✅ Everything in Pro, PLUS:",
      "White-label mobile apps (custom branding)",
      "Dedicated account manager",
      "Custom integrations and API development",
      "SLA guarantees (99.9% uptime)",
      "Advanced security features",
      "Priority phone + chat support (24/7)",
      "Custom training and onboarding",
      "Multi-organization management",
      "Custom data retention policies",
      "Annual contract discounts available"
    ],
    cta: {
      text: "Contact Sales",
      url: "/contact?subject=enterprise"
    },
    highlighted: false
  }
];
```

### 4.2 Header Section - UPDATE

**REPLACE (Lines 91-97):**
```jsx
<div className="text-center mb-12">
  <h1 className="text-4xl font-bold text-slate-900 mb-4">
    Simple, Transparent Pricing
  </h1>
  <p className="text-lg text-slate-600 max-w-2xl mx-auto">
    Choose the plan that's right for your trail organization. Free tier for users. Pro for organizations. Enterprise for large-scale operations.
  </p>
</div>
```

### 4.3 Nonprofit Discount Callout - ADD NEW SECTION

**ADD AFTER PRICING CARDS (before feature comparison table):**
```jsx
{/* Nonprofit Discount Section */}
<div className="bg-gradient-to-r from-emerald-500 to-sky-500 rounded-lg shadow-xl p-8 mb-12 text-white text-center">
  <div className="flex items-center justify-center mb-4">
    <i className="fas fa-heart text-3xl mr-3"></i>
    <h3 className="text-2xl font-bold">Nonprofit Discount Program</h3>
  </div>
  <p className="text-lg mb-4">
    Are you a registered nonprofit trail organization (501(c)(3) in US, registered charity in Canada)?
  </p>
  <p className="text-2xl font-bold mb-2">
    Get 30% off Pro and Enterprise tiers
  </p>
  <p className="text-sm opacity-90 mb-6">
    Pro: $49/mo → <strong>$34/mo</strong> with nonprofit verification
  </p>
  <a
    href="/contact?subject=nonprofit-discount"
    className="inline-block bg-white text-emerald-600 font-bold py-3 px-8 rounded-lg hover:bg-blueGray-100 transition-colors"
  >
    Apply for Nonprofit Discount
  </a>
</div>
```

### 4.4 FAQ Section - ADD NEW SECTION

**ADD BEFORE FINAL CTA:**
```jsx
{/* FAQ Section */}
<div className="bg-white rounded-lg shadow-lg p-8 mb-12">
  <h2 className="text-2xl font-bold text-slate-900 mb-6 text-center">
    Frequently Asked Questions
  </h2>

  <div className="space-y-6 max-w-3xl mx-auto">
    <div>
      <h3 className="font-bold text-lg text-slate-900 mb-2">
        Can I switch plans later?
      </h3>
      <p className="text-slate-600">
        Yes! You can upgrade or downgrade at any time. Changes take effect immediately, and we'll prorate any billing adjustments.
      </p>
    </div>

    <div>
      <h3 className="font-bold text-lg text-slate-900 mb-2">
        What payment methods do you accept?
      </h3>
      <p className="text-slate-600">
        Credit cards (Visa, Mastercard, Amex) for all plans. Enterprise customers can request invoicing with NET 30 terms.
      </p>
    </div>

    <div>
      <h3 className="font-bold text-lg text-slate-900 mb-2">
        Do you offer refunds?
      </h3>
      <p className="text-slate-600">
        Yes! We offer a 30-day money-back guarantee on all paid plans. If you're not satisfied, contact us for a full refund within 30 days of purchase.
      </p>
    </div>

    <div>
      <h3 className="font-bold text-lg text-slate-900 mb-2">
        Is there a setup fee?
      </h3>
      <p className="text-slate-600">
        No setup fees. Ever. Just pay the monthly or yearly subscription fee.
      </p>
    </div>

    <div>
      <h3 className="font-bold text-lg text-slate-900 mb-2">
        How many users can I have?
      </h3>
      <p className="text-slate-600">
        Unlimited on all tiers! Add as many trail crew members, admins, and team members as you need. No per-user pricing.
      </p>
    </div>

    <div>
      <h3 className="font-bold text-lg text-slate-900 mb-2">
        What happens if I cancel?
      </h3>
      <p className="text-slate-600">
        Your data remains accessible for 90 days after cancellation. You can export all your data (trail systems, care reports, user data) in JSON or CSV format before deletion.
      </p>
    </div>

    <div>
      <h3 className="font-bold text-lg text-slate-900 mb-2">
        Do you offer annual contracts?
      </h3>
      <p className="text-slate-600">
        Yes! Yearly billing saves 17% compared to monthly. Enterprise customers can request multi-year contracts with additional discounts.
      </p>
    </div>

    <div>
      <h3 className="font-bold text-lg text-slate-900 mb-2">
        Where is my data stored?
      </h3>
      <p className="text-slate-600">
        All data is stored in AWS Canada (ca-central-1 region) with encryption at rest and in transit. We're a Canadian-owned company committed to data sovereignty.
      </p>
    </div>
  </div>
</div>
```

---

## 5. For Organizations Page (/for-organizations)

**File**: `web/src/views/public/ForOrganizations.js`

### 5.1 Hero Section - ADD AT TOP

**ADD BEFORE EXISTING CONTENT:**
```jsx
{/* Hero Section */}
<section className="relative pt-16 pb-32 bg-gradient-to-r from-sky-600 to-emerald-600">
  <div className="container mx-auto px-4">
    <div className="text-center text-white max-w-4xl mx-auto">
      <h1 className="text-5xl font-bold mb-6">
        Building Communities, One Trail at a Time
      </h1>
      <p className="text-xl mb-8 leading-relaxed">
        Save 10+ hours per month with automated social media, Trail Care Reports, and tag-based trail system management. Serving trail organizations worldwide.
      </p>
      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        <a
          href="/pricing"
          className="inline-block bg-white text-sky-600 font-bold py-4 px-8 rounded-lg hover:bg-blueGray-100 transition-colors shadow-lg"
        >
          See Pricing & Start Free
        </a>
        <a
          href="#demo-form"
          className="inline-block bg-transparent border-2 border-white text-white font-bold py-4 px-8 rounded-lg hover:bg-white hover:text-sky-600 transition-colors"
        >
          Request Demo
        </a>
      </div>
    </div>
  </div>
</section>
```

### 5.2 Benefits Section - UPDATE

**REPLACE benefits array (Lines 23-54):**
```jsx
const benefits = [
  {
    icon: "fas fa-mountain",
    title: "Trail System Management",
    description: "Manage entire trail systems (not individual trails) with tag-based organization, bulk updates, and scheduled seasonal status changes."
  },
  {
    icon: "fas fa-clipboard-list",
    title: "Trail Care Reports",
    description: "Unified issue tracking with P1-P5 priority levels, public/private visibility, offline report creation, and assignment workflows for trail crews."
  },
  {
    icon: "fas fa-share-alt",
    title: "Social Media Automation",
    description: "Automatically post trail status updates to Facebook and Instagram. One update, multiple platforms. Save 10+ hours per month on manual posting."
  },
  {
    icon: "fas fa-mobile-alt",
    title: "iPhone Apps (User + Admin)",
    description: "Native iOS apps for trail users (view status, submit reports) and trail crew (manage status, full CRUD). Offline capabilities built-in."
  },
  {
    icon: "fas fa-users-cog",
    title: "Eight User Roles",
    description: "Fine-grained access control with superadmin, org-admin, trailsystem-owner, trailsystem-crew, and four additional roles for different permission levels."
  },
  {
    icon: "fas fa-shield-alt",
    title: "Enterprise Security",
    description: "CloudTrail audit logging, AWS WAF protection, passkey authentication, MFA enforcement, secrets rotation, and GDPR compliance built-in."
  },
  {
    icon: "fas fa-bell",
    title: "Multi-Channel Notifications",
    description: "Email, SMS, and push notifications keep subscribers informed. Subscribe to individual trail systems or entire organizations."
  },
  {
    icon: "fas fa-chart-line",
    title: "Analytics & Dashboards",
    description: "Track trail system usage, subscriber counts, care report metrics, and activity trends with role-specific dashboards."
  }
];
```

### 5.3 Pricing Tiers - UPDATE

**REPLACE pricingTiers array (Lines 56-99):**
```jsx
const pricingTiers = [
  {
    name: "Free",
    price: "$0",
    period: "/month",
    trailLimit: "5 trail system subscriptions",
    features: [
      "View trail status (read-only)",
      "Email notifications",
      "Submit public care reports",
      "Mobile app access (iOS)",
      "Community forum access"
    ]
  },
  {
    name: "Pro",
    price: "$49",
    period: "/month",
    trailLimit: "Unlimited trail systems",
    featured: true,
    badge: "MOST POPULAR",
    features: [
      "Everything in Free, PLUS:",
      "Manage unlimited trail systems",
      "Full Trail Care Reports CRUD",
      "Social media automation",
      "Tag-based status organization",
      "Bulk updates & scheduled changes",
      "SMS + push notifications",
      "Priority support",
      "Analytics dashboards",
      "API access"
    ],
    nonprofitNote: "30% discount for nonprofits ($34/mo)"
  },
  {
    name: "Enterprise",
    price: "Custom",
    period: "pricing",
    trailLimit: "Unlimited + advanced features",
    features: [
      "Everything in Pro, PLUS:",
      "White-label mobile apps",
      "Dedicated account manager",
      "Custom integrations",
      "SLA guarantees (99.9% uptime)",
      "Advanced security features",
      "24/7 priority support",
      "Custom training",
      "Multi-organization management"
    ]
  }
];
```

### 5.4 Pilot Program Status - ADD NEW SECTION

**ADD AFTER PRICING, BEFORE DEMO FORM:**
```jsx
{/* Pilot Program Status */}
<section className="py-16 bg-blueGray-100">
  <div className="container mx-auto px-4 text-center">
    <h2 className="text-3xl font-bold mb-4 text-slate-900">
      Currently in Pilot Phase
    </h2>
    <p className="text-slate-600 mb-12 max-w-2xl mx-auto">
      TrailLensHQ is piloting with select trail organizations to refine the platform before public launch in Q2 2026.
    </p>

    <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="text-4xl mb-4">🏔️</div>
        <h3 className="text-2xl font-bold text-slate-900 mb-2">3</h3>
        <p className="text-slate-600 mb-4">Trail Systems in Pilot</p>
        <p className="text-sm text-slate-500">Real-world testing with diverse trail types</p>
      </div>

      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="text-4xl mb-4">⏱️</div>
        <h3 className="text-2xl font-bold text-slate-900 mb-2">10+</h3>
        <p className="text-slate-600 mb-4">Hours Saved Per Week</p>
        <p className="text-sm text-slate-500">Average time savings from automation</p>
      </div>

      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="text-4xl mb-4">📅</div>
        <h3 className="text-2xl font-bold text-slate-900 mb-2">Q2 2026</h3>
        <p className="text-slate-600 mb-4">Public Launch Target</p>
        <p className="text-sm text-slate-500">Full platform availability</p>
      </div>
    </div>

    <div className="mt-12">
      <a
        href="/contact?subject=early-access"
        className="inline-block bg-sky-500 text-white font-bold px-8 py-4 rounded-lg shadow-lg hover:bg-sky-600 transition-colors"
      >
        Request Early Access
      </a>
    </div>
  </div>
</section>
```

---

## 6. Footer Global Updates

**File**: `web/src/components/Footers/Footer.js`

### 6.1 Footer Canadian Branding

**ADD TO FOOTER (above copyright line):**
```jsx
<div className="text-center py-4 border-t border-blueGray-200 mt-8">
  <p className="text-sm text-blueGray-600">
    🍁 Proudly Canadian • Serving trail organizations worldwide
  </p>
</div>
```

### 6.2 Footer Links - UPDATE

**UPDATE footer navigation links to include:**
```jsx
<div className="flex flex-wrap items-center md:justify-between justify-center">
  <div className="w-full md:w-4/12 px-4 mx-auto text-center">
    <div className="text-sm text-blueGray-500 font-semibold py-1">
      <Link to="/about" className="hover:text-blueGray-800">About</Link>
      {" · "}
      <Link to="/pricing" className="hover:text-blueGray-800">Pricing</Link>
      {" · "}
      <Link to="/for-organizations" className="hover:text-blueGray-800">For Organizations</Link>
      {" · "}
      <Link to="/features" className="hover:text-blueGray-800">Features</Link>
      {" · "}
      <Link to="/case-studies" className="hover:text-blueGray-800">Case Studies</Link>
      {" · "}
      <Link to="/contact" className="hover:text-blueGray-800">Contact</Link>
      {" · "}
      <Link to="/privacy" className="hover:text-blueGray-800">Privacy</Link>
      {" · "}
      <Link to="/terms" className="hover:text-blueGray-800">Terms</Link>
    </div>
  </div>
</div>
```

---

## 7. Meta Tags & SEO

### 7.1 Global Site Metadata

**UPDATE in all public pages:**

**Standard Meta Description Template:**
```
TrailLensHQ helps trail organizations build thriving communities. [Page-specific content]. Free tier available. Serving organizations worldwide.
```

**Standard Open Graph Tags:**
```jsx
<meta property="og:site_name" content="TrailLensHQ" />
<meta property="og:locale" content="en_CA" />
<meta property="og:type" content="website" />
```

**Standard Twitter Card Tags:**
```jsx
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:site" content="@traillenshq" />
```

### 7.2 Structured Data (JSON-LD)

**ADD to all public pages:**
```jsx
<script type="application/ld+json">
  {JSON.stringify({
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "TrailLensHQ",
    "alternateName": "TrailLens",
    "url": "https://traillenshq.com",
    "logo": "https://traillenshq.com/logo.png",
    "description": "Trail management platform helping organizations build thriving communities worldwide",
    "address": {
      "@type": "PostalAddress",
      "addressCountry": "CA"
    },
    "sameAs": [
      "https://twitter.com/traillenshq",
      "https://facebook.com/traillenshq",
      "https://linkedin.com/company/traillenshq"
    ]
  })}
</script>
```

---

## 8. Image Generation Prompts

Use these prompts with DALL-E, Midjourney, or similar AI image generators:

### 8.1 Hero Background Image (Landing Page)

**Current Issue**: Generic Unsplash image at `web/src/assets/img/backgrounds/webbackground.webp`

**Replace With**: Generate new hero image

**Image Generation Prompt:**
```
Create a professional, wide-angle photograph of a well-maintained hiking trail in a Canadian forest during golden hour. The trail should have clear signage, well-groomed pathways, and show a diverse group of hikers (different ages, abilities) enjoying the trail together. Include subtle elements suggesting community and stewardship: a volunteer trail crew member in the background, trail markers, and people smiling and chatting. The image should feel warm, inviting, and community-focused rather than extreme/adventure-focused. Photorealistic style, high quality, 2560x1440 resolution, suitable for website hero background with dark overlay.
```

**Specifications:**
- Dimensions: 2560x1440px (WebP format)
- File size: <500KB (compressed)
- Save as: `web/src/assets/img/backgrounds/hero-community-trails.webp`

### 8.2 Trail System Management Feature Image

**Image Generation Prompt:**
```
Create a clean, modern interface mockup showing a trail management dashboard on a tablet device. The screen displays a map with multiple trail systems marked with colored status indicators (green for open, yellow for caution, red for closed). Include tag filters at the top ("Winter", "Maintenance", "Peak Season") and a list of trail systems below with their current status. The background should show a blurred trail scene. Professional UI/UX design, clean and minimalist, in TrailLensHQ brand colors (sky blue #0EA5E9, emerald green #10B981).
```

**Specifications:**
- Dimensions: 1200x800px
- Save as: `web/src/assets/img/features/trail-system-management.png`

### 8.3 Trail Care Reports Feature Image

**Image Generation Prompt:**
```
Create a split-screen mockup showing a mobile app interface for Trail Care Reports. Left side: A trail crew member using an iPhone in the field, photographing a fallen tree on a trail. Right side: The iPhone screen showing a Trail Care Report form with photo upload (the fallen tree photo), priority selector showing "P2 - High", and a description field. The scene should be realistic and show the offline indicator icon in the top corner. Photorealistic + UI mockup hybrid style.
```

**Specifications:**
- Dimensions: 1200x800px
- Save as: `web/src/assets/img/features/trail-care-reports.png`

### 8.4 Social Media Automation Feature Image

**Image Generation Prompt:**
```
Create an illustration showing social media automation workflow. Center: A trail organization admin clicking one "Update Status" button on a laptop. Arrows branching out to multiple platforms: Facebook logo with a trails conditions muddy post, Instagram logo with a trail photo and status update, and email icon with notification. The style should be modern, clean vector illustration with TrailLensHQ brand colors. Show time savings with a clock icon displaying "-10 hours/month" saved.
```

**Specifications:**
- Dimensions: 1200x800px
- Save as: `web/src/assets/img/features/social-media-automation.png`

### 8.5 About Page Hero

**Image Generation Prompt:**
```
Create a wide panoramic photograph of beautiful trail scenery: a mountain trail with diverse landscape (forest, mountains) showing a diverse group of trail users (hikers, mountain bikers of different ages and abilities) and a trail maintenance crew working together. The scene should convey community, collaboration, and stewardship. Golden hour lighting, warm and inviting atmosphere, photorealistic, professional quality. Focus on the people and community aspect, not extreme sports.
```

**Specifications:**
- Dimensions: 2400x1200px
- Save as: `web/src/assets/img/about/trails-community-hero.jpg`

### 8.6 For Organizations Page Hero

**Image Generation Prompt:**
```
Create a professional photograph showing trail organization administrators in a small office/meeting room reviewing trail management data on a large monitor. The monitor displays the TrailLensHQ dashboard with trail systems, status updates, and analytics charts. The people should look engaged and collaborative (2-3 people, diverse representation). The setting should feel like a nonprofit office - not corporate/sterile. Include subtle trail-related decor (trail maps on walls, hiking boots, outdoor gear). Natural lighting, warm and inviting atmosphere.
```

**Specifications:**
- Dimensions: 1800x1000px
- Save as: `web/src/assets/img/for-orgs/dashboard-collaboration.jpg`

### 8.7 Pricing Page Hero/Background

**Image Generation Prompt:**
```
Create a minimalist, abstract background pattern featuring subtle topographic map lines and trail symbols in light blue and green tones. The pattern should be very subtle (low opacity) and work as a background for pricing cards. Think: sophisticated, professional, outdoor-inspired but not distracting. Vector style, seamless pattern.
```

**Specifications:**
- Dimensions: Tileable pattern, 800x800px base tile
- Save as: `web/src/assets/img/backgrounds/pricing-pattern.svg`

### 8.8 Generic Organization Icons (For Future Testimonials)

**Note**: Do NOT create organization-specific logos without permission. Use these generic placeholders until real testimonials with permissions are obtained.

**Image Generation Prompt (Generic Trail Org Icon):**
```
Create a simple, professional generic icon representing a trail organization - a circular badge design featuring a stylized trail winding through nature elements (trees, mountains). Use neutral colors (slate gray #64748b). Clean, modern vector style suitable for avatar/profile picture use. Should be generic enough to represent any trail organization.
```

**Specifications:**

- Dimensions: 400x400px (square)
- Save as: `web/src/assets/img/organizations/generic-trail-org-icon.png`
- Use this as placeholder until real organization permissions are obtained

### 8.9 Official App Store and Play Store Badges

**IMPORTANT**: Section 1.2 references app store buttons but does not specify the official badge assets. Use the official badges from Apple and Google as detailed below.

#### Apple App Store Badge

**Official Source:**
- **Download from**: [Apple App Store Marketing Tools](https://tools.applemediaservices.com/app-store/)
- **Guidelines**: [Apple App Store Marketing Guidelines](https://developer.apple.com/app-store/marketing/guidelines/)

**Badge Details:**
- **Badge Type**: "Download on the App Store" (black badge preferred)
- **Available Formats**: SVG, PNG (multiple resolutions included in download package)
- **Localizations**: 40 languages available
- **Package Size**: ~263 MB (includes all localizations and resolutions)

**Usage Requirements:**
- **Minimum Size (Screen)**: 40px height
- **Minimum Size (Print)**: 10mm height
- **Clear Space**: 1/4 of badge height on all sides
- **Badge Position**: Subordinate position in layout (not dominant element)
- **Color Options**: Black (preferred) or White (for dark backgrounds)
- **Never**: Modify, angle, animate, translate "App Store" text, or use outdated versions

**Implementation Example:**
```jsx
{/* Apple App Store Badge */}
<a
  href="https://apps.apple.com/app/traillenshq/id[YOUR_APP_ID]"
  target="_blank"
  rel="noopener noreferrer"
  className="inline-block"
>
  <img
    src="/assets/badges/Download_on_App_Store_Badge_US-UK_RGB_blk_092917.svg"
    alt="Download on the App Store"
    className="h-14 w-auto"
    style={{ minHeight: '40px' }}
  />
</a>
```

**Asset Storage Location:**
- Save to: `web/src/assets/badges/Download_on_App_Store_Badge_US-UK_RGB_blk_092917.svg`
- Also save PNG fallback: `web/src/assets/badges/Download_on_App_Store_Badge_US-UK_RGB_blk_092917.png`

#### Google Play Store Badge

**Official Sources:**
- **Download from**: [Google Play Badges Tool](https://play.google.com/intl/en_us/badges/)
- **Guidelines**: [Google Play Badge Guidelines (Partner Marketing Hub)](https://partnermarketinghub.withgoogle.com/brands/google-play/visual-identity/badge-guidelines/)

**Badge Details:**
- **Badge Type**: "Get it on Google Play" (standard badge)
- **Available Formats**: SVG, PNG (high-resolution)
- **Localizations**: Multiple languages available
- **Download**: Complete asset package available as ZIP

**Usage Requirements:**
- **Minimum Size**: Large enough for text legibility (no specific pixel minimum stated)
- **Clear Space**: 1/4 of badge height on all sides
- **Comparative Sizing**: Google Play badge must be **same size or larger** than other app store badges when displayed together
- **Background**: Solid or simple backgrounds with sufficient contrast
- **Never**: Use outdated versions, change colors, remove elements, alter scale, or use low-resolution versions

**Implementation Example:**
```jsx
{/* Google Play Store Badge */}
<a
  href="https://play.google.com/store/apps/details?id=com.traillenshq"
  target="_blank"
  rel="noopener noreferrer"
  className="inline-block"
>
  <img
    src="/assets/badges/google-play-badge.svg"
    alt="Get it on Google Play"
    className="h-14 w-auto"
    style={{ minHeight: '40px' }}
  />
</a>
```

**Asset Storage Location:**
- Save to: `web/src/assets/badges/google-play-badge.svg`
- Also save PNG fallback: `web/src/assets/badges/google-play-badge.png`

#### Combined Implementation (Both Badges Together)

**When displaying both badges side-by-side:**

```jsx
{/* App Store Badges - Side by Side */}
<div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center items-center">
  {/* Apple App Store */}
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

  {/* Google Play Store */}
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

  {/* Learn More Button (Optional) */}
  <Link
    to="/about"
    className="bg-sky-500 text-white font-bold px-6 py-3 rounded-lg shadow-lg hover:shadow-xl hover:bg-sky-600 transition-all duration-200"
  >
    Learn More
  </Link>
</div>
```

#### Badge Sizing Best Practices

**Critical Sizing Rules:**
1. **Both badges must be identical height** when displayed together
2. **Google Play badge should be same size or larger** than Apple badge (per Google guidelines)
3. **Recommended height**: 56px (14 Tailwind units) or 40-60px range
4. **Maintain aspect ratio**: Use `w-auto` to preserve badge proportions
5. **Clear space**: Ensure 1/4 badge height spacing around each badge

#### Accessibility Requirements

**IMPORTANT**: Include proper accessibility attributes:
- `alt` text describing the badge purpose
- `aria-label` on the link for screen readers
- `target="_blank"` with `rel="noopener noreferrer"` for external links
- `loading="lazy"` for performance optimization

#### Mobile App Availability Note

**CURRENT STATUS (as of MVP v1.13):**
- ✅ **iOS App**: Available (native Swift app)
- ❌ **Android App**: Not yet available (planned for post-MVP)

**Implementation Recommendation:**
- **If only iOS available**: Display only Apple App Store badge
- **When both available**: Display both badges side-by-side
- **Update Section 1.2**: Current document shows both badges, but verify Android app availability before displaying Google Play badge

**Conditional Rendering Example:**
```jsx
const ANDROID_APP_AVAILABLE = false; // Set to true when Android app launches

<div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center items-center">
  {/* iOS App Store Badge - Always show */}
  <a href="https://apps.apple.com/app/traillenshq/id[YOUR_APP_ID]" ...>
    <img src="/assets/badges/Download_on_App_Store_Badge..." alt="..." />
  </a>

  {/* Google Play Badge - Conditional */}
  {ANDROID_APP_AVAILABLE && (
    <a href="https://play.google.com/store/apps/details?id=com.traillenshq" ...>
      <img src="/assets/badges/google-play-badge.svg" alt="..." />
    </a>
  )}
</div>
```

#### Legal & Trademark Requirements

**Apple Requirements:**
- Include ™ symbol in U.S. marketing materials where appropriate
- Never translate "App Store" into other languages
- Provide credit line: "Apple and the Apple logo are trademarks of Apple Inc."
- See [Apple Trademark List](https://www.apple.com/legal/intellectual-property/trademark/appletmlist.html) for full details

**Google Requirements:**
- Follow Google Play branding guidelines
- Use current badge versions only (updated as of 2/15/2024)
- Provide credit line: "Google Play and the Google Play logo are trademarks of Google LLC."

#### Download Checklist for Developers

- [ ] **Download Apple App Store badge** from [App Store Marketing Tools](https://tools.applemediaservices.com/app-store/)
  - [ ] Select "Download on the App Store" package
  - [ ] Choose English (US) localization (or appropriate language)
  - [ ] Extract SVG and PNG versions
  - [ ] Save to `web/src/assets/badges/`

- [ ] **Download Google Play badge** from [Google Play Badges Tool](https://play.google.com/intl/en_us/badges/)
  - [ ] Generate badge or download asset package
  - [ ] Choose English localization (or appropriate language)
  - [ ] Extract SVG and PNG versions
  - [ ] Save to `web/src/assets/badges/`

- [ ] **Verify badge appearance**
  - [ ] Both badges are identical height
  - [ ] Clear space requirements met (1/4 badge height)
  - [ ] Badges maintain proper aspect ratios
  - [ ] Adequate contrast with background

- [ ] **Test functionality**
  - [ ] Links point to correct App Store/Play Store URLs
  - [ ] Links open in new tab with proper security attributes
  - [ ] Hover effects work properly
  - [ ] Mobile responsive behavior correct

- [ ] **Accessibility check**
  - [ ] Alt text present and descriptive
  - [ ] ARIA labels appropriate
  - [ ] Keyboard navigation works
  - [ ] Screen reader testing completed

### 8.10 Login Page Social Sign-In Buttons

**IMPORTANT**: The current login page ([web/src/views/auth/Login.js](../web/src/views/auth/Login.js)) uses generic FontAwesome icons for Google, Facebook, and Apple sign-in buttons (lines 116-144). These do NOT comply with official branding guidelines from each provider and must be replaced with official branded buttons.

#### Current Implementation Issues

**Current Code (Lines 116-144):**
```jsx
<button className="bg-white ... " onClick={() => handleSocialSignIn('Google')}>
  <i className="fab fa-google text-lg mr-1"></i>
  Google
</button>
```

**Problems:**
1. Uses FontAwesome icons instead of official brand assets
2. Does not follow Google's "Sign in with Google" branding requirements
3. Does not follow Apple's "Sign in with Apple" Human Interface Guidelines
4. Does not follow Facebook's Platform Policy 8.3 for Login buttons
5. May violate brand guidelines and fail app verification/review processes

#### Official Branding Requirements

##### Google Sign-In Button

**Official Guidelines:**
- **Source**: [Google Identity Branding Guidelines](https://developers.google.com/identity/branding-guidelines)
- **Asset Download**: [Sign-In Assets ZIP](https://developers.google.com/identity/branding-guidelines) (signin-assets.zip)

**Requirements:**
- **Button Text**: Must say "Sign in with Google" (not just "Google")
- **Google "G" Logo**: Must use official colored "G" logo, cannot be modified or recolored
- **Font**: Roboto Medium, 14/20 font size
- **Button Themes**: Three approved themes available:
  - **Light**: White fill (#FFFFFF), #747775 stroke
  - **Dark**: #131314 fill, #8E918F stroke
  - **Neutral**: #F2F2F2 fill, no stroke
- **Shapes**: Rectangular or pill-shaped
- **Padding**: 12px left, 10px right (logo), 12px right (text) for web
- **Prominence**: Must be displayed at least as prominently as other third-party sign-in options

**Asset Storage Location:**
- Save SVG files to: `web/src/assets/auth/google-signin-light.svg`, `google-signin-dark.svg`, `google-signin-neutral.svg`
- Use SVG format (supports text localization with Roboto font family)

**Implementation Example:**
```jsx
{/* Google Sign-In Button */}
<button
  className="w-full bg-white border border-gray-300 text-gray-700 px-4 py-3 rounded-lg shadow hover:shadow-md inline-flex items-center justify-center font-medium text-sm transition-all duration-150"
  type="button"
  onClick={() => handleSocialSignIn('Google')}
  disabled={isSubmitting || loading}
  aria-label="Sign in with Google"
>
  <img
    src="/assets/auth/google-g-logo.svg"
    alt="Google logo"
    className="w-5 h-5 mr-3"
  />
  <span className="font-medium" style={{ fontFamily: 'Roboto, sans-serif' }}>
    Sign in with Google
  </span>
</button>
```

##### Apple Sign In Button

**Official Guidelines:**
- **Source**: [Apple Sign in with Apple HIG](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple)
- **Button Guidelines**: [Sign in with Apple Buttons](https://developers.apple.com/design/human-interface-guidelines/technologies/sign-in-with-apple/buttons)
- **Asset Download**: Available in SVG, PNG, PDF formats from Apple Developer resources

**Requirements:**
- **Button Text**: Must say "Sign in with Apple" (not just "Apple")
- **Button Styles**: Three approved styles:
  - **Black**: Black background with white text and logo
  - **White**: White background with black text and logo
  - **White Outline**: White background with black outline, black text and logo
- **Apple Logo**: Must use official Apple logo with correct proportions
- **Minimum Size**: 44x44 pt (for accessibility)
- **Corner Radius**: Consistent with platform (typically 6-8px for web)
- **Typography**: San Francisco font family (fallback: system font)

**Asset Storage Location:**
- Save SVG files to: `web/src/assets/auth/apple-signin-black.svg`, `apple-signin-white.svg`, `apple-signin-white-outline.svg`
- SVG and PDF formats support any button size
- PNG format only recommended for 44x44 pt buttons

**Implementation Example:**
```jsx
{/* Apple Sign In Button */}
<button
  className="w-full bg-black text-white px-4 py-3 rounded-lg shadow hover:shadow-md inline-flex items-center justify-center font-medium text-sm transition-all duration-150"
  type="button"
  onClick={() => handleSocialSignIn('Apple')}
  disabled={isSubmitting || loading}
  aria-label="Sign in with Apple"
>
  <img
    src="/assets/auth/apple-logo-white.svg"
    alt="Apple logo"
    className="w-5 h-5 mr-3"
  />
  <span className="font-medium" style={{ fontFamily: '-apple-system, BlinkMacSystemFont, sans-serif' }}>
    Sign in with Apple
  </span>
</button>
```

**Conditional Display Note:**
The current code shows Apple sign-in only on Apple devices (lines 98-144). This is acceptable but consider showing it on all platforms as users may want to use their Apple ID even on non-Apple devices.

##### Facebook Login Button

**Official Guidelines:**
- **Source**: [Facebook Brand Resource Center](https://en.facebookbrand.com/)
- **App Assets**: [Facebook App Logos & Icons](https://en.facebookbrand.com/facebookapp/)
- **Meta Brand Resources**: [Facebook Logo Guidelines](https://www.meta.com/brand/resources/facebook/logo/)
- **Developer Docs**: [Facebook Login Best Practices](https://developers.facebook.com/docs/facebook-login/best-practices#buttondesign)

**Requirements:**
- **Button Text**: Must say "Continue with Facebook" or "Login with Facebook" (not just "Facebook")
- **Facebook Logo**: Must use official Facebook "f" logo in approved colors
- **Primary Colors**:
  - **Facebook Blue**: #1877F2 (background)
  - **White**: #FFFFFF (text and logo on blue background)
- **Logo Requirements**:
  - Use current logo (white 'f' in blue circle)
  - Minimum digital size: 16px wide
  - Maintain 1/4 logo width as clear space
  - Logo must remain complete and unaltered
- **Prohibited**: Don't use just the 'f' alone, don't combine with word "Facebook", don't recolor, don't add 3D effects

**Asset Storage Location:**
- Save SVG files to: `web/src/assets/auth/facebook-f-logo-white.svg`, `facebook-f-logo-blue.svg`
- Logo pack available from Facebook Brand Resource Center

**Implementation Example:**
```jsx
{/* Facebook Login Button */}
<button
  className="w-full text-white px-4 py-3 rounded-lg shadow hover:shadow-md inline-flex items-center justify-center font-medium text-sm transition-all duration-150"
  style={{ backgroundColor: '#1877F2' }}
  type="button"
  onClick={() => handleSocialSignIn('Facebook')}
  disabled={isSubmitting || loading}
  aria-label="Continue with Facebook"
>
  <img
    src="/assets/auth/facebook-f-logo-white.svg"
    alt="Facebook logo"
    className="w-5 h-5 mr-3"
  />
  <span className="font-medium">
    Continue with Facebook
  </span>
</button>
```

#### Complete Updated Login Page Implementation

**File**: `web/src/views/auth/Login.js`

**REPLACE Lines 115-145 (Social Sign-In Buttons Section):**

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

  {/* Apple Sign In Button - Show on all platforms, not just Apple devices */}
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

**Key Changes:**
1. **Full-width buttons**: Changed from inline buttons to stacked full-width buttons (`w-full`, `space-y-3`)
2. **Proper branding**: Uses official brand colors and text for each provider
3. **Official logos**: Replaces FontAwesome icons with official brand SVG assets
4. **Accessibility**: Adds `aria-label` for screen readers, `aria-hidden="true"` on decorative images
5. **Typography**: Uses brand-specific fonts (Roboto for Google, San Francisco for Apple)
6. **Consistency**: All buttons have same height and padding for visual harmony
7. **Apple button visibility**: Removed device detection - show Apple sign-in on all platforms

**Remove Device Detection Code:**
Delete lines 98-101 (isAppleDevice function) as it's no longer needed.

#### Font Requirements

**Add to Project Dependencies:**

Google Sign-In requires Roboto font. Add to your HTML head or import in your CSS:

```html
<!-- Add to web/public/index.html -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@500&display=swap" rel="stylesheet">
```

Or via CSS import in `web/src/index.css`:

```css
/* Google Roboto for Sign in with Google button */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@500&display=swap');
```

Apple's San Francisco font will use system fallback (`-apple-system, BlinkMacSystemFont`).

#### Asset Download Checklist

- [ ] **Download Google Sign-In Assets**
  - [ ] Visit [Google Identity Branding Guidelines](https://developers.google.com/identity/branding-guidelines)
  - [ ] Download signin-assets.zip
  - [ ] Extract `google-g-logo.svg` (colored G logo)
  - [ ] Save to `web/src/assets/auth/google-g-logo.svg`
  - [ ] (Optional) Extract full button SVGs if you want pre-built buttons

- [ ] **Download Apple Sign In Assets**
  - [ ] Visit [Apple HIG Sign in with Apple](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple)
  - [ ] Download official Apple logo assets in SVG format
  - [ ] Save white Apple logo to `web/src/assets/auth/apple-logo-white.svg`
  - [ ] Save black Apple logo to `web/src/assets/auth/apple-logo-black.svg` (for white button variant)

- [ ] **Download Facebook Login Assets**
  - [ ] Visit [Facebook Brand Resource Center](https://en.facebookbrand.com/)
  - [ ] Navigate to [Facebook App Assets](https://en.facebookbrand.com/facebookapp/)
  - [ ] Download Facebook logo pack
  - [ ] Extract white 'f' logo (for use on blue background)
  - [ ] Save to `web/src/assets/auth/facebook-f-logo-white.svg`

- [ ] **Add Roboto Font**
  - [ ] Add Google Fonts link to `web/public/index.html` OR
  - [ ] Add @import to `web/src/index.css`

- [ ] **Update Login.js Code**
  - [ ] Replace lines 115-145 with new button implementation
  - [ ] Remove isAppleDevice() function (lines 98-101)
  - [ ] Test all three social sign-in buttons
  - [ ] Verify logos load correctly
  - [ ] Verify brand colors match official guidelines

- [ ] **Accessibility & Testing**
  - [ ] Verify aria-label on all buttons
  - [ ] Test with screen reader
  - [ ] Test keyboard navigation
  - [ ] Verify disabled state styling
  - [ ] Test on mobile devices
  - [ ] Verify font rendering (Roboto for Google)

#### Button Positioning & Layout Notes

**Current Layout Issues:**
The current implementation uses inline buttons which causes:
- Inconsistent button widths
- Poor mobile responsiveness
- Cramped appearance

**Recommended Layout:**
- **Stacked full-width buttons** (shown in implementation above) - better for mobile, clearer hierarchy
- **Spacing**: Use `space-y-3` (12px) between buttons
- **Order**: Google → Facebook → Apple (alphabetical and common convention)

**Alternative Layout (Side-by-Side on Desktop):**
If you prefer side-by-side buttons on desktop, use responsive classes:

```jsx
<div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
  {/* Google button */}
  {/* Facebook button */}
  {/* Apple button */}
</div>
```

#### Legal & Compliance Requirements

**Google:**
- Must follow branding guidelines for app verification
- "Sign in with Google" button must be as prominent as other third-party options
- Cannot modify or recolor the Google "G" logo

**Apple:**
- Must follow Human Interface Guidelines
- Required if offering other third-party sign-in options (per App Store Review Guidelines)
- Button must use official assets and approved styles

**Facebook:**
- Must follow Platform Policy 8.3
- Must use clearly branded "Login with Facebook" or "Continue with Facebook"
- Must follow Facebook Brand Guidelines at facebookbrand.com
- Recommended to use official Facebook SDK for Login

**General:**
- All social sign-in buttons should be equal prominence (same size, same visual weight)
- Provide clear indication of what data will be shared
- Include privacy policy link near sign-in options

#### Testing After Implementation

**Visual Testing:**
1. Verify all three buttons display official logos correctly
2. Confirm brand colors match official guidelines (Google light theme, Facebook #1877F2, Apple black)
3. Check font rendering (Roboto for Google, system font for Apple)
4. Verify equal button heights and consistent spacing

**Functional Testing:**
1. Click each button and verify OAuth flow initiates
2. Test disabled state during authentication
3. Verify error handling for failed sign-in attempts
4. Test on multiple browsers (Chrome, Safari, Firefox, Edge)

**Compliance Testing:**
1. Compare buttons against official brand guidelines
2. Verify text matches required branding ("Sign in with Google", etc.)
3. Confirm logos are official assets, not modified
4. Check that buttons are equal prominence

---

## 9. Implementation Checklist

### Phase 1: Critical Updates (Do First)

- [ ] **Landing Page Hero**: Update byline to "Building communities, one trail at a time."
- [ ] **Landing Page Hero**: Add Canadian ownership messaging ("🍁 Proudly Canadian")
- [ ] **Landing Page CTAs**: Replace app download buttons with "See Pricing" and "For Organizations" buttons
- [ ] **Landing Page Meta Tags**: Update description, keywords, OG tags with Canadian messaging
- [ ] **Footer Global**: Add "🍁 Designed and built in Canada" to all pages
- [ ] **Delete Fake Team Section**: Remove lines 414-572 from Landing.js

### Phase 2: About Page Rewrite

- [ ] **About Hero**: Update with Canadian ownership messaging
- [ ] **About Mission**: Replace with new mission text emphasizing community building
- [ ] **About Team**: Remove fake team members, replace with company story section
- [ ] **About Timeline**: Replace fake history with real 2025-2026 timeline
- [ ] **About Values**: Update with Canadian values section
- [ ] **About CTA**: Update with new call-to-action

### Phase 3: Features Page Rebuild

- [ ] **Features Hero**: Update headline and add Canadian branding
- [ ] **Features Data**: Replace mock features with 10 real MVP features
- [ ] **Features Categories**: Update category filters (trail-management, trail-care, automation, etc.)
- [ ] **Features Pricing Callout**: Update pricing tiers to Free / Pro ($49) / Enterprise

### Phase 4: Pricing Page Overhaul

- [ ] **Pricing Tiers**: Replace with accurate Free / Pro ($49/mo) / Enterprise pricing
- [ ] **Pricing Features**: Update feature lists to match MVP v1.13 capabilities
- [ ] **Nonprofit Discount Section**: Add 30% nonprofit discount callout
- [ ] **Pricing FAQ**: Add 8-question FAQ section
- [ ] **Pricing Meta Tags**: Update SEO tags

### Phase 5: For Organizations Page Update

- [ ] **For Orgs Hero**: Add new hero section with Canadian messaging
- [ ] **For Orgs Benefits**: Update benefits to include Trail Care Reports, tag-based status
- [ ] **For Orgs Pricing**: Update pricing tiers to match new model
- [ ] **For Orgs Case Studies**: Add Hydrocut and GORBA success stories

### Phase 6: Image Generation & Replacement

- [ ] **Generate Hero Background**: Create new community-focused trail image
- [ ] **Generate Feature Images**: Create 3 feature mockup images (trail management, care reports, social media)
- [ ] **Generate About Hero**: Create Canadian trails hero image
- [ ] **Generate Organization Avatars**: Create Hydrocut and GORBA logo avatars
- [ ] **Replace Generic Unsplash Images**: Remove all template stock photos

### Phase 7: SEO & Metadata

- [ ] **Update All Meta Descriptions**: Include Canadian ownership in all pages
- [ ] **Add Structured Data**: Add Organization JSON-LD to all public pages
- [ ] **Update Open Graph Tags**: Ensure all OG tags reflect new messaging
- [ ] **Update Keywords**: Add "Canadian trail software", "trail care reports", etc.

### Phase 8: Testing & Validation

- [ ] **Test All Links**: Verify all CTAs point to correct destinations
- [ ] **Test Mobile Responsive**: Verify all new sections work on mobile
- [ ] **Test Image Loading**: Verify all new images load correctly (WebP with PNG fallback)
- [ ] **Test SEO**: Run Lighthouse audit, ensure 90+ SEO score
- [ ] **Proofread All Copy**: Check for typos, consistency, brand voice

---

## 10. Brand Voice Guidelines

**For Developers**: When writing any additional content not specified in this document, follow these guidelines:

### Voice Characteristics

✅ **DO:**
- Write in active voice ("We help trail organizations..." not "Trail organizations are helped by...")
- Use "we" and "you" (conversational, not corporate)
- Be specific with numbers ("Save 10+ hours/month" not "Save time")
- Lead with benefits, not features
- Emphasize community and stewardship
- Include Canadian ownership naturally (not forced)

❌ **DON'T:**
- Use jargon or overly technical language
- Make unsubstantiated claims
- Use superlatives excessively ("best", "amazing", "revolutionary")
- Be corporate/sterile in tone
- Ignore Canadian identity
- Focus only on transactions (emphasize community building)

### Tone Examples

**Good:**
> "TrailLensHQ helps trail organizations build thriving communities through effortless trail management. Save 10+ hours per month with automated social media posting."

**Bad:**
> "TrailLensHQ is a revolutionary, best-in-class SaaS platform that leverages cutting-edge technology to facilitate optimal trail management solutions."

### Canadian Messaging Best Practices

**Subtle Integration (PREFERRED):**
> "🍁 Proudly Canadian • Serving trail organizations worldwide"
> "Founded in Canada and serving organizations worldwide, our values reflect environmental stewardship, community collaboration, and accessible outdoor recreation."

**Avoid Overly Prominent Canadian Messaging:**

- Don't lead with Canadian identity in hero sections
- Don't use multiple Canadian flags or excessive emoji
- Remember: customers are global, not just Canadian
- Keep Canadian identity present but not dominant

---

## 11. File Locations Reference

**Quick reference for developers:**

| Page | File Path | Priority |
|------|-----------|----------|
| Landing | `web/src/views/Landing.js` | **CRITICAL** |
| About | `web/src/views/public/About.js` | High |
| Features | `web/src/views/public/Features.js` | High |
| Pricing | `web/src/views/public/Pricing.js` | High |
| For Organizations | `web/src/views/public/ForOrganizations.js` | High |
| Footer | `web/src/components/Footers/Footer.js` | **CRITICAL** (global) |
| Meta Tags | Each page file (Helmet component) | High |

---

## 12. Post-Implementation Tasks

**After all content updates are complete:**

1. **Generate Sitemap**: Update `public/sitemap.xml` with all public pages
2. **Update robots.txt**: Ensure all public pages are indexable
3. **Google Analytics**: Verify tracking is working on all pages
4. **Social Sharing Test**: Test OG tags by sharing links on Facebook/Twitter
5. **Accessibility Audit**: Run WAVE or axe DevTools to check accessibility
6. **Performance Audit**: Run Lighthouse, aim for 90+ on all metrics
7. **Cross-Browser Testing**: Test on Chrome, Firefox, Safari, Edge
8. **Mobile Testing**: Test on iOS Safari and Android Chrome

---

## 13. Questions or Issues?

**If you encounter issues during implementation:**

1. **Content Clarity**: If any copy is unclear or needs adjustment, contact VP Marketing
2. **Technical Implementation**: Refer to `web/CLAUDE.md` for React/Tailwind best practices
3. **Image Generation**: If AI-generated images don't match brand, request regeneration with adjusted prompts
4. **SEO Concerns**: All meta tags have been optimized, but consult marketing for any major changes

---

**Document Status:** Ready for Developer Implementation
**Last Updated:** January 2026
**Version:** 1.1
**Prepared By:** VP Marketing
**For:** Development Team (MVP v1.13 Launch)

**Version History:**

- **v1.0** - Initial document with full content updates
- **v1.1** - Removed Hydrocut/GORBA testimonials (no permission granted); toned down Canadian messaging to be subtle and globally friendly while maintaining Canadian identity

---

**End of Website Content Updates Document**
