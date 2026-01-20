# ADR-004: Use Existing WebApp Login Method

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
The TestResultDBAccess REST API is being integrated with the TestResultWebApp. The web application already has a robust user authentication and session management system. Implementing a separate login mechanism for the API would duplicate logic, increase maintenance, and potentially introduce security inconsistencies.

## Decision
The REST API will leverage the existing login and session management system of the TestResultWebApp. API endpoints will validate user sessions or tokens issued by the web application, ensuring a unified authentication experience for both UI and API consumers.

## Consequences
### Positive
- Reduces duplication of authentication logic.
- Centralizes user management and security policies.
- Simplifies user experience and administration.

### Negative
- Tightly couples API authentication to the web application's session mechanism.
- Changes in the webapp login system may require API updates.

### Neutral
- API consumers must obtain valid sessions/tokens from the webapp.

## Alternatives Considered
### 1. Implement Separate API Authentication (Rejected)
A standalone authentication system for the API (e.g., OAuth2, API keys).

Rejected because:
- Increases complexity and maintenance.
- Risks inconsistent security policies.

## References
- [TestResultWebApp REST API Implementation](https://testresultwebapp.wam-sso.bosch.com/api/v1/docs/)
