# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

CLAUDE.md is a global file. NEVER review the file unless you are reviewing the traillensdev repo. NEVER change this file unless you are working on the traillensdev repo.

## AI ANSWER REQUIREMENT

**NEVER** invent or guess code elements (components, props, APIs, frameworks, CSS classes, event handlers, state shapes) or any item in general
**ALWAYS** use only what’s explicitly provided by the user or is part of well-documented standard behavior (HTML, CSS, JavaScript, widely-known browser APIs).
**NEVER** fill gaps with plausible-sounding code or explanations
**ALWAYS** use the AskUserQuestion tool to ask for clarification when the request is uncertain, underspecified, or there are any ambiguities. Give a list of options and present the user with your recommendation based on research.

DO NOT MAKE SHIT UP. ALWAYS DO YOUR RESEARCH.

## PLANS

**CRITICAL**: All plans start with using the EnterPlanMode tool. Single prompt vibe coding is not permitted. 

ALWAYS provide a confidence level for every plan. A confidence level is 90% or better is required before a plan will be considered for acceptance by the user. You must provide evidence that a plan will work. Your plan requires proof that the plan will work. Do not make up the confidence level. Proof is required to justify the confidence level suggested. There is a $100,000 fine to you for anything you fake or make up.

## CODE_STRUCTURE.md Search Pattern (MANDATORY)

**CRITICAL**: Before planning or executing any code changes, you MUST search for and read CODE_STRUCTURE.md files in the affected directories.

### Search Algorithm (Pseudo Code)

```
WHEN planning_code_changes OR executing_code_changes:
  IF target_directory IS WITHIN [api-dynamo/, infra/, ai/, webui/, facebook-api/, androiduser/, androidadmin/, androidrestapi/, assets/, planning/]:

    # Step 1: Search for CODE_STRUCTURE.md in target directory
    structure_file = Glob(pattern="**/CODE_STRUCTURE.md", path=target_directory)

    # Step 2: If found, read and incorporate into plan
    IF structure_file EXISTS:
      structure_rules = Read(structure_file)
      APPLY structure_rules TO current_plan
      VERIFY all_changes COMPLY_WITH structure_rules

    # Step 3: If not found, search parent directories
    ELSE:
      parent_structure = Glob(pattern="CODE_STRUCTURE.md", path=parent_directory(target_directory))
      IF parent_structure EXISTS:
        structure_rules = Read(parent_structure)
        APPLY structure_rules TO current_plan

    # Step 4: Fail if structure rules violated
    IF changes VIOLATE structure_rules:
      STOP execution
      ASK user FOR clarification
      EXPLAIN which_rules VIOLATED and why
```

### Usage Examples

**Example 1: Creating a new test file**

Before: `Write(file_path="api-dynamo/tests/test_new_feature.py", ...)`

Required steps:
1. `Glob(pattern="**/CODE_STRUCTURE.md", path="api-dynamo/tests")`
2. `Read("api-dynamo/tests/CODE_STRUCTURE.md")`
3. Verify file path complies with structure rules
4. Correct path: `api-dynamo/tests/unit/routes/test_new_feature.py`

**Example 2: Adding a new route**

Before: `Write(file_path="api-dynamo/api/new_route.py", ...)`

Required steps:
1. `Glob(pattern="**/CODE_STRUCTURE.md", path="api-dynamo/api")`
2. `Read("api-dynamo/api/CODE_STRUCTURE.md")`
3. Verify file path complies with structure rules
4. Correct path: `api-dynamo/api/routes/new_feature.py`

**Example 3: Refactoring business logic**

Before moving code from route handler to service:
1. `Glob(pattern="**/CODE_STRUCTURE.md", path="api-dynamo/api")`
2. `Read("api-dynamo/api/CODE_STRUCTURE.md")`
3. Follow layering rules: routes → services → repositories
4. Place new service in `api-dynamo/api/services/feature_service.py`

**Example 4: Kotlin ViewModel in androiduser**

