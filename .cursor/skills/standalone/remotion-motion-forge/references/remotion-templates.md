# Remotion Composition Templates

Reference code patterns for the 4 composition template types used by remotion-motion-forge. Each template demonstrates core Remotion APIs and design-token integration.

## Core Remotion APIs Quick Reference

```typescript
import {
  useCurrentFrame,       // Current frame number (0-indexed)
  useVideoConfig,        // { fps, width, height, durationInFrames }
  interpolate,           // Map frame ranges to value ranges
  spring,                // Physics-based spring animations
  AbsoluteFill,          // Full-frame positioned container
  Sequence,              // Time-offset child rendering
  Img,                   // Image with delay-loading (prevents flicker)
  staticFile,            // Reference files from public/ directory
  Easing,                // Easing functions for interpolate()
} from "remotion";
import { Composition } from "remotion";  // Used in Root.tsx only
```

### interpolate()

Maps a frame value to an output range with optional easing and clamping:

```typescript
const frame = useCurrentFrame();

const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});

const translateY = interpolate(frame, [0, 20], [50, 0], {
  extrapolateRight: "clamp",
  easing: Easing.out(Easing.ease),
});
```

### spring()

Physics-based animation for natural-feeling motion:

```typescript
const { fps } = useVideoConfig();
const frame = useCurrentFrame();

const scale = spring({
  frame,
  fps,
  config: { damping: 12, stiffness: 200, mass: 0.5 },
});

const slideIn = spring({ frame: frame - 15, fps, config: { damping: 15 } });
const marginLeft = interpolate(slideIn, [0, 1], [-200, 0]);
```

### Sequence

Offsets child rendering in time. Children only mount during their active window:

```tsx
<>
  <Sequence durationInFrames={90}>
    <IntroScene />
  </Sequence>
  <Sequence from={90} durationInFrames={120}>
    <MainContent />
  </Sequence>
  <Sequence from={210}>
    <OutroScene />
  </Sequence>
</>
```

### Images

```tsx
import { Img, staticFile } from "remotion";

<Img src={staticFile("logo.png")} style={{ width: 200 }} />
<Img src={staticFile(`frames/frame${frame}.png`)} />
```

Place image files in `remotion/public/`.

---

## Template 1: AppDemo

App interaction walkthrough with animated UI mockups.

**Specs**: 1920×1080 (16:9), 30–60s, 30fps

**Scene structure**: Title Card → Feature Walkthrough (2–4 scenes) → CTA

