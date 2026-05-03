---
name: optimade-property-yaml
description: Generate one OPTIMADE property-definition source YAML file in the definition-provider/source-schema format. Use for drafting or revising property YAML only; do not use for standards, entrytypes, or published JSON definitions.
---

# OPTIMADE Property YAML

## Purpose

This skill creates source YAML files for OPTIMADE property definitions. The output is intended for definition-provider style repositories and OPTIMADE property tooling. The output is not the published JSON schema page.

## Scope

- Generate one property-definition YAML file.
- Do not generate standards, entrytypes, response schemas, or packaged archives.
- Do not convert to JSON unless explicitly requested.

## Workflow

1. Read `references/spec-notes.md`.
2. Read `references/authoring-rules.md`.
3. Inspect curated examples in `references/examples/`.
4. Before drafting, identify whether the requested property contains nested objects that should be represented by existing reusable semantic definitions, or by a new reusable semantic definition.
5. When available, consult `external/OPTIMADE` for standard source YAML definitions.
6. When available, consult `external/optimade-property-tools` for tooling conventions.
7. Start from `assets/starter-property.yaml`.
8. Draft a single source YAML document.
9. If writing to disk, run `scripts/validate_yaml.py` on the generated file.
10. Return only the YAML document when asked to generate a file inline.

## Retrieval And Reference Behavior

- Prefer standard OPTIMADE definitions over invented patterns.
- Prefer provider-template source YAML examples for formatting.
- Use curated examples first.
- Use upstream submodules as supplemental references when present.
- If a close standard analogy is found, mirror its structure and style where appropriate.
- If no close analogy is found, use the starter template and explicitly conservative wording.

## Required Conventions

- `x-optimade-definition.kind` must be `property`.
- `x-optimade-definition.name` must match the intended property name.
- `x-optimade-definition.label` must follow the chosen label convention from `authoring-rules.md`.
- `x-optimade-type` must match the declared property shape.
- `description` must be normative, precise, and style-consistent with OPTIMADE examples. For multi-line descriptions, use YAML `|-` block scalars and prefer one sentence per source line.
- Dictionary properties should document keys under `**Requirements/Conventions**` using `It MUST be a dictionary with the following keys:` and markdown subitems that state REQUIRED/OPTIONAL, type, and explanation.
- Prefer reusable common properties for nested structures that have semantic identity across multiple fields. Such reusable definitions should be broken out even when they are used inside another property rather than exposed directly as top-level entry fields.
- Do not factor out nested definitions merely because they share the same JSON shape. A generic 3-vector, 3x3 matrix, or list-of-strings should usually remain inline unless the field name and domain semantics make it an independently meaningful concept.
- Do not use dictionary keys to carry domain data. If a collection is conceptually keyed by values such as identifiers, labels, numbers, names, or coordinates, model it as a list of dictionaries where the former key is an explicit field in each item.
- If fast lookup by such values is needed, recommend a separate index structure outside the OPTIMADE property definitions. Index dictionaries may use data-bearing keys because they are implementation lookup aids, not semantic properties.
- Use `x-optimade-dimensions` for fixed-size arrays and matrices when dimensions are known.
- Represent exact fractional vectors as lists of fraction strings, not comma-separated strings.
- Use `x-optimade-unit` and `x-optimade-unit-definitions` only when semantically justified.
- Use `$$inherit` only when there is a clear upstream pattern to inherit from.
- When inheriting a reusable standalone definition that has its own `$id` and semantic value as a definition, inherit it verbatim. Do not alter it with `$$keep`, local overrides, or partial field selection; validation rules that depend on higher-level context should be handled at the higher level.

## Output Rules

- Output valid YAML only.
- Do not wrap output in markdown fences.
- Do not include prose before or after the YAML.
- Do not include comments in generated YAML unless the user explicitly asks for comments.
- Do not invent semantics, units, or constraints that were not supplied or strongly implied.

## Self-Check

- Confirm required fields are present.
- Confirm top-level field ordering follows `authoring-rules.md`.
- Confirm `kind: property`.
- Confirm type information is internally consistent.
- Confirm units, if present, are consistent with the property description.
- Confirm the filename, property name, label, and `$id` are mutually consistent where enough context is available.
