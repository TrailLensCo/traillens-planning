# Copyright (c) 2026 TrailLensCo

# Async Python Vulnerability Patterns Reference

## Purpose

This document catalogs 77 async Python vulnerability patterns commonly found in production
asyncio codebases. It serves as a reference for the `python-security-scan` skill and for
code reviewers evaluating async Python code in the TrailLens platform.

Each pattern includes a detection regex suitable for automated scanning, severity rating,
code examples showing both the vulnerable and corrected forms, and an assessment of production
impact if the issue goes unaddressed.

Patterns are organized into 13 subcategories covering event loop blocking, coroutine lifecycle,
concurrency control, resource management, race conditions, timeouts, error handling, AWS Lambda,
FastAPI/Starlette, aioboto3/AWS SDK, TaskGroup/ExceptionGroup, context variables, and
signal/thread safety.

Research was drawn from 40+ external sources including the Python 3.14 asyncio documentation,
AWS Lambda async guides, FastAPI documentation, CWE databases, and community articles on
asyncio pitfalls. Full source list is at the bottom of this document.

---

## Summary Table

| # | Category | Issue Name | Detection Pattern (grep regex) | Severity | Description |
|---|----------|-----------|-------------------------------|----------|-------------|
| 1 | A. Event Loop Blocking | Blocking calls in async functions | `async\s+def.*\n.*time\.sleep\|requests\.\(get\|post\|put\|delete\|patch\)\|open\(` | CRITICAL | Sync I/O inside async functions blocks the event loop |
| 2 | B. Coroutine Lifecycle | Missing await on coroutines | `(?<!await\s)\b\w+\.\w+\(\)` (manual review required) | CRITICAL | Coroutine created but never awaited, silently does nothing |
| 3 | B. Coroutine Lifecycle | Fire-and-forget tasks | `asyncio\.create_task\(` without assignment | HIGH | Task reference not stored, may be garbage collected |
| 4 | C. Concurrency Control | Unbounded concurrency | `asyncio\.gather\(\*\[` | HIGH | Dynamic task list with no semaphore limit |
| 5 | F. Timeouts & Flow Control | Missing timeouts on external calls | `await\s+\w+\.\(get\|post\|put\|delete\|request\)\(` without `timeout=` | HIGH | External calls can hang indefinitely |
| 6 | E. Race Conditions & Data Integrity | TOCTOU race conditions | `if.*is None.*\n.*await` | CRITICAL | Check-then-act with await between check and act |
| 7 | D. Resource Management | Resource leaks | `await\s+session\.\(client\|resource\)\(` without `async with` | HIGH | Client/resource not properly closed |
| 8 | A. Event Loop Blocking | Event loop blocking from CPU-bound work | `async\s+def.*\n.*json\.loads\|hashlib\.\|bcrypt\.\|re\.compile` | MEDIUM | CPU-intensive work in async handler starves event loop |
| 9 | D. Resource Management | aioboto3 context manager misuse | `await\s+session\.\(client\|resource\)\(` without `async with` | HIGH | aioboto3 resources not used as async context managers |
| 10 | G. Error Handling | Swallowed CancelledError | `except\s+Exception\b` inside async function | CRITICAL | Catches CancelledError, prevents task cancellation |
| 11 | I. FastAPI & Starlette | Sync/async function mismatch | `^def\s+\w+.*\n.*await\b` or sync handler calling async | HIGH | Non-async function in async framework context |
| 12 | C. Concurrency Control | Missing optimistic locking | `\.update_item\(` without `ConditionExpression` | HIGH | Concurrent updates cause lost writes |
| 13 | C. Concurrency Control | Shared mutable state without lock | Module-level `\w+\s*[:=]\s*\{\}\|\[\]` modified in `async def` | HIGH | Race conditions on shared dicts/lists |
| 14 | D. Resource Management | Async generator not closed | `async\s+for.*\n.*break` without `aclose()` | MEDIUM | Resources held by generator are never released |
| 15 | A. Event Loop Blocking | DNS resolution blocking | `getaddrinfo\|socket\.gethostbyname` in async context | LOW | Default resolver uses threads, can block |
| 16 | C. Concurrency Control | Deadlock from nested locks | Multiple `async\s+with\s+\w+_lock` in nested scope | CRITICAL | Inconsistent lock ordering causes deadlocks |
| 17 | C. Concurrency Control | Semaphore leak on exception | `\.acquire\(\)` without `async with` or try/finally | HIGH | Semaphore never released after exception |
| 18 | H. AWS Lambda Specific | Lambda event loop reuse | `asyncio\.run\(` in Lambda handler | CRITICAL | Closes event loop, breaks warm invocation reuse and module-level client caching |
| 19 | B. Coroutine Lifecycle | Exception swallowed in gather | `gather\(.*return_exceptions\s*=\s*True` | MEDIUM | Exceptions mixed into results list go unchecked |
| 20 | B. Coroutine Lifecycle | Missing cleanup in task cancellation | `except.*CancelledError` without `finally` block | HIGH | Resources not cleaned up when task is cancelled |
| 21 | K. TaskGroup & ExceptionGroup | TaskGroup used without async with context manager | `TaskGroup\(\)` not inside `async with` | CRITICAL | TaskGroup cleanup and exception handling never runs |
| 22 | K. TaskGroup & ExceptionGroup | Accessing TaskGroup create_task result before block exits | `\.result\(\)` inside TaskGroup block | HIGH | Task results only safe after async with block exits |
| 23 | G. Error Handling | Catching ExceptionGroup with plain except instead of except* | `except\s+ExceptionGroup` | HIGH | Loses ability to handle individual sub-exceptions |
| 24 | G. Error Handling | Raising empty ExceptionGroup | `ExceptionGroup\([^,]+,\s*\[\s*\]\)` | MEDIUM | Creating ExceptionGroup with empty list raises ValueError |
| 25 | G. Error Handling | Nested ExceptionGroup context loss | N/A (design review) | MEDIUM | except* matches sub-exceptions at any depth, losing parent context |
| 26 | G. Error Handling | TaskGroup missing CancelledError cleanup | `tg\.create_task` where target lacks `finally:` block | HIGH | Cancelled tasks in TaskGroup must handle cleanup in try/finally |
| 27 | F. Timeouts & Flow Control | Unbounded asyncio.Queue memory exhaustion | `asyncio\.Queue\(\s*\)` | CRITICAL | Queue without maxsize grows without limit until OOM |
| 28 | F. Timeouts & Flow Control | Queue consumer exception causing silent deadlock | `await.*queue\.get\(\)` without try/except | CRITICAL | Dead consumer causes other coroutines to wait forever |
| 29 | B. Coroutine Lifecycle | Queue.put()/get() called without await | `queue\.\(put\|get\)\(` not preceded by `await` | CRITICAL | Coroutine never executes, silent data loss |
| 30 | L. Context Variables | Context variables lost in run_in_executor | `run_in_executor\(` | HIGH | contextvars not propagated to ThreadPoolExecutor |
| 31 | L. Context Variables | Context variable changes in threads not propagated back | N/A (design pattern) | HIGH | Changes to ContextVar in asyncio.to_thread() not propagated back |
| 32 | L. Context Variables | Starlette middleware contextvars inconsistency | `ContextVar` usage in middleware classes | HIGH | ContextVar changes in middleware not reflected across task boundaries |
| 33 | I. FastAPI & Starlette | BackgroundTasks blocking the entire application | `background_tasks\.add_task\(` | CRITICAL | Sync functions in BackgroundTasks run in main thread pool |
| 34 | I. FastAPI & Starlette | BackgroundTasks cannot be used with BaseHTTPMiddleware | `BaseHTTPMiddleware` combined with `BackgroundTasks` | HIGH | BaseHTTPMiddleware runs BackgroundTasks in foreground |
| 35 | I. FastAPI & Starlette | FastAPI dependency injection session leak under concurrency | `async def.*yield.*session` | CRITICAL | Async generator dependencies can leak sessions on exception |
| 36 | I. FastAPI & Starlette | Sync dependencies blocking thread pool | `def\s+\w+\(.*\).*:\s*\n.*yield` (sync generator deps) | CRITICAL | Sync dependency generators with blocking DB calls exhaust thread pool |
| 37 | I. FastAPI & Starlette | Mixing lifespan with on_event decorators | `lifespan` + `on_event` in same app | HIGH | on_event handlers silently ignored when lifespan param provided |
| 38 | I. FastAPI & Starlette | StreamingResponse generator continues after client disconnect | `StreamingResponse` without disconnect checking | HIGH | Async generator keeps running after client disconnects |
| 39 | I. FastAPI & Starlette | Lifespan partial startup failure without cleanup | `@asynccontextmanager` lifespan without `try/finally` | HIGH | First resource never cleaned up if second allocation fails |
| 40 | I. FastAPI & Starlette | BaseHTTPMiddleware forces streaming into memory | `BaseHTTPMiddleware` with streaming endpoints | CRITICAL | Loads entire StreamingResponse/FileResponse into memory |
| 41 | I. FastAPI & Starlette | BaseHTTPMiddleware request body consumed | `await request\.body\(\)` inside middleware | HIGH | Reading body in middleware consumes receive queue |
| 42 | I. FastAPI & Starlette | CORS middleware order causing preflight failures | `add_middleware\(CORSMiddleware` not as last add_middleware | HIGH | CORSMiddleware must be last added (first to execute) |
| 43 | J. aioboto3 & AWS SDK | aiobotocore synchronous SSL/filesystem calls | N/A (internal library behavior) | HIGH | aiobotocore internally performs sync operations blocking event loop |
| 44 | J. aioboto3 & AWS SDK | aioboto3 S3 streaming API breaking change | `\.read\(\d+\)` on S3 Body objects | HIGH | After v9.6.0, stream.read(chunk_size) throws TypeError |
| 45 | H. AWS Lambda Specific | aioboto3 DEFAULT_SESSION caching stale event loop | `aioboto3\.\(client\|resource\)\(` | HIGH | Global DEFAULT_SESSION caches old event loop after replacement |
| 46 | J. aioboto3 & AWS SDK | aioboto3 connection pool hang on high-volume S3 | Concurrent put_object/get_object without semaphore | HIGH | Thousands of concurrent S3 operations exhaust connection pool |
| 47 | J. aioboto3 & AWS SDK | aioboto3 batch_writer UnprocessedItems not retried | `batch_write_item\(` without UnprocessedItems retry | MEDIUM | Low-level batch_write_item drops UnprocessedItems silently |
| 48 | E. Race Conditions & Data Integrity | asyncio.shield losing inner task reference | `asyncio\.shield\(` without storing result | HIGH | Inner task garbage collected before completion |
| 49 | E. Race Conditions & Data Integrity | asyncio.shield CancelledError consumption | `asyncio\.shield\(` with `except.*CancelledError` | MEDIUM | Shielded task catches CancelledError, task.cancelled() returns False |
| 50 | H. AWS Lambda Specific | SIGTERM not handled by asyncio.run() | `asyncio\.run\(` without SIGTERM handler | HIGH | Lambda/containers use SIGTERM for shutdown but asyncio.run() only handles SIGINT |
| 51 | M. Signal & Thread Safety | Signal handler lambda late binding | `add_signal_handler\(.*lambda` without default arg | MEDIUM | Lambda in loop for signal handlers binds late |
| 52 | M. Signal & Thread Safety | Default thread pool shared between DNS and run_in_executor | `run_in_executor\(None,` used heavily | HIGH | getaddrinfo and run_in_executor share default pool, heavy use starves DNS |
| 53 | M. Signal & Thread Safety | asyncio.to_thread() contextvars performance overhead | Heavy `asyncio\.to_thread\(` in hot paths | MEDIUM | Every to_thread call copies context, measurable overhead at high frequency |
| 54 | A. Event Loop Blocking | Standard library logging blocking event loop | `logging\.\(FileHandler\|StreamHandler\|SocketHandler\)` in async code | HIGH | FileHandler/StreamHandler perform sync I/O blocking event loop |
| 55 | M. Signal & Thread Safety | QueueListener not started or stopped | `QueueListener\(` without `.start()` and `.stop()` | MEDIUM | Missing start() accumulates logs, missing stop() loses final batch |
| 56 | F. Timeouts & Flow Control | aiohttp timeout includes connection pool queue wait | `ClientTimeout\(total=` without separate `connect` timeout | HIGH | Pool wait counts toward total timeout |
| 57 | D. Resource Management | Creating new aiohttp sessions per request | `aiohttp\.ClientSession\(\)` inside route handlers | HIGH | New session per request defeats pooling, exhausts file descriptors |
| 58 | D. Resource Management | aiofiles uses thread pool (not true async) | Heavy `aiofiles\.open\(` usage | MEDIUM | aiofiles delegates to thread pool, heavy use exhausts shared pool |
| 59 | M. Signal & Thread Safety | uvloop scheduling/timing behavioral differences | `uvloop` in requirements | MEDIUM | uvloop has different message delivery timing than default loop |
| 60 | M. Signal & Thread Safety | Async fixtures and tests in different event loops | `@pytest_asyncio\.fixture\(scope=` | HIGH | pytest-asyncio fixtures and tests may run in different event loops |
| 61 | M. Signal & Thread Safety | pytest-asyncio event loop closed prematurely | `@pytest_asyncio\.fixture` with `scope="class"` | HIGH | Bug in v0.23+ causes premature loop closure with async generator fixtures |
| 62 | F. Timeouts & Flow Control | asyncio.wait FIRST_COMPLETED leaking unfinished tasks | `asyncio\.wait\(.*FIRST_COMPLETED` without cancelling pending | HIGH | Pending tasks never cancelled, causing resource leaks |
| 63 | G. Error Handling | asyncio.gather does not cancel on first failure | `asyncio\.gather\(` without return_exceptions and without cancellation | HIGH | Unlike TaskGroup, gather does not cancel remaining tasks on failure |
| 64 | C. Concurrency Control | asyncio.Lock is not reentrant | `async with.*lock:` calling functions that also acquire same lock | HIGH | Same task acquiring lock twice causes deadlock |
| 65 | C. Concurrency Control | asyncio.Condition lost wakeup | `condition\.notify` followed by state changes before `await` | HIGH | Value can change again before woken consumers run |
| 66 | C. Concurrency Control | asyncio.Condition.notify() vs Task.cancel() race | `condition\.notify\(` with concurrent cancellation | HIGH | CPython bug: notify + cancel on same waiter loses notification |
| 67 | C. Concurrency Control | asyncio.Event.clear() race condition | `\.set\(\).*\.clear\(\)` on same Event | MEDIUM | set() then clear() creates race where some waiters miss the event |
| 68 | F. Timeouts & Flow Control | asyncio.wait_for race condition (Python 3.8-3.11) | `asyncio\.wait_for\(` on Python < 3.12 | CRITICAL | wait_for can swallow CancelledError and return result instead |
| 69 | F. Timeouts & Flow Control | asyncio.timeout(0) swallows prior cancellation | `asyncio\.timeout\(0\)` | HIGH | timeout(0) converts prior CancelledError to TimeoutError |
| 70 | M. Signal & Thread Safety | Event loop policy deprecated in Python 3.14 | `set_event_loop_policy\(\|get_event_loop_policy\(` | HIGH | set/get_event_loop_policy() deprecated, removed in 3.16 |
| 71 | M. Signal & Thread Safety | get_event_loop() raises RuntimeError in 3.14 | `asyncio\.get_event_loop\(\)` outside async context | HIGH | No longer creates implicit loop when none exists |
| 72 | M. Signal & Thread Safety | Subprocess wait() deadlock on full pipe | `await.*process\.wait\(\)` with `stdout=.*PIPE` | HIGH | Full output buffer causes wait() to deadlock |
| 73 | M. Signal & Thread Safety | WebSocket client set growing unbounded | `connected_clients\.add\(` without removal in finally | HIGH | Crashed connections leak from client set |
| 74 | M. Signal & Thread Safety | WebSocket send buffering on disconnect causing OOM | WebSocket send in loop without timeout/heartbeat | HIGH | Abrupt disconnect causes send() to buffer indefinitely |
| 75 | M. Signal & Thread Safety | Calling asyncio APIs from wrong thread | `set_result\(\|\.cancel\(\)` in threaded code without call_soon_threadsafe | CRITICAL | asyncio objects not thread-safe |
| 76 | C. Concurrency Control | Priority queue task starvation | `PriorityQueue` without timestamp | MEDIUM | PriorityQueue without aging starves low-priority tasks |
| 77 | M. Signal & Thread Safety | asyncio debug mode in production | `PYTHONASYNCIODEBUG\|set_debug\(True\)` | MEDIUM | Debug mode adds significant overhead |

---

## A. Event Loop Blocking

---

### 1. Blocking Calls in Async Functions

**Severity:** CRITICAL

**Description:**
Calling synchronous blocking functions such as `time.sleep()`, `requests.get()`, or the
built-in `open()` inside an `async def` function blocks the entire event loop. While the
blocking call executes, no other coroutines can run. In a server handling hundreds of
concurrent connections, a single `time.sleep(5)` call freezes all request processing for
five seconds.

**BAD Pattern:**

```python
import time
import requests

async def fetch_trail_data(trail_id: str) -> dict:
    # WRONG: blocks the entire event loop for 1 second
    time.sleep(1)

    # WRONG: synchronous HTTP call blocks all concurrent coroutines
    response = requests.get(f"https://api.example.com/trails/{trail_id}")
    return response.json()

async def read_config() -> str:
    # WRONG: synchronous file I/O blocks the event loop
    with open("/etc/config.json") as f:
        return f.read()
```

**GOOD Pattern:**

```python
import asyncio
import aiofiles
import httpx

async def fetch_trail_data(trail_id: str) -> dict:
    # CORRECT: non-blocking sleep
    await asyncio.sleep(1)

    # CORRECT: async HTTP client
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.example.com/trails/{trail_id}",
            timeout=10.0,
        )
        return response.json()

async def read_config() -> str:
    # CORRECT: async file I/O
    async with aiofiles.open("/etc/config.json") as f:
        return await f.read()
```

**Detection Approach:**
Grep for `time.sleep`, `requests.get`, `requests.post`, synchronous `open(` calls within
files that contain `async def`. The regex `async\s+def` combined with
`time\.sleep|requests\.(get|post|put|delete|patch)` across the same file flags candidates.

**Impact:**
Event loop starvation. Under load, a single blocking call causes cascading latency spikes
across all concurrent requests. In Lambda, this wastes billed execution time. At 1,157 RPS
sustained throughput, even a 100ms blocking call queues hundreds of requests.

---

### 8. Event Loop Blocking from CPU-Bound Work

**Severity:** MEDIUM

**Description:**
CPU-intensive operations such as hashing passwords, parsing large JSON payloads, image
processing, or complex regex compilation block the event loop thread. While the CPU work
executes, no other coroutines can run, causing latency spikes for all concurrent requests.

**BAD Pattern:**

```python
import hashlib
import json

async def process_payload(raw_data: bytes) -> dict:
    # WRONG: CPU-bound JSON parsing blocks event loop
    data = json.loads(raw_data)  # blocks if raw_data is megabytes

    # WRONG: CPU-bound hash computation blocks event loop
    checksum = hashlib.sha256(raw_data).hexdigest()

    return {"data": data, "checksum": checksum}
```

**GOOD Pattern:**

