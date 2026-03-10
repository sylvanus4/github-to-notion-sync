# Gmail Filter Templates

JSON templates for creating Gmail filters via `gws gmail users settings filters create`.

## Template: GitHub Notifications to Low Priority

```json
{
  "criteria": {
    "from": "notifications@github.com"
  },
  "action": {
    "addLabelIds": ["LOW_PRIORITY_LABEL_ID"],
    "removeLabelIds": ["INBOX"]
  }
}
```

## Template: Notion Notifications to Low Priority

```json
{
  "criteria": {
    "from": "notify@mail.notion.so"
  },
  "action": {
    "addLabelIds": ["LOW_PRIORITY_LABEL_ID"],
    "removeLabelIds": ["INBOX"]
  }
}
```

## Template: RunPod Notifications to Low Priority

```json
{
  "criteria": {
    "from": "@runpod.io"
  },
  "action": {
    "addLabelIds": ["LOW_PRIORITY_LABEL_ID"],
    "removeLabelIds": ["INBOX"]
  }
}
```

## Template: Calendar RSVP to Low Priority

```json
{
  "criteria": {
    "from": "calendar-notification@google.com",
    "query": "수락 OR 거절 OR accepted OR declined"
  },
  "action": {
    "addLabelIds": ["LOW_PRIORITY_LABEL_ID"],
    "removeLabelIds": ["INBOX"]
  }
}
```

## Template: Spam Domain to Trash

```json
{
  "criteria": {
    "from": "@spam-domain.com"
  },
  "action": {
    "removeLabelIds": ["INBOX"],
    "addLabelIds": ["TRASH"]
  }
}
```

## Usage

1. List existing filters to avoid duplicates:

```bash
gws gmail users settings filters list --params '{"userId": "me"}'
```

2. Replace `LOW_PRIORITY_LABEL_ID` with the actual label ID from:

```bash
gws gmail users labels list --params '{"userId": "me"}'
```

3. Create the filter:

```bash
gws gmail users settings filters create \
  --params '{"userId": "me"}' \
  --json '<TEMPLATE_JSON>'
```

## Dynamic Filter Generation

After each triage run, identify patterns that appeared 2+ times and generate new filters. The triage skill will:

1. Count sender occurrences across all trashed/labeled emails
2. For senders with 2+ occurrences, generate a filter template
3. Check against existing filters to avoid duplicates
4. Present new filters to the user for confirmation before creation
