# Read-only review pack: Portal CMS Django

Generated: 2026-11-19 20:20 UTC
Configured root available: yes

This pack contains review questions, not findings or an approved change plan.
Use the matching skill and the target repository's current guidance. Inspect
relevant non-secret source read-only. Do not include source excerpts or secrets.

## Review questions

- [ ] Are Django settings, production security controls, external configuration, and sensitive logging handled safely?
- [ ] Are CILogon/OAuth authentication, COmanage group synchronization, and resource-provider permissions least-privileged and failure-safe?
- [ ] Are CMS routes, published content/versioning, permissions, and resource-provider data boundaries protected against regressions?
- [ ] Are migrations and CIDER/upstream schema coupling reviewed and tested with nonproduction configuration only?
- [ ] Are framework and dependency modernization opportunities based on current compatibility evidence?
- [ ] Which changes affect authentication, permissions, routes, migrations, public content, or external schemas and require explicit human planning?

## Reviewer notes

Record only sanitized observations, safe evidence references, and proposed
improvements. Label each item proposed. An authorized human must decide
whether to create a separate implementation plan.
