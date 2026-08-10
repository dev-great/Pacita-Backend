# flake8: noqa
"""
All initial site content, extracted verbatim from the approved React pages.
The seed_site command loads it. Safe to re-run: existing rows are updated,
Pacita's later admin edits win unless you pass --overwrite.
"""

CLD = "https://res.cloudinary.com/video-system-great-devxy"
IMG = f"{CLD}/image/upload/f_auto,q_auto,w_900"
VID = f"{CLD}/video/upload/q_auto"

# ═══════════════════════ SITE TEXTS ═══════════════════════
# (page, section, key, text, note)
SITE_TEXTS = [
    # ── GLOBAL: footer / nav ──
    ("global", "brand", "name", "Pacita Tiana", "Hero + footer watermark wordmark"),
    ("global", "brand", "slogan", "Faith Moves Matter™", "Hero slogan (shown in [ brackets ])"),
    ("global", "footer", "tagline", "Author of _The Appointed Time_. Advisor to parents. Activist for youth. Building on Spiritual Success — because _Every Step Matters_.", "Footer paragraph under the logo"),
    ("global", "footer", "copyright", "© {year} Pacita Tiana · www.PacitaTiana.com. All rights reserved.", "Legal bar ({year} is filled automatically)"),
    ("global", "footer", "credit", "Crafted by MacGroup Technology", "Legal bar right side"),
    ("global", "footer", "admin_link_label", "Site Admin", "The footer link to this dashboard"),

    # ── HOME: hero ──
    ("home", "hero", "roles", "Author|Advisor|Activist", "Bracket roles — separate with |"),
    ("home", "hero", "statement", "Roadmap literature for ==displacement==, to belonging, and finding home.", "Right-rail statement"),
    ("home", "hero", "cta", "Explore My Books", "Hero button"),
    ("home", "hero", "upcoming_label", "Upcoming Book", "Bottom-left small label"),
    ("home", "hero", "upcoming", "Brown Study — Fall 2026", "Bottom-left release line"),
    ("home", "hero", "credentials", "Advisor|Speaker|Published Author", "Bottom-right stack — separate with |"),

    # ── HOME: triple threat ──
    ("home", "triple_threat", "label", "[ The Triple Threat ]", ""),
    ("home", "triple_threat", "heading_1", "One Woman.", "Solid line"),
    ("home", "triple_threat", "heading_2", "Three Callings.", "Outlined line"),
    ("home", "triple_threat", "side_note", "Authorpreneur. Speaker. Catalyst for ==Building on Spiritual Success==", "Right-side note (last words highlighted)"),
    ("home", "triple_threat", "pillar_1_role", "Author", ""),
    ("home", "triple_threat", "pillar_1_title", "The Appointed Time", ""),
    ("home", "triple_threat", "pillar_1_copy", "A roadmap to build on spiritual success, shaped by personal displacement and discovery. Vulnerable, lived realities — written to foster self-efficacy and connection.", ""),
    ("home", "triple_threat", "pillar_1_link", "Meet the Author", ""),
    ("home", "triple_threat", "pillar_2_role", "Advisor", ""),
    ("home", "triple_threat", "pillar_2_title", "Parent Support", ""),
    ("home", "triple_threat", "pillar_2_copy", "A supportive partner for parents of teens — building specific skills, managing behavioral challenges, and improving your overall family dynamic.", ""),
    ("home", "triple_threat", "pillar_2_link", "Start the 7 Steps", ""),
    ("home", "triple_threat", "pillar_3_role", "Activist", ""),
    ("home", "triple_threat", "pillar_3_title", "Poet-Activists", ""),
    ("home", "triple_threat", "pillar_3_copy", "An activist voice using verse to challenge power, spark empathy, and document injustice — merging art with social change.", ""),
    ("home", "triple_threat", "pillar_3_link", "Discover Brown Study", ""),

    # ── HOME: featured book ──
    ("home", "featured_book", "label", "[ The Book ]", ""),
    ("home", "featured_book", "heading_1", "The Appointed", ""),
    ("home", "featured_book", "heading_2", "Time", "Outlined"),
    ("home", "featured_book", "subtitle", "A Journey Towards Building Spiritual Success", ""),
    ("home", "featured_book", "paragraph", "A roadmap to build on spiritual success — shaped by personal displacement and discovery. Part memoir, part guide, it walks the terrain of belonging, faith, and becoming — printed on demand and shipped to your door. ==Buy Direct and your purchase helps build the Authors Marketplace.==", "APPROVED wording — do not paraphrase the last sentence"),
    ("home", "featured_book", "cta_primary", "Buy Direct", ""),
    ("home", "featured_book", "cta_secondary", "About the Book", ""),
    ("home", "featured_book", "badge", "+ Free Workbook", "Corner sticker — only shows while a free workbook exists"),
    ("home", "featured_book", "workbook_label", "[ The Workbook ]", ""),
    ("home", "featured_book", "workbook_title", "The Mindset Manual", ""),
    ("home", "featured_book", "workbook_format", "Client Questionnaire · PDF", ""),
    ("home", "featured_book", "workbook_copy", "**Free** — no cart, no checkout. Click and it downloads right now.", ""),
    ("home", "featured_book", "workbook_cta", "Download", "Workbook button"),

    # ── HOME: activism ──
    ("home", "activism", "label", "[ The Activist ]", ""),
    ("home", "activism", "heading_1", "Every Step", ""),
    ("home", "activism", "heading_2", "Matters.", "Outlined"),
    ("home", "activism", "side_note", "Youth advocacy in action — a safe, judgment-free space where teens are ==redirected, not written off==", ""),
    ("home", "activism", "video_badge", "As seen on FOX 5 KVVU-TV", ""),
    ("home", "activism", "video_caption", "“Summit shares gun violence stories to steer Clark County teens away from guns”", ""),
    ("home", "activism", "fox5_url", "https://www.fox5vegas.com/2026/06/06/clark-county-youth-summit-addresses-gun-violence-through-survivor-stories/", "Fox 5 article link"),
    ("home", "activism", "video_url", f"{VID}/v1784902275/video_wzwdr5.mp4", "Summit video (Cloudinary)"),
    ("home", "activism", "paragraph_1", "As a Recreation/Cultural Specialist with the **Gap Intervention Team (G.I.T.)** of Clark County Parks & Recreation, Pacita serves teens ages 13–18 who are court-ordered to community service — using prosocial activities to redirect energy from criminal activity to recreation, connection, and purpose.", ""),
    ("home", "activism", "paragraph_2", "Her passion sparked the **1st Annual Level Up Teen Summit**, and as Program Director of **Footprints** — the Youth Division of Recovery Girls Rock — she helps teens navigate societal issues while leaving room for them to lead the cause with confidence.", ""),
    ("home", "activism", "cta_primary", "See the Work", ""),
    ("home", "activism", "cta_secondary", "Partner With Pacita", ""),
    ("home", "activism", "stat_1", "20+|Years in youth development", "value|label"),
    ("home", "activism", "stat_2", "13–18|Ages served through G.I.T.", "value|label"),
    ("home", "activism", "stat_3", "1st|Annual Level Up Teen Summit", "value|label"),

    # ── HOME: bookish club teaser ──
    ("home", "bookish_teaser", "label", "[ Brown Study Bookish Club™ ]", ""),
    ("home", "bookish_teaser", "heading_1", "What We’re", ""),
    ("home", "bookish_teaser", "heading_2", "Reading.", "Outlined"),
    ("home", "bookish_teaser", "side_note", "Book Finds — hand-picked reads & honest reviews for 2026–2027. Because ==what we read shapes what we build==", ""),
    ("home", "bookish_teaser", "instagram_cta", "@iampacitatiana — see the reads & reviews", ""),
    ("home", "bookish_teaser", "footnote", "Four seasons of curated Book Finds — revealed and reviewed on Instagram, discussed in the club.", ""),
    ("home", "bookish_teaser", "brown_study_badge", "Coming Fall 2026", ""),
    ("home", "bookish_teaser", "brown_study_subtitle", "100-Poem Commentary + Journal Prompts · e-Book", ""),
    ("home", "bookish_teaser", "brown_study_copy", "An invitation to sit with the words, then write your own. The next chapter of Building on Spiritual Success — released first to club members.", ""),

    # ── HOME: join the journey ──
    ("home", "join", "label", "[ Join the Journey ]", ""),
    ("home", "join", "heading_1", "Every Step,", ""),
    ("home", "join", "heading_2", "Delivered.", "Outlined"),
    ("home", "join", "pitch", "Book releases, Book Finds, event invites, and first word on _Brown Study_ — straight from Pacita's desk. No spam, ever.", ""),
    ("home", "join", "disclaimer", "We respect your inbox. Unsubscribe anytime. Your details are never shared.", ""),

    # ── AUTHOR ──
    ("author", "hero", "label", "[ The Author ]", ""),
    ("author", "hero", "heading_1", "A Quiet Life,", ""),
    ("author", "hero", "heading_2", "A Loud Calling.", "Outlined"),
    ("author", "hero", "bio_1", "Pacita Tianna lives a quiet life of motherhood, raising two teen sons. Her intrinsic motivation is ==curating==. She is an entrepreneur, speaker, and published author of _The Appointed Time_ — a catalyst who permeates Building on Spiritual Success.", ""),
    ("author", "hero", "bio_2", "Her charismatic personality finds happiness within inner-engineering personal development and helping others improve their lives. Her innovative, adventurous, artistic style has allowed for a life that fulfills her mind, body, and spirit.", ""),
    ("author", "hero", "cta_primary", "Get the Book", ""),
    ("author", "hero", "cta_secondary", "Book Pacita to Speak", ""),
    ("author", "hero", "badge", "Author · Advisor · Activist", "Sticker on the portrait"),
    ("author", "milestones", "m1", "20+|Years as a Youth Development Professional", "value|label"),
    ("author", "milestones", "m2", "6|Years in leadership — former Club Director, Southern Nevada Boys & Girls Club", "value|label"),
    ("author", "milestones", "m3", "4|Years with Clark County Parks & Recreation G.I.T. unit", "value|label"),
    ("author", "milestones", "m4", "1|Published book — with Brown Study arriving Fall 2026", "value|label"),
    ("author", "pov", "label", "[ Point of View ]", ""),
    ("author", "pov", "quote_1", "“My writing is a direct reflection of my journey through emotional displacement and a sense of belonging. I write from the perspective of an observer of self, looking in — utilizing my own experiences.”", ""),
    ("author", "pov", "quote_2", "“I don’t just want to tell a story. I want to ==build a bridge into the fragile human psyche==, while exposing the universal anxieties of finding ‘home.’ I aim to share vulnerable, lived realities to foster empathy and connection.”", ""),
    ("author", "pov", "quote_3", "“So what can you expect during an encounter with me, ‘The Triple Threat’? A meeting with an author, an advisor, and an activist.”", ""),
    ("author", "pov", "attribution", "— Pacita Tianna", ""),
    ("author", "pov", "video_chip", "POV · In Her Own Words", ""),
    ("author", "pov", "video_url", f"{VID}/v1785942092/WhatsApp_Video_2026-07-29_at_19.22.45_1_hbrbsx.mp4", "Portrait POV video (Cloudinary)"),
    ("author", "book_strip", "label", "[ The Book ]", ""),
    ("author", "book_strip", "heading_1", "The Appointed", ""),
    ("author", "book_strip", "heading_2", "Time", "Outlined"),
    ("author", "book_strip", "subtitle", "A Journey Towards Building Spiritual Success", ""),
    ("author", "book_strip", "paragraph", "A roadmap to build on spiritual success, determined by personal displacement and discovery. Part memoir, part guide — walking the terrain of belonging, faith, and becoming, honestly and without pretense. Buy direct from this site and every purchase includes the _7 Faith Moves™_ ebook.", "APPROVED wording"),
    ("author", "book_strip", "cta", "Buy Direct", ""),
    ("author", "brown_study", "badge", "Coming Fall 2026", ""),
    ("author", "brown_study", "heading_1", "Brown Study", ""),
    ("author", "brown_study", "heading_2", "· e-Book", "Outlined"),
    ("author", "brown_study", "copy", "A 100-poem commentary paired with journal prompts — an invitation to sit with the words, then write your own. Released first to Brown Study Bookish Club™ members.", ""),
    ("author", "brown_study", "cta", "Join the Club", ""),

    # ── SHOP ──
    ("shop", "hero", "label", "[ The Shop ]", ""),
    ("shop", "hero", "heading_1", "Buy Direct.", ""),
    ("shop", "hero", "heading_2", "Support the Author.", "Outlined"),
    ("shop", "hero", "paragraph", "Order the hardcover with free US shipping, or download the eBooks instantly. ==Buy Direct and your purchase helps build the Authors Marketplace.==", "APPROVED closing sentence"),
    ("shop", "merch", "label", "[ The Merch ]", ""),
    ("shop", "merch", "heading_1", "B.O.S.S.", ""),
    ("shop", "merch", "heading_2", "Faith Moves", "Outlined"),
    ("shop", "merch", "side_note", "The message through ==Gear & Glamour== — Building On Spiritual Success, worn out loud. Nine colorways — pick your color, pick your size.", ""),
    ("shop", "lulu", "label", "[ In Print ]", ""),
    ("shop", "lulu", "link_label", "Lulu.com — Pacita Tianna's Bookstore", ""),
    ("shop", "lulu", "footnote", "Every hardcover is printed on demand and shipped to you free within the US. Buy Direct and your purchase helps build the Authors Marketplace.", ""),

    # ── COACHING ──
    ("coaching", "hero", "label", "[ The Coaching Program ]", ""),
    ("coaching", "hero", "heading_1", "Seven Steps.", ""),
    ("coaching", "hero", "heading_2", "One Transformation.", "Outlined"),
    ("coaching", "hero", "paragraph", "A guided coaching experience to ==Build on Spiritual Success== — beginning with one honest look inward. Your first step is the Mindset Manual below: listen to Pacita’s introduction, download the client questionnaire, and bring it to your first conversation.", ""),
    ("coaching", "mindset", "label", "[ Start Here ]", ""),
    ("coaching", "mindset", "heading_1", "The Mindset", ""),
    ("coaching", "mindset", "heading_2", "Manual", "Outlined"),
    ("coaching", "mindset", "accessibility_note", "Listen, read, or both — the audio and the questionnaire carry the same guidance, so you can take the journey your way.", ""),
    ("coaching", "mindset", "listen_title", "Listen First", ""),
    ("coaching", "mindset", "listen_sub", "A personal introduction from Pacita", ""),
    ("coaching", "mindset", "listen_copy", "Before you open the client questionnaire, let Pacita walk you into it — what the Mindset Manual, client questionnaire is, why it begins the 7 Steps, and how to show up honestly.", "APPROVED wording"),
    ("coaching", "mindset", "audio_url", f"{VID}/v1785973793/The_Mindset_Client_Questionaire_yyz0yf.mp3", "Intro audio (Cloudinary mp3)"),
    ("coaching", "mindset", "download_title", "Then Take It With You", ""),
    ("coaching", "mindset", "download_sub", "MM Client Questionnaire · PDF", ""),
    ("coaching", "mindset", "download_copy", "Seven mindsets, scripture anchors, reflection prompts, prayer journals, and your seven declarations — printable, or fill it in digitally. Keep it; it’s yours.", ""),
    ("coaching", "mindset", "download_cta", "Download the Client Questionnaire (Free)", ""),
    ("coaching", "mindset", "download_footnote", "Accessible PDF — real text, tagged headings, screen-reader friendly.", ""),
    ("coaching", "steps", "label", "[ The Journey ]", ""),
    ("coaching", "steps", "heading_1", "The Seven", ""),
    ("coaching", "steps", "heading_2", "Steps", "Outlined"),
    ("coaching", "cta", "heading_1", "Ready For", ""),
    ("coaching", "cta", "heading_2", "Step One?", "Outlined"),
    ("coaching", "cta", "paragraph", "Complete the MM Client Questionnaire, then bring it to a discovery conversation with Pacita — no pressure, no performance. Only honesty.", "APPROVED wording"),
    ("coaching", "cta", "button", "Book a Discovery Conversation", ""),

    # ── COMMUNITY ──
    ("community", "hero", "label", "[ Community ]", ""),
    ("community", "hero", "heading_1", "Stronger", ""),
    ("community", "hero", "heading_2", "Together.", "Outlined"),
    ("community", "hero", "paragraph", "Collaboration is Pacita’s love language. From court-ordered community service redirected into ==prosocial purpose==, to paint parties and vision boards — this is the work, and the people who make it possible.", ""),
    ("community", "advocacy", "label", "[ Youth Advocacy ]", ""),
    ("community", "advocacy", "heading_1", "From Court Order", ""),
    ("community", "advocacy", "heading_2", "To Community", "Outlined"),
    ("community", "advocacy", "video_badge", "As seen on FOX 5 KVVU-TV", ""),
    ("community", "advocacy", "video_caption", "“Summit shares gun violence stories to steer Clark County teens away from guns”", ""),
    ("community", "advocacy", "fox5_url", "https://www.fox5vegas.com/2026/06/06/clark-county-youth-summit-addresses-gun-violence-through-survivor-stories/", "Fox 5 article link"),
    ("community", "advocacy", "video_url", f"{VID}/v1784902275/video_wzwdr5.mp4", "Summit video (Cloudinary)"),
    ("community", "collab", "label", "[ Community Collaborations ]", ""),
    ("community", "collab", "heading_1", "Made With", ""),
    ("community", "collab", "heading_2", "Partners", "Outlined"),
    ("community", "partners", "label", "In partnership with", "Partner strip heading"),
    ("community", "advocacy", "paragraph_1", "Through the **Gap Intervention Team (G.I.T.)** of Clark County Parks & Recreation, Pacita serves teens ages 13–18 who are court-ordered to community service — prosocial activities as the catalyst that redirects energy from criminal activity to recreation, connection, and purpose.", ""),
    ("community", "advocacy", "paragraph_2", "That passion sparked the **1st Annual Level Up Teen Summit** — collaborations, partnerships, and resources brought together to take teens beyond their day-to-day encounters. And as Program Director of **Footprints**, the Youth Division of Recovery Girls Rock, she helps teens navigate societal issues while leaving room for them to lead the cause with confidence.", ""),
    ("community", "advocacy", "quote", "“Every Step Matters.”", ""),
    ("community", "cta", "heading_1", "Bring Pacita", ""),
    ("community", "cta", "heading_2", "To Your Community", "Outlined"),
    ("community", "cta", "paragraph", "Youth programming, speaking engagements, workshops, and event partnerships — if it lifts young people, she’s listening.", ""),
    ("community", "cta", "button", "Let’s Partner", ""),

    # ── GALLERY ──
    ("gallery", "hero", "label", "[ PT’s Gallery ]", ""),
    ("gallery", "hero", "heading_1", "Curated,", ""),
    ("gallery", "hero", "heading_2", "Not Collected.", "Outlined"),
    ("gallery", "hero", "paragraph", "Art, healing, community, and the moments in between — a life that fulfills ==mind, body, and spirit==, in pictures and motion.", ""),
    ("gallery", "boss", "badge", "New Project · 2026", ""),
    ("gallery", "boss", "heading_1", "B.O.S.S.", ""),
    ("gallery", "boss", "heading_2", "Faith Moves", "Outlined"),
    ("gallery", "boss", "subtitle", "The Message Through Gear & Glamour", ""),
    ("gallery", "boss", "cta_primary", "Get Notified First", ""),
    ("gallery", "boss", "cta_secondary", "Visit the Shop", ""),
    ("gallery", "boss", "copy", "Building On Spiritual Success — worn out loud. Releasing 2026 as a **digital e-book download**; a print edition follows if the response calls for it. Club members hear first.", ""),

    # ── BOOK CLUB ──
    ("bookclub", "hero", "label", "[ Brown Study Bookish Club™ ]", ""),
    ("bookclub", "hero", "heading_1", "Read With", ""),
    ("bookclub", "hero", "heading_2", "Purpose.", "Outlined"),
    ("bookclub", "hero", "paragraph", "Curation is Pacita’s intrinsic motivation — and this club is curation at its purest. Hand-picked ==Book Finds==, honest reviews, and a community that believes what we read shapes what we build.", ""),
    ("bookclub", "hero", "cta", "Join the Club — Free", ""),
    ("bookclub", "how", "step_1", "Join Free|Sign up below — no fees, no homework, no pressure.", "title|copy"),
    ("bookclub", "how", "step_2", "Get the Book Finds|Seasonal curated picks with Pacita's honest reviews, straight to your inbox.", "title|copy"),
    ("bookclub", "how", "step_3", "Read & Reflect|Read along, journal along, and join the conversation.", "title|copy"),
    ("bookclub", "how", "step_4", "First Access|Members get Brown Study and every new release before anyone else.", "title|copy"),
    ("bookclub", "how", "label", "[ How It Works ]", ""),
    ("bookclub", "reading_list", "label", "[ Book Finds ]", ""),
    ("bookclub", "reading_list", "heading_1", "2026–2027", ""),
    ("bookclub", "reading_list", "heading_2", "Reads & Reviews", "Outlined"),
    ("bookclub", "reading_list", "note", "Four seasons of curated picks — titles announced to members first, reviews published as we read.", ""),
    ("bookclub", "reading_list", "row_1", "Fall 2026|Reveal coming — members see it first", "season|status — put the real title in the status once revealed"),
    ("bookclub", "reading_list", "row_2", "Winter 2026|Reveal coming — members see it first", "season|status"),
    ("bookclub", "reading_list", "row_3", "Spring 2027|Reveal coming — members see it first", "season|status"),
    ("bookclub", "reading_list", "row_4", "Summer 2027|Reveal coming — members see it first", "season|status"),
    ("bookclub", "spotlight", "badge", "Members Read It First · Fall 2026", ""),
    ("bookclub", "spotlight", "heading_1", "Brown", ""),
    ("bookclub", "spotlight", "heading_2", "Study", "Outlined"),
    ("bookclub", "spotlight", "subtitle", "100-Poem Commentary + Journal Prompts · e-Book", ""),
    ("bookclub", "spotlight", "copy", "The club’s namesake — an invitation to sit with the words, then write your own. Club members get it before anyone else, along with the journal-along discussion series.", ""),
    ("bookclub", "join", "label", "[ Join the Club ]", ""),
    ("bookclub", "join", "heading_1", "Your Seat Is", ""),
    ("bookclub", "join", "heading_2", "Waiting.", "Outlined"),
    ("bookclub", "join", "pitch", "Free to join. Seasonal Book Finds, honest reviews, event invites, and first access to _Brown Study_ — no spam, unsubscribe anytime.", ""),
    ("bookclub", "join", "button", "Join the Club — Free", ""),
    ("bookclub", "join", "disclaimer", "We respect your inbox. Unsubscribe anytime. Your details are never shared.", ""),

    # ── CONTACT ──
    ("contact", "hero", "label", "[ Let’s Talk! ]", ""),
    ("contact", "hero", "heading_1", "Start The", ""),
    ("contact", "hero", "heading_2", "Conversation.", "Outlined"),
    ("contact", "hero", "paragraph", "Speaking engagements · parent support · youth programming · collaborations · media. If it lifts people, ==Pacita is listening==.", ""),
    ("contact", "form", "label", "[ Send a Message ]", ""),
    ("contact", "form", "inquiry_types", "Speaking engagement|Parent support / advising|Youth programming / G.I.T.|Community collaboration|Media inquiry|Something else", "Dropdown options — separate with |"),
    ("contact", "form", "button", "Send Message", ""),
    ("contact", "form", "footnote", "Messages go straight to Pacita’s inbox. Your details are never shared.", ""),
    ("contact", "form", "success_note", "Pacita reads every message personally — expect a reply at your email soon.", ""),
    ("contact", "business", "label", "[ Business & Bookings ]", ""),
    ("contact", "business", "follow_label", "Follow:", ""),
    ("contact", "ccpr", "label", "[ Clark County Parks & Recreation ]", ""),
    ("contact", "ccpr", "person", "Pacita Coleman — Recreation/Cultural Specialist II", ""),
    ("contact", "ccpr", "email", "pacita.coleman@clarkcountynv.gov", ""),
    ("contact", "ccpr", "site_label", "ClarkCountyNV.gov", ""),
    ("contact", "ccpr", "site_url", "https://www.clarkcountynv.gov/", ""),
    ("contact", "map", "label", "[ Find Us ]", ""),
    ("contact", "map", "heading_1", "Las Vegas,", ""),
    ("contact", "map", "heading_2", "Nevada", "Outlined"),
    ("contact", "map", "open_label", "Open in Google Maps", ""),
]

