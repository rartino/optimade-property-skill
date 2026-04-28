# OPTIMADE Property YAML Skill

This repository distributes a reusable AI-agent skill for generating OPTIMADE property-definition source YAML files.

The skill targets source YAML, not published JSON. Source YAML files are the authoring-layer files used by OPTIMADE and definition-provider style tooling, and may include features such as `$$schema` and `$$inherit` that are processed into final JSON definitions.

The skill is intentionally scoped to property definitions only. It does not generate standards, entrytypes, response schemas, provider indexes, or packaged archives.

## Repository Layout

- `skills/optimade-property-yaml/`: canonical skill package. This is the directory to install or symlink into an agent skill directory.
- `skills/optimade-property-yaml/SKILL.md`: cross-agent skill instructions.
- `skills/optimade-property-yaml/references/`: concise operational reference notes and curated examples.
- `skills/optimade-property-yaml/assets/starter-property.yaml`: minimal starting template.
- `skills/optimade-property-yaml/scripts/`: lightweight validation, example selection, and smoke-test helpers.
- `external/OPTIMADE`: upstream OPTIMADE repository submodule for standard source definitions and specification context.
- `external/optimade-property-tools`: upstream property-tooling submodule for provider workflow conventions.
- `tests/`: prompt and expected-shape fixtures for manual or automated skill checks.

The canonical skill folder is `skills/optimade-property-yaml/`. `.agents/skills` and `.claude/skills` are installation targets, not the source layout of this repository.

## Installation

### Codex

```sh
./install-codex.sh
```

This symlinks:

```text
skills/optimade-property-yaml -> ~/.agents/skills/optimade-property-yaml
```

### Claude Code

```sh
./install-claude.sh
```

This symlinks:

```text
skills/optimade-property-yaml -> ~/.claude/skills/optimade-property-yaml
```

### Manual Installation

For Codex, create either a user-level or project-local symlink:

```sh
mkdir -p ~/.agents/skills
ln -s /path/to/optimade-property-skill/skills/optimade-property-yaml ~/.agents/skills/optimade-property-yaml
```

```sh
mkdir -p <project>/.agents/skills
ln -s /path/to/optimade-property-skill/skills/optimade-property-yaml <project>/.agents/skills/optimade-property-yaml
```

For Claude Code:

```sh
mkdir -p ~/.claude/skills
ln -s /path/to/optimade-property-skill/skills/optimade-property-yaml ~/.claude/skills/optimade-property-yaml
```

```sh
mkdir -p <project>/.claude/skills
ln -s /path/to/optimade-property-skill/skills/optimade-property-yaml <project>/.claude/skills/optimade-property-yaml
```

## Submodules

Initialize submodules with:

```sh
git submodule update --init --recursive
```

Update submodules with:

```sh
git submodule update --remote --merge
```

The skill is written defensively and can still use curated examples if the submodules are absent or uninitialized. The upstream submodules improve analogy search and style matching.

## Dependencies And Smoke Test

Install lightweight local dependencies:

```sh
make deps
```

Run the smoke test:

```sh
make smoke
```

The smoke test validates `assets/starter-property.yaml` and runs example selection for `magnetic moment`.

## Usage

Example prompt for Codex:

```text
Use the optimade-property-yaml skill. Generate one OPTIMADE property-definition source YAML file for `band_gap` in the `structures` context. Search the available OPTIMADE standard definitions for analogous properties and unit conventions first. Output YAML only.
```

The expected output is one YAML source document. It should not be wrapped in markdown fences and should not include explanatory prose unless the user asks for explanation rather than generation.

## Validation

`skills/optimade-property-yaml/scripts/validate_yaml.py` is a lightweight structural validator. It checks YAML parsing, top-level shape, required fields, `x-optimade-definition.kind: property`, description/title/id strings, and simple `$$inherit` structure inside unit definitions.

It does not prove full semantic validity against all OPTIMADE meta-schema rules. Future integration can call `optimade-property-tools` or the relevant `process_schemas` workflow for complete provider-level validation.

## Distribution

The repository can be distributed on GitHub. If an agent supports direct installation from a GitHub directory URL, use the URL to:

```text
https://github.com/<org>/optimade-property-skill/tree/main/skills/optimade-property-yaml
```

The full OPTIMADE source corpus is better provided through retrieval, a vector store, or initialized submodules than bundled entirely into the skill. The skill should remain small and focused.

## License Notes

This repository uses the MIT License. Curated examples may be inspired by upstream OPTIMADE or definition-provider-template files; review upstream licenses before publishing copied examples verbatim in downstream projects.