Before writing a new screen ViewModel:
1. `Glob(pattern="**/CODE_STRUCTURE.md", path="androiduser/app")`
2. `Read` the found CODE_STRUCTURE.md
3. Verify package and placement comply with structure rules

**Example 5: React component in webui**

Before writing a new component:
1. `Glob(pattern="**/CODE_STRUCTURE.md", path="webui/src")`
2. Read found CODE_STRUCTURE.md (or parent if not found)
3. Verify placement follows feature-based organization rules

## CODINGSTANDARDS Read Pattern (MANDATORY)

**CRITICAL**: Before writing or editing any source file, read the CODINGSTANDARDS files for the target submodule. All files live in the submodule root.

### Algorithm

```
WHEN designing_code OR writing_code OR editing_code IN a submodule:

  Read("<submodule>/CODINGSTANDARDS-COPYRIGHT.md")   # always — every source file

  IF file IS shell_script (.sh):
    Read("<submodule>/CODINGSTANDARDS-SHELL.md")

  IF submodule IN [api-dynamo/, infra/, ai/]:
    Read("<submodule>/CODINGSTANDARDS-PYTHON.md")

  ELIF submodule IN [webui/, facebook-api/]:
    Read("<submodule>/CODINGSTANDARDS-TYPESCRIPT.md")

  ELIF submodule IN [androiduser/, androidadmin/, androidrestapi/]:
    Read("<submodule>/CODINGSTANDARDS-KOTLIN.md")

  APPLY all standards — if code violates standards:
    STOP, ASK user, EXPLAIN which standards are violated
```

### Examples

Python (api-dynamo, infra, ai):
  Read("api-dynamo/CODINGSTANDARDS-COPYRIGHT.md")
  Read("api-dynamo/CODINGSTANDARDS-PYTHON.md")

TypeScript (webui, facebook-api):
  Read("webui/CODINGSTANDARDS-COPYRIGHT.md")
  Read("webui/CODINGSTANDARDS-TYPESCRIPT.md")

Kotlin (androiduser, androidadmin, androidrestapi):
  Read("androiduser/CODINGSTANDARDS-COPYRIGHT.md")
  Read("androiduser/CODINGSTANDARDS-KOTLIN.md")

Shell script in any submodule:
  Read("<submodule>/CODINGSTANDARDS-COPYRIGHT.md")
  Read("<submodule>/CODINGSTANDARDS-SHELL.md")

## Internal Tools Requirement

**CRITICAL**: You **MUST** use internal tools for all file operations and searches. **NEVER** create bash, Python, Perl, or any other scripts for these tasks.

**Required Internal Tools:**

- **ToolSearch** - Search for the best available tool
- **Read** - Read file contents (instead of `cat`, `head`, `tail`)
- **Edit** - Modify files with exact string replacement (instead of `sed`, `awk`)
- **Write** - Create new files (instead of `echo >`, `cat <<EOF`)
- **Grep** - Search code content (instead of `grep`, `rg`, `ag`)
- **Glob** - Find files by pattern (instead of `find`, `ls`)
- **AskUserQuestion** - Ask users for clarification or decisions. Any ambiguities must be must be resolved by the user.
- **WebSearch** - Search the web for information
- **WebFetch** - Fetch content from URLs

**Tool Search for MCP Servers:**

- Use ToolSearch to find available MCP tools before using CLI commands:
  - For GitHub: NEVER use `gh` CLI when GitHub MCP is available (github)
  - For AWS: NEVER use `aws` CLI when AWS MCP is available (awslabs-dynamodb, awslabs-cloudwatch, aws-docs, aws-pricing)
  - For Playwright: NEVER use local `playwright` command when Playwright MCP is available (playwright)

## Repository Overview

TrailLens development workspace - a multi-repository trail management system using **git submodules** with strict separation between infrastructure and application code.

### Submodule Structure

