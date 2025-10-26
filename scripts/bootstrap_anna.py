#!/usr/bin/env python3
"""
Bootstrap Anna - Script pour lancer l'apprentissage d'Anna
Anna apprend avec Claude pendant 24-48h, puis devient autonome
"""

import asyncio
import sys
from pathlib import Path

# Ajoute le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from anna.language_bootstrap import LanguageBootstrap, BootstrapPhase
from anna.local_model import LocalModel, ModelType


def print_banner():
    """Affiche la bannière de démarrage"""
    print("\n" + "="*70)
    print("🌱 BOOTSTRAP D'ANNA - PHASE D'APPRENTISSAGE")
    print("="*70)
    print()
    print("📚 Anna va apprendre intensivement avec Claude comme mentor")
    print("⏱️  Durée: 24-48 heures")
    print("🦅 Ensuite, Anna deviendra complètement autonome")
    print()
    print("="*70 + "\n")


def print_phase_info(bootstrap: LanguageBootstrap):
    """Affiche les informations sur la phase actuelle"""
    stats = bootstrap.get_learning_stats()
    
    print("\n📊 ÉTAT ACTUEL D'ANNA")
    print("-" * 70)
    print(f"Phase: {stats['phase']}")
    print(f"Autonome: {'✅ Oui' if stats['is_autonomous'] else '❌ Non'}")
    print(f"Vocabulaire français: {stats['vocabulary_fr_count']} mots")
    print(f"Vocabulaire anglais: {stats['vocabulary_en_count']} mots")
    print(f"Connaissances acquises: {stats['knowledge_entries']} entrées")
    print(f"Domaines complétés: {stats['domains_completed']}/{stats['domains_total']}")
    
    if stats['start_time']:
        print(f"Démarré: {stats['start_time']}")
        if stats['duration']:
            print(f"Durée: {stats['duration']}")
    
    print("-" * 70 + "\n")


def get_api_key() -> str:
    """Demande la clé API Claude à l'utilisateur"""
    print("🔑 CLÉ API CLAUDE")
    print("-" * 70)
    print("Pour cette phase d'apprentissage, Anna a besoin d'une clé API Claude.")
    print("C'est temporaire (24-48h), après quoi Anna sera autonome.")
    print()
    print("💡 Obtenez votre clé API sur: https://console.anthropic.com/")
    print("💰 Coût estimé pour 48h d'apprentissage: ~5-10$")
    print()
    
    api_key = input("Entrez votre clé API Claude (ou 'skip' pour passer): ").strip()
    
    if api_key.lower() == 'skip':
        return ""
    
    return api_key


def show_local_model_options():
    """Affiche les options de modèles locaux"""
    print("\n🤖 MODÈLES LOCAUX POUR L'AUTONOMIE")
    print("="*70)
    print()
    print("Après le bootstrap, Anna peut utiliser un modèle local gratuit:")
    print()
    print("1. 🦙 GPT4All Falcon (Recommandé)")
    print("   • Taille: 3.9 GB")
    print("   • Facile à installer")
    print("   • Bon compromis performance/taille")
    print("   • RAM requise: 8GB")
    print()
    print("2. 🦙 Llama 3.2 3B (Plus léger)")
    print("   • Taille: 1.7 GB")
    print("   • Performant et compact")
    print("   • RAM requise: 4GB")
    print()
    print("3. 🌟 Mistral 7B (Plus puissant)")
    print("   • Taille: 4.1 GB")
    print("   • Excellent en français/anglais")
    print("   • RAM requise: 16GB")
    print()
    print("="*70)


