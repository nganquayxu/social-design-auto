# [BRAND_NAME] infographic style guide

Reference images: `_style-reference/` (sample-01..10 = finished posts, palette-and-chart-types.png = palette + chart types).

## Format
- Portrait 4:5 (1080 x 1350 px), Instagram feed.
- Light, airy background (white to very pale blue, subtle gradient). No dark full-bleed backgrounds, except small dark-navy highlight cards.

## Palette (blue monochrome, light to dark)
#132458 · #183990 · #163eb7 · #124de3 · #256bf7 · #3083ff · #57a7ff · #8dc7ff · #bbdcff · #d9ebff · #eef6ff
- Text/primary dark: #132458 (deep navy). Accent: #124de3 / #256bf7 (vivid blue).
- Use only blues + white. A single grey or soft pink/red only when a chart truly needs a negative/contrast value.
- Charts: darkest blue = biggest/primary series, lightening steps for the rest.

## Typography
- Clean geometric/grotesque sans-serif (Inter / Satoshi style), very bold, tight tracking.
- Headline: 2 lines, ALL CAPS, heavy weight. Line 1 in navy #132458, line 2 in vivid blue #124de3. Takes the top ~25% of the canvas.
- Small kicker above headline: ALL CAPS, light weight, small (topic + data date), e.g. "BERKSHIRE HATHAWAY | Q2 2026 13F".
- Subhead: 1-2 sentences, regular weight, sentence case, navy.
- Numbers are the hero: big, bold, blue.

## Layout
1. Kicker (top-left) + [BRAND_NAME] logo cluster (top-right or bottom-right).
2. Two-tone headline.
3. One-sentence subhead with the key stat.
4. Hero visual: ONE main chart or stat block (bar list, line chart, waterfall, donut, table, yield curve, flow of cards).
5. Takeaway strip: rounded pale-blue (#eef6ff / #d9ebff) card with icon (lightbulb/chip/coins) + one bold sentence.
6. Footer: "Source:" and "Note:" in small text, left; "Calculations by [BRAND_NAME]." at the end. Logo "[BRAND_NAME]" (blue script) + "powered by aws" + "Google Cloud Partner" bottom-right.

## Components
- Rounded cards (radius ~16-24px), soft shadow or 1px pale-blue border.
- Highlight card: dark navy (#132458) with white text and a large number.
- Charts: thin gridlines, direct data labels (no legend when avoidable), dots with value callouts on line charts, rounded bars, +/- deltas in blue pills.
- Company logos next to rows/columns when the post is about specific companies.
- Optional faint photo/illustration at the edge of the canvas (data center, building, portrait) fading into the white background; keep text readable.

## Tone
- Finance/markets, factual, concise. Always cite the data source and the as-of date. Educational only, not financial advice.

## Prompt template for image generation
"Create a 1080x1350 (4:5) finance infographic in the [BRAND_NAME] style from the attached references and style-guide.md.
Topic/data: <paste from brief.md>.
Headline (2 lines, caps; line 1 navy, line 2 vivid blue): <...>. Subhead: <...>.
Hero visual: <chart type> using ONLY the numbers in the brief, do not invent or alter numbers.
Takeaway strip: <one sentence>. Footer: Source: <...>. Calculations by [BRAND_NAME]. Include [BRAND_NAME] logo + powered by AWS + Google Cloud Partner bottom-right.
Palette and typography exactly per style-guide.md. Light airy background, no clutter."
