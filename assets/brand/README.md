# Fluxzero GitHub brand assets

These assets carry the Fluxzero website identity into GitHub. The source of truth is `fluxzero-site/src/config/brand.mjs` and the website's versioned brand vectors and styles.

The September 2026 set uses website brand `ea5f28b5-8e77-4cd0-ac01-fa8b5114a472`: a dark `#05070B` background, pale `#F4F7FF` text, and the existing blue-gradient mark and wordmark. The display and body lettering use the website's Google Sans Flex and Inter fonts. All lettering is upright, as required for the GitHub identity. Text is converted to outlines for reliable GitHub rendering. Supply descriptive image alt text wherever these exports are embedded.

| Asset | Use |
| --- | --- |
| `2026-09/fluxzero-logo.svg` | Unmodified website mark and wordmark. |
| `2026-09/fluxzero-mark.svg` | Unmodified website symbol. |
| `2026-09/organization-hero.svg` | Original organization profile hero. |
| `2026-09/profile/hero.svg` | Compact organization hero; homepage headline verbatim. |
| `2026-09/profile/{cli,agents,sdk}-{light,dark}.svg` | Linked icon buttons with functional captions for light and dark GitHub themes. |
| `2026-09/repository-header.svg` | Shared header for Fluxzero-owned projects. |
| `2026-09/engineering-header.svg` | Compact header for platform engineering forks. |
| `2026-09/avatar.png` | Organization avatar, with padding for circular crops. |
| `2026-09/social/*.png` | Repository-specific GitHub social previews, 1280 × 640 pixels. |

SVG sources are included for the avatar and social previews. Keep existing versioned URLs available when refreshing the identity; old commits and release READMEs may reference them.

## Regeneration

Use Python with `fonttools` and a website checkout:

```sh
python scripts/build-brand-assets.py --website /path/to/flux-website
```

Run this from the repository root. To export PNGs, use an SVG renderer such as `sharp`, preserving each SVG's native dimensions. The organization avatar is 512 × 512 pixels; social previews are 1280 × 640 pixels. Review both compact and full-size renders before publishing.

The logo vectors are copied directly from the website. Font binaries are not redistributed here. Fluxzero logos and branding are all rights reserved.

## Copy source

Marketing copy, including all banners, comes verbatim from the website's `src/pages/index.astro`:

- “The European cloud for AI-built apps” — homepage headline.
- “The all-in-one cloud with frontend, backend, data, security, and observability working as one.” — homepage introduction.
- “Everything your product needs to run” — homepage platform comparison.

Button labels identify tools. Their captions describe function: “Create and run projects”, “For your coding agent”, and “Java and Kotlin”. Do not add new marketing slogans when revising the profile or image exports. Preview changes before publishing them on the organization page.