```tsx
// remotion/compositions/AppDemo.tsx
import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Img,
  staticFile,
} from "remotion";
import { colors, typography, spacing, animations } from "../tokens/design-tokens";

const TitleCard: React.FC<{ title: string; subtitle: string }> = ({
  title,
  subtitle,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleScale = spring({ frame, fps, config: { damping: 12 } });
  const subtitleOpacity = interpolate(frame, [20, 40], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: colors.surface.dark,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <h1
        style={{
          fontFamily: typography.fontFamily.sans,
          fontSize: typography.size["3xl"] * 2,
          fontWeight: typography.weight.bold,
          color: colors.brand[100],
          transform: `scale(${titleScale})`,
        }}
      >
        {title}
      </h1>
      <p
        style={{
          fontFamily: typography.fontFamily.sans,
          fontSize: typography.size.xl,
          color: colors.foreground.secondary.dark,
          opacity: subtitleOpacity,
          marginTop: spacing[4],
        }}
      >
        {subtitle}
      </p>
    </AbsoluteFill>
  );
};

const PhoneMockup: React.FC<{ screenshotPath: string }> = ({
  screenshotPath,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const slideUp = spring({ frame, fps, config: { damping: 14 } });
  const translateY = interpolate(slideUp, [0, 1], [300, 0]);

  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <div
        style={{
          width: 375,
          height: 812,
          borderRadius: 40,
          overflow: "hidden",
          boxShadow: shadows.xl,
          transform: `translateY(${translateY}px)`,
          border: `3px solid ${colors.brand[600]}`,
        }}
      >
        <Img
          src={staticFile(screenshotPath)}
          style={{ width: "100%", height: "100%", objectFit: "cover" }}
        />
      </div>
    </AbsoluteFill>
  );
};

const CTACard: React.FC<{ text: string; url?: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pop = spring({ frame, fps, config: { damping: 10, stiffness: 300 } });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: colors.brand[600],
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          transform: `scale(${pop})`,
          padding: `${spacing[8]}px ${spacing[12]}px`,
          backgroundColor: colors.surface.light,
          borderRadius: radii.lg,
        }}
      >
        <h2
          style={{
            fontFamily: typography.fontFamily.sans,
            fontSize: typography.size["2xl"],
            fontWeight: typography.weight.semibold,
            color: colors.brand[600],
          }}
        >
          {text}
        </h2>
      </div>
    </AbsoluteFill>
  );
};

export const AppDemoComposition: React.FC<{
  title: string;
  subtitle: string;
  screens: string[];
  ctaText: string;
}> = ({ title, subtitle, screens, ctaText }) => {
  const screenDuration = 120; // 4 seconds per screen at 30fps

  return (
    <AbsoluteFill>
      <Sequence durationInFrames={90}>
        <TitleCard title={title} subtitle={subtitle} />
      </Sequence>

      {screens.map((screen, i) => (
        <Sequence
          key={screen}
          from={90 + i * screenDuration}
          durationInFrames={screenDuration}
        >
          <PhoneMockup screenshotPath={screen} />
        </Sequence>
      ))}

      <Sequence from={90 + screens.length * screenDuration} durationInFrames={90}>
        <CTACard text={ctaText} />
      </Sequence>
    </AbsoluteFill>
  );
};
```

**Root.tsx registration**:

```tsx
<Composition
  id="AppDemo"
  component={AppDemoComposition}
  durationInFrames={30 * 45}
  fps={30}
  width={1920}
  height={1080}
  defaultProps={{
    title: "Platform Demo",
    subtitle: "See what's new",
    screens: ["screen1.png", "screen2.png", "screen3.png"],
    ctaText: "Try it today",
  }}
/>
```

---

## Template 2: FeatureHighlight

Single feature spotlight with annotations and metrics.

**Specs**: 1920×1080 (16:9), 15–30s, 30fps

**Scene structure**: Hook (3s) → Feature showcase → Key benefit → CTA

