# Déployer la documentation sur GitHub Pages

Le site à publier est le dossier docs/site. Le workflow prêt à l’emploi est dans .github/workflows/deploy-documentation.yml.

## En local

Ouvrir directement docs/site/index.html, ou lancer :

~~~powershell
python -m http.server 8000 --directory docs/site
~~~

Puis aller sur http://localhost:8000.

## Dans l’organisation GitHub

1. Créer le dépôt AutomaticCheck dans l’organisation.
2. Envoyer la branche main.
3. Dans **Settings → Pages**, choisir **GitHub Actions** comme source.
4. L’action « Publier la documentation » publie automatiquement le site.

L’URL habituelle est https://<organisation>.github.io/AutomaticCheck/.

Un administrateur de l’organisation doit autoriser GitHub Pages et l’exécution des Actions. Le workflow peut aussi être démarré manuellement depuis l’onglet **Actions**.