```python
import asyncio
import hashlib
import json
from functools import partial

async def process_payload(raw_data: bytes) -> dict:
    loop = asyncio.get_running_loop()

    # CORRECT: offload CPU-bound work to thread pool
    data = await loop.run_in_executor(None, json.loads, raw_data)
    checksum = await loop.run_in_executor(
        None, partial(lambda d: hashlib.sha256(d).hexdigest(), raw_data)
    )

    return {"data": data, "checksum": checksum}
```

**Detection Approach:**
Grep for `json.loads`, `hashlib.`, `bcrypt.`, `re.compile`, `PIL.Image`, `cv2.` inside
`async def` functions. These are candidates for `run_in_executor` offloading. The threshold
depends on payload size; anything processing user-supplied data of variable size should be
reviewed.

**Impact:**
Latency spikes affecting all concurrent requests. A single request parsing a 10MB JSON
payload blocks the event loop for hundreds of milliseconds, during which no other request
can proceed. P99 latency degrades proportionally to the frequency of CPU-bound operations.

---

### 15. DNS Resolution Blocking

**Severity:** LOW

**Description:**
Python's default DNS resolver (`socket.getaddrinfo`) is synchronous and blocks the calling
thread. In asyncio, this is typically offloaded to a thread pool, but under high concurrency
the thread pool can become saturated, causing DNS lookups to queue and increasing latency.
The default thread pool size is min(32, os.cpu_count() + 4).

**BAD Pattern:**

```python
import socket

async def resolve_endpoint(hostname: str) -> str:
    # WRONG: synchronous DNS resolution blocks thread pool
    result = socket.getaddrinfo(hostname, 443)
    return result[0][4][0]
```

**GOOD Pattern:**

```python
import asyncio

async def resolve_endpoint(hostname: str) -> str:
    loop = asyncio.get_running_loop()
    # CORRECT: use asyncio's built-in async resolver
    infos = await loop.getaddrinfo(hostname, 443)
    return infos[0][4][0]

# BETTER: use aiodns for fully async DNS resolution
# import aiodns
# resolver = aiodns.DNSResolver()
# result = await resolver.query(hostname, 'A')
```

**Detection Approach:**
Grep for `socket.getaddrinfo` and `socket.gethostbyname` in files containing `async def`.
These synchronous calls should be replaced with `loop.getaddrinfo()` or an async DNS library.

**Impact:**
Under normal load, the impact is minimal because the thread pool handles DNS lookups
efficiently. Under high concurrency (hundreds of new connections per second), thread pool
saturation causes DNS resolution to queue, adding hundreds of milliseconds of latency.
Most HTTP clients (httpx, aiohttp) handle this internally, so this issue primarily affects
code that performs direct DNS lookups.

---

### 54. Standard Library Logging Blocking Event Loop

**Severity:** HIGH

**Description:**
Python's standard library logging handlers (`FileHandler`, `StreamHandler`, `SocketHandler`)
perform synchronous I/O operations. When used from async code, these handlers block the
event loop thread during every log write. Under high log volume, this causes measurable
latency spikes as the event loop waits for disk I/O or network socket writes to complete.

**BAD Pattern:**

```python
import logging

# WRONG: FileHandler performs synchronous disk I/O on every log call
logger = logging.getLogger("traillens")
handler = logging.FileHandler("/var/log/traillens.log")
logger.addHandler(handler)

async def process_request(request_id: str) -> dict:
    # Each log call blocks the event loop for disk I/O
    logger.info(f"Processing request {request_id}")
    result = await do_work(request_id)
    logger.info(f"Completed request {request_id}")
    return result
```

**GOOD Pattern:**

```python
import logging
from logging.handlers import QueueHandler, QueueListener
from queue import Queue

# CORRECT: QueueHandler is non-blocking, QueueListener writes in background thread
log_queue: Queue = Queue(maxsize=10000)
queue_handler = QueueHandler(log_queue)

# Background thread handles actual I/O
file_handler = logging.FileHandler("/var/log/traillens.log")
listener = QueueListener(log_queue, file_handler, respect_handler_level=True)
listener.start()

logger = logging.getLogger("traillens")
logger.addHandler(queue_handler)

async def process_request(request_id: str) -> dict:
    # Non-blocking: message queued, written by background thread
    logger.info(f"Processing request {request_id}")
    result = await do_work(request_id)
    logger.info(f"Completed request {request_id}")
    return result

# At shutdown:
# listener.stop()
```

**Detection Approach:**
Grep for `logging.FileHandler`, `logging.StreamHandler`, `logging.SocketHandler` in files
that contain `async def`. These should be replaced with `QueueHandler` + `QueueListener`
or a structured logging library that handles async properly.

**Impact:**
Under moderate log volume (100+ log calls per second), each synchronous write introduces
microseconds to milliseconds of event loop blocking. At scale, this compounds into
measurable P99 latency degradation. Disk I/O spikes (e.g., log rotation) can cause
multi-second stalls.

---

## B. Coroutine Lifecycle

---

### 2. Missing Await on Coroutines

**Severity:** CRITICAL

**Description:**
When a coroutine function is called without `await`, Python creates a coroutine object but
never schedules it for execution. The coroutine silently does nothing. Python 3.14 emits a
`RuntimeWarning: coroutine was never awaited` but this is easy to miss in production logs.
The result is silent data loss or operations that appear to succeed but never execute.

**BAD Pattern:**

```python
async def save_audit_log(action: str, user_id: str) -> None:
    await repo.put_item({"action": action, "user_id": user_id})

async def handle_request(user_id: str) -> dict:
    # WRONG: coroutine created but never awaited - audit log is never saved
    save_audit_log("trail_view", user_id)

    return {"status": "ok"}
```

**GOOD Pattern:**

```python
async def handle_request(user_id: str) -> dict:
    # CORRECT: await the coroutine
    await save_audit_log("trail_view", user_id)

    return {"status": "ok"}
```

**Detection Approach:**
Static analysis is the most reliable approach. Look for coroutine function calls that are
not preceded by `await`, `asyncio.create_task()`, `asyncio.ensure_future()`, or assigned
for later awaiting. Python's `-W error::RuntimeWarning` flag turns the warning into an
exception during testing. The `flake8-async` linter plugin also detects this pattern.

**Impact:**
Silent data loss. Operations such as audit logging, notification sending, or database writes
appear to succeed but never execute. This is extremely difficult to diagnose in production
because no exception is raised.

---

### 3. Fire-and-Forget Tasks

**Severity:** HIGH

**Description:**
When `asyncio.create_task()` is called and the returned `Task` object is not stored in a
variable, the only reference is the event loop's weak reference set. If no strong reference
exists, the garbage collector may destroy the task before it completes. Any exception raised
in the task is also silently lost.

**BAD Pattern:**

```python
async def process_upload(file_id: str) -> None:
    # WRONG: task reference not stored, may be garbage collected
    asyncio.create_task(resize_image(file_id))
    asyncio.create_task(generate_thumbnail(file_id))

    # These tasks may never complete if GC runs
```

**GOOD Pattern:**

```python
# Module-level set to hold strong references
_background_tasks: set[asyncio.Task] = set()

async def process_upload(file_id: str) -> None:
    # CORRECT: store reference and add done callback for cleanup
    task = asyncio.create_task(resize_image(file_id))
    _background_tasks.add(task)
    task.add_done_callback(_background_tasks.discard)

    task2 = asyncio.create_task(generate_thumbnail(file_id))
    _background_tasks.add(task2)
    task2.add_done_callback(_background_tasks.discard)
```

**Detection Approach:**
Grep for `asyncio.create_task(` that is not preceded by an assignment (`=`). The pattern
`^\s*asyncio\.create_task\(` (line starts with optional whitespace then the call) indicates
the return value is discarded.

**Impact:**
Tasks silently disappear. Background work such as image processing, notification sending, or
cache warming may randomly fail to complete. Exceptions in fire-and-forget tasks are logged
only as "Task exception was never retrieved" and only when the task is garbage collected.

---

### 19. Exception Swallowed in Gather

**Severity:** MEDIUM

**Description:**
`asyncio.gather(return_exceptions=True)` captures exceptions as return values instead of
raising them. If the calling code does not explicitly check each result for exception
instances, errors are silently ignored. The function appears to succeed even though some
operations failed.

**BAD Pattern:**

```python
async def sync_all_trails(trail_ids: list[str]) -> list[dict]:
    results = await asyncio.gather(
        *[sync_trail(tid) for tid in trail_ids],
        return_exceptions=True,  # Exceptions become return values
    )

    # WRONG: returns exceptions mixed in with valid results
    # No error checking - caller receives Exception objects as data
    return results
```

**GOOD Pattern:**

```python
async def sync_all_trails(trail_ids: list[str]) -> list[dict]:
    results = await asyncio.gather(
        *[sync_trail(tid) for tid in trail_ids],
        return_exceptions=True,
    )

    # CORRECT: check each result for exceptions
    successful = []
    failed = []
    for tid, result in zip(trail_ids, results):
        if isinstance(result, BaseException):
            log_error(f"Failed to sync trail {tid}: {result}")
            failed.append(tid)
        else:
            successful.append(result)

    if failed:
        log_warning(f"Failed to sync {len(failed)} trails: {failed}")

    return successful
```

**Detection Approach:**
Grep for `gather\(.*return_exceptions\s*=\s*True` and check whether the results are
subsequently inspected with `isinstance(result, (Exception, BaseException))`. If the results
are returned or processed without exception checking, flag it.

**Impact:**
Silent partial failures. In a batch operation syncing 1,000 trail systems, 50 failures would
be silently swallowed and the operation would report success. Data inconsistency accumulates
over time without any alerts or logging.

---

### 20. Missing Cleanup in Task Cancellation

**Severity:** HIGH

**Description:**
When a task is cancelled (via `task.cancel()`), `asyncio.CancelledError` is raised at the
next `await` point in the coroutine. If the coroutine holds resources (database connections,
file handles, temporary files) and does not have a `finally` block, those resources are
leaked. The `except CancelledError` block should perform cleanup and then re-raise.

**BAD Pattern:**

```python
async def process_upload(file_path: str) -> str:
    temp_file = await create_temp_file()
    try:
        data = await read_file(file_path)
        processed = await transform(data)
        # If cancelled here, temp_file is never cleaned up
        result = await upload_to_s3(processed)
        return result
    except asyncio.CancelledError:
        # WRONG: no cleanup of temp_file
        raise
    except Exception as e:
        log_error(f"Upload failed: {e}")
        raise
```

**GOOD Pattern:**

```python
async def process_upload(file_path: str) -> str:
    temp_file = await create_temp_file()
    try:
        data = await read_file(file_path)
        processed = await transform(data)
        result = await upload_to_s3(processed)
        return result
    except asyncio.CancelledError:
        log_warning("Upload cancelled, cleaning up")
        raise
    except Exception as e:
        log_error(f"Upload failed: {e}")
        raise
    finally:
        # CORRECT: cleanup runs on success, exception, AND cancellation
        await cleanup_temp_file(temp_file)
```

**Detection Approach:**
Grep for `except.*CancelledError` and verify a `finally` block exists in the same
try/except structure. Also look for `async def` functions that acquire resources (open files,
create temp files, acquire connections) without a `finally` block for cleanup. The pattern
`except\s+.*CancelledError` without a subsequent `finally:` in the same block flags
candidates.

**Impact:**
Resource leaks on cancellation. In timeout scenarios (`asyncio.wait_for`), task group
cancellation, or graceful shutdown, resources are not released. Temporary files accumulate,
database connections are exhausted, and file descriptors leak. This is particularly harmful
in Lambda where the execution environment persists across warm invocations.

---

### 29. Queue.put()/get() Called Without await

**Severity:** CRITICAL

**Description:**
`asyncio.Queue.put()` and `asyncio.Queue.get()` are coroutine methods that must be awaited.
Calling them without `await` creates a coroutine object that is never scheduled, meaning
data is never actually placed into or retrieved from the queue. This results in silent data
loss because no error is raised -- the coroutine is simply garbage collected.

**BAD Pattern:**

```python
import asyncio

queue = asyncio.Queue(maxsize=100)

async def producer(data: list[dict]) -> None:
    for item in data:
        # WRONG: coroutine created but never awaited - data silently lost
        queue.put(item)

async def consumer() -> list[dict]:
    results = []
    while True:
        # WRONG: coroutine created but never awaited - hangs or returns coroutine object
        item = queue.get()
        results.append(item)
```

**GOOD Pattern:**

```python
import asyncio

queue: asyncio.Queue[dict] = asyncio.Queue(maxsize=100)

async def producer(data: list[dict]) -> None:
    for item in data:
        # CORRECT: await the coroutine
        await queue.put(item)

async def consumer() -> list[dict]:
    results = []
    while not queue.empty():
        # CORRECT: await the coroutine
        item = await queue.get()
        results.append(item)
        queue.task_done()
    return results
```

**Detection Approach:**
Grep for `queue\.put\(` and `queue\.get\(` that are not preceded by `await` on the same
line. The regex `(?<!await\s)queue\.(put|get)\(` catches most cases, though variable names
for the queue may differ.

**Impact:**
Complete silent data loss. The producer appears to succeed but no items enter the queue.
The consumer receives coroutine objects instead of data, or blocks indefinitely waiting for
items that were never enqueued. This is one of the most insidious async bugs because there
are no error messages -- only missing data.

---

## C. Concurrency Control

---

### 4. Unbounded Concurrency

**Severity:** HIGH

**Description:**
Using `asyncio.gather(*[task for item in items])` where `items` is a dynamic collection
creates an unbounded number of concurrent tasks. If the collection contains thousands of
items, this launches thousands of simultaneous connections to databases or external services,
overwhelming connection pools and causing throttling or failures.

**BAD Pattern:**

```python
async def notify_all_users(user_ids: list[str]) -> None:
    # WRONG: if user_ids has 10,000 entries, this opens 10,000 simultaneous
    # connections to the notification service
    await asyncio.gather(*[
        send_notification(uid) for uid in user_ids
    ])
```

**GOOD Pattern:**

```python
async def notify_all_users(user_ids: list[str]) -> None:
    # CORRECT: limit concurrency with a semaphore
    semaphore = asyncio.Semaphore(50)

    async def _send_limited(uid: str) -> None:
        async with semaphore:
            await send_notification(uid)

    await asyncio.gather(*[
        _send_limited(uid) for uid in user_ids
    ])
```

**Detection Approach:**
Grep for `asyncio\.gather\(\*\[` which indicates a dynamic list of coroutines being spread
into gather. Review whether a semaphore or concurrency limit is applied.

**Impact:**
DynamoDB throttling (`ProvisionedThroughputExceededException`), connection pool exhaustion,
external API rate limit violations, and cascading timeouts. At scale, this pattern can
cause a complete service outage when a single request triggers thousands of downstream calls.

---

### 12. Missing Optimistic Locking

**Severity:** HIGH

**Description:**
When multiple async coroutines concurrently read-modify-write the same DynamoDB item without
optimistic locking (ConditionExpression with a version field), the last write wins and
intermediate updates are silently lost. This is the async equivalent of a classic lost-update
problem.

**BAD Pattern:**

```python
async def increment_view_count(trail_id: str) -> None:
    async with session.resource("dynamodb") as dynamo:
        table = await dynamo.Table("trails")

        # READ
        response = await table.get_item(Key={"trail_id": trail_id})
        item = response["Item"]
        current_count = item["view_count"]

        # TOCTOU GAP: another coroutine can read the same count here

        # WRITE: may overwrite another coroutine's increment
        await table.update_item(
            Key={"trail_id": trail_id},
            UpdateExpression="SET view_count = :count",
            ExpressionAttributeValues={":count": current_count + 1},
        )
```

**GOOD Pattern:**

```python
async def increment_view_count(trail_id: str) -> None:
    async with session.resource("dynamodb") as dynamo:
        table = await dynamo.Table("trails")

        # CORRECT: atomic increment - no read needed
        await table.update_item(
            Key={"trail_id": trail_id},
            UpdateExpression="SET view_count = view_count + :inc",
            ExpressionAttributeValues={":inc": 1},
        )

# For non-trivial updates, use optimistic locking with version field
async def update_trail_details(trail_id: str, new_name: str, version: int) -> None:
    async with session.resource("dynamodb") as dynamo:
        table = await dynamo.Table("trails")

        # CORRECT: conditional write with version check
        await table.update_item(
            Key={"trail_id": trail_id},
            UpdateExpression="SET trail_name = :name, version = :new_ver",
            ConditionExpression="version = :expected_ver",
            ExpressionAttributeValues={
                ":name": new_name,
                ":new_ver": version + 1,
                ":expected_ver": version,
            },
        )
```

**Detection Approach:**
Grep for `update_item(` and `put_item(` calls that do not include `ConditionExpression` in
the same call. The pattern `\.update_item\(` without `ConditionExpression` on nearby lines
flags candidates. Not all updates require optimistic locking (atomic increments are safe),
so manual review is needed.

**Impact:**
Lost updates under concurrent access. At 1,157 RPS, concurrent updates to the same item
are common. Without optimistic locking, view counts are undercounted, user profile updates
are lost, and inventory quantities become inconsistent.

---

### 13. Shared Mutable State Without Lock

**Severity:** HIGH

**Description:**
Module-level mutable data structures (dicts, lists, sets) accessed by concurrent async
functions can experience race conditions. Although Python's GIL prevents true parallel
execution of bytecode, async code yields at every `await` point. If one coroutine reads a
dict, yields at an `await`, and another coroutine modifies the same dict, the first
coroutine sees inconsistent state when it resumes.

**BAD Pattern:**

```python
# Module-level shared state
_cache: dict[str, dict] = {}

async def get_trail_cached(trail_id: str) -> dict:
    if trail_id in _cache:
        return _cache[trail_id]

    # YIELD POINT: another coroutine can modify _cache here
    trail = await repo.get_trail(trail_id)

    # May overwrite a value set by another coroutine
    _cache[trail_id] = trail
    return trail

async def invalidate_cache(trail_id: str) -> None:
    # Race condition with get_trail_cached
    if trail_id in _cache:
        del _cache[trail_id]
```

**GOOD Pattern:**

```python
import asyncio

_cache: dict[str, dict] = {}
_cache_lock = asyncio.Lock()

async def get_trail_cached(trail_id: str) -> dict:
    async with _cache_lock:
        if trail_id in _cache:
            return _cache[trail_id]

    # Fetch outside lock to avoid holding lock during I/O
    trail = await repo.get_trail(trail_id)

    async with _cache_lock:
        # Double-check after acquiring lock
        if trail_id not in _cache:
            _cache[trail_id] = trail
        return _cache[trail_id]

async def invalidate_cache(trail_id: str) -> None:
    async with _cache_lock:
        _cache.pop(trail_id, None)
```

**Detection Approach:**
Grep for module-level assignments to mutable types (`\w+\s*[:=]\s*\{\}|\[\]|set\(\)`) and
check if these variables are modified within `async def` functions. Look for patterns where
the variable is both read and written across `await` yield points without an `asyncio.Lock`.

**Impact:**
Cache corruption, stale data served to users, duplicate processing. Under concurrent load,
race conditions manifest as intermittent bugs that are difficult to reproduce. The probability
of collision increases with request rate.

---

### 16. Deadlock from Nested Locks

**Severity:** CRITICAL

