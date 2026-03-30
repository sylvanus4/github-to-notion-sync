---
name: trading-scenario-analyzer
description: >-
  Analyze news headlines for 18-month investment scenarios. Orchestrates scenario-analyst (main analysis)
  and strategy-reviewer (second opinion) agents to produce comprehensive reports with 1st/2nd/3rd-order
  impacts, recommended stocks, and review feedback in Japanese.
  Use for "scenario analysis", "headline scenario", "18-month outlook", "シナ리오 분석", "뉴스 시나리오", "18개월 전망".
  Do NOT use for daily stock signals (use daily-stock-check).
  Do NOT use for AlphaEar analysis (use alphaear-deepear-lite).
  Do NOT use for weekly price updates (use weekly-stock-update).
metadata:
  author: tradermonty
  version: "1.0.0"
  category: analysis
  source: claude-trading-skills
  api_required: none
---

# Headline Scenario Analyzer

## Overview

このスキルは、ニュースヘッドラインを起点として中長期（18ヶ月）の投資シナリオを分析します。
2つの専門エージェント（`scenario-analyst`と`strategy-reviewer`）を順次呼び出し、
多角的な分析と批判的レビューを統合した包括的なレポートを生成します。

## When to Use This Skill

以下の場合にこのスキルを使用してください：

- ニュースヘッドラインから中長期の投資影響を分析したい
- 18ヶ月後のシナリオを複数構築したい
- セクター・銘柄への影響を1次/2次/3次で整理したい
- セカンドオピニオンを含む包括的な分析が必要
- 日本語でのレポート出力が必要

**使用例:**
```
/headline-scenario-analyzer "Fed raises interest rates by 50bp, signals more hikes ahead"
/headline-scenario-analyzer "China announces new tariffs on US semiconductors"
/headline-scenario-analyzer "OPEC+ agrees to cut oil production by 2 million barrels per day"
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Skill（オーケストレーター）                        │
│                                                                      │
│  Phase 1: 準備                                                       │
│  ├─ ヘッドライン解析                                                  │
│  ├─ イベントタイプ分類                                                │
│  └─ リファレンス読み込み                                              │
│                                                                      │
│  Phase 2: エージェント呼び出し（Cursor Task subagent pattern）        │
│  ├─ scenario-analyst（主分析）→ references/agents/scenario-analyst.md│
│  └─ strategy-reviewer（セカンドオピニオン）→ references/agents/strategy-reviewer.md│
│                                                                      │
│  Phase 3: 統合・レポート生成                                          │
│  └─ outputs/reports/trading/scenario_analysis_<topic>_YYYYMMDD.md   │
└─────────────────────────────────────────────────────────────────────┘
```

## Workflow

### Phase 1: 準備

#### Step 1.1: ヘッドライン解析

ユーザーから入力されたヘッドラインを解析します。

1. **ヘッドライン確認**
   - 引数としてヘッドラインが渡されているか確認
   - 渡されていない場合はユーザーに入力を求める

2. **キーワード抽出**
   - 主要なエンティティ（企業名、国名、機関名）
   - 数値データ（金利、価格、数量）
   - アクション（引き上げ、引き下げ、発表、合意等）

#### Step 1.2: イベントタイプ分類

ヘッドラインを以下のカテゴリに分類：

| カテゴリ | 例 |
|---------|-----|
| 金融政策 | FOMC、ECB、日銀、利上げ、利下げ、QE/QT |
| 地政学 | 戦争、制裁、関税、貿易摩擦 |
| 規制・政策 | 環境規制、金融規制、独禁法 |
| テクノロジー | AI、EV、再エネ、半導体 |
| コモディティ | 原油、金、銅、農産物 |
| 企業・M&A | 買収、破綻、決算、業界再編 |

#### Step 1.3: リファレンス読み込み

イベントタイプに基づき、関連するリファレンスを読み込みます：

```
Read references/headline_event_patterns.md
Read references/sector_sensitivity_matrix.md
Read references/scenario_playbooks.md
```

**リファレンス内容:**
- `headline_event_patterns.md`: 過去のイベントパターンと市場反応
- `sector_sensitivity_matrix.md`: イベント×セクターの影響度マトリクス
- `scenario_playbooks.md`: シナリオ構築のテンプレートとベストプラクティス

---

### Phase 2: エージェント呼び出し（Cursor Task Subagent Pattern）

#### Step 2.1: scenario-analyst 呼び出し

CursorのTask subagent toolを使用してメイン分析を実行します。
**Agent定義**: `references/agents/scenario-analyst.md` を参照。

