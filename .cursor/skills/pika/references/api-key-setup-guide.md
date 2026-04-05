# Pika API Key 발급 및 설정 가이드

> 프로젝트의 Pika 스킬(`pikastream-video-meeting`, `pika-text-to-video`, `pika-video-pipeline`)을 사용하려면 두 가지 API 키가 필요합니다.

| 환경변수 | 용도 | 발급처 |
|---------|------|--------|
| `PIKA_DEV_KEY` | PikaStream 실시간 화상 회의 (아바타 생성, 음성 클론, 미팅 참여) | Pika Developer Portal |
| `FAL_KEY` | Pika v2.2 비디오 생성 API (text-to-video, image-to-video, 특수효과 등) | fal.ai Dashboard |

---

## 1. PIKA_DEV_KEY — Pika Developer Key

### 용도

`pikastream-video-meeting` 스킬에서 사용합니다. Google Meet / Zoom 에 AI 아바타를 참가시키는 실시간 비디오 스트리밍에 필요합니다.

### 발급 절차

#### Step 1: Pika 개발자 포털 접속

브라우저에서 아래 URL로 이동합니다.

```
https://www.pika.me/dev/
```

#### Step 2: 계정 생성 / 로그인

- 이미 Pika 계정이 있다면 로그인합니다.
- 없으면 **Sign Up** 을 클릭하여 신규 가입합니다.
- Google OAuth, 이메일 가입 등을 지원합니다.

#### Step 3: Developer Key 생성

1. 개발자 대시보드에서 **"Create Developer Key"** (또는 유사한 버튼)를 클릭합니다.
2. 키가 생성되면 즉시 복사합니다.
3. 키는 `dk_` 접두사로 시작합니다 (예: `dk_abc123xyz...`).

> **주의**: 키는 생성 직후에만 전체 내용을 확인할 수 있습니다. 반드시 안전한 곳에 복사해 두세요.

#### Step 4: 환경변수 설정

프로젝트 루트의 `.env` 파일에 입력합니다:

```bash
PIKA_DEV_KEY=dk_your-actual-key-here
```

### 요금

| 항목 | 비용 |
|------|------|
| PikaStream 화상 회의 | **$0.275/분** (영상 + 음성 합산) |
| 아바타 생성 (1회) | 초기 설정 시 1회 비용 발생 |
| 음성 클론 (1회) | 초기 설정 시 1회 비용 발생 |

### Pika 소비자 요금제 (참고)

Pika는 크레딧 기반 구독제도 제공합니다 (개발자 API와 별도):

| 플랜 | 월 비용 | 월 크레딧 | 비고 |
|------|---------|----------|------|
| Basic (무료) | $0 | ~80 | 테스트용, 속도 제한 있음 |
| Standard | ~$8 | ~700 | 일반 사용 |
| Pro | ~$28–35 | ~2,300 | 전문 사용 |
| Fancy | ~$76–95 | ~6,000 | 대량 생산 |

> 소비자 플랜 크레딧과 Developer Key API 과금은 별도 체계입니다.

---

## 2. FAL_KEY — fal.ai API Key

### 용도

`pika-text-to-video` 스킬에서 사용합니다. Pika의 비디오 생성 모델(v2.2)이 fal.ai 인프라에서 호스팅되며, 아래 기능을 모두 이 키로 호출합니다:

- Text-to-Video (텍스트 → 비디오)
- Image-to-Video (이미지 → 비디오)
- Pikascenes (다중 이미지 합성)
- Pikaframes (키프레임 전환)
- Pikaffects (16종 특수효과)
- Pikaswaps (비디오 내 요소 교체)
- Pikadditions (비디오에 요소 추가)

### 발급 절차

#### Step 1: fal.ai 가입

브라우저에서 아래 URL로 이동합니다.

```
https://fal.ai/login
```

세 가지 로그인 방법 중 선택:

| 방법 | 설명 |
|------|------|
| **GitHub OAuth** | GitHub 계정으로 간편 가입 (개발자에게 추천) |
| **Google OAuth** | Google 계정으로 간편 가입 |
| **SSO/SAML** | 기업 SSO를 통한 가입 |

#### Step 2: API Key 생성

1. 가입/로그인 후 아래 URL로 이동합니다:

```
https://fal.ai/dashboard/keys
```

2. **"Create Key"** 버튼을 클릭합니다.
3. 키 이름을 입력합니다 (예: `pika-skills-key`).
4. **Scope** 를 선택합니다:

| Scope | 권한 | 추천 |
|-------|------|------|
| **API** | 모델 호출, API 관련 Platform API 접근 | ✅ 대부분의 경우 이것으로 충분 |
| **ADMIN** | API + CLI 배포(`fal deploy`, `fal run`), 앱 관리 | 고급 사용 시 |

5. **키를 즉시 복사합니다.**

> **중요**: 키는 생성 직후에만 전체 내용을 확인할 수 있습니다. 페이지를 벗어나면 다시 볼 수 없습니다!

