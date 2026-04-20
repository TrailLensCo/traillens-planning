# Copyright (c) 2026 TrailLensCo
# All rights reserved.

# Failure Mode Vulnerability Patterns for Python Applications

## Purpose

This document captures 80 failure mode vulnerability patterns for Python applications, particularly FastAPI services deployed on AWS Lambda with DynamoDB, SNS, SES, and Cognito dependencies. It serves as a reference for the `python-security-scan` skill and future code reviews.

## Summary Table

| # | Failure Mode | Severity | Category | Detection Pattern |
|---|-------------|----------|----------|-------------------|
| 1 | Missing retry on transient failures | CRITICAL | Retry and Recovery | SNS/SES/DynamoDB calls without retry config |
| 2 | No circuit breaker | HIGH | Retry and Recovery | Repeated calls to external service without fast-fail |
| 3 | Cascading failure risk | CRITICAL | External Service Resilience | All endpoints fail when one dependency fails |
| 4 | JWKS cache empty on startup failure | CRITICAL | External Service Resilience | Auth fails for all users if Cognito down at cold start |
| 5 | Partial write without cleanup | CRITICAL | Data Integrity | Multi-table write where 2nd fails, 1st not rolled back |
| 6 | Silent notification failure | HIGH | External Service Resilience | SNS publish fails, exception swallowed |
| 7 | Missing idempotency keys | MEDIUM | Data Integrity | Create ops generate new UUID on retry |
| 8 | Connection pool exhaustion | HIGH | External Service Resilience | No max_pool_connections or pool monitoring |
| 9 | Timeout without fallback | HIGH | External Service Resilience | External call times out, generic 500 returned |
| 10 | Missing health check | HIGH | External Service Resilience | Health returns static "healthy" without dep checks |
| 11 | Error response leaking internals | MEDIUM | Error Handling | Stack traces or AWS errors in response body |
| 12 | Retry storm amplification | HIGH | Retry and Recovery | DynamoDB throttle + Lambda retry = amplification |
| 13 | No dead letter handling | HIGH | Error Handling | Async ops with no DLQ or failure recovery |
| 14 | Graceful degradation missing | HIGH | Error Handling | Non-critical service failure takes down main op |
| 15 | Stale cache without rotation detection | HIGH | Error Handling | JWKS cache doesn't detect key rotation |
| 16 | Exception suppression without context | MEDIUM | Error Handling | Exception caught, logged without type/context |
| 17 | No per-user rate limiting | CRITICAL | Security/Rate Limiting | Unlimited attempts enable brute force |
| 18 | Missing input validation before external calls | MEDIUM | Error Handling | Invalid data passed to SNS/DynamoDB |
| 19 | No request-level instrumentation | MEDIUM | Error Handling | Cannot determine which dependency failed |
| 20 | Missing error recovery strategy | HIGH | Retry and Recovery | No retry, no DLQ, no fallback on failure |
| 21 | Lambda-API Gateway timeout mismatch | CRITICAL | Lambda-Specific | Lambda timeout > API Gateway 29s limit |
| 22 | Ephemeral storage (/tmp) exhaustion | HIGH | Lambda-Specific | /tmp writes without cleanup in finally blocks |
| 23 | Lambda concurrency vs API Gateway throughput | CRITICAL | Lambda-Specific | API GW accepts but Lambda throttles |
| 24 | Reserved concurrency starving other functions | HIGH | Lambda-Specific | Over-reserving reduces pool for others |
| 25 | Lambda payload size exceeded (6MB) | HIGH | Lambda-Specific | Endpoints returning unbounded results |
| 26 | Lambda deployment package size exceeded | MEDIUM | Lambda-Specific | No size monitoring in CI/CD |
| 27 | Lambda memory leak across warm invocations | HIGH | Lambda-Specific | Module-level mutable containers grow unbounded |
| 28 | Lambda recursive invocation loop | CRITICAL | Lambda-Specific | Lambda writes to trigger source |
| 29 | Lambda environment variable 4KB limit | MEDIUM | Lambda-Specific | Combined env vars exceed 4KB |
| 30 | Cold start timeout during VPC ENI attachment | HIGH | Lambda-Specific | VPC subnet IP exhaustion |
| 31 | Lambda layer runtime version mismatch | MEDIUM | Lambda-Specific | Layer built for different Python version |
| 32 | GSI write throttling backpressure on base table | CRITICAL | DynamoDB-Specific | GSI capacity < base table write rate |
| 33 | DynamoDB hot partition throttling | HIGH | DynamoDB-Specific | Low-cardinality partition key |
| 34 | DynamoDB item size limit (400KB) exceeded | HIGH | DynamoDB-Specific | Unbounded list_append operations |
| 35 | DynamoDB transaction conflict | HIGH | DynamoDB-Specific | Mixed transactional and non-transactional writes |
| 36 | DynamoDB TTL deletion delay (up to 48 hours) | MEDIUM | DynamoDB-Specific | TTL-dependent logic without explicit filter |
| 37 | DynamoDB BatchWriteItem partial failure | HIGH | DynamoDB-Specific | batch_write_item without UnprocessedItems retry |
| 38 | DynamoDB scan without pagination | CRITICAL | DynamoDB-Specific | scan/query without LastEvaluatedKey check |
| 39 | DynamoDB conditional check failure without retry | MEDIUM | DynamoDB-Specific | ConditionExpression without exception handling |
| 40 | SES bounce rate exceeding account threshold | CRITICAL | SES-Specific | SES sends without bounce handling |
| 41 | SES complaint rate threshold violation | CRITICAL | SES-Specific | No complaint feedback processing |
| 42 | SES sandbox mode sending restriction | HIGH | SES-Specific | Deploy without production SES access |
| 43 | SES sending quota exhaustion | HIGH | SES-Specific | Burst sends without rate limiting |
| 44 | SNS message attribute filtering mismatch | MEDIUM | SNS-Specific | Publish attributes vs subscription filters |
| 45 | SNS FIFO topic endpoint limitation | MEDIUM | SNS-Specific | Non-SQS subscriber on FIFO topic |
| 46 | SNS message size limit (256KB) | MEDIUM | SNS-Specific | Publish without payload size validation |
| 47 | Cognito token revocation gap | CRITICAL | Cognito-Specific | JWT verification without revocation check |
| 48 | Cognito user pool rate limit exhaustion | HIGH | Cognito-Specific | Cognito API calls without caching |
| 49 | Cognito hosted UI custom domain propagation | MEDIUM | Cognito-Specific | Immediate verification after domain change |
| 50 | Cognito token size increase after enabling revocation | LOW | Cognito-Specific | Token handling with size assumptions |
| 51 | Abandoned multipart upload storage leak | MEDIUM | S3-Specific | No lifecycle rule for incomplete uploads |
| 52 | S3 lifecycle rule overwrite on update | HIGH | S3-Specific | Lifecycle updates without reading existing rules |
| 53 | aioboto3 event loop closed on reuse | HIGH | Python/asyncio | Global session with closed event loop |
| 54 | aioboto3 resource not closed (session leak) | HIGH | Python/asyncio | Resource without async context manager |
| 55 | asyncio task cancellation not re-raised | HIGH | Python/asyncio | CancelledError catch without raise |
| 56 | asyncio yield inside TaskGroup | HIGH | Python/asyncio | yield breaking structured concurrency |
| 57 | Blocking I/O in async handler | CRITICAL | Python/asyncio | Sync calls in async def |
| 58 | Unbounded asyncio concurrency | HIGH | Python/asyncio | Unlimited concurrent tasks |
| 59 | DynamoDB Decimal serialization | MEDIUM | Python/asyncio | Decimal not JSON-serializable |
| 60 | Secrets Manager rotation during active request | HIGH | Secrets/Configuration | Secret caching without rotation handling |
| 61 | STS credential expiration without refresh | HIGH | Secrets/Configuration | AssumeRole without refresh logic |
| 62 | CloudWatch metric filter ignoring late data | MEDIUM | Observability/Monitoring | Alarm config without treat_missing_data |
| 63 | EMF metric dimension/count limit | MEDIUM | Observability/Monitoring | Excess metrics/dimensions silently dropped |
| 64 | X-Ray subsegment outside handler | MEDIUM | Observability/Monitoring | Module-level AWS calls with active tracing |
| 65 | Distributed trace context lost in async processing | MEDIUM | Observability/Monitoring | Message handlers without trace extraction |
| 66 | Mangum lifespan running per-request | HIGH | FastAPI/Application | Heavy lifespan handlers with Mangum |
| 67 | FastAPI HTTPException in middleware not handled | MEDIUM | FastAPI/Application | HTTPException inside BaseHTTPMiddleware |
| 68 | Pydantic V2 nested subclass serialization | MEDIUM | FastAPI/Application | Model inheritance in nested fields |
| 69 | FastAPI dependency circular import | MEDIUM | FastAPI/Application | Circular imports in dependency chains |
| 70 | Configuration drift between infra and application | HIGH | Infrastructure/Deployment | StackReference outputs vs env vars |
| 71 | Lambda layer version not updated | MEDIUM | Infrastructure/Deployment | Pinned layer version ARNs |
| 72 | API Gateway stage deployment not propagated | HIGH | Infrastructure/Deployment | API changes without deployment creation |
| 73 | DNS resolution failure cascade | CRITICAL | DNS/Network | No DNS caching, single-region |
| 74 | Lambda VPC subnet IP address exhaustion | HIGH | DNS/Network | Subnet CIDR vs expected concurrency |
| 75 | API Gateway request validation bypass | MEDIUM | API Gateway | No request validators configured |
| 76 | API Gateway throttling layer confusion | MEDIUM | API Gateway | Conflicting throttling levels |
| 77 | Feature flag cold start performance penalty | MEDIUM | Feature Flag | Remote flag evaluation on cold start |
| 78 | Feature flag stale cache after provider outage | MEDIUM | Feature Flag | No default values configured |
| 79 | DynamoDB schema migration without dual-write | HIGH | Data Integrity | Attribute changes without backward compat |
| 80 | SQS partial batch failure without ReportBatchItemFailures | HIGH | Data Integrity | Entire batch retried on single failure |

---

# Category P: Retry and Recovery (Patterns 1, 2, 12, 20)

---

## 1. Missing Retry on Transient Failures

**Severity:** CRITICAL

**Description:** External service calls (SNS, SES, DynamoDB, Cognito) fail transiently due to throttling, network blips, or brief outages. Without retry logic, these transient failures become permanent failures.

**Vulnerable Pattern:**
```python
async def send_notification(sns_client, topic_arn, message):
    try:
        await sns_client.publish(TopicArn=topic_arn, Message=message)
    except ClientError as e:
        log_error("SNS publish failed", metadata={"error": str(e)})
        raise  # No retry — transient failure becomes permanent
```

**Resilient Pattern:**
```python
from botocore.config import Config

config = Config(
    retries={"max_attempts": 3, "mode": "adaptive"},
    connect_timeout=2,
    read_timeout=10,
)
# Client configured with adaptive retry handles transient failures automatically
```

**Detection:** Search for `sns_client.publish`, `ses_client.send_email`, `dynamodb.put_item` without retry configuration on the client.

**Impact:** Trail condition notifications silently dropped during SNS throttling. Users unable to verify phone numbers during brief SNS outages.

---

## 2. No Circuit Breaker

**Severity:** HIGH

**Description:** When an external service is degraded, every request continues to call it, adding load to the already-failing service and causing all requests to hang or timeout.

**Vulnerable Pattern:**
```python
async def get_jwks():
    # Every request tries to fetch JWKS, even during Cognito outage
    async with httpx.AsyncClient() as client:
        response = await client.get(jwks_url, timeout=5)
        return response.json()
```

**Resilient Pattern:**
```python
_failure_count = 0
_circuit_open_until = None

async def get_jwks():
    if _circuit_open_until and datetime.now() < _circuit_open_until:
        return _cached_jwks  # Fast-fail with cached data
    try:
        result = await _fetch_jwks()
        _failure_count = 0
        return result
    except Exception:
        _failure_count += 1
        if _failure_count >= 3:
            _circuit_open_until = datetime.now() + timedelta(seconds=30)
        return _cached_jwks
```

**Detection:** Search for repeated external service calls without failure counting or fast-fail logic.

**Impact:** During Cognito degradation, 1000+ concurrent auth requests all attempt JWKS fetch, extending the outage.

---

## 12. Retry Storm Amplification

**Severity:** HIGH

**Description:** DynamoDB throttles requests. Lambda's built-in retry sends the same request again. Combined with SDK retries, this creates 9x amplification.

**Vulnerable Pattern:**
```python
# SDK retries 3x + Lambda retries 3x = 9 attempts for 1 request
config = Config(retries={"max_attempts": 3, "mode": "standard"})

# Lambda configured with default retry behavior (2 retries)
```

**Resilient Pattern:**
```python
# Use adaptive retry mode — adjusts based on throttling signals
config = Config(retries={"max_attempts": 3, "mode": "adaptive"})

# Lambda: set MaximumRetryAttempts=0 for sync invocations
# Use idempotency tokens to safely handle any retries
```

**Detection:** Search for retry configuration without `mode: "adaptive"` and Lambda configurations without retry limits.

**Impact:** Brief DynamoDB throttle causes retry storm extending the outage duration by 3-9x.

---

## 20. Missing Error Recovery Strategy

**Severity:** HIGH

**Description:** When operations fail, there is no mechanism to retry, queue for later, or alert operators.

**Vulnerable Pattern:**
```python
try:
    await sns_client.publish(...)
except Exception:
    log_error("Failed")  # Notification gone forever
```

**Resilient Pattern:**
```python
try:
    await sns_client.publish(...)
except Exception as e:
    log_error("SNS publish failed, storing for retry", error_code="SNS_RETRY_QUEUED")
    await failed_notifications_repo.create(FailedNotification(
        topic_arn=arn, message=msg, error=str(e), retry_count=0,
    ))
```

**Detection:** Search for caught exceptions where the only action is logging.

**Impact:** All notifications during SNS outage permanently lost with no recovery path.

---

# Category Q: Data Integrity (Patterns 5, 7)

---

## 5. Partial Write Without Cleanup

**Severity:** CRITICAL

**Description:** Multi-step operations write to multiple tables/services. If step 2 fails after step 1 succeeds, the system is left in an inconsistent state with no rollback.

**Vulnerable Pattern:**
```python
async def update_trail_status(repo, sns_client, trail_id, status):
    await repo.update(trail_id, {"status": status})  # Step 1: DB succeeds
    await create_history_entry(trail_id, status)       # Step 2: History succeeds
    await sns_client.publish(...)                       # Step 3: SNS FAILS
    # DB shows "closed" but subscribers never notified!
```

**Resilient Pattern:**
```python
async def update_trail_status(repo, sns_client, trail_id, status):
    await repo.update(trail_id, {"status": status})
    await create_history_entry(trail_id, status)
    try:
        await sns_client.publish(...)
        return {"status": "updated", "notification": "sent"}
    except Exception as e:
        log_error("SNS failed after DB update", error_code="PARTIAL_WRITE",
                  metadata={"trail_id": trail_id, "error": str(e)})
        return {"status": "updated", "notification": "failed"}
```

**Detection:** Search for functions with multiple `await repo.update/create` or `await client.publish` calls without transaction boundaries.

**Impact:** Admin closes trail. DB updates. SNS fails silently. Subscribers still see trail as open.

---

## 7. Missing Idempotency Keys

**Severity:** MEDIUM

**Description:** Create operations generate a new UUID for each request. If the client retries due to timeout, duplicate resources are created.

**Vulnerable Pattern:**
```python
async def create_trail_system(request_body, repo):
    entity_id = str(uuid4())  # New ID every time
    await repo.create(TrailSystemEntity(id=entity_id, **request_body))
```

**Resilient Pattern:**
```python
async def create_trail_system(request_body, repo):
    idempotency_key = request_body.get("idempotency_key")
    if idempotency_key:
        existing = await repo.get_by_idempotency_key(idempotency_key)
        if existing:
            return existing
    entity_id = str(uuid4())
    await repo.create(TrailSystemEntity(
        id=entity_id, idempotency_key=idempotency_key, **request_body
    ))
```

**Detection:** Search for `uuid4()` in create methods without idempotency key checks.

**Impact:** Client retry after timeout creates duplicate trail systems with different IDs.

---

# Category R: External Service Resilience (Patterns 3, 4, 6, 8, 9, 10)

---

## 3. Cascading Failure Risk

**Severity:** CRITICAL

**Description:** When one dependency fails (e.g., DynamoDB), ALL endpoints fail instead of only the affected ones. No isolation between dependency failures.

**Vulnerable Pattern:**
```python
@router.get("/health")
async def health_check():
    return {"status": "healthy"}  # Static — doesn't check anything
```

**Resilient Pattern:**
```python
@router.get("/health")
async def health_check(dynamo_table=Depends(get_table)):
    checks = {}
    try:
        await dynamo_table.describe_table()
        checks["dynamodb"] = "healthy"
    except Exception:
        checks["dynamodb"] = "unhealthy"
    status = "healthy" if all(v == "healthy" for v in checks.values()) else "degraded"
    return {"status": status, "dependencies": checks}
```

**Detection:** Search for health endpoints that return static responses without dependency verification.

