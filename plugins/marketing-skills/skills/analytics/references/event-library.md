# Event Library Reference

Comprehensive list of events to track by business type and context.

## Contents
- Naming Vocabulary (standard action verbs, naming rules)
- Marketing Site Events (navigation & engagement, CTA & form interactions, conversion events)
- Product/App Events (onboarding, core usage, errors & support)
- Monetization Events (pricing & checkout, subscription management)
- E-commerce Events (browsing, cart, checkout, post-purchase)
- B2B / SaaS Specific Events (team & collaboration, integration events, account events)
- Event Properties (Parameters)
- Funnel Event Sequences
- Tracking Plan Governance (status columns, change protocol, schema versions)

## Naming Vocabulary

One verb per meaning. A plan that mixes `_complete`, `_completed`, `_done`, and `_finished` splits one action into four events that never add up.

| Verb | Use for |
|------|---------|
| `_started` | The first step of a multi-step process |
| `_completed` | Successful completion of a process |
| `_failed` | An attempt that errored |
| `_submitted` | A form or data submission |
| `_viewed` | A passive view of a page, modal, or content |
| `_clicked` | A direct click on a specific element |
| `_selected` | A choice among options (plan, variant, filter) |
| `_opened` / `_closed` | A modal, drawer, or chat window |
| `_downloaded` | A file download |
| `_activated` | A feature used for the first time |
| `_upgraded` / `_cancelled` | Plan changes |
| `_dismissed` | A prompt the user explicitly closed or ignored |
| `_searched` | A search query submitted |

Naming rules:
- Object first, then the verb: `plan_selected`, not `selected_plan`.
- Past tense for anything finished: `checkout_completed`, not `checkout_complete`.
- Specific over generic: `trial_started`, not `event_triggered`.
- Four words at most: `onboarding_step_completed`, not a sentence.

## Marketing Site Events

### Navigation & Engagement

| Event Name | Description | Properties |
|------------|-------------|------------|
| page_view | Page loaded (enhanced) | page_title, page_location, content_group |
| scroll_depth | User scrolled to threshold | depth (25, 50, 75, 100) |
| outbound_link_clicked | Click to external site | link_url, link_text |
| internal_link_clicked | Click within site | link_url, link_text, location |
| video_played | Video started | video_id, video_title, duration |
| video_completed | Video finished | video_id, video_title, duration |

### CTA & Form Interactions

| Event Name | Description | Properties |
|------------|-------------|------------|
| cta_clicked | Call to action clicked | button_text, cta_location, page |
| form_started | User began form | form_name, form_location |
| form_field_completed | Field filled | form_name, field_name |
| form_submitted | Form successfully sent | form_name, form_location |
| form_error | Form validation failed | form_name, error_type |
| resource_downloaded | Asset downloaded | resource_name, resource_type |

### Conversion Events

| Event Name | Description | Properties |
|------------|-------------|------------|
| signup_started | Initiated signup | source, page |
| signup_completed | Finished signup | method, plan, source |
| demo_requested | Demo form submitted | company_size, industry |
| contact_submitted | Contact form sent | inquiry_type |
| newsletter_subscribed | Email list signup | source, list_name |
| trial_started | Free trial began | plan, source |

---

## Product/App Events

### Onboarding

| Event Name | Description | Properties |
|------------|-------------|------------|
| signup_completed | Account created | method, referral_source |
| onboarding_started | Began onboarding | - |
| onboarding_step_completed | Step finished | step_number, step_name |
| onboarding_completed | All steps done | steps_completed, time_to_complete |
| onboarding_skipped | User skipped onboarding | step_skipped_at |
| first_key_action_completed | Aha moment reached | action_type |

### Core Usage

| Event Name | Description | Properties |
|------------|-------------|------------|
| session_started | App session began | session_number |
| feature_used | Feature interaction | feature_name, feature_category |
| action_completed | Core action done | action_type, count |
| content_created | User created content | content_type |
| content_edited | User modified content | content_type |
| content_deleted | User removed content | content_type |
| search_performed | In-app search | query, results_count |
| settings_changed | Settings modified | setting_name, new_value |
| invite_sent | User invited others | invite_type, count |

### Errors & Support

| Event Name | Description | Properties |
|------------|-------------|------------|
| error_occurred | Error experienced | error_type, error_message, page |
| help_opened | Help accessed | help_type, page |
| support_contacted | Support request made | contact_method, issue_type |
| feedback_submitted | User feedback given | feedback_type, rating |

---

## Monetization Events

### Pricing & Checkout

| Event Name | Description | Properties |
|------------|-------------|------------|
| pricing_viewed | Pricing page seen | source |
| plan_selected | Plan chosen | plan_name, billing_cycle |
| checkout_started | Began checkout | plan, value |
| payment_info_entered | Payment submitted | payment_method |
| purchase_completed | Purchase successful | plan, value, currency, transaction_id |
| purchase_failed | Purchase failed | error_reason, plan |

### Subscription Management

