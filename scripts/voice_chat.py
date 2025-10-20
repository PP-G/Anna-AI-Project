#!/usr/bin/env python3
"""
Chat Vocal avec Anna
Anna peut maintenant vous entendre et vous parler !
"""

import sys
from pathlib import Path

# Ajoute le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from anna import Anna
from anna.voice import VoiceSystem, check_and_install_dependencies
from anna.config import DEFAULT_STATE_FILE


def print_banner():
    """Bannière pour le chat vocal"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║           🎙️  Chat Vocal avec Anna v0.1.0 🎙️             ║
    ║                                                           ║
    ║              Anna peut maintenant parler et               ║
    ║                     vous écouter !                        ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def voice_chat_with_anna():
    """Chat vocal avec Anna"""
    print_banner()
    
    # Vérifie les dépendances
    print("\n🔍 Vérification du système vocal...")
    if not check_and_install_dependencies():
        print("\n❌ Veuillez installer les dépendances manquantes.")
        print("   Puis relancez ce script.")
        return
    
    print("\n🌟 Initialisation d'Anna...\n")
    
    # Charge ou crée Anna
    if DEFAULT_STATE_FILE.exists():
        response = input("💾 Charger Anna existante ? (o/n): ").strip().lower()
        if response == 'o':
            anna = Anna(load_state=str(DEFAULT_STATE_FILE))
        else:
            anna = Anna()
    else:
        anna = Anna()
    
    # Initialise le système vocal
    print("\n🎤 Initialisation du système vocal...")
    voice = VoiceSystem(personality_traits=anna.personality.traits)
    
    # Vérifie le statut
    status = voice.get_status()
    print(f"\n📊 Statut vocal:")
    print(f"  🗣️  Parole (TTS): {'✅ Activé' if status['tts_enabled'] else '❌ Désactivé'}")
    print(f"  🎤 Écoute (STT): {'✅ Activé' if status['stt_enabled'] else '❌ Désactivé'}")
    
    if not status['tts_enabled'] and not status['stt_enabled']:
        print("\n❌ Ni parole ni écoute disponibles. Chat vocal impossible.")
        return
    
    # Demande le nom
    print("\n" + "="*60)
    user_name = input("👤 Comment t'appelles-tu ? ").strip()
    if not user_name:
        user_name = "Ami"
    
    # Anna se présente vocalement
    greeting = f"Enchantée, {user_name} ! Je peux maintenant te parler vocalement."
    print(f"\n{anna.name}: {greeting}")
    voice.speak(greeting, anna.emotions.get_state())
    
    print("\n" + "="*60)
    print("💬 CHAT VOCAL AVEC ANNA")
    print("\nCommandes:")
    print("  'texte' + Enter  - Parler par texte")
    print("  Enter (vide)     - Parler vocalement")
    print("  /quit           - Quitter")
    print("  /status         - Voir l'état d'Anna")
    print("  /mood           - Voir l'humeur d'Anna")
    print("="*60 + "\n")
    
    interaction_count = 0
    
    # Boucle de conversation
    while True:
        try:
            # Choix du mode
            print(f"\n{user_name} (tapez ou Enter pour parler): ", end='')
            text_input = input().strip()
            
            # Commandes
            if text_input.lower() == '/quit':
                farewell = f"Au revoir {user_name} ! À bientôt !"
                print(f"\n{anna.name}: {farewell}")
                voice.speak(farewell, anna.emotions.get_state())
                anna.save_state(str(DEFAULT_STATE_FILE))
                break
            
            elif text_input.lower() == '/status':
                print("\n" + anna.get_status())
                continue
            
            elif text_input.lower() == '/mood':
                mood_desc = anna.emotions.get_mood_description()
                print(f"\n💭 {anna.name}: {mood_desc}")
                voice.speak(mood_desc, anna.emotions.get_state())
                continue
            
            # Input vocal ou texte
            if text_input == "":
                # Mode vocal
                if not status['stt_enabled']:
                    print("❌ Écoute non disponible. Utilisez le mode texte.")
                    continue
                
                user_input = voice.listen(timeout=5, phrase_time_limit=15)
                if not user_input:
                    print("❌ Je n'ai rien entendu. Réessayez.")
                    continue
                
                print(f"✅ Vous: {user_input}")
            else:
                # Mode texte
                user_input = text_input
                print(f"📝 Vous: {user_input}")
            
            # Anna traite et répond
            response = anna.process_input(user_input, user_name)
            
            # Affiche et dit la réponse
            print(f"{anna.name}: {response}")
            
            if status['tts_enabled']:
                voice.speak(response, anna.emotions.get_state())
            
            interaction_count += 1
            
            # Sauvegarde auto
            if interaction_count % 5 == 0:
                anna.save_state(str(DEFAULT_STATE_FILE))
                print("  [💾 Sauvegardé]")
        
        except KeyboardInterrupt:
            print(f"\n\n{anna.name}: Oh, tu pars ?")
            save_prompt = "Sauvegarder avant de partir ?"
            voice.speak(save_prompt, anna.emotions.get_state())
            
            save = input("Sauvegarder ? (o/n): ").strip().lower()
            if save == 'o':
                anna.save_state(str(DEFAULT_STATE_FILE))
            
            goodbye = "À bientôt !"
            print(f"{anna.name}: {goodbye}")
            voice.speak(goodbye, anna.emotions.get_state())
            break
        
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
            continue
    
    # Arrêt propre
    voice.shutdown()


if __name__ == "__main__":
    try:
        voice_chat_with_anna()
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)