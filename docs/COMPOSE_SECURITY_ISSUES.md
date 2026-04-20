# Copyright (c) 2026 TrailLensCo
# All rights reserved.

# Jetpack Compose Security Vulnerability Patterns Reference

This document catalogs 59 Jetpack Compose security vulnerability patterns relevant to Android applications
built with Jetpack Compose (androiduser, androidadmin). Each pattern includes detection strategies,
vulnerable and secure code examples, and references to CWE and OWASP classifications.

**Applicable to:** `androiduser/` and `androidadmin/` submodules (Kotlin 2.0.0, Jetpack Compose, Hilt DI,
Navigation Compose, Retrofit + OkHttp)

---

## Summary Table

| ID | Severity | Category | Description |
| -- | -------- | -------- | ----------- |
| COMPOSE-001 | CRITICAL | Navigation & Deep Link Security | Implicit Deep Link Exploitation |
| COMPOSE-002 | CRITICAL | Navigation & Deep Link Security | Navigation Argument Injection |
| COMPOSE-003 | HIGH | Navigation & Deep Link Security | Authentication Screen Bypass via Deep Link |
| COMPOSE-004 | HIGH | Navigation & Deep Link Security | Back Stack Manipulation Attack |
| COMPOSE-005 | MEDIUM | Navigation & Deep Link Security | SavedStateHandle Argument Tampering |
| COMPOSE-006 | HIGH | Navigation & Deep Link Security | Navigation Route Type Confusion |
| COMPOSE-007 | HIGH | Navigation & Deep Link Security | BackHandler Bypass on Protected Screens |
| COMPOSE-008 | HIGH | State Management Security | MutableState Exposure from ViewModel |
| COMPOSE-009 | HIGH | State Management Security | MutableStateFlow External Mutation |
| COMPOSE-010 | MEDIUM | State Management Security | SnapshotStateList Thread Safety Violation |
| COMPOSE-011 | MEDIUM | State Management Security | State Hoisting Sensitive Data Leak |
| COMPOSE-012 | MEDIUM | State Management Security | Stale State via remember Without Keys |
| COMPOSE-013 | LOW | State Management Security | Derived State Caching Sensitive Values |
| COMPOSE-014 | HIGH | Side-Effect Security | LaunchedEffect Key Manipulation |
| COMPOSE-015 | HIGH | Side-Effect Security | DisposableEffect Missing Cleanup |
| COMPOSE-016 | MEDIUM | Side-Effect Security | rememberUpdatedState Staleness |
| COMPOSE-017 | MEDIUM | Side-Effect Security | SideEffect Timing Leak |
| COMPOSE-018 | HIGH | Side-Effect Security | produceState Uncancelled Coroutine Leak |
| COMPOSE-019 | CRITICAL | UI Security & Screen Protection | Missing FLAG_SECURE on Sensitive Screens |
| COMPOSE-020 | CRITICAL | UI Security & Screen Protection | Tapjacking via Overlay Attack |
| COMPOSE-021 | HIGH | UI Security & Screen Protection | Partial Occlusion UI Deception |
| COMPOSE-022 | HIGH | UI Security & Screen Protection | Task Hijacking (StrandHogg) |
| COMPOSE-023 | MEDIUM | UI Security & Screen Protection | Recent Apps Screenshot Exposure |
| COMPOSE-024 | HIGH | Text Input & Credential Security | Password Field Missing Visual Transformation |
| COMPOSE-025 | HIGH | Text Input & Credential Security | Clipboard Data Leakage from TextField |
| COMPOSE-026 | MEDIUM | Text Input & Credential Security | IME Keyboard Data Interception |
| COMPOSE-027 | MEDIUM | Text Input & Credential Security | AutoCorrect on Sensitive Fields |
| COMPOSE-028 | MEDIUM | Text Input & Credential Security | Autofill Sensitive Data Exposure |
| COMPOSE-029 | HIGH | Accessibility & Semantics Security | Accessibility Service Data Exfiltration |
| COMPOSE-030 | MEDIUM | Accessibility & Semantics Security | contentDescription Sensitive Data Exposure |
| COMPOSE-031 | MEDIUM | Accessibility & Semantics Security | testTag Information Leakage in Production |
| COMPOSE-032 | LOW | Accessibility & Semantics Security | Semantics Tree Sensitive Metadata |
| COMPOSE-033 | CRITICAL | Serialization & Deserialization Security | rememberSaveable Unsafe Custom Saver |
| COMPOSE-034 | HIGH | Serialization & Deserialization Security | Parcelable Navigation Argument Deserialization |
| COMPOSE-035 | HIGH | Serialization & Deserialization Security | Bundle Injection via Intent Extras |
| COMPOSE-036 | MEDIUM | Serialization & Deserialization Security | State Restoration Tampering After Process Death |
| COMPOSE-037 | HIGH | Image & Media Security | Image Loader URL Injection |
| COMPOSE-038 | MEDIUM | Image & Media Security | SVG/Vector Parsing Denial of Service |
| COMPOSE-039 | MEDIUM | Image & Media Security | Bitmap Memory Exhaustion |
| COMPOSE-040 | CRITICAL | WebView & Interop Security | WebView JavaScript Interface Exploitation |
| COMPOSE-041 | HIGH | WebView & Interop Security | WebView Unsafe File Access |
| COMPOSE-042 | HIGH | WebView & Interop Security | AndroidView Interop Lifecycle Mismatch |
| COMPOSE-043 | HIGH | WebView & Interop Security | Cross-App Scripting via WebView |
| COMPOSE-044 | HIGH | Component & Intent Security | Exported Activity Without Validation |
| COMPOSE-045 | HIGH | Component & Intent Security | Intent Redirection Vulnerability |
| COMPOSE-046 | HIGH | Component & Intent Security | Content Provider URI Permission Leak |
| COMPOSE-047 | MEDIUM | Component & Intent Security | Implicit Intent Interception |
| COMPOSE-048 | HIGH | Build & Obfuscation Security | @Preview Data in Production APK |
| COMPOSE-049 | MEDIUM | Build & Obfuscation Security | Debug Logging in Production Build |
| COMPOSE-050 | MEDIUM | Build & Obfuscation Security | Missing R8/ProGuard Compose Rules |
| COMPOSE-051 | MEDIUM | Performance & DoS Security | Infinite Recomposition Loop |
| COMPOSE-052 | MEDIUM | Performance & DoS Security | Unbounded LazyColumn Memory Exhaustion |
| COMPOSE-053 | LOW | Performance & DoS Security | Animation Resource Exhaustion |
| COMPOSE-054 | CRITICAL | Network & Communication Security | Missing Certificate Pinning |
| COMPOSE-055 | HIGH | Network & Communication Security | Cleartext Traffic Permitted |
| COMPOSE-056 | HIGH | Network & Communication Security | Plaintext Credential Storage |
| COMPOSE-057 | CRITICAL | Authentication & Biometric Security | Biometric Authentication Without CryptoObject |
| COMPOSE-058 | HIGH | Authentication & Biometric Security | Missing Root/Tamper Detection |
| COMPOSE-059 | HIGH | Authentication & Biometric Security | Insecure Local Authentication Gate |

---

## Category 1: Navigation & Deep Link Security

### COMPOSE-001: Implicit Deep Link Exploitation

- **Severity:** CRITICAL
- **Category:** Navigation & Deep Link Security
- **Description:** Jetpack Navigation Compose automatically creates implicit deep links for every destination in the format `android-app://androidx.navigation/$route`. These internal links are accessible from external applications. An attacker who knows the app's route structure can invoke any destination directly, bypassing authentication screens and intended navigation flow. This vulnerability was documented by PT Security research and affects all apps using NavHost with string-based routes.
- **Detection Strategy:** Search for `NavHost` or `composable(` route definitions paired with exported activities in `AndroidManifest.xml`. Any exported activity hosting a `NavHost` exposes all its routes via implicit deep links.
- **Detection Regex:** `composable\(\s*route\s*=\s*"[^"]+"`  combined with  `android:exported="true"` in manifest
- **Impact:** Complete bypass of authentication gates, access to protected screens, exposure of sensitive data without user interaction.
- **CWE:** CWE-284 (Improper Access Control)
- **OWASP Mobile:** M1:2024 - Improper Credential Usage, M3:2024 - Insecure Authentication/Authorization

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Exported activity hosts NavHost - all routes accessible externally
// AndroidManifest.xml: <activity android:exported="true" ...>

