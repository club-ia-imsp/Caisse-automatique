# Cahier des charges complet AutomaticCheck

**Version :** 2.0  
**Date :** 4 septembre 2026  
**Statut :** prototype expérimental en évolution  
**Porteur :** Sara Houéfa ADJAHO  
**Domaine :** commerce connecté, systèmes embarqués, RFID et gestion commerciale

## 1. Synthèse

AutomaticCheck est un projet de caisse intelligente destiné à simplifier le passage en caisse. La cible est un panier instrumenté dans lequel le client dépose ses articles. Le système identifie les produits, calcule le montant et accompagne l’encaissement sans saisie manuelle article par article.

La version actuelle est un prototype RFID : un identifiant lu sur une carte ou une étiquette est envoyé au serveur, associé à un produit dans SQLite puis affiché dans une interface mobile. Un panier physique a été conçu et imprimé en 3D avec des articles de démonstration. Cette preuve de concept confirme le principe de reconnaissance et de mise à jour du panier.

Le projet n’est pas prêt pour un déploiement commercial. Le paiement est simulé, les ventes et stocks ne sont pas encore transactionnels, et le matériel RFID final doit encore être sélectionné et testé.

## 2. Origine et évolution

La première trajectoire, présentée dans le rapport d’avancement d’avril 2026, reposait sur la reconnaissance visuelle par caméra et intelligence artificielle. Elle explorait une caisse utilisant détection de produits, catalogue, panier, facture, stock et une évolution SaaS.

Les essais ont révélé une limite importante : la reconnaissance caméra n’était pas assez fiable en situation réelle. Variations de lumière, ressemblances entre produits et occultations partielles causaient des erreurs. L’équipe a donc décidé de pivoter vers un panier physique intelligent utilisant des capteurs et la RFID.

Il faut distinguer les trois niveaux suivants :

- ancienne piste : caméra, IA, FastAPI, PostgreSQL, React et SaaS envisagé ;
- prototype présent : panier 3D, lecture série, Flask, SQLite, interface web et code ESP32/MFRC522 ;
- cible magasin : RFID UHF, antennes, pesée, écran, paiement réel, réseau et supervision.

## 3. Contexte et problème

Dans les commerces d’Afrique de l’Ouest et du Bénin, le passage en caisse peut générer attente, erreurs de saisie et difficulté de suivi des ventes. La fiche descriptive de l’innovation identifie les files d’attente, les oublis ou doublons de caisse et la faiblesse du suivi de stock avec les systèmes traditionnels.

AutomaticCheck doit proposer une solution locale, progressive et maintenable. Elle repose sur des composants accessibles, une architecture logicielle ouverte et une interface utilisable par le personnel et les clients. L’objectif n’est pas de supprimer le rôle du personnel : il s’agit de réduire les tâches répétitives et de le recentrer sur l’assistance, la qualité de service et la gestion du magasin.

## 4. Vision et objectifs

### Vision

Créer une solution de panier et de caisse intelligente fiable, abordable et adaptée aux commerces africains, capable d’évoluer d’un pilote local à un déploiement dans plusieurs magasins.

### Objectif général

Identifier automatiquement les produits déposés dans un panier, calculer le montant de l’achat et présenter une interface d’encaissement claire.

### Objectifs spécifiques

1. Concevoir un panier physique instrumenté.
2. Identifier les produits grâce à des étiquettes RFID.
3. Associer chaque identifiant à un nom, prix, catégorie et stock.
4. Mettre à jour le panier après ajout ou retrait d’article.
5. Afficher le détail de l’achat sur un téléphone, une tablette ou un écran embarqué.
6. Préparer les paiements adaptés au terrain : espèces, carte puis Mobile Money.
7. Préparer la gestion de stock, la maintenance et les statistiques de vente.

## 5. Utilisateurs et parties prenantes

| Acteur | Besoin | Rôle |
|---|---|---|
| Client | Acheter vite et comprendre son total | Dépose les produits, vérifie le panier, paie |
| Agent de caisse | Intervenir si nécessaire | Assiste, gère les exceptions et les espèces |
| Responsable | Contrôler catalogue, prix et stock | Administre l’exploitation |
| Technicien | Installer et dépanner | Configure le matériel, réseau et logiciels |
| Équipe projet | Valider et développer | Conçoit, teste et pilote l’innovation |

## 6. Parcours utilisateur cible