**Impact:** Load balancer routes traffic to instances that cannot reach database. All requests fail with 500 errors.

---

## 4. JWKS Cache Empty on Startup Failure

**Severity:** CRITICAL

**Description:** If the JWKS endpoint is unreachable during Lambda cold start and there's no cached data, all authentication fails until the next successful fetch.

**Vulnerable Pattern:**
```python
_jwks = None

async def get_jwks():
    if _jwks is not None:
        return _jwks
    try:
        _jwks = await fetch_from_cognito()
    except Exception:
        return None  # All auth fails!
```

**Resilient Pattern:**
```python
async def get_jwks():
    if _jwks is not None and not _is_expired():
        return _jwks
    for attempt in range(3):
        try:
            _jwks = await fetch_from_cognito()
            return _jwks
        except Exception:
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
    return _jwks  # Return stale cache if available
```

**Detection:** Search for JWKS fetch without retry logic on cold start paths.

**Impact:** Lambda cold start during Cognito maintenance -- all users locked out until next warm invocation.

---

## 6. Silent Notification Failure

**Severity:** HIGH

**Description:** SNS/SES publish exceptions are caught and swallowed. The API returns success even though the notification was never delivered.

**Vulnerable Pattern:**
```python
try:
    await sns_client.publish(TopicArn=arn, Message=msg)
except Exception:
    log_error("SNS failed")  # Swallowed — caller thinks it worked
```

**Resilient Pattern:**
```python
try:
    await sns_client.publish(TopicArn=arn, Message=msg)
except Exception as e:
    log_error("SNS failed", error_code="SNS_PUBLISH_FAILURE",
              metadata={"topic": arn, "error_type": type(e).__name__})
    await store_failed_notification(arn, msg, str(e))  # Store for replay
```

**Detection:** Search for `except Exception` blocks that log but don't propagate or store the failure.

**Impact:** Notifications permanently lost during SNS outages with no recovery mechanism.

---

## 8. Connection Pool Exhaustion

**Severity:** HIGH

**Description:** Without connection pool limits, a traffic spike can exhaust all available connections, causing all subsequent requests to fail.

**Vulnerable Pattern:**
```python
session = aioboto3.Session()
async with session.client("dynamodb") as client:
    await client.put_item(...)  # No pool size configuration
```

**Resilient Pattern:**
```python
from botocore.config import Config
config = Config(max_pool_connections=50, connect_timeout=2, read_timeout=10,
                retries={"max_attempts": 3, "mode": "adaptive"})
session = aioboto3.Session()
async with session.client("dynamodb", config=config) as client:
    await client.put_item(...)
```

**Detection:** Search for aioboto3 client creation without `max_pool_connections` in Config.

**Impact:** Traffic spike exhausts connection pool, all DynamoDB calls fail, cascade to all endpoints.

---

## 9. Timeout Without Fallback

**Severity:** HIGH

**Description:** External call times out but the error handler returns a generic 500, giving the client no useful information.

**Vulnerable Pattern:**
```python
except Exception as exc:
    raise HTTPException(status_code=500, detail="Internal server error")
```

**Resilient Pattern:**
```python
except asyncio.TimeoutError:
    raise HTTPException(status_code=504, detail="Upstream service timeout")
except ClientError as e:
    if e.response["Error"]["Code"] == "ProvisionedThroughputExceededException":
        raise HTTPException(status_code=429, detail="Service busy, please retry")
    raise HTTPException(status_code=502, detail="Upstream service error")
```

**Detection:** Search for `except Exception` followed by `HTTPException(500)` without specific exception handlers.

**Impact:** Client receives generic 500 for all failures. Cannot distinguish retryable from non-retryable.

---

## 10. Missing Health Check

**Severity:** HIGH

**Description:** Health endpoint returns static "healthy" without verifying database connectivity or dependency availability.

**Vulnerable Pattern:**
```python
@router.get("/health")
async def health():
    return {"status": "healthy"}  # Static response — no actual checking
```

**Resilient Pattern:**
```python
@router.get("/health")
async def health(dynamo=Depends(get_dynamo)):
    checks = {}
    try:
        await asyncio.wait_for(dynamo.describe_table(), timeout=2.0)
        checks["dynamodb"] = "healthy"
    except Exception:
        checks["dynamodb"] = "unhealthy"
    overall = "healthy" if all(v == "healthy" for v in checks.values()) else "degraded"
    return {"status": overall, "checks": checks}
```

**Detection:** Search for health endpoints that don't call any external service.

**Impact:** Load balancer routes traffic to unhealthy instances. All requests fail downstream.

---

# Category S: Error Handling (Patterns 11, 13, 14, 15, 16, 18, 19)

---

## 11. Error Response Leaking Internals

**Severity:** MEDIUM

**Description:** Error responses include AWS error codes, stack traces, or internal service details.

**Vulnerable Pattern:**
```python
except ClientError as e:
    raise HTTPException(status_code=500, detail=str(e))  # Leaks AWS internals
```

**Resilient Pattern:**
```python
except ClientError as e:
    log_error("DynamoDB error", metadata={"aws_error": str(e)})
    raise HTTPException(status_code=500, detail="Internal server error")
```

**Detection:** Search for `detail=str(e)` or `detail=str(exc)` in HTTPException calls.

**Impact:** Attacker learns about DynamoDB table names, ARNs, throttling limits from error messages.

---

## 13. No Dead Letter Handling

**Severity:** HIGH

**Description:** When async operations fail, the message is retried and eventually discarded with no visibility or recovery mechanism.

**Vulnerable Pattern:**
```python
async def handle_event(event):
    # No try/except — failure retried by Lambda, then discarded
    await process_notification(event)
```

**Resilient Pattern:**
```python
async def handle_event(event):
    try:
        await process_notification(event)
    except Exception as e:
        log_error("Event processing failed", error_code="EVENT_PROCESSING_FAILURE",
                  metadata={"event_id": event.get("id"), "error": str(e)})
        await store_to_dlq(event, str(e))
        raise  # Let Lambda retry, DLQ catches final failures
```

**Detection:** Search for Lambda handlers without try/except that stores failures, and infra without DLQ config.

**Impact:** Failed notifications permanently lost. No way to replay or recover.

---

## 14. Graceful Degradation Missing

**Severity:** HIGH

**Description:** A non-critical dependency failure (notifications, analytics) causes the entire operation to fail.

**Vulnerable Pattern:**
```python
async def update_status(repo, sns_client, trail_id, status):
    await repo.update(trail_id, status)
    await sns_client.publish(...)  # If this fails, entire operation fails
```

**Resilient Pattern:**
```python
async def update_status(repo, sns_client, trail_id, status):
    await repo.update(trail_id, status)  # Critical
    try:
        await sns_client.publish(...)  # Non-critical — best effort
    except Exception:
        notification_status = "failed"
    return {"success": True, "notification": notification_status}
```

**Detection:** Search for non-critical operations not wrapped in try/except.

**Impact:** SNS outage prevents trail status updates even though the database update would succeed.

---

## 15. Stale Cache Without Rotation Detection

**Severity:** HIGH

**Description:** JWKS cache has a fixed TTL but doesn't detect key rotation. Users with tokens signed by new keys are rejected.

**Vulnerable Pattern:**
```python
_cached_jwks = None
_cache_time = None
CACHE_TTL = 3600  # 1 hour

async def get_jwks():
    if _cached_jwks and (time.time() - _cache_time) < CACHE_TTL:
        return _cached_jwks  # Stale — new kid not recognized
    return await _refresh_jwks()
```

**Resilient Pattern:**
```python
async def get_jwks(expected_kid=None):
    if _cached_jwks and not _is_expired():
        if expected_kid is None or _has_kid(expected_kid):
            return _cached_jwks
    return await _refresh_jwks()  # Refresh on kid mismatch
```

**Detection:** Search for JWKS cache without kid-based refresh logic.

**Impact:** Cognito rotates keys, users locked out for up to 1 hour until cache expires.

---

## 16. Exception Suppression Without Context

**Severity:** MEDIUM

**Description:** Exceptions are caught and logged but the error type and context are not captured.

**Vulnerable Pattern:**
```python
except Exception as e:
    log_error("Something went wrong", metadata={"error": str(e)})
    # Missing: error type, operation, entity, dependency
```

**Resilient Pattern:**
```python
except Exception as e:
    log_error("DynamoDB get_item failed",
              error_code="DYNAMODB_READ_FAILURE",
              metadata={
                  "error_type": type(e).__name__,
                  "operation": "get_item",
                  "table": table_name,
                  "entity_id": entity_id,
                  "error": str(e),
              })
```

**Detection:** Search for `log_error` calls that only include `str(e)` without `type(e).__name__`.

**Impact:** During outages, logs show generic errors. Cannot determine root cause.

---

## 18. Missing Input Validation Before External Calls

**Severity:** MEDIUM

**Description:** User input is passed directly to external services without validation.

**Vulnerable Pattern:**
```python
async def send_sms(phone_number: str, message: str, sns_client):
    # No validation — invalid phone numbers waste SNS API calls
    await sns_client.publish(PhoneNumber=phone_number, Message=message)
```

**Resilient Pattern:**
```python
import re

PHONE_PATTERN = re.compile(r"^\+[1-9]\d{1,14}$")

async def send_sms(phone_number: str, message: str, sns_client):
    if not PHONE_PATTERN.match(phone_number):
        raise ValueError(f"Invalid phone number format: must be E.164")
    if len(message) > 140:
        raise ValueError("SMS message exceeds 140 character limit")
    await sns_client.publish(PhoneNumber=phone_number, Message=message)
```

**Detection:** Search for external service calls where parameters come directly from request body.

**Impact:** Invalid input wastes API calls and produces confusing AWS error messages.

---

## 19. No Request-Level Instrumentation

**Severity:** MEDIUM

**Description:** Error handlers log generic messages without request context (dependency, request ID, duration).

**Vulnerable Pattern:**
```python
except Exception as e:
    log_error("Request failed")  # Which request? Which dependency? How long?
```

**Resilient Pattern:**
```python
import time

start = time.monotonic()
try:
    result = await dynamo_table.get_item(Key={"id": entity_id})
except Exception as e:
    duration_ms = (time.monotonic() - start) * 1000
    log_error("DynamoDB get_item failed",
              metadata={
                  "dependency": "dynamodb",
                  "operation": "get_item",
                  "entity_id": entity_id,
                  "duration_ms": round(duration_ms, 2),
                  "error_type": type(e).__name__,
              })
    raise
```

**Detection:** Search for error handlers that don't include operation name, entity ID, or dependency in metadata.

**Impact:** During multi-service outage, cannot determine which service is failing from logs alone.

---

# Category T: Security/Rate Limiting (Pattern 17)

---

## 17. No Per-User Rate Limiting

**Severity:** CRITICAL

**Description:** Authentication endpoints accept unlimited requests per user, enabling brute force attacks.

**Vulnerable Pattern:**
```python
async def verify_otp(phone_number, otp_code, ...):
    if stored_hash == hash(otp_code):
        return {"verified": True}  # No rate limit — brute force possible
```

**Resilient Pattern:**
```python
MAX_ATTEMPTS = 5
async def verify_otp(phone_number, otp_code, otp_repo, ...):
    record = await otp_repo.get_by_phone(phone_number)
    if record.attempts >= MAX_ATTEMPTS:
        raise ValueError("Too many attempts. Request a new code.")
    await otp_repo.increment_attempts(phone_number)
    if stored_hash != hash(otp_code):
        raise ValueError("Invalid OTP code")
```

**Detection:** Search for OTP/login verify endpoints without attempt counting.

**Impact:** Attacker brute-forces 6-digit OTP (1M combinations) to verify any phone number.

---

# Category A: Lambda-Specific Failures (Patterns 21-31)

---

## 21. Lambda-API Gateway Timeout Mismatch

**Severity:** CRITICAL

**Description:** Lambda timeout is configured longer than API Gateway's hard 29-second integration timeout limit. The client receives a 504 Gateway Timeout while Lambda continues executing and billing. The orphaned Lambda invocation may complete writes that the client assumes failed, causing duplicate operations on retry.

**Vulnerable Pattern:**
```python
# Pulumi infrastructure code
lambda_function = aws.lambda_.Function(
    "api-handler",
    timeout=300,  # 5 minutes — but API Gateway cuts off at 29s
    handler="api.main.handler",
    runtime="python3.14",
)

api_integration = aws.apigateway.Integration(
    "api-integration",
    type="AWS_PROXY",
    integration_http_method="POST",
    uri=lambda_function.invoke_arn,
    # API Gateway REST API hard limit: 29 seconds
)
```

**Resilient Pattern:**
```python
# Set Lambda timeout to 25 seconds (4s buffer under 29s limit)
lambda_function = aws.lambda_.Function(
    "api-handler",
    timeout=25,  # 4s buffer under API Gateway 29s limit
    handler="api.main.handler",
    runtime="python3.14",
)

# For long-running tasks, use async invocation pattern
async def start_long_task(task_id: str, payload: dict):
    """Start long-running task via async Lambda invocation."""
    await lambda_client.invoke(
        FunctionName="long-task-processor",
        InvocationType="Event",  # Async — returns 202 immediately
        Payload=json.dumps({"task_id": task_id, **payload}),
    )
    return {"task_id": task_id, "status": "processing"}
```

**Detection:** Compare Lambda timeout configuration against 29s API Gateway limit. Any Lambda behind REST API Gateway with timeout > 29s is vulnerable.

**Impact:** Client gets 504 after 29s. Lambda runs for remaining 271s, billing continues. Client retries, creating duplicate writes. At scale, orphaned invocations consume concurrency quota.

---

## 22. Ephemeral Storage (/tmp) Exhaustion

**Severity:** HIGH

**Description:** Files written to `/tmp` persist across warm Lambda invocations. Without cleanup, the 512MB default ephemeral storage fills up, causing `ENOSPC` (no space left on device) errors on subsequent invocations.

**Vulnerable Pattern:**
```python
import tempfile

async def process_upload(file_content: bytes, filename: str):
    temp_path = f"/tmp/{filename}"
    with open(temp_path, "wb") as f:
        f.write(file_content)
    # Process file...
    result = await analyze_file(temp_path)
    return result
    # /tmp file NOT cleaned up — persists across warm invocations
```

**Resilient Pattern:**
```python
import tempfile
import os

async def process_upload(file_content: bytes, filename: str):
    temp_path = None
    try:
        # Use unique temp file to avoid collisions
        fd, temp_path = tempfile.mkstemp(suffix=f"_{filename}", dir="/tmp")
        os.close(fd)
        with open(temp_path, "wb") as f:
            f.write(file_content)
        result = await analyze_file(temp_path)
        return result
    finally:
        # Always clean up temp files
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
```

**Detection:** Search for `/tmp` file writes without corresponding cleanup in `finally` blocks.

**Impact:** After ~50-100 warm invocations processing uploads, `/tmp` fills. All subsequent file operations fail with `OSError: [Errno 28] No space left on device`.

---

## 23. Lambda Concurrent Execution Limit vs API Gateway Throughput

**Severity:** CRITICAL

**Description:** API Gateway default throttle is 10,000 RPS but Lambda default concurrency is only 1,000 per region. API Gateway accepts requests that Lambda cannot process, resulting in throttling (429) errors visible only to end users.

**Vulnerable Pattern:**
```python
# Pulumi infrastructure — no concurrency planning
api_stage = aws.apigateway.Stage(
    "prod",
    stage_name="prod",
    # Default: 10,000 RPS throttle
)

lambda_function = aws.lambda_.Function(
    "api-handler",
    # Default: shares 1,000 regional concurrency with ALL functions
)
```

**Resilient Pattern:**
```python
# Match API Gateway throttle to Lambda capacity
api_stage = aws.apigateway.Stage(
    "prod",
    stage_name="prod",
    method_settings=[{
        "method_path": "*/*",
        "throttling_rate_limit": 500,   # Match Lambda capacity
        "throttling_burst_limit": 250,
    }],
)

# Reserve concurrency for critical functions
lambda_function = aws.lambda_.Function(
    "api-handler",
    reserved_concurrent_executions=200,  # Guaranteed capacity
)
```

**Detection:** Compare API Gateway throttle settings against Lambda reserved/unreserved concurrency. If API GW rate > Lambda concurrency, requests will throttle.

**Impact:** During traffic spikes, API Gateway accepts 10K RPS but Lambda can only handle 1K. 90% of requests return 429/502 errors. Users experience widespread failures.

---

## 24. Reserved Concurrency Starving Other Functions

**Severity:** HIGH

**Description:** Over-reserving concurrency for one Lambda function reduces the unreserved pool available to all other functions in the region. This can cause unrelated functions to throttle.

**Vulnerable Pattern:**
```python
# Reserve 900 of 1000 total regional concurrency
critical_function = aws.lambda_.Function(
    "critical-handler",
    reserved_concurrent_executions=900,
    # Leaves only 100 for ALL other functions in the region
)
```

**Resilient Pattern:**
```python
# Reserve proportionally, leave adequate unreserved pool
# Total regional limit: 1000 (default)
# Rule: never reserve more than 60% of total
api_handler = aws.lambda_.Function(
    "api-handler",
    reserved_concurrent_executions=200,
)

background_processor = aws.lambda_.Function(
    "background-processor",
    reserved_concurrent_executions=100,
)

# 700 unreserved concurrency remains for other functions
```