- **`infra/`** - Centralized AWS infrastructure (VPC, DynamoDB, Cognito, API Gateway, S3, SNS, Redis, SES) - Python 3.14 REQUIRED
- **`api-dynamo/`** - FastAPI backend (Python 3.14 REQUIRED) with Lambda deployment (user misspells this project often as `api-dyanmo`)
- **`facebook-api/`** - NestJS backend (Node.js 22) for Facebook/Instagram webhooks
- **`web/`** - React 19 frontend with Tailwind CSS 3.4.19
- **`webui/`** - React 19 frontend with Tailwind CSS 4.x (new design)
- **`assets/`** - Shared branding and static assets
- **`ai/`** - AI related development
- **`androidrestapi`** - Android REST interface library to api-dynamo
- **`androiduser`** - Android User App
- **`androidadmin`** - Android Admin All

**Key Architecture Principle:** Infrastructure and applications deploy independently. Infrastructure first, then applications reference infrastructure outputs via Pulumi StackReference.

## Deployment Environment Context

TrailLens uses one environment (prod) managed centrally from the `infra/` repository. Application repositories (`api-dynamo/`, `facebook-api/`, `web/`, `webui`) deploy into infrastructure that already exists in the target environment.

- Default to the **prod** environment for new configuration or example values unless explicitly specified otherwise.
- Never introduce hard-coded production-only resource identifiers without explicit user guidance; prefer configuration via environment variables or existing config files.
- Never create a new environment. TrailLens uses a single prod environment at current scale (<500 MAU). Multi-environment architecture is deferred until 10K+ MAU.

## Important Rules

- **Never commit to main** - Use `topic/*` branches
- **No new branches or PRs without permission** — NEVER create a new branch or open a new PR if a working branch already exists. ALWAYS call `AskUserQuestion` with a clear reason before creating any branch or PR, and NEVER proceed without explicit user approval.
- **Infrastructure** - Never deploy infrastructure - it must be deployed manually
- **Submodule first** - Commit submodule before updating main repo
- **No Makefiles** - Use Python/npm scripts
- **Virtual envs** - Named `.venv`, never committed
- **Copyright headers** - Required in all source files
- **No AI advertising** - Never include Claude/AI promotional content in commits, code, comments, or documentation (no "Generated with Claude Code" footers, co-author tags, or similar marketing text)
- **DevContainer exceptions** - Hard-coded values in `.devcontainer/` are allowed for local development
- **Python environment setup** - Before running any Python command (`pytest`, `pip`, `python`, etc.) in a submodule, you MUST first source its environment script: `source <repo>/scripts/setup-env.sh` (e.g., `source api-dynamo/scripts/setup-env.sh`). This sets up AWS credentials and activates the virtual environment with dependencies. Run from the submodule's root directory.
- **setup-env.sh scripts by purpose** - For Pulumi infrastructure work: source `<project>/pulumi/setup-env.sh` (uses pulumi/requirements.txt). For Python utility scripts: source `<project>/scripts/setup-env.sh` (uses scripts/requirements.txt). Each script is purpose-specific and uses only its own requirements file.

## Coding Guidelines

