# Eleken Full Homepage Design System & Brand Specification
*Authoritative reverse-engineered design architecture for the complete Eleken homepage (`eleken.co`)*

---

## 1. Core Visual Principles

1. **Monochrome Warm Canvas**: The canvas is a warm linen off-white (`#f9f7f3`). All typography, cards, and UI elements exist strictly in shades of black, charcoal, and warm gray.
2. **Zero Accent Colors**: Strict prohibition against orange, blue, purple, or pastel chips.
3. **Rigid Unified Button Standard**: Every button across all 16 sections shares the exact production geometry: `padding: 9px 16px`, `border-radius: 10px`, `font-size: 13px`, `line-height: 1.2` (total height ~34px), and `gap: 10px`.
4. **Scrubbed Letter-by-Letter Scroll Scrub**: Editorial narrative sections transition letter-by-letter and icon-by-icon from muted gray (`#888686`) to deep black (`#000000`) as the reader scrolls.
5. **Generous Vertical Spacing**: Standard section rhythm uses `96px` to `150px` bottom margins, creating an unhurried, editorial reading experience.

---

## 2. Color Palette System

| Role | Token / Value | Hex | Usage |
| :--- | :--- | :--- | :--- |
| **Canvas Background** | `--canvas` | `#f9f7f3` | Primary viewport background (warm paper texture) |
| **Card Surface** | `--white` | `#ffffff` | Elevated cards, service tiles, review boxes, containers |
| **Primary Ink** | `--ink` | `#1d1e22` | Headings, active letters, solid primary buttons |
| **Primary Ink Hover** | `--ink-hover` | `#393a3f` | Button hover background |
| **Revealed Text (Active)** | `--text-active` | `#000000` | Fully revealed characters in scroll animation |
| **Unrevealed Text (Inactive)** | `--text-inactive`| `#888686` / `#757576` | Unreached characters in scroll scrub animation |
| **Muted Body Text** | `--body` | `#616161` | General paragraph copy and secondary labels |
| **Hairline Dividers** | `--border` | `#e4e4e4` | Card outlines, navbar divider, input borders |
| **Subtle Card Borders** | `--border-subtle` | `#ece9e3` | Bento grid and service tile hairline borders |
| **Mockup Surfaces** | `--canvas-subtle` | `#f3f1ec` | Mockup wrapper backgrounds, metric card tags |

---

## 3. Typography Hierarchy Matrix

All headings use **`Regolapro`** (Medium 500 or Bold 700). Body copy uses **`Inter Variable Local`**.

| Element / Class | Font Family | Size (Desktop) | Size (Mobile) | Weight | Line Height | Letter Spacing | Color |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Hero H1** (`.hero-h1`) | `Regolapro` | `52px` | `38px` | `500` / `700` | `1.1` (`57.2px`) | `-1.04px` | `#1d1e22` |
| **Section H2** (`.section-h2`) | `Regolapro` | `32px` | `24px` | `500` | `1.25` (`40px`) | `-0.64px` | `#1d1e22` |
| **Editorial Narrative** (`.animated-text`) | `Regolapro` | **`28px`** | **`22px`** | `500` | `1.28571` (`36px`) | `-0.56px` | Scrubbed `#888686` → `#000000` |
| **Service Title** (`.service-title`) | `Regolapro` | `24px` | `20px` | `500` | `1.25` | `-0.48px` | `#1d1e22` |
| **Big Metric Stat** (`.case-stat`) | `Regolapro` | `32px` | `28px` | `700` | `1.1` | `-0.64px` | `#1d1e22` |
| **Card H3 Title** (`.reason-title`, `.case-title`) | `Regolapro` | `22px` | `19px` | `500` | `1.3` (`28.6px`) | `-0.44px` | `#1d1e22` |
| **Numbered Headings** (`.numbered-title`) | `Regolapro` | `19px` | `17px` | `500` | `1.35` | `-0.38px` | `#1d1e22` |
| **Body Paragraphs** (`body`, `.p`, `.hero-desc`) | `Inter Variable` | `15px` | `13px` | `400` | `1.6` (`24px`) | `0px` | `#616161` |
| **Buttons & CTAs** (`.btn`) | `Inter Variable` | **`13px`** | **`13px`** | `500` | `1.2` (`15.6px`) | `0px` | White or Charcoal |
| **Footer & Meta Links** | `Inter Variable` | `12px` / `14px` | `11px` | `400` / `500` | `1.5` | `0px` | `#8c8c8c` |

---

## 4. Editorial Narrative & Scroll Scrub Reveal System

The section starting with *"You're pouring money into marketing and sales..."* is a signature Eleken brand touchpoint.

### Layout Geometry
- **Container Max-Width**: `549px` (centered with `margin: 0 auto 150px`)
- **Item Rhythm**: `margin-bottom: 36px` between narrative blocks and the bullet list
- **List Gap**: `32px` vertical gap between list items, `16px` horizontal gap between icon and text
- **List Icon**: `24×24px` circle with centered diagonal cross `[⊗]`, stroke `2px`, color `currentColor`

