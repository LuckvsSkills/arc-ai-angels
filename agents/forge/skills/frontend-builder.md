---
name: frontend-builder
description: "Bouw moderne frontends met HTML/CSS/JS of React voor ARC AI Agents projecten."
metadata: { "openclaw": { "emoji": "🎨" } }
---
# Frontend Builder

Gebruik deze skill voor het bouwen van frontends.

## ARC AI Agents design systeem
Gebruik altijd deze kleuren en stijl voor consistentie:

```css
:root {
    --bg:        #0a0a0f;
    --bg2:       #111118;
    --accent:    #c9a84c;
    --text:      #e2e8f0;
    --textMuted: #94a3b8;
    --border:    rgba(255,255,255,0.08);
    --radius:    12px;
}
```

## Component templates

### Hero sectie
```html
<section class="hero">
    <h1>Titel</h1>
    <p>Subtitel beschrijving</p>
    <a href="#" class="btn-primary">Call to Action</a>
</section>
```

### Feature kaart
```html
<div class="card">
    <div class="card-icon">🚀</div>
    <h3>Feature titel</h3>
    <p>Feature beschrijving</p>
</div>
```

### Navigatie
```html
<nav>
    <div class="logo">Naam</div>
    <ul>
        <li><a href="#features">Features</a></li>
        <li><a href="#contact">Contact</a></li>
    </ul>
    <button class="btn-primary">Start</button>
</nav>
```

## React component template
```jsx
import { useState } from 'react'

export default function Component({ title, children }) {
    const [active, setActive] = useState(false)
    
    return (
        <div className={`component ${active ? 'active' : ''}`}>
            <h2>{title}</h2>
            {children}
        </div>
    )
}
```

## Responsive breakpoints
```css
/* Mobile first */
.container { padding: 16px; }

@media (min-width: 768px) {
    .container { padding: 24px; max-width: 1200px; margin: 0 auto; }
}
```
