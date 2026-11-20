# Portal CMS Django application review skill

Use this skill for read-only review of `../Operations_PortalCMS_Django`. The paired
`../Operations_CMS_Infrastructure` repository owns deployed configuration, systemd,
Nginx, release selection, migrations, and production operations. The
`../Operations_Django_Development` repository owns the integrated local harness. Keep
these repository boundaries explicit; all target and context repositories remain
read-only to this workflow. Write proposed improvements only to `analysis_reports/` in
this repository and never apply them to a reviewed repository, regardless of approval
or plan status.

## Before reviewing

1. Read the effective `AGENTS.md` for the app and paired infrastructure repositories.
   Inspect Git status at each relevant root and preserve existing tracked, untracked,
   and submodule work.
2. Use current app source and tests as the authority for application behavior. Read
   `README.md` and `dev_documentation/CURRENT_STATE.md` for orientation, but treat
   operational snapshots and claims about external consumers as dated until verified
   from code or a separately authorized source.
3. For deployed runtime and dependency questions, trace the active infrastructure
   inventory selection, app variables/playbook, selected uv project/lock, config and
   service templates, and release workflow. The app's own `pyproject.toml` describes
   its project contract but does not by itself establish the deployed environment.
   Do not copy current tags, hostnames, paths, environment names, or package versions
   into durable findings.
4. Never read external runtime JSON, `.env` files, databases, backups, media, logs,
   Ansible Vault/password files, Terraform state, credentials, private keys, or
   generated secret-bearing configuration. Infrastructure password files are
   Ansible Vault-encrypted; do not open or decrypt them. Never scan target contents for
   secrets.

## Application map and contracts

- The Django project is under `operations_portalcms_django/`. Its main apps are
  `portal` (shared CMS integration, identity adapters, permission helpers, page
  workflow, health check), `resources` (CIDER-backed resource and software views),
  `infrastructure_news`, and `integration_news`.
- Root URL ordering matters: explicit application routes precede the django CMS catch-
  all. Treat route renames, removals, or method changes as public behavior changes.
- Authentication uses django-allauth with CILogon. Local signup is intentionally
  closed; review social-login adapter/provider policy, account linking, and failure
  behavior. Do not conflate CILogon authentication with Resource Provider group
  membership: the current app documentation says that membership is owned centrally
  outside CILogon and is not synchronized by this app at login. Verify current code
  before relying on that statement.
- Focus-area pages use django CMS versioning and custom submit-for-review/unlock
  endpoints. Review draft locks, editor versus publisher permissions, page-specific
  grants, plugin/media permissions, and CMS versioning compatibility together.
  Permission/group setup management commands can mutate access control; never run
  them during a review.
- `infrastructure_news` and `integration_news` own the status and integration feeds.
  Both have draft/published state, custom publish/unpublish permissions, and public
  JSON feeds. Existing unversioned feed paths and serialized fields are external
  contracts. Confirm consumers before recommending route, cache, status, ID, time-zone,
  or field changes. Do not assume delivery flags cause email or Slack delivery.
- `resources` reads Operations API/CIDER data and persists local cache tables. Review
  upstream schema validation, freshness/fallback behavior, local-vs-remote identifiers,
  request timeouts, cache/privacy headers, and the sync transaction boundary. The
  synchronization command has dry-run and optional stale-group pruning behavior; a
  dry run still makes external API requests, and pruning changes local data. Do not run
  the command during this review.
- `GET /healthz/` returns app version/status and performs a lightweight database
  readiness query; failures return a generic unavailable response. Review its public
  information boundary and verify how current infrastructure consumes it, without
  probing a running service.
- The external JSON config selected by `APP_CONFIG` is required at runtime. Settings
  validate required keys/types for non-debug deployments. Review the loader and its
  validation code, never the actual config file or values.
- News tables retain established table naming and the public feeds expose selected
  published content. Treat model/table and migration changes as high-risk data and
  consumer changes. The Drupal news import is retained cutover tooling, not a routine
  job; changes/removal require checking its guarded plan/apply design and approved
  cleanup status.

## Review focus

- Authentication and authorization: fail-closed behavior, CILogon provider policy,
  group ownership boundaries, publisher permissions, page locks, staff/superuser
  exceptions, and CSRF/method restrictions on state transitions.
- Public exposure: published-only filtering, active flags, feed schemas, cache
  boundaries, version identifiers, timestamps/time zones, and whether public pages or
  feeds disclose author/contact/configuration details.
- CIDER integration: input validation, API error handling, stale cache/fallback rules,
  transactional sync, dry-run behavior, deletion/pruning, and consistency with the
  upstream schema. Keep network-dependent checks pending unless separately authorized.
- CMS content and media: page-version workflow, plugin permissions, uploaded media
  access, template escaping, external assets, and safe handling of rich text and links.
- Runtime safety: `APP_CONFIG` validation, host/origin/cookie/security settings,
  database readiness/error responses, static/media paths, logging, and config
  permissions. Do not expose actual settings or runtime values in review output.
- Dependency compatibility: compare the app manifest with the exact infrastructure-
  selected uv lock and declared system packages/services. Infrastructure code is the
  source of truth for app-specific OS needs; ordinary OS security/basic updates remain
  apt-managed. Keep deployment and host upgrade changes in infrastructure scope.
- Migrations and external compatibility: stable table/data contracts, CMS plugin and
  django CMS versioning behavior, CIDER schemas, feed consumers, and migration gates.
  Separate application changes from migration approval and release operations.

## Tests and prohibited actions

Tests cover authentication/signup policy, CMS page-review/group permissions, news
permissions and public feed schemas, resource API fallback/errors and synchronization,
health-check behavior, and import planning. The standalone integration/check scripts
are not guaranteed-safe unit tests: repository documentation warns that they can touch
whichever database `APP_CONFIG` selects and may create or alter users/groups/content.
Do not run them against production or an ambiguous config. Do not run any tests or
management command during this review unless a separate task requests checks that the
current target `AGENTS.md` explicitly permits with deliberately nonproduction config.

Never run migrations, `manage.py` write commands, CIDER sync/import/group setup,
database/media tools, Ansible, Terraform, vault, cloud, deployments, service commands,
production database access, or live OAuth checks. Report prohibited or unavailable
validation as pending for an authorized operator.

## Findings format

For each finding, include **Observation**, **safe evidence reference**, **risk**,
**proposed improvement**, **confidence**, **affected contract**, and **human gate**.
Do not include runtime values, personal data, news content, tokens, secrets, raw logs,
or external infrastructure details. Separate verified code behavior from inference.
Mark every recommendation **proposed** until an authorized human records a separate
implementation plan.
