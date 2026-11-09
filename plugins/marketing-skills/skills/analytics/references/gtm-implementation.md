# Google Tag Manager Implementation Reference

Detailed guide for implementing tracking via Google Tag Manager.

## Contents
- Container Structure (tags, triggers, variables)
- Naming Conventions
- Data Layer Patterns
- Common Tag Configurations (GA4 configuration tag, GA4 event tag, Facebook pixel)
- Single-Page App Page Views
- Preview and Debug
- Workspaces and Versioning (publishing protocol, environments)
- Consent Management
- Advanced Patterns (tag sequencing, exception handling, custom JavaScript variables)

## Container Structure

### Tags

Tags are code snippets that execute when triggered.

**Common tag types:**
- GA4 Configuration (base setup)
- GA4 Event (custom events)
- Google Ads Conversion
- Facebook Pixel
- LinkedIn Insight Tag
- Custom HTML (for other pixels)

### Triggers

Triggers define when tags fire.

**Built-in triggers:**
- Page View: All Pages, DOM Ready, Window Loaded
- Click: All Elements, Just Links
- Form Submission
- Scroll Depth
- Timer
- Element Visibility

**Custom triggers:**
- Custom Event (from dataLayer)
- Trigger Groups (multiple conditions)

### Variables

Variables capture dynamic values.

**Built-in (enable as needed):**
- Click Text, Click URL, Click ID, Click Classes
- Page Path, Page URL, Page Hostname
- Referrer
- Form Element, Form ID

**User-defined:**
- Data Layer variables
- JavaScript variables
- Lookup tables
- RegEx tables
- Constants

---

## Naming Conventions

### Recommended Format

```
[Type] - [Description] - [Detail]

Tags:
GA4 - Event - Signup Completed
GA4 - Config - Base Configuration
FB - Pixel - Page View
HTML - LiveChat Widget

Triggers:
Click - CTA Button
Submit - Contact Form
View - Pricing Page
Custom - signup_completed

Variables:
DL - user_id
JS - Current Timestamp
LT - Campaign Source Map
```

---

## Data Layer Patterns

### Basic Structure

```javascript
// Initialize (in <head> before GTM)
window.dataLayer = window.dataLayer || [];

// Push event
dataLayer.push({
  'event': 'event_name',
  'property1': 'value1',
  'property2': 'value2'
});
```

### Page Load Data

```javascript
// Set on page load (before GTM container)
window.dataLayer = window.dataLayer || [];
dataLayer.push({
  'pageType': 'product',
  'contentGroup': 'products',
  'user': {
    'loggedIn': true,
    'userId': '12345',
    'userType': 'premium'
  }
});
```

### Form Submission

```javascript
document.querySelector('#contact-form').addEventListener('submit', function() {
  dataLayer.push({
    'event': 'form_submitted',
    'formName': 'contact',
    'formLocation': 'footer'
  });
});
```

### Button Click

```javascript
document.querySelector('.cta-button').addEventListener('click', function() {
  dataLayer.push({
    'event': 'cta_clicked',
    'ctaText': this.innerText,
    'ctaLocation': 'hero'
  });
});
```

### E-commerce Events

```javascript
// Product view
dataLayer.push({ ecommerce: null }); // Clear previous
dataLayer.push({
  'event': 'view_item',
  'ecommerce': {
    'items': [{
      'item_id': 'SKU123',
      'item_name': 'Product Name',
      'price': 99.99,
      'item_category': 'Category',
      'quantity': 1
    }]
  }
});

// Add to cart
dataLayer.push({ ecommerce: null });
dataLayer.push({
  'event': 'add_to_cart',
  'ecommerce': {
    'items': [{
      'item_id': 'SKU123',
      'item_name': 'Product Name',
      'price': 99.99,
      'quantity': 1
    }]
  }
});

// Purchase
dataLayer.push({ ecommerce: null });
dataLayer.push({
  'event': 'purchase',
  'ecommerce': {
    'transaction_id': 'T12345',
    'value': 99.99,
    'currency': 'USD',
    'tax': 5.00,
    'shipping': 10.00,
    'items': [{
      'item_id': 'SKU123',
      'item_name': 'Product Name',
      'price': 99.99,
      'quantity': 1
    }]
  }
});
```

---

## Common Tag Configurations

### GA4 Configuration Tag

**Tag Type:** Google Analytics: GA4 Configuration

**Settings:**
- Measurement ID: G-XXXXXXXX
- Send page view: Checked (for pageviews)
- User Properties: Add any user-level dimensions

**Trigger:** All Pages

### GA4 Event Tag

**Tag Type:** Google Analytics: GA4 Event

**Settings:**
- Configuration Tag: Select your config tag
- Event Name: {{DL - event_name}} or hardcode
- Event Parameters: Add parameters from dataLayer

**Trigger:** Custom Event with event name match

### Facebook Pixel - Base

**Tag Type:** Custom HTML

```html
<script>
  !function(f,b,e,v,n,t,s)
  {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
  n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];
  s.parentNode.insertBefore(t,s)}(window, document,'script',
  'https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', 'YOUR_PIXEL_ID');
  fbq('track', 'PageView');
</script>
```

**Trigger:** All Pages

### Facebook Pixel - Event

**Tag Type:** Custom HTML

```html
<script>
  fbq('track', 'Lead', {
    content_name: '{{DL - form_name}}'
  });
</script>
```

**Trigger:** Custom Event - form_submitted

---

## Single-Page App Page Views