1. Le client prend un panier intelligent ou arrive à une borne.
2. Les tags produits sont lus automatiquement.
3. Le système retrouve les produits et actualise le panier.
4. L’écran affiche les articles, quantités et montant.
5. Le retrait d’un article met à jour le panier.
6. Le client sélectionne un moyen de paiement.
7. La transaction est confirmée par un prestataire réel.
8. La vente est enregistrée et le stock ajusté.

Dans le prototype actuel, les étapes de lecture, identification et affichage sont démontrées sur UID connu. La confirmation de paiement reste fictive.

## 7. Exigences fonctionnelles

### Identification

- Lire un UID transmis par le lecteur RFID sur le port série.
- Nettoyer espaces, tirets et deux-points puis convertir en majuscules.
- Rechercher le produit correspondant dans la base.
- Informer l’utilisateur lorsqu’un tag n’est pas reconnu.
- Empêcher les relectures répétées. Le prototype applique un délai de deux secondes.

### Panier

- Afficher nom, prix, catégorie et total.
- Permettre l’ajout et le retrait.
- Vider le panier sur action explicite.
- Dans le prototype, le même UID bascule entre ajout et retrait.
- Dans la cible, gérer plusieurs unités et rendre le panier persistant pendant la session.

### Catalogue et stock

- Enregistrer UID, nom, prix, catégorie et stock.
- Autoriser un utilisateur habilité à administrer le catalogue.
- Prévoir une procédure de pose et d’enregistrement des tags.
- Décrémenter le stock uniquement après paiement réel validé.
- Journaliser ventes, annulations et ajustements.

### Paiement et facture

- Présenter les choix de paiement dans le prototype.
- Connecter, dans la cible, uniquement des prestataires homologués.
- Produire un reçu avec articles, montants, date, transaction et moyen de paiement.
- Ne jamais stocker de donnée bancaire sensible dans l’application.

## 8. Architecture et état réel du dépôt

| Composant | Technologie actuelle | Fonction |
|---|---|---|
| Serveur | Python et Flask | Sert l’interface et l’API locale sur le port 5000 |
| Catalogue | SQLite | Conserve les produits de démonstration |
| RFID | pyserial | Lit les lignes reçues du port COM |
| Interface | HTML, CSS, JavaScript | Affiche le panier sur navigateur mobile |
| Microcontrôleur | Sketch Arduino MFRC522 | Lit un UID et l’écrit à 115200 bauds |

Le panier est gardé en mémoire par le serveur Flask. Les routes API permettent de consulter le panier, les produits et le statut série, de simuler un scan, de vider le panier et de confirmer un paiement de démonstration.

Les descriptions IA, FastAPI, PostgreSQL, caméra, JWT, factures PDF et SaaS trouvées dans le rapport d’avancement décrivent une phase antérieure. Elles ne doivent pas être annoncées comme fonctionnalités présentes dans le code actuel.

## 9. Matériel et décision RFID

### Déjà réalisé

- Panier prototype conçu et imprimé en 3D.
- Articles de démonstration.
- Application Flask, base SQLite et interface mobile.
- Code ESP32/MFRC522 disponible pour une preuve de concept 13,56 MHz.

### À acquérir pour un panier avancé

| Groupe | Équipements |
|---|---|
| Calcul | Raspberry Pi 4 ou 5, carte SD, alimentation 5V/3A |
| RFID | Lecteur UHF, deux antennes patch, câbles SMA |
| Tags | Étiquettes UHF EPC Gen2 en quantité adaptée |
| Contrôle | Quatre cellules de charge 50 kg et modules HX711 |
| Interface | Écran tactile HDMI 7 pouces |
| Énergie | Power bank, câbles et connecteurs |
| Intégration | Boîtier IP54, support écran, fond de panier compatible pesée |

Pour le magasin, prévoir un serveur local, Wi-Fi professionnel, éventuel portique UHF, borne de recharge et terminaux de paiement.

**Décision obligatoire :** MFRC522 travaille à 13,56 MHz alors que la cible magasin prévue repose sur UHF 860-960 MHz. Les lecteurs et tags ne sont pas compatibles. Pour lire plusieurs produits dans un panier, l’UHF est la trajectoire la plus cohérente, mais elle demande un autre matériel et l’adaptation du logiciel.

## 10. Bénéfices attendus pour le contexte africain

AutomaticCheck peut réduire les manipulations à la caisse, améliorer la lisibilité de l’achat et donner une meilleure trace des ventes. Il doit pouvoir être assemblé et maintenu avec des composants standard, en tenant compte des réalités réseau, énergie et paiement locales.