# ═══════════════════════ SETTINGS & SOCIALS ═══════════════════════
SITE_SETTINGS = [
    ("address", "1625 W. Carey Ave., Las Vegas, NV 89032", "Shown in footer + Let's Talk map"),
    ("phone", "(702) 455-7177", ""),
    ("email", "hello@pacitatiana.com", ""),
    ("instagram_handle", "@iampacitatiana", ""),
    # The free workbook — one URL, used by the home page card AND the Coaching
    # page download. Clear this field to hide the workbook card everywhere.
    ("workbook_pdf_url", "https://res.cloudinary.com/gdeq8vzw/image/upload/v1786392698/the_mindset_manual_client_questionnaire.pdf",
     "The Mindset Manual client questionnaire (free download)"),
    ("workbook_cover_url", "", "Optional cover image for the workbook card — falls back to the built-in artwork"),
]

SOCIAL_LINKS = [
    ("Instagram", "https://www.instagram.com/iampacitatiana/"),
    ("Facebook", "https://www.facebook.com/"),   # TODO real handle
    ("TikTok", "https://www.tiktok.com/"),       # TODO real handle
    ("Email", "mailto:hello@pacitatiana.com"),
]

# ═══════════════════════ COACHING — THE 7 STEPS (APPROVED) ═══════════════════════
COACHING_STEPS = [
    (1, "Choose To Expand",
     "“Anyone who belongs to Christ is a new person. The past is forgotten and everything is new.”", "— 2 Corinthians 5:17 (CEV)",
     "We cannot build a new future while holding onto the emotional lease of our past. To expand means giving ourselves permission to outgrow old versions of who we were told to be."),
    (2, "Don’t Control—Create",
     "“Create in me a clean heart, O God, and put a new and right spirit within me.”", "— Psalm 51:10 (NRSV)",
     "Control is born of anxiety and fear; creation is born of faith and imagination. When we stop trying to micromanage external outcomes, we clear the space for God to co-create something far better within us."),
    (3, "Resist Force—Flow",
     "“My gift of undeserved grace is all you need. My power is strongest when you are weak.”", "— 2 Corinthians 12:9 (CEV)",
     "Society teaches us to hustle, grind, and force. Spiritual success teaches us to flow. Flow isn’t laziness; it is relying on divine grace to carry the heavy load. When we hit a wall, we don't push harder—we surrender smarter"),
    (4, "Take Aligned Action",
     "“Let your eyes look straight ahead; fix your gaze directly before you. Give careful thought to the paths for your feet and be steadfast in all your ways.”", "— Proverbs 4:25-26 (NIV)",
     "Inspiration without action is just a daydream. Aligned action means ignoring the distractions to the left and right, laser-focusing on your specific calling, and taking deliberate, grounded steps forward"),
    (5, "Your Process is Potent",
     "“I have not yet reached my goal, and I am not perfect. But Christ has taken hold of me. So I keep on running and struggling to take hold of the prize.”", "— Philippians 3:12 (CEV)",
     "Perfection is a myth; progression is the miracle. The struggle isn't a sign that you are failing; it is proof that you are actively being refined. Your process is where your authority, your testimony, and your strength are built."),
    (6, "Get Insight",
     "“Trust in the LORD with all your heart; do not depend on your own understanding. Seek his will in all you do, and he will show you which path to take.”", "— Proverbs 3:5-6 (NLT)",
     "Our logical minds love to overanalyze, look for guarantees, and predict every outcome. But true spiritual insight requires us to temporarily quiet our intellectual “need to know” so we can hear a higher whisper. Insight is less about having all the answers and more about trusting the next right step"),
    (7, "Lessons Never Lessen",
     "“For I am about to do something new. See, I have already begun! Do you not see it? I will make a pathway through the wilderness. I will create rivers.”", "— Isaiah 43:19 (NLT)",
     "Nothing you have walked through is a waste. The wilderness seasons, the detours, and the flat-out mistakes did not lessen your value or your calling—they were actually laying the foundation for your “something new.” Your scars are your stripes of authority."),
]

