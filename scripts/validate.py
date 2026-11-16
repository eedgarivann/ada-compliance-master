#!/usr/bin/env python3
"""Validate plugin manifests and Agent Skills frontmatter."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
AGENT_SCHEMA = ROOT / "schemas" / "plugin.schema.json"
AGENT_MANIFEST = ROOT / "plugin.json"
CURSOR_MANIFEST = ROOT / ".cursor-plugin" / "plugin.json"
SKILLS_DIR = ROOT / "skills"

NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
MAX_NAME = 64
MAX_DESC = 1024
ALLOWED_FRONTMATTER = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
}


class Errors(list):
    def fail(self, message: str) -> None:
        self.append(message)

    def raise_if_any(self) -> None:
        if self:
            for item in self:
                print(f"ERROR: {item}", file=sys.stderr)
            raise SystemExit(1)


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_agent_manifest(errors: Errors) -> dict:
    if not AGENT_MANIFEST.is_file():
        errors.fail(f"missing {AGENT_MANIFEST.relative_to(ROOT)}")
        return {}
    schema = load_json(AGENT_SCHEMA)
    try:
        data = load_json(AGENT_MANIFEST)
    except json.JSONDecodeError as exc:
        errors.fail(f"plugin.json is not valid JSON: {exc}")
        return {}
    validator = jsonschema.Draft202012Validator(schema)
    for err in validator.iter_errors(data):
        loc = "/".join(str(p) for p in err.path) or "<root>"
        errors.fail(f"plugin.json {loc}: {err.message}")
    if isinstance(data, dict) and "logo" in data:
        errors.fail(
            "plugin.json must not include 'logo' (Agent Plugins 1.0.0 closed schema). "
            "Put the logo path in .cursor-plugin/plugin.json instead."
        )
    return data if isinstance(data, dict) else {}


def validate_cursor_manifest(errors: Errors) -> dict:
    if not CURSOR_MANIFEST.is_file():
        errors.fail(f"missing {CURSOR_MANIFEST.relative_to(ROOT)}")
        return {}
    try:
        data = load_json(CURSOR_MANIFEST)
    except json.JSONDecodeError as exc:
        errors.fail(f".cursor-plugin/plugin.json is not valid JSON: {exc}")
        return {}
    if not isinstance(data, dict):
        errors.fail(".cursor-plugin/plugin.json must be a JSON object")
        return {}
    name = data.get("name")
    if not isinstance(name, str) or not NAME_RE.fullmatch(name) or len(name) > MAX_NAME:
        errors.fail(
            ".cursor-plugin/plugin.json 'name' must be 1–64 char lowercase kebab-case "
            f"(got {name!r})"
        )
    author = data.get("author")
    if author is not None:
        if not isinstance(author, dict) or not isinstance(author.get("name"), str) or not author["name"].strip():
            errors.fail(".cursor-plugin/plugin.json 'author.name' is required when author is set")
    logo = data.get("logo")
    if logo is not None:
        if not isinstance(logo, str) or logo.startswith("/") or ".." in Path(logo).parts:
            errors.fail(f".cursor-plugin/plugin.json 'logo' must be a relative path inside the repo (got {logo!r})")
        else:
            logo_path = ROOT / logo
            if not logo_path.is_file():
                errors.fail(f".cursor-plugin/plugin.json logo file missing: {logo}")
    skills = data.get("skills")
    if skills is not None:
        paths = skills if isinstance(skills, list) else [skills]
        for item in paths:
            if not isinstance(item, str) or item.startswith("/") or ".." in Path(item).parts:
                errors.fail(f".cursor-plugin/plugin.json skills path must be relative (got {item!r})")
            elif not (ROOT / item).exists():
                errors.fail(f".cursor-plugin/plugin.json skills path missing: {item}")
    return data


def validate_skill(skill_dir: Path, errors: Errors) -> None:
    skill_file = skill_dir / "SKILL.md"
    rel = skill_file.relative_to(ROOT)
    if not skill_file.is_file():
        errors.fail(f"missing {rel}")
        return
    text = skill_file.read_text(encoding="utf-8")
    if not text.startswith("---"):
        errors.fail(f"{rel}: missing YAML frontmatter")
        return
    parts = text.split("---", 2)
    if len(parts) < 3:
        errors.fail(f"{rel}: frontmatter not closed")
        return
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        errors.fail(f"{rel}: invalid YAML frontmatter: {exc}")
        return
    if not isinstance(data, dict):
        errors.fail(f"{rel}: frontmatter must be a mapping")
        return
    unknown = set(data) - ALLOWED_FRONTMATTER
    # Unknown fields are ignored by the Agent Skills spec; warn but do not fail.
    if unknown:
        print(f"NOTE: {rel} has extra frontmatter fields: {sorted(unknown)}")
    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.fail(f"{rel}: missing required field 'name'")
    else:
        if len(name) > MAX_NAME:
            errors.fail(f"{rel}: name exceeds {MAX_NAME} characters")
        if name != name.lower() or not NAME_RE.fullmatch(name) or "--" in name:
            errors.fail(
                f"{rel}: name {name!r} must be lowercase letters, digits and single hyphens, "
                "and must not start or end with a hyphen"
            )
        if name != skill_dir.name:
            errors.fail(f"{rel}: name {name!r} must match folder {skill_dir.name!r}")
    desc = data.get("description")
    if not isinstance(desc, str) or not desc.strip():
        errors.fail(f"{rel}: missing required field 'description'")
    elif len(desc) > MAX_DESC:
        errors.fail(f"{rel}: description exceeds {MAX_DESC} characters ({len(desc)})")
    if not parts[2].strip():
        errors.fail(f"{rel}: body is empty")


def main() -> int:
    errors = Errors()
    agent = validate_agent_manifest(errors)
    cursor = validate_cursor_manifest(errors)
    if agent and cursor:
        if agent.get("name") and cursor.get("name") and agent["name"] != cursor["name"]:
            errors.fail(
                f"plugin name mismatch: plugin.json={agent['name']!r} "
                f"vs .cursor-plugin/plugin.json={cursor['name']!r}"
            )
        if agent.get("version") and cursor.get("version") and agent["version"] != cursor["version"]:
            errors.fail("version mismatch between plugin.json and .cursor-plugin/plugin.json")
    if not SKILLS_DIR.is_dir():
        errors.fail("missing skills/")
    else:
        skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir() and not p.name.startswith("."))
        if not skill_dirs:
            errors.fail("skills/ has no skill directories")
        for skill_dir in skill_dirs:
            validate_skill(skill_dir, errors)
        print(f"checked {len(skill_dirs)} skill(s)")
    errors.raise_if_any()
    print("All plugin manifests and skills are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
