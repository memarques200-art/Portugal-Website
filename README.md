# Portugal — Une présentation

Un site d'une seule page qui présente le Portugal, par Luís Marques, en français, italien et allemand.

## Pages

| # | Page | Contenu |
|---|------|---------|
| — | Accueil | Présentation, « Qui suis-je ? », le Portugal en un coup d'œil |
| 01 | Géographie | Chiffres clés, climat, relief, Madère et Açores |
| 02 | Histoire | Drapeau, traité de Windsor, routes maritimes, grandes dates |
| 03 | Institutions | Séparation des pouvoirs, Révolution des Œillets, comparaison Portugal–Suisse |
| 04 | Société | Vie quotidienne, langue portugaise, saudade, diaspora |
| 05 | Culture & gastronomie | Fado, azulejos, plats, vins, fêtes de juin |
| 06 | Sport | Palmarès, Cristiano Ronaldo, surf, rink-hockey… |
| 07 | Régions | Les 5 régions du continent et les 2 archipels |
| 08 | Conclusion | Ce que le Portugal représente pour moi |

## Utilisation

- Ouvrir `index.html` dans un navigateur (le dossier `images/` doit être à côté).
- Pendant la présentation, les flèches **←** et **→** du clavier passent d'une page à l'autre.
- Chaque page a sa propre adresse (`index.html#sport`, etc.), donc on peut actualiser la page sans revenir à l'accueil.
- La langue choisie (FR / IT / DE) est mémorisée.

## Version en un seul fichier

Pour obtenir un seul fichier HTML avec les images intégrées (pratique pour l'envoyer ou le mettre sur une clé USB) :

```
python3 tools/make_single_file.py
```

## Modifier les textes

Les textes sont dans l'objet `I18N` à la fin de `index.html`, avec une entrée par langue (`fr`, `it`, `de`).
Chaque élément traduit porte un attribut `data-i18n="clé"` qui correspond à une clé de cet objet.
Pour changer un texte, modifiez-le dans les trois langues **et** dans le HTML (la version française y est écrite directement).
