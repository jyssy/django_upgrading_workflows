# Read-only review pack: Portal CMS Infrastructure

Generated: 2026-11-19 20:19 UTC
Configured root available: yes

This pack contains review questions, not findings or an approved change plan.
Use the matching skill and the target repository's current guidance. Inspect
relevant non-secret source read-only. Do not include source excerpts or secrets.

## Review questions

- [ ] Do Terraform resources and backends use least privilege, encryption, narrow network exposure, and safe state practices?
- [ ] Do Ansible deployment tasks use safe secret references, explicit targeting, idempotent configuration, and bounded privilege?
- [ ] Are migration enablement, static collection, and service restart behavior clearly separated and controlled?
- [ ] Are Nginx, Gunicorn, PostgreSQL connectivity, TLS/certificate handling, patching, backups, and monitoring aligned with current practices?
- [ ] Which follow-up validations are explicitly forbidden to the reviewer and must remain pending for an authorized operator?

## Reviewer notes

Record only sanitized observations, safe evidence references, and proposed
improvements. Label each item proposed. An authorized human must decide
whether to create a separate implementation plan.