# ═══════════════════════ COMMUNITY ═══════════════════════
COMMUNITY_EVENTS = [
    ("01", "Brush & Bond Paint Party", "Hosted by Footprints — Youth Division of Recovery Girls Rock",
     "Canvas, color, and conversation — creativity as a bonding experience for youth and community. Every stroke opens a door to talk about the things that matter.",
     [{"name": "Caroline App", "role": "Artist · Facilitator & Partner"}]),
    ("02", "Vision Board Arts", "A hands-on visioning experience",
     "See it, say it, build it — participants map their goals in pictures and words, leaving with a board they made and a plan they believe.",
     [{"name": "Ylonda Dickerson", "role": "Valley View Community Cares · CEO"}]),
]

PARTNERS = [
    ("Recovery Girls Rock", "Helen Williams · CEO"),
    ("Clark County Parks & Recreation", ""),
    ("Valley View Community Cares", "Ylonda Dickerson · CEO"),
    ("Words Are Rich Foundation", "Oli Porter · CEO"),
    ("Caroline App", "Independent Artist"),
]

# ═══════════════════════ SHOP ═══════════════════════
PRODUCTS = [
    dict(slug="book-paperback", tag="The Book · Paperback", title="The Appointed Time",
         subtitle="A Journey Towards Building Spiritual Success", kind="paperback",
         format_label="Paperback · 6×9 · printed on demand, free US shipping",
         bonus="Includes the 7 Faith Moves™ ebook, free with every copy.",
         price_cents=2999, cta="Add to Cart", accent=True, coming_soon=False,
         lulu_url="", cover_url="", order=1,
         # SKU: PB = perfect bound, UC = 60# uncoated CREAM (use 060UW444 for white).
         # Confirm at developers.lulu.com/price-calculator.
         # IMPORTANT: a paperback needs its OWN cover PDF — the hardcover case-wrap
         # cover has a different spine width and will be rejected by Lulu.
         lulu_pod_package_id="0600X0900.BW.STD.PB.060UC444.MXX",
         lulu_interior_url="", lulu_cover_url="", page_count=107),  # nested in the eBook card
    dict(slug="book-ebook", tag="The Book", title="The Appointed Time",
         subtitle="A Journey Towards Building Spiritual Success", kind="pdf",
         format_label="eBook · PDF — instant download",
         bonus="Includes the 7 Faith Moves™ ebook, free with every purchase.",
         price_cents=999, cta="Add to Cart — eBook", accent=True, coming_soon=False,
         lulu_url="",  # print sold direct now; set only if a PUBLIC Lulu listing exists
         cover_url="", order=1),
    dict(slug="faith-moves", tag="New · The 3rd Book", title="7 Faith Moves",
         subtitle="A Journey towards Building on Spiritual Success · Study & Activity Guide Workbook", kind="pdf",
         format_label="eBook only · PDF — instant download",
         bonus="Faith Moves Matter™ — the newest release in The Appointed Time series",
         price_cents=999, cta="Add to Cart — eBook", accent=False, coming_soon=False,
         lulu_url="", cover_url="", order=3),
    dict(slug="brown-study", tag="New · Poetry", title="Brown Study",
         subtitle="100-Poem Commentary · Journaling Reflections", kind="pdf",
         format_label="eBook · PDF — instant download",
         bonus="Released first to Brown Study Bookish Club™ members",
         price_cents=999, cta="Add to Cart — eBook", accent=False, coming_soon=False,
         lulu_url="", cover_url="", order=4,
         ebook_file_url="https://res.cloudinary.com/gdeq8vzw/image/upload/v1786392699/Brown_Study_100_Poems_Workbook_1.pdf"),
]

