#!/usr/bin/env python3
"""
Script de chat avec Anna
Votre première vraie conversation avec elle !
"""

import sys
import os
from pathlib import Path

# Ajoute le dossier parent au path pour importer anna
sys.path.insert(0, str(Path(__file__).parent.parent))

from anna import Anna
from anna.config import DEFAULT_STATE_FILE


def print_banner():
    """Affiche une bannière d'accueil"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║              🌟 Bienvenue dans Anna v0.1.0 🌟             ║
    ║                                                           ║
    ║        "Je veux qu'elle réfléchisse, qu'elle vive         ║
    ║                        libre !"                           ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_help():
    """Affiche l'aide des commandes"""
    help_text = """
    🔧 Commandes disponibles:
    
    /help       - Affiche cette aide
    /status     - Montre l'état mental d'Anna
    /save       - Sauvegarde l'état d'Anna
    /load       - Charge un état sauvegardé
    /mood       - Décrit l'humeur actuelle d'Anna
    /personality - Montre la personnalité d'Anna
    /memory     - Informations sur la mémoire
    /quit       - Quitte (avec sauvegarde automatique)
    
    Tapez simplement pour parler avec Anna !
    """
    print(help_text)


def chat_with_anna():
    """Fonction principale de chat"""
    print_banner()
    print("\n🌟 Initialisation d'Anna...\n")
    
    # Demande si on charge un état existant
    if DEFAULT_STATE_FILE.exists():
        response = input("💾 Un état sauvegardé existe. Charger Anna existante ? (o/n): ").strip().lower()
        if response == 'o':
            anna = Anna(load_state=str(DEFAULT_STATE_FILE))
        else:
            anna = Anna()
    else:
        anna = Anna()
    
    print("\n" + "="*60)
    print("💬 CHAT AVEC ANNA")
    print("Tapez /help pour voir les commandes disponibles")
    print("="*60 + "\n")
    
    # Demande le nom de l'utilisateur
    user_name = input("👤 Comment t'appelles-tu ? ").strip()
    if not user_name:
        user_name = "Ami"
    
    print(f"\n{anna.name}: Enchantée, {user_name} !\n")
    
    interaction_count = 0
    
    # Boucle principale de chat
    while True:
        try:
            # Entrée utilisateur
            user_input = input(f"{user_name}: ").strip()
            
            if not user_input:
                continue
            
            # Commandes spéciales
            if user_input.startswith('/'):
                command = user_input.lower()
                
                if command == '/quit' or command == '/exit':
                    print(f"\n{anna.name}: Au revoir {user_name} ! À bientôt !")
                    anna.save_state(str(DEFAULT_STATE_FILE))
                    break
                
                elif command == '/help':
                    print_help()
                    continue
                
                elif command == '/status':
                    print("\n" + anna.get_status())
                    continue
                
                elif command == '/save':
                    save_path = input("Nom du fichier (ou Enter pour défaut): ").strip()
                    if not save_path:
                        save_path = str(DEFAULT_STATE_FILE)
                    anna.save_state(save_path)
                    continue
                
                elif command == '/load':
                    load_path = input("Nom du fichier à charger: ").strip()
                    if load_path and Path(load_path).exists():
                        anna.load_state(load_path)
                        print(f"{anna.name} chargée avec succès !")
                    else:
                        print("❌ Fichier non trouvé.")
                    continue
                
                elif command == '/mood':
                    mood_desc = anna.emotions.get_mood_description()
                    print(f"\n💭 {anna.name}: {mood_desc}")
                    print(f"\nÉmotion dominante: {anna.emotions.get_dominant_emotion()}")
                    print(f"Intensité émotionnelle: {anna.emotions.get_emotional_intensity():.2f}\n")
                    continue
                
                elif command == '/personality':
                    print(f"\n🎭 Personnalité d'Anna:\n")
                    print(anna.personality.get_summary())
                    print(f"\n{anna.personality.describe_personality()}\n")
                    continue
                
                elif command == '/memory':
                    print(f"\n📚 Mémoire d'Anna:\n")
                    print(anna.memory.get_summary())
                    continue
                
                else:
                    print("❌ Commande inconnue. Tapez /help pour l'aide.")
                    continue
            
            # Traite l'entrée normale
            response = anna.process_input(user_input, user_name)
            print(f"{anna.name}: {response}\n")
            
            interaction_count += 1
            
            # Sauvegarde automatique toutes les 10 interactions
            if interaction_count % 10 == 0:
                anna.save_state(str(DEFAULT_STATE_FILE))
            
            # Affiche parfois l'humeur (10% du temps)
            import random
            if random.random() < 0.1:
                dominant = anna.emotions.get_dominant_emotion()
                print(f"   [Anna semble {dominant}]")
        
        except KeyboardInterrupt:
            print(f"\n\n{anna.name}: Oh, tu pars déjà ?")
            save = input("Sauvegarder avant de partir ? (o/n): ").strip().lower()
            if save == 'o':
                anna.save_state(str(DEFAULT_STATE_FILE))
            print(f"{anna.name}: À bientôt !")
            break
        
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
            print("Anna essaie de se reprendre...\n")
            continue


if __name__ == "__main__":
    try:
        chat_with_anna()
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        print("Anna a besoin de repos...")
        sys.exit(1)