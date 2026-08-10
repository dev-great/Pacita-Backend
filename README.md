# Pacita Tianna — Site Backend (Django Admin + REST API)

The complete backend for **www.pacitatiana.com**: a Django admin where Pacita can
edit **every text on every page**, manage shop products & the B.O.S.S. Faith Moves
shirts, re-order the gallery, watch orders come in — plus Square checkout,
the Lulu Print API for paperback fulfillment, and EmailJS order notifications.

---

## 1 · Quick start

```bash
cd pacita_backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env        # fill in keys as they become available (works empty for local dev)

python manage.py migrate
python manage.py seed_site  # loads ALL the approved site content (241 rows)
python manage.py createsuperuser   # Pacita's admin login
python manage.py runserver
```

- Admin: **http://127.0.0.1:8000/admin/**
- API root examples: `/api/content/home/`, `/api/products/`, `/api/gallery/`

Re-running `seed_site` never destroys Pacita's admin edits. To reset everything
back to the approved content: `python manage.py seed_site --overwrite`.

## 2 · What Pacita can manage in the admin

| Admin section | What it controls |
|---|---|
| **Site texts** | Every headline, paragraph, label & button on all 8 pages, addressed by page → section → key (a "note" column says where each text appears). |
| **Coaching steps** | The 7 Steps — titles, scriptural anchors, mindset shifts. |
| **Products** | Shop cards: title, copy, price (cents), cover URL, coming-soon flag, Lulu link, private eBook file URL. Add new products any time. |
| **Shirts** | The 9 B.O.S.S. colorways: color name, swatch, Cloudinary image, price, on/off. |
| **Gallery items** | Every photo/video as a Cloudinary link. The `order` column IS her approved arrangement — she can re-order with list editing. |
| **Community events / Partners** | Brush & Bond, Vision Board Arts + the "In partnership with" strip. |
| **Social links / Site settings** | Address, phone, email, Instagram/Facebook/TikTok. |
| **Orders** | Every checkout with customer, items, shipping address, status. |
| **Lulu print jobs** | Print/ship status per order, tracking URLs. |
| **Inbox** | Contact form messages, Bookish Club members, newsletter subscribers. |

## 3 · Public API (what the React site calls)

| Endpoint | Returns |
|---|---|
| `GET /api/content/<page>/` | `{section: {key: text}}` — pages: `home, author, shop, coaching, community, gallery, bookclub, contact, global` |
| `GET /api/steps/` | The 7 Steps `[{n, title, anchor, anchorRef, copy}]` |
| `GET /api/products/` | Shop cards (id, title, priceCents, cover, luluHref, …) |
| `GET /api/shirts/` | Shirt colorways (id, color, swatch, src, priceCents, sizes) |
| `GET /api/gallery/` | All items in Pacita's approved order |
| `GET /api/community/` | Events + partner strip |
| `GET /api/globals/` | Contact settings + social links (nav/footer) |
| `POST /api/checkout/` | `{items:[{id, qty}], customer:{name,email,phone}}` → `{checkoutUrl}` (Square-hosted) |
| `POST /api/contact/` | Stores a Let's Talk submission |
| `POST /api/club/join/` | Bookish Club sign-up |
| `POST /api/subscribe/` | Join the Journey newsletter |
| `POST /api/webhooks/square/` | Square payment webhook (signature-verified) |
| `POST /api/webhooks/lulu/` | Lulu print-job status webhook |

**Multi-value texts** use `|` separators (e.g. `home/hero/roles = "Author|Advisor|Activist"`,
stats as `"20+|Years in youth development"`) — split on `|` in the frontend.

### Frontend wiring example

```ts
const API = import.meta.env.VITE_API_URL; // e.g. https://api.pacitatiana.com

const content = await fetch(`${API}/api/content/home/`).then(r => r.json());
// content.hero.statement, content.triple_threat.pillar_1_title, ...

// checkout replaces the old /api/create-checkout serverless function:
const res = await fetch(`${API}/api/checkout/`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ items: cart.map(i => ({ id: i.id, qty: i.qty })), customer }),
});
const { checkoutUrl } = await res.json();
window.location.href = checkoutUrl;
```

Footer link to the dashboard (per Pacita's request):

```tsx
<a href="https://api.pacitatiana.com/admin/" target="_blank" rel="noopener noreferrer">Site Admin</a>
```

## 4 · Payments & fulfillment flow

1. **Cart → `POST /api/checkout/`** — prices come from the DB (never the client).
   Shirt ids arrive as `shirt-3--XL`; the size suffix is stripped for pricing and
   kept in the line-item title. Physical items (paperback kind or shirts) make
   Square ask for a shipping address.
2. **Customer pays on the Square-hosted page.**
3. **Square webhook (`payment.updated` → COMPLETED)** — signature verified,
   order marked paid, shipping address pulled from the Square order,
   **EmailJS email sent to Pacita** with name / email / phone / address / items.
4. **Lulu (optional automation)** — with `LULU_AUTO_PRINT=True`, a paid order
   containing the paperback automatically creates a Lulu Print-Job (interior +
   cover file URLs, pod package id, customer address). Status changes stream
   back through the Lulu webhook and show in the admin; SHIPPED marks the order
   fulfilled. Start in **sandbox** (`LULU_USE_SANDBOX=True`).

> Note: Lulu never charges the buyer — Square takes the payment; Lulu bills the
> Lulu account (card on file) for print + shipping when the job goes to production.

Register the Lulu webhook once (Django shell):

```python
from lulu_api.services import register_webhook
register_webhook("https://api.pacitatiana.com/api/webhooks/lulu/")
```

## 5 · EmailJS template (`new_order`)

Create a template with variables:
`{{order_id}} {{customer_name}} {{customer_email}} {{customer_phone}} {{shipping_address}} {{items}} {{total}}`
→ To email: `hello@pacitatiana.com`. Enable **"Allow EmailJS API for non-browser
applications"** and set `EMAILJS_PRIVATE_KEY`.

## 6 · Deployment notes

- Any Python host works (Railway, Render, Fly.io, a VPS): `gunicorn config.wsgi`.
- SQLite is fine to start; swap the `DATABASES` block for Postgres when needed.
- Static files are served by WhiteNoise — run `python manage.py collectstatic`.
- Set `DJANGO_DEBUG=False`, a real `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`,
  `CORS_ALLOWED_ORIGINS=https://www.pacitatiana.com`, and the Square webhook URL
  must exactly match `SQUARE_WEBHOOK_NOTIFICATION_URL`.

## 7 · TODOs already marked in the seed

- Real Lulu product URL for the paperback card (`Product.lulu_url`).
- Real shirt price (`Shirt.price_cents`, seeded at $25.00).
- Facebook / TikTok handles (Social links).
- Product cover URLs (`Product.cover_url`) — currently the frontend uses local
  asset imports; paste Cloudinary URLs to switch to CMS-driven covers.
- `LULU_POD_PACKAGE_ID` — confirm in Lulu's price calculator for the 6×9 book.
