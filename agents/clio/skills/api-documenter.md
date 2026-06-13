---
name: api-documenter
description: "Documenteer REST API endpoints voor ARC AI Agents projecten."
metadata: { "openclaw": { "emoji": "📖" } }
---
# API Documenter

Gebruik deze skill voor het documenteren van API endpoints.

## API documentatie formaat

### Endpoint documentatie
````markdown
## GET /api/items
Haalt alle items op.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Item naam",
    "description": "Beschrijving"
  }
]
```

## POST /api/items
Maakt een nieuw item aan.

**Request body:**
```json
{
  "name": "Item naam",
  "description": "Beschrijving"
}
```

**Response:**
```json
{
  "id": 2,
  "name": "Item naam",
  "description": "Beschrijving"
}
```
````

## Authenticatie documenteren
````markdown
## Authenticatie
Alle endpoints vereisen een JWT token in de header:
````
Authorization: Bearer [token]
Token ophalen via POST /api/auth/login

## Workflow
1. Lees backend code van Forge
2. Identificeer alle router endpoints
3. Schrijf beschrijving per endpoint
4. Voeg request/response voorbeelden toe
5. Sla op als API.md in project directory
