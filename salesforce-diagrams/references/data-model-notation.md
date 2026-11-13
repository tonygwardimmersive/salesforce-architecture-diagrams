# Data Model (ERD) Notation

Summary of the Salesforce data model diagram conventions used in the official product data model gallery. Entities usually map to Salesforce objects.

## Entities

- Rounded-corner boxes with two labels: the **logical name** (often the object's singular label) and the **API name**. Managed-package API names usually omit the namespace; the suffix shows the type: `__c` custom object or setting, `__mdt` custom metadata, `__x` external object.
- Optional representative attributes: `#` marks part of the logical unique key; `•` marks a non-key attribute.

### Entity styling by licence (relative to the focus cloud)

| Style | Meaning |
| --- | --- |
| Focus-cloud brand colour | Object comes with the focus cloud's licence |
| White fill, black border | Object from a different licence, not extended by the focus cloud (e.g. Account, Contact on a Sales/Service ERD) |
| Light grey fill, black border | Object from a different licence that the focus cloud extends (extra fields, relationships, record types) |
| No border | Virtual entity: logically present but not a physical object (accessed via API or Salesforce Connect) |
| Dashed border | Subtype implemented as a record type |
| Dotted border | Purely logical subtype (no record type or separate object) |

Industry clouds share one Industry colour scheme.

### Subtypes

Subtypes sit inside their supertype box. The supertype holds common attributes and relationships; subtypes hold specific ones. Subtypes are mutually exclusive (a record is exactly one subtype) and can nest. Border style shows implementation: solid = a real separate object tracks it; dashed = record type; dotted = logical only.

## Relationships

- **Cardinality**: a crow's foot at an end means many on that end; no crow's foot means at most one.
- **Master-detail (parent-child)**: a UML-style diamond on the singular (master) end. The detail is cascade-deleted with the parent and inherits its visibility. Lookups have no diamond.
- **Optionality**: marked at the end next to the cardinality mark.
  - Many end: almost always a circle (zero or more).
  - Singular end, circle + bar: optional (zero or one).
  - Singular end, double bar: required (exactly one).
  - The diagram may show a logically required relationship that is physically optional (e.g. Contact to Account ignoring private contacts); use this sparingly.
- **End names**: verb phrases at each end ("part of" / "made up of") so each relationship reads as a sentence in both directions: "Each Contact must be primarily a contact for one and only one Account" / "Each Account may be primarily represented by one or more Contacts."
- **Colour**: relationships added by the focus cloud are coloured; black lines come with another licence.
- **Recursive relationships**: drawn as a curved line from an entity back to itself.
- **Mutually exclusive relationships**: an arc across several relationship lines means only one applies to any occurrence. A broken line passing through the arc is not part of it.

## Layout conventions

- Relationship lines straight, horizontal or vertical; diagonal only when unavoidable.
- Resize entity boxes (taller or wider) to give relationships straight landing points; heavily related entities end up larger, which signals importance.
- Keep crow's feet consistently on one orientation across the whole diagram:
  - **Upside-down layout**: crow's feet on the left/top, so child entities sit above or left of parents and the most specific entities land top-left.
  - **Right-side-up layout**: crow's feet on the right/bottom, so parents sit top-left and children below or right.

## Rendering guidance

- **Lucid target**: use the Lucid ERD tool with entities (id, name, attributes with `PK` on keys) and relationships (from, fromAttribute, to, toAttribute, fromCardinality, toCardinality, label). Use `exactlyOne` for required lookups and master-detail, `zeroOrOne` for optional lookups, `zeroOrMore` on the child side. Lucid's ERD shapes don't show licence colouring or the master-detail diamond, so tell the user these need a manual pass.
- **SVG target**: entity cards with the logical name as title and the API name as the first attribute; relationships as connectors with pills stating cardinality and type ("N : 1 lookup", "N : 1 master-detail"). Note that crow's foot glyphs aren't drawn by the renderer.