```tsx
// remotion/compositions/FeatureHighlight.tsx
import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Easing,
} from "remotion";
import { colors, typography, spacing } from "../tokens/design-tokens";

const ZoomReveal: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const zoom = spring({ frame, fps, config: { damping: 8, stiffness: 100 } });
  const scale = interpolate(zoom, [0, 1], [0.3, 1]);
  const opacity = interpolate(frame, [0, 15], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        transform: `scale(${scale})`,
        opacity,
      }}
    >
      {children}
    </AbsoluteFill>
  );
};

const MetricCounter: React.FC<{ value: number; label: string; suffix?: string }> = ({
  value,
  label,
  suffix = "",
}) => {
  const frame = useCurrentFrame();
  const displayValue = Math.min(
    Math.round(interpolate(frame, [0, 60], [0, value], {
      extrapolateRight: "clamp",
      easing: Easing.out(Easing.quad),
    })),
    value
  );

  return (
    <div style={{ textAlign: "center" }}>
      <div
        style={{
          fontFamily: typography.fontFamily.mono,
          fontSize: 72,
          fontWeight: typography.weight.bold,
          color: colors.brand[600],
        }}
      >
        {displayValue.toLocaleString()}{suffix}
      </div>
      <div
        style={{
          fontFamily: typography.fontFamily.sans,
          fontSize: typography.size.lg,
          color: colors.foreground.secondary.light,
          marginTop: spacing[2],
        }}
      >
        {label}
      </div>
    </div>
  );
};

const TextReveal: React.FC<{ text: string; delay?: number }> = ({
  text,
  delay = 0,
}) => {
  const frame = useCurrentFrame();
  const adjustedFrame = frame - delay;

  if (adjustedFrame < 0) return null;

  const opacity = interpolate(adjustedFrame, [0, 15], [0, 1], {
    extrapolateRight: "clamp",
  });
  const translateY = interpolate(adjustedFrame, [0, 15], [20, 0], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.ease),
  });

  return (
    <div
      style={{
        fontFamily: typography.fontFamily.sans,
        fontSize: typography.size["2xl"],
        fontWeight: typography.weight.semibold,
        color: colors.foreground.primary.light,
        opacity,
        transform: `translateY(${translateY}px)`,
      }}
    >
      {text}
    </div>
  );
};

export const FeatureHighlightComposition: React.FC<{
  hookText: string;
  featureTitle: string;
  featureDescription: string;
  metricValue: number;
  metricLabel: string;
  metricSuffix?: string;
  ctaText: string;
}> = ({
  hookText,
  featureTitle,
  featureDescription,
  metricValue,
  metricLabel,
  metricSuffix,
  ctaText,
}) => {
  return (
    <AbsoluteFill style={{ backgroundColor: colors.surface.light }}>
      {/* Hook — 3 seconds */}
      <Sequence durationInFrames={90}>
        <ZoomReveal>
          <h1
            style={{
              fontFamily: typography.fontFamily.sans,
              fontSize: 64,
              fontWeight: typography.weight.bold,
              color: colors.brand[900],
            }}
          >
            {hookText}
          </h1>
        </ZoomReveal>
      </Sequence>

      {/* Feature showcase — 10 seconds */}
      <Sequence from={90} durationInFrames={300}>
        <AbsoluteFill
          style={{
            justifyContent: "center",
            alignItems: "center",
            padding: spacing[12],
          }}
        >
          <TextReveal text={featureTitle} />
          <TextReveal text={featureDescription} delay={30} />
        </AbsoluteFill>
      </Sequence>

      {/* Metric — 7 seconds */}
      <Sequence from={390} durationInFrames={210}>
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
          <MetricCounter
            value={metricValue}
            label={metricLabel}
            suffix={metricSuffix}
          />
        </AbsoluteFill>
      </Sequence>

      {/* CTA — 5 seconds */}
      <Sequence from={600} durationInFrames={150}>
        <ZoomReveal>
          <div
            style={{
              padding: `${spacing[6]}px ${spacing[10]}px`,
              backgroundColor: colors.brand[600],
              borderRadius: 12,
            }}
          >
            <span
              style={{
                fontFamily: typography.fontFamily.sans,
                fontSize: typography.size["2xl"],
                fontWeight: typography.weight.bold,
                color: "#FFFFFF",
              }}
            >
              {ctaText}
            </span>
          </div>
        </ZoomReveal>
      </Sequence>
    </AbsoluteFill>
  );
};
```

---

## Template 3: DSShowcase

Design system before/after visualization with token callouts.

**Specs**: 1920×1080 (16:9), 20–40s, 30fps

**Scene structure**: "Before" state → Animated transition → "After" state → Token callouts

