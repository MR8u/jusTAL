# jusTAL

# TODO :

    - Trailer et incident 
    - Remplacer les " et ' problèmatique (commande du script)
    - [A-z]- [A-z] et inverse

## Template : 

### Remplacer :

    - TEI.teiHeader.fileDesc.titleStmt.title[@type="sub"] = numPV = #deliberation
    - TEI.teiHeader.fileDesc.titleStmt.respStmt[6].name = nomDuRelecteur
    - TEI.text.body.div1[@corresp] = numPV = #deliberation
    - TEI.text.body.div1.head.title = numPV = #deliberation

### Nouvelle structure :

'''
<div1 type="pv" corresp="#pv">
    <div2 type="seance" date="#date_seance">
        <div3 type="ouverture">
            <div4 type="membrePresent"></div4>
            <div4 type="ordreDuJour"></div4>
        </div3>
        <div3 type="question" n="n" corresp="#decision">
            <div4 type="introduction"></div4>
            <writing type="rapport" who="#membre"></writing>
            <div4 type="discussion">
                <div4 type="vote" n="n">
                </div4>
            </div4>
        </div3>
    </div2>
</div1>
'''

## Problèmes :

    - <h2> >> <hi rend="underline">
    - <pb> dans un seg  PV1982-01-05.xml (<pb n="2"/>)
    - <div4 type="vote"> can't containe <seg> so keep <p> atm
    - toujours le président qui soumet au vote ?
    - Double speakers :

'''PV1982-01-05.xml 
    <u who="#peretti_achille #joxe_louis">
        <seg><hi rend="underline">Monsieur PERETTI</hi> et <hi rend="underline">Monsieur JOXE</hi> sont d'accord pour considérer que le texte de la loi est obscur et mal rédigé.</seg>
    </u>
'''
    - Incident : <who> ? <seg> or <p> ? SHOULD ONLY CONTAIN <desc>

'''PV1982-01-05.xml
    <incident>
        <seg><hi rend="underline">Monsieur le Président</hi> suspend la séance pendant quinze minutes puis demande à Monsieur VEDEL de donner lecture de la modification qu'il propose au projet de décision.</seg>
    </incident>
'''
    - Vote : <seg> or <p> ?
    
'''PV1982-01-05.xml
    <div4 type="vote" n="1">
        <p>Le projet est adopté à l'unanimité par les membres du Conseil.</p>
    </div4>
'''
     - Trailer : <trailer> can't contain <p> but can contain <seg> 

'''PV1982-01-05.xml
    <trailer>
        <seg>La séance est levée à 18 h 25.</seg>
    </trailer>
'''
    
    - Transcriptor note ? 

'''PV1982-02-11
    <u who="#">
        <seg>Après cette discussion, il est donc décidé de ne pas modifier le projet et de se contenter du visa tel qu'il est actuellement proposé par le rapporteur.</seg>
        <seg>Il est donné lecture du projet.</seg>
    </u>
    <u who="#">
        <seg>Une discussion rapide intervient sur ce point et le Conseil n'ayant jamais exprimé clairement sa position dans une décision, il est considéré comme suffisant de faire disparaître, dans le considérant, les termes "en l'absence de toute réserve au profit du pouvoir règlementaire" qui provoquent la difficulté.</seg> 
    </u>
'''

    - Trailer who ?

'''PV1982-02-11
    <seg><hi rend="underline">Monsieur GROS</hi> pose la question du caractère contradictoire des
    procédures.</seg>
'''
    - Balise pour ce genre de problème :
    
'''PV1982-02-18-23
    <seg>Il apparaît, en conclusion, que le représentant de 1'Etat, <!-- ajout manuscrit illisible --> paralysé temporairement, du fait de la procédure instaurée par la loi,
    alors qu'un acte administratif illégal est exécutoire. Cette procédure
    ne respecte donc pas pleinement les dispositions de l'article 72
    et, dans cette mesure, il est donc proposé une déclaration de
    non conformité à la Constitution. Celle-ci n'entraînera pas
    l'inconstitutionnalité de l'ensemble de la loi mais devra amener
    à revenir sur certaines dispositions d'abrogation.</seg>
'''
    - Id de décision introuvable (partiel)
'''PV1982-02-18-23
<div2 type="question" n="1" corresp="#DC8">
'''

    - Incident mal définis :

