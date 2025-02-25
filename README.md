Fonctionnalités :
-  Chiffrement AES :  Utilisation de l'algorithme AES pour sécuriser les fichiers avec un mot de passe et un sel généré aléatoirement.
-  Déchiffrement AES : Permet de déchiffrer les fichiers protégés avec AES en utilisant le mot de passe correct.
-  PBKDF2 Key Derivation : Utilisation de PBKDF2 avec HMAC-SHA256 pour dériver une clé de chiffrement sécurisée à partir d'un mot de passe.
-  Stockage sécurisé du sel et IV.
-  Interface en ligne de commande simple et efficace.
-  Gestion de la configuration : Sauvegarde des paramètres de configuration (chemin, nom de fichier, etc.) dans un fichier de configuration (confg.ini).
-  Génération d’un exécutable .exe avec PyInstaller
-  Sécurisation des mots de passe : Les mots de passe sont stockés de manière sécurisée grâce à l'usage de getpass pour éviter l'affichage en clair.

Technologies :
-  Python 3 : Ce projet est écrit en Python 3, avec une utilisation de bibliothèques associées.
-  Cryptography : Utilisation de la bibliothèque Python cryptography pour la gestion des algorithmes de chiffrement.
-  PyInstaller (pour la conversion en .exe)
-  ConfigParser (pour la gestion de configuration)

Prérequis :
-  Python 3.x
-  Bibliothèque cryptography → Installez avec : pip install cryptography

Création executable (.exe) :
-  Installez PyInstaller → pip install pyinstaller
-  Générer l’exécutable → pyinstaller --onefile --icon=icon.ico script.py
     --onefile : Génère un seul fichier .exe
     --icon=icon.ico : Permet d’ajouter une icône personnalisée (optionnel)
-  Exécuter l’application : Allez dans le dossier dist/ → script.exe
