# Authoring Rules

## File Naming

Use `<property_name>.yaml` unless the project has a provider-specific prefix convention. Property names should be lowercase snake_case unless an upstream convention says otherwise. Do not change user-provided canonical names without reason.

## `$id`

Use the project or provider URL pattern if supplied by the user. If no provider URL is supplied, use a clear placeholder pattern and avoid claiming it is final. Keep `$id`, filename, and `x-optimade-definition.name` consistent.

## Field Ordering

Recommended top-level order:

1. `$$schema`
2. `$id`
3. `title`
4. `$comment`
5. `x-optimade-type`
6. `x-optimade-definition`
7. `x-optimade-unit`
8. `x-optimade-unit-definitions`
9. `type`
10. `items`
11. `description`
12. `examples`

Omit fields that are not relevant. Keep nested definitions readable and use the same ordering where practical.

## `x-optimade-definition`

Required nested keys:

- `kind: "property"`
- `version`
- `format`
- `name`
- `label`

The `name` should be the canonical property name. The `label` should be stable and provider-specific when applicable. In provider definitions, labels commonly combine property name, provider or namespace, and entrytype context.

## `title`

Use a human-readable title. Do not simply copy the snake_case property name unless that is genuinely the clearest title.

## `description`

Use precise, normative language. Use YAML block scalars for long descriptions. State units and interpretation clearly. Mention relationships to other properties only when known.

Use YAML's `|-` block-scalar style for all multi-line descriptions. Prefer one sentence per source line, even within the same paragraph, because this makes source diffs readable and avoids rewriting whole paragraphs for small textual edits. Preserve blank lines between conceptual paragraphs and section headings.

For dictionary properties, include a `**Requirements/Conventions**` section. Describe the dictionary itself with the exact sentence `It MUST be a dictionary with the following keys:` and then document each key as a markdown sublist item in this form:

```markdown
- It MUST be a dictionary with the following keys:

    - **field_name**: REQUIRED; Type phrase.
      Explanation sentence.
      Additional explanation sentence when needed.

    - **optional_field**: OPTIONAL; Type phrase.
      Explanation sentence.
```

Use `REQUIRED` or `OPTIONAL` explicitly. Give the value type immediately after the semicolon, e.g. `String.`, `Boolean.`, `Integer 3x3 matrix.`, `List of 3 Integers.`, or `List of 3 Fractions (String).` Keep follow-up explanation lines indented under the same field item. Escape underscores in markdown field names where needed, e.g. `**rot\_type**`.

## `x-optimade-type`

Choose the OPTIMADE type from the property shape:

- Use `string`, `integer`, `float`, `boolean`, or `timestamp` for scalar values.
- Use `list` for arrays and include `items` definitions.
- Use `dictionary` for object-like mappings and include `properties` or describe the mapping clearly.
- For nested arrays, each list level should have its own `x-optimade-type`, JSON Schema `type`, `x-optimade-unit`, and `items` where applicable.
- Use `x-optimade-dimensions` for arrays with known semantic dimensions. Provide both `names` and `sizes`, e.g. a 3-vector should use `names: ["dim_lattice"]` and `sizes: [3]`, and a 3 by 3 matrix should use `names: ["dim_lattice", "dim_lattice"]` and `sizes: [3, 3]`.

Keep `x-optimade-type` aligned with JSON Schema `type` and `items`. Typical mappings are `float` to `number`, `integer` to `integer`, `string` to `string`, `boolean` to `boolean`, `list` to `array`, and `dictionary` to `object`. Include `null` in `type` only when the provider convention allows unknown or unavailable values.

Represent exact fractional vectors as lists of fraction strings, not as one comma-separated string. For example, use `["0", "0", "1/4"]` for a 3-vector of fractions. Describe this shape as `List of 3 Fractions (String).`

## Units

Use `x-optimade-unit` only for physical quantities with clear units. Use `dimensionless` for dimensionless quantities and `inapplicable` when a unit does not apply. Use `x-optimade-unit-definitions` when a unit needs definition or inherited definition.

Use `$$inherit` only when an appropriate inherited unit definition exists in the examples or upstream sources. Do not invent unusual units. If no trusted unit definition is available, use conservative wording and ask for the provider's preferred unit source when necessary.

## Examples

Include examples when they clarify value shape or units. Keep examples minimal and schema-compatible. Do not add examples if the user explicitly wants a minimal file.

Use curated examples as formatting guides, not only as semantic references. In particular, `_exmpl_symop.yaml` demonstrates the preferred style for dictionary properties, markdown key documentation, fixed array dimensions, and exact fraction vectors.

## Do Not Guess

Do not invent physical meaning, provider URLs, enumerations, constraints, allowed ranges, or units. Use placeholders only when the user clearly expects a template.

## Prefer Upstream Patterns

Search curated examples first. Search upstream OPTIMADE source definitions when present. Prefer existing standard names, unit definitions, description style, and schema structure over novel patterns. If several examples conflict, prefer the one closest in semantics and most consistent with current OPTIMADE source style.
