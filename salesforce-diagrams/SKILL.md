---
name: salesforce-diagrams
description: Produces architecture diagrams that follow the Salesforce Architects "Salesforce Diagrams" standard (Header with title, description and key; Cards with icon, title, attributes, footer and footer icons; elbow Connectors with Pills and numbered steps). Covers the six standard diagram types - Capability Map, System Landscape, Solution Architecture, Roadmap, Interaction/Process Flow, and Data Model (ERD) - and renders them to SVG/PNG or to an editable Lucidchart document. Use this skill whenever the user asks for a Salesforce architecture diagram, integration or process flow, system landscape, solution design visual, capability map, roadmap, data model/ERD, or wants an existing diagram made "Salesforce standard" or "Architect Centre style", even if they don't mention the standard by name. Also use it for diagrams going into an SDD, proposal, SOW or design review.
---

# Salesforce Diagrams

Generate diagrams that look and read like the Salesforce Architects reference gallery. The standard is about communication first: one clear message per diagram, read left-to-right and top-to-bottom, built only from the standard components.

## Workflow

1. **Pin the message and audience.** Write one sentence stating what the diagram must convey and to whom. Anything not needed for that message is left out; if two messages compete, plan two diagrams. Ask only if the subject is genuinely unclear; otherwise state assumptions in one line.
2. **Pick the diagram type** using the table below, then read `references/diagram-types.md` for that type's layout pattern.
3. **Read `references/standard-components.md`** before composing. It defines the header, card anatomy, connectors, pills, key, palette and accessibility rules. For ERDs read `references/data-model-notation.md` instead of (or as well as) the components file.
4. **Write the spec** as JSON per `references/spec-format.md`. Lay out on a grid: columns ~480px apart for flows, 20-24px padding inside containers, nothing overlapping.
5. **Render and look at it:**
   ```bash
   python scripts/render_svg.py spec.json out.svg --png out.png
   ```
   (Use `python3` if `python` isn't on PATH.) The PNG needs `cairosvg`, `rsvg-convert` or Inkscape; if none is available the script says so and exits 2, but the SVG is still written, so view that instead or install `cairosvg` with pip.
   View the PNG. Fix overlaps, crossing connectors, cramped pills and any "card grown" warnings (they mean content didn't fit and neighbours may now overlap). Iterate until it reads cleanly.
6. **Deliver** in the format the user wants (see Output targets). Default: present the SVG and PNG.

## Choosing the diagram type

| The message is about... | Type | Key trait |
| --- | --- | --- |
| What the business needs and which products deliver it | Capability Map | Stacked bands: drivers, capabilities, platform/products |
| Which systems/clouds exist and how they connect | System Landscape | Systems as cards, grouped by org/boundary, light connectors |
| How a specific solution works technically | Solution Architecture | Detailed connectors with pills naming the mechanism |
| What gets delivered when, and dependencies | Roadmap | Time columns x lanes, cards spanning time |
| The order of steps/messages in a process | Interaction / Process Flow | Numbered step pills, explicit direction |
| Objects, relationships, cardinality | Data Model (ERD) | Entity boxes, crow's foot, focus-cloud colouring |

## Rules that are easy to get wrong

- Every diagram has the **Header**: clear title, a description at least half the title's font size, and a **Key** whenever icons, colours or line styles aren't self-labelled. The header is at least 10% of the height and full width.
- **Every property is a Card.** Only the title is mandatory; add attributes, footer and footer icons only when they carry information. Cards may nest to show grouping or containment.
- **Connectors are elbowed (orthogonal) and straight wherever possible.** Line style must mean something and appear in the key. Use **pills** to name what flows (e.g. "Order Event", "REST / OAuth 2.0"); use **numbered pills** for sequence in process flows.
- **Contrast**: text-to-background contrast of at least 4.5:1. Using the Salesforce colour numbers, background and text should be 50+ points apart.
- Don't use real Salesforce product logos unless the user supplies them; use coloured icon discs with short glyphs and explain them in the key. Point the user to the official Lucid shape library if they want the real logos (see `references/lucid-output.md`).
- For client work, use the client's real system names and integration patterns. Never invent endpoints, volumes or SLAs; leave a placeholder attribute such as "Volume: TBC" instead.

## Output targets

- **SVG + PNG (default):** run the renderer and present both. SVG is editable in draw.io, Figma or Visio import; PNG is for slides and documents.
- **Lucidchart (editable):** see `references/lucid-output.md`. In short: pass the rendered SVG unchanged to the Lucid SVG-conversion tool; for ERDs use Lucid's ERD tool directly.
- **Inside a deck or document:** embed the PNG. If the user's brand styling skill applies (for example a company brand skill), keep the Salesforce diagram conventions for the diagram itself and apply brand styling only to the surrounding slide or page.

## Reference files

- `references/standard-components.md`: header, card anatomy and variations, containers, icons, connectors, pills, key, palette, accessibility.
- `references/diagram-types.md`: layout pattern and checklist for each of the six types.
- `references/data-model-notation.md`: ERD notation (entity styles, crow's foot, optionality, master-detail diamond, subtypes, layout conventions).
- `references/spec-format.md`: the JSON spec the renderer accepts, with field-by-field notes.
- `references/lucid-output.md`: how to get diagrams into Lucidchart and the known limitations.
- `assets/examples/`: worked specs (process flow, roadmap) to copy from.
