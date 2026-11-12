# Health Contracts

- `/healthz`: process/service health; status/readiness DTOs report configuration/capability
- Readiness may be `not reported` until safe DTO exists
- Do not expose paths · credentials · raw probes · private config