**Detection:** Sum all `reserved_concurrent_executions` across functions. If sum exceeds 80% of regional limit, other functions are at risk of starvation.

**Impact:** Background job function reserves 900 concurrency. Auth function (unreserved) throttles during traffic spike. All users locked out while background jobs run normally.

---

## 25. Lambda Payload Size Exceeded (6MB)

**Severity:** HIGH

**Description:** Lambda synchronous invocation has a 6MB response payload limit. Endpoints that return unbounded query results will fail with a 413 error when results exceed this limit.

**Vulnerable Pattern:**
```python
@router.get("/trail-systems/{org_id}/reports")
async def get_all_reports(org_id: str, repo=Depends(get_repo)):
    # Returns ALL reports — no pagination
    reports = await repo.list_all_reports(org_id)
    return {"reports": reports}  # Could be 10MB+ for active organizations
```

**Resilient Pattern:**
```python
@router.get("/trail-systems/{org_id}/reports")
async def get_reports(
    org_id: str,
    limit: int = Query(default=50, le=100),
    cursor: str = Query(default=None),
    repo=Depends(get_repo),
):
    reports, next_cursor = await repo.list_reports(
        org_id, limit=limit, cursor=cursor
    )
    return {
        "reports": reports,
        "next_cursor": next_cursor,
        "count": len(reports),
    }
```

**Detection:** Search for endpoints returning list results without `limit`/`cursor` parameters or pagination logic.

**Impact:** Organization with 5000+ reports triggers 6MB limit. Lambda returns 413, client receives opaque error. No partial results available.

---

## 26. Lambda Deployment Package Size Exceeded

**Severity:** MEDIUM

**Description:** Lambda has a 250MB unzipped deployment package limit (50MB zipped for direct upload). Adding dependencies without monitoring size can push past this limit, causing deployment failures.

**Vulnerable Pattern:**
```python
# requirements.txt growing without auditing
boto3==1.35.0
fastapi==0.115.0
pandas==2.2.0         # 150MB+ unzipped — do we actually need this?
numpy==2.1.0          # 50MB+ — pulled in by pandas
scipy==1.14.0         # 80MB+ — "just in case"
```

**Resilient Pattern:**
```python
# requirements.txt — audited, minimal dependencies
boto3==1.35.0
fastapi==0.115.0
# Heavy computation moved to separate Lambda with layer
# pandas/numpy only in data-processing function, not API handler

# CI/CD pipeline includes size check:
# unzip -l package.zip | tail -1 | awk '{print $1}'
# Fail if > 200MB (80% of 250MB limit)
```

**Detection:** Check deployment pipeline for package size validation. Audit `requirements.txt` for heavy libraries (pandas, numpy, scipy, tensorflow) in API handler functions.

**Impact:** Deployment fails silently or with cryptic error. Rollback required. CI/CD pipeline blocked until dependency audit completed.

---

## 27. Lambda Memory Leak Across Warm Invocations

**Severity:** HIGH

**Description:** Module-level mutable containers (dicts, lists, sets) grow unbounded across warm Lambda invocations. Without size limits, memory usage increases until the function hits its memory limit and is killed.

**Vulnerable Pattern:**
```python
# Module-level cache with no size limit
_cache = {}

async def get_user_profile(user_id: str, repo):
    if user_id in _cache:
        return _cache[user_id]
    profile = await repo.get(user_id)
    _cache[user_id] = profile  # Grows forever across warm invocations
    return profile
```

**Resilient Pattern:**
```python
from functools import lru_cache
from cachetools import TTLCache

# Bounded cache with TTL and max size
_profile_cache = TTLCache(maxsize=1000, ttl=300)  # 1000 items, 5min TTL

async def get_user_profile(user_id: str, repo):
    cached = _profile_cache.get(user_id)
    if cached is not None:
        return cached
    profile = await repo.get(user_id)
    _profile_cache[user_id] = profile
    return profile
```

**Detection:** Search for module-level mutable containers (`_cache = {}`, `_items = []`, `_seen = set()`) without `maxsize`, `TTLCache`, or `lru_cache` bounds.

**Impact:** After thousands of warm invocations, cache holds 100K+ entries. Lambda OOM-killed, cold start required. During high traffic, multiple functions OOM simultaneously.

---

## 28. Lambda Recursive Invocation Loop

**Severity:** CRITICAL

**Description:** Lambda writes to a service (S3, SNS, SQS, DynamoDB Streams) that triggers the same Lambda function, creating an infinite invocation loop. AWS charges for every invocation until the loop is detected or concurrency is exhausted.

**Vulnerable Pattern:**
```python
# Lambda triggered by S3 PutObject on bucket "uploads"
async def handle_s3_event(event, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        processed = await process_image(bucket, key)
        # Write BACK to the same bucket — triggers this Lambda again!
        await s3_client.put_object(
            Bucket=bucket,  # Same bucket that triggered us
            Key=f"processed/{key}",
            Body=processed,
        )
```

**Resilient Pattern:**
```python
# Option 1: Write to a different bucket
OUTPUT_BUCKET = os.environ["OUTPUT_BUCKET"]  # Different bucket

async def handle_s3_event(event, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        # Skip if already processed (prefix guard)
        if key.startswith("processed/"):
            return {"statusCode": 200, "body": "Skipped"}
        processed = await process_image(bucket, key)
        await s3_client.put_object(
            Bucket=OUTPUT_BUCKET,  # Different bucket — no loop
            Key=f"processed/{key}",
            Body=processed,
        )
```

**Detection:** Trace Lambda trigger source (S3 bucket, SNS topic, SQS queue, DynamoDB stream) and verify Lambda does not write back to the same source. Check for AWS recursive loop detection configuration.

**Impact:** Infinite loop creates thousands of invocations per second. At $0.20 per 1M invocations, a 10-minute loop at 1K/sec costs $120 and exhausts regional concurrency for all functions.

---

## 29. Lambda Environment Variable 4KB Limit

**Severity:** MEDIUM

**Description:** All Lambda environment variables combined cannot exceed 4KB. KMS-encrypted values are base64-encoded, increasing their size by ~33%. Adding new env vars can silently push past the limit, causing deployment failures.

**Vulnerable Pattern:**
```python
# Pulumi — adding env vars without tracking total size
lambda_function = aws.lambda_.Function(
    "api-handler",
    environment={
        "variables": {
            "DATABASE_URL": "...",           # 100 bytes
            "COGNITO_USER_POOL_ID": "...",   # 50 bytes
            "JWKS_URL": "...",               # 150 bytes
            "FEATURE_FLAGS": '{"flag1": true, "flag2": false, ...}',  # 2KB JSON blob
            "ALLOWED_ORIGINS": "https://a.com,https://b.com,...",     # 1KB
            # Total approaching 4KB limit
        }
    },
)
```

**Resilient Pattern:**
```python
# Store large config in SSM Parameter Store or Secrets Manager
lambda_function = aws.lambda_.Function(
    "api-handler",
    environment={
        "variables": {
            "CONFIG_PARAM_NAME": "/traillens/prod/config",  # Reference only
            "COGNITO_USER_POOL_ID": cognito_pool.id,
            "ENVIRONMENT": "prod",
        }
    },
)

# Application code loads config from SSM at cold start
_config = None

async def get_config():
    global _config
    if _config is None:
        ssm = session.client("ssm")
        param = await ssm.get_parameter(
            Name=os.environ["CONFIG_PARAM_NAME"], WithDecryption=True
        )
        _config = json.loads(param["Parameter"]["Value"])
    return _config
```

**Detection:** Sum environment variable sizes in Lambda configuration. Alert if total exceeds 3KB (75% of limit).

**Impact:** Adding a new environment variable causes deployment failure. Rollback required. If discovered in production deployment, service unavailable until resolved.

---

## 30. Cold Start Timeout During VPC ENI Attachment

**Severity:** HIGH

**Description:** Lambda functions in a VPC require an Elastic Network Interface (ENI). If the VPC subnet runs out of IP addresses or security group rules are misconfigured, ENI attachment fails or takes 10+ seconds, causing cold start timeouts.

**Vulnerable Pattern:**
```python
# Single small subnet for Lambda
vpc_subnet = aws.ec2.Subnet(
    "lambda-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/28",  # Only 11 usable IPs!
    # 1000 concurrent Lambda = 1000 ENIs needed
)

lambda_function = aws.lambda_.Function(
    "api-handler",
    vpc_config={
        "subnet_ids": [vpc_subnet.id],  # Single subnet, single AZ
        "security_group_ids": [sg.id],
    },
)
```

**Resilient Pattern:**
```python
# Multiple large subnets across AZs
lambda_subnets = []
for i, az in enumerate(["us-east-1a", "us-east-1b", "us-east-1c"]):
    subnet = aws.ec2.Subnet(
        f"lambda-subnet-{i}",
        vpc_id=vpc.id,
        cidr_block=f"10.0.{i * 32}.0/19",  # 8190 IPs each
        availability_zone=az,
    )
    lambda_subnets.append(subnet)

lambda_function = aws.lambda_.Function(
    "api-handler",
    vpc_config={
        "subnet_ids": [s.id for s in lambda_subnets],  # Multi-AZ
        "security_group_ids": [sg.id],
    },
)
```

**Detection:** Compare VPC subnet CIDR sizes against expected Lambda concurrency. A /28 subnet provides only 11 IPs. Each concurrent Lambda needs one IP.

**Impact:** During traffic spike, new Lambda instances cannot acquire ENIs. Cold starts fail with timeout. Users experience 10-30 second latency or 504 errors.

---

## 31. Lambda Layer Runtime Version Mismatch

**Severity:** MEDIUM

**Description:** Lambda Layers built with one Python version may contain C extensions (e.g., compiled `.so` files) incompatible with a different runtime version. Upgrading the function runtime without rebuilding layers causes import errors at runtime.

**Vulnerable Pattern:**
```python
# Layer built with Python 3.12
# Function upgraded to Python 3.14
lambda_function = aws.lambda_.Function(
    "api-handler",
    runtime="python3.14",
    layers=[
        # This layer was built with Python 3.12 — C extensions may break
        "arn:aws:lambda:us-east-1:123456:layer:my-deps:3",
    ],
)
```

**Resilient Pattern:**
```python
# Rebuild layers as part of runtime upgrade process
# CI/CD pipeline:
# 1. Build layer with target runtime
# 2. Test function with new layer
# 3. Deploy layer, then update function

lambda_layer = aws.lambda_.LayerVersion(
    "deps-layer",
    compatible_runtimes=["python3.14"],
    code=pulumi.FileArchive("./layer-python314.zip"),
    description="Dependencies built for Python 3.14",
)

lambda_function = aws.lambda_.Function(
    "api-handler",
    runtime="python3.14",
    layers=[lambda_layer.arn],  # Matching runtime
)
```

**Detection:** Compare layer `compatible_runtimes` against function runtime. Check layer build pipeline for runtime version pinning.

**Impact:** Function fails on cold start with `ImportError` for any C extension in the layer. All requests return 500 until layer is rebuilt.

---

# Category B: DynamoDB-Specific Failures (Patterns 32-39)

---

## 32. GSI Write Throttling Backpressure on Base Table

**Severity:** CRITICAL

**Description:** When a Global Secondary Index (GSI) cannot keep up with writes, DynamoDB throttles writes to the base table itself. This is because GSI updates are handled asynchronously and the base table write is rejected if the GSI replication lags too far behind.

**Vulnerable Pattern:**
```python
# Base table: on-demand (auto-scales)
# GSI: provisioned with low WCU — creates bottleneck
table = aws.dynamodb.Table(
    "trail-systems",
    billing_mode="PAY_PER_REQUEST",
    global_secondary_indexes=[{
        "name": "status-index",
        "hash_key": "status",  # Low cardinality — hot GSI partition
        "projection_type": "ALL",
        # GSI inherits on-demand but hot partition limits still apply
    }],
)
```

**Resilient Pattern:**
```python
table = aws.dynamodb.Table(
    "trail-systems",
    billing_mode="PAY_PER_REQUEST",
    global_secondary_indexes=[{
        "name": "org-updated-index",
        "hash_key": "org_id",       # High cardinality partition key
        "range_key": "updated_at",   # Enables time-range queries
        "projection_type": "KEYS_ONLY",  # Minimize GSI size
    }],
)

# Monitor GSI throttle metrics
gsi_throttle_alarm = aws.cloudwatch.MetricAlarm(
    "gsi-throttle-alarm",
    metric_name="WriteThrottleEvents",
    namespace="AWS/DynamoDB",
    dimensions={"TableName": "trail-systems", "GlobalSecondaryIndexName": "org-updated-index"},
    threshold=0,
    comparison_operator="GreaterThanThreshold",
)
```

**Detection:** Review GSI partition key cardinality. If GSI hash key has fewer than 100 distinct values, hot partition throttling is likely under load. Monitor `WriteThrottleEvents` per GSI.

**Impact:** GSI on `status` field (3 values: open/closed/maintenance) creates hot partition. At 1K writes/sec, GSI throttles, which throttles ALL base table writes. Entire API returns 500 errors.

---

## 33. DynamoDB Hot Partition Throttling

**Severity:** HIGH

**Description:** A single DynamoDB partition can handle at most 1,000 WCU or 3,000 RCU. If the partition key has low cardinality, one partition receives disproportionate traffic and throttles regardless of total table capacity.

**Vulnerable Pattern:**
```python
# Low-cardinality partition key — only 3 possible values
await table.put_item(Item={
    "partition_key": "active",     # Only: active, inactive, deleted
    "sort_key": f"trail#{trail_id}",
    "data": trail_data,
})
```

**Resilient Pattern:**
```python
import hashlib

def get_write_shard(entity_id: str, shard_count: int = 10) -> str:
    """Distribute writes across shards for hot keys."""
    shard = int(hashlib.md5(entity_id.encode()).hexdigest(), 16) % shard_count
    return str(shard)

# High-cardinality partition key with write sharding
await table.put_item(Item={
    "pk": f"ORG#{org_id}",              # High cardinality
    "sk": f"TRAIL#{trail_id}",
    "gsi1pk": f"STATUS#{status}#SHARD#{get_write_shard(trail_id)}",
    "data": trail_data,
})
```

**Detection:** Analyze partition key values. If fewer than 100 distinct partition key values exist and table receives >100 WCU, hot partition throttling is likely.

**Impact:** Table provisioned for 10,000 WCU but single partition limited to 1,000 WCU. 90% of capacity wasted. Users see intermittent throttling errors during peak usage.

---

## 34. DynamoDB Item Size Limit (400KB) Exceeded

**Severity:** HIGH

**Description:** DynamoDB items have a hard 400KB size limit. Items that grow over time (e.g., appending to list attributes) will silently fail when they reach this limit. The `ValidationException` is often not caught specifically.

**Vulnerable Pattern:**
```python
async def add_activity_log(table, trail_id: str, entry: dict):
    # list_append grows the item indefinitely
    await table.update_item(
        Key={"pk": f"TRAIL#{trail_id}", "sk": "METADATA"},
        UpdateExpression="SET activity_log = list_append(activity_log, :entry)",
        ExpressionAttributeValues={":entry": [entry]},
    )
    # Item grows until 400KB limit hit — ValidationException!
```

**Resilient Pattern:**
```python
MAX_LOG_ENTRIES = 100
ITEM_SIZE_WARN_KB = 350

async def add_activity_log(table, trail_id: str, entry: dict):
    # Check current item size before appending
    response = await table.get_item(
        Key={"pk": f"TRAIL#{trail_id}", "sk": "METADATA"},
        ProjectionExpression="activity_log",
    )
    current_log = response.get("Item", {}).get("activity_log", [])

    if len(current_log) >= MAX_LOG_ENTRIES:
        # Overflow to separate items
        await table.put_item(Item={
            "pk": f"TRAIL#{trail_id}",
            "sk": f"LOG#{datetime.now().isoformat()}",
            "entries": current_log[-50:],  # Archive older entries
        })
        # Keep only recent entries on main item
        current_log = current_log[-50:]

    current_log.append(entry)
    await table.update_item(
        Key={"pk": f"TRAIL#{trail_id}", "sk": "METADATA"},
        UpdateExpression="SET activity_log = :log",
        ExpressionAttributeValues={":log": current_log},
    )
```

**Detection:** Search for `list_append` in UpdateExpression without size guards or overflow logic. Any unbounded list attribute is a risk.

**Impact:** Active trail system accumulates 2000+ activity log entries. Item reaches 400KB. All subsequent updates fail with `ValidationException`. Trail system becomes read-only.

---

## 35. DynamoDB Transaction Conflict

**Severity:** HIGH

**Description:** `TransactWriteItems` uses optimistic concurrency control. If a non-transactional write modifies an item that is part of an active transaction, the transaction fails with `TransactionCanceledException`. Background processes (TTL cleanup, GSI backfill) can trigger this unexpectedly.

**Vulnerable Pattern:**
```python
# Transaction writes to user and org items
await dynamodb_client.transact_write_items(
    TransactItems=[
        {"Put": {"TableName": "users", "Item": user_item}},
        {"Put": {"TableName": "orgs", "Item": org_item}},
    ]
)

# Meanwhile, a background Lambda updates the same org item
# via non-transactional write — causes TransactionCanceledException
await table.update_item(
    Key={"pk": org_id},
    UpdateExpression="SET last_active = :now",
    ExpressionAttributeValues={":now": datetime.now().isoformat()},
)
```

