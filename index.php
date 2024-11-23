<!DOCTYPE html>
<html lang="fr">
<head>
	<title>Mocodo online</title>
	<meta charset="utf-8" />
	<meta name="apple-mobile-web-app-title" content="Mocodo" />
	<meta name="application-name" content="Mocodo" />
	<meta name="theme-color" content="#fff" />
	<link rel="stylesheet" href="web/reset.css" />
	<link rel="stylesheet" href="web/style.css" />
	<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
	<link rel="icon" type="image/png" href="/favicon-32x32.png" sizes="32x32" />
	<link rel="icon" type="image/png" href="/favicon-16x16.png" sizes="16x16" />
	<link rel="manifest" href="/manifest.json" />
	<link rel="mask-icon" href="/safari-pinned-tab.svg" color="#0d42ff" />
	<script src="web/jquery-1.7.2.min.js"></script>
	<script src="web/js.cookie.js"></script>
	<script src="web/mocodo.js"></script>
	<script src="web/flashlight.js"></script>
	<script src="web/ace-builds/ace.js"></script>
	<script src="web/ace-builds/ext-language_tools.js"></script>
	<script async defer src="https://buttons.github.io/buttons.js"></script>
</head>
<?php
if (strpos($_SERVER['HTTP_REFERER'], 'localhost')) {
    $mocodo = "~/opt/anaconda3/bin/mocodo";
    $web_url = "http://localhost:8898/mocodo/web/";
  } else {
    $mocodo = "~/.local/bin/mocodo";
    $web_url = "https://www.mocodo.net/web/";
  }
$version = shell_exec("$mocodo --version");
$version = !empty($version) ? trim($version) : '';

