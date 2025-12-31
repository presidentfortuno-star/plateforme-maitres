"""
PLATEFORME MAÎTRES DE MAISON
============================

Application complète avec:
- Espace Maîtres: Créer un compte et ajouter ses coordonnées
- Espace Parents: Chercher et trouver les maîtres

Lancer avec:
  streamlit run app_platform.py
"""

import streamlit as st
import json
import os
from datetime import datetime
import streamlit.components.v1 as components

# Vérification Google Search Console
components.html(
    """
    <script>
        var meta = document.createElement('meta');
        meta.name = "google-site-verification";
        meta.content = "72BQlsL9Ov6yC70acGkWbF_X9LiSTk0dL_hxBQHLcRA";
        parent.document.getElementsByTagName('head')[0].appendChild(meta);
    </script>
    """,
    height=0,
)

# Configuration
st.set_page_config(
    page_title="Plateforme Maîtres de Maison",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)



    


DB_FILE = "maitres_data.json"

# ==================== FONCTIONS DE BASE DE DONNÉES ====================

def charger_donnees():
    """Charger les données des maîtres"""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def sauvegarder_donnees(donnees):
    """Sauvegarder les données"""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(donnees, f, ensure_ascii=False, indent=2)

# ==================== INTERFACE PRINCIPALE ====================

st.title("👨‍🏫 Plateforme Maîtres de Maison")
st.markdown("**Connectez maîtres et parents pour un enseignement de qualité**")

# Sidebar - Sélection de l'espace
st.sidebar.markdown("---")
espace = st.sidebar.radio(
    "**Choisissez votre espace:**",
    ["👨‍👩‍👧 Accueil", "👨‍🏫 Espace Maîtres", "👨‍👩‍👧‍👦 Espace Parents"]
)

# ==================== ACCUEIL ====================