**Resilient Pattern:**
```python
MAX_TRANSACTION_RETRIES = 3

async def create_user_with_org(dynamodb_client, user_item, org_item):
    for attempt in range(MAX_TRANSACTION_RETRIES):
        try:
            await dynamodb_client.transact_write_items(
                TransactItems=[
                    {"Put": {"TableName": "users", "Item": user_item}},
                    {"Update": {
                        "TableName": "orgs",
                        "Key": {"pk": org_item["pk"]},
                        "UpdateExpression": "SET member_count = member_count + :one",
                        "ExpressionAttributeValues": {":one": 1},
                    }},
                ]
            )
            return
        except ClientError as e:
            if e.response["Error"]["Code"] == "TransactionCanceledException":
                if attempt < MAX_TRANSACTION_RETRIES - 1:
                    await asyncio.sleep(0.1 * (2 ** attempt))
                    continue
            raise
```

**Detection:** Search for `transact_write_items` without `TransactionCanceledException` handling. Check for background processes that write to the same items.

**Impact:** User registration fails intermittently when background `last_active` update collides with registration transaction. Users see "Registration failed" during peak activity.

---

## 36. DynamoDB TTL Deletion Delay (Up to 48 Hours)

**Severity:** MEDIUM

**Description:** DynamoDB TTL does not delete items immediately when they expire. Expired items can remain visible in reads for up to 48 hours. Code that relies on TTL for session expiry or access control without explicit filtering will allow access to expired resources.

**Vulnerable Pattern:**
```python
async def get_session(table, session_id: str):
    response = await table.get_item(
        Key={"pk": f"SESSION#{session_id}", "sk": "DATA"}
    )
    item = response.get("Item")
    if item:
        return item  # TTL may be expired but item still exists!
    return None
```

**Resilient Pattern:**
```python
import time

async def get_session(table, session_id: str):
    response = await table.get_item(
        Key={"pk": f"SESSION#{session_id}", "sk": "DATA"}
    )
    item = response.get("Item")
    if item is None:
        return None

    # Always check expiry explicitly — never rely on TTL deletion
    expires_at = item.get("expires_at", 0)
    if int(expires_at) < int(time.time()):
        return None  # Expired — treat as non-existent

    return item
```

**Detection:** Search for DynamoDB reads of TTL-managed items without explicit expiry filtering (`expires_at > now()`).

**Impact:** User session expired 24 hours ago but TTL has not deleted the item. User retains access to resources they should no longer reach.

---

## 37. DynamoDB BatchWriteItem Partial Failure

**Severity:** HIGH

**Description:** `BatchWriteItem` is not atomic. It can succeed for some items and fail for others. Failed items are returned in `UnprocessedItems` but are silently dropped if the response is not checked.

**Vulnerable Pattern:**
```python
async def batch_create_entries(table, entries: list[dict]):
    # Process in batches of 25 (DynamoDB limit)
    for i in range(0, len(entries), 25):
        batch = entries[i:i + 25]
        await dynamodb_client.batch_write_item(
            RequestItems={
                table_name: [
                    {"PutRequest": {"Item": entry}} for entry in batch
                ]
            }
        )
        # UnprocessedItems NOT checked — failed items silently dropped
```

**Resilient Pattern:**
```python
MAX_BATCH_RETRIES = 5

async def batch_create_entries(table_name: str, entries: list[dict]):
    for i in range(0, len(entries), 25):
        batch = entries[i:i + 25]
        request_items = {
            table_name: [
                {"PutRequest": {"Item": entry}} for entry in batch
            ]
        }

        for attempt in range(MAX_BATCH_RETRIES):
            response = await dynamodb_client.batch_write_item(
                RequestItems=request_items
            )
            unprocessed = response.get("UnprocessedItems", {})
            if not unprocessed:
                break
            request_items = unprocessed
            # Exponential backoff for unprocessed items
            await asyncio.sleep(0.1 * (2 ** attempt))
        else:
            log_error("BatchWriteItem incomplete after retries",
                      error_code="DYNAMODB_BATCH_INCOMPLETE",
                      metadata={"unprocessed_count": sum(
                          len(v) for v in unprocessed.values()
                      )})
            raise RuntimeError("BatchWriteItem failed to complete")
```

**Detection:** Search for `batch_write_item` calls without checking `UnprocessedItems` in the response.

**Impact:** Bulk import of 500 trail system entries. 23 items fail due to throttling. Data appears complete but 23 entries are silently missing. Discovered weeks later by users.

---

## 38. DynamoDB Scan Without Pagination

**Severity:** CRITICAL

**Description:** DynamoDB `Scan` and `Query` return at most 1MB of data per response. Without checking `LastEvaluatedKey` and paginating, the application receives only partial results and treats them as complete.

**Vulnerable Pattern:**
```python
async def get_all_trail_systems(table, org_id: str):
    response = await table.query(
        KeyConditionExpression=Key("pk").eq(f"ORG#{org_id}"),
    )
    return response["Items"]  # Only first 1MB! Could be 20% of total
```

**Resilient Pattern:**
```python
async def get_all_trail_systems(table, org_id: str) -> list[dict]:
    items = []
    last_key = None

    while True:
        kwargs = {
            "KeyConditionExpression": Key("pk").eq(f"ORG#{org_id}"),
        }
        if last_key:
            kwargs["ExclusiveStartKey"] = last_key

        response = await table.query(**kwargs)
        items.extend(response["Items"])

        last_key = response.get("LastEvaluatedKey")
        if not last_key:
            break

    return items
```

**Detection:** Search for `table.scan()` or `table.query()` calls that access `response["Items"]` without checking `LastEvaluatedKey`.

**Impact:** Organization with 2000 trail systems. Query returns first 200 (1MB). Admin dashboard shows 200 trail systems. 1800 trail systems invisible. Data integrity silently compromised.

---

## 39. DynamoDB Conditional Check Failure Without Retry

**Severity:** MEDIUM

**Description:** Optimistic locking with `ConditionExpression` is expected to fail under concurrent access. Without catching `ConditionalCheckFailedException` and retrying with a fresh version, operations fail unnecessarily.

**Vulnerable Pattern:**
```python
async def update_trail_count(table, org_id: str, delta: int):
    await table.update_item(
        Key={"pk": f"ORG#{org_id}", "sk": "METADATA"},
        UpdateExpression="SET trail_count = trail_count + :delta, version = version + :one",
        ConditionExpression="version = :expected_version",
        ExpressionAttributeValues={
            ":delta": delta,
            ":one": 1,
            ":expected_version": current_version,
        },
    )
    # ConditionalCheckFailedException not handled — operation fails
```

**Resilient Pattern:**
```python
MAX_OPTIMISTIC_RETRIES = 5

async def update_trail_count(table, org_id: str, delta: int):
    for attempt in range(MAX_OPTIMISTIC_RETRIES):
        # Read current version
        response = await table.get_item(
            Key={"pk": f"ORG#{org_id}", "sk": "METADATA"},
            ProjectionExpression="trail_count, version",
        )
        item = response["Item"]
        current_version = item["version"]

        try:
            await table.update_item(
                Key={"pk": f"ORG#{org_id}", "sk": "METADATA"},
                UpdateExpression="SET trail_count = trail_count + :delta, version = :new_ver",
                ConditionExpression="version = :expected",
                ExpressionAttributeValues={
                    ":delta": delta,
                    ":new_ver": current_version + 1,
                    ":expected": current_version,
                },
            )
            return  # Success
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                if attempt < MAX_OPTIMISTIC_RETRIES - 1:
                    await asyncio.sleep(0.05 * (2 ** attempt))
                    continue
            raise

    raise RuntimeError("Optimistic lock failed after max retries")
```

**Detection:** Search for `ConditionExpression` usage without `ConditionalCheckFailedException` exception handling and retry logic.

**Impact:** Two admins add trail systems simultaneously. One update fails with unhandled exception. Trail count becomes incorrect. Requires manual correction.

---

# Category C: SES-Specific Failures (Patterns 40-43)

---

## 40. SES Bounce Rate Exceeding Account Threshold

**Severity:** CRITICAL

**Description:** AWS SES monitors bounce rates across the account. If the bounce rate exceeds 5%, the account enters review. Above 10%, all sending is paused. A single campaign to stale email addresses can shut down transactional email for the entire application.

**Vulnerable Pattern:**
```python
async def send_welcome_emails(ses_client, user_emails: list[str]):
    for email in user_emails:
        # No validation, no bounce processing, no suppression list
        await ses_client.send_email(
            Source="noreply@traillens.com",
            Destination={"ToAddresses": [email]},
            Message={"Subject": {"Data": "Welcome"}, "Body": {"Text": {"Data": "..."}}},
        )
```

**Resilient Pattern:**
```python
async def send_welcome_email(ses_client, email: str, suppression_repo):
    # Check suppression list before sending
    if await suppression_repo.is_suppressed(email):
        log_info("Skipping suppressed email", metadata={"email_hash": hash(email)})
        return {"sent": False, "reason": "suppressed"}

    try:
        await ses_client.send_email(
            Source="noreply@traillens.com",
            Destination={"ToAddresses": [email]},
            Message={"Subject": {"Data": "Welcome"}, "Body": {"Text": {"Data": "..."}}},
        )
        return {"sent": True}
    except ClientError as e:
        if "MessageRejected" in str(e):
            await suppression_repo.add(email, reason="rejected")
        raise

# Separate bounce handler (SNS subscription)
async def handle_bounce_notification(event):
    bounce = json.loads(event["Message"])
    for recipient in bounce["bounce"]["bouncedRecipients"]:
        await suppression_repo.add(
            recipient["emailAddress"],
            reason=bounce["bounce"]["bounceType"],
        )
```

**Detection:** Search for SES `send_email` calls without checking a suppression list. Verify SNS subscription exists for SES bounce notifications.

**Impact:** Marketing campaign sent to 10,000 addresses including 600 stale ones. Bounce rate hits 6%. AWS pauses account review. All transactional email (password resets, OTP codes, trail condition alerts) blocked for 24-48 hours.

---

## 41. SES Complaint Rate Threshold Violation

**Severity:** CRITICAL

**Description:** SES complaint rate threshold is 0.1% for review and 0.5% for pause. Users marking emails as spam count as complaints. Without complaint processing and unsubscribe honoring, the account can be suspended.

**Vulnerable Pattern:**
```python
async def send_trail_alert(ses_client, subscribers: list[str], alert: dict):
    for email in subscribers:
        # No unsubscribe link, no complaint handling
        await ses_client.send_email(
            Source="alerts@traillens.com",
            Destination={"ToAddresses": [email]},
            Message={
                "Subject": {"Data": f"Trail Alert: {alert['title']}"},
                "Body": {"Text": {"Data": alert["body"]}},
            },
        )
```

**Resilient Pattern:**
```python
async def send_trail_alert(ses_client, email: str, alert: dict, prefs_repo):
    # Check user preferences before sending
    prefs = await prefs_repo.get_preferences(email)
    if not prefs.get("trail_alerts_enabled", True):
        return {"sent": False, "reason": "unsubscribed"}

    unsubscribe_url = generate_unsubscribe_url(email, "trail_alerts")

    await ses_client.send_email(
        Source="alerts@traillens.com",
        Destination={"ToAddresses": [email]},
        Message={
            "Subject": {"Data": f"Trail Alert: {alert['title']}"},
            "Body": {"Html": {"Data": f"""
                {alert['body']}
                <br><br>
                <a href="{unsubscribe_url}">Unsubscribe from trail alerts</a>
            """}},
        },
        # List-Unsubscribe header for email clients
        Tags=[{"Name": "category", "Value": "trail_alerts"}],
    )

# Process complaint notifications
async def handle_complaint(event):
    complaint = json.loads(event["Message"])
    for recipient in complaint["complaint"]["complainedRecipients"]:
        await prefs_repo.disable_all_emails(recipient["emailAddress"])
```

**Detection:** Search for SES sends without unsubscribe links in HTML body. Verify complaint notification SNS subscription exists.

**Impact:** 50 users mark trail alerts as spam. Complaint rate exceeds 0.5%. AWS pauses all email sending. Password resets and OTP codes stop working. Users locked out of accounts.

---

## 42. SES Sandbox Mode Sending Restriction

**Severity:** HIGH

**Description:** New SES accounts start in sandbox mode with severe restrictions: 200 emails/day, 1 email/second, and only verified email addresses can receive mail. Production deployment without requesting production access causes all transactional emails to fail for non-verified recipients.

**Vulnerable Pattern:**
```python
# Deployed to production without checking SES account status
async def send_otp(ses_client, phone_email: str, otp_code: str):
    await ses_client.send_email(
        Source="noreply@traillens.com",
        Destination={"ToAddresses": [phone_email]},
        Message={
            "Subject": {"Data": "Your verification code"},
            "Body": {"Text": {"Data": f"Code: {otp_code}"}},
        },
    )
    # Fails for every non-verified email address in sandbox!
```

**Resilient Pattern:**
```python
# Pre-deployment checklist in CI/CD
async def verify_ses_production_access(ses_client):
    """Verify SES account is out of sandbox before deployment."""
    response = await ses_client.get_account()
    if response.get("EnforcementStatus") != "HEALTHY":
        raise RuntimeError(
            "SES account not in production mode. "
            "Request production access: https://console.aws.amazon.com/ses/"
        )
    send_quota = response.get("SendQuota", {})
    if send_quota.get("Max24HourSend", 0) <= 200:
        raise RuntimeError("SES still in sandbox mode (200/day limit)")

# Application code with proper error handling
async def send_otp(ses_client, email: str, otp_code: str):
    try:
        await ses_client.send_email(
            Source="noreply@traillens.com",
            Destination={"ToAddresses": [email]},
            Message={
                "Subject": {"Data": "Your verification code"},
                "Body": {"Text": {"Data": f"Code: {otp_code}"}},
            },
        )
    except ClientError as e:
        if "MessageRejected" in str(e) and "not verified" in str(e).lower():
            log_error("SES sandbox restriction", error_code="SES_SANDBOX_BLOCK",
                      metadata={"email_domain": email.split("@")[1]})
        raise
```

**Detection:** Check SES account status in deployment pipeline. Verify `get_account()` returns production-level quotas before production deployment.

**Impact:** Application launches. First 200 users receive verification emails. User 201+ cannot verify their email. Registration effectively broken until SES production access approved (1-3 business days).

---

## 43. SES Sending Quota Exhaustion

**Severity:** HIGH

**Description:** SES enforces daily sending quotas and per-second rate limits. Burst-sending (e.g., batch notifications) without rate limiting exhausts the quota, causing `ThrottlingException` for all subsequent sends including critical transactional emails.

**Vulnerable Pattern:**
```python
async def send_bulk_trail_alerts(ses_client, subscribers: list[str], alert: dict):
    # Send to 5000 subscribers as fast as possible
    tasks = [
        ses_client.send_email(
            Source="alerts@traillens.com",
            Destination={"ToAddresses": [email]},
            Message={"Subject": {"Data": alert["title"]}, "Body": {"Text": {"Data": alert["body"]}}},
        )
        for email in subscribers
    ]
    await asyncio.gather(*tasks)  # 5000 concurrent sends — exceeds rate limit
```

**Resilient Pattern:**
```python
import asyncio

SES_RATE_LIMIT = 10  # emails per second (adjust to account quota)

async def send_bulk_trail_alerts(ses_client, subscribers: list[str], alert: dict):
    semaphore = asyncio.Semaphore(SES_RATE_LIMIT)
    results = {"sent": 0, "failed": 0}

    async def rate_limited_send(email: str):
        async with semaphore:
            try:
                await ses_client.send_email(
                    Source="alerts@traillens.com",
                    Destination={"ToAddresses": [email]},
                    Message={
                        "Subject": {"Data": alert["title"]},
                        "Body": {"Text": {"Data": alert["body"]}},
                    },
                )
                results["sent"] += 1
            except ClientError as e:
                if "Throttling" in str(e):
                    await asyncio.sleep(1)  # Back off on throttle
                results["failed"] += 1
            await asyncio.sleep(0.1)  # Rate limit spacing

    tasks = [rate_limited_send(email) for email in subscribers]
    await asyncio.gather(*tasks)
    return results
```

**Detection:** Search for SES `send_email` in loops or `asyncio.gather` without rate limiting (semaphore or sleep). Check for `ThrottlingException` handling.

**Impact:** Bulk alert send exhausts daily quota by 10 AM. All password reset and OTP emails fail for the rest of the day. Users cannot log in or recover accounts.

---

# Category D: SNS-Specific Failures (Patterns 44-46)

---

## 44. SNS Message Attribute Filtering Mismatch

**Severity:** MEDIUM

**Description:** SNS subscription filter policies silently drop messages that do not match. If publish code changes attribute names or values without updating subscription filters, messages are discarded without any error.

