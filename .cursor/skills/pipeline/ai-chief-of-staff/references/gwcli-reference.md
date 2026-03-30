# gwcli Command Reference

All commands use `--format json` for structured output the agent can parse.

## Gmail

| Task | Command |
|------|---------|
| List unread emails | `gwcli gmail list --unread --limit 20 --format json` |
| Search emails | `gwcli gmail search "QUERY" --format json` |
| Read full email | `gwcli gmail read MSG_ID --format json` |
| Draft email reply | `gwcli gmail draft --to EMAIL --subject SUBJ --body BODY` |
| Reply to email | `gwcli gmail reply MSG_ID --body "TEXT"` |
| Archive email | `gwcli gmail archive MSG_ID` |
| View thread | `gwcli gmail thread THREAD_ID --format json` |

## Calendar

| Task | Command |
|------|---------|
| Today's events | `gwcli calendar events --days 1 --format json` |
| Week's events | `gwcli calendar events --days 7 --format json` |
| Custom range | `gwcli calendar events --days N --limit M --format json` |
| Search events | `gwcli calendar search "QUERY" --format json` |
| List calendars | `gwcli calendar list --format json` |

## Drive

| Task | Command |
|------|---------|
| List files | `gwcli drive list --limit 20 --format json` |
| Search files | `gwcli drive search "QUERY" --format json` |
| Download file | `gwcli drive download FILE_ID --output PATH` |
| Export doc | `gwcli drive export DOC_ID --format pdf` |

## Profile Management

| Task | Command |
|------|---------|
| List profiles | `gwcli profiles list` |
| Add profile | `gwcli profiles add NAME --client PATH` |
| Set default | `gwcli profiles set-default NAME` |
| Use specific profile | `gwcli --profile NAME gmail list` |
