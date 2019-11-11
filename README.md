# dofusCup
Web scraping &amp; analyse des résultats de compétition.

--

Fonctions les plus importantes:

computeCup(baseUrl)   // Extrait les données de toutes les équipes, doit être utilisée avant n'importe quelle autre fonction.

computeTopCup(x, classementUrl)  // Extrait les données de toutes les équipes ayant au moins x points.

computePosition(X, classementUrl)  // Extrait les données des X premières équipes au classement.

removeForfait()  // Enleve toutes les équipes ayant été forfait au moins une fois.

writeStats()   // Calcule la représentation des classes/duos et trios, puis écrit les résultats dans stats.txt

writeOutput() //  Produit le classement contenant les classes des équipes, puis écrit les résultats dans output.txt