**Description:**
When two or more async functions acquire multiple `asyncio.Lock` instances in different
orders, a deadlock can occur. Coroutine A holds lock_1 and waits for lock_2, while
coroutine B holds lock_2 and waits for lock_1. Neither can proceed.

**BAD Pattern:**

```python
lock_trails = asyncio.Lock()
lock_users = asyncio.Lock()

async def assign_trail_to_user(trail_id: str, user_id: str) -> None:
    # Acquires trails lock first, then users lock
    async with lock_trails:
        trail = await repo.get_trail(trail_id)
        async with lock_users:
            user = await repo.get_user(user_id)
            await repo.assign(trail, user)

async def remove_user_from_trail(user_id: str, trail_id: str) -> None:
    # WRONG: acquires users lock first, then trails lock - opposite order
    async with lock_users:
        user = await repo.get_user(user_id)
        async with lock_trails:
            trail = await repo.get_trail(trail_id)
            await repo.unassign(trail, user)
```

**GOOD Pattern:**

```python
lock_trails = asyncio.Lock()
lock_users = asyncio.Lock()

# CORRECT: always acquire locks in consistent alphabetical/priority order
async def assign_trail_to_user(trail_id: str, user_id: str) -> None:
    async with lock_trails:
        async with lock_users:
            trail = await repo.get_trail(trail_id)
            user = await repo.get_user(user_id)
            await repo.assign(trail, user)

async def remove_user_from_trail(user_id: str, trail_id: str) -> None:
    # CORRECT: same lock order as assign_trail_to_user
    async with lock_trails:
        async with lock_users:
            trail = await repo.get_trail(trail_id)
            user = await repo.get_user(user_id)
            await repo.unassign(trail, user)
```

**Detection Approach:**
Grep for nested `async with \w+_lock` or `async with \w+lock` patterns. When multiple lock
acquisitions appear in the same function, verify that all functions acquire locks in the same
order. The pattern `async\s+with\s+\w+.*lock.*\n.*async\s+with\s+\w+.*lock` flags nested
lock acquisitions.

**Impact:**
Complete service hang. When a deadlock occurs, the affected coroutines wait forever, consuming
Lambda execution time and connection slots. Under load, more coroutines pile up waiting for
the locked resources, cascading into a full outage. Deadlocks are notoriously difficult to
debug in production because they require specific timing to reproduce.

---

### 17. Semaphore Leak on Exception

**Severity:** HIGH

**Description:**
When `asyncio.Semaphore.acquire()` is called explicitly (not via `async with`) and an
exception occurs before `release()`, the semaphore count is permanently decremented. Over
time, this exhausts the semaphore and all coroutines waiting to acquire it are blocked.

**BAD Pattern:**

```python
semaphore = asyncio.Semaphore(10)

async def process_request(request_data: dict) -> dict:
    # WRONG: if process() raises, semaphore is never released
    await semaphore.acquire()
    result = await process(request_data)  # may raise
    semaphore.release()
    return result
```

**GOOD Pattern:**

```python
semaphore = asyncio.Semaphore(10)

async def process_request(request_data: dict) -> dict:
    # CORRECT: async with guarantees release even on exception
    async with semaphore:
        result = await process(request_data)
        return result
```

**Detection Approach:**
Grep for `\.acquire\(\)` on `Semaphore` or `Lock` objects and verify that the corresponding
`release()` is in a `finally` block, or that `async with` is used instead. The pattern
`semaphore\.acquire|lock\.acquire` without `async with` on the same line flags potential
leaks.

**Impact:**
Gradual resource starvation. Each exception that skips the `release()` permanently reduces
available permits. After enough exceptions, the semaphore is exhausted and all new requests
block indefinitely. This is a slow-burning production issue that may take hours or days to
manifest depending on error rate.

---

### 64. asyncio.Lock Is Not Reentrant

**Severity:** HIGH

**Description:**
Unlike `threading.RLock`, `asyncio.Lock` is not reentrant. If the same task attempts to
acquire an `asyncio.Lock` it already holds, it will deadlock. There is no `asyncio.RLock`
in the standard library. This commonly occurs when a function acquires a lock, then calls
another function that also tries to acquire the same lock.

**BAD Pattern:**

```python
import asyncio

_lock = asyncio.Lock()

async def update_record(record_id: str, data: dict) -> None:
    async with _lock:
        record = await fetch_record(record_id)
        record.update(data)
        await save_record(record)
        # WRONG: validate_and_save also acquires _lock -> deadlock
        await validate_and_save(record)

async def validate_and_save(record: dict) -> None:
    async with _lock:  # DEADLOCK: same task already holds _lock
        if validate(record):
            await save_record(record)
```

**GOOD Pattern:**

```python
import asyncio

_lock = asyncio.Lock()

async def update_record(record_id: str, data: dict) -> None:
    async with _lock:
        record = await fetch_record(record_id)
        record.update(data)
        await save_record(record)
        # CORRECT: call internal version that doesn't acquire lock
        await _validate_and_save_unlocked(record)

async def _validate_and_save_unlocked(record: dict) -> None:
    """Internal version - caller must hold _lock."""
    if validate(record):
        await save_record(record)

async def validate_and_save(record: dict) -> None:
    """Public version - acquires lock."""
    async with _lock:
        await _validate_and_save_unlocked(record)
```

**Detection Approach:**
Grep for `async with.*lock:` and trace function calls within the locked section. If any
called function also acquires the same lock, this is a deadlock. Requires manual review
or static analysis tooling that traces call graphs.

**Impact:**
Deadlock. The task hangs forever waiting for a lock it already holds. In Lambda, this
burns execution time until the timeout kills the invocation. In a server, the connection
slot is permanently consumed, and under load this cascades into full service unavailability.

---

### 65. asyncio.Condition Lost Wakeup

**Severity:** HIGH

**Description:**
`asyncio.Condition.notify()` or `notify_all()` schedules waiters to be woken, but the
wakeup is not immediate. Between the notification and the waiter actually running, other
coroutines can modify the shared state. A waiter that checks the condition after waking
may find it no longer holds, leading to lost wakeups or incorrect behavior if the waiter
does not re-check the condition in a loop.

**BAD Pattern:**

```python
import asyncio

condition = asyncio.Condition()
data_ready = False
data_value = None

async def producer(value: str) -> None:
    global data_ready, data_value
    async with condition:
        data_value = value
        data_ready = True
        condition.notify()
        # WRONG: state may change before consumer runs
        data_ready = False  # Consumer may never see data_ready == True

async def consumer() -> str:
    async with condition:
        # WRONG: single check instead of loop
        if not data_ready:
            await condition.wait()
        # data_ready may be False if producer cleared it before consumer ran
        return data_value
```

**GOOD Pattern:**

```python
import asyncio

condition = asyncio.Condition()
data_ready = False
data_value = None

async def producer(value: str) -> None:
    global data_ready, data_value
    async with condition:
        data_value = value
        data_ready = True
        condition.notify()
        # CORRECT: do not modify state after notify

async def consumer() -> str:
    async with condition:
        # CORRECT: always wait in a loop checking the predicate
        while not data_ready:
            await condition.wait()
        return data_value

# BETTER: use wait_for which handles the loop internally
async def consumer_better() -> str:
    async with condition:
        await condition.wait_for(lambda: data_ready)
        return data_value
```

**Detection Approach:**
Grep for `condition.notify` and check whether state is modified after the notify call
within the same locked section. Also check that consumers use `while` loops (not `if`)
around `condition.wait()`, or use `condition.wait_for()`.

**Impact:**
Lost wakeups cause consumers to miss data or hang indefinitely. In producer-consumer
patterns, this leads to processing delays, message loss, or deadlocks depending on
whether the consumer retries.

---

### 66. asyncio.Condition.notify() vs Task.cancel() Race

**Severity:** HIGH

**Description:**
A CPython bug causes `asyncio.Condition.notify()` and `Task.cancel()` to race when both
target the same waiting task. If `cancel()` is called on a task waiting on a Condition,
and `notify()` is called concurrently, the notification can be entirely lost. The cancelled
task consumes the notification slot, but no other waiter is woken in its place.

**BAD Pattern:**

```python
import asyncio

condition = asyncio.Condition()

async def worker(task_id: int) -> None:
    async with condition:
        await condition.wait()
        # If this task is cancelled while waiting, the notification
        # is consumed but no other worker is woken

async def coordinator(workers: list[asyncio.Task]) -> None:
    # Cancel a specific worker
    workers[0].cancel()
    # Notify one worker - may be lost if it hits the cancelled task
    async with condition:
        condition.notify(1)
```

**GOOD Pattern:**

```python
import asyncio

condition = asyncio.Condition()

async def worker(task_id: int) -> None:
    async with condition:
        try:
            await condition.wait()
        except asyncio.CancelledError:
            # CORRECT: re-notify to prevent lost wakeup
            condition.notify(1)
            raise

async def coordinator(workers: list[asyncio.Task]) -> None:
    workers[0].cancel()
    async with condition:
        # CORRECT: notify extra to account for possible cancellation
        condition.notify(2)
```

**Detection Approach:**
Grep for `condition.notify(` in codebases that also use `task.cancel()` or
`asyncio.wait_for()` (which cancels internally). Manual review needed to verify whether
the notify target could be a cancelled waiter.

**Impact:**
Intermittent lost wakeups in producer-consumer systems. One notification disappears into
a cancelled task, leaving a live waiter blocked indefinitely. This is a subtle timing bug
that manifests rarely in development but frequently under production concurrency.

---

### 67. asyncio.Event.clear() Race Condition

**Severity:** MEDIUM

**Description:**
Calling `event.set()` followed immediately by `event.clear()` creates a race condition.
`set()` schedules wakeups for all waiters, but the wakeups are not processed synchronously.
If `clear()` is called before all waiters have run, some waiters may miss the event entirely
because the event is already cleared when they check it.

**BAD Pattern:**

```python
import asyncio

event = asyncio.Event()

async def pulse() -> None:
    # WRONG: set then clear creates race
    event.set()
    event.clear()
    # Some waiters may never wake because event is cleared before they run

async def waiter(waiter_id: int) -> None:
    await event.wait()
    print(f"Waiter {waiter_id} woke up")
```

**GOOD Pattern:**

```python
import asyncio

event = asyncio.Event()

async def pulse() -> None:
    event.set()
    # CORRECT: yield control so waiters can process the event
    await asyncio.sleep(0)
    event.clear()

async def waiter(waiter_id: int) -> None:
    await event.wait()
    print(f"Waiter {waiter_id} woke up")
```

**Detection Approach:**
Grep for `.set()` followed by `.clear()` on the same Event variable without an intervening
`await`. The pattern `\.set\(\).*\.clear\(\)` on nearby lines flags candidates.

**Impact:**
Lost wakeups for some waiters. In scenarios where an event is used to signal "data available"
and then immediately cleared, some consumers miss the signal and wait indefinitely. This
manifests as intermittent hangs in multi-consumer patterns.

---

### 76. Priority Queue Task Starvation

**Severity:** MEDIUM

**Description:**
`asyncio.PriorityQueue` orders items by priority value, but without an aging mechanism,
low-priority items can be starved indefinitely if higher-priority items keep arriving. This
is a classic scheduling problem that manifests in async task dispatchers and work queues.

**BAD Pattern:**

```python
import asyncio

queue: asyncio.PriorityQueue = asyncio.PriorityQueue()

async def enqueue(priority: int, task_data: dict) -> None:
    # WRONG: no aging - low priority items may never be processed
    await queue.put((priority, task_data))

async def worker() -> None:
    while True:
        priority, task_data = await queue.get()
        await process(task_data)
        queue.task_done()
```

**GOOD Pattern:**

```python
import asyncio
import time

queue: asyncio.PriorityQueue = asyncio.PriorityQueue()

async def enqueue(priority: int, task_data: dict) -> None:
    # CORRECT: include timestamp for aging - older items get higher effective priority
    timestamp = time.monotonic()
    await queue.put((priority, timestamp, task_data))

async def worker() -> None:
    while True:
        priority, timestamp, task_data = await queue.get()
        age = time.monotonic() - timestamp
        # Optionally log or alert on stale items
        if age > 60.0:
            log_warning(f"Task aged {age:.1f}s in queue")
        await process(task_data)
        queue.task_done()
```

**Detection Approach:**
Grep for `PriorityQueue` and check whether items include a timestamp or monotonic counter
that prevents indefinite starvation of low-priority items.

**Impact:**
Low-priority tasks never execute if the queue has a steady stream of high-priority items.
In a notification system, "low priority" alerts may be delayed hours or indefinitely,
violating SLA requirements.

---

## D. Resource Management

---

### 7. Resource Leaks

**Severity:** HIGH

**Description:**
Async clients and resources (httpx.AsyncClient, aiohttp.ClientSession, aioboto3 clients)
must be properly closed after use. Without `async with` or explicit `await client.aclose()`,
connection pools, file descriptors, and sockets are leaked. Over time, this causes
"too many open files" errors and connection pool exhaustion.

**BAD Pattern:**

```python
async def upload_photo(photo_data: bytes) -> str:
    # WRONG: client never closed - connection leak
    client = httpx.AsyncClient()
    response = await client.post("https://api.example.com/upload", content=photo_data)
    return response.json()["url"]

async def get_from_dynamo(key: str) -> dict:
    session = aioboto3.Session()
    # WRONG: resource not used as context manager
    dynamo = await session.resource("dynamodb")
    table = await dynamo.Table("trails")
    result = await table.get_item(Key={"id": key})
    return result.get("Item")
```

**GOOD Pattern:**

```python
async def upload_photo(photo_data: bytes) -> str:
    # CORRECT: async context manager ensures cleanup
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "https://api.example.com/upload",
            content=photo_data,
        )
        return response.json()["url"]

async def get_from_dynamo(key: str) -> dict:
    session = aioboto3.Session()
    # CORRECT: async with ensures resource cleanup
    async with session.resource("dynamodb") as dynamo:
        table = await dynamo.Table("trails")
        result = await table.get_item(Key={"id": key})
        return result.get("Item")
```

**Detection Approach:**
Grep for `httpx.AsyncClient()`, `aiohttp.ClientSession()`, `session.resource(`,
`session.client(` that are not inside an `async with` block. The pattern
`=\s*(httpx\.AsyncClient|aiohttp\.ClientSession)\(` without a preceding `async with` on the
same or previous line flags potential leaks.

**Impact:**
File descriptor exhaustion (`OSError: [Errno 24] Too many open files`), connection pool
depletion, memory leaks. These manifest gradually under sustained load and cause cascading
failures that are difficult to diagnose. Lambda invocations may fail after many warm reuses.

---

### 9. aioboto3 Context Manager Misuse

**Severity:** HIGH

**Description:**
aioboto3 resources and clients return async context managers that must be used with
`async with`. Calling `await session.resource("dynamodb")` without `async with` creates
a resource that is never properly cleaned up. The aioboto3 documentation explicitly requires
async context manager usage for all client and resource creation.

**BAD Pattern:**

```python
import aioboto3

async def query_trails() -> list[dict]:
    session = aioboto3.Session()

    # WRONG: resource created without async with - never cleaned up
    dynamo = await session.resource("dynamodb")
    table = await dynamo.Table("trails")
    response = await table.scan()
    return response["Items"]

async def send_notification(message: str) -> None:
    session = aioboto3.Session()

    # WRONG: client created without async with
    sns = await session.client("sns")
    await sns.publish(TopicArn="arn:aws:sns:...", Message=message)
```

**GOOD Pattern:**

```python
import aioboto3

async def query_trails() -> list[dict]:
    session = aioboto3.Session()

    # CORRECT: async with ensures cleanup
    async with session.resource("dynamodb") as dynamo:
        table = await dynamo.Table("trails")
        response = await table.scan()
        return response["Items"]

async def send_notification(message: str) -> None:
    session = aioboto3.Session()

    # CORRECT: async with ensures cleanup
    async with session.client("sns") as sns:
        await sns.publish(TopicArn="arn:aws:sns:...", Message=message)
```

**Detection Approach:**
Grep for `await\s+session\.(resource|client)\(` and verify the line or preceding line
contains `async with`. The pattern `(?<!async with )await\s+\w+\.(resource|client)\(` flags
potential misuse.

**Impact:**
Identical to issue #7 (Resource Leaks) but specific to AWS SDK connections. Leaked boto3
connections accumulate across Lambda warm invocations, eventually exhausting the underlying
urllib3 connection pool and causing `botocore.exceptions.EndpointConnectionError`.

---

### 14. Async Generator Not Closed

**Severity:** MEDIUM

**Description:**
When an `async for` loop over an async generator is exited early via `break` or `return`,
the generator's `finally` block may not execute unless `aclose()` is called. This can leak
resources such as database cursors, file handles, or network connections held by the
generator. PEP 789 documents this class of bugs in detail.

**BAD Pattern:**

```python
async def stream_trail_data(query: str):
    async with session.resource("dynamodb") as dynamo:
        table = await dynamo.Table("trails")
        # Generator holds DynamoDB resource open
        last_key = None
        while True:
            kwargs = {"FilterExpression": query}
            if last_key:
                kwargs["ExclusiveStartKey"] = last_key
            response = await table.scan(**kwargs)
            for item in response["Items"]:
                yield item
            last_key = response.get("LastEvaluatedKey")
            if not last_key:
                break

async def find_first_match(query: str) -> dict | None:
    # WRONG: break exits the async for but generator is not closed
    # DynamoDB resource may not be cleaned up
    async for trail in stream_trail_data(query):
        if trail["status"] == "open":
            return trail  # Generator not properly closed
    return None
```

**GOOD Pattern:**

```python
async def find_first_match(query: str) -> dict | None:
    gen = stream_trail_data(query)
    try:
        async for trail in gen:
            if trail["status"] == "open":
                return trail
        return None
    finally:
        # CORRECT: explicitly close the generator
        await gen.aclose()
```

**Detection Approach:**
Grep for `async for` loops that contain `break` or `return` statements. Check whether the
async generator is explicitly closed with `aclose()` in a `finally` block. The pattern
`async\s+for.*\n.*break|return` in the same block flags candidates.

**Impact:**
Resource leaks from unclosed database cursors, file handles, or network connections. In
long-running services, leaked resources accumulate and cause "too many open files" or
connection pool exhaustion. In Lambda, resources may persist across warm invocations.

---

### 57. Creating New aiohttp Sessions Per Request

**Severity:** HIGH

**Description:**
Creating a new `aiohttp.ClientSession()` for every HTTP request defeats connection pooling,
causes excessive TCP handshake overhead, and eventually exhausts file descriptors. Each
session creates its own connection pool, SSL context, and cookie jar. The aiohttp
documentation explicitly warns against creating sessions per-request.

**BAD Pattern:**

```python
import aiohttp

async def fetch_trail_info(trail_id: str) -> dict:
    # WRONG: new session per request - no connection reuse
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.example.com/trails/{trail_id}") as resp:
            return await resp.json()

async def fetch_all_trails(trail_ids: list[str]) -> list[dict]:
    # WRONG: creates len(trail_ids) separate sessions
    return await asyncio.gather(*[
        fetch_trail_info(tid) for tid in trail_ids
    ])
```

**GOOD Pattern:**