```tsx
// remotion/compositions/DSShowcase.tsx
import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Easing,
} from "remotion";
import { colors, typography, spacing, radii } from "../tokens/design-tokens";

const SplitScreen: React.FC<{
  leftContent: React.ReactNode;
  rightContent: React.ReactNode;
  splitProgress: number; // 0 = full left, 1 = full right
}> = ({ leftContent, rightContent, splitProgress }) => {
  const splitX = interpolate(splitProgress, [0, 1], [100, 50]);

  return (
    <AbsoluteFill>
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          width: `${splitX}%`,
          height: "100%",
          overflow: "hidden",
        }}
      >
        {leftContent}
      </div>
      <div
        style={{
          position: "absolute",
          right: 0,
          top: 0,
          width: `${100 - splitX}%`,
          height: "100%",
          overflow: "hidden",
        }}
      >
        {rightContent}
      </div>
      {/* Divider line */}
      <div
        style={{
          position: "absolute",
          left: `${splitX}%`,
          top: 0,
          width: 3,
          height: "100%",
          backgroundColor: colors.brand[600],
          boxShadow: `0 0 20px ${colors.brand[600]}`,
        }}
      />
    </AbsoluteFill>
  );
};

const TokenBadge: React.FC<{
  name: string;
  value: string;
  color?: string;
  delay?: number;
}> = ({ name, value, color, delay = 0 }) => {
  const frame = useCurrentFrame();
  const adjustedFrame = frame - delay;
  if (adjustedFrame < 0) return null;

  const { fps } = useVideoConfig();
  const pop = spring({
    frame: adjustedFrame,
    fps,
    config: { damping: 10, stiffness: 200 },
  });

  return (
    <div
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: spacing[2],
        padding: `${spacing[2]}px ${spacing[4]}px`,
        backgroundColor: colors.surface.card.dark,
        borderRadius: radii.lg,
        transform: `scale(${pop})`,
        margin: spacing[2],
      }}
    >
      {color && (
        <div
          style={{
            width: 16,
            height: 16,
            borderRadius: 4,
            backgroundColor: color,
          }}
        />
      )}
      <span
        style={{
          fontFamily: typography.fontFamily.mono,
          fontSize: typography.size.sm,
          color: colors.foreground.secondary.dark,
        }}
      >
        {name}
      </span>
      <span
        style={{
          fontFamily: typography.fontFamily.mono,
          fontSize: typography.size.sm,
          color: colors.foreground.primary.dark,
          fontWeight: typography.weight.semibold,
        }}
      >
        {value}
      </span>
    </div>
  );
};

const ColorSwatch: React.FC<{
  label: string;
  hex: string;
  size?: number;
  delay?: number;
}> = ({ label, hex, size = 80, delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const adjustedFrame = frame - delay;
  if (adjustedFrame < 0) return null;

  const scale = spring({
    frame: adjustedFrame,
    fps,
    config: { damping: 12 },
  });

  return (
    <div style={{ textAlign: "center", transform: `scale(${scale})` }}>
      <div
        style={{
          width: size,
          height: size,
          borderRadius: radii.lg,
          backgroundColor: hex,
          boxShadow: `0 4px 12px ${hex}66`,
        }}
      />
      <span
        style={{
          fontFamily: typography.fontFamily.mono,
          fontSize: typography.size.xs,
          color: colors.foreground.secondary.dark,
          marginTop: spacing[1],
          display: "block",
        }}
      >
        {label}
      </span>
    </div>
  );
};

export const DSShowcaseComposition: React.FC<{
  title: string;
  beforeLabel?: string;
  afterLabel?: string;
  tokens: Array<{ name: string; value: string; color?: string }>;
}> = ({ title, beforeLabel = "Before", afterLabel = "After", tokens }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const splitProgress = interpolate(frame, [180, 300], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.ease),
  });

  return (
    <AbsoluteFill style={{ backgroundColor: colors.surface.dark }}>
      {/* Title — 3 seconds */}
      <Sequence durationInFrames={90}>
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
          <h1
            style={{
              fontFamily: typography.fontFamily.sans,
              fontSize: 56,
              fontWeight: typography.weight.bold,
              color: colors.foreground.primary.dark,
            }}
          >
            {title}
          </h1>
        </AbsoluteFill>
      </Sequence>

      {/* Before → split → After transition — 15 seconds */}
      <Sequence from={90} durationInFrames={450}>
        <SplitScreen
          splitProgress={splitProgress}
          leftContent={
            <AbsoluteFill
              style={{
                backgroundColor: "#1a1a2e",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <span
                style={{
                  fontFamily: typography.fontFamily.sans,
                  fontSize: 36,
                  color: "#888",
                }}
              >
                {beforeLabel}
              </span>
            </AbsoluteFill>
          }
          rightContent={
            <AbsoluteFill
              style={{
                backgroundColor: colors.surface.dark,
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <span
                style={{
                  fontFamily: typography.fontFamily.sans,
                  fontSize: 36,
                  color: colors.brand[100],
                }}
              >
                {afterLabel}
              </span>
            </AbsoluteFill>
          }
        />
      </Sequence>

      {/* Token callouts — remaining time */}
      <Sequence from={540}>
        <AbsoluteFill
          style={{
            justifyContent: "center",
            alignItems: "center",
            flexWrap: "wrap",
            gap: spacing[4],
            padding: spacing[12],
          }}
        >
          {tokens.map((token, i) => (
            <TokenBadge
              key={token.name}
              name={token.name}
              value={token.value}
              color={token.color}
              delay={i * 8}
            />
          ))}
        </AbsoluteFill>
      </Sequence>
    </AbsoluteFill>
  );
};
```

