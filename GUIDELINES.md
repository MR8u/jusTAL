
## Structure des PVs

Nous avons volontairement supprimer le paramètre n (e. g. \<div3 question n="1" \>). Tel que nous l'utilisions jusqu'à présent, celà revient a dénombré le nombre d'element enfant d'un élement parent (exemple 3 question dans une séance), c'est quelque choses que l'on peut faire automatiquement très simplement et qui nous pensons qu'il n'est pas tellement nécéssaire de le précisé.

Nous avons laissez la div4 pv.seance.question.conclusion même si elle n'est actuellement pas utilisé. Nous estimons qu'elle pourrait être utile par la suite.

```xml
<div1 type="pv" corresp="#pv">
    <div2 type="seance" corresp="#date?(_[a-z])">
        <div3 type="ouverture">
            <div4 type="membrePresent"></div4>
            <div4 type="ordreDuJour"></div4>
        </div3>
        <div3 type="question" corresp="#decision">
            <div4 type="introduction"></div4>
            <div4 type="rapport"></div4>
            <div4 type="discussion"></div4>
            <div4 type="conclusion"></div4>
        </div3>
        <div3 type="cloture"></div3>
    </div2>
</div1>
```

- "#pv" représente l'identifiant du pv de ce fichier. Ex : 
    - #PV1982-01-05
- "#date?(_[a-z])" représente la date de la séance suivi optionellement d'une lettre si plusieurs séance on eu lieu à la même date. Ex : 
    - 1 séance a cette date : "#1982-01-05"
    - 2 séances a cette date :  "#1982-01-05_a", "#1982-01-05_b"
- "#decision" l'identifiant de la décision traiter dans la balise. Ex
    - #DC-81-134

## Writing et Utterance

Pour réprensenter le contenu d'un élément de structure (ouverture, rapport, discussion ...) nous utilisons soit la balise \<u\> soit la balise \<writing\>. Il est a se stade encore difficile de définir clairement l'une et l'autre mais pour résumer :

- La balise \<u\> doit être utiliser pour réprésenter les élements de dialogues direct entre les conseillers.

- La balise \<writing\> doit être utiliser pour représenter le reste des élements : les parties d'une rapport, les notes de transcriptions ...

Le texte a l'interieur des deux balises est représenté a l'aide de balise \<seg\>.

L'intervenant doit être renseigné par le paramètre @who et il peut prendre plusieurs valeurs :

- Un ou plusieurs identifiant de conseiller, lorsque ceux-ci que la transcription regroupe plusieurs prise de parole en une seul. Les identifiantes doivent alors être séparé par un espace Ex :
    - "#vedel_george" ou "#vedel_george #frey_roger"
- Le raccourcis "#president" lorsqu'il est question du président du conseil. Cela permets de gagner du temps lorsque l'on a un doute sur l'identité de celui-ci durant la séance. Le bonne identifiant sera remis lors de l'automatisation. 
- le raccourcis "#all" lorsqu'il est question de l'ensemble des conseillers présent durant la séance.
- Aucune valeur lorsque l'intervenant n'est pas clairement identifier ou pour des notes de transcriptions. Le paramètre @who est alors retirer.


```xml
<writing who="#segalat_andre">
    <seg></seg>
</writing>
<u who="#vedel_george">
    <seg>...</seg>
    <seg>...</seg>
</u>
<writing>
    <seg>...</seg>
</writing>
<u who="#vedel_george #frey_roger">
    <seg>...</seg>
    <seg>...</seg>
</u>
<u who="#all">
    <seg>...</seg>
    <seg>...</seg>
</u>
```

Il faudra ajouter par la suite la balise \<floatingText\> ici.

## Incident et Pause

