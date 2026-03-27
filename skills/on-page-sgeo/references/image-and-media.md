# Image and Media Optimization

Images affect page speed (LCP), visual stability (CLS), accessibility, image search visibility, and increasingly, multimodal AI search. Getting image optimization right is mostly about not getting it wrong — the defaults in most CMSs and frameworks are bad.

## Format Decision Tree

Choose the format based on the image content, not habit:

| Image Type | Best Format | Why | Fallback |
|------------|------------|-----|----------|
| Photographs / complex imagery | WebP | 25-35% smaller than JPEG at equivalent quality, 95% browser support | JPEG (use `<picture>` with `<source>` for WebP + JPEG fallback) |
| Photographs (cutting-edge) | AVIF | 50% smaller than JPEG, better quality at low bitrates | WebP (85% browser support for AVIF — check your audience) |
| Icons, illustrations, logos | SVG | Scalable to any size, tiny file size, CSS-stylable | PNG only if SVG is impractical |
| Screenshots with text | PNG or WebP | JPEG artifacts are visible on sharp text edges | — |
| Animated content | Video (MP4/WebM) | 90% smaller than GIF for equivalent content | GIF only for tiny UI micro-animations (<50KB) |

**Stop using JPEG and PNG by default.** WebP has 95% browser support as of 2026. The only reason to serve JPEG/PNG is as a fallback for the remaining 5%.

## Compression Targets

Different image roles have different size budgets:

| Image Role | Target Size | Why |
|------------|-------------|-----|
| Hero / above-fold | < 150KB | Directly impacts LCP. The hero image is usually the LCP element. |
| In-content images | < 100KB | Balance between quality and page weight |
| Thumbnails | < 30KB | Small display size means small file is fine |
| Icons | < 5KB | Should be SVG whenever possible |

**Tools:**
- **Squoosh** (squoosh.app) — Manual, single image, visual quality comparison
- **Sharp** (Node.js) — Programmatic, build pipeline integration
- **next/image** (Next.js) — Automatic optimization, responsive srcset, lazy loading
- **Imagify / ShortPixel** (WordPress) — Plugin-based automatic optimization on upload

## Responsive Images

Serve different image sizes for different viewports. Don't send a 2400px image to a 375px phone screen.

**`srcset` and `sizes` attributes:**

```html
<img
  src="photo-800.webp"
  srcset="photo-400.webp 400w, photo-800.webp 800w, photo-1200.webp 1200w"
  sizes="(max-width: 600px) 400px, (max-width: 1024px) 800px, 1200px"
  alt="Descriptive alt text"
  width="1200"
  height="675"
  loading="lazy"
>
```

**Art direction with `<picture>`:**

Use `<picture>` when you need different image crops for different viewports (not just different sizes):

```html
<picture>
  <source media="(max-width: 600px)" srcset="photo-mobile.webp">
  <source media="(max-width: 1024px)" srcset="photo-tablet.webp">
  <img src="photo-desktop.webp" alt="Descriptive alt text" width="1200" height="675">
</picture>
```

## Lazy Loading Rules

- Add `loading="lazy"` to all images below the fold
- **NEVER** lazy-load the LCP image (usually the hero image, the first large image on the page)
- **NEVER** lazy-load images in the first viewport (approximately the first 600-800px of content)
- The browser needs to start loading the LCP image immediately — lazy loading delays it by definition

**How to identify the LCP image:** Run PageSpeed Insights on your page. The "Largest Contentful Paint element" section tells you exactly which element is LCP. If it's an image, that image must not be lazy-loaded.

## CLS Prevention

Cumulative Layout Shift happens when images load and push content around. Two ways to prevent it:

**Option 1: Explicit `width` and `height` attributes**
```html
<img src="photo.webp" alt="..." width="1200" height="675">
```
The browser calculates the aspect ratio and reserves space before the image loads.

**Option 2: CSS `aspect-ratio`**
```css
img { aspect-ratio: 16 / 9; width: 100%; height: auto; }
```

**Both work.** HTML attributes are more reliable across browsers. CSS is cleaner when you control the stylesheet. Pick one and be consistent.

**Common CLS mistake:** Lazy-loaded images without dimensions. The browser reserves zero space, the image loads, and everything below it shifts. Always set dimensions on lazy-loaded images.

## Alt Text Guide

Alt text serves three purposes: accessibility (screen readers), image search ranking, and AI image understanding.

**Rules:**

- Descriptive and concise — under 125 characters
- Describe what the image shows, not what you want to rank for
- Include the keyword ONLY if the image genuinely relates to it
- Decorative images (visual separators, background patterns): `alt=""` — empty string, not omitted

**Examples:**

```
BAD:  alt="image"
WHY:  Useless to screen readers and crawlers.

BAD:  alt="" (on a meaningful chart or screenshot)
WHY:  Tells screen readers to skip it, tells crawlers it's decorative.

BAD:  alt="SEO audit tool best technical SEO checklist 2026"
WHY:  Keyword stuffing. Describes what you want to rank for, not the image.

GOOD: alt="Screaming Frog crawl report showing 47 pages with redirect chains"
WHY:  Describes the actual image content. Specific. Useful to screen readers.

GOOD: alt="Bar chart comparing LCP scores: before optimization 4.2s, after 1.8s"
WHY:  Describes the data in the chart for users who cannot see it.
```

## File Naming

Use descriptive, hyphenated file names:

```
BAD:  IMG_4827.jpg, photo1.png, Untitled-1.webp
GOOD: technical-seo-audit-crawl-report.webp, invoice-dashboard-screenshot.webp
```

File names are a minor signal but contribute to image search visibility and URL readability.

Run `scripts/check-images.py --url <URL>` to audit all images on a page — alt text quality, file sizes, format detection, dimension attributes, and lazy loading compliance.