@Composable
fun AppNavigation() {
    val navController = rememberNavController()
    NavHost(navController = navController, startDestination = "login") {
        composable("login") { LoginScreen(navController) }
        composable("dashboard") { DashboardScreen(navController) }
        composable("admin/settings") { AdminSettingsScreen(navController) }
        // All routes get implicit deep links:
        // android-app://androidx.navigation/login
        // android-app://androidx.navigation/dashboard
        // android-app://androidx.navigation/admin/settings
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: Validate authorization on every destination, not just the start screen
@Composable
fun AppNavigation(authViewModel: AuthViewModel = hiltViewModel()) {
    val navController = rememberNavController()
    val isAuthenticated by authViewModel.isAuthenticated.collectAsStateWithLifecycle()

    NavHost(navController = navController, startDestination = "login") {
        composable("login") { LoginScreen(navController) }
        composable("dashboard") {
            // Each screen validates auth independently
            RequireAuth(isAuthenticated, navController) {
                DashboardScreen(navController)
            }
        }
        composable("admin/settings") {
            RequireAuth(isAuthenticated, navController) {
                RequireRole("admin", authViewModel) {
                    AdminSettingsScreen(navController)
                }
            }
        }
    }
}

@Composable
fun RequireAuth(
    isAuthenticated: Boolean,
    navController: NavController,
    content: @Composable () -> Unit
) {
    if (isAuthenticated) {
        content()
    } else {
        LaunchedEffect(Unit) {
            navController.navigate("login") {
                popUpTo(0) { inclusive = true }
            }
        }
    }
}
```

---

### COMPOSE-002: Navigation Argument Injection

- **Severity:** CRITICAL
- **Category:** Navigation & Deep Link Security
- **Description:** Navigation routes that accept arguments (e.g., `composable("user/{userId}")`) allow external applications to inject arbitrary argument values via deep links or crafted intents. The `matchDeepLink` function adds deep link arguments to a `globalArgs` object without validation. Attackers can pass malicious user IDs, URLs, or other parameters that composables process without sanitization.
- **Detection Strategy:** Search for route definitions with path parameters (`{param}`) or query parameters and verify that all parameter values are validated before use.
- **Detection Regex:** `composable\(\s*"[^"]*\{[^}]+\}[^"]*"`
- **Impact:** Access to other users' data (IDOR), injection of malicious URLs into WebViews, bypassing business logic validation.
- **CWE:** CWE-20 (Improper Input Validation)
- **OWASP Mobile:** M4:2024 - Insufficient Input/Output Validation

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Navigation argument used directly without validation
composable("user/{userId}") { backStackEntry ->
    val userId = backStackEntry.arguments?.getString("userId") ?: ""
    // Attacker sends: android-app://androidx.navigation/user/admin_user_id
    UserProfileScreen(userId = userId)
}

composable("webview/{url}") { backStackEntry ->
    val url = backStackEntry.arguments?.getString("url") ?: ""
    // Attacker sends: android-app://androidx.navigation/webview/https://evil.com
    WebViewScreen(url = url)
}
```

**Secure Pattern:**

```kotlin
// SECURE: Validate all navigation arguments before use
composable("user/{userId}") { backStackEntry ->
    val userId = backStackEntry.arguments?.getString("userId") ?: ""
    val currentUserId = authViewModel.currentUserId

    // Validate: user can only access their own profile or allowed profiles
    if (userId == currentUserId || authViewModel.canViewProfile(userId)) {
        UserProfileScreen(userId = userId)
    } else {
        UnauthorizedScreen()
    }
}

composable("webview/{url}") { backStackEntry ->
    val rawUrl = backStackEntry.arguments?.getString("url") ?: ""
    val allowedDomains = listOf("traillens.com", "api.traillens.com")

    // Validate URL against allowlist
    val uri = Uri.parse(rawUrl)
    if (uri.host in allowedDomains && uri.scheme == "https") {
        WebViewScreen(url = rawUrl)
    } else {
        ErrorScreen(message = "Invalid URL")
    }
}
```

---

### COMPOSE-003: Authentication Screen Bypass via Deep Link

- **Severity:** HIGH
- **Category:** Navigation & Deep Link Security
- **Description:** Many Compose apps perform authorization checks only on the start/home screen, relying on the assumption that users must navigate through it first. Implicit deep links bypass the start destination entirely, allowing direct access to any registered composable destination. If authorization logic is centralized only in the home screen composable, all other screens become accessible without authentication.
- **Detection Strategy:** Search for authentication checks and verify they exist on every protected composable, not just the start destination. If auth checks appear only in one composable or only in a `NavHost` wrapper, the pattern is vulnerable.
- **Detection Regex:** `startDestination\s*=\s*"(login|auth|pin|splash)"` without per-destination auth checks
- **Impact:** Unauthorized access to all application screens and their data.
- **CWE:** CWE-306 (Missing Authentication for Critical Function)
- **OWASP Mobile:** M3:2024 - Insecure Authentication/Authorization

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Auth check only on the start screen
@Composable
fun AppNavigation() {
    val navController = rememberNavController()
    NavHost(navController = navController, startDestination = "pin_entry") {
        composable("pin_entry") {
            // Only this screen checks authentication
            PinEntryScreen(onSuccess = { navController.navigate("main") })
        }
        composable("main") { MainScreen(navController) }
        composable("settings") { SettingsScreen(navController) }
        composable("payment/{amount}") { PaymentScreen(navController) }
        // Attacker skips pin_entry entirely via implicit deep link
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: Centralized auth middleware applied to all protected routes
@Composable
fun AppNavigation(authViewModel: AuthViewModel = hiltViewModel()) {
    val navController = rememberNavController()
    val authState by authViewModel.authState.collectAsStateWithLifecycle()

    NavHost(navController = navController, startDestination = "pin_entry") {
        composable("pin_entry") {
            PinEntryScreen(onSuccess = { navController.navigate("main") })
        }
        protectedComposable("main", authState, navController) {
            MainScreen(navController)
        }
        protectedComposable("settings", authState, navController) {
            SettingsScreen(navController)
        }
        protectedComposable("payment/{amount}", authState, navController) {
            PaymentScreen(navController)
        }
    }
}

fun NavGraphBuilder.protectedComposable(
    route: String,
    authState: AuthState,
    navController: NavController,
    content: @Composable () -> Unit
) {
    composable(route) {
        when (authState) {
            AuthState.Authenticated -> content()
            else -> LaunchedEffect(Unit) {
                navController.navigate("pin_entry") {
                    popUpTo(0) { inclusive = true }
                }
            }
        }
    }
}
```

---

### COMPOSE-004: Back Stack Manipulation Attack

- **Severity:** HIGH
- **Category:** Navigation & Deep Link Security
- **Description:** External applications can construct complex navigation stacks by sending crafted intents with multiple destination IDs. Using `Intent.FLAG_ACTIVITY_NEW_TASK`, attackers create arbitrary fragment/destination hierarchies that violate intended application flow. The navigation library processes each ID sequentially, executing destination initialization logic regardless of business rules.
- **Detection Strategy:** Check for exported activities with `launchMode` settings that allow task manipulation. Verify that `android:taskAffinity` is explicitly set to empty string to prevent task hijacking.
- **Detection Regex:** `android:exported="true"` without `android:taskAffinity=""`
- **Impact:** Application state manipulation, unauthorized navigation sequences, business logic bypass.
- **CWE:** CWE-441 (Unintended Proxy or Intermediary)
- **OWASP Mobile:** M8:2024 - Security Misconfiguration

**Vulnerable Pattern:**

```xml
<!-- VULNERABLE: Exported activity with default task affinity -->
<activity
    android:name=".MainActivity"
    android:exported="true">
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
    </intent-filter>
</activity>
```

**Secure Pattern:**

```xml
<!-- SECURE: Empty task affinity prevents StrandHogg-style attacks -->
<activity
    android:name=".MainActivity"
    android:exported="true"
    android:taskAffinity="">
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
    </intent-filter>
</activity>
<!-- All secondary activities should also have empty taskAffinity -->
```

---

### COMPOSE-005: SavedStateHandle Argument Tampering

- **Severity:** MEDIUM
- **Category:** Navigation & Deep Link Security
- **Description:** ViewModels using `SavedStateHandle` to retrieve navigation arguments may process externally-injected values without validation. Before Navigation 2.8.0's type-safe APIs, arguments were retrieved as raw strings or primitives with no type enforcement. Even with type-safe navigation, the underlying Bundle mechanism can be manipulated through crafted intents.
- **Detection Strategy:** Search for `savedStateHandle.get<>()` or `savedStateHandle["key"]` calls and verify type validation and range checking on retrieved values.
- **Detection Regex:** `savedStateHandle\.(get|getStateFlow)\s*[<\[]`
- **Impact:** Business logic bypass through unexpected argument values, potential injection if values are used in queries or URLs.
- **CWE:** CWE-20 (Improper Input Validation)
- **OWASP Mobile:** M4:2024 - Insufficient Input/Output Validation

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Using SavedStateHandle values without validation
@HiltViewModel
class UserViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val userRepository: UserRepository
) : ViewModel() {

    // Directly using potentially tampered argument
    private val userId: String = savedStateHandle["userId"] ?: ""

    init {
        viewModelScope.launch {
            // No validation - attacker controls userId via deep link
            val user = userRepository.getUser(userId)
            _uiState.value = UiState.Success(user)
        }
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: Validate and sanitize SavedStateHandle values
@HiltViewModel
class UserViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val userRepository: UserRepository,
    private val authRepository: AuthRepository
) : ViewModel() {

    private val userId: String = savedStateHandle.get<String>("userId")
        ?.takeIf { it.matches(Regex("^[a-zA-Z0-9-]{36}$")) }
        ?: throw IllegalArgumentException("Invalid userId format")

    init {
        viewModelScope.launch {
            val currentUser = authRepository.getCurrentUser()
            // Verify the requesting user has access to this profile
            if (currentUser.id == userId || currentUser.hasRole("admin")) {
                val user = userRepository.getUser(userId)
                _uiState.value = UiState.Success(user)
            } else {
                _uiState.value = UiState.Error("Unauthorized")
            }
        }
    }
}
```

---

### COMPOSE-006: Navigation Route Type Confusion

- **Severity:** HIGH
- **Category:** Navigation & Deep Link Security
- **Description:** Before Navigation 2.8.0 introduced type-safe routes with Kotlin serialization, navigation arguments were passed as strings in the route URL. This allowed type confusion where a numeric ID could be replaced with a string, or path segments could be injected. Even with type-safe APIs, custom `NavType` implementations may perform unsafe deserialization of complex objects passed through navigation.
- **Detection Strategy:** Search for string-based route construction with concatenation or interpolation and custom `NavType` implementations.
- **Detection Regex:** `navController\.navigate\(\s*"[^"]*\$\{` or `object\s*:\s*NavType<`
- **Impact:** Type confusion leading to crashes, data corruption, or injection attacks through malformed route parameters.
- **CWE:** CWE-843 (Access of Resource Using Incompatible Type)
- **OWASP Mobile:** M4:2024 - Insufficient Input/Output Validation

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: String-based route construction with user input
fun navigateToUser(navController: NavController, userId: String) {
    // userId could contain "../admin" or other path traversal
    navController.navigate("user/$userId")
}

// VULNERABLE: Custom NavType with unsafe deserialization
val UserNavType = object : NavType<User>(isNullableAllowed = false) {
    override fun get(bundle: Bundle, key: String): User? {
        @Suppress("DEPRECATION")
        return bundle.getParcelable(key)  // Deprecated, not type-safe
    }
    override fun parseValue(value: String): User {
        return Json.decodeFromString(value)  // Unsafe deserialization
    }
    // ...
}
```

**Secure Pattern:**

```kotlin
// SECURE: Type-safe navigation with Kotlin serialization (Navigation 2.8.0+)
@Serializable
data class UserRoute(val userId: String)

// In NavHost
composable<UserRoute> { backStackEntry ->
    val route = backStackEntry.toRoute<UserRoute>()
    // Type safety enforced by serialization
    UserProfileScreen(userId = route.userId)
}

// Navigation with type safety
fun navigateToUser(navController: NavController, userId: String) {
    // Sanitize before navigating
    require(userId.matches(Regex("^[a-zA-Z0-9-]+$"))) { "Invalid userId" }
    navController.navigate(UserRoute(userId = userId))
}
```

---

### COMPOSE-007: BackHandler Bypass on Protected Screens

- **Severity:** HIGH
- **Category:** Navigation & Deep Link Security
- **Description:** `BackHandler` composables that guard critical operations (e.g., preventing back-navigation during payment processing) can be bypassed through system-level navigation gestures, activity recreation, or configuration changes. The `BackHandler` only intercepts the system back event and does not protect against all navigation paths. Additionally, only the innermost enabled `BackHandler` is active, meaning nested composables can inadvertently override security-critical back handlers.
- **Detection Strategy:** Search for `BackHandler` used to protect critical flows and verify that the protection is also enforced at the navigation graph level (e.g., `popUpTo` with `inclusive`).
- **Detection Regex:** `BackHandler\s*\(` on screens with sensitive operations
- **Impact:** Premature exit from critical operations, inconsistent transaction state, bypassing confirmation dialogs.
- **CWE:** CWE-841 (Improper Enforcement of Behavioral Workflow)
- **OWASP Mobile:** M8:2024 - Security Misconfiguration

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Only BackHandler protects the payment flow
@Composable
fun PaymentScreen(navController: NavController) {
    var isProcessing by remember { mutableStateOf(false) }

    BackHandler(enabled = isProcessing) {
        // Block back during payment - but this can be bypassed by:
        // 1. System gesture navigation on some devices
        // 2. Activity recreation
        // 3. A nested BackHandler in a dialog
    }

    // Payment processing UI...
}
```

**Secure Pattern:**

```kotlin
// SECURE: Multi-layer protection for critical flows
@Composable
fun PaymentScreen(
    navController: NavController,
    viewModel: PaymentViewModel = hiltViewModel()
) {
    val paymentState by viewModel.paymentState.collectAsStateWithLifecycle()
    val isProcessing = paymentState is PaymentState.Processing

    // Layer 1: BackHandler for system back button
    BackHandler(enabled = isProcessing) {
        // Show confirmation dialog instead of silently blocking
        viewModel.showExitConfirmation()
    }

    // Layer 2: Navigation graph prevents back-stack pop during processing
    DisposableEffect(isProcessing) {
        if (isProcessing) {
            navController.enableOnBackPressed(false)
        }
        onDispose {
            navController.enableOnBackPressed(true)
        }
    }

    // Layer 3: Server-side transaction state ensures idempotency
    // Even if user navigates away, transaction completes correctly
}
```

---

## Category 2: State Management Security

### COMPOSE-008: MutableState Exposure from ViewModel

- **Severity:** HIGH
- **Category:** State Management Security
- **Description:** Exposing `MutableState<T>` or `mutableStateOf()` directly from a ViewModel allows any composable to mutate the state without going through the ViewModel's business logic. This breaks encapsulation and enables external components (including injected or malicious code in debug builds) to set arbitrary state values, bypassing validation, authorization checks, and audit logging.
- **Detection Strategy:** Search for `public` or `internal` `MutableState` properties in ViewModels. Only `State<T>` (read-only) should be publicly visible.
- **Detection Regex:** `(val|var)\s+\w+\s*=\s*mutableStateOf\(` in ViewModel classes without private modifier
- **Impact:** State corruption, bypass of business logic validation, unauthorized data modification.
- **CWE:** CWE-732 (Incorrect Permission Assignment for Critical Resource)
- **OWASP Mobile:** M8:2024 - Security Misconfiguration

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: MutableState exposed publicly
class AccountViewModel : ViewModel() {
    // Any composable can set this to any value
    var accountBalance = mutableStateOf(0.0)
    var isAdmin = mutableStateOf(false)
    var userRole = mutableStateOf("user")
}

// Attacker (or buggy composable) can do:
// viewModel.isAdmin.value = true
// viewModel.accountBalance.value = 999999.0
```

**Secure Pattern:**

```kotlin
// SECURE: Private mutable state with read-only public accessor
class AccountViewModel : ViewModel() {
    private val _accountBalance = mutableStateOf(0.0)
    val accountBalance: State<Double> = _accountBalance

    private val _isAdmin = mutableStateOf(false)
    val isAdmin: State<Boolean> = _isAdmin

    // State changes only through validated methods
    fun updateBalance(amount: Double) {
        require(amount >= 0) { "Balance cannot be negative" }
        _accountBalance.value = amount
    }
}
```

---

### COMPOSE-009: MutableStateFlow External Mutation

- **Severity:** HIGH
- **Category:** State Management Security
- **Description:** Exposing `MutableStateFlow` instead of `StateFlow` from a ViewModel allows external callers to emit arbitrary values directly, bypassing the ViewModel's state management logic. Unlike `MutableState`, `MutableStateFlow` is thread-safe but the security concern is identical: external mutation bypasses validation, authorization, and audit controls.
- **Detection Strategy:** Search for `MutableStateFlow` return types or public properties in ViewModels. Only `StateFlow` should be exposed.
- **Detection Regex:** `(val|var)\s+\w+\s*[:=]\s*MutableStateFlow` without private modifier
- **Impact:** State corruption, unauthorized data modification, bypassed business rules.
- **CWE:** CWE-732 (Incorrect Permission Assignment for Critical Resource)
- **OWASP Mobile:** M8:2024 - Security Misconfiguration

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: MutableStateFlow exposed to composables
class UserViewModel : ViewModel() {
    val userState = MutableStateFlow<UserState>(UserState.LoggedOut)
    val permissions = MutableStateFlow<Set<String>>(emptySet())
}

// Any composable can emit:
// viewModel.userState.value = UserState.LoggedIn(adminUser)
// viewModel.permissions.value = setOf("admin", "superuser")
```

**Secure Pattern:**

```kotlin
// SECURE: Backing property pattern with read-only exposure
class UserViewModel : ViewModel() {
    private val _userState = MutableStateFlow<UserState>(UserState.LoggedOut)
    val userState: StateFlow<UserState> = _userState.asStateFlow()

    private val _permissions = MutableStateFlow<Set<String>>(emptySet())
    val permissions: StateFlow<Set<String>> = _permissions.asStateFlow()

    // Controlled state transitions
    fun login(credentials: Credentials) {
        viewModelScope.launch {
            val result = authRepository.authenticate(credentials)
            _userState.value = result
            _permissions.value = result.permissions
        }
    }
}
```

---

### COMPOSE-010: SnapshotStateList Thread Safety Violation

- **Severity:** MEDIUM
- **Category:** State Management Security
- **Description:** `SnapshotStateList` and `SnapshotStateMap` (returned by `mutableStateListOf()` and `mutableStateMapOf()`) provide snapshot isolation between different snapshots but are NOT thread-safe within the same snapshot. If two threads modify the same `SnapshotStateList` from the same snapshot without synchronization, data races occur. This can lead to corrupted data, lost updates, or `ConcurrentModificationException` crashes, any of which may leave the application in an insecure state.
- **Detection Strategy:** Search for `mutableStateListOf()` or `mutableStateMapOf()` usage where modifications happen from coroutines on different dispatchers or background threads.
- **Detection Regex:** `mutableState(ListOf|MapOf)\s*\(` combined with `Dispatchers\.(IO|Default)` access patterns
- **Impact:** Data corruption, inconsistent UI state, potential crash leaving app in insecure state.
- **CWE:** CWE-362 (Concurrent Execution using Shared Resource with Improper Synchronization)
- **OWASP Mobile:** M8:2024 - Security Misconfiguration

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: SnapshotStateList modified from multiple threads
class DataViewModel : ViewModel() {
    val items = mutableStateListOf<Item>()

    fun loadItems() {
        viewModelScope.launch(Dispatchers.IO) {
            val newItems = repository.fetchItems()
            // UNSAFE: Modifying snapshot state from IO dispatcher
            items.addAll(newItems)
        }
    }

    fun deleteItem(item: Item) {
        viewModelScope.launch(Dispatchers.Default) {
            // UNSAFE: Concurrent modification from different dispatcher
            items.remove(item)
        }
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: All state modifications on Main dispatcher
class DataViewModel : ViewModel() {
    private val _items = mutableStateListOf<Item>()
    val items: List<Item> = _items

    fun loadItems() {
        viewModelScope.launch {
            val newItems = withContext(Dispatchers.IO) {
                repository.fetchItems()
            }
            // Safe: Back on Main dispatcher for state mutation
            _items.addAll(newItems)
        }
    }

    fun deleteItem(item: Item) {
        // viewModelScope defaults to Dispatchers.Main
        viewModelScope.launch {
            _items.remove(item)
        }
    }
}
```

---

### COMPOSE-011: State Hoisting Sensitive Data Leak

- **Severity:** MEDIUM
- **Category:** State Management Security
- **Description:** State hoisting—moving state up to a common ancestor—can inadvertently expose sensitive data (passwords, tokens, PII) to composables that should not have access. When sensitive state is hoisted too high in the composition tree, all child composables in that subtree gain read access. In combination with accessibility services or debug tools, this broadens the attack surface for sensitive data exposure.
- **Detection Strategy:** Search for sensitive state variables (containing password, token, secret, pin, ssn, credit card patterns) that are hoisted above the composable that directly uses them.
- **Detection Regex:** `(password|token|secret|pin|ssn|creditCard|cvv)\s*[:=]` in composable function parameters
- **Impact:** Sensitive data accessible to unintended UI components, increased attack surface.
- **CWE:** CWE-200 (Exposure of Sensitive Information to an Unauthorized Actor)
- **OWASP Mobile:** M9:2024 - Insecure Data Storage

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Password state hoisted to parent composable
@Composable
fun AuthScreen() {
    var password by remember { mutableStateOf("") }

    Column {
        // Password is now accessible to all children
        HeaderSection(password = password)  // Header doesn't need password
        PasswordInput(password = password, onPasswordChange = { password = it })
        LoginButton(password = password)
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: Sensitive state scoped to minimum required composables
@Composable
fun AuthScreen(viewModel: AuthViewModel = hiltViewModel()) {
    Column {
        HeaderSection()
        // Password state managed inside the ViewModel, not hoisted
        PasswordSection(
            onLogin = { password -> viewModel.login(password) }
        )
    }
}

@Composable
private fun PasswordSection(onLogin: (String) -> Unit) {
    // Password state contained within this scope only
    var password by remember { mutableStateOf("") }

    PasswordInput(
        password = password,
        onPasswordChange = { password = it }
    )
    LoginButton(onClick = {
        onLogin(password)
        password = ""  // Clear after use
    })
}
```

---

### COMPOSE-012: Stale State via remember Without Keys

- **Severity:** MEDIUM
- **Category:** State Management Security
- **Description:** Using `remember` without appropriate keys can cause stale references to persist across recompositions. When a remembered value depends on a changing parameter (such as a user ID or session token), failing to include that parameter as a key means the remembered value reflects the old parameter. This can lead to displaying another user's data, using an expired token, or operating on stale authorization context.
- **Detection Strategy:** Search for `remember { }` blocks that reference parameters from outer scope but do not include those parameters as keys.
- **Detection Regex:** `remember\s*\{` without `remember\(.*key` when referencing function parameters
- **Impact:** Data leakage between user sessions, stale authorization context, displaying incorrect data.
- **CWE:** CWE-613 (Insufficient Session Expiration)
- **OWASP Mobile:** M3:2024 - Insecure Authentication/Authorization

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Remembered value doesn't update when userId changes
@Composable
fun UserProfileScreen(userId: String) {
    // If userId changes (e.g., user switch), this remembers the OLD data
    val userData = remember {
        // This closure captures the initial userId and never updates
        loadUserData(userId)
    }

    Text(text = "Welcome, ${userData.name}")
}
```

**Secure Pattern:**

```kotlin
// SECURE: Key-based remember updates when userId changes
@Composable
fun UserProfileScreen(userId: String) {
    val userData = remember(userId) {
        loadUserData(userId)
    }

    Text(text = "Welcome, ${userData.name}")
}
```

---

### COMPOSE-013: Derived State Caching Sensitive Values

- **Severity:** LOW
- **Category:** State Management Security
- **Description:** `derivedStateOf` caches computed values and only recomputes when dependencies change. If sensitive data (decrypted secrets, temporary tokens) is computed via `derivedStateOf`, the decrypted value remains cached in memory longer than necessary, increasing the window for memory dump attacks on rooted devices.
- **Detection Strategy:** Search for `derivedStateOf` blocks that compute or transform sensitive values (tokens, decrypted data, PII).
- **Detection Regex:** `derivedStateOf\s*\{[^}]*(decrypt|token|secret|password|key)`
- **Impact:** Extended exposure of sensitive data in memory, exploitable via memory dump on rooted devices.
- **CWE:** CWE-316 (Cleartext Storage of Sensitive Information in Memory)
- **OWASP Mobile:** M9:2024 - Insecure Data Storage

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Decrypted token cached in derivedStateOf
@Composable
fun SecureScreen(encryptedToken: String) {
    val decryptedToken by remember {
        derivedStateOf {
            // Decrypted value stays cached in memory
            CryptoUtil.decrypt(encryptedToken)
        }
    }
    ApiClient.setHeader("Authorization", "Bearer $decryptedToken")
}
```

**Secure Pattern:**

```kotlin
// SECURE: Use token transiently, don't cache decrypted values in state
@Composable
fun SecureScreen(viewModel: SecureViewModel = hiltViewModel()) {
    // Token management handled in ViewModel with proper lifecycle
    LaunchedEffect(Unit) {
        viewModel.initializeSecureSession()
    }
    // UI does not hold decrypted sensitive values
}
```

---

## Category 3: Side-Effect Security

### COMPOSE-014: LaunchedEffect Key Manipulation

- **Severity:** HIGH
- **Category:** Side-Effect Security
- **Description:** `LaunchedEffect` restarts its coroutine block whenever any of its keys change. If an attacker can influence a key value (e.g., through a navigation argument or external input), they can force repeated execution of the effect. This can trigger repeated API calls, authentication flows, or resource-intensive operations, potentially causing denial of service or race conditions in security-sensitive flows.
- **Detection Strategy:** Search for `LaunchedEffect` with keys derived from user input, navigation arguments, or external data sources.
- **Detection Regex:** `LaunchedEffect\s*\([^)]*\b(argument|param|input|query|url)\b`
- **Impact:** Repeated execution of sensitive operations, API abuse, race conditions in authentication flows.
- **CWE:** CWE-400 (Uncontrolled Resource Consumption)
- **OWASP Mobile:** M4:2024 - Insufficient Input/Output Validation

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: LaunchedEffect key controlled by external input
@Composable
fun PaymentScreen(transactionId: String) {
    // Attacker changes transactionId via deep link, retriggering payment
    LaunchedEffect(transactionId) {
        paymentService.processPayment(transactionId)
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: Idempotent effect with validation and deduplication
@Composable
fun PaymentScreen(
    transactionId: String,
    viewModel: PaymentViewModel = hiltViewModel()
) {
    val paymentState by viewModel.paymentState.collectAsStateWithLifecycle()

    LaunchedEffect(transactionId) {
        // Validate format
        if (!transactionId.matches(Regex("^txn-[a-f0-9-]{36}$"))) return@LaunchedEffect
        // Check if already processed (idempotency)
        if (paymentState !is PaymentState.Idle) return@LaunchedEffect
        viewModel.processPayment(transactionId)
    }
}
```

---

### COMPOSE-015: DisposableEffect Missing Cleanup

- **Severity:** HIGH
- **Category:** Side-Effect Security
- **Description:** `DisposableEffect` requires an `onDispose` block to clean up resources when the composable leaves the composition or keys change. Missing or incomplete cleanup can leave security-sensitive resources active: listeners that continue receiving sensitive events, broadcast receivers that remain registered, or connections that stay open. When `DisposableEffect` keys are incorrect, the effect is not restarted when parameters change, causing it to operate with stale security context.
- **Detection Strategy:** Search for `DisposableEffect` blocks and verify each has a substantive `onDispose` block. Flag empty `onDispose {}` blocks.
- **Detection Regex:** `onDispose\s*\{\s*\}` (empty cleanup block)
- **Impact:** Resource leaks, continued processing with stale credentials, unauthorized event monitoring.
- **CWE:** CWE-404 (Improper Resource Shutdown or Release)
- **OWASP Mobile:** M8:2024 - Security Misconfiguration

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: DisposableEffect with empty cleanup
@Composable
fun LocationTracker() {
    val context = LocalContext.current
    DisposableEffect(Unit) {
        val receiver = object : BroadcastReceiver() {
            override fun onReceive(context: Context, intent: Intent) {
                // Processes location updates with current user context
                handleLocationUpdate(intent)
            }
        }
        context.registerReceiver(receiver, IntentFilter(LocationManager.PROVIDERS_CHANGED_ACTION))

        onDispose {
            // EMPTY - receiver continues receiving events after composable is removed
        }
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: Proper cleanup in onDispose
@Composable
fun LocationTracker() {
    val context = LocalContext.current
    DisposableEffect(Unit) {
        val receiver = object : BroadcastReceiver() {
            override fun onReceive(ctx: Context, intent: Intent) {
                handleLocationUpdate(intent)
            }
        }
        context.registerReceiver(
            receiver,
            IntentFilter(LocationManager.PROVIDERS_CHANGED_ACTION)
        )

        onDispose {
            context.unregisterReceiver(receiver)
        }
    }
}
```

---

### COMPOSE-016: rememberUpdatedState Staleness

- **Severity:** MEDIUM
- **Category:** Side-Effect Security
- **Description:** `rememberUpdatedState` captures a reference to a value that may change across recompositions, allowing a long-running effect to always read the latest value. If developers forget to use `rememberUpdatedState` for callbacks or values that change over time (such as authentication tokens or user permissions), the effect continues using the stale original value. This can result in operations executing with expired or revoked authorization.
- **Detection Strategy:** Search for `LaunchedEffect(Unit)` or long-running effects that reference lambda parameters or mutable values without `rememberUpdatedState`.
- **Detection Regex:** `LaunchedEffect\(Unit\)\s*\{[^}]*\b(onResult|callback|token|permission)\b` without `rememberUpdatedState`
- **Impact:** Operations executing with expired tokens or revoked permissions, authorization bypass.
- **CWE:** CWE-613 (Insufficient Session Expiration)
- **OWASP Mobile:** M3:2024 - Insecure Authentication/Authorization

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Stale token used in long-running effect
@Composable
fun DataSyncScreen(authToken: String) {
    LaunchedEffect(Unit) {
        // This captures the INITIAL authToken and never updates
        while (isActive) {
            api.syncData(authToken)  // Uses expired token
            delay(30_000)
        }
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: Always reads the latest token
@Composable
fun DataSyncScreen(authToken: String) {
    val currentToken by rememberUpdatedState(authToken)

    LaunchedEffect(Unit) {
        while (isActive) {
            api.syncData(currentToken)  // Always uses current token
            delay(30_000)
        }
    }
}
```

---

### COMPOSE-017: SideEffect Timing Leak

- **Severity:** MEDIUM
- **Category:** Side-Effect Security
- **Description:** `SideEffect` runs after every successful recomposition and is not scoped to any lifecycle. If a `SideEffect` performs security-sensitive operations (logging auth state, updating external state, sending analytics), the timing and frequency of its execution can leak information about recomposition patterns, which in turn reveals user interaction patterns, state changes, and UI structure to any code monitoring recomposition frequency.
- **Detection Strategy:** Search for `SideEffect` blocks that log sensitive data, update external analytics, or communicate with external systems.
- **Detection Regex:** `SideEffect\s*\{[^}]*(log|analytics|track|report|send)`
- **Impact:** Information leakage through timing analysis, excessive logging of sensitive state changes.
- **CWE:** CWE-208 (Observable Timing Discrepancy)
- **OWASP Mobile:** M6:2024 - Inadequate Privacy Controls

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: SideEffect leaks auth state to analytics on every recomposition
@Composable
fun ProtectedContent(isAdmin: Boolean, userId: String) {
    SideEffect {
        // Runs on every recomposition - frequency reveals interaction patterns
        analytics.log("render_protected", mapOf(
            "isAdmin" to isAdmin.toString(),
            "userId" to userId
        ))
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: Use LaunchedEffect with specific keys for controlled execution
@Composable
fun ProtectedContent(isAdmin: Boolean, userId: String) {
    // Only fires when the specific tracked values change
    LaunchedEffect(isAdmin, userId) {
        analytics.log("auth_state_change", mapOf(
            "role" to if (isAdmin) "admin" else "user"
            // Don't log userId to analytics
        ))
    }
}
```

---

### COMPOSE-018: produceState Uncancelled Coroutine Leak

- **Severity:** HIGH
- **Category:** Side-Effect Security
- **Description:** `produceState` launches a coroutine that produces state values over time. If the producer coroutine spawns child coroutines or uses `withContext` blocks that are not structured properly, they may not cancel when the composable leaves the composition. This can result in continued execution with stale security context, network requests using expired credentials, or data writes to resources the user no longer has access to.
- **Detection Strategy:** Search for `produceState` blocks that launch child coroutines or use `GlobalScope` instead of the provided scope.
- **Detection Regex:** `produceState\s*\([^)]*\)\s*\{[^}]*GlobalScope\.launch`
- **Impact:** Continued execution after composable disposal, stale security context, resource leaks.
- **CWE:** CWE-404 (Improper Resource Shutdown or Release)
- **OWASP Mobile:** M8:2024 - Security Misconfiguration

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Unstructured coroutine inside produceState
@Composable
fun LiveDataScreen(userId: String) {
    val data by produceState<List<Item>>(initialValue = emptyList(), userId) {
        // WRONG: GlobalScope outlives the composable
        GlobalScope.launch {
            repository.observeItems(userId).collect { items ->
                value = items  // Writes to disposed state
            }
        }
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: Use structured concurrency within produceState
@Composable
fun LiveDataScreen(userId: String) {
    val data by produceState<List<Item>>(initialValue = emptyList(), userId) {
        // Correct: Uses the ProduceStateScope's coroutine context
        // Automatically cancelled when composable leaves composition
        repository.observeItems(userId).collect { items ->
            value = items
        }
    }
}
```

---

## Category 4: UI Security & Screen Protection

### COMPOSE-019: Missing FLAG_SECURE on Sensitive Screens

- **Severity:** CRITICAL
- **Category:** UI Security & Screen Protection
- **Description:** `FLAG_SECURE` prevents screenshots, screen recordings, and display on non-secure outputs (such as screen casting). In Compose, this flag must be set on the hosting Activity's window since Compose does not have its own window management. Unlike the View system, Compose properly propagates FLAG_SECURE to all composables including dialogs and popups when set on the Activity. However, failing to set the flag at all leaves sensitive screens (banking, medical, authentication) completely unprotected.
- **Detection Strategy:** Search for screens displaying sensitive data (account balances, medical records, payment info) and verify the hosting Activity sets `FLAG_SECURE`. Check for lifecycle-aware toggling for per-screen protection.
- **Detection Regex:** `FLAG_SECURE` absence in Activities hosting sensitive composables
- **Impact:** Sensitive data captured via screenshots, screen recordings, or screen casting by malicious apps.
- **CWE:** CWE-200 (Exposure of Sensitive Information to an Unauthorized Actor)
- **OWASP Mobile:** M9:2024 - Insecure Data Storage

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: No FLAG_SECURE on activity hosting sensitive composables
class BankingActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            BankingApp()  // Displays account balances, transactions
        }
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: FLAG_SECURE set on activity, with per-screen lifecycle control
class BankingActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.setFlags(
            WindowManager.LayoutParams.FLAG_SECURE,
            WindowManager.LayoutParams.FLAG_SECURE
        )
        setContent {
            BankingApp()
        }
    }
}

// For per-screen control within a single Activity:
@Composable
fun SecureScreenWrapper(content: @Composable () -> Unit) {
    val activity = LocalContext.current as? Activity
    DisposableEffect(Unit) {
        activity?.window?.addFlags(WindowManager.LayoutParams.FLAG_SECURE)
        onDispose {
            activity?.window?.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)
        }
    }
    content()
}
```

---

### COMPOSE-020: Tapjacking via Overlay Attack

- **Severity:** CRITICAL
- **Category:** UI Security & Screen Protection
- **Description:** Tapjacking is the Android equivalent of clickjacking: a malicious app draws an overlay on top of the target app, tricking the user into tapping security-relevant controls (confirmation buttons, permission grants). In Compose, there is no direct `Modifier.filterTouchesWhenObscured` API. Protection must be applied at the View/Window level. Prior to Android 12 (API 31), apps must explicitly set `filterTouchesWhenObscured`. Android 12+ blocks touches from non-trusted overlays by default, but only for layers with opacity >= 0.8.
- **Detection Strategy:** Search for security-sensitive buttons (confirm payment, grant permission, delete account) and verify overlay protection is applied to the hosting Activity or View.
- **Detection Regex:** `filterTouchesWhenObscured` absence in activities with sensitive actions
- **Impact:** Users tricked into confirming sensitive actions (payments, permission grants, data deletion).
- **CWE:** CWE-1021 (Improper Restriction of Rendered UI Layers or Frames)
- **OWASP Mobile:** M8:2024 - Security Misconfiguration

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: No overlay protection on payment confirmation
@Composable
fun PaymentConfirmation(amount: Double, onConfirm: () -> Unit) {
    Button(onClick = onConfirm) {
        Text("Pay $${"%.2f".format(amount)}")
    }
    // Malicious overlay can cover the amount while exposing the button
}
```

**Secure Pattern:**

```kotlin
// SECURE: Overlay protection applied at the Activity level
class PaymentActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Protect against overlay attacks
        window.decorView.filterTouchesWhenObscured = true

        // For Android 12+: hide overlay windows on this activity
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            window.setHideOverlayWindows(true)
        }

        setContent {
            PaymentConfirmation(
                amount = intent.getDoubleExtra("amount", 0.0),
                onConfirm = { processPayment() }
            )
        }
    }
}
```

---

### COMPOSE-021: Partial Occlusion UI Deception

- **Severity:** HIGH
- **Category:** UI Security & Screen Protection
- **Description:** Unlike full occlusion (which can be blocked by `filterTouchesWhenObscured`), partial occlusion allows the touch target to remain visible while surrounding context is obscured. A malicious app can display a deceptive overlay that changes the perceived meaning of a button without blocking touches. For example, changing "Transfer $10 to John" to "Transfer $10,000 to Attacker" while leaving the "Confirm" button touchable. The `FLAG_WINDOW_IS_PARTIALLY_OBSCURED` flag can detect this but requires manual handling.
- **Detection Strategy:** Verify that security-critical screens handle `MotionEvent.FLAG_WINDOW_IS_PARTIALLY_OBSCURED`. Check for use of Android 16+ `accessibilityDataSensitive` attribute on sensitive views.
- **Detection Regex:** `FLAG_WINDOW_IS_PARTIALLY_OBSCURED` or `accessibilityDataSensitive` absence on critical screens
- **Impact:** Users deceived into confirming manipulated transaction details.
- **CWE:** CWE-1021 (Improper Restriction of Rendered UI Layers or Frames)
- **OWASP Mobile:** M8:2024 - Security Misconfiguration

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: No partial occlusion detection
@Composable
fun TransferConfirmation(amount: Double, recipient: String) {
    // Overlay can cover the amount/recipient while leaving the button visible
    Text("Transfer $${"%.2f".format(amount)} to $recipient")
    Button(onClick = { executeTransfer(amount, recipient) }) {
        Text("Confirm Transfer")
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: Detect and respond to partial occlusion
@Composable
fun TransferConfirmation(amount: Double, recipient: String) {
    var isObscured by remember { mutableStateOf(false) }

    AndroidView(
        factory = { context ->
            ComposeView(context).apply {
                setOnTouchListener { _, event ->
                    isObscured = event.flags and
                        MotionEvent.FLAG_WINDOW_IS_PARTIALLY_OBSCURED != 0
                    false
                }
            }
        }
    )

    Text("Transfer $${"%.2f".format(amount)} to $recipient")

    if (isObscured) {
        Text(
            "Screen is partially obscured. Please close other apps.",
            color = MaterialTheme.colorScheme.error
        )
    }

    Button(
        onClick = { if (!isObscured) executeTransfer(amount, recipient) },
        enabled = !isObscured
    ) {
        Text("Confirm Transfer")
    }
}
```

---

### COMPOSE-022: Task Hijacking (StrandHogg)

- **Severity:** HIGH
- **Category:** UI Security & Screen Protection
- **Description:** Task hijacking (StrandHogg attack) occurs when a malicious app sets its `taskAffinity` to match the target app's package name. When the target app is launched, the malicious activity appears on top, displaying a phishing UI that looks identical to the legitimate app. Many developers mistakenly believe that adopting Kotlin and Jetpack Compose automatically prevents this vulnerability, but task hijacking operates at the Android component architecture level, not the UI layer.
- **Detection Strategy:** Check `AndroidManifest.xml` for `taskAffinity` settings. All activities should have `android:taskAffinity=""` to prevent hijacking.
- **Detection Regex:** `<activity[^>]+(?!android:taskAffinity)` (activities missing taskAffinity)
- **Impact:** Credential theft via phishing overlay, session hijacking, complete impersonation of the legitimate app.
- **CWE:** CWE-200 (Exposure of Sensitive Information to an Unauthorized Actor)
- **OWASP Mobile:** M3:2024 - Insecure Authentication/Authorization

**Vulnerable Pattern:**

```xml
<!-- VULNERABLE: Default taskAffinity matches package name -->
<application android:name=".TrailLensApp">
    <activity
        android:name=".MainActivity"
        android:exported="true">
        <!-- taskAffinity defaults to package name, enabling StrandHogg -->
    </activity>
    <activity android:name=".PaymentActivity" />
</application>
```

**Secure Pattern:**

```xml
<!-- SECURE: Empty taskAffinity on all activities -->
<application
    android:name=".TrailLensApp"
    android:taskAffinity="">
    <activity
        android:name=".MainActivity"
        android:exported="true"
        android:taskAffinity="">
        <intent-filter>
            <action android:name="android.intent.action.MAIN" />
            <category android:name="android.intent.category.LAUNCHER" />
        </intent-filter>
    </activity>
    <activity
        android:name=".PaymentActivity"
        android:taskAffinity=""
        android:exported="false" />
</application>
```

---

### COMPOSE-023: Recent Apps Screenshot Exposure

- **Severity:** MEDIUM
- **Category:** UI Security & Screen Protection
- **Description:** When an app enters the background, Android captures a screenshot for the Recent Apps (task switcher) screen. This screenshot includes whatever was visible on screen at that moment, potentially exposing sensitive data. Without `FLAG_SECURE`, banking details, medical records, authentication tokens, and other sensitive information are captured and visible to anyone who can see the device's Recent Apps screen. In Compose, this requires lifecycle-aware management since screens may need selective protection.
- **Detection Strategy:** Verify screens displaying sensitive data implement lifecycle observers that either set `FLAG_SECURE` or display a privacy overlay when the app goes to the background.
- **Detection Regex:** `Lifecycle.Event.ON_STOP` or `FLAG_SECURE` near sensitive screens
- **Impact:** Sensitive data visible in Recent Apps screen, accessible to shoulder surfers or device-sharing scenarios.
- **CWE:** CWE-200 (Exposure of Sensitive Information to an Unauthorized Actor)
- **OWASP Mobile:** M9:2024 - Insecure Data Storage

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Sensitive data visible in Recent Apps screenshot
@Composable
fun AccountDetailsScreen(viewModel: AccountViewModel = hiltViewModel()) {
    val balance by viewModel.balance.collectAsStateWithLifecycle()
    val ssn by viewModel.socialSecurityNumber.collectAsStateWithLifecycle()

    Column {
        Text("Balance: $$balance")
        Text("SSN: $ssn")
        // All visible in Recent Apps thumbnail
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: Lifecycle-aware privacy protection
@Composable
fun AccountDetailsScreen(viewModel: AccountViewModel = hiltViewModel()) {
    val balance by viewModel.balance.collectAsStateWithLifecycle()
    val lifecycleOwner = LocalLifecycleOwner.current
    val activity = LocalContext.current as? Activity

    // Set FLAG_SECURE when this screen is active
    DisposableEffect(lifecycleOwner) {
        val observer = LifecycleEventObserver { _, event ->
            when (event) {
                Lifecycle.Event.ON_RESUME -> {
                    activity?.window?.addFlags(WindowManager.LayoutParams.FLAG_SECURE)
                }
                Lifecycle.Event.ON_PAUSE -> {
                    // Optionally clear when leaving
                    activity?.window?.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)
                }
                else -> {}
            }
        }
        lifecycleOwner.lifecycle.addObserver(observer)
        onDispose {
            lifecycleOwner.lifecycle.removeObserver(observer)
            activity?.window?.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)
        }
    }

    Column {
        Text("Balance: $$balance")
        // SSN not displayed directly, shown only on explicit tap
    }
}
```

---

## Category 5: Text Input & Credential Security

### COMPOSE-024: Password Field Missing Visual Transformation

- **Severity:** HIGH
- **Category:** Text Input & Credential Security
- **Description:** Compose `TextField` and `OutlinedTextField` do not mask input by default. A password field without `visualTransformation = PasswordVisualTransformation()` displays the password in cleartext, making it visible to shoulder surfers, screen recordings, and accessibility services. Additionally, `keyboardType = KeyboardType.Password` only suggests the keyboard type to the IME but does NOT mask the displayed text.
- **Detection Strategy:** Search for TextField composables used for passwords that lack `PasswordVisualTransformation`.
- **Detection Regex:** `(TextField|OutlinedTextField)\s*\([^)]*password[^)]*(?!PasswordVisualTransformation)`  (case insensitive)
- **Impact:** Password visible in cleartext on screen, captured by screen recording or shoulder surfing.
- **CWE:** CWE-549 (Missing Password Field Masking)
- **OWASP Mobile:** M9:2024 - Insecure Data Storage

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Password displayed in cleartext
@Composable
fun LoginForm() {
    var password by remember { mutableStateOf("") }

    TextField(
        value = password,
        onValueChange = { password = it },
        label = { Text("Password") },
        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password)
        // Missing: visualTransformation = PasswordVisualTransformation()
    )
}
```

**Secure Pattern:**

```kotlin
// SECURE: Password masked with visual transformation
@Composable
fun LoginForm() {
    var password by remember { mutableStateOf("") }
    var passwordVisible by remember { mutableStateOf(false) }

    OutlinedTextField(
        value = password,
        onValueChange = { password = it },
        label = { Text("Password") },
        visualTransformation = if (passwordVisible)
            VisualTransformation.None
        else
            PasswordVisualTransformation(),
        keyboardOptions = KeyboardOptions(
            keyboardType = KeyboardType.Password,
            imeAction = ImeAction.Done,
            capitalization = KeyboardCapitalization.None,
            autoCorrect = false
        ),
        trailingIcon = {
            IconButton(onClick = { passwordVisible = !passwordVisible }) {
                Icon(
                    imageVector = if (passwordVisible)
                        Icons.Filled.Visibility
                    else
                        Icons.Filled.VisibilityOff,
                    contentDescription = "Toggle password visibility"
                )
            }
        }
    )
}
```

---

### COMPOSE-025: Clipboard Data Leakage from TextField

- **Severity:** HIGH
- **Category:** Text Input & Credential Security
- **Description:** By default, Compose `TextField` allows copy, cut, and paste operations via long-press context menu or keyboard shortcuts. For password fields and sensitive data fields (credit cards, SSN), the copy and cut operations expose sensitive content to the system clipboard, which is accessible to all applications. Android 12 shows clipboard previews in the notification shade, and Android 13+ auto-clears clipboard after 60 seconds, but older versions retain clipboard content indefinitely.
- **Detection Strategy:** Search for TextField composables handling sensitive data (passwords, credit cards, SSN) that do not disable copy/cut operations.
- **Detection Regex:** `(TextField|OutlinedTextField|BasicTextField)\s*\([^)]*\b(password|creditCard|ssn|cvv|pin)\b` without clipboard restriction
- **Impact:** Sensitive data exposed to all applications via system clipboard.
- **CWE:** CWE-200 (Exposure of Sensitive Information to an Unauthorized Actor)
- **OWASP Mobile:** M9:2024 - Insecure Data Storage

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Password field allows copy/cut to clipboard
@Composable
fun PasswordField() {
    var password by remember { mutableStateOf("") }

    TextField(
        value = password,
        onValueChange = { password = it },
        visualTransformation = PasswordVisualTransformation()
        // Copy/cut still available via long-press menu
    )
}
```

**Secure Pattern:**

```kotlin
// SECURE: Clipboard operations restricted for sensitive fields
@Composable
fun PasswordField() {
    var password by remember { mutableStateOf("") }

    CompositionLocalProvider(
        LocalClipboardManager provides object : ClipboardManager {
            // Allow paste (for password managers) but block copy/cut
            override fun getText(): AnnotatedString? =
                LocalClipboardManager.current.getText()
            override fun setText(annotatedString: AnnotatedString) {
                // No-op: prevent copying password to clipboard
            }
        }
    ) {
        TextField(
            value = password,
            onValueChange = { password = it },
            visualTransformation = PasswordVisualTransformation(),
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Password,
                autoCorrect = false
            )
        )
    }
}
```

---

### COMPOSE-026: IME Keyboard Data Interception

- **Severity:** MEDIUM
- **Category:** Text Input & Credential Security
- **Description:** Standard Android IME (Input Method Editor) keyboards have broad system privileges and can log keystrokes, access clipboard, transmit data over the network, and access accessibility events. Third-party keyboards from untrusted sources may exfiltrate sensitive input data. While the app cannot control which keyboard the user has installed, it should use `KeyboardType.Password` to signal the IME to suppress auto-complete, predictions, and learning for sensitive fields.
- **Detection Strategy:** Search for sensitive input fields that do not set appropriate `keyboardType` or `imeAction` options.
- **Detection Regex:** `KeyboardOptions\s*\([^)]*(?!keyboardType\s*=\s*KeyboardType\.Password)` on password/sensitive fields
- **Impact:** Sensitive input data logged or transmitted by malicious IME keyboards.
- **CWE:** CWE-319 (Cleartext Transmission of Sensitive Information)
- **OWASP Mobile:** M5:2024 - Insecure Communication

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Sensitive field uses default keyboard type
@Composable
fun CreditCardInput() {
    var cardNumber by remember { mutableStateOf("") }

    TextField(
        value = cardNumber,
        onValueChange = { cardNumber = it },
        label = { Text("Card Number") }
        // Default keyboard: IME may cache/suggest card numbers
    )
}
```

**Secure Pattern:**

```kotlin
// SECURE: Appropriate keyboard type suppresses IME learning
@Composable
fun CreditCardInput() {
    var cardNumber by remember { mutableStateOf("") }

    TextField(
        value = cardNumber,
        onValueChange = { input ->
            cardNumber = input.filter { it.isDigit() }.take(16)
        },
        label = { Text("Card Number") },
        keyboardOptions = KeyboardOptions(
            keyboardType = KeyboardType.Number,
            imeAction = ImeAction.Next,
            autoCorrect = false
        ),
        // For highest security, consider a custom in-app keyboard
    )
}
```

---

### COMPOSE-027: AutoCorrect on Sensitive Fields

- **Severity:** MEDIUM
- **Category:** Text Input & Credential Security
- **Description:** When `autoCorrect` is enabled (the default) in `KeyboardOptions`, the IME stores typed words in its dictionary for future predictions. For sensitive fields (passwords, PINs, security answers, medical data), this means sensitive values are stored in the IME's learned dictionary and may appear as auto-suggestions in other apps. This persists across app uninstallation since the IME dictionary is independent of the app.
- **Detection Strategy:** Search for sensitive input fields where `autoCorrect` is not explicitly set to `false`.
- **Detection Regex:** `KeyboardOptions\s*\([^)]*(?!autoCorrect\s*=\s*false)` on sensitive fields
- **Impact:** Sensitive input persisted in IME dictionary, suggesting sensitive values in other apps.
- **CWE:** CWE-312 (Cleartext Storage of Sensitive Information)
- **OWASP Mobile:** M9:2024 - Insecure Data Storage

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: autoCorrect not disabled for security question
@Composable
fun SecurityQuestionInput() {
    var answer by remember { mutableStateOf("") }

    TextField(
        value = answer,
        onValueChange = { answer = it },
        label = { Text("Mother's maiden name") },
        keyboardOptions = KeyboardOptions(
            keyboardType = KeyboardType.Text
            // autoCorrect defaults to true - answer is learned by IME
        )
    )
}
```

**Secure Pattern:**

```kotlin
// SECURE: autoCorrect disabled, capitalization disabled
@Composable
fun SecurityQuestionInput() {
    var answer by remember { mutableStateOf("") }

    TextField(
        value = answer,
        onValueChange = { answer = it },
        label = { Text("Mother's maiden name") },
        keyboardOptions = KeyboardOptions(
            keyboardType = KeyboardType.Text,
            autoCorrect = false,
            capitalization = KeyboardCapitalization.None
        )
    )
}
```

---

### COMPOSE-028: Autofill Sensitive Data Exposure

- **Severity:** MEDIUM
- **Category:** Text Input & Credential Security
- **Description:** Android's Autofill Framework can expose sensitive data to third-party autofill providers. In Compose, `Modifier.autofill()` or semantic autofill hints inform the autofill service about field types. Malicious autofill providers can harvest form data, and legitimate providers may store sensitive data insecurely. For high-security fields (PINs, OTPs, 2FA codes), autofill should be explicitly disabled to prevent data exposure to third-party services.
- **Detection Strategy:** Search for security-critical input fields (OTP, PIN, 2FA) that do not disable autofill.
- **Detection Regex:** `autofill|AutofillType` on OTP/PIN/2FA fields without explicit disable
- **Impact:** Sensitive one-time codes or PINs exposed to third-party autofill providers.
- **CWE:** CWE-200 (Exposure of Sensitive Information to an Unauthorized Actor)
- **OWASP Mobile:** M9:2024 - Insecure Data Storage

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: OTP field with autofill enabled
@Composable
fun OtpInput() {
    var otp by remember { mutableStateOf("") }

    TextField(
        value = otp,
        onValueChange = { otp = it },
        label = { Text("Enter OTP") }
        // Autofill service may capture OTP codes
    )
}
```

**Secure Pattern:**

```kotlin
// SECURE: Autofill disabled for OTP/2FA fields
@Composable
fun OtpInput() {
    var otp by remember { mutableStateOf("") }

    TextField(
        value = otp,
        onValueChange = { input ->
            otp = input.filter { it.isDigit() }.take(6)
        },
        label = { Text("Enter OTP") },
        keyboardOptions = KeyboardOptions(
            keyboardType = KeyboardType.Number,
            autoCorrect = false
        ),
        modifier = Modifier.semantics {
            // Mark as not eligible for autofill
            this[SemanticsProperties.Password] = Unit
        }
    )
}
```

---

## Category 6: Accessibility & Semantics Security

### COMPOSE-029: Accessibility Service Data Exfiltration

- **Severity:** HIGH
- **Category:** Accessibility & Semantics Security
- **Description:** Android accessibility services have broad privileges to read all content displayed on screen, including text from TextFields, content descriptions, and the entire semantics tree. Malicious apps masquerading as accessibility services can capture passwords, account balances, personal messages, and any text content. In Compose, the semantics tree is the accessibility equivalent of the View hierarchy, and all composables that emit text or have content descriptions are accessible. The `accessibilityDataSensitive` attribute (Android 16+) can restrict access from non-trusted accessibility services.
- **Detection Strategy:** Verify that security-sensitive composables use `password` semantics property where appropriate and leverage `accessibilityDataSensitive` on Android 16+.
- **Detection Regex:** `SemanticsProperties\.Password` on sensitive fields; `accessibilityDataSensitive` on sensitive views
- **Impact:** Sensitive data (passwords, financial data, PII) exfiltrated by malicious accessibility services.
- **CWE:** CWE-200 (Exposure of Sensitive Information to an Unauthorized Actor)
- **OWASP Mobile:** M6:2024 - Inadequate Privacy Controls

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Sensitive data readable by any accessibility service
@Composable
fun AccountBalance(balance: Double) {
    Text(
        text = "Balance: $${"%.2f".format(balance)}",
        // Accessibility services can read this value
    )
}

@Composable
fun PasswordInput() {
    var password by remember { mutableStateOf("") }
    BasicTextField(
        value = password,
        onValueChange = { password = it }
        // No password semantics - accessibility services see cleartext
    )
}
```

**Secure Pattern:**

```kotlin
// SECURE: Password semantics applied, sensitive data protected
@Composable
fun AccountBalance(balance: Double) {
    Text(
        text = "Balance: $${"%.2f".format(balance)}",
        modifier = Modifier.semantics {
            // On Android 16+, restrict to trusted accessibility services
            contentDescription = "Account balance available"
            // Don't include the actual amount in content description
        }
    )
}

@Composable
fun PasswordInput() {
    var password by remember { mutableStateOf("") }
    BasicTextField(
        value = password,
        onValueChange = { password = it },
        modifier = Modifier.semantics {
            password()  // Marks as password - accessibility hides content
        },
        visualTransformation = PasswordVisualTransformation()
    )
}
```

---

### COMPOSE-030: contentDescription Sensitive Data Exposure

- **Severity:** MEDIUM
- **Category:** Accessibility & Semantics Security
- **Description:** Developers sometimes include sensitive data in `contentDescription` for accessibility, making it readable by ALL accessibility services (not just screen readers). Content descriptions like "Account ending in 4532, balance $10,543.21" expose both account numbers and balances to any installed accessibility service. The content description should provide functional context without revealing sensitive specifics.
- **Detection Strategy:** Search for `contentDescription` assignments that include dynamic sensitive data (account numbers, balances, names, emails).
- **Detection Regex:** `contentDescription\s*=\s*"[^"]*\$\{[^}]*(balance|account|ssn|email|phone|amount)`
- **Impact:** Sensitive data exposed via accessibility APIs to all installed accessibility services.
- **CWE:** CWE-200 (Exposure of Sensitive Information to an Unauthorized Actor)
- **OWASP Mobile:** M6:2024 - Inadequate Privacy Controls

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Sensitive data in content description
Icon(
    imageVector = Icons.Default.AccountBalance,
    contentDescription = "Account ${account.number}, Balance $${"%.2f".format(account.balance)}"
)

Image(
    painter = rememberAsyncImagePainter(user.profileUrl),
    contentDescription = "Profile photo of ${user.fullName}, ${user.email}"
)
```

**Secure Pattern:**

```kotlin
// SECURE: Functional description without sensitive specifics
Icon(
    imageVector = Icons.Default.AccountBalance,
    contentDescription = "Account balance"  // No specific amount
)

Image(
    painter = rememberAsyncImagePainter(user.profileUrl),
    contentDescription = "User profile photo"  // No PII
)
```

---

### COMPOSE-031: testTag Information Leakage in Production

- **Severity:** MEDIUM
- **Category:** Accessibility & Semantics Security
- **Description:** `Modifier.testTag()` adds metadata to the semantics tree that is intended for UI testing. In production builds, these tags remain accessible through the accessibility framework and UI Automator, revealing internal component names, screen identifiers, and UI structure. This information assists reverse engineering and helps attackers understand the app's navigation flow, identify high-value targets, and craft more effective attacks. Tags like "PaymentConfirmButton" or "AdminSettingsPanel" are particularly revealing.
- **Detection Strategy:** Search for `Modifier.testTag()` usage and verify production builds strip or obfuscate test tags.
- **Detection Regex:** `\.testTag\s*\(\s*"[^"]+"\s*\)`
- **Impact:** Internal app structure exposed, aiding reverse engineering and targeted attacks.
- **CWE:** CWE-215 (Insertion of Sensitive Information Into Debugging Code)
- **OWASP Mobile:** M7:2024 - Insufficient Binary Protections

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Descriptive test tags in production
@Composable
fun AdminPanel() {
    Button(
        onClick = { deleteAllUsers() },
        modifier = Modifier.testTag("AdminDeleteAllUsersButton")
    ) {
        Text("Delete All")
    }

    TextField(
        value = apiKey,
        onValueChange = { apiKey = it },
        modifier = Modifier.testTag("AdminApiKeyInput")
    )
}
```

**Secure Pattern:**

```kotlin
// SECURE: Conditional test tags stripped in production
object TestTags {
    fun tag(name: String): Modifier =
        if (BuildConfig.DEBUG) Modifier.testTag(name) else Modifier
}

@Composable
fun AdminPanel() {
    Button(
        onClick = { deleteAllUsers() },
        modifier = TestTags.tag("admin_delete_btn")
    ) {
        Text("Delete All")
    }

    TextField(
        value = apiKey,
        onValueChange = { apiKey = it },
        modifier = TestTags.tag("admin_api_key")
    )
}
```

---

### COMPOSE-032: Semantics Tree Sensitive Metadata

- **Severity:** LOW
- **Category:** Accessibility & Semantics Security
- **Description:** The Compose semantics tree contains rich metadata about every composable node: text values, state descriptions, custom actions, roles, and hierarchy information. Tools like Layout Inspector, UI Automator, and accessibility services can traverse this tree to extract information about the app's internal state. Custom semantics properties added via `Modifier.semantics {}` can inadvertently expose business logic state, feature flags, user roles, or other sensitive metadata.
- **Detection Strategy:** Search for custom semantics properties that include sensitive state information.
- **Detection Regex:** `Modifier\.semantics\s*\{[^}]*(role|admin|feature|flag|internal)`
- **Impact:** Internal application state, feature flags, and user roles exposed via semantics tree.
- **CWE:** CWE-200 (Exposure of Sensitive Information to an Unauthorized Actor)
- **OWASP Mobile:** M7:2024 - Insufficient Binary Protections

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Internal state exposed in semantics
@Composable
fun FeatureGatedContent(isAdmin: Boolean, featureFlags: Set<String>) {
    Box(
        modifier = Modifier.semantics {
            stateDescription = "admin=$isAdmin, flags=${featureFlags.joinToString()}"
        }
    ) {
        // Content...
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: Only expose necessary accessibility information
@Composable
fun FeatureGatedContent(isAdmin: Boolean, featureFlags: Set<String>) {
    Box(
        modifier = Modifier.semantics {
            // Only describe the UI role, not internal state
            role = Role.Tab
            contentDescription = "Settings panel"
        }
    ) {
        // Content...
    }
}
```

---

## Category 7: Serialization & Deserialization Security

### COMPOSE-033: rememberSaveable Unsafe Custom Saver

- **Severity:** CRITICAL
- **Category:** Serialization & Deserialization Security
- **Description:** `rememberSaveable` persists state across configuration changes and process death by serializing values into a `Bundle`. Custom `Saver` implementations that use `Serializable` or perform JSON deserialization without validation are vulnerable to the same deserialization attacks that affect Android's Parcel/Bundle system. When an app is restored after process death, the Android system restores the saved Bundle which may have been tampered with on a rooted device. Any deserialized object should be treated as untrusted input.
- **Detection Strategy:** Search for custom `Saver` implementations that use `Serializable`, JSON deserialization, or `Parcelable` without type validation.
- **Detection Regex:** `Saver\s*\(\s*save\s*=|listSaver\s*\(|mapSaver\s*\(` with `Serializable|Json\.decodeFromString|getParcelable`
- **Impact:** Arbitrary code execution, privilege escalation, data corruption through crafted serialized payloads.
- **CWE:** CWE-502 (Deserialization of Untrusted Data)
- **OWASP Mobile:** M4:2024 - Insufficient Input/Output Validation

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Custom Saver with unsafe deserialization
data class UserSession(
    val userId: String,
    val role: String,
    val permissions: List<String>
) : Serializable

val UserSessionSaver = Saver<UserSession, Any>(
    save = { session ->
        // Serializable objects are vulnerable to deserialization attacks
        session as Serializable
    },
    restore = { saved ->
        // Unsafe: Deserializes without type validation
        @Suppress("UNCHECKED_CAST")
        saved as UserSession
    }
)

@Composable
fun SessionScreen() {
    var session by rememberSaveable(stateSaver = UserSessionSaver) {
        mutableStateOf(UserSession("user1", "admin", listOf("all")))
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: Custom Saver with explicit field serialization and validation
data class UserSession(
    val userId: String,
    val role: String,
    val permissions: List<String>
)

val UserSessionSaver = listSaver<UserSession, String>(
    save = { session ->
        listOf(session.userId, session.role) + session.permissions
    },
    restore = { list ->
        require(list.size >= 2) { "Invalid saved state" }
        val userId = list[0]
        val role = list[1]
        val permissions = list.drop(2)

        // Validate restored values
        require(userId.matches(Regex("^[a-zA-Z0-9-]{1,36}$"))) { "Invalid userId" }
        require(role in setOf("user", "admin", "moderator")) { "Invalid role" }
        require(permissions.all { it in VALID_PERMISSIONS }) { "Invalid permission" }

        UserSession(userId, role, permissions)
    }
)
```

---

### COMPOSE-034: Parcelable Navigation Argument Deserialization

- **Severity:** HIGH
- **Category:** Serialization & Deserialization Security
- **Description:** Navigation arguments passed as `Parcelable` or `Serializable` objects undergo automatic deserialization when retrieved from the back stack Bundle. The deprecated `Bundle.getParcelable(key)` method (pre-Android 13) does not validate the type of the deserialized object, allowing type confusion attacks. Even with the type-safe `Bundle.getParcelable(key, Class)` method (Android 13+), the Parcelable data itself may contain tampered values if originating from an external intent.
- **Detection Strategy:** Search for deprecated `getParcelable()` calls without class parameter and for navigation arguments of Parcelable type from external sources.
- **Detection Regex:** `getParcelable\s*\(\s*"[^"]+"\s*\)` (deprecated, no class parameter)
- **Impact:** Type confusion, data corruption, potential code execution through crafted Parcelable payloads.
- **CWE:** CWE-502 (Deserialization of Untrusted Data)
- **OWASP Mobile:** M4:2024 - Insufficient Input/Output Validation

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Deprecated getParcelable without type safety
composable("details/{data}") { backStackEntry ->
    @Suppress("DEPRECATION")
    val data = backStackEntry.arguments?.getParcelable<ItemData>("data")
    // No validation of deserialized data
    data?.let { ItemDetailsScreen(it) }
}
```

**Secure Pattern:**

```kotlin
// SECURE: Type-safe deserialization with validation
composable("details/{data}") { backStackEntry ->
    val data = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
        backStackEntry.arguments?.getParcelable("data", ItemData::class.java)
    } else {
        @Suppress("DEPRECATION")
        backStackEntry.arguments?.getParcelable("data")
    }

    // Validate all fields of deserialized object
    data?.let { item ->
        require(item.id.matches(Regex("^[a-zA-Z0-9-]+$"))) { "Invalid item ID" }
        require(item.price >= 0) { "Invalid price" }
        ItemDetailsScreen(item)
    } ?: ErrorScreen("Invalid data")
}
```

---

### COMPOSE-035: Bundle Injection via Intent Extras

- **Severity:** HIGH
- **Category:** Serialization & Deserialization Security
- **Description:** When an Activity receives an Intent, all extras are deserialized as a Bundle. An attacker can send an Intent with additional, unexpected extra parameters that are automatically deserialized. If the app's composables read values from the Activity's intent extras, they may process attacker-controlled data. The key risk is that `intent.extras` deserializes ALL bundled objects, not just the ones the app expects, which can trigger deserialization of malicious objects.
- **Detection Strategy:** Search for `intent.extras` or `intent.getStringExtra()` usage in Activities hosting Compose content. Verify that extras are validated and unexpected keys are rejected.
- **Detection Regex:** `intent\.(extras|get\w+Extra)\s*[(\[]`
- **Impact:** Processing attacker-controlled data, triggering deserialization vulnerabilities, bypassing input validation.
- **CWE:** CWE-502 (Deserialization of Untrusted Data)
- **OWASP Mobile:** M4:2024 - Insufficient Input/Output Validation

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Directly using intent extras without validation
class DetailActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            val itemId = intent.getStringExtra("itemId") ?: ""
            val action = intent.getStringExtra("action") ?: ""
            // Attacker controls both values via crafted intent
            DetailScreen(itemId = itemId, action = action)
        }
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: Validate intent source and extras
class DetailActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Verify intent comes from expected source
        val callingPackage = callingActivity?.packageName
        val isTrustedSource = callingPackage == packageName

        setContent {
            val itemId = intent.getStringExtra("itemId")
                ?.takeIf { it.matches(Regex("^[a-zA-Z0-9-]{1,36}$")) }
                ?: run {
                    ErrorScreen("Invalid item")
                    return@setContent
                }

            val action = intent.getStringExtra("action")
                ?.takeIf { it in setOf("view", "edit") }
                ?: "view"

            DetailScreen(
                itemId = itemId,
                action = action,
                isExternalLaunch = !isTrustedSource
            )
        }
    }
}
```

---

### COMPOSE-036: State Restoration Tampering After Process Death

- **Severity:** MEDIUM
- **Category:** Serialization & Deserialization Security
- **Description:** When Android kills an app's process to reclaim memory, it saves UI state via `onSaveInstanceState` and restores it when the user returns. This saved state, stored in Bundles, can be examined and modified on rooted devices. State saved via `rememberSaveable` (authentication status, user roles, feature gates) is vulnerable to tampering between save and restore. An attacker can modify the saved Bundle on disk to change the restored state.
- **Detection Strategy:** Search for `rememberSaveable` storing security-relevant state (auth flags, roles, permissions) and verify that restored values are revalidated against a trusted source.
- **Detection Regex:** `rememberSaveable\s*\{[^}]*(isAuth|isAdmin|role|permission|logged)`
- **Impact:** Authentication bypass, role escalation, feature gate bypass via tampered saved state.
- **CWE:** CWE-472 (External Control of Assumed-Immutable Web Parameter)
- **OWASP Mobile:** M3:2024 - Insecure Authentication/Authorization

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Auth state persisted in rememberSaveable and trusted on restore
@Composable
fun AppRoot() {
    var isAuthenticated by rememberSaveable { mutableStateOf(false) }
    var userRole by rememberSaveable { mutableStateOf("user") }

    if (isAuthenticated) {
        // On restore, tampered state could set isAuthenticated=true, userRole="admin"
        MainApp(userRole = userRole)
    } else {
        LoginScreen(onLogin = { role ->
            isAuthenticated = true
            userRole = role
        })
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: Revalidate auth state from trusted source on restore
@Composable
fun AppRoot(authViewModel: AuthViewModel = hiltViewModel()) {
    // Auth state comes from ViewModel backed by encrypted storage + server validation
    val authState by authViewModel.authState.collectAsStateWithLifecycle()

    LaunchedEffect(Unit) {
        // Revalidate session on every cold start / process restore
        authViewModel.validateSession()
    }

    when (authState) {
        is AuthState.Authenticated -> MainApp(
            userRole = (authState as AuthState.Authenticated).role
        )
        is AuthState.Validating -> SplashScreen()
        else -> LoginScreen()
    }
}
```

---

## Category 8: Image & Media Security

### COMPOSE-037: Image Loader URL Injection

- **Severity:** HIGH
- **Category:** Image & Media Security
- **Description:** Image loading libraries (Coil, Glide) used with Compose accept URL strings to load remote images. If these URLs come from untrusted sources (navigation arguments, deep links, server responses), an attacker can inject malicious URLs. This can lead to SSRF (if the app has internal network access), tracking pixel injection (loading attacker-controlled URLs that log access), or loading inappropriate/offensive content. Coil and Glide do not validate URL domains by default.
- **Detection Strategy:** Search for `AsyncImage`, `rememberAsyncImagePainter`, or `SubcomposeAsyncImage` where the model/url comes from user input or navigation arguments.
- **Detection Regex:** `(AsyncImage|rememberAsyncImagePainter|SubcomposeAsyncImage)\s*\([^)]*model\s*=\s*\b(url|imageUrl|param)`
- **Impact:** SSRF through internal network image loading, tracking pixel injection, inappropriate content display.
- **CWE:** CWE-918 (Server-Side Request Forgery)
- **OWASP Mobile:** M4:2024 - Insufficient Input/Output Validation

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Image URL from navigation argument loaded without validation
composable("profile/{imageUrl}") { backStackEntry ->
    val imageUrl = backStackEntry.arguments?.getString("imageUrl") ?: ""

    AsyncImage(
        model = imageUrl,  // Attacker controls URL via deep link
        contentDescription = "Profile photo"
    )
}
```

**Secure Pattern:**

```kotlin
// SECURE: URL validated against allowlist before loading
composable("profile/{imageUrl}") { backStackEntry ->
    val imageUrl = backStackEntry.arguments?.getString("imageUrl") ?: ""
    val allowedHosts = setOf("cdn.traillens.com", "images.traillens.com")

    val validUrl = remember(imageUrl) {
        val uri = Uri.parse(imageUrl)
        if (uri.scheme == "https" && uri.host in allowedHosts) imageUrl else null
    }

    AsyncImage(
        model = validUrl ?: R.drawable.default_profile,
        contentDescription = "Profile photo"
    )
}
```

---

### COMPOSE-038: SVG/Vector Parsing Denial of Service

- **Severity:** MEDIUM
- **Category:** Image & Media Security
- **Description:** SVG files and Android Vector Drawables are XML-based formats that can contain deeply nested elements, recursive references, or extremely large path data. Parsing a crafted SVG with Coil's `SvgDecoder` or rendering a malicious VectorDrawable can cause excessive CPU usage, memory exhaustion, or application freeze. This is an XML bomb / billion laughs attack adapted for image formats.
- **Detection Strategy:** Search for SVG loading from untrusted sources. Verify that SVG loading includes size limits and timeout constraints.
- **Detection Regex:** `SvgDecoder|\.svg|image/svg` in image loading configurations
- **Impact:** Application freeze, denial of service, memory exhaustion.
- **CWE:** CWE-400 (Uncontrolled Resource Consumption)
- **OWASP Mobile:** M4:2024 - Insufficient Input/Output Validation

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: SVG loaded from untrusted source without size limits
val imageLoader = ImageLoader.Builder(context)
    .components {
        add(SvgDecoder.Factory())  // Accepts any SVG, no size limit
    }
    .build()

AsyncImage(
    model = untrustedSvgUrl,
    imageLoader = imageLoader,
    contentDescription = "User uploaded image"
)
```

**Secure Pattern:**

```kotlin
// SECURE: SVG loading with size constraints and timeout
val imageLoader = ImageLoader.Builder(context)
    .components {
        add(SvgDecoder.Factory())
    }
    .memoryCachePolicy(CachePolicy.ENABLED)
    .diskCachePolicy(CachePolicy.ENABLED)
    .respectCacheHeaders(true)
    .build()

AsyncImage(
    model = ImageRequest.Builder(context)
        .data(untrustedSvgUrl)
        .size(1024, 1024)  // Limit decoded size
        .memoryCacheKey(untrustedSvgUrl)
        .build(),
    imageLoader = imageLoader,
    contentDescription = "User uploaded image"
)
```

---

### COMPOSE-039: Bitmap Memory Exhaustion

- **Severity:** MEDIUM
- **Category:** Image & Media Security
- **Description:** Loading images without downsampling can exhaust available memory. A 4000x4000 RGBA bitmap requires approximately 64MB of memory. If an attacker can cause the app to load multiple high-resolution images simultaneously (e.g., through crafted deep links or manipulated API responses), it can trigger `OutOfMemoryError` and crash the app. In Compose's `LazyColumn`, rapid scrolling through a list of large images can temporarily load many full-resolution images before recycling kicks in.
- **Detection Strategy:** Search for image loading without explicit size constraints or downsampling configuration. Check `LazyColumn` items that load remote images without size limits.
- **Detection Regex:** `(AsyncImage|Image)\s*\([^)]*(?!\.size\(|\.resize\(|coil)` in LazyColumn items
- **Impact:** Application crash via OutOfMemoryError, denial of service.
- **CWE:** CWE-400 (Uncontrolled Resource Consumption)
- **OWASP Mobile:** M4:2024 - Insufficient Input/Output Validation

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Full-resolution images in LazyColumn
LazyColumn {
    items(imageUrls) { url ->
        AsyncImage(
            model = url,  // Loads full resolution, no size limit
            contentDescription = null,
            modifier = Modifier.fillMaxWidth()
        )
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: Explicit size constraints and memory-aware loading
LazyColumn {
    items(imageUrls, key = { it }) { url ->
        AsyncImage(
            model = ImageRequest.Builder(LocalContext.current)
                .data(url)
                .size(800, 600)  // Downsample to display size
                .crossfade(true)
                .memoryCachePolicy(CachePolicy.ENABLED)
                .build(),
            contentDescription = null,
            modifier = Modifier
                .fillMaxWidth()
                .height(200.dp)
        )
    }
}
```

---

## Category 9: WebView & Interop Security

### COMPOSE-040: WebView JavaScript Interface Exploitation

- **Severity:** CRITICAL
- **Category:** WebView & Interop Security
- **Description:** When embedding `WebView` in Compose via `AndroidView`, enabling JavaScript and adding `@JavascriptInterface` methods creates a bridge between web content and native Android code. If the WebView loads untrusted content (user-generated HTML, third-party websites), malicious JavaScript can invoke these native methods. The `addJavascriptInterface()` method injects the Java object into ALL frames including iframes, making it susceptible to injection by malicious third parties.
- **Detection Strategy:** Search for `AndroidView` creating `WebView` with `addJavascriptInterface` and verify the loaded URLs are from trusted sources only.
- **Detection Regex:** `addJavascriptInterface\s*\(` combined with `WebView` in AndroidView
- **Impact:** Arbitrary code execution in the app's context, data theft, unauthorized API calls via native bridge.
- **CWE:** CWE-749 (Exposed Dangerous Method or Function)
- **OWASP Mobile:** M4:2024 - Insufficient Input/Output Validation

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: JavaScript interface exposed to untrusted content
@Composable
fun WebContent(url: String) {
    AndroidView(factory = { context ->
        WebView(context).apply {
            settings.javaScriptEnabled = true
            addJavascriptInterface(object {
                @JavascriptInterface
                fun getAuthToken(): String = authManager.getToken()

                @JavascriptInterface
                fun executeAction(action: String) = actionExecutor.run(action)
            }, "Android")
            loadUrl(url)  // url could be attacker-controlled
        }
    })
}
```

**Secure Pattern:**

```kotlin
// SECURE: Restricted JavaScript interface with URL validation
@Composable
fun WebContent(url: String) {
    val allowedDomains = listOf("traillens.com", "cdn.traillens.com")
    val parsedUri = Uri.parse(url)

    if (parsedUri.scheme != "https" || parsedUri.host !in allowedDomains) {
        ErrorScreen("Untrusted URL")
        return
    }

    AndroidView(factory = { context ->
        WebView(context).apply {
            settings.apply {
                javaScriptEnabled = true
                allowFileAccess = false
                allowFileAccessFromFileURLs = false
                allowUniversalAccessFromFileURLs = false
                mixedContentMode = WebSettings.MIXED_CONTENT_NEVER_ALLOW
            }
            webViewClient = object : WebViewClient() {
                override fun shouldOverrideUrlLoading(
                    view: WebView, request: WebResourceRequest
                ): Boolean {
                    return request.url.host !in allowedDomains
                }
            }
            // Only add interface if loading trusted content
            // Minimize exposed methods
            loadUrl(url)
        }
    })
}
```

---

### COMPOSE-041: WebView Unsafe File Access

- **Severity:** HIGH
- **Category:** WebView & Interop Security
- **Description:** WebView settings like `allowFileAccess`, `allowFileAccessFromFileURLs`, and `allowUniversalAccessFromFileURLs` control access to the local filesystem from web content. When enabled, JavaScript running in the WebView can read local files, including the app's private data directory containing databases, shared preferences, and cached credentials. These settings are often left at default values (some are `true` by default on older API levels).
- **Detection Strategy:** Search for WebView creation in `AndroidView` and verify file access settings are explicitly disabled.
- **Detection Regex:** `WebView\s*\([^)]*\)\.apply\s*\{` without `allowFileAccess\s*=\s*false`
- **Impact:** Local file exfiltration, access to app's private data, credential theft.
- **CWE:** CWE-200 (Exposure of Sensitive Information to an Unauthorized Actor)
- **OWASP Mobile:** M9:2024 - Insecure Data Storage

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Default WebView settings allow file access
AndroidView(factory = { context ->
    WebView(context).apply {
        settings.javaScriptEnabled = true
        // File access settings left at defaults
        loadUrl(url)
    }
})
```

**Secure Pattern:**

```kotlin
// SECURE: Explicitly disable all file access
AndroidView(factory = { context ->
    WebView(context).apply {
        settings.apply {
            javaScriptEnabled = true
            allowFileAccess = false
            allowFileAccessFromFileURLs = false
            allowUniversalAccessFromFileURLs = false
            allowContentAccess = false
            mixedContentMode = WebSettings.MIXED_CONTENT_NEVER_ALLOW
            domStorageEnabled = false  // Unless specifically needed
        }
        loadUrl(url)
    }
})
```

---

### COMPOSE-042: AndroidView Interop Lifecycle Mismatch

- **Severity:** HIGH
- **Category:** WebView & Interop Security
- **Description:** When using `AndroidView` to embed traditional Views in Compose, the View's lifecycle does not automatically align with the composable's lifecycle. A `WebView` or other complex View created in `AndroidView` may continue executing JavaScript, making network requests, or processing events after the composable leaves the composition. The `update` lambda is called on recomposition but `onRelease` (added in Compose 1.6) must be used for cleanup. Without proper cleanup, background WebView processes can continue with stale credentials or expired sessions.
- **Detection Strategy:** Search for `AndroidView` with `WebView` and verify `onRelease` or `DisposableEffect` cleanup is implemented.
- **Detection Regex:** `AndroidView\s*\(\s*factory\s*=\s*\{[^}]*WebView` without `onRelease` or disposal logic
- **Impact:** Continued execution with stale credentials, resource leaks, background data processing.
- **CWE:** CWE-404 (Improper Resource Shutdown or Release)
- **OWASP Mobile:** M8:2024 - Security Misconfiguration

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: No cleanup when composable leaves composition
@Composable
fun WebContent(url: String) {
    AndroidView(
        factory = { context ->
            WebView(context).apply {
                settings.javaScriptEnabled = true
                loadUrl(url)
            }
        }
        // Missing onRelease - WebView continues running
    )
}
```

**Secure Pattern:**

```kotlin
// SECURE: Proper lifecycle cleanup with onRelease
@Composable
fun WebContent(url: String) {
    AndroidView(
        factory = { context ->
            WebView(context).apply {
                settings.javaScriptEnabled = true
                loadUrl(url)
            }
        },
        onRelease = { webView ->
            webView.stopLoading()
            webView.loadUrl("about:blank")
            webView.clearHistory()
            webView.clearCache(true)
            webView.destroy()
        }
    )
}
```

---

### COMPOSE-043: Cross-App Scripting via WebView

- **Severity:** HIGH
- **Category:** WebView & Interop Security
- **Description:** When a Compose app loads URLs in a WebView based on external input (Intent data, deep links, navigation arguments), attackers can inject `javascript:` URIs or craft URLs with XSS payloads. If `shouldOverrideUrlLoading()` does not validate URLs and `evaluateJavascript()` accepts unsanitized input, the injected JavaScript executes in the WebView's security context, with access to any JavaScript interfaces, local storage, and cookies belonging to the loaded domain.
- **Detection Strategy:** Search for `loadUrl()`, `evaluateJavascript()`, or `shouldOverrideUrlLoading()` handling URLs from external sources.
- **Detection Regex:** `loadUrl\s*\(\s*\b(url|intent|argument|param)\b` or `evaluateJavascript\s*\(\s*\$\{`
- **Impact:** JavaScript execution in the app's WebView context, session theft, data exfiltration.
- **CWE:** CWE-79 (Cross-site Scripting)
- **OWASP Mobile:** M4:2024 - Insufficient Input/Output Validation

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Unsanitized URL loaded in WebView
@Composable
fun WebViewer(viewModel: WebViewModel = hiltViewModel()) {
    val url by viewModel.url.collectAsStateWithLifecycle()

    AndroidView(factory = { context ->
        WebView(context).apply {
            settings.javaScriptEnabled = true
            // url could be "javascript:alert(document.cookie)"
            loadUrl(url)
        }
    })
}
```

**Secure Pattern:**

```kotlin
// SECURE: URL validation before loading
@Composable
fun WebViewer(viewModel: WebViewModel = hiltViewModel()) {
    val url by viewModel.url.collectAsStateWithLifecycle()

    val safeUrl = remember(url) {
        val uri = Uri.parse(url)
        when {
            uri.scheme !in listOf("https", "http") -> null  // Blocks javascript:
            uri.host == null -> null
            uri.host !in ALLOWED_DOMAINS -> null
            else -> url
        }
    }

    if (safeUrl != null) {
        AndroidView(factory = { context ->
            WebView(context).apply {
                settings.javaScriptEnabled = true
                webViewClient = object : WebViewClient() {
                    override fun shouldOverrideUrlLoading(
                        view: WebView, request: WebResourceRequest
                    ): Boolean {
                        val host = request.url.host
                        return host == null || host !in ALLOWED_DOMAINS
                    }
                }
                loadUrl(safeUrl)
            }
        })
    } else {
        ErrorScreen("Invalid URL")
    }
}
```

---

## Category 10: Component & Intent Security

### COMPOSE-044: Exported Activity Without Validation

- **Severity:** HIGH
- **Category:** Component & Intent Security
- **Description:** Activities hosting Compose content that are declared as `android:exported="true"` in the manifest can be launched by any application on the device. If the Activity reads Intent data to configure its Compose UI (e.g., displaying specific content, triggering actions), any external app can launch it with arbitrary Intent data. This is especially dangerous when combined with Compose Navigation's implicit deep links, as the entire navigation graph becomes externally accessible.
- **Detection Strategy:** Search for exported activities in the manifest and verify they validate incoming Intent data before passing it to composables.
- **Detection Regex:** `android:exported="true"` for activities other than the launcher
- **Impact:** Unauthorized access to app functionality, data injection, triggering unintended actions.
- **CWE:** CWE-926 (Improper Export of Android Application Components)
- **OWASP Mobile:** M8:2024 - Security Misconfiguration

**Vulnerable Pattern:**

```xml
<!-- VULNERABLE: Non-launcher activity exported without need -->
<activity
    android:name=".DetailActivity"
    android:exported="true" />

<activity
    android:name=".AdminActivity"
    android:exported="true" />
```

**Secure Pattern:**

```xml
<!-- SECURE: Only export what's necessary, with permission protection -->
<activity
    android:name=".DetailActivity"
    android:exported="false" />

<activity
    android:name=".AdminActivity"
    android:exported="false" />

<!-- If export is required, protect with permission -->
<activity
    android:name=".ShareReceiverActivity"
    android:exported="true"
    android:permission="com.traillens.SHARE_PERMISSION">
    <intent-filter>
        <action android:name="android.intent.action.SEND" />
        <data android:mimeType="image/*" />
    </intent-filter>
</activity>
```

---

### COMPOSE-045: Intent Redirection Vulnerability

- **Severity:** HIGH
- **Category:** Component & Intent Security
- **Description:** Intent redirection occurs when an app extracts an Intent from incoming extras and uses it to start another component via `startActivity()` or `startService()`. If the extracted Intent is not validated, an attacker can redirect it to access the app's non-exported components, gaining access to internal activities, content providers (with URI permissions), and services. In Compose apps, this often occurs when deep link handlers or notification handlers extract and forward Intents.
- **Detection Strategy:** Search for `startActivity()` calls that use Intents extracted from other Intents' extras. Also check for `PendingIntent` creation with mutable flags.
- **Detection Regex:** `intent\.getParcelableExtra\s*\([^)]*\)\s*.*startActivity|startService`
- **Impact:** Access to non-exported components, content provider data leak via URI permissions, privilege escalation.
- **CWE:** CWE-940 (Improper Verification of Source of a Communication Channel)
- **OWASP Mobile:** M3:2024 - Insecure Authentication/Authorization

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Intent redirection without validation
class RouterActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Extract Intent from extras and launch it blindly
        val targetIntent = intent.getParcelableExtra<Intent>("target_intent")
        if (targetIntent != null) {
            startActivity(targetIntent)  // Attacker controls destination
        }
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: Validate intent before redirection
class RouterActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val targetIntent = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            intent.getParcelableExtra("target_intent", Intent::class.java)
        } else {
            @Suppress("DEPRECATION")
            intent.getParcelableExtra("target_intent")
        }

        if (targetIntent != null) {
            // Validate the target component belongs to this app
            val targetComponent = targetIntent.component
            if (targetComponent != null && targetComponent.packageName == packageName) {
                // Strip dangerous flags
                targetIntent.removeFlags(
                    Intent.FLAG_GRANT_READ_URI_PERMISSION or
                    Intent.FLAG_GRANT_WRITE_URI_PERMISSION or
                    Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION or
                    Intent.FLAG_GRANT_PREFIX_URI_PERMISSION
                )
                startActivity(targetIntent)
            }
        }
        finish()
    }
}
```

---

### COMPOSE-046: Content Provider URI Permission Leak

- **Severity:** HIGH
- **Category:** Component & Intent Security
- **Description:** When an attacker sends a crafted Intent with `FLAG_GRANT_READ_URI_PERMISSION` or `FLAG_GRANT_WRITE_URI_PERMISSION` pointing to the app's `ContentProvider` or `FileProvider`, the receiving component can inadvertently grant the attacker persistent access to the app's private files. In Compose apps using `FileProvider` for image sharing or file download, improper URI permission handling can expose the app's entire `files/` directory or specific sensitive files.
- **Detection Strategy:** Search for `FileProvider` configuration in manifest and `Intent.FLAG_GRANT_*` usage. Verify that content URIs are scoped to specific paths and permissions are temporary.
- **Detection Regex:** `FLAG_GRANT_(READ|WRITE)_URI_PERMISSION|FLAG_GRANT_PERSISTABLE_URI_PERMISSION`
- **Impact:** Persistent read/write access to app's private files, data exfiltration, data manipulation.
- **CWE:** CWE-281 (Improper Preservation of Permissions)
- **OWASP Mobile:** M9:2024 - Insecure Data Storage

**Vulnerable Pattern:**

```xml
<!-- VULNERABLE: FileProvider with overly broad path configuration -->
<provider
    android:name="androidx.core.content.FileProvider"
    android:authorities="${applicationId}.fileprovider"
    android:exported="false"
    android:grantUriPermissions="true">
    <meta-data
        android:name="android.support.FILE_PROVIDER_PATHS"
        android:resource="@xml/file_paths" />
</provider>

<!-- file_paths.xml - VULNERABLE: entire files directory exposed -->
<paths>
    <files-path name="all_files" path="." />
</paths>
```

**Secure Pattern:**

```xml
<!-- SECURE: FileProvider with narrowly scoped paths -->
<provider
    android:name="androidx.core.content.FileProvider"
    android:authorities="${applicationId}.fileprovider"
    android:exported="false"
    android:grantUriPermissions="true">
    <meta-data
        android:name="android.support.FILE_PROVIDER_PATHS"
        android:resource="@xml/file_paths" />
</provider>

<!-- file_paths.xml - SECURE: only specific directories exposed -->
<paths>
    <cache-path name="shared_images" path="shared_images/" />
    <!-- No access to files/, databases/, shared_prefs/ -->
</paths>
```

---

### COMPOSE-047: Implicit Intent Interception

- **Severity:** MEDIUM
- **Category:** Component & Intent Security
- **Description:** When a Compose app sends implicit intents (intents without a specific target component), any app that declares a matching intent filter can intercept them. If the Intent contains sensitive data (auth tokens, user IDs, file URIs), the intercepting app gains access to this data. This is particularly relevant in Compose apps that use `Intent.ACTION_SEND` for sharing, `Intent.ACTION_VIEW` for opening URLs, or custom implicit intents for inter-app communication.
- **Detection Strategy:** Search for `Intent()` creation without explicit component specification that includes sensitive data in extras or data URI.
- **Detection Regex:** `Intent\s*\(\s*(Intent\.ACTION_|"[^"]+"\s*)\)` without `setComponent` or `setPackage`
- **Impact:** Sensitive data intercepted by malicious app, credential theft, session hijacking.
- **CWE:** CWE-927 (Use of Implicit Intent for Sensitive Communication)
- **OWASP Mobile:** M5:2024 - Insecure Communication

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Sensitive data in implicit intent
@Composable
fun ShareButton(userToken: String, content: String) {
    Button(onClick = {
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_TEXT, content)
            putExtra("auth_token", userToken)  // Sensitive data in implicit intent
        }
        context.startActivity(intent)
    }) {
        Text("Share")
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: No sensitive data in implicit intents
@Composable
fun ShareButton(content: String) {
    val context = LocalContext.current
    Button(onClick = {
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_TEXT, content)
            // Never include auth tokens or sensitive data
        }
        // Use chooser to let user pick the target app
        val chooser = Intent.createChooser(intent, "Share via")
        context.startActivity(chooser)
    }) {
        Text("Share")
    }
}
```

---

## Category 11: Build & Obfuscation Security

### COMPOSE-048: @Preview Data in Production APK

- **Severity:** HIGH
- **Category:** Build & Obfuscation Security
- **Description:** `@Preview` composable functions and their `@PreviewParameter` providers are compiled into the production APK unless explicitly stripped by R8/ProGuard. Preview functions often contain hardcoded sample data (fake user names, test API endpoints, mock credentials, feature flag overrides) that can be extracted through reverse engineering. The preview functions themselves may reveal internal component names, state structures, and UI architecture.
- **Detection Strategy:** Verify that ProGuard/R8 rules include `-checkdiscard` for Preview annotations. Check for sensitive sample data in Preview functions.
- **Detection Regex:** `@Preview` functions containing hardcoded data like `"admin"`, `"password"`, API URLs, or `"test"`
- **Impact:** Internal app architecture exposed, sample/test credentials discoverable, debug data in production.
- **CWE:** CWE-215 (Insertion of Sensitive Information Into Debugging Code)
- **OWASP Mobile:** M7:2024 - Insufficient Binary Protections

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Preview with sensitive sample data, compiled into production APK
@Preview
@Composable
fun AdminPanelPreview() {
    AdminPanel(
        apiKey = "sk-test-abc123def456",
        adminEmail = "admin@traillens.com",
        debugEndpoint = "https://staging-api.traillens.com/v1"
    )
}

@Preview
@Composable
fun LoginPreview() {
    LoginScreen(
        initialEmail = "test@traillens.com",
        initialPassword = "TestPassword123!"
    )
}
```

**Secure Pattern:**

```kotlin
// SECURE: Strip previews from production and use safe sample data

// proguard-rules.pro:
// -checkdiscard class * {
//     @androidx.compose.ui.tooling.preview.Preview <methods>;
// }

@Preview
@Composable
fun AdminPanelPreview() {
    AdminPanel(
        apiKey = "PREVIEW_PLACEHOLDER",
        adminEmail = "preview@example.com",
        debugEndpoint = "https://example.com/api"
    )
}

// Additionally, verify R8 strips preview code:
// ./gradlew assembleRelease
// Check APK does not contain @Preview methods
```

---

### COMPOSE-049: Debug Logging in Production Build

- **Severity:** MEDIUM
- **Category:** Build & Obfuscation Security
- **Description:** `Log.d()`, `Log.v()`, `println()`, and `Timber.d()` calls that log sensitive data (auth tokens, user data, API responses, navigation state) are often left in production builds. On Android, any app with `READ_LOGS` permission (or via `adb logcat` on debuggable devices) can read Logcat output. Sensitive information logged during Compose state changes, navigation events, or API calls is accessible to other applications.
- **Detection Strategy:** Search for logging statements that include sensitive variable names. Verify R8 rules strip debug/verbose log calls in release builds.
- **Detection Regex:** `Log\.(d|v|i)\s*\([^)]*\b(token|password|secret|key|credential|session|cookie)\b`
- **Impact:** Sensitive data exposed via Logcat, accessible to other apps or via USB debugging.
- **CWE:** CWE-532 (Insertion of Sensitive Information into Log File)
- **OWASP Mobile:** M9:2024 - Insecure Data Storage

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Sensitive data logged in production
class AuthViewModel : ViewModel() {
    fun login(email: String, password: String) {
        Log.d("Auth", "Login attempt: email=$email, password=$password")
        viewModelScope.launch {
            val token = authRepository.authenticate(email, password)
            Log.d("Auth", "Token received: $token")
        }
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: Conditional logging stripped in release builds
class AuthViewModel : ViewModel() {
    fun login(email: String, password: String) {
        if (BuildConfig.DEBUG) {
            Log.d("Auth", "Login attempt for: ${email.take(3)}***")
        }
        viewModelScope.launch {
            val token = authRepository.authenticate(email, password)
            // Never log tokens, even in debug
        }
    }
}

// R8/ProGuard rules to strip Log.d and Log.v:
// -assumenosideeffects class android.util.Log {
//     public static int d(...);
//     public static int v(...);
// }
```

---

### COMPOSE-050: Missing R8/ProGuard Compose Rules

- **Severity:** MEDIUM
- **Category:** Build & Obfuscation Security
- **Description:** Jetpack Compose requires specific R8/ProGuard rules to function correctly while also ensuring proper code shrinking and obfuscation. Missing rules can cause runtime crashes in release builds, while overly broad keep rules prevent obfuscation of sensitive class names, method names, and string constants. Without proper configuration, Compose's runtime reflection on composable functions and state objects can fail, or conversely, internal class structures remain fully readable after decompilation.
- **Detection Strategy:** Verify `proguard-rules.pro` contains Compose-specific rules and does not use overly broad keep directives like `-keep class ** { *; }`.
- **Detection Regex:** `-keep class \*\*\s*\{\s*\*;\s*\}` (overly broad keep rules)
- **Impact:** Release build crashes or insufficient obfuscation exposing internal app structure.
- **CWE:** CWE-693 (Protection Mechanism Failure)
- **OWASP Mobile:** M7:2024 - Insufficient Binary Protections

**Vulnerable Pattern:**

```proguard
# VULNERABLE: No Compose rules or overly broad keep rules
-keep class ** { *; }
# This keeps ALL classes - no obfuscation at all
```

**Secure Pattern:**

```proguard
# SECURE: Targeted Compose rules with proper obfuscation

# Keep Compose runtime
-keepclasseswithmembers class * {
    @androidx.compose.runtime.Composable <methods>;
}

# Strip Preview annotations from release builds
-checkdiscard class * {
    @androidx.compose.ui.tooling.preview.Preview <methods>;
}

# Keep Compose Navigation serializable routes
-keepclassmembers class * implements kotlinx.serialization.KSerializer {
    *** INSTANCE;
}

# Strip debug logging
-assumenosideeffects class android.util.Log {
    public static int d(...);
    public static int v(...);
}
```

---

## Category 12: Performance & DoS Security

### COMPOSE-051: Infinite Recomposition Loop

- **Severity:** MEDIUM
- **Category:** Performance & DoS Security
- **Description:** An infinite recomposition loop occurs when a composable modifies state that triggers its own recomposition, creating an endless cycle. This causes 100% CPU utilization, UI freeze, battery drain, and potential ANR (Application Not Responding) dialog. While this is typically a bug, it can be triggered intentionally by an attacker who can influence input parameters (via deep links or navigation arguments) to create conditions that trigger the loop.
- **Detection Strategy:** Search for state modifications inside composable functions (not in event handlers or effects). Look for `mutableStateOf` writes that occur during composition.
- **Detection Regex:** `@Composable[^{]*\{[^}]*\.value\s*=` (state write during composition, outside of callbacks)
- **Impact:** Application freeze, denial of service, battery drain.
- **CWE:** CWE-835 (Loop with Unreachable Exit Condition)
- **OWASP Mobile:** M4:2024 - Insufficient Input/Output Validation

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: State modification during composition causes infinite loop
@Composable
fun BrokenCounter() {
    var count by remember { mutableStateOf(0) }
    count++  // Modifies state during composition -> triggers recomposition -> infinite loop

    Text("Count: $count")
}

// VULNERABLE: Side effect without key creates infinite loop
@Composable
fun BrokenFetcher(data: String) {
    var result by remember { mutableStateOf("") }
    // New object created each recomposition -> LaunchedEffect restarts -> state changes -> loop
    LaunchedEffect(Any()) {
        result = fetchData(data)
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: State modification only in event handlers or effects
@Composable
fun WorkingCounter() {
    var count by remember { mutableStateOf(0) }

    Button(onClick = { count++ }) {  // State change in event handler
        Text("Count: $count")
    }
}

// SECURE: Stable key prevents unnecessary restarts
@Composable
fun WorkingFetcher(data: String) {
    var result by remember { mutableStateOf("") }
    LaunchedEffect(data) {  // Stable key - only restarts when data changes
        result = fetchData(data)
    }
}
```

---

### COMPOSE-052: Unbounded LazyColumn Memory Exhaustion

- **Severity:** MEDIUM
- **Category:** Performance & DoS Security
- **Description:** `LazyColumn` and `LazyRow` efficiently compose only visible items, but if the data source grows unboundedly (infinite scroll without pagination limits, unbounded API responses) or if items contain large composables (full-resolution images, complex nested layouts), memory usage can grow until `OutOfMemoryError` crashes the app. Additionally, without stable `key` functions, recomposing the entire list on data changes creates excessive garbage collection pressure.
- **Detection Strategy:** Search for `LazyColumn` or `LazyRow` without pagination limits or with data sources that can grow without bounds. Check for missing `key` parameter in `items()` calls.
- **Detection Regex:** `items\s*\([^)]*\)\s*\{` without `key =` parameter
- **Impact:** Application crash via OutOfMemoryError, degraded performance, device resource exhaustion.
- **CWE:** CWE-400 (Uncontrolled Resource Consumption)
- **OWASP Mobile:** M4:2024 - Insufficient Input/Output Validation

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Unbounded list without pagination or keys
@Composable
fun InfiniteList(viewModel: ListViewModel = hiltViewModel()) {
    val items by viewModel.allItems.collectAsStateWithLifecycle()

    LazyColumn {
        items(items) { item ->  // No key = position-based identity
            LargeItemCard(item)  // Heavy composable per item
        }
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: Paginated list with stable keys
@Composable
fun PaginatedList(viewModel: ListViewModel = hiltViewModel()) {
    val items by viewModel.pagedItems.collectAsStateWithLifecycle()
    val listState = rememberLazyListState()

    LazyColumn(state = listState) {
        items(
            items = items,
            key = { item -> item.id }  // Stable unique key
        ) { item ->
            LightweightItemCard(item)
        }
    }

    // Load more when approaching the end
    val shouldLoadMore by remember {
        derivedStateOf {
            val lastVisibleItem = listState.layoutInfo.visibleItemsInfo.lastOrNull()
            lastVisibleItem != null && lastVisibleItem.index >= items.size - 5
        }
    }

    LaunchedEffect(shouldLoadMore) {
        if (shouldLoadMore) viewModel.loadNextPage()
    }
}
```

---

### COMPOSE-053: Animation Resource Exhaustion

- **Severity:** LOW
- **Category:** Performance & DoS Security
- **Description:** `rememberInfiniteTransition()` creates animations that run indefinitely. If multiple infinite transitions are created dynamically (e.g., one per item in a list, or triggered by untrusted input), they consume CPU resources proportionally. An attacker who can influence the number of animated components (through crafted deep links or API response manipulation) can cause excessive CPU usage, battery drain, and UI jank, effectively creating a denial of service condition.
- **Detection Strategy:** Search for `rememberInfiniteTransition()` inside `LazyColumn` items or composables that are dynamically created based on external data.
- **Detection Regex:** `rememberInfiniteTransition\s*\(\s*\)` inside `items\s*\(` blocks
- **Impact:** Excessive CPU usage, battery drain, UI freeze on lower-end devices.
- **CWE:** CWE-400 (Uncontrolled Resource Consumption)
- **OWASP Mobile:** M4:2024 - Insufficient Input/Output Validation

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Infinite animation per list item
LazyColumn {
    items(items) { item ->
        val infiniteTransition = rememberInfiniteTransition(label = "pulse")
        val alpha by infiniteTransition.animateFloat(
            initialValue = 0.3f,
            targetValue = 1f,
            animationSpec = infiniteRepeatable(tween(1000)),
            label = "alpha"
        )
        // With 1000 items, 1000 infinite animations run simultaneously
        ItemCard(item, alpha = alpha)
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: Animate only visible items, limit animation scope
LazyColumn {
    items(items, key = { it.id }) { item ->
        // Only animate if the item needs attention (e.g., new items)
        if (item.isNew) {
            val alpha by animateFloatAsState(
                targetValue = 1f,
                animationSpec = tween(500),  // Finite animation
                label = "newItemFade"
            )
            ItemCard(item, alpha = alpha)
        } else {
            ItemCard(item, alpha = 1f)
        }
    }
}
```

---

## Category 13: Network & Communication Security

### COMPOSE-054: Missing Certificate Pinning

- **Severity:** CRITICAL
- **Category:** Network & Communication Security
- **Description:** Without certificate pinning, HTTPS connections rely solely on the device's trust store for server certificate validation. On rooted devices or devices with user-installed CA certificates, an attacker can perform man-in-the-middle attacks by installing a rogue certificate. For Compose apps using Retrofit/OkHttp, certificate pinning must be configured on the OkHttpClient to validate the server's certificate against known pins. Network Security Config provides a declarative alternative but is less flexible for pin rotation.
- **Detection Strategy:** Search for OkHttpClient configuration and verify `CertificatePinner` is configured. Check for `network_security_config.xml` with pin entries.
- **Detection Regex:** `CertificatePinner` or `network-security-config.*pin-set` absence in network configuration
- **Impact:** Complete interception of HTTPS traffic, credential theft, API token exfiltration, data manipulation.
- **CWE:** CWE-295 (Improper Certificate Validation)
- **OWASP Mobile:** M5:2024 - Insecure Communication

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: No certificate pinning
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    @Provides
    @Singleton
    fun provideOkHttpClient(): OkHttpClient {
        return OkHttpClient.Builder()
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .build()
        // No certificate pinning - MITM possible on rooted devices
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: Certificate pinning with backup pins for rotation
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    @Provides
    @Singleton
    fun provideOkHttpClient(): OkHttpClient {
        val certificatePinner = CertificatePinner.Builder()
            .add(
                "api.traillens.com",
                "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",  // Primary
                "sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB="   // Backup
            )
            .build()

        return OkHttpClient.Builder()
            .certificatePinner(certificatePinner)
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .build()
    }
}
```

---

### COMPOSE-055: Cleartext Traffic Permitted

- **Severity:** HIGH
- **Category:** Network & Communication Security
- **Description:** Android 9 (API 28) and above block cleartext (HTTP) traffic by default, but apps can override this via `android:usesCleartextTraffic="true"` in the manifest or via `network_security_config.xml`. If cleartext traffic is permitted, all API calls, authentication requests, and data transfers can be intercepted on the local network without any certificate manipulation. This is particularly dangerous for apps that handle authentication tokens or personal data.
- **Detection Strategy:** Check `AndroidManifest.xml` for `android:usesCleartextTraffic="true"` and `network_security_config.xml` for `cleartextTrafficPermitted="true"`.
- **Detection Regex:** `usesCleartextTraffic\s*=\s*"true"|cleartextTrafficPermitted\s*=\s*"true"`
- **Impact:** All network traffic interceptable via simple packet capture, no MITM proxy needed.
- **CWE:** CWE-319 (Cleartext Transmission of Sensitive Information)
- **OWASP Mobile:** M5:2024 - Insecure Communication

**Vulnerable Pattern:**

```xml
<!-- VULNERABLE: Cleartext traffic allowed -->
<application
    android:usesCleartextTraffic="true"
    ... >
```

**Secure Pattern:**

```xml
<!-- SECURE: Cleartext traffic blocked (default on API 28+) -->
<application
    android:usesCleartextTraffic="false"
    android:networkSecurityConfig="@xml/network_security_config"
    ... >

<!-- network_security_config.xml -->
<network-security-config>
    <domain-config cleartextTrafficPermitted="false">
        <domain includeSubdomains="true">traillens.com</domain>
        <pin-set expiration="2027-01-01">
            <pin digest="SHA-256">base64_encoded_pin_here</pin>
            <pin digest="SHA-256">backup_pin_here</pin>
        </pin-set>
    </domain-config>
    <!-- Only allow cleartext for local dev if needed -->
    <debug-overrides>
        <trust-anchors>
            <certificates src="user" />
        </trust-anchors>
    </debug-overrides>
</network-security-config>
```

---

### COMPOSE-056: Plaintext Credential Storage

- **Severity:** HIGH
- **Category:** Network & Communication Security
- **Description:** Storing authentication tokens, API keys, or user credentials in `SharedPreferences`, `DataStore`, or files without encryption leaves them readable on rooted devices or through backup extraction. The deprecated `EncryptedSharedPreferences` from Jetpack Security Crypto and the modern approach using DataStore with Tink encryption both address this. Compose apps often store tokens for state restoration, and using plain `DataStore` or `SharedPreferences` for tokens is a common mistake.
- **Detection Strategy:** Search for token/credential storage in `SharedPreferences` or `DataStore` without encryption. Check for `EncryptedSharedPreferences` or Tink encryption usage.
- **Detection Regex:** `(sharedPreferences|dataStore|preferences)\s*\.[^}]*(token|password|secret|apiKey|credential)` without encryption wrapper
- **Impact:** Credential theft on rooted devices, backup extraction of tokens, session hijacking.
- **CWE:** CWE-312 (Cleartext Storage of Sensitive Information)
- **OWASP Mobile:** M9:2024 - Insecure Data Storage

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Token stored in plain SharedPreferences
class TokenManager(context: Context) {
    private val prefs = context.getSharedPreferences("auth", Context.MODE_PRIVATE)

    fun saveToken(token: String) {
        prefs.edit().putString("auth_token", token).apply()
        // Stored in cleartext at /data/data/pkg/shared_prefs/auth.xml
    }

    fun getToken(): String? = prefs.getString("auth_token", null)
}
```

**Secure Pattern:**

```kotlin
// SECURE: Token stored with encryption using Android Keystore
class SecureTokenManager(context: Context) {
    private val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build()

    private val encryptedPrefs = EncryptedSharedPreferences.create(
        context,
        "secure_auth",
        masterKey,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )

    fun saveToken(token: String) {
        encryptedPrefs.edit().putString("auth_token", token).apply()
    }

    fun getToken(): String? = encryptedPrefs.getString("auth_token", null)
}

// For new projects, prefer DataStore + Tink:
// https://developer.android.com/topic/security/data
```

---

## Category 14: Authentication & Biometric Security

### COMPOSE-057: Biometric Authentication Without CryptoObject

- **Severity:** CRITICAL
- **Category:** Authentication & Biometric Security
- **Description:** Android's `BiometricPrompt` can be used with or without a `CryptoObject`. Without a `CryptoObject`, the biometric authentication is purely a UI gate that returns a boolean success/failure result. Tools like Frida can hook `BiometricPrompt.AuthenticationCallback.onAuthenticationSucceeded()` and trigger it directly with a null `CryptoObject`, completely bypassing the biometric check. Research shows 70% of apps with biometric authentication can be bypassed this way. The secure approach binds a cryptographic key to the biometric authentication, making the key usable only after genuine biometric verification.
- **Detection Strategy:** Search for `BiometricPrompt.authenticate()` calls and verify a `CryptoObject` is passed. Check that the cryptographic key requires user authentication.
- **Detection Regex:** `\.authenticate\s*\([^)]*\)` without `CryptoObject` parameter, or `authenticate\(promptInfo\)` (no CryptoObject)
- **Impact:** Complete bypass of biometric authentication on rooted devices using Frida or similar instrumentation.
- **CWE:** CWE-287 (Improper Authentication)
- **OWASP Mobile:** M3:2024 - Insecure Authentication/Authorization

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Biometric auth without CryptoObject - bypassable via Frida
@Composable
fun BiometricGate(onAuthenticated: () -> Unit) {
    val context = LocalContext.current
    val activity = context as FragmentActivity

    LaunchedEffect(Unit) {
        val biometricPrompt = BiometricPrompt(
            activity,
            object : BiometricPrompt.AuthenticationCallback() {
                override fun onAuthenticationSucceeded(
                    result: BiometricPrompt.AuthenticationResult
                ) {
                    // Frida can call this directly, bypassing biometrics
                    onAuthenticated()
                }
            }
        )
        val promptInfo = BiometricPrompt.PromptInfo.Builder()
            .setTitle("Authenticate")
            .setNegativeButtonText("Cancel")
            .build()

        // No CryptoObject - pure UI gate, easily bypassed
        biometricPrompt.authenticate(promptInfo)
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: Biometric auth with CryptoObject bound to Keystore
@Composable
fun BiometricGate(onAuthenticated: (Cipher) -> Unit) {
    val context = LocalContext.current
    val activity = context as FragmentActivity

    LaunchedEffect(Unit) {
        // Create key that requires biometric authentication
        val keyGenerator = KeyGenerator.getInstance(
            KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore"
        )
        keyGenerator.init(
            KeyGenParameterSpec.Builder("biometric_key",
                KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT)
                .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
                .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
                .setUserAuthenticationRequired(true)
                .setInvalidatedByBiometricEnrollment(true)
                .build()
        )
        keyGenerator.generateKey()

        val keyStore = KeyStore.getInstance("AndroidKeyStore")
        keyStore.load(null)
        val key = keyStore.getKey("biometric_key", null) as SecretKey
        val cipher = Cipher.getInstance("AES/GCM/NoPadding")
        cipher.init(Cipher.ENCRYPT_MODE, key)

        val biometricPrompt = BiometricPrompt(
            activity,
            object : BiometricPrompt.AuthenticationCallback() {
                override fun onAuthenticationSucceeded(
                    result: BiometricPrompt.AuthenticationResult
                ) {
                    // CryptoObject is only usable after genuine biometric auth
                    val authenticatedCipher = result.cryptoObject?.cipher
                    if (authenticatedCipher != null) {
                        onAuthenticated(authenticatedCipher)
                    }
                }
            }
        )
        val promptInfo = BiometricPrompt.PromptInfo.Builder()
            .setTitle("Authenticate")
            .setNegativeButtonText("Cancel")
            .build()

        // Authenticate with CryptoObject - cannot be bypassed by Frida
        biometricPrompt.authenticate(promptInfo, BiometricPrompt.CryptoObject(cipher))
    }
}
```

---

### COMPOSE-058: Missing Root/Tamper Detection

- **Severity:** HIGH
- **Category:** Authentication & Biometric Security
- **Description:** Compose apps running on rooted devices are vulnerable to runtime instrumentation (Frida, Xposed), memory inspection, API hooking, and certificate pinning bypass. Without root detection and tamper detection, attackers can modify app behavior at runtime, bypass authentication, intercept encrypted data, and inject malicious code. While root detection can be bypassed by sophisticated attackers, it raises the bar and deters opportunistic attacks. Google's Play Integrity API provides device attestation that is harder to forge.
- **Detection Strategy:** Verify the app implements root detection (via SafetyNet/Play Integrity API or libraries like rootbeer). Check that the app responds appropriately to detected root/tamper conditions.
- **Detection Regex:** `(SafetyNet|PlayIntegrity|RootBeer|isRooted|isDeviceRooted)` presence check
- **Impact:** All security controls bypassable on rooted devices without detection, including biometrics, certificate pinning, and encryption.
- **CWE:** CWE-693 (Protection Mechanism Failure)
- **OWASP Mobile:** M7:2024 - Insufficient Binary Protections

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: No root or tamper detection
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            // App runs identically on rooted and non-rooted devices
            TrailLensApp()
        }
    }
}
```

**Secure Pattern:**

```kotlin
// SECURE: Root/tamper detection with appropriate response
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {
            val integrityViewModel: IntegrityViewModel = hiltViewModel()
            val integrityState by integrityViewModel.state.collectAsStateWithLifecycle()

            LaunchedEffect(Unit) {
                integrityViewModel.checkDeviceIntegrity()
            }

            when (integrityState) {
                IntegrityState.Checking -> SplashScreen()
                IntegrityState.Trusted -> TrailLensApp()
                IntegrityState.Untrusted -> {
                    // Degrade gracefully - don't reveal detection to attacker
                    TrailLensApp(restrictedMode = true)
                    // In restricted mode: disable sensitive features,
                    // report to backend, limit data access
                }
            }
        }
    }
}

// Use Play Integrity API for device attestation
class IntegrityViewModel @Inject constructor(
    private val integrityManager: IntegrityManager
) : ViewModel() {
    // Implementation using Play Integrity API
    // Verdict verified server-side, not client-side
}
```

---

### COMPOSE-059: Insecure Local Authentication Gate

- **Severity:** HIGH
- **Category:** Authentication & Biometric Security
- **Description:** A local authentication gate (PIN screen, pattern lock, biometric check) implemented purely in Compose state provides no real security. If the authentication state is a simple boolean in a ViewModel or `rememberSaveable`, it can be bypassed through: (1) deep link navigation that skips the gate screen, (2) state restoration with tampered saved state, (3) Frida instrumentation that modifies the boolean value, or (4) process death and restore with modified Bundle. Secure local authentication must be backed by cryptographic operations (Keystore) that cannot be simulated.
- **Detection Strategy:** Search for authentication gates that use simple boolean state without backing cryptographic verification. Flag patterns where `isAuthenticated` is a simple state variable.
- **Detection Regex:** `(isAuthenticated|isUnlocked|isPinVerified)\s*=\s*mutableStateOf\s*\(\s*(false|true)\s*\)`
- **Impact:** Complete bypass of local authentication, access to all protected screens and data.
- **CWE:** CWE-287 (Improper Authentication)
- **OWASP Mobile:** M3:2024 - Insecure Authentication/Authorization

**Vulnerable Pattern:**

```kotlin
// VULNERABLE: Boolean-based auth gate, trivially bypassable
@Composable
fun AppGate() {
    var isAuthenticated by rememberSaveable { mutableStateOf(false) }

    if (isAuthenticated) {
        MainApp()
    } else {
        PinScreen(onCorrectPin = { isAuthenticated = true })
    }
    // Bypassed by: deep link, state tampering, Frida hook
}
```

**Secure Pattern:**

```kotlin
// SECURE: Cryptographic authentication gate
@Composable
fun AppGate(viewModel: AuthGateViewModel = hiltViewModel()) {
    val authState by viewModel.authState.collectAsStateWithLifecycle()

    when (authState) {
        is AuthGateState.Locked -> {
            PinScreen(onPinEntered = { pin ->
                // PIN verified against salted hash stored in EncryptedSharedPreferences
                // Success unlocks a Keystore key needed for data decryption
                viewModel.verifyPin(pin)
            })
        }
        is AuthGateState.Unlocked -> {
            // Data decryption key is available only after successful auth
            val decryptionCipher = (authState as AuthGateState.Unlocked).cipher
            MainApp(decryptionCipher = decryptionCipher)
        }
        is AuthGateState.Failed -> {
            ErrorScreen("Authentication failed. ${viewModel.remainingAttempts} attempts remaining.")
        }
    }
}

// The decryption cipher is bound to Keystore and requires authenticated session
// It cannot be obtained without genuine authentication
```

---

## Detection Summary

### By Severity

| Severity | Count | Pattern IDs |
| -------- | ----- | ----------- |
| CRITICAL | 8 | COMPOSE-001, 002, 019, 020, 033, 040, 054, 057 |
| HIGH | 28 | COMPOSE-003, 004, 006, 007, 008, 009, 014, 015, 018, 021, 022, 024, 025, 029, 034, 035, 037, 041, 042, 043, 044, 045, 046, 048, 055, 056, 058, 059 |
| MEDIUM | 20 | COMPOSE-005, 010, 011, 012, 016, 017, 023, 026, 027, 028, 030, 031, 036, 038, 039, 047, 049, 050, 051, 052 |
| LOW | 3 | COMPOSE-013, 032, 053 |

### By Category

| Category | Count | Pattern ID Range |
| -------- | ----- | ---------------- |
| Navigation & Deep Link Security | 7 | COMPOSE-001 to COMPOSE-007 |
| State Management Security | 6 | COMPOSE-008 to COMPOSE-013 |
| Side-Effect Security | 5 | COMPOSE-014 to COMPOSE-018 |
| UI Security & Screen Protection | 5 | COMPOSE-019 to COMPOSE-023 |
| Text Input & Credential Security | 5 | COMPOSE-024 to COMPOSE-028 |
| Accessibility & Semantics Security | 4 | COMPOSE-029 to COMPOSE-032 |
| Serialization & Deserialization Security | 4 | COMPOSE-033 to COMPOSE-036 |
| Image & Media Security | 3 | COMPOSE-037 to COMPOSE-039 |
| WebView & Interop Security | 4 | COMPOSE-040 to COMPOSE-043 |
| Component & Intent Security | 4 | COMPOSE-044 to COMPOSE-047 |
| Build & Obfuscation Security | 3 | COMPOSE-048 to COMPOSE-050 |
| Performance & DoS Security | 3 | COMPOSE-051 to COMPOSE-053 |
| Network & Communication Security | 3 | COMPOSE-054 to COMPOSE-056 |
| Authentication & Biometric Security | 3 | COMPOSE-057 to COMPOSE-059 |
| **Total** | **59** | |

### CWE Coverage

| CWE | Description | Pattern Count |
| --- | ----------- | ------------- |
| CWE-20 | Improper Input Validation | 3 |
| CWE-79 | Cross-site Scripting | 1 |
| CWE-200 | Exposure of Sensitive Information | 7 |
| CWE-208 | Observable Timing Discrepancy | 1 |
| CWE-215 | Sensitive Information in Debug Code | 2 |
| CWE-281 | Improper Preservation of Permissions | 1 |
| CWE-284 | Improper Access Control | 1 |
| CWE-287 | Improper Authentication | 2 |
| CWE-295 | Improper Certificate Validation | 1 |
| CWE-306 | Missing Authentication for Critical Function | 1 |
| CWE-312 | Cleartext Storage of Sensitive Information | 2 |
| CWE-316 | Cleartext Storage in Memory | 1 |
| CWE-319 | Cleartext Transmission of Sensitive Information | 2 |
| CWE-362 | Race Condition | 1 |
| CWE-400 | Uncontrolled Resource Consumption | 5 |
| CWE-404 | Improper Resource Shutdown | 3 |
| CWE-441 | Unintended Proxy | 1 |
| CWE-472 | External Control of Assumed-Immutable Parameter | 1 |
| CWE-502 | Deserialization of Untrusted Data | 3 |
| CWE-532 | Sensitive Information in Log File | 1 |
| CWE-549 | Missing Password Field Masking | 1 |
| CWE-613 | Insufficient Session Expiration | 2 |
| CWE-693 | Protection Mechanism Failure | 2 |
| CWE-732 | Incorrect Permission Assignment | 2 |
| CWE-749 | Exposed Dangerous Method | 1 |
| CWE-835 | Unreachable Exit Condition | 1 |
| CWE-841 | Improper Enforcement of Behavioral Workflow | 1 |
| CWE-843 | Access Using Incompatible Type | 1 |
| CWE-918 | Server-Side Request Forgery | 1 |
| CWE-926 | Improper Export of Android Components | 1 |
| CWE-927 | Implicit Intent for Sensitive Communication | 1 |
| CWE-940 | Improper Verification of Source | 1 |
| CWE-1021 | Improper Restriction of UI Layers | 2 |

### OWASP Mobile Top 10 (2024) Coverage

| OWASP ID | Description | Pattern Count |
| -------- | ----------- | ------------- |
| M1:2024 | Improper Credential Usage | 1 |
| M3:2024 | Insecure Authentication/Authorization | 8 |
| M4:2024 | Insufficient Input/Output Validation | 14 |
| M5:2024 | Insecure Communication | 3 |
| M6:2024 | Inadequate Privacy Controls | 3 |
| M7:2024 | Insufficient Binary Protections | 4 |
| M8:2024 | Security Misconfiguration | 10 |
| M9:2024 | Insecure Data Storage | 9 |

---

## References

- [PT Security: Android Jetpack Navigation Deep Links Handling Exploitation](https://swarm.ptsecurity.com/android-jetpack-navigation-deep-links-handling-exploitation/)
- [PT Security: Android Jetpack Navigation Go Even Deeper](https://swarm.ptsecurity.com/android-jetpack-navigation-go-even-deeper/)
- [Android Developers: Tapjacking](https://developer.android.com/privacy-and-security/risks/tapjacking)
- [Android Developers: Unsafe Deserialization](https://developer.android.com/privacy-and-security/risks/unsafe-deserialization)
- [Android Developers: Intent Redirection](https://developer.android.com/privacy-and-security/risks/intent-redirection)
- [Android Developers: Cross-App Scripting](https://developer.android.com/privacy-and-security/risks/cross-app-scripting)
- [Android Developers: StrandHogg / Task Affinity](https://developer.android.com/privacy-and-security/risks/strandhogg)
- [Android Developers: Log Info Disclosure](https://developer.android.com/privacy-and-security/risks/log-info-disclosure)
- [Android Developers: WebView Native Bridges](https://developer.android.com/privacy-and-security/risks/insecure-webview-native-bridges)
- [Android Developers: Secure Activities](https://developer.android.com/security/fraud-prevention/activities)
- [OWASP Mobile Top 10 (2024)](https://owasp.org/www-project-mobile-top-10/)
- [HackTricks: Bypass Biometric Authentication Android](https://book.hacktricks.xyz/mobile-pentesting/android-app-pentesting/bypass-biometric-authentication-android)
- [Guardsquare: Secure In-App Keyboard](https://www.guardsquare.com/mobile-app-security-research-center/malware/secure-in-app-keyboard)
- [GitHub Security Lab: Android Deserialization Vulnerabilities](https://securitylab.github.com/resources/android-deserialization-vulnerabilities/)
