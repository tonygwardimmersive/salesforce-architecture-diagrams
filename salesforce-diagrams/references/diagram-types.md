# Diagram Types

The six types in the Salesforce reference gallery, with the layout pattern observed in the gallery examples and a checklist for each. All types use the standard header and cards.

## Contents
1. Capability Map
2. System Landscape
3. Solution Architecture
4. Roadmap
5. Interaction / Process Flow
6. Data Model (ERD)

---

## 1. Capability Map

**Purpose:** shows the product mix and key capabilities in a solution, focused on business drivers, functionality and value rather than integration detail. Gallery examples: Business Capability Map, Data 360 Technical Capability Map, Loyalty Management Capability Map, Center of Excellence.

**Layout pattern:** full-width horizontal container bands stacked top to bottom, each holding a row of equal-width child cards.

- Band 1, **Business Drivers**: collapsed cards (title only), e.g. Revenue Growth, Customer Retention.
- Band 2, **Business Capabilities**: cards with a title and two to four attribute lines.
- Band 3, **Platform / Products**: a container (e.g. "Salesforce Platform") whose left column lists shared platform traits as attributes, holding detailed product cards (icon, title, attributes), with a "Platform Services" footer and footer icons along the bottom.
- The key lists the product icons used.

**Checklist:** reads top (why) to bottom (how); 4-6 cards per band; each capability traceable to at least one product card; no connectors needed (positioning conveys the mapping) unless a specific dependency must be called out.

## 2. System Landscape

**Purpose:** shows the products and technical systems involved in an implementation, their specific aspects, and the connections between them. Gallery examples: Data 360 Marketing, Einstein, Retail, Salesforce Role Hierarchy, Single-Org Architecture.

**Layout pattern:**

- Salesforce org(s) as large containers in the centre; clouds and major features as nested cards inside.
- External systems grouped by kind in containers to the left (sources) and right (targets), or above (channels/users) and below (data/back office).
- Connectors are fewer and higher-level than in a solution architecture; a short pill may name the integration style.
- Org-strategy variants (single org, multi-org, hub and spoke) show each org as its own container.

**Checklist:** every system the client named appears exactly once; boundaries (org, cloud vendor, on-premise) are containers; data direction is clear; detail kept to "what connects to what".

## 3. Solution Architecture

**Purpose:** detailed view of the products and technologies in a solution, focused on how they connect and communicate. Gallery examples: AWS + Data 360, Customer Zero Implementation, Data 360 Actions & Activations, Loyalty Management.

**Layout pattern:**

- A central hub card (e.g. "Data 360 Home Org") with nested feature cards.
- Sources on the left and bottom, consumers/targets on the right and top.
- Every connector carries a **pill** naming the mechanism ("Zero Copy (Query & File Federation)", "Out of the box connector", "Ingestion API + MuleSoft", "Data Action").
- Small inline glyphs beside connector endpoints can mark cadence (batch, streaming, real-time) when explained in the key.
- Connector colour may separate Salesforce-owned from third-party paths (keyed).

**Checklist:** every connector has a pill; protocol/auth/cadence shown where it matters to the decision; sync vs async visually distinguished; no step numbers (use a process flow for sequence).

## 4. Roadmap

**Purpose:** plan and visualise implementation of capabilities, components, features or systems over time, showing order, dependencies and priorities. Gallery examples: Capability, Component, Feature and System Roadmaps; Agentforce Release Plan; Agentforce Roadmap.

**Layout pattern** (use the renderer's `timeline`):

- Time columns across the top (quarters, sprints, releases), with alternating light grey column fills.
- Lanes down the left (business area, cloud, team, workstream).
- Each item is a card spanning its time window horizontally, placed within its lane. Attributes give dates and "Dependencies: ...". Footer icons tag value themes (efficiency, retention, revenue, AI) and are keyed.
- Optional dependency connectors between cards (elbow, arrow to the dependent item).

**Checklist:** card left/right edges match dates; dependencies stated; lanes not overcrowded (stagger vertically); key explains value-theme icons.

## 5. Interaction / Process Flow

**Purpose:** captures the time-based steps, data flows or interactions supporting a process, with numbered sequencing. Gallery examples: Asynchronous Processing via Platform Events, Claim Check, Customer Personalization Flow, External Integrations via HTTP, Hospitality Loyalty Management Process, Queuing.

**Layout pattern:**

- Participants as tall cards arranged left to right in order of first involvement.
- Sub-components (events, queues, objects, flows) as nested cards inside participants, so connectors attach to the specific component.
- Numbered pills (1, 2, 3...) on connectors. Return paths run right to left on a lower or upper track.
- Sync/async context shown via footer icons or line style, explained in the key.
- Fan-in/fan-out (e.g. events 1..n to one subscriber) uses a shared elbow junction (`via` in the spec).

**Checklist:** numbers follow reading order wherever possible; each number is explained in the description, an attribute or an accompanying table; no unnumbered connectors except a clearly keyed return or callback; error and retry paths drawn dashed or in a separate diagram.

## 6. Data Model (ERD)

**Purpose:** entities (objects), relationships and concepts for a metadata implementation.

**Layout pattern:** see `data-model-notation.md`. In short: rounded entity boxes with logical name and API name; crow's foot notation with optionality marks; master-detail shown with a diamond; colour by licence relative to the focus cloud; straight horizontal or vertical relationship lines; consistent crow's foot orientation throughout.

**Rendering:** when Lucid is the target, use Lucid's ERD tool (it produces real ERD shapes). Otherwise the SVG renderer can approximate an ERD with entity cards and connectors, but crow's foot endpoints are not drawn; label cardinality in pills ("1 : N", "master-detail") and say so to the user.