A single-page app changes routes without loading a new page, so a Page View trigger fires once and every later screen goes unrecorded (reports show one path, or `(not set)`). Pick one of two approaches, and only one: both together double-count.

**A: History Change trigger (simplest).** GA4's enhanced measurement can already send page views on browser-history changes ("Page changes based on browser history events"). Either leave that on and add nothing in GTM, or turn it off and build the GTM version:
1. Trigger: type History Change, named `History Change - Route`.
2. Tag: GA4 Event, event name `page_view`, parameters `page_location` = `{{Page URL}}` and `page_title` = `{{Page Title}}`, fired by that trigger.
3. Keep the Google tag's page view for the first load; the History Change trigger covers the routes after it. If the router also rewrites the URL on load, the first screen counts twice: add a trigger condition that skips it, or use approach B.

**B: Router push (more reliable).** The app pushes a page view after each navigation, once the new title is set:

```javascript
// In the router's after-navigation hook
router.afterEach((to) => {
  window.dataLayer.push({
    event: 'page_view',
    page_path: to.path,
    page_title: document.title
  });
});
```

Test either approach by clicking through three routes in Preview and counting one page view per route in DebugView.

---

## Preview and Debug

### Preview Mode

1. Click "Preview" in GTM
2. Enter site URL
3. GTM debug panel opens at bottom

**What to check:**
- Tags fired on this event
- Tags not fired (and why)
- Variables and their values
- Data layer contents

### Debug Tips

**Tag not firing:**
- Check trigger conditions
- Verify data layer push
- Check tag sequencing

**Wrong variable value:**
- Check data layer structure
- Verify variable path (nested objects)
- Check timing (data may not exist yet)

**Multiple firings:**
- Check trigger uniqueness
- Look for duplicate tags
- Check tag firing options

---

## Workspaces and Versioning

### Workspaces

Use workspaces for team collaboration:
- Default workspace for production
- Separate workspaces for large changes
- Merge when ready

### Version Management

**Best practices:**
- Name every version descriptively
- Add notes explaining changes
- Review changes before publish
- Keep production version noted

**Version notes example:**
```
v15: Added purchase conversion tracking
- New tag: GA4 - Event - Purchase
- New trigger: Custom Event - purchase
- New variables: DL - transaction_id, DL - value
- Tested: Chrome, Safari, Mobile
```

### Publishing Protocol

1. Test in Preview mode: the events fire on the right triggers.
2. Check GA4 DebugView: the parameters arrive.
3. Read the workspace's change summary, so nothing unrelated ships with it.
4. Write version notes: what changed and why.
5. Publish.
6. Confirm in GA4 Realtime that the events still arrive after publishing.

### Environments

Create environments in Admin → Environments (for example development and staging besides live). Give developers the staging snippet so they test against the same container before you publish to live.

---

## Consent Management

### Consent Mode Integration

```javascript
// Default state (before consent)
gtag('consent', 'default', {
  'analytics_storage': 'denied',
  'ad_storage': 'denied'
});

// Update on consent
function grantConsent() {
  gtag('consent', 'update', {
    'analytics_storage': 'granted',
    'ad_storage': 'granted'
  });
}
```

Run the default command before GTM loads. If the consent banner loads asynchronously, add `'wait_for_update': 500` (milliseconds) to the default so tags wait for the banner's answer instead of firing as denied.

**Basic vs advanced consent mode.** Basic mode blocks Google tags until the visitor consents: declined visitors send nothing. Advanced mode loads the tags with storage denied and sends cookieless pings, which GA4 uses to model the declined share. Advanced gives fuller numbers; basic is simpler to defend. Record which one the property uses, since reports mean different things under each.

### GTM Consent Overview

1. Enable Consent Overview in Admin
2. Configure consent for each tag
3. Tags respect consent state automatically

---

## Advanced Patterns

### Tag Sequencing

**Setup tags to fire in order:**
Tag Configuration > Advanced Settings > Tag Sequencing

**Use cases:**
- Config tag before event tags
- Pixel initialization before tracking
- Cleanup after conversion

### Exception Handling

**Trigger exceptions** - Prevent tag from firing:
- Exclude certain pages
- Exclude internal traffic
- Exclude during testing

### Custom JavaScript Variables

```javascript
// Get URL parameter
function() {
  var params = new URLSearchParams(window.location.search);
  return params.get('campaign') || '(not set)';
}

// Get cookie value
function() {
  var match = document.cookie.match('(^|;) ?user_id=([^;]*)(;|$)');
  return match ? match[2] : null;
}

// Read a machine-readable amount, not the localized display text.
// Example: <span class="product-price" data-price="1234.56">$1,234.56</span>
function() {
  var el = document.querySelector('.product-price');
  var raw = el ? el.getAttribute('data-price') : null;
  if (raw === null || !/^(?:0|[1-9][0-9]*)(?:\.[0-9]+)?$/.test(raw)) return null;
  var amount = Number(raw);
  return isFinite(amount) ? amount : null;
}
```

For monetary tracking, prefer the numeric amount and currency from the application data layer. If a DOM variable is needed, have the application render `data-price` as an unformatted, non-negative decimal in major currency units; pass its currency separately. Do not infer the amount or currency from presentation text: `parseFloat` turns `$1,234.56` into `1` after removing `$`, and localized separators have different meanings. A missing or invalid amount returns `null`, so skip that monetary event or diagnose it before sending; reserve `0` for an explicitly free item.
