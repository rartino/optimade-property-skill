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

## Inheritance

Use `$$inherit` when reusing a shared definition rather than duplicating a nested schema.

If the inherited target is a reusable standalone definition with its own `$id` and semantic value as an independently addressable definition, inherit it verbatim. Do not combine it with `$$keep`, local overrides, or partial field selection. Such trimming changes the meaning of the referenced definition while preserving its identity, which makes validation and documentation misleading. If a parent property needs stricter presence/absence rules for inherited fields, describe or validate those constraints at the parent level instead.

## Avoid Data-Bearing Dictionary Keys

OPTIMADE property definitions should not rely on dictionary keys as scientific, mathematical, or domain data.
Dictionary keys in a property schema should be fixed field identifiers, not values such as names, labels, numbers, coordinates, external IDs, or category codes.

Do not define a semantic property as a map whose keys are data values, for example:

```yaml
properties:
  "42":
    ...
  "63":
    ...
```

or:

```yaml
properties: {}
description: Values are keyed by object label.
```

Instead, represent the collection as a list of dictionaries and make the former key an explicit field on each item:

```yaml
x-optimade-type: list
type:
- array
items:
  x-optimade-type: dictionary
  type:
  - object
  required: [identifier, value]
  properties:
    identifier:
      x-optimade-type: string
      x-optimade-unit: inapplicable
      type:
      - string
      description: Identifier that was previously used as the dictionary key.
    value:
      ...
```

This makes the data model explicit, validates the former key with the same schema machinery as every other value, and avoids hiding important semantics in JSON object member names.
It also keeps the property compatible with tools that treat dictionary keys as schema structure rather than data.

If consumers need fast lookup by identifiers, recommend a companion index outside the OPTIMADE property definitions.
Such indices may be ordinary JSON dictionaries keyed by data values because they are implementation lookup aids, not semantic OPTIMADE properties.
For example, a data file may expose a list-valued property under its semantic `data` payload and a separate top-level `indices` or provider-specific lookup section that maps identifiers to list positions.
Do not define those lookup indices as OPTIMADE properties unless their keys are fixed schema fields rather than data values.

## Reusable Semantic Definitions

Before writing a property that contains nested dictionaries or repeated object shapes, do a semantic factoring pass.
Look for inner structures that represent the same domain concept in more than one property or file.
When such a concept has a stable name, stable interpretation, and useful standalone documentation, break it out into its own reusable property definition and reference it with `$$inherit`.
This applies even when the concept is normally nested inside larger properties and is not exposed as a top-level entry field.

Good candidates for reusable definitions are structures such as:

- an exact rational number represented as a string, where syntax and exact-arithmetic semantics need to be reused consistently;
- a person, author, instrument, calculation step, provenance record, uncertainty record, markup bundle, or other named concept that carries stable meaning beyond one parent property;
- a nested object with several fields that together form one meaningful concept and recur in several places.

Bad candidates are shapes that are only technically identical but do not have a shared domain meaning.
Do not create reusable definitions named only for shape, such as `three_vector`, `matrix_3x3`, `string_list`, or `object_entry`, unless the user explicitly asks for that abstraction or the shape itself is the scientific quantity being defined.
Instead, keep these structures inline under the outer property and describe their dimensions with `x-optimade-dimensions`.

Prefer names that describe semantics, not implementation details.
For example, names like `provenance_record`, `uncertainty`, or `string_markups` describe reusable concepts; names like `matrix`, `vector`, or `entry` often describe only implementation shape and should usually remain as documented fields inside a more meaningful parent concept.

When choosing where to place a reusable definition:

- Use `core` for domain-independent primitives that can sensibly be reused across unrelated domains, such as exact fraction strings or markup dictionaries.
- Use a shared domain category when the concept is meaningful across several entry types or higher-level properties in that domain.
- Use an entrytype-specific category only when the property is meaningful primarily as an exposed field of that entry type.

A reusable definition does not need to live in the same category as the parent property that uses it.
Choose the category based on the reusable concept's own scope, not on the first parent field where it appears.

Keep parent properties responsible for context.
If the same reusable object is used in two contexts with different required/optional fields, do not alter the inherited definition.
Instead, make the reusable definition broad enough to describe the common object and document context-specific requirements in the parent property.

## Avoid Recursive Property Schemas

Avoid recursive property definitions where a property or nested object directly or indirectly contains another instance of itself.
Even when a JSON Schema dialect can express recursion, recursive shapes are harder to document clearly, harder for schema browsers to render, and harder for generic clients to validate and consume consistently.

If the source data is recursive, first look for a bounded, non-recursive representation that preserves the same semantics.
Common flattening patterns include:

- a registry of primitive objects with stable identifiers;
- fixed-depth rule tables rather than open-ended expression trees;
- lists of dictionaries where references are explicit fields;
- explicit parent, child, target, or rule identifiers instead of nested self-similar objects;
- separate semantic data lists plus non-semantic lookup indices when fast access is needed.

Do not flatten by merely hiding the recursion in data-bearing dictionary keys or unconstrained `properties: {}` maps.
The flattened representation should make every meaningful value an ordinary schema-validated field.

When it is not obvious that the flattened representation is equivalent to the source representation, require a converter or round-trip test before adopting it.
The test should reconstruct the source representation, or otherwise compare source and flattened semantics over the relevant cases.
If users may need to recover the source form, document the reconstruction rule in the property description.

For example, a provider may receive an asymmetric-unit boundary expression as a recursive tree from a source library.
A good OPTIMADE-facing property can instead represent the same information as a bounded set of plane definitions and fixed-depth boundary rule tables, provided a small reconstruction routine or exhaustive test demonstrates equivalence to the source tree.
This is an example of the flattening principle, not a general endorsement of any particular scientific category or provider-specific naming scheme.

## Examples

Include examples when they clarify value shape or units. Keep examples minimal and schema-compatible. Do not add examples if the user explicitly wants a minimal file.

Use curated examples as formatting guides, not only as semantic references. In particular, dictionary-property examples demonstrate the preferred style for markdown key documentation, fixed array dimensions, and exact fraction vectors.

## Do Not Guess

Do not invent physical meaning, provider URLs, enumerations, constraints, allowed ranges, or units. Use placeholders only when the user clearly expects a template.

## Prefer Upstream Patterns

Search curated examples first. Search upstream OPTIMADE source definitions when present. Prefer existing standard names, unit definitions, description style, and schema structure over novel patterns. If several examples conflict, prefer the one closest in semantics and most consistent with current OPTIMADE source style.
