# Read-only review pack: Portal CMS Django

Generated: 2026-11-20 18:58 UTC
Configured root available: yes

This pack contains review questions, not findings or an approved change plan.
Use the matching skill and the target repository's current guidance. Inspect
relevant non-secret source read-only. Do not include source excerpts or secrets.

## Review questions

- [ ] Does APP_CONFIG remain the required, validated runtime-config entry point without exposing its contents or weakening production settings?
- [ ] Do CILogon login/signup rules remain distinct from Resource Provider membership ownership, with page/news/resource permissions fail-closed?
- [ ] Do CMS draft/review/publish locks, focus-area editor/publisher roles, and POST-only state transitions preserve the intended workflow?
- [ ] Do public news feeds preserve published/active filtering, route and serialized-field contracts, cache behavior, and consumer compatibility?
- [ ] Do CIDER resource views and sync preserve upstream validation, caching/fallback rules, transaction semantics, dry-run behavior, and guarded stale-group pruning?
- [ ] Does healthz expose only intended readiness/version information and keep database failure details generic?
- [ ] Are test commands separated from database-mutating integration scripts, and is every requested check restricted to deliberately nonproduction config?
- [ ] Do dependency recommendations compare the app manifest with the infrastructure-selected uv project and lock, without copying transient pins?
- [ ] Which proposed changes affect auth/group ownership, page workflow, public feeds, CIDER data, migrations, or external schemas and need an explicit plan?

## Reviewer notes

Record only sanitized observations, safe evidence references, and proposed
improvements. Label each item proposed. An authorized human must decide
whether to create a separate implementation plan.
