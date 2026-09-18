# Security Notes

## Failed Login Protection

The application tracks failed login attempts using the `UserProfile`
model.

A user account is blocked after 5 failed login attempts.

The following information is stored:

- Failed login attempt count
- Whether the account is blocked
- Date and time when the account was blocked

A successful login resets the failed login attempt counter.

## Account Blocking

When an account reaches 5 failed attempts:

- The account is marked as login blocked.
- Further login attempts are rejected.
- The user is informed that the account has been blocked.
- An administrator can manage the account through the admin account
  management interface.

## Production Limitations

The current implementation is designed for the training project and
should be strengthened before production deployment.

Potential production improvements include:

- Rate limiting based on IP address and account.
- Temporary lockout instead of permanent blocking.
- CAPTCHA after repeated failed attempts.
- Centralized security monitoring.
- More detailed audit logging.
- Protection against distributed login attacks.
- Email notification when an account is blocked.
- Administrative account-unlock workflow.
- HTTPS for all authentication traffic.
- Secure cookie configuration.
- Stronger password and authentication policies.

The current five-attempt mechanism provides basic protection but should
not be considered a complete production-grade authentication security
system.