---

## Template 4: PromoReel

Social media promo and YouTube B-roll with kinetic typography.

**Specs**: 1080×1920 (9:16) for Shorts/Reels or 1920×1080 (16:9), 15–60s, 30fps

**Scene structure**: Hook (1–3s) → Value proposition (3–5 scenes) → CTA

```tsx
// remotion/compositions/PromoReel.tsx
import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Easing,
} from "remotion";
import { colors, typography, spacing } from "../tokens/design-tokens";

const KineticText: React.FC<{
  lines: string[];
  staggerFrames?: number;
}> = ({ lines, staggerFrames = 8 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ textAlign: "center" }}>
      {lines.map((line, i) => {
        const lineFrame = frame - i * staggerFrames;
        if (lineFrame < 0) return null;

        const slideUp = spring({
          frame: lineFrame,
          fps,
          config: { damping: 12, stiffness: 150 },
        });
        const translateY = interpolate(slideUp, [0, 1], [60, 0]);
        const opacity = interpolate(lineFrame, [0, 10], [0, 1], {
          extrapolateRight: "clamp",
        });

        return (
          <div
            key={`${line}-${i}`}
            style={{
              fontFamily: typography.fontFamily.sans,
              fontSize: i === 0 ? 64 : 48,
              fontWeight: i === 0 ? typography.weight.bold : typography.weight.semibold,
              color: i === 0 ? colors.brand[100] : colors.foreground.secondary.dark,
              transform: `translateY(${translateY}px)`,
              opacity,
              lineHeight: 1.2,
            }}
          >
            {line}
          </div>
        );
      })}
    </div>
  );
};

const LogoReveal: React.FC<{ logoPath: string }> = ({ logoPath }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({ frame, fps, config: { damping: 8, stiffness: 200 } });
  const glow = interpolate(frame, [20, 40], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <div
        style={{
          transform: `scale(${scale})`,
          filter: `drop-shadow(0 0 ${glow * 30}px ${colors.brand[600]}66)`,
        }}
      >
        <img
          src={logoPath}
          alt=""
          style={{ width: 200, height: 200, objectFit: "contain" }}
        />
      </div>
    </AbsoluteFill>
  );
};

const SlideTransition: React.FC<{
  children: React.ReactNode;
  direction?: "left" | "right" | "up" | "down";
}> = ({ children, direction = "right" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({ frame, fps, config: { damping: 14 } });

  const transforms = {
    left: `translateX(${interpolate(progress, [0, 1], [-1920, 0])}px)`,
    right: `translateX(${interpolate(progress, [0, 1], [1920, 0])}px)`,
    up: `translateY(${interpolate(progress, [0, 1], [-1080, 0])}px)`,
    down: `translateY(${interpolate(progress, [0, 1], [1080, 0])}px)`,
  };

  return (
    <AbsoluteFill style={{ transform: transforms[direction] }}>
      {children}
    </AbsoluteFill>
  );
};

export const PromoReelComposition: React.FC<{
  hookLines: string[];
  scenes: Array<{ lines: string[]; bgColor?: string }>;
  ctaText: string;
  logoPath?: string;
}> = ({ hookLines, scenes, ctaText, logoPath }) => {
  const sceneDuration = 90; // 3 seconds per scene

  return (
    <AbsoluteFill style={{ backgroundColor: colors.surface.dark }}>
      {/* Hook — 3 seconds */}
      <Sequence durationInFrames={90}>
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
          <KineticText lines={hookLines} />
        </AbsoluteFill>
      </Sequence>

      {/* Value proposition scenes */}
      {scenes.map((scene, i) => (
        <Sequence
          key={`scene-${i}`}
          from={90 + i * sceneDuration}
          durationInFrames={sceneDuration}
        >
          <SlideTransition direction={i % 2 === 0 ? "right" : "left"}>
            <AbsoluteFill
              style={{
                backgroundColor: scene.bgColor || colors.surface.dark,
                justifyContent: "center",
                alignItems: "center",
                padding: spacing[10],
              }}
            >
              <KineticText lines={scene.lines} />
            </AbsoluteFill>
          </SlideTransition>
        </Sequence>
      ))}

      {/* CTA with optional logo */}
      <Sequence from={90 + scenes.length * sceneDuration} durationInFrames={120}>
        <AbsoluteFill
          style={{
            backgroundColor: colors.brand[600],
            justifyContent: "center",
            alignItems: "center",
            gap: spacing[8],
          }}
        >
          {logoPath && <LogoReveal logoPath={logoPath} />}
          <KineticText lines={[ctaText]} />
        </AbsoluteFill>
      </Sequence>
    </AbsoluteFill>
  );
};
```