**Vulnerable Pattern:**
```python
# Publisher changed attribute name from "event_type" to "type"
await sns_client.publish(
    TopicArn=topic_arn,
    Message=json.dumps(event_data),
    MessageAttributes={
        "type": {  # Was "event_type" — filter policy doesn't match
            "DataType": "String",
            "StringValue": "trail_alert",
        }
    },
)

# Subscription filter still expects "event_type"
# Filter policy: {"event_type": ["trail_alert"]}
# Result: message silently dropped
```

**Resilient Pattern:**
```python
# Define attribute names as constants shared between publisher and subscriber
ATTR_EVENT_TYPE = "event_type"
ATTR_PRIORITY = "priority"

async def publish_trail_alert(sns_client, topic_arn: str, event_data: dict):
    await sns_client.publish(
        TopicArn=topic_arn,
        Message=json.dumps(event_data),
        MessageAttributes={
            ATTR_EVENT_TYPE: {
                "DataType": "String",
                "StringValue": "trail_alert",
            },
            ATTR_PRIORITY: {
                "DataType": "String",
                "StringValue": event_data.get("priority", "normal"),
            },
        },
    )

# Integration test validates filter policy matches publish attributes
async def test_filter_policy_matches_publish():
    """Verify subscription filter policies match published attributes."""
    subscriptions = await sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)
    for sub in subscriptions["Subscriptions"]:
        attrs = await sns_client.get_subscription_attributes(
            SubscriptionArn=sub["SubscriptionArn"]
        )
        filter_policy = json.loads(attrs["Attributes"].get("FilterPolicy", "{}"))
        for key in filter_policy:
            assert key in [ATTR_EVENT_TYPE, ATTR_PRIORITY], f"Unknown filter key: {key}"
```

**Detection:** Cross-reference SNS `publish` `MessageAttributes` keys with subscription `FilterPolicy` keys. Any mismatch means messages are silently dropped.

**Impact:** Trail condition alerts published with wrong attribute name. No subscribers receive alerts. No error logged. Users unaware of dangerous trail conditions.

---

## 45. SNS FIFO Topic Endpoint Limitation

**Severity:** MEDIUM

**Description:** SNS FIFO topics only support SQS FIFO queues as subscribers. HTTP/HTTPS endpoints, email, SMS, and Lambda subscriptions are not supported and will silently fail or be rejected.

**Vulnerable Pattern:**
```python
# FIFO topic created for ordered message delivery
fifo_topic = aws.sns.Topic(
    "trail-events",
    fifo_topic=True,
    name="trail-events.fifo",
)

# HTTP endpoint subscription — NOT supported on FIFO topics
aws.sns.TopicSubscription(
    "webhook-subscription",
    topic=fifo_topic.arn,
    protocol="https",
    endpoint="https://api.traillens.com/webhooks/trail-events",
    # This will fail or be silently ignored
)
```

**Resilient Pattern:**
```python
# Use standard topic for HTTP/Lambda subscribers
standard_topic = aws.sns.Topic(
    "trail-events",
    name="trail-events",
    # Standard topic — supports all subscription protocols
)

# If ordering is needed, use SQS FIFO as intermediary
fifo_queue = aws.sqs.Queue(
    "trail-events-ordered",
    fifo_queue=True,
    name="trail-events-ordered.fifo",
)

# Standard topic → SQS FIFO for ordered processing
# Standard topic → HTTP/Lambda for real-time notifications
```

**Detection:** Check SNS FIFO topic subscriptions for non-SQS protocol types (HTTP, HTTPS, email, SMS, Lambda).

**Impact:** Webhook notification system built on FIFO topic. Subscriptions silently fail. External integrations never receive events. Discovered only when partner complains about missing data.

---

## 46. SNS Message Size Limit (256KB)

**Severity:** MEDIUM

**Description:** SNS messages have a hard 256KB limit. Publishing messages with large payloads (e.g., including full entity data instead of just IDs) fails with `InvalidParameterValue`.

**Vulnerable Pattern:**
```python
async def publish_trail_update(sns_client, topic_arn: str, trail_data: dict):
    # Full trail data including images, history, metadata
    await sns_client.publish(
        TopicArn=topic_arn,
        Message=json.dumps(trail_data),  # Could be 500KB+
    )
```

**Resilient Pattern:**
```python
import sys

MAX_SNS_MESSAGE_BYTES = 256 * 1024  # 256KB

async def publish_trail_update(sns_client, topic_arn: str, trail_id: str, event_type: str):
    # Publish reference, not full data — subscribers fetch details
    message = json.dumps({
        "trail_id": trail_id,
        "event_type": event_type,
        "timestamp": datetime.now().isoformat(),
    })

    message_size = sys.getsizeof(message.encode("utf-8"))
    if message_size > MAX_SNS_MESSAGE_BYTES:
        log_error("SNS message too large", metadata={"size": message_size})
        raise ValueError(f"Message size {message_size} exceeds 256KB limit")

    await sns_client.publish(TopicArn=topic_arn, Message=message)
```

**Detection:** Search for `sns_client.publish` where `Message` contains full entity data or unbounded content without size validation.

**Impact:** Trail system with extensive metadata generates 300KB message. Publish fails. Trail update succeeds in DB but notification lost. Subscribers out of sync.

---

# Category E: Cognito-Specific Failures (Patterns 47-50)

---

## 47. Cognito Token Revocation Gap

**Severity:** CRITICAL

**Description:** When a Cognito refresh token is revoked (e.g., on password change or admin action), the associated access and ID tokens remain valid until their natural expiry (default 1 hour). Applications that only verify token signature and expiration continue granting access to revoked sessions.

**Vulnerable Pattern:**
```python
async def verify_token(token: str, jwks):
    # Only checks signature and expiration — NOT revocation
    payload = jwt.decode(
        token,
        jwks,
        algorithms=["RS256"],
        audience=CLIENT_ID,
    )
    return payload  # Token may be revoked but still valid!
```

**Resilient Pattern:**
```python
ACCESS_TOKEN_TTL = 300  # 5 minutes — minimize revocation gap

async def verify_token(token: str, jwks):
    payload = jwt.decode(
        token,
        jwks,
        algorithms=["RS256"],
        audience=CLIENT_ID,
    )

    # For sensitive operations, check token against revocation
    token_use = payload.get("token_use")
    if token_use == "access":
        # Short-lived tokens (5 min) minimize revocation gap
        # For admin/destructive operations, verify with Cognito directly
        if is_sensitive_operation():
            try:
                await cognito_client.get_user(AccessToken=token)
            except ClientError as e:
                if e.response["Error"]["Code"] == "NotAuthorizedException":
                    raise HTTPException(status_code=401, detail="Token revoked")
                raise
    return payload

# Configure short access token lifetime in Cognito
# User Pool → App client → Access token expiration: 5 minutes
```

**Detection:** Search for JWT verification code that checks only signature and expiration without revocation checking. Review Cognito access token TTL configuration.

**Impact:** Admin revokes compromised user session. Attacker continues using access token for up to 1 hour. All actions during this window are authorized despite revocation. Data exfiltration or unauthorized modifications occur.

---

## 48. Cognito User Pool Rate Limit Exhaustion

**Severity:** HIGH

**Description:** Cognito has default rate limits: 50 sign-ups/second, 120 sign-ins/second. Each Lambda invocation that calls Cognito for token verification (instead of verifying locally) multiplies API calls. At scale, rate limits are quickly exhausted.

**Vulnerable Pattern:**
```python
async def verify_user(access_token: str):
    # Calls Cognito API for EVERY request — 1000 RPS = 1000 Cognito calls/sec
    response = await cognito_client.get_user(AccessToken=access_token)
    return response["UserAttributes"]
```

**Resilient Pattern:**
```python
import jwt
from cachetools import TTLCache

# Cache JWKS locally — verify tokens without Cognito API calls
_jwks_cache = TTLCache(maxsize=10, ttl=3600)

async def get_jwks_cached(jwks_url: str):
    cached = _jwks_cache.get("jwks")
    if cached:
        return cached
    async with httpx.AsyncClient() as client:
        response = await client.get(jwks_url, timeout=5)
        jwks = response.json()
    _jwks_cache["jwks"] = jwks
    return jwks

async def verify_user(access_token: str, jwks_url: str):
    # Local verification — zero Cognito API calls
    jwks = await get_jwks_cached(jwks_url)
    payload = jwt.decode(
        access_token,
        jwks,
        algorithms=["RS256"],
        audience=CLIENT_ID,
    )
    return payload
```

**Detection:** Search for `cognito_client.get_user()` or `cognito_client.admin_get_user()` in authentication middleware (called per request). These should be replaced with local JWT verification.

**Impact:** At 1,000 RPS, every request calls Cognito. Rate limit (120/sec) exceeded by 8x. All authentication fails. Users see "Too many requests" errors across the entire application.

---

## 49. Cognito Hosted UI Custom Domain Propagation

**Severity:** MEDIUM

**Description:** Cognito custom domain changes propagate through CloudFront and can take up to 60 minutes. Deployment scripts that verify the domain immediately after change will fail or see stale configuration.

**Vulnerable Pattern:**
```python
# Infrastructure deployment script
await cognito_client.update_user_pool_domain(
    Domain="auth.traillens.com",
    UserPoolId=user_pool_id,
    CustomDomainConfig={"CertificateArn": new_cert_arn},
)

# Immediately verify — will likely fail
response = await cognito_client.describe_user_pool_domain(Domain="auth.traillens.com")
assert response["DomainDescription"]["Status"] == "ACTIVE"  # FAILS — still propagating
```

**Resilient Pattern:**
```python
import asyncio

async def update_cognito_domain(cognito_client, domain: str, pool_id: str, cert_arn: str):
    await cognito_client.update_user_pool_domain(
        Domain=domain,
        UserPoolId=pool_id,
        CustomDomainConfig={"CertificateArn": cert_arn},
    )

    # Poll with timeout — propagation takes up to 60 minutes
    max_wait = 3600  # 60 minutes
    poll_interval = 30  # seconds
    elapsed = 0

    while elapsed < max_wait:
        response = await cognito_client.describe_user_pool_domain(Domain=domain)
        status = response["DomainDescription"]["Status"]
        if status == "ACTIVE":
            log_info("Cognito domain active", metadata={"domain": domain})
            return
        if status == "FAILED":
            raise RuntimeError(f"Cognito domain update failed: {domain}")
        log_info("Waiting for domain propagation",
                 metadata={"status": status, "elapsed_s": elapsed})
        await asyncio.sleep(poll_interval)
        elapsed += poll_interval

    raise TimeoutError(f"Cognito domain not active after {max_wait}s")
```

**Detection:** Search for `update_user_pool_domain` followed by immediate `describe_user_pool_domain` without polling/waiting logic.

**Impact:** Certificate rotation script marks deployment as failed. Manual intervention required. If old certificate expires before propagation completes, login pages show SSL errors.

---

## 50. Cognito Token Size Increase After Enabling Revocation

**Severity:** LOW

**Description:** Enabling token revocation on a Cognito User Pool adds the `origin_jti` claim to access and ID tokens. This increases token size, which can break applications with hardcoded token size limits or cookie size constraints.

**Vulnerable Pattern:**
```python
# Cookie-based token storage with fixed size limit
def set_auth_cookie(response, token: str):
    # 4096 byte cookie limit — tokens with revocation claims may exceed this
    response.set_cookie(
        key="access_token",
        value=token,
        max_age=3600,
        httponly=True,
        # No size check — may silently truncate or fail
    )
```

**Resilient Pattern:**
```python
MAX_COOKIE_SIZE = 4096

def set_auth_cookie(response, token: str):
    token_size = len(token.encode("utf-8"))
    if token_size > MAX_COOKIE_SIZE:
        log_warning("Token exceeds cookie size limit",
                    metadata={"token_size": token_size, "limit": MAX_COOKIE_SIZE})
        # Fall back to header-based auth or session reference
        session_id = create_session_reference(token)
        response.set_cookie(
            key="session_id",
            value=session_id,
            max_age=3600,
            httponly=True,
        )
        return

    response.set_cookie(
        key="access_token",
        value=token,
        max_age=3600,
        httponly=True,
    )
```

**Detection:** Search for token storage code with hardcoded size limits. Check Cognito User Pool revocation settings and measure token sizes.

**Impact:** Enabling revocation adds ~50 bytes to tokens. Tokens near cookie limit break. Some users cannot authenticate until cookie handling is updated.

---

# Category F: S3-Specific Failures (Patterns 51-52)

---

## 51. Abandoned Multipart Upload Storage Leak

**Severity:** MEDIUM

**Description:** Failed or aborted multipart uploads leave orphaned parts in S3, incurring storage costs. Without a lifecycle rule to clean up incomplete uploads, these costs accumulate indefinitely.

**Vulnerable Pattern:**
```python
# S3 bucket without multipart cleanup lifecycle rule
bucket = aws.s3.Bucket(
    "trail-photos",
    # No lifecycle rules — orphaned multipart parts accumulate forever
)

# Upload code that can fail mid-upload
async def upload_large_file(s3_client, bucket: str, key: str, file_path: str):
    upload = await s3_client.create_multipart_upload(Bucket=bucket, Key=key)
    upload_id = upload["UploadId"]
    # If this crashes, upload parts remain forever
    parts = []
    for i, chunk in enumerate(read_chunks(file_path)):
        part = await s3_client.upload_part(
            Bucket=bucket, Key=key, UploadId=upload_id,
            PartNumber=i + 1, Body=chunk,
        )
        parts.append({"PartNumber": i + 1, "ETag": part["ETag"]})
    await s3_client.complete_multipart_upload(
        Bucket=bucket, Key=key, UploadId=upload_id,
        MultipartUpload={"Parts": parts},
    )
```

**Resilient Pattern:**
```python
# S3 bucket with multipart cleanup lifecycle rule
bucket = aws.s3.Bucket(
    "trail-photos",
    lifecycle_rules=[{
        "id": "cleanup-incomplete-uploads",
        "enabled": True,
        "abort_incomplete_multipart_upload_days": 7,
    }],
)

# Upload code with proper cleanup on failure
async def upload_large_file(s3_client, bucket: str, key: str, file_path: str):
    upload = await s3_client.create_multipart_upload(Bucket=bucket, Key=key)
    upload_id = upload["UploadId"]
    try:
        parts = []
        for i, chunk in enumerate(read_chunks(file_path)):
            part = await s3_client.upload_part(
                Bucket=bucket, Key=key, UploadId=upload_id,
                PartNumber=i + 1, Body=chunk,
            )
            parts.append({"PartNumber": i + 1, "ETag": part["ETag"]})
        await s3_client.complete_multipart_upload(
            Bucket=bucket, Key=key, UploadId=upload_id,
            MultipartUpload={"Parts": parts},
        )
    except Exception:
        await s3_client.abort_multipart_upload(
            Bucket=bucket, Key=key, UploadId=upload_id,
        )
        raise
```

**Detection:** Search for S3 bucket definitions without `abort_incomplete_multipart_upload_days` lifecycle rule. Check for `create_multipart_upload` without try/finally cleanup.

**Impact:** 100 failed uploads per day leave 5GB of orphaned parts per month. At $0.023/GB, costs are small individually but accumulate to $1,380/year without cleanup.

---

## 52. S3 Lifecycle Rule Overwrite on Update

**Severity:** HIGH

**Description:** `put_bucket_lifecycle_configuration` replaces ALL existing lifecycle rules. Adding a new rule without reading existing rules first deletes all previous rules, potentially removing critical expiration and transition policies.

**Vulnerable Pattern:**
```python
# Adding a new rule — overwrites ALL existing rules
async def add_archive_rule(s3_client, bucket: str):
    await s3_client.put_bucket_lifecycle_configuration(
        Bucket=bucket,
        LifecycleConfiguration={
            "Rules": [{
                "ID": "archive-old-photos",
                "Status": "Enabled",
                "Transitions": [{"Days": 90, "StorageClass": "GLACIER"}],
                "Filter": {"Prefix": "photos/"},
            }]
            # Existing rules (cleanup, expiration) are DELETED
        },
    )
```

**Resilient Pattern:**
```python
async def add_lifecycle_rule(s3_client, bucket: str, new_rule: dict):
    # Read existing rules first
    try:
        existing = await s3_client.get_bucket_lifecycle_configuration(Bucket=bucket)
        rules = existing.get("Rules", [])
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchLifecycleConfiguration":
            rules = []
        else:
            raise

    # Check for duplicate rule ID
    existing_ids = {r["ID"] for r in rules}
    if new_rule["ID"] in existing_ids:
        rules = [r if r["ID"] != new_rule["ID"] else new_rule for r in rules]
    else:
        rules.append(new_rule)

    # Write back ALL rules (existing + new)
    await s3_client.put_bucket_lifecycle_configuration(
        Bucket=bucket,
        LifecycleConfiguration={"Rules": rules},
    )
```

**Detection:** Search for `put_bucket_lifecycle_configuration` calls without a preceding `get_bucket_lifecycle_configuration`.

**Impact:** Adding archive rule deletes cleanup rule. Incomplete multipart uploads accumulate. Temporary files never expire. Storage costs increase 300% over 6 months before discovery.

---

# Category G: Python/asyncio Failures (Patterns 53-59)

---

## 53. aioboto3 Event Loop Closed on Reuse

**Severity:** HIGH

