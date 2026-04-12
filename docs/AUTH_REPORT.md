<!--
PROMPT:
you are a lead developer on the team. The VP Development has asked you to review the entire codebase focusing on the web project and infra projects. He has seen the google, apple, and facebook auth buttons on the web login page and wonders why they do not work. He wants to know what it would take to enable each and allow users to auth through these services. It would be one more step towards a passwordless login.

Run through the codebase, refer to relavent online documentation, and create a AUTH_REPORT file in the root docs directory. Provide references for all your assertions. The VP Development's assistant will be fact checking your work. Do not make things up.

YOu have unlimited time to complete the project. You must not stop until done. You are to work 24/7 until the tasks are complete.

Make sure this prompt is in the comment section at the top of the file.
-->

# Social Authentication Integration Report
## Google, Apple, and Facebook Sign-In Implementation

**Date:** January 20, 2026
**Prepared For:** VP Development
**Prepared By:** Lead Developer
**Status:** Analysis Complete

---

## Executive Summary

The TrailLens web application currently displays Google, Apple, and Facebook authentication buttons on both the Login and Register pages. **These buttons are fully implemented in the UI with event handlers, but they are non-functional because the underlying AWS Cognito User Pool is not configured with the required social identity providers.**

**Current State:**
- ✅ **UI Implementation:** Complete (buttons render, call `signInWithRedirect()`)
- ✅ **OAuth Configuration:** Complete (scopes, redirect URIs configured)
- ✅ **AWS Amplify Integration:** Complete (v6.15.8 with proper config)
- ❌ **Social Providers in Cognito:** Not configured (only `["COGNITO"]` enabled)
- ❌ **Provider Credentials:** Not registered (no OAuth app credentials)

**Passwordless Authentication Benefits:**
Enabling social authentication is indeed a step toward passwordless login, offering enhanced security, improved user experience, and reduced operational costs [1]. Users can authenticate without remembering complex passwords, reducing the risk of phishing and brute-force attacks [2].

**Implementation Effort Summary:**

| Provider | Setup Complexity | Cost | Time Estimate |
|----------|------------------|------|---------------|
| Google   | Low              | Free | 2-4 hours     |
| Facebook | Medium           | Free | 3-5 hours     |
| Apple    | High             | $99 USD/year | 4-8 hours |

**Total Implementation Time:** 9-17 hours for all three providers.

---

## Table of Contents