Subagentに渡すプロンプト例:
```
以下のヘッドラインについて18ヶ月シナリオ分析を実行してください。

## 対象ヘッドライン
[入力されたヘッドライン]

## イベントタイプ
[分類結果]

## リファレンス情報
[読み込んだリファレンスの要約]

## 分析要件
1. WebSearchで過去2週間の関連ニュースを収集
2. Base/Bull/Bearの3シナリオを構築（確率合計100%）
3. 1次/2次/3次影響をセクター別に分析
4. ポジティブ/ネガティブ影響銘柄を各3-5銘柄選定（米国市場のみ）
5. 全て日本語で出力
```

**期待する出力:**
- 関連ニュース記事リスト
- 3シナリオ（Base/Bull/Bear）の詳細
- セクター影響分析（1次/2次/3次）
- 銘柄推奨リスト

#### Step 2.2: strategy-reviewer 呼び出し

scenario-analystの分析結果を受けて、レビューエージェントを呼び出します。
**Agent定義**: `references/agents/strategy-reviewer.md` を参照。

Subagentに渡すプロンプト例:
```
以下のシナリオ分析をレビューしてください。

## 対象ヘッドライン
[入力されたヘッドライン]

## 分析結果
[scenario-analystの出力全文]

## レビュー要件
以下の観点でレビューを実施：
1. 見落とされているセクター/銘柄
2. シナリオ確率配分の妥当性
3. 影響分析の論理的整合性
4. 楽観/悲観バイアスの検出
5. 代替シナリオの提案
6. タイムラインの現実性

建設的かつ具体的なフィードバックを日本語で出力してください。
```

**期待する出力:**
- 見落としの指摘
- シナリオ確率への意見
- バイアスの指摘
- 代替シナリオの提案
- 最終推奨事項

---

### Phase 3: 統合・レポート生成

#### Step 3.1: 結果統合

両エージェントの出力を統合し、最終投資判断を作成します。

**統合ポイント:**
1. レビューで指摘された見落としを補完
2. 確率配分の調整（必要な場合）
3. バイアスを考慮した最終判断
4. 具体的なアクションプランの策定

#### Step 3.2: レポート生成

以下の形式で最終レポートを生成し、ファイルに保存します。

**保存先:** `outputs/reports/trading/scenario_analysis_<topic>_YYYYMMDD.md`

```markdown
# ヘッドライン・シナリオ分析レポート

**分析日時**: YYYY-MM-DD HH:MM
**対象ヘッドライン**: [入力されたヘッドライン]
**イベントタイプ**: [分類カテゴリ]

---

## 1. 関連ニュース記事
[scenario-analystが収集したニュースリスト]

## 1b. データ出所・数値一覧（必須）
| 数値・事実 | 値 | 出典（媒体/公式） | 取得日 |
|------------|-----|-------------------|--------|
| （ヘッドラインまたはWebSearch由来のみ。捏造禁止） | | | |

## 2. 想定シナリオ概要（18ヶ月後まで）

### Base Case（XX%確率）
[シナリオ詳細]

### Bull Case（XX%確率）
[シナリオ詳細]

### Bear Case（XX%確率）
[シナリオ詳細]

## 3. セクター・業種への影響

### 1次的影響（直接的）
[影響テーブル]

### 2次的影響（バリューチェーン・関連産業）
[影響テーブル]

### 3次的影響（マクロ・規制・技術）
[影響テーブル]

## 4. ポジティブ影響が見込まれる銘柄（3-5銘柄）
[銘柄テーブル]

## 5. ネガティブ影響が見込まれる銘柄（3-5銘柄）
[銘柄テーブル]

## 6. セカンドオピニオン・レビュー
[strategy-reviewerの出力]

## 7. 最終投資判断・示唆

### 推奨アクション
[レビューを踏まえた具体的アクション]

### リスク要因
[主要リスクの列挙]

### モニタリングポイント
[フォローすべき指標・イベント]

---
**生成**: trading-scenario-analyzer skill
**エージェント**: scenario-analyst, strategy-reviewer
```

#### Step 3.3: レポート保存

1. `outputs/reports/trading/` ディレクトリが存在しない場合は作成
2. `scenario_analysis_<topic>_YYYYMMDD.md` として保存（例: `scenario_analysis_venezuela_20260104.md`）
3. 保存完了をユーザーに通知
4. **プロジェクトルートに直接保存しないこと**

---

## Resources

### References
- `references/headline_event_patterns.md` - イベントパターンと市場反応
- `references/sector_sensitivity_matrix.md` - セクター感応度マトリクス
- `references/scenario_playbooks.md` - シナリオ構築テンプレート

### Agent Definitions (for Cursor Task Subagent)
- `references/agents/scenario-analyst.md` - メインシナリオ分析
- `references/agents/strategy-reviewer.md` - セカンドオピニオン・レビュー