'''PV1982-02-18-23
<incident>
<p>
	<u>Monsieur le Président</u>, après avoir demandé si d'autres membres
souhaitent intervenir, lève la séance à 18h05, après avoir
indiqué que l'examen de la loi relative aux droits et libertés
des communes, des départements et des régions, sera poursuivi
lors de la séance du 23 février 1980 à 10 heures.
</p>
<pb n="18"/>
<p>
	<h1>SEANCE DU MARDI 23 FEVRIER 1982</h1>
</p>
<p>
	Le Conseil se réunit à 10 heures 30, tous ses membres étant présents,
à l'exception de Monsieur Valéry GISCARD d'ESTAING qui est excusé.
</p>
<p>
	<u>M. Le Président</u> rappelle l'ordre du jour porte sur la poursuite
de l'examen de la conformité à la Constitution de la loi relative
aux droits et libertés des communes, des départements et des
régions.
</p>
</incident>
'''

    - Doit être inclu dans l'utterance ?

'''PV1982-02-18-23
<p>
	Monsieur LECOURT donne alors lecture de son projet de décision.
</p>
'''

    - Doit être dans la discussion ou dans l'introduction de la séance ?

'''PV1982-02-18-23
<u who="#lecourt_robert">
    <seg><hi rend="underline">Monsieur LECOURT</hi> indique qu'éclairé par la délibération du Conseil, lors de sa séance du 18 février 1982, il est en mesure de lui proposer un projet de décision.</seg>
    <seg>Avant de donner lecture de ce projet, il en indique les lignes directrices.</seg>
    <seg>Conformément au voeu du Conseil, il a écarté deux systèmes. D'une part, une déclaration de conformité et, d'autre part, une annulation totale de la loi.</seg>
    <seg>Le projet qu'il propose censure donc seulement certaines dispositions des articles 2, 3, 45, 46 et 69-1, dans la mesure où elles comportent une méconnaissance des dispositions de l’article 72 de la Constitution. Il indique qu'il n'a pas cru devoir proposer l'annulation des articles 4, 47 et 69-11, dans la mesure où ces textes relatifs au recours d'une personne lésée prêtent à des divergences. Sa décision s'efforce de préciser la portée générale qu'il convient de donner à l'article 72 de la Constitution et d'analyser les lacunes procédurales que comporte la présente loi, dans la mise en oeuvre du contrôle administratif qui incombe au représentant de l'Etat.</seg>
    <seg>Monsieur LECOURT donne alors lecture de son projet de décision.</seg>
</u>
<u who="#frey_roger">
    <seg><hi rend="underline">Monsieur le Président</hi> remercie Monsieur LECOURT et déclare que la discussion générale portant sur ce projet est ouverte.</seg>
</u>
'''

    - Doit-on utiliser who ici ?

'''PV1982-06-28
    <u who="#frey_roger">
        <seg>Après la lecture de ce projet de décision, Monsieur le Président déclare ouverte la discussion générale.</seg>
    </u>
'''

    - Remarque sur les effets de la transcription

'''
    <u who="#segalat_andre">
        <seg>Monsieur SEGALAT déclare se rallier à la proposition de Monsieur VEDEL qui est prudente.</seg>
    </u>
'''

    - A ca place dans le rapport ? 

'''PV1982-07-27
<seg>
    <u>Monsieur GROS</u> déclare alors en avoir terminé avec son rapport.
</seg>

<seg>
    <u>Monsieur le Président</u> remercie Monsieur GROS pour son exposé
fort intéressant et détaillé et lui demande de bien vouloir
lire son projet de décision.
</seg>
'''

    - Introduire un type pause ? / interlude ? / cloture -> réouverture ?

'''PV1982-07-27
<div3 type="divers">
    <p>Au terme de la séance, Monsieur le Président MONNERVILLE demande à ses collègues d’excuser son absence lors de la séance de l'après-midi. Il remercie tous les membres du Conseil pour la sympathie qu'ils lui ont témoignée à l'occasion de l'épreuve pénible qui lui a été infligée.</p>
    <p>La séance est levée à 13 h 15.</p>
</div3>
'''

    - n=1 -> n=2

'''PV1982-07-27
<div5 type="vote" n="2">
    <p>Il soumet au vote la décision proposée. Celle-ci est adoptée à l'unanimité par les membres du Conseil.</p>
</div5>
''' 

    - Manque id decision

'''PV1982-07-30
<div3 type="question" n="1"></div3>
'''