if espace == "👨‍👩‍👧 Accueil":
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 👨‍🏫 Vous êtes Maître de Maison?
        
        - Créez votre compte gratuitement
        - Ajoutez vos compétences
        - Publiez vos coordonnées
        - Trouvez des élèves
        
        **[Allez à l'Espace Maîtres](#)**
        """)
    
    with col2:
        st.markdown("""
        ### 👨‍👩‍👧‍👦 Vous êtes Parent?
        
        - Cherchez des maîtres qualifiés
        - Filtrez par compétence
        - Filtrez par ville
        - Voyez les tarifs et coordonnées
        
        **[Allez à l'Espace Parents](#)**
        """)
    
    st.markdown("---")
    st.markdown("""
    ### 📊 Statistiques
    """)
    
    donnees = charger_donnees()
    nb_maitres = len(donnees)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("👨‍🏫 Maîtres inscrits", nb_maitres)
    col2.metric("📚 Compétences offertes", "maths, français, anglais, informatique...")
    col3.metric("🌍 Villes couvertes", "Abidjan, Bingerville, Cocody...")

# ==================== ESPACE MAÎTRES ====================

elif espace == "👨‍🏫 Espace Maîtres":
    st.header("Créez Votre Profil de Maître")
    
    donnees = charger_donnees()
    
    tab1, tab2 = st.tabs(["S'inscrire/Modifier", "Voir mon profil"])
    
    with tab1:
        st.subheader("Inscription / Modification de profil")
        
        # Formulaire
        col1, col2 = st.columns(2)
        
        with col1:
            nom = st.text_input("**Nom complet**", placeholder="Jean Kouadio")
            email = st.text_input("**Email**", placeholder="jean@example.com")
            telephone = st.text_input("**Téléphone**", placeholder="+225 01 23 45 67")
        
        with col2:
            ville = st.selectbox(
                "**Ville**",
                ["Abidjan", "Bingerville", "Cocody", "Yamoussoukro", "Autre"]
            )
            if ville == "Autre":
                ville = st.text_input("Précisez votre ville")
            
            tarif = st.text_input("**Tarif horaire**", placeholder="3000/h")
        
        # Compétences
        st.subheader("Compétences")
        competences_disponibles = [
            "Mathématiques", "Français", "Anglais", "Physique",
            "Chimie", "Informatique", "SVT", "Histoire",
            "Géographie", "Lecture", "Autre"
        ]
        
        competences = st.multiselect(
            "**Sélectionnez vos compétences**",
            competences_disponibles,
            default=[]
        )
        
        # Description
        description = st.text_area(
            "**Description (optionnel)**",
            placeholder="Parlez de votre expérience, votre pédagogie, etc.",
            height=100
        )
        
        # Bouton Enregistrer
        if st.button("💾 Enregistrer mon profil", use_container_width=True):
            if not nom or not email or not telephone or not competences:
                st.error("❌ Veuillez remplir tous les champs obligatoires!")
            else:
                # Sauvegarder
                donnees[email] = {
                    "nom": nom,
                    "email": email,
                    "telephone": telephone,
                    "ville": ville,
                    "tarif": tarif,
                    "competences": competences,
                    "description": description,
                    "date_inscription": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                sauvegarder_donnees(donnees)
                st.success(f"✅ Profil enregistré! {nom}, bienvenue sur la plateforme!")
                st.balloons()
    
    with tab2:
        st.subheader("Mon Profil")
        email = st.text_input("**Entrez votre email pour voir votre profil**", key="email_view")
        
        if email:
            if email in donnees:
                profil = donnees[email]
                st.success(f"✅ Profil trouvé!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Nom:** {profil['nom']}")
                    st.write(f"**Email:** {profil['email']}")
                    st.write(f"**Téléphone:** {profil['telephone']}")
                
                with col2:
                    st.write(f"**Ville:** {profil['ville']}")
                    st.write(f"**Tarif:** {profil['tarif']}")
                    st.write(f"**Inscription:** {profil['date_inscription']}")
                
                st.write("**Compétences:**")
                st.write(", ".join(profil['competences']))
                
                if profil['description']:
                    st.write("**Description:**")
                    st.write(profil['description'])
            else:
                st.warning("⚠️ Aucun profil trouvé avec cet email. Veuillez d'abord vous inscrire.")

# ==================== ESPACE PARENTS ====================

elif espace == "👨‍👩‍👧‍👦 Espace Parents":
    st.header("Trouvez Votre Maître Idéal")
    
    donnees = charger_donnees()
    
    if not donnees:
        st.info("ℹ️ Aucun maître inscrit pour l'instant. Revenez bientôt!")
    else:
        # Formulaire de recherche
        col1, col2 = st.columns(2)
        
        with col1:
            competence_search = st.multiselect(
                "**Chercher par compétence(s)**",
                ["Mathématiques", "Français", "Anglais", "Physique",
                 "Chimie", "Informatique", "SVT", "Histoire",
                 "Géographie", "Lecture"],
                default=[]
            )
        
        with col2:
            ville_search = st.multiselect(
                "**Chercher par ville**",
                ["Abidjan", "Bingerville", "Cocody", "Yamoussoukro"],
                default=[]
            )
        
        # Bouton Chercher
        if st.button("🔍 Chercher", use_container_width=True):
            resultats = []
            
            for email, profil in donnees.items():
                # Vérifier la compétence
                comp_ok = (not competence_search) or any(
                    comp in profil['competences'] for comp in competence_search
                )
                
                # Vérifier la ville
                ville_ok = (not ville_search) or (profil['ville'] in ville_search)
                
                if comp_ok and ville_ok:
                    resultats.append(profil)
            
            # Afficher les résultats
            st.markdown("---")
            
            if not resultats:
                st.warning("❌ Aucun maître trouvé avec ces critères.")
                st.info("Essayez d'autres critères de recherche!")
            else:
                st.success(f"✅ {len(resultats)} maître(s) trouvé(s)!")
                
                # Afficher chaque maître
                for profil in resultats:
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"### 👤 {profil['nom']}")
                            st.write(f"📍 **Ville:** {profil['ville']}")
                            st.write(f"💰 **Tarif:** {profil['tarif']}")
                            st.write(f"📚 **Compétences:** {', '.join(profil['competences'])}")
                            
                            if profil['description']:
                                st.write(f"✍️ **À propos:** {profil['description']}")
                        
                        with col2:
                            st.markdown("""
                            **Contacter:**
                            """)
                            st.write(f"📧 {profil['email']}")
                            st.write(f"📱 {profil['telephone']}")
                        
                        st.divider()
        
        # Afficher tous les maîtres
        st.markdown("---")
        st.subheader("📋 Tous les maîtres inscrits")
        
        for email, profil in donnees.items():
            with st.expander(f"👤 {profil['nom']} - {profil['ville']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Email:** {profil['email']}")
                    st.write(f"**Téléphone:** {profil['telephone']}")
                    st.write(f"**Tarif:** {profil['tarif']}")
                
                with col2:
                    st.write(f"**Compétences:** {', '.join(profil['competences'])}")
                    st.write(f"**Inscription:** {profil['date_inscription']}")
                
                if profil['description']:
                    st.write(f"**Description:** {profil['description']}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><small>© 2025 Plateforme Maîtres de Maison | Version 2.0 | 📱 Responsive</small></p>
</div>
""", unsafe_allow_html=True)

