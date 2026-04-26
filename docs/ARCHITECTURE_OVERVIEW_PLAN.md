# ARCHITECTURE_OVERVIEW.svg — Design Plan

## Goal

Create `planning/docs/ARCHITECTURE_OVERVIEW.svg` as a high-level companion to the detailed `ARCHITECTURE.svg` (v3.0). The overview should show *how pieces connect* at a glance — no cost annotations, no memory specs, no performance SLAs.

## Style Reference

- Base style on `planning/docs/backup/ARCHITECTURE_v4.svg` (v2.0 archetype)
- Plain white background (`#FFFFFF`) — no colored layer bands
- Box style: `rx="5"`, `stroke="#232F3E"`, `stroke-width="2"`, white text
- Title: 14px bold · Subtitle: 11px
- Arrows: `stroke="#232F3E"`, `stroke-width="1.5"`, simple triangle arrowhead marker

## Color Palette

| Category | Color |
|---|---|
| Clients / Frontend | `#4A90E2` (blue) |
| AWS Services | `#FF9900` (orange) |
| Lambda functions | `#9B59B6` (purple) |
| External services | `#7ED321` (green) |
| Disabled / future | `#95A5A6` (gray, dashed border) |
| Infrastructure / IaC | `#5D6D7E` (slate) |

## Layer Structure (9 layers, top → bottom)

| # | Layer | Components |
|---|---|---|
| 1 | Clients | iOS App · Android App · Web Browser (webui/) |
| 2 | CDN/Network | CloudFront + ACM · Route53 DNS · Amplify Hosting |
| 3 | API | API Gateway · Main API Lambda (FastAPI/Mangum) · Social Media Lambda (NestJS) |
| 4 | Event-Driven | Single box: "Event-Driven Lambdas ×9" — push, SMS, email, photo processor, SES forwarder, 4 Cognito triggers |
| 5 | Auth | Cognito User Pool (magic link + passkey · 4 auth triggers) |
| 6 | Data | DynamoDB (single table · 66 access patterns · 6 GSIs) · S3 Buckets (photos, assets, email) · Redis (disabled · future — dashed border) |
| 7 | Messaging | SNS Topics (condition change · alerts) · SES (email domain · receipt) · Secrets Manager |
| 8 | Infrastructure | VPC (private subnets) · CloudWatch + X-Ray · Pulumi IaC (infra/ + api-dynamo/) |
| 9 | External | APNS / FCM (push) · Facebook / Instagram · SMTP Relay |

**Removed from original plan:** WAF — not currently in use, omitted from overview.

## Key Arrows (14 connections)

| From | To | Label |
|---|---|---|
| iOS / Android / Web | CloudFront | HTTPS |
| CloudFront | API Gateway | cached requests |
| API Gateway | Main API Lambda | FastAPI handler |
| API Gateway | Social Media Lambda | NestJS handler |
| Main API Lambda | DynamoDB | read/write |
| Main API Lambda | Cognito User Pool | token validation |
| Main API Lambda | SNS Topics | publish events |
| Main API Lambda | S3 Buckets | photo upload URL |
| SNS Topics | Event-Driven Lambdas | trigger push/SMS/email |
| S3 Buckets | Event-Driven Lambdas | S3 event → photo-processor |
| Cognito User Pool | Event-Driven Lambdas | auth challenge triggers |
| Event-Driven Lambdas | SES | email send |
| Event-Driven Lambdas | APNS / FCM | push notifications |
| Amplify Hosting | S3 Buckets | static assets origin |

## Canvas & Spacing Problems Encountered

### Problem 1: Canvas size vs. token budget

Generating the full SVG inline requires ~1,500–2,000 lines of raw XML (boxes + arrows + text + markers + legend). Each write attempt consumed the full response token budget before the file could be completed.

### Problem 2: Coordinate scaling

The approved plan used 1300×1000px coordinates. The user requested doubling to ~2600×2000px. Recalculating all x/y/width/height values manually mid-response is error-prone and consumes significant tokens before any SVG is saved.

**Proposed fix:** Start from 2600×2000 as the canonical coordinate system. Use a fixed grid:
- Box width: 280px · Box height: 110px · Horizontal gap: 60px
- Layer y-starts (approx): 80, 260, 460, 680, 900, 1100, 1320, 1540, 1760
- Left label column: x=20, width=100px
- Content area: x=140 to x=2560

### Problem 3: Arrow routing with 9 layers

With layers spanning ~1800px vertically, arrows from mid-diagram layers (e.g., Main API Lambda at y≈460) to deep layers (e.g., DynamoDB at y≈1100) need waypoints to avoid crossing unrelated boxes. Need explicit path routing using SVG `<path d="M ... C ... "/>` curves or elbow connectors.

**Proposed fix:** Route all downward arrows along a dedicated "arrow lane" on the right side of each source box, curving to the left side of each destination box.

### Problem 4: Event-Driven summary box sizing

The "Event-Driven Lambdas ×9" box needs to list 9 sub-labels. At 11px font, 9 lines ≈ 110px minimum height. Box should be wider than standard to center in the layer. Proposed: 600×140px centered in the content area.

## Approach for Next Session

1. Write the SVG in sections using the Write tool:
   - Step 1: SVG header + `<defs>` (arrowhead markers)
   - Step 2: Layer background rectangles + section labels
   - Step 3: All component boxes (layer by layer)
   - Step 4: All arrows
   - Step 5: Legend + footer
2. Use Edit tool to append each section to avoid re-writing the whole file
3. Or: use the shell-code-writer agent to produce the SVG via a Python generation script (generates the XML programmatically, no token-per-character overhead)

## Footer

`TrailLensHQ System Architecture Overview v1.0 | April 2026 | ca-central-1`

## Legend (bottom-right)

5 color swatches: Clients · AWS Services · Lambda · External · Disabled/Future
