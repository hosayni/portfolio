## Objectif

<!-- Décrire le problème et le résultat attendu en une ou deux phrases. -->

## Changements

<!-- Liste des modifications, avec les chemins de fichiers concernés. -->

-

## Vérifications

- [ ] `npm run lint`, `npm run check` et `npm run build` passent dans `web/`
- [ ] `npm run test:e2e` passe (ou la CI le confirme)
- [ ] `ruff check .` et `pytest` passent dans `api/`
- [ ] `docker compose config` passe (et `docker compose build` si Docker change)
- [ ] Le site fonctionne sans l'API (contenu de repli)
- [ ] Accessibilité : navigation clavier et contrastes vérifiés
- [ ] Aucun secret ajouté au dépôt (`.env` ignoré)
- [ ] Toute exception `npm audit` est justifiée et datée
- [ ] Documentation mise à jour si le comportement change

## Captures

<!-- Optionnel : avant / après, mobile et desktop. -->
