# components/classifier.py
from PIL import Image

# Catégories de vêtements
CATEGORIES = [
    "t-shirt", "chemise", "pull", "veste", "manteau",
    "jean", "pantalon", "short", "jupe", "robe",
    "chaussures", "basket", "sandales", "bottes",
    "casquette", "sac", "ceinture"
]

COULEURS = [
    "noir", "blanc", "gris", "bleu", "rouge",
    "vert", "jaune", "orange", "rose", "marron", "beige"
]

STYLES = [
    "casual", "élégant", "sportif", "traditionnel africain"
]

def classifier_image(image_path):
    """
    Pour l'instant retourne une classification manuelle.
    On intégrera CLIP après.
    """
    return {
        "categorie": "à définir",
        "couleur": "à définir",
        "style": "à définir",
        "nom": "nouveau vêtement"
    }