Les marchés visés sont les supermarchés, boutiques de distribution, pharmacies, stations-service et commerces avec un catalogue stable. La valeur réelle devra être démontrée par un pilote : réduction du temps d’attente, baisse des erreurs, facilité de formation et coût d’exploitation acceptable.

Le choix des moyens de paiement doit être réalisé avec les commerçants, banques et opérateurs Mobile Money concernés. Aucune intégration de paiement ne doit être mise en production sans conformité locale et contrat avec le prestataire.

## 11. Exigences non fonctionnelles

| Domaine | Exigence |
|---|---|
| Fiabilité | Pas de double ajout ni retrait injustifié |
| Performance | Mise à jour rapide après lecture |
| Ergonomie | Interface française, lisible sur téléphone et écran |
| Réseau | Comportement maîtrisé en cas de Wi-Fi faible ou indisponible |
| Sécurité | Accès admin, journal d’événements, secrets hors du code |
| Données | Sauvegarde catalogue et ventes ; protection des données personnelles |
| Énergie | Autonomie pilotée et recharge définie |
| Maintenance | Composants remplaçables et diagnostic documenté |

## 12. Hors périmètre actuel

- Paiement réel par carte, Mobile Money ou espèces automatisé.
- Stock et factures transactionnels.
- Gestion d’utilisateurs et rôles.
- Historique persistant des ventes.
- Lecture UHF multi-tags et pesée.
- Détection anti-fraude.
- SaaS multi-magasins, haute disponibilité et supervision de production.

## 13. Risques et mesures

| Risque | Conséquence | Mesure |
|---|---|---|
| Confusion MFRC522/UHF | Achat incompatible | Valider la technologie avant commande |
| Lectures parasites | Panier erroné | Réglage antennes, filtrage, pesée |
| Énergie ou réseau instable | Service interrompu | Batterie, recharge et stratégie de reprise |
| Paiement non sécurisé | Risque financier | Prestataire homologué uniquement |
| Coût trop élevé | Déploiement bloqué | Pilote chiffré et composants standards |
| Faible adoption | Usage limité | Tests avec clients et personnel |
| Données inexactes | Prix ou stocks erronés | Administration contrôlée et journal |

## 14. Feuille de route

### Phase 1 - Stabiliser le prototype

- Vérifier lecteur, port COM et tags.
- Compléter le catalogue et les tests d’ajout/retrait.
- Documenter la pose des étiquettes et les tests.

### Phase 2 - Choisir et tester l’UHF

- Comparer lecteurs, tags et antennes.
- Mesurer les lectures parasites et les zones de lecture.
- Définir le rôle de la pesée.

### Phase 3 - Construire le panier pilote

- Intégrer lecteur, antennes, alimentation et écran.
- Protéger les composants.
- Rendre panier et ventes persistants.
- Tester avec de vrais articles.

### Phase 4 - Exploiter et payer

- Choisir un partenaire de paiement.
- Ajouter factures, stock, rôles et sauvegardes.
- Former le personnel et définir le support.

### Phase 5 - Déployer

- Équiper un magasin pilote.
- Mesurer lecture correcte, délai, incidents, adoption et coût.
- Décider du passage à l’échelle sur les résultats.

## 15. Recette du prototype actuel

1. La base se crée avec les produits de démonstration.
2. Le serveur démarre et l’interface est accessible sur réseau local.
3. Un UID connu ajoute un article.
4. Un UID inconnu ne modifie pas le panier.
5. Une relecture immédiate est ignorée.
6. Après le délai de protection, le même UID retire l’article suivant le fonctionnement actuel.
7. La simulation fonctionne sans lecteur.
8. La réinitialisation vide le panier.
9. Le paiement simulé refuse un panier vide et confirme un panier non vide.

## 16. Indicateurs de réussite du pilote

- délai entre dépôt et affichage ;
- taux de lecture correcte ;
- taux de faux ajouts ou retraits ;
- temps complet de passage ;
- nombre d’interventions d’un agent ;
- disponibilité sur une journée ;
- satisfaction clients et personnel ;
- coût par panier et coût de maintenance.

## 17. Conclusion

AutomaticCheck dispose d’une base concrète : panier 3D, démonstration RFID, catalogue et interface. L’évolution depuis la vision artificielle vers un panier physique montre que la fiabilité terrain prime sur la sophistication technique.

La priorité est de valider le choix RFID, d’intégrer progressivement le matériel et de tester dans un contexte réel. Les fonctions de production - paiement, stock, sécurité, support et déploiement multi-magasins - doivent venir après validation fiable du cœur du parcours.
