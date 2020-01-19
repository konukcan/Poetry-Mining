
######Introduction.


L'évolution culturele est une discipline des sciences cognitives importante et en plein développement qui essaye de mettre au jour les lois de transmission et d'évolution des objets culturelles à travers les sociétés et à travers le temps. 
La recherche en évolution culturelle marche de pair avec les humanités numériques. Ces dernières consistent à exploiter l'outil informatique afin d'automatiser la recherche sur des textes mis sous forme numérique de façon à pouvoir tirer des informations de très larges bases de données historiques et/ou de textes littéraires.
La raison pour laquelle ceci est très important pour un domaine de recherche comme l'évolution culturelle est aisée à comprendre : en étant capable de traiter de façon automatique de très larges bases de données, bien plus grandes que ce qu'un lecteur individuelle aurait pu traiter, elle permette à la recherche d'aller au-delà du texte individuel ou du petit corpus de textes et d'observer des régularités à l'échelle d'une culture ou d'une période historique tout entière, ainsi que leur variaiton au cours du temps.

Etant donné que c'est le domaine de recherche dans lequel je compte me spécialiser, il est important pour moi de me familiariser avec les outils utilisés au sein des humanités numériques. Etant donné que le codage est une pratique totalement neuve pour moi, mon but pour ce semestre de formation à la programmation était avant tout de me familiariser avec les outils et modules disponibles sur Python dans le domaine de l'analyse textuelle.

J'ai fait beaucoup de tentatives dans ce sens et dans beaucoup de directions différentes. Beaucoup desdites tentatives ont été infructueuses (largement en raison de mon manque d'expérience) - je parle rapidement de ces échecs dans la dernière section de cette présentation ("Retour sur expériences"). Mais j'ai tout de même pû au bout du compte programmer deux tâches intéressantes d'analyse textuelle : premièrement un code pour extraire les fréquences relatives de mots dans des textes littéraires. Deuxièmement, identifer les émotions dominantes dans les phrases d'un texte, en se servant pour cela du lexique émotionnel **FEEL** (French Extended Emotional Lexicon) mis en place par Abdaoui *et al*.  (2014). 

J'ai travaillé pour cette recherche sur trois ouvrages poétiques majeurs du XIXe siècle français : *Les Chants de Maldoror*  de Lautréamont, *Les Fleurs du mal* de Baudelaire et les *Oeuvres complètes* de Rimbaud.
Les liens vers ces textes complets, trouvables sur internet et que j'ai utilisé pour mon analyse, ainsi que le lexique FEEL, sont disponibles dans les répositoires consacrés au sein de ce projet.

##Table des matières

#Extraire des fréquences de mots avec FreqDist ()
#Identifier des émotions dans des phrases avec le lexique FEEL
#Retours sur expérience et choses que j'ai apprises


##**Extraire des fréquences de mots avec FreqDist ()**

The first task we had to perform during this project (and that would be useful) for the two operations later to be performed on text, was to be able to extract the text from online databases.

Finding suited online texts among the databases available online was in itself not an easy task, because we had to find texts that were both large enough to be representative of the whole work of an author, importable under html format and not corrupt (not full of parsitic characters in the middle of the text - I cover all the failed attempts I had with this regard in the last section.

To perform text extraction I used two main modules:

1) the request modules form python, which allowed me to get a text from the internet.

```ruby
import requests
url = 'http://www.gutenberg.org/files/12005/12005-h/12005-h.htm'
r = requests.get(url)
r.encoding = 'utf-8'
html = r.text

```

Ici en 'url' on a mis l'url de la page Gutenberg qui renvoie au texte complet des Chants de Maldoror de Lautréamont, mais il est possible de la remplacer par une autre url pour requérir un autre texte.

Une fois ceci fait il est importer de nettoyer le texte pour le rendre propre à l'analyse, car celui-ci est bruité, en particulier par des balises html.

Pour cela on utilise le module BeautifulSoup, qui permet de sélectionner spécifiquement le texte dans un document qui mêle du texte et d'autres types de données :

