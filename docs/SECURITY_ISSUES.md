# Copyright (c) 2026 TrailLensCo
# All rights reserved.

# Python Security Vulnerability Patterns Reference

This document catalogs 84 Python security vulnerability patterns relevant to the TrailLens stack
(FastAPI, aioboto3, DynamoDB, Cognito, Lambda, S3, SNS, SES). Each pattern includes detection
regexes, vulnerable and secure code examples, and references to CWE and OWASP classifications.

---

## Summary Table

| ID | Severity | Category | Description |
|----|----------|----------|-------------|
| SEC-AUTH-001 | CRITICAL | Authentication & Session Management | JWT Algorithm Confusion Attack |
| SEC-AUTH-002 | CRITICAL | Authentication & Session Management | JWT None Algorithm Bypass |
| SEC-AUTH-003 | HIGH | Authentication & Session Management | JWT Missing Expiration Validation |
| SEC-AUTH-004 | CRITICAL | Authentication & Session Management | JWT Secret in Source Code |
| SEC-AUTH-005 | HIGH | Authentication & Session Management | OAuth State Parameter Missing/Static |
| SEC-AUTH-006 | HIGH | Authentication & Session Management | OAuth Redirect URI Insufficient Validation |
| SEC-AUTH-007 | MEDIUM | Authentication & Session Management | Missing PKCE in OAuth Flow |
| SEC-AUTH-008 | CRITICAL | Authentication & Session Management | Cognito Email-Based Account Takeover |
| SEC-AUTH-009 | HIGH | Authentication & Session Management | Cognito Unverified Email Attribute Change |
| SEC-AUTH-010 | HIGH | Authentication & Session Management | Session Fixation |
| SEC-AUTH-011 | MEDIUM | Authentication & Session Management | Missing Cookie Security Attributes |
| SEC-AUTH-012 | CRITICAL | Authentication & Session Management | Weak Password Hashing |
| SEC-AUTH-013 | HIGH | Authentication & Session Management | MFA TOTP Brute Force |
| SEC-AUTH-014 | HIGH | Authentication & Session Management | MFA Token Replay After Logout |
| SEC-AUTH-015 | HIGH | Authentication & Session Management | WebAuthn Challenge Replay |
| SEC-AUTHZ-001 | CRITICAL | Authorization & Access Control | Broken Object-Level Authorization (BOLA/IDOR) |
| SEC-AUTHZ-002 | HIGH | Authorization & Access Control | Broken Function-Level Authorization |
| SEC-AUTHZ-003 | CRITICAL | Authorization & Access Control | Multi-Tenant Data Isolation Failure |
| SEC-AUTHZ-004 | CRITICAL | Authorization & Access Control | Missing Tenant Scoping in DynamoDB |
| SEC-AUTHZ-005 | HIGH | Authorization & Access Control | Role Escalation via Mass Assignment |
| SEC-AUTHZ-006 | HIGH | Authorization & Access Control | Cognito Identity Pool Excessive Privileges |
| SEC-AUTHZ-007 | MEDIUM | Authorization & Access Control | Sequential/Predictable Resource IDs |
| SEC-INJ-001 | CRITICAL | Input Validation & Injection | DynamoDB FilterExpression Injection |
| SEC-INJ-002 | CRITICAL | Input Validation & Injection | DynamoDB KeyConditionExpression Injection |
| SEC-INJ-003 | HIGH | Input Validation & Injection | DynamoDB Scan Condition Injection |
| SEC-INJ-004 | HIGH | Input Validation & Injection | Path Traversal |
| SEC-INJ-005 | CRITICAL | Input Validation & Injection | OS Command Injection |
| SEC-INJ-006 | HIGH | Input Validation & Injection | Server-Side Request Forgery (SSRF) |
| SEC-INJ-007 | CRITICAL | Input Validation & Injection | Server-Side Template Injection |
| SEC-INJ-008 | CRITICAL | Input Validation & Injection | Python Code Injection via eval/exec |
| SEC-INJ-009 | MEDIUM | Input Validation & Injection | Regular Expression Denial of Service (ReDoS) |
| SEC-INJ-010 | HIGH | Input Validation & Injection | HTTP Header Injection |
| SEC-INJ-011 | HIGH | Input Validation & Injection | Mass Assignment via Pydantic Models |
| SEC-INJ-012 | CRITICAL | Input Validation & Injection | Unsafe Deserialization |
| SEC-INJ-013 | MEDIUM | Input Validation & Injection | X-Forwarded-For Spoofing |
| SEC-CRYPTO-001 | CRITICAL | Cryptographic Failures | Hardcoded AWS Access Keys |
| SEC-CRYPTO-002 | HIGH | Cryptographic Failures | Weak Random Number Generation |
| SEC-CRYPTO-003 | HIGH | Cryptographic Failures | Missing Encryption at Rest |
| SEC-CRYPTO-004 | CRITICAL | Cryptographic Failures | Hardcoded Database Credentials |
| SEC-CRYPTO-005 | MEDIUM | Cryptographic Failures | Non-Constant-Time Comparison |
| SEC-CRYPTO-006 | HIGH | Cryptographic Failures | Secrets in Lambda Environment Variables |
| SEC-PII-001 | HIGH | PII & Data Protection | PII in Application Logs |
| SEC-PII-002 | HIGH | PII & Data Protection | PII in Error Responses |
| SEC-PII-003 | MEDIUM | PII & Data Protection | Missing Data Masking |
| SEC-PII-004 | MEDIUM | PII & Data Protection | Missing Data Retention Controls |
| SEC-PII-005 | HIGH | PII & Data Protection | GDPR Right-to-Erasure Gaps |
| SEC-PII-006 | CRITICAL | PII & Data Protection | Cross-Tenant Data Leakage |
| SEC-CONFIG-001 | HIGH | Configuration & Deployment | Debug Mode in Production |
| SEC-CONFIG-002 | HIGH | Configuration & Deployment | Wildcard CORS |
| SEC-CONFIG-003 | MEDIUM | Configuration & Deployment | Missing Security Headers |
| SEC-CONFIG-004 | CRITICAL | Configuration & Deployment | Overly Permissive IAM |
| SEC-CONFIG-005 | CRITICAL | Configuration & Deployment | S3 Bucket Public Access |
| SEC-CONFIG-006 | MEDIUM | Configuration & Deployment | S3 Missing Lifecycle Rules |
| SEC-CONFIG-007 | HIGH | Configuration & Deployment | Lambda Env Var Secret Exposure |
| SEC-CONFIG-008 | HIGH | Configuration & Deployment | Cognito Guest Access Misconfigured |
| SEC-CONFIG-009 | MEDIUM | Configuration & Deployment | Cognito Identity Pool ID Hardcoded |
| SEC-DEP-001 | VARIES | Dependency & Supply Chain | Known Vulnerable Dependencies |
| SEC-DEP-002 | MEDIUM | Dependency & Supply Chain | Unpinned Dependencies |
| SEC-DEP-003 | HIGH | Dependency & Supply Chain | Typosquatting Risk |
| SEC-DEP-004 | MEDIUM | Dependency & Supply Chain | Abandoned Packages |
| SEC-ERR-001 | HIGH | Error Handling | Stack Traces in Responses |
| SEC-ERR-002 | MEDIUM | Error Handling | Verbose Error Messages |
| SEC-ERR-003 | MEDIUM | Error Handling | Timing Attack on Authentication |
| SEC-ERR-004 | MEDIUM | Error Handling | User Enumeration via Error Messages |
| SEC-ERR-005 | MEDIUM | Error Handling | Bare Except Swallowing Errors |
| SEC-ERR-006 | CRITICAL | Error Handling | Python 2 Except Syntax |
| SEC-ERR-007 | MEDIUM | Error Handling | Exception Re-wrapping Loses Subclass Info |
| SEC-API-001 | HIGH | API Security | Missing Rate Limiting |
| SEC-API-002 | HIGH | API Security | Excessive Data Exposure |
| SEC-API-003 | MEDIUM | API Security | Missing Request Size Limits |
| SEC-API-004 | HIGH | API Security | Missing API Gateway Throttling |
| SEC-API-005 | HIGH | API Security | Missing WAF Protection |
| SEC-LOG-001 | MEDIUM | Logging & Monitoring | Log Injection |
| SEC-LOG-002 | MEDIUM | Logging & Monitoring | Insufficient Security Logging |
| SEC-LOG-003 | MEDIUM | Logging & Monitoring | Missing Security Alarms |
| SEC-LOG-004 | CRITICAL | Logging & Monitoring | Credentials in Log Output |
| SEC-LOG-005 | MEDIUM | Logging & Monitoring | Missing Audit Trail |
| SEC-LOG-006 | HIGH | Logging & Monitoring | Silent Exception in Middleware |
| SEC-ASYNC-001 | HIGH | Async & Concurrency Security | Race Condition in Check-Then-Act |
| SEC-ASYNC-002 | HIGH | Async & Concurrency Security | Missing asyncio.Lock on Shared State |
| SEC-ASYNC-003 | HIGH | Async & Concurrency Security | DynamoDB Optimistic Locking Missing |
| SEC-ASYNC-004 | MEDIUM | Async & Concurrency Security | aioboto3 Resource Leak |
| SEC-AWS-001 | HIGH | AWS Service-Specific | SES Email Spoofing |
| SEC-AWS-002 | HIGH | AWS Service-Specific | SNS Data Exfiltration |
| SEC-AWS-003 | HIGH | AWS Service-Specific | Lambda Event Injection |
| SEC-AWS-004 | MEDIUM | AWS Service-Specific | Lambda Secret Initialization per Invocation |
| SEC-AWS-005 | LOW | AWS Service-Specific | Missing X-Ray Tracing |

---

## Category 1: Authentication & Session Management

### SEC-AUTH-001: JWT Algorithm Confusion Attack

- **Severity:** CRITICAL
- **Category:** Authentication & Session Management
- **Description:** Attacker changes the `alg` header from RS256 to HS256, causing the server to use the public RSA key as an HMAC secret. Since the public key is publicly available, the attacker can forge valid tokens.
- **Detection Regex:** `jwt\.decode\((?!.*algorithms)` or `algorithms\s*=\s*\[.*HS256.*RS256`
- **Impact:** Complete authentication bypass. Attacker can forge tokens for any user.
- **CWE:** CWE-327 (Use of a Broken or Risky Cryptographic Algorithm)
- **OWASP:** A07:2021 - Identification and Authentication Failures

**Vulnerable Pattern:**

```python
import jwt

async def verify_token(token: str, public_key: str) -> dict:
    # VULNERABLE: Accepts both HS256 and RS256
    # Attacker sets alg=HS256 and signs with the public key
    payload = jwt.decode(
        token,
        public_key,
        algorithms=["HS256", "RS256"],
    )
    return payload
```

**Secure Pattern:**

```python
import jwt

async def verify_token(token: str, public_key: str) -> dict:
    # SECURE: Only RS256 accepted - HS256 tokens are rejected
    payload = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
    )
    return payload
```

---

### SEC-AUTH-002: JWT None Algorithm Bypass

- **Severity:** CRITICAL
- **Category:** Authentication & Session Management
- **Description:** Attacker sets the JWT `alg` header to `"none"` and submits an unsigned token. If the server does not enforce signature verification, the token is accepted without cryptographic validation.
- **Detection Regex:** `jwt\.decode\(.*options.*verify_signature.*False` or `jwt\.decode\(.*algorithms.*none`
- **Impact:** Complete authentication bypass. Any unsigned token is accepted as valid.
- **CWE:** CWE-345 (Insufficient Verification of Data Authenticity)
- **OWASP:** A07:2021 - Identification and Authentication Failures

**Vulnerable Pattern:**

```python
import jwt

async def verify_token(token: str) -> dict:
    # VULNERABLE: Signature verification disabled
    payload = jwt.decode(
        token,
        options={"verify_signature": False},
    )
    return payload
```

**Secure Pattern:**

```python
import jwt

async def verify_token(token: str, public_key: str) -> dict:
    # SECURE: Signature verification enabled, specific algorithm required
    payload = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
    )
    return payload
```

---

### SEC-AUTH-003: JWT Missing Expiration Validation

- **Severity:** HIGH
- **Category:** Authentication & Session Management
- **Description:** Tokens without `exp` claim or with expiration verification disabled remain valid indefinitely. A leaked or stolen token can be used forever.
- **Detection Regex:** `jwt\.decode\(.*options.*verify_exp.*False`
- **Impact:** Stolen tokens remain valid indefinitely. No way to force re-authentication.
- **CWE:** CWE-613 (Insufficient Session Expiration)
- **OWASP:** A07:2021 - Identification and Authentication Failures

**Vulnerable Pattern:**

```python
import jwt

async def verify_token(token: str, public_key: str) -> dict:
    # VULNERABLE: Expiration check disabled
    payload = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        options={"verify_exp": False},
    )
    return payload
```

**Secure Pattern:**

```python
import jwt

async def verify_token(token: str, public_key: str) -> dict:
    # SECURE: verify_exp is True by default in PyJWT
    # Tokens without exp claim or with expired exp are rejected
    payload = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        options={
            "require": ["exp", "iat", "sub"],
        },
    )
    return payload
```

---

### SEC-AUTH-004: JWT Secret in Source Code

- **Severity:** CRITICAL
- **Category:** Authentication & Session Management
- **Description:** JWT signing secrets hardcoded in application source code. Anyone with read access to the repository can forge valid tokens for any user.
- **Detection Regex:** `(SECRET_KEY|JWT_SECRET|SIGNING_KEY)\s*=\s*["'][^"']+["']`
- **Impact:** Complete authentication bypass if source code is leaked or accessible.
- **CWE:** CWE-798 (Use of Hard-coded Credentials)
- **OWASP:** A04:2021 - Insecure Design

**Vulnerable Pattern:**

```python
import jwt

# VULNERABLE: Secret hardcoded in source code
SECRET_KEY = "my-super-secret-jwt-key-12345"

async def create_token(user_id: str) -> str:
    payload = {"sub": user_id}
    return jwt.encode(payload, SECRET_KEY, algorithm="RS256")
```

**Secure Pattern:**

```python
import jwt
import aioboto3

# SECURE: Secret retrieved from AWS Secrets Manager at module level
_session = aioboto3.Session()
_jwt_secret: str | None = None

async def _get_jwt_secret() -> str:
    global _jwt_secret
    if _jwt_secret is None:
        async with _session.client("secretsmanager") as client:
            response = await client.get_secret_value(SecretId="traillens/jwt-secret")
            _jwt_secret = response["SecretString"]
    return _jwt_secret

async def create_token(user_id: str) -> str:
    secret = await _get_jwt_secret()
    payload = {"sub": user_id}
    return jwt.encode(payload, secret, algorithm="RS256")
```

---

### SEC-AUTH-005: OAuth State Parameter Missing/Static

- **Severity:** HIGH
- **Category:** Authentication & Session Management
- **Description:** OAuth authorization flows without a cryptographically random `state` parameter are vulnerable to Cross-Site Request Forgery (CSRF). An attacker can initiate an OAuth flow and trick a victim into completing it, linking the attacker's account.
- **Detection Regex:** `authorize_url.*(?!state)` or `state\s*=\s*["'][^"']+["']`
- **Impact:** Account linking CSRF. Attacker can link their external account to victim's TrailLens account.
- **CWE:** CWE-352 (Cross-Site Request Forgery)
- **OWASP:** A07:2021 - Identification and Authentication Failures

**Vulnerable Pattern:**

```python
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/auth/facebook/login")
async def facebook_login():
    # VULNERABLE: No state parameter - susceptible to CSRF
    redirect_url = (
        f"https://www.facebook.com/v18.0/dialog/oauth"
        f"?client_id={settings.FB_CLIENT_ID}"
        f"&redirect_uri={settings.FB_REDIRECT_URI}"
        f"&scope=email"
    )
    return RedirectResponse(redirect_url)
```

**Secure Pattern:**

```python
import secrets
import hmac
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/auth/facebook/login")
async def facebook_login(request: Request):
    # SECURE: Cryptographically random state parameter
    state = secrets.token_urlsafe(32)
    request.session["oauth_state"] = state

    redirect_url = (
        f"https://www.facebook.com/v18.0/dialog/oauth"
        f"?client_id={settings.FB_CLIENT_ID}"
        f"&redirect_uri={settings.FB_REDIRECT_URI}"
        f"&scope=email"
        f"&state={state}"
    )
    return RedirectResponse(redirect_url)

@router.get("/auth/facebook/callback")
async def facebook_callback(request: Request, code: str, state: str):
    # SECURE: Validate state matches what was stored in session
    expected_state = request.session.pop("oauth_state", None)
    if not expected_state or not hmac.compare_digest(state, expected_state):
        raise HTTPException(status_code=403, detail="Invalid OAuth state")
    # Proceed with token exchange
```

---

### SEC-AUTH-006: OAuth Redirect URI Insufficient Validation

- **Severity:** HIGH
- **Category:** Authentication & Session Management
- **Description:** Using prefix matching or pattern matching for `redirect_uri` validation allows attackers to redirect authorization codes to attacker-controlled subdomains or paths (e.g., `https://myapp.com.evil.com`).
- **Detection Regex:** `redirect_uri.*startswith` or `redirect_uri.*\.match`
- **Impact:** Authorization code theft via open redirect, leading to account takeover.
- **CWE:** CWE-601 (URL Redirection to Untrusted Site)
- **OWASP:** A07:2021 - Identification and Authentication Failures

**Vulnerable Pattern:**

```python
from fastapi import APIRouter, HTTPException

ALLOWED_PREFIX = "https://app.traillenshq.com"

@router.get("/auth/callback")
async def auth_callback(redirect_uri: str, code: str):
    # VULNERABLE: Prefix matching allows https://app.traillenshq.com.evil.com
    if not redirect_uri.startswith(ALLOWED_PREFIX):
        raise HTTPException(status_code=400, detail="Invalid redirect")
    return RedirectResponse(redirect_uri)
```

**Secure Pattern:**

```python
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

# SECURE: Exact match against allow list
ALLOWED_REDIRECT_URIS: frozenset[str] = frozenset({
    "https://app.traillenshq.com/auth/callback",
    "https://app.traillenshq.com/auth/callback/facebook",
})

@router.get("/auth/callback")
async def auth_callback(redirect_uri: str, code: str):
    if redirect_uri not in ALLOWED_REDIRECT_URIS:
        raise HTTPException(status_code=400, detail="Invalid redirect")
    return RedirectResponse(redirect_uri)
```

---

### SEC-AUTH-007: Missing PKCE in OAuth Flow

- **Severity:** MEDIUM
- **Category:** Authentication & Session Management
- **Description:** Without Proof Key for Code Exchange (PKCE), authorization codes can be intercepted by malicious apps on the same device (especially mobile). PKCE binds the authorization code to the original client.
- **Detection Regex:** `authorize_url.*(?!code_challenge)` or `token_exchange.*(?!code_verifier)`
- **Impact:** Authorization code interception on mobile or shared environments.
- **CWE:** CWE-287 (Improper Authentication)
- **OWASP:** A07:2021 - Identification and Authentication Failures

**Vulnerable Pattern:**

```python
import httpx
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/auth/login")
async def oauth_login():
    # VULNERABLE: No PKCE - authorization code can be intercepted
    redirect_url = (
        f"{settings.AUTH_URL}/authorize"
        f"?client_id={settings.CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={settings.REDIRECT_URI}"
    )
    return RedirectResponse(redirect_url)

@router.get("/auth/callback")
async def oauth_callback(code: str):
    # VULNERABLE: No code_verifier in token exchange
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.AUTH_URL}/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.CLIENT_ID,
                "redirect_uri": settings.REDIRECT_URI,
            },
        )
    return response.json()
```

**Secure Pattern:**

```python
import hashlib
import base64
import secrets
import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

router = APIRouter()

def _generate_pkce_pair() -> tuple[str, str]:
    """Generate PKCE code_verifier and code_challenge."""
    code_verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
    code_challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return code_verifier, code_challenge

@router.get("/auth/login")
async def oauth_login(request: Request):
    # SECURE: PKCE code_challenge sent with authorization request
    code_verifier, code_challenge = _generate_pkce_pair()
    request.session["pkce_verifier"] = code_verifier

    redirect_url = (
        f"{settings.AUTH_URL}/authorize"
        f"?client_id={settings.CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={settings.REDIRECT_URI}"
        f"&code_challenge={code_challenge}"
        f"&code_challenge_method=S256"
    )
    return RedirectResponse(redirect_url)

@router.get("/auth/callback")
async def oauth_callback(request: Request, code: str):
    # SECURE: code_verifier proves this is the original requestor
    code_verifier = request.session.pop("pkce_verifier", None)
    if not code_verifier:
        raise HTTPException(status_code=400, detail="Missing PKCE verifier")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.AUTH_URL}/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.CLIENT_ID,
                "redirect_uri": settings.REDIRECT_URI,
                "code_verifier": code_verifier,
            },
        )
    return response.json()
```

---

### SEC-AUTH-008: Cognito Email-Based Account Takeover

- **Severity:** CRITICAL
- **Category:** Authentication & Session Management
- **Description:** Using `email` claim instead of `sub` claim for user identification. If Cognito allows users to change their email and attribute writes are unrestricted, an attacker can change their email to match another user's email and take over their account.
- **Detection Regex:** `cognito.*email.*(?!sub)` or `claims\[["']email["']\]`
- **Impact:** Complete account takeover by changing email to match target user.
- **CWE:** CWE-287 (Improper Authentication)
- **OWASP:** A01:2021 - Broken Access Control

