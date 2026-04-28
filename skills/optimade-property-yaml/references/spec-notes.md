# Specification Notes

This skill targets OPTIMADE property-definition source YAML files, not the published JSON form. OPTIMADE property definitions are based on JSON Schema concepts extended with OPTIMADE-specific metadata such as `x-optimade-type`, `x-optimade-definition`, units, dimensions, and implementation annotations.

Source YAML files may include authoring features that are later processed into published JSON, including `$$schema`, `$$inherit`, and local inheritance paths used by definition-provider tooling. Published schema-browser JSON examples are useful conceptually, but they are not the formatting target for this skill.

Generate only one property definition at a time. Do not generate standards, entrytypes, response schemas, provider indexes, or packaged archives unless the user explicitly asks outside this skill's core scope.

Formatting should primarily follow source YAML examples from the OPTIMADE repository and definition-provider-template style repositories. Standard definitions, units, dimensions, and descriptions should be reused or mirrored where appropriate.

If upstream references are unavailable, rely on the curated examples in this skill and use conservative generic patterns. Prefer a correct minimal definition over a detailed definition with invented semantics.
