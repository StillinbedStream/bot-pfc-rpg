
from PFCBot.messages.message import Message

class Help(Message):
    def __init__(self, channel=None):
        self.content = "\n".join([
            "T'es nouveau, si tu veux jouer, fais ces commandes :",
            "`!register [pseudo]` : enregistre toi avec un pseudo",
            "`!players` : liste les joueurs",
            "`!attack [pseudo du joueur]` : attaque la personne ayant le pseudo fourni",
            "",
            "**Note pour jouer :** quand tu reçois une attaque, réponds par pierre, feuille ou ciseaux",
            "",
            "Commandes de base pour jouer : ",
            "`!help` : message d'aide avec la liste des commandes",
            "`!register [pseudo]` : s'enregistrer avec le pseudo donné",
            "`!attack [pseudo du joueur]` : attaquer le joueur avec le pseudo donné",
            "`!next-fights` : affiche la liste de nos combats en cours.",
            "`pierre`, `feuille`, ou `ciseaux` : donner son choix au prochain combat",
            "",
            "",
            "Liste des commandes en plus :",
            "`!help` : message d'aide avec la liste des commandes",
            "`!players` : liste les noms des joueurs",
            "`!show-actifs` : Liste tous les joueurs actifs",
            "`!mystats` : voir mes statistiques",
            "`!current-fights` : liste les combats en cours",
            "`!ranking` : liste le classement des joueurs avec leurs points",
            "`!actif` : vous met en mode actif, vous pouvez être attaqué et attaquer à nouveau",
            "`!passif` : vous met en mode passif, vous ne pouvez plus attaquer et être attaqué",
            "`!cancel` : supprime le combat en cours, n'en abuse pas s'il te plaît.",
            "",
            "PS : J'ai soif de boire https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHHzo3NXvZN2D63gbYVvpzWJ9lyk4gC6v3mheuGX-XeOc-FRe5&s"
        ])
        self.channel = channel