```python
import aiohttp

# Module-level session (created at startup, closed at shutdown)
_session: aiohttp.ClientSession | None = None

async def get_session() -> aiohttp.ClientSession:
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30, connect=5),
        )
    return _session

async def fetch_trail_info(trail_id: str) -> dict:
    # CORRECT: reuse shared session
    session = await get_session()
    async with session.get(f"https://api.example.com/trails/{trail_id}") as resp:
        return await resp.json()

async def fetch_all_trails(trail_ids: list[str]) -> list[dict]:
    # CORRECT: all requests share the same session and connection pool
    return await asyncio.gather(*[
        fetch_trail_info(tid) for tid in trail_ids
    ])
```

**Detection Approach:**
Grep for `aiohttp.ClientSession()` inside route handlers or functions that are called
per-request. The pattern `aiohttp\.ClientSession\(\)` inside `async def` functions that
are not startup/lifespan functions flags potential per-request session creation.

**Impact:**
TCP connection churn (new TLS handshake per request), file descriptor exhaustion under load,
increased latency from missing connection reuse (keep-alive). At 1,157 RPS, this creates
1,157 new TCP connections per second instead of reusing a pool of ~100.

---

### 58. aiofiles Uses Thread Pool (Not True Async)

**Severity:** MEDIUM

**Description:**
`aiofiles` provides an async interface to file operations, but internally it delegates all
I/O to a thread pool executor. This means heavy use of `aiofiles` can exhaust the shared
default `ThreadPoolExecutor`, which is also used by `asyncio.to_thread()`,
`loop.run_in_executor(None, ...)`, and DNS resolution. It is not "truly" async I/O.

**BAD Pattern:**

```python
import aiofiles

async def process_batch(file_paths: list[str]) -> list[str]:
    results = []
    # WRONG: hundreds of concurrent aiofiles calls exhaust thread pool
    tasks = [read_file(path) for path in file_paths]
    return await asyncio.gather(*tasks)

async def read_file(path: str) -> str:
    async with aiofiles.open(path) as f:
        return await f.read()
```

**GOOD Pattern:**

```python
import aiofiles
import asyncio

# CORRECT: limit concurrent file I/O to avoid thread pool exhaustion
_file_semaphore = asyncio.Semaphore(10)

async def read_file(path: str) -> str:
    async with _file_semaphore:
        async with aiofiles.open(path) as f:
            return await f.read()

async def process_batch(file_paths: list[str]) -> list[str]:
    # Concurrency bounded by semaphore
    return await asyncio.gather(*[read_file(path) for path in file_paths])
```

**Detection Approach:**
Grep for heavy `aiofiles.open(` usage, especially inside `asyncio.gather` or other
unbounded concurrency patterns. If dozens or hundreds of aiofiles operations run
concurrently, the thread pool will be saturated.

**Impact:**
Thread pool exhaustion causes all `run_in_executor` calls to queue, including DNS resolution
and other I/O offloading. This degrades latency for the entire application, not just file
operations. The default thread pool has min(32, os.cpu_count() + 4) workers.

---

## E. Race Conditions & Data Integrity

---

### 6. TOCTOU Race Conditions

**Severity:** CRITICAL

**Description:**
Time-of-Check to Time-of-Use (TOCTOU) occurs when code checks a condition, then performs
an action based on that condition, but an `await` between the check and the action allows
other coroutines to run and change the state. This is especially dangerous in async code
because every `await` is an explicit yield point where any other coroutine can execute.

**BAD Pattern:**

```python
async def get_or_create_trail(trail_name: str) -> dict:
    # CHECK: look up trail
    existing = await repo.get_trail_by_name(trail_name)

    # TOCTOU GAP: another coroutine can create the same trail here

    if existing is None:
        # ACT: create trail - may duplicate if another coroutine created it
        return await repo.create_trail(trail_name)

    return existing
```

**GOOD Pattern:**

```python
async def get_or_create_trail(trail_name: str) -> dict:
    # CORRECT: use DynamoDB conditional write to make check-and-act atomic
    try:
        return await repo.create_trail(
            trail_name,
            condition_expression="attribute_not_exists(trail_name)",
        )
    except repo.ConditionalCheckFailedException:
        # Trail already exists, retrieve it
        return await repo.get_trail_by_name(trail_name)
```

**Detection Approach:**
Grep for patterns where an `if ... is None` or `if not ...` check is followed by an `await`
call within the same block. The regex `if\s+\w+\s+is\s+None` in proximity to `await` is a
starting point. Manual review is needed to confirm the check and act are not atomic.

**Impact:**
Duplicate records, inconsistent state, double-charging users, duplicate notifications.
In DynamoDB, this can create duplicate items that violate business uniqueness constraints.
This class of bug is intermittent and load-dependent, making it extremely hard to reproduce
in testing but common in production under concurrent traffic.

---

### 48. asyncio.shield Losing Inner Task Reference

**Severity:** HIGH

**Description:**
`asyncio.shield()` wraps a coroutine in a new future that absorbs cancellation, allowing
the inner task to continue. However, if the outer (shielded) reference is dropped without
being awaited or stored, the inner task has no strong reference and may be garbage collected
before completion. The shield protects against cancellation but not against reference loss.

**BAD Pattern:**

```python
import asyncio

async def save_critical_data(data: dict) -> None:
    await repo.save(data)

async def handler(data: dict) -> dict:
    # WRONG: shielded task reference not stored - inner task may be GC'd
    asyncio.shield(save_critical_data(data))
    return {"status": "accepted"}
```

**GOOD Pattern:**

```python
import asyncio

_background_tasks: set[asyncio.Task] = set()

async def handler(data: dict) -> dict:
    # CORRECT: store the shielded task reference
    task = asyncio.ensure_future(asyncio.shield(save_critical_data(data)))
    _background_tasks.add(task)
    task.add_done_callback(_background_tasks.discard)
    return {"status": "accepted"}

# BETTER: await the shielded coroutine directly
async def handler_better(data: dict) -> dict:
    try:
        await asyncio.shield(save_critical_data(data))
    except asyncio.CancelledError:
        # Shield absorbed cancellation, inner task continues
        pass
    return {"status": "accepted"}
```

**Detection Approach:**
Grep for `asyncio.shield(` where the return value is not assigned to a variable or
immediately awaited. The pattern `^\s*asyncio\.shield\(` (no assignment) flags fire-and-forget
shield calls.

**Impact:**
Critical data writes silently fail to complete. The shield gives false confidence that the
operation is protected from cancellation, but without a strong reference the inner task is
subject to garbage collection. This is worse than a regular fire-and-forget because
developers believe the shield provides protection.

---

### 49. asyncio.shield CancelledError Consumption

**Severity:** MEDIUM

**Description:**
When a shielded coroutine is cancelled, `asyncio.shield()` raises `CancelledError` on the
outer future but the inner task continues running. If code catches `CancelledError` from the
shield and checks `task.cancelled()`, it returns `False` because the inner task was not
actually cancelled. This can confuse error handling logic that relies on `task.cancelled()`
to determine whether cleanup is needed.

**BAD Pattern:**

```python
import asyncio

async def process_with_shield() -> str | None:
    task = asyncio.ensure_future(long_running_operation())
    try:
        result = await asyncio.shield(task)
        return result
    except asyncio.CancelledError:
        # WRONG: assumes task was cancelled, but shield absorbed cancellation
        if task.cancelled():
            # This branch never executes - task is still running
            return None
        # Falls through without handling
        return None
```

**GOOD Pattern:**

```python
import asyncio

async def process_with_shield() -> str | None:
    task = asyncio.ensure_future(long_running_operation())
    try:
        result = await asyncio.shield(task)
        return result
    except asyncio.CancelledError:
        # CORRECT: understand that inner task is still running
        # Wait for it to complete if needed
        try:
            result = await asyncio.wait_for(task, timeout=5.0)
            return result
        except (asyncio.TimeoutError, asyncio.CancelledError):
            task.cancel()
            return None
```

**Detection Approach:**
Grep for `asyncio.shield(` combined with `except.*CancelledError` and `task.cancelled()`.
If the cancellation handler relies on `task.cancelled()` returning True, it will behave
incorrectly.

**Impact:**
Incorrect error handling and resource management. Code paths designed for "task was
cancelled" scenarios never execute, while the inner task continues running without
supervision. This can lead to resource leaks or unexpected behavior when the unsupervised
task completes later.

---

## F. Timeouts & Flow Control

---

### 5. Missing Timeouts on External Calls

**Severity:** HIGH

**Description:**
Awaiting an external HTTP call, database query, or service invocation without a timeout
parameter means the coroutine can hang indefinitely if the remote service is unresponsive.
In Lambda, this burns billed execution time until the Lambda timeout kills the invocation.
In a server, it ties up a connection slot forever.

**BAD Pattern:**

```python
async def get_trail_details(trail_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        # WRONG: no timeout - hangs forever if service is down
        response = await client.get(f"https://api.example.com/trails/{trail_id}")
        return response.json()

async def get_user(user_id: str) -> dict:
    async with session.resource("dynamodb") as dynamo:
        table = await dynamo.Table("users")
        # WRONG: no timeout on DynamoDB call
        response = await table.get_item(Key={"user_id": user_id})
        return response.get("Item")
```

**GOOD Pattern:**

```python
async def get_trail_details(trail_id: str) -> dict:
    async with httpx.AsyncClient(timeout=10.0) as client:
        # CORRECT: explicit timeout
        response = await client.get(f"https://api.example.com/trails/{trail_id}")
        return response.json()

async def get_user(user_id: str) -> dict:
    # CORRECT: wrap with asyncio.wait_for for operations without native timeout
    async with session.resource("dynamodb") as dynamo:
        table = await dynamo.Table("users")
        response = await asyncio.wait_for(
            table.get_item(Key={"user_id": user_id}),
            timeout=5.0,
        )
        return response.get("Item")
```

**Detection Approach:**
Grep for `await\s+\w+\.(get|post|put|delete|request|query|scan|get_item|put_item)\(` and
verify the presence of `timeout=` in the same call. Also check that `httpx.AsyncClient()`
or `aiohttp.ClientSession()` constructors include a `timeout` parameter.

**Impact:**
Resource exhaustion. Hanging coroutines consume Lambda execution time (billed per 1ms),
connection pool slots, and memory. A single unresponsive downstream service can cascade
into a full outage as all available connections become stuck.

---

### 27. Unbounded asyncio.Queue Memory Exhaustion

**Severity:** CRITICAL

**Description:**
Creating an `asyncio.Queue()` without specifying `maxsize` creates an unbounded queue. If
the producer is faster than the consumer, or if the consumer crashes, items accumulate
indefinitely in memory until the process runs out of memory (OOM). This is especially
dangerous in Lambda where memory is limited and billed.

**BAD Pattern:**

```python
import asyncio

# WRONG: unbounded queue - if consumer dies, memory grows without limit
queue: asyncio.Queue = asyncio.Queue()

async def producer(items: list[dict]) -> None:
    for item in items:
        await queue.put(item)  # Never blocks - queue grows forever

async def consumer() -> None:
    while True:
        item = await queue.get()
        await process(item)  # If this crashes, queue fills up
        queue.task_done()
```

**GOOD Pattern:**

```python
import asyncio

# CORRECT: bounded queue provides backpressure
queue: asyncio.Queue[dict] = asyncio.Queue(maxsize=1000)

async def producer(items: list[dict]) -> None:
    for item in items:
        # Blocks when queue is full - backpressure prevents OOM
        await queue.put(item)

async def consumer() -> None:
    while True:
        try:
            item = await queue.get()
            await process(item)
        except Exception as e:
            log_error(f"Consumer error: {e}")
        finally:
            queue.task_done()
```

**Detection Approach:**
Grep for `asyncio.Queue()` with no arguments or `asyncio.Queue(maxsize=0)` (which is also
unbounded). The regex `asyncio\.Queue\(\s*\)` catches the common case.

**Impact:**
Out-of-memory crash. In Lambda with 256MB memory, an unbounded queue of JSON objects can
fill memory in seconds under high throughput. The Lambda invocation is killed, losing all
queued data. In a server, OOM causes process restart, dropping all in-flight requests.

---

### 28. Queue Consumer Exception Causing Silent Deadlock

**Severity:** CRITICAL

**Description:**
When a consumer task processing items from an `asyncio.Queue` crashes with an unhandled
exception, it stops consuming. If there is only one consumer, or all consumers crash,
producers calling `queue.put()` on a full bounded queue block indefinitely. Additionally,
`queue.join()` waits forever because `task_done()` is never called for the item that
caused the crash.

**BAD Pattern:**

```python
import asyncio

queue: asyncio.Queue[dict] = asyncio.Queue(maxsize=100)

async def consumer() -> None:
    while True:
        item = await queue.get()
        # WRONG: if process() raises, task_done() never called
        # and consumer loop exits silently
        await process(item)
        queue.task_done()
```

**GOOD Pattern:**

```python
import asyncio

queue: asyncio.Queue[dict] = asyncio.Queue(maxsize=100)

async def consumer() -> None:
    while True:
        item = await queue.get()
        try:
            await process(item)
        except Exception as e:
            # CORRECT: log error but continue consuming
            log_error(f"Failed to process item: {e}")
        finally:
            # CORRECT: always call task_done, even on failure
            queue.task_done()
```

**Detection Approach:**
Grep for `await.*queue.get()` and check whether the subsequent processing is wrapped in
try/except with `queue.task_done()` in a finally block. The absence of error handling
around queue consumption is the flag.

**Impact:**
Silent deadlock. Producers block on `queue.put()` and `queue.join()` hangs forever. In
Lambda, this burns execution time until timeout. In a server, the entire pipeline stalls
without any error message, making diagnosis extremely difficult.

---

### 56. aiohttp Timeout Includes Connection Pool Queue Wait

**Severity:** HIGH

**Description:**
`aiohttp.ClientTimeout.total` starts counting from the moment the coroutine is called, not
from when a connection is acquired from the pool. If the connection pool is exhausted and
the request queues for a connection, the queue wait time counts toward the total timeout.
This means requests may timeout before they even start, especially under high concurrency.

**BAD Pattern:**

```python
import aiohttp

# WRONG: total timeout includes pool wait time
session = aiohttp.ClientSession(
    timeout=aiohttp.ClientTimeout(total=5.0)
)

async def fetch(url: str) -> dict:
    # If pool is exhausted and request waits 4s for connection,
    # only 1s remains for the actual request
    async with session.get(url) as resp:
        return await resp.json()
```

**GOOD Pattern:**

```python
import aiohttp

# CORRECT: separate timeouts for connection acquisition and request
session = aiohttp.ClientSession(
    timeout=aiohttp.ClientTimeout(
        total=30.0,       # Total including pool wait
        connect=5.0,      # Connection acquisition timeout
        sock_connect=5.0, # TCP connection timeout
        sock_read=10.0,   # Individual read timeout
    ),
    connector=aiohttp.TCPConnector(
        limit=100,        # Connection pool size
        limit_per_host=30,
    ),
)

async def fetch(url: str) -> dict:
    async with session.get(url) as resp:
        return await resp.json()
```

**Detection Approach:**
Grep for `ClientTimeout(total=` without separate `connect` or `sock_connect` timeouts.
Also check whether `TCPConnector` limits are configured to prevent pool exhaustion.

**Impact:**
Premature timeouts under load. When the connection pool is saturated, requests timeout
during pool wait before making any network call. This appears as random timeout errors
that increase with concurrency, misleading operators into thinking the downstream service
is slow when the actual bottleneck is local pool exhaustion.

---

### 62. asyncio.wait FIRST_COMPLETED Leaking Unfinished Tasks

**Severity:** HIGH

**Description:**
`asyncio.wait()` with `return_when=FIRST_COMPLETED` returns as soon as any task completes,
but does not cancel the remaining pending tasks. If the caller does not explicitly cancel
or await the pending tasks, they continue running in the background, consuming resources.
Over time, leaked tasks accumulate and cause memory exhaustion or unexpected side effects.

**BAD Pattern:**

```python
import asyncio

async def race_requests(urls: list[str]) -> dict:
    tasks = [asyncio.create_task(fetch(url)) for url in urls]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    # WRONG: pending tasks continue running, never cancelled
    result = done.pop().result()
    return result
```

**GOOD Pattern:**

```python
import asyncio

async def race_requests(urls: list[str]) -> dict:
    tasks = [asyncio.create_task(fetch(url)) for url in urls]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    # CORRECT: cancel all pending tasks
    for task in pending:
        task.cancel()

    # Wait for cancellation to complete
    if pending:
        await asyncio.wait(pending)

    result = done.pop().result()
    return result
```

**Detection Approach:**
Grep for `asyncio.wait(` with `FIRST_COMPLETED` and verify that the `pending` set is
iterated with `.cancel()` calls. Missing cancellation of pending tasks is the flag.

**Impact:**
Resource leak. Each leaked task consumes memory, holds connections, and may perform
unwanted side effects (writing to database, sending notifications). At scale, leaked tasks
accumulate across requests, degrading performance until eventual OOM or connection
exhaustion.

---

### 68. asyncio.wait_for Race Condition (Python 3.8-3.11)

**Severity:** CRITICAL