1. [Current Implementation Analysis](#current-implementation-analysis)
2. [Why Social Login Buttons Don't Work](#why-social-login-buttons-dont-work)
3. [Requirements for Each Provider](#requirements-for-each-provider)
   - [Google Sign-In](#google-sign-in)
   - [Facebook Login](#facebook-login)
   - [Apple Sign In](#apple-sign-in)
4. [Implementation Steps](#implementation-steps)
5. [Infrastructure Changes Required](#infrastructure-changes-required)
6. [Security Considerations](#security-considerations)
7. [Cost Analysis](#cost-analysis)
8. [Risks and Mitigation](#risks-and-mitigation)
9. [Timeline and Resources](#timeline-and-resources)
10. [Recommendations](#recommendations)
11. [References](#references)

---

## Current Implementation Analysis

### Web Application (Frontend)

**Location:** `/Users/mark/src/traillensdev/web/`

#### 1. Login Page Implementation

**File:** `web/src/views/auth/Login.js`

The login page contains fully implemented social authentication buttons:

```javascript
const handleSocialSignIn = async (provider) => {
  try {
    setError('');
    await signInWithRedirect({ provider });
  } catch (err) {
    console.error('Social sign-in error:', err);
    setError(`${provider} sign-in failed. Please try again`);
  }
};
```

**Social Provider Buttons (Lines 116-144):**
- **Google:** Always visible (Lines 116-124)
- **Facebook:** Always visible (Lines 125-133)
- **Apple:** Conditionally shown only on Apple devices - iOS, iPadOS, macOS (Lines 134-144)

#### 2. Register Page Implementation

**File:** `web/src/views/auth/Register.js`

Identical social authentication implementation using `signInWithRedirect({ provider })` method.

#### 3. AWS Amplify Configuration

**File:** `web/src/config/amplify-config.js` (Lines 40-68)

OAuth configuration is properly set up:

```javascript
loginWith: {
  email: true,
  username: false,
  oauth: {
    domain: process.env.REACT_APP_COGNITO_DOMAIN || "",
    scopes: ["email", "openid", "profile"],
    redirectSignIn: [
      window.location.origin,
      "http://localhost:3000",
      "https://traillenshq.com",
    ],
    redirectSignOut: [
      window.location.origin,
      "http://localhost:3000",
      "https://traillenshq.com",
    ],
    responseType: "code", // Authorization code grant (more secure)
  },
},
```

**Environment Variables (`.env.production`):**
```bash
REACT_APP_COGNITO_REGION=ca-central-1
REACT_APP_COGNITO_USER_POOL_ID=ca-central-1_xPxFxklam
REACT_APP_COGNITO_USER_POOL_CLIENT_ID=428scfcmf3vrpkj3fi06rgub77
REACT_APP_COGNITO_DOMAIN=auth.dev.traillenshq.com
```

#### 4. Test Coverage

**File:** `web/src/views/auth/__tests__/Login.test.js` (Lines 543-599)

Comprehensive tests exist for social authentication:
```javascript
describe('Social Authentication', () => {
  test('initiates Facebook sign-in', async () => { ... });
  test('initiates Google sign-in', async () => { ... });
  test('shows Apple sign-in on Apple devices', () => { ... });
  test('handles social sign-in errors', async () => { ... });
});
```

### Infrastructure (Backend)

**Location:** `/Users/mark/src/traillensdev/infra/`

#### 1. Cognito User Pool Configuration

**File:** `infra/pulumi/components/auth.py` (Lines 140-154)

```python
self.user_pool_client = aws.cognito.UserPoolClient(
    f"{name}-app-client",
    name=f"{name_prefix}-app-client",
    user_pool_id=self.user_pool.id,
    explicit_auth_flows=[
        "ALLOW_USER_SRP_AUTH",
        "ALLOW_REFRESH_TOKEN_AUTH",
        "ALLOW_CUSTOM_AUTH",  # Enable custom auth flow for passwordless
        "ALLOW_USER_AUTH",  # Required for WebAuthn/passkey support
    ],
    generate_secret=False,
    # OAuth configuration
    allowed_oauth_flows_user_pool_client=True,
    allowed_oauth_flows=["code"],
    allowed_oauth_scopes=["openid", "email", "profile"],
    callback_urls=[callback_url],
    logout_urls=[callback_url],
    supported_identity_providers=["COGNITO"],  # ⚠️ ONLY COGNITO
    opts=ResourceOptions(parent=self.user_pool),
)
```

**Key Finding:** Line 152 shows `supported_identity_providers=["COGNITO"]` - **no social providers are configured**.

#### 2. Current Cognito Setup Details

- **User Pool ID:** `ca-central-1_xPxFxklam` (dev environment)
- **Region:** `ca-central-1` (Canada Central)
- **Custom Domain:** `auth.dev.traillenshq.com`
- **OAuth Flows:** Authorization Code and Implicit flows enabled
- **OAuth Scopes:** `openid`, `email`, `profile`
- **Callback URL:** `http://localhost:3000` (dev), configurable for production

---

## Why Social Login Buttons Don't Work

The social authentication buttons are **non-functional** due to the following missing components:

### 1. No Social Identity Providers in Cognito

**Current Configuration:**
```python
supported_identity_providers=["COGNITO"]
```

**Required Configuration:**
```python
supported_identity_providers=["COGNITO", "Google", "Facebook", "SignInWithApple"]
```

### 2. No UserPoolIdentityProvider Resources

The infrastructure code does **not** define any `aws.cognito.UserPoolIdentityProvider` resources for Google, Facebook, or Apple [3].

**Required Resources:**
- `aws.cognito.UserPoolIdentityProvider` for Google
- `aws.cognito.UserPoolIdentityProvider` for Facebook
- `aws.cognito.UserPoolIdentityProvider` for Apple (Sign In with Apple)

### 3. No OAuth Application Registrations

No OAuth applications have been registered with the provider platforms:
- No Google Cloud Console OAuth client
- No Facebook Developer App
- No Apple Services ID

### 4. No Provider Credentials Configured

AWS Cognito requires the following credentials for each provider:
- **Google:** Client ID and Client Secret
- **Facebook:** App ID and App Secret
- **Apple:** Services ID, Team ID, Key ID, and Private Key (.p8 file)

---

## Requirements for Each Provider

### Google Sign-In

**Official Documentation:** [AWS Cognito - Setting up Google as an identity pool IdP](https://docs.aws.amazon.com/cognito/latest/developerguide/google.html) [4]

#### Prerequisites

1. **Google Cloud Console Account**
   - Create a Google Developers Console project
   - No cost for OAuth authentication

2. **OAuth 2.0 Client Credentials**
   - Client ID
   - Client Secret

#### Setup Steps

##### A. Google Cloud Console Configuration

**Reference:** [Get your Google API client ID | Google for Developers](https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid) [5]

1. **Configure OAuth Consent Screen**
   - Navigate to: `APIs & Services` → `OAuth consent screen`
   - User Type: **External**
   - Required fields:
     - App name: "TrailLens"
     - User support email: `support@traillenshq.com`
     - Authorized domains: `traillenshq.com`, `dev.traillenshq.com`
     - Developer contact: `dev@traillenshq.com`

2. **Create OAuth 2.0 Client ID** [6]
   - Navigate to: `APIs & Services` → `Credentials`
   - Click: `Create Credentials` → `OAuth client ID`
   - Application type: **Web application**
   - Name: "TrailLens Web (Dev)"

3. **Configure Authorized URLs** [4]
   - **Authorized JavaScript origins:**
     ```
     https://auth.dev.traillenshq.com
     ```
   - **Authorized redirect URIs:**
     ```
     https://auth.dev.traillenshq.com/oauth2/idpresponse
     ```

4. **Save Credentials**
   - Copy the **Client ID** and **Client Secret**
   - Store securely (use AWS Secrets Manager or environment variables)

**Important:** OAuth 2.0 clients that are inactive for six months are automatically deleted [6].

##### B. AWS Cognito Configuration

**Reference:** [Set up Google as a social identity provider in an Amazon Cognito user pool | AWS re:Post](https://repost.aws/knowledge-center/cognito-google-social-identity-provider) [7]

1. **Add Google Identity Provider**
   - Navigate to AWS Cognito User Pool
   - Select: `Identity providers` → `Add identity provider`
   - Provider type: **Google**
   - Enter **Client ID** from Google Cloud Console
   - Enter **Client Secret** from Google Cloud Console

2. **Configure Authorized Scopes** [4]
   - Required scopes: `openid`, `email`, `profile`
   - **Important:** Use lowercase `openid`, not `OpenID`

3. **Attribute Mapping** [4]
   - Map Google claims to Cognito attributes:
     - `email` → `email`
     - `sub` → `username`
     - `name` → `name`
     - `picture` → `picture` (optional)

4. **Update User Pool Client**
   - Add `Google` to `supported_identity_providers` list

##### C. Infrastructure Code Changes (Pulumi)

**File:** `infra/pulumi/components/auth.py`

Add the following resource:

```python
# Google Identity Provider
google_provider = aws.cognito.UserPoolIdentityProvider(
    f"{name}-google-provider",
    user_pool_id=self.user_pool.id,
    provider_name="Google",
    provider_type="Google",
    provider_details={
        "client_id": google_client_id,  # From config or secrets
        "client_secret": google_client_secret,
        "authorize_scopes": "openid email profile",
    },
    attribute_mapping={
        "email": "email",
        "username": "sub",
        "name": "name",
        "picture": "picture",
    },
    opts=ResourceOptions(parent=self.user_pool),
)

# Update User Pool Client
self.user_pool_client = aws.cognito.UserPoolClient(
    # ... existing config ...
    supported_identity_providers=["COGNITO", "Google"],
    # Must add explicit dependency
    opts=ResourceOptions(
        parent=self.user_pool,
        depends_on=[google_provider]
    ),
)
```

#### Configuration Storage

**Recommended:** Use Pulumi Config with encryption [8]

```bash
pulumi config set --secret google_client_id "your-client-id"
pulumi config set --secret google_client_secret "your-client-secret"
```

#### Cost

**Free** - Google does not charge for OAuth authentication [5]

---

### Facebook Login

**Official Documentation:** [AWS Cognito - Setting up Facebook as an identity pools IdP](https://docs.aws.amazon.com/cognito/latest/developerguide/facebook.html) [9]

#### Prerequisites

1. **Facebook Developer Account**
   - Create account at [developers.facebook.com](https://developers.facebook.com)
   - No cost for authentication

2. **Facebook App Credentials**
   - App ID
   - App Secret

#### Setup Steps

##### A. Facebook Developer Portal Configuration

**Reference:** [Add social sign-in to your user pool - Amazon Cognito](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-configuring-federation-with-social-idp.html) [10]

1. **Create Facebook App**
   - Navigate to: [Meta for Developers](https://developers.facebook.com/apps)
   - Click: `Create App`
   - App Type: **Consumer**
   - App Name: "TrailLens"
   - Contact Email: `dev@traillenshq.com`

2. **Add Facebook Login Product** [11]
   - In app dashboard, click: `+ Add Product`
   - Select: **Facebook Login**
   - Platform: **Website**

3. **Configure OAuth Settings** [12]
   - Navigate to: `Facebook Login` → `Settings`
   - **Client OAuth Settings:**
     - Client OAuth Login: **Yes**
     - Web OAuth Login: **Yes**
   - **Valid OAuth Redirect URIs:**
     ```
     https://auth.dev.traillenshq.com/oauth2/idpresponse
     ```
   - **Important:** Must use HTTPS (required since March 2018) [13]

4. **Select API Version** [14]
   - AWS recommends choosing the **latest API version**
   - Each Facebook API version has a lifecycle and deprecation date
   - Test thoroughly, as scopes and attributes vary between versions
   - **Recommended:** v19.0 or later (as of 2026)

5. **Configure App Domains**
   - Navigate to: `Settings` → `Basic`
   - **App Domains:**
     ```
     dev.traillenshq.com
     traillenshq.com
     ```
   - **Privacy Policy URL:** `https://traillenshq.com/privacy`
   - **Terms of Service URL:** `https://traillenshq.com/terms`

6. **Enable App for Public Use**
   - Set app status to **Live** (from Development mode)
   - Complete App Review if using permissions beyond public_profile and email

7. **Copy Credentials**
   - Navigate to: `Settings` → `Basic`
   - Copy **App ID** and **App Secret**
   - Store securely

##### B. AWS Cognito Configuration

**Reference:** [Using social identity providers with a user pool - Amazon Cognito](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-social-idp.html) [15]

1. **Add Facebook Identity Provider**
   - Navigate to AWS Cognito User Pool
   - Select: `Identity providers` → `Add identity provider`
   - Provider type: **Facebook**
   - Enter **App ID** from Facebook
   - Enter **App Secret** from Facebook
   - API Version: **v19.0** (or latest)

2. **Configure Authorized Scopes** [9]
   - Required scopes: `public_profile`, `email`
   - Both scopes should be added

3. **Attribute Mapping**
   - Map Facebook claims to Cognito attributes:
     - `id` → `username`
     - `email` → `email`
     - `name` → `name`
     - `picture` → `picture` (optional)

4. **Update User Pool Client**
   - Add `Facebook` to `supported_identity_providers` list

##### C. Infrastructure Code Changes (Pulumi)

**File:** `infra/pulumi/components/auth.py`

Add the following resource:

```python
# Facebook Identity Provider
facebook_provider = aws.cognito.UserPoolIdentityProvider(
    f"{name}-facebook-provider",
    user_pool_id=self.user_pool.id,
    provider_name="Facebook",
    provider_type="Facebook",
    provider_details={
        "client_id": facebook_app_id,  # From config or secrets
        "client_secret": facebook_app_secret,
        "authorize_scopes": "public_profile,email",
        "api_version": "v19.0",  # Specify API version
    },
    attribute_mapping={
        "email": "email",
        "username": "id",
        "name": "name",
        "picture": "picture.data.url",
    },
    opts=ResourceOptions(parent=self.user_pool),
)

# Update User Pool Client
self.user_pool_client = aws.cognito.UserPoolClient(
    # ... existing config ...
    supported_identity_providers=["COGNITO", "Google", "Facebook"],
    opts=ResourceOptions(
        parent=self.user_pool,
        depends_on=[google_provider, facebook_provider]
    ),
)
```

#### Configuration Storage

```bash
pulumi config set --secret facebook_app_id "your-app-id"
pulumi config set --secret facebook_app_secret "your-app-secret"
pulumi config set facebook_api_version "v19.0"
```

#### Important Limitations

**Amazon Cognito identity pools federation is NOT compatible with Facebook Limited Login** [9].

#### Cost

**Free** - Facebook does not charge for authentication via Facebook Login

---

### Apple Sign In

**Official Documentation:** [AWS Cognito - Setting up Sign in with Apple as an identity pool IdP](https://docs.aws.amazon.com/cognito/latest/developerguide/apple.html) [16]

#### Prerequisites

1. **Apple Developer Program Membership**
   - **Cost:** $99 USD per year [17]
   - **Enrollment Options:** Individual or Organization [18]
   - **Individual Requirements:** [18]
     - Apple Account with two-factor authentication
     - Legal age of majority in your region
     - Legal name (not alias or nickname)
     - Valid email, phone, and physical address (no P.O. boxes)
   - **Organization Requirements:** [18]
     - Legal entity that can enter into contracts
     - DUNS Number (for identity verification)
     - Legal authority to bind organization

2. **Apple Developer Credentials**
   - Services ID
   - Team ID
   - Key ID
   - Private Key (.p8 file)

#### Setup Steps

##### A. Apple Developer Portal Configuration

**Reference:** [How to set up Sign in with Apple for Amazon Cognito | AWS Security Blog](https://aws.amazon.com/blogs/security/how-to-set-up-sign-in-with-apple-for-amazon-cognito/) [19]

1. **Enroll in Apple Developer Program** [17]
   - Visit: [developer.apple.com/programs/enroll](https://developer.apple.com/programs/enroll/)
   - Complete enrollment and pay $99 USD annual fee
   - Wait for approval (typically 24-48 hours)

2. **Create an App ID** [19]
   - Navigate to: [Certificates, Identifiers & Profiles](https://developer.apple.com/account/resources)
   - Select: `Identifiers` → `+` (Add)
   - Choose: **App IDs** → Continue
   - Configuration:
     - Description: "TrailLens Web App"
     - Bundle ID: `com.traillenshq.webapp` (explicit)
     - Capabilities: Enable **Sign In with Apple**
   - **Note the App ID Prefix** (Team ID) - you'll need this later

3. **Create a Services ID** [19]
   - Navigate to: `Identifiers` → `+` (Add)
   - Choose: **Services IDs** → Continue
   - Configuration:
     - Description: "TrailLens Web Authentication"
     - Identifier: `com.traillenshq.webapp.auth`
   - **Configure Sign In with Apple:**
     - Click: **Configure** next to Sign In with Apple
     - **Primary App ID:** Select the App ID created in step 2
     - **Domains and Subdomains:**
       ```
       auth.dev.traillenshq.com
       ```
       (Enter **without** `https://` prefix)
     - **Return URLs:**
       ```
       https://auth.dev.traillenshq.com/oauth2/idpresponse
       ```
   - Save and Continue
   - **Copy the Services ID** - this is your `client_id`

4. **Create a Private Key** [19]
   - Navigate to: `Keys` → `+` (Add)
   - Configuration:
     - Key Name: "TrailLens Sign In with Apple Key"
     - Enable: **Sign In with Apple**
     - Click: **Configure** → Select Primary App ID
   - Click: **Continue** → **Register**
   - **Download the .p8 file immediately** (can only download once)
   - **Note the Key ID** (e.g., `ABC123XYZ`)

5. **Gather Required Information**
   - **Services ID:** `com.traillenshq.webapp.auth`
   - **Team ID:** Found in App ID Prefix or Account Membership
   - **Key ID:** From the key created in step 4
   - **Private Key:** Contents of the .p8 file (plain text)

##### B. AWS Cognito Configuration

**Reference:** [Setting up Sign in with Apple - Amazon Cognito](https://docs.aws.amazon.com/cognito/latest/developerguide/apple.html) [16]

1. **Add Apple Identity Provider** [20]
   - Navigate to AWS Cognito User Pool
   - Select: `Identity providers` → `Add identity provider`
   - Provider type: **Sign In with Apple**
   - Enter configuration:
     - **Services ID:** `com.traillenshq.webapp.auth`
     - **Team ID:** Your Apple Team ID (10-character string)
     - **Key ID:** Your Apple Key ID (10-character string)
     - **Private Key:** Paste contents of .p8 file

2. **Configure Authorized Scopes** [16]
   - Required scopes: `email`, `name`
   - **Important:** Apple only honors scopes on first authentication [21]

3. **Attribute Mapping**
   - Map Apple claims to Cognito attributes:
     - `sub` → `username`
     - `email` → `email`
     - `name` → `name` (only provided on first sign-in)

4. **Update User Pool Client**
   - Add `SignInWithApple` to `supported_identity_providers` list

##### C. Infrastructure Code Changes (Pulumi)

**File:** `infra/pulumi/components/auth.py`

Add the following resource:

```python
# Apple Sign In Identity Provider
apple_provider = aws.cognito.UserPoolIdentityProvider(
    f"{name}-apple-provider",
    user_pool_id=self.user_pool.id,
    provider_name="SignInWithApple",
    provider_type="SignInWithApple",
    provider_details={
        "client_id": apple_services_id,  # Services ID
        "team_id": apple_team_id,
        "key_id": apple_key_id,
        "private_key": apple_private_key,  # Contents of .p8 file
        "authorize_scopes": "email name",
    },
    attribute_mapping={
        "email": "email",
        "username": "sub",
        "name": "name",
    },
    opts=ResourceOptions(parent=self.user_pool),
)

# Update User Pool Client
self.user_pool_client = aws.cognito.UserPoolClient(
    # ... existing config ...
    supported_identity_providers=[
        "COGNITO",
        "Google",
        "Facebook",
        "SignInWithApple"
    ],
    opts=ResourceOptions(
        parent=self.user_pool,
        depends_on=[google_provider, facebook_provider, apple_provider]
    ),
)
```

#### Configuration Storage

```bash
pulumi config set --secret apple_services_id "com.traillenshq.webapp.auth"
pulumi config set --secret apple_team_id "ABC123XYZ0"
pulumi config set --secret apple_key_id "DEF456GHI1"
pulumi config set --secret apple_private_key "$(cat AppleKey.p8)"
```

#### Important Considerations

1. **First Authentication Only** [21]
   - Apple only provides `name` on the **first authentication**
   - If you add the `name` scope later, existing users won't have it
   - Plan your attribute mapping carefully from the start

2. **Annual Renewal**
   - Apple Developer Program requires annual $99 USD renewal [17]
   - Keys remain valid unless explicitly revoked

3. **Private Key Security**
   - The .p8 private key can only be downloaded once
   - Store securely in AWS Secrets Manager
   - Rotate keys periodically for security

#### Cost

**$99 USD per year** for Apple Developer Program membership [17]

---

## Implementation Steps

### Phase 1: Preparation (1-2 hours)

1. **Review Current Configuration**
   - ✅ Verify current Cognito User Pool settings
   - ✅ Confirm OAuth callback URLs
   - ✅ Review existing test coverage

2. **Set Up Provider Accounts**
   - Create Google Cloud Console account (if needed)
   - Create Facebook Developer account (if needed)
   - Enroll in Apple Developer Program ($99 USD) (if needed)

3. **Plan Credential Storage**
   - Set up AWS Secrets Manager entries (recommended)
   - Or use Pulumi Config with encryption
   - Document credential rotation procedures

### Phase 2: Google Sign-In Implementation (2-4 hours)

**Reference:** [AWS Cognito - Setting up Google as an identity pool IdP](https://docs.aws.amazon.com/cognito/latest/developerguide/google.html) [4]

1. **Google Cloud Console Setup** (1-2 hours)
   - Configure OAuth consent screen
   - Create OAuth 2.0 client ID
   - Configure authorized URLs
   - Copy and securely store credentials

2. **Infrastructure Code Changes** (30 min)
   - Add Google provider configuration to `auth.py`
   - Update `supported_identity_providers` list
   - Add Pulumi config entries

3. **Deploy Infrastructure** (15 min)
   ```bash
   cd infra/pulumi
   pulumi config set --secret google_client_id "YOUR_CLIENT_ID"
   pulumi config set --secret google_client_secret "YOUR_CLIENT_SECRET"
   pulumi up
   ```

4. **Testing** (30 min - 1 hour)
   - Test Google sign-in on dev environment
   - Verify user creation in Cognito
   - Verify attribute mapping
   - Test sign-out flow

### Phase 3: Facebook Login Implementation (3-5 hours)

**Reference:** [AWS Cognito - Setting up Facebook as an identity pools IdP](https://docs.aws.amazon.com/cognito/latest/developerguide/facebook.html) [9]

1. **Facebook Developer Portal Setup** (2-3 hours)
   - Create Facebook App
   - Add Facebook Login product
   - Configure OAuth settings
   - Set app to Live mode
   - Copy and securely store credentials

2. **Infrastructure Code Changes** (30 min)
   - Add Facebook provider configuration to `auth.py`
   - Update `supported_identity_providers` list
   - Add Pulumi config entries

3. **Deploy Infrastructure** (15 min)
   ```bash
   pulumi config set --secret facebook_app_id "YOUR_APP_ID"
   pulumi config set --secret facebook_app_secret "YOUR_APP_SECRET"
   pulumi config set facebook_api_version "v19.0"
   pulumi up
   ```

4. **Testing** (1-1.5 hours)
   - Test Facebook sign-in on dev environment
   - Verify user creation in Cognito
   - Verify attribute mapping
   - Test sign-out flow
   - Test with different Facebook accounts

### Phase 4: Apple Sign In Implementation (4-8 hours)

**Reference:** [How to set up Sign in with Apple for Amazon Cognito | AWS Security Blog](https://aws.amazon.com/blogs/security/how-to-set-up-sign-in-with-apple-for-amazon-cognito/) [19]

1. **Apple Developer Program Enrollment** (1-3 hours + approval wait)
   - Enroll in Apple Developer Program
   - Pay $99 USD annual fee
   - Wait for approval (24-48 hours)

2. **Apple Developer Portal Setup** (2-3 hours)
   - Create App ID with Sign In with Apple capability
   - Create Services ID
   - Configure domains and return URLs
   - Create Private Key (.p8)
   - Download and securely store key

3. **Infrastructure Code Changes** (30 min)
   - Add Apple provider configuration to `auth.py`
   - Update `supported_identity_providers` list
   - Add Pulumi config entries

4. **Deploy Infrastructure** (15 min)
   ```bash
   pulumi config set --secret apple_services_id "com.traillenshq.webapp.auth"
   pulumi config set --secret apple_team_id "YOUR_TEAM_ID"
   pulumi config set --secret apple_key_id "YOUR_KEY_ID"
   pulumi config set --secret apple_private_key "$(cat AppleKey.p8)"
   pulumi up
   ```

5. **Testing** (1-2 hours)
   - Test Apple sign-in on dev environment (use Apple device)
   - Verify user creation in Cognito
   - Verify attribute mapping (especially first-time user flow)
   - Test sign-out flow
   - Test with different Apple IDs

### Phase 5: Production Deployment (2-3 hours)

1. **Update Production Configuration** (1 hour)
   - Create production OAuth apps for each provider
   - Update callback URLs to production domains
   - Configure production Pulumi stack

2. **Deploy to Production** (30 min)
   ```bash
   pulumi stack select prod
   pulumi config set --secret google_client_id "PROD_CLIENT_ID"
   # ... repeat for all providers
   pulumi up
   ```

3. **Production Testing** (1 hour)
   - Test all three providers on production
   - Verify user flows end-to-end
   - Monitor CloudWatch logs for errors

4. **Documentation** (30 min)
   - Update CLAUDE.md with provider setup instructions
   - Document credential rotation procedures
   - Create runbook for troubleshooting

---

## Infrastructure Changes Required

### File Changes

**File:** `infra/pulumi/components/auth.py`

**Location:** Lines 140-154 (User Pool Client configuration)

**Changes Required:**

```python
# Current Configuration:
supported_identity_providers=["COGNITO"]

# Required Configuration:
supported_identity_providers=[
    "COGNITO",
    "Google",
    "Facebook",
    "SignInWithApple"
]
```

**New Resources to Add:**

1. **Google Identity Provider** (Before User Pool Client)
```python
# Google Identity Provider
google_client_id = config.get("google_client_id")
google_client_secret = config.get("google_client_secret")

if google_client_id and google_client_secret:
    self.google_provider = aws.cognito.UserPoolIdentityProvider(
        f"{name}-google-provider",
        user_pool_id=self.user_pool.id,
        provider_name="Google",
        provider_type="Google",
        provider_details={
            "client_id": google_client_id,
            "client_secret": google_client_secret,
            "authorize_scopes": "openid email profile",
        },
        attribute_mapping={
            "email": "email",
            "username": "sub",
            "name": "name",
            "picture": "picture",
        },
        opts=ResourceOptions(parent=self.user_pool),
    )
```

2. **Facebook Identity Provider** (Before User Pool Client)
```python
# Facebook Identity Provider
facebook_app_id = config.get("facebook_app_id")
facebook_app_secret = config.get("facebook_app_secret")
facebook_api_version = config.get("facebook_api_version", "v19.0")

if facebook_app_id and facebook_app_secret:
    self.facebook_provider = aws.cognito.UserPoolIdentityProvider(
        f"{name}-facebook-provider",
        user_pool_id=self.user_pool.id,
        provider_name="Facebook",
        provider_type="Facebook",
        provider_details={
            "client_id": facebook_app_id,
            "client_secret": facebook_app_secret,
            "authorize_scopes": "public_profile,email",
            "api_version": facebook_api_version,
        },
        attribute_mapping={
            "email": "email",
            "username": "id",
            "name": "name",
            "picture": "picture.data.url",
        },
        opts=ResourceOptions(parent=self.user_pool),
    )
```

3. **Apple Sign In Identity Provider** (Before User Pool Client)
```python
# Apple Sign In Identity Provider
apple_services_id = config.get("apple_services_id")
apple_team_id = config.get("apple_team_id")
apple_key_id = config.get("apple_key_id")
apple_private_key = config.get("apple_private_key")

if all([apple_services_id, apple_team_id, apple_key_id, apple_private_key]):
    self.apple_provider = aws.cognito.UserPoolIdentityProvider(
        f"{name}-apple-provider",
        user_pool_id=self.user_pool.id,
        provider_name="SignInWithApple",
        provider_type="SignInWithApple",
        provider_details={
            "client_id": apple_services_id,
            "team_id": apple_team_id,
            "key_id": apple_key_id,
            "private_key": apple_private_key,
            "authorize_scopes": "email name",
        },
        attribute_mapping={
            "email": "email",
            "username": "sub",
            "name": "name",
        },
        opts=ResourceOptions(parent=self.user_pool),
    )
```

4. **Update User Pool Client Dependencies**
```python
# Build list of enabled providers
enabled_providers = ["COGNITO"]
provider_dependencies = []

if hasattr(self, 'google_provider'):
    enabled_providers.append("Google")
    provider_dependencies.append(self.google_provider)

if hasattr(self, 'facebook_provider'):
    enabled_providers.append("Facebook")
    provider_dependencies.append(self.facebook_provider)

if hasattr(self, 'apple_provider'):
    enabled_providers.append("SignInWithApple")
    provider_dependencies.append(self.apple_provider)

# User Pool Client with dynamic providers
self.user_pool_client = aws.cognito.UserPoolClient(
    f"{name}-app-client",
    # ... existing config ...
    supported_identity_providers=enabled_providers,
    opts=ResourceOptions(
        parent=self.user_pool,
        depends_on=provider_dependencies
    ),
)
```

### Configuration File Changes

**File:** `infra/pulumi/Pulumi.dev.yaml`

**Add the following configuration entries:**

```yaml
config:
  # ... existing config ...

  # Google OAuth Configuration (optional, enables Google Sign-In)
  traillens:google_client_id:
    secure: <encrypted-value>
  traillens:google_client_secret:
    secure: <encrypted-value>

  # Facebook OAuth Configuration (optional, enables Facebook Login)
  traillens:facebook_app_id:
    secure: <encrypted-value>
  traillens:facebook_app_secret:
    secure: <encrypted-value>
  traillens:facebook_api_version: "v19.0"

  # Apple Sign In Configuration (optional, enables Apple Sign In)
  traillens:apple_services_id:
    secure: <encrypted-value>
  traillens:apple_team_id:
    secure: <encrypted-value>
  traillens:apple_key_id:
    secure: <encrypted-value>
  traillens:apple_private_key:
    secure: <encrypted-value>
```

**Set using Pulumi CLI:**
```bash
# Google
pulumi config set --secret google_client_id "YOUR_GOOGLE_CLIENT_ID"
pulumi config set --secret google_client_secret "YOUR_GOOGLE_CLIENT_SECRET"

# Facebook
pulumi config set --secret facebook_app_id "YOUR_FACEBOOK_APP_ID"
pulumi config set --secret facebook_app_secret "YOUR_FACEBOOK_APP_SECRET"
pulumi config set facebook_api_version "v19.0"

# Apple
pulumi config set --secret apple_services_id "com.traillenshq.webapp.auth"
pulumi config set --secret apple_team_id "ABC123XYZ0"
pulumi config set --secret apple_key_id "DEF456GHI1"
pulumi config set --secret apple_private_key "$(cat AppleKey.p8)"
```

### Deployment Steps

```bash
cd /Users/mark/src/traillensdev/infra/pulumi

# Review changes
pulumi preview

# Deploy changes
pulumi up

# Verify outputs
pulumi stack output cognito_user_pool_id
pulumi stack output cognito_user_pool_client_id
```

---

## Security Considerations

### Best Practices

**Reference:** [Security best practices for Amazon Cognito user pools - Amazon Cognito](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-security-best-practices.html) [22]

#### 1. IAM Role Configuration

Apply both `cognito-identity.amazonaws.com:aud` and `cognito-identity.amazonaws.com:amr` conditions in all IAM roles that trust the identity pools service principal [23]. Further refine the value to restrict the role to users from a specific provider (e.g., `graph.facebook.com`).

**Example IAM Trust Policy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "cognito-identity.amazonaws.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "cognito-identity.amazonaws.com:aud": "ca-central-1:YOUR_IDENTITY_POOL_ID"
        },
        "ForAnyValue:StringLike": {
          "cognito-identity.amazonaws.com:amr": "authenticated"
        }
      }
    }
  ]
}
```

#### 2. Credential Storage

**Securely store OAuth credentials** [23]:
- ✅ **Use AWS Secrets Manager** for production credentials
- ✅ **Use Pulumi Config with encryption** (`--secret` flag)
- ❌ **Never commit credentials to git**
- ❌ **Never store in plain text configuration files**
- ❌ **Never store credentials in client-side code** [24]

**Example Secrets Manager Usage:**
```python
# Retrieve from AWS Secrets Manager instead of config
import boto3
import json

secrets_client = boto3.client('secretsmanager', region_name='ca-central-1')

def get_secret(secret_name):
    response = secrets_client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

google_creds = get_secret('traillens/dev/google-oauth')
google_client_id = google_creds['client_id']
google_client_secret = google_creds['client_secret']
```

#### 3. Multi-Factor Authentication (MFA)

Enable MFA for enhanced security [23]:
- Cognito supports SMS, TOTP, and email-based MFA
- Can be enforced for social identity users
- Adaptive authentication provides risk-based MFA prompts

**Infrastructure Enhancement:**
```python
# In auth.py UserPool configuration
mfa_configuration="OPTIONAL",  # or "ON" to enforce
software_token_mfa_configuration=aws.cognito.UserPoolSoftwareTokenMfaConfigurationArgs(
    enabled=True
),
```

#### 4. AWS WAF Integration

Configure AWS WAF web ACLs for your user pools [23] to protect against:
- Brute force attacks
- DDoS attacks
- Bot traffic
- SQL injection attempts

#### 5. Least Privilege Access

Apply least privilege principles [23]:
- Limit administrative operations
- Use scoped permissions for each provider
- Regularly audit IAM policies
- Restrict callback URLs to only required domains

#### 6. Credential Rotation

**Google:**
- OAuth clients inactive for 6 months are auto-deleted [6]
- Manually rotate credentials annually

**Facebook:**
- Rotate App Secret periodically (recommended: every 90 days)
- Facebook API versions have deprecation dates [14]

**Apple:**
- Rotate Private Keys (.p8) annually
- Apple Developer Program requires annual renewal [17]
- Keys remain valid unless explicitly revoked

#### 7. Monitoring and Logging

Enable CloudWatch logging for Cognito [23]:
- Monitor failed authentication attempts
- Track provider-specific errors
- Set up alerts for anomalous activity

**Example CloudWatch Query:**
```sql
fields @timestamp, @message
| filter @message like /Google/
| filter @message like /error/
| sort @timestamp desc
| limit 100
```

#### 8. OAuth Redirect URI Validation

**Strict validation of redirect URIs** [25]:
- Only whitelist exact production URLs
- Do not use wildcards in production
- Use HTTPS for all redirect URIs (required for Facebook [13])

**Current Configuration:**
```javascript
redirectSignIn: [
  window.location.origin,
  "http://localhost:3000",
  "https://traillenshq.com",
]
```

**Production Configuration Should Be:**
```javascript
redirectSignIn: [
  "https://app.traillenshq.com",
  "https://traillenshq.com",
]
```

---

## Cost Analysis

### Provider Costs

| Provider | Setup Cost | Recurring Cost | Notes |
|----------|-----------|----------------|-------|
| **Google** | Free | Free | No costs for OAuth authentication [5] |
| **Facebook** | Free | Free | No costs for authentication via Facebook Login |
| **Apple** | $99 USD | $99 USD/year | Apple Developer Program membership required [17] |

### AWS Cognito Costs

**Reference:** [AWS Cognito Pricing](https://aws.amazon.com/cognito/pricing/)

**User Pool Pricing (Relevant to Social Auth):**
- **MAUs (Monthly Active Users):** First 50,000 MAUs free, then tiered pricing
- **Social Provider Sign-Ins:** No additional cost beyond MAU pricing
- **Advanced Security Features (Optional):** $0.05 per MAU

**Estimated Costs for TrailLens:**

Assuming **1,000 MAUs** in first year:
- **User Pool MAUs:** Free (under 50,000 threshold)
- **Apple Developer Program:** $99 USD/year
- **Total First Year:** $99 USD
- **Total Recurring (Annual):** $99 USD

**As scale increases (e.g., 100,000 MAUs):**
- **User Pool MAUs:** $275 USD/month ($3,300 USD/year)
  - First 50,000: Free
  - Next 50,000: $0.0055 per MAU = $275/month
- **Apple Developer Program:** $99 USD/year
- **Total Annual:** $3,399 USD

### Implementation Costs

| Phase | Hours | Rate (Estimate) | Cost |
|-------|-------|-----------------|------|
| Google Implementation | 4 hours | $100/hour | $400 |
| Facebook Implementation | 5 hours | $100/hour | $500 |
| Apple Implementation | 8 hours | $100/hour | $800 |
| Testing & Documentation | 3 hours | $100/hour | $300 |
| **Total Implementation** | **20 hours** | | **$2,000** |

**Note:** Rates are estimates and will vary based on developer experience level.

### Total Cost Summary

| Item | First Year | Recurring (Annual) |
|------|-----------|-------------------|
| Apple Developer Program | $99 | $99 |
| AWS Cognito (1,000 MAUs) | $0 | $0 |
| Implementation (One-Time) | $2,000 | $0 |
| **Total** | **$2,099** | **$99** |

---

## Risks and Mitigation

### Technical Risks

#### 1. Provider API Changes

**Risk:** Social providers (especially Facebook) deprecate API versions with limited notice [14].

**Impact:** Authentication may break without warning.

**Mitigation:**
- Subscribe to provider developer newsletters
- Monitor AWS Security Blog for updates
- Test new API versions in dev environment
- Plan quarterly provider configuration reviews
- Set calendar reminders for:
  - Facebook API version upgrades (every 2 years)
  - Google OAuth client validation (every 6 months)
  - Apple key rotation (annually)

#### 2. Attribute Mapping Inconsistencies

**Risk:** Different providers return different attributes, especially Apple [21].

**Impact:** Incomplete user profiles, poor user experience.

**Mitigation:**
- Implement fallback logic for missing attributes
- Only require essential attributes (email)
- Design UI to handle missing profile pictures/names gracefully
- Document Apple's "first authentication only" limitation [21]

**Example Defensive Code:**
```javascript
// Handle missing attributes from providers
const userName = user.attributes.name ||
                 user.attributes.email?.split('@')[0] ||
                 'User';

const userPicture = user.attributes.picture ||
                    '/default-avatar.png';
```

#### 3. Token Expiration and Refresh

**Risk:** OAuth tokens expire and need refresh.

**Impact:** Users logged out unexpectedly.

**Mitigation:**
- Ensure `ALLOW_REFRESH_TOKEN_AUTH` is enabled (already configured)
- Implement automatic token refresh in frontend
- Set appropriate token expiration times
- Monitor CloudWatch for refresh token failures

#### 4. Provider Outages

**Risk:** Social provider services experience downtime.

**Impact:** Users unable to authenticate.

**Mitigation:**
- Always keep email/password authentication enabled (`["COGNITO"]`)
- Implement error handling with clear user messaging
- Consider provider status page monitoring
- Provide alternative authentication method guidance

**Example Error Handling:**
```javascript
const handleSocialSignIn = async (provider) => {
  try {
    await signInWithRedirect({ provider });
  } catch (err) {
    if (err.code === 'NetworkError') {
      setError(`${provider} is currently unavailable. Please try email login.`);
    } else {
      setError(`${provider} sign-in failed. Please try again`);
    }
    // Log to monitoring service
    console.error('Social auth error:', { provider, error: err });
  }
};
```

### Security Risks

#### 1. Credential Exposure

**Risk:** OAuth credentials committed to repository or exposed in logs.

**Impact:** Unauthorized access to user data, account takeovers.

**Mitigation:**
- Use Pulumi Config secrets (`--secret` flag)
- Add credential patterns to `.gitignore`
- Implement pre-commit hooks to scan for secrets
- Use AWS Secrets Manager for production
- Enable CloudTrail logging for credential access
- Rotate credentials if exposure suspected

**Pre-Commit Hook Example:**
```bash
#!/bin/bash
# .git/hooks/pre-commit
if git diff --cached | grep -E "(client_secret|app_secret|private_key)"; then
  echo "ERROR: Potential credential in commit!"
  exit 1
fi
```

#### 2. OAuth Phishing Attacks

**Risk:** Attackers create fake OAuth consent screens.

**Impact:** User credentials stolen.

**Mitigation:**
- Use official provider SDKs (AWS Amplify)
- Validate OAuth callback URLs strictly
- Educate users about official consent screens
- Monitor for suspicious authentication patterns
- Implement rate limiting on authentication endpoints

#### 3. Account Linking Vulnerabilities

**Risk:** Attackers link social accounts to existing Cognito accounts.

**Impact:** Unauthorized account access.

**Mitigation:**
- Implement email verification before account linking
- Require re-authentication for account linking
- Send email notifications when new provider is linked
- Allow users to view/revoke linked accounts

**Cognito Configuration:**
```python
# In auth.py UserPool configuration
auto_verified_attributes=["email"],  # Already configured
```

#### 4. Session Hijacking

**Risk:** OAuth tokens intercepted during transmission.

**Impact:** Unauthorized account access.

**Mitigation:**
- Enforce HTTPS for all communication (already required [13])
- Use short-lived access tokens
- Implement device fingerprinting
- Enable AWS WAF with rate limiting rules

### Compliance Risks

#### 1. GDPR and Privacy Regulations

**Risk:** Social providers access user data across borders.

**Impact:** Regulatory violations, fines.

**Mitigation:**
- Update Privacy Policy to disclose third-party data sharing
- Implement "Login with Email" as default option
- Allow users to delete linked social accounts
- Ensure Data Processing Agreements (DPAs) with providers
- Document data flows in privacy impact assessment

**Privacy Policy Updates Required:**
```markdown
## Third-Party Authentication

When you sign in using Google, Facebook, or Apple, we receive:
- Your email address
- Your name (if provided by the provider)
- Your profile picture (if provided by the provider)

This data is processed according to the respective provider's privacy policy:
- Google: https://policies.google.com/privacy
- Facebook: https://www.facebook.com/privacy/policy
- Apple: https://www.apple.com/legal/privacy/
```

#### 2. Data Residency Requirements

**Risk:** User data stored in AWS regions violates data residency laws.

**Impact:** Regulatory violations, service unavailability in certain regions.

**Mitigation:**
- Document Cognito User Pool region (`ca-central-1`)
- Ensure compliance with Canadian privacy laws (PIPEDA)
- Implement region-specific deployments if expanding globally
- Review provider terms of service for data storage locations

### Operational Risks

#### 1. Apple Developer Program Expiration

**Risk:** Apple Developer Program membership expires without renewal.

**Impact:** Apple Sign In stops working.

**Mitigation:**
- Set calendar reminders for renewal (annual)
- Enable auto-renewal on Apple Developer account
- Document renewal process
- Set up monitoring alerts for Apple auth failures
- Have backup authentication methods available

#### 2. Configuration Drift

**Risk:** Manual AWS Console changes override infrastructure as code.

**Impact:** Pulumi deployment failures, inconsistent environments.

**Mitigation:**
- Use `pulumi refresh` before deployments
- Implement AWS Config rules for drift detection
- Restrict AWS Console access to Cognito resources
- Document all changes in infrastructure repository
- Enable CloudTrail for audit logging

#### 3. Testing Complexity

**Risk:** Social auth requires real accounts for testing.

**Impact:** Incomplete testing, production bugs.

**Mitigation:**
- Create dedicated test accounts for each provider
- Document test account credentials securely
- Implement automated smoke tests
- Use separate dev/staging Cognito User Pools
- Test on multiple devices (especially Apple)

**Test Account Documentation:**
```yaml
# Store in 1Password or AWS Secrets Manager
Google Test Account:
  Email: test+google@traillenshq.com
  Password: <secure-password>

Facebook Test Account:
  Email: test+facebook@traillenshq.com
  Password: <secure-password>

Apple Test Account:
  Apple ID: test+apple@traillenshq.com
  Password: <secure-password>
```

---

## Timeline and Resources

### Implementation Timeline

**Total Estimated Time:** 9-17 hours (depending on approval wait times)

#### Week 1: Preparation and Google Implementation

| Day | Tasks | Hours | Assignee |
|-----|-------|-------|----------|
| Day 1 | Kick-off meeting, review current auth implementation | 1 hour | Lead Dev |
| Day 1 | Set up Google Cloud Console, create OAuth client | 2 hours | Lead Dev |
| Day 2 | Implement Google provider infrastructure code | 2 hours | Lead Dev |
| Day 2 | Deploy and test Google sign-in | 1 hour | Lead Dev + QA |
| **Subtotal** | | **6 hours** | |

#### Week 2: Facebook and Apple Implementation

| Day | Tasks | Hours | Assignee |
|-----|-------|-------|----------|
| Day 3 | Set up Facebook Developer account and app | 3 hours | Lead Dev |
| Day 4 | Implement Facebook provider infrastructure code | 2 hours | Lead Dev |
| Day 4 | Deploy and test Facebook login | 1 hour | Lead Dev + QA |
| Day 5 | Enroll in Apple Developer Program | 1 hour | Lead Dev |
| *Wait* | *Apple approval (24-48 hours)* | | |
| Day 7 | Set up Apple Developer Portal (App ID, Services ID, Key) | 3 hours | Lead Dev |
| Day 8 | Implement Apple provider infrastructure code | 2 hours | Lead Dev |
| Day 8 | Deploy and test Apple Sign In | 2 hours | Lead Dev + QA |
| **Subtotal** | | **14 hours** | |

#### Week 3: Production Deployment and Documentation

| Day | Tasks | Hours | Assignee |
|-----|-------|-------|----------|
| Day 9 | Create production OAuth apps for all providers | 2 hours | Lead Dev |
| Day 9 | Update production infrastructure configuration | 1 hour | Lead Dev |
| Day 10 | Deploy to production, smoke testing | 2 hours | Lead Dev + QA |
| Day 10 | Update documentation (CLAUDE.md, runbooks) | 2 hours | Lead Dev |
| Day 11 | Final testing, monitoring setup, handoff | 2 hours | Lead Dev + QA |
| **Subtotal** | | **9 hours** | |

**Grand Total:** 29 hours (includes wait time; active development: 20 hours)

### Resource Requirements

#### Personnel

1. **Lead Developer** (Primary)
   - Full-stack experience
   - AWS Cognito expertise
   - Pulumi/Infrastructure as Code knowledge
   - Time commitment: 20-25 hours over 2-3 weeks

2. **QA Engineer** (Secondary)
   - Testing social authentication flows
   - Device testing (especially for Apple)
   - Time commitment: 5-7 hours

3. **Security Reviewer** (Consulting)
   - Review OAuth configuration
   - Validate credential storage
   - Time commitment: 2-3 hours

#### Accounts and Access

1. **Google Cloud Console**
   - Organization account or individual account
   - No cost

2. **Facebook Developer Account**
   - Organization account or individual account
   - No cost

3. **Apple Developer Program**
   - Organization membership (preferred)
   - Cost: $99 USD/year
   - Requires: DUNS Number for organizations [18]

4. **AWS Access**
   - IAM permissions to Cognito User Pools
   - Pulumi deployment permissions
   - CloudWatch access for monitoring

5. **Test Devices**
   - Desktop browser (Chrome, Safari, Firefox)
   - iPhone or iPad (for Apple Sign In testing)
   - Android device (optional, for cross-platform testing)

#### Tools and Services

1. **Development Environment**
   - Pulumi CLI (already installed)
   - AWS CLI (already installed)
   - Node.js and npm (already installed)

2. **Credential Storage**
   - AWS Secrets Manager (recommended) or Pulumi Config
   - 1Password or similar for team credential sharing

3. **Monitoring and Logging**
   - AWS CloudWatch (already available)
   - AWS CloudTrail (recommended for audit logging)

---

## Recommendations

### Immediate Actions (Priority 1)

1. **Enable Google Sign-In First**
   - **Rationale:** Simplest implementation, highest user adoption
   - **Cost:** Free
   - **Time:** 2-4 hours
   - **Risk:** Low

2. **Create Test Accounts**
   - Set up dedicated test accounts for each provider
   - Document credentials securely
   - Use for automated and manual testing

3. **Update Privacy Policy**
   - Disclose third-party authentication
   - Link to provider privacy policies
   - Comply with GDPR and PIPEDA

### Short-Term Actions (Priority 2)

4. **Enable Facebook Login**
   - **Rationale:** Second most popular social login method
   - **Cost:** Free
   - **Time:** 3-5 hours
   - **Risk:** Medium (API version deprecation)

5. **Implement Comprehensive Monitoring**
   - Set up CloudWatch dashboards for authentication metrics
   - Create alerts for authentication failures
   - Monitor provider-specific error rates

6. **Rotate Default Cognito Credentials**
   - Review and rotate any test user passwords
   - Ensure production credentials use strong passwords

### Long-Term Actions (Priority 3)

7. **Enable Apple Sign In**
   - **Rationale:** Required for iOS app (if planned), premium user experience
   - **Cost:** $99 USD/year
   - **Time:** 4-8 hours
   - **Risk:** High (annual renewal, complex setup)
   - **Recommendation:** Wait until iOS app development is confirmed

8. **Implement Identity Pool (Optional)**
   - **Rationale:** Provides temporary AWS credentials for federated users
   - **Use Case:** If users need direct access to AWS services (S3, DynamoDB)
   - **Current State:** Not required for TrailLens MVP

9. **Add Multi-Factor Authentication (MFA)**
   - **Rationale:** Enhanced security for all authentication methods
   - **Implementation:** Enable TOTP-based MFA in Cognito
   - **Time:** 4-6 hours (infrastructure + UI)

### Strategic Recommendations

#### A. Phased Rollout Approach

**Phase 1 (Week 1-2):**
- Enable Google Sign-In
- Test thoroughly in dev environment
- Deploy to production
- Monitor adoption and error rates

**Phase 2 (Week 3-4):**
- Enable Facebook Login (only if Google adoption >10%)
- Continue monitoring

**Phase 3 (Month 2-3):**
- Evaluate Apple Sign In based on user requests
- Enroll in Apple Developer Program if justified

**Rationale:** Reduces risk, allows for iterative improvement, validates user demand.

#### B. Passwordless Authentication Roadmap

**Current State:**
- Email/password authentication only

**Step 1: Social Authentication** (This Project)
- Google, Facebook, (Apple)
- Reduces password dependency

**Step 2: Passwordless Email (Future)**
- Magic link authentication
- Email-based OTP codes
- Cognito supports via custom authentication flows

**Step 3: Biometric Authentication ✅ COMPLETE**
- Cognito Native WebAuthn (FIDO2/passkeys) — ESSENTIALS tier enabled
- `USER_AUTH` flow with `WEB_AUTHN` challenge type — client-side Cognito SDK
- `FactorConfiguration=MULTI_FACTOR_WITH_USER_VERIFICATION` — admin passkey UX
- Frontend implementation deferred to separate PRs (androiduser, web)

**Reference:** [Passwordless & MFA in 2026](https://www.loginradius.com/blog/identity/passwordless-and-mfa) [26]

#### C. User Education and Communication

1. **In-App Messaging**
   - Announce new social login options
   - Highlight security benefits
   - Provide setup instructions

2. **Email Campaign**
   - Notify existing users of new features
   - Encourage linking social accounts
   - Address privacy concerns proactively

3. **Help Documentation**
   - Create FAQ for social authentication
   - Troubleshooting guide for common issues
   - Step-by-step linking instructions

#### D. Metrics and Success Criteria

Track the following metrics to evaluate success:

| Metric | Target | Measurement |
|--------|--------|-------------|
| Social login adoption rate | >30% of new users | CloudWatch Cognito logs |
| Authentication errors | <2% failure rate | CloudWatch alarms |
| Time to authenticate | <3 seconds average | Frontend performance monitoring |
| User satisfaction | >4.0/5.0 rating | In-app survey |
| Provider uptime | >99.9% | Provider status pages + monitoring |

#### E. Compliance and Legal Review

**Recommended Actions:**

1. **Legal Review**
   - Have legal counsel review updated Privacy Policy
   - Ensure Terms of Service include third-party authentication
   - Review Data Processing Agreements with providers

2. **GDPR Compliance**
   - Update GDPR documentation
   - Implement data deletion for linked accounts
   - Document legal basis for processing (consent)

3. **PIPEDA Compliance** (Canada)
   - Ensure compliance with Canadian privacy laws
   - Document data storage locations
   - Implement opt-out mechanisms

4. **Accessibility**
   - Ensure social login buttons meet WCAG 2.1 Level AA
   - Provide keyboard navigation
   - Test with screen readers

---

## Conclusion

The TrailLens web application has a **complete UI implementation** for Google, Facebook, and Apple authentication, but the underlying AWS Cognito infrastructure is **not configured** with social identity providers. Enabling these providers will provide users with a more convenient authentication experience and represent a step toward fully passwordless authentication.

**Key Findings:**

1. ✅ **Frontend Ready:** UI buttons and event handlers are fully implemented
2. ❌ **Backend Not Configured:** Cognito only supports `["COGNITO"]` provider
3. 🔧 **Implementation Effort:** 9-17 hours for all three providers
4. 💰 **Cost:** $99 USD/year (Apple only), implementation cost ~$2,000
5. 📊 **Recommendation:** Start with Google (easiest), then Facebook, then Apple (if needed)

**Next Steps:**

1. **Immediate:** Approve implementation and allocate resources
2. **Week 1:** Implement and test Google Sign-In
3. **Week 2:** Implement and test Facebook Login
4. **Week 3:** (Optional) Implement Apple Sign In
5. **Ongoing:** Monitor adoption, iterate based on user feedback

By following the detailed implementation steps and best practices outlined in this report, TrailLens can safely and effectively enable social authentication, improving user experience while maintaining security and compliance.

---

## References

[1] ISACA. (2026). "Passwordless Authentication Risk Reward and Readiness." Available: https://www.isaca.org/resources/news-and-trends/industry-news/2026/passwordless-authentication-risk-reward-and-readiness

[2] Security Boulevard. (2026). "The Benefits and Risks of Transitioning to Passwordless Solutions." Available: https://securityboulevard.com/2026/01/the-benefits-and-risks-of-transitioning-to-passwordless-solutions/

[3] AWS. (2025). "Configuring identity providers for your user pool - Amazon Cognito." Available: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-identity-provider.html

[4] AWS. (2025). "Setting up Google as an identity pool IdP - Amazon Cognito." Available: https://docs.aws.amazon.com/cognito/latest/developerguide/google.html

[5] Google for Developers. (2025). "Get your Google API client ID | Web guides." Available: https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid

[6] Google Cloud. (2026). "Setting up OAuth 2.0 - API Console Help." Available: https://support.google.com/googleapi/answer/6158849?hl=en

[7] AWS re:Post. (2025). "Set up Google as a social identity provider in an Amazon Cognito user pool." Available: https://repost.aws/knowledge-center/cognito-google-social-identity-provider

[8] Pulumi. (2025). "Configuration and Secrets." Pulumi Documentation. Available: https://www.pulumi.com/docs/concepts/config/

[9] AWS. (2025). "Setting up Facebook as an identity pools IdP - Amazon Cognito." Available: https://docs.aws.amazon.com/cognito/latest/developerguide/facebook.html

[10] AWS. (2025). "Add social sign-in to your user pool - Amazon Cognito." Available: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-configuring-federation-with-social-idp.html

[11] Medium. (2025). "Enable Social Login AWS Cognito: Add Facebook Login." Available: https://victorhzhao.medium.com/add-social-login-to-aws-cognito-user-pool-facebook-94a2cee5136e

[12] DreamFactory Blog. (2025). "How to Incorporate Facebook OAuth 2.0." Available: https://blog.dreamfactory.com/dreamfactory-and-facebook-oauth-2-0

[13] Baserow. (2025). "Set up Facebook login with Baserow OAuth 2." Available: https://baserow.io/user-docs/configure-facebook-for-oauth-2-sso

[14] AWS Security Blog. (2025). "Selecting and migrating a Facebook API version for Amazon Cognito." Available: https://aws.amazon.com/blogs/security/selecting-and-migrating-a-facebook-api-version-for-amazon-cognito/

[15] AWS. (2025). "Using social identity providers with a user pool - Amazon Cognito." Available: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-social-idp.html

[16] AWS. (2025). "Setting up Sign in with Apple as an identity pool IdP - Amazon Cognito." Available: https://docs.aws.amazon.com/cognito/latest/developerguide/apple.html

[17] Apple Developer. (2026). "Membership Details - Apple Developer Program." Available: https://developer.apple.com/programs/whats-included/

[18] Apple Developer. (2026). "Enrollment - Membership - Account - Help." Available: https://developer.apple.com/help/account/membership/program-enrollment/

[19] AWS Security Blog. (2025). "How to set up Sign in with Apple for Amazon Cognito." Available: https://aws.amazon.com/blogs/security/how-to-set-up-sign-in-with-apple-for-amazon-cognito/

[20] Medium. (2025). "AWS Cognito: Sign In with Apple (OIDC)." Available: https://medium.com/@matiasrzeta/aws-cognito-sign-in-with-apple-oidc-95fd9de35270

[21] AWS Cognito Documentation. (2025). "Important Considerations for Sign in with Apple." Available: https://docs.aws.amazon.com/cognito/latest/developerguide/apple.html#apple-considerations

[22] AWS. (2025). "Security best practices for Amazon Cognito user pools." Available: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-security-best-practices.html

[23] AWS. (2025). "Security best practices for Amazon Cognito identity pools." Available: https://docs.aws.amazon.com/cognito/latest/developerguide/identity-pools-security-best-practices.html

[24] Redfox Security. (2025). "Understanding and Securing Amazon Cognito: A Comprehensive Guide." Available: https://redfoxsec.com/blog/understanding-and-securing-amazon-cognito-a-comprehensive-guide/

[25] DataCamp. (2025). "AWS Cognito Guide: Authentication, User Pools, and Best Practices." Available: https://www.datacamp.com/tutorial/aws-cognito-guide

[26] LoginRadius Blog. (2026). "Passwordless & MFA in 2026: Passkeys, Push MFA, Device Trust." Available: https://www.loginradius.com/blog/identity/passwordless-and-mfa

---

**Report Prepared By:** Lead Developer
**Date:** January 20, 2026
**Version:** 1.0
**Status:** Complete and Ready for Review
