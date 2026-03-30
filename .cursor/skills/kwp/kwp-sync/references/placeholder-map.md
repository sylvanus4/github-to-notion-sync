# KWP Placeholder Mapping

`~~category` placeholders used in Anthropic Knowledge Work Plugins and their mapped tool names for this project.

## Common Placeholders (Used Across Multiple Plugins)

| Placeholder | Mapped Tool | MCP Status |
|-------------|-------------|------------|
| `~~chat` | Slack | Configured |
| `~~source control` | GitHub | Configured |
| `~~knowledge base` | Notion | Configured |
| `~~design tool` | Figma | Configured |
| `~~design` | Figma | Configured |
| `~~project tracker` | Linear | Not configured |
| `~~email` | Gmail | Not configured |
| `~~calendar` | Google Calendar | Not configured |
| `~~cloud storage` | Google Drive | Not configured |
| `~~monitoring` | Datadog | Not configured |
| `~~incident management` | PagerDuty | Not configured |
| `~~data warehouse` | BigQuery | Not configured |
| `~~office suite` | Google Workspace | Not configured |
| `~~meeting transcription` | Fireflies | Not configured |
| `~~product analytics` | Amplitude | Not configured |
| `~~marketing automation` | HubSpot | Not configured |
| `~~support platform` | Intercom | Not configured |
| `~~CRM` | HubSpot | Not configured |

## Domain-Specific Placeholders

### Human Resources
| Placeholder | Mapped Tool |
|-------------|-------------|
| `~~HRIS` | BambooHR |
| `~~ATS` | Greenhouse |
| `~~compensation data` | Pave |

### IT / Operations
| Placeholder | Mapped Tool |
|-------------|-------------|
| `~~ITSM` | ServiceNow |
| `~~procurement` | Coupa |
| `~~CI` | GitHub Actions |

### Legal
| Placeholder | Mapped Tool |
|-------------|-------------|
| `~~CLM` | DocuSign CLM |

### SEO / Marketing
| Placeholder | Mapped Tool |
|-------------|-------------|
| `~~SEO tools` | Ahrefs |

### Bio-Research
| Placeholder | Mapped Tool |
|-------------|-------------|
| `~~literature database` | PubMed |
| `~~journal access` | PubMed |
| `~~chemical database` | ChEMBL |
| `~~drug target database` | Open Targets |
| `~~clinical data platform` | ClinicalTrials.gov |
| `~~scientific illustration` | BioRender |
| `~~AI research platform` | Semantic Scholar |
| `~~genomics platform` | NCBI GEO |
| `~~data repository` | Synapse |
| `~~tool database` | Benchling |

## Notes

- "Configured" means the MCP server is already set up in Cursor IDE
- "Not configured" means the tool mapping is applied textually but no MCP server is connected
- To add a new MCP server, update `.cursor/mcp.json` or configure via Cursor IDE settings
- When new `~~category` placeholders appear in upstream updates, add them to this table before running sync