```ruby

from bs4 import beautifulSoup
soup = BeautifulSoup(html, features="lxml")
text = soup.get_text()

```
Ensuite, pour éviter de bruiter l'analyse, on enlève les parties du texte qui ne font pas partie de l’œuvre et qui sont simplement des ajouts introductifs et conclusifs de la librairie Gutenberg.
Il s'agissait pour cela simplement de copier coller ces parties de textes dans une fenêtre de Jupyter pour savoir combien de lignes ils faisaient chacun, et ensuite de soustraire d'autant de lignes notre document pour n'avoir que le texte qui se trouve entre l'un et l'autre :

```ruby
#enlever l'exergue de début du texte
text_sans_préface = text[86:]
#Enlever les copyrights de fin sur la page gutenberg
text_sans_copyright = text_sans_préface[0:-370]
```

On tokenise ensuite le texte en mots en utilisant le module Regexp qui fait partie du package de nltk, étape préalable au comput de mots :

```ruby
tokenizer = nltk.tokenize.RegexpTokenizer('\w+')
tokens = tokenizer.tokenize(text_sans_copyright)
```
Puis, afin de mettre sur le même plan tous les mots et ne pas avoir de bruit dû au fait que le compteur de fréquence considère comme différents les mots qui commenceraient par une majuscule et les autres. Pour cela on place les tokens de mots isolés à l'étape précédente dans une nouvelle liste en les mettant tous en minuscule au passage, avec la méthode .lower() de nltk.

````ruby
words = [token.lower() for token in tokens]``

Avant d'utiliser la fonction freqdist( ) sur cette liste, je dois aussi éliminer tous les mots sans intérêt qui, si ils sont très fréquents, risque de brouiller l'analyse en mettant en avant des mots sans intérêt car peu chargés sémantiquement même si ils sont très fréquents. 
Pour cela je crée trois listes différentes de mots sans intérêt :

```ruby
#Liste des 'stops-words'
nltk.download('stopwords')
sw = nltk.corpus.stopwords.words('french')

#Listes d'autres mots parasites
artifacts = ["a", "i", "o", "or","h", "chants","the","of", "project","là", "l","1", "with","any", "this","work", "gutenberg","and","l", "-" "of", "to", "you", "in", "tm"]

uninteresting = ["comme", "cette", "si", "plus", "car","où",  "sans", "ni", "tout", "dont","vers", "sous", "leurs","tous" ]
```

La première est créée a priori. Il s'agit simplement de la liste des 'stopwords' du français établie par nltk. C'est-à-dire tous les mots comme les conjonctions de coordination ou les articles définis qui sont très fréquents dans un texte, tout simplement parce qu'il assurent des fonctions grammaticales importantes et pas parce qu'ils auraient un lien avec le contenu thématique du texte.

Les deux suivantes sont créées a posteriori, en faisant quelques essais de tests de fréquence et en voyant que certains mots 'parasites' s'introduisaient dans la liste des mots les plus fréquents.

La première, 'artifacts', rassemble tous les bruits dûs à l'imperfection des étapes précédentes de nettoyage de texte. Les caractères isolés, nombres ou tirets sont probablement des erreurs du tokeniser dûes à une légère corruption du texte (ou des espaces se trouvent au milieu de mots alors qu'ils ne le devraient pas) ou bien à des imperfections dans son traitement par Beautiful Soup. Pour les mots en anglais, ils s'agit des mentions de la librairie Gutenberg qui se trouve au milieu du texte, entre les chapitres ou autres et qui demeurent donc même après que l'on ait 'élagué' les extrêmités. 
L'exclusion de 'chants', même si ils s'agit en soit d'un mot pertinent, est due au fait que sa fréquence est artificiellement gonflée par le rappel du titre dans tous les débuts de pages ou chapitres des Chants de Maldoror (chant 1, strophe x, chant 2, etc.) de sorte que sa fréquence n'est pas dû tout représentative.

