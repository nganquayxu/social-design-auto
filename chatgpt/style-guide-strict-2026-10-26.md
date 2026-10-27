# Spiking infographic style guide (strict)

Two sources of truth, both in this folder:
1. COLORS: the official palette in `_style-reference/palette-and-chart-types.png` (hex list below). All 10 sample posts were built from it.
2. LAYOUT / TYPE / SPACING: the 10 finished posts `_style-reference/sample-01..10.webp`.
References are MANDATORY, not inspiration: every design must be built from the 2-3 closest samples and checked against them at the end. The official logo is `spiking-logo-final.png`.

## Format
- Portrait 4:5, 1080 x 1350 px. White background (#FFFFFF), optional very faint #EEF6FF wash. No dark full-bleed backgrounds.

## Colors: ONLY this palette (exact hex, nothing else)
#132458 · #183990 · #163eb7 · #124de3 · #256bf7 · #3083ff · #57a7ff · #8dc7ff · #bbdcff · #d9ebff · #eef6ff
Use them like this:
- Headline line 1, body text, dark highlight cards: #132458 (white text on dark cards).
- Headline line 2, hero numbers, key labels: #124de3.
- Chart fills, darkest = biggest/primary series: #124de3 → #256bf7 → #3083ff → #57a7ff → #8dc7ff → #bbdcff → #d9ebff → #eef6ff. Deep accents only when needed: #163eb7, #183990.
- Pale cards / strips: #eef6ff or #d9ebff.
- Do NOT use pure black, grey, any other blue, purple, green or red. (Only if a chart truly needs a negative/contrast value, use a soft pink/red dot as in the palette sheet.) Do NOT sample colors from the sample images; use the hex values above.

## Typography
- One clean geometric grotesque (Inter Tight / Satoshi look), EXTRA-BOLD, tight tracking, ALL CAPS headlines.
- Headline: 2 lines across the full width at the top (~22-25% of height), same size on both lines. Line 1 #132458, line 2 #124de3.
- Optional small kicker above (caps, light, one line: topic + date).
- Hero numbers: very large, bold, #124de3. Labels: regular, #132458, readable (nothing under ~22px at 1080 wide).

## Headline wording
Simple, catchy, curiosity-driven, max ~6 words per line, plain words. Hooks: "HOW X MAKES MONEY", "WHERE X REALLY MAKES MONEY", "TOP 10 ...", "WHO OWNS THE MARKET?". Must stay TRUE to the chart data.

## Layout (copy the closest sample)
1. Kicker (optional) + two-line headline.
2. ONE short sentence under it (optional).
3. ONE hero visual ~60% of the canvas. Preferred formats (high-search US-stock topics):
   - Ranked list with bars + company logos: "Top 10/15 ..." (sample-02, sample-07)
   - "Where $100 of revenue goes" waterfall (sample-08, sample-10)
   - Donut / share list: portfolio, index weights, revenue by segment (sample-04, sample-05)
   - Simple 2-line chart + 2-3 big stat cards (sample-03, sample-06, sample-09)
   - Chain of 4-6 cards with logo + one big number (sample-01)
   Other allowed chart types from the palette sheet: horizontal/vertical bars, donut, pie, pyramid, bubbles, dot plot, treemap.
4. Footer: ONE line "Source: ...". Spiking lockup bottom-right = the real `spiking-logo-final.png`.

## Logo rule (hard rule)
- The Spiking logo MUST be the original `spiking-logo-final.png` from this folder, placed as-is. Never generate, redraw, recreate, recolor, stretch or "improve" it with AI. If the image generator draws it, replace it with the real PNG before delivering. Leave clean empty space bottom-right for it.
- Same for third-party company logos: use the real logos, never invent them.

## Less text
- No Key Takeaway box, no extra callout boxes, no "Note:" paragraphs, no tiny footnotes, no methodology text, no legends if direct labels work.
- On canvas: kicker + headline + one short sentence + chart labels + one-line source. Each chart row = logo/name + bar + ONE value. Max 10-12 rows.

## Components
- Rounded cards (~20px radius), rounded bar ends, thin light gridlines only if needed, value labels at bar end, +/- deltas as small #124de3 pills.
- Optional faint photo (data center, HQ, portrait) fading into white at an edge, never behind text (sample-01, sample-04).

## Content to prioritize (US stock investing, high search demand)
Top holdings of S&P 500 / Nasdaq / Berkshire and other famous portfolios; best/worst performing stocks YTD; Magnificent 7 comparisons (revenue, profit, P/E); "how [company] makes money" (revenue by segment); where $100 of revenue goes; dividend leaders; biggest companies by market cap; sector weights; earnings winners; AI infrastructure winners; ETF top holdings (SPY, QQQ, VOO). Primary sources only (SEC filings, company reports, Fed, index providers); as-of date in the kicker or source line.

## Final approval checklist (all must pass before delivering)
1. Logo: the real `spiking-logo-final.png`, untouched and crisp. Never AI-made.
2. References: compared side by side with the 2-3 closest approved samples; layout, fonts, spacing and colors match.
3. Colors: only the palette hex values above (no black/grey/other blues).
4. Data: every figure verified against a primary source BEFORE designing; as-of date and source line present; numbers in the chart match the brief exactly.
5. Text: headline simple and truthful; no Key Takeaway box, no notes, no tiny text; nothing cut off or overlapping.
6. Quality: inspect the exported PNG at full size (1080x1350): spelling, alignment, spacing, logo accuracy, visual consistency with the samples.
7. Delivery: only replace an existing page for the same day (e.g. in Canva) after items 1-6 pass.

## Prompt template for image generation
"Create a 1080x1350 (4:5) US-stock infographic that matches the attached Spiking reference posts EXACTLY in layout, fonts and spacing. Do not invent a new style.
Colors, exact hex only: white background; headline line 1 and body text #132458; headline line 2 and hero numbers #124de3; dark cards #132458; pale cards #eef6ff / #d9ebff; chart bars from #124de3, #256bf7, #3083ff, #57a7ff, #8dc7ff, #bbdcff (darkest = largest). No black, no grey, no other colors.
Headline (2 lines, ALL CAPS, extra-bold, same size): <LINE 1> / <LINE 2>. Optional one-line subhead: <...>.
Hero visual: <ranked list with bars + logos | waterfall | donut list | 2-line chart with stat cards>, using ONLY these numbers: <verified data>. Max 10-12 rows, one value per row.
No Key Takeaway box, no notes, no small footnotes. Footer: one line 'Source: <...>'. Leave an empty clean area bottom-right for the Spiking logo; do NOT draw any Spiking logo (the real PNG will be placed afterwards).
Light, airy, minimal text."
