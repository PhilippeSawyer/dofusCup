# dofusCup
Web scraping &amp; analyse des résultats de compétition.

--

Fonctions les plus importantes:


// Extrait les données de toutes les équipes, doit être utilisée avant n'importe quelle autre fonction.

computeCup(baseUrl) 


// Extrait les données de toutes les équipes ayant au moins x points.

computeTopCup(x, classementUrl)


// Extrait les données des X premières équipes au classement.

computePosition(X, classementUrl)  


// Enleve toutes les équipes ayant été forfait au moins une fois.

removeForfait()


// Calcule la représentation des classes/duos et trios, puis écrit les résultats dans stats.txt

writeStats()  


//  Produit le classement contenant les classes des équipes, puis écrit les résultats dans output.txt

writeOutput() 