| Event Name | Description | Properties |
|------------|-------------|------------|
| trial_started | Trial began | plan, trial_length |
| trial_ended | Trial expired | plan, converted (bool) |
| subscription_upgraded | Plan upgraded | from_plan, to_plan, value |
| subscription_downgraded | Plan downgraded | from_plan, to_plan |
| subscription_cancelled | Cancelled | plan, reason, tenure, save_offer_shown |
| subscription_renewed | Renewed | plan, value |
| billing_updated | Payment method changed | - |
| save_offer_accepted | Took a retention offer at cancel | offer_type, plan, discount_pct |
| subscription_paused | Paused instead of cancelling | pause_duration_days, pause_reason |
| subscription_reactivated | Cancelled customer returned | plan, days_since_cancel |
| churn_risk_detected | Risk score crossed a threshold | risk_score, risk_signals |

---

## E-commerce Events

### Browsing

| Event Name | Description | Properties |
|------------|-------------|------------|
| product_viewed | Product page viewed | product_id, product_name, category, price |
| product_list_viewed | Category/list viewed | list_name, products[] |
| product_searched | Search performed | query, results_count |
| product_filtered | Filters applied | filter_type, filter_value |
| product_sorted | Sort applied | sort_by, sort_order |

### Cart

| Event Name | Description | Properties |
|------------|-------------|------------|
| product_added_to_cart | Item added | product_id, product_name, price, quantity |
| product_removed_from_cart | Item removed | product_id, product_name, price, quantity |
| cart_viewed | Cart page viewed | cart_value, items_count |

### Checkout

| Event Name | Description | Properties |
|------------|-------------|------------|
| checkout_started | Checkout began | cart_value, items_count |
| checkout_step_completed | Step finished | step_number, step_name |
| shipping_info_entered | Address entered | shipping_method |
| payment_info_entered | Payment entered | payment_method |
| coupon_applied | Coupon used | coupon_code, discount_value |
| purchase_completed | Order placed | transaction_id, value, currency, items[] |

### Post-Purchase

| Event Name | Description | Properties |
|------------|-------------|------------|
| order_confirmed | Confirmation viewed | transaction_id |
| refund_requested | Refund initiated | transaction_id, reason |
| refund_completed | Refund processed | transaction_id, value |
| review_submitted | Product reviewed | product_id, rating |

---

## B2B / SaaS Specific Events

### Team & Collaboration

| Event Name | Description | Properties |
|------------|-------------|------------|
| team_created | New team/org made | team_size, plan |
| team_member_invited | Invite sent | role, invite_method |
| team_member_joined | Member accepted | role |
| team_member_removed | Member removed | role |
| role_changed | Permissions updated | user_id, old_role, new_role |

### Integration Events

| Event Name | Description | Properties |
|------------|-------------|------------|
| integration_viewed | Integration page seen | integration_name |
| integration_started | Setup began | integration_name |
| integration_connected | Successfully connected | integration_name |
| integration_disconnected | Removed integration | integration_name, reason |

### Account Events

| Event Name | Description | Properties |
|------------|-------------|------------|
| account_created | New account | source, plan |
| account_upgraded | Plan upgrade | from_plan, to_plan |
| account_churned | Account closed | reason, tenure, mrr_lost |
| account_reactivated | Returned customer | previous_tenure, new_plan |

---

## Event Properties (Parameters)

Mark every property in the tracking plan as **required** or **optional**. A required property is one the event is useless without (`value` and `currency` on a purchase, `step_name` on an onboarding step); QA fails an event that arrives without it. Optional properties add context and can be added later without breaking reports.

### Standard Properties to Include

**User Context:**
```
user_id: "12345"
user_type: "free" | "trial" | "paid"
account_id: "acct_123"
plan_type: "starter" | "pro" | "enterprise"
```

**Session Context:**
```
session_id: "sess_abc"
session_number: 5
page: "/pricing"
referrer: "https://google.com"
```

**Campaign Context:**
```
source: "google"
medium: "cpc"
campaign: "spring-sale"
content: "hero-cta"
```

**Product Context (E-commerce):**
```
product_id: "SKU123"
product_name: "Product Name"
category: "Category"
price: 99.99
quantity: 1
currency: "USD"
```

**Timing:**
```
timestamp: "2024-01-15T10:30:00Z"
time_on_page: 45
session_duration: 300
```

---

## Funnel Event Sequences

### Signup Funnel
1. signup_started
2. signup_step_completed (email)
3. signup_step_completed (password)
4. signup_completed
5. onboarding_started

### Purchase Funnel
1. pricing_viewed
2. plan_selected
3. checkout_started
4. payment_info_entered
5. purchase_completed

### E-commerce Funnel
1. product_viewed
2. product_added_to_cart
3. cart_viewed
4. checkout_started
5. shipping_info_entered
6. payment_info_entered
7. purchase_completed

---

## Tracking Plan Governance

Keep one tracking plan (a sheet or a table) as the single source of truth. Beyond the columns in SKILL.md, add:

| Column | Values |
|--------|--------|
| Implemented in | GTM / app code / server |
| Status | Draft / Implemented / Verified |
| Owner | The team that answers when the event breaks |

**Change protocol:**
1. **New event:** add it to the plan and get sign-off before anyone implements it.
2. **Renamed event:** send the old and the new name side by side for a deprecation period (30 days is a common default), then remove the old one. Reports that use the old name break on the day it stops.
3. **Removed event:** mark it archived in the plan; keep the row so historical data still has a definition.
4. **New property:** non-breaking. Implement it and update the plan.
5. **Removed property:** treat it as a rename, with a deprecation period.

**Schema versions:** when the taxonomy changes fast, add a `schema_version` property to critical events (`checkout_completed`, `signup_completed`). Reports can then filter old and new shapes apart during a migration.
