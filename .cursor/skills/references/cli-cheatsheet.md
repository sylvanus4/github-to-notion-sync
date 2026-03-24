# gws CLI Cheatsheet

## Gmail

```bash
gws gmail +send --to alice@co.com --subject 'Hello' --body 'Hi!'
gws gmail +triage                          # unread inbox summary
gws gmail +triage --max 5 --query 'from:boss'
gws gmail +watch --project my-gcp-project  # stream new emails as NDJSON
gws gmail users messages list --params '{"userId": "me", "q": "is:unread"}' --fields "messages(id,threadId)"
gws gmail users messages get --params '{"userId": "me", "id": "MSG_ID"}'
gws gmail users labels list --params '{"userId": "me"}'
```

## Drive

```bash
gws drive +upload ./report.pdf
gws drive +upload ./report.pdf --parent FOLDER_ID
gws drive files list --params '{"pageSize": 10}' --fields "files(id,name,mimeType)"
gws drive files list --params '{"q": "mimeType = '\''application/pdf'\''"}' --page-all
gws drive files get --params '{"fileId": "FILE_ID"}' -o ./download.pdf
gws drive files copy --params '{"fileId": "TEMPLATE_ID"}' --json '{"name": "Copy"}'
gws drive permissions create --params '{"fileId": "FILE_ID"}' --json '{"role": "writer", "type": "user", "emailAddress": "user@co.com"}'
gws drive permissions list --params '{"fileId": "FILE_ID"}'
```

## Calendar

```bash
gws calendar +agenda                        # upcoming events
gws calendar +agenda --today
gws calendar +agenda --week --format table
gws calendar +insert --summary 'Standup' --start '2026-03-10T09:00:00+09:00' --end '2026-03-10T09:30:00+09:00'
gws calendar +insert --summary 'Review' --start ... --end ... --attendee alice@co.com
gws calendar events list --params '{"calendarId": "primary", "timeMin": "2026-03-01T00:00:00Z"}' --fields "items(id,summary,start,end)"
```

## Sheets

```bash
gws sheets +read --spreadsheet ID --range 'Sheet1!A1:D10'
gws sheets +append --spreadsheet ID --values 'Alice,100,true'
gws sheets +append --spreadsheet ID --json-values '[["a","b"],["c","d"]]'
gws sheets spreadsheets create --json '{"properties": {"title": "Q1 Budget"}}'
gws sheets spreadsheets values get --params '{"spreadsheetId": "ID", "range": "Sheet1!A1:C10"}'
```

## Docs

```bash
gws docs documents create --json '{"title": "Meeting Notes"}'
gws docs +write --document DOC_ID --text 'Hello, world!'
gws docs documents get --params '{"documentId": "DOC_ID"}'
```

## Chat

```bash
gws chat +send --space spaces/AAAAxxxx --text 'Hello team!'
gws chat spaces list
gws chat spaces messages list --params '{"parent": "spaces/AAAAxxxx"}'
```

## Workflows

```bash
gws workflow +standup-report               # today's meetings + open tasks
gws workflow +meeting-prep                 # next meeting: agenda, attendees, docs
gws workflow +weekly-digest                # weekly summary
gws workflow +email-to-task --message-id MSG_ID
gws workflow +file-announce --file-id FILE_ID --space spaces/AAAAxxxx
```

## Schema & Help

```bash
gws --help
gws <service> --help
gws schema <service>.<resource>.<method>
```
