# Expected Shape Notes

A generated `band_gap` response should be one YAML document. It should define a property with `x-optimade-definition.kind: property` and `x-optimade-definition.name: band_gap`.

The `type` and `x-optimade-type` fields should align. Since the prompt asks for a scalar electronic band gap, a float/number shape is expected unless the user requests a different representation.

Unit information should be present and should use eV/electronvolt conventions if supported by the available examples or upstream sources.

The output should not include standards, entrytypes, response schemas, markdown fences, or explanatory prose.