**Description:** When using `asyncio.run()` (as Mangum does per invocation), a module-level `aioboto3.Session()` references the event loop from the first invocation. On warm starts, a new event loop is created but the cached session still references the old (closed) loop, causing `RuntimeError: Event loop is closed`.

**Vulnerable Pattern:**
```python
import aioboto3

# Module-level session — binds to first event loop
session = aioboto3.Session()

async def handler(event, context):
    # Second invocation: new event loop, but session references old closed loop
    async with session.resource("dynamodb") as dynamo:
        table = await dynamo.Table("trail-systems")
        # RuntimeError: Event loop is closed
```

**Resilient Pattern:**
```python
import aioboto3

async def handler(event, context):
    # Create session per invocation — uses current event loop
    session = aioboto3.Session()
    async with session.resource("dynamodb") as dynamo:
        table = await dynamo.Table("trail-systems")
        # Works correctly with any event loop

# Alternative: lazy session initialization
_session = None

def get_session():
    global _session
    try:
        loop = asyncio.get_running_loop()
        if _session is None or _session._session._loop is not loop:
            _session = aioboto3.Session()
    except RuntimeError:
        _session = aioboto3.Session()
    return _session
```

**Detection:** Search for `aioboto3.Session()` at module level (outside async functions). Check if Mangum or `asyncio.run()` is used (creates new event loop per invocation).

**Impact:** First Lambda invocation succeeds. All warm-start invocations fail with `RuntimeError: Event loop is closed`. Appears as intermittent failure — works after cold start, fails on reuse.

---

## 54. aioboto3 Resource Not Closed (Session Leak)

**Severity:** HIGH

**Description:** Since aioboto3 v8.0+, resources and clients must be used as async context managers. Creating them without `async with` leaks connections and file descriptors, eventually causing `ResourceWarning` and connection pool exhaustion.

**Vulnerable Pattern:**
```python
async def get_trail(table_name: str, trail_id: str):
    session = aioboto3.Session()
    dynamodb = await session.resource("dynamodb")  # NOT closed!
    table = await dynamodb.Table(table_name)
    response = await table.get_item(Key={"pk": trail_id})
    # Connection leaked — never closed
    return response.get("Item")
```

**Resilient Pattern:**
```python
async def get_trail(table_name: str, trail_id: str):
    session = aioboto3.Session()
    async with session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table(table_name)
        response = await table.get_item(Key={"pk": trail_id})
        return response.get("Item")
    # Resource properly closed on exit
```

**Detection:** Search for `await session.resource(` or `await session.client(` without `async with`. Any aioboto3 resource/client creation not inside `async with` is a leak.

**Impact:** Each leaked resource holds open HTTP connections. After 50 invocations, connection pool exhausted. All DynamoDB calls hang waiting for connections. Lambda timeout.

---

## 55. asyncio Task Cancellation Not Re-raised

**Severity:** HIGH

**Description:** `asyncio.CancelledError` is used by the event loop to cancel tasks during shutdown. Catching it without re-raising breaks structured concurrency and prevents proper cleanup, potentially leaving the application in an inconsistent state.

**Vulnerable Pattern:**
```python
async def process_trail_update(trail_id: str):
    try:
        await update_database(trail_id)
        await send_notification(trail_id)
    except asyncio.CancelledError:
        log_warning("Task cancelled")
        # CancelledError swallowed — task appears to complete normally
        # Parent TaskGroup/gather cannot detect cancellation
    except Exception as e:
        log_error("Update failed", metadata={"error": str(e)})
```

**Resilient Pattern:**
```python
async def process_trail_update(trail_id: str):
    try:
        await update_database(trail_id)
        await send_notification(trail_id)
    except asyncio.CancelledError:
        log_warning("Task cancelled, cleaning up",
                    metadata={"trail_id": trail_id})
        # Perform minimal cleanup
        await rollback_if_needed(trail_id)
        raise  # MUST re-raise to propagate cancellation
    except Exception as e:
        log_error("Update failed", metadata={"error": str(e)})
        raise
```

**Detection:** Search for `except asyncio.CancelledError` or `except CancelledError` blocks that do not end with `raise`.

**Impact:** Lambda timeout triggers task cancellation. Cancelled task swallows error, returns partial result. Database updated but notification not sent. No error logged. Inconsistent state.

---

## 56. asyncio Yield Inside TaskGroup

**Severity:** HIGH

**Description:** Using `yield` inside a `TaskGroup` (or `asyncio.timeout`) context breaks structured concurrency as defined in PEP 789. The generator can be suspended while the TaskGroup is active, leading to tasks that escape their scope.

**Vulnerable Pattern:**
```python
async def stream_trail_updates(org_id: str):
    async with asyncio.TaskGroup() as tg:
        results = []
        for trail_id in trail_ids:
            tg.create_task(fetch_update(trail_id, results))
        # yield inside TaskGroup — breaks structured concurrency
        for result in results:
            yield result  # Generator suspended, TaskGroup scope violated
```

**Resilient Pattern:**
```python
async def stream_trail_updates(org_id: str):
    # Collect all results inside TaskGroup
    results = []
    async with asyncio.TaskGroup() as tg:
        for trail_id in trail_ids:
            tg.create_task(fetch_update(trail_id, results))
    # TaskGroup complete — safe to yield
    for result in results:
        yield result
```

**Detection:** Search for `yield` statements inside `async with asyncio.TaskGroup()` or `async with asyncio.timeout()` blocks.

**Impact:** Tasks created in TaskGroup escape scope when generator is suspended. Exceptions from escaped tasks crash the event loop with unhandled error. Difficult to reproduce, manifests under load.

---

## 57. Blocking I/O in Async Handler

**Severity:** CRITICAL

**Description:** Synchronous I/O operations (file reads, synchronous HTTP calls, `time.sleep()`) in async functions block the entire event loop, preventing all other concurrent operations from progressing.

**Vulnerable Pattern:**
```python
async def generate_report(org_id: str):
    # Blocking file I/O — blocks entire event loop
    with open("/tmp/template.html", "r") as f:
        template = f.read()

    # Blocking HTTP call — blocks entire event loop
    import requests
    response = requests.get(f"https://api.example.com/data/{org_id}")

    # time.sleep blocks event loop — use asyncio.sleep instead
    import time
    time.sleep(1)

    return template.format(data=response.json())
```

**Resilient Pattern:**
```python
import aiofiles
import httpx
import asyncio

async def generate_report(org_id: str):
    # Non-blocking file I/O
    async with aiofiles.open("/tmp/template.html", "r") as f:
        template = await f.read()

    # Non-blocking HTTP call
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.example.com/data/{org_id}",
            timeout=10.0,
        )

    # Non-blocking sleep
    await asyncio.sleep(1)

    return template.format(data=response.json())
```

**Detection:** Search for `open()`, `requests.get/post`, `time.sleep()`, `urllib.request`, `subprocess.run()` inside `async def` functions.

**Impact:** Single blocking call in async handler stalls all concurrent requests. At 100 concurrent connections, one 5-second blocking call makes all 100 requests wait 5 seconds. P95 latency spikes to 5000ms.

---

## 58. Unbounded asyncio Concurrency

**Severity:** HIGH

**Description:** Creating unlimited concurrent tasks with `asyncio.gather()` or `TaskGroup` exhausts connection pools, triggers API rate limits, and causes memory spikes. Each task consumes memory and a connection.

**Vulnerable Pattern:**
```python
async def process_all_trails(org_id: str, trail_ids: list[str]):
    # 5000 concurrent tasks — exhausts connection pool
    tasks = [update_trail(trail_id) for trail_id in trail_ids]
    results = await asyncio.gather(*tasks)
    return results
```

**Resilient Pattern:**
```python
import asyncio

MAX_CONCURRENT = 50  # Match connection pool size

async def process_all_trails(org_id: str, trail_ids: list[str]):
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    results = []

    async def bounded_update(trail_id: str):
        async with semaphore:
            return await update_trail(trail_id)

    tasks = [bounded_update(tid) for tid in trail_ids]
    results = await asyncio.gather(*tasks)
    return results
```

**Detection:** Search for `asyncio.gather(*[` or `tg.create_task(` inside loops without a `Semaphore` limiting concurrency.

**Impact:** Processing 5000 trail systems creates 5000 concurrent DynamoDB calls. Connection pool (50 connections) exhausted. 4950 tasks queue, timeout, and fail. DynamoDB throttles due to burst.

---

## 59. DynamoDB Decimal Serialization

**Severity:** MEDIUM

**Description:** DynamoDB returns numbers as `decimal.Decimal` objects, which are not JSON-serializable by default. Passing DynamoDB items directly to `json.dumps()` or FastAPI's `JSONResponse` raises `TypeError`.

**Vulnerable Pattern:**
```python
from fastapi.responses import JSONResponse

async def get_trail(table, trail_id: str):
    response = await table.get_item(Key={"pk": trail_id})
    item = response.get("Item")
    return JSONResponse(content=item)
    # TypeError: Object of type Decimal is not JSON serializable
```

**Resilient Pattern:**
```python
import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    """JSON encoder that handles DynamoDB Decimal types."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            if obj % 1 == 0:
                return int(obj)
            return float(obj)
        return super().default(obj)

def convert_decimals(obj):
    """Recursively convert Decimals in DynamoDB items."""
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    if isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    return obj

async def get_trail(table, trail_id: str):
    response = await table.get_item(Key={"pk": trail_id})
    item = response.get("Item")
    return convert_decimals(item)
```

**Detection:** Search for DynamoDB query/get_item results passed directly to `JSONResponse`, `json.dumps()`, or returned from FastAPI endpoints without Decimal conversion.

**Impact:** Every endpoint that returns DynamoDB data crashes with `TypeError`. 500 errors on all read endpoints. Discovered only in integration testing or production.

---

# Category H: Secrets/Configuration Failures (Patterns 60-61)

---

## 60. Secrets Manager Rotation During Active Request

**Severity:** HIGH

**Description:** During secret rotation, there is a brief window where the old secret is invalidated but the application cache still holds the old value. Requests during this window fail with authentication errors.

**Vulnerable Pattern:**
```python
# Cache secret indefinitely — never sees rotation
_db_password = None

async def get_db_password(secrets_client):
    global _db_password
    if _db_password is None:
        response = await secrets_client.get_secret_value(SecretId="db-password")
        _db_password = response["SecretString"]
    return _db_password
    # After rotation: cached password is invalid, all DB calls fail
```

**Resilient Pattern:**
```python
from cachetools import TTLCache

# Short TTL cache — refreshes during rotation window
_secret_cache = TTLCache(maxsize=10, ttl=300)  # 5 minute TTL

async def get_db_password(secrets_client):
    cached = _secret_cache.get("db-password")
    if cached:
        return cached

    response = await secrets_client.get_secret_value(SecretId="db-password")
    secret = response["SecretString"]
    _secret_cache["db-password"] = secret
    return secret

async def get_db_connection(secrets_client):
    password = await get_db_password(secrets_client)
    try:
        return await connect_to_db(password)
    except AuthenticationError:
        # Rotation may have occurred — clear cache and retry
        _secret_cache.pop("db-password", None)
        password = await get_db_password(secrets_client)
        return await connect_to_db(password)
```

**Detection:** Search for secret caching without TTL or without retry-on-auth-failure logic. Any indefinitely cached secret is vulnerable to rotation disruption.

**Impact:** Secret rotates at 2 AM. Lambda warm instances cache old password. All database calls fail until Lambda cold-starts. 15-60 minutes of errors depending on traffic.

---

## 61. STS Credential Expiration Without Refresh

**Severity:** HIGH

**Description:** `AssumeRole` credentials expire after 1 hour (default). Module-level credential caching without refresh logic causes all AWS API calls to fail when credentials expire.

**Vulnerable Pattern:**
```python
# Module-level — cached across warm invocations
_assumed_credentials = None

async def get_cross_account_client(sts_client, role_arn: str):
    global _assumed_credentials
    if _assumed_credentials is None:
        response = await sts_client.assume_role(
            RoleArn=role_arn, RoleSessionName="traillens"
        )
        _assumed_credentials = response["Credentials"]
    # After 1 hour, these credentials expire — all calls fail
    return boto3.client("s3",
        aws_access_key_id=_assumed_credentials["AccessKeyId"],
        aws_secret_access_key=_assumed_credentials["SecretAccessKey"],
        aws_session_token=_assumed_credentials["SessionToken"],
    )
```

**Resilient Pattern:**
```python
from datetime import datetime, timedelta

_assumed_credentials = None
_credentials_expiry = None
REFRESH_BUFFER = timedelta(minutes=5)

async def get_cross_account_client(sts_client, role_arn: str):
    global _assumed_credentials, _credentials_expiry

    # Refresh if expired or within 5 minutes of expiry
    now = datetime.utcnow()
    if (_assumed_credentials is None or
            _credentials_expiry is None or
            now >= _credentials_expiry - REFRESH_BUFFER):
        response = await sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName="traillens",
            DurationSeconds=3600,
        )
        _assumed_credentials = response["Credentials"]
        _credentials_expiry = _assumed_credentials["Expiration"].replace(tzinfo=None)

    session = aioboto3.Session(
        aws_access_key_id=_assumed_credentials["AccessKeyId"],
        aws_secret_access_key=_assumed_credentials["SecretAccessKey"],
        aws_session_token=_assumed_credentials["SessionToken"],
    )
    return session
```

**Detection:** Search for `assume_role` results cached at module level without expiration checking. Any `Credentials` cache without TTL or expiry comparison is vulnerable.

**Impact:** Cross-account S3 access works for first hour. After expiry, all photo uploads/downloads fail. Error: `ExpiredTokenException`. Affects all warm Lambda instances simultaneously.

---

# Category I: Observability/Monitoring Failures (Patterns 62-65)

---

## 62. CloudWatch Metric Filter Ignoring Late Data

**Severity:** MEDIUM

**Description:** CloudWatch Alarms evaluate at fixed intervals. If EMF (Embedded Metric Format) metrics arrive late (common with Lambda cold starts or high load), they are backfilled after the evaluation period. The alarm never sees the data.

**Vulnerable Pattern:**
```python
# Alarm with default missing data treatment
alarm = aws.cloudwatch.MetricAlarm(
    "api-error-rate",
    metric_name="ErrorCount",
    namespace="TrailLens/API",
    period=60,
    evaluation_periods=3,
    threshold=10,
    comparison_operator="GreaterThanThreshold",
    # Default: treat_missing_data="missing" — alarm stays in current state
    # Late data never triggers alarm
)
```

**Resilient Pattern:**
```python
alarm = aws.cloudwatch.MetricAlarm(
    "api-error-rate",
    metric_name="ErrorCount",
    namespace="TrailLens/API",
    period=60,
    evaluation_periods=3,
    threshold=10,
    comparison_operator="GreaterThanThreshold",
    treat_missing_data="breaching",  # Missing data = assume error
    # Late data still processed, but alarm fires on missing data too
    datapoints_to_alarm=2,  # 2 of 3 periods — reduces false positives
)
```

**Detection:** Search for CloudWatch alarms without `treat_missing_data` configuration. Check EMF emission timing in Lambda functions.

**Impact:** Error spike occurs during Lambda cold start burst. Metrics arrive 2 minutes late. Alarm evaluates during gap, sees no data, stays OK. Error spike undetected for 10+ minutes.

---

## 63. EMF Metric Dimension/Count Limit

**Severity:** MEDIUM

**Description:** CloudWatch Embedded Metric Format (EMF) allows at most 100 metrics and 30 dimensions per EMF entry. Excess metrics and dimensions are silently dropped without error.

**Vulnerable Pattern:**
```python
import json

def emit_request_metrics(request_data: dict):
    metrics = {
        "_aws": {
            "Timestamp": int(time.time() * 1000),
            "CloudWatchMetrics": [{
                "Namespace": "TrailLens/API",
                "Dimensions": [
                    # 35 dimensions — exceeds 30 limit, extras silently dropped
                    ["endpoint", "method", "status", "user_type", "org_id",
                     "region", "device", "browser", "os", "version",
                     "feature", "cache_hit", "auth_type", "response_size",
                     "db_calls", "retry_count", "cold_start", "memory_used",
                     "duration_bucket", "error_type", "throttled", "timeout",
                     "batch_size", "page_size", "sort_order", "filter_count",
                     "include_deleted", "locale", "timezone", "api_version",
                     "client_id", "request_source", "compression", "encoding",
                     "protocol"]
                ],
                "Metrics": [{"Name": "Latency", "Unit": "Milliseconds"}],
            }],
        },
    }
    print(json.dumps(metrics))  # EMF output — some dimensions silently dropped
```

**Resilient Pattern:**
```python
MAX_DIMENSIONS = 9  # Well under 30 limit — leave room for AWS-added dimensions
MAX_METRICS = 50    # Well under 100 limit

def emit_request_metrics(endpoint: str, method: str, status: int, duration_ms: float):
    metrics = {
        "_aws": {
            "Timestamp": int(time.time() * 1000),
            "CloudWatchMetrics": [{
                "Namespace": "TrailLens/API",
                "Dimensions": [
                    # Focused, high-value dimensions only
                    ["endpoint", "method", "status_class"]
                ],
                "Metrics": [
                    {"Name": "Latency", "Unit": "Milliseconds"},
                    {"Name": "RequestCount", "Unit": "Count"},
                ],
            }],
        },
        "endpoint": endpoint,
        "method": method,
        "status_class": f"{status // 100}xx",
        "Latency": duration_ms,
        "RequestCount": 1,
    }
    print(json.dumps(metrics))
```

