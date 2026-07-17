---
name: vision
description: Use when the user shares a screenshot, image, or UI design reference. Analyze visual layouts, compare UI states, identify styling issues, read text/numbers from images, and translate visual designs into CSS/HTML changes. Trigger on phrases like "look at this screenshot", "compare these UIs", "fix the layout", "read this image", or when any image file is attached.
---

# Vision Skill

Analyze images, screenshots, and UI designs shared by the user.

## Capabilities

1. **Read images** — Use the Read tool to open PNG/JPG files and PDFs
2. **Analyze UI** — Describe layout, colors, spacing, alignment, and visual hierarchy
3. **Compare states** — Before/after comparisons for UI changes
4. **Extract text** — Read numbers, labels, and text from calculator screenshots
5. **Identify issues** — Spot misalignment, overflow, contrast problems, missing elements
6. **Translate to code** — Convert visual observations into CSS/HTML edit suggestions

## Workflow

When the user shares an image:

1. Read the image file using the Read tool
2. Describe what you see in detail (layout, colors, elements, spacing)
3. If comparing two images, highlight differences
4. If asked to fix something, propose specific CSS/HTML changes with exact selectors and values
5. If asked to verify, check against the design spec or TEST_GUIDE.md expected values

## Calculator UI Context

This project has a dark theme calculator UI:
- Background gradient: `#1a1a2e` → `#16213e`
- Calculator card: `#0f3460`
- Button base: `#16213e`
- Operator buttons: `#e94560` (red)
- Equals button: `#2ed573` (green)
- Text: `#ffffff` (white)
- Border radius: `20px` for card, `12px` for buttons

Use these values as reference when analyzing UI screenshots.
