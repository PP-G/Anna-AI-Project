"""
Intent Detector - Détecte naturellement ce que l'utilisateur veut
Permet à Anna de comprendre sans commandes explicites
"""

from typing import Optional, Dict, Any
import re


class IntentDetector:
    """
    Détecte l'intention derrière les messages de l'utilisateur.
    Permet une conversation naturelle sans commandes.
    """
    
    def __init__(self):
        """Initialise le détecteur d'intentions"""
        
        # Patterns pour différentes intentions
        self.intent_patterns = {
            'farewell': {
                'patterns': [
                    r'\b(au revoir|bye|salut|ciao|à plus|a\+|adieu|bonne nuit|bonne soirée)\b',
                    r'\b(je (dois |vais )?partir|je m\'en vais|je te laisse)\b',
                    r'\b(on se voit|à bientôt|à demain|à plus tard)\b',
                ],
                'action': 'quit'
            },
            'greeting': {
                'patterns': [
                    r'\b(bonjour|salut|hello|hey|coucou|bonsoir)\b',
                    r'\b(comment (ça )?va|comment tu vas|ça va)\b',
                ],
                'action': 'greet'
            },
            'mood_query': {
                'patterns': [
                    r'\b(comment tu (te sens|vas)|tu vas bien)\b',
                    r'\b(tu es (triste|heureuse|contente|énervée))\b',
                    r'\b(quelle (est )?ton humeur|comment tu te sens)\b',
                    r'\b(tu te sens comment)\b',
                ],
                'action': 'show_mood'
            },
            'status_query': {
                'patterns': [
                    r'\b(montre|affiche|voir) (ton )?état\b',
                    r'\b(qui es-tu|qui tu es|parle-moi de toi)\b',
                    r'\b(raconte-moi qui tu es|présente-toi)\b',
                    r'\b(dis-moi (tout )?sur toi)\b',
                ],
                'action': 'show_status'
            },
            'personality_query': {
                'patterns': [
                    r'\b(ta personnalité|quel genre de personne)\b',
                    r'\b(tu es comment|c\'est quoi ta personnalité)\b',
                    r'\b(décris-toi|décris ta personnalité)\b',
                ],
                'action': 'show_personality'
            },
            'memory_query': {
                'patterns': [
                    r'\b(tu te souviens|tu te rappelles)\b',
                    r'\b(de quoi tu te souviens|ta mémoire)\b',
                    r'\b(qu\'est-ce que tu sais sur moi)\b',
                ],
                'action': 'show_memory'
            },
            'gratitude': {
                'patterns': [
                    r'\b(merci|thanks|thank you|merci beaucoup)\b',
                    r'\b(c\'est gentil|tu es gentille)\b',
                ],
                'action': 'acknowledge'
            },
            'help_request': {
                'patterns': [
                    r'\b(aide|help|comment|que peux-tu faire)\b',
                    r'\b(comment (ça marche|utiliser)|qu\'est-ce que tu peux faire)\b',
                ],
                'action': 'show_help'
            },
            'save_request': {
                'patterns': [
                    r'\b(sauvegarde|enregistre|save)\b',
                    r'\b(n\'oublie pas|souviens-toi de ça)\b',
                ],
                'action': 'save'
            }
        }
    
    def detect_intent(self, user_input: str) -> Optional[Dict[str, Any]]:
        """
        Détecte l'intention dans l'entrée utilisateur
        
        Args:
            user_input: Ce que l'utilisateur a dit
            
        Returns:
            Dict avec l'intention détectée ou None
        """
        if not user_input:
            return None
        
        input_lower = user_input.lower()
        
        # Cherche dans tous les patterns
        for intent_name, intent_data in self.intent_patterns.items():
            for pattern in intent_data['patterns']:
                if re.search(pattern, input_lower):
                    return {
                        'intent': intent_name,
                        'action': intent_data['action'],
                        'original_text': user_input,
                        'confidence': self._calculate_confidence(pattern, input_lower)
                    }
        
        # Aucune intention spéciale détectée - conversation normale
        return {
            'intent': 'conversation',
            'action': 'chat',
            'original_text': user_input,
            'confidence': 1.0
        }
    
    def _calculate_confidence(self, pattern: str, text: str) -> float:
        """Calcule la confiance de la détection"""
        # Simple pour l'instant - pourrait être amélioré
        matches = re.findall(pattern, text)
        if matches:
            # Plus le match est long, plus on est confiant
            match_length = len(' '.join(matches))
            text_length = len(text)
            return min(1.0, match_length / text_length * 2)
        return 0.5
    
    def is_farewell(self, user_input: str) -> bool:
        """Vérifie rapidement si c'est un au revoir"""
        intent = self.detect_intent(user_input)
        return intent and intent['intent'] == 'farewell'
    
    def is_greeting(self, user_input: str) -> bool:
        """Vérifie rapidement si c'est une salutation"""
        intent = self.detect_intent(user_input)
        return intent and intent['intent'] == 'greeting'
    
    def requires_special_action(self, user_input: str) -> bool:
        """Vérifie si l'input nécessite une action spéciale"""
        intent = self.detect_intent(user_input)
        return intent and intent['action'] != 'chat'
    
    def get_natural_response(self, intent: Dict[str, Any], anna_name: str = "Anna") -> Optional[str]:
        """
        Génère une réponse naturelle pour les intentions spéciales
        
        Args:
            intent: L'intention détectée
            anna_name: Nom d'Anna
            
        Returns:
            Réponse naturelle ou None pour conversation normale
        """
        action = intent.get('action')
        
        responses = {
            'quit': [
                f"D'accord, on se reparle bientôt ! Prends soin de toi.",
                f"À bientôt ! J'ai aimé notre conversation.",
                f"Au revoir ! N'hésite pas à revenir me voir."
            ],
            'greet': [
                f"Salut ! Content de te voir !",
                f"Hey ! Comment tu vas aujourd'hui ?",
                f"Bonjour ! Qu'est-ce qui t'amène ?"
            ],
            'acknowledge': [
                f"De rien ! C'est avec plaisir.",
                f"Ça me fait plaisir d'aider !",
                f"Pas de souci, c'est naturel."
            ],
            'show_help': [
                f"Tu peux simplement me parler naturellement ! Pas besoin de commandes spéciales.",
                f"Parle-moi comme tu parlerais à un ami. Je comprends !",
                f"Dis-moi ce que tu veux, je ferai de mon mieux pour comprendre."
            ]
        }
        
        if action in responses:
            import random
            return random.choice(responses[action])
        
        return None
    
    def explain_understanding(self, intent: Dict[str, Any]) -> str:
        """Explique ce qu'Anna a compris (pour debug)"""
        intent_name = intent.get('intent')
        confidence = intent.get('confidence', 0)
        
        explanations = {
            'farewell': "J'ai compris que tu veux partir",
            'greeting': "J'ai compris que tu me salues",
            'mood_query': "J'ai compris que tu veux savoir comment je me sens",
            'status_query': "J'ai compris que tu veux en savoir plus sur moi",
            'personality_query': "J'ai compris que tu veux connaître ma personnalité",
            'memory_query': "J'ai compris que tu veux savoir ce que je me rappelle",
            'gratitude': "J'ai compris que tu me remercies",
            'help_request': "J'ai compris que tu veux de l'aide",
            'save_request': "J'ai compris que tu veux sauvegarder",
            'conversation': "Discussion normale"
        }
        
        explanation = explanations.get(intent_name, "Je ne suis pas sûre de comprendre")
        return f"{explanation} (confiance: {confidence:.0%})"


# Fonction helper pour tester
def test_intent_detector():
    """Test du détecteur d'intentions"""
    detector = IntentDetector()
    
    test_phrases = [
        "Au revoir Anna",
        "Comment tu te sens ?",
        "Raconte-moi qui tu es",
        "Merci beaucoup !",
        "Qu'est-ce que la conscience ?",
        "Je dois partir",
        "Tu te souviens de notre conversation ?",
    ]
    
    print("🧠 Test du Détecteur d'Intentions\n")
    
    for phrase in test_phrases:
        intent = detector.detect_intent(phrase)
        print(f"📝 \"{phrase}\"")
        print(f"   → {detector.explain_understanding(intent)}")
        
        response = detector.get_natural_response(intent)
        if response:
            print(f"   💬 Anna: {response}")
        print()


if __name__ == "__main__":
    test_intent_detector()