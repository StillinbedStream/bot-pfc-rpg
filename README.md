# bot-pfc-rpg
Un bot discord pour jouer à un pierre-feuille-ciseaux RPG communautaire !


# Comment installer le bot sur sa machine

## Pré-requis

### Installer git
Il faut d'abord installer git sur sa machine. Je te conseille soit [git-scm](https://git-scm.com/downloads) soit [gitkraken](https://www.gitkraken.com/).
Pour les utilisateurs de *git-scm sur windows*, pensez bien à ajouter le chemin de git dans la variable PATH, l'installeur vous propose l'option.
Pour les utilisateurs de linux, vous pouvez utiliser la commande suivante : 
```
sudo apt-get install git
```

### Installer python 3.7.6
Tu peux installer python via ce site : [python](https://www.python.org/downloads/release/python-376/)
Pour les utilisateurs avancés sur linux, je conseille l'utilisation de [pyenv](https://amaral.northwestern.edu/resources/guides/pyenv-tutorial). Tu peux aussi tester avec une autre version de python, mais je ne te garantis pas que le bot fonctionnera.

*Petit tips : (A NE PAS UTILISER SI TU N'INSTALLES PAS PYENV)* Pour utiliser pyenv, n'oublies pas d'installer les pré-requis nécessaires : 
```
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
```


## git clone
D'abord, il faut cloner le repository sur ta machine. Pour se faire, tu peux utiliser gitkraken ou entrer la commande suivante quelque soit la version de ton OS :  
```
git clone https://github.com/StillinbedStream/bot-pfc-rpg.git
```

Tu es utilisateur Windows et ta console te dit que la commande n'existe pas ? Tu as certainement oublier d'ajouter GIT dans la variable PATH. Cherche sur google comment ajouter la variable PATH.

## Installer les dépendances
Il y a quelques dépendances nécessaires. Tu peux facilement les installer en utilisant la commande suivante : 
```
pip install -r requirements.txt
```

# Configurer le fichier .env
Le fichier .env contient l'ensemble des variables d'environnement à initialiser lors du lancement du bot. Vous devez le remplir de la manière suivante : 
```
DISCORD_TOKEN=XXXXXXXX
DISCORD_GUILD=YYYYYYYY
ID_CHANNEL=ZZZZZZZZ
```
PS : Pour le moment, ID_CHANNEL ne sert à rien mais elle sera bientôt utilisée par le bot pour les systèmes d'achievement !


## lancer le bot
Pour exécuter le bot, rien de plus simple, il suffit d'exécuter la commande suivante :
```
python run-bot.py
``` 

# Tu veux améliorer le bot toi-même ?
## Tu es débutant ?
Si tu es débutant, je te conseille de modifier quelques éléments dans le code et de relancer le bot.
Essaye de t'imprégner du code et de le comprendre petit à petit en modifiant quelques éléments. 

Aussi, tu peux essayer de créer ton propre bot pour comprendre comment discord.py fonctionne [avec ce lien](https://twitter.com/Still_In_Bed/status/1246761244843020294). 

Si tu as des questions, n'hésite pas à rejoindre le [discord](https://discordapp.com/invite/UE6DSrS) de notre communauté.

## Accède à la doc discord.py
Tu peux accéder facilement à la documentation de [discord.py](https://discordpy.readthedocs.io/en/latest/). Tu y trouveras ce qu'il te faut pour comprendre le fonction de discord.py et améliorer le code.


# Tu veux participer à l'aventure ?
Que tu sois programmeur débutant, confirmé ou que tu veuilles juste tester le bot, tu peux rejoindre l'aventure de différentes manières : ou en passant sur notre [chaine twitch](twitch.tv/stillinbed).
* Rejoins [le discord](https://discordapp.com/invite/UE6DSrS), tu pourras tester le bot et discuter avec nous !
* Passe faire un coucou sur la [chaine twitch](twitch.tv/stillinbed)


# TODO-LIST:
Voici les prochains objectifs à atteindre :
* Achivements : les utilisateurs du serveur discord seront tenus au courant dans un channel (ID_CHANNEL)
* RPG (Niveaux, Sorts) : grace à cette mise à jour, nous pourrons nous lancer des sorts pour pimenter le jeu !
* Tournoi : une version tournoi pour pouvoir passer des soirées d'enfer sur le live ! 
