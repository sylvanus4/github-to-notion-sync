---
name: content-repurposing-engine
description: Transform long-form content into platform-specific formats — Twitter threads, LinkedIn posts, newsletter, blog summary, video script, infographic brief, and email snippet.
disable-model-invocation: true
arguments: [source_content]
---

Repurpose `$source_content` into multiple platform formats.

## Output Platforms

| Platform | Format | Length |
|----------|--------|--------|
| Twitter/X | Thread (5-10 tweets) | 280 chars/tweet |
| LinkedIn | Professional post | 1300 chars |
| Newsletter | Section with CTA | 300-500 words |
| Blog | Summary with key takeaways | 500-800 words |
| Video Script | Outline with talking points | 3-5 min |
| Infographic | Brief with data points | Bullet format |
| Email | Snippet with subject line | 150-200 words |

## Process

1. **Extract Core**: Identify the single core message
2. **Adapt Tone**: Adjust for each platform's audience
3. **Format**: Apply platform-specific structure and constraints
4. **Hook**: Add platform-appropriate opening hooks
5. **CTA**: Include relevant calls to action

## Rules

- Preserve core message across all formats
- Never just truncate — rewrite for each platform
- Include hashtags for social platforms
- Korean output for all platforms unless specified otherwise