### Scroll Scrub Animation Specification
- **Color Transition**:
  - Inactive State: `color: #888686;`
  - Active State: `color: #000000;`
  - Media/Icons: `opacity: 0.4;` (inactive) → `opacity: 1.0;` (active)
  - CSS Transition: `transition: color 0.3s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1);`
- **Dual Engine Implementation**:
  - **GSAP ScrollTrigger**: Loaded via CDN, configured with `start: 'top 65%', end: 'bottom 35%', scrub: 0.5`.
  - **Frame-Throttled Fallback**: Native `requestAnimationFrame` scrub calculates character count based on viewport intersection.

---

## 5. Rigid Unified Button System (1:1 from Eleken Production)

Buttons across the entire site are unified into a single geometric standard:

```css
:root {
  --btn-padding: 9px 16px;
  --btn-radius: 10px;           /* 10px squircle contour */
  --btn-font-size: 13px;
  --btn-font-weight: 500;
  --btn-line-height: 1.2;
  --btn-gap: 10px;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--btn-gap);
  padding: var(--btn-padding);
  font-family: var(--font-body);
  font-size: var(--btn-font-size);
  font-weight: var(--btn-font-weight);
  border-radius: var(--btn-radius);
  line-height: var(--btn-line-height);
  color: #ffffff;
  background-color: #1d1e22;
  text-decoration: none;
  box-sizing: border-box;
  white-space: nowrap;
  transition: background-color 0.2s ease, border-color 0.2s ease;
}

/* Computed Dimensions */
/* Height: ~34px (9px top + 15.6px text + 9px bottom) */
/* Horizontal Padding: 16px */
/* Corner Radius: 10px */

.btn-arrow-icon {
  width: 16px;
  height: 17px;
  min-width: 16px;
  display: block;
  flex-shrink: 0;
  transition: transform 0.2s ease;
}

.btn:hover .btn-arrow-icon {
  transform: translateX(3px);
}

/* Mobile Breakpoint (max-width: 479px) */
@media screen and (max-width: 479px) {
  .btn {
    justify-content: center;
    padding: 13px 16px;
    font-size: 13px;
    line-height: 1;
  }
}
```

### The 2 Allowed Variants
1. **Primary Solid Black (`.btn` / `.btn-primary`)**:
   - Background: `#1d1e22`
   - Text: `#ffffff`
   - Border: `1px solid transparent`
   - Hover: `background: #393a3f;`
   - *Used for*: Main CTA ("Book a call", "Get started"), Editorial CTA ("More on UX audit"), Case Study Actions ("More product design examples", "Check more examples", "More UX case studies"), Service exploration.
2. **Secondary Light Canvas (`.btn.light-arrow` / `.btn-light`)**:
   - Background: `#f9f7f3`
   - Text: `#1d1e22`
   - Border: `1px solid #e4e4e4`
   - Hover: `background: #ffffff; border-color: #1d1e22;`
   - *Used for*: Secondary actions ("Check portfolio", "More on design engineering").

---

## 6. Full 16-Section Homepage Architecture

The homepage is composed of 16 sequential sections on the `#f9f7f3` canvas:

### Section 1: Sticky Navigation
- **Elements**: Eleken wordmark (`24px` height), Links (`Case studies`, `Services`, `Industries`, `Pricing`, `About`, `Blog`), Primary CTA button (`Get started`).
- **Behavior**: Smooth fade/hide on downward scroll, instant reveal on upward scroll.

### Section 2: Hero Section
- **Heading**: `UI/UX design agency for B2B SaaS` (`52px` Regolapro).
- **Description**: Target audience positioning statement.
- **CTAs**: Primary `Book a call` + Secondary `Check portfolio →`.
- **Metrics Marquee/Grid**: 8 metric tiles (`200%`, `2K`, `90%`, `x2`, `30+`, `$18M`, `$200M`, `1,200`).

### Section 3: Editorial Scroll Text Reveal
- **Narrative**: *"You're pouring money into marketing and sales..."*
- **4 Key Pain Points**: Real-time scrubbed letter-by-letter with circle-cross SVG indicators.
- **CTA**: Primary black button `More on UX audit →`.

### Section 4: Bento Grid — What Brings SaaS Teams to Us
- **Grid Layout**: 3 columns × 2 rows, `8px` gap, white cards with `28×28px` hairline icons (`1.5px` stroke).
- **6 Core Reasons**:
  1. *The product is powerful. Users just don't see it.*
  2. *We launch in two months, and the product isn't ready.*
  3. *Onboarding leaks users.*
  4. *The product outgrew its developer-built UI.*
  5. *Design moves too slow for our roadmap.*
  6. *The sprint is on fire — and our designer just left.*

