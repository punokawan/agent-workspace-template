# Core Web Vitals

Use this when an audit covers page speed, a page fails Core Web Vitals in Search Console, or the user asks whether slowness hurts rankings.

## Contents
- Thresholds and how Google measures them
- Field data versus lab data
- Speed factors to check
- Fixes by metric
- Tools

## Thresholds and how Google measures them

| Metric | What it measures | Good | Needs improvement | Poor |
|---|---|---|---|---|
| **LCP** (Largest Contentful Paint) | Loading: when the main content is visible | ≤ 2.5s | 2.5–4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | Responsiveness: delay after a tap, click, or key press | ≤ 200ms | 200–500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | Visual stability: unexpected layout jumps | ≤ 0.1 | 0.1–0.25 | > 0.25 |

- A page passes when the **75th percentile** of real-user visits is in the "Good" band for all three metrics.
- Mobile and desktop are assessed separately. Report both, and lead with mobile.
- Search Console groups similar URLs, so one slow template can fail hundreds of pages at once. Fix the template, not the URL.
- Map to audit priority: "Poor" on key templates is **High**; "Needs improvement" is **Medium**.

## Field data versus lab data

- **Field data** (CrUX, the Chrome User Experience Report: a rolling 28-day window of real Chrome users) is what Google uses for the page experience signal. Search Console's Core Web Vitals report and the field section of PageSpeed Insights show it.
- **Lab data** (Lighthouse, the lab section of PageSpeed Insights, WebPageTest) is a synthetic load on one device and network. Use it to find causes, not to declare pass or fail.
- Low-traffic pages may have no field data. Say so, use the origin-level data if it exists, and label lab-only findings as lab results.
- For your own monitoring, the `web-vitals` JavaScript library reports the same metrics from real users to your analytics.
- After a fix ships, field data needs up to 28 days to reflect it. Don't judge a fix after a few days.

## Speed factors to check

- Server response time (TTFB; aim for 0.8s or less)
- Image optimization
- JavaScript execution
- CSS delivery
- Caching headers
- CDN usage
- Font loading

## Fixes by metric

### LCP above 2.5s
- Find the LCP element first (usually a hero image or headline block).
- Serve that image in a modern format (WebP or AVIF) at the displayed size, and preload it or give it `fetchpriority="high"`. Never lazy-load the LCP image.
- Reduce server response time: caching, a CDN for static assets, fewer redirects before the page.
- Remove render-blocking CSS and JavaScript from the critical path.

### INP above 200ms
- Break long tasks (over 50ms) into smaller chunks and yield to the main thread.
- Defer non-critical JavaScript, and load third-party scripts (chat widgets, tag managers, A/B testing tools) after the page is interactive.
- Move low-priority work off the interaction path (`requestIdleCallback`, web workers).
- Keep event handlers short; show visual feedback before slow work starts.

### CLS above 0.1
- Set explicit `width` and `height` (or `aspect-ratio`) on images, videos, and iframes.
- Reserve space for ads, embeds, and banners before they load.
- Don't insert content above existing content after load (cookie bars, promo bars) unless it responds to a user action.
- Stop web fonts from moving text: preload key fonts and match the fallback font's metrics (`size-adjust`), or use `font-display: optional`.

## Tools

- PageSpeed Insights (field and lab data for one URL)
- Search Console Core Web Vitals report (field data for URL groups)
- WebPageTest (filmstrips and request waterfalls)
- Chrome DevTools Performance panel (long tasks, layout shifts)