**Description:**
In Python 3.8 through 3.11, `asyncio.wait_for()` has a race condition where it can
swallow a `CancelledError` and return the task's result instead. This occurs when the task
completes at the exact moment `wait_for` is cancelled. The task's result is silently
discarded. This was fixed in Python 3.12 (CPython issue #43389).

**BAD Pattern:**

```python
import asyncio

# On Python 3.8-3.11:
async def fetch_with_timeout(url: str) -> dict:
    # DANGEROUS: wait_for may swallow CancelledError and return result
    # or cancel and return None when it should have returned data
    result = await asyncio.wait_for(fetch(url), timeout=5.0)
    return result
```

**GOOD Pattern:**

```python
import asyncio
import sys

async def fetch_with_timeout(url: str) -> dict:
    if sys.version_info >= (3, 12):
        # CORRECT: fixed in Python 3.12+
        return await asyncio.wait_for(fetch(url), timeout=5.0)
    else:
        # WORKAROUND for Python 3.8-3.11: use asyncio.timeout context manager
        # or manual task + wait implementation
        task = asyncio.create_task(fetch(url))
        try:
            return await asyncio.wait_for(asyncio.shield(task), timeout=5.0)
        except asyncio.TimeoutError:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            raise
```

**Detection Approach:**
Grep for `asyncio.wait_for(` in projects that target Python versions before 3.12. Check
`python_requires` in pyproject.toml or setup.cfg. If the minimum Python version is < 3.12,
flag all `wait_for` usage for review.

**Impact:**
Silent data loss or incorrect cancellation behavior. The race condition causes intermittent
bugs where results are discarded or cancellation fails to propagate. This is extremely
difficult to reproduce because it requires exact timing between task completion and
cancellation. Python 3.14 is not affected (fix is in 3.12+).

---

### 69. asyncio.timeout(0) Swallows Prior Cancellation

**Severity:** HIGH

**Description:**
Using `asyncio.timeout(0)` can convert a prior `CancelledError` into a `TimeoutError`.
If a task has already been cancelled and hits an `async with asyncio.timeout(0):` block,
the `CancelledError` is caught by the timeout context manager and re-raised as
`TimeoutError`, masking the original cancellation.

**BAD Pattern:**

```python
import asyncio

async def quick_check(data: dict) -> bool:
    # WRONG: timeout(0) can mask CancelledError as TimeoutError
    try:
        async with asyncio.timeout(0):
            result = await validate(data)
            return result
    except TimeoutError:
        # This may actually be a CancelledError in disguise
        return False
```

**GOOD Pattern:**

```python
import asyncio

async def quick_check(data: dict) -> bool:
    # CORRECT: use a small non-zero timeout
    try:
        async with asyncio.timeout(0.001):
            result = await validate(data)
            return result
    except TimeoutError:
        return False

# OR: handle CancelledError explicitly before timeout block
async def quick_check_safe(data: dict) -> bool:
    try:
        async with asyncio.timeout(0.001):
            result = await validate(data)
            return result
    except asyncio.CancelledError:
        raise  # Re-raise actual cancellation
    except TimeoutError:
        return False
```

**Detection Approach:**
Grep for `asyncio.timeout(0)` or `asyncio.timeout(0.0)`. Zero-duration timeouts are
always suspicious and should use a small positive value instead.

**Impact:**
Cancellation signals are converted to timeout errors, preventing proper task cleanup and
shutdown behavior. In graceful shutdown scenarios, tasks that should be cancelled instead
report timeout errors, confusing error handling and potentially preventing clean shutdown.

---

## G. Error Handling

---

### 10. Swallowed CancelledError

**Severity:** CRITICAL

**Description:**
In Python 3.9+, `asyncio.CancelledError` is a subclass of `BaseException`, not `Exception`.
However, many codebases still have `except Exception:` blocks that accidentally catch
`CancelledError` in Python 3.8 and earlier (where it was a subclass of `Exception`).
Even in Python 3.14, catching `BaseException` or using a bare `except:` will swallow
cancellation. If `CancelledError` is caught and not re-raised, task cancellation fails
silently, leading to zombie tasks that never terminate.

**BAD Pattern:**

```python
async def fetch_with_retry(url: str) -> dict:
    while True:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                return response.json()
        except Exception as e:
            # WRONG: in Python <3.9, this catches CancelledError
            # Even in 3.14, this pattern is fragile - bare except: would catch it
            log_error(f"Retry after error: {e}")
            await asyncio.sleep(1)

async def process_data(data: bytes) -> None:
    try:
        result = await heavy_computation(data)
        await save_result(result)
    except BaseException:
        # WRONG: catches CancelledError and swallows it
        log_error("Something went wrong")
```

**GOOD Pattern:**

```python
async def fetch_with_retry(url: str) -> dict:
    while True:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                return response.json()
        except asyncio.CancelledError:
            # CORRECT: always re-raise CancelledError
            raise
        except Exception as e:
            log_error(f"Retry after error: {e}")
            await asyncio.sleep(1)

async def process_data(data: bytes) -> None:
    try:
        result = await heavy_computation(data)
        await save_result(result)
    except asyncio.CancelledError:
        # CORRECT: re-raise after cleanup
        raise
    except Exception as e:
        log_error(f"Processing failed: {e}")
```

**Detection Approach:**
Grep for `except\s+Exception` and `except\s+BaseException` and bare `except:` within
`async def` functions. Each match should be reviewed to verify that `CancelledError` is
either excluded or re-raised.

**Impact:**
Zombie tasks that never terminate. Task cancellation (used by `asyncio.wait_for` timeouts,
`TaskGroup` cancellation, and graceful shutdown) becomes ineffective. Resources held by the
task are never released. In Lambda, this can cause invocations to run until the Lambda
timeout, wasting billed execution time.

---

### 23. Catching ExceptionGroup with Plain except Instead of except*

**Severity:** HIGH

**Description:**
Python 3.11+ introduced `except*` syntax for handling `ExceptionGroup`. Using plain
`except ExceptionGroup` loses the ability to selectively handle individual sub-exceptions
by type. The `except*` syntax automatically unwraps the group and matches sub-exceptions,
re-raising any that are not handled. Using plain `except` forces manual iteration over
`.exceptions` and loses the automatic re-raise behavior.

**BAD Pattern:**

```python
import asyncio

async def process_batch(items: list[dict]) -> list[dict]:
    try:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(process(item)) for item in items]
    except ExceptionGroup as eg:
        # WRONG: manual iteration loses except* benefits
        for exc in eg.exceptions:
            if isinstance(exc, ValueError):
                log_error(f"Validation error: {exc}")
            elif isinstance(exc, ConnectionError):
                log_error(f"Connection error: {exc}")
            else:
                raise  # This re-raises the whole group, not the unhandled exception
```

**GOOD Pattern:**

```python
import asyncio

async def process_batch(items: list[dict]) -> list[dict]:
    try:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(process(item)) for item in items]
    except* ValueError as eg:
        # CORRECT: handles only ValueError sub-exceptions
        for exc in eg.exceptions:
            log_error(f"Validation error: {exc}")
    except* ConnectionError as eg:
        # CORRECT: handles only ConnectionError sub-exceptions
        for exc in eg.exceptions:
            log_error(f"Connection error: {exc}")
    # Unhandled exception types are automatically re-raised
```

**Detection Approach:**
Grep for `except\s+ExceptionGroup` (without the `*`). This indicates plain except syntax
is being used instead of `except*`. Note that `except*` is the correct form for handling
sub-exceptions in ExceptionGroups.

**Impact:**
Incorrect exception handling. Unhandled sub-exception types may be swallowed or the entire
group may be re-raised when only specific sub-exceptions should propagate. This makes error
recovery unreliable and can mask important errors in concurrent task processing.

---

### 24. Raising Empty ExceptionGroup

**Severity:** MEDIUM

**Description:**
Creating an `ExceptionGroup` with an empty list of exceptions and raising it causes a
`ValueError` at runtime. This typically occurs when code collects errors in a list and
creates an ExceptionGroup without checking if the list is empty first.

**BAD Pattern:**

```python
async def validate_all(items: list[dict]) -> None:
    errors: list[Exception] = []
    for item in items:
        try:
            await validate(item)
        except ValueError as e:
            errors.append(e)

    # WRONG: raises ValueError if errors list is empty
    raise ExceptionGroup("Validation errors", errors)
```

**GOOD Pattern:**

```python
async def validate_all(items: list[dict]) -> None:
    errors: list[Exception] = []
    for item in items:
        try:
            await validate(item)
        except ValueError as e:
            errors.append(e)

    # CORRECT: only raise if there are actual errors
    if errors:
        raise ExceptionGroup("Validation errors", errors)
```

**Detection Approach:**
Grep for `ExceptionGroup(` and verify that the exceptions list is checked for emptiness
before raising. The pattern `raise\s+ExceptionGroup\(` without a preceding `if` check on
the error list is suspicious.

**Impact:**
`ValueError: second argument (exceptions) must be a non-empty sequence` at runtime.
This is a straightforward bug that crashes the code path, but it only manifests when no
validation errors occur (the "happy path"), making it easy to miss in testing that focuses
on error scenarios.

---

### 25. Nested ExceptionGroup Context Loss

**Severity:** MEDIUM

**Description:**
When `ExceptionGroup` instances are nested (a group containing other groups), `except*`
matches sub-exceptions at any nesting depth. This means the parent context (which group
the exception came from) is lost in the handler. If error handling depends on knowing which
group a sub-exception belongs to, the `except*` syntax alone is insufficient.

**BAD Pattern:**

```python
import asyncio

async def process_all() -> None:
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(batch_a())  # May raise ExceptionGroup with ValueErrors
            tg.create_task(batch_b())  # May also raise ExceptionGroup with ValueErrors
    except* ValueError as eg:
        # WRONG: cannot distinguish whether ValueError came from batch_a or batch_b
        # eg.exceptions contains flattened ValueErrors from both batches
        for exc in eg.exceptions:
            log_error(f"ValueError: {exc}")  # Lost batch context
```

**GOOD Pattern:**

```python
import asyncio

async def process_all() -> None:
    # CORRECT: handle each batch separately to preserve context
    results: dict[str, BaseException | None] = {}

    async def tracked_batch(name: str, coro) -> None:
        try:
            await coro()
        except Exception as e:
            results[name] = e
            raise

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(tracked_batch("batch_a", batch_a))
            tg.create_task(tracked_batch("batch_b", batch_b))
    except* ValueError as eg:
        for exc in eg.exceptions:
            # Context preserved via tracked_batch wrapper
            log_error(f"ValueError in batch: {exc}")
```

**Detection Approach:**
This requires design-level review. Look for nested TaskGroup usage or TaskGroups whose
tasks themselves may raise ExceptionGroups. If error handling in the outer `except*` needs
to know which inner task produced a particular sub-exception, the pattern is problematic.

**Impact:**
Incorrect error attribution in logging and monitoring. When errors from different sources
are mixed in a flattened ExceptionGroup, operators cannot determine the root cause. This
complicates debugging of concurrent batch operations.

---

### 26. TaskGroup Missing CancelledError Cleanup

**Severity:** HIGH

**Description:**
When one task in a `TaskGroup` fails, all remaining tasks are cancelled. The cancelled
tasks receive `CancelledError` at their next `await` point. If these tasks hold resources
(database connections, file handles, locks) and do not handle `CancelledError` in a
`try/finally` block, those resources are leaked. This is pattern #20 applied specifically
to TaskGroup contexts.

**BAD Pattern:**

```python
import asyncio

async def resize_image(image_id: str) -> str:
    conn = await get_db_connection()
    # If another task in the group fails, this task is cancelled
    # conn is never released
    result = await process_image(conn, image_id)
    await release_connection(conn)
    return result

async def process_batch(image_ids: list[str]) -> list[str]:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(resize_image(iid)) for iid in image_ids]
    return [t.result() for t in tasks]
```

**GOOD Pattern:**

```python
import asyncio

async def resize_image(image_id: str) -> str:
    conn = await get_db_connection()
    try:
        result = await process_image(conn, image_id)
        return result
    finally:
        # CORRECT: cleanup runs even when cancelled by TaskGroup
        await release_connection(conn)

async def process_batch(image_ids: list[str]) -> list[str]:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(resize_image(iid)) for iid in image_ids]
    return [t.result() for t in tasks]
```

**Detection Approach:**
Grep for `tg.create_task(` and examine the target coroutines. If they acquire resources
(connections, files, locks) without `try/finally` blocks, they will leak resources when
cancelled by TaskGroup.

**Impact:**
Resource leaks on partial batch failures. If one task in a group of 100 fails, the other
99 are cancelled. Without proper cleanup, 99 database connections or file handles are
leaked. Repeated batch failures can quickly exhaust connection pools.

---

### 63. asyncio.gather Does Not Cancel on First Failure

**Severity:** HIGH

**Description:**
Unlike `asyncio.TaskGroup`, `asyncio.gather()` does not cancel remaining tasks when one
fails (unless `return_exceptions=False` is used, in which case it raises the first
exception but other tasks keep running). This means failed operations leave zombie tasks
running in the background, consuming resources and potentially producing unwanted side
effects.

**BAD Pattern:**

```python
import asyncio

async def process_items(items: list[dict]) -> list[dict]:
    # WRONG: if one task fails, others continue running
    # They may write to database, send notifications, etc.
    results = await asyncio.gather(*[
        process(item) for item in items
    ])
    return results
```

**GOOD Pattern:**

```python
import asyncio

# OPTION 1: Use TaskGroup (Python 3.11+) - cancels on first failure
async def process_items(items: list[dict]) -> list[dict]:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(process(item)) for item in items]
    return [t.result() for t in tasks]

# OPTION 2: Manual cancellation with gather
async def process_items_compat(items: list[dict]) -> list[dict]:
    tasks = [asyncio.create_task(process(item)) for item in items]
    try:
        return await asyncio.gather(*tasks)
    except Exception:
        # Cancel all remaining tasks on first failure
        for task in tasks:
            task.cancel()
        # Wait for cancellation to complete
        await asyncio.gather(*tasks, return_exceptions=True)
        raise
```

**Detection Approach:**
Grep for `asyncio.gather(` without `return_exceptions=True` and without surrounding
try/except that cancels tasks. If failure of one operation should stop all others, gather
without cancellation is incorrect.

**Impact:**
Wasted resources and unwanted side effects. If a batch of 100 tasks includes one that
validates input and fails early, the other 99 continue executing (writing to database,
sending emails, etc.). This produces inconsistent state and wastes compute resources.

---

## H. AWS Lambda Specific

---

### 18. Lambda Event Loop Reuse

**Severity:** CRITICAL

**Description:**
`asyncio.run()` creates a new event loop, runs the coroutine, and then **closes the event
loop**. In AWS Lambda, the execution environment is reused across invocations (warm start).
If the handler calls `asyncio.run()`, the event loop is closed after the first invocation.
Subsequent warm invocations either fail with "Event loop is closed" or create a new event
loop, negating the benefits of connection reuse across invocations.

This also breaks module-level client caching. If aioboto3 sessions, HTTP clients, or database
connections are initialized at module level for reuse across warm invocations, `asyncio.run()`
closing the event loop invalidates all of these cached clients. They were created on the
now-closed loop and cannot be used on a new loop, causing errors like "attached to a different
event loop" or "Event loop is closed" on the second invocation.

**BAD Pattern:**

```python
import asyncio

# Module-level client initialization for reuse across invocations
session = aioboto3.Session()

def handler(event, context):
    # WRONG: asyncio.run() closes the event loop after each invocation
    # Warm invocations fail or lose connection reuse
    return asyncio.run(async_handler(event, context))

async def async_handler(event, context):
    async with session.resource("dynamodb") as dynamo:
        table = await dynamo.Table("trails")
        return await table.get_item(Key={"id": event["trail_id"]})
```

**GOOD Pattern:**

```python
import asyncio

session = aioboto3.Session()

# CORRECT: reuse the event loop across warm invocations
def handler(event, context):
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(async_handler(event, context))

async def async_handler(event, context):
    async with session.resource("dynamodb") as dynamo:
        table = await dynamo.Table("trails")
        return await table.get_item(Key={"id": event["trail_id"]})

# ALTERNATIVE: use mangum for FastAPI in Lambda (handles loop lifecycle)
# from mangum import Mangum
# handler = Mangum(app)
```

**Detection Approach:**
Grep for `asyncio\.run\(` in Lambda handler files. The pattern is straightforward. Also check
for `asyncio.new_event_loop()` followed by `loop.close()` in handler functions.

**Impact:**
First invocation succeeds, subsequent warm invocations fail with `RuntimeError: Event loop
is closed`. This causes intermittent 500 errors that appear random because cold starts work
but warm starts fail. Connection reuse across invocations is also broken, increasing latency
from repeated connection setup. Module-level clients (aioboto3 sessions, HTTP clients) become
unusable after the first invocation, forcing re-creation on every call and negating all
warm-start performance benefits.

---

### 45. aioboto3 DEFAULT_SESSION Caching Stale Event Loop

**Severity:** HIGH

**Description:**
aioboto3 maintains a global `DEFAULT_SESSION` that caches the event loop from when it was
first created. If the event loop is replaced (e.g., after `asyncio.run()` closes it and a
new one is created), the cached session references the old, closed loop. Operations on the
stale session fail with "Event loop is closed" or "attached to a different event loop".

**BAD Pattern:**

```python
import aioboto3

# WRONG: module-level convenience methods cache the event loop
async def get_trail(trail_id: str) -> dict:
    # Uses aioboto3's DEFAULT_SESSION which may reference a closed event loop
    async with aioboto3.resource("dynamodb") as dynamo:
        table = await dynamo.Table("trails")
        result = await table.get_item(Key={"trail_id": trail_id})
        return result.get("Item")
```

**GOOD Pattern:**

```python
import aioboto3

# CORRECT: always create explicit sessions
session = aioboto3.Session()

async def get_trail(trail_id: str) -> dict:
    # Explicit session, not DEFAULT_SESSION
    async with session.resource("dynamodb") as dynamo:
        table = await dynamo.Table("trails")
        result = await table.get_item(Key={"trail_id": trail_id})
        return result.get("Item")
```

**Detection Approach:**
Grep for `aioboto3.client(` and `aioboto3.resource(` (module-level convenience methods
that use DEFAULT_SESSION). These should be replaced with explicit `aioboto3.Session()`
instances.

**Impact:**
`RuntimeError: Event loop is closed` or `RuntimeError: attached to a different event loop`
on the second and subsequent Lambda invocations. The first invocation succeeds because the
session is fresh. Warm invocations fail intermittently depending on whether the event loop
was replaced.

---

### 50. SIGTERM Not Handled by asyncio.run()

**Severity:** HIGH

**Description:**
`asyncio.run()` installs a handler for SIGINT (Ctrl+C) that cancels the main task, but it
does not handle SIGTERM. AWS Lambda sends SIGTERM during graceful shutdown (Lambda Extensions
API), and container orchestrators (ECS, Kubernetes) use SIGTERM as the standard shutdown
signal. Without a SIGTERM handler, the process is killed abruptly without cleanup.

**BAD Pattern:**

```python
import asyncio

async def main() -> None:
    server = await start_server()
    try:
        await server.serve_forever()
    finally:
        await cleanup_resources()

# WRONG: asyncio.run() only handles SIGINT, not SIGTERM
# Lambda/container SIGTERM kills process without cleanup
asyncio.run(main())
```

**GOOD Pattern:**

```python
import asyncio
import signal

async def main() -> None:
    loop = asyncio.get_running_loop()

    # CORRECT: handle SIGTERM for graceful shutdown
    shutdown_event = asyncio.Event()

    def handle_sigterm() -> None:
        shutdown_event.set()

    loop.add_signal_handler(signal.SIGTERM, handle_sigterm)
    loop.add_signal_handler(signal.SIGINT, handle_sigterm)

    server = await start_server()
    try:
        await shutdown_event.wait()
    finally:
        await server.shutdown()
        await cleanup_resources()

asyncio.run(main())
```

**Detection Approach:**
Grep for `asyncio.run(` in entry points and check whether SIGTERM handlers are registered
via `loop.add_signal_handler(signal.SIGTERM, ...)`. Lambda handler files and container
entry points without SIGTERM handling are vulnerable.

**Impact:**
Abrupt shutdown without cleanup. In-flight requests are dropped, database transactions are
left uncommitted, temporary files are not cleaned up, and connection pools are not drained.
In Lambda, this means the Extension shutdown phase cannot perform cleanup, potentially
losing buffered logs or metrics.

---

## I. FastAPI & Starlette

---

### 11. Sync/Async Function Mismatch

**Severity:** HIGH

**Description:**
In FastAPI, route handlers can be either `async def` (runs on the event loop) or `def`
(runs in a thread pool). Using `def` for a handler that needs to call async code forces
the use of `asyncio.run()` or `loop.run_until_complete()` which either creates a new event
loop or blocks the existing one. Conversely, using `async def` and then calling synchronous
blocking code inside it blocks the event loop.

**BAD Pattern:**

```python
from fastapi import FastAPI

app = FastAPI()

# WRONG: sync handler tries to call async code
@app.get("/trails/{trail_id}")
def get_trail(trail_id: str):
    # Cannot use await here - not an async function
    # Tempting to use asyncio.run() but that creates a new event loop
    import asyncio
    result = asyncio.run(repo.get_trail(trail_id))  # WRONG
    return result

# WRONG: async handler calls sync blocking code
@app.get("/trails")
async def list_trails():
    import requests
    # Blocks the event loop
    response = requests.get("https://external-api.com/trails")
    return response.json()
```

**GOOD Pattern:**

```python
from fastapi import FastAPI

app = FastAPI()

# CORRECT: async handler uses await
@app.get("/trails/{trail_id}")
async def get_trail(trail_id: str):
    result = await repo.get_trail(trail_id)
    return result

# CORRECT: if you must call sync code, use def (FastAPI runs it in threadpool)
@app.get("/trails")
def list_trails():
    import requests
    response = requests.get("https://external-api.com/trails")
    return response.json()

# BETTER: async handler with async HTTP client
@app.get("/trails")
async def list_trails():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://external-api.com/trails")
        return response.json()
```

**Detection Approach:**
Grep for `def\s+\w+` (non-async) route handlers in FastAPI that contain `asyncio.run` or
`loop.run_until_complete`. Also grep for `async def` handlers that import or call `requests`,
`time.sleep`, or other known blocking modules.

**Impact:**
Event loop deadlocks (if `asyncio.run()` is called from within an existing loop) or event
loop blocking (if sync code runs in async handler). FastAPI's automatic thread pool execution
for sync handlers provides a safety net, but only if the handler is correctly declared as
`def` (not `async def`).

---

### 33. BackgroundTasks Blocking the Entire Application

**Severity:** CRITICAL

**Description:**
FastAPI's `BackgroundTasks` runs synchronous functions in the main thread pool (the same
pool used by sync route handlers). If a CPU-bound or blocking sync function is added as a
background task, it occupies a thread pool worker for the duration. Under load, enough
blocking background tasks can exhaust the entire thread pool, preventing sync route handlers
from executing.

