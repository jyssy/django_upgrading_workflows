# Read-only review pack: Service Index Django

Generated: 2026-11-19 20:19 UTC
Configured root available: yes

This pack contains review questions, not findings or an approved change plan.
Use the matching skill and the target repository's current guidance. Inspect
relevant non-secret source read-only. Do not include source excerpts or secrets.

## Review questions

- [ ] Are Django settings separated safely from external runtime configuration, with production debug and cookie/security settings explicit?
- [ ] Are authentication, authorization, API permissions, and user-admin integration boundaries current and least-privileged?
- [ ] Are multi-schema data access, migrations, and tenant boundaries handled consistently and tested without production access?
- [ ] Are dependency and framework modernization opportunities supported by current compatibility evidence?
- [ ] Are error handling, logging, observability, and tests adequate without logging sensitive values?
- [ ] Which proposed changes touch settings, routes, migrations, authentication, schema behavior, or external interfaces and therefore need explicit human planning?

## Reviewer notes

Record only sanitized observations, safe evidence references, and proposed
improvements. Label each item proposed. An authorized human must decide
whether to create a separate implementation plan.