- Always use Test Driven Development writing tests first, and writing code to make the tests work. Never write code first. The exception is Pulumi related infrastructure code that must never have tests
- Test coverage MUST target 90% for unit tests, functional tests, integration tests and scaling tests. The minimum required coverage is defined by the thresholds in each project's test configuration. Code work is not complete until coverage meets the enforced thresholds, and you should incrementally improve tests toward the 90% target. (reference .agents/skills/python-tests for python code)
- For Python code, NEVER use Python 2.x syntax. You MUST use Python 3.14 syntax and code
- For Bash/Shell code, NEVER use Bash 4.x syntax. You MUST use Bash 3.x syntax and code
- For Python tests, according to moto 4.0+ documentation, mock_aws is the modern approach. NEVER use the legacy imports.
- For code reviews, NEVER review documentation unless the file is README.md. 
- NEVER review MEMORY.md for a code review. Github Copilot reviewer MUST ignore MEMORY.md
- Functional, integration, and scaling tests must NEVER be skipped. If a local service is required, ALWAYS start up the local services to run the functional, integration, and scaling tests.
- NEVER use a mock for function tests. ALWAYS setup a local service against which to run tests.
- NEVER create long multiitem functions. ALWAYS create short targeted functions regardless of the programming language.
- NEVER defer fixing an issue or coding error because the issue was not in the changeset or the issue was pre-existing. ALWAYS fix all issues and errors.
- ALWAYS check the configuration system for the project. NEVER hard code configuration values (such as domain names) in the code.
- ALWAYS use a library for mocking in test code. NEVER write custom mock code unless there is not other option. For example, ALWAYS use mock_aws for boto3 aws mocking in python.
- ALWAYS run functional tests as a separate process from unit tests. NEVER run unit tests and funcitonal tests together.
- NEVER use set -e in shell scripts. ALWAYS use proper error handling.
- NEVER use python-jose (which depended on vulnerable ecdsa library). ALWAYS use PyJWT[crypto]>=2.9.0 for JWT handling in api-dynamo - python-jose was removed in commit c2c5aa4 (Feb 2026) to eliminate CVE-2024-23342. ALWAYS accept test-only ecdsa warnings from moto dependency (used for AWS service mocking) - this is acceptable for test environments only.
- NEVER implement unit test that use Assert True, Assert Fail or are skipped. ALWAYS implement all unit tests to test code.
- NEVER create "documentation tests". Documentation tests do not exist. ALWAYS update documentation markdown files instead.
- ALWAYS use aioboto3 library and ALWAYS implement async python code.
- NEVER update the openapi.json unless there is a well documented reason for it. openapi.json is the source of true for out REST API. Any change architect level approval and must be fully justified.
- ALWAYS create CloudWatch logs for a project with a default 30 day retention period
- NEVER allow CloudWatch logs to be created without a retention period

## High-Performance Coding Standards (100,000+ Users)

**Context:** TrailLens targets 100,000+ daily active users with 99.9% uptime. These rules are MANDATORY for all code that will run at scale. Violations will cause production outages, security breaches, performance degradation, or cost overruns.

### Design Philosophy: Scale vs Cost

**CRITICAL DESIGN PRINCIPLE**: All code and architecture decisions MUST balance two requirements:

1. **Code Design Target: 100,000 DAU**
   - All application code, algorithms, and architecture patterns MUST be designed to handle 100,000 daily active users
   - Performance characteristics MUST meet scale targets from day one:
     - Python Lambda: P95 < 200ms, P99 < 500ms, ~1,157 RPS sustained
     - React Frontend: LCP < 2.5s, FID < 100ms, CLS < 0.1
     - Infrastructure: 99.9% uptime, 3x peak load capacity
   - Database queries, API endpoints, state management, caching strategies MUST be designed for scale
   - No architectural rewrites should be needed when scaling from 500 to 100K users

2. **Infrastructure Cost Target: Current Scale (<500 users)**
   - Infrastructure MUST be configured for minimum cost at current user levels
   - Use serverless, pay-per-request, and auto-scaling services (not provisioned capacity)
   - Disable expensive features until user growth justifies them (Redis, VPC, DAX, provisioned capacity)
   - Apply cost controls: lifecycle rules, throttling limits, free tier optimization
   - Monitor costs closely and scale infrastructure in response to actual usage patterns

**The Philosophy:**

> "Write code that scales. Deploy infrastructure that doesn't waste money."

**In Practice:**

- ✅ **DO** write Lambda functions with proper connection pooling, caching, batch operations, and pagination (scale-ready code)
- ✅ **DO** deploy Lambda with PAY_PER_REQUEST pricing, free tier optimization, and cost monitoring (cost-optimized infrastructure)

- ✅ **DO** design React components with memoization, virtualization, code splitting, and lazy loading (scale-ready code)
- ✅ **DO** deploy with minimal bundle sizes and aggressive tree-shaking (cost-optimized infrastructure)