**Root.tsx registration (9:16 for Reels)**:

```tsx
<Composition
  id="PromoReel-Vertical"
  component={PromoReelComposition}
  durationInFrames={30 * 30}
  fps={30}
  width={1080}
  height={1920}
  defaultProps={{
    hookLines: ["Your App.", "Reimagined."],
    scenes: [
      { lines: ["Lightning Fast", "Search"] },
      { lines: ["Smart Filters", "Built In"] },
      { lines: ["Real-time", "Collaboration"] },
    ],
    ctaText: "Download Now",
  }}
/>
```

---

## Reusable Components Reference

These components are used across templates and stored in `remotion/components/`:

| Component | File | Used In | Purpose |
|-----------|------|---------|---------|
| `TextReveal` | `TextReveal.tsx` | FeatureHighlight, AppDemo | Fade + slide-up text animation |
| `KineticText` | `KineticText.tsx` | PromoReel | Staggered multi-line text with spring physics |
| `SplitScreen` | `SplitScreen.tsx` | DSShowcase | Animated split-screen with divider |
| `TokenBadge` | `TokenBadge.tsx` | DSShowcase | Design token label with color swatch |
| `ColorSwatch` | `ColorSwatch.tsx` | DSShowcase | Animated color circle with label |
| `MetricCounter` | `MetricCounter.tsx` | FeatureHighlight | Animated number counter |
| `ZoomReveal` | `ZoomReveal.tsx` | FeatureHighlight, AppDemo | Scale + fade entrance |
| `SlideTransition` | `SlideTransition.tsx` | PromoReel | Directional slide-in with spring |
| `PhoneMockup` | `PhoneMockup.tsx` | AppDemo | Device frame with screenshot |
| `LogoReveal` | `LogoReveal.tsx` | PromoReel | Scale + glow logo animation |
| `CodeBlock` | `CodeBlock.tsx` | FeatureHighlight | Syntax-highlighted code display |
| `TransitionWipe` | `TransitionWipe.tsx` | All | Scene transition effects |
