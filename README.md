# Project overview
Named entity recognition on the french corpus _POLUX_ (_Politiques X Universités_).

## Documentation
Please read [full documentation](doc/documentation.md).

You can run [this script](doc/generate_doc.py) to update documentation from the source code:

## ETAT DU PROJET 
# Guide d’utilisation du Pipeline

Ce projet met en place un pipeline qui enchaîne plusieurs étapes pour traiter des documents et, selon la commande choisie, effectuer des opérations comme l’extraction de texte ou la reconnaissance d’entités nommées (NER). Toutefois, dans notre cas, la NER n’a pas pu être rendue fonctionnelle. Voici un aperçu du fonctionnement global et des difficultés rencontrées.

## Sommaire

1. [Présentation générale du pipeline](#1-présentation-générale-du-pipeline)  
2. [Classes de commande : Fetcher et NerMotor](#2-classes-de-commande--fetcher-et-nermotor)  
3. [Définitions de types et validation](#3-définitions-de-types-et-validation)  
4. [Utilitaires annexes](#4-utilitaires-annexes)  
5. [Problèmes rencontrés autour de la NER](#5-problèmes-rencontrés-autour-de-la-ner)  
6. [Ce qui fonctionne malgré tout](#6-ce-qui-fonctionne-malgré-tout)

---

## 1. Présentation générale du pipeline

Le pipeline se compose principalement d’un fichier `pipeline.py` (ou `utils/pipeline.py`) proposant deux fonctions :

### a. `cli()`
- Lit les arguments en ligne de commande grâce à `argparse` :  
  - `command` : nom de la commande à exécuter (`fetch` ou `ner`)  
  - `--input` : chemin d’un fichier JSON lines en entrée  
  - `--output` : répertoire de sortie  
  - `--files` : chemin vers les fichiers bruts à traiter  
- Vérifie que l’entrée (`--input`) correspond bien à un `.json` et qu’elle existe.  
- Crée un répertoire de sortie (via `make_output(...)`).
- Charge la commande (par exemple `load_cmd(args.command)`).
- Retourne un objet `argparse.Namespace` regroupant tout ce dont le reste du pipeline a besoin (la commande, le logger, etc.).

### b. `pipe(env)`
- Ouvre le fichier d’entrée (`env.input_path`) et le fichier de sortie (`env.output_path`).  
- Pour chaque ligne du fichier d’entrée :  
  1. Parse la ligne JSON pour obtenir un dictionnaire.  
  2. Transforme ce dictionnaire en un objet `Document`.  
  3. Traite ce document en appelant `env.cmd.process(doc)`.  
  4. Écrit le document mis à jour dans le fichier de sortie.  
- Affiche un récapitulatif final sur le nombre de documents traités et logge tous les événements importants.

---

## 2. Classes de commande : Fetcher et NerMotor

### a. `Fetcher`
- Lit un document sur le disque (HTML, PDF ou TXT).  
- Extrait le texte en interne (fonctions privées comme `__fetch_html`, `__fetch_pdf`, `__fetch_txt`).  
- Met à jour le champ `text` du document avec le contenu extrait.

### b. `NerMotor`
- Parcourt (en théorie) le champ `doc.text` afin d’identifier les entités nommées (LOC) via trois modèles : **Flair**, **Spacy** et **Stanza**.
- Stocke la liste des positions `[start, end]` pour chaque entité dans des champs `doc.locs["flair"]`, `doc.locs["spacy"]`, `doc.locs["stanza"]`.

---

## 3. Définitions de types et validation

Plusieurs éléments du code utilisent des métaclasses ou Pydantic pour :
- Valider la taille du fichier et son **hash** (Blake3).  
- Gérer les énumérations (ex. `Author`, `DocumentType`, `NerModel`).  
- Vérifier que le document respecte la structure attendue (champs `id`, `text`, etc.).  

En cas de non-respect (fichier manquant, taille non conforme, etc.), une exception est levée et le pipeline s’arrête.

---

## 4. Utilitaires annexes

- **`hash_file(file)`** : calcule et retourne un hash (Blake3) au format hexadécimal de 64 caractères.  
- **`count_lines(file)`** : compte le nombre de lignes dans un flux en lecture, puis se replace au point initial.  
- **`create_logger(...)`** : crée un logger Python pour générer un CSV (`log.csv`) retraçant les actions et erreurs survenues pendant l’exécution.

---

## 5. Problèmes rencontrés autour de la NER

Plusieurs points ont empêché l’implémentation de la NER de fonctionner :

1. **Utilisation d’une variable `doc_metadata` inexistante**  
   - Dans certains endroits du code, la reconnaissance fait référence à `doc_metadata["text"]` au lieu de `doc.text`.  
   - Cette variable `doc_metadata` n’est pas définie, et il est donc impossible de récupérer le texte.

2. **Accès en mode dictionnaire sur un objet Pydantic**  
   - Le code tente parfois de modifier les champs du document en utilisant `doc["locs"][...]`, ce qui n’est pas possible si `doc` est un objet Pydantic.  
   - Cette confusion empêche le stockage correct des entités détectées.

3. **Variable `files` non initialisée**  
   - Dans le `cli()`, la variable `files` n’est jamais correctement alimentée alors que `args.files` devrait être utilisée.  
   - Sans un chemin valide, la recherche ou l’ouverture de fichiers devient incohérente.

4. **Incohérences de nommage**  
   - On retrouve parfois le terme “ner” ou “NER” selon les endroits du code.  
   - Cette différence peut casser l’enchaînement de commande ou les imports locaux.

5. **Répartition des imports et déclarations en doublon**  
   - Spacy, Stanza et d’autres éléments sont importés plusieurs fois dans différentes sections.  
   - Les définitions d’enums ou de classes se répètent, ce qui complique la lecture et peut provoquer des conflits.

Dans l’état actuel, ces différents problèmes s’additionnent et empêchent la NER de produire le résultat attendu.

---

## 6. Ce qui fonctionne malgré tout

- **La commande `fetch`** :  
  L’extraction de texte (HTML, PDF, TXT) se lance correctement et permet de remplir le champ `text`.  

- **La validation Pydantic** :  
  Les contrôles de taille, de hash ou de métadonnées fonctionnent et peuvent interrompre le pipeline si un document n’est pas conforme.  

- **Le logging et l’export JSON** :  
  Les documents transformés sont bien réécrits au format JSON et les logs sont générés dans un fichier CSV, assurant un suivi des erreurs et des étapes franchies.

En dépit de ces éléments positifs, la partie NER n’a pas pu aboutir pour les raisons listées ci-dessus.

```bash
user% cd polux24_loc
user% python3 doc/generate_doc.py
```

## Credits
2024, [MIT Licence](https://opensource.org/license/mit):
- By [Camille Monnot](https://github.com/Rber085) & [Adrien Vergne](https://github.com/TeaS0710)
- Dir. [Caroline Koudouro-Parfait](https://github.com/carolinekoudoroparfait) & [Gaël Lejeune](https://github.com/rundimeco).