La balise \<incident\> peut être utilisé pour représenter trois cas : 
- Les éléments inhabituel au cours d'une séance, comme la sortie d'un conseillé ou (manque d'exemple pour le moment)
- Les problèmes lié directement a la transcription qui perturbe le modèle que nous avons établis. La balise sert alors a isoler les élements pour éviter qu'il perturbe les différents scripts d'automatisation.
-  les différentes pauses au cours d'une séance. 
    - Nous voulions utiliser la balise \<pause\> mais après vérification elle ne peut contenir ni texte ni autres balise. 
    - Attention : Les changements de séance ne sont pas considéré comme des pauses. Un bon moyen de différencier les deux est que lors d'une pause le séance est généralement "suspendue" alors qu'elle est "levée" lors d'un changement.

Les elements contenu dans la balise \<incident\> doivent être représenter par une balise \<desc\>.

Pour le moment cette balise fait l'affaire mais nous avons quand même deux remarques:
    - \<incident\> ne permets pas d'inclure une balise \<u\> ou même \<writing\>. Dans le cas de Vedel qui quitte la séance a cause de l'article du journal Le Monde (PV1982-11-18), Vedel prend clairement la parole et c'est dommage de perdre l'information.
    - Il faudrait pouvoir différencier les deux cas d'usages. Nous pensons pouvoir a terme trouver une balise plus approprier pour les problèmes liées directement a la transcription.

```xml
<incident>
    <desc><hi rend="underline">Monsieur VEDEL</hi> demande au Président de bien vouloir l'excuser. Il souhaite, en effet, se retirer ayant, comme chacun le sait, dans un article du 3 février 1979, paru dans le journal "Le Monde", pris position sur la question essentielle qu'aura à connaître le Conseil c'est-à-dire l'obligation de mixité.</desc>
    <desc>Cet article ne peut être assimilé à une chronique de droit, même s'il ne présente pas un caractère polémique. Ne voulant pas être dans la position de "Barbe molle", avocat cher à Courteline, qui est tantôt juge, tantôt avocat, Monsieur VEDEL préfère se retirer.</desc>
</incident>

<incident>
    <desc>La séance est suspendue à 13 heures et reprise à 15 heures.</desc>
</incident>
```

## Vote

Le vote est représenter par une balise \<span\> et un paramètre @type="vote". Il est essentiel que le vote soit contenu dans une balise seg d'une balise \<u\> ou \<writing\> mais ce n'est pas impossible par la suite et cela ne pause aucun problème. 

Même remarque que plus haut pour le paramètre @n.

```xml
<writing>
    <seg><span type="vote">Le projet est adopté à l'unanimité par les membres du Conseil.</span></seg>
</writing>

<u who="#vedel_george">
    <seg><hi rend="underline">Monsieur le Président</hi> remercie Monsieur SEGALAT pour ...</seg>
    <seg> Aucune observation n'étant présentée Monsieur le Président soumet le projet de décision de Monsieur SEGALAT au vote du Conseil. <span type="vote">Ce projet est adopté à l'unanimité.</span></seg>
</u>

```

# Titres et Soulignement

Les titres qui structures le rapport et qui sont représenter dans les transcription par des \<h1\>, \<h2\>, \<h3\> ... doivent être représenter avec la balise \<hi\> et le paramètre @style="titreN" où N représente la hierarchie du titre.

Le texte souligné qui est représenter dans les transcription par la balise \<u\> doit être représenter avec la balise \<hi\> et le paramètre @rend="underline".

```xml
<hi style="titre2"></hi>

<hi rend="underline">Monsieur le Président</hi>
```

## Raccourcis pour l'autocomplétion

```xml
<!-- #abadie_georges #ameller_michel #antonini_jules #auriol_vincent #badinter_robert #barrot_jacques #bazy-malaurie_claire #belloubet_nicole #brouillet_rene #cabannes_jean #canivet_guy #cassin_rene #charasse_michel #chatenay_victor #chatenet_pierre #chenot_bernard #chirac_jacques #colliard_jean-claude #coste-floret_paul #coty_rene #dailly_etienne #de-guillenchmidt_jacqueline #debre_jean-louis #delepine_maurice #denoix-de-saint-marc_renaud #deschamps_andre #dubois_georges-leon #dumas_roland #dutheillet-de-lamothe_olivier #fabius_laurent #fabre_robert #faure_maurice #frey_roger #gilbert-jules_jean #giscard-d-estaing_valery #goguel_francois #gourault_jacqueline #gros_louis #guena_yves #haenel_hubert #hyest_jean-jacques #jospin_lionel #joxe_louis #joxe_pierre #jozeau-marigne_leon #juppe_alain #lancelot_alain #latscha_jacques #le-coq-de-kerland_charles #lecourt_robert #legatte_paul #lenoir_noelle #lottin_dominique #luchaire_francois #luquiens_corinne #maestracci_nicole #malbec_veronique #marcilhacy_pierre #mayer_daniel #mazeaud_pierre #mezard_jacques #michard-pellissier_jean #michelet_edmond #mollet-vieville_francis #monnerville_gaston #monnet_henri #noel_leon #palewski_gaston #pasteur-vallery-radot_louis #patin_maurice #pelletier_monique #peretti_achille #pezant_jean-louis #pillet_francois #pinault_michel #pompidou_georges #rey_henri #robert_jacques #rudloff_marcel #sainteny_jean #sarkozy_nicolas #schnapper_dominique #segalat_andre #seners_francois #simonnet_maurice-rene #steinmetz_pierre #vedel_georges #veil_simone #waline_marcel -->

<!-- #PV1958-11-22 #PV1958-12-13 #PV1959-01-08 #PV1959-03-18 #PV1959-03-21 #PV1959-05-14 #PV1959-06-24-25 #PV1959-07-24 #PV1959-11-27 #PV1960-01-15 #PV1960-01-29 #PV1960-04-07 #PV1960-05-12 #PV1960-07-08 #PV1960-08-11 #PV1960-10-10 #PV1960-10-14 #PV1960-11-18 #PV1960-12-17 #PV1960-12-20 #PV1960-12-23 #PV1961-01-14 #PV1961-01-20 #PV1961-02-17 #PV1961-04-23 #PV1961-05-03 #PV1961-05-30 #PV1961-06-30 #PV1961-07-18 #PV1961-07-28 #PV1961-09-08 #PV1961-09-14 #PV1961-10-04 #PV1961-10-18 #PV1961-12-22 #PV1962-01-16 #PV1962-03-25 #PV1962-04-03 #PV1962-04-13 #PV1962-05-09 #PV1962-07-10 #PV1962-07-31 #PV1962-10-15 #PV1962-11-06 #PV1962-12-04 #PV1963-02-19 #PV1963-03-12 #PV1963-06-11 #PV1963-07-09 #PV1963-07-30 #PV1963-10-04 #PV1963-12-20 #PV1964-01-21 #PV1964-03-17 #PV1964-05-12 #PV1964-05-22 #PV1964-06-11 #PV1964-07-30 #PV1964-09-17 #PV1964-10-15 #PV1964-12-18 #PV1964-12-21 #PV1965-02-09 #PV1965-07-02 #PV1965-10-14 #PV1965-11-18 #PV1965-11-30 #PV1965-12-05-06-07 #PV1965-12-09 #PV1965-12-14 #PV1965-12-19-20-21-22-28 #PV1966-03-10 #PV1966-07-08 #PV1966-10-13 #PV1966-11-17 #PV1966-12-21 #PV1967-01-26 #PV1967-02-27 #PV1967-05-09 #PV1967-05-11 #PV1967-07-12 #PV1967-10-18 #PV1967-12-12 #PV1968-01-30 #PV1968-04-04 #PV1968-06-06 #PV1968-07-26 #PV1968-10-11 #PV1968-11-27 #PV1969-02-27 #PV1969-04-27-28-29 #PV1969-05-02 #PV1969-05-14-15 #PV1969-05-17 #PV1969-05-21 #PV1969-06-01-03 #PV1969-06-05 #PV1969-06-10 #PV1969-06-13-15-17-18-19 #PV1969-06-26 #PV1969-07-09 #PV1969-10-14 #PV1969-10-24 #PV1969-11-20 #PV1970-01-15 #PV1970-02-23 #PV1970-05-21 #PV1970-06-19 #PV1970-07-09 #PV1970-10-09 #PV1970-11-13 #PV1970-12-17 #PV1970-12-30 #PV1971-04-01 #PV1971-04-23 #PV1971-05-18 #PV1971-06-17 #PV1971-07-16 #PV1971-10-15 #PV1972-01-20 #PV1972-02-29 #PV1972-04-28 #PV1972-06-28 #PV1972-10-12 #PV1972-11-08 #PV1972-12-21 #PV1973-02-20 #PV1973-05-17 #PV1973-07-05 #PV1973-07-11 #PV1973-10-11 #PV1973-11-07 #PV1973-11-28 #PV1973-12-19 #PV1973-12-27 #PV1974-04-03 #PV1974-04-18 #PV1974-04-21 #PV1974-04-25 #PV1974-05-07 #PV1974-05-09 #PV1974-05-19-22-23-24 #PV1974-05-21 #PV1974-10-03 #PV1974-12-23 #PV1974-12-30 #PV1975-01-14-15 #PV1975-04-17 #PV1975-05-15 #PV1975-07-23 #PV1975-10-02 #PV1975-11-19 #PV1975-12-30 #PV1976-01-28 #PV1976-03-03 #PV1976-06-02 #PV1976-06-14 #PV1976-07-06 #PV1976-07-15 #PV1976-10-06 #PV1976-11-08 #PV1976-12-02 #PV1976-12-20 #PV1976-12-28 #PV1976-12-29-30 #PV1977-01-12 #PV1977-02-15 #PV1977-04-27 #PV1977-06-07 #PV1977-07-05 #PV1977-07-20 #PV1977-10-18 #PV1977-11-03 #PV1977-11-16 #PV1977-11-23 #PV1977-12-30 #PV1978-01-18 #PV1978-04-27 #PV1978-04-29 #PV1978-05-10 #PV1978-05-31 #PV1978-06-14 #PV1978-07-27 #PV1978-10-05 #PV1978-11-22 #PV1978-12-29 #PV1979-01-17 #PV1979-02-22 #PV1979-04-26 #PV1979-05-23 #PV1979-05-30 #PV1979-07-12 #PV1979-07-25 #PV1979-09-13 #PV1979-10-10 #PV1979-11-21 #PV1979-12-24 #PV1979-12-30 #PV1980-01-09 #PV1980-05-06 #PV1980-05-14 #PV1980-06-17 #PV1980-07-01 #PV1980-07-17 #PV1980-07-22 #PV1980-10-15 #PV1980-10-24 #PV1980-10-29 #PV1980-12-02 #PV1980-12-19 #PV1980-12-30 #PV1981-01-19-20 #PV1981-01-21 #PV1981-02-24 #PV1981-03-09 #PV1981-03-19 #PV1981-03-31 #PV1981-04-09 #PV1981-04-10 #PV1981-04-11 #PV1981-04-29 #PV1981-05-13-14-15 #PV1981-06-11 #PV1981-07-10 #PV1981-10-09 #PV1981-10-30-31 #PV1981-12-12-21_1982-01-06-07-08-09-11-15-16 #PV1981-12-16 #PV1981-12-30 #PV1981-12-31 #PV1982-01-05 #PV1982-02-11 #PV1982-02-18-23 #PV1982-02-24-25 #PV1982-03-25 #PV1982-04-16-20 #PV1982-06-23 #PV1982-06-28 #PV1982-07-27 #PV1982-07-30 #PV1982-10-12 #PV1982-10-22 #PV1982-11-10 #PV1982-11-18 #PV1982-11-26 #PV1982-12-02 #PV1982-12-14 #PV1982-12-28 #PV1982-12-29 #PV1982-12-30 #PV1983-01-12 #PV1983-01-14 #PV1983-03-24 #PV1983-04-25 #PV1983-05-28 #PV1983-06-15 #PV1983-07-19 #PV1983-07-20 #PV1983-10-12 #PV1983-12-14 #PV1983-12-29 #PV1984-01-19-20 #PV1984-02-28 #PV1984-06-04 #PV1984-06-18 #PV1984-07-25-26 #PV1984-08-30 #PV1984-09-12 #PV1984-10-10-11 #PV1984-12-29 #PV1985-01-18 #PV1985-01-25 #PV1985-05-22 #PV1985-06-26 #PV1985-07-10 #PV1985-07-17 #PV1985-07-24 #PV1985-08-08 #PV1985-08-23 #PV1985-10-09 #PV1985-11-13 #PV1985-12-13 #PV1985-12-28 #PV1986-01-16 #PV1986-03-05 #PV1986-03-19 #PV1986-04-01 #PV1986-04-16 #PV1986-04-25 #PV1986-06-03 #PV1986-06-25-26 #PV1986-07-01-02 #PV1986-07-03 #PV1986-07-29 #PV1986-08-12 #PV1986-08-26 #PV1986-09-02-03 #PV1986-09-18 #PV1986-10-24 #PV1986-11-17-18 #PV1986-12-02 #PV1986-12-22 #PV1986-12-29 #PV1987-01-06 #PV1987-01-22-23 #PV1987-02-20 #PV1987-03-17 #PV1987-05-05 #PV1987-06-02 #PV1987-06-26 #PV1987-07-07 #PV1987-07-22 #PV1987-07-28 #PV1987-09-23 #PV1987-10-05 #PV1987-11-24 #PV1987-12-01 #PV1987-12-28 #PV1987-12-30 #PV1988-01-05 #PV1988-01-07 #PV1988-01-19 #PV1988-02-23 #PV1988-03-10 #PV1988-03-22 #PV1988-04-06 #PV1988-04-07 #PV1988-04-12 #PV1988-04-26-27 #PV1988-04-28 #PV1988-05-03 #PV1988-05-10 #PV1988-05-11 #PV1988-06-04 #PV1988-07-13-14 #PV1988-07-20 #PV1988-07-21 #PV1988-10-05 #PV1988-10-18 #PV1988-10-25 #PV1988-11-09 #PV1988-12-06 #PV1988-12-20 #PV1988-12-29 #PV1989-01-12 #PV1989-01-17-18 #PV1989-02-01 #PV1989-05-11 #PV1989-06-07 #PV1989-07-04 #PV1989-07-08 #PV1989-07-25 #PV1989-07-26 #PV1989-07-28 #PV1989-10-11 #PV1989-10-24 #PV1989-11-07 #PV1989-12-05 #PV1989-12-28-29 #PV1990-01-09 #PV1990-01-11 #PV1990-01-22 #PV1990-03-06 #PV1990-05-04 #PV1990-05-29 #PV1990-06-06 #PV1990-07-05 #PV1990-07-25 #PV1990-10-02 #PV1990-11-07 #PV1990-12-06 #PV1990-12-27 #PV1990-12-28 #PV1991-01-08 #PV1991-01-16 #PV1991-03-12 #PV1991-04-11 #PV1991-05-06 #PV1991-05-07-08-09 #PV1991-05-23 #PV1991-06-13 #PV1991-07-09 #PV1991-07-23 #PV1991-07-24 #PV1991-07-25 #PV1991-07-29 #PV1991-08-02 #PV1991-10-01 #PV1991-11-20 #PV1991-12-19 #PV1991-12-30 #PV1992-01-15 #PV1992-02-21 #PV1992-02-25 #PV1992-04-07-08-09 #PV1992-06-09 #PV1992-07-07 #PV1992-07-28 #PV1992-07-29 #PV1992-09-02 #PV1992-09-15 #PV1992-09-18 #PV1992-09-22-23 #PV1992-10-06 #PV1992-12-08 #PV1992-12-17 #PV1992-12-29 #PV1993-01-05 #PV1993-01-06 #PV1993-01-07 #PV1993-01-12 #PV1993-01-19-20 #PV1993-01-21 #PV1993-04-06 #PV1993-06-21 #PV1993-06-30 #PV1993-07-20 #PV1993-07-28 #PV1993-08-03 #PV1993-08-05 #PV1993-08-11 #PV1993-08-12-13 #PV1993-09-22 #PV1993-11-04 #PV1993-11-19 #PV1993-12-16 #PV1993-12-17 #PV1993-12-29 #PV1994-01-13 #PV1994-01-20 #PV1994-01-21 #PV1994-01-27 #PV1994-03-08-10 #PV1994-03-29 #PV1994-05-31 #PV1994-06-07 #PV1994-06-14 #PV1994-07-06 #PV1994-07-07 #PV1994-07-21 #PV1994-07-26-27 #PV1994-07-29 #PV1994-08-03 #PV1994-10-11 #PV1994-11-03 #PV1994-12-20 #PV1994-12-29 #PV1995-01-10 #PV1995-01-11 #PV1995-01-17-18 #PV1995-01-19 #PV1995-01-25 #PV1995-01-26 #PV1995-02-02 #PV1995-02-08 #PV1995-02-15 #PV1995-03-08 #PV1995-03-09 #PV1995-04-05 #PV1995-04-06 #PV1995-04-09 #PV1995-04-12 #PV1995-04-26 #PV1995-04-27 #PV1995-05-12 #PV1995-06-08 #PV1995-06-28 #PV1995-07-12 #PV1995-07-27 #PV1995-09-14 #PV1995-10-05 #PV1995-10-11 #PV1995-11-08 #PV1995-11-29 #PV1995-12-08 #PV1995-12-15 #PV1995-12-28 #PV1995-12-29 #PV1995-12-30 -->

<!-- #ORGA-58-1 #PDR-58-1 #PDR-59-2 #ORGA-59-2 #ORGA-59-3 #DC-59-1 #ORGA-59-4 #DC-59-2 #DC-59-3 #DC-59-4 #FNR-59-1 #L-59-1 #DC-60-6 #DC-59-5 #L-60-3 #L-60-2 #L-60-4 #L-60-5 #D-60-1 #L-60-6 #L-60-7 #DC-60-7 #DC-60-8 #ORGA-59-5 #L-60-9 #ORGA-60-6 #L-60-8 #DC-60-9 #REF-60-1 #DC-60-10 #L-60-10 #REF-60-2 #REF-60-3 #REF-61-4 #DC-60-11 #L-61-11 #L-61-12 #AR16-61-1 #L-61-13 #DC-61-12 #FNR-61-2 #D-61-2 #L-61-14 #L-61-15 #DC-61-13 #DC-61-14 #FNR-61-3 #AUTR-61-1 #ORGA-61-7 #FNR-61-4 #L-61-16 #DC-61-15 #DC-61-16 #L-61-17 #L-62-18 #REF-62-5 #REF-62-6 #L-62-19 #REF-62-7 #ORGA-62-8 #DC-62-17 #DC-62-18 #DC-62-19 #ORGA-62-9 #REF-62-8 #DC-62-20 #REF-62-9 #L-62-21 #L-62-20 #L-63-22 #L-63-23 #DC-63-21 #DC-63-22 #L-63-24 #DC-63-23 #ORGA-63-10 #DC-63-24 #DC-63-25 #D-64-3 #L-64-27 #L-64-28 #L-64-29 #FNR-64-6 #FNR-63-5 #L-63-25 #L-63-26 #L-64-30 #DC-64-26 #ORGA-64-11 #DC-64-27 #L-64-31 #L-64-32 #L-65-33 #L-65-34 #L-65-35 #ORGA-65-12 #PDR-65-3 #PDR-65-4 #PDR-65-5 #PDR-65-6 #PDR-65-7 #PDR-65-8 #PDR-65-9 #PDR-65-10 #PDR-65-11 #L-66-36 #L-66-38 #L-66-37 #I-66-1 #DC-66-29 #DC-66-30 #DC-66-28 #L-66-39 #L-66-40 #L-66-41 #ORGA-66-13 #L-66-42 #FNR-66-7 #L-67-43 #DC-67-31 #L-67-44 #L-67-45 #DC-67-32 #DC-67-33 #DC-67-34 #L-67-46 #ORGA-67-14 #L-67-47 #L-67-48 #L-67-49 #DC-68-35 #L-68-50 #L-68-51 #DC-68-36 #ORGA-68-15 #ORGA-68-16 #FNR-68-8 #L-69-52 #L-69-53 #PDR-69-12 #REF-69-10 #PDR-69-13 #PDR-69-14 #PDR-69-15 #PDR-69-16 #PDR-69-17 #PDR-69-18 #PDR-69-19 #PDR-69-20 #PDR-69-21 #L-69-54 #PDR-69-22 #L-69-55 #L-69-56 #ORGA-69-17 #L-69-57 #L-69-58 #DC-69-37 #DC-69-38 #L-70-61 #L-70-59 #L-70-60 #L-70-62 #DC-70-39 #DC-70-40 #L-70-63 #ORGA-70-18 #L-70-64 #L-70-66 #L-70-65 #DC-70-41 #L-71-67 #L-71-68 #L-71-69 #L-71-70 #DC-71-42 #DC-71-43 #DC-71-45 #DC-71-44 #ORGA-71-19 #DC-71-46 #L-72-71 #L-72-73 #L-72-72 #REF-72-11 #DC-72-47 #DC-72-48 #ORGA-72-20 #L-72-74 #L-72-75 #L-73-76 #DC-73-49 #DC-73-50 #L-73-77 #ORGA-73-21 #L-73-78 #L-73-79 #L-73-80 #L-73-81 #DC-73-51 #PDR-74-23 #PDR-74-24 #PDR-74-25 #PDR-74-29 #PDR-74-26 #PDR-74-27 #PDR-74-28 #PDR-74-30 #PDR-74-31 #PDR-74-32 #PDR-74-33 #L-74-82 #ORGA-74-22 #DC-74-52 #DC-74-53 #DC-74-54 #L-75-83 #DC-75-55 #DC-75-57 #DC-75-58 #DC-75-56 #ORGA-75-23 #L-75-84 #L-75-86 #L-75-85 #DC-75-59 #DC-75-60 #DC-75-61 #DC-75-63 #DC-75-62 #L-76-88 #L-76-87 #DC-76-64 #L-76-89 #L-76-90 #L-76-91 #DC-76-65 #DC-76-66 #I-76-2 #DC-76-67 #DC-76-68 #ORGA-76-24 #L-76-93 #L-76-92 #DC-76-69 #DC-76-70 #L-76-94 #I-76-3 #DC-76-78 #DC-76-76 #DC-76-73 #DC-76-74 #DC-76-71 #DC-76-72 #DC-76-77 #DC-76-75 #L-77-95 #L-77-96 #L-77-98 #L-77-97 #I-77-4 #FNR-77-9 #DC-77-79 #DC-77-80_81 #DC-77-83 #DC-77-84 #DC-77-85 #L-77-99 #DC-77-82 #I-77-5 #ORGA-77-25 #DC-77-86 #L-77-101 #L-77-100 #DC-77-87 #DC-77-88 #DC-77-89 #DC-77-90 #DC-77-92 #DC-77-91 #ORGA-78-26 #DC-78-93 #L-78-102 #L-78-103 #DC-78-94 #DC-78-96 #DC-78-97 #DC-78-95 #ORGA-78-27 #L-78-104 #DC-78-98 #DC-78-100 #DC-78-99 #L-78-105 #DC-78-103 #DC-78-101 #DC-78-102 #L-79-106 #FNR-79-10 #DC-79-104 #FNR-79-11 #L-79-107 #DC-79-107 #DC-79-106 #DC-79-105 #L-79-108 #L-79-109 #L-79-110 #ORGA-79-28 #DC-79-108 #L-79-111 #L-79-112 #DC-79-110 #DC-79-111 #DC-79-112 #DC-79-109 #DC-80-113 #L-80-113 #DC-80-114 #DC-80-115 #DC-80-116 #DC-80-118 #DC-80-121 #DC-80-120 #DC-80-117 #DC-80-119 #DC-80-122 #L-80-115 #ORGA-80-29 #L-80-114 #DC-80-123 #L-80-116 #L-80-117 #DC-80-124 #L-80-119 #L-80-118 #DC-80-125 #DC-80-126 #L-80-120 #DC-80-127 #DC-80-128 #PDR-81-34 #ORGA-81-30 #L-81-121 #PDR-81-35 #PDR-81-37 #PDR-81-36 #PDR-81-38 #PDR-81-39 #PDR-81-40 #PDR-81-41 #PDR-81-42 #PDR-81-43 #PDR-81-44 #PDR-81-45 #PDR-81-46 #PDR-81-47 #ELEC-81-1 #ORGA-81-31 #ORGA-81-32 #DC-81-130 #DC-81-129 #DC-81-132 #DC-81-131 #DC-81-133 #DC-81-135 #DC-81-136 #DC-81-134 #DC-82-139 #DC-82-137 #DC-82-138 #L-82-122 #ELEC-82-2 #L-82-124 #L-82-123 #L-82-125 #DC-82-140 #DC-82-142 #DC-82-141 #DC-82-143 #ORGA-82-33 #L-82-126 #DC-82-144 #DC-82-145 #L-82-127 #L-82-128 #DC-82-146 #L-82-129 #DC-82-147 #DC-82-148 #DC-82-149 #DC-82-154 #DC-82-150 #DC-82-155 #DC-82-151 #DC-82-152 #DC-82-153 #D-83-4 #ORGA-83-34 #DC-83-156 #DC-83-157 #DC-83-158 #DC-83-159 #DC-83-160 #DC-83-161 #L-83-130 #L-83-131 #L-83-132 #DC-83-162 #ORGA-83-35 #L-83-133 #L-83-134 #DC-83-163 #L-83-135 #DC-83-166 #DC-83-164 #DC-83-167 #DC-83-165 #DC-83-168 #DC-84-169 #L-84-136 #DC-84-170 #L-84-137 #DC-84-171 #DC-84-176 #DC-84-174 #DC-84-172 #DC-84-175 #DC-84-173 #DC-84-177 #DC-84-178 #DC-84-179 #DC-84-180 #ORGA-84-36 #DC-84-181 #DC-84-186 #DC-84-184 #DC-84-182 #DC-84-183 #DC-84-185 #DC-85-187 #DC-85-188 #L-85-138 #DC-85-194 #DC-85-195 #DC-85-191 #DC-85-189 #DC-85-192 #DC-85-193 #DC-85-190 #L-85-140 #DC-85-196 #L-85-139 #DC-85-197 #ORGA-85-37 #L-85-141 #L-85-142 #L-85-143 #L-85-144 #DC-85-198 #DC-85-199 #DC-85-205 #ORGA-85-38 #DC-85-201 #DC-85-203 #DC-85-202 #DC-85-200 #DC-85-204 #ORGA-86-39 #L-86-145 #L-86-146 #ORGA-86-40 #ORGA-86-41 #ELEC-86-3 #ORGA-86-42 #DC-86-206 #DC-86-207 #DC-86-208 #DC-86-209 #DC-86-210 #DC-86-212 #DC-86-211 #DC-86-214 #DC-86-215 #DC-86-213 #DC-86-216 #DC-86-217 #L-86-147 #ORGA-86-43 #DC-86-218 #L-86-148 #DC-86-219 #DC-86-220 #DC-86-221 #DC-86-223 #DC-86-222 #DC-86-225 #DC-86-224 #L-87-149 #L-87-150 #ORGA-87-44 #DC-87-226 #DC-87-228 #DC-87-227 #ORGA-87-45 #DC-87-229 #DC-87-230 #L-87-151 #ORGA-87-46 #ORGA-87-47 #L-87-152 #I-87-6 #PDR-87-48 #PDR-87-49 #ORGA-87-48 #DC-87-237 #DC-87-239 #DC-87-231 #DC-87-235 #DC-87-236 #DC-87-238 #DC-87-233 #DC-87-232 #DC-87-234 #DC-87-240 #DC-87-241 #L-88-153 #DC-88-242 #PDR-88-51 #L-88-154 #L-88-155 #PDR-88-52 #PDR-88-50 #PDR-88-53 #L-88-156 #PDR-88-54 #PDR-88-55 #PDR-88-56 #PDR-88-57 #PDR-88-58 #PDR-88-59 #L-88-157 #PDR-88-60 #ELEC-88-4 #ELEC-88-5 #DC-88-243 #L-88-158 #ELEC-88-6 #ELEC-88-7 #ORGA-88-49 #DC-88-244 #PDR-88-61 #ORGA-88-50 #ORGA-88-51 #REF-88-12 #DC-88-245 #L-88-159 #REF-88-13 #REF-88-14 #I-88-7 #DC-88-246 #DC-88-250 #DC-88-249 #DC-88-251 #DC-88-247 #DC-88-248 #I-89-10 #ORGA-89-52 #DC-89-252 #ORGA-89-53 #DC-89-253 #DC-89-254 #DC-89-255 #DC-89-258 #DC-89-256 #DC-89-257 #DC-89-259 #L-89-160 #DC-89-260 #DC-89-261 #ORGA-89-54 #L-89-161 #DC-89-262 #I-89-8 #L-89-162 #DC-89-268 #DC-89-270 #DC-89-264 #DC-89-265 #DC-89-266 #DC-89-271 #DC-89-263 #DC-89-267 #DC-89-272 #DC-89-269 #I-89-9 #L-90-163 #DC-90-273 #L-90-164 #DC-90-274 #DC-90-275 #DC-90-276 #ORGA-90-55 #DC-90-277 #ORGA-90-56 #DC-90-279 #DC-90-278 #DC-90-280 #DC-90-281 #DC-90-286 #DC-90-285 #DC-90-282 #ORGA-91-57 #DC-90-283 #DC-90-284 #DC-90-288 #DC-90-287 #ORGA-91-58 #L-91-165 #DC-91-289 #DC-91-291 #DC-91-290 #DC-91-292 #L-91-166 #ORGA-91-59 #DC-91-293 #DC-91-295 #DC-91-298 #DC-91-294 #DC-91-296 #DC-91-297 #DC-91-299 #ORGA-91-60 #DC-91-300 #L-91-167 #DC-91-302 #DC-91-301 #DC-91-303 #DC-91-304 #DC-92-306 #DC-92-305 #DC-92-307 #DC-92-308 #DC-92-309 #L-92-168 #ORGA-92-61 #REF-92-15 #DC-92-310 #DC-92-311 #DC-92-312 #REF-92-16 #REF-92-17 #REF-92-18 #DC-92-313 #REF-92-19 #ORGA-92-62 #REF-92-20 #L-92-169 #L-92-170 #DC-92-314 #L-92-171 #L-92-172 #L-92-173 #ORGA-93-63 #ORGA-93-65 #ORGA-93-64 #DC-92-315 #DC-92-316 #DC-92-317 #L-93-174 #DC-93-320 #DC-93-318 #DC-93-319 #DC-93-321 #DC-93-322 #DC-93-324 #DC-93-323 #DC-93-326 #DC-93-325 #L-93-175 #ORGA-93-66 #DC-93-327 #DC-93-328 #ELEC-93-8 #DC-93-330 #DC-93-331 #DC-93-332 #DC-93-329 #DC-93-334 #DC-93-333 #DC-93-335 #DC-93-336 #DC-93-337 #ORGA-94-67 #DC-94-338 #L-94-176 #ELEC-93-8R #ELEC-94-9 #DC-94-339 #ORGA-94-68 #DC-94-340 #DC-94-341 #DC-94-342 #DC-94-346 #R2_AN-93-1213 #DC-94-343_344 #DC-94-345 #DC-94-347 #DC-94-348 #ORGA-94-69 #D-94-5 #DC-94-349 #DC-94-350 #DC-94-351 #DC-94-355 #DC-94-354 #DC-94-353_356 #DC-95-363 #DC-94-352 #DC-94-359 #DC-94-357 #DC-94-358 #DC-95-361 #DC-95-362 #DC-95-360 #DC-95-364 #ORGA-95-70 #ORGA-95-71 #ORGA-95-72 #PDR-95-63 #ORGA-95-73 #PDR-95-64 #PDR-95-67 #PDR-95-62 #PDR-95-66 #PDR-95-65 #PDR-95-68 #PDR-95-69 #PDR-95-70 #PDR-95-71 #PDR-95-72 #PDR-95-73 #PDR-95-74 #PDR-95-75 #PDR-95-76 #PDR-95-77 #PDR-95-78 #PDR-95-79 #PDR-95-80 #D-95-6 #PDR-95-81 #L-95-177 #ELEC-95-10 #ORGA-95-74 #PDR-95-82 #PDR-95-83 #DC-95-365 #I-95-11 #I-95-12 #ORGA-95-75 #PDR-95-87 #PDR-95-84 #PDR-95-85 #PDR-95-86 #PDR-95-89 #PDR-95-90 #PDR-95-91 #PDR-95-88 #PDR-95-92 #DC-95-366 #DC-95-367 #PDR-95-93 #DC-95-368 #DC-95-369 #DC-95-371 #DC-95-370 -->
```