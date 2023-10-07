<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">
<html lang="fr">
<head>
<a href="https://github.com/laowantong/mocodo"><img style="position: absolute; top: 0; right: 0; border: 0; width: 149px; height: 149px;" src="web/fork-me-right-turquoise@2x.png" alt="Fork me on GitHub"></a>
<title>Mocodo online</title>
<meta charset="utf-8">
<link rel="stylesheet" href="web/reset.css" />
<link rel="stylesheet" href="web/style.css" />

<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="icon" type="image/png" href="/favicon-32x32.png" sizes="32x32">
<link rel="icon" type="image/png" href="/favicon-16x16.png" sizes="16x16">
<link rel="manifest" href="/manifest.json">
<link rel="mask-icon" href="/safari-pinned-tab.svg" color="#0d42ff">
<meta name="apple-mobile-web-app-title" content="Mocodo">
<meta name="application-name" content="Mocodo">
<meta name="theme-color" content="#fff">
</head>

<body>

<div id="wrap">
	<div id="banner">
	    <img src="web/mocodonline.svg" />
	</div>​
	<form method="post" id="mainForm" action="web/download.php" autocomplete="off">
		<input type="hidden" name="state" id="state" value="dirty"/>
		<div id="inputZone">
			<div class="line"></div>
			<ul class='tabs'>
				<li><a href='#aboutContents' class="first_tab"><span class="circled">&#8505;</span></a></li>
				<li><a href='#inputContents' class="active"><span>Entrée</span></a></li>
				<li><a href='#paramContents'><span>Options</span></a></li>
				<li><a href='#geoContents' id="geoTab"><span>Retouches</span></a></li>
			</ul>
			<div class="pane">
				<div id="inputButtons" class='buttons'>
					<div class="button-with-popup" id="arrangeButton">
						<span class="customButton tooltip" onmouseenter="closePopup()" onmousedown="startCountdown(this)" onmouseup="stopCountdown('arrange')" style="background-image: url(web/png/arrange.png);"><span class="tooltiptext">Réorganiser</span></span>
						<div class="popup-menu" onmouseleave="closePopup(this)">
							<span class="popup-item popup-close" onclick="closePopup()">⨉</span>
							<span class="popup-item" onclick="rewrite('arrange:current')">sur la grille actuelle</span>
							<span class="popup-item" onclick="rewrite('arrange:wide')">en privilégiant la largeur</span>
							<span class="popup-item" onclick="rewrite('arrange:balanced=0')">sur la plus petite grille équilibrée</span>
							<span class="popup-item" onclick="rewrite('arrange:balanced=1')">sur la seconde plus petite grille équilibrée</span>
							<span class="popup-item" onclick="rewrite('arrange')">sans contraintes (par défaut)</span>
						</div>
					</div>
					<div class="button-with-popup" id="flipButton">
						<span class="customButton tooltip" onmouseenter="closePopup()" onmousedown="startCountdown(this)" onmouseup="stopCountdown('flip:hvd')" style="background-image: url(web/png/flip.png);"><span class="tooltiptext">Inverser</span></span>
						<div class="popup-menu" onmouseleave="closePopup(this)">
							<span class="popup-item popup-close" onclick="closePopup()">⨉</span>
							<span class="popup-item" onclick="rewrite('flip:h')">horizontalement</span>
							<span class="popup-item" onclick="rewrite('flip:v')">verticalement</span>
							<span class="popup-item" onclick="rewrite('flip:d')">selon la première diagonale</span>
							<span class="popup-item" onclick="rewrite('flip:hvd')">selon la deuxième diagonale (par défaut)</span>
						</div>
					</div>
					<div class="button-with-popup" id="typoButton">
						<span class="customButton tooltip" onmouseenter="closePopup()" onmousedown="startCountdown(this)" onmouseup="stopCountdown('ascii:labels snake:labels lower:attrs,roles upper:boxes')" style="background-image: url(web/png/typo.png);"><span class="tooltiptext">Éditer</span></span>
						<div class="popup-menu" onmouseleave="closePopup(this)">
							<span class="popup-item popup-close" onclick="closePopup()">⨉</span>
							<span class="popup-item" onclick="rewrite('ascii:labels')">libellés en ASCII</span>
							<span class="popup-item" onclick="rewrite('snake:labels')">libellés en <i>snake case</i></span>
							<span class="popup-item" onclick="rewrite('lower:attrs,roles')">attributs en minuscules</span>
							<span class="popup-item" onclick="rewrite('upper:boxes')">noms des entités et des associations en majuscules</span>
							<span class="popup-item" onclick="rewrite('ascii:labels snake:labels lower:attrs,roles upper:boxes')">tous les précédents à la fois (par défaut)</span>
							<span class="popup-item" onclick="rewrite('fix:cards')">correction des fautes de frappe dans les cardinalités</span>
						</div>
					</div>
					<div class="button-with-popup" id="createButton">
						<span class="customButton tooltip" onmouseenter="closePopup()" onmousedown="startCountdown(this)" onmouseup="stopCountdown('create:entities')" style="background-image: url(web/png/create.png);"><span class="tooltiptext">Révéler</span></span>
						<div class="popup-menu" onmouseleave="closePopup(this)">
							<span class="popup-item popup-close" onclick="closePopup()">⨉</span>
							<span class="popup-item" onclick="rewrite('create:dfs')">mettre des DF partout où c'est possible</span>
							<span class="popup-item" onclick="rewrite('create:df_arrows')">ajouter des flèches aux DF</span>
							<span class="popup-item" onclick="rewrite('create:cifs')" id="createCifs" style="display: none;">ajouter les CIF correspondant aux agrégats</span>
							<span class="popup-item" onclick="rewrite('create:types=')">mettre en évidence les types à remplir</span>
							<span class="popup-item" onclick="rewrite('create:types')">deviner les types à partir du nom des attributs</span>
							<span class="popup-item" onclick="rewrite('delete:types')">supprimer les types</span>
							<span class="popup-item" onclick="rewrite('create:entities')">réparer l'oubli d'entités référencées dans des associationss (par défaut)</span>
						</div>
					</div>
					<div class="button-with-popup" id="jokerButton">
						<span class="customButton tooltip" onmouseenter="closePopup()" onmousedown="startCountdown(this)" onmouseup="stopCountdown('obfuscate')" style="background-image: url(web/png/joker.png);"><span class="tooltiptext">Masquer</span></span>
						<div class="popup-menu" onmouseleave="closePopup(this)">
							<span class="popup-item popup-close" onclick="closePopup()">⨉</span>
							<span class="popup-item" onclick="rewrite('obfuscate')">masquer avec du faux texte (par défaut)</span>
							<span class="popup-item" onclick="rewrite('drown')">masquer avec des libellés génériques numérotés</span>
							<span class="popup-item" onclick="rewrite('delete')" title="Crée un MCD à compléter. À accompagner de la liste des descriptifs des attributs obtenue avec l'option « Dictionnaire des données en Markdown (deux colonnes) ».">masquer les attributs et les cardinalités</span>
							<span class="popup-item" onclick="rewrite('create:types=PLACEHOLDER randomize:types')">remplir les types au hasard</span>
							<span class="popup-item" onclick="rewrite('grow:from_scratch,arity_3=1 arrange')">créer un MCD aléatoire avec des libellés génériques numérotés</span>
							<span class="popup-item" onclick="rewrite('grow:from_scratch,arity_3=1 obfuscate create:roles lower:roles arrange')">créer un MCD d'entraînement à la conversion en relationnel</span>
						</div>
					</div>
					<div class="button-with-popup" id="explodeButton" style="display: none;">
						<span class="customButton tooltip explosion-call" onmouseenter="closePopup()" onmousedown="startCountdown(this)" onmouseup="stopCountdown('explode:arity=3 arrange')" style="background-image: url(web/png/explode.png);"><span class="tooltiptext">Décomposer</span></span>
						<div class="popup-menu" onmouseleave="closePopup(this)">
							<span class="popup-item popup-close" onclick="closePopup()">⨉</span>
							<span class="popup-item" onclick="rewrite('drain')">drainer les DF porteuses d'attributs</span>
							<span class="popup-item" onclick="rewrite('split arrange')">décomposer les DF ternaires et plus</span>
							<span class="popup-item explosion-call" onclick="rewrite('explode:arity=3 arrange')">décomposer les non-DF ternaires et plus (par défaut)</span>
							<span class="popup-item explosion-call" onclick="rewrite('explode:arity=2.5 arrange')">décomposer les non-DF binaires et plus porteuses d'attributs</span>
							<span class="popup-item explosion-call" onclick="rewrite('explode:arity=2 arrange')">décomposer toutes les non-DF binaires et plus</span>
						</div>
					</div>
				</div>
				<div id="aboutContents" class="contents">
					<p>
					Mocodo est un logiciel d'aide à l'enseignement et à l'apprentissage des <a href="https://fr.wikipedia.org/wiki/Base_de_données_relationnelle">bases de données relationnelles</a>.
					</p><p>
					<ul>
						<li>En entrée, il prend un <a href="https://fr.wikipedia.org/wiki/Modèle_entité-association">MCD</a> (modèle conceptuel de données) décrit dans un langage dédié minimaliste.</li>
						<li>En sortie, il produit un diagramme entité-association et, à la demande, un <a href="https://fr.wikipedia.org/wiki/Merise_(informatique)#MLD_:_modèle_logique_des_données">MLD</a> (schéma relationnel, sous forme graphique ou textuelle), un <a href="https://fr.wikipedia.org/wiki/Langage_de_définition_de_données">DDL</a> (requêtes SQL de création de la base), un <a href="https://fr.wikipedia.org/wiki/Diagramme_de_classes">diagramme de classes UML</a>, etc.</li>
						<li>En bonus, il est capable de réorganiser automatiquement votre MCD de façon esthétique, et de lui appliquer des opérations de réécriture qui vont du mondain (typographie) à l'académique (décomposition d'associations), en passant par le merveilleux (inférence de types, génération d'exercices et d'exemples).</li>
					</ul>
					<p>
					Ce site est prévu pour une utilisation basique et occasionnelle, typiquement en salle de classe. Si vous souhaitez avoir accès à toutes les fonctionnalités de Mocodo, une installation en local est recommandée :
					</p>
					<br>
					<pre>> pip install mocodo</pre>
					</br>
					<p>
					Sous cette forme, Mocodo est un puissant <a href="https://fr.wikipedia.org/wiki/Interface_en_ligne_de_commande">logiciel en ligne de commande</a>, multiplateforme, <a href="https://github.com/laowantong/mocodo"><i>open-source</i></a>, <a href="https://fr.wikipedia.org/wiki/Licence_MIT">libre</a> et gratuit. Il s'intègre particulièrement bien à l'environnement <a href="https://jupyter.org">Jupyter Notebook</a>.
					</p>
					<br>
					<p>
					Pour en savoir plus, suivez nos tutoriels interactifs (onglet Entrée), puis plongez-vous dans la <a target="_blank" href="https://rawgit.com/laowantong/mocodo/master/doc/fr_refman.html">documentation</a>.
					</p>
					<br>
					<p style="font-size:small; font-style:italic; text-align:right;">
					Aristide Grange, Université de Lorraine, Metz (France)
					</p>
				</div>
				<div id="inputContents" class="contents">
					<div id=inputPane>
						<div><input type="text" oninput="markAsDirty();unbox()" onfocus="onFocus(this)" name="title" id="title" value="MCD" onblur="onBlur(this)" autocomplete="off" /></div>
						<select onchange="changeTitleToNthTuto();unbox()" name="tutorial" id="tutorial" title="Parcourez notre galerie de MCD pour apprendre la syntaxe de Mocodo."></select>
						<textarea hidden name="text"><?php
							$encoded_string = (isset($_GET['mcd'])) ? $_GET['mcd'] : '';
							echo (zlib_decode(base64_decode(strtr($encoded_string, '-_', '+/'))));
						?></textarea>
						<div id="editor-wrapper">
						<div id="editor"></div>
						</div>
					</div>
				</div>
				<div id="paramContents" class="contents">
					<div><label class="fixedWidth" for="shapes">Police et proportions</label><select onchange="markAsDirty();writeCookie()" name="shapes" id="shapes"></select></div>
					<div><label class="fixedWidth" for="colors">Palette de couleurs</label><select onchange="markAsDirty();writeCookie()" name="colors" id="colors"></select></div>
					<div><label class="fixedWidth" for="flashlight">Mode nuit</label><input type="checkbox" id="flashlight" onclick="switchOnFlashlight(event)"></div>
					<div>
						<label class="fixedWidth" for="adjust_width">Ajustement de la largeur des libellés</label>
						<input type="number" value="1.00" max="2.00" min="0.50" step="0.01" onchange="writeCookie()" name="adjust_width" id="adjust_width" style="width: 5em; border-radius: 0;">
					</div>
					<div><label class="fixedWidth" for="delays">Temps de calcul limité à </label><select onchange="writeCookie()" name="delays" id="delays"></select></div>
					<div><label class="fixedWidth" for="detect_overlaps" title="Lève une erreur en cas de chevauchement de pattes horizontales ou verticales.">Détecter les chevauchements</label><input type="checkbox" name="detect_overlaps" id="detect_overlaps" onchange='markAsDirty();writeCookie()' checked /></div>
					<div style="color:#222;"><label class="fixedWidth" title="Les formats cochés seront générés et inclus dans l'archive téléchargée.">Format des images en sortie</label><span title="Pour le web, zoom illimité. Requis."><input type="checkbox" disabled="true" id="svg" checked /><label for="svg">&nbsp;SVG&nbsp;&nbsp;</label></span><span title="Multi-usage, zoom limité."><input type="checkbox" name="png" id="png" onchange='markAsDirty();writeCookie()' /><label for="png">&nbsp;PNG&nbsp;&nbsp;</label></span><span title="Pour l'impression, zoom illimité."><input type="checkbox" name="pdf" id="pdf" onchange='markAsDirty();writeCookie()' /><label for="pdf">&nbsp;PDF&nbsp;&nbsp;</label></span></div>
					<div><label class="fixedWidth" for="knowledge" title="Vous pouvez adapter les traitements et l'interface de Mocodo online à des besoins plus avancés.">Notions et fonctionnalités supplémentaires</label><details style="display: inline-flex;"><summary style="color:#666;">Activer…</summary><label class="fixedWidth"></label><ul name="knowledge" id="knowledge"></ul></details></div>
					<div><label class="fixedWidth" for="conversions" title="Les formats cochés seront affichés sous l'onglet « Autres sorties » et inclus dans l'archive téléchargée.">Conversions en sortie</label><ul name="conversions" id="conversions"><details><summary style="color:#666;">Autres options de conversions…</summary></details></ul>
					</div>
				</div>
				<div id="geoContents" class="contents">
					<fieldset><legend>Coordonnées du centre des boîtes</legend><div id="coords"></div></fieldset>
					<fieldset><legend>Décalage des cardinalités</legend><div id="cards"></div></fieldset>
					<fieldset><legend>Zone de rognage</legend><div id="size"></div></fieldset>
					<fieldset><legend>Position des flèches des associations</legend><div id="arrows"></div></fieldset>
				</div>
			</div>
		</div>
		<div id="outputZone">
			<div class="line"></div>
			<ul class='tabs'>
				<li><a href='#diagramAndSupplementOutput' id="diagramTab" class="first_tab active"><span>Diagramme</span></a></li>
				<li><a href='#convertOutput'><span>Autres sorties</span></a></li>
				<li><a href='#errorOutput' id="errorTab"><span>Erreurs</span></a></li>
			</ul>
			<div class="pane">
				<div id="outputButtons" class='buttons'>
					<span class="customButton tooltip" id="refreshButton" onclick="generate()" style="background-image: url(web/png/refresh.png);"><span class="tooltiptext">Rafraîchir</span></span>
					<div id="rotatingButton" style="display: none">
						<span class="customButton" id="empty" style="background-image: url(web/png/empty.png);"></span>
						<span class="customButton" id="refreshRotatingButton" style="background-image: url(web/png/refresh_rotating.png);"></span>
					</div>
					<a class="customButton tooltip" id="downloadButton" href="" download="" target="_blank" style="background-image: url(web/png/download.png);"><span class="tooltiptext">Télécharger</span></a>
				</div>
				<div id="diagramAndSupplementOutput">
					<div id="diagramOutput" class="contents active never_refreshed"><img src="web/generate_tip.svg"/></div>
					<div id="diagramOutputSupplement" class="contents"></div>
				</div>
				<div id="convertOutput" class="contents never_refreshed"><img src="web/generate_tip.svg"/></div>
				<div id="errorOutput" class="contents"></div>
			</div>
		</div>
	</form>