**Vulnerable Pattern:**

```python
from fastapi import Depends

async def get_current_user(claims: dict = Depends(verify_cognito_token)):
    # VULNERABLE: email is mutable - attacker can change theirs to victim's
    user_id = claims["email"]
    user = await user_repo.get_by_email(user_id)
    return user
```

**Secure Pattern:**

```python
from fastapi import Depends, HTTPException

async def get_current_user(claims: dict = Depends(verify_cognito_token)):
    # SECURE: sub is immutable Cognito user ID (UUID format)
    user_id = claims["sub"]
    user = await user_repo.get_by_sub(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
```

---

### SEC-AUTH-009: Cognito Unverified Email Attribute Change

- **Severity:** HIGH
- **Category:** Authentication & Session Management
- **Description:** By default, Cognito allows users to change their email address without requiring verification of the new email. This can lead to account takeover when email is used for identification or password recovery.
- **Detection Regex:** `update_user_attributes.*email` without verification enforcement
- **Impact:** Account takeover through unverified email change affecting password recovery flows.
- **CWE:** CWE-287 (Improper Authentication)
- **OWASP:** A07:2021 - Identification and Authentication Failures

**Vulnerable Pattern:**

```python
import aioboto3

async def update_user_email(access_token: str, new_email: str):
    session = aioboto3.Session()
    async with session.client("cognito-idp") as client:
        # VULNERABLE: Email changed without verification requirement
        # User pool does not enforce email_verified before allowing login
        await client.update_user_attributes(
            AccessToken=access_token,
            UserAttributes=[
                {"Name": "email", "Value": new_email},
            ],
        )
```

**Secure Pattern:**

```python
import aioboto3

# SECURE: Cognito User Pool configured with:
# - auto_verified_attributes=["email"]
# - Verification required before attribute update takes effect
# This is configured in infrastructure (Pulumi/CloudFormation):
#
#   user_pool = aws.cognito.UserPool(
#       "user-pool",
#       auto_verified_attributes=["email"],
#       user_attribute_update_settings={
#           "attributes_require_verification_before_update": ["email"],
#       },
#   )

async def update_user_email(access_token: str, new_email: str):
    session = aioboto3.Session()
    async with session.client("cognito-idp") as client:
        # SECURE: Cognito sends verification code to new email
        # email_verified is set to false until user confirms
        await client.update_user_attributes(
            AccessToken=access_token,
            UserAttributes=[
                {"Name": "email", "Value": new_email},
            ],
        )
        # User must verify new email before it becomes active
```

---

### SEC-AUTH-010: Session Fixation

- **Severity:** HIGH
- **Category:** Authentication & Session Management
- **Description:** After successful authentication, the session ID is not regenerated. An attacker who knows (or sets) a session ID before login can hijack the session after the victim authenticates.
- **Detection Regex:** `login.*(?!regenerate|new_session|rotate)` or `session.*=.*request\.cookies`
- **Impact:** Session hijacking after successful authentication.
- **CWE:** CWE-384 (Session Fixation)
- **OWASP:** A07:2021 - Identification and Authentication Failures

**Vulnerable Pattern:**

```python
from fastapi import APIRouter, Request, Response

router = APIRouter()

@router.post("/auth/login")
async def login(request: Request, response: Response, credentials: LoginRequest):
    user = await authenticate(credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # VULNERABLE: Reusing existing session - attacker who set the
    # session cookie before login now has access
    request.session["user_id"] = user.id
    return {"message": "Login successful"}
```

**Secure Pattern:**

```python
import secrets
from datetime import datetime, UTC
from fastapi import APIRouter, HTTPException, Request, Response

router = APIRouter()

@router.post("/auth/login")
async def login(request: Request, response: Response, credentials: LoginRequest):
    user = await authenticate(credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # SECURE: Clear old session and generate new session ID
    request.session.clear()
    request.session["user_id"] = user.id
    request.session["_csrf_token"] = secrets.token_urlsafe(32)
    request.session["_created_at"] = datetime.now(UTC).isoformat()
    return {"message": "Login successful"}
```

---

### SEC-AUTH-011: Missing Cookie Security Attributes

- **Severity:** MEDIUM
- **Category:** Authentication & Session Management
- **Description:** Session cookies set without `HttpOnly`, `Secure`, and `SameSite` attributes are vulnerable to XSS theft, man-in-the-middle interception, and CSRF attacks.
- **Detection Regex:** `set_cookie\((?!.*httponly)` or `set_cookie\((?!.*secure)`
- **Impact:** Session theft via XSS (missing HttpOnly), MITM (missing Secure), or CSRF (missing SameSite).
- **CWE:** CWE-614 (Sensitive Cookie in HTTPS Session Without 'Secure' Attribute)
- **OWASP:** A07:2021 - Identification and Authentication Failures

**Vulnerable Pattern:**

```python
from fastapi import APIRouter, Response

router = APIRouter()

@router.post("/auth/login")
async def login(response: Response, credentials: LoginRequest):
    token = await create_session_token(credentials)
    # VULNERABLE: Cookie accessible to JavaScript, sent over HTTP, no CSRF protection
    response.set_cookie("session", token)
    return {"message": "Login successful"}
```

**Secure Pattern:**

```python
from fastapi import APIRouter, Response

router = APIRouter()

@router.post("/auth/login")
async def login(response: Response, credentials: LoginRequest):
    token = await create_session_token(credentials)
    # SECURE: All security attributes set
    response.set_cookie(
        key="session",
        value=token,
        httponly=True,       # Not accessible via JavaScript
        secure=True,         # Only sent over HTTPS
        samesite="strict",   # Not sent on cross-site requests
        max_age=3600,        # 1 hour expiration
        path="/",
        domain=".traillenshq.com",
    )
    return {"message": "Login successful"}
```

---

### SEC-AUTH-012: Weak Password Hashing

- **Severity:** CRITICAL
- **Category:** Authentication & Session Management
- **Description:** Using MD5 or SHA1 for password hashing. Modern GPUs can compute 180+ billion MD5 hashes per second, making brute-force trivial. Password hashing requires intentionally slow algorithms.
- **Detection Regex:** `hashlib\.(md5|sha1)\(` or `hashlib\.new\(["'](md5|sha1)`
- **Impact:** Mass password compromise if database is leaked. GPU cracking at 180B+ attempts/sec for MD5.
- **CWE:** CWE-328 (Use of Weak Hash)
- **OWASP:** A04:2021 - Insecure Design

**Vulnerable Pattern:**

```python
import hashlib

async def create_user(username: str, password: str):
    # VULNERABLE: MD5 is not a password hashing algorithm
    # GPU can crack at 180+ billion hashes/second
    hashed = hashlib.md5(password.encode()).hexdigest()
    await user_repo.create(username=username, password_hash=hashed)

async def verify_password(password: str, stored_hash: str) -> bool:
    return hashlib.md5(password.encode()).hexdigest() == stored_hash
```

**Secure Pattern:**

```python
import bcrypt

async def create_user(username: str, password: str):
    # SECURE: bcrypt with cost factor 12 (~250ms per hash)
    # Intentionally slow - resistant to GPU acceleration
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12))
    await user_repo.create(username=username, password_hash=hashed.decode("utf-8"))

async def verify_password(password: str, stored_hash: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        stored_hash.encode("utf-8"),
    )
```

---

### SEC-AUTH-013: MFA TOTP Brute Force

- **Severity:** HIGH
- **Category:** Authentication & Session Management
- **Description:** Missing rate limiting on TOTP verification endpoint. A 6-digit TOTP code has only 1,000,000 possible values. Without rate limiting, an attacker can brute-force a valid code within the 30-second window.
- **Detection Regex:** `verify_totp.*(?!rate_limit|throttle|attempt)` or `totp\.verify\(`
- **Impact:** MFA bypass through brute-force of 6-digit TOTP code.
- **CWE:** CWE-307 (Improper Restriction of Excessive Authentication Attempts)
- **OWASP:** A07:2021 - Identification and Authentication Failures

**Vulnerable Pattern:**

```python
import pyotp
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/auth/verify-mfa")
async def verify_mfa(user_id: str, totp_code: str):
    user = await user_repo.get(user_id)
    totp = pyotp.TOTP(user.totp_secret)

    # VULNERABLE: No rate limiting - attacker can try all 1M codes
    if totp.verify(totp_code):
        return {"token": await create_access_token(user_id)}
    raise HTTPException(status_code=401, detail="Invalid MFA code")
```

**Secure Pattern:**

```python
import pyotp
from fastapi import APIRouter, HTTPException, Request

router = APIRouter()

MAX_MFA_ATTEMPTS = 5
MFA_LOCKOUT_SECONDS = 300  # 5 minutes

@router.post("/auth/verify-mfa")
async def verify_mfa(request: Request, user_id: str, totp_code: str):
    # SECURE: Check rate limit before verification
    attempt_count = await rate_limiter.get_attempts(
        key=f"mfa:{user_id}",
        window_seconds=MFA_LOCKOUT_SECONDS,
    )
    if attempt_count >= MAX_MFA_ATTEMPTS:
        raise HTTPException(
            status_code=429,
            detail="Too many MFA attempts. Try again later.",
        )

    await rate_limiter.increment(key=f"mfa:{user_id}", window_seconds=MFA_LOCKOUT_SECONDS)

    user = await user_repo.get(user_id)
    totp = pyotp.TOTP(user.totp_secret)

    if totp.verify(totp_code, valid_window=1):
        await rate_limiter.reset(key=f"mfa:{user_id}")
        return {"token": await create_access_token(user_id)}

    raise HTTPException(status_code=401, detail="Invalid MFA code")
```

---

### SEC-AUTH-014: MFA Token Replay After Logout

- **Severity:** HIGH
- **Category:** Authentication & Session Management
- **Description:** Access tokens and refresh tokens are not invalidated on the server side after logout. An attacker who obtained a token before logout can continue using it.
- **Detection Regex:** `logout.*(?!revoke|invalidate|blacklist|delete)` or `logout.*return.*200`
- **Impact:** Stolen tokens remain valid after user logs out.
- **CWE:** CWE-613 (Insufficient Session Expiration)
- **OWASP:** A07:2021 - Identification and Authentication Failures

**Vulnerable Pattern:**

```python
from fastapi import APIRouter

router = APIRouter()

@router.post("/auth/logout")
async def logout():
    # VULNERABLE: Token not invalidated server-side
    # Attacker with a copy of the token can still use it
    return {"message": "Logged out"}
```

**Secure Pattern:**

```python
import aioboto3
from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/auth/logout")
async def logout(
    access_token: str = Depends(get_access_token),
    claims: dict = Depends(get_current_user_claims),
):
    session = aioboto3.Session()

    # SECURE: Revoke tokens server-side via Cognito
    async with session.client("cognito-idp") as client:
        await client.global_sign_out(AccessToken=access_token)

    # Also add token to deny list for edge cases
    await token_denylist.add(
        token_jti=claims["jti"],
        expires_at=claims["exp"],
    )

    return {"message": "Logged out"}
```

---

### SEC-AUTH-015: WebAuthn Challenge Replay

- **Severity:** HIGH
- **Category:** Authentication & Session Management
- **Description:** WebAuthn challenges that are not single-use or time-limited can be replayed. An attacker who intercepts a challenge-response pair can replay it to authenticate.
- **Detection Regex:** `webauthn.*challenge.*(?!delete|expire|single_use)` or `verify_authentication.*(?!pop.*challenge)`
- **Impact:** Authentication bypass through replayed WebAuthn challenge-response pairs.
- **CWE:** CWE-294 (Authentication Bypass by Capture-replay)
- **OWASP:** A07:2021 - Identification and Authentication Failures

**Vulnerable Pattern:**

```python
from fastapi import APIRouter

router = APIRouter()

# VULNERABLE: Challenge stored without expiration, not deleted after use
challenges: dict[str, bytes] = {}

@router.post("/webauthn/authenticate/begin")
async def begin_authentication(user_id: str):
    challenge = generate_challenge()
    challenges[user_id] = challenge  # Never expires, never deleted
    return {"challenge": challenge}

@router.post("/webauthn/authenticate/complete")
async def complete_authentication(user_id: str, response: AuthResponse):
    challenge = challenges.get(user_id)  # Same challenge can be reused
    if verify_authentication(challenge, response):
        return {"token": await create_access_token(user_id)}
```

**Secure Pattern:**

```python
import secrets
import time
from fastapi import APIRouter, HTTPException

router = APIRouter()

CHALLENGE_TTL_SECONDS = 120  # 2 minutes

@router.post("/webauthn/authenticate/begin")
async def begin_authentication(user_id: str):
    challenge = secrets.token_bytes(32)
    # SECURE: Challenge stored with expiration timestamp in DynamoDB
    await challenge_store.put(
        user_id=user_id,
        challenge=challenge,
        ttl=int(time.time()) + CHALLENGE_TTL_SECONDS,
    )
    return {"challenge": challenge}

@router.post("/webauthn/authenticate/complete")
async def complete_authentication(user_id: str, response: AuthResponse):
    # SECURE: Challenge retrieved and immediately deleted (single-use)
    challenge_record = await challenge_store.pop(user_id=user_id)
    if not challenge_record:
        raise HTTPException(status_code=400, detail="No pending challenge")

    # SECURE: Check expiration
    if time.time() > challenge_record["ttl"]:
        raise HTTPException(status_code=400, detail="Challenge expired")

    if not verify_authentication(challenge_record["challenge"], response):
        raise HTTPException(status_code=401, detail="Authentication failed")

    return {"token": await create_access_token(user_id)}
```

---

## Category 2: Authorization & Access Control

### SEC-AUTHZ-001: Broken Object-Level Authorization (BOLA/IDOR)

- **Severity:** CRITICAL
- **Category:** Authorization & Access Control
- **Description:** API endpoints accept resource IDs directly from user input without verifying the requesting user has permission to access that resource. This is the number one API vulnerability, accounting for approximately 40% of API attacks.
- **Detection Regex:** `(get|delete|update).*\{(id|trail_id|user_id)\}` without auth dependency
- **Impact:** Unauthorized access to any user's data by changing resource ID in the request.
- **CWE:** CWE-639 (Authorization Bypass Through User-Controlled Key)
- **OWASP:** API1:2023 - Broken Object Level Authorization

**Vulnerable Pattern:**

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/trails/{trail_id}")
async def get_trail(trail_id: str):
    # VULNERABLE: No authorization check - any user can access any trail
    response = await table.get_item(Key={"id": trail_id})
    return response.get("Item")

@router.delete("/trails/{trail_id}")
async def delete_trail(trail_id: str):
    # VULNERABLE: Any user can delete any trail
    await table.delete_item(Key={"id": trail_id})
    return {"message": "Deleted"}
```

**Secure Pattern:**

```python
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

@router.get("/trails/{trail_id}")
async def get_trail(
    trail_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
):
    # SECURE: Fetch resource and verify ownership
    response = await table.get_item(
        Key={"tenant_id": user.org_id, "id": trail_id},
    )
    item = response.get("Item")
    if not item:
        raise HTTPException(status_code=404, detail="Resource not found")

    # SECURE: Additional permission check
    if not await authz.can_read(user, item):
        raise HTTPException(status_code=403, detail="Access denied")

    return TrailResponse(**item)

@router.delete("/trails/{trail_id}")
async def delete_trail(
    trail_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
):
    if not await authz.can_delete(user, trail_id):
        raise HTTPException(status_code=403, detail="Access denied")

    await table.delete_item(
        Key={"tenant_id": user.org_id, "id": trail_id},
        ConditionExpression="attribute_exists(id)",
    )
    return {"message": "Deleted"}
```

---

### SEC-AUTHZ-002: Broken Function-Level Authorization

- **Severity:** HIGH
- **Category:** Authorization & Access Control
- **Description:** Administrative endpoints lack proper authorization checks. Regular users can access admin functionality by directly calling the endpoint URL.
- **Detection Regex:** `@router\.(post|put|delete).*admin` without `Depends(require_admin)`
- **Impact:** Privilege escalation. Regular users can perform admin actions.
- **CWE:** CWE-285 (Improper Authorization)
- **OWASP:** API5:2023 - Broken Function Level Authorization

**Vulnerable Pattern:**

```python
from fastapi import APIRouter

router = APIRouter(prefix="/admin")

@router.post("/users/{user_id}/ban")
async def ban_user(user_id: str):
    # VULNERABLE: No admin role check - any authenticated user can ban others
    await user_repo.update(user_id, banned=True)
    return {"message": "User banned"}

@router.delete("/trails/{trail_id}")
async def admin_delete_trail(trail_id: str):
    # VULNERABLE: No admin authorization
    await trail_repo.delete(trail_id)
    return {"message": "Trail deleted"}
```

**Secure Pattern:**

```python
from fastapi import APIRouter, Depends, HTTPException
from api.shared.logging import log_info

router = APIRouter(prefix="/admin")

async def require_admin(user: AuthenticatedUser = Depends(get_current_user)):
    """Dependency that enforces admin role."""
    if "admin" not in user.roles:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

@router.post("/users/{user_id}/ban")
async def ban_user(
    user_id: str,
    admin: AuthenticatedUser = Depends(require_admin),
):
    # SECURE: Only users with admin role can reach this code
    await user_repo.update(user_id, banned=True)
    log_info("User banned", metadata={"admin_id": admin.id, "target_user_id": user_id})
    return {"message": "User banned"}

@router.delete("/trails/{trail_id}")
async def admin_delete_trail(
    trail_id: str,
    admin: AuthenticatedUser = Depends(require_admin),
):
    await trail_repo.delete(trail_id)
    log_info("Trail deleted by admin", metadata={"admin_id": admin.id, "trail_id": trail_id})
    return {"message": "Trail deleted"}
```

---

### SEC-AUTHZ-003: Multi-Tenant Data Isolation Failure

- **Severity:** CRITICAL
- **Category:** Authorization & Access Control
- **Description:** Tenant identification derived from request headers or query parameters instead of verified JWT claims. Attackers can modify headers to access other tenants' data.
- **Detection Regex:** `tenant_id\s*=\s*request\.(headers|query)` or `org_id\s*=\s*request\.headers`
- **Impact:** Complete cross-tenant data access. Attacker reads/modifies any organization's data.
- **CWE:** CWE-668 (Exposure of Resource to Wrong Sphere)
- **OWASP:** A01:2021 - Broken Access Control

**Vulnerable Pattern:**

```python
from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/trail-systems")
async def list_trail_systems(request: Request):
    # VULNERABLE: Tenant ID from request header - attacker can change it
    tenant_id = request.headers.get("X-Tenant-ID")

    response = await table.query(
        KeyConditionExpression="tenant_id = :tid",
        ExpressionAttributeValues={":tid": tenant_id},
    )
    return response["Items"]
```

**Secure Pattern:**

```python
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/trail-systems")
async def list_trail_systems(
    user: AuthenticatedUser = Depends(get_current_user),
):
    # SECURE: Tenant ID from verified JWT claims - cannot be forged
    tenant_id = user.org_id  # Extracted from token_claims["custom:org_id"]

    response = await table.query(
        KeyConditionExpression="tenant_id = :tid",
        ExpressionAttributeValues={":tid": tenant_id},
    )
    return [TrailSystemResponse(**item) for item in response["Items"]]
