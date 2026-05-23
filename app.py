# app.py
import streamlit as st
import os
from PIL import Image
from components.database import init_db, ajouter_vetement, get_tous_vetements, supprimer_vetement
from components.classifier import classifier_image, CATEGORIES, COULEURS, STYLES
from components.recommender import generer_tenues

# --- Configuration ---
st.set_page_config(
    page_title="Mon Dressing Intelligent",
    page_icon="👗",
    layout="wide"
)

# Initialiser la base de données
init_db()
os.makedirs("uploads", exist_ok=True)

# --- Titre ---
st.title("👗 Mon Dressing Intelligent")
st.caption("Ajoute tes vêtements et découvre des tenues stylées")

# --- Navigation ---
page = st.sidebar.selectbox(
    "Navigation",
    ["👤 Mon Profil", "➕ Ajouter un vêtement", "👚 Mon Dressing", "✨ Générer des tenues"]
)

# ============================================
# PAGE 0 : Mon Profil
# ============================================
if page == "👤 Mon Profil":
    st.header("👤 Mon Profil")

    col1, col2 = st.columns(2)

    with col1:
        genre = st.selectbox(
            "Je suis",
            ["Homme", "Femme", "Non spécifié"]
        )

        morphologie = st.selectbox(
            "Ma morphologie",
            ["Mince", "Athlétique", "Normale", "Ronde"]
        )

    with col2:
        ville = st.text_input("Ma ville", placeholder="Ex: Cotonou, Dakar, Abidjan...")

        style_prefere = st.selectbox(
            "Mon style préféré",
            ["Casual", "Élégant", "Sportif", "Traditionnel africain", "Mixte"]
        )

    budget = st.slider(
        "Mon budget mensuel vêtements (FCFA)",
        min_value=0,
        max_value=100000,
        value=20000,
        step=5000
    )

    if st.button("💾 Sauvegarder mon profil"):
        st.session_state["profil"] = {
            "genre": genre,
            "morphologie": morphologie,
            "ville": ville,
            "style_prefere": style_prefere,
            "budget": budget
        }
        st.success("✅ Profil sauvegardé !")
        st.balloons()

    # Afficher le profil actuel
    if "profil" in st.session_state:
        st.divider()
        st.subheader("Ton profil actuel :")
        p = st.session_state["profil"]
        col1, col2, col3 = st.columns(3)
        col1.metric("Genre", p["genre"])
        col2.metric("Ville", p["ville"] if p["ville"] else "Non renseigné")
        col3.metric("Budget", f"{p['budget']:,} FCFA")

# ============================================
# PAGE 1 : Ajouter un vêtement
# ============================================
if page == "➕ Ajouter un vêtement":
    st.header("Ajoute un vêtement à ton dressing")

    photo = st.file_uploader(
        "📷 Prends une photo de ton vêtement",
        type=["jpg", "jpeg", "png"]
    )

    if photo:
        image = Image.open(photo)
        st.image(image, caption="Ta photo", width=300)

        # Sauvegarde la photo
        image_path = f"uploads/{photo.name}"
        image.save(image_path)

        st.subheader("Remplis les informations :")

        nom = st.text_input("Nom du vêtement", value="Mon vêtement")
        categorie = st.selectbox("Catégorie", CATEGORIES)
        couleur = st.selectbox("Couleur", COULEURS)
        style = st.selectbox("Style", STYLES)

        if st.button("💾 Sauvegarder dans mon dressing"):
            ajouter_vetement(nom, categorie, couleur, style, image_path)
            st.success(f"✅ {nom} ajouté à ton dressing !")
            st.balloons()

# ============================================
# PAGE 2 : Mon Dressing
# ============================================
elif page == "👚 Mon Dressing":
    st.header("Ton Dressing")

    vetements = get_tous_vetements()

    if not vetements:
        st.info("Ton dressing est vide. Commence par ajouter des vêtements !")
    else:
        st.write(f"**{len(vetements)} vêtements** dans ton dressing")

        cols = st.columns(3)
        for i, vetement in enumerate(vetements):
            with cols[i % 3]:
                if os.path.exists(vetement[5]):
                    st.image(vetement[5], caption=vetement[1], width=300)
                else:
                    st.write("📷 Photo non disponible")
                st.write(f"📁 {vetement[2]} | 🎨 {vetement[3]} | 🎯 {vetement[4]}")
                if st.button(f"🗑️ Supprimer", key=f"del_{vetement[0]}"):
                    supprimer_vetement(vetement[0])
                    st.rerun()

# ============================================
# PAGE 3 : Générer des tenues
# ============================================
elif page == "✨ Générer des tenues":
    st.header("✨ Tenues suggérées")

    vetements = get_tous_vetements()

    if len(vetements) < 3:
        st.warning("Ajoute au moins 3 vêtements pour générer des tenues !")
    else:
        st.write(f"L'IA va créer des tenues avec tes **{len(vetements)} vêtements**")

        if st.button("🎨 Générer mes tenues"):
            with st.spinner("L'IA réfléchit à tes meilleures tenues..."):
                profil = st.session_state.get("profil", None)
                data, erreur = generer_tenues(vetements, profil)

                if erreur:
                    st.error(erreur)

                elif data:
                    # Créer un dictionnaire id → vêtement pour accès rapide
                    vetements_dict = {v[0]: v for v in vetements}

                    # Afficher chaque tenue en carte
                    for i, tenue in enumerate(data["tenues"]):
                        st.divider()
                        st.subheader(f"👗 Tenue {i+1} — {tenue['nom']}")

                        col_info, col_photos = st.columns([1, 2])

                        with col_info:
                            st.write(f"📅 **Occasion :** {tenue['occasion']}")
                            st.write(f"✅ **Pourquoi ça marche :** {tenue['pourquoi']}")

                        with col_photos:
                            # Afficher les photos des vêtements de cette tenue
                            ids = tenue.get("vetements_ids", [])
                            photos_cols = st.columns(len(ids)) if ids else []

                            for j, vid in enumerate(ids):
                                if vid in vetements_dict:
                                    v = vetements_dict[vid]
                                    with photos_cols[j]:
                                        if os.path.exists(v[5]):
                                            st.image(v[5], caption=v[1], width=150)
                                        else:
                                            st.write(f"👕 {v[1]}")
                                        st.caption(f"{v[3]} • {v[2]}")

                    # Conseil final
                    st.divider()
                    st.info(f"💡 **Conseil prochain achat :** {data['conseil']}")