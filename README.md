Chatbot Finance — Copilote Financier Éducatif

1. Objectif du projet

Le Chatbot Finance est un assistant conversationnel éducatif destiné à vulgariser les concepts de finance personnelle et d’investissement.
Il agit comme un copilote : il répond à des questions, effectue des calculs financiers standards (intérêts composés, mensualités de prêt, DCA), et puise dans une base de connaissances locale pour fournir des explications fiables et sourcées.

Important : le bot ne fournit aucun conseil financier personnalisé au sens réglementaire.
Il délivre uniquement des informations générales et oriente vers un humain pour les cas spécifiques.
``` bash
Chatbot_Finance/
│
├── app/
│   ├── main.py                # Point d’entrée FastAPI (serveur + routes API + templates)
│   ├── intents.py             # Détection des intentions utilisateur (calc, prêt, rag)
│   ├── tools/
│   │   └── calculators.py     # Fonctions de calcul financier (compound, loan_payment)
│   ├── rag/
│   │   └── retriever.py       # Moteur RAG : recherche sémantique dans les fichiers du dossier knowledge
│   ├── services/
│   │   └── chat.py            # Orchestrateur de logique : relie intents, calculs et RAG
│   ├── templates/
│   │   └── index.html         # Interface web du chatbot (frontend minimal)
│   └── static/
│       └── styles.css         # Styles CSS du chat
│
├── data/
│   └── knowledge/             # Documents texte/markdown servant de base de connaissance
│
├── requirements.txt           # Dépendances Python
└── README.md                  # Documentation du projet
```
3. Fonctionnement général

Le chatbot combine trois modules principaux :
- intents.py : Détection d’intention. Analyse le texte utilisateur pour déterminer s’il s’agit d’un calcul ou d’une question d’information
- tools/calculators.py : Calculs financiers. Contient les fonctions : compound() (intérêts composés) et loan_payment() (mensualités de prêt).
- rag/retriever.py : Recherche sémantique (RAG). Analyse la question et retrouve les passages pertinents dans data/knowledge/

``` bash 
Utilisateur → interface_web → FastAPI → detect_intent()
                   ↓
      ┌──────── calc:compound ────────► calcul
      │
      ├──────── calc:loan ────────────► calcul
      │
      └──────── rag (par défaut) ─────► recherche_documentaire
                   ↓
         Réponse formatée → Interface
```
4. Détail des modules et fonctions

main.py
	•	Lance le serveur FastAPI.
	•	Sert la page HTML (index.html).
	•	Gère les routes :
	•	/api/chat → réception du message utilisateur et appel au service chat_service.
	•	/health → vérifie que l’API répond.

services/chat.py
	•	Fonction clé : chat(message, history)
	•	Orchestration :
	1.	Appelle detect_intent() pour identifier le type de requête.
	2.	Route vers :
	•	compound() ou loan_payment() si c’est un calcul.
	•	answer_with_knowledge() si c’est une question.
	3.	Formate et renvoie la réponse (texte + historique).

intents.py
	•	detect_intent(text) : analyse les mots-clés (“intérêt”, “loan”, etc.).
	•	parse_params(text) : extrait les valeurs numériques du texte.
Actuellement basé sur la position, amélioration prévue pour reconnaître les unités (“%”, “$”, “ans”).

tools/calculators.py
	•	compound(principal, rate, years, n=12)
Calcule la valeur future selon la formule des intérêts composés.
	•	loan_payment(principal, rate, years, n=12)
Calcule la mensualité d’un prêt amortissable.

rag/retriever.py
	•	Initialise un index vectoriel avec SentenceTransformers.
	•	Stocke les embeddings des documents du dossier data/knowledge.
	•	answer_with_knowledge(question)
Recherche les passages les plus pertinents, retourne un extrait et les chemins de fichiers sources.

templates/index.html et static/styles.css
	•	Interface web simple (HTML + JS) :
	•	Affiche les bulles de discussion.
	•	Envoie les messages à /api/chat.
	•	CSS minimal pour une interface claire et sombre.

⸻

5. Instructions d’exécution
Prérequis
	•	Python ≥ 3.10
	•	Environnement virtuel (venv ou conda)
	•	Dépendances du fichier requirements.txt

Étapes
	1.	Cloner le dépôt
	``` bash
	git clone https://github.com/Mandchouno/Chatbot_Finance.git
	cd Chatbot_Finance
	```
	2. Créer et activer un environnement virtuel
	``` bash
	python3 -m venv .venv
	source .venv/bin/activate   # macOS/Linux
	# ou
	.venv\Scripts\activate      # Windows
	```
	3. Installer les dépendances
	``` bash
	pip install -r requirements.txt
	```
	4.	Lancer le serveur
	``` bash
	python -m app.main
	```

