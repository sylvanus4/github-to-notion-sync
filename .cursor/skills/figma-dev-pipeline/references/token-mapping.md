# Design Token Mapping Rules

Figma 디자인 토큰을 코드 토큰으로 변환하는 규칙.

## Color Mapping

### Tailwind CSS

| Figma Token | Tailwind Class | CSS Variable |
|-------------|---------------|--------------|
| primary-50 ~ primary-900 | bg-primary-50 ~ bg-primary-900 | --color-primary-{shade} |
| secondary-* | bg-secondary-* | --color-secondary-{shade} |
| neutral-* | bg-gray-* | --color-neutral-{shade} |
| success | bg-green-500 | --color-success |
| warning | bg-yellow-500 | --color-warning |
| error | bg-red-500 | --color-error |
| info | bg-blue-500 | --color-info |

### CSS Modules / Vanilla

```css
:root {
  --color-primary-500: #3B82F6;
  /* Figma token name → CSS variable */
}
```

## Typography Mapping

| Figma Token | Tailwind | CSS |
|-------------|---------|-----|
| heading-1 | text-4xl font-bold | font-size: 2.25rem; font-weight: 700 |
| heading-2 | text-3xl font-semibold | font-size: 1.875rem; font-weight: 600 |
| heading-3 | text-2xl font-semibold | font-size: 1.5rem; font-weight: 600 |
| body-lg | text-lg | font-size: 1.125rem |
| body-md | text-base | font-size: 1rem |
| body-sm | text-sm | font-size: 0.875rem |
| caption | text-xs | font-size: 0.75rem |

## Spacing Mapping

| Figma Token | Tailwind | CSS |
|-------------|---------|-----|
| space-1 (4px) | p-1, m-1, gap-1 | 0.25rem |
| space-2 (8px) | p-2, m-2, gap-2 | 0.5rem |
| space-3 (12px) | p-3, m-3, gap-3 | 0.75rem |
| space-4 (16px) | p-4, m-4, gap-4 | 1rem |
| space-6 (24px) | p-6, m-6, gap-6 | 1.5rem |
| space-8 (32px) | p-8, m-8, gap-8 | 2rem |

## Layout Mapping

| Figma Auto Layout | CSS | Tailwind |
|-------------------|-----|---------|
| Horizontal, gap: 8 | display: flex; gap: 8px | flex gap-2 |
| Vertical, gap: 16 | display: flex; flex-direction: column; gap: 16px | flex flex-col gap-4 |
| Wrap | flex-wrap: wrap | flex-wrap |
| Fill container | width: 100% | w-full |
| Fixed width | width: Npx | w-[Npx] |
| Hug contents | width: fit-content | w-fit |

## Border Radius Mapping

| Figma Token | Tailwind | CSS |
|-------------|---------|-----|
| radius-none (0) | rounded-none | border-radius: 0 |
| radius-sm (4px) | rounded-sm | border-radius: 0.25rem |
| radius-md (8px) | rounded-md | border-radius: 0.5rem |
| radius-lg (12px) | rounded-lg | border-radius: 0.75rem |
| radius-xl (16px) | rounded-xl | border-radius: 1rem |
| radius-full | rounded-full | border-radius: 9999px |

## Shadow Mapping

| Figma Token | Tailwind | CSS |
|-------------|---------|-----|
| shadow-sm | shadow-sm | box-shadow: 0 1px 2px rgba(0,0,0,0.05) |
| shadow-md | shadow-md | box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1) |
| shadow-lg | shadow-lg | box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1) |

## Naming Convention Rules

1. Figma 토큰이 프로젝트에 이미 있으면 기존 이름 사용
2. 신규 토큰은 프로젝트 네이밍 패턴을 따름
3. 시맨틱 토큰 우선 (color-primary가 #3B82F6보다 우선)
4. 컴포넌트 전용 토큰은 `{component}-{property}` 형식
