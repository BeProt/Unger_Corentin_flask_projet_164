# Module 164 2023.03.25


Le "début de la fin"

Le projet consiste en une interface (HTML, FLASK, Python, etc.) et une BD MySql.

Il s’agit d’une gestion des produits de la marque BeProt, montrant les type, les categorie, le stockage dans les entrepôt de ce produits. Soit un système CRUD (Create Read Update Delete) adapté aux besoin sur les 4 tables de la BD BeProt : Soit “t_entrepot”; “t_categorie”; "t_produit"; "t_produit_stocker_entrepot". Quels sont les prérequis pour faire fonctionner mon projet ? Un serveur MySql doit être installé • Heidi SQl (Laragon) ou XAMPP ou UWAMP • MAC : MAMP ou https://www.codeur.com/tuto/creation-de-site-internet/version-mysql/

Python doit être installé. • ATTENTION : Cocher la case pour que le “PATH” intègre le programme Python • Une fois la “case à cocher” du PATH cochée, il faut choisir d’installer • Un peu avant la fin du processus d’installation, cliquer sur “disabled length limit” et cliquer sur “CLOSE” • Le test de Python se fait après avec le programme “PyCharm” Installer “GIT” • https://gitforwindows.org/ • Le test de “GIT” se fait dans le programme “PyCharm”

Configuration de PyCharm • Il faut installer “PyCharm” (community) et utiliser la même version IDE pour faire fonctionner le projet.

• Lors de l’installation, il faut cocher toutes les options ASSOCIATIONS, ADD PATH, etc

• Ouvrir “PyCharm” pour la première fois pour le configurer. Choisir le bouton “New Project”

• Changer le répertoire pour ce nouveau projet, il faut créer un nouveau répertoire “vide” sur votre disque en local.

• Il est important d’avoir sélectionné le répertoire que vous venez de créer car “PyCharm” va automatiquement créer un environnement virtuel (venv) dans ce répertoire

• Menu : File->Settings->Editor->General->Auto Import (rubrique Python) cocher “Show auto-import tooltip”

PyCharm vient d’ouvrir une fenêtre avec le contenu du “main.py” pour configurer les actions “UNDO” et “REDO”

• Sélectionner tout le texte avec “CTRL-A” puis “CTRL-X” (Couper), puis “CTL-Z” (UNDO) et faites un REDO “CTRL-Y” et “PyCharm” va vous demander de choisir l’action du “CTRL-Y” raccourci pour faire un “REDO”. Guide pour faire fonctionner le projet

Démarrer le serveur MySql (Laragon(heidi.sql), uwamp ou xamp ou mamp, etc.))

• Dans “PyCharm”, importer MA BD à partir du fichier DUMP

• Ouvrir le fichier APP_FILMS_164/database/1_ImportationDumpSql.py

• Cliquer avec le bouton droit sur l’onglet de ce fichier et choisir “run” (CTRL-MAJ-F10)

En cas d’erreurs /!
• Ouvrir le fichier .env à la racine du projet, contrôler les indications de connexion pour la bd.

Test simple de la connexion à la BD

• Ouvrir le fichier APP_FILMS_164/database/2_test_connection_bd.py

• Cliquer avec le bouton droit sur l’onglet de ce fichier et choisir “run” (CTRL-MAJ-F10)

Démarrer le microframework FLASK

• Dans le répertoire racine du projet, ouvrir le fichier run_mon_app.py

• Cliquer avec le bouton droit sur l’onglet de ce fichier et choisir “run” (CTRL-MAJ-F10)

• Dans la console du “run” il doit y avoir un lien à cliquer de cette forme :

o Running on http://127.0.0.1:5505/homepage

• Cliquer dessus afin d'ouvrir dans votre navigateur mon projet Vous voici sur le visuel de mon projet final 

https://fr.web.img6.acsta.net/pictures/18/10/31/17/34/2348073.jpg