**BAD Pattern:**

```python
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()

def generate_report(report_id: str) -> None:
    # CPU-bound: blocks a thread pool worker for minutes
    data = fetch_all_data(report_id)  # Sync blocking I/O
    result = crunch_numbers(data)     # CPU-bound computation
    save_report(result)               # Sync blocking I/O

@app.post("/reports/{report_id}")
async def create_report(report_id: str, background_tasks: BackgroundTasks):
    # WRONG: sync CPU-bound function blocks thread pool worker
    background_tasks.add_task(generate_report, report_id)
    return {"status": "accepted"}
```

**GOOD Pattern:**

```python
import asyncio
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()

async def generate_report(report_id: str) -> None:
    # CORRECT: async function with offloaded CPU work
    data = await fetch_all_data_async(report_id)
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, crunch_numbers, data)
    await save_report_async(result)

@app.post("/reports/{report_id}")
async def create_report(report_id: str, background_tasks: BackgroundTasks):
    # CORRECT: async background task doesn't block thread pool
    background_tasks.add_task(generate_report, report_id)
    return {"status": "accepted"}
```

**Detection Approach:**
Grep for `background_tasks.add_task(` and check whether the target function is `def` (sync)
or `async def`. Sync functions that perform blocking I/O or CPU-bound work are problematic.

**Impact:**
Thread pool exhaustion causes all sync route handlers to queue, leading to request timeouts
across the entire application. The background tasks appear to work in development (low
concurrency) but cause cascading failures under production load.

---

### 34. BackgroundTasks Cannot Be Used with BaseHTTPMiddleware

**Severity:** HIGH

**Description:**
Starlette's `BaseHTTPMiddleware` wraps the response in a way that forces background tasks
to run before the response is sent to the client. The tasks that should run "in the
background" (after response) actually run in the foreground, blocking the response. This
is a known limitation documented in Starlette's issues.

**BAD Pattern:**

```python
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import BackgroundTasks, FastAPI

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        return response

app = FastAPI()
app.add_middleware(LoggingMiddleware)

@app.post("/process")
async def process(background_tasks: BackgroundTasks):
    # WRONG: BackgroundTasks run BEFORE response due to BaseHTTPMiddleware
    background_tasks.add_task(slow_background_work)
    return {"status": "accepted"}  # Client waits for background work to finish
```

**GOOD Pattern:**

```python
from starlette.types import ASGIApp, Receive, Scope, Send
from fastapi import BackgroundTasks, FastAPI

# CORRECT: use pure ASGI middleware instead of BaseHTTPMiddleware
class LoggingMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            # Custom logging logic
            pass
        await self.app(scope, receive, send)

app = FastAPI()
app.add_middleware(LoggingMiddleware)

@app.post("/process")
async def process(background_tasks: BackgroundTasks):
    # CORRECT: BackgroundTasks run after response with pure ASGI middleware
    background_tasks.add_task(slow_background_work)
    return {"status": "accepted"}
```

**Detection Approach:**
Grep for `BaseHTTPMiddleware` in the same codebase as `BackgroundTasks`. If both are used,
the background tasks will not actually run in the background.

**Impact:**
Response latency includes background task duration. If a background task takes 30 seconds,
the client waits 30 seconds for a response that should have been instant. This defeats the
entire purpose of background tasks and can cause client timeouts.

---

### 35. FastAPI Dependency Injection Session Leak Under Concurrency

**Severity:** CRITICAL

**Description:**
FastAPI async generator dependencies (using `yield`) can leak resources under high
concurrency when exceptions prevent the `finally` block from executing. If an exception
occurs after `yield` but the framework fails to close the generator (due to event loop
issues or middleware interference), the session/connection is never returned to the pool.

**BAD Pattern:**

```python
from fastapi import Depends, FastAPI

app = FastAPI()

async def get_db_session():
    session = await create_session()
    yield session
    # WRONG: if exception occurs and generator is not properly closed,
    # session is never released
    await session.close()

@app.get("/trails")
async def list_trails(session=Depends(get_db_session)):
    return await session.execute("SELECT * FROM trails")
```

**GOOD Pattern:**

```python
from fastapi import Depends, FastAPI

app = FastAPI()

async def get_db_session():
    session = await create_session()
    try:
        yield session
    finally:
        # CORRECT: finally block ensures cleanup even on exception
        await session.close()

@app.get("/trails")
async def list_trails(session=Depends(get_db_session)):
    return await session.execute("SELECT * FROM trails")
```

**Detection Approach:**
Grep for `async def.*yield.*session` in dependency functions and verify that the cleanup
code is in a `finally` block, not just after the `yield` statement. The pattern
`yield.*\n.*close\(\)` without `finally:` flags the issue.

**Impact:**
Connection pool exhaustion under high concurrency. Each leaked session occupies a pool slot
permanently. Under sustained load, the pool is exhausted within minutes, causing all
subsequent requests to fail with connection timeout errors.

---

### 36. Sync Dependencies Blocking Thread Pool

**Severity:** CRITICAL

**Description:**
FastAPI runs synchronous dependency generators in the main thread pool. If a sync dependency
performs blocking database calls or I/O, it occupies a thread pool worker for the entire
request lifecycle. Under load, blocking sync dependencies exhaust the thread pool, preventing
other sync operations from executing.

**BAD Pattern:**

```python
from fastapi import Depends, FastAPI
import sqlite3

app = FastAPI()

# WRONG: sync generator with blocking DB call
def get_db():
    conn = sqlite3.connect("trails.db")  # Blocking I/O
    yield conn
    conn.close()

@app.get("/trails")
async def list_trails(db=Depends(get_db)):
    # Async handler, but db dependency blocks a thread
    cursor = db.execute("SELECT * FROM trails")  # Blocking
    return cursor.fetchall()
```

**GOOD Pattern:**

```python
from fastapi import Depends, FastAPI
import aiosqlite

app = FastAPI()

# CORRECT: async generator with async DB operations
async def get_db():
    async with aiosqlite.connect("trails.db") as conn:
        yield conn

@app.get("/trails")
async def list_trails(db=Depends(get_db)):
    cursor = await db.execute("SELECT * FROM trails")
    return await cursor.fetchall()
```

**Detection Approach:**
Grep for sync generator dependencies (`def` with `yield`) that contain blocking calls
(database connections, file I/O, HTTP requests). The pattern `def\s+\w+.*:\s*\n.*yield`
where the function contains blocking operations flags candidates.

**Impact:**
Thread pool exhaustion. The default thread pool has ~40 workers. If each request holds a
thread for 100ms of blocking I/O, maximum throughput is ~400 RPS. At the 1,157 RPS target,
the thread pool is exhausted and requests queue indefinitely.

---

### 37. Mixing Lifespan with on_event Decorators

**Severity:** HIGH

**Description:**
FastAPI (via Starlette) supports two mechanisms for startup/shutdown: the `lifespan`
parameter and `@app.on_event()` decorators. However, if the `lifespan` parameter is
provided, all `on_event` handlers are silently ignored. This can cause critical
initialization code to not run without any error or warning.

**BAD Pattern:**

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_database()
    yield
    # Shutdown
    await close_database()

app = FastAPI(lifespan=lifespan)

# WRONG: this handler is silently ignored because lifespan is provided
@app.on_event("startup")
async def startup_cache():
    await init_cache()  # Never executes!

# WRONG: this handler is also silently ignored
@app.on_event("shutdown")
async def shutdown_cache():
    await close_cache()  # Never executes!
```

**GOOD Pattern:**

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # CORRECT: all startup/shutdown in lifespan
    await init_database()
    await init_cache()
    yield
    await close_cache()
    await close_database()

app = FastAPI(lifespan=lifespan)
# No on_event decorators needed
```

**Detection Approach:**
Grep for both `lifespan` in `FastAPI(` constructor and `on_event(` decorators in the same
application. If both are present, the `on_event` handlers are dead code.

**Impact:**
Silent initialization failure. Critical services (caches, connection pools, background
workers) are never started because their `on_event` handlers are ignored. The application
appears to start normally but fails when it tries to use uninitialized resources.

---

### 38. StreamingResponse Generator Continues After Client Disconnect

**Severity:** HIGH

**Description:**
When a client disconnects during a `StreamingResponse`, the async generator that produces
the response body continues running. FastAPI/Starlette does not automatically cancel the
generator on disconnect. This wastes server resources (CPU, memory, database connections)
generating data that will never be sent.

**BAD Pattern:**

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

async def generate_large_report():
    for page in range(1000):
        # WRONG: continues generating even after client disconnects
        data = await fetch_page(page)  # Expensive DB query
        yield format_csv(data)

@app.get("/reports/export")
async def export_report():
    return StreamingResponse(
        generate_large_report(),
        media_type="text/csv",
    )
```

**GOOD Pattern:**

```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

app = FastAPI()

async def generate_large_report(request: Request):
    for page in range(1000):
        # CORRECT: check for client disconnect
        if await request.is_disconnected():
            return
        data = await fetch_page(page)
        yield format_csv(data)

@app.get("/reports/export")
async def export_report(request: Request):
    return StreamingResponse(
        generate_large_report(request),
        media_type="text/csv",
    )
```

**Detection Approach:**
Grep for `StreamingResponse` and check whether the generator function accepts a `Request`
parameter and calls `request.is_disconnected()`. Generators without disconnect checking
will waste resources after client disconnect.

**Impact:**
Wasted compute resources. A client that starts a large CSV export and then closes the tab
still causes the server to generate and discard the entire report. Under load, multiple
abandoned streams can exhaust database connections and CPU, degrading service for other
users.

---

### 39. Lifespan Partial Startup Failure Without Cleanup

**Severity:** HIGH

**Description:**
In a FastAPI lifespan function, if multiple resources are initialized and the second one
fails, the first resource is never cleaned up because the code never reaches the `yield`
point (and therefore never reaches the shutdown code after `yield`).

**BAD Pattern:**

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # WRONG: if init_cache fails, db connection is leaked
    db = await init_database()
    cache = await init_cache()  # If this fails, db is never closed
    yield
    await cache.close()
    await db.close()

app = FastAPI(lifespan=lifespan)
```

**GOOD Pattern:**

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = await init_database()
    try:
        cache = await init_cache()
        try:
            yield
        finally:
            await cache.close()
    finally:
        # CORRECT: db is always closed, even if cache init fails
        await db.close()

app = FastAPI(lifespan=lifespan)
```

**Detection Approach:**
Grep for `@asynccontextmanager` lifespan functions and check whether resource initialization
before `yield` is wrapped in `try/finally`. Multiple `await init_*()` calls without
try/finally nesting are vulnerable.

**Impact:**
Resource leaks on startup failure. If the second service fails to initialize, the first
service's connection is leaked. Repeated startup attempts (e.g., container restart loop)
accumulate leaked connections until the database connection limit is reached.

---

### 40. BaseHTTPMiddleware Forces Streaming Into Memory

**Severity:** CRITICAL

**Description:**
Starlette's `BaseHTTPMiddleware` reads the entire response body into memory before the
middleware's `dispatch` method returns. This converts `StreamingResponse` and `FileResponse`
into in-memory responses. A streaming endpoint designed to serve a 1GB file will load the
entire file into memory, causing OOM.

**BAD Pattern:**

```python
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)  # Loads entire body into memory!
        duration = time.time() - start
        response.headers["X-Duration"] = str(duration)
        return response

app = FastAPI()
app.add_middleware(TimingMiddleware)

@app.get("/download/{file_id}")
async def download_file(file_id: str):
    # This 1GB file will be loaded entirely into memory by middleware
    return StreamingResponse(stream_file(file_id), media_type="application/octet-stream")
```

**GOOD Pattern:**

```python
from starlette.types import ASGIApp, Receive, Scope, Send
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import time

# CORRECT: pure ASGI middleware preserves streaming
class TimingMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start = time.time()
        first_response = True

        async def timed_send(message):
            nonlocal first_response
            if message["type"] == "http.response.start" and first_response:
                first_response = False
                duration = time.time() - start
                headers = list(message.get("headers", []))
                headers.append((b"x-duration", str(duration).encode()))
                message["headers"] = headers
            await send(message)

        await self.app(scope, receive, timed_send)

app = FastAPI()
app.add_middleware(TimingMiddleware)
```

**Detection Approach:**
Grep for `BaseHTTPMiddleware` in applications that also use `StreamingResponse` or
`FileResponse`. If both are present, streaming responses will be loaded into memory.

**Impact:**
OOM for large responses. A 100MB file download through `BaseHTTPMiddleware` requires 100MB
of RAM per concurrent download. With 10 concurrent downloads, that is 1GB of RAM consumed
just by the middleware buffering. In Lambda with 256MB memory, a single large response
causes an invocation failure.

---

### 41. BaseHTTPMiddleware Request Body Consumed

**Severity:** HIGH

**Description:**
When middleware reads the request body via `await request.body()`, it consumes the ASGI
`receive` channel. The body is cached in the `Request` object, but downstream code that
tries to read the body via the raw `receive` callable will get nothing. This can break
WebSocket upgrades and chunked transfer encoding.

**BAD Pattern:**

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class BodyLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # WRONG: consumes the body, may break downstream
        body = await request.body()
        log_info(f"Request body size: {len(body)}")
        response = await call_next(request)
        return response
```

**GOOD Pattern:**

```python
from starlette.types import ASGIApp, Receive, Scope, Send

class BodyLoggingMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # CORRECT: intercept receive to peek at body without consuming
        body_parts: list[bytes] = []
        body_complete = False

        async def logging_receive():
            nonlocal body_complete
            message = await receive()
            if message["type"] == "http.request":
                body_parts.append(message.get("body", b""))
                if not message.get("more_body", False):
                    body_complete = True
                    total = sum(len(p) for p in body_parts)
                    log_info(f"Request body size: {total}")
            return message

        await self.app(scope, logging_receive, send)
```

**Detection Approach:**
Grep for `await request.body()` or `await request.json()` inside middleware classes. Body
consumption in middleware can break downstream request processing.

**Impact:**
Downstream route handlers receive empty bodies, causing deserialization errors or missing
data. This is particularly insidious because it only manifests when the middleware is active
and can appear as intermittent failures if only some requests go through the middleware path.

---

### 42. CORS Middleware Order Causing Preflight Failures

**Severity:** HIGH

**Description:**
Starlette middleware is executed in reverse order of how it is added (last added = first
to execute). `CORSMiddleware` must be the outermost middleware (first to execute) so it can
handle OPTIONS preflight requests before other middleware processes them. If another
middleware runs before CORS, it may reject the preflight request.

**BAD Pattern:**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# WRONG: CORSMiddleware added first, executes last
app.add_middleware(CORSMiddleware, allow_origins=["https://example.com"])
app.add_middleware(AuthMiddleware)  # Runs before CORS, rejects OPTIONS requests
```

**GOOD Pattern:**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORRECT: CORSMiddleware added last, executes first
app.add_middleware(AuthMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=["https://example.com"])
```

**Detection Approach:**
Grep for `add_middleware(CORSMiddleware` and check whether it is the last `add_middleware`
call. If other middleware is added after CORS, those middleware will execute before CORS and
may reject preflight requests.

**Impact:**
CORS preflight failures. Browsers send OPTIONS requests before cross-origin API calls. If
AuthMiddleware runs first and rejects the OPTIONS request (no auth token), the browser
blocks the actual API call. This manifests as "CORS error" in the browser console and
breaks all cross-origin API communication.

---

## J. aioboto3 & AWS SDK

---

### 43. aiobotocore Synchronous SSL/Filesystem Calls

**Severity:** HIGH

**Description:**
aiobotocore (the foundation of aioboto3) internally performs synchronous operations for SSL
context creation, certificate loading, and filesystem access (reading AWS config files).
These synchronous calls block the event loop thread. This is a known limitation documented
in aiobotocore issue #1023 -- the library is "mostly async" but certain initialization
paths are synchronous.

**BAD Pattern:**

```python
import aioboto3

# The session creation itself may trigger sync filesystem reads
# (reading ~/.aws/config, ~/.aws/credentials)
session = aioboto3.Session()

async def handler():
    # First call may block event loop during SSL context initialization
    async with session.client("dynamodb") as client:
        # Subsequent calls reuse SSL context, less blocking
        await client.get_item(TableName="trails", Key={"id": {"S": "trail-1"}})
```

**GOOD Pattern:**

```python
import aioboto3
import asyncio

session = aioboto3.Session()

# CORRECT: initialize clients at startup (cold start) when blocking is acceptable
# This moves the sync SSL/config overhead to initialization
_dynamodb_initialized = False

async def ensure_clients():
    global _dynamodb_initialized
    if not _dynamodb_initialized:
        # Force SSL context creation during initialization
        async with session.client("dynamodb") as client:
            await client.describe_endpoints()
        _dynamodb_initialized = True

async def handler():
    await ensure_clients()
    async with session.client("dynamodb") as client:
        await client.get_item(TableName="trails", Key={"id": {"S": "trail-1"}})
```

**Detection Approach:**
This is a known library limitation and cannot be detected by grep alone. Document it as a
known issue and mitigate by performing initial client creation during startup/cold start
when event loop blocking is acceptable.

**Impact:**
Occasional event loop stalls during SSL context creation (tens to hundreds of milliseconds).
Most noticeable on cold starts or when new client types are first used. Under steady-state
operation, SSL contexts are cached and the impact is minimal.

---

### 44. aioboto3 S3 Streaming API Breaking Change

**Severity:** HIGH

**Description:**
After aioboto3 v9.6.0, the S3 response body streaming API changed. Calling
`stream.read(chunk_size)` directly throws `TypeError`. Instead, you must use
`stream.content.read(chunk_size)` or iterate the stream. This is a breaking change that
is not well-documented and causes runtime errors in code that worked with earlier versions.

**BAD Pattern:**

```python
import aioboto3

session = aioboto3.Session()

async def download_file(bucket: str, key: str) -> bytes:
    async with session.client("s3") as s3:
        response = await s3.get_object(Bucket=bucket, Key=key)
        stream = response["Body"]
        # WRONG: throws TypeError in aioboto3 >= 9.6.0
        data = await stream.read(4096)
        return data
```

