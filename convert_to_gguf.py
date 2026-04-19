# convert_to_gguf.py
#
# Robust HuggingFace → GGUF conversion using subprocess

"""
Script de conversion HuggingFace -> GGUF pour Ollama/llama.cpp

Usage :
    python convert_to_gguf.py [--llama_cpp_dir PATH] [--hf_model_dir PATH] [--output PATH] [--outtype f16|q4_0|...] 

Exemple pour Ollama :
    python convert_to_gguf.py --hf_model_dir PicoGPT --output PicoGPT.gguf

Ensuite, uploadez le .gguf sur Ollama :
    ollama create <modèle> -f ./PicoGPT.gguf
"""

import argparse
import subprocess
from pathlib import Path
import sys

def main():
    parser = argparse.ArgumentParser(description="Convertit un modèle HuggingFace en GGUF pour Ollama/llama.cpp")
    parser.add_argument('--llama_cpp_dir', type=str, default='llama.cpp', help='Dossier contenant llama.cpp et convert_hf_to_gguf.py')
    parser.add_argument('--hf_model_dir', type=str, default='PicoGPT1-Scratch', help='Dossier du modèle HuggingFace à convertir')
    parser.add_argument('--output', type=str, default='PicoGPT1-Scratch.gguf', help='Nom du fichier GGUF de sortie')
    parser.add_argument('--outtype', type=str, default='f16', help='Type de poids de sortie (f16, q4_0, q8_0, etc.)')
    args = parser.parse_args()

    llama_cpp_dir = Path(args.llama_cpp_dir)
    hf_model_dir = Path(args.hf_model_dir)
    output_gguf = Path(args.output)
    outtype = args.outtype

    converter = llama_cpp_dir / "convert_hf_to_gguf.py"
    if not converter.exists():
        print(f"[ERREUR] Le script convert_hf_to_gguf.py est introuvable dans {llama_cpp_dir}")
        print("Clonez llama.cpp : git clone https://github.com/ggerganov/llama.cpp")
        sys.exit(1)

    if not hf_model_dir.exists():
        print(f"[ERREUR] Le dossier du modèle HuggingFace {hf_model_dir} est introuvable.")
        sys.exit(1)

    cmd = [
        sys.executable,
        str(converter),
        str(hf_model_dir),
        "--outfile", str(output_gguf),
        "--outtype", outtype,
    ]

    print("[INFO] Lancement de la conversion GGUF :")
    print(" ".join(cmd))
    print()
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        print("[ERREUR] La conversion a échoué.")
        sys.exit(e.returncode)

    print(f"\n[SUCCÈS] Conversion terminée. Fichier généré : {output_gguf}")
    print("\nPour uploader sur Ollama :")
    print(f"  ollama create <nom> -f ./{output_gguf}")

if __name__ == "__main__":
    main()
