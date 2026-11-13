# Standard Components

Distilled from the Salesforce Architects "How to Build Salesforce Diagrams" and "Standard Components" guides, plus measurements taken from the reference gallery images.

## Header

Present on every diagram.

- **Title**: short and instantly understandable. Renderer default 30px, navy `#032D60`.
- **Description**: one to three sentences on what the diagram covers, its purpose and scope. Font size at least half the title's (renderer: 15px), same navy.
- **Logo** (optional): the author's logo or company name, top-left above the title.
- **Key** (optional but usually needed): explains any icon, colour or line style that isn't labelled on the diagram itself. Arrange items in even rows. Sits in a white rounded panel on the right.
- **Size**: at least 10% of the total diagram height and the full width.
- **Look**: white area on the left with a large curved edge, light grey (`#E5E5E5`) band on the right, white key panel inside the grey.

## Cards

Every property (system, cloud, concept, capability, step, entity) is a card: a white or tinted rounded rectangle.

Anatomy, top to bottom (only the title is required):

1. **Card icon**: circular icon disc top-left representing the property.
2. **Card title**: bold, beside the icon, with a light grey rule beneath it extending to the card's right edge.
3. **Card attributes**: a plain list of details (features, objects, settings), one per line, no bullets.
4. **Card footer**: a full-width light grey band with centred text giving an extra characteristic (package/object/API name, owner, environment, capability grouping).
5. **Card footer icons**: a centred row of small icon discs below the footer (channels, shared services, capabilities). Every footer icon must be explained in the key.

Common variations:

- **Collapsed card**: title only, or title with rule. Used for simple items or nested children.
- **Detailed card**: icon, title and attributes.
- **Detailed card with footer**: adds footer and footer icons.

Sizing and colour: resize cards freely to keep connectors straight and to signal importance. Fill may be transparent/white or coloured to distinguish types (explain colour meaning in the key).

Measured styling (reference gallery):

- Outer cards: near-black border (`#181818`), about 2.5px, corner radius about 16px.
- Nested cards: thinner border (about 1.5px), radius about 12px.
- Kit-of-parts sample border: grey-50 `#747474`. Either is acceptable; be consistent within a diagram.
- Title rule and footer band: grey-90 `#E5E5E5`. Alternative mid grey: grey-80 `#C9C9C9`.

## Containers

Cards can contain other cards to show hierarchy, boundaries or classification (for example an "External Systems" card holding Data Lakes, Warehouses, Microservices). A container is a normal card with its title at the top-left and children laid out in a row or grid inside it. Nesting can go several levels deep (Org > Cloud > Feature), but stop at three for readability.

## Icons

- Use Salesforce product logos for products and the Lightning Design System icon set for other concepts.
- When real logos are unavailable (the default for generated output), use solid colour discs with a 1-3 character white glyph, coloured by product family (see palette below), and include them in the key.
- Footer icons always appear in the key.

## Connectors

- Always **elbow (orthogonal)** routing; keep lines straight wherever the layout allows. Avoid crossing lines; reroute or move cards instead.
- A connector represents a relationship, integration or process step between two cards.
- **Line style carries meaning** and must be in the key. A common convention from the gallery: solid line = synchronous / publish / call; dashed line = asynchronous / subscribe / callback.
- **Endpoints** show direction for integration and process connectors (arrowheads; double-ended for bidirectional). On relationship connectors endpoints show cardinality and optionality (crow's foot, circle, bar).
- Connector colour can distinguish ownership (for example blue = Salesforce, black = others) if keyed.

## Pills

Rounded capsules sitting on a connector that name what passes along it: message or payload ("Event A Message Header"), mechanism ("Zero Copy (Query & File Federation)", "REST / OAuth 2.0"), or action ("Data Activation"). A pill on a dashed connector gets a dashed outline. In process flows, **numbered circular pills** (1, 2, 3...) give the sequence, and the description or attributes explain each step.

## Palette

Neutral system (Salesforce colour numbers, 0 = black, 100 = white):

| Use | Value |
| --- | --- |
| Header title and description text | Navy `#032D60` |
| Card text | `#181818` |
| Card border | `#181818` (gallery) or grey-50 `#747474` (kit) |
| Rules, footer band, header band | grey-90 `#E5E5E5` |
| Alternate fill | grey-80 `#C9C9C9` |
| Timeline alternating column | `#F3F4F6` |

Icon disc colours (approximations of Salesforce product colours, sampled from gallery images; replace with official values if the brand team supplies them):

| Family | Hex |
| --- | --- |
| Platform / Agentforce / general Salesforce | `#032D60` |
| Sales | `#0B827C` |
| Service | `#A0094F` |
| Marketing | `#DD7A01` |
| Commerce | `#04844B` |
| Data 360 (Data Cloud) | `#2E0B3B` |
| Industries | `#5A1BA9` |
| Slack | `#4A154B` |
| MuleSoft | `#00A0DF` |
| External / third party | `#3E3E3C` |
| Synchronous context marker | `#F38151` |
| Asynchronous context marker | `#6E9AE0` |

## Accessibility

- Text-to-background contrast at least 4.5:1 (WCAG AA).
- Using colour numbers, keep text and background at least 50 points apart (background 90 means text 40 or lower). Apply the same rule to borders where they carry meaning.
- Never rely on colour alone: pair it with line style, a label or an icon in the key.
- Export to PDF where screen-reader access matters; the SVG `<title>` and `<desc>` carry the header text.