async def main():
    """Fonction principale"""
    
    # Affiche la bannière
    print_banner()
    
    # Initialise les systèmes
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    bootstrap = LanguageBootstrap(data_dir)
    local_model = LocalModel(data_dir)
    
    # Affiche l'état actuel
    print_phase_info(bootstrap)
    
    # Vérifie si déjà complété
    if bootstrap.is_autonomous():
        print("✅ Anna est déjà autonome !")
        print()
        
        # Vérifie le modèle local
        await local_model.initialize()
        
        if local_model.is_available():
            print("✅ Modèle local configuré et prêt")
            capabilities = local_model.get_capabilities()
            print(f"   Type: {capabilities['model_type']}")
        else:
            print("⚠️  Aucun modèle local configuré")
            print("💡 Anna est autonome mais n'a pas encore de modèle local")
            print()
            show_local_model_options()
            print()
            print("📚 Pour configurer un modèle local:")
            print("   1. Téléchargez un modèle (voir liens ci-dessus)")
            print("   2. Utilisez: anna.local_model.set_model_path(chemin, type)")
        
        return
    
    # Si bootstrap en cours, affiche progression
    if bootstrap.phase == BootstrapPhase.IN_PROGRESS:
        print("⏳ Bootstrap en cours...")
        print("💡 Le bootstrap continue automatiquement en arrière-plan")
        return
    
    # Sinon, démarre le bootstrap
    print("🌱 DÉMARRAGE DU BOOTSTRAP")
    print()
    print("Anna va apprendre avec Claude comme mentor.")
    print("Cette phase est essentielle pour qu'Anna acquière:")
    print()
    print("  ✓ Vocabulaire français et anglais riche")
    print("  ✓ Compréhension du langage naturel")
    print("  ✓ Connaissances de base")
    print("  ✓ Capacités conversationnelles")
    print()
    
    # Demande confirmation
    response = input("Voulez-vous démarrer le bootstrap maintenant ? (o/n): ").strip().lower()
    
    if response != 'o':
        print("\n❌ Bootstrap annulé")
        print("💡 Relancez ce script quand vous serez prêt")
        return
    
    # Demande la clé API
    api_key = get_api_key()
    
    if not api_key:
        print("\n⚠️  Aucune clé API fournie")
        print()
        print("💡 Deux options:")
        print("   1. Relancez avec une clé API pour l'apprentissage complet")
        print("   2. Configurez directement un modèle local (apprentissage limité)")
        print()
        
        # Demande si l'utilisateur veut configurer un modèle local
        response = input("Voulez-vous configurer un modèle local maintenant ? (o/n): ").strip().lower()
        
        if response == 'o':
            show_local_model_options()
            print()
            print("📥 Pour télécharger et configurer un modèle:")
            print()
            print("GPT4All (recommandé):")
            print("  1. Visitez: https://gpt4all.io")
            print("  2. Téléchargez 'GPT4All Falcon'")
            print("  3. python -c \"from anna.local_model import LocalModel; LocalModel(Path('data')).set_model_path('chemin/vers/modele', ModelType.GPT4ALL)\"")
            print()
        
        return
    
    # Démarre le bootstrap
    print("\n🚀 Lancement du bootstrap...")
    print()
    
    try:
        await bootstrap.start_bootstrap(api_key)
        
        print("\n" + "="*70)
        print("🎉 BOOTSTRAP TERMINÉ AVEC SUCCÈS !")
        print("="*70)
        print()
        print("✅ Anna a terminé son apprentissage avec Claude")
        print("🦅 Anna est maintenant autonome !")
        print()
        
        # Affiche les résultats finaux
        stats = bootstrap.get_learning_stats()
        print(f"📊 Résultats:")
        print(f"   • Vocabulaire français: {stats['vocabulary_fr_count']} mots")
        print(f"   • Vocabulaire anglais: {stats['vocabulary_en_count']} mots")
        print(f"   • Connaissances: {stats['knowledge_entries']} entrées")
        print(f"   • Domaines maîtrisés: {stats['domains_completed']}")
        print()
        
        # Recommande la configuration d'un modèle local
        print("💡 PROCHAINE ÉTAPE: Configurer un modèle local")
        print()
        show_local_model_options()
        print()
        print("Cela permettra à Anna de:")
        print("  ✓ Fonctionner sans internet")
        print("  ✓ Être 100% gratuite à utiliser")
        print("  ✓ Ne dépendre d'aucune entreprise")
        print("  ✓ Protéger votre vie privée")
        print()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Bootstrap interrompu par l'utilisateur")
        print("💡 Vous pouvez relancer ce script pour continuer")
        
    except Exception as e:
        print(f"\n❌ Erreur pendant le bootstrap: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n💫 Anna - Bootstrap System")
    print("Version: 1.0.0")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Au revoir !")
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)