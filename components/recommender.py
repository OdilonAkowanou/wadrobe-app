# components/recommender.py
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

def generer_tenues(liste_vetements, profil=None):
    if len(liste_vetements) < 3:
        return None, "Ajoute au moins 3 vêtements pour générer des tenues !"

    dressing_texte = "\n".join([
        f"- ID:{v[0]} | {v[1]} (catégorie: {v[2]}, couleur: {v[3]}, style: {v[4]})"
        for v in liste_vetements
    ])

    profil_texte = ""
    if profil:
        profil_texte = f"""
Profil :
- Genre : {profil.get('genre', 'Non spécifié')}
- Morphologie : {profil.get('morphologie', 'Non spécifiée')}
- Ville : {profil.get('ville', 'Non spécifiée')}
- Style préféré : {profil.get('style_prefere', 'Non spécifié')}
- Budget : {profil.get('budget', 0)} FCFA
"""

    prompt = f"""
Tu es un styliste expert en mode africaine contemporaine.

{profil_texte}

Voici le dressing avec les IDs :
{dressing_texte}

Réponds UNIQUEMENT avec un JSON valide, sans texte avant ou après.
Format exact :
{{
  "tenues": [
    {{
      "nom": "Nom créatif de la tenue",
      "occasion": "Occasion idéale",
      "pourquoi": "Explication courte pourquoi ça marche",
      "vetements_ids": [1, 2, 3]
    }},
    {{
      "nom": "Nom créatif de la tenue 2",
      "occasion": "Occasion idéale",
      "pourquoi": "Explication courte",
      "vetements_ids": [1, 4]
    }},
    {{
      "nom": "Nom créatif de la tenue 3",
      "occasion": "Occasion idéale",
      "pourquoi": "Explication courte",
      "vetements_ids": [2, 3, 4]
    }}
  ],
  "conseil": "Un conseil sur le prochain vêtement à acheter"
}}

Utilise les vrais IDs des vêtements listés ci-dessus.
"""

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/mistral-nemo",
                "messages": [{"role": "user", "content": prompt}]
            }
        )

        content = response.json()["choices"][0]["message"]["content"]
        
        # Nettoyer le JSON
        content = content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        content = content.strip()
        
        data = json.loads(content)
        return data, None

    except Exception as e:
        try:
            detail = response.json()
        except:
            detail = "pas de réponse"
        return None, f"Erreur : {str(e)} | Détail : {detail}"