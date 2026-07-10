# README_Change_EXTRA_PP_OWNER.md

## Doel
Dit document beschrijft hoe een **extra parkeerplaats (PP)** wordt toegevoegd aan een bestaande eigenaar in het VVE-BRAIN systeem.

## Wanneer toepassen?
- Een eigenaar koopt een extra parkeerplaats.
- Een parkeerplaats wordt overgedragen van de ene naar de andere eigenaar.
- De splitsingsakte wordt gewijzigd met betrekking tot parkeerplaatsen.

---

## 📋 **BENODIGDE GEGEVENS**

| Gegeven | Voorbeeld | Opmerking |
|---------|-----------|-----------|
| Eigenaar | A-88 - Slotlaan 363 | Bestaande eigenaar |
| Parkeerplaatsnummer | A-93 - Slotlaan 395pp | Nieuw toe te voegen |
| Extra stemmen | 1 | Per parkeerplaats |
| Extra breukdelen | 12 | Per parkeerplaats |

---

## 🛠️ **STAPPENPLAN**

### Stap 1: Controleer huidige gegevens
```sql
-- Bekijk huidige eigenaar
SELECT * FROM owners_with_parking WHERE Split_Number = 'A-88';