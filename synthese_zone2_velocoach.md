# Synthèse Zone 2 — Protocole personnalisé Jean Gay

*Document de référence à intégrer au projet VeloCoach AI. Source : synthèse vidéo pédagogique + calibrage sur données ICU réelles (01/07/2026, FTP 219W, 69kg).*

---

## 1. Définition physiologique de la Zone 2

- Intensité située **10-15% sous le premier seuil lactate (LT1)**, soit environ **65-75% de FTP**.
- RPE cible : **3-4/10** (conversation possible mais concentration requise — ni "trop facile" type récup, ni proche du seuil).
- Marqueur biologique : lactatémie stable **1-2 mmol/L**, proche des valeurs de repos. Pas de dérive dans le temps (contrairement à un effort au-dessus du 2e seuil qui dérive progressivement jusqu'à l'épuisement).
- Le LT1 lui-même correspond à un RPE ~5/10 — trop élevé pour des sorties d'endurance classiques répétées 3-4×/semaine. D'où la marge de 10-15% en dessous.

## 2. Pourquoi ça marche — les deux adaptations clés

| Adaptation | Mécanisme | Bénéfice |
|---|---|---|
| Angiogenèse | Création de nouveaux capillaires sanguins musculaires | Plus d'apport O2/nutriments, meilleure clairance |
| Biogenèse mitochondriale | Création/adaptation des mitochondries | Meilleure utilisation glucides/lipides, meilleure clairance du lactate |

Ces deux adaptations sont aussi obtenues en haute intensité, mais par des **voies différentes**. D'où l'intérêt de ne pas saturer une seule voie sur toute une saison — alterner Z2 et haute intensité maximise le signal adaptatif sur le long terme.

## 3. Repères puissance pour Jean (calibré sur FTP courant)

> ⚠️ FTP variable — recalculer ces zones à chaque mise à jour de l'eFTP ICU.

| Zone | % FTP | Watts (FTP 219W) | RPE | Rôle |
|---|---|---|---|---|
| Z1 récupération stricte | <60% | <130 W | 1-2/10 | Drainage, digestion de charge |
| **Vraie Z2** | 65-75% | **142-164 W** | 3-4/10 | Volume aérobie, angiogenèse/mitochondries |
| Seuil / Sweet Spot | 88-94% | 193-206 W | 6-7/10 | Combler le déficit d'endurance seuil (limiter prioritaire) |

**Constat de calibrage (juin 2026)** : plusieurs sorties étiquetées "Z2" dans l'historique tournaient en réalité à 84-131W de moyenne (38-60% FTP) — c'est de la Z1, pas de la Z2. Souvent lié à la chaleur (28-38°C sur la majorité des sorties de juin en Auvergne). Bien distinguer l'intention (vrai stimulus Z2 vs récupération) avant de partir rouler.

## 4. Erreurs à éviter (issues de la synthèse vidéo)

1. **Rouler trop près du LT1 en continu** — non soutenable sur la durée, génère trop de fatigue pour le bénéfice apporté.
2. **Piloter à la puissance moyenne de sortie plutôt qu'à la puissance des portions roulées** — particulièrement faux en terrain vallonné/montagne (le profil de Jean) où les descentes cassent la moyenne.
3. **Ignorer le RPE au profit du seul chiffre en watts** — le RPE intègre fatigue, sommeil, chaleur, stress ; les watts seuls non.
4. **Croire que 100% Z2 est optimal** — la littérature converge vers un ratio **80/20** basse/haute intensité, pas 100/0.
5. **Bannir toutes les sorties de groupe** — accepter l'équilibre plaisir/précision ; une sortie club peut même devenir une excellente séance seuil si le rythme du groupe colle à la cible.
6. **Ne pas adapter selon le temps disponible** :
   - Peu de temps disponible → viser le **haut** de la Z2 (proche 75% FTP) pour maximiser le stress dans la fenêtre courte.
   - Beaucoup de temps disponible → possibilité de redescendre légèrement l'intensité pour éviter la fatigue cumulée excessive sur gros volume.

## 5. Types de séances à alterner

### A — Z2 continue longue (3-4h)
142-164W tenus en continu y compris en montée, descentes en récupération passive. Format recommandé pour développer la capacité à *tenir* une intensité dans la durée — cible directement le déficit d'endurance seuil à 1h. Idéal en période creuse / hiver, départ tôt pour éviter la chaleur.

### B — Z2 fractionnée par blocs de col
Chaque montée en haut de Z2 (155-164W), descentes en récupération. Adapté au terrain d'Auvergne. Piloter sur la puissance de la portion roulée, jamais sur la moyenne globale.

### C — Seuil progressif (priorité n°1 actuelle)
2-3×15-20min à 193-206W, récupération 5min à Z1. Progression : 3×15min → 3×20min → 2×25min sur les semaines suivantes.
**Point d'exécution critique** : verrouiller la puissance cible dès la première minute de chaque intervalle (pas de montée en charge molle) — écart identifié sur une séance récente où le temps réel passé en zone SS était très inférieur à l'intention affichée.

### D — Récupération stricte
<130W, RPE 1-2/10, 45min max. Rôle différent de la Z2 — ne pas confondre les deux dans la planification.

### E — Sortie club / intensité imposée
Accepter que l'intensité déborde parfois de la Z2 stricte si le groupe roule plus fort — peut devenir une séance seuil productive si bien exploitée.

## 6. Règle de dosage selon le contexte