```

---

### SEC-AUTHZ-004: Missing Tenant Scoping in DynamoDB

- **Severity:** CRITICAL
- **Category:** Authorization & Access Control
- **Description:** DynamoDB queries and scans without `tenant_id` in the key condition allow cross-tenant data access. Every data operation must be scoped to the authenticated tenant.
- **Detection Regex:** `(query|scan|get_item)\((?!.*tenant)` or `Key=\{["']id["']:`
- **Impact:** Cross-tenant data access. Users in one organization can read/modify another organization's data.
- **CWE:** CWE-639 (Authorization Bypass Through User-Controlled Key)
- **OWASP:** A01:2021 - Broken Access Control

**Vulnerable Pattern:**

```python
import aioboto3

async def get_trail(trail_id: str):
    session = aioboto3.Session()
    async with session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table("trails")
        # VULNERABLE: No tenant scoping - any trail can be fetched
        response = await table.get_item(Key={"id": trail_id})
        return response.get("Item")

async def list_all_trails():
    session = aioboto3.Session()
    async with session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table("trails")
        # VULNERABLE: Full table scan - returns all tenants' data
        response = await table.scan()
        return response["Items"]
```

**Secure Pattern:**

```python
import aioboto3

async def get_trail(tenant_id: str, trail_id: str):
    session = aioboto3.Session()
    async with session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table("trails")
        # SECURE: Composite key includes tenant_id
        response = await table.get_item(
            Key={"tenant_id": tenant_id, "id": trail_id},
        )
        return response.get("Item")

async def list_trails_for_tenant(tenant_id: str):
    session = aioboto3.Session()
    async with session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table("trails")
        # SECURE: Query scoped to tenant partition
        response = await table.query(
            KeyConditionExpression="tenant_id = :tid",
            ExpressionAttributeValues={":tid": tenant_id},
        )
        return response["Items"]
```

---

### SEC-AUTHZ-005: Role Escalation via Mass Assignment

- **Severity:** HIGH
- **Category:** Authorization & Access Control
- **Description:** API accepts user-controlled fields like `role`, `is_admin`, or `permissions` directly from the request body. Attackers can include these fields to escalate their privileges.
- **Detection Regex:** `(role|is_admin|permissions).*request\.(body|json)` or `\*\*request\.json\(\)`
- **Impact:** Privilege escalation. Regular user gains admin access by including role fields in request.
- **CWE:** CWE-915 (Improperly Controlled Modification of Dynamically-Determined Object Attributes)
- **OWASP:** API3:2023 - Broken Object Property Level Authorization

**Vulnerable Pattern:**

```python
from fastapi import APIRouter
from pydantic import BaseModel

class UserModel(BaseModel):
    username: str
    email: str
    role: str = "user"         # Dangerous: attacker can set role="admin"
    is_admin: bool = False     # Dangerous: attacker can set is_admin=True

router = APIRouter()

@router.post("/users")
async def create_user(user: UserModel):
    # VULNERABLE: All fields from request body accepted including role
    await user_repo.create(**user.model_dump())
    return {"message": "User created"}
```

**Secure Pattern:**

```python
from fastapi import APIRouter, Depends
from pydantic import BaseModel

# SECURE: Separate input model without sensitive fields
class UserCreateRequest(BaseModel):
    username: str
    email: str
    # No role, is_admin, or permissions fields

class UserInternal(BaseModel):
    username: str
    email: str
    role: str
    is_admin: bool

router = APIRouter()

@router.post("/users")
async def create_user(
    user_input: UserCreateRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    # SECURE: Server sets role - never from user input
    user = UserInternal(
        username=user_input.username,
        email=user_input.email,
        role="user",
        is_admin=False,
    )
    await user_repo.create(**user.model_dump())
    return {"message": "User created"}
```

---

### SEC-AUTHZ-006: Cognito Identity Pool Excessive Privileges

- **Severity:** HIGH
- **Category:** Authorization & Access Control
- **Description:** IAM roles attached to Cognito Identity Pool authenticated/unauthenticated roles grant overly broad permissions (wildcard actions or resources), allowing users to access AWS services beyond what the application requires.
- **Detection Regex:** `identity_pool.*role.*\*` or `IdentityPool.*PolicyDocument.*\*`
- **Impact:** Authenticated users can directly access AWS resources (S3 buckets, DynamoDB tables) beyond application scope.
- **CWE:** CWE-250 (Execution with Unnecessary Privileges)
- **OWASP:** A01:2021 - Broken Access Control

**Vulnerable Pattern:**

```python
# Pulumi infrastructure code
import json
import pulumi_aws as aws

# VULNERABLE: Wildcard permissions on identity pool role
auth_role_policy = aws.iam.RolePolicy(
    "cognito-auth-role-policy",
    role=auth_role.name,
    policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": [
                "s3:*",           # Full S3 access
                "dynamodb:*",     # Full DynamoDB access
            ],
            "Resource": "*",      # All resources
        }],
    }),
)
```

**Secure Pattern:**

```python
# Pulumi infrastructure code
import json
import pulumi_aws as aws

# SECURE: Least-privilege permissions scoped to specific resources
auth_role_policy = aws.iam.RolePolicy(
    "cognito-auth-role-policy",
    role=auth_role.name,
    policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["s3:GetObject"],
                "Resource": (
                    f"arn:aws:s3:::{photos_bucket}"
                    "/${cognito-identity.amazonaws.com:sub}/*"
                ),
            },
            {
                "Effect": "Allow",
                "Action": ["s3:PutObject"],
                "Resource": (
                    f"arn:aws:s3:::{photos_bucket}"
                    "/${cognito-identity.amazonaws.com:sub}/*"
                ),
                "Condition": {
                    "StringEquals": {"s3:x-amz-acl": "private"},
                },
            },
        ],
    }),
)
```

---

### SEC-AUTHZ-007: Sequential/Predictable Resource IDs

- **Severity:** MEDIUM
- **Category:** Authorization & Access Control
- **Description:** Using auto-incrementing or sequential integers as resource IDs makes Broken Object-Level Authorization (BOLA) exploitation trivial. Attackers can enumerate all resources by incrementing the ID.
- **Detection Regex:** `(auto_increment|serial|nextval|count\s*\+\s*1)` or `id\s*=\s*\d+`
- **Impact:** Trivial enumeration of all resources when combined with BOLA vulnerabilities.
- **CWE:** CWE-330 (Use of Insufficiently Random Values)
- **OWASP:** API1:2023 - Broken Object Level Authorization

**Vulnerable Pattern:**

```python
# VULNERABLE: Sequential IDs allow trivial enumeration
_counter = 0

async def create_trail(name: str, tenant_id: str) -> str:
    global _counter
    _counter += 1
    trail_id = str(_counter)  # 1, 2, 3, 4... easy to guess

    await table.put_item(Item={
        "tenant_id": tenant_id,
        "id": trail_id,
        "name": name,
    })
    return trail_id
```

**Secure Pattern:**

```python
from uuid import uuid4

async def create_trail(name: str, tenant_id: str) -> str:
    # SECURE: UUIDv4 - 122 bits of randomness, infeasible to enumerate
    trail_id = str(uuid4())

    await table.put_item(Item={
        "tenant_id": tenant_id,
        "id": trail_id,
        "name": name,
    })
    return trail_id
```

---

## Category 3: Input Validation & Injection

### SEC-INJ-001: DynamoDB FilterExpression Injection

- **Severity:** CRITICAL
- **Category:** Input Validation & Injection
- **Description:** User input concatenated or formatted directly into DynamoDB `FilterExpression` strings. Unlike SQL injection, DynamoDB injection can manipulate filter conditions to bypass authorization or extract data.
- **Detection Regex:** `FilterExpression\s*=\s*f["']` or `FilterExpression.*\.format\(`
- **Impact:** Data exfiltration, authorization bypass, or denial of service through malformed expressions.
- **CWE:** CWE-943 (Improper Neutralization of Special Elements in Data Query Logic)
- **OWASP:** A05:2021 - Security Misconfiguration

**Vulnerable Pattern:**

```python
import aioboto3

async def search_trails(tenant_id: str, trail_name: str):
    session = aioboto3.Session()
    async with session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table("trails")
        # VULNERABLE: User input directly in FilterExpression
        response = await table.query(
            KeyConditionExpression="tenant_id = :tid",
            FilterExpression=f"trail_name = {trail_name}",
            ExpressionAttributeValues={":tid": tenant_id},
        )
        return response["Items"]
```

**Secure Pattern:**

```python
import aioboto3

async def search_trails(tenant_id: str, trail_name: str):
    session = aioboto3.Session()
    async with session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table("trails")
        # SECURE: Parameterized expression with ExpressionAttributeValues
        response = await table.query(
            KeyConditionExpression="tenant_id = :tid",
            FilterExpression="trail_name = :tname",
            ExpressionAttributeValues={
                ":tid": tenant_id,
                ":tname": trail_name,
            },
        )
        return response["Items"]
```

---

### SEC-INJ-002: DynamoDB KeyConditionExpression Injection

- **Severity:** CRITICAL
- **Category:** Input Validation & Injection
- **Description:** User input concatenated into `KeyConditionExpression`. This directly controls which partition and sort key ranges are queried, potentially allowing access to other tenants' partitions.
- **Detection Regex:** `KeyConditionExpression\s*=\s*f["']` or `KeyConditionExpression.*\.format\(`
- **Impact:** Cross-tenant data access by injecting different partition key values.
- **CWE:** CWE-943 (Improper Neutralization of Special Elements in Data Query Logic)
- **OWASP:** A05:2021 - Security Misconfiguration

**Vulnerable Pattern:**

```python
import aioboto3

async def get_trails_by_date(tenant_id: str, date_range: str):
    session = aioboto3.Session()
    async with session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table("trails")
        # VULNERABLE: User input in KeyConditionExpression
        response = await table.query(
            KeyConditionExpression=f"tenant_id = :tid AND created_at {date_range}",
            ExpressionAttributeValues={":tid": tenant_id},
        )
        return response["Items"]
```

**Secure Pattern:**

```python
import aioboto3
from boto3.dynamodb.conditions import Key

async def get_trails_by_date(tenant_id: str, start_date: str, end_date: str):
    session = aioboto3.Session()
    async with session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table("trails")
        # SECURE: Using boto3 condition builder - parameterized by design
        response = await table.query(
            KeyConditionExpression=(
                Key("tenant_id").eq(tenant_id)
                & Key("created_at").between(start_date, end_date)
            ),
        )
        return response["Items"]
```

---

### SEC-INJ-003: DynamoDB Scan Condition Injection

- **Severity:** HIGH
- **Category:** Input Validation & Injection
- **Description:** Scan operations with injected filter conditions are particularly dangerous because scans examine every item in the table. A manipulated condition can cause the scan to return all items across all tenants.
- **Detection Regex:** `\.scan\(.*FilterExpression\s*=\s*[^A]` or `scan.*f["']`
- **Impact:** Full table data exfiltration. Scans touch every item, maximizing data exposure.
- **CWE:** CWE-943 (Improper Neutralization of Special Elements in Data Query Logic)
- **OWASP:** A05:2021 - Security Misconfiguration

**Vulnerable Pattern:**

```python
import aioboto3

async def search_all_trails(search_term: str):
    session = aioboto3.Session()
    async with session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table("trails")
        # VULNERABLE: Unparameterized scan with user input
        response = await table.scan(
            FilterExpression=f"contains(description, {search_term})",
        )
        return response["Items"]
```

**Secure Pattern:**

```python
import aioboto3
from boto3.dynamodb.conditions import Attr

async def search_trails_for_tenant(tenant_id: str, search_term: str):
    session = aioboto3.Session()
    async with session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table("trails")
        # SECURE: Use query (not scan) + parameterized filter + tenant scoping
        response = await table.query(
            KeyConditionExpression="tenant_id = :tid",
            FilterExpression=Attr("description").contains(search_term),
            ExpressionAttributeValues={":tid": tenant_id},
        )
        return response["Items"]
```

---

### SEC-INJ-004: Path Traversal

- **Severity:** HIGH
- **Category:** Input Validation & Injection
- **Description:** Using `os.path.join()` with user-supplied filenames containing `../` sequences. `os.path.join("/uploads", "../etc/passwd")` resolves to `/etc/passwd`, allowing access to arbitrary files.
- **Detection Regex:** `os\.path\.join\(.*request` or `open\(.*request\.(filename|path)`
- **Impact:** Arbitrary file read/write outside intended directory.
- **CWE:** CWE-22 (Improper Limitation of a Pathname to a Restricted Directory)
- **OWASP:** A05:2021 - Security Misconfiguration

**Vulnerable Pattern:**

```python
import os
from fastapi import APIRouter, UploadFile

router = APIRouter()

UPLOAD_DIR = "/tmp/uploads"

@router.post("/upload")
async def upload_file(file: UploadFile):
    # VULNERABLE: "../../../etc/passwd" bypasses upload directory
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)
    return {"path": filepath}
```

**Secure Pattern:**

```python
from pathlib import Path
from werkzeug.utils import secure_filename
from fastapi import APIRouter, HTTPException, UploadFile

router = APIRouter()

UPLOAD_DIR = Path("/tmp/uploads")

@router.post("/upload")
async def upload_file(file: UploadFile):
    # SECURE: Strip path components, validate result is within upload dir
    safe_name = secure_filename(file.filename)
    if not safe_name:
        raise HTTPException(status_code=400, detail="Invalid filename")

    filepath = UPLOAD_DIR / safe_name

    # SECURE: Verify resolved path is within upload directory
    if not filepath.resolve().is_relative_to(UPLOAD_DIR.resolve()):
        raise HTTPException(status_code=400, detail="Invalid file path")

    content = await file.read()
    filepath.write_bytes(content)
    return {"path": str(filepath)}
```

---

### SEC-INJ-005: OS Command Injection

- **Severity:** CRITICAL
- **Category:** Input Validation & Injection
- **Description:** Using `subprocess` with `shell=True` and user-controlled input. The shell interprets metacharacters like `;`, `|`, `&&`, and backticks, allowing arbitrary command execution.
- **Detection Regex:** `subprocess\.(run|call|Popen)\(.*shell\s*=\s*True`
- **Impact:** Remote code execution. Attacker can run any OS command with application privileges.
- **CWE:** CWE-78 (Improper Neutralization of Special Elements used in an OS Command)
- **OWASP:** A05:2021 - Security Misconfiguration

**Vulnerable Pattern:**

```python
import subprocess
from fastapi import APIRouter

router = APIRouter()

@router.post("/photos/resize")
async def resize_photo(filename: str, width: int, height: int):
    # VULNERABLE: shell=True with user input
    # Attacker sends filename="photo.jpg; rm -rf /"
    subprocess.run(
        f"convert {filename} -resize {width}x{height} output.jpg",
        shell=True,
    )
    return {"message": "Resized"}
```

**Secure Pattern:**

```python
import subprocess
from pathlib import Path
from werkzeug.utils import secure_filename
from fastapi import APIRouter, HTTPException

router = APIRouter()

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

@router.post("/photos/resize")
async def resize_photo(filename: str, width: int, height: int):
    # SECURE: Validate input, use array form (no shell interpretation)
    safe_name = secure_filename(filename)
    if not safe_name or Path(safe_name).suffix.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid filename")

    if not (1 <= width <= 4096 and 1 <= height <= 4096):
        raise HTTPException(status_code=400, detail="Invalid dimensions")

    result = subprocess.run(
        ["convert", safe_name, "-resize", f"{width}x{height}", "output.jpg"],
        shell=False,  # No shell interpretation
        capture_output=True,
        timeout=30,
    )
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail="Resize failed")

    return {"message": "Resized"}
```

---

### SEC-INJ-006: Server-Side Request Forgery (SSRF)

- **Severity:** HIGH
- **Category:** Input Validation & Injection
- **Description:** HTTP requests made with user-controlled URLs. In AWS environments, attackers can access the Instance Metadata Service (IMDS) at `169.254.169.254` to steal IAM role credentials.
- **Detection Regex:** `(requests\.get|httpx\.get|aiohttp.*get)\(.*request\.(body|query|json)`
- **Impact:** AWS credential theft via IMDS, internal network scanning, access to internal services.
- **CWE:** CWE-918 (Server-Side Request Forgery)
- **OWASP:** A05:2021 - Security Misconfiguration

**Vulnerable Pattern:**

```python
import httpx
from fastapi import APIRouter

router = APIRouter()

@router.post("/fetch-preview")
async def fetch_url_preview(url: str):
    # VULNERABLE: Attacker provides url=http://169.254.169.254/latest/meta-data/iam/
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return {"content": response.text}
```

**Secure Pattern:**

```python
import ipaddress
import socket
import httpx
from urllib.parse import urlparse
from fastapi import APIRouter, HTTPException

router = APIRouter()

ALLOWED_SCHEMES = {"https"}
BLOCKED_IP_RANGES = [
    ipaddress.ip_network("169.254.0.0/16"),   # Link-local / IMDS
    ipaddress.ip_network("10.0.0.0/8"),        # Private
    ipaddress.ip_network("172.16.0.0/12"),     # Private
    ipaddress.ip_network("192.168.0.0/16"),    # Private
    ipaddress.ip_network("127.0.0.0/8"),       # Loopback
    ipaddress.ip_network("0.0.0.0/8"),         # Current network
]

async def validate_url(url: str) -> str:
    """Validate URL is safe for server-side fetch."""
    parsed = urlparse(url)
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise HTTPException(status_code=400, detail="Only HTTPS URLs allowed")

    # Resolve hostname to IP and check against blocked ranges
    try:
        ip = ipaddress.ip_address(socket.gethostbyname(parsed.hostname))
    except (socket.gaierror, ValueError) as exc:
        raise HTTPException(status_code=400, detail="Invalid URL") from exc

    for blocked_range in BLOCKED_IP_RANGES:
        if ip in blocked_range:
            raise HTTPException(status_code=400, detail="URL not allowed")

    return url

@router.post("/fetch-preview")
async def fetch_url_preview(url: str):
    # SECURE: URL validated against allowlist and blocked IP ranges
    safe_url = await validate_url(url)
    async with httpx.AsyncClient(follow_redirects=False, timeout=5.0) as client:
        response = await client.get(safe_url)
    return {"content": response.text[:1000]}  # Limit response size
```

---

### SEC-INJ-007: Server-Side Template Injection

- **Severity:** CRITICAL
- **Category:** Input Validation & Injection
- **Description:** User input passed directly to Jinja2 `Template()` constructor. Jinja2 templates can execute arbitrary Python code via `{{ config.__class__.__init__.__globals__ }}` and similar expressions.
- **Detection Regex:** `Template\(.*request` or `Template\(.*user_input`
- **Impact:** Remote code execution. Attacker can execute arbitrary Python code on the server.
- **CWE:** CWE-1336 (Improper Neutralization of Special Elements Used in a Template Engine)
- **OWASP:** A05:2021 - Security Misconfiguration

**Vulnerable Pattern:**

```python
from jinja2 import Template
from fastapi import APIRouter

router = APIRouter()

@router.post("/notifications/render")
async def render_notification(template_text: str, context: dict):
    # VULNERABLE: User input as template source
    # Attacker sends: "{{ config.__class__.__init__.__globals__['os'].popen('id').read() }}"
    template = Template(template_text)
    rendered = template.render(**context)
    return {"rendered": rendered}
```

**Secure Pattern:**

```python
from jinja2 import FileSystemLoader, SandboxedEnvironment, select_autoescape
from fastapi import APIRouter, HTTPException

router = APIRouter()

# SECURE: Templates loaded from filesystem, not user input
env = SandboxedEnvironment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html", "xml"]),
)

ALLOWED_TEMPLATES = {"trail_update", "welcome", "password_reset"}

@router.post("/notifications/render")
async def render_notification(template_name: str, context: dict):
    if template_name not in ALLOWED_TEMPLATES:
        raise HTTPException(status_code=400, detail="Invalid template")

    # SECURE: Fixed template from filesystem, user data only in context
    template = env.get_template(f"{template_name}.html")
    rendered = template.render(**context)
    return {"rendered": rendered}
```

---

### SEC-INJ-008: Python Code Injection via eval/exec

- **Severity:** CRITICAL
- **Category:** Input Validation & Injection
- **Description:** Using `eval()` or `exec()` with user-controlled input allows arbitrary Python code execution. Even `ast.literal_eval()` should be used cautiously and only for literal data structures.
- **Detection Regex:** `eval\(.*request` or `exec\(.*request` or `eval\(.*user`
- **Impact:** Remote code execution. Attacker can execute any Python code on the server.
- **CWE:** CWE-95 (Improper Neutralization of Directives in Dynamically Evaluated Code)
- **OWASP:** A05:2021 - Security Misconfiguration

**Vulnerable Pattern:**

```python
from fastapi import APIRouter

router = APIRouter()

@router.post("/calculate")
async def calculate(expression: str):
    # VULNERABLE: eval with user input
    # Attacker: expression="__import__('os').system('rm -rf /')"
    result = eval(expression)
    return {"result": result}

@router.post("/filter")
async def apply_filter(filter_code: str, data: list):
    # VULNERABLE: exec with user input
    local_vars = {"data": data}
    exec(f"result = [x for x in data if {filter_code}]", {}, local_vars)
    return {"filtered": local_vars.get("result")}
```

**Secure Pattern:**

```python
import ast
import operator
from fastapi import APIRouter, HTTPException

router = APIRouter()

# SECURE: Whitelist of allowed operations for safe math evaluation
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

def safe_eval_math(expression: str) -> float:
    """Evaluate simple math expressions without eval()."""
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError("Invalid expression") from exc

    def _eval_node(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return _eval_node(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.BinOp) and type(node.op) in SAFE_OPERATORS:
            left = _eval_node(node.left)
            right = _eval_node(node.right)
            return SAFE_OPERATORS[type(node.op)](left, right)
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")

    return _eval_node(tree)

@router.post("/calculate")
async def calculate(expression: str):
    try:
        result = safe_eval_math(expression)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"result": result}
```

---

### SEC-INJ-009: Regular Expression Denial of Service (ReDoS)

- **Severity:** MEDIUM
- **Category:** Input Validation & Injection
- **Description:** Regular expressions with nested quantifiers (e.g., `(a+)+`, `(a|a)*`) cause catastrophic backtracking. A carefully crafted input string can cause exponential time complexity, freezing the server.
- **Detection Regex:** `re\.(compile|match|search)\(.*(\.\*\+|\.\+\*|\([^)]*\+\)[^)]*\+)`
- **Impact:** Denial of service. Single request can consume 100% CPU for minutes/hours.
- **CWE:** CWE-1333 (Inefficient Regular Expression Complexity)
- **OWASP:** A05:2021 - Security Misconfiguration

**Vulnerable Pattern:**

```python
import re
from fastapi import APIRouter

router = APIRouter()

# VULNERABLE: Nested quantifiers cause catastrophic backtracking
# Input "aaaaaaaaaaaaaaaaaaaaaaaaaab" takes exponential time
EMAIL_REGEX = re.compile(r"^([a-zA-Z0-9_.+-]+)+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$")

@router.post("/validate-email")
async def validate_email(email: str):
    if EMAIL_REGEX.match(email):
        return {"valid": True}
    return {"valid": False}
```

**Secure Pattern:**

```python
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

router = APIRouter()

# SECURE: Use Pydantic's EmailStr for email validation (no regex needed)
class EmailInput(BaseModel):
    email: EmailStr

@router.post("/validate-email")
async def validate_email(input_data: EmailInput):
    return {"valid": True, "email": input_data.email}

# If regex is needed, avoid nested quantifiers
# SECURE: No nested quantifiers, linear backtracking
import re
SAFE_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$")
```

---

### SEC-INJ-010: HTTP Header Injection

- **Severity:** HIGH
- **Category:** Input Validation & Injection
- **Description:** User input containing CRLF (`\r\n`) characters injected into HTTP response headers. This can inject arbitrary headers or even inject a complete response body (HTTP response splitting).
- **Detection Regex:** `Response.*headers.*request` or `headers\[.*\]\s*=\s*.*request`
- **Impact:** Cache poisoning, XSS via injected headers, session fixation via Set-Cookie injection.
- **CWE:** CWE-113 (Improper Neutralization of CRLF Sequences in HTTP Headers)
- **OWASP:** A05:2021 - Security Misconfiguration

**Vulnerable Pattern:**

```python
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/redirect")
async def redirect_with_header(request: Request):
    # VULNERABLE: User input in header value
    # Attacker: location="http://evil.com\r\nSet-Cookie: session=attacker_token"
    location = request.query_params.get("next", "/")
    response = JSONResponse({"redirect": location})
    response.headers["X-Redirect-Target"] = location  # CRLF injection
    return response
```

**Secure Pattern:**

```python
import re
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

router = APIRouter()

CRLF_PATTERN = re.compile(r"[\r\n]")

def sanitize_header_value(value: str) -> str:
    """Strip CRLF characters from header values."""
    return CRLF_PATTERN.sub("", value)

@router.get("/redirect")
async def redirect_with_header(request: Request):
    location = request.query_params.get("next", "/")

    # SECURE: Validate against allowlist and strip CRLF
    if not location.startswith("/"):
        raise HTTPException(status_code=400, detail="Invalid redirect target")

    safe_location = sanitize_header_value(location)
    response = JSONResponse({"redirect": safe_location})
    response.headers["X-Redirect-Target"] = safe_location
    return response
```

---

### SEC-INJ-011: Mass Assignment via Pydantic Models

- **Severity:** HIGH
- **Category:** Input Validation & Injection
- **Description:** Pydantic request models that include internal-only fields (like `role`, `is_admin`, `tenant_id`, or `created_by`) allow attackers to set these fields by including them in the request body.
- **Detection Regex:** Pydantic models with `(role|is_admin|tenant_id|internal)` used as request body type
- **Impact:** Privilege escalation, tenant isolation bypass, data integrity violations.
- **CWE:** CWE-915 (Improperly Controlled Modification of Dynamically-Determined Object Attributes)
- **OWASP:** API3:2023 - Broken Object Property Level Authorization

**Vulnerable Pattern:**

```python
from pydantic import BaseModel
from fastapi import APIRouter

# VULNERABLE: Single model used for both input and storage
class TrailSystem(BaseModel):
    name: str
    description: str
    tenant_id: str          # Internal field - should not be user-settable
    created_by: str         # Internal field
    status: str = "active"  # Internal field

router = APIRouter()

@router.post("/trail-systems")
async def create_trail_system(trail_system: TrailSystem):
    # Attacker sets tenant_id to another org's ID
    await repo.create(trail_system.model_dump())
```

**Secure Pattern:**

```python
from uuid import uuid4
from pydantic import BaseModel
from fastapi import APIRouter, Depends

# SECURE: Separate models for input vs storage
class TrailSystemCreateRequest(BaseModel):
    """Fields the client is allowed to set."""
    name: str
    description: str

class TrailSystemRecord(BaseModel):
    """Full record including server-set fields."""
    id: str
    name: str
    description: str
    tenant_id: str
    created_by: str
    status: str

router = APIRouter()

@router.post("/trail-systems")
async def create_trail_system(
    request: TrailSystemCreateRequest,
    user: AuthenticatedUser = Depends(get_current_user),
):
    # SECURE: Server sets internal fields from verified JWT claims
    record = TrailSystemRecord(
        id=str(uuid4()),
        name=request.name,
        description=request.description,
        tenant_id=user.org_id,
        created_by=user.id,
        status="active",
    )
    await repo.create(record.model_dump())
    return TrailSystemResponse(**record.model_dump())
```

---

### SEC-INJ-012: Unsafe Deserialization

- **Severity:** CRITICAL
- **Category:** Input Validation & Injection
- **Description:** Using `pickle.loads()`, `pickle.load()`, `yaml.load()` (without SafeLoader), or `shelve.open()` on untrusted input. Python pickle can execute arbitrary code during deserialization.
- **Detection Regex:** `pickle\.(loads|load)\(` or `yaml\.load\((?!.*SafeLoader|.*safe_load)` or `shelve\.open\(`
- **Impact:** Remote code execution. Attacker can execute arbitrary Python code on deserialization.
- **CWE:** CWE-502 (Deserialization of Untrusted Data)
- **OWASP:** A08:2021 - Software and Data Integrity Failures

**Vulnerable Pattern:**

```python
import pickle
import yaml
from fastapi import APIRouter

router = APIRouter()

@router.post("/import-data")
async def import_data(data: bytes):
    # VULNERABLE: pickle.loads can execute arbitrary code
    imported = pickle.loads(data)
    return {"imported": len(imported)}

@router.post("/import-config")
async def import_config(config_yaml: str):
    # VULNERABLE: yaml.load without SafeLoader can execute Python
    config = yaml.load(config_yaml)
    return {"config": config}
```

**Secure Pattern:**

```python
import json
import yaml
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/import-data")
async def import_data(data: str):
    # SECURE: JSON is safe - no code execution during parsing
    try:
        imported = json.loads(data)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="Invalid JSON") from exc
    return {"imported": len(imported)}

@router.post("/import-config")
async def import_config(config_yaml: str):
    # SECURE: yaml.safe_load only allows basic types
    try:
        config = yaml.safe_load(config_yaml)
    except yaml.YAMLError as exc:
        raise HTTPException(status_code=400, detail="Invalid YAML") from exc
    return {"config": config}
```

---

### SEC-INJ-013: X-Forwarded-For Spoofing

- **Severity:** MEDIUM
- **Category:** Input Validation & Injection
- **Description:** Trusting the `X-Forwarded-For` header for IP-based authorization or rate limiting. This header is trivially spoofable by clients unless the proxy/load balancer strips and resets it.
- **Detection Regex:** `request\.headers\[["']x-forwarded-for["']\]` used for auth or rate limiting
- **Impact:** IP-based access control bypass, rate limiting bypass, audit log poisoning.
- **CWE:** CWE-290 (Authentication Bypass by Spoofing)
- **OWASP:** A07:2021 - Identification and Authentication Failures

**Vulnerable Pattern:**

```python
from fastapi import APIRouter, Request, HTTPException

router = APIRouter()

ADMIN_IP_ALLOWLIST = {"10.0.1.50", "10.0.1.51"}

@router.get("/admin/dashboard")
async def admin_dashboard(request: Request):
    # VULNERABLE: X-Forwarded-For is client-controlled
    # Attacker sends: X-Forwarded-For: 10.0.1.50
    client_ip = request.headers.get("x-forwarded-for", "").split(",")[0].strip()
    if client_ip not in ADMIN_IP_ALLOWLIST:
        raise HTTPException(status_code=403, detail="IP not allowed")
    return {"dashboard": "data"}
```

**Secure Pattern:**

```python
import json
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

async def get_trusted_client_ip(request: Request) -> str:
    """Extract client IP from trusted proxy chain.

    API Gateway sets X-Forwarded-For with the actual client IP
    as the rightmost untrusted address. In AWS API Gateway + Lambda,
    use the sourceIp from requestContext instead.
    """
    # SECURE: Use API Gateway's verified source IP
    # In Lambda context, this comes from the event's requestContext
    aws_event = request.scope.get("aws.event", {})
    source_ip = (
        aws_event
        .get("requestContext", {})
        .get("identity", {})
        .get("sourceIp")
    )

    if source_ip:
        return source_ip

    # Fallback: use the direct connection IP (not X-Forwarded-For)
    return request.client.host

@router.get("/admin/dashboard")
async def admin_dashboard(
    admin: AuthenticatedUser = Depends(require_admin),
):
    # SECURE: Use JWT-based auth instead of IP allowlist
    return {"dashboard": "data"}
```

---

## Category 4: Cryptographic Failures

### SEC-CRYPTO-001: Hardcoded AWS Access Keys

- **Severity:** CRITICAL
- **Category:** Cryptographic Failures
- **Description:** AWS access key IDs (`AKIA...`) and secret access keys hardcoded in source code. These are immediately exploitable if the repository is public or if any developer's machine is compromised.
- **Detection Regex:** `AKIA[0-9A-Z]{16}` or `aws_secret_access_key\s*=\s*["']`
- **Impact:** Full AWS account compromise. Attacker can access all services the key has permissions for.
- **CWE:** CWE-798 (Use of Hard-coded Credentials)
- **OWASP:** A04:2021 - Insecure Design

**Vulnerable Pattern:**

```python
import aioboto3

# VULNERABLE: AWS credentials in source code
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

async def get_dynamo_table():
    session = aioboto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    async with session.resource("dynamodb") as dynamodb:
        return await dynamodb.Table("trails")
```

**Secure Pattern:**

```python
import aioboto3

# SECURE: Use IAM roles (Lambda execution role) - no credentials in code
# AWS SDK automatically uses the Lambda execution role
session = aioboto3.Session()

async def get_dynamo_table():
    # SECURE: Credentials come from Lambda execution role via STS
    async with session.resource("dynamodb") as dynamodb:
        return await dynamodb.Table("trails")
```

---

### SEC-CRYPTO-002: Weak Random Number Generation

- **Severity:** HIGH
- **Category:** Cryptographic Failures
- **Description:** Using the `random` module for security-sensitive operations (tokens, passwords, session IDs). The `random` module uses a Mersenne Twister PRNG that is not cryptographically secure and can be predicted after observing 624 outputs.
- **Detection Regex:** `random\.(randint|choice|randrange|random|sample)\(` in security context
- **Impact:** Predictable tokens, session IDs, or passwords. Attacker can predict future values.
- **CWE:** CWE-330 (Use of Insufficiently Random Values)
- **OWASP:** A04:2021 - Insecure Design

**Vulnerable Pattern:**

```python
import random
import string

def generate_api_key() -> str:
    # VULNERABLE: random module is predictable (Mersenne Twister)
    # Attacker who observes 624 consecutive outputs can predict all future values
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=32))

def generate_reset_token() -> str:
    # VULNERABLE: Predictable password reset token
    return str(random.randint(100000, 999999))
```

**Secure Pattern:**

```python
import secrets

def generate_api_key() -> str:
    # SECURE: secrets module uses OS-level CSPRNG
    return secrets.token_urlsafe(32)

def generate_reset_token() -> str:
    # SECURE: Cryptographically random 6-digit code
    return f"{secrets.randbelow(1000000):06d}"
```

---

### SEC-CRYPTO-003: Missing Encryption at Rest

- **Severity:** HIGH
- **Category:** Cryptographic Failures
- **Description:** DynamoDB tables, S3 buckets, or other data stores created without encryption at rest. Data stored in plaintext on disk is vulnerable if physical media is compromised or if snapshots/backups are improperly secured.
- **Detection Regex:** `Table\((?!.*SSESpecification|.*sse_specification)` or `Bucket\((?!.*ServerSideEncryption)`
- **Impact:** Data exposure if physical media or backup snapshots are compromised.
- **CWE:** CWE-311 (Missing Encryption of Sensitive Data)
- **OWASP:** A04:2021 - Insecure Design

**Vulnerable Pattern:**

```python
# Pulumi infrastructure code
import pulumi_aws as aws

# VULNERABLE: No encryption configuration - data stored in plaintext
table = aws.dynamodb.Table(
    "trails",
    name="trails",
    attributes=[
        {"name": "tenant_id", "type": "S"},
        {"name": "id", "type": "S"},
    ],
    hash_key="tenant_id",
    range_key="id",
    billing_mode="PAY_PER_REQUEST",
)
```

**Secure Pattern:**

```python
# Pulumi infrastructure code
import pulumi_aws as aws

# SECURE: AWS-managed encryption at rest enabled
table = aws.dynamodb.Table(
    "trails",
    name="trails",
    attributes=[
        {"name": "tenant_id", "type": "S"},
        {"name": "id", "type": "S"},
    ],
    hash_key="tenant_id",
    range_key="id",
    billing_mode="PAY_PER_REQUEST",
    server_side_encryption=aws.dynamodb.TableServerSideEncryptionArgs(
        enabled=True,
    ),
    point_in_time_recovery=aws.dynamodb.TablePointInTimeRecoveryArgs(
        enabled=True,
    ),
)
```

---

### SEC-CRYPTO-004: Hardcoded Database Credentials

- **Severity:** CRITICAL
- **Category:** Cryptographic Failures
- **Description:** Database passwords, connection strings, or API keys hardcoded in application source code. Compromised source code or repository access immediately exposes all credentials.
- **Detection Regex:** `(password|passwd|db_pass)\s*=\s*["'][^"']+["']` or `(connection_string|DATABASE_URL)\s*=\s*["']`
- **Impact:** Direct database access if source code is leaked.
- **CWE:** CWE-798 (Use of Hard-coded Credentials)
- **OWASP:** A04:2021 - Insecure Design

**Vulnerable Pattern:**

```python
# VULNERABLE: Database credentials in source code
DB_HOST = "prod-db.cluster-abc123.us-east-1.rds.amazonaws.com"
DB_PASSWORD = "SuperSecretPassword123!"
DB_CONNECTION_STRING = f"postgresql://admin:{DB_PASSWORD}@{DB_HOST}:5432/traillens"

async def get_db_connection():
    return await asyncpg.connect(DB_CONNECTION_STRING)
```

**Secure Pattern:**

```python
import json
import aioboto3

_db_credentials: dict | None = None

async def _get_db_credentials() -> dict:
    """Retrieve database credentials from AWS Secrets Manager."""
    global _db_credentials
    if _db_credentials is None:
        session = aioboto3.Session()
        async with session.client("secretsmanager") as client:
            response = await client.get_secret_value(
                SecretId="traillens/prod/db-credentials",
            )
            _db_credentials = json.loads(response["SecretString"])
    return _db_credentials

async def get_db_connection():
    # SECURE: Credentials from Secrets Manager, rotated automatically
    creds = await _get_db_credentials()
    return await asyncpg.connect(
        host=creds["host"],
        port=creds["port"],
        user=creds["username"],
        password=creds["password"],
        database=creds["dbname"],
        ssl="require",
    )
```

---

### SEC-CRYPTO-005: Non-Constant-Time Comparison

- **Severity:** MEDIUM
- **Category:** Cryptographic Failures
- **Description:** Using `==` to compare secrets, tokens, or API keys. The `==` operator short-circuits on the first different byte, leaking information about the secret through timing differences. Attackers can determine the correct value one character at a time.
- **Detection Regex:** `(secret|token|api_key|password_hash)\s*==\s*`
- **Impact:** Secret recovery through timing side-channel. Attacker determines correct value character by character.
- **CWE:** CWE-208 (Observable Timing Discrepancy)
- **OWASP:** A04:2021 - Insecure Design

**Vulnerable Pattern:**

```python
from fastapi import APIRouter, HTTPException, Header

router = APIRouter()

@router.get("/webhook")
async def handle_webhook(x_webhook_secret: str = Header()):
    stored_secret = await get_webhook_secret()
    # VULNERABLE: == short-circuits on first different byte
    # Timing difference reveals how many leading bytes match
    if x_webhook_secret == stored_secret:
        return {"status": "accepted"}
    raise HTTPException(status_code=401, detail="Invalid secret")
```

**Secure Pattern:**

```python
import hmac
from fastapi import APIRouter, HTTPException, Header

router = APIRouter()

@router.get("/webhook")
async def handle_webhook(x_webhook_secret: str = Header()):
    stored_secret = await get_webhook_secret()
    # SECURE: Constant-time comparison - always compares all bytes
    if hmac.compare_digest(
        x_webhook_secret.encode("utf-8"),
        stored_secret.encode("utf-8"),
    ):
        return {"status": "accepted"}
    raise HTTPException(status_code=401, detail="Invalid secret")
```

---

### SEC-CRYPTO-006: Secrets in Lambda Environment Variables

- **Severity:** HIGH
- **Category:** Cryptographic Failures
- **Description:** Storing secrets (API keys, passwords, tokens) in Lambda environment variables. Environment variables are visible in the Lambda console, CloudFormation templates, and CloudTrail logs. They persist in memory across invocations.
- **Detection Regex:** `os\.environ\[["'](SECRET|KEY|PASSWORD|TOKEN|API_KEY)` or `os\.getenv\(["'](SECRET|KEY|PASSWORD)`
- **Impact:** Secret exposure via AWS Console, CloudFormation, CloudTrail, or memory dumps.
- **CWE:** CWE-321 (Use of Hard-coded Cryptographic Key)
- **OWASP:** A04:2021 - Insecure Design

**Vulnerable Pattern:**

```python
import os

# VULNERABLE: Secrets stored as environment variables
# Visible in Lambda console, CloudFormation, CloudTrail
STRIPE_API_KEY = os.environ["STRIPE_API_KEY"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
JWT_SECRET = os.getenv("JWT_SECRET")

async def process_payment(amount: float):
    return await stripe.charge(api_key=STRIPE_API_KEY, amount=amount)
```

**Secure Pattern:**

```python
import os
import aioboto3

_secrets_cache: dict[str, str] = {}

async def get_secret(secret_id: str) -> str:
    """Retrieve secret from AWS Secrets Manager with caching."""
    if secret_id not in _secrets_cache:
        session = aioboto3.Session()
        async with session.client("secretsmanager") as client:
            response = await client.get_secret_value(SecretId=secret_id)
            _secrets_cache[secret_id] = response["SecretString"]
    return _secrets_cache[secret_id]

# SECURE: Only the secret ARN/name in environment variable
STRIPE_SECRET_ID = os.environ.get("STRIPE_SECRET_ID", "traillens/prod/stripe")

async def process_payment(amount: float):
    api_key = await get_secret(STRIPE_SECRET_ID)
    return await stripe.charge(api_key=api_key, amount=amount)
```

---

## Category 5: PII & Data Protection

### SEC-PII-001: PII in Application Logs

- **Severity:** HIGH
- **Category:** PII & Data Protection
- **Description:** Personally Identifiable Information (email addresses, phone numbers, IP addresses, names) logged to CloudWatch or other log systems. Log data is often retained for extended periods, shared across teams, and may be processed by third-party tools.
- **Detection Regex:** `(log|logger)\.(info|debug|error)\(.*\b(email|phone|ssn|password|name)\b`
- **Impact:** PII exposure in logs accessible to operations teams, third-party log aggregators, or compliance violations (GDPR/CCPA).
- **CWE:** CWE-532 (Insertion of Sensitive Information into Log File)
- **OWASP:** A09:2021 - Security Logging and Monitoring Failures

**Vulnerable Pattern:**

```python
from api.shared.logging import log_info, log_error

async def create_user(email: str, phone: str, name: str):
    # VULNERABLE: PII in log messages - visible in CloudWatch
    log_info(f"Creating user: {name}, email: {email}, phone: {phone}")

    user = await user_repo.create(email=email, phone=phone, name=name)

    log_info(f"User created successfully: {email} from {request.client.host}")
    return user
```

**Secure Pattern:**

```python
from api.shared.logging import log_info

async def create_user(email: str, phone: str, name: str):
    # SECURE: Only non-PII identifiers in logs
    log_info("Creating user", metadata={"request_id": correlation_id})

    user = await user_repo.create(email=email, phone=phone, name=name)

    log_info("User created successfully", metadata={"user_id": user.id})
    return user
```

---

### SEC-PII-002: PII in Error Responses

- **Severity:** HIGH
- **Category:** PII & Data Protection
- **Description:** Error responses that include PII such as email addresses, user names, or internal identifiers. These responses are visible to attackers and may be cached by intermediaries.
- **Detection Regex:** `HTTPException\(.*\b(email|phone|user|name)\b` or `JSONResponse\(.*\b(email|name)\b`
- **Impact:** User data leakage to attackers, cached PII in CDN/proxy layers.
- **CWE:** CWE-209 (Generation of Error Message Containing Sensitive Information)
- **OWASP:** A10:2021 - Server-Side Request Forgery (grouped with information disclosure)

**Vulnerable Pattern:**

```python
from fastapi import HTTPException

async def get_user_by_email(email: str):
    user = await user_repo.find_by_email(email)
    if not user:
        # VULNERABLE: Confirms email existence/non-existence to attacker
        raise HTTPException(
            status_code=404,
            detail=f"User with email {email} not found",
        )
    return user
```

**Secure Pattern:**

```python
from fastapi import HTTPException
from api.shared.logging import log_info

async def get_user_by_email(email: str):
    user = await user_repo.find_by_email(email)
    if not user:
        # SECURE: Generic error message, details in server-side logs only
        log_info("User lookup failed", metadata={"lookup_type": "email"})
        raise HTTPException(
            status_code=404,
            detail="Resource not found",
        )
    return user
```

---

### SEC-PII-003: Missing Data Masking

- **Severity:** MEDIUM
- **Category:** PII & Data Protection
- **Description:** API responses returning full PII fields (complete email, phone number, SSN) when only partial information is needed for display. Over-exposing data increases the impact of any response interception.
- **Detection Regex:** `return.*model_dump\(\)` without field filtering or `return.*response\["Item"\]`
- **Impact:** Unnecessary PII exposure in API responses, increasing data breach impact.
- **CWE:** CWE-359 (Exposure of Private Personal Information to an Unauthorized Actor)
- **OWASP:** API3:2023 - Broken Object Property Level Authorization

**Vulnerable Pattern:**

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/users/{user_id}/profile")
async def get_user_profile(user_id: str):
    user = await user_repo.get(user_id)
    # VULNERABLE: Returns all fields including full email, phone, address
    return user.model_dump()
```

**Secure Pattern:**

```python
from pydantic import BaseModel
from fastapi import APIRouter

class UserProfileResponse(BaseModel):
    """Public-facing user profile with masked PII."""
    id: str
    display_name: str
    email_masked: str    # j***@example.com
    phone_masked: str    # ***-***-1234

def mask_email(email: str) -> str:
    local, domain = email.split("@")
    return f"{local[0]}***@{domain}"

def mask_phone(phone: str) -> str:
    return f"***-***-{phone[-4:]}"

router = APIRouter()

@router.get("/users/{user_id}/profile")
async def get_user_profile(user_id: str):
    user = await user_repo.get(user_id)
    # SECURE: Return masked PII through response model
    return UserProfileResponse(
        id=user.id,
        display_name=user.display_name,
        email_masked=mask_email(user.email),
        phone_masked=mask_phone(user.phone),
    )
```

---

### SEC-PII-004: Missing Data Retention Controls

- **Severity:** MEDIUM
- **Category:** PII & Data Protection
- **Description:** DynamoDB items containing PII stored without TTL (Time-to-Live) or lifecycle management. Data accumulates indefinitely, increasing breach impact and violating data minimization principles.
- **Detection Regex:** `put_item\((?!.*ttl|.*expires_at)` for PII-containing items
- **Impact:** Unbounded PII accumulation, increased breach impact, regulatory non-compliance.
- **CWE:** CWE-359 (Exposure of Private Personal Information to an Unauthorized Actor)
- **OWASP:** A04:2021 - Insecure Design

**Vulnerable Pattern:**

```python
import time
import aioboto3

async def store_user_activity(user_id: str, activity: dict):
    session = aioboto3.Session()
    async with session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table("user_activity")
        # VULNERABLE: No TTL - activity data retained forever
        await table.put_item(Item={
            "user_id": user_id,
            "timestamp": int(time.time()),
            "activity": activity,
            "ip_address": activity.get("ip"),  # PII stored indefinitely
        })
```

**Secure Pattern:**

```python
import time
import aioboto3

# Data retention: 90 days for user activity
ACTIVITY_RETENTION_DAYS = 90

async def store_user_activity(user_id: str, activity: dict):
    session = aioboto3.Session()
    async with session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table("user_activity")
        now = int(time.time())
        # SECURE: TTL ensures automatic deletion after retention period
        await table.put_item(Item={
            "user_id": user_id,
            "timestamp": now,
            "activity": activity,
            # PII excluded from activity log
            "ttl": now + (ACTIVITY_RETENTION_DAYS * 86400),
        })
```

---

### SEC-PII-005: GDPR Right-to-Erasure Gaps

- **Severity:** HIGH
- **Category:** PII & Data Protection
- **Description:** User deletion that does not remove data from all storage locations (DynamoDB tables, S3 buckets, CloudWatch logs, backups, caches). GDPR Article 17 requires erasure from all systems.
- **Detection Regex:** `delete_user.*(?!s3|cognito|logs)` or single-table deletion for user data
- **Impact:** Regulatory non-compliance (GDPR fines up to 4% of annual global revenue), user trust violation.
- **CWE:** CWE-359 (Exposure of Private Personal Information to an Unauthorized Actor)
- **OWASP:** A01:2021 - Broken Access Control

**Vulnerable Pattern:**

```python
import aioboto3

async def delete_user(user_id: str):
    session = aioboto3.Session()
    async with session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table("users")
        # VULNERABLE: Only deletes from one table
        # User data remains in: trail_systems, photos, activity_log,
        # S3 uploads, Cognito, CloudWatch logs
        await table.delete_item(Key={"id": user_id})
        return {"message": "User deleted"}
```

**Secure Pattern:**

```python
import aioboto3
from api.shared.logging import log_info, log_error

async def delete_user(user_id: str, org_id: str):
    """Delete all user data across all storage systems (GDPR Art. 17)."""
    session = aioboto3.Session()
    deletion_results: dict[str, bool] = {}

    # 1. Delete from all DynamoDB tables
    async with session.resource("dynamodb") as dynamodb:
        for table_name in ["users", "user_activity", "user_preferences"]:
            table = await dynamodb.Table(table_name)
            try:
                await table.delete_item(Key={"tenant_id": org_id, "id": user_id})
                deletion_results[table_name] = True
            except Exception:
                deletion_results[table_name] = False

    # 2. Delete S3 uploads
    async with session.client("s3") as s3:
        prefix = f"{org_id}/{user_id}/"
        paginator = s3.get_paginator("list_objects_v2")
        async for page in paginator.paginate(Bucket=settings.PHOTOS_BUCKET, Prefix=prefix):
            objects = [{"Key": obj["Key"]} for obj in page.get("Contents", [])]
            if objects:
                await s3.delete_objects(
                    Bucket=settings.PHOTOS_BUCKET,
                    Delete={"Objects": objects},
                )
        deletion_results["s3_photos"] = True

    # 3. Delete Cognito user
    async with session.client("cognito-idp") as cognito:
        await cognito.admin_delete_user(
            UserPoolId=settings.COGNITO_USER_POOL_ID,
            Username=user_id,
        )
        deletion_results["cognito"] = True

    # 4. Audit log (no PII in the log entry itself)
    log_info("User data deletion completed", metadata={
        "user_id": user_id,
        "deletion_results": deletion_results,
    })

    return {"status": "deleted", "systems_processed": list(deletion_results.keys())}
```

---

### SEC-PII-006: Cross-Tenant Data Leakage

- **Severity:** CRITICAL
- **Category:** PII & Data Protection
- **Description:** DynamoDB queries or scans that do not include `tenant_id` filtering, allowing data from one organization to be returned to users in another organization. This is the data protection counterpart to SEC-AUTHZ-004.
- **Detection Regex:** `(query|scan)\((?!.*tenant)` or `get_item\(.*Key=\{["']id`
- **Impact:** Complete cross-tenant data leakage. PII from one organization exposed to another.
- **CWE:** CWE-668 (Exposure of Resource to Wrong Sphere)
- **OWASP:** A01:2021 - Broken Access Control

**Vulnerable Pattern:**

```python
import aioboto3

async def search_users(search_term: str):
    session = aioboto3.Session()
    async with session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table("users")
        # VULNERABLE: No tenant scoping - returns users from ALL organizations
        response = await table.scan(
            FilterExpression="contains(display_name, :term)",
            ExpressionAttributeValues={":term": search_term},
        )
        return response["Items"]  # Contains PII from all tenants
```

**Secure Pattern:**

```python
import aioboto3
from boto3.dynamodb.conditions import Key, Attr

async def search_users(tenant_id: str, search_term: str):
    session = aioboto3.Session()
    async with session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table("users")
        # SECURE: Query scoped to tenant partition
        response = await table.query(
            KeyConditionExpression=Key("tenant_id").eq(tenant_id),
            FilterExpression=Attr("display_name").contains(search_term),
            ProjectionExpression="id, display_name",  # Only non-PII fields
        )
        return [UserSearchResult(**item) for item in response["Items"]]
```

---

## Category 6: Configuration & Deployment

### SEC-CONFIG-001: Debug Mode in Production

- **Severity:** HIGH
- **Category:** Configuration & Deployment
- **Description:** FastAPI or Uvicorn running with debug mode enabled in production. Debug mode exposes stack traces, reloads code on change, and may enable interactive debuggers.
- **Detection Regex:** `FastAPI\(.*debug\s*=\s*True` or `uvicorn\.run\(.*reload\s*=\s*True`
- **Impact:** Stack trace exposure (internal paths, library versions, local variables), automatic code reload vulnerabilities.
- **CWE:** CWE-489 (Active Debug Code)
- **OWASP:** A02:2021 - Cryptographic Failures (grouped with misconfig)

**Vulnerable Pattern:**

```python
from fastapi import FastAPI

# VULNERABLE: Debug mode hardcoded to True
app = FastAPI(debug=True)

if __name__ == "__main__":
    import uvicorn
    # VULNERABLE: reload=True in production
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

**Secure Pattern:**

```python
import os
from fastapi import FastAPI

# SECURE: Debug mode from environment, defaults to False
app = FastAPI(
    debug=os.environ.get("FASTAPI_DEBUG", "false").lower() == "true",
    docs_url=None if os.environ.get("ENVIRONMENT") == "prod" else "/docs",
    redoc_url=None if os.environ.get("ENVIRONMENT") == "prod" else "/redoc",
)

# Lambda handler - no uvicorn.run in production
# Production uses Mangum adapter for API Gateway integration
```

---

### SEC-CONFIG-002: Wildcard CORS

- **Severity:** HIGH
- **Category:** Configuration & Deployment
- **Description:** CORS middleware configured with `allow_origins=["*"]` combined with `allow_credentials=True`. This allows any website to make authenticated cross-origin requests to the API, stealing user data.
- **Detection Regex:** `CORSMiddleware.*allow_origins.*\*` or `allow_origins\s*=\s*\["'\*`
- **Impact:** Cross-origin data theft. Any website can make authenticated API calls on behalf of logged-in users.
- **CWE:** CWE-942 (Permissive Cross-domain Policy with Untrusted Domains)
- **OWASP:** A02:2021 - Cryptographic Failures (grouped with misconfig)

**Vulnerable Pattern:**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# VULNERABLE: Wildcard origin with credentials
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Secure Pattern:**

```python
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# SECURE: Explicit origin allowlist from configuration
ALLOWED_ORIGINS = os.environ.get(
    "CORS_ALLOWED_ORIGINS",
    "https://app.traillenshq.com",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-Correlation-ID"],
    max_age=3600,
)
```

---

### SEC-CONFIG-003: Missing Security Headers

- **Severity:** MEDIUM
- **Category:** Configuration & Deployment
- **Description:** API responses missing security headers like `Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options`, and `Content-Security-Policy`. These headers provide defense-in-depth against various attack classes.
- **Detection Regex:** Missing `SecurityHeadersMiddleware` or `Strict-Transport-Security` in response headers
- **Impact:** Increased susceptibility to clickjacking, MIME sniffing attacks, and protocol downgrade attacks.
- **CWE:** CWE-693 (Protection Mechanism Failure)
- **OWASP:** A02:2021 - Cryptographic Failures (grouped with misconfig)

**Vulnerable Pattern:**

```python
from fastapi import FastAPI

# VULNERABLE: No security headers configured
app = FastAPI()

# Responses lack:
# - Strict-Transport-Security
# - X-Content-Type-Options
# - X-Frame-Options
# - Cache-Control for sensitive data
```

**Secure Pattern:**

```python
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Request-ID"] = request.headers.get(
            "X-Correlation-ID", "unknown"
        )
        return response

app = FastAPI()
app.add_middleware(SecurityHeadersMiddleware)
```

---

### SEC-CONFIG-004: Overly Permissive IAM

- **Severity:** CRITICAL
- **Category:** Configuration & Deployment
- **Description:** IAM policies with wildcard actions (`"Action": "*"`) or wildcard resources (`"Resource": "*"`). Overly broad permissions violate the principle of least privilege and maximize blast radius of any credential compromise.
- **Detection Regex:** `"Action"\s*:\s*"\*"` or `"Resource"\s*:\s*"\*"` or `"Action"\s*:\s*"[a-z]+:\*"`
- **Impact:** Full AWS service access from compromised Lambda or credentials. Maximum blast radius.
- **CWE:** CWE-250 (Execution with Unnecessary Privileges)
- **OWASP:** A02:2021 - Cryptographic Failures (grouped with misconfig)

**Vulnerable Pattern:**

```python
# Pulumi infrastructure code
import json
import pulumi_aws as aws

# VULNERABLE: Wildcard actions and resources
lambda_role_policy = aws.iam.RolePolicy(
    "lambda-policy",
    role=lambda_role.name,
    policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": "*",
            "Resource": "*",
        }],
    }),
)
```

**Secure Pattern:**

```python
# Pulumi infrastructure code
import json
import pulumi
import pulumi_aws as aws

# SECURE: Least-privilege with specific actions and resource ARNs
lambda_role_policy = aws.iam.RolePolicy(
    "lambda-policy",
    role=lambda_role.name,
    policy=pulumi.Output.all(
        trails_table.arn, photos_bucket.arn,
    ).apply(lambda args: json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "dynamodb:GetItem",
                    "dynamodb:PutItem",
                    "dynamodb:Query",
                    "dynamodb:UpdateItem",
                    "dynamodb:DeleteItem",
                ],
                "Resource": [args[0], f"{args[0]}/index/*"],
            },
            {
                "Effect": "Allow",
                "Action": ["s3:GetObject", "s3:PutObject"],
                "Resource": f"{args[1]}/*",
            },
        ],
    })),
)
```

---

### SEC-CONFIG-005: S3 Bucket Public Access

- **Severity:** CRITICAL
- **Category:** Configuration & Deployment
- **Description:** S3 buckets with public access enabled via bucket policy (`"Principal": "*"`), ACLs, or disabled Public Access Block settings. This exposes all bucket contents to the internet.
- **Detection Regex:** `"Principal"\s*:\s*"\*"` or `PublicAccessBlock.*False` or `block_public_acls\s*=\s*False`
- **Impact:** Complete data exposure. All objects in the bucket accessible to anyone on the internet.
- **CWE:** CWE-284 (Improper Access Control)
- **OWASP:** A02:2021 - Cryptographic Failures (grouped with misconfig)

**Vulnerable Pattern:**

```python
# Pulumi infrastructure code
import pulumi_aws as aws

# VULNERABLE: No public access block - default allows public access
photos_bucket = aws.s3.Bucket(
    "photos-bucket",
    acl="public-read",  # All objects publicly readable
)
```

**Secure Pattern:**

```python
# Pulumi infrastructure code
import pulumi_aws as aws

photos_bucket = aws.s3.Bucket(
    "photos-bucket",
    acl="private",
)

# SECURE: Block all public access
aws.s3.BucketPublicAccessBlock(
    "photos-bucket-public-access-block",
    bucket=photos_bucket.id,
    block_public_acls=True,
    block_public_policy=True,
    ignore_public_acls=True,
    restrict_public_buckets=True,
)
```

---

### SEC-CONFIG-006: S3 Missing Lifecycle Rules

- **Severity:** MEDIUM
- **Category:** Configuration & Deployment
- **Description:** S3 buckets without lifecycle rules accumulate data indefinitely, leading to unbounded storage growth and costs. Old data that is no longer needed should be transitioned to cheaper storage or deleted.
- **Detection Regex:** `Bucket\((?!.*lifecycle)` or `s3\.Bucket\((?!.*lifecycle_rule)`
- **Impact:** Unbounded storage cost growth, retention of data beyond required periods.
- **CWE:** CWE-459 (Incomplete Cleanup)
- **OWASP:** A02:2021 - Cryptographic Failures (grouped with misconfig)

**Vulnerable Pattern:**

```python
# Pulumi infrastructure code
import pulumi_aws as aws

# VULNERABLE: No lifecycle rules - storage grows indefinitely
uploads_bucket = aws.s3.Bucket(
    "uploads-bucket",
    acl="private",
)
```

**Secure Pattern:**

```python
# Pulumi infrastructure code
import pulumi_aws as aws

# SECURE: Lifecycle rules manage storage cost and data retention
uploads_bucket = aws.s3.Bucket(
    "uploads-bucket",
    acl="private",
    lifecycle_rules=[
        {
            "enabled": True,
            "prefix": "tmp/",
            "expiration": {"days": 7},  # Temp uploads deleted after 7 days
        },
        {
            "enabled": True,
            "prefix": "photos/",
            "transitions": [
                {"days": 90, "storage_class": "STANDARD_IA"},
                {"days": 365, "storage_class": "GLACIER"},
            ],
        },
    ],
)
```

---

### SEC-CONFIG-007: Lambda Env Var Secret Exposure

- **Severity:** HIGH
- **Category:** Configuration & Deployment
- **Description:** Lambda functions using `os.environ` or `os.getenv` to read secrets that are stored as plaintext environment variables. These are visible in the Lambda console, CloudFormation templates, and API calls.
- **Detection Regex:** `os\.environ\[["'](SECRET|KEY|PASSWORD|TOKEN)` or `os\.getenv\(["'](SECRET|KEY|PASSWORD)`
- **Impact:** Secrets visible in AWS Console, CloudFormation stack, and GetFunctionConfiguration API.
- **CWE:** CWE-798 (Use of Hard-coded Credentials)
- **OWASP:** A02:2021 - Cryptographic Failures (grouped with misconfig)

**Vulnerable Pattern:**

```python
import os

# VULNERABLE: Secrets as plaintext environment variables
# Visible in: Lambda console, CloudFormation, GetFunctionConfiguration API
THIRD_PARTY_API_KEY = os.environ["THIRD_PARTY_API_KEY"]
WEBHOOK_SECRET = os.environ["WEBHOOK_SECRET"]
```

**Secure Pattern:**

```python
import json
import os
import aioboto3

# SECURE: Only secret ARN/name in environment variables
SECRET_ARN = os.environ.get("SECRET_ARN", "traillens/prod/api-keys")

_secrets: dict | None = None

async def get_secrets() -> dict:
    """Load secrets from AWS Secrets Manager (cached)."""
    global _secrets
    if _secrets is None:
        session = aioboto3.Session()
        async with session.client("secretsmanager") as client:
            response = await client.get_secret_value(SecretId=SECRET_ARN)
            _secrets = json.loads(response["SecretString"])
    return _secrets
```

---

### SEC-CONFIG-008: Cognito Guest Access Misconfigured

- **Severity:** HIGH
- **Category:** Configuration & Deployment
- **Description:** Cognito Identity Pool configured with unauthenticated (guest) access enabled and IAM role with overly broad permissions. Guest users can access AWS resources directly without authentication.
- **Detection Regex:** `allow_unauthenticated_identities\s*=\s*True` or `IdentityPool.*Unauthenticated.*allow`
- **Impact:** Unauthenticated users can access AWS resources (DynamoDB, S3, etc.) with the unauthenticated role's permissions.
- **CWE:** CWE-287 (Improper Authentication)
- **OWASP:** A02:2021 - Cryptographic Failures (grouped with misconfig)

**Vulnerable Pattern:**

```python
# Pulumi infrastructure code
import json
import pulumi_aws as aws

# VULNERABLE: Guest access with broad permissions
identity_pool = aws.cognito.IdentityPool(
    "identity-pool",
    identity_pool_name="traillens-identity-pool",
    allow_unauthenticated_identities=True,  # Guests allowed
)

# VULNERABLE: Guest role has DynamoDB read access
unauth_role_policy = aws.iam.RolePolicy(
    "unauth-role-policy",
    role=unauth_role.name,
    policy=json.dumps({
        "Statement": [{
            "Effect": "Allow",
            "Action": ["dynamodb:GetItem", "dynamodb:Query"],
            "Resource": "*",
        }],
    }),
)
```

**Secure Pattern:**

```python
# Pulumi infrastructure code
import pulumi_aws as aws

# SECURE: Guest access disabled - all users must authenticate
identity_pool = aws.cognito.IdentityPool(
    "identity-pool",
    identity_pool_name="traillens-identity-pool",
    allow_unauthenticated_identities=False,
)

# If guest access is required, use minimal permissions:
# unauth_role_policy = aws.iam.RolePolicy(
#     "unauth-role-policy",
#     role=unauth_role.name,
#     policy=json.dumps({
#         "Statement": [{
#             "Effect": "Allow",
#             "Action": ["s3:GetObject"],
#             "Resource": f"arn:aws:s3:::{public_assets_bucket}/public/*",
#         }],
#     }),
# )
```

---

### SEC-CONFIG-009: Cognito Identity Pool ID Hardcoded

- **Severity:** MEDIUM
- **Category:** Configuration & Deployment
- **Description:** Cognito Identity Pool IDs or User Pool IDs hardcoded in application source code. These IDs reveal AWS region, account structure, and can be used in enumeration attacks.
- **Detection Regex:** `(us-east-1|us-west-2|eu-west-1|ca-central-1):[a-f0-9-]{36}` or `us-east-1_[a-zA-Z0-9]+`
- **Impact:** Information disclosure about AWS infrastructure. Pool IDs can be used for credential stuffing or enumeration.
- **CWE:** CWE-200 (Exposure of Sensitive Information to an Unauthorized Actor)
- **OWASP:** A02:2021 - Cryptographic Failures (grouped with misconfig)

**Vulnerable Pattern:**

```python
# VULNERABLE: Pool IDs hardcoded in source code
COGNITO_USER_POOL_ID = "us-east-1_AbCdEfGhI"
COGNITO_IDENTITY_POOL_ID = "us-east-1:12345678-1234-1234-1234-123456789012"
COGNITO_CLIENT_ID = "1abc2def3ghi4jkl5mno6pqr"
```

**Secure Pattern:**

```python
import os

# SECURE: Pool IDs from environment variables (set by infrastructure)
COGNITO_USER_POOL_ID = os.environ["COGNITO_USER_POOL_ID"]
COGNITO_IDENTITY_POOL_ID = os.environ["COGNITO_IDENTITY_POOL_ID"]
COGNITO_CLIENT_ID = os.environ["COGNITO_CLIENT_ID"]

# These are set in the Lambda function configuration by Pulumi:
#   environment={
#       "variables": {
#           "COGNITO_USER_POOL_ID": user_pool.id,
#           "COGNITO_CLIENT_ID": user_pool_client.id,
#       },
#   },
```

---

## Category 7: Dependency & Supply Chain

### SEC-DEP-001: Known Vulnerable Dependencies

- **Severity:** VARIES (depends on specific vulnerability)
- **Category:** Dependency & Supply Chain
- **Description:** Using packages with known CVEs. Notable example: `python-jose` depends on the vulnerable `ecdsa` library (CVE-2024-23342). TrailLens migrated to `PyJWT[crypto]` in commit c2c5aa4.
- **Detection Regex:** `python-jose` or `ecdsa` in requirements.txt, or known vulnerable version pins
- **Impact:** Varies by CVE. CVE-2024-23342 (ecdsa) allows private key extraction via timing attacks.
- **CWE:** CWE-1395 (Dependency on Vulnerable Third-Party Component)
- **OWASP:** A03:2021 - Injection (grouped with vulnerable components)

**Vulnerable Pattern:**

```text
# requirements.txt
# VULNERABLE: python-jose depends on ecdsa (CVE-2024-23342)
python-jose[cryptography]==3.3.0
```

```python
# VULNERABLE: Using deprecated python-jose
from jose import jwt

payload = jwt.decode(token, key, algorithms=["RS256"])
```

**Secure Pattern:**

```text
# requirements.txt
# SECURE: PyJWT with cryptography backend (no ecdsa dependency)
PyJWT[crypto]>=2.9.0
```

```python
# SECURE: Using PyJWT
import jwt

payload = jwt.decode(token, key, algorithms=["RS256"])
```

---

### SEC-DEP-002: Unpinned Dependencies

- **Severity:** MEDIUM
- **Category:** Dependency & Supply Chain
- **Description:** Dependencies in `requirements.txt` without version pins. A malicious or buggy new release can be automatically installed, introducing vulnerabilities or breaking changes.
- **Detection Regex:** Package names without `==` version pins in requirements.txt
- **Impact:** Supply chain attack via compromised package update. Silent introduction of vulnerabilities.
- **CWE:** CWE-1395 (Dependency on Vulnerable Third-Party Component)
- **OWASP:** A03:2021 - Injection (grouped with vulnerable components)

**Vulnerable Pattern:**

```text
# requirements.txt
# VULNERABLE: No version pins - any version installed
fastapi
uvicorn
aioboto3
pydantic
PyJWT
```

**Secure Pattern:**

```text
# requirements.txt
# SECURE: Exact version pins for reproducible builds
fastapi==0.115.0
uvicorn==0.32.0
aioboto3==13.3.0
pydantic==2.10.0
PyJWT[crypto]==2.9.0

# Generated with: pip freeze > requirements.txt
# Audit with: pip-audit
# Update with: pip-compile --upgrade
```

---

### SEC-DEP-003: Typosquatting Risk

- **Severity:** HIGH
- **Category:** Dependency & Supply Chain
- **Description:** Installing packages with names similar to popular packages but controlled by attackers. Examples: `python-jost` (vs `python-jose`), `requets` (vs `requests`), `coloursama` (vs `colorama`).
- **Detection Regex:** Manual review of new package additions against known typosquatting lists
- **Impact:** Remote code execution. Typosquat packages typically exfiltrate credentials or install backdoors on `pip install`.
- **CWE:** CWE-1395 (Dependency on Vulnerable Third-Party Component)
- **OWASP:** A03:2021 - Injection (grouped with vulnerable components)

**Vulnerable Pattern:**

```text
# requirements.txt
# VULNERABLE: Typosquatting - wrong package name
python-jost==3.3.0           # Should be: python-jose (now deprecated, use PyJWT)
requets==2.31.0              # Should be: requests
coloursama==0.4.6            # Should be: colorama
```

**Secure Pattern:**

```text
# requirements.txt
# SECURE: Verified package names, installed from trusted index
--index-url https://pypi.org/simple/
--require-hashes

PyJWT[crypto]==2.9.0 \
    --hash=sha256:abc123...
requests==2.31.0 \
    --hash=sha256:def456...

# Verification steps:
# 1. pip-audit to check for known vulnerabilities
# 2. pip install --require-hashes for hash verification
# 3. Review new dependencies on pypi.org before adding
```

---

### SEC-DEP-004: Abandoned Packages

- **Severity:** MEDIUM
- **Category:** Dependency & Supply Chain
- **Description:** Dependencies that are no longer maintained receive no security patches. Vulnerabilities discovered after abandonment remain permanently unpatched. `python-jose` is a notable example (deprecated, last release 2021).
- **Detection Regex:** `python-jose` or packages with no releases in 2+ years
- **Impact:** Unpatched vulnerabilities accumulate over time. No security fixes available.
- **CWE:** CWE-1395 (Dependency on Vulnerable Third-Party Component)
- **OWASP:** A03:2021 - Injection (grouped with vulnerable components)

**Vulnerable Pattern:**

```text
# requirements.txt
# VULNERABLE: Abandoned packages
python-jose==3.3.0    # Last release: 2021, deprecated
pycrypto==2.6.1       # Abandoned, replaced by pycryptodome
```

**Secure Pattern:**

```text
# requirements.txt
# SECURE: Actively maintained alternatives
PyJWT[crypto]==2.9.0     # Active replacement for python-jose
pycryptodome==3.20.0     # Active replacement for pycrypto

# Maintenance check:
# - Last release date < 2 years ago
# - Active issue/PR responses
# - Multiple maintainers
# - Security advisory response history
```

---

## Category 8: Error Handling

### SEC-ERR-001: Stack Traces in Responses

- **Severity:** HIGH
- **Category:** Error Handling
- **Description:** Returning Python stack traces (`traceback.format_exc()`) in API error responses. Stack traces reveal internal file paths, library versions, local variable values, and application architecture.
- **Detection Regex:** `traceback\.format_exc\(\)` in response context or `return.*traceback`
- **Impact:** Information disclosure: internal paths, library versions, code structure, and local variable values.
- **CWE:** CWE-209 (Generation of Error Message Containing Sensitive Information)
- **OWASP:** A10:2021 - Server-Side Request Forgery (grouped with information disclosure)

**Vulnerable Pattern:**

```python
import traceback
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/trails/{trail_id}")
async def get_trail(trail_id: str):
    try:
        return await trail_service.get(trail_id)
    except Exception:
        # VULNERABLE: Full stack trace in response
        return JSONResponse(
            status_code=500,
            content={
                "error": traceback.format_exc(),
                # Reveals: file paths, library versions, local variables
            },
        )
```

**Secure Pattern:**

```python
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.shared.logging import log_error
from api.shared.correlation import get_correlation_id

router = APIRouter()

@router.get("/trails/{trail_id}")
async def get_trail(trail_id: str):
    try:
        return await trail_service.get(trail_id)
    except Exception as exc:
        # SECURE: Log full details server-side, return generic message
        correlation_id = get_correlation_id()
        log_error(
            "Failed to get trail",
            metadata={
                "trail_id": trail_id,
                "error_type": type(exc).__name__,
                "correlation_id": correlation_id,
            },
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "correlation_id": correlation_id,
            },
        )
```

---

### SEC-ERR-002: Verbose Error Messages

- **Severity:** MEDIUM
- **Category:** Error Handling
- **Description:** Error responses that include internal details like table names, ARNs, endpoint URLs, or database query details. These aid attackers in understanding the backend architecture.
- **Detection Regex:** `HTTPException\(.*\b(table|arn|endpoint|dynamo|lambda|bucket)\b`
- **Impact:** Architecture disclosure aids targeted attacks. Table names, ARNs, and endpoints map the attack surface.
- **CWE:** CWE-209 (Generation of Error Message Containing Sensitive Information)
- **OWASP:** A10:2021 - Server-Side Request Forgery (grouped with information disclosure)

**Vulnerable Pattern:**

```python
from fastapi import HTTPException

async def get_trail(trail_id: str):
    try:
        response = await table.get_item(Key={"id": trail_id})
    except Exception as exc:
        # VULNERABLE: Reveals DynamoDB table name and AWS details
        raise HTTPException(
            status_code=500,
            detail=f"Failed to query DynamoDB table 'traillens-prod-trails': {exc}",
        ) from exc
```

**Secure Pattern:**

```python
from fastapi import HTTPException
from api.shared.logging import log_error

async def get_trail(trail_id: str):
    try:
        response = await table.get_item(Key={"id": trail_id})
    except Exception as exc:
        # SECURE: Internal details in logs only, generic message to client
        log_error("DynamoDB query failed", metadata={
            "operation": "get_item",
            "trail_id": trail_id,
            "error_type": type(exc).__name__,
        })
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve resource",
        ) from exc
```

---

### SEC-ERR-003: Timing Attack on Authentication

- **Severity:** MEDIUM
- **Category:** Error Handling
- **Description:** Using `==` operator for comparing passwords, tokens, or API keys in authentication flows. The `==` operator returns immediately on the first byte difference, allowing attackers to determine the correct value through timing measurements.
- **Detection Regex:** `(password|token|secret|api_key)\s*==\s*` or `verify.*==`
- **Impact:** Secret recovery through timing side-channel analysis.
- **CWE:** CWE-208 (Observable Timing Discrepancy)
- **OWASP:** A04:2021 - Insecure Design

**Vulnerable Pattern:**

```python
from fastapi import APIRouter, Header, HTTPException

router = APIRouter()

INTERNAL_API_KEY = "sk_live_abc123def456"

@router.post("/internal/sync")
async def internal_sync(x_api_key: str = Header()):
    # VULNERABLE: == enables timing attack
    if x_api_key == INTERNAL_API_KEY:
        return await perform_sync()
    raise HTTPException(status_code=401, detail="Invalid API key")
```

**Secure Pattern:**

```python
import hmac
from fastapi import APIRouter, Header, HTTPException

router = APIRouter()

@router.post("/internal/sync")
async def internal_sync(x_api_key: str = Header()):
    stored_key = await get_api_key_from_secrets_manager()
    # SECURE: Constant-time comparison
    if hmac.compare_digest(
        x_api_key.encode("utf-8"),
        stored_key.encode("utf-8"),
    ):
        return await perform_sync()
    raise HTTPException(status_code=401, detail="Invalid API key")
```

---

### SEC-ERR-004: User Enumeration via Error Messages

- **Severity:** MEDIUM
- **Category:** Error Handling
- **Description:** Different error messages for "user not found" vs "wrong password" allow attackers to enumerate valid usernames/emails. This information is then used for targeted credential stuffing attacks.
- **Detection Regex:** `"user not found"` or `"invalid password"` or `"email not registered"` in error responses
- **Impact:** Username/email enumeration enabling targeted credential stuffing and social engineering.
- **CWE:** CWE-204 (Observable Response Discrepancy)
- **OWASP:** A07:2021 - Identification and Authentication Failures

**Vulnerable Pattern:**

```python
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/auth/login")
async def login(email: str, password: str):
    user = await user_repo.find_by_email(email)
    if not user:
        # VULNERABLE: Reveals that email is not registered
        raise HTTPException(status_code=404, detail="User not found")

    if not await verify_password(password, user.password_hash):
        # VULNERABLE: Reveals that email IS registered but password is wrong
        raise HTTPException(status_code=401, detail="Invalid password")

    return {"token": await create_token(user.id)}
```

**Secure Pattern:**

```python
from fastapi import APIRouter, HTTPException
from api.shared.logging import log_info

router = APIRouter()

@router.post("/auth/login")
async def login(email: str, password: str):
    user = await user_repo.find_by_email(email)

    # SECURE: Same error message regardless of failure reason
    if not user or not await verify_password(password, user.password_hash):
        log_info("Login failed", metadata={"has_user": user is not None})
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"token": await create_token(user.id)}
```

---

### SEC-ERR-005: Bare Except Swallowing Errors

- **Severity:** MEDIUM
- **Category:** Error Handling
- **Description:** Using bare `except:` or broad `except Exception:` clauses that silently swallow errors. This hides security-relevant failures like authentication errors, authorization failures, and data corruption.
- **Detection Regex:** `except\s*:` or `except\s+Exception\s*:` followed by `pass` or minimal handling
- **Impact:** Security failures silently ignored. Authentication/authorization errors may be treated as success.
- **CWE:** CWE-396 (Declaration of Catch for Generic Exception)
- **OWASP:** A10:2021 - Server-Side Request Forgery (grouped with information disclosure)

**Vulnerable Pattern:**

```python
async def check_user_permission(user_id: str, resource_id: str) -> bool:
    try:
        result = await authz_service.check(user_id, resource_id)
        return result.allowed
    except:
        # VULNERABLE: Authorization failure silently treated as "allowed"
        return True

async def process_payment(amount: float, user_id: str):
    try:
        await payment_service.charge(user_id, amount)
    except Exception:
        # VULNERABLE: Payment failure silently swallowed
        pass
```

**Secure Pattern:**

```python
from fastapi import HTTPException
from api.shared.logging import log_error, log_info

async def check_user_permission(user_id: str, resource_id: str) -> bool:
    try:
        result = await authz_service.check(user_id, resource_id)
        return result.allowed
    except ConnectionError as exc:
        # SECURE: Fail closed - deny access on authorization service failure
        log_error("Authorization service unavailable", metadata={
            "user_id": user_id,
            "error": str(exc),
        })
        return False
    except Exception as exc:
        log_error("Unexpected authorization error", metadata={
            "user_id": user_id,
            "error_type": type(exc).__name__,
        })
        return False  # Fail closed

async def process_payment(amount: float, user_id: str) -> bool:
    try:
        await payment_service.charge(user_id, amount)
        return True
    except PaymentDeclinedError as exc:
        log_info("Payment declined", metadata={"user_id": user_id})
        raise HTTPException(status_code=402, detail="Payment declined") from exc
    except PaymentServiceError as exc:
        log_error("Payment service error", metadata={
            "user_id": user_id,
            "error": str(exc),
        })
        raise HTTPException(status_code=503, detail="Payment service unavailable") from exc
```

---

### SEC-ERR-006: Python 2 Except Syntax

- **Severity:** CRITICAL
- **Category:** Error Handling
- **Description:** Using Python 2 `except Type, var:` syntax instead of Python 3 `except (Type1, Type2) as var:`. In Python 3 this is a SyntaxError that prevents the entire module from loading. All functionality in the affected module becomes unavailable at runtime.
- **Detection Regex:** `except\s+\w+\s*,\s*\w+`
- **Impact:** Module fails to load in Python 3. All functionality in the module is unavailable. In authentication modules, this means all auth checks fail.
- **CWE:** CWE-670 (Always-Incorrect Control Flow Implementation)
- **OWASP:** A05:2021 - Security Misconfiguration

**Vulnerable Pattern:**

```python
try:
    payload = jwt.decode(token, options={"verify_signature": False})
except JWTError, ValueError, KeyError:
    # VULNERABLE: Python 2 syntax — SyntaxError in Python 3
    # Module cannot load; all code in this file is inaccessible
    payload = {}
```

**Secure Pattern:**

```python
try:
    payload = jwt.decode(token, options={"verify_signature": False})
except (JWTError, ValueError, KeyError):
    # SECURE: Python 3 tuple syntax for multiple exception types
    payload = {}
```

---

### SEC-ERR-007: Exception Re-wrapping Loses Subclass Info

- **Severity:** MEDIUM
- **Category:** Error Handling
- **Description:** Catching a base exception class and re-raising as the same base class with `str(e)` discards the specific subclass type. For example, `ExpiredSignatureError` (a subclass of `InvalidTokenError`) becomes plain `InvalidTokenError`. Downstream code that distinguishes exception types cannot function correctly.
- **Detection Regex:** `except\s+(\w+)\s+as\s+(\w+):\s*\n\s*raise\s+\1\(str\(\2\)\)` (multiline)
- **Impact:** Callers cannot distinguish between exception subtypes. In JWT handling, expired tokens are treated the same as invalid tokens, preventing token refresh flows.
- **CWE:** CWE-755 (Improper Handling of Exceptional Conditions)
- **OWASP:** A07:2021 - Identification and Authentication Failures

**Vulnerable Pattern:**

```python
from jwt.exceptions import InvalidTokenError as JWTError

try:
    claims = jwt.decode(token, public_key, algorithms=["RS256"])
except JWTError as e:
    # VULNERABLE: ExpiredSignatureError becomes plain InvalidTokenError
    # Callers cannot distinguish expired vs. invalid tokens
    raise JWTError(str(e)) from e
```

**Secure Pattern:**

```python
from jwt.exceptions import InvalidTokenError as JWTError

try:
    claims = jwt.decode(token, public_key, algorithms=["RS256"])
except JWTError:
    # SECURE: Preserves original subclass (e.g., ExpiredSignatureError)
    raise
except Exception as e:
    # Wrap non-JWT exceptions into JWTError for consistent caller handling
    raise JWTError(str(e)) from e
```

---

## Category 9: API Security

### SEC-API-001: Missing Rate Limiting

- **Severity:** HIGH
- **Category:** API Security
- **Description:** API endpoints without rate limiting are vulnerable to brute-force attacks, credential stuffing, and denial of service. Authentication endpoints are especially critical.
- **Detection Regex:** Router definitions without rate limiting middleware or dependency
- **Impact:** Brute-force attacks, credential stuffing, API abuse, and denial of service.
- **CWE:** CWE-770 (Allocation of Resources Without Limits or Throttling)
- **OWASP:** API4:2023 - Unrestricted Resource Consumption

**Vulnerable Pattern:**

```python
from fastapi import APIRouter

router = APIRouter()

@router.post("/auth/login")
async def login(email: str, password: str):
    # VULNERABLE: No rate limiting - unlimited login attempts
    user = await authenticate(email, password)
    return {"token": await create_token(user.id)}

@router.post("/auth/forgot-password")
async def forgot_password(email: str):
    # VULNERABLE: Can be used to spam any email address
    await send_reset_email(email)
    return {"message": "Reset email sent"}
```

**Secure Pattern:**

```python
from fastapi import APIRouter, Depends, HTTPException, Request

router = APIRouter()

MAX_LOGIN_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 300  # 5 minutes

async def rate_limit_login(request: Request):
    """Rate limit login attempts by IP address."""
    client_ip = request.client.host
    key = f"login_attempts:{client_ip}"

    attempts = await rate_store.get_count(key, window=LOGIN_WINDOW_SECONDS)
    if attempts >= MAX_LOGIN_ATTEMPTS:
        raise HTTPException(
            status_code=429,
            detail="Too many login attempts. Try again later.",
            headers={"Retry-After": str(LOGIN_WINDOW_SECONDS)},
        )
    await rate_store.increment(key, window=LOGIN_WINDOW_SECONDS)

@router.post("/auth/login")
async def login(
    email: str,
    password: str,
    _: None = Depends(rate_limit_login),
):
    # SECURE: Rate limited to 5 attempts per 5 minutes per IP
    user = await authenticate(email, password)
    return {"token": await create_token(user.id)}
```

---

### SEC-API-002: Excessive Data Exposure

- **Severity:** HIGH
- **Category:** API Security
- **Description:** API endpoints returning raw database records instead of filtered response models. Internal fields (creation timestamps, internal flags, admin notes, hashed passwords) are exposed to clients.
- **Detection Regex:** `return.*response\["Item"\]` or `return.*model_dump\(\)` without filtering
- **Impact:** Exposure of internal data, sensitive metadata, and implementation details to API consumers.
- **CWE:** CWE-359 (Exposure of Private Personal Information to an Unauthorized Actor)
- **OWASP:** API3:2023 - Broken Object Property Level Authorization

**Vulnerable Pattern:**

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/trails/{trail_id}")
async def get_trail(trail_id: str):
    response = await table.get_item(Key={"tenant_id": org_id, "id": trail_id})
    # VULNERABLE: Returns ALL DynamoDB attributes including internal ones
    # Exposes: internal_notes, admin_flags, created_by_ip, version, etc.
    return response["Item"]
```

**Secure Pattern:**

```python
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

class TrailResponse(BaseModel):
    """Public-facing trail data - only fields the client should see."""
    id: str
    name: str
    description: str
    difficulty: str
    length_km: float
    status: str
    updated_at: str

router = APIRouter()

@router.get("/trails/{trail_id}", response_model=TrailResponse)
async def get_trail(trail_id: str):
    response = await table.get_item(
        Key={"tenant_id": org_id, "id": trail_id},
        # SECURE: Only fetch needed attributes
        ProjectionExpression="id, #n, description, difficulty, length_km, #s, updated_at",
        ExpressionAttributeNames={"#n": "name", "#s": "status"},
    )
    item = response.get("Item")
    if not item:
        raise HTTPException(status_code=404, detail="Resource not found")
    # SECURE: Response model filters out any extra attributes
    return TrailResponse(**item)
```

---

### SEC-API-003: Missing Request Size Limits

- **Severity:** MEDIUM
- **Category:** API Security
- **Description:** API endpoints without request body size limits. Attackers can send extremely large payloads to exhaust memory, cause timeouts, or incur excessive costs.
- **Detection Regex:** Missing `max_content_length` or body size middleware
- **Impact:** Denial of service through memory exhaustion or excessive Lambda duration/cost.
- **CWE:** CWE-770 (Allocation of Resources Without Limits or Throttling)
- **OWASP:** API4:2023 - Unrestricted Resource Consumption

**Vulnerable Pattern:**

```python
from fastapi import APIRouter, UploadFile

router = APIRouter()

@router.post("/upload")
async def upload_photo(file: UploadFile):
    # VULNERABLE: No file size limit - attacker uploads 10GB file
    content = await file.read()  # Reads entire file into memory
    await s3.put_object(Bucket=BUCKET, Key=f"photos/{file.filename}", Body=content)
    return {"uploaded": True}
```

**Secure Pattern:**

```python
from fastapi import APIRouter, HTTPException, UploadFile

router = APIRouter()

MAX_PHOTO_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}

@router.post("/upload")
async def upload_photo(file: UploadFile):
    # SECURE: Validate content type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # SECURE: Stream with size limit
    total_size = 0
    chunks: list[bytes] = []
    while True:
        chunk = await file.read(8192)
        if not chunk:
            break
        total_size += len(chunk)
        if total_size > MAX_PHOTO_SIZE:
            raise HTTPException(status_code=413, detail="File too large (max 10MB)")
        chunks.append(chunk)

    content = b"".join(chunks)
    await s3.put_object(Bucket=BUCKET, Key=f"photos/{file.filename}", Body=content)
    return {"uploaded": True}
```

---

### SEC-API-004: Missing API Gateway Throttling

- **Severity:** HIGH
- **Category:** API Security
- **Description:** API Gateway deployed without stage-level or method-level throttling. Without throttling, a single client can overwhelm Lambda concurrency limits and cause denial of service for all users.
- **Detection Regex:** `RestApi\((?!.*throttle)` or `Stage\((?!.*throttle)`
- **Impact:** Denial of service. Single attacker exhausts Lambda concurrency (default 1000), blocking all users.
- **CWE:** CWE-770 (Allocation of Resources Without Limits or Throttling)
- **OWASP:** API4:2023 - Unrestricted Resource Consumption

**Vulnerable Pattern:**

```python
# Pulumi infrastructure code
import pulumi_aws as aws

# VULNERABLE: No throttling configured
api_stage = aws.apigateway.Stage(
    "prod-stage",
    rest_api=api.id,
    stage_name="prod",
    deployment=deployment.id,
)
```

**Secure Pattern:**

```python
# Pulumi infrastructure code
import pulumi_aws as aws

# SECURE: Stage-level and method-level throttling
api_stage = aws.apigateway.Stage(
    "prod-stage",
    rest_api=api.id,
    stage_name="prod",
    deployment=deployment.id,
)

# SECURE: Default throttling for all methods
aws.apigateway.MethodSettings(
    "api-settings",
    rest_api=api.id,
    stage_name=api_stage.stage_name,
    method_path="*/*",
    settings=aws.apigateway.MethodSettingsSettingsArgs(
        throttling_rate_limit=5000,    # 5000 RPS steady state
        throttling_burst_limit=2500,   # 2500 burst
    ),
)

# Stricter limits for auth endpoints
aws.apigateway.MethodSettings(
    "auth-settings",
    rest_api=api.id,
    stage_name=api_stage.stage_name,
    method_path="auth/POST",
    settings=aws.apigateway.MethodSettingsSettingsArgs(
        throttling_rate_limit=1000,
        throttling_burst_limit=500,
    ),
)
```

---

### SEC-API-005: Missing WAF Protection

- **Severity:** HIGH
- **Category:** API Security
- **Description:** API Gateway deployed without AWS WAF (Web Application Firewall). WAF provides rate limiting, IP blocking, SQL injection detection, and bot protection at the edge before requests reach Lambda.
- **Detection Regex:** `RestApi\((?!.*waf|.*web_acl)` or missing `WebAcl` association
- **Impact:** No edge-level protection against common attacks (SQLi, XSS, bot traffic, DDoS).
- **CWE:** CWE-693 (Protection Mechanism Failure)
- **OWASP:** A02:2021 - Cryptographic Failures (grouped with misconfig)

**Vulnerable Pattern:**

```python
# Pulumi infrastructure code
import pulumi_aws as aws

# VULNERABLE: No WAF protection on API Gateway
api = aws.apigateway.RestApi(
    "traillens-api",
    name="traillens-api",
)

# API is directly exposed to all internet traffic
# No rate limiting, no IP blocking, no SQLi detection
```

**Secure Pattern:**

```python
# Pulumi infrastructure code
import pulumi_aws as aws

# SECURE: WAF with managed rules
web_acl = aws.wafv2.WebAcl(
    "api-waf",
    scope="REGIONAL",
    default_action=aws.wafv2.WebAclDefaultActionArgs(
        allow=aws.wafv2.WebAclDefaultActionAllowArgs(),
    ),
    rules=[
        aws.wafv2.WebAclRuleArgs(
            name="rate-limit",
            priority=1,
            action=aws.wafv2.WebAclRuleActionArgs(
                block=aws.wafv2.WebAclRuleActionBlockArgs(),
            ),
            statement=aws.wafv2.WebAclRuleStatementArgs(
                rate_based_statement=aws.wafv2.WebAclRuleStatementRateBasedStatementArgs(
                    limit=2000,              # 2000 requests per 5 minutes per IP
                    aggregate_key_type="IP",
                ),
            ),
            visibility_config=aws.wafv2.WebAclRuleVisibilityConfigArgs(
                sampled_requests_enabled=True,
                cloudwatch_metrics_enabled=True,
                metric_name="rate-limit",
            ),
        ),
        aws.wafv2.WebAclRuleArgs(
            name="aws-managed-common",
            priority=2,
            override_action=aws.wafv2.WebAclRuleOverrideActionArgs(
                none=aws.wafv2.WebAclRuleOverrideActionNoneArgs(),
            ),
            statement=aws.wafv2.WebAclRuleStatementArgs(
                managed_rule_group_statement=aws.wafv2.WebAclRuleStatementManagedRuleGroupStatementArgs(
                    vendor_name="AWS",
                    name="AWSManagedRulesCommonRuleSet",
                ),
            ),
            visibility_config=aws.wafv2.WebAclRuleVisibilityConfigArgs(
                sampled_requests_enabled=True,
                cloudwatch_metrics_enabled=True,
                metric_name="aws-common-rules",
            ),
        ),
    ],
    visibility_config=aws.wafv2.WebAclVisibilityConfigArgs(
        sampled_requests_enabled=True,
        cloudwatch_metrics_enabled=True,
        metric_name="api-waf",
    ),
)

# Associate WAF with API Gateway
aws.wafv2.WebAclAssociation(
    "api-waf-association",
    resource_arn=api_stage.arn,
    web_acl_arn=web_acl.arn,
)
```

---

## Category 10: Logging & Monitoring

### SEC-LOG-001: Log Injection

- **Severity:** MEDIUM
- **Category:** Logging & Monitoring
- **Description:** User input logged without sanitization. Attackers inject newlines or control characters to forge log entries, hide malicious activity, or exploit log processing tools (e.g., injecting ANSI escape codes for terminal-based viewers).
- **Detection Regex:** `(log|logger)\.(info|error)\(.*request\.(body|query|headers)` or `log.*f".*request`
- **Impact:** Log forgery, hiding attack evidence, exploiting log analysis tools.
- **CWE:** CWE-117 (Improper Output Neutralization for Logs)
- **OWASP:** A09:2021 - Security Logging and Monitoring Failures

**Vulnerable Pattern:**

```python
from api.shared.logging import log_info

@router.get("/search")
async def search_trails(q: str):
    # VULNERABLE: User input directly in log message
    # Attacker: q="harmless\n[CRITICAL] Admin access granted to attacker"
    log_info(f"Search query: {q}")
    results = await trail_service.search(q)
    return results
```

**Secure Pattern:**

```python
import re
from api.shared.logging import log_info

def sanitize_log_value(value: str, max_length: int = 200) -> str:
    """Remove control characters and truncate for safe logging."""
    sanitized = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", value)
    return sanitized[:max_length]

@router.get("/search")
async def search_trails(q: str):
    # SECURE: Sanitized input in structured metadata field
    log_info("Trail search executed", metadata={
        "query": sanitize_log_value(q),
        "query_length": len(q),
    })
    results = await trail_service.search(q)
    return results
```

---

### SEC-LOG-002: Insufficient Security Logging

- **Severity:** MEDIUM
- **Category:** Logging & Monitoring
- **Description:** Security-relevant events (failed logins, permission denials, password changes, admin actions) not logged. Without these logs, security incidents cannot be detected or investigated.
- **Detection Regex:** Authentication/authorization handlers without log statements
- **Impact:** Inability to detect attacks in progress or investigate security incidents after the fact.
- **CWE:** CWE-778 (Insufficient Logging)
- **OWASP:** A09:2021 - Security Logging and Monitoring Failures

**Vulnerable Pattern:**

```python
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/auth/login")
async def login(email: str, password: str):
    user = await user_repo.find_by_email(email)
    if not user or not await verify_password(password, user.password_hash):
        # VULNERABLE: Failed login not logged - brute force is invisible
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": await create_token(user.id)}

@router.put("/users/{user_id}/role")
async def update_role(user_id: str, role: str):
    # VULNERABLE: Admin action not logged
    await user_repo.update_role(user_id, role)
    return {"message": "Role updated"}
```

**Secure Pattern:**

```python
from fastapi import APIRouter, Depends, HTTPException, Request
from api.shared.logging import log_info, log_warning

router = APIRouter()

@router.post("/auth/login")
async def login(request: Request, email: str, password: str):
    user = await user_repo.find_by_email(email)
    if not user or not await verify_password(password, user.password_hash):
        # SECURE: Failed login logged with context for threat detection
        log_warning("AUTH_FAILURE", metadata={
            "event": "login_failed",
            "client_ip": request.client.host,
            "user_agent": request.headers.get("user-agent", "unknown"),
        })
        raise HTTPException(status_code=401, detail="Invalid credentials")

    log_info("Login successful", metadata={"user_id": user.id})
    return {"token": await create_token(user.id)}

@router.put("/users/{user_id}/role")
async def update_role(
    user_id: str,
    role: str,
    admin: AuthenticatedUser = Depends(require_admin),
):
    # SECURE: Admin action logged for audit trail
    log_info("Admin role change", metadata={
        "admin_id": admin.id,
        "target_user_id": user_id,
        "new_role": role,
    })
    await user_repo.update_role(user_id, role)
    return {"message": "Role updated"}
```

---

### SEC-LOG-003: Missing Security Alarms

- **Severity:** MEDIUM
- **Category:** Logging & Monitoring
- **Description:** No CloudWatch alarms configured for security-relevant metrics. Without automated alerts, attacks can proceed undetected for hours or days.
- **Detection Regex:** Missing CloudWatch metric filters or alarms for `AUTH_FAILURE`, `COGNITO_API_FAILURE`, or error rate thresholds
- **Impact:** Attacks proceed undetected. No automated response to credential stuffing, brute force, or data exfiltration.
- **CWE:** CWE-778 (Insufficient Logging)
- **OWASP:** A09:2021 - Security Logging and Monitoring Failures

**Vulnerable Pattern:**

```python
# Pulumi infrastructure code
# VULNERABLE: No security alarms defined
# Auth failures, unusual API patterns, and errors go unnoticed

lambda_function = aws.lambda_.Function(
    "api",
    # ... function config ...
)
# No CloudWatch alarms, no metric filters, no SNS notifications
```

**Secure Pattern:**

```python
# Pulumi infrastructure code
import pulumi_aws as aws

# SECURE: CloudWatch metric filter for auth failures
auth_failure_filter = aws.cloudwatch.LogMetricFilter(
    "auth-failure-filter",
    log_group_name=api_log_group.name,
    pattern='{ $.error_code = "AUTH_FAILURE" }',
    metric_transformation=aws.cloudwatch.LogMetricFilterMetricTransformationArgs(
        name="AuthFailureCount",
        namespace="TrailLens/Security",
        value="1",
    ),
)

# SECURE: Alarm on excessive auth failures (possible brute force)
auth_failure_alarm = aws.cloudwatch.MetricAlarm(
    "auth-failure-alarm",
    metric_name="AuthFailureCount",
    namespace="TrailLens/Security",
    statistic="Sum",
    period=300,           # 5 minute window
    evaluation_periods=1,
    threshold=50,         # 50 failures in 5 minutes
    comparison_operator="GreaterThanThreshold",
    alarm_actions=[security_sns_topic.arn],
    alarm_description="Possible brute force attack - 50+ auth failures in 5 minutes",
)
```

---

### SEC-LOG-004: Credentials in Log Output

- **Severity:** CRITICAL
- **Category:** Logging & Monitoring
- **Description:** Logging API keys, passwords, tokens, AWS credentials, or other secrets. These appear in CloudWatch Logs, which may be accessible to operations teams, exported to third-party tools, or retained beyond the secret's lifetime.
- **Detection Regex:** `(log|logger|print)\(.*\b(password|secret|token|key|authorization|bearer)\b`
- **Impact:** Secret exposure in long-lived logs. Credential rotation does not eliminate exposure if old values are in logs.
- **CWE:** CWE-532 (Insertion of Sensitive Information into Log File)
- **OWASP:** A09:2021 - Security Logging and Monitoring Failures

**Vulnerable Pattern:**

```python
from api.shared.logging import log_info, log_error

async def call_external_api(api_key: str, endpoint: str):
    # VULNERABLE: API key logged
    log_info(f"Calling {endpoint} with key {api_key}")

    headers = {"Authorization": f"Bearer {api_key}"}
    response = await client.get(endpoint, headers=headers)

    if response.status_code != 200:
        # VULNERABLE: Full headers (including auth) in error log
        log_error(f"API call failed: {response.status_code}, headers: {headers}")
```

**Secure Pattern:**

```python
from api.shared.logging import log_info, log_error

async def call_external_api(api_key: str, endpoint: str):
    # SECURE: Only log non-sensitive identifiers
    log_info("External API call initiated", metadata={
        "endpoint": endpoint,
        "key_prefix": api_key[:4] + "***",  # First 4 chars only for debugging
    })

    headers = {"Authorization": f"Bearer {api_key}"}
    response = await client.get(endpoint, headers=headers)

    if response.status_code != 200:
        # SECURE: Log status without credentials
        log_error("External API call failed", metadata={
            "endpoint": endpoint,
            "status_code": response.status_code,
        })
```

---

### SEC-LOG-005: Missing Audit Trail

- **Severity:** MEDIUM
- **Category:** Logging & Monitoring
- **Description:** Data modification operations (create, update, delete) performed without audit logging. Without audit trails, unauthorized changes cannot be detected or attributed.
- **Detection Regex:** `(put_item|update_item|delete_item)\((?!.*audit|.*log)` or write operations without log statements
- **Impact:** Cannot detect unauthorized data changes, attribute changes to specific users, or reconstruct event timelines.
- **CWE:** CWE-778 (Insufficient Logging)
- **OWASP:** A09:2021 - Security Logging and Monitoring Failures

**Vulnerable Pattern:**

```python
import aioboto3

async def update_trail_condition(tenant_id: str, trail_id: str, condition: str):
    session = aioboto3.Session()
    async with session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table("trails")
        # VULNERABLE: No audit trail - who changed what and when?
        await table.update_item(
            Key={"tenant_id": tenant_id, "id": trail_id},
            UpdateExpression="SET #c = :condition",
            ExpressionAttributeNames={"#c": "condition"},
            ExpressionAttributeValues={":condition": condition},
        )
```

**Secure Pattern:**

```python
import time
import aioboto3
from api.shared.logging import log_info

async def update_trail_condition(
    tenant_id: str,
    trail_id: str,
    condition: str,
    updated_by: str,
):
    session = aioboto3.Session()
    async with session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table("trails")
        now = int(time.time())

        # SECURE: Update with audit metadata
        await table.update_item(
            Key={"tenant_id": tenant_id, "id": trail_id},
            UpdateExpression=(
                "SET #c = :condition, updated_at = :now, updated_by = :user"
            ),
            ExpressionAttributeNames={"#c": "condition"},
            ExpressionAttributeValues={
                ":condition": condition,
                ":now": now,
                ":user": updated_by,
            },
        )

        # SECURE: Structured audit log
        log_info("Trail condition updated", metadata={
            "tenant_id": tenant_id,
            "trail_id": trail_id,
            "new_condition": condition,
            "updated_by": updated_by,
            "timestamp": now,
        })

        # SECURE: Write to audit table for long-term retention
        audit_table = await dynamodb.Table("audit_log")
        await audit_table.put_item(Item={
            "tenant_id": tenant_id,
            "event_id": f"{trail_id}#{now}",
            "action": "update_trail_condition",
            "resource_id": trail_id,
            "actor_id": updated_by,
            "changes": {"condition": condition},
            "timestamp": now,
        })
```

---

### SEC-LOG-006: Silent Exception in Middleware

- **Severity:** HIGH
- **Category:** Logging & Monitoring
- **Description:** Middleware catching broad exceptions (`except Exception`) without logging before returning an error response. Unhandled exceptions that escape route handlers become invisible to CloudWatch, preventing alerting and incident response. This is especially dangerous in security-critical middleware (e.g., security headers, CORS, auth middleware) where silent failures mask attack attempts.
- **Detection Regex:** `except\s+Exception.*:\s*\n(?:.*\n)*?.*(?:JSONResponse|Response)\(.*status_code=5` (multiline — look for except blocks returning 5xx without a `log_error` call)
- **Impact:** Production errors invisible. No CloudWatch alarms fire. Security incidents go undetected. Attack patterns cannot be identified in logs.
- **CWE:** CWE-778 (Insufficient Logging)
- **OWASP:** A09:2021 - Security Logging and Monitoring Failures

**Vulnerable Pattern:**

```python
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
        except Exception:
            # VULNERABLE: Exception silently swallowed — no log, no alert
            response = JSONResponse({"detail": "Internal server error"}, status_code=500)
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response
```

**Secure Pattern:**

```python
from starlette.middleware.base import BaseHTTPMiddleware
from api.shared.logging import log_error

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
        except Exception as exc:
            # SECURE: Log with structured error code for CloudWatch metric filter
            log_error(
                "Unhandled exception in request pipeline",
                error_code="UNHANDLED_REQUEST_ERROR",
                metadata={
                    "path": request.url.path,
                    "method": request.method,
                    "error": str(exc),
                },
            )
            response = JSONResponse({"detail": "Internal server error"}, status_code=500)
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response
```

---

## Category 11: Async & Concurrency Security

### SEC-ASYNC-001: Race Condition in Check-Then-Act

- **Severity:** HIGH
- **Category:** Async & Concurrency Security
- **Description:** Pattern where code checks a condition asynchronously (e.g., "does this record exist?") then acts on the result. Between the check and the act, another coroutine can modify the state, leading to duplicate records, double-spending, or authorization bypass.
- **Detection Regex:** `if.*await.*\n.*await.*create` or `get.*await.*\n.*if not.*\n.*await.*put`
- **Impact:** Duplicate record creation, double-spending, race condition bypass of unique constraints.
- **CWE:** CWE-367 (Time-of-check Time-of-use Race Condition)
- **OWASP:** A08:2021 - Software and Data Integrity Failures

**Vulnerable Pattern:**

```python
import aioboto3

async def create_reservation(tenant_id: str, trail_id: str, user_id: str):
    session = aioboto3.Session()
    async with session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table("reservations")

        # VULNERABLE: Check-then-act race condition
        # Two concurrent requests can both see "no existing" and both create
        existing = await table.get_item(
            Key={"tenant_id": tenant_id, "id": f"{trail_id}#{user_id}"},
        )
        if "Item" not in existing:
            await table.put_item(Item={
                "tenant_id": tenant_id,
                "id": f"{trail_id}#{user_id}",
                "trail_id": trail_id,
                "user_id": user_id,
            })
            return {"status": "reserved"}
        return {"status": "already_reserved"}
```

**Secure Pattern:**

```python
import aioboto3
from botocore.exceptions import ClientError

async def create_reservation(tenant_id: str, trail_id: str, user_id: str):
    session = aioboto3.Session()
    async with session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table("reservations")

        # SECURE: Atomic put with condition - no race condition possible
        try:
            await table.put_item(
                Item={
                    "tenant_id": tenant_id,
                    "id": f"{trail_id}#{user_id}",
                    "trail_id": trail_id,
                    "user_id": user_id,
                },
                ConditionExpression="attribute_not_exists(id)",
            )
            return {"status": "reserved"}
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ConditionalCheckFailedException":
                return {"status": "already_reserved"}
            raise
```

---

### SEC-ASYNC-002: Missing asyncio.Lock on Shared State

- **Severity:** HIGH
- **Category:** Async & Concurrency Security
- **Description:** Module-level mutable state accessed by multiple async coroutines without an `asyncio.Lock`. While Python's GIL prevents true parallel execution, `await` points allow coroutine interleaving, creating race conditions on shared state.
- **Detection Regex:** Global mutable variables modified in `async def` without `asyncio.Lock`
- **Impact:** Corrupted shared state, inconsistent cache, lost updates.
- **CWE:** CWE-362 (Concurrent Execution using Shared Resource with Improper Synchronization)
- **OWASP:** A08:2021 - Software and Data Integrity Failures

**Vulnerable Pattern:**

```python
# VULNERABLE: Shared mutable state without lock
_cache: dict[str, dict] = {}

async def get_config(key: str) -> dict:
    if key not in _cache:
        # Between this check and the assignment below, another coroutine
        # could also reach here and start fetching the same config
        config = await fetch_config_from_dynamodb(key)
        _cache[key] = config  # Race: another coroutine may overwrite
    return _cache[key]

async def invalidate_cache(key: str):
    # Race: another coroutine may read stale data between check and delete
    if key in _cache:
        del _cache[key]
```

**Secure Pattern:**

```python
import asyncio

_cache: dict[str, dict] = {}
_cache_lock = asyncio.Lock()

async def get_config(key: str) -> dict:
    # SECURE: Lock prevents interleaving between check and set
    async with _cache_lock:
        if key not in _cache:
            config = await fetch_config_from_dynamodb(key)
            _cache[key] = config
        return _cache[key]

async def invalidate_cache(key: str):
    # SECURE: Lock prevents race between read and delete
    async with _cache_lock:
        _cache.pop(key, None)
```

---

### SEC-ASYNC-003: DynamoDB Optimistic Locking Missing

- **Severity:** HIGH
- **Category:** Async & Concurrency Security
- **Description:** DynamoDB `update_item` operations without `ConditionExpression` for version checking. Concurrent updates can silently overwrite each other (last-write-wins), losing data.
- **Detection Regex:** `update_item\((?!.*ConditionExpression)` or `put_item\((?!.*ConditionExpression)`
- **Impact:** Lost updates in concurrent write scenarios. Data integrity violations.
- **CWE:** CWE-367 (Time-of-check Time-of-use Race Condition)
- **OWASP:** A08:2021 - Software and Data Integrity Failures

**Vulnerable Pattern:**

```python
import aioboto3

async def update_trail_description(tenant_id: str, trail_id: str, description: str):
    session = aioboto3.Session()
    async with session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table("trails")
        # VULNERABLE: No version check - concurrent updates silently lost
        # User A reads version 5, User B reads version 5
        # User A writes (version becomes 6), User B writes (overwrites A's changes)
        await table.update_item(
            Key={"tenant_id": tenant_id, "id": trail_id},
            UpdateExpression="SET description = :desc",
            ExpressionAttributeValues={":desc": description},
        )
```

**Secure Pattern:**

```python
import aioboto3
from botocore.exceptions import ClientError
from fastapi import HTTPException

async def update_trail_description(
    tenant_id: str,
    trail_id: str,
    description: str,
    expected_version: int,
):
    session = aioboto3.Session()
    async with session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table("trails")
        try:
            # SECURE: Optimistic locking via version field
            await table.update_item(
                Key={"tenant_id": tenant_id, "id": trail_id},
                UpdateExpression="SET description = :desc, version = :new_ver",
                ConditionExpression="version = :expected_ver",
                ExpressionAttributeValues={
                    ":desc": description,
                    ":new_ver": expected_version + 1,
                    ":expected_ver": expected_version,
                },
            )
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ConditionalCheckFailedException":
                raise HTTPException(
                    status_code=409,
                    detail="Resource was modified by another request. Please retry.",
                ) from exc
            raise
```

---

### SEC-ASYNC-004: aioboto3 Resource Leak

- **Severity:** MEDIUM
- **Category:** Async & Concurrency Security
- **Description:** Creating aioboto3 clients or resources without using `async with` context manager. Resources that are not properly closed leak connections, leading to connection pool exhaustion and eventual service failure.
- **Detection Regex:** `aioboto3\.(Session\(\)\.)?(client|resource)\(` without `async with`
- **Impact:** Connection pool exhaustion, memory leaks, eventual Lambda timeout or crash.
- **CWE:** CWE-404 (Improper Resource Shutdown or Release)
- **OWASP:** A10:2021 - Server-Side Request Forgery (grouped with resource management)

**Vulnerable Pattern:**

```python
import aioboto3

async def get_trail(tenant_id: str, trail_id: str):
    session = aioboto3.Session()
    # VULNERABLE: Resource not used with async context manager
    # Connection is never properly closed
    dynamodb = await session.resource("dynamodb").__aenter__()
    table = await dynamodb.Table("trails")
    response = await table.get_item(Key={"tenant_id": tenant_id, "id": trail_id})
    # dynamodb.__aexit__ never called - connection leaked
    return response.get("Item")
```

**Secure Pattern:**

```python
import aioboto3

session = aioboto3.Session()

async def get_trail(tenant_id: str, trail_id: str):
    # SECURE: async with ensures proper cleanup
    async with session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table("trails")
        response = await table.get_item(
            Key={"tenant_id": tenant_id, "id": trail_id},
        )
        return response.get("Item")
    # Connection properly closed when exiting async with block
```

---

## Category 12: AWS Service-Specific

### SEC-AWS-001: SES Email Spoofing

- **Severity:** HIGH
- **Category:** AWS Service-Specific
- **Description:** SES configured without DKIM, SPF, or DMARC records. Attackers who gain access to the SES API (or find an SSRF vulnerability) can send emails appearing to come from the application's domain.
- **Detection Regex:** `send_email\(` without DKIM/DMARC configuration checks
- **Impact:** Phishing emails sent from the application's verified domain, bypassing email filters.
- **CWE:** CWE-284 (Improper Access Control)
- **OWASP:** A02:2021 - Cryptographic Failures (grouped with misconfig)

**Vulnerable Pattern:**

```python
import aioboto3

async def send_notification(to_email: str, subject: str, body: str):
    session = aioboto3.Session()
    async with session.client("ses") as ses:
        # VULNERABLE: No input validation on recipient
        # No DKIM/SPF/DMARC configured for domain
        await ses.send_email(
            Source="noreply@traillenshq.com",
            Destination={"ToAddresses": [to_email]},
            Message={
                "Subject": {"Data": subject},
                "Body": {"Html": {"Data": body}},
            },
        )
```

**Secure Pattern:**

```python
import re
import aioboto3
from api.shared.logging import log_info, log_error

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$")

async def send_notification(to_email: str, subject: str, body: str):
    # SECURE: Validate recipient email format
    if not EMAIL_REGEX.match(to_email):
        raise ValueError("Invalid email address")

    session = aioboto3.Session()
    async with session.client("ses") as ses:
        try:
            # SECURE: Use configuration set for tracking and DKIM
            await ses.send_email(
                Source="noreply@traillenshq.com",
                Destination={"ToAddresses": [to_email]},
                Message={
                    "Subject": {"Data": subject},
                    "Body": {"Html": {"Data": body}},
                },
                ConfigurationSetName="traillens-email-config",
            )
            log_info("Email sent", metadata={
                "recipient_domain": to_email.split("@")[1],
            })
        except Exception as exc:
            log_error("SES_SEND_FAILURE", metadata={
                "error_type": type(exc).__name__,
            })
            raise
```

---

### SEC-AWS-002: SNS Data Exfiltration

- **Severity:** HIGH
- **Category:** AWS Service-Specific
- **Description:** SNS topic policies that allow unauthorized subscriptions or publishing. Attackers can subscribe their endpoint to receive all notifications (data exfiltration) or publish malicious messages (spam/phishing).
- **Detection Regex:** SNS topic policy with `"Principal": "*"` or `"sns:Subscribe"` without conditions
- **Impact:** Data exfiltration via unauthorized subscription, spam/phishing via unauthorized publishing.
- **CWE:** CWE-200 (Exposure of Sensitive Information to an Unauthorized Actor)
- **OWASP:** A02:2021 - Cryptographic Failures (grouped with misconfig)

**Vulnerable Pattern:**

```python
# Pulumi infrastructure code
import json
import pulumi_aws as aws

notifications_topic = aws.sns.Topic("notifications")

# VULNERABLE: Anyone can subscribe or publish
aws.sns.TopicPolicy(
    "notifications-policy",
    arn=notifications_topic.arn,
    policy=json.dumps({
        "Statement": [{
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["sns:Subscribe", "sns:Publish"],
            "Resource": "*",
        }],
    }),
)
```

**Secure Pattern:**

```python
# Pulumi infrastructure code
import json
import pulumi
import pulumi_aws as aws

notifications_topic = aws.sns.Topic(
    "notifications",
    kms_master_key_id="alias/aws/sns",  # Encryption at rest
)

# SECURE: Only specific Lambda role can publish
aws.sns.TopicPolicy(
    "notifications-policy",
    arn=notifications_topic.arn,
    policy=pulumi.Output.all(
        notifications_topic.arn, api_lambda_role.arn,
    ).apply(lambda args: json.dumps({
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"AWS": args[1]},
            "Action": "sns:Publish",
            "Resource": args[0],
        }],
    })),
)
```

---

### SEC-AWS-003: Lambda Event Injection

- **Severity:** HIGH
- **Category:** AWS Service-Specific
- **Description:** Lambda handler using event fields directly without validation. The event object is user-controlled (from API Gateway, SQS, S3 triggers, etc.) and can contain unexpected types, missing keys, or malicious values.
- **Detection Regex:** `event\[["'].*["']\]` without validation or `event\.get\(` used directly in queries
- **Impact:** Injection attacks, type confusion, or crashes from malformed event data.
- **CWE:** CWE-20 (Improper Input Validation)
- **OWASP:** A05:2021 - Security Misconfiguration

**Vulnerable Pattern:**

```python
import json

async def handler(event: dict, context):
    # VULNERABLE: Direct event field access without validation
    # API Gateway event body could be anything
    body = json.loads(event["body"])
    trail_name = body["name"]      # KeyError if missing
    trail_id = body["trail_id"]    # Could be any type

    # VULNERABLE: User-controlled values directly in DynamoDB operation
    await table.put_item(Item={
        "id": trail_id,
        "name": trail_name,
    })
```

**Secure Pattern:**

```python
import json
from uuid import uuid4
from pydantic import BaseModel, ValidationError

class CreateTrailRequest(BaseModel):
    name: str
    description: str = ""

async def handler(event: dict, context):
    # SECURE: Validate event structure
    body_str = event.get("body")
    if not body_str:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing body"})}

    try:
        body = json.loads(body_str)
    except json.JSONDecodeError:
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid JSON"})}

    # SECURE: Pydantic validation enforces types and constraints
    try:
        request = CreateTrailRequest(**body)
    except ValidationError as exc:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Validation failed", "details": exc.errors()}),
        }

    # SECURE: Validated data used in DynamoDB operation
    await table.put_item(Item={
        "tenant_id": user.org_id,  # From verified JWT, not event
        "id": str(uuid4()),
        "name": request.name,
        "description": request.description,
    })
```

---

### SEC-AWS-004: Lambda Secret Initialization per Invocation

- **Severity:** MEDIUM
- **Category:** AWS Service-Specific
- **Description:** Fetching secrets from AWS Secrets Manager inside the Lambda handler function instead of at module level. This adds latency to every request and increases Secrets Manager API costs (currently $0.05 per 10,000 API calls).
- **Detection Regex:** `def handler.*:.*get_secret_value` or `async def handler.*:.*secretsmanager`
- **Impact:** Added latency per request, increased Secrets Manager costs, potential throttling at high scale.
- **CWE:** CWE-400 (Uncontrolled Resource Consumption)
- **OWASP:** A02:2021 - Cryptographic Failures (grouped with misconfig)

**Vulnerable Pattern:**

```python
import json
import aioboto3

async def handler(event: dict, context):
    # VULNERABLE: Secret fetched on EVERY invocation
    # Adds ~50-100ms latency per request, costs $0.05 per 10K calls
    session = aioboto3.Session()
    async with session.client("secretsmanager") as client:
        response = await client.get_secret_value(SecretId="traillens/api-keys")
        secrets = json.loads(response["SecretString"])

    # Use secrets...
    api_key = secrets["stripe_key"]
```

**Secure Pattern:**

```python
import json
import aioboto3

# SECURE: Module-level secret cache - survives across invocations
_session = aioboto3.Session()
_secrets_cache: dict[str, dict] | None = None

async def _get_secrets() -> dict:
    """Fetch secrets once and cache for Lambda container lifetime."""
    global _secrets_cache
    if _secrets_cache is None:
        async with _session.client("secretsmanager") as client:
            response = await client.get_secret_value(SecretId="traillens/api-keys")
            _secrets_cache = json.loads(response["SecretString"])
    return _secrets_cache

async def handler(event: dict, context):
    # SECURE: Cached - only first invocation fetches from Secrets Manager
    secrets = await _get_secrets()
    api_key = secrets["stripe_key"]
```

---

### SEC-AWS-005: Missing X-Ray Tracing

- **Severity:** LOW
- **Category:** AWS Service-Specific
- **Description:** Lambda functions and API Gateway without AWS X-Ray tracing enabled. Without distributed tracing, performance bottlenecks, error chains, and security-relevant latency patterns are invisible.
- **Detection Regex:** `Function\((?!.*tracing_config)` or `Stage\((?!.*xray_tracing_enabled)`
- **Impact:** Blind to distributed performance issues, unable to trace request paths through microservices for security investigation.
- **CWE:** CWE-778 (Insufficient Logging)
- **OWASP:** A09:2021 - Security Logging and Monitoring Failures

**Vulnerable Pattern:**

```python
# Pulumi infrastructure code
import pulumi_aws as aws

# VULNERABLE: No X-Ray tracing - blind to performance and security issues
lambda_function = aws.lambda_.Function(
    "api",
    function_name="traillens-api",
    runtime="python3.14",
    handler="api.main.handler",
    role=lambda_role.arn,
    # No tracing_config
)

api_stage = aws.apigateway.Stage(
    "prod",
    rest_api=api.id,
    stage_name="prod",
    deployment=deployment.id,
    # No xray_tracing_enabled
)
```

**Secure Pattern:**

```python
# Pulumi infrastructure code
import pulumi_aws as aws

# SECURE: X-Ray tracing enabled
lambda_function = aws.lambda_.Function(
    "api",
    function_name="traillens-api",
    runtime="python3.14",
    handler="api.main.handler",
    role=lambda_role.arn,
    tracing_config=aws.lambda_.FunctionTracingConfigArgs(
        mode="Active",
    ),
)

api_stage = aws.apigateway.Stage(
    "prod",
    rest_api=api.id,
    stage_name="prod",
    deployment=deployment.id,
    xray_tracing_enabled=True,
)

# Lambda role needs X-Ray permissions
aws.iam.RolePolicyAttachment(
    "lambda-xray-policy",
    role=lambda_role.name,
    policy_arn="arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess",
)
```

---

## Sources

1. https://cwe.mitre.org/data/definitions/327.html - CWE-327: Use of a Broken or Risky Cryptographic Algorithm
2. https://cwe.mitre.org/data/definitions/345.html - CWE-345: Insufficient Verification of Data Authenticity
3. https://cwe.mitre.org/data/definitions/613.html - CWE-613: Insufficient Session Expiration
4. https://cwe.mitre.org/data/definitions/798.html - CWE-798: Use of Hard-coded Credentials
5. https://cwe.mitre.org/data/definitions/352.html - CWE-352: Cross-Site Request Forgery
6. https://cwe.mitre.org/data/definitions/601.html - CWE-601: URL Redirection to Untrusted Site
7. https://cwe.mitre.org/data/definitions/287.html - CWE-287: Improper Authentication
8. https://cwe.mitre.org/data/definitions/384.html - CWE-384: Session Fixation
9. https://cwe.mitre.org/data/definitions/614.html - CWE-614: Sensitive Cookie Without Secure Attribute
10. https://cwe.mitre.org/data/definitions/328.html - CWE-328: Use of Weak Hash
11. https://cwe.mitre.org/data/definitions/307.html - CWE-307: Improper Restriction of Excessive Authentication Attempts
12. https://cwe.mitre.org/data/definitions/294.html - CWE-294: Authentication Bypass by Capture-replay
13. https://cwe.mitre.org/data/definitions/639.html - CWE-639: Authorization Bypass Through User-Controlled Key
14. https://cwe.mitre.org/data/definitions/285.html - CWE-285: Improper Authorization
15. https://cwe.mitre.org/data/definitions/668.html - CWE-668: Exposure of Resource to Wrong Sphere
16. https://cwe.mitre.org/data/definitions/915.html - CWE-915: Improperly Controlled Modification of Dynamically-Determined Object Attributes
17. https://cwe.mitre.org/data/definitions/250.html - CWE-250: Execution with Unnecessary Privileges
18. https://cwe.mitre.org/data/definitions/330.html - CWE-330: Use of Insufficiently Random Values
19. https://cwe.mitre.org/data/definitions/943.html - CWE-943: Improper Neutralization of Special Elements in Data Query Logic
20. https://cwe.mitre.org/data/definitions/22.html - CWE-22: Improper Limitation of a Pathname to a Restricted Directory
21. https://cwe.mitre.org/data/definitions/78.html - CWE-78: OS Command Injection
22. https://cwe.mitre.org/data/definitions/918.html - CWE-918: Server-Side Request Forgery
23. https://cwe.mitre.org/data/definitions/1336.html - CWE-1336: Improper Neutralization of Special Elements in Template Engine
24. https://cwe.mitre.org/data/definitions/95.html - CWE-95: Improper Neutralization of Directives in Dynamically Evaluated Code
25. https://cwe.mitre.org/data/definitions/1333.html - CWE-1333: Inefficient Regular Expression Complexity
26. https://cwe.mitre.org/data/definitions/113.html - CWE-113: HTTP Response Splitting
27. https://cwe.mitre.org/data/definitions/502.html - CWE-502: Deserialization of Untrusted Data
28. https://cwe.mitre.org/data/definitions/290.html - CWE-290: Authentication Bypass by Spoofing
29. https://cwe.mitre.org/data/definitions/311.html - CWE-311: Missing Encryption of Sensitive Data
30. https://cwe.mitre.org/data/definitions/208.html - CWE-208: Observable Timing Discrepancy
31. https://cwe.mitre.org/data/definitions/321.html - CWE-321: Use of Hard-coded Cryptographic Key
32. https://cwe.mitre.org/data/definitions/532.html - CWE-532: Insertion of Sensitive Information into Log File
33. https://cwe.mitre.org/data/definitions/209.html - CWE-209: Generation of Error Message Containing Sensitive Information
34. https://cwe.mitre.org/data/definitions/359.html - CWE-359: Exposure of Private Personal Information
35. https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/ - OWASP API1:2023
36. https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/ - OWASP API3:2023
37. https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/ - OWASP API4:2023
38. https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/ - OWASP API5:2023
39. https://owasp.org/Top10/A01_2021-Broken_Access_Control/ - OWASP A01:2021
40. https://owasp.org/Top10/A02_2021-Cryptographic_Failures/ - OWASP A02:2021
41. https://owasp.org/Top10/A03_2021-Injection/ - OWASP A03:2021
42. https://owasp.org/Top10/A04_2021-Insecure_Design/ - OWASP A04:2021
43. https://owasp.org/Top10/A05_2021-Security_Misconfiguration/ - OWASP A05:2021
44. https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/ - OWASP A07:2021
45. https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/ - OWASP A08:2021
46. https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/ - OWASP A09:2021
47. https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_(SSRF)/ - OWASP A10:2021
48. https://portswigger.net/web-security/jwt - PortSwigger JWT Attacks
49. https://portswigger.net/web-security/jwt/algorithm-confusion - JWT Algorithm Confusion
50. https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html - OWASP JWT Cheat Sheet
51. https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html - OWASP Authentication Cheat Sheet
52. https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html - OWASP Session Management
53. https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html - OWASP CSRF Prevention
54. https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-verifying-a-jwt.html - AWS Cognito JWT Verification
55. https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ExpressionAttributeValues.html - DynamoDB Expression Attribute Values
56. https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html - DynamoDB Partition Key Design
57. https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html - Lambda Environment Variables
58. https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html - AWS Secrets Manager
59. https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html - AWS WAF Developer Guide
60. https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html - AWS X-Ray Developer Guide
61. https://cwe.mitre.org/data/definitions/1395.html - CWE-1395: Dependency on Vulnerable Third-Party Component
62. https://cwe.mitre.org/data/definitions/489.html - CWE-489: Active Debug Code
63. https://cwe.mitre.org/data/definitions/942.html - CWE-942: Permissive Cross-domain Policy
64. https://cwe.mitre.org/data/definitions/693.html - CWE-693: Protection Mechanism Failure
65. https://cwe.mitre.org/data/definitions/284.html - CWE-284: Improper Access Control
66. https://cwe.mitre.org/data/definitions/459.html - CWE-459: Incomplete Cleanup
67. https://cwe.mitre.org/data/definitions/200.html - CWE-200: Exposure of Sensitive Information
68. https://cwe.mitre.org/data/definitions/204.html - CWE-204: Observable Response Discrepancy
69. https://cwe.mitre.org/data/definitions/396.html - CWE-396: Declaration of Catch for Generic Exception
70. https://cwe.mitre.org/data/definitions/770.html - CWE-770: Allocation of Resources Without Limits
71. https://cwe.mitre.org/data/definitions/117.html - CWE-117: Improper Output Neutralization for Logs
72. https://cwe.mitre.org/data/definitions/778.html - CWE-778: Insufficient Logging
73. https://cwe.mitre.org/data/definitions/367.html - CWE-367: Time-of-check Time-of-use Race Condition
74. https://cwe.mitre.org/data/definitions/362.html - CWE-362: Concurrent Execution using Shared Resource
75. https://cwe.mitre.org/data/definitions/404.html - CWE-404: Improper Resource Shutdown or Release
76. https://cwe.mitre.org/data/definitions/400.html - CWE-400: Uncontrolled Resource Consumption
77. https://cwe.mitre.org/data/definitions/20.html - CWE-20: Improper Input Validation
78. https://pyjwt.readthedocs.io/en/stable/ - PyJWT Documentation
79. https://aioboto3.readthedocs.io/en/latest/ - aioboto3 Documentation
80. https://fastapi.tiangolo.com/tutorial/security/ - FastAPI Security Tutorial