### Section 5: Services Architecture — Pinned Scroll & 3D Isometric Animation
- **Layout & Behavior**: Rather than static cards, this section is a **tall scroll-pinned track** (`height: 450vh`) with a sticky viewport panel (`position: sticky; top: 80px`). As the reader scrolls through the section, it remains fixed in place while two synchronized layers animate:
  1. **Left (Text & CTAs)**: The 5 core services cross-fade in place (`[data-state="active"]`, `[data-state="before"]`, `[data-state="after"]`) with smooth 0.4s transitions.
  2. **Right (3D Isometric Scene)**: A dedicated Lottie animation renders the isometric wireframe cube structure with the signature orange sphere in the center (matching `media_1793173666272_fb35056a.png`), scrubbing frame-by-frame (frames 0 to 112) as the user scrolls.
- **5 Core Services**:
  1. **Product Redesign**: *"For SaaS teams with a product that works but doesn't convert or retain."* (Outcomes: Higher conversion, better adoption). Button: `Explore redesign services →`. Lottie: Initial cube base with central orange sphere.
  2. **Pre-launch Product Design**: *"For founders who've built with devs or AI but aren't customer-ready."* (Outcomes: Faster time to market). Button: `Explore pre-launch design services →`. Lottie: Middle tier cubes forming.
  3. **Team Extension**: *"For teams whose roadmap is moving faster than design capacity."* (Outcomes: No design bottleneck). Button: `Explore team extension services →`. Lottie: Upper cube layers stacking.
  4. **UX Audit**: *"For teams that know something is broken but aren't sure where to start."* (Outcomes: Clear priorities, less guesswork). Button: `Explore UX audit services →`. Lottie: High-density isometric facets.
  5. **Design System**: *"For teams shipping fast with AI who need interface consistency."* (Outcomes: AI-ready foundation, less rework). Button: `Explore design systems services →`. Lottie: Full isometric pyramid assembly complete.
  3. **Team Extension**: *"For teams whose roadmap is moving faster than design capacity."* (Outcomes: No design bottleneck). Button: `Explore team extension services →`.
  4. **UX Audit**: *"For teams that know something is broken but aren't sure where to start."* (Outcomes: Clear priorities, less guesswork). Button: `Explore UX audit services →`.
  5. **Design System**: *"For teams shipping fast with AI who need interface consistency."* (Outcomes: AI-ready foundation, less rework). Button: `Explore design systems services →`.

### Section 6: Case Studies — What Happens When You Fix the Right Problem
- **Headline**: `What happens when you fix the right product problem` (`34px` Regolapro Medium, centered, `letter-spacing: -0.8px`, `margin-bottom: 48px`).
- **Grid Geometry**: 2 columns × 2 rows, `16px` gap between columns, `16px` gap between rows. All cards have `border-radius: 12px` and pure white `#ffffff` surface on the `#f9f7f3` canvas.
- **Top Row (Editorial Callouts)**:
  - Both cards feature generous `padding: 44px 44px 38px`, `min-height: 240px`, with flex-direction column and `justify-content: space-between`.
  - Left Card:
    - Text: *"Eleken redesigned Datawisp's core UX to make its complex data logic easier to understand and use."* (`20px` Regolapro Medium, `line-height: 1.45`, `color: #1d1e22`, `letter-spacing: -0.3px`).
    - CTA: `<a href="#" class="btn btn-primary">More product design examples →</a>` (solid black, `10px` radius).
  - Right Card:
    - Text: *“Client has seen a huge growth in users (from 0 to 2k) and new paid customers thanks to the new design.”* (`20px` Regolapro Medium, `line-height: 1.45`, `color: #1d1e22`, `letter-spacing: -0.3px`).
    - CTA: `<a href="#" class="btn btn-primary">More works by our designers →</a>` (solid black, `10px` radius).
