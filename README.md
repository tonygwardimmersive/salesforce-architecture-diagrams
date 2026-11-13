# Salesforce Architecture Diagrams skill

A Claude skill that produces architecture diagrams following the Salesforce Architects
["Salesforce Diagrams" standard](https://architect.salesforce.com/docs/architect/reference-diagrams/guide/introduction.html):
a header with title, description and key; cards with icon, title, attributes and footer; and
elbow connectors with pills and numbered steps.

It covers the six standard diagram types:

| Type | Use it for |
| --- | --- |
| Capability Map | What the business needs and which products deliver it |
| System Landscape | Which systems and clouds exist and how they connect |
| Solution Architecture | How a specific solution works technically |
| Roadmap | What gets delivered when, and the dependencies |
| Interaction / Process Flow | The order of steps or messages in a process |
| Data Model (ERD) | Objects, relationships and cardinality |

Diagrams are written as a JSON spec and rendered to SVG/PNG by `scripts/render_svg.py`. They can
also be pushed into Lucidchart as an editable document.

## Repository layout

```
salesforce-diagrams/           The skill itself (this is what gets installed)
  SKILL.md                     Entry point: workflow, type selection, rules
  references/                  Component standard, diagram types, ERD notation, spec format, Lucid output
  scripts/render_svg.py        JSON spec -> SVG (+ optional PNG)
  assets/examples/             Worked specs with rendered PNGs
salesforce-diagrams.skill      Pre-built zip of the skill, for upload to claude.ai / Claude Desktop
build-skill.sh                 Rebuilds salesforce-diagrams.skill from the folder
salesforce-reference-diagrams/ Source material captured from the Salesforce Architects site (not installed)
```

## Installation

### Claude.ai or Claude Desktop

1. Go to **Settings > Capabilities** and make sure **Code execution and file creation** is on
   (the skill runs a Python script to render diagrams).
2. Under **Skills**, choose **Upload skill** and select `salesforce-diagrams.skill` from this repo.
3. Turn the skill on. Claude will use it whenever you ask for a Salesforce architecture diagram.

If you've changed anything in `salesforce-diagrams/`, rebuild the package first:

```bash
./build-skill.sh
```

### Claude Code

Copy (or symlink) the skill folder into a skills directory.

For your user, available in every project:

```bash
mkdir -p ~/.claude/skills
cp -r salesforce-diagrams ~/.claude/skills/
# or, to pick up edits from this repo automatically:
ln -s "$(pwd)/salesforce-diagrams" ~/.claude/skills/salesforce-diagrams
```

For a single project, shared with anyone who clones it:

```bash
mkdir -p /path/to/project/.claude/skills
cp -r salesforce-diagrams /path/to/project/.claude/skills/
```

Restart Claude Code (or start a new session), then check it's listed with `/skills`.

### Rendering dependencies

The renderer only needs Python 3's standard library to produce SVG. For PNG output it needs one of:

- `cairosvg` (`pip install cairosvg`)
- `rsvg-convert` (e.g. `apt install librsvg2-bin` or `brew install librsvg`)
- Inkscape

Without any of these, the SVG is still written and the script exits with code 2.

## Usage

Just ask Claude for a diagram, for example:

> Draw a Salesforce-standard process flow for an order placed on Commerce Cloud being sent to SAP via MuleSoft.

> Create a system landscape for a single Sales Cloud + Service Cloud org integrated with Marketing Cloud and an ERP.

> Give me an ERD for Account, Contact, Opportunity and a custom Project__c object.

Claude writes a spec, renders it, reviews the image, and iterates until it reads cleanly. To ask
for an editable Lucidchart version, say so (requires the Lucid connector).

You can also run the renderer directly:

```bash
python3 salesforce-diagrams/scripts/render_svg.py \
  salesforce-diagrams/assets/examples/process-flow.json out.svg --png out.png
```

See `salesforce-diagrams/references/spec-format.md` for the spec format.

## Attribution

The diagram standard, and the material in `salesforce-reference-diagrams/`, come from
[Salesforce Architects reference diagrams](https://architect.salesforce.com/docs/architect/reference-diagrams/guide/introduction.html).
The skill does not include Salesforce product logos; use the official Lucid shape library if you need them.