A noter, pour cette liste et la suivante, que je n'ai pas fait de distinction entre les mots à exclure pour un texte et pour les deux autres; tous ne présentent pas les mêmes mots 'parasites', mais comme cela simplifie les choses j'ai préféré rassembler tous les mots à exclure dans une seule et même liste, réutilisable pour les différents textes (exclure un mot d'un texte où il n'est pas présent n'étant pas un problème de toute façon). 

La deuxième liste, 'uninteresting', rassemble tous les mots qui font légitimement partie du décompte final, mais qui ne présente pas d'intérêt, pour la raison que, comme les 'stopwords', ce sont d'avantage des mots fonctionnels servant à structurer la phrase grammaticalement parlant que des mots porteurs de sens et donc indicateurs des champs lexicaux dominant dans un texte donné.

Une fois ces listes crées, je crée une nouvelle liste, 'words_clean', qui va contenir tous les mots de mon texte (en lettres minuscules), à l'exception de ceux présents dans les listes précédentes, que j'exclue en itérant sur la liste précédente, 'words', avec une boucle for :
```ruby
words_clean = []
for word in words:
    if word not in sw+artifacts+uninteresting:
                    words_clean.append(word)

```
Une fois ceci fait, il ne me reste plus qu'a effectuer la dernière étape, qui consiste à utiliser la fonction freqdist sur la liste ainsi crée puis à plotter les résultats : 

```ruby
freqdist = nltk.FreqDist(words_clean)
freqdist.plot(25)
```


Ce qui donne les résultats suivants :

Pour Baudelaire : 
![plot Baudelaire] https://github.com/konukcan/Poetry-Mining/blob/master/plot%20baudelaire.png

Pour Rimbaud :

![plot Rimbaud]https://github.com/konukcan/Poetry-Mining/blob/master/plot%20rimbaud.png


Pour Lautréamont :

![plot Lautréamont]https://github.com/konukcan/Poetry-Mining/blob/master/plot%20lautr%C3%A9amont.png

Ce que l'on peut voir sur ces graphiques c'est le fait qu'il y a une relative uniformité de la distribution entre les deux premiers auteurs, tandis que le dernier auteur se trouve à part dans une certaine distance. En quelque sorte, ceci atteste que, lexicalement parlant du moins, entre les trois auteurs les plus novateurs du XIX e siècle français, il y a une plus grande originalité dans le choix des mots chez Lautréamont qui s'écarte des tropes lexicales de la poésie classiques.

D'autre part, on peut rapidement aussi voir une plus grande présence du champ lexical se rapport au corps, dans ses dimensions anatomiques, et d'une certaine manière identifier une poésie plus incarnée chez Lautréamont que chez ses deux contemporains. 
Ceci confirme des intuitions déjà observées par certains critiques littéraires, en utilisant d'autres méthodes quantitative, qui en renforcent la certitude d'une certaine manière (voir par exemple Bachelard, 1963)


## **Identifier des émotions dans des phrases avec le lexique FEEL**


La deuxième opération que j'ai pu mettre en oeuvre consiste à extraire le sentiment de phrases du texte, en utilisant un lexique émotionnel.
J'ai utilisé le lexique FEEL, développé par Abaxxx et al. et disponible en accès libre en ligne (déposé sur GitHub). Celui-ci se compose de près de 15000 mots et expressions de la langue française, et associés à eux, une certaine polarité de sentiment et un score binaire pour six émotions : joie, peur, tristesse, colère, surprise et dégoût.

Nous avons considéré que l'analyse par pure polarité (positive ou négative), utilisée dans les 'Sentiment analysis' classique et qui fonctionne pour des  tweets ou des critiques de cinéma, n'était pas très pertinente pour analyser des textes littéraires plus complexes et nous avons décidé de nous concentrer sur les émotions un peu plus complexes distinguées par ce lexique.

De plus, le score binaire donné par cette liste permettait de les additionner pour a voir des scores globaux à l'échelle de la phrase. 

La stratégie adopté a donc été la suivante:

itérer une boucle sur chaque phrase, qui considèrerait chaque mot à l'intérieur de ladite phrase pour, si celui-ci se trouve dans le lexique émotionnel FEEL, ajouter son score pour chacune des six émotions prises en compte au score global de la phrase, ce qui permet de donner un aperçu instantané des 'grandes tendances' émotionnelles dans chacune des phrases d'un passage de telle ou telle oeuvre;

Nous n'avons pas cherché à additionner ces scores à l'échelle des oeuvres entières ou de chapitres, ce qui n'aurait pas eu de sens étant donné qu'elles sont de longueur inégale (une oeuvre plus longue étant destinée à avoir a priori des scores plus élevés pour toutes les émotions, sans que cela renseigne quoi que ce soit sur son contenu réel).
Nous n'avons pas non plus cherché à faire des moyennes à l'échelle de l'oeuvre, car celle-ci aurait été très facilement faussée par la présence plus ou moins grande de phrases ayant de très faibles valences émotionnelles, ou tout simplement des scores de 0 (notamment les phrases très courtes, beaucoup plus présente dans des vers très réguliers comme ceux des Fleurs du Mal que dans la poésie de Rimbaud ou dans la prose emphatique de Lautréamont).

Ce que cet outil doit permettre, c'est avant tout de sélectionner un passage du texte choisi et d'avoir en un seul 'print' un aperçu immédiat des émotions dominantes dans ledit passage.

Le code et les étapes que j'ai utilisées sont les suivantes :

Premièrement, une importation et un nettoyage du texte, qui est le même que dans le code précédent pour les fréquences de mots :
```ruby

import requests
from bs4 import BeautifulSoup
import nltk

url = 'https://archive.org/stream/leschantsdemaldo00laut/leschantsdemaldo00laut_djvu.txt'

r = requests.get(url)
r.encoding = 'utf-8'
html = r.text

soup = BeautifulSoup(html, features="lxml")
text = soup.get_text()

#enlever l'exergue de début du texte
text_sans_préface = text[86:]
#Enlever les copyrights de fin sur la page gutenberg
text_sans_copyright = text_sans_préface[0:-370]
```

Ensuite, rendre le lexique FEEL utilisable pour mon analyse:

Premièrement, en le mettant sous forme de DataFrame avec pandas :
```ruby
file = 'FEEL.csv'
feel_data = pd.read_csv(file)
feely_data = pd.DataFrame(feel_data)

```

Deuxièmement, en créant un dictionnaire qui ne retient que les deux valeurs qui nous intéresse, associées l'une à l'autre : les mots, situés dans la colonne 'word' du DataFrame, qui seront les keys du dictionnaire  ; les 6 valences émotionnelles respectivement associées à chaque mot, qui sont situées dans les colonnes 3 à 10. Ce qui donne :

```ruby
feely_dict = {}

for index, row in feely_data.iterrows():
    feely_dict[row['word']] = list(row[3:10])

```

Une fois ceci fait, je split le texte ainsi obtenu à l'échelle de la phrase en utilisant la fonction .split() :
```ruby
sentences = text.split(".")
```
Puis je vais créer une boucle qui va itérer sur chaque phrase du texte pour créer un array associé à cette phrase, puis sur chaque mot de la phrase de telle façon que pour chacun des mots se trouvant dans le dictionnaire précédemment crée, les valeurs pour les 6 émotions distinguées lui étant associées s'ajoutent à l'array de cette phrase en s'additionnant. On ajoutera
ensuite les suites de phrases et leurs scores respectifs à un array plus large qui contiendra les valeurs pour toutes les phrases du texte. Soit en tout :
```ruby
sentences_and_scores = []

for sent in sentences:
    array = []
    for mot in sent.split():
        if mot in feely_dict:
           array.append(feely_dict.get(mot))
    sentences_and_scores.append(sent)
    sentences_and_scores.append([sum(i) for i in zip(*array)])

```
Ce code permet de mettre à la suite l'un de l'autre, dans l'array sentences_and_scores ainsi constitué, les phrases du texte et leur score global.

Ceci une fois fait, il ne reste plus qu'à faire une boucle d'impression sur les éléments de la liste en insérant entre chaque élément des séparateurs/ passage à la ligne pour plus de clarté et de lisibilité :

```ruby
for element in sentences_and_scores[n:n+x]:
    print("::: \n")
    print(stuff)
```


En connaissant à peu près l'ordre du texte, on peut aller chercher un passage qui nous intéresse pour savoir quelle est l'émotion dominante dans cette partie de l'oeuvre.

Par exemple, en allant chercher du texte au hasard au milieu des Chants de Maldoror en prenant comme index au début de la boucle  ' for element in sentences_and_scores[550:600]', on obtient un output qui a cette forme :


``````

 Et, quand je r�de
autour des habitations des hommes, pendant les nuits orageuses, les yeux
ardents, les cheveux flagell�s par le vent des temp�tes, isol� comme une
pierre au milieu du chemin, je couvre ma face fl�trie, avec un morceau
de velours, noir comme la suie qui remplit l'int�rieur des chemin�es: il
ne faut pas que les yeux soient t�moins de la laideur que l'�tre supr�me,
avec un sourire de haine puissante, a mise sur moi
::: 

[1, 3, 3, 4, 0, 5]
::: 

 Chaque matin, quand
le soleil se l�ve pour les autres, en r�pandant la joie et la chaleur
salutaires dans la nature, tandis qu'aucun de mes traits ne bouge, en
regardant fixement l'espace plein de t�n�bres, accroupi vers le fond de
ma caverne aim�e, dans un d�sespoir qui m'enivre comme le vin, je meurtris
de mes puissantes mains ma poitrine en lambeaux
::: 

[1, 2, 1, 1, 1, 0]
::: 

 Pourtant, je sens que je
ne suis pas atteint de la rage! Pourtant, je sens que je ne suis pas le
seul qui souffre! Pourtant, je sens que je respire! Comme un condamn� qui
essaie ses muscles, en r�fl�chissant sur leur sort, et qui va bient�t
monter � l'�chafaud, debout, sur mon lit de paille, les yeux ferm�s, je
tourne lentement mon col de droite � gauche, de gauche � droite, pendant
des heures enti�res; je ne tombe pas raide mort
::: 

[0, 4, 4, 1, 0, 3]


`````

Ce qui se lit de la manière suivante : 


Ces phrases de façon générale on un très faible score pour l'émotion 'joie' (entre 0 et 1),  mais un score plus élevé pour les émotions suivantes dans la liste : peur, tristesse, colère (entre 1 et 4 selon les cas, avec des valeurs constamment hautes notamment pour la première et la troisième. 
On observe aussi qu'elles ont des valeurs très constrastées d'une phrase à la suivante pour l'émotion 'dégoût', allant de très fort (5, pour la première) à très faible (0 pour la seconde), pour des phrases qui pourtant sont de longueur comparable et se suivent dans le texte.

Ceci permet donc d'avoir une idée certes imprécise mais très rapide ( au simple coup d'oeil) des émotions à l'oeuvre dans un passage de texte, apportant ainsi un outil intéressant à l'analyse textuelle en complément de la lecture attentive et normale.


##**Retour sur expérience et choses que j'ai apprises**


Cette expérience de programmation a été dans l'ensemble très bénéfique. 
L'expérience la plus agréable a été de voir que certaines choses en termes d'analyse de texte qui me semblaient de prime abord très compliquées et irréalisables pour quelqu'un qui n'a jamais codé auparavant s'avéraient à l'essai faisables à force de recherche, de demande de conseils et d'essais/erreurs.
J'ai tout de même eu quelques frustrations au cours de ce travail, la principale ayant été de ne pas avoir réussi à lemmatiser le texte pour augmenter la pertinence des résultats, à la fois de l'analyse de fréquence et de l'analyse des émotions. La raison en est d'une part que presque tous les lemmatiseurs et bases de données disponibles en open source sont fait pour l'anglais ; d'autre part que les deux lemmatiseurs que j'ai pu trouver qui acceptaient le français, Spacy et TreeTagger n'ont pas été utilisable, le premier parce qu'il n'accepte que des strings en inputs et ne fonctionne pas sur des listes (et en dépit de maints essais et demandes de conseils, je n'ai pas réussi à résoudre le problème en itérant sur une liste de strings, notamment en raison du fait qu'il faut d'abord faire un parsing de la syntaxe avant de pouvoir lemmatiser dans Spacy). Quant à TreeTagger, je n'ai tout simplement pas réussi à l'installer, le problème étant certainement dû d'une façon ou d'une autre à mon ordinateur car tout se passait de façon bien différente sur des ordinateurs de tiers/amis.

En dépit du fait que nous avions eu moins de préparation en amont que l'année dernière, cette expérience de programmation ce semestre a tout de même été très agréable et donnait une bonne introduction au code qui m'a donné confiance dans ma capacité à réutilisé cet outil dans le cadre de mes travaux de recherche ultérieurs.