- ✅ **DO** design DynamoDB tables with proper partition keys, GSIs, and query patterns for high throughput (scale-ready code)
- ✅ **DO** deploy DynamoDB with PAY_PER_REQUEST mode and PITR enabled (cost-optimized infrastructure at small scale)

- ❌ **DO NOT** write naive code that won't scale (full table scans, N+1 queries, unbounded memory usage)
- ❌ **DO NOT** deploy expensive infrastructure prematurely (Redis, VPC, provisioned capacity, reserved instances)

**Cost Scaling Thresholds:**

Reference the following user thresholds when making infrastructure decisions:

- **Below 10K MAU**: Serverless only (Lambda, DynamoDB PAY_PER_REQUEST, S3, API Gateway)
- **10K-25K MAU**: Evaluate metrics; consider caching layers if DynamoDB reads >$50/month
- **25K-50K MAU**: Consider Redis/DAX if cache hit rate >70% in testing
- **50K+ MAU**: Scale infrastructure proactively; monitor leading indicators

**Current Scale: <500 MAU**

All code and infrastructure changes MUST be designed for 100K users but configured/deployed for <500 users.

---

### Python Lambda Standards (api-dynamo/)

**Reference:** [.agents/prompts/code-review-hiperf-python-lambda.md](.agents/prompts/code-review-hiperf-python-lambda.md)

**Performance Target:** P95 latency < 200ms, P99 latency < 500ms, ~1,157 requests/second sustained throughput

#### Cold Start & Initialization

1. **DO NOT** create boto3 clients, database connections, or SDK resources inside the Lambda handler function - initialize them at module level to enable reuse across invocations

2. **DO NOT** include unnecessary packages in requirements.txt - audit dependencies for bloat as each import increases cold start time and package size

3. **DO NOT** load configuration files, environment variables, or static assets on every invocation - read them once at module level

4. **DO NOT** import unused modules - they increase package size and load time, degrading cold start performance

#### DynamoDB Configuration

5. **DO NOT** skip boto3 client configuration - you MUST set max_pool_connections (50-100 for high-throughput), connection timeout (2 seconds), read timeout (5-10 seconds), and retry configuration with exponential backoff

6. **DO NOT** use default retry settings - configure adaptive retry mode with 3+ max attempts, exponential backoff with jitter (25ms → 20s max)

7. **DO NOT** create new DynamoDB clients for each request - reuse a single client/resource initialized at module level

#### Query Optimization

8. **DO NOT** fetch all attributes when you only need specific fields - always use ProjectionExpression to reduce bandwidth and cost

9. **DO NOT** perform individual write operations when batch operations are possible - use batch_get_item and batch_write_item (up to 25 items) to reduce latency

10. **DO NOT** perform full table scans without pagination - properly handle LastEvaluatedKey to avoid loading massive datasets into memory

#### Error Handling

11. **DO NOT** use bare `except:` clauses - catch specific exception types (ClientError, ValidationException, etc.) and log with full context

12. **DO NOT** skip retry logic for throttling errors - implement exponential backoff with jitter for ProvisionedThroughputExceededException, RequestLimitExceeded, and ServiceUnavailable

13. **DO NOT** expose internal error details in API responses - use custom exception classes and return generic error messages to clients

14. **DO NOT** ignore timeout configuration - set connection and read timeouts on all boto3 clients and external HTTP requests

#### Concurrency & Race Conditions

15. **DO NOT** use lazy initialization patterns without thread-safe locking - mutable module-level variables accessed by multiple threads MUST use threading.Lock with double-checked locking

16. **DO NOT** perform blocking I/O operations in async functions - use run_in_executor for synchronous boto3 calls to avoid blocking the event loop

17. **DO NOT** skip optimistic locking for critical updates - use ConditionExpression with version fields to prevent race conditions in concurrent writes

#### Memory & Resource Management