</div>
<div id="navigation">
	<a target="_blank" href="https://github.com/laowantong/mocodo">Mocodo 3.2.1</a>
	&nbsp;∙&nbsp;
	<a target="_blank" href="https://rawgit.com/laowantong/mocodo/master/doc/fr_refman.html">Documentation</a>
	&nbsp;∙&nbsp;
	<a target="_blank" href="https://www.transifex.com/aristide/mocodo">Localisation</a>
	&nbsp;∙&nbsp;
	<a target="_blank" href="https://github.com/laowantong/mocodo/issues">Récriminations</a>
	&nbsp;∙&nbsp;
	<a target="_blank" href="" title="En ligne de commande, faites `mocodo --help` pour afficher mon adresse mail." onclick="alert('En ligne de commande, faites :\n\xA0\xA0\xA0\xA0mocodo --help\npour afficher mon adresse mail.')">Contact</a>
</div>

<script type="text/javascript" charset="utf8" src="web/jquery-1.7.2.min.js"></script>
<script type="text/javascript" charset="utf8" src="web/js.cookie.js"></script>
<script type="text/javascript" charset="utf8" src="web/mocodo.js"></script>
<script type="text/javascript" charset="utf8" src="web/flashlight.js"></script>
<script type="text/javascript" charset="utf8" src="web/ace-builds/ace.js"></script>
<script type="text/javascript" charset="utf8" src="web/ace-builds/ext-language_tools.js"></script>

</body>
</html>