- **Périodes de compétition ou blocs très chargés** → baisser l'intensité des sorties Z2, préserver l'énergie pour les séances intenses et les courses. Ne pas ajouter de charge inutile.
- **Hiver / périodes creuses** → Z2 plus stricte et plus continue, meilleure récupération disponible, moins de contraintes de calendrier.
- **Chaleur extrême (>30°C, cas fréquent en Auvergne l'été)** → réduire la puissance cible de façon proportionnelle ; le RPE doit primer sur le chiffre en watts ce jour-là.
- **Ratio global saison** : viser 80-90% du temps en basse intensité, 10-20% en haute intensité — la proportion augmente vers 90% à mesure que le volume hebdomadaire total augmente.

## 7. Points de vigilance spécifiques au suivi ICU

- L'eFTP ICU **décroît automatiquement** en l'absence d'effort seuil récent exploitable par le modèle — une baisse de 1-2W/semaine sans séance qualité n'est pas une perte de forme réelle, c'est un artefact de modèle. Ne pas ajuster les zones d'entraînement sur cette seule base sans séance de vérification.
- Toujours croiser l'intitulé d'une séance avec `icu_zone_times` réel avant de la considérer comme "faite comme prévu" — l'écart entre intention et exécution peut être important (ex. temps réel en zone SS très inférieur à la durée d'intervalle prévue).
- Le découplage (`decoupling`) est un bon marqueur de qualité de la séance Z2/seuil : viser <5% en valeur absolue. Des valeurs >15-20% (positives ou négatives) sur des sorties courtes ou avec beaucoup d'arrêts sont souvent du bruit de mesure plutôt qu'un vrai signal physiologique — à interpréter avec prudence sur les sorties <1h ou très fragmentées.

## 8. Validation croisée — autres sources (recherche web, juillet 2026)

*Cette section complète la vidéo avec d'autres coachs/chercheurs. Sources : CTS/TrainRight, San-Millán (physiologiste de Pogačar), Seiler (recherche polarisée), Roadman Cycling, études PLOS ONE / littérature masters.*

### Convergences avec la vidéo
- Définitions %FTP cohérentes : 55-75% (système 6 zones) ou 60-70% (système 3 zones), RPE 5-6/10 selon CTS — légèrement plus haut que la vidéo (3-4/10), confirmant que le RPE prime sur le chiffre exact.
- Seiler & Kjerland (2006, *Scand J Med Sci Sports*) : étude sur des skieurs de fond élite (384 séances) confirmant le schéma ~80% facile / ~20% dur, quasi rien en zone intermédiaire. Répliqué chez rameurs et coureurs élite.
- Concept de "zone noire" (76-105% FTP) : intensité assez dure pour exiger de la récupération, pas assez pour driver les meilleures adaptations aérobies/VO2max — la zone la moins rentable de toutes.

### Apport San-Millán (physiologiste utilisé par UAE Team Emirates / Pogačar)
- 3 bénéfices clés de la Z2 : oxydation des graisses, fonction mitochondriale, transport du lactate entre fibres (transporteurs MCT1/MCT4).
- Z2 = zone "FatMax", recrutement dominant fibres de type I.
- **Point critique terrain vallonné** : chaque pic de puissance ("power surge") supprime l'oxydation des graisses pendant jusqu'à 30 minutes après le pic. Sur un terrain avec relances fréquentes (Auvergne), ça casse le stimulus métabolique voulu à répétition — piloter la puissance en montée sans à-coups devient encore plus critique qu'en terrain plat.

### Spécificités masters/cycliste expérimenté (directement applicables)
- **Durée minimale efficace** : pour un athlète avec CTL élevé et système aérobie déjà développé, il faut un stimulus plus important — la dose minimale efficace en Z2 est de **2 à 4h**, contre 60-90min pour un cycliste intermédiaire. Valide les sorties longues déjà pratiquées ; confirme que les sorties Z2 d'1h-1h30 sont un complément utile mais insuffisant seul pour créer une nouvelle adaptation à ce niveau.
- **Plafond VO2max après 40 ans** : une seule séance VO2max/semaine maximum — une deuxième vole de la récupération sans ajouter de forme. Les adaptations d'un bloc VO2max (6-8 semaines) disparaissent en 4-6 semaines sans entretien → caler les blocs juste avant les objectifs, pas des mois en amont.
- **Musculation — argument renforcé** : l'entraînement en résistance chargée est l'un des seuls moyens de préserver/reconstruire les fibres de type II — ni la Z2, ni même le travail seuil n'y suffisent. Méta-analyse 2025 (262 cyclistes entraînés, 17 études) : la musculation améliore significativement l'efficience de pédalage, la puissance anaérobie et la performance CLM, sans effet négatif sur la VO2max.
- **Travail à cadence basse — piste à explorer** : étude Hebisz & Hebisz (2024, *PLOS ONE*) — intervalles à cadence basse (50-70 rpm) vs cadence libre, 8 semaines, cyclistes entraînés : +8,7% VO2max (vs +4,6%) et +8,1% puissance aérobie max (vs +3%) pour le groupe cadence basse. Mécanisme : la cadence basse force les fibres de type II à travailler en aérobie, un signal d'adaptation qu'elles reçoivent rarement. Pertinent vu le profil MMP de Jean (bon sprint neuromusculaire, lacune anaérobie 30s-2min) : blocs de 4-10min à 50-65rpm, RPE 7/10, 4-6 répétitions, récup 4min.
- **Repère power-to-weight par tranche d'âge** : cyclistes 60-80 ans, courbe moyenne 2,25-2,5 w/kg ; les athlètes bien entraînés dépassent largement cette moyenne. Point de contexte utile, sans remettre en cause l'objectif personnel de 3,5 w/kg.

### Nuance scientifique
Une étude sur la variabilité individuelle des seuils de Z2 (cohorte de 50 cyclistes expérimentés) souligne les limites des prescriptions basées uniquement sur des %FTP fixes, et appelle à des approches individualisées — cohérent avec l'importance du RPE et du test lactate soulignée dans la vidéo source.
