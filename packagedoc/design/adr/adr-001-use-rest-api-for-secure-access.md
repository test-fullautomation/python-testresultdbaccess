
# ADR-001: Use REST API for Secure Access

## Status
Accepted

## Date
2025-11-08

## Author
Tran Duy Ngoan (MS/EMC51-XC)

## Reviewer
- Tran Duy Ngoan (MS/EMC51-XC)

## History
| Date       | Version | Description     |
|------------|---------|-----------------|
| 2025-11-08 | 1.0     | Initial version |

## Context
The test result database is now located in a security zone that restricts direct access from outside. Direct database access is only possible from within the secure network. Users and systems outside the security zone require a secure way to access test result data.

## Decision
Introduce a REST API, exposed by the Test Result WebApp, as the primary access method for users and systems outside the security zone. The REST API will enforce authentication, authorization, and logging, and will only expose necessary data and operations.

## Consequences
### Positive
- All external access is funneled through the REST API, improving security and auditability.
- The architecture supports defense-in-depth and compliance with security policies.

### Negative
- Adds an extra layer of indirection for external users.
- Requires maintenance of the REST API and its security.

### Neutral
- Direct DB access is only available to trusted/internal users within the security zone.

## Alternatives Considered
### 1. Direct DB Access Only (Rejected)
Allow all users to access the database directly.

Rejected because:
- Violates security zone restrictions.
- Increases risk of unauthorized access and data breaches.

## References
- [TestResultWebApp REST API Implementation](https://testresultwebapp.wam-sso.bosch.com/api/v1/docs/)
