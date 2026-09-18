# Security Settings Documentation

## Day 4 - Task 2: Secure Account Management

This document explains the Django session and cookie security settings used for secure account management.

### 1. SESSION_COOKIE_HTTPONLY

```python
SESSION_COOKIE_HTTPONLY = True
```

This prevents JavaScript running in the browser from accessing the Django session cookie.

It helps reduce the risk of session cookie theft through client-side scripts.

---

### 2. SESSION_COOKIE_SECURE

```python
SESSION_COOKIE_SECURE = True
```

This setting makes Django send the session cookie only over HTTPS connections.

It should be enabled when the application is deployed using HTTPS.

During local development with:

```text
http://127.0.0.1:8000/
```

it should not be blindly enabled because the browser will not send secure cookies over normal HTTP.

---

### 3. CSRF_COOKIE_SECURE

```python
CSRF_COOKIE_SECURE = True
```

This makes the CSRF cookie available only over HTTPS connections.

It should be enabled in a production environment where HTTPS is configured.

It should not be blindly enabled during local HTTP development because it can prevent the CSRF cookie from being sent.

---

### 4. SESSION_EXPIRE_AT_BROWSER_CLOSE

```python
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
```

This makes the user's session expire when the browser is closed.

It can provide additional protection on shared or public computers.

---

### 5. SESSION_COOKIE_AGE

```python
SESSION_COOKIE_AGE = 3600
```

This defines the maximum age of the session cookie in seconds.

`3600` seconds means the session can remain active for approximately one hour.

---

## Local Development vs Production

The development project currently runs using:

```text
http://127.0.0.1:8000/
```

Therefore, secure-cookie settings such as:

```python
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

should not be enabled blindly during local HTTP development.

In production, the application should use HTTPS and secure-cookie settings should be configured appropriately.

Other production security measures should also include HTTPS, secure secret-key management, proper `ALLOWED_HOSTS` configuration, secure deployment configuration, monitoring and rate limiting.

---

## Failed Login Protection

The application tracks failed login attempts using the `UserProfile.failed_login_attempts` field.

After five failed login attempts, login is blocked for that account.

The failed login event is also recorded in the custom audit log.

### Limitations

The current implementation uses a database counter and does not provide a complete production-grade rate-limiting system.

A production system could improve this by using:

* Temporary time-based lockouts
* Redis or another shared cache
* IP-based rate limiting
* Increasing lockout delays
* Monitoring and security alerts
* CAPTCHA after repeated failures
* Centralized security monitoring

This implementation is intended for training and demonstrates the basic concept of failed-login protection.