**GOOD Pattern:**

```python
import aioboto3

session = aioboto3.Session()

async def download_file(bucket: str, key: str) -> bytes:
    async with session.client("s3") as s3:
        response = await s3.get_object(Bucket=bucket, Key=key)
        stream = response["Body"]
        # CORRECT: use .content.read() for chunked reading
        chunks: list[bytes] = []
        async with stream as body:
            async for chunk in body:
                chunks.append(chunk)
        return b"".join(chunks)

# ALTERNATIVE: read entire body
async def download_file_simple(bucket: str, key: str) -> bytes:
    async with session.client("s3") as s3:
        response = await s3.get_object(Bucket=bucket, Key=key)
        async with response["Body"] as stream:
            return await stream.read()
```

**Detection Approach:**
Grep for `.read(\d+)` on S3 body objects. The pattern `response.*Body.*\.read\(\d+\)`
flags potential breaking API usage.

**Impact:**
`TypeError` at runtime when reading S3 objects. This breaks file downloads, asset serving,
and any S3 streaming operations. The error only occurs at runtime and may not be caught
by tests that mock S3.

---

### 46. aioboto3 Connection Pool Hang on High-Volume S3

**Severity:** HIGH

**Description:**
When thousands of concurrent S3 operations (put_object, get_object) are launched without
concurrency limits, the underlying aiohttp connection pool is exhausted. New requests queue
for available connections, and with enough queued requests, the entire application hangs.
The default connection pool limit in aiobotocore is 10 connections per endpoint.

**BAD Pattern:**

```python
import aioboto3
import asyncio

session = aioboto3.Session()

async def upload_all(files: list[tuple[str, bytes]]) -> None:
    async with session.client("s3") as s3:
        # WRONG: thousands of concurrent uploads exhaust connection pool
        await asyncio.gather(*[
            s3.put_object(Bucket="assets", Key=key, Body=data)
            for key, data in files
        ])
```

**GOOD Pattern:**

```python
import aioboto3
import asyncio

session = aioboto3.Session()

async def upload_all(files: list[tuple[str, bytes]]) -> None:
    # CORRECT: limit concurrency to connection pool size
    semaphore = asyncio.Semaphore(50)

    async def upload_one(s3_client, key: str, data: bytes) -> None:
        async with semaphore:
            await s3_client.put_object(Bucket="assets", Key=key, Body=data)

    async with session.client("s3") as s3:
        await asyncio.gather(*[
            upload_one(s3, key, data) for key, data in files
        ])
```

**Detection Approach:**
Grep for concurrent `put_object` or `get_object` calls inside `asyncio.gather` without
a semaphore. The pattern `gather\(\*\[.*put_object\|get_object` flags unbounded S3
concurrency.

**Impact:**
Application hang. All requests queue for S3 connections, and the event loop appears frozen.
No error is raised -- the application simply stops processing. In Lambda, this burns
execution time until timeout. Recovery requires restarting the process.

---

### 47. aioboto3 batch_writer UnprocessedItems Not Retried

**Severity:** MEDIUM

**Description:**
When using the low-level `batch_write_item()` API (not the `Table.batch_writer()` context
manager), DynamoDB may return `UnprocessedItems` if some writes were throttled. The
low-level API does not automatically retry these items -- they are silently dropped unless
the caller explicitly handles them. The high-level `Table.batch_writer()` handles retries
automatically.

**BAD Pattern:**

```python
import aioboto3

session = aioboto3.Session()

async def bulk_write(items: list[dict]) -> None:
    async with session.client("dynamodb") as client:
        # WRONG: UnprocessedItems silently dropped
        response = await client.batch_write_item(
            RequestItems={
                "trails": [
                    {"PutRequest": {"Item": item}} for item in items
                ]
            }
        )
        # response may contain UnprocessedItems but we ignore them
```

**GOOD Pattern:**

```python
import aioboto3
import asyncio

session = aioboto3.Session()

async def bulk_write(items: list[dict]) -> None:
    async with session.resource("dynamodb") as dynamo:
        table = await dynamo.Table("trails")
        # CORRECT: batch_writer handles retries automatically
        async with table.batch_writer() as writer:
            for item in items:
                await writer.put_item(Item=item)

# ALTERNATIVE: manual retry for low-level API
async def bulk_write_with_retry(items: list[dict]) -> None:
    async with session.client("dynamodb") as client:
        request_items = {
            "trails": [
                {"PutRequest": {"Item": item}} for item in items
            ]
        }

        while request_items:
            response = await client.batch_write_item(RequestItems=request_items)
            request_items = response.get("UnprocessedItems", {})
            if request_items:
                # CORRECT: exponential backoff before retry
                await asyncio.sleep(0.5)
```

**Detection Approach:**
Grep for `batch_write_item(` and check whether `UnprocessedItems` is handled in the
response. The absence of `UnprocessedItems` processing after `batch_write_item` flags
potential silent data loss.

**Impact:**
Silent data loss. Under DynamoDB throttling, items are dropped without error. The caller
believes all items were written successfully. This is especially dangerous during bulk
imports or data migrations where thousands of items are written.

---

## K. TaskGroup & ExceptionGroup

---

### 21. TaskGroup Used Without async with Context Manager

**Severity:** CRITICAL

**Description:**
`asyncio.TaskGroup` must be used as an async context manager (`async with`). Creating a
`TaskGroup` without `async with` means the group's `__aenter__` and `__aexit__` methods
are never called, so task scheduling, exception propagation, and cleanup never happen.
Tasks created via `tg.create_task()` outside the context manager may not be properly
managed.

**BAD Pattern:**

```python
import asyncio

async def process_all(items: list[dict]) -> None:
    # WRONG: TaskGroup not used as context manager
    tg = asyncio.TaskGroup()
    for item in items:
        tg.create_task(process(item))
    # Tasks are not properly managed - no waiting, no exception handling
```

**GOOD Pattern:**

```python
import asyncio

async def process_all(items: list[dict]) -> None:
    # CORRECT: async with ensures proper task management
    async with asyncio.TaskGroup() as tg:
        for item in items:
            tg.create_task(process(item))
    # All tasks are complete when we reach this point
    # If any task failed, ExceptionGroup was raised
```

**Detection Approach:**
Grep for `TaskGroup()` and verify it is used with `async with`. The pattern
`=\s*asyncio\.TaskGroup\(\)` without `async with` on the same line flags misuse.

**Impact:**
Tasks may not execute or may execute without proper supervision. Exceptions are not
collected into an ExceptionGroup, so errors from individual tasks are lost. The TaskGroup
provides no value without the context manager -- it is equivalent to fire-and-forget tasks
with extra overhead.

---

### 22. Accessing TaskGroup create_task Result Before Block Exits

**Severity:** HIGH

**Description:**
Inside an `async with asyncio.TaskGroup() as tg:` block, tasks created with
`tg.create_task()` are scheduled but may not be complete. Calling `.result()` on a task
inside the block raises `InvalidStateError` if the task has not finished yet. Task results
are only safely accessible after the `async with` block exits, which guarantees all tasks
have completed.

**BAD Pattern:**

```python
import asyncio

async def fetch_all(urls: list[str]) -> list[dict]:
    results = []
    async with asyncio.TaskGroup() as tg:
        for url in urls:
            task = tg.create_task(fetch(url))
            # WRONG: task may not be done yet
            results.append(task.result())  # Raises InvalidStateError
    return results
```

**GOOD Pattern:**

```python
import asyncio

async def fetch_all(urls: list[str]) -> list[dict]:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch(url)) for url in urls]

    # CORRECT: access results after the block exits (all tasks complete)
    return [task.result() for task in tasks]
```

**Detection Approach:**
Grep for `.result()` inside `async with asyncio.TaskGroup()` blocks. Results should only
be accessed after the block exits. The pattern `tg\.create_task.*\.result\(\)` in the
same block scope flags premature result access.

**Impact:**
`asyncio.InvalidStateError: Result is not set` at runtime. The error occurs nondeterministically
depending on task completion timing. Fast tasks may complete before `.result()` is called
(passing in development), while slower tasks fail in production.

---

## L. Context Variables

---

### 30. Context Variables Lost in run_in_executor

**Severity:** HIGH

**Description:**
`contextvars` are automatically propagated to tasks created with `asyncio.create_task()` and
`asyncio.to_thread()`, but they are NOT propagated when using `loop.run_in_executor()`.
Thread pool workers started via `run_in_executor` do not receive the caller's context,
so `ContextVar` values (such as correlation IDs, request IDs, or user context) are lost.

**BAD Pattern:**

```python
import asyncio
import contextvars

request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("request_id")

def sync_work() -> str:
    # WRONG: request_id_var is not set in executor thread
    rid = request_id_var.get("unknown")  # Always returns "unknown"
    return f"Processed by request {rid}"

async def handler(request_id: str) -> str:
    request_id_var.set(request_id)
    loop = asyncio.get_running_loop()
    # WRONG: context not propagated to executor
    result = await loop.run_in_executor(None, sync_work)
    return result
```

**GOOD Pattern:**

```python
import asyncio
import contextvars

request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("request_id")

def sync_work() -> str:
    rid = request_id_var.get("unknown")
    return f"Processed by request {rid}"

async def handler(request_id: str) -> str:
    request_id_var.set(request_id)

    # OPTION 1: Copy context manually
    loop = asyncio.get_running_loop()
    ctx = contextvars.copy_context()
    result = await loop.run_in_executor(None, ctx.run, sync_work)
    return result

    # OPTION 2: Use asyncio.to_thread (propagates context automatically)
    # result = await asyncio.to_thread(sync_work)
    # return result
```

**Detection Approach:**
Grep for `run_in_executor(` and check whether the called function uses `ContextVar`. If so,
verify that `contextvars.copy_context()` is used, or suggest switching to
`asyncio.to_thread()` which propagates context automatically.

**Impact:**
Lost correlation IDs in logs, missing request context in monitoring, incorrect user context
in authorization checks. In a structured logging system, logs from executor threads lack
the correlation ID, making request tracing impossible.

---

### 31. Context Variable Changes in Threads Not Propagated Back

**Severity:** HIGH

**Description:**
When `asyncio.to_thread()` or `run_in_executor` with `copy_context()` is used, the context
is copied to the thread. Any changes to `ContextVar` values made inside the thread are
isolated to that copy and are NOT propagated back to the calling coroutine. This is by
design (contexts are copy-on-write), but developers often expect changes to be visible
in the caller.

**BAD Pattern:**

```python
import asyncio
import contextvars

result_var: contextvars.ContextVar[str] = contextvars.ContextVar("result")

def compute_in_thread() -> None:
    result = expensive_computation()
    # WRONG: this change is not visible to the caller
    result_var.set(result)

async def handler() -> str:
    await asyncio.to_thread(compute_in_thread)
    # WRONG: result_var still has its pre-thread value
    return result_var.get("default")  # Returns "default", not the computed result
```

**GOOD Pattern:**

```python
import asyncio
import contextvars

result_var: contextvars.ContextVar[str] = contextvars.ContextVar("result")

def compute_in_thread() -> str:
    # CORRECT: return the result instead of setting a ContextVar
    return expensive_computation()

async def handler() -> str:
    result = await asyncio.to_thread(compute_in_thread)
    # CORRECT: use the return value
    result_var.set(result)  # Set in caller's context if needed
    return result
```

**Detection Approach:**
This requires design-level review. Grep for `ContextVar` usage inside functions passed to
`asyncio.to_thread()` or `run_in_executor()`. If `ContextVar.set()` is called inside the
thread function and the caller reads the variable afterward, the pattern is incorrect.

**Impact:**
Silent data loss. The caller reads stale values from ContextVars that were "updated" in the
thread. This is particularly dangerous for request-scoped context (user ID, permissions,
locale) where stale values can lead to authorization bugs or incorrect behavior.

---

### 32. Starlette Middleware contextvars Inconsistency

**Severity:** HIGH

**Description:**
Starlette middleware layers execute in separate task contexts. Changes to `ContextVar`
values in one middleware may not be visible in route handlers or other middleware if they
run as separate tasks. This is particularly problematic with `BaseHTTPMiddleware` which
wraps the downstream application in a new context.

**BAD Pattern:**

```python
import contextvars
from starlette.middleware.base import BaseHTTPMiddleware

request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("request_id")

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id_var.set(request.headers.get("X-Request-ID", "unknown"))
        response = await call_next(request)
        return response

# In route handler:
async def handler():
    # WRONG: may not see the ContextVar set by middleware
    # BaseHTTPMiddleware may run handler in a different task context
    rid = request_id_var.get("default")
```

**GOOD Pattern:**

```python
import contextvars
from starlette.types import ASGIApp, Receive, Scope, Send

request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("request_id")

# CORRECT: use pure ASGI middleware for consistent context propagation
class RequestIdMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            headers = dict(scope.get("headers", []))
            request_id = headers.get(b"x-request-id", b"unknown").decode()
            request_id_var.set(request_id)
        await self.app(scope, receive, send)

# ALTERNATIVE: use request.state instead of ContextVar for per-request data
class RequestIdMiddlewareAlt:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            scope["state"] = scope.get("state", {})
            scope["state"]["request_id"] = "from-header"
        await self.app(scope, receive, send)
```

**Detection Approach:**
Grep for `ContextVar` usage in middleware classes, especially `BaseHTTPMiddleware` subclasses.
Verify that the ContextVar values are accessible in route handlers by checking whether the
middleware and handlers share the same task context.

**Impact:**
Lost request context (correlation IDs, user identity, locale). Logs lack request tracing
information, monitoring misattributes errors, and authorization decisions may use incorrect
context. This is a common source of "works in testing, fails in production" bugs.

---

## M. Signal & Thread Safety

---

### 51. Signal Handler Lambda Late Binding

**Severity:** MEDIUM

**Description:**
When registering signal handlers in a loop using `lambda`, Python's late binding means all
lambdas reference the variable from the last iteration. This is a general Python closure
issue, but it commonly appears in asyncio signal handler registration.

**BAD Pattern:**

```python
import asyncio
import signal

async def setup_signals():
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
        # WRONG: all lambdas reference the last value of sig (SIGHUP)
        loop.add_signal_handler(sig, lambda: handle_signal(sig))
```

**GOOD Pattern:**

```python
import asyncio
import signal

async def setup_signals():
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
        # CORRECT: default argument captures current value of sig
        loop.add_signal_handler(sig, lambda s=sig: handle_signal(s))

    # BETTER: use functools.partial
    # from functools import partial
    # for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
    #     loop.add_signal_handler(sig, partial(handle_signal, sig))
```

**Detection Approach:**
Grep for `add_signal_handler(.*lambda` and check whether the lambda captures loop variables
without default argument binding. The pattern `lambda:.*\bsig\b` (referencing a loop
variable without default) flags the issue.

**Impact:**
All signals trigger the same handler with the wrong signal number. SIGTERM handler runs
SIGHUP logic, SIGINT handler runs SIGHUP logic. This causes incorrect shutdown behavior
and can prevent graceful shutdown.

---

### 52. Default Thread Pool Shared Between DNS and run_in_executor

**Severity:** HIGH

**Description:**
asyncio's default `ThreadPoolExecutor` is shared between `loop.getaddrinfo()` (DNS),
`loop.run_in_executor(None, ...)`, and `asyncio.to_thread()`. If application code submits
many blocking tasks to the default executor, DNS resolution for all HTTP clients (aiohttp,
httpx, aiobotocore) queues behind the application tasks. This can cause DNS timeouts even
though the DNS server is responsive.

**BAD Pattern:**

```python
import asyncio

async def process_batch(items: list[dict]) -> None:
    loop = asyncio.get_running_loop()
    # WRONG: floods default executor with 1000 tasks
    # DNS resolution for HTTP clients queues behind these
    await asyncio.gather(*[
        loop.run_in_executor(None, cpu_bound_work, item)
        for item in items
    ])
```

**GOOD Pattern:**

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

# CORRECT: dedicated executor for application work
_app_executor = ThreadPoolExecutor(max_workers=16, thread_name_prefix="app-worker")

async def process_batch(items: list[dict]) -> None:
    loop = asyncio.get_running_loop()
    # Application tasks use dedicated executor, leaving default free for DNS
    await asyncio.gather(*[
        loop.run_in_executor(_app_executor, cpu_bound_work, item)
        for item in items
    ])
