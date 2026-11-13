# Getting Diagrams into Lucidchart

Salesforce recommends Lucidchart for architecture diagrams and publishes its shape library and gallery templates there. This skill reaches Lucid in three ways, in order of preference.

## 1. SVG conversion (default for all non-ERD types)

1. Render the spec with `scripts/render_svg.py` and check the PNG.
2. Pass the SVG file's contents **unchanged** to the Lucid SVG conversion tool (`lucid_convert_svg_to_diagram`) with a title matching the header title. Don't simplify or rewrite the SVG first; the converter needs the original.
3. Share the returned link. Mention that the converter approximates some styling, so the user should glance over rounded corners, dashed pill outlines and clipped footer bands.

Result: an editable Lucid document with the same layout, but built from generic shapes, not the Salesforce library shapes.

Lucid connector tools are third-party app tools. If the user hasn't already chosen Lucid in the conversation, offer it rather than assuming.

## 2. Lucid ERD tool (data models)

Use `lucid_create_erd` for data models: real, editable ERD tables with crow's foot lines. Map the spec as described in `data-model-notation.md`. Licence colouring and the master-detail diamond need a manual pass afterwards.

## 3. Starting from an official Salesforce template (highest fidelity)

When the user wants the genuine Salesforce shapes and logos:

1. The user opens the matching gallery template with "Open in Lucidchart" on the Salesforce Architects page, which copies it into their Lucid account. Alternatively, they enable the Salesforce shape library in Lucid.
2. Find it with the Lucid search tool, read its structure with `fetch`, and use the content as the starting point or as a style reference (colours, sizes, spacing).
3. Generate the new diagram content and tell the user which template elements to reuse.

Known Lucid quirk (from the Salesforce guide): in diagrams created from a template, footer icons can come undocked from their card and must be dragged back into the centre of the footer.

## Open question to verify on first use

It hasn't been confirmed whether generated Lucid documents can reference shapes from the Salesforce shape library directly. Until it is, treat output as "styled to match" rather than "built from library shapes", and say so.