- **Bottom Row (Large Showcase Cards)**:
  - Left Showcase (`NWORX`):
    - Top Mockup Container (`.case-media`): `background: #f2efe9; height: 270px; padding: 28px 28px 0; display: flex; align-items: flex-end;`.
    - Inner App Mockup Window: White floating card (`border-radius: 8px 8px 0 0; box-shadow: 0 4px 20px rgba(0,0,0,0.04); height: 242px; border: 1px solid rgba(0,0,0,0.06); border-bottom: none;`).
      - Dark sidebar (`#17181c`, `108px` width) with `▲ NWORX` brand mark, dark search box, active `● Goals` item, `Chat`, `Journal`, `Activity`.
      - Right content pane: `Goals > Cohort 1`, title `Leaderboards`, subtext `See leaderboards for a specific goal or milestone.`, dropdown `Goal 1: Scope long-term development... ▼`, and two rank cards (`1. Olivia Rhye 1204 pts.` & `2. Esther Howard 1104 pts.`).
    - Bottom Content Area (`.case-body`): `padding: 40px 44px 40px; display: flex; flex-direction: column; justify-content: space-between;`.
      - Stat: `200%` (`42px` Regolapro Bold, `letter-spacing: -1px`, `line-height: 1`, `margin-bottom: 8px`).
      - Headline: `increase in positive feedback.` (`23px` Regolapro Medium, `letter-spacing: -0.4px`, `margin-bottom: 12px`).
      - Description: `There has been a 200% improvement in the positive anecdotes on the App UI` (`15px` Inter Regular, `#616161`, `line-height: 1.55`, `margin-bottom: 28px`).
      - CTA: `<a href="#" class="btn btn-primary">Check more examples →</a>` (solid black, `10px` radius).
  - Right Showcase (`ANDSEND`):
    - Top Mockup Container (`.case-media`): `background: #edeae4; height: 270px; padding: 28px 28px 0; display: flex; align-items: flex-end;`.
    - Inner App Mockup Window: White floating card (`border-radius: 8px 8px 0 0; box-shadow: 0 4px 20px rgba(0,0,0,0.04); height: 242px; border: 1px solid rgba(0,0,0,0.06); border-bottom: none;`).
      - Light sidebar (`115px` width, `border-right: 1px solid #eee`) with `Search ⌘K`, `+ Add contact`, `4/5 Get started →` step box, `⚡ Actions 6`, `Playbooks`, `Conversations`, `Contacts`.
      - Right content pane: Title `Focus`, and three task checklist rows (`[ ] Liam Rodriguez • Book a Call`, `[☑] Isabella Rivera • Reply` with blue checkbox, `[ ] Melania Perez • Follow-up`).
    - Bottom Content Area (`.case-body`): `padding: 40px 44px 40px; display: flex; flex-direction: column; justify-content: space-between;`.
      - Stat: `2x` (`42px` Regolapro Bold, `letter-spacing: -1px`, `line-height: 1`, `margin-bottom: 8px`).
      - Headline: `activation rates after a full UX overhaul.` (`23px` Regolapro Medium, `letter-spacing: -0.4px`, `margin-bottom: 12px`).
      - Description: `Eleken rebuilt core flows from scratch until the product could onboard users without a single sales call.` (`15px` Inter Regular, `#616161`, `line-height: 1.55`, `margin-bottom: 28px`).
      - CTA: `<a href="#" class="btn btn-primary">More UX case studies →</a>` (solid black, `10px` radius).

### Section 7: Domain Expertise & Industries
- **Headline**: `11 years and 400+ products means we rarely start from zero`.
- **6 Industry Tiles**: Fintech, Healthcare, B2B Data, AI Products, Geospatial, DevTools & Cyber.
- **CTA**: Secondary light button `Check portfolio →`.

### Section 8: AI Paradigm Shift Philosophy (1:1 with media_1793177449527_be0d320c)
- **Headline**: `AI made screens cheap. Product judgment became more valuable` (`34px` Regolapro Medium, centered, `letter-spacing: -0.8px`, `margin-bottom: 16px`).
- **Subtitle**: `Teams come to our SaaS design agency with products built in Lovable, Cursor, or Claude Code. The screens usually look fine. That was never the hard part.` (`15px` Inter Regular, `#616161`, centered, `max-width: 580px`, `margin-bottom: 56px`).
- **4 Borderless Typography Columns**:
  - Pure typography layout with zero cards, zero borders, and centered text alignment (`display: grid; grid-template-columns: repeat(4, 1fr); gap: 36px`).
  - `01`: `Understand your users` — *"Why they drop out of onboarding, and which feature they never find."*
  - `02`: `Know your numbers` — *"Where activation, conversion, or retention falls, and what that costs you."*
  - `03`: `Decide what to fix first` — *"Which problems are worth solving now, and which can wait."*
  - `04`: `Build faster with AI` — *"Then use AI to ship the right solution, not just more prototypes."*
  - **Number Metrics**: Large soft grey numerals (`38px` Regolapro, `#9e9fa3`, `line-height: 1`, `margin-bottom: 20px`).
  - **Column Titles**: `17px` Regolapro Semibold (`#1d1e22`, `letter-spacing: -0.3px`, `margin-bottom: 10px`).
  - **Column Descriptions**: `14px` Inter Regular (`#616161`, `line-height: 1.5`, `max-width: 240px`).

### Section 9: Senior Designer Focus — Orbital Lottie Animation (1:1 with media_1793178436489_ce97b62a)
- **Vertical Dotted Connector Arrow**: Centered vertical dashed line (`stroke: #c8c5be; stroke-dasharray: 3 3`) with arrow pointing downward (`↓`), seamlessly bridging Section 8 into Section 9.
- **Headline**: `You're paying a senior product designer to:` (`34px` Regolapro Medium, centered, `line-height: 1.25`, `margin-bottom: 36px`).
- **Official Lottie Animation Architecture (`orbit-desktop.json` / `orbit-lottie-data.js`)**:
  - **Asset Specs**: Vector Lottie animation (`1120×398px`, 800 frames at 30 fps = 26.67s cycle, looping smoothly).
  - **13 Vector Layers**:
    - **Rotating Orbits**: 4 concentric dashed rings (`circle-64`, `circle-96`, `circle-136`, `circle-184`) rotating at calibrated speeds along their axes.
    - **Central 3D Sphere**: Smooth floating orange sphere with 3D spherical gradient and ambient occlusion shadow.
    - **4 Floating Callout Cards with Halo Markers**:
      1. `Get into your users' heads.` (`card-2` + `marker-2`) on Orbit 3.
      2. `Get into your numbers.` (`card-0` + `marker-0`) on Orbit 2.
      3. `Decide which product problems are worth solving.` (`card-1` + `marker-1`) on Orbit 1.
      4. `Use AI to explore and implement the right solution much faster.` (`card-3` + `marker-3`) on Orbit 4.
  - **Interactive Lifecycle**: Autoplays and continuously loops with native SVG vector fidelity. Responsive scaling down across viewports (`398px` desktop, `320px` tablet, `240px` mobile).

