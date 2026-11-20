#!/usr/bin/env python3
"""Generate safe, dated review packs without reading target repository contents."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import os
import re
import tempfile


ROOT = Path(__file__).resolve().parent
PROFILE_FILE = ROOT / "review_profiles.json"
OUTPUT_ROOT = ROOT / "analysis_reports"
ALLOWED_ROOTS = {
    "service-index-django": "service-index-uv-sand/Operations_ServiceIndex_Django",
    "service-index-infrastructure": "Operations_ServiceIndex_Infrastructure",
    "portal-cms-django": "Operations_PortalCMS_Django",
    "portal-cms-infrastructure": "Operations_CMS_Infrastructure",
}


def load_profiles() -> list[dict[str, object]]:
    data = json.loads(PROFILE_FILE.read_text(encoding="utf-8"))
    profiles = data.get("repositories")
    if not isinstance(profiles, list) or not profiles:
        raise ValueError("review_profiles.json must define repositories")
    for profile in profiles:
        if not isinstance(profile, dict) or not all(
            isinstance(profile.get(key), str) for key in ("id", "label", "path")
        ) or not isinstance(profile.get("questions"), list):
            raise ValueError("invalid repository review profile")
        profile_id = str(profile["id"])
        if (
            profile_id not in ALLOWED_ROOTS
            or profile["path"] != ALLOWED_ROOTS[profile_id]
            or not re.fullmatch(r"[a-z0-9-]+", profile_id)
            or not all(isinstance(question, str) for question in profile["questions"])
        ):
            raise ValueError("review profile exceeds the configured repository scope")
    if {str(profile["id"]) for profile in profiles} != set(ALLOWED_ROOTS):
        raise ValueError("review_profiles.json must contain each configured target once")
    return profiles


def atomic_write(destination: Path, content: str) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=".review-", dir=destination.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, destination)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def render(profile: dict[str, object], run_at: datetime, available: bool) -> str:
    questions = profile["questions"]
    lines = [
        f"# Read-only review pack: {profile['label']}",
        "",
        f"Generated: {run_at.strftime('%Y-%m-%d %H:%M UTC')}",
        f"Configured root available: {'yes' if available else 'no'}",
        "",
        "This pack contains review questions, not findings or an approved change plan.",
        "Use the matching skill and the target repository's current guidance. Inspect",
        "relevant non-secret source read-only. Do not include source excerpts or secrets.",
        "",
        "## Review questions",
        "",
    ]
    lines.extend(f"- [ ] {question}" for question in questions)
    lines.extend(
        [
            "",
            "## Reviewer notes",
            "",
            "Record only sanitized observations, safe evidence references, and proposed",
            "improvements. Label each item proposed. An authorized human must decide",
            "whether to create a separate implementation plan.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    profiles = load_profiles()
    now = datetime.now(timezone.utc)
    run_id = now.strftime("%Y%m%dT%H%M%S.%fZ")
    if (OUTPUT_ROOT / run_id).exists():
        raise FileExistsError("review pack destination already exists; refusing to overwrite")
    for profile in profiles:
        # Only check the configured root. Never enumerate or open its contents.
        target = ROOT.parent / str(profile["path"])
        # Do not follow a symlink in any configured path component.
        parts = [target, *target.parents]
        available = not any(part.is_symlink() for part in parts) and target.is_dir()
        report = OUTPUT_ROOT / run_id / f"{profile['id']}.md"
        atomic_write(report, render(profile, now, available))
    print(f"Created {len(profiles)} review packs in analysis_reports/{run_id}/")


if __name__ == "__main__":
    main()
