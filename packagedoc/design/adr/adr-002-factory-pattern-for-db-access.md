
# ADR-002: Factory Pattern for Database Access

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
TestResultDBAccess must support multiple access methods (direct DB and REST API) and remain extensible for future access types. A unified interface is needed to abstract the creation and use of these access methods.

## Decision
Adopt the Factory design pattern to instantiate the appropriate database access class (DirectDBAccess or RestApiDBAccess) based on configuration or user input. All access classes implement a common interface.

## Consequences
### Positive
- Simplifies client code and improves maintainability.
- Makes it easy to add new access methods in the future.
- Ensures consistent API and behavior across access types.

### Negative
- Adds a layer of abstraction that may slightly increase complexity.

### Neutral
- No significant neutral impacts identified.

## Alternatives Considered
### 1. Hardcoded Access Method Selection (Rejected)
Manually select and instantiate access classes in client code.

Rejected because:
- Reduces maintainability and extensibility.
- Increases risk of inconsistent usage.