$lib = $_GET['lib'];
if ($lib) {
	echo "<script>$(document).ready(function() { $('#lib').val('{$lib}'); });</script>";
}
?>
<body>
	<div id="wrap">
		<div id="banner">
			<img
				src="web/mocodonline.svg"
				alt="Mocodo online"
				style="width: 589px; height: auto;"
			/>
		</div>
		<div id="motto">
			<span>Modélisation Conceptuelle de Données. Nickel. Ni souris.</span>
		</div>
		<form method="post" id="mainForm" action="web/download.php" autocomplete="off">
			<input type="hidden" name="state" id="state" value="dirty" />
			<div id="inputZone">
				<div class="line"></div>
				<ul class="tabs">
					<li><a href="#aboutContents" class="first_tab"><span class="info-symbol" style="background-image: url(web/png/info.png);"></span></a></li>
					<li><a href="#inputContents" class="active"><span>Entrée</span></a></li>
					<li><a href="#paramContents"><span>Options</span></a></li>
					<li><a href="#geoContents" id="geoTab"><span>Retouches</span></a></li>
				</ul>
				<div class="pane">
					<div id="inputButtons" class="buttons">
						<div class="button-with-popup" id="arrangeButton">
							<span class="customButton tooltip" onmouseenter="closePopup()" onclick="handleClick(this, 'arrange')" style="background-image: url(web/png/arrange.png);"><span class="tooltiptext">Réarranger</span></span>
							<div class="popup-menu" onmouseleave="closePopup(this)">
								<span class="popup-item popup-close" onclick="closePopup()">⨉</span>
								<span class="popup-item" onclick="rewrite('arrange:current')">sur la grille actuelle</span>
								<span class="popup-item" onclick="rewrite('arrange:wide')">en privilégiant la largeur</span>
								<span class="popup-item" onclick="rewrite('arrange:balanced=0')">sur la plus petite grille équilibrée</span>
								<span class="popup-item" onclick="rewrite('arrange:balanced=1')">sur la seconde plus petite grille équilibrée</span>
								<span class="popup-item" onclick="rewrite('arrange')">sans contraintes (double clic)</span>
							</div>
						</div>
						<div class="button-with-popup" id="flipButton">
							<span class="customButton tooltip" onmouseenter="closePopup()" onclick="handleClick(this, 'flip:hvd')" style="background-image: url(web/png/flip.png);"><span class="tooltiptext">Inverser</span></span>
							<div class="popup-menu" onmouseleave="closePopup(this)">
								<span class="popup-item popup-close" onclick="closePopup()">⨉</span>
								<span class="popup-item" onclick="rewrite('flip:h')">horizontalement</span>
								<span class="popup-item" onclick="rewrite('flip:v')">verticalement</span>
								<span class="popup-item" onclick="rewrite('flip:d')">selon la première diagonale</span>
								<span class="popup-item" onclick="rewrite('flip:hvd')">selon la deuxième diagonale (double clic)</span>
							</div>
						</div>
						<div class="button-with-popup" id="typoButton">
							<span class="customButton tooltip" onmouseenter="closePopup()" onclick="handleClick(this, 'ascii:labels snake:labels lower:attrs,roles upper:boxes')" style="background-image: url(web/png/typo.png);">
								<span class="tooltiptext">Éditer</span>
							</span>
							<div class="popup-menu" onmouseleave="closePopup(this)">
								<span class="popup-item popup-close" onclick="closePopup()">⨉</span>
								<span class="popup-item" onclick="rewrite('camel:labels')">libellés en <i>camelCase</i></span>
								<span class="popup-item" onclick="rewrite('pascal:labels')">libellés en <i>PascalCase</i></span>
								<span class="popup-item" onclick="rewrite('snake:labels')">libellés en <i>snake_case</i></span>
								<span class="popup-item" onclick="rewrite('ascii:labels')">libellés en ASCII</span>
								<span class="popup-item" onclick="rewrite('lower:attrs,roles')">attributs en minuscules</span>
								<span class="popup-item" onclick="rewrite('upper:boxes')">noms des entités et des associations en majuscules</span>
								<span class="popup-item" onclick="rewrite('snake:labels ascii:labels lower:attrs,roles upper:boxes')">les quatre précédents à la fois (double clic)</span>
								<span class="popup-item" onclick="rewrite('fix:cards')">correction des fautes de frappe dans les cardinalités</span>
							</div>
						</div>
						<div class="button-with-popup" id="createButton">
							<span class="customButton tooltip" onmouseenter="closePopup()" onclick="handleClick(this, 'create:entities')" style="background-image: url(web/png/create.png);"><span class="tooltiptext">Révéler</span></span>
							<div class="popup-menu" onmouseleave="closePopup(this)">
								<span class="popup-item popup-close" onclick="closePopup()">⨉</span>
								<span class="popup-item" onclick="rewrite('create:dfs')">mettre des DF partout où c'est possible</span>
								<span class="popup-item" onclick="rewrite('create:df_arrows')">ajouter des flèches aux DF 11</span>
								<span class="popup-item" onclick="rewrite('create:cifs')" id="createCifs" style="display: none;">ajouter les CIF correspondant aux agrégats</span>
								<span class="popup-item" onclick="rewrite('create:types=')">mettre en évidence les types à remplir</span>
								<span class="popup-item" onclick="rewrite('create:types')">deviner les types à partir du nom des attributs</span>
								<span class="popup-item" onclick="rewrite('delete:types')">supprimer les types</span>
								<span class="popup-item" onclick="rewrite('create:entities')">réparer l'oubli d'entités référencées dans des associations (double clic)</span>
							</div>
						</div>
						<div class="button-with-popup" id="jokerButton">
							<span class="customButton tooltip" onmouseenter="closePopup()" onclick="handleClick(this, 'obfuscate')" style="background-image: url(web/png/joker.png);"><span class="tooltiptext">Masquer</span></span>
							<div class="popup-menu" onmouseleave="closePopup(this)">
								<span class="popup-item popup-close" onclick="closePopup()">⨉</span>
								<span class="popup-item" onclick="rewrite('drown')">masquer avec des libellés génériques numérotés</span>
								<span class="popup-item" onclick="rewrite('delete')" title="Crée un MCD à compléter. À accompagner de la liste des descriptifs des attributs obtenue avec l'option « Dictionnaire des données en Markdown (deux colonnes) ».">masquer les attributs et les cardinalités</span>
								<span class="popup-item" onclick="rewrite('create:types=PLACEHOLDER randomize:types')">remplir les types au hasard</span> <!-- Create the types as an arbitrary NONEMPTY string, then randomize them. -->
								<span class="popup-item" onclick="rewrite('grow:n=9,from_scratch,ent_attrs=3 obfuscate:labels=en4 create:roles lower:roles arrange')">créer un MCD d'entraînement à la conversion en relationnel</span>
								<span class="popup-item" onclick="rewrite('grow:from_scratch,arity_3=1 arrange')">créer un MCD aléatoire avec des libellés génériques numérotés</span>
								<span class="popup-item" onclick="rewrite('obfuscate')">masquer avec du faux texte (double clic)</span>
							</div>
						</div>
						<div class="button-with-popup" id="explodeButton" style="display: none;">
							<span class="customButton tooltip explosion-call" onmouseenter="closePopup()" onclick="handleClick(this, 'explode:arity=3 arrange')" style="background-image: url(web/png/explode.png);">
								<span class="tooltiptext">Décomposer</span>
							</span>
							<div class="popup-menu" onmouseleave="closePopup(this)">
								<span class="popup-item popup-close" onclick="closePopup()">⨉</span>
								<span class="popup-item" onclick="rewrite('drain')">drainer les DF porteuses d'attributs</span>
								<span class="popup-item" onclick="rewrite('split arrange')">décomposer les DF ternaires et plus</span>
								<span class="popup-item explosion-call" onclick="rewrite('explode:arity=3 arrange')">décomposer les non-DF ternaires et plus (double clic)</span>
								<span class="popup-item explosion-call" onclick="rewrite('explode:arity=2.5 arrange')">décomposer les non-DF binaires et plus porteuses d'attributs</span>
								<span class="popup-item explosion-call" onclick="rewrite('explode:arity=2 arrange')">décomposer toutes les non-DF binaires et plus</span>
							</div>
						</div>
					</div>
					<div id="aboutContents" class="contents">
						<p style="height: 2em;"><a class="github-button" href="https://github.com/laowantong/mocodo" data-icon="octicon-star" data-show-count="true" aria-label="Star laowantong/mocodo on GitHub">Star</a></p>
						<p>Mocodo est un logiciel d'aide à l'enseignement et à l'apprentissage des <a href="https://fr.wikipedia.org/wiki/Base_de_données_relationnelle">bases de données relationnelles</a>.</p>
						<ul>
							<li>En entrée, il prend un <a href="https://fr.wikipedia.org/wiki/Modèle_entité-association">MCD</a> (modèle conceptuel de données) décrit dans un langage dédié minimaliste.</li>
							<li>En sortie, il produit un diagramme entité-association et, à la demande, un <a href="https://fr.wikipedia.org/wiki/Merise_(informatique)#MLD_:_modèle_logique_des_données">MLD</a> (schéma relationnel, sous forme graphique ou textuelle), un <a href="https://fr.wikipedia.org/wiki/Langage_de_définition_de_données">DDL</a> (script SQL de création de la base), un <a href="https://fr.wikipedia.org/wiki/Diagramme_de_classes">diagramme de classes UML</a>, etc.</li>
							<li>En bonus, il est capable de réarranger automatiquement votre MCD de façon esthétique, et de lui appliquer des opérations de réécriture qui vont du mondain (typographie) à l'académique (décomposition d'associations), en passant par le merveilleux (inférence de types, génération d'exercices et d'exemples).</li>
						</ul>
						<p>Ce site est prévu pour une utilisation basique et occasionnelle, typiquement en salle de classe. Si vous travaillez sur des données confidentielles¹, ou souhaitez avoir accès à toutes les fonctionnalités de Mocodo, vous pouvez, soit l'importer sous <a href="https://www.basthon.fr">Basthon</a>, soit l'installer sur votre ordinateur :</p>
						<br />
						<pre>&gt; pip install mocodo</pre>
						<br />
						<p>Sous cette dernière forme, Mocodo est un puissant <a href="https://fr.wikipedia.org/wiki/Interface_en_ligne_de_commande">logiciel en ligne de commande</a>, multiplateforme, <a href="https://github.com/laowantong/mocodo"><i>open-source</i></a>, <a href="https://fr.wikipedia.org/wiki/Licence_MIT">libre</a> et gratuit. Il s'intègre particulièrement bien à l'environnement <a href="https://jupyter.org">Jupyter Notebook</a>.</p>
						<br />
						<p>Pour en savoir plus, suivez nos tutoriels interactifs (onglet Entrée), puis plongez-vous dans la <a target="_blank" href="https://rawgit.com/laowantong/mocodo/master/doc/fr_refman.html">documentation</a>.</p>
						<br />
						<p style="font-size: small; font-style: italic; text-align: right;">Aristide Grange, Université de Lorraine, Metz (France)</p>
						<div class="footnote">
							<hr>
							<p>¹ Ce site stocke dans votre navigateur un <a href="https://www.cnil.fr/fr/cookies-et-autres-traceurs/regles/cookies/que-dit-la-loi">cookie non soumis à obligation de consentement préalable</a> qui lui permet de retrouver vos réglages de l'onglet Options. Côté serveur, il stocke le dernier état de votre travail afin de le mettre à votre disposition sous forme d'archive téléchargeable. Ce dossier est détruit au bout de 24 heures. Pour le détruire dès la fin d'une session, effacez le texte d'entrée et pressez le bouton de rafraîchissement. Sous Basthon ou en local, rien ne quitte votre ordinateur.</p>
						</div>
					</div>
					<div id="inputContents" class="contents">
						<div id="inputPane">
							<div><input type="text" oninput="markAsDirty();get_from_lib()" onfocus="onFocus(this)" name="title" id="title" value="MCD" onblur="onBlur(this)" autocomplete="off" /></div>
							<select onchange="changeTitleToNthTuto();get_from_lib()" name="tutorial" id="tutorial" title="Parcourez notre galerie de MCD pour apprendre la syntaxe de Mocodo."></select>
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
						<div class="settings-pane">
							<div class="setting-row">
								<label class="setting-label" for="shapes">Police et proportions</label>
								<div class="setting-controls">
									<select onchange="markAsDirty();writeCookie()" name="shapes" id="shapes">
										<!-- To be populated by JS -->
									</select>
								</div>
							</div>
							<div class="setting-row">
								<label class="setting-label" for="colors">Palette de couleurs</label>
								<div class="setting-controls">
									<select onchange="markAsDirty();writeCookie()" name="colors" id="colors">
										<!-- To be populated by JS -->
									</select>
								</div>
							</div>
							<div class="setting-row">
								<label class="setting-label" for="flashlight">Mode nuit</label>
								<div class="setting-controls">
									<input type="checkbox" id="flashlight" onclick="switchOnFlashlight(event)" />
								</div>
							</div>
							<div class="setting-row">
								<label class="setting-label" for="adjust_width">Ajustement de la largeur des libellés</label>
								<div class="setting-controls">
									<input type="number" value="1.00" max="2.00" min="0.50" step="0.01" onchange="writeCookie()" name="adjust_width" id="adjust_width" style="width: 5em; border-radius: 0;" />
								</div>
							</div>
							<div class="setting-row">
								<label class="setting-label" for="detect_overlaps" title="Lève une erreur en cas de chevauchement de pattes horizontales ou verticales.">Détection des chevauchements</label>
								<div class="setting-controls">
									<input type="checkbox" name="detect_overlaps" id="detect_overlaps" onchange="markAsDirty();writeCookie()" checked />
								</div>
							</div>
							<div class="setting-row">
								<label class="setting-label" title="Les formats cochés seront générés et inclus dans l'archive téléchargée.">Format des images en sortie</label>
								<div class="setting-row">
									<span>
										<input type="checkbox" disabled="true" id="svg" checked />
										<label for="svg" title="Pour le web, zoom illimité. Requis.">&nbsp;SVG&nbsp;&nbsp;</label>
										<input type="checkbox" name="png" id="png" onchange="markAsDirty();writeCookie()" />
										<label for="png" title="Multi-usage, zoom limité.">&nbsp;PNG&nbsp;&nbsp;</label>
										<input type="checkbox" name="pdf" id="pdf" onchange="markAsDirty();writeCookie()" />
										<label for="pdf" title="Pour l'impression, zoom illimité.">&nbsp;PDF&nbsp;&nbsp;</label>
									</span>
								</div>
							</div>
							<div class="setting-row">
								<label class="setting-label" for="conversions" title="Les formats cochés seront affichés sous l'onglet « Autres sorties » et inclus dans l'archive téléchargée.">Conversions en sortie</label>
								<ul class="setting-controls" name="conversions" id="conversions">
									<!-- To be populated by JS -->
									<details class="setting-details">
										<summary>Autres options de conversions…</summary>
										<!-- To be populated by JS -->
									</details>
								</ul>
							</div>
							<div class="setting-row">
								<label class="setting-label" for="knowledge" title="Vous pouvez adapter les traitements et l'interface de Mocodo online à des besoins plus avancés.">Utilisation avancée</label>
								<details class="setting-details">
									<summary>Découvrir…</summary>
									<ul class="setting-controls" name="knowledge" id="knowledge">
										<!-- To be populated by JS -->
									</ul>
								</details>
							</div>
							<div class="setting-row">
								<label class="setting-label" for="lib" title="URL d'un répertoire distant. Si l'utilisateur modifie le titre du MCD, Mocodo y cherchera un fichier de même nom (extension '.mcd' facultative) et, s'il existe, remplacera le texte d'entrée par son contenu.">Bibliothèque de MCD</label>
								<div class="setting-controls">
									<input type="url" name="lib" id="lib" onchange="markAsDirty();writeCookie()" placeholder="https://your_server.com/path/to/your/mcd/directory"
									pattern="[Hh][Tt][Tt][Pp][Ss]?:\/\/(?:(?:[a-zA-Z\u00a1-\uffff0-9]+-?)*[a-zA-Z\u00a1-\uffff0-9]+)(?:\.(?:[a-zA-Z\u00a1-\uffff0-9]+-?)*[a-zA-Z\u00a1-\uffff0-9]+)*(?:\.(?:[a-zA-Z\u00a1-\uffff]{2,}))(?::\d{2,5})?(?:\/[^\s]*)?" />
								</div>
							</div>
							<div style="display: none;">
								<select onchange="markAsDirty();writeCookie()" name="sql_case" id="sql_case">
									<option selected="selected">snake_case</option>
									<option>camelCase</option>
									<option>PascalCase</option>
								</select>
								<select onchange="markAsDirty();writeCookie()" name="fk_format" id="fk_format">
									<option value="#{label}" selected="selected">avec # au début</option>
									<option value="{label}#">avec # à la fin</option>
									<option value="{label}">telles quelles</option>
								</select>
								<select onchange="markAsDirty();writeCookie()" name="strengthen_card" id="strengthen_card">
									<option>1,1</option>
									<option value="_1,1_" selected="selected">1̲,1̲</option>
									<option>(1,1)</option>
									<option>1,1(R)</option>
									<option>1,1🄡</option>
									<option>1,1®</option>
									<option>(R)1,1</option>
									<option>🄡1,1</option>
									<option>®1,1</option>
								</select>
							</div>
						</div>
					</div>
					<div id="geoContents" class="contents">
						<fieldset>
							<legend>Coordonnées du centre des boîtes</legend>
							<div id="coords"></div>
						</fieldset>
						<fieldset>
							<legend>Décalage des cardinalités</legend>
							<div id="cards"></div>
						</fieldset>
						<fieldset>
							<legend>Zone de rognage</legend>
							<div id="size"></div>
						</fieldset>
						<fieldset>
							<legend>Position des flèches des associations</legend>
							<div id="arrows"></div>
						</fieldset>
					</div>
				</div>
			</div>
			<div id="outputZone">
				<div class="line"></div>
				<ul class="tabs">
					<li><a href="#diagramAndSupplementOutput" id="diagramTab" class="first_tab active"><span>Diagramme</span></a></li>
					<li><a href="#convertOutput"><span>Autres sorties</span></a></li>
					<li><a href="#errorOutput" id="errorTab"><span>Erreurs</span></a></li>
				</ul>
				<div class="pane">
					<div id="outputButtons" class="buttons">
						<span class="customButton tooltip" id="refreshButton" onclick="generate()" style="background-image: url(web/png/refresh.png);"><span class="tooltiptext">Rafraîchir</span></span>
						<div id="rotatingButton" style="display: none;">
							<span class="customButton" id="empty" style="background-image: url(web/png/empty.png);"></span>
							<span class="customButton" id="refreshRotatingButton" style="background-image: url(web/png/refresh_rotating.png);"></span>
						</div>
						<a class="customButton tooltip" id="downloadButton" href="" download="" target="_blank" style="background-image: url(web/png/download.png);"><span class="tooltiptext">Télécharger</span></a>
					</div>
					<div id="diagramAndSupplementOutput">
						<div id="diagramOutput" class="contents active never_refreshed"><img src="web/generate_tip.svg" alt="Cliquez sur le bouton de génération pour rafraîchir le MCD" /></div>
						<div id="diagramOutputSupplement" class="contents"></div>
					</div>
					<div id="convertOutput" class="contents never_refreshed"><img src="web/generate_tip.svg" alt="Cliquez sur le bouton de génération pour rafraîchir le MCD" /></div>
					<div id="errorOutput" class="contents"></div>
				</div>
			</div>
		</form>
	</div>
	<div id="navigation">
		<a title="Voir le code sur GitHub." target="_blank" href="https://github.com/laowantong/mocodo">Mocodo <?php echo $version; ?></a>
		&nbsp;∙&nbsp;
		<a href="javascript:void(0);" 
			onclick="sendToBasthon()" 
			title="Ouvrir ce MCD dans un notebook pour accéder à toutes les fonctionnalités du logiciel sans avoir à l'installer."
			style="cursor: pointer; display: inline-block;">
			<img class="inlineIcon" src="web/png/basthon_play.png" alt="Basthon" />
			&nbsp;&nbsp;Basthon
		</a>
		&nbsp;∙&nbsp;
		<a target="_blank" href="https://rawgit.com/laowantong/mocodo/master/doc/fr_refman.html">Documentation</a>
		&nbsp;∙&nbsp;
		<a title="Contacter l'auteur par mail." onclick="alert('Pour envoyer vos compliments à l\'auteur, trouvez d\'abord son nom sous l\'onglet d\'information, puis adressez un mail à prénom.nom@univ-lorraine.fr. Attention, tout problème ou demande concernant le logiciel doit préférablement faire l\'objet d\'une issue GitHub (« Récriminations »).')">Félicitations</a>
		&nbsp;∙&nbsp;
		<a title="Créer une issue GitHub." target="_blank" href="https://github.com/laowantong/mocodo/issues">Récriminations</a>
	</div>
</body>
</html>
