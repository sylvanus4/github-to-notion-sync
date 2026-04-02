## X-to-Notion

X (Twitter) 트윗이나 아티클을 가져와서 한국어로 번역한 후 Notion에 게시합니다.

### Usage

```
/x-to-notion <URL>
/x-to-notion <URL> parent=<notion-page-id>
/x-to-notion <URL> skip-translate
```

### Execution

Read and follow the `x-to-notion` skill:
`.cursor/skills/pipeline/x-to-notion/SKILL.md`

### What this does

1. **Fetch**: FxTwitter API로 트윗 내용 가져오기 (X Article 자동 감지)
2. **Parse**: 블록 구조를 마크다운으로 변환 (헤더, 코드, 이미지, 링크, 리스트)
3. **Translate**: 기술 용어와 코드 블록을 보존하면서 한국어로 번역
4. **Publish**: Notion 페이지로 게시 (기본: AI 자동 정리 하위 페이지)
5. **Verify**: 페이지 생성 확인 및 manifest.json 기록

### Parameters

| Parameter | Required | Description |
|---|---|---|
| URL | Yes | x.com 또는 twitter.com 링크 |
| `parent=<id>` | No | Notion 부모 페이지 ID (기본: AI 자동 정리) |
| `skip-translate` | No | 한국어 번역 생략 (영문 그대로 업로드) |

### Output

- `output/x-to-notion/{date}/` 디렉토리에 중간 산출물 저장
- Notion 페이지 생성 (🐦 아이콘)
- `manifest.json`에 전체 파이프라인 상태 기록
