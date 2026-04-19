## Note sur llama.cpp et git

Pour éviter d'ajouter tout le dossier `llama.cpp` dans votre dépôt principal, il est recommandé d'utiliser un sous-module git :

```bash
git submodule add https://github.com/ggerganov/llama.cpp llama.cpp
```

Si vous avez déjà ajouté le dossier par erreur :

```bash
git rm --cached -r llama.cpp
git submodule add https://github.com/ggerganov/llama.cpp llama.cpp
```

Après un clonage, initialisez les sous-modules avec :

```bash
git submodule update --init --recursive
```

# PicoGPT1 Scratch — Entraînement et Conversion d'un Mini GPT-2

Ce projet montre comment entraîner un petit modèle GPT-2 sur un dataset d'instructions/réponses, puis le convertir au format GGUF pour une utilisation avec llama.cpp.

## 1. Préparation du dataset

Le script `prepare_dataset.py` télécharge un sous-ensemble du dataset [tatsu-lab/alpaca](https://huggingface.co/datasets/tatsu-lab/alpaca) et le convertit au format texte attendu :

```
<prompt>
<réponse>

<prompt>
<réponse>
...etc
```

Exécutez :

```bash
python prepare_dataset.py
```

Cela crée le fichier `train.txt`.

## 2. Entraînement du modèle

L'entraînement se fait dans le notebook `train.ipynb`.

Étapes principales :
- Chargement du tokenizer GPT-2
- Chargement et formatage du dataset
- Définition d'une petite architecture GPT-2 (2 couches, 128 dimensions)
- Entraînement avec HuggingFace Transformers (`Trainer`)
- Sauvegarde du modèle et du tokenizer dans le dossier `PicoGPT/`

Ouvrez et exécutez toutes les cellules de `train.ipynb`.

## 3. Tester le modèle

Le notebook `test.ipynb` permet de charger le modèle entraîné et de générer des réponses à partir de prompts personnalisés.

Modifiez la variable `prompt` dans le notebook pour tester différents cas.



## 4. Conversion et utilisation avec Ollama

### Conversion au format GGUF
Pour utiliser le modèle avec [llama.cpp](https://github.com/ggerganov/llama.cpp) ou l'uploader sur Ollama, il faut le convertir au format GGUF.

Le script `convert_to_gguf.py` utilise le script officiel de conversion de llama.cpp (`convert_hf_to_gguf.py`).

Avant de lancer la conversion, vérifiez que le dossier `llama.cpp` (avec le script `convert_hf_to_gguf.py`) est bien présent.

Exemple de commande pour convertir le modèle :

```bash
python convert_to_gguf.py --hf_model_dir PicoGPT --output PicoGPT.gguf
```

Le fichier `.gguf` sera généré dans le dossier courant.

### Création du modèle Ollama
1. Créez un fichier `Modelfile` avec ce contenu :
	 ```
	 FROM ./PicoGPT1-Scratch.gguf
	 SYSTEM You are a friendly assistant.
	 ```
2. Créez le modèle Ollama :
	 ```bash
	 ollama create nazleduc/PicoGPT1-Scratch -f Modelfile
	 ```
	 (Remplacez `nazleduc/PicoGPT1-Scratch` par le nom souhaité)

### Utilisation du modèle avec Ollama
- Pour lancer une session interactive :
	```bash
	ollama run nazleduc/PicoGPT1-Scratch
	```
- Pour utiliser l'API locale :
	```bash
	curl http://localhost:11434/api/generate -d '{
		"model": "nazleduc/PicoGPT1-Scratch",
		"prompt": "What is psychoanalysis?"
	}'
	```
- Pour lister les modèles disponibles :
	```bash
	ollama list
	```

### Suppression du modèle
Pour supprimer le modèle localement :
```bash
ollama rm nazleduc/PicoGPT1-Scratch
```

## 5. Références

- [Vidéo originale](https://www.youtube.com/watch?v=MpHj4UD4kiw)
- [Repo original](https://github.com/hassanhabib/LLMfromNothing)