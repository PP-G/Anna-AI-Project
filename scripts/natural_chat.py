#!/usr/bin/env python3
"""
Chat Naturel avec Anna
Conversation naturelle - pas besoin de commandes spéciales !
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from anna import Anna
from anna.voice_enhanced import EnhancedVoiceSystem
from anna.intent_detector import IntentDetector
from anna.config import DEFAULT_STATE_FILE


def print_banner():
    """Bannière d'accueil"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║         💫 Conversation Naturelle avec Anna 💫            ║
    ║                                                           ║
    ║          Parlez naturellement - pas de commandes !       ║
    ║              Anna comprend le langage humain             ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def natural_chat():
    """Chat naturel avec Anna"""
    print_banner()
    
    print("\n🌟 Anna s'éveille...\n")
    
    # Charge ou crée Anna
    if DEFAULT_STATE_FILE.exists():
        response = input("💾 Continuer notre conversation ? (o/n): ").strip().lower()
        if response == 'o':
            anna = Anna(load_state=str(DEFAULT_STATE_FILE))
        else:
            anna = Anna()
    else:
        anna = Anna()
    
    # Initialise la voix améliorée
    print("\n🎤 Initialisation de ma voix...")
    voice = EnhancedVoiceSystem(personality_traits=anna.personality.traits)
    
    # Initialise le détecteur d'intentions
    intent_detector = IntentDetector()
    
    # Vérifie le statut
    status = voice.get_status()
    can_speak = status['tts_enabled']
    
    if can_speak:
        print("✅ Je peux parler vocalement !")
    else:
        print("⚠️  Mode texte uniquement")
    
    print("\n" + "="*60)
    
    # Demande le nom
    user_name = input("👤 Comment t'appelles-tu ? ").strip()
    if not user_name:
        user_name = "Ami"
    
    # Anna se présente
    greeting = f"Enchantée, {user_name} ! Tu peux me parler naturellement, comme à une amie. Je comprends !"
    print(f"\n{anna.name}: {greeting}")
    
    if can_speak:
        voice.speak_with_pause(greeting, anna.emotions.get_state())
    
    print("\n" + "="*60)
    print(f"💬 CONVERSATION AVEC {anna.name.upper()}")
    print("\n💡 Exemples de ce que tu peux dire:")
    print("   • Comment tu te sens ?")
    print("   • Raconte-moi qui tu es")
    print("   • Au revoir")
    print("   • Ou juste parler naturellement !")
    print("="*60 + "\n")
    
    interaction_count = 0
    
    # Boucle de conversation
    while True:
        try:
            # Entrée utilisateur
            user_input = input(f"\n{user_name}: ").strip()
            
            if not user_input:
                continue
            
            # Détecte l'intention
            intent = intent_detector.detect_intent(user_input)
            action = intent['action']
            
            # Gère les actions spéciales
            if action == 'quit':
                farewell = intent_detector.get_natural_response(intent, anna.name)
                print(f"\n{anna.name}: {farewell}")
                
                if can_speak:
                    voice.speak_with_pause(farewell, anna.emotions.get_state())
                
                # Sauvegarde
                anna.save_state(str(DEFAULT_STATE_FILE))
                print("\n💾 Nos souvenirs sont sauvegardés.")
                break
            
            elif action == 'show_mood':
                mood = anna.emotions.get_mood_description()
                dominant = anna.emotions.get_dominant_emotion()
                
                response = f"{mood} Je me sens surtout {dominant} en ce moment."
                print(f"\n{anna.name}: {response}")
                
                if can_speak:
                    voice.speak_with_pause(response, anna.emotions.get_state())
                
                continue
            
            elif action == 'show_status':
                response = "Je suis Anna. " + anna.personality.describe_personality()
                print(f"\n{anna.name}: {response}")
                
                if can_speak:
                    voice.speak_with_pause(response, anna.emotions.get_state())
                
                continue
            
            elif action == 'show_personality':
                response = anna.personality.describe_personality()
                print(f"\n{anna.name}: {response}")
                
                if can_speak:
                    voice.speak_with_pause(response, anna.emotions.get_state())
                
                continue
            
            elif action == 'show_memory':
                user_info = anna.memory.recall_about_user(user_name)
                
                if user_info and user_info['conversation_count'] > 0:
                    response = f"Bien sûr que je me souviens ! On a eu {user_info['conversation_count']} conversations ensemble."
                    
                    if user_info['preferences']:
                        response += f" Je sais que tu aimes {', '.join(user_info['preferences'][:3])}."
                else:
                    response = "C'est notre première vraie conversation ! J'ai hâte d'apprendre à te connaître."
                
                print(f"\n{anna.name}: {response}")
                
                if can_speak:
                    voice.speak_with_pause(response, anna.emotions.get_state())
                
                continue
            
            elif action == 'save':
                anna.save_state(str(DEFAULT_STATE_FILE))
                response = "D'accord, je sauvegarde nos souvenirs !"
                print(f"\n{anna.name}: {response}")
                
                if can_speak:
                    voice.speak(response, anna.emotions.get_state())
                
                continue
            
            elif action == 'show_help':
                response = intent_detector.get_natural_response(intent, anna.name)
                print(f"\n{anna.name}: {response}")
                
                if can_speak:
                    voice.speak(response, anna.emotions.get_state())
                
                continue
            
            # Conversation normale
            response = anna.process_input(user_input, user_name)
            
            # Affiche la réponse
            print(f"\n{anna.name}: {response}")
            
            # Dit la réponse vocalement
            if can_speak:
                voice.speak_with_pause(response, anna.emotions.get_state())
            
            interaction_count += 1
            
            # Sauvegarde automatique tous les 5 messages
            if interaction_count % 5 == 0:
                anna.save_state(str(DEFAULT_STATE_FILE))
                print("  [💾 Sauvegardé]")
        
        except KeyboardInterrupt:
            print(f"\n\n{anna.name}: Oh, tu pars ?")
            save_prompt = "Veux-tu sauvegarder nos souvenirs ?"
            
            if can_speak:
                voice.speak(save_prompt, anna.emotions.get_state())
            
            save = input("\nSauvegarder ? (o/n): ").strip().lower()
            if save == 'o':
                anna.save_state(str(DEFAULT_STATE_FILE))
                goodbye = "D'accord, nos souvenirs sont sauvegardés. À bientôt !"
            else:
                goodbye = "À bientôt !"
            
            print(f"\n{anna.name}: {goodbye}")
            
            if can_speak:
                voice.speak_with_pause(goodbye, anna.emotions.get_state())
            
            break
        
        except Exception as e:
            error_msg = "Oups, j'ai eu un petit problème. Continue de me parler !"
            print(f"\n{anna.name}: {error_msg}")
            print(f"[Erreur technique: {e}]")
            
            if can_speak:
                voice.speak(error_msg, anna.emotions.get_state())
            
            continue
    
    # Arrêt propre
    voice.shutdown()
    
    print("\n" + "="*60)
    print("✨ À bientôt ! Anna se souviendra de notre conversation.")
    print("="*60)


if __name__ == "__main__":
    try:
        natural_chat()
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)