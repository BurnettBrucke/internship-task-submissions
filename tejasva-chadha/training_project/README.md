# Student Training Portal

The Student Training Portal is a secure, role-based student training management application built on Django and styled with premium, responsive Bootstrap 5 templates.

---

## Role and Permission Matrix

| Role | Student Directory | Edit Marks | Add Feedback | User Management | Audit Logs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Administrator** | Full Access (Read/Write) | Yes | Read Only | Full Access (Approve/Toggle) | Full Access (Read) |
| **Trainer** | Assigned Students Only | Assigned Only | Assigned Students Only | Access Denied | Access Denied |
| **Student** | Own Profile Only | Read Only (Own) | Own Visible Feedback Only | Access Denied | Access Denied |

---

## Session and Cookie Security Analysis

During local development and production deployments, the following Django settings govern cookie and session security:

* **`SESSION_COOKIE_HTTPONLY`** (Default: `True`):
  * **Mechanism**: Instructs browsers not to expose session cookies to client-side scripts (e.g. `document.cookie`).
  * **Security Value**: High. Mitigates Session Hijacking risks associated with Cross-Site Scripting (XSS) injection.
* **`SESSION_COOKIE_SECURE`** (Default: `False` in Dev, `True` in Prod):
  * **Mechanism**: Tells the browser to only transmit session cookies over secure HTTPS connections.
  * **HTTPS Dependency**: **Yes**. Requires HTTPS.
  * **Dev Warning**: If set to `True` during local HTTP development, the browser will refuse to send session cookies back to Django, causing login requests to fail silently or loop.
* **`CSRF_COOKIE_SECURE`** (Default: `False` in Dev, `True` in Prod):
  * **Mechanism**: Instructs the browser to only send the CSRF cookie over secure HTTPS connections.
  * **HTTPS Dependency**: **Yes**. Requires HTTPS.
  * **Dev Warning**: If set to `True` during local HTTP development, forms will fail CSRF verification because the CSRF token cookie is dropped.
* **`SESSION_EXPIRE_AT_BROWSER_CLOSE`** (Default: `False`):
  * **Mechanism**: If `True`, session cookies are discarded as soon as the user closes the browser session, rather than persisting.
  * **Security Value**: Prevents unauthorized reuse of sessions on shared or public computers after browser exit.
* **`SESSION_COOKIE_AGE`** (Default: `1209600` / 2 weeks):
  * **Mechanism**: Dictates session persistence duration in seconds.
  * **Security Value**: Shorter cookie ages (e.g. 1800 seconds / 30 mins) minimize the vulnerability window if a device is left unattended.

---

## Login Protection (Brute Force Lockout)

To safeguard accounts against brute force attacks, a login lockout mechanism has been implemented:
1. **Attempt Tracking**: Tracks consecutive invalid login attempts per username in Django's cache framework.
2. **Lockout Trigger**: Upon reaching **5 consecutive failures**, the account is locked in the cache (`login_block_<username>`) for **5 minutes**.
3. **User Feedback**: A clear Bootstrap alert informs the user that the account is temporarily blocked.
4. **Audit Logging**: Every failed attempt, block, and successful login is recorded with IP address, timestamp, and details inside the `AuditLog` database model.

### Production Recommendations & Limitations:
* **IP-based Blocking**: Username-based blocking can lead to Denial of Service (DoS) where an attacker intentionally locks legitimate users. In production, blocking should be based on a combination of username and IP address.
* **Production Libraries**: Use field-tested packages like `django-axes` or `django-defender` which support Redis/database backend storage, reverse proxy IP detection (e.g. Cloudflare headers), and custom cool-off periods.
* **Cache Persistence**: In-memory cache resets when the server restarts. In production, persistent cache nodes (e.g. Redis) should be used.
