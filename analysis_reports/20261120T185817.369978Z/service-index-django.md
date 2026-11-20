# Read-only review pack: Service Index Django

Generated: 2026-11-20 18:58 UTC
Configured root available: yes

This pack contains review questions, not findings or an approved change plan.
Use the matching skill and the target repository's current guidance. Inspect
relevant non-secret source read-only. Do not include source excerpts or secrets.

## Review questions

- [ ] Do the viewer/editor boundaries consistently protect browser views, exports, logs, staff/contact data, event workflows, and the API?
- [ ] Does the hosts API retain its authenticated GET-only contract, group authorization, explicit response fields, and safe exposure of host/contact fields?
- [ ] Do CILogon/allauth signup and login policies, and the access_django_user_admin producer/consumer interface, remain intentional and fail-closed?
- [ ] Do route decorators and method checks protect legacy login/logout/lock cleanup and username-based privilege helpers, and do validation/logging/tests protect inventory and contact data?
- [ ] Are schema or migration changes compatible with documented multi-schema procedures and existing database consumers?
- [ ] Do dependency recommendations compare the local uv environment with the infrastructure-selected production uv project and lock, without copying transient pins?
- [ ] Which proposed changes affect auth, API schema, exports, personal/host data, migrations, or external package interfaces and need an explicit plan?

## Reviewer notes

Record only sanitized observations, safe evidence references, and proposed
improvements. Label each item proposed. An authorized human must decide
whether to create a separate implementation plan.
