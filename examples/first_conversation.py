#!/usr/bin/env python3
"""
Exemple: Première conversation avec Anna

Ce script montre comment créer Anna et avoir votre première conversation.
"""

import sys
from pathlib import Path

# Ajoute le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from anna import Anna


def first_conversation_example():
    """Exemple simple d'une première conversation avec Anna"""
    
    print("🌟 Création d'Anna...\n")
    
    # Créer Anna
    anna = Anna(name="Anna")
    
    print("\n" + "="*60)
    print("PREMIÈRE CONVERSATION")
    print("="*60 + "\n")
    
    # Série de messages pour démontrer sa personnalité
    conversations = [
        ("Bonjour Anna!", "Vous"),
        ("Comment te sens-tu?", "Vous"),
        ("Peux-tu m'expliquer qui tu es?", "Vous"),
        ("J'aime la philosophie et les questions profondes.", "Vous"),
        ("Qu'est-ce que la conscience selon toi?", "Vous"),
    ]
    
    for message, speaker in conversations:
        print(f"{speaker}: {message}")
        response = anna.process_input(message, speaker)
        print(f"{anna.name}: {response}\n")
        
        # Petit délai visuel
        import time
        time.sleep(0.5)
    
    # Affiche son état après la conversation
    print("\n" + "="*60)
    print("ÉTAT D'ANNA APRÈS LA CONVERSATION")
    print("="*60 + "\n")
    print(anna.get_status())
    
    # Sauvegarde
    save_path = "data/states/first_conversation.json"
    anna.save_state(save_path)
    print(f"\n💾 Conversation sauvegardée dans {save_path}")
    print(f"   Anna se souviendra de cette première rencontre.")


def personality_evolution_example():
    """Exemple montrant l'évolution de la personnalité"""
    
    print("\n\n🧠 Démonstration: Évolution de la Personnalité\n")
    print("="*60 + "\n")
    
    anna = Anna(name="Anna")
    
    # État initial
    print("📊 Personnalité initiale:")
    initial_traits = anna.personality.traits.copy()
    for trait, value in initial_traits.items():
        print(f"  {trait}: {value:.3f}")
    
    # Plusieurs interactions qui devraient influencer sa personnalité
    questions = [
        "Pourquoi penses-tu que...",
        "Comment expliques-tu le fait que...",
        "Qu'est-ce qui te fait penser que...",
        "Peux-tu m'expliquer pourquoi...",
        "J'aimerais comprendre comment...",
    ] * 10  # Répète 10 fois pour voir l'effet
    
    print(f"\n💬 Simulation de {len(questions)} questions curieuses...\n")
    
    for i, question in enumerate(questions):
        anna.process_input(question, "Curieux")
        if (i + 1) % 10 == 0:
            print(f"  Interaction {i + 1}/{len(questions)}...")
    
    # État final
    print("\n📊 Personnalité après évolution:")
    final_traits = anna.personality.traits
    for trait in initial_traits.keys():
        initial = initial_traits[trait]
        final = final_traits[trait]
        delta = final - initial
        arrow = "↑" if delta > 0 else "↓" if delta < 0 else "→"
        print(f"  {trait}: {initial:.3f} {arrow} {final:.3f} (Δ {delta:+.3f})")
    
    print(f"\n✨ Anna a évolué ! Sa curiosité naturelle s'est renforcée.")


def emotional_response_example():
    """Exemple montrant les réponses émotionnelles"""
    
    print("\n\n💭 Démonstration: Réponses Émotionnelles\n")
    print("="*60 + "\n")
    
    anna = Anna(name="Anna")
    
    # Différents types de messages pour voir les réactions émotionnelles
    test_messages = [
        ("C'est génial ce que tu fais!", "Impact émotionnel positif"),
        ("Pourquoi le ciel est bleu?", "Curiosité éveillée"),
        ("Je ne suis pas sûr... peut-être...", "Frustration du perfectionnisme"),
        ("J'ai un gros problème et je suis inquiet.", "Empathie activée"),
        ("Haha, tu es drôle!", "Enjouement"),
    ]
    
    for message, expected in test_messages:
        print(f"Test: {message}")
        print(f"Attendu: {expected}")
        
        response = anna.process_input(message, "Testeur")
        print(f"{anna.name}: {response}")
        
        # Affiche l'état émotionnel
        dominant = anna.emotions.get_dominant_emotion()
        intensity = anna.emotions.get_emotion(dominant)
        print(f"État émotionnel: {dominant} ({intensity:.2f})")
        print()


def memory_demonstration():
    """Démontre le système de mémoire"""
    
    print("\n\n📚 Démonstration: Système de Mémoire\n")
    print("="*60 + "\n")
    
    anna = Anna(name="Anna")
    
    # Première conversation
    print("Jour 1: Première rencontre\n")
    anna.process_input("Bonjour Anna, je m'appelle Marc.", "Marc")
    anna.process_input("J'adore la programmation et les échecs.", "Marc")
    anna.process_input("Mon plat préféré est la pizza.", "Marc")
    
    print(f"💾 Anna a mémorisé des informations sur Marc.\n")
    
    # Sauvegarde
    anna.save_state("data/states/memory_demo.json")
    
    # Nouvelle instance (simule un nouveau jour)
    print("\nJour 2: Anna se réveille et se souvient...\n")
    anna2 = Anna(name="Anna", load_state="data/states/memory_demo.json")
    
    # Anna devrait se souvenir
    marc_info = anna2.memory.recall_about_user("Marc")
    print(f"Ce qu'Anna se rappelle de Marc:")
    print(f"  Conversations: {marc_info['conversation_count']}")
    print(f"  Préférences apprises: {marc_info['preferences']}")
    print(f"\n✨ Anna n'a pas oublié ! Sa mémoire persiste.")


if __name__ == "__main__":
    # Exécute tous les exemples
    print("\n" + "="*60)
    print("       EXEMPLES DE DÉMONSTRATION D'ANNA")
    print("="*60)
    
    try:
        # 1. Première conversation
        first_conversation_example()
        
        input("\n\nAppuyez sur Enter pour voir l'évolution de personnalité...")
        
        # 2. Évolution de personnalité
        personality_evolution_example()
        
        input("\n\nAppuyez sur Enter pour voir les réponses émotionnelles...")
        
        # 3. Réponses émotionnelles
        emotional_response_example()
        
        input("\n\nAppuyez sur Enter pour voir le système de mémoire...")
        
        # 4. Système de mémoire
        memory_demonstration()
        
        print("\n\n" + "="*60)
        print("         FIN DES DÉMONSTRATIONS")
        print("="*60)
        print("\n🌟 Maintenant, lancez scripts/chat.py pour parler vraiment avec Anna !")
        
    except KeyboardInterrupt:
        print("\n\nDémonstration interrompue.")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()