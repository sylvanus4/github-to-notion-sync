# XML Reference for DOCX Editing

When editing unpacked DOCX XML in `unpacked/word/`, use these patterns.

## Schema Compliance

- **Element order in `<w:pPr>`**: `<w:pStyle>`, `<w:numPr>`, `<w:spacing>`, `<w:ind>`, `<w:jc>`, `<w:rPr>` last
- **Whitespace**: Add `xml:space="preserve"` to `<w:t>` with leading/trailing spaces
- **RSIDs**: Must be 8-digit hex (e.g., `00AB1234`)

## Tracked Changes

### Insertion

```xml
<w:ins w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:t>inserted text</w:t></w:r>
</w:ins>
```

### Deletion

```xml
<w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>deleted text</w:delText></w:r>
</w:del>
```

**Inside `<w:del>`**: Use `<w:delText>` instead of `<w:t>`, and `<w:delInstrText>` instead of `<w:instrText>`.

### Minimal edits

Only mark what changes:

```xml
<!-- Change "30 days" to "60 days" -->
<w:r><w:t>The term is </w:t></w:r>
<w:del w:id="1" w:author="Claude" w:date="...">
  <w:r><w:delText>30</w:delText></w:r>
</w:del>
<w:ins w:id="2" w:author="Claude" w:date="...">
  <w:r><w:t>60</w:t></w:r>
</w:ins>
<w:r><w:t> days.</w:t></w:r>
```

### Deleting entire paragraphs/list items

Add `<w:del/>` inside `<w:pPr><w:rPr>` so the paragraph mark is deleted. Without it, accepting changes leaves an empty paragraph.

### Rejecting another author's insertion

Nest deletion inside their insertion:

```xml
<w:ins w:author="Jane" w:id="5">
  <w:del w:author="Claude" w:id="10">
    <w:r><w:delText>their inserted text</w:delText></w:r>
  </w:del>
</w:ins>
```

### Restoring another author's deletion

Add insertion after (don't modify their deletion):

```xml
<w:del w:author="Jane" w:id="5">
  <w:r><w:delText>deleted text</w:delText></w:r>
</w:del>
<w:ins w:author="Claude" w:id="10">
  <w:r><w:t>deleted text</w:t></w:r>
</w:ins>
```

## Comments

After `comment.py`, add markers to document.xml.

**CRITICAL**: `<w:commentRangeStart>` and `<w:commentRangeEnd>` are siblings of `<w:r>`, never inside. Use `<w:commentReference w:id="N"/>` for each. Nest reply markers inside parent's range.

## Images

1. Add file to `word/media/`
2. Add `<Relationship Id="rId5" Type=".../image" Target="media/image1.png"/>` to `word/_rels/document.xml.rels`
3. Add content type to `[Content_Types].xml`
4. Reference in document.xml with `<w:drawing><wp:inline><wp:extent cx="914400" cy="914400"/>` (EMUs: 914400=1") and `<a:blip r:embed="rId5"/>`
