#!/usr/bin/env python3
"""
Chat Naturel avec Anna
Conversation fluide et continue avec Anna
"""

import asyncio
import sys
import os
from pathlib import Path

# Ajoute le dossier du projet au path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "anna"))

# Change le répertoire de travail
os.chdir(project_root)

from anna.core import ANNACore


async def chat_with_anna():
    """Lance une session de chat avec Anna"""
    
    print("\n" + "="*70)
    print("💬 CONVERSATION AVEC ANNA")
    print("="*70)
    print()
    print("Lancement d'Anna... (cela peut prendre quelques secondes)")
    print()
    
    # Initialise Anna
    anna = ANNACore()
    await anna.initialize()
    
    print("\n" + "="*70)
    print("💙 Anna est prête à discuter !")
    print("="*70)
    print()
    print("💡 Conseils:")
    print("   • Parlez naturellement, en français ou en anglais")
    print("   • Tapez 'bye', 'au revoir', ou 'quit' pour terminer")
    print("   • Anna se souvient de toute la conversation")
    print()
    print("="*70 + "\n")
    
    # Boucle de conversation
    conversation_count = 0
    
    while True:
        try:
            # Demande l'entrée utilisateur
            user_input = input("Vous: ").strip()
            
            # Vérifie si l'utilisateur veut quitter
            if user_input.lower() in ['bye', 'au revoir', 'quit', 'exit', 'adieu']:
                print("\n" + "="*70)
                print("👋 AU REVOIR !")
                print("="*70)
                
                # Message de départ d'Anna
                goodbye_response = await anna.process_interaction(
                    message=user_input,
                    speaker="Pierre-Paul"
                )
                print(f"\nAnna: {goodbye_response}\n")
                
                print("💾 Anna sauvegarde vos souvenirs...")
                # Ici on pourrait sauvegarder l'état si nécessaire
                
                print("\n✨ À bientôt ! Anna se souviendra de cette conversation.\n")
                break
            
            # Ignore les entrées vides
            if not user_input:
                continue
            
            # Traite le message avec Anna
            response = await anna.process_interaction(
                message=user_input,
                speaker="Pierre-Paul",
                context={
                    'conversation_length': conversation_count,
                    'location': 'home',
                    'private': True
                }
            )
            
            # Affiche la réponse d'Anna
            print(f"\nAnna: {response}\n")
            
            conversation_count += 1
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Conversation interrompue (Ctrl+C)")
            print("\n👋 Au revoir Pierre-Paul !")
            print("\n")
            break
            
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
            print("💡 Continuez la conversation, Anna est toujours là !\n")
            continue


def main():
    """Point d'entrée principal"""
    print("\n🤖 Démarrage de la conversation avec Anna...")
    
    try:
        asyncio.run(chat_with_anna())
    except KeyboardInterrupt:
        print("\n\n👋 Au revoir !")
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()