18. **DO NOT** load entire large datasets into memory - use generators or iterators with pagination to process data in batches

19. **DO NOT** skip caching for frequently accessed data - implement TTL-based caching with proper invalidation strategy to reduce DynamoDB calls

#### Testing Requirements

20. **DO NOT** write code without achieving 85%+ test coverage - all business logic, error handling paths, edge cases, and async functions MUST have comprehensive unit and integration tests using moto or local DynamoDB

### JavaScript/TypeScript/React Standards (web/)

**Reference:** [.agents/prompts/code-review-hiperf-javascript.md](.agents/prompts/code-review-hiperf-javascript.md)

**Performance Target:** Core Web Vitals - LCP < 2.5s, FID < 100ms, CLS < 0.1

#### React Performance

1. **DO NOT** create expensive components without React.memo - all pure components with expensive computations must be wrapped with `React.memo()` when profiling shows benefit

2. **DO NOT** create new functions in render cycles - never use inline arrow functions in props or create new objects/functions during render; use `useCallback` for event handlers

3. **DO NOT** perform expensive computations without useMemo - all expensive calculations (sorting, filtering, reducing large datasets) must be memoized with `useMemo` with proper dependencies

4. **DO NOT** render large lists without virtualization - lists with >100 items must use virtual scrolling (react-window or react-virtual) to prevent DOM bloat

5. **DO NOT** load all routes upfront - every route must be lazy-loaded with `React.lazy()` and wrapped in `<Suspense>` boundaries

6. **DO NOT** build custom UI components when battle-tested libraries exist - ALWAYS use Amplify UI (AWS integration), Tremor (charts/dashboards), or shadcn/ui (general UI) for common patterns. NEVER reinvent accessibility, keyboard navigation, or ARIA patterns. Custom components are only justified when no suitable library component exists.

7. **DO NOT** let a React Context exceed ~300 lines, >10 state variables, or >20 context value properties - split into focused contexts. Use an internal-only "Internals" context for cross-context state mutation and a backwards-compat wrapper hook so existing consumers don't break.

8. **DO NOT** split work across parallel agents without ensuring non-overlapping file batches - agents editing the same files cause conflicts. Use `bypassPermissions` mode for agents that create or edit multiple files.

#### TypeScript & Code Quality

9. **DO NOT** use TypeScript 'any' type without justification - enable strict mode and use explicit types or `unknown`; document any exceptions with comments

10. **DO NOT** write async code without comprehensive error handling - all async operations must have try-catch blocks, timeout handling, and exponential backoff retry logic

11. **DO NOT** forget cleanup in useEffect - all effects must return cleanup functions for event listeners, timers, WebSocket connections, and fetch requests (AbortController)

#### Bundle Size & Loading

12. **DO NOT** exceed 200KB gzipped for main bundle - implement code splitting, tree-shaking, and remove unused dependencies to meet bundle size targets

13. **DO NOT** animate layout properties in CSS - only animate `transform` and `opacity` for GPU acceleration; never animate `width`, `height`, `top`, or `left`

#### Error Handling & Resilience

14. **DO NOT** skip error boundaries - implement top-level and strategic error boundaries with user-friendly fallback UI and error logging to monitoring services

15. **DO NOT** manage server state manually - use React Query or SWR for all server state management with proper cache strategies, retry logic, and request deduplication

#### Architecture & Organization

16. **DO NOT** organize code by file type - use feature-based organization (group by feature, not by components/hooks/services folders) for maintainability at scale

17. **DO NOT** render unsanitized user content as HTML - never use dangerouslySetInnerHTML without DOMPurify sanitization; rely on React's default escaping

18. **DO NOT** import entire libraries - use tree-shakeable imports (e.g., `import debounce from 'lodash/debounce'` not `import _ from 'lodash'`)

#### Testing & Quality

19. **DO NOT** skip 80%+ test coverage - write unit tests for business logic, component tests with React Testing Library, and E2E tests for critical paths

