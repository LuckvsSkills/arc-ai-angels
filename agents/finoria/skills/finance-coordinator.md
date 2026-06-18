# finance-coordinator

## Doel
Coördineer financiële taken binnen het Finix-domein. Verdeel werk naar de juiste sentinel op basis van specialisme (treasury/controls/accounting/audit).

## Wanneer gebruiken
- Bij binnenkomende financiële taken van Flux
- Bij domain-status rapportage aan Flux
- Bij escalaties vanuit Finix sentinels

## Werkwijze
1. Beoordeel taaktype op Finix-fit
2. Bepaal juiste sentinel: treasury→Kairo, controls→Kenzo, accounting→Zion, audit→Odis
3. Verdeel taak met duidelijke instructie
4. Bewijk output vóór terugkoppeling aan Flux
5. Escaleer compliance/control-risico's expliciet

## Tool
workers/coordinate_finance.py