### Section 10: Execution Process — S-Track Timeline & Traveling Sphere Animation (1:1 with media_1793181353212_e26a995b)
- **Headline**: `We spend less time drawing screens and own more of what happens around them` (`36px` Regolapro Medium, centered, `line-height: 1.2`, `margin-bottom: 64px`).
- **S-Curve Kinetic Track Architecture**:
  - **SVG Track (`#ps-track-path`)**: Continuous dashed grey path (`stroke: #d8d4ca; stroke-dasharray: 4 4; stroke-width: 1.2`) that starts on the top left, spans across the top row, curves in a smooth $180^\circ$ semi-circle arc on the right, and loops back horizontally across the bottom row.
  - **Traveling 3D Sphere (`<div id="ps-sphere" class="ps-sphere">`)**: Rendered with strict 1:1 circular aspect ratio (`22×22px; border-radius: 50%`) with radial 3D lighting (`radial-gradient(circle at 35% 32%, #ff9e58 0%, #eb681e 55%, #b54508 100%)`) and soft shadow (`0 4px 14px rgba(235, 104, 30, 0.45)`). Positioned via normalized percentage coordinate mapping (`left: (pt.x / 1040) * 100%; top: (pt.y / 320) * 100%`) from `path.getPointAtLength(...)`, guaranteeing that the ball is permanently locked to the dashed line while being completely immune to non-uniform aspect ratio oval distortion.
  - **Kinetic Scroll Dynamics**: Default resting position is set to ratio `0.49` (top track right before the curve, matching Eleken's screenshot). As the user scrolls across the section, the sphere glides smoothly along the track through Steps 1 to 5.
  - **5 Sequential Step Nodes**:
    - **Top Row (Steps 1, 2, 3)**:
      - `01 Identify what matters`: Connected via vertical dashed stem from top track (`x1="160" y1="18" x2="160" y2="48"`). *"Start with the business problem. Dig into analytics, funnels, user behavior, interviews, sales calls, and the product itself to understand what needs to change — and why."*
      - `02 Design the right solution`: Connected via vertical dashed stem (`x1="520" y1="18" x2="520" y2="48"`). *"Turn what we learn into flows and experiences built around the behavior we need to change, not just the screens someone asked for."*
      - `03 Build it faster`: Connected via vertical dashed stem (`x1="880" y1="18" x2="880" y2="48"`). *"Use AI to prototype and refine working interfaces. When your team is ready for it, work with your existing components and deliver the frontend through GitHub instead of another Figma handoff."*
    - **Bottom Row (Right-to-Left alignment under Steps 2 & 3)**:
      - `04 Validate what we built` (under Step 3): Connected via vertical dashed stem from bottom track with marker dot (`cx="880" cy="270"`). *"Put the solution in front of users, stakeholders, or real product data to see whether it solves the problem we started with."*
      - `05 Measure, learn, iterate` (under Step 2): Connected via vertical dashed stem with marker dot (`cx="520" cy="270"`). *"Watch activation, conversion, adoption, time to value, retention, support volume — whatever metric the original problem was tied to — and improve from there."*
- **CTA**: Primary black button `Get a dedicated designer →` (`10px` radius, `padding: 9px 16px`, `16×17px` SVG arrow).

### Section 11: The Broken Handoff Rollercoaster Animation (1:1 with media_1793181379649_7d4fb1ca)
- **Headline**: `Finding the right fix is only half the job. It has to reach production intact` (`36px` Regolapro Medium, centered, `line-height: 1.25`, `margin-bottom: 16px`).
- **Subtitle**: `The traditional workflow makes you build the same interface twice: designers create it in Figma, then developers recreate it in code.` (`15px` Inter Regular, `#616161`, centered, `max-width: 580px`, `margin-bottom: 56px`).
- **Interactive Rollercoaster Path Animation (100% Scroll Scrubbing)**:
  - **Organic Continuous Rollercoaster Track (`#handoff-path`)**: Authentic $C^1/C^2$ continuous cubic Bézier spline directly extracted from Eleken's high-resolution asset. Replaces all sharp triangular `/\` mountain peaks with wide, gentle, natural wave crests, wide loops, and calm settling trajectories:
    `d="M 130.0 212.8 C 130.0 212.8, 175.2 201.4, 197.8 203.2 C 221.2 205.0, 247.3 226.4, 267.9 224.7 C 285.1 223.3, 302.3 213.1, 313.6 202.0 C 324.4 191.3, 328.0 171.2, 335.0 160.0 C 340.1 151.8, 344.2 140.2, 350.0 140.0 C 357.1 139.7, 369.2 156.5, 375.0 168.0 C 381.6 181.0, 385.1 199.5, 385.0 215.0 C 384.9 230.2, 382.8 254.9, 375.0 260.0 C 369.2 263.8, 355.8 260.5, 350.0 255.0 C 342.6 247.9, 339.7 229.0, 340.0 215.0 C 340.4 199.2, 347.0 181.1, 355.0 165.0 C 363.8 147.3, 379.3 115.3, 392.1 113.8 C 402.7 112.6, 414.9 131.1, 425.0 142.3 C 436.0 154.5, 444.7 173.7, 455.0 185.0 C 463.2 194.0, 471.4 202.2, 480.0 206.3 C 487.1 209.6, 493.3 210.8, 501.7 210.2 C 513.8 209.3, 530.9 201.2, 545.1 195.5 C 559.4 189.8, 574.2 186.0, 587.0 175.9 C 602.2 163.9, 612.8 131.5, 627.6 125.0 C 638.4 120.3, 650.2 124.6, 662.0 127.6 C 675.8 131.1, 695.2 135.7, 704.9 146.5 C 715.0 157.8, 717.7 177.8, 720.0 195.0 C 722.5 213.7, 727.7 244.2, 718.0 255.0 C 709.3 264.7, 684.2 265.3, 670.0 262.0 C 656.7 258.9, 640.9 247.9, 635.0 238.0 C 630.2 229.9, 628.6 217.2, 632.0 210.0 C 635.4 202.9, 645.9 196.9, 655.0 195.0 C 665.7 192.7, 681.2 195.9, 693.1 201.1 C 706.1 206.8, 714.3 225.7, 729.2 229.7 C 747.3 234.6, 773.1 221.7, 796.0 220.0 C 820.0 218.2, 870.0 219.6, 870.0 219.6"`
  - **Scroll-Scrubbed Active Drawing Path (`#handoff-draw`)**: Rather than a detached self-playing CSS timer, the orange vector stroke (`#eb681e`, 2px width, round caps) grows directly with scroll position: `strokeDashoffset = pathLength * (1 - scrollProgress)`. Scrolling forward draws the line; scrolling backward retracts it.
  - **Mathematically Locked Station Coordinates**: Every station marker dot and text label is positioned along the path at exact segment points and verified with `path.getPointAtLength(s.ratio * pathLength)`:
    1. `FIGMA` (Ratio `0.0000`, `x=130.0, y=212.8`): Origin checkpoint with outlined orange circle (`○`, `r=7`). Label on top.
    2. `HANDOFF` (Ratio `0.0968`, `x=267.9, y=224.7`): Solid orange checkpoint dot (`●`, `r=6.5`) with glow filter. Label underneath.
    3. `MISSING STATES` (Ratio `0.3993`, `x=392.1, y=113.8`): Gentle, wide top peak of first rollercoaster loop with orange checkpoint dot (`●`, `r=6.5`). Label on top.
    4. `INTERPRETATION` (Ratio `0.5028`, `x=501.7, y=210.2`): Mid-valley checkpoint with orange dot (`●`, `r=6.5`). Label underneath.
    5. `DESIGN QA` (Ratio `0.6102`, `x=627.6, y=125.0`): Wide rounded arch crest of second loop with orange checkpoint dot (`●`, `r=6.5`). Label on top.
    6. `REWORK` (Ratio `0.9036`, `x=729.2, y=229.7`): Post-corkscrew loop checkpoint with orange dot (`●`, `r=6.5`). Label underneath.
    7. `PRODUCTION` (Ratio `1.0000`, `x=870.0, y=219.6`): Final station with crossed orange circle (`⊗`, `r=8`), label on top, and subtitle *"not as designed"* underneath.
  - **Dynamic Bloom State**: Each station node stays hidden (`opacity: 0; transform: scale(0.3)`) until the scrubbed line arrives at its exact coordinate, where it springs open (`opacity: 1; transform: scale(1)`) via `cubic-bezier(0.34, 1.56, 0.64, 1)`.
- **Closing Statement**: `That means another handoff, another round of interpretation, and another place for the experience to change along the way.` (`15px`, `#616161`, centered, `max-width: 580px`).
- **Connector Arrow**: Dotted vertical arrow (`↓`) linking to the code delivery solution.

### Section 12: Frontend Code Delivery & Design Engineering (1:1 with media_1793183263805_79aeec38)
- **Headline**: `We give your developers working frontend code, not just Figma files` (`36px` Regolapro Medium, centered, `line-height: 1.25`, `max-width: 720px`).
- **3 Editorial Columns (Borderless Canvas)**:
  - `01 Working Interface`: *"Our designers start with the flows and logic, then use AI to turn them into a working interface fast. Every interaction, state, and visual detail is still shaped by a designer. You can review and comment on the working design just like in Figma."*
  - `02 Existing Components`: *"AI builds with the components your product already has, like your tables, buttons, forms, and patterns, instead of creating duplicates. We connect it to your Storybook and review everything it produces. No Storybook yet? We set it up and document your components, because clear descriptions are what help AI use them correctly."*
  - `03 Ready for Integration`: *"Once you approve the design, we open a pull request in your repository. Your developers review the code like any other PR, then integrate it with the real product and connect the backend."*
- **Design Engineering Arch Track & Scrubbed Flow**:
  - **Organic Continuous Spline Curve (`viewBox="0 0 920 220"`)**: Fully continuous $C^1/C^2$ cubic Bézier spline directly extracted from Eleken's high-resolution asset. Replaces previous segmented angular ramps with an authentic, gentle arch that flows through an inflection wave at `WORKING INTERFACE`, crests at a broad rounded horizontal plateau at `DESIGNER REFINEMENT`, and descends smoothly into `GITHUB`:
    `d="M 100.0 165.2 C 100.0 165.2, 123.5 167.7, 134.6 168.7 C 145.0 169.7, 153.9 171.0, 164.7 171.2 C 177.1 171.4, 191.4 170.6, 204.7 169.3 C 218.1 168.0, 231.7 166.0, 244.8 163.2 C 257.7 160.4, 270.3 156.7, 282.9 152.7 C 295.5 148.7, 307.3 143.9, 320.4 139.4 C 334.6 134.5, 349.8 129.8, 365.1 124.4 C 381.4 118.7, 398.5 112.2, 415.2 105.9 C 431.9 99.6, 449.1 92.7, 465.4 86.8 C 480.8 81.2, 496.9 75.0, 510.5 71.4 C 521.4 68.6, 531.9 66.9, 540.5 65.9 C 546.9 65.1, 551.4 65.0, 557.5 65.0 C 564.6 65.0, 572.1 65.1, 580.6 65.9 C 591.1 66.9, 603.7 68.6, 615.7 71.4 C 628.7 74.4, 642.2 78.5, 655.8 83.7 C 670.6 89.4, 686.4 97.4, 700.9 104.7 C 714.8 111.7, 728.3 119.5, 741.0 126.8 C 752.6 133.5, 763.9 140.8, 774.1 146.5 C 782.7 151.2, 790.1 155.7, 798.1 158.8 C 805.4 161.6, 820.0 164.8, 820.0 164.8"`
  - **4 Mathematically Locked Checkpoint Stations**:
    1. `STORYBOOK` (Ratio `0.0000`, `x=100.0, y=165.2`): Hollow orange ring (`○`, `r=7`), text on top.
    2. `WORKING INTERFACE` (Ratio `0.2964`, `x=320.4, y=139.4`): Solid orange dot (`●`, `r=6.5`) with downward pointing arrow (`↓`), 2-line title below.
    3. `DESIGNER REFINEMENT` (Ratio `0.6252`, `x=557.5, y=65.0`): Apex solid orange dot (`●`, `r=6.5`) with upward pointing arrow (`↑`), 2-line title above.
    4. `GITHUB` (Ratio `1.0000`, `x=820.0, y=164.8`): Hollow orange ring (`○`, `r=7`), text on top.
  - **Scroll Scrubbing**: Path stroke offset dynamically scrubs with scroll (`#fe-draw`), blooming each station node as the stroke arrives.
- **CTA**: Primary black button `More on design engineering →` (`10px` radius, `padding: 9px 16px`, `16×17px` SVG arrow).

### Section 13: Dedicated Designer Engagement Model (1:1 with media_1793184810253_65721322)
- **Grid Architecture**: 2-column asymmetric split (`440px` sticky left column, `1fr` right column, `72px` gap).
- **Left Column: Philosophy & 3D Dimetric Illustration (Pinned)**:
  - **Headline**: `Work with us like you would with your own designer` (`36px` Regolapro Medium, `#1d1e22`, `line-height: 1.22`, `margin-bottom: 20px`).
  - **Lead Paragraph**: `Most SaaS design agencies hand you an account manager and a project scope. We add a dedicated SaaS designer to your team who works with you directly, gets into your product, and keeps moving from one priority to the next.` (`15px`, `#616161`, `line-height: 1.55`).
  - **Authentic 3D Dimetric Architectural Graphic (`SVG_V3`)**:
    - **Authentic Oblique/Dimetric Projection**: Modeled directly from Eleken's pixel skeleton with asymmetric angles ($45^\circ$ left receding axis, $18.6^\circ$ right receding axis) replacing standard symmetric $30^\circ$ isometric distortion.
    - **Dashed Wireframe Diamond Base**: Ground platform with subtle `#c4c0b6` dashed perimeter (`stroke-dasharray="3 3"`).
    - **Modular Team Cubes**: 6 translucent white wireframe cubes (`fill="rgba(255,255,255,0.75)"`, stroke `#b5b0a6`, 1px stroke-width) showing existing team and product structure.
    - **Hero Dedicated Designer Cube (`.hero-cube-wrap`)**: Prominent front-right orange cube (`#fba16c` top, `#eb681e` left, `#c44e0b` right, `#b54508` border) with soft floor glow and real-time scroll-synced floating elevation (`translateY(${-lift}px)`).
    - **Transparent Wireframe Floating Pavilion Frame**: Elevated at $z=70..90$ with center square opening, transparent facets (`rgba(255,255,255,0.45..0.55)`), delicate `#9e998e` 1.1px strokes, and 4 corner hip lines, allowing full visibility of all cubes underneath.
  - **Sticky Behavior**: Stays pinned at `top: 110px` while the user scrolls down through all 4 steps.
- **Right Column: Scroll-Scrubbed Vertical Stepper**:
  - Continuous vertical progress line situated between the step numbers (`01-04`) and step content.
  - **Zero-Lag Scroll Scrubbing**: Removed CSS transition delay so the active orange bar (`#eb681e`) scrubs downward synchronously with `requestAnimationFrame` as the user scrolls through the 4 steps.
  - **Step Activation Contrast**: Active steps highlight in vibrant orange (`#eb681e` for numbers) and full ink black (`#1d1e22`, opacity 1.0); inactive future steps remain cleanly dimmed (`opacity: 0.32; #a39e93`).
  - **Interactive Click-to-Scroll**: Clicking on any step (`01`, `02`, `03`, `04`) smoothly scrolls the viewport to center that step.
  - **4 Engagement Steps**:
    1. `01 Start when you need us`: *"We match you with a designer and can get started in days, not months."*
    2. `02 Work together directly`: *"Your designer joins your Slack, calls, Figma, GitHub, or whatever your team already uses. No account manager passing messages back and forth."*
    3. `03 Keep them for as long as there's work`: *"Redesign one flow, move to the next, build a design system, help with new features. The same designer keeps the product context instead of starting from zero every project."*
    4. `04 Scale when the workload changes`: *"Add capacity when the roadmap gets busy. Reduce or pause our SaaS UX design subscription when development needs time to catch up."*

### Section 14: Clutch 4.9 Social Proof & Verified Reviews
- **Headline**: `4.9 is our Clutch average`.
- **3 Testimonial Cards**: Verified quotes from Mathew Beechener (Datawisp), Jeff Houlé (SEOCrawl), and David K. (NWORX).

### Section 15: Curated Blog Posts Carousel (1:1 with media_1793183299181_b829b2b5)
- **Header Row**:
  - **Headline**: `Explore our blog posts` (`36px` Regolapro Medium, left-aligned, `#1d1e22`).
  - **Functional Carousel Controls**: Top-right circular outline buttons (`44×44px`, `border: 1px solid #d8d4ca; border-radius: 50%`) with left (`←`) and right (`→`) arrows. Clicking `→` or `←` slides the track by one card width with smooth cubic-bezier easing and dynamic disabled opacity when at boundary.
- **Sliding Multi-Post Track**:
  - 5 Curated thought-leadership cards with custom vector line art illustrations:
    1. *UX Design for SaaS: Best Practices for Clearer Product Flows*
    2. *AI Design Workflow That Actually Works in 2026 [How We Do It at Eleken]*
    3. *Design System For SaaS: Ready-Made Examples and How to Build One That Scales*
    4. *How to Design a SaaS Dashboard Users Actually Look At*
    5. *Product Onboarding: Proven Patterns to Increase SaaS Activation*

### Section 14: Final Risk-Free Trial CTA Box
- **Headline**: `Test our SaaS design subscription on your own product`.
- **Copy**: *"Give us a part of your product that's underperforming. We'll dig into the users, evidence, and business goals, and start working on the solution."*
- **Action**: Primary button `Book a call →` with 3-day money-back guarantee note.

### Section 15: FAQ Accordion
- 4 interactive accordions answering contracts, mobile designs, timezones, and designer pairing.

### Section 16: Multi-Column Site Footer
- **4 Columns**: Solutions, Industries, Case Studies, Global Offices (Kyiv, London, San Francisco).

---

## 7. Default Icon Library Standard
- **Stroke Width**: `1.5px` (bento cards) to `2px` (bullet list icons).
- **Linecaps & Linejoins**: Always `round` (`stroke-linecap="round" stroke-linejoin="round"`).
- **ViewBox**: Standard `24×24` or `28×28`.
- **Fill**: Strictly `none`.
- **Colors**:
  - Inactive / Muted: `rgba(29, 30, 34, 0.4)` or `#8c8c8c`
  - Active: `#1d1e22` / `#000000`