```

**Detection Approach:**
Grep for `run_in_executor(None,` (using default executor) used heavily. If dozens or
hundreds of concurrent calls use the default executor, DNS resolution may be starved.

**Impact:**
DNS resolution failures and timeouts for HTTP clients. All outbound HTTP connections
(to DynamoDB, S3, external APIs) fail because DNS lookups queue behind application
executor tasks. This appears as random connection timeouts that are difficult to diagnose.

---

### 53. asyncio.to_thread() contextvars Performance Overhead

**Severity:** MEDIUM

**Description:**
`asyncio.to_thread()` copies the entire `contextvars.Context` for every call. In hot paths
where `to_thread()` is called thousands of times per second, the context copy overhead
becomes measurable. Each copy duplicates all ContextVar values, and with many ContextVars
(logging context, request context, tracing spans), this adds microseconds per call.

**BAD Pattern:**

```python
import asyncio

async def process_items(items: list[dict]) -> list[dict]:
    results = []
    for item in items:
        # WRONG: copies entire context for each of 10,000 items
        result = await asyncio.to_thread(transform, item)
        results.append(result)
    return results
```

**GOOD Pattern:**

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

_executor = ThreadPoolExecutor(max_workers=8)

async def process_items(items: list[dict]) -> list[dict]:
    loop = asyncio.get_running_loop()

    # OPTION 1: use run_in_executor (no context copy) if context not needed
    results = await asyncio.gather(*[
        loop.run_in_executor(_executor, transform, item)
        for item in items
    ])
    return results

    # OPTION 2: batch items to reduce context copies
    # batch_results = await asyncio.to_thread(transform_batch, items)
    # return batch_results
```

**Detection Approach:**
Grep for `asyncio.to_thread(` in loops or high-frequency code paths. If `to_thread` is
called thousands of times per second and context propagation is not needed, switching to
`run_in_executor` avoids the overhead.

**Impact:**
Measurable overhead (microseconds per call) at high frequency. For 10,000 calls per second,
this adds tens of milliseconds of total overhead. The impact is minor for most applications
but relevant for high-throughput Lambda handlers processing large batches.

---

### 55. QueueListener Not Started or Stopped

**Severity:** MEDIUM

**Description:**
Python's `logging.handlers.QueueListener` must be explicitly started with `.start()` and
stopped with `.stop()`. Forgetting to start it means log messages accumulate in the queue
and are never processed. Forgetting to stop it means the final batch of log messages is
lost when the process exits.

**BAD Pattern:**

```python
import logging
from logging.handlers import QueueHandler, QueueListener
from queue import Queue

log_queue: Queue = Queue()
queue_handler = QueueHandler(log_queue)
file_handler = logging.FileHandler("/var/log/app.log")
listener = QueueListener(log_queue, file_handler)

# WRONG: listener.start() never called - logs accumulate in queue forever

logger = logging.getLogger("app")
logger.addHandler(queue_handler)
logger.info("This message is queued but never written to disk")
```

**GOOD Pattern:**

```python
import logging
import atexit
from logging.handlers import QueueHandler, QueueListener
from queue import Queue

log_queue: Queue = Queue(maxsize=10000)
queue_handler = QueueHandler(log_queue)
file_handler = logging.FileHandler("/var/log/app.log")
listener = QueueListener(log_queue, file_handler, respect_handler_level=True)

# CORRECT: start the listener
listener.start()

# CORRECT: ensure stop on exit to flush final messages
atexit.register(listener.stop)

logger = logging.getLogger("app")
logger.addHandler(queue_handler)
```

**Detection Approach:**
Grep for `QueueListener(` and verify that `.start()` is called on the instance. Also check
for `.stop()` in shutdown/cleanup code or registered with `atexit`.

**Impact:**
Missing `.start()`: all log messages are lost -- they queue indefinitely and are never
written. Missing `.stop()`: the last batch of messages (potentially including error context
for a crash) is lost on process exit.

---

### 59. uvloop Scheduling/Timing Behavioral Differences

**Severity:** MEDIUM

**Description:**
`uvloop` (a popular high-performance event loop for asyncio based on libuv) has subtly
different scheduling and timing behavior compared to the default asyncio event loop.
Specifically, the order of callback execution and the granularity of timer scheduling
can differ. Code that depends on specific callback ordering or sub-millisecond timing
may behave differently under uvloop.

**BAD Pattern:**

```python
import uvloop
import asyncio

# Code that depends on specific callback ordering
async def timing_sensitive():
    event = asyncio.Event()
    result = []

    async def task_a():
        await asyncio.sleep(0)
        result.append("a")

    async def task_b():
        await asyncio.sleep(0)
        result.append("b")

    # WRONG: assumes a runs before b, but uvloop may schedule differently
    asyncio.create_task(task_a())
    asyncio.create_task(task_b())
    await asyncio.sleep(0.001)
    assert result == ["a", "b"]  # May fail under uvloop
```

**GOOD Pattern:**

```python
import asyncio

async def timing_independent():
    result = []

    async def task_a():
        await asyncio.sleep(0)
        result.append("a")

    async def task_b():
        await asyncio.sleep(0)
        result.append("b")

    # CORRECT: do not depend on execution order
    await asyncio.gather(task_a(), task_b())
    # Assert both ran, not their order
    assert set(result) == {"a", "b"}
```

**Detection Approach:**
Grep for `uvloop` in requirements files or code. If present, review tests for assertions
that depend on specific callback ordering or precise timing.

**Impact:**
Tests pass with default event loop but fail with uvloop, or vice versa. In production,
timing-dependent code produces incorrect results intermittently. This is particularly
relevant when switching from development (default loop) to production (uvloop).

---

### 60. Async Fixtures and Tests in Different Event Loops

**Severity:** HIGH

**Description:**
When using `pytest-asyncio`, fixtures and tests may run on different event loops depending
on fixture scope. A `session`-scoped fixture runs on a different loop than a `function`-scoped
test by default. Sharing asyncio objects (locks, events, tasks) between different loops
causes `RuntimeError: attached to a different loop`.

**BAD Pattern:**

```python
import pytest
import pytest_asyncio
import asyncio

@pytest_asyncio.fixture(scope="session")
async def shared_lock():
    # Created on session-scoped event loop
    return asyncio.Lock()

@pytest.mark.asyncio
async def test_with_lock(shared_lock):
    # WRONG: runs on function-scoped event loop
    # shared_lock was created on a different loop
    async with shared_lock:  # RuntimeError: attached to a different loop
        pass
```

**GOOD Pattern:**

```python
import pytest
import pytest_asyncio
import asyncio

# OPTION 1: Match fixture scope to test scope
@pytest_asyncio.fixture(scope="function")
async def lock():
    return asyncio.Lock()

@pytest.mark.asyncio
async def test_with_lock(lock):
    async with lock:
        pass

# OPTION 2: Use pytest-asyncio loop_scope configuration
# In pyproject.toml:
# [tool.pytest.ini_options]
# asyncio_mode = "auto"
```

**Detection Approach:**
Grep for `@pytest_asyncio.fixture(scope=` and check whether the scope is wider than
`function`. Session or class-scoped async fixtures that create asyncio objects are
problematic.

**Impact:**
`RuntimeError` in tests. Async fixtures with wider scope than the test create objects on
a different event loop. This causes confusing test failures that are difficult to debug
because the error message ("attached to a different loop") does not indicate a scope mismatch.

---

### 61. pytest-asyncio Event Loop Closed Prematurely

**Severity:** HIGH

**Description:**
In pytest-asyncio v0.23+, a bug causes the event loop to be closed prematurely when async
generator fixtures with wider scope (e.g., `scope="class"`) are used. The loop is closed
before the fixture's cleanup code runs, causing `RuntimeError: Event loop is closed` during
teardown.

**BAD Pattern:**

```python
import pytest_asyncio

@pytest_asyncio.fixture(scope="class")
async def db_session():
    session = await create_db_session()
    yield session
    # WRONG: event loop may be closed before this runs in pytest-asyncio 0.23+
    await session.close()  # RuntimeError: Event loop is closed
```

**GOOD Pattern:**

```python
import pytest_asyncio

@pytest_asyncio.fixture(scope="function")
async def db_session():
    session = await create_db_session()
    yield session
    # CORRECT: function-scoped fixtures don't have premature loop closure
    await session.close()

# ALTERNATIVE: use sync cleanup that doesn't need event loop
@pytest_asyncio.fixture(scope="class")
async def db_session():
    session = await create_db_session()
    yield session
    # Sync cleanup as fallback
    session.close_sync()
```

**Detection Approach:**
Grep for `@pytest_asyncio.fixture` with `scope="class"` or `scope="session"` that contain
async cleanup code after `yield`. Check the pytest-asyncio version -- v0.23+ has this bug.

**Impact:**
Test suite failures during fixture cleanup. The tests themselves pass, but teardown fails,
leaving resources uncleaned (database connections, temporary files). This can cause
subsequent test failures due to resource leaks or state contamination.

---

### 70. Event Loop Policy Deprecated in Python 3.14

**Severity:** HIGH

**Description:**
Python 3.14 deprecates `asyncio.set_event_loop_policy()` and
`asyncio.get_event_loop_policy()`. These will be removed in Python 3.16. Code that uses
custom event loop policies (e.g., for uvloop or Windows ProactorEventLoop) must migrate
to the new `loop_factory` parameter of `asyncio.run()`.

**BAD Pattern:**

```python
import asyncio
import uvloop

# WRONG: deprecated in Python 3.14, removed in 3.16
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
asyncio.run(main())
```

**GOOD Pattern:**

```python
import asyncio
import uvloop

# CORRECT: use loop_factory parameter (Python 3.12+)
asyncio.run(main(), loop_factory=uvloop.new_event_loop)
```

**Detection Approach:**
Grep for `set_event_loop_policy(` and `get_event_loop_policy(`. These are deprecated and
should be replaced with `loop_factory` parameter to `asyncio.run()`.

**Impact:**
`DeprecationWarning` in Python 3.14, `RuntimeError` in Python 3.16+. Code that uses custom
event loop policies will break completely when upgrading to Python 3.16.

---

### 71. get_event_loop() Raises RuntimeError in 3.14

**Severity:** HIGH

**Description:**
In Python 3.14, `asyncio.get_event_loop()` raises `RuntimeError` when called outside of
an async context (when no event loop is running). In earlier versions, it would implicitly
create a new event loop. This breaking change affects code that calls `get_event_loop()`
in module-level initialization or synchronous functions.

**BAD Pattern:**

```python
import asyncio

# WRONG: in Python 3.14, this raises RuntimeError at module level
loop = asyncio.get_event_loop()
loop.run_until_complete(init_resources())
```

**GOOD Pattern:**

```python
import asyncio

# CORRECT: use asyncio.run() which manages the loop lifecycle
asyncio.run(init_resources())

# CORRECT: inside async context, use get_running_loop()
async def setup():
    loop = asyncio.get_running_loop()
    # Use loop as needed
```

**Detection Approach:**
Grep for `asyncio.get_event_loop()` outside of `async def` functions. Module-level calls
and calls in synchronous functions are problematic in Python 3.14+.

**Impact:**
`RuntimeError: no current event loop` at module import time or during synchronous function
execution. This is a breaking change that prevents the application from starting. It
commonly affects legacy code that was written for Python 3.6-3.9.

---

### 72. Subprocess wait() Deadlock on Full Pipe

**Severity:** HIGH

**Description:**
Using `await process.wait()` with `stdout=asyncio.subprocess.PIPE` or
`stderr=asyncio.subprocess.PIPE` can deadlock if the subprocess generates enough output to
fill the OS pipe buffer (typically 64KB). The subprocess blocks waiting to write to the full
pipe, while the parent blocks in `wait()` without reading from the pipe.

**BAD Pattern:**

```python
import asyncio

async def run_command(cmd: list[str]) -> int:
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # WRONG: deadlocks if subprocess outputs > 64KB
    await process.wait()
    stdout = await process.stdout.read()
    return process.returncode
```

**GOOD Pattern:**

```python
import asyncio

async def run_command(cmd: list[str]) -> tuple[int, str, str]:
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # CORRECT: communicate() reads stdout/stderr while waiting
    stdout, stderr = await process.communicate()
    return process.returncode, stdout.decode(), stderr.decode()
```

**Detection Approach:**
Grep for `await.*process.wait()` in code that also uses `stdout=.*PIPE` or
`stderr=.*PIPE`. The combination of `wait()` with piped output is the deadlock condition.
`communicate()` should be used instead.

**Impact:**
Deadlock. The subprocess and parent process both block indefinitely. In Lambda, this burns
execution time until timeout. The deadlock only occurs when the subprocess produces enough
output, making it timing-dependent and hard to reproduce in development.

---

### 73. WebSocket Client Set Growing Unbounded

**Severity:** HIGH

**Description:**
When tracking connected WebSocket clients in a set, clients that disconnect due to errors
or network issues may not be removed if the removal code is not in a `finally` block. Over
time, the set grows with stale references, causing memory leaks and failed broadcast attempts.

**BAD Pattern:**

```python
import asyncio
from fastapi import FastAPI, WebSocket

app = FastAPI()
connected_clients: set[WebSocket] = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)

    # WRONG: if receive() raises, websocket is never removed from set
    while True:
        data = await websocket.receive_text()
        await broadcast(data)

    connected_clients.discard(websocket)  # Never reached on error
```

**GOOD Pattern:**

```python
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()
connected_clients: set[WebSocket] = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await broadcast(data)
    except WebSocketDisconnect:
        pass
    finally:
        # CORRECT: always remove from set, even on error
        connected_clients.discard(websocket)
```

**Detection Approach:**
Grep for `connected_clients.add(` or similar patterns and verify that the corresponding
removal is in a `finally` block. The pattern `\.add\(.*websocket` without removal in
`finally` flags the issue.

**Impact:**
Memory leak from stale WebSocket references. Broadcast operations attempt to send to
disconnected clients, causing additional errors. The client set grows unbounded, eventually
consuming significant memory and slowing broadcast operations.

---

### 74. WebSocket Send Buffering on Disconnect Causing OOM

**Severity:** HIGH

**Description:**
When a WebSocket client disconnects abruptly (without clean close), `send()` calls do not
immediately raise an error. Instead, data is buffered in the send queue. If the server
continues sending data to a disconnected client without detecting the disconnect, the buffer
grows until OOM.

**BAD Pattern:**

```python
async def stream_updates(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await get_next_update()
        # WRONG: if client disconnected, this buffers data until OOM
        await websocket.send_json(data)
```

**GOOD Pattern:**

```python
import asyncio
from fastapi import WebSocket

async def stream_updates(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await get_next_update()
            # CORRECT: use timeout to detect stuck sends
            try:
                await asyncio.wait_for(
                    websocket.send_json(data),
                    timeout=5.0,
                )
            except asyncio.TimeoutError:
                break  # Client likely disconnected
    except Exception:
        pass
    finally:
        try:
            await websocket.close()
        except Exception:
            pass
```

**Detection Approach:**
Grep for `websocket.send` in loops without timeout or heartbeat mechanisms. Continuous
sending without disconnect detection is the vulnerability.

**Impact:**
OOM from unbounded send buffer growth. A single disconnected client can consume megabytes
or gigabytes of memory if the server sends data at high frequency. With multiple disconnected
clients, memory exhaustion is rapid.

---

### 75. Calling asyncio APIs from Wrong Thread

**Severity:** CRITICAL

**Description:**
asyncio objects (Futures, Tasks, Events, Locks, Queues) are not thread-safe. Calling methods
like `future.set_result()`, `task.cancel()`, or `event.set()` from a thread other than the
event loop thread causes data corruption or `RuntimeError`. The correct approach is to use
`loop.call_soon_threadsafe()` or `asyncio.run_coroutine_threadsafe()` from other threads.

**BAD Pattern:**

```python
import asyncio
import threading

loop = asyncio.get_event_loop()
future = loop.create_future()

def callback_from_thread():
    # WRONG: called from a different thread, not thread-safe
    future.set_result("done")

thread = threading.Thread(target=callback_from_thread)
thread.start()
```

**GOOD Pattern:**

```python
import asyncio
import threading

loop = asyncio.get_event_loop()
future = loop.create_future()

def callback_from_thread():
    # CORRECT: thread-safe way to set result from another thread
    loop.call_soon_threadsafe(future.set_result, "done")

thread = threading.Thread(target=callback_from_thread)
thread.start()

# ALTERNATIVE: run a coroutine from another thread
def run_coro_from_thread():
    coro = async_function()
    future = asyncio.run_coroutine_threadsafe(coro, loop)
    result = future.result(timeout=10)
```

**Detection Approach:**
Grep for `set_result(`, `.cancel()`, `event.set()` in code that runs in threads (inside
`run_in_executor` callbacks, `threading.Thread` targets, or thread pool workers). If these
methods are called without `call_soon_threadsafe`, the code is unsafe.

**Impact:**
Data corruption, `RuntimeError`, or silent failures. The event loop's internal state can
become inconsistent, leading to unpredictable behavior including deadlocks, dropped callbacks,
or crashes. These bugs are intermittent and timing-dependent.

---

### 77. asyncio Debug Mode in Production

**Severity:** MEDIUM

**Description:**
asyncio debug mode (`PYTHONASYNCIODEBUG=1` or `loop.set_debug(True)`) enables slow callback
detection, coroutine tracking with creation stack traces, and additional logging. While
invaluable for development, these features add significant overhead in production: slow
callback checks run after every callback, and stack trace capture for every coroutine
creation adds microseconds.

**BAD Pattern:**

```python
import asyncio
import os

# WRONG: debug mode left enabled in production
os.environ["PYTHONASYNCIODEBUG"] = "1"

async def main():
    loop = asyncio.get_running_loop()
    loop.set_debug(True)  # WRONG: adds overhead in production
    await serve()

asyncio.run(main())
```

**GOOD Pattern:**

```python
import asyncio
import os

async def main():
    loop = asyncio.get_running_loop()
    # CORRECT: only enable debug mode in development
    if os.environ.get("ENVIRONMENT") == "development":
        loop.set_debug(True)
    await serve()

asyncio.run(main())
```

**Detection Approach:**
Grep for `PYTHONASYNCIODEBUG` and `set_debug(True)` in production code and configuration.
These should be conditional on a development/debug flag, not hardcoded.

**Impact:**
Performance degradation from debug overhead. Slow callback detection adds ~100us per
callback. Stack trace capture for coroutines adds ~10us per creation. At 1,157 RPS with
multiple coroutines per request, this compounds into measurable latency increases.

---

## Sources

1. Python 3.14 asyncio-dev documentation - https://docs.python.org/3.14/library/asyncio-dev.html
2. Mastering Python Async Patterns 2026 - DEV Community
3. Python asyncio shared state bugs - Inngest - https://www.inngest.com/blog/python-asyncio-shared-state-bugs
4. Avoiding Race Conditions in Python 2025 - Medium
5. Asyncio Race Conditions - Super Fast Python - https://superfastpython.com/asyncio-race-conditions/
6. PEP 789 - Async Generator Cancellation Bugs - https://peps.python.org/pep-0789/
7. Asyncio Task Cancellation Best Practices - Super Fast Python - https://superfastpython.com/asyncio-task-cancellation/
8. Asyncio Deadlocks - Super Fast Python - https://superfastpython.com/asyncio-deadlocks/
9. Async Python in AWS Lambda 2026 - Medium
10. aioboto3 Documentation - https://aioboto3.readthedocs.io/
11. FastAPI Concurrency and async/await - https://fastapi.tiangolo.com/async/
12. FastAPI Performance Mistakes - DEV Community
13. TOCTOU Race Conditions in Web Apps - Defuse Security - https://defuse.ca/race-conditions-in-web-applications.htm
14. CWE-367: Time-of-check Time-of-use (TOCTOU) Race Condition - https://cwe.mitre.org/data/definitions/367.html
15. Asyncio Exception Handling - roguelynn - https://www.roguelynn.com/words/asyncio-exception-handling/
16. Python docs - Coroutines and tasks - https://docs.python.org/3/library/asyncio-task.html
17. Python docs - Developing with asyncio - https://docs.python.org/3/library/asyncio-dev.html
18. Python docs - Policies - https://docs.python.org/3/library/asyncio-policy.html
19. Real Python - Exception Groups - https://realpython.com/python311-exception-groups/
20. PEP 654 - Exception Groups and except* - https://peps.python.org/pep-0654/
21. Hynek - Waiting in asyncio - https://hynek.me/articles/waiting-in-asyncio/
22. SuperFastPython - Asyncio Deadlock - https://superfastpython.com/asyncio-deadlock/
23. SuperFastPython - Asyncio Shield - https://superfastpython.com/asyncio-shield/
24. SuperFastPython - Asyncio Log Blocking - https://superfastpython.com/asyncio-log-blocking/
25. Inngest - asyncio primitives - https://www.inngest.com/blog/no-lost-updates-python-asyncio
26. death.andgravity.com - Limiting concurrency - https://death.andgravity.com/limit-concurrency
27. discuss.python.org - contextvars - https://discuss.python.org/t/back-propagation-of-contextvar-changes-from-worker-threads/15928
28. GitHub - FastAPI BackgroundTasks - https://github.com/fastapi/fastapi/discussions/11210
29. GitHub - FastAPI SQLAlchemy deadlock - https://github.com/fastapi/fastapi/discussions/6628
30. Starlette docs - Middleware - https://starlette.dev/middleware/
31. GitHub - aiobotocore blocks - https://github.com/aio-libs/aiobotocore/issues/1023
32. GitHub - aioboto3 S3 streaming - https://github.com/terricain/aioboto3/issues/266
33. GitHub - aioboto3 stale loop - https://github.com/terricain/aioboto3/issues/180
34. Medium - Async Lambda 2026 - https://medium.com/@joerosborne/how-to-use-async-python-functions-in-aws-lambda-in-2026-7eceaa797732
35. CPython Issue - wait_for cancellation - https://bugs.python.org/issue43389
36. aiohttp docs - Request Lifecycle - https://docs.aiohttp.org/en/stable/http_request_lifecycle.html
37. pytest-asyncio docs - https://pytest-asyncio.readthedocs.io/en/latest/concepts.html
38. sailor.li - asyncio sharp corners - https://sailor.li/asyncio
39. roguelynn - asyncio graceful shutdowns - https://roguelynn.com/words/asyncio-graceful-shutdowns/