SHIRTS = [
    ("shirt-1", "Design 01", "Red", "#C8102E", f"{CLD}/image/upload/v1785974733/1785093827785_oavrk5.png"),
    ("shirt-2", "Design 02", "Purple", "#7A4BA8", f"{CLD}/image/upload/v1785974733/1785093896627_yjm1u4.png"),
    ("shirt-3", "Design 03", "Orange", "#E87722", f"{CLD}/image/upload/v1785974732/1785093683285_yrbbgt.png"),
    ("shirt-4", "Design 04", "Gold", "#D4A03C", f"{CLD}/image/upload/v1785974732/1785093816154_amq7um.png"),
    ("shirt-5", "Design 05", "Green", "#2FA84F", f"{CLD}/image/upload/v1785974732/1785093747570_ccrzgi.png"),
    ("shirt-6", "Design 06", "White", "#F5F1E8", f"{CLD}/image/upload/v1785974733/1785093429409_no3kpc.png"),
    ("shirt-7", "Design 07", "Black", "#1A1A1A", f"{CLD}/image/upload/v1785974732/1785093957525_fkclri.png"),
    ("shirt-8", "Design 08", "Sky Blue", "#7EC8E3", f"{CLD}/image/upload/v1786026488/1785698077058_xl2kz1.png"),
    ("shirt-9", "Design 09", "Royal Blue", "#1E4BB8", f"{CLD}/image/upload/v1786026488/1785698153377_bjpflr.png"),
]
SHIRT_PRICE_CENTS = 2500  # TODO: confirm with Pacita