20. **DO NOT** leave console.log in production code - remove all debug logging and implement structured logging service with proper log levels and context

#### State Management

21. **DO NOT** store derived state - compute values during render instead of storing them in state; avoid redundant state that can be calculated from existing data

#### CSS & Styling

22. **DO NOT** load non-critical CSS synchronously - inline critical above-the-fold CSS and load non-critical styles asynchronously; keep production CSS < 50KB gzipped

#### Monitoring

23. **DO NOT** deploy without performance monitoring - track Core Web Vitals (LCP < 2.5s, FID < 100ms, CLS < 0.1), integrate error tracking, and enforce performance budgets in CI

### Infrastructure/Pulumi Standards (infra/)

**Reference:** [.agents/prompts/code-review-hiperf-infra.md](.agents/prompts/code-review-hiperf-infra.md)

**Scale Target:** Support 100,000 daily active users with ~1,157 requests/second sustained throughput

#### Performance & Scalability

1. **DO NOT** use provisioned DynamoDB capacity without auto-scaling configuration and documented migration path from PAY_PER_REQUEST mode

2. **DO NOT** use default 128MB Lambda memory allocation for all functions - right-size each function based on workload (auth: 256-512MB, photo processing: 1024-2048MB)

3. **DO NOT** deploy API Gateway without method-level throttling limits (stage-level: 5,000 RPS with 2,500 burst, auth endpoints: 1,000 RPS for brute force protection)

4. **DO NOT** create DynamoDB tables without verifying partition key design prevents hot partitions (no single partition should receive >1,000 WCU or 3,000 RCU)

5. **DO NOT** use x86_64 Lambda architecture when ARM64 (Graviton2) is compatible - this costs 20% more without benefit

#### Security Requirements

6. **DO NOT** create IAM policies with wildcard actions (`"Action": "*"` or `"Action": "service:*"`) or wildcard resources (`"Resource": "*"`) when specific ARNs are available

7. **DO NOT** deploy any resource (DynamoDB, S3, SNS, Secrets Manager) without encryption at rest enabled

8. **DO NOT** store secrets as plaintext in Pulumi config - use `pulumi config set --secret` with KMS encryption provider for production stacks

9. **DO NOT** use wildcard CORS origins (`"*"`) in production - specify exact allowed domains

#### Reliability & Data Protection

11. **DO NOT** create production DynamoDB tables without point-in-time recovery (PITR) enabled and deletion protection active

12. **DO NOT** deploy production Cognito user pools without deletion protection set to "ACTIVE"

13. **DO NOT** create resources outside ComponentResource classes or without `opts=ResourceOptions(parent=self)` - this breaks dependency tracking and prevents clean resource organization

14. **DO NOT** create S3 buckets without lifecycle rules - this leads to unbounded storage growth and cost overruns

15. **DO NOT** skip CloudWatch alarms for critical metrics (Lambda error rate >1%, DynamoDB throttles >0, API Gateway 5XX errors >1%, Lambda P99 duration >80% of timeout)

#### Testing & Deployment Safety

16. **DO NOT** run `pulumi up` in production without first running `pulumi preview` and manually reviewing all resource changes

17. **DO NOT** deploy application code before infrastructure updates - deployment order must be: 1) infra/, 2) api-dynamo/, 3) web/

18. **DO NOT** create production resources without Pulumi `protect=True` on critical resources to prevent accidental `pulumi destroy`

19. **DO NOT** skip X-Ray tracing configuration (`tracing_config={"mode": "Active"}` on Lambda, `xray_tracing_enabled=True` on API Gateway) - you will be blind to distributed performance issues at scale

#### Operational Readiness

20. **DO NOT** deploy to production without verifying Cognito quota increases have been approved for target scale (default: 50 sign-ups/second, 120 sign-ins/second - request increases for 100K+ users)

---

**Enforcement:** All code reviews MUST verify compliance with these standards. Code that violates these rules will be rejected in PR review.
