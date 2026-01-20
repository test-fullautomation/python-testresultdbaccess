
# ADR-003: Support Both Direct and REST API Access

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
Some users and systems operate within the secure network and can access the database directly, while others (external or less trusted) must use the REST API. Supporting both methods provides flexibility and meets diverse operational and security requirements.

## Decision
TestResultDBAccess will support both direct database access (for trusted/internal users) and REST API access (for external/untrusted users). The access method is selected at runtime based on configuration or user input.

## Consequences
### Positive
- Maximizes flexibility for different deployment scenarios.
- Allows gradual migration to REST API if required by future security policies.

### Negative
- Requires careful documentation and best practices to avoid data consistency issues.
- Increases complexity in configuration and testing.

### Neutral
- Both access methods must be maintained and supported.

## Alternatives Considered
### 1. REST API Only (Rejected)
Restrict all access to go through the REST API, even for internal users.

Rejected because:
- Reduces performance and flexibility for trusted internal users.
- Increases operational overhead for internal-only deployments.

### 2. Direct DB Access Only (Rejected)
Allow only direct database access for all users.

Rejected because:
- Fails to meet security requirements for external/untrusted access.
- Limits future extensibility and integration.