#### Step 3: 환경변수 설정

프로젝트 루트의 `.env` 파일에 입력합니다:

```bash
FAL_KEY=your-fal-api-key-here
```

#### Step 4: 동작 확인 (선택)

Python에서 간단히 테스트할 수 있습니다:

```python
import fal_client

result = fal_client.subscribe(
    "fal-ai/pika/v2.2/text-to-video",
    arguments={
        "prompt": "A cat walking on a rainbow bridge",
        "resolution": "720p",
        "duration": "5",
    },
)
print(result["video"]["url"])
```

위 코드가 비디오 URL을 출력하면 정상적으로 연동된 것입니다.

### 요금

fal.ai는 **선불 크레딧** 시스템을 사용합니다. 크레딧을 미리 충전한 후 API 호출 시 차감됩니다.

#### Pika 모델별 비용

| 모델 / 모드 | 해상도 | 비용 |
|-------------|--------|------|
| Pika v2.2 Text-to-Video | 720p, 5초 | **~$0.20**/영상 |
| Pika v2.2 Text-to-Video | 1080p, 5초 | **~$0.45**/영상 |
| Pika v2.2 Image-to-Video | 720p, 5초 | ~$0.20/영상 |
| Pika v2.2 Image-to-Video | 1080p, 5초 | ~$0.45/영상 |
| Pikascenes (다중이미지) | 1080p | ~$0.45/영상 |
| Pikaframes (키프레임) | 720p | ~$0.20/영상 |
| Pikaffects (특수효과) | — | ~$0.20/영상 |
| Pikaswaps (요소교체) | — | ~$0.20/영상 |
| Pikadditions (요소추가) | — | ~$0.20/영상 |

#### 크레딧 주요 정보

| 항목 | 내용 |
|------|------|
| 결제 방식 | 선불 크레딧 충전 (카드 결제) |
| 최소 충전 금액 | fal.ai 대시보드에서 확인 |
| 크레딧 유효기간 | **구매 후 365일** |
| 무료/프로모션 크레딧 | 유효기간 1주~1년 (프로모션에 따라 상이) |
| 동시 요청 제한 | 신규 계정 2건 → 크레딧 구매 시 최대 40건까지 확대 |
| 과금 기준 | 성공한 결과만 과금 (서버 에러, 큐 대기 시간은 비과금) |

#### 팀 사용 시 주의

팀 계정을 사용하는 경우, 대시보드 좌상단에서 **올바른 팀을 선택**한 후 키를 생성해야 합니다. 키는 생성한 계정/팀에 귀속됩니다.

---

## 3. .env 파일 설정 요약

프로젝트 루트의 `.env` 파일에 아래 두 줄을 실제 값으로 교체합니다:

```bash
# Pika Developer Key (pikastream-video-meeting 스킬용)
PIKA_DEV_KEY=dk_your-actual-key

# fal.ai API Key (pika-text-to-video 스킬용)
FAL_KEY=your-fal-api-key
```

### 어떤 키가 어떤 스킬에 필요한가

| 스킬 | `PIKA_DEV_KEY` | `FAL_KEY` |
|------|:--------------:|:---------:|
| `pikastream-video-meeting` | ✅ 필수 | — |
| `pika-text-to-video` | — | ✅ 필수 |
| `pika-video-pipeline` | — | ✅ (내부에서 pika-text-to-video 호출) |

> 두 키는 **독립적**입니다. 화상 회의만 사용한다면 `PIKA_DEV_KEY`만, 비디오 생성만 사용한다면 `FAL_KEY`만 설정해도 됩니다.

---

## 4. 보안 주의사항

- `.env` 파일은 `.gitignore`에 포함되어 있어 Git에 커밋되지 않습니다.
- API 키를 코드에 하드코딩하지 마세요.
- 키가 유출되었다면 즉시 해당 대시보드에서 키를 재발급(revoke + regenerate)하세요.
- `.env.example`에는 실제 키가 아닌 빈 값만 유지합니다.

---

## 5. 유용한 링크

| 리소스 | URL |
|--------|-----|
| Pika 개발자 포털 | https://www.pika.me/dev/ |
| Pika Skills SDK (GitHub) | https://github.com/Pika-Labs/Pika-Skills |
| fal.ai 가입/로그인 | https://fal.ai/login |
| fal.ai API Key 대시보드 | https://fal.ai/dashboard/keys |
| fal.ai 요금 안내 | https://fal.ai/pricing |
| fal.ai Pika v2.2 Text-to-Video | https://fal.ai/models/fal-ai/pika/v2.2/text-to-video |
| fal.ai Pika v2.2 Image-to-Video | https://fal.ai/models/fal-ai/pika/v2.2/image-to-video |
| fal.ai 인증 가이드 | https://docs.fal.ai/documentation/setting-up/authentication |
| fal.ai Python 클라이언트 | https://docs.fal.ai/documentation/development/getting-started/installation |
