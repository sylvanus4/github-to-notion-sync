# Slack Canvas Markdown Specification

Slack Canvas uses its own markdown flavor — distinct from both standard markdown
and Slack message formatting (mrkdwn). This reference documents the supported
syntax based on the `slack_create_canvas` and `slack_update_canvas` MCP tool
schemas.

## Headers

Canvas supports headers up to depth 3 only.

```markdown
# Heading 1
## Heading 2
### Heading 3
```

**CRITICAL**: Never use `####` or deeper. Any deeper headers must be truncated
to `###` before publishing.

## Text Formatting

Standard markdown inline formatting is supported:

```markdown
**bold text**
*italic text*
~~strikethrough~~
`inline code`
```

## Links

Use standard markdown link syntax with full URLs only:

```markdown
[Link text](https://example.com)
```

**Allowed schemes**: `http://`, `https://`, `mailto:`, `tel:`, `ftp://`, `slack://`

**CRITICAL**: No relative links. All links must be fully qualified URLs.

## Images

Images must be on standalone lines (not inline):

```markdown
![Alt text](https://example.com/image.png)
```

Images cannot be placed inline with other text.

## User and Channel Mentions

Canvas mentions use image-link syntax, NOT Slack mrkdwn angle-bracket syntax:

```markdown
![](@U1234567890)        <!-- user mention -->
![](#C1234567890)        <!-- channel mention -->
```

**CRITICAL**: Never use `<@U1234567890>` or `<#C1234567890>` — those are
Slack message format, not Canvas format.

## Emojis

Use Slack-style emoji shortcodes:

```markdown
:tada: :wave: :rocket: :white_check_mark:
```

## Dates

Use the special date syntax for formatted dates:

```markdown
![](slack_date:2026-03-18)
```

Never append day names or date text after the date syntax.

## Lists

Standard markdown list syntax is supported:

```markdown
- Bulleted item 1
- Bulleted item 2
  - Nested bullet

1. Numbered item 1
2. Numbered item 2
   1. Nested number
```

**Constraints**:
- List items support only plain text with inline formatting (bold, italic,
  inline code, links)
- Do NOT nest block quotes, code blocks, or headings inside list items
- Do NOT mix list types when nesting: bulleted lists can only nest bulleted
  lists; numbered lists can only nest numbered lists

## Tables

Standard markdown table syntax:

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
```

**CRITICAL**: Escape literal `|` characters in cell content with `\|`.

## Code Blocks

Fenced code blocks with optional language hint:

````markdown
```python
def hello():
    print("Hello Canvas")
```
````

**Constraint**: Code blocks must be at the top level — not inside list items
or block quotes.

## Block Quotes

Standard markdown block quotes (`>`) are NOT supported in Canvas. Convert
them to callouts instead.

## Callouts

Use the callout directive syntax:

```markdown
::: {.callout}
This is a callout block. Use it instead of block quotes.
:::
```

**Constraints**:
- No tables inside callouts
- Callouts must be at the top level

## Layouts (Multi-Column)

Create multi-column layouts (max 3 columns):

```markdown
::: {.layout}
::: {.column}
Content for column 1
:::
::: {.column}
Content for column 2
:::
::: {.column}
Content for column 3
:::
:::
```

**Constraints**:
- Maximum 3 columns
- No tables or callouts inside layouts

## Citations

Use numbered footnote-style references:

```markdown
This claim needs a source [1]. Another fact [2].

Sources:

[1] [Source Title](https://example.com/source1)

[2] [Another Source](https://example.com/source2)
```

Separate each source with two newlines.

## Writing Style Guidelines

Canvas content follows essay/article style by default:

- Write in full paragraphs with natural transitions
- Break content into logical sections with headers
- Only use bullet/numbered lists if explicitly requested
- Use transitions: "First," "Additionally," "Furthermore," "Moreover," "Finally"

## Transformation Cheat Sheet

| Standard Markdown | Canvas Markdown |
|-------------------|-----------------|
| `####` Header 4 | `###` (truncated) |
| `> blockquote` | `::: {.callout}\n...\n:::` |
| `<@U123>` mention | `![](@U123)` |
| `<#C123>` channel | `![](#C123)` |
| `[text](./relative)` | Must convert to full URL |
| `|` in table cell | `\|` (escaped) |
| Nested code in list | Extract to top level |
