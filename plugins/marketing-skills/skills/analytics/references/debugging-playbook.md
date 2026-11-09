# Tracking Debug Playbook

A step-by-step method for finding why an analytics event, parameter, or count is wrong. For conversions that must reach an ad platform (pixels, Conversions API, imports) and for "GA4 and Google Ads don't match," use the **conversion-tracking** skill instead.

## Contents
- Why tracking bugs are hard
- The debug stack
- Tools
- Common issues and fixes
- Debug checklist

## Why tracking bugs are hard

1. They fail silently: no error, just missing or doubled data.
2. They often appear only in production.
3. Timing, consent, ad blockers, and configuration can all cause them.

Work layer by layer. Verify each layer before moving to the next, and don't guess.

## The debug stack

```
Layer 5: GA4 reports and DebugView    what you see
Layer 4: GA4 processing               where it lands (filters, thresholds, custom definitions)
Layer 3: Network request              what was sent
Layer 2: GTM tags and triggers        what GTM did
Layer 1: dataLayer and app code       what the app pushed
```

When something is missing at layer 5, start at layer 1 and confirm each layer on the way up.

## Tools

### GTM Preview mode

1. GTM → Preview, enter the site URL, connect.
2. Perform the action you are debugging in the connected tab.
3. In the Tag Assistant panel: the left column lists events as they happen (page view, click, custom event); the middle shows tags fired and not fired for the selected event; the variables tab shows each variable's value at that moment.

### GA4 DebugView

Debug traffic appears in Admin → Data display → DebugView. Turn debug mode on in one of three ways:
- Run the site through GTM Preview mode (debug mode is on automatically).
- Add `debug_mode: true` to the Google tag or the event's parameters.
- Use the GA Debugger browser extension.

Events usually show within seconds. Standard reports take 24–48 hours.

### Browser DevTools, Network tab

1. Filter requests by `collect`.
2. Perform the action.
3. Open the request to `google-analytics.com/g/collect` (or your first-party endpoint) and read the payload: event name (`en`) and parameters (`ep.*`, `epn.*`).

## Common issues and fixes

### The event fires in GTM Preview but not in GA4

1. **Consent denied.** In Preview, check the consent state; `analytics_storage` denied means no hit or a cookieless ping. Test with consent granted.
2. **A data filter drops it.** Admin → Data filters: an active internal-traffic or developer filter removes your test traffic. Test from an excluded network, or check the filter state.
3. **Debug mode is off.** DebugView shows only debug traffic (see Tools).
4. **Wrong property.** Compare the measurement ID in the Google tag with the data stream you are viewing.
5. **Two Google tags (GA4 configuration).** Duplicates double sessions and confuse data. Keep one, firing on all pages.

### The event doesn't fire in GTM Preview at all

1. **Trigger.** Is the tag's trigger listed under that event in Preview? If not, the trigger didn't fire.
2. **Conditions.** Reproduce the action and read the variable values at that moment: do they match the trigger conditions?
3. **dataLayer event name.** For custom-event triggers, the pushed `event` must match the trigger exactly, including case.
4. **Timing.** The element isn't there yet: switch from Page View to DOM Ready or Window Loaded. In a single-page app, route changes are not page loads: use a History Change trigger or a router push (see gtm-implementation.md, Single-Page App Page Views).

### A parameter shows as (not set) or undefined

1. **In the request?** Search the collect payload for the parameter. Missing means the GTM variable didn't resolve.
2. **The GTM variable.** In Preview, read the data layer variable's value; `undefined` means the push lacked the key or the key is misspelled.
3. **The push itself.** In the console: `dataLayer.filter(e => e.event === 'your_event_name')`. Is the key present and spelled right?
4. **Registered in GA4?** A parameter needs a custom definition (Admin → Custom definitions) to appear in reports; without one it exists only in raw data and exports.

### The event fires twice per action

Find it: count tags fired for the action in Preview, and count collect hits in the Network tab. Usual causes:

1. **Enhanced measurement plus a GTM tag** for the same action (outbound clicks, file downloads, video). Turn off one of them.
2. **Two Google tags**, each sending its own hits.
3. **Single-page app double page views:** GA4's history-based page views plus a History Change tag. Keep one.
4. **Two triggers that both match.** Make the triggers specific, or add exceptions.

### Sessions or users look wrong

- **Too many sessions:** duplicate Google tags; double page views in a single-page app; the client ID cookie blocked or cleared.
- **Too few sessions or users:** consent mode blocking non-consenting visitors (expected under strict consent); tags firing on only some pages.
- **Sessions restart between pages:** cross-domain measurement not configured, cookie domain mismatch, or a self-referral (see ga4-implementation.md, Cross-Domain Tracking).

### GA4 and an ad platform disagree

Expected to a degree, and owned by the **conversion-tracking** skill: date bookkeeping, attribution models, windows, and modeling all differ. Load its discrepancies reference before calling it a bug.

## Debug checklist

```
[ ] Exact event name and parameters expected, from the tracking plan
[ ] App pushes to dataLayer (console: dataLayer)
[ ] GTM Preview: trigger fires at the right moment
[ ] GTM Preview: parameters resolve (not undefined)
[ ] Network: collect request carries the right payload
[ ] DebugView: event and parameters arrive
[ ] Reports: event appears after processing (24-48 h)
[ ] Consent: tested with analytics consent granted
[ ] Filters: no data filter drops the test traffic
```