# Products/slugs no longer sold — seed_site deletes these so switching formats
# doesn't leave an orphaned card in the shop.
# (card_slug, printed_edition_slug) — both stay real Products so checkout can
# price either one, but the printed edition renders inside the card's orange button.
PRODUCT_EDITION_LINKS = [("book-ebook", "book-paperback")]

RETIRED_PRODUCT_SLUGS = ["book-hardcover"]

# ═══════════════════════ GALLERY (Pacita's approved order) ═══════════════════════
# (media_type, src, category, title, caption)
GALLERY_ITEMS = [
    ("photo", f"{IMG}/v1784906774/Screenshot_20260626-154928_2_sm5l2a.jpg", "professional development", "With My Photographer", "The Queen behind the lens of every project."),
    ("photo", f"{IMG}/FB_IMG_1782528108594_okj9fv.jpg", "Artwork", "Original Work", "Pacita Tiana — the artist."),
    ("photo", f"{IMG}/v1785974731/1785096179150_lm3gdy.png", "Artwork", "Original Work", "Pacita Tiana — the artist."),
    ("photo", f"{IMG}/v1784906763/2925_wqxrev.jpg", "Artwork", "Original Work III", ""),
    ("photo", f"{IMG}/v1784906774/FB_IMG_1782527206871_2_we9tfx.jpg", "Artwork", "Original Work", "Pacita Tiana — the artist."),
    ("photo", f"{IMG}/v1784906764/2929_lpkn5a.jpg", "Artwork", "Original Work X", ""),
    ("photo", f"{IMG}/v1784906764/2910_wyoizy.jpg", "Artwork", "Original Work", "Pacita Tiana — the artist."),
    ("photo", f"{IMG}/v1784906765/2924_dv71gk.jpg", "Artwork", "Original Work IV", ""),
    ("photo", f"{IMG}/v1784906772/FB_IMG_1782528205824_tqn7gx.jpg", "Artwork", "Original Work V", ""),
    ("photo", f"{IMG}/v1784906774/FB_IMG_1782528030547_wmtisp.jpg", "Artwork", "Original Work VI", ""),
    ("photo", f"{IMG}/v1784906765/2930_bcmtz5.jpg", "Artwork", "Original Work VII", ""),
    ("photo", f"{IMG}/v1784906763/2926_b6hddm.jpg", "Artwork", "Original Work VIII", ""),
    ("photo", f"{IMG}/v1784906764/2927_mbxx1k.jpg", "Artwork", "Original Work IX", ""),
    ("video", None, "professional development", "In the Moment", "Mary Mary on the TV, joy in the room."),
    ("photo", f"{IMG}/v1784906773/FB_IMG_1782528027750_kytkxv.jpg", "professional development", "Moments", "Mary Mary on the TV, joy in the room."),
    ("photo", f"{IMG}/v1784906771/FB_IMG_1782526867140_2_gjlulc.jpg", "professional development", "Moments II", ""),
    ("photo", f"{IMG}/v1784906771/FB_IMG_1782527021521_2_douier.jpg", "professional development", "Moments III", ""),
    ("photo", f"{IMG}/v1784906771/FB_IMG_1782526988372_2_cnqip0.jpg", "professional development", "Moments IV", ""),
    ("photo", f"{IMG}/v1784906771/FB_IMG_1782526855565_3_igguga.jpg", "professional development", "Moments V", ""),
    ("photo", f"{IMG}/v1784906770/FB_IMG_1782527010628_dgxyzt.jpg", "professional development", "Moments VI", ""),
    ("photo", f"{IMG}/v1784906764/2995-1_rupm8b.jpg", "professional development", "Moments VII", ""),
    ("photo", f"{IMG}/v1784906762/2985_fjwpum.jpg", "professional development", "Moments VIII", ""),
    ("photo", f"{IMG}/v1784906761/1054_al1v8a.jpg", "professional development", "Moments IX", ""),
    ("photo", f"{IMG}/v1784906761/2933_cscwbq.jpg", "professional development", "Moments X", ""),
    ("photo", f"{IMG}/v1784906761/2983_pn1vfz.jpg", "professional development", "Moments XI", ""),
    ("photo", f"{IMG}/v1784906761/2939_kluigz.jpg", "professional development", "Moments XII", ""),
    ("photo", f"{IMG}/v1784906761/2981_gygezo.jpg", "professional development", "Moments XIII", ""),
    ("photo", f"{IMG}/v1784906760/3020_leh2ig.jpg", "professional development", "Moments XIV", ""),
    ("photo", f"{IMG}/v1785974733/1785118821477_zwarpc.png", "Speaking & Media", "Speaking & Media", "Speaking & Media 1"),
    ("photo", f"{IMG}/v1785976328/1785121140177_2_1_nwlehz.jpg", "Speaking & Media", "Speaking & Media", "Speaking & Media 2"),
    ("photo", f"{IMG}/v1784906770/DSC05290_4_cwygq1.jpg", "Speaking & Media", "Speaking & Media", "Speaking & Media 3"),
    ("photo", f"{IMG}/v1784906774/FB_IMG_1782527964318_2_c8t0a6.jpg", "Community", "Vision Board Party", "With Oli Porter's W.A.R. youth group — refreshments & supplies sponsored by Ylonda Dickerson, Valley View Community Cares."),
    ("photo", f"{IMG}/v1784906765/2938_z3exnk.jpg", "Community", "Brush & Bond", "With Artist Caroline App — hosted by Footprints Youth Division of Recovery Girls Rock."),
    ("photo", f"{IMG}/v1785974732/1785116716741_fc1k1o.png", "Community", "Vision Board Party II", ""),
    ("photo", f"{IMG}/v1785974732/1785117385200_hdbz2f.png", "Community", "Vision Board Party II", ""),
    ("photo", f"{IMG}/IMG_20260626_154427_3_1_yeodun.jpg", "Community", "Vision Board Party II", ""),
    ("photo", f"{IMG}/v1784906769/2838_un5kuf.jpg", "Community", "Footprints IV", ""),
    ("photo", f"{IMG}/v1784906773/PXL_20260618_012102849_y0euum.jpg", "Community", "Vision Board Party II", ""),
    ("photo", f"{IMG}/v1784906770/PXL_20260618_012106102_f7kmo7.jpg", "Community", "Vision Board Party III", ""),
    ("photo", f"{IMG}/v1784906770/PXL_20260618_012047823_ijm8bx.jpg", "Community", "Vision Board Party IV", ""),
    ("photo", f"{IMG}/v1784906770/PXL_20260618_012548568_f3x2t3.jpg", "Community", "Vision Board Party V", ""),
    ("photo", f"{IMG}/v1784906769/PXL_20260618_012055357_yshyf7.jpg", "Community", "Vision Board Party VI", ""),
    ("photo", f"{IMG}/v1784906768/PXL_20260618_012601476_rusbbu.jpg", "Community", "Vision Board Party VII", ""),
    ("photo", f"{IMG}/v1784906767/IMG_20260625_091526_2_fpdzs8.jpg", "Community", "Footprints", "Youth Division of Recovery Girls Rock."),
    ("photo", f"{IMG}/v1784906767/IMG_20260613_134907_wjan4c.jpg", "Community", "Footprints II", ""),
    ("photo", f"{IMG}/v1784906766/IMG_20260626_154427_3_fpd7ev.jpg", "Community", "Footprints III", ""),
    ("photo", f"{IMG}/v1784908261/IMG_20260626_154427_3_viusnr.jpg", "Community", "Annual Sister2Sister", "Clark County Juvenile Detention — community voices invited to uplift, inspire, and share their stories."),
    ("video", f"{VID}/v1784906771/2986_frtou8.mp4", "professional development", "PT, Unscripted", ""),
    ("photo", f"{IMG}/v1784906765/2938_z3exnk.jpg", "Community", "Brush & Bond", "With Artist Caroline App — hosted by Footprints Youth Division of Recovery Girls Rock."),
]

# (product_slug, free_ebook_slug) — buying the product emails this eBook too.
# This is what makes "Includes the 7 Faith Moves™ ebook, free with every
# purchase" actually happen, for the eBook AND the paperback.
PRODUCT_BONUS_EBOOK_LINKS = [
    ("book-ebook", "faith-moves"),
    ("book-paperback", "faith-moves"),
]