**Detection:** Count dimensions and metrics in EMF output. Any EMF entry with >30 dimensions or >100 metrics has silently dropped data.

**Impact:** Monitoring dashboard shows partial data. Key metrics silently missing. Performance degradation goes undetected because the dropped metric was the one that mattered.

---

## 64. X-Ray Subsegment Outside Handler

**Severity:** MEDIUM

**Description:** AWS X-Ray requires an active segment to create subsegments. Module-level AWS SDK calls (e.g., boto3 client initialization) run outside the Lambda handler where no X-Ray segment exists, causing `SegmentNotFoundException`.

**Vulnerable Pattern:**
```python
import boto3
from aws_xray_sdk.core import patch_all

patch_all()  # Patches boto3 to create X-Ray subsegments

# Module-level — runs before handler, no X-Ray segment active
dynamodb = boto3.resource("dynamodb")  # SegmentNotFoundException!
table = dynamodb.Table("trail-systems")
```

**Resilient Pattern:**
```python
import boto3
from aws_xray_sdk.core import patch_all, xray_recorder

patch_all()

# Module-level initialization without X-Ray tracing
xray_recorder.configure(context_missing="LOG_ERROR")  # Log instead of raise

# Or: lazy initialization inside handler
_table = None

async def get_table():
    global _table
    if _table is None:
        dynamodb = boto3.resource("dynamodb")
        _table = dynamodb.Table("trail-systems")
    return _table
```

**Detection:** Search for boto3 client/resource creation at module level with X-Ray SDK `patch_all()` active. Look for `context_missing` configuration.

**Impact:** Lambda fails on every cold start with `SegmentNotFoundException`. Falls back to error handling, adding 100-500ms to cold start. If error is fatal, Lambda never starts.

---

## 65. Distributed Trace Context Lost in Async Processing

**Severity:** MEDIUM

**Description:** When processing SQS/SNS messages asynchronously, the X-Ray trace context from the original request is lost unless explicitly extracted from message attributes. This breaks end-to-end tracing across service boundaries.

**Vulnerable Pattern:**
```python
async def handle_sqs_message(event):
    for record in event["Records"]:
        body = json.loads(record["body"])
        # Trace context from original request is lost
        # New trace created — no connection to original request
        await process_trail_update(body["trail_id"])
```

**Resilient Pattern:**
```python
from aws_xray_sdk.core import xray_recorder

async def handle_sqs_message(event):
    for record in event["Records"]:
        body = json.loads(record["body"])

        # Extract trace header from message attributes
        trace_header = record.get("attributes", {}).get("AWSTraceHeader")
        if trace_header:
            # Continue the original trace
            segment = xray_recorder.begin_segment(
                "process-trail-update",
                traceid=extract_trace_id(trace_header),
                parent_id=extract_parent_id(trace_header),
            )
        else:
            segment = xray_recorder.begin_segment("process-trail-update")

        try:
            await process_trail_update(body["trail_id"])
        finally:
            xray_recorder.end_segment()
```

**Detection:** Search for SQS/SNS message handlers without `AWSTraceHeader` extraction from message attributes.

**Impact:** Cannot trace a user request end-to-end through API Gateway, Lambda, SQS, and processing Lambda. During debugging, the trail goes cold at the queue boundary. Root cause analysis takes hours instead of minutes.

---

# Category J: FastAPI/Application Failures (Patterns 66-69)

---

## 66. Mangum Lifespan Running Per-Request

**Severity:** HIGH

**Description:** Mangum (ASGI adapter for Lambda) does not maintain lifespan across invocations. FastAPI's lifespan handlers (`startup`/`shutdown`) run on every Lambda invocation, not once per instance. Heavy initialization in lifespan adds latency to every request.

**Vulnerable Pattern:**
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from mangum import Mangum

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs on EVERY Lambda invocation with Mangum
    app.state.db_pool = await create_db_pool()  # 500ms startup
    app.state.cache = await warm_cache()          # 200ms startup
    yield
    await app.state.db_pool.close()

app = FastAPI(lifespan=lifespan)
handler = Mangum(app)
# Every request pays 700ms lifespan cost
```

**Resilient Pattern:**
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from mangum import Mangum

# Module-level initialization — runs once per cold start
_dynamo_resource = None

async def get_dynamo():
    global _dynamo_resource
    if _dynamo_resource is None:
        session = aioboto3.Session()
        _dynamo_resource = await session.resource("dynamodb").__aenter__()
    return _dynamo_resource

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lightweight lifespan — only set references
    app.state.get_dynamo = get_dynamo
    yield

app = FastAPI(lifespan=lifespan)
handler = Mangum(app)
# Module-level init: once per cold start
# Lifespan: near-zero cost per invocation
```

**Detection:** Search for heavy initialization (database pools, cache warming, HTTP client creation) inside FastAPI lifespan handlers when Mangum is used.

**Impact:** Every Lambda invocation pays 700ms lifespan cost. At P50 latency of 100ms, lifespan adds 7x overhead. Users experience 800ms response times for a 100ms operation.

---

## 67. FastAPI HTTPException in Middleware Not Handled

**Severity:** MEDIUM

**Description:** Raising `HTTPException` inside a `BaseHTTPMiddleware` does not get caught by FastAPI's default exception handler. Instead, it propagates as an unhandled exception, returning a 500 Internal Server Error.

**Vulnerable Pattern:**
```python
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        token = request.headers.get("Authorization")
        if not token:
            # This HTTPException is NOT caught by FastAPI's handler!
            raise HTTPException(status_code=401, detail="Missing token")
        response = await call_next(request)
        return response
    # Client receives 500 Internal Server Error instead of 401
```

**Resilient Pattern:**
```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        token = request.headers.get("Authorization")
        if not token:
            # Return Response directly — not HTTPException
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing authentication token"},
            )
        response = await call_next(request)
        return response
```

**Detection:** Search for `raise HTTPException` inside classes that extend `BaseHTTPMiddleware`.

**Impact:** Authentication middleware intended to return 401 returns 500 instead. Client sees "Internal Server Error" for missing token. Confusing error messages. Security scanners flag 500s as vulnerabilities.

---

## 68. Pydantic V2 Nested Subclass Serialization

**Severity:** MEDIUM

**Description:** In Pydantic V2, when a parent class is used as a type annotation for a field, instances of child classes lose their subclass-specific fields during serialization. This is a breaking change from Pydantic V1.

**Vulnerable Pattern:**
```python
from pydantic import BaseModel

class Notification(BaseModel):
    message: str

class EmailNotification(Notification):
    email_to: str
    subject: str

class TrailAlert(BaseModel):
    trail_id: str
    notification: Notification  # Type annotation is parent class

# Subclass-specific fields dropped during serialization
alert = TrailAlert(
    trail_id="trail-123",
    notification=EmailNotification(
        message="Trail closed",
        email_to="user@example.com",
        subject="Alert",
    ),
)
print(alert.model_dump())
# {"trail_id": "trail-123", "notification": {"message": "Trail closed"}}
# email_to and subject are LOST
```

**Resilient Pattern:**
```python
from pydantic import BaseModel
from typing import Annotated, Literal, Union

class EmailNotification(BaseModel):
    type: Literal["email"] = "email"
    message: str
    email_to: str
    subject: str

class PushNotification(BaseModel):
    type: Literal["push"] = "push"
    message: str
    device_token: str

# Discriminated union preserves all fields
NotificationType = Annotated[
    Union[EmailNotification, PushNotification],
    Field(discriminator="type"),
]

class TrailAlert(BaseModel):
    trail_id: str
    notification: NotificationType

alert = TrailAlert(
    trail_id="trail-123",
    notification=EmailNotification(
        message="Trail closed",
        email_to="user@example.com",
        subject="Alert",
    ),
)
print(alert.model_dump())
# {"trail_id": "trail-123", "notification": {"type": "email", "message": "Trail closed", "email_to": "user@example.com", "subject": "Alert"}}
```

**Detection:** Search for Pydantic model fields annotated with a parent class type where subclasses are used at runtime. Check for `model_dump()` calls on models with inheritance.

**Impact:** API responses silently drop notification-specific fields. Frontend cannot render email vs push notification details. Data loss in API responses goes undetected until users report missing information.

---

## 69. FastAPI Dependency Circular Import

**Severity:** MEDIUM

**Description:** Circular imports between route modules and dependency modules do not cause errors at import time in Python. They surface at request time as `AttributeError` or `ImportError`, making them difficult to catch in testing.

**Vulnerable Pattern:**
```python
# routes/trails.py
from api.dependencies.auth import get_current_user  # Imports auth module
from api.services.trail_service import TrailService

@router.get("/trails")
async def list_trails(user=Depends(get_current_user)):
    ...

# dependencies/auth.py
from api.routes.trails import router  # Circular — imports routes module
# At request time: AttributeError or partially initialized module
```

**Resilient Pattern:**
```python
# dependencies/auth.py — NO imports from routes
from api.services.user_service import UserService

async def get_current_user(token: str = Depends(oauth2_scheme)):
    return await UserService.verify_token(token)

# routes/trails.py — imports from dependencies (one-directional)
from api.dependencies.auth import get_current_user

@router.get("/trails")
async def list_trails(user=Depends(get_current_user)):
    ...

# Dependency direction: routes → dependencies → services → repositories
# Never: dependencies → routes or services → routes
```

**Detection:** Map import graph between route and dependency modules. Any cycle indicates a circular import risk. Use `importlib` analysis or `pylint` circular import detection.

**Impact:** Application starts successfully. First request to affected route fails with `AttributeError: partially initialized module`. Intermittent — depends on import order. Difficult to reproduce in unit tests.

---

# Category K: Infrastructure/Deployment Failures (Patterns 70-72)

---

## 70. Configuration Drift Between Infra and Application

**Severity:** HIGH

**Description:** Infrastructure (Pulumi) and application code reference the same resources (DynamoDB table names, Cognito pool IDs, S3 bucket names) but can drift when one is updated without the other. Hardcoded resource names bypass the StackReference mechanism.

**Vulnerable Pattern:**
```python
# Application code — hardcoded table name
TABLE_NAME = "traillens-prod-trail-systems"  # Hardcoded!

async def get_trail(trail_id: str):
    async with session.resource("dynamodb") as dynamo:
        table = await dynamo.Table(TABLE_NAME)
        # If infra renames table, this breaks silently
```

**Resilient Pattern:**
```python
import os

# Application code — table name from environment variable
TABLE_NAME = os.environ["TRAIL_SYSTEMS_TABLE_NAME"]

# Pulumi infra — exports table name
pulumi.export("trail_systems_table_name", table.name)

# Pulumi app deployment — imports from infra
infra_ref = pulumi.StackReference("TrailLensCo/infra/prod")
table_name = infra_ref.get_output("trail_systems_table_name")

lambda_function = aws.lambda_.Function(
    "api-handler",
    environment={
        "variables": {
            "TRAIL_SYSTEMS_TABLE_NAME": table_name,
        }
    },
)
```

**Detection:** Search for hardcoded AWS resource names (table names, bucket names, pool IDs, topic ARNs) in application code. All resource names should come from environment variables.

**Impact:** Infrastructure team renames DynamoDB table for consistency. Application still references old name. All database operations fail. Requires synchronized deployment.

---

## 71. Lambda Layer Version Not Updated

**Severity:** MEDIUM

**Description:** Publishing a new Lambda Layer version does not automatically update functions that reference the old version. Functions continue using the pinned ARN until explicitly updated.

**Vulnerable Pattern:**
```python
# Function references specific layer version
lambda_function = aws.lambda_.Function(
    "api-handler",
    layers=[
        "arn:aws:lambda:us-east-1:123456:layer:shared-deps:3",
        # layer:4 published with security fix — this function still uses :3
    ],
)
```

**Resilient Pattern:**
```python
# Layer managed in same Pulumi stack — auto-updates
shared_layer = aws.lambda_.LayerVersion(
    "shared-deps",
    compatible_runtimes=["python3.14"],
    code=pulumi.FileArchive("./layers/shared-deps.zip"),
)

lambda_function = aws.lambda_.Function(
    "api-handler",
    layers=[shared_layer.arn],  # Always uses latest version
)

# CI/CD: after publishing new layer, update all functions
# pulumi up automatically handles this when layer is in same stack
```

**Detection:** Search for hardcoded layer version ARNs (`:3`, `:5`, etc.) in Lambda function configurations. Compare against latest published layer version.

**Impact:** Security patch published in layer version 4. Production functions still run version 3 with vulnerability. Patch appears deployed but is not active.

---

## 72. API Gateway Stage Deployment Not Propagated

**Severity:** HIGH

**Description:** Modifying API Gateway resources (routes, methods, integrations) does not automatically update the deployed stage. Changes require an explicit deployment to take effect. Without a new deployment, the stage serves the old configuration.

**Vulnerable Pattern:**
```python
# Add new route to API Gateway
new_resource = aws.apigateway.Resource(
    "trail-reports",
    rest_api=api.id,
    parent_id=api.root_resource_id,
    path_part="reports",
)

new_method = aws.apigateway.Method(
    "trail-reports-get",
    rest_api=api.id,
    resource_id=new_resource.id,
    http_method="GET",
    authorization="COGNITO_USER_POOLS",
)

# No deployment created — stage still serves old configuration
# New route returns 404 in production
```

**Resilient Pattern:**
```python
# Pulumi handles this automatically with proper dependencies
deployment = aws.apigateway.Deployment(
    "api-deployment",
    rest_api=api.id,
    # Trigger redeployment when routes change
    triggers={
        "redeployment": pulumi.Output.all(
            new_resource.id,
            new_method.id,
        ).apply(lambda ids: hashlib.sha1(",".join(ids).encode()).hexdigest()),
    },
)

stage = aws.apigateway.Stage(
    "prod",
    rest_api=api.id,
    deployment=deployment.id,
    stage_name="prod",
)
```

**Detection:** Check Pulumi/CloudFormation for API Gateway deployments that depend on all route changes. Compare current deployment timestamp against last route modification.

**Impact:** New endpoint added and tested in development. Deployed to production. Returns 404 because stage not redeployed. Feature appears broken. Hours of debugging before realizing deployment is stale.

---

# Category L: DNS/Network Failures (Patterns 73-74)

---

## 73. DNS Resolution Failure Cascade

**Severity:** CRITICAL

**Description:** AWS services rely on DNS for endpoint resolution. A DNS failure (as seen in the October 2025 us-east-1 outage) cascades to all AWS services simultaneously. Without DNS caching or fallback, the entire application becomes unavailable.

**Vulnerable Pattern:**
```python
# No DNS caching — every API call resolves DNS
# Single region — no failover
session = aioboto3.Session(region_name="us-east-1")

async def handler(event, context):
    async with session.resource("dynamodb") as dynamo:
        # DNS failure → cannot resolve dynamodb.us-east-1.amazonaws.com
        # All operations fail simultaneously
        table = await dynamo.Table("trail-systems")
        return await table.get_item(Key={"pk": event["trail_id"]})
```

**Resilient Pattern:**
```python
from botocore.config import Config

# Enable endpoint caching and connection keepalive
config = Config(
    retries={"max_attempts": 3, "mode": "adaptive"},
    connect_timeout=2,
    read_timeout=10,
    # Keep connections alive — reduces DNS lookups
    tcp_keepalive=True,
)

# For critical paths: cache DNS at application level
import socket
_dns_cache = {}

def cached_getaddrinfo(host, port, *args, **kwargs):
    key = (host, port)
    if key not in _dns_cache:
        _dns_cache[key] = _original_getaddrinfo(host, port, *args, **kwargs)
    return _dns_cache[key]

_original_getaddrinfo = socket.getaddrinfo
# Note: DNS caching in Lambda should use short TTL to handle endpoint changes
```

**Detection:** Architecture review for single-region deployment without DNS resilience. Check for TCP keepalive and connection reuse configuration.

**Impact:** Regional DNS outage (as occurred October 2025) makes all AWS services unreachable. DynamoDB, S3, SES, SNS, Cognito all fail simultaneously. Complete application outage until DNS recovers.

---

## 74. Lambda VPC Subnet IP Address Exhaustion

**Severity:** HIGH

**Description:** Each concurrent Lambda execution in a VPC requires an Elastic Network Interface (ENI) with a private IP address. If the VPC subnet does not have enough available IPs for peak concurrency, new Lambda instances cannot start.

**Vulnerable Pattern:**
```python
# Small subnet — only 251 usable IPs
vpc_subnet = aws.ec2.Subnet(
    "lambda-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",  # 251 usable IPs
    availability_zone="us-east-1a",
)

# Lambda with 500+ expected concurrent executions
lambda_function = aws.lambda_.Function(
    "api-handler",
    vpc_config={
        "subnet_ids": [vpc_subnet.id],
        "security_group_ids": [sg.id],
    },
    reserved_concurrent_executions=500,  # Needs 500 IPs!
)
```

**Resilient Pattern:**
```python
# Large subnets across multiple AZs
subnets = []
for i, az in enumerate(["us-east-1a", "us-east-1b", "us-east-1c"]):
    subnet = aws.ec2.Subnet(
        f"lambda-subnet-{az}",
        vpc_id=vpc.id,
        cidr_block=f"10.0.{i * 32}.0/19",  # 8190 usable IPs each
        availability_zone=az,
    )
    subnets.append(subnet)

# Total: 24,570 IPs across 3 AZs — handles 1000+ concurrency
lambda_function = aws.lambda_.Function(
    "api-handler",
    vpc_config={
        "subnet_ids": [s.id for s in subnets],
        "security_group_ids": [sg.id],
    },
)
```

**Detection:** Calculate: subnet IPs available = (2^(32 - prefix)) - 5 (AWS reserved). Compare against Lambda reserved concurrency + unreserved burst. Alert if IPs < 2x expected concurrency.

**Impact:** Traffic spike requires 500 concurrent Lambdas. Subnet has 251 IPs. 249 Lambdas succeed, 251 fail to start. Users experience intermittent timeouts. Errors increase as concurrency increases.

---

# Category M: API Gateway Failures (Patterns 75-76)

---

## 75. API Gateway Request Validation Bypass

**Severity:** MEDIUM

**Description:** Without explicit request validators on API Gateway methods, all requests (including malformed ones) reach Lambda. This wastes Lambda invocations on invalid requests and increases attack surface.

**Vulnerable Pattern:**
```python
# API Gateway method without request validation
method = aws.apigateway.Method(
    "create-trail",
    rest_api=api.id,
    resource_id=trail_resource.id,
    http_method="POST",
    authorization="COGNITO_USER_POOLS",
    # No request_validator_id — all requests reach Lambda
    # No request_models — no schema validation
)
```

**Resilient Pattern:**
```python
# Create request validator
validator = aws.apigateway.RequestValidator(
    "body-validator",
    rest_api=api.id,
    validate_request_body=True,
    validate_request_parameters=True,
)

# Define request model
model = aws.apigateway.Model(
    "create-trail-model",
    rest_api=api.id,
    content_type="application/json",
    schema=json.dumps({
        "type": "object",
        "required": ["name", "org_id"],
        "properties": {
            "name": {"type": "string", "minLength": 1, "maxLength": 200},
            "org_id": {"type": "string", "pattern": "^[a-zA-Z0-9-]+$"},
        },
    }),
)

method = aws.apigateway.Method(
    "create-trail",
    rest_api=api.id,
    resource_id=trail_resource.id,
    http_method="POST",
    authorization="COGNITO_USER_POOLS",
    request_validator_id=validator.id,
    request_models={"application/json": model.name},
)
```

**Detection:** Search for API Gateway methods without `request_validator_id` configured. List all POST/PUT/PATCH methods and verify schema validation exists.

**Impact:** Malformed requests invoke Lambda (billed), increase cold starts, and expose application to injection attacks that API Gateway could have blocked. 30% of Lambda cost may be wasted on invalid requests.

---

## 76. API Gateway Throttling Layer Confusion

**Severity:** MEDIUM

**Description:** API Gateway has 4 throttling layers: account-level, stage-level, method-level, and usage plan. These interact in non-obvious ways. A method-level override can be more restrictive than intended, and usage plan limits apply in addition to (not instead of) stage limits.

**Vulnerable Pattern:**
```python
# Stage-level: 1000 RPS
stage = aws.apigateway.Stage(
    "prod",
    method_settings=[{
        "method_path": "*/*",
        "throttling_rate_limit": 1000,
        "throttling_burst_limit": 500,
    }],
)

# Method-level override: accidentally set to 10 RPS
method_settings = aws.apigateway.MethodSettings(
    "trail-list-settings",
    rest_api=api.id,
    stage_name="prod",
    method_path="trails/GET",
    settings={
        "throttling_rate_limit": 10,     # Overrides to 10 RPS!
        "throttling_burst_limit": 5,
    },
)

# Usage plan: adds ADDITIONAL limit on top
usage_plan = aws.apigateway.UsagePlan(
    "standard-plan",
    throttle_settings={
        "rate_limit": 100,  # Client limited to 100 RPS regardless of method
        "burst_limit": 50,
    },
)
```

**Resilient Pattern:**
```python
# Document all throttling layers explicitly
# Account limit: 10,000 RPS (AWS default)
# Stage limit: 1,000 RPS (our config)
# Method overrides: only where specifically needed

stage = aws.apigateway.Stage(
    "prod",
    method_settings=[{
        "method_path": "*/*",
        "throttling_rate_limit": 1000,
        "throttling_burst_limit": 500,
    }],
)

# Only override specific methods that need different limits
# Auth endpoints: lower limit for brute force protection
method_settings_auth = aws.apigateway.MethodSettings(
    "auth-settings",
    rest_api=api.id,
    stage_name="prod",
    method_path="auth~1login/POST",
    settings={
        "throttling_rate_limit": 50,    # Intentionally low for auth
        "throttling_burst_limit": 25,
    },
)

# Document: effective limit = min(account, stage, method, usage_plan)
```

**Detection:** List all throttling configurations across all layers. Calculate effective limit for each method as `min(account, stage, method, usage_plan)`. Verify effective limits match intended limits.

**Impact:** Trail listing endpoint limited to 10 RPS instead of intended 1000 RPS. Dashboard loading fails for organizations with many concurrent users. Support tickets about "slow dashboard" are actually throttling.

---

# Category N: Feature Flag Failures (Patterns 77-78)

---

## 77. Feature Flag Cold Start Performance Penalty

**Severity:** MEDIUM

**Description:** Feature flag SDKs that fetch flag state from a remote service add 100-500ms to every Lambda cold start. This is especially impactful when flags are evaluated in the hot path of every request.

**Vulnerable Pattern:**
```python
from feature_flags_sdk import FeatureFlagClient

# Remote fetch on every cold start — 100-500ms added
client = FeatureFlagClient(
    api_key=os.environ["FLAG_API_KEY"],
    # Default: fetches all flags from remote service on init
)

async def handler(event, context):
    if client.is_enabled("new_trail_ui"):
        return await new_handler(event)
    return await old_handler(event)
```

**Resilient Pattern:**
```python
from feature_flags_sdk import FeatureFlagClient

# Local evaluation with cached flags + background refresh
client = FeatureFlagClient(
    api_key=os.environ["FLAG_API_KEY"],
    bootstrap_flags={
        "new_trail_ui": False,  # Safe defaults for cold start
        "batch_notifications": True,
    },
    cache_ttl=300,  # 5 minute cache
    async_refresh=True,  # Background refresh, non-blocking
)

async def handler(event, context):
    # Evaluates locally from cache — <1ms
    if client.is_enabled("new_trail_ui"):
        return await new_handler(event)
    return await old_handler(event)
```

**Detection:** Search for feature flag SDK initialization without `bootstrap_flags` or local cache configuration. Check cold start latency metrics for SDK initialization overhead.

**Impact:** 300ms added to every cold start. With 20% cold start rate and 1000 RPS, 200 requests/second pay 300ms penalty. P95 latency increases from 200ms to 500ms during cold start bursts.

---

## 78. Feature Flag Stale Cache After Provider Outage

**Severity:** MEDIUM

**Description:** During an extended feature flag provider outage, all Lambda functions run on stale cached flag state. If the cache has no default values configured, flags evaluate to `None` or throw errors.

**Vulnerable Pattern:**
```python
async def check_feature(flag_name: str) -> bool:
    try:
        return await flag_client.is_enabled(flag_name)
    except Exception:
        # Provider down — no default, returns None
        return None  # None is falsy but not False — subtle bugs

# Caller treats None as False, but comparison breaks:
# if check_feature("x") == False:  → never matches None
```

**Resilient Pattern:**
```python
# Define sensible defaults for ALL flags
FLAG_DEFAULTS = {
    "new_trail_ui": False,        # Safe: old UI works
    "batch_notifications": True,   # Safe: notifications continue
    "maintenance_mode": False,     # Safe: service stays available
}

async def check_feature(flag_name: str) -> bool:
    default = FLAG_DEFAULTS.get(flag_name, False)
    try:
        result = await flag_client.is_enabled(flag_name)
        if result is None:
            return default
        return result
    except Exception as e:
        log_warning("Feature flag provider unavailable, using default",
                    metadata={"flag": flag_name, "default": default, "error": str(e)})
        return default
```

**Detection:** Search for feature flag evaluation without explicit default values. Check for `None` return values from flag checks.

**Impact:** Flag provider outage lasts 2 hours. All flags return `None`. Features gated behind flags behave unpredictably. Some features silently disabled, others silently enabled (including incomplete features).

---

# Category O: Data Integrity Failures (Patterns 79-80)

---

## 79. DynamoDB Schema Migration Without Dual-Write

**Severity:** HIGH

**Description:** Changing DynamoDB item structure (adding required attributes, changing attribute format) without backward compatibility breaks in-flight requests. Lambda instances running old code cannot read items written by new code, and vice versa.

**Vulnerable Pattern:**
```python
# V1: location stored as string
# {"pk": "TRAIL#123", "location": "Moab, UT"}

# V2 deployment: location changed to object (breaking change)
# {"pk": "TRAIL#123", "location": {"city": "Moab", "state": "UT", "lat": 38.57, "lng": -109.55}}

async def get_trail_location(table, trail_id: str):
    response = await table.get_item(Key={"pk": f"TRAIL#{trail_id}"})
    item = response["Item"]
    # Old items have string location — this crashes
    return f"{item['location']['city']}, {item['location']['state']}"
```

**Resilient Pattern:**
```python
# Phase 1: Dual-write (old + new format) — deploy to all instances
async def update_trail_location(table, trail_id: str, location: dict):
    await table.update_item(
        Key={"pk": f"TRAIL#{trail_id}"},
        UpdateExpression="SET #loc = :loc, location_v2 = :loc_v2",
        ExpressionAttributeNames={"#loc": "location"},
        ExpressionAttributeValues={
            ":loc": f"{location['city']}, {location['state']}",  # Old format
            ":loc_v2": location,  # New format
        },
    )

# Phase 1: Read from new format, fall back to old
async def get_trail_location(table, trail_id: str) -> dict:
    response = await table.get_item(Key={"pk": f"TRAIL#{trail_id}"})
    item = response["Item"]

    # Try new format first
    if "location_v2" in item:
        return item["location_v2"]

    # Fall back to old string format
    if isinstance(item.get("location"), str):
        parts = item["location"].split(", ")
        return {"city": parts[0], "state": parts[1] if len(parts) > 1 else ""}

    return item.get("location", {})

# Phase 2 (after all items migrated): remove old format reads
# Phase 3 (after verification): remove old format writes
```

**Detection:** Search for DynamoDB item attribute structure changes without backward-compatible reading logic. Check for migration scripts that update all items before code handles both formats.

**Impact:** V2 Lambda deployed while V1 instances still warm. V1 reads V2 items and crashes. V2 reads V1 items and crashes. Rolling deployment causes 50% error rate until all instances updated.

---

## 80. SQS Partial Batch Failure Without ReportBatchItemFailures

**Severity:** HIGH

**Description:** When processing SQS messages in batches, a single failed message causes the entire batch to be retried. Successfully processed messages are reprocessed, potentially causing duplicate operations. Without `ReportBatchItemFailures`, there is no way to report individual item failures.

**Vulnerable Pattern:**
```python
# Lambda event source mapping without ReportBatchItemFailures
event_source = aws.lambda_.EventSourceMapping(
    "sqs-trigger",
    event_source_arn=queue.arn,
    function_name=processor.name,
    batch_size=10,
    # No function_response_types — entire batch retried on any failure
)

async def handler(event, context):
    for record in event["Records"]:
        message = json.loads(record["body"])
        await process_message(message)  # If 1 of 10 fails, all 10 retry
```

**Resilient Pattern:**
```python
# Enable partial batch failure reporting
event_source = aws.lambda_.EventSourceMapping(
    "sqs-trigger",
    event_source_arn=queue.arn,
    function_name=processor.name,
    batch_size=10,
    function_response_types=["ReportBatchItemFailures"],
)

async def handler(event, context):
    failed_items = []

    for record in event["Records"]:
        try:
            message = json.loads(record["body"])
            await process_message(message)
        except Exception as e:
            log_error("Message processing failed",
                      metadata={
                          "message_id": record["messageId"],
                          "error": str(e),
                      })
            failed_items.append({"itemIdentifier": record["messageId"]})

    # Return only failed items for retry — successful items not reprocessed
    return {"batchItemFailures": failed_items}
```

**Detection:** Search for SQS event source mappings without `function_response_types=["ReportBatchItemFailures"]`. Check handler return value for `batchItemFailures` format.

**Impact:** Batch of 10 messages. 1 malformed message fails. All 10 retried. 9 successful messages reprocessed, creating duplicates. Malformed message retries 3 times, causing 27 duplicate operations total.

---

## Sources

### Existing Sources
- [Retry Failed Python Requests 2025 - Decodo](https://decodo.com/blog/python-requests-retry)
- [Microservices Resilience Patterns - GeeksforGeeks](https://www.geeksforgeeks.org/system-design/microservices-resilience-patterns/)
- [Circuit Breaker Pattern - talent500](https://talent500.com/blog/circuit-breaker-pattern-microservices-design-best-practices/)
- [API Gateway Resilience - Zuplo](https://zuplo.com/learning-center/api-gateway-resilience-fault-tolerance)
- [Lambda Timeout Best Practices - Lumigo/Dash0](https://lumigo.io/aws-lambda-performance-optimization/aws-lambda-timeout-best-practices/)
- [DynamoDB Intermittent Timeout Errors - AWS re:Post](https://repost.aws/knowledge-center/dynamodb-intermittent-timeout-errors)
- [FastAPI Error Handling Patterns - Better Stack](https://betterstack.com/community/guides/scaling-python/error-handling-fastapi/)
- [Boto3 Retries Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/retries.html)
- [Cognito Key Rotation - AWS re:Post](https://repost.aws/questions/QUa8TZhP3_TGGd9akoxH3B7w/cognito-key-rotation)
- [SNS Message Delivery Retries - AWS Docs](https://docs.aws.amazon.com/sns/latest/dg/sns-message-delivery-retries.html)
- [Idempotency - Powertools for AWS Lambda](https://docs.aws.amazon.com/powertools/python/latest/utilities/idempotency/)
- [Error Handling in Distributed Systems - Temporal](https://temporal.io/blog/error-handling-in-distributed-systems)
- [Resilient Python with Tenacity - AmitavRoy](https://www.amitavroy.com/articles/building-resilient-python-applications-with-tenacity-smart-retries-for-a-fail-proof-architecture)
- [Connection Pooling Best Practices DynamoDB - Reintech](https://reintech.io/blog/connection-pooling-sdk-best-practices-dynamodb)
- [Lambda Error Troubleshooting - Site24x7](https://www.site24x7.com/learn/aws-lambda-error-troubleshooting-guide.html)

### New Sources
- [AWS Lambda Troubleshooting](https://docs.aws.amazon.com/lambda/latest/dg/troubleshooting-configuration.html)
- [Lambda Timeout Best Practices](https://lumigo.io/aws-lambda-performance-optimization/aws-lambda-timeout-best-practices/)
- [Lambda Quotas](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html)
- [API Gateway Timeout](https://aws.amazon.com/about-aws/whats-new/2024/06/amazon-api-gateway-integration-timeout-limit-29-seconds/)
- [DynamoDB Error Handling](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Programming.Errors.html)
- [DynamoDB GSI Throttling](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/gsi-throttling.html)
- [DynamoDB Transactions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis.html)
- [DynamoDB TTL](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)
- [DynamoDB BatchWriteItem](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_BatchWriteItem.html)
- [SES Bounce Handling](https://aws.amazon.com/blogs/messaging-and-targeting/handling-bounces-and-complaints/)
- [SES Sending Quotas](https://docs.aws.amazon.com/ses/latest/dg/manage-sending-quotas.html)
- [SNS FIFO Topics](https://docs.aws.amazon.com/sns/latest/dg/sns-fifo-topics.html)
- [Cognito Token Revocation](https://docs.aws.amazon.com/cognito/latest/developerguide/token-revocation.html)
- [Cognito Quotas](https://docs.aws.amazon.com/cognito/latest/developerguide/quotas.html)
- [S3 Multipart Lifecycle](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpu-abort-incomplete-mpu-lifecycle-config.html)
- [Lambda Recursive Loop Detection](https://docs.aws.amazon.com/lambda/latest/dg/invocation-recursion.html)
- [Lambda Reserved Concurrency](https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html)
- [Lambda Execution Environment](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html)
- [PEP 789](https://peps.python.org/pep-0789/)
- [Mangum Lifespan](https://mangum.fastapiexpert.com/lifespan/)
- [CloudWatch EMF Spec](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format_Specification.html)
- [Secrets Manager Rotation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/troubleshoot_rotation.html)
- [Lambda SQS Partial Batch](https://docs.aws.amazon.com/prescriptive-guidance/latest/lambda-event-filtering-partial-batch-responses-for-sqs/best-practices-partial-batch-responses.html)
- [AWS Oct 2025 DNS Outage](https://medium.com/@ismailkovvuru/aws-us-east-1-dns-dynamodb-outage-oct-20-2025-root-cause-lessons-and-the-future-of-cloud-47bd1848a0c8)