---

## Important Notes

### 言語
- 全ての分析・出力は**日本語**で行う
- 銘柄ティッカーは英語表記を維持

### 対象市場
- 銘柄選定は**米国市場上場銘柄のみ**
- ADR含む

### 時間軸
- シナリオは**18ヶ月**を対象
- 0-6ヶ月/6-12ヶ月/12-18ヶ月の3フェーズで記述

### 確率配分
- Base + Bull + Bear = **100%**
- 各シナリオの確率は根拠とともに記述

### セカンドオピニオン
- **必須**で実行（strategy-reviewerを常に呼び出す）
- レビュー結果は最終判断に反映

### 出力先（重要）
- **必ず** `outputs/reports/trading/` ディレクトリ配下に保存すること
- パス: `outputs/reports/trading/scenario_analysis_<topic>_YYYYMMDD.md`
- 例: `outputs/reports/trading/scenario_analysis_fed_rate_hike_20260104.md`
- `outputs/reports/trading/` ディレクトリが存在しない場合は作成すること
- **プロジェクトルートに直接保存してはならない**

---

## Mandatory Output Contract (Eval-Aligned)

最終レポート（または統合回答）は次を **必須** とする（日本語で記述。ユーザーが韓国語を明示した場合は韓国語可だが、同じ構造を維持）:

1. **構造化見出し**: テンプレートの `## 1.`〜`## 7.` 見出しを欠かさない。
2. **数値の根拠**: 見出し「データ出所・数値一覧」を追加し、ヘッドラインまたは **WebSearch で取得した事実** から引用した **少なくとも3つの数値**（金利bp、関税率%、バレル数、価格、時価総額など）を表形式で示す。捏造禁止—取得できなかった数値は `N/A`。
3. **シナリオ確率**: Base/Bull/Bear は **%** で記載し合計 **100%**。
4. **アクション**: `## 7. 最終投資判断・示唆` に **推奨アクション**（買い/売り/様子見/ヘッジ等）を1つ明記し、**監視KPI** を箇条書き。
5. **リスク・無効化**: 少なくとも1つの **無効化条件**（例: 「OPECが増産合意ならベアシナリオへシフト」）を記載。
6. **レビュー統合**: strategy-reviewer の指摘を要約し、最終判断にどう反映したかを1段落で書く。

## Quality Checklist

レポート完成前に以下を確認：

- [ ] 「データ出所・数値一覧」に少なくとも3つの根拠付き数値があるか
- [ ] 無効化条件が記載されているか
- [ ] ヘッドラインが正しく解析されているか
- [ ] イベントタイプの分類が適切か
- [ ] 3シナリオの確率合計が100%か
- [ ] 1次/2次/3次影響の論理的繋がりがあるか
- [ ] 銘柄選定に具体的な根拠があるか
- [ ] strategy-reviewerのレビューが含まれているか
- [ ] レビューを踏まえた最終判断が記載されているか
- [ ] レポートが正しいパスに保存されたか

## Examples

### Example 1: Fed rate headline
**User:** "Fed raises interest rates by 50bp, signals more hikes ahead"
**Action:** Classifies as monetary policy; loads headline_event_patterns, sector_sensitivity_matrix, scenario_playbooks; invokes scenario-analyst and strategy-reviewer subagents.
**Output:** `scenario_analysis_fed_rate_hike_YYYYMMDD.md` with Base/Bull/Bear scenarios (100% total), 1st/2nd/3rd-order impacts, recommended stocks, and review feedback.

### Example 2: Geopolitical tariff
**User:** "China announces new tariffs on US semiconductors"
**Action:** Classifies as geopolitical/trade; loads geopolitical references; runs full pipeline with web research and second-opinion review.
**Output:** Japanese report with sector impact analysis (semis, tech, supply chain), positive/negative stock picks, and strategy-reviewer critique.

### Example 3: Commodity OPEC decision
**User:** "OPEC+ agrees to cut oil production by 2 million barrels per day"
**Action:** Classifies as commodity; analyzes energy sector impacts, inflation implications, and cross-asset effects over 18 months.
**Output:** Report with three scenarios, commodity-sensitive sectors, and monitoring points (inventory, demand, geopolitical follow-through).

## Error Handling

| Error | Action |
|-------|--------|
| ヘッドライン未提供 | ユーザーにヘッドライン入力を求める |
| scenario-analyst/subagent 失敗 | リトライ、または手動で参照を読み分析を実行 |
| 確率合計≠100% | Base+Bull+Bear の確率を再調整して100%に |
| 保存先ディレクトリなし | `outputs/reports/trading/` を作成してから保存 |
