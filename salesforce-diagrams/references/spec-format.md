# Diagram Spec Format (for scripts/render_svg.py)

A single JSON object. All coordinates are pixels in the **body** area (y=0 is just below the header). Worked examples: `assets/examples/process-flow.json`, `assets/examples/capability-roadmap.json`.

```json
{
  "type": "interaction-process-flow",
  "width": 1400,
  "header_gap": 40,
  "header": { ... },
  "timeline": { ... },
  "cards": [ ... ],
  "connectors": [ ... ]
}
```

## header

| Field | Notes |
| --- | --- |
| `title` | Required. |
| `description` | One to three sentences: purpose, scope, message. |
| `logo` | Optional text for the logo placeholder (e.g. company name). |
| `title_size` | Default 30. The description is automatically at least half this size. |
| `key` | List of items: `{"icon": {"glyph": "S", "colour": "sync"}, "label": "Synchronous"}` or `{"line": "solid" | "dashed" | "dotted", "colour": "#...", "label": "Publish"}`. |
| `key_columns` | Optional; otherwise chosen automatically. |

The header grows to fit its text and key.

## cards

| Field | Notes |
| --- | --- |
| `id` | Required, unique. Used by connectors. |
| `x`, `y`, `w`, `h` | Required. Absolute body coordinates, including nested cards. If content doesn't fit, `h` is increased and a warning printed; re-check the layout. |
| `title` | Required. |
| `icon` | `"SF"` or `{"glyph": "SF", "colour": "platform"}`. Colour is a palette name (platform, sales, service, marketing, commerce, data360, industries, slack, mulesoft, external, sync, async) or a hex value. |
| `attributes` | List of strings, one per line (long lines wrap). |
| `footer` | Text in the grey footer band. |
| `footer_icons` | List of icons as above. |
| `nested` | `true` for cards inside a container: thinner border, smaller title, drawn above containers. |
| `layer` | Optional draw order override (higher = on top). |
| `fill`, `stroke`, `stroke_width`, `radius` | Styling overrides. |
| `border` | `"dashed"`, `"dotted"` or `"none"` (useful for ERD subtype and virtual entity styles). |
| `title_rule` | `false` hides the grey rule under the title. |
| `title_size`, `attr_size`, `icon_r` | Size overrides. |

Containers are ordinary cards; place nested cards inside their bounds with about 24px padding and leave room under the container's title (about 130px if it has an icon and attributes, about 60px if it has a title only).

## connectors

| Field | Notes |
| --- | --- |
| `from`, `to` | Card ids. |
| `from_side`, `to_side` | `left`, `right`, `top`, `bottom`. Auto-chosen from relative positions if omitted. |
| `from_port`, `to_port` | 0-1 position along that side (default 0.5). Use different values to separate parallel connectors. |
| `straight` | `true` forces a straight line (the target port aligns to the source). |
| `via` | x (for left/right sides) or y (top/bottom) of the elbow's middle segment; give several connectors the same `via` for a clean fan-in/fan-out. |
| `style` | `solid` (default), `dashed`, `dotted`. |
| `arrow` | `end` (default), `start`, `both`, `none`. |
| `colour` | Palette name or hex (keyed if used). |
| `label` | Pill text; use `\n` for two lines. Placed on the longest segment. |
| `step` | Number for a circular step pill (process flows). Overrides `label`. |
| `label_pos` | 0-1 position of the pill along its segment (default 0.5). |

## timeline (roadmaps)

```json
"timeline": {"columns": ["Q1","Q2","Q3","Q4"], "label_w": 110, "header_h": 60,
             "lanes": [{"label": "Sales", "h": 420}, {"label": "Service", "h": 300}]}
```

The grid starts at body x=40, y=0. Column width = (width - 80 - label_w) / number of columns. Place each card's `x` and `w` to span its dates, and its `y` within the lane (the first lane starts at `header_h`).

## Layout tips

- Process flow: participants about 320px wide with about 180px gaps, so pills fit on the connectors.
- Capability map: bands as full-width containers about 24px apart; child cards in equal widths.
- Keep the outer margin 40px. Width 1400 suits most slides; use 1800+ for dense landscapes.
- After rendering, view the PNG; fix any warning and any connector passing through a card.
