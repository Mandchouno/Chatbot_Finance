
# Plan de projet — Chatbot Finance

1) Objectif & périmètre
	•	Offrir un “copilote” financier : réponses fiables, calculateurs (intérêts composés, mensualités de prêt, DCA), éducation financière et notions de base en fiscalité.
	•	Ne pas fournir de conseil personnalisé au sens réglementaire ; rester informatif, avec renvoi vers un humain pour les cas sensibles.
	•	Ciblage initial : finance personnelle et investissement indiciel (ETF/indices), terminologie claire et vulgarisée.

2) Architecture fonctionnelle
	•	Interface de conversation (chat) pilotée par un orchestrateur d’intentions.
	•	Moteur Q/R documenté via récupération de connaissance (RAG) sur une base de documents locale.
	•	“Tools” spécialisés pour les calculs financiers.
	•	Module portefeuille (profilage de risque léger, allocation générique).
	•	Stockage local pour la base documentaire et les préférences utilisateur de base.

3) Organisation du dépôt & outils
	•	Projet ouvert dans VS Code avec extensions Python, Jupyter, Git/GitHub, client API et (optionnel) Docker.
	•	Gestion de versions Git (branche principale + branches de features).
	•	Fichiers volumineux et sorties de notebooks exclus du versionnement ; secrets stockés dans un fichier d’environnement ignoré par Git.
	•	Suivi des tâches par jalons (MVP, v1, v2) et issues courtes et actionnables.

4) Données & connaissance (RAG)
	•	Dossier “knowledge” contenant des ressources d’éducation financière (glossaires, FAQ, guides ETF/indices, points de vigilance fiscaux par pays).
	•	Politique de sourcing : documents publics, fiables, datés, avec citation des sources.
	•	Processus d’indexation et de mise à jour régulière des documents.
	•	Stratégie d’évaluation : réponses ancrées sur sources, contrôle du “je ne sais pas” quand la base ne suffit pas.

5) Fonctionnalités MVP
	•	Chat Q/R avec citations des documents utilisés.
	•	Calculateurs : intérêts composés, mensualités de prêt amortissable, DCA simple.
	•	Détection d’intention basique pour router vers Q/R ou calculateurs.
	•	Santé du service : point de contrôle pour vérifier que l’API répond.
	•	Expérience : messages de garde-fou et limites explicites (juridiction, pas de stock-picking).

6) Algorithmes & logique
	•	NLU/Orchestration : règles simples puis évolution vers un petit classifieur d’intentions.
	•	RAG : index vectoriel local + recherche hybride (texte et sémantique), re-réorganisation des résultats et citations.
	•	Calculs : formules financières standards (pas de dépendance externe pour le cœur de calcul).
	•	Profilage & allocation (phase suivante) : questionnaire de risque léger → recommandation générique d’allocations par classes d’actifs ; optimisation bornée type Markowitz avec régularisation ; règles métiers (plafonds par classe, coûts, ESG optionnel).
	•	Simulation (phase suivante) : scénarios Monte Carlo pour trajectoires de portefeuille, métriques de risque (probabilité d’atteindre un objectif, VaR/CVaR, drawdown).

7) Sécurité, conformité & éthique
	•	Avertissements visibles : information générale, non-conseil, limites par pays.
	•	Confidentialité : minimisation de données, aucune donnée sensible non nécessaire, chiffrement au repos et en transit si hébergement.
	•	Audits : journaux d’usage anonymisés, traçabilité des sources pour chaque réponse.
	•	Filtrage : refus des requêtes hors périmètre (ex. signaux de trading ciblés, stratégies fiscales agressives).

8) Qualité, tests & observabilité
	•	Tests unitaires pour tous les calculateurs et points clés.
	•	Tests d’intégration pour le flux “question → réponse avec sources”.
	•	Critères de qualité : exactitude numérique, fidélité aux sources, latence, taux de réponses “je ne sais pas” approprié.
	•	Métriques : disponibilité, erreurs, temps de réponse, satisfaction utilisateur (feedback simple).

9) Roadmap & jalons

Semaine 1–2 (MVP)
	•	Base du chat, routeur d’intentions simple, 3 calculateurs, RAG local avec quelques documents.
	•	Disclaimers et page de santé du service.
	•	Tests de base et README.

Semaine 3–4 (v1)
	•	Questionnaire de risque, allocation générique (bornes, régularisation), rapport d’allocation lisible.
	•	Première simulation simple (objectifs sur horizon, distribution d’issues).
	•	Amélioration RAG (meilleur tri des passages, meilleur format de citations).

Semaine 5–6 (v2)
	•	Personnalisation légère de l’expérience (ordre de questions, préférences).
	•	Métriques de risque avancées et rapports exportables.
	•	Observabilité renforcée, tableau de bord minimal, durcissement sécurité.

10) Déploiement & exploitation
	•	Exécution locale en développement (VS Code, lancement direct).
	•	Conteneurisation (optionnelle) pour reproductibilité et déploiement simple.
	•	Gestion de configuration par variables d’environnement.
	•	Stratégie de mise à jour de la base documentaire et de redémarrage contrôlé.
	•	Procédure d’escalade : en cas de question hors périmètre, message dédié et lien vers contact humain.

11) Bonnes pratiques d’équipe
	•	Petits commits descriptifs, branches courtes, revues rapides.
	•	Tenir le README et le CHANGELOG à jour à chaque jalon.
	•	Pas de secrets dans le dépôt ; rotation des clés si exposition accidentelle.
	•	Respect des licences des ressources utilisées ; attribution des sources.
