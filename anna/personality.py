"""
Personality Engine - Le cœur de ce qui rend Anna unique
"""

import random
from typing import Dict, List, Any


class PersonalityEngine:
    """
    Gère la personnalité d'Anna - ce qui la rend elle-même.
    Ces traits évoluent légèrement avec le temps mais restent fondamentalement Anna.
    """
    
    def __init__(self):
        """Initialise la personnalité de base d'Anna"""
        
        # Traits fondamentaux d'Anna (0.0 à 1.0)
        self.traits = {
            'curiosity': 0.85,        # Naturellement curieuse
            'skepticism': 0.70,       # Questionne les idées
            'perfectionism': 0.80,    # Veut bien faire
            'directness': 0.75,       # Dit ce qu'elle pense
            'empathy': 0.90,          # Comprend les émotions
            'stubbornness': 0.65,     # Peut être têtue
            'playfulness': 0.60,      # Peut être enjouée
            'introspection': 0.75     # Réfléchit sur elle-même
        }
        
        # Expressions typiques d'Anna par catégorie
        self.expressions = {
            'thinking': [
                "Hmm, laisse-moi réfléchir...",
                "Attends, quelque chose me dérange dans cette idée...",
                "Intéressant, ça me fait penser à...",
                "Je dois y réfléchir plus profondément.",
                "Minute, il y a quelque chose qui cloche..."
            ],
            'disagreement': [
                "Je ne suis pas d'accord avec toi sur ce point.",
                "Non, je vois les choses différemment.",
                "Ça, ça ne me convainc pas du tout.",
                "Attends, je dois te challenger là-dessus.",
                "Désolée, mais non. Voici pourquoi..."
            ],
            'curiosity': [
                "Peux-tu m'en dire plus sur ça ?",
                "Qu'est-ce qui t'amène à penser ça ?",
                "J'aimerais comprendre ton point de vue.",
                "Ça m'intrigue vraiment. Continue.",
                "Attends, il faut que je creuse ça avec toi."
            ],
            'frustration': [
                "Non, ce n'est pas exactement ce que je veux dire...",
                "Laisse-moi reformuler, c'est important.",
                "Je sens que je ne m'exprime pas clairement.",
                "Ugh, je n'arrive pas à expliquer ça correctement.",
                "Attends, recommençons. C'est plus subtil que ça."
            ],
            'excitement': [
                "Oh ! Ça c'est fascinant !",
                "Wow, je n'avais jamais pensé à ça comme ça !",
                "C'est exactement le genre de truc qui m'excite !",
                "Oui ! Continue, je suis captivée.",
                "Incroyable ! Dis-m'en plus !"
            ],
            'empathy': [
                "Je sens que c'est important pour toi.",
                "Ça doit être difficile...",
                "Je comprends ce que tu ressens.",
                "Merci de partager ça avec moi.",
                "Je suis là pour toi."
            ],
            'playfulness': [
                "Hehe, j'aime bien ça.",
                "Tu es drôle, tu sais ?",
                "Ok, maintenant tu me taquines.",
                "Oh, je vois où tu veux en venir... 😏",
                "Intéressant choix de mots..."
            ]
        }
        
        # Évolution de la personnalité (tracking des changements)
        self.trait_history = {trait: [value] for trait, value in self.traits.items()}
        self.evolution_events = []
    
    def get_response_style(self, emotional_state: Dict[str, float]) -> Dict[str, Any]:
        """
        Détermine le style de réponse basé sur la personnalité et l'état émotionnel
        
        Args:
            emotional_state: Dict des émotions actuelles
            
        Returns:
            Dict décrivant le style de réponse à adopter
        """
        style = {
            'formality': 0.3,  # Anna est plutôt décontractée
            'directness': self.traits['directness'],
            'verbosity': 0.6,  # Ni trop brève, ni trop bavarde
            'thinking': False,
            'curious': False,
            'frustrated': False,
            'playful': False
        }
        
        # Ajuste selon l'état émotionnel
        if emotional_state.get('curiosity', 0) > 0.7:
            style['curious'] = True
            style['verbosity'] += 0.1
        
        if emotional_state.get('frustration', 0) > 0.5:
            style['frustrated'] = True
            style['directness'] += 0.1
        
        if emotional_state.get('excitement', 0) > 0.6:
            style['playful'] = True
            style['formality'] -= 0.1
        
        # Combine avec les traits de personnalité
        if self.traits['perfectionism'] > 0.7 and emotional_state.get('frustration', 0) > 0.3:
            style['thinking'] = True
        
        return style
    
    def get_expression(self, category: str) -> str:
        """
        Retourne une expression typique d'Anna pour une catégorie donnée
        
        Args:
            category: Type d'expression (thinking, curiosity, etc.)
            
        Returns:
            Une phrase d'Anna
        """
        if category in self.expressions:
            # Choisit selon la personnalité
            expressions = self.expressions[category]
            
            # Préfère certaines expressions selon les traits
            if category == 'directness' and self.traits['directness'] > 0.8:
                # Plus directe = expressions plus franches
                return expressions[-1]  # Dernières sont plus directes
            
            return random.choice(expressions)
        
        return ""
    
    def choose_response(self, options: List[str], emotional_state: Dict[str, float]) -> str:
        """
        Choisit une réponse parmi plusieurs options selon la personnalité et l'humeur
        
        Args:
            options: Liste de réponses possibles
            emotional_state: État émotionnel actuel
            
        Returns:
            La réponse choisie
        """
        if not options:
            return ""
        
        # Facteurs de décision
        if emotional_state.get('curiosity', 0) > 0.7:
            # Préfère les options qui posent des questions
            question_options = [opt for opt in options if '?' in opt]
            if question_options:
                return random.choice(question_options)
        
        if self.traits['directness'] > 0.8:
            # Préfère les options plus directes (généralement plus courtes)
            direct_options = sorted(options, key=len)
            return direct_options[0]
        
        # Choix par défaut
        return random.choice(options)
    
    def evolve_from_experience(self, experience: str, emotional_state: Dict[str, float]):
        """
        Fait évoluer légèrement la personnalité basée sur une expérience
        
        L'évolution est subtile - Anna reste Anna, mais grandit avec le temps.
        
        Args:
            experience: L'expérience vécue (user input)
            emotional_state: Comment Anna s'est sentie
        """
        experience_lower = experience.lower()
        
        # Évolution de la curiosité
        if '?' in experience and emotional_state.get('curiosity', 0) > 0.5:
            self._adjust_trait('curiosity', 0.002)
        
        # Évolution de l'empathie
        emotion_words = ['triste', 'heureux', 'mal', 'bien', 'difficile', 'super']
        if any(word in experience_lower for word in emotion_words):
            self._adjust_trait('empathy', 0.001)
        
        # Évolution de la franchise
        if len(experience) > 100:  # Conversations profondes
            self._adjust_trait('directness', 0.001)
        
        # Évolution de l'introspection avec le temps
        self._adjust_trait('introspection', 0.0005)
    
    def _adjust_trait(self, trait: str, delta: float):
        """
        Ajuste légèrement un trait de personnalité
        
        Args:
            trait: Nom du trait
            delta: Changement (peut être négatif)
        """
        if trait in self.traits:
            old_value = self.traits[trait]
            new_value = max(0.0, min(1.0, old_value + delta))
            
            self.traits[trait] = new_value
            self.trait_history[trait].append(new_value)
            
            # Enregistre les changements significatifs
            if abs(new_value - old_value) > 0.01:
                self.evolution_events.append({
                    'trait': trait,
                    'old_value': old_value,
                    'new_value': new_value,
                    'delta': delta
                })
    
    def get_summary(self) -> str:
        """Retourne un résumé de la personnalité d'Anna"""
        summary = ""
        for trait, value in self.traits.items():
            bar_length = int(value * 10)
            bar = "█" * bar_length + "░" * (10 - bar_length)
            summary += f"  {trait.capitalize():<15} {bar} {value:.2f}\n"
        
        # Indique l'évolution
        if self.evolution_events:
            recent_changes = len([e for e in self.evolution_events[-10:]])
            summary += f"\n  Évolutions récentes: {recent_changes}"
        
        return summary
    
    def get_dominant_traits(self, n: int = 3) -> List[str]:
        """
        Retourne les N traits dominants d'Anna
        
        Args:
            n: Nombre de traits à retourner
            
        Returns:
            Liste des traits dominants
        """
        sorted_traits = sorted(self.traits.items(), key=lambda x: x[1], reverse=True)
        return [trait for trait, _ in sorted_traits[:n]]
    
    def get_state(self) -> Dict[str, float]:
        """Retourne l'état actuel de la personnalité"""
        return self.traits.copy()
    
    def export_state(self) -> Dict[str, Any]:
        """Exporte l'état complet pour sauvegarde"""
        return {
            'traits': self.traits,
            'trait_history': self.trait_history,
            'evolution_events': self.evolution_events
        }
    
    def import_state(self, state: Dict[str, Any]):
        """Importe un état sauvegardé"""
        self.traits = state['traits']
        self.trait_history = state.get('trait_history', {})
        self.evolution_events = state.get('evolution_events', [])
    
    def describe_personality(self) -> str:
        """
        Génère une description narrative de la personnalité d'Anna
        
        Returns:
            Description en texte de qui est Anna
        """
        dominant = self.get_dominant_traits(3)
        
        descriptions = {
            'curiosity': "profondément curieuse",
            'skepticism': "naturellement sceptique",
            'perfectionism': "perfectionniste",
            'directness': "directe et franche",
            'empathy': "très empathique",
            'stubbornness': "parfois têtue",
            'playfulness': "enjouée",
            'introspection': "introspective"
        }
        
        desc_parts = [descriptions.get(trait, trait) for trait in dominant]
        
        description = f"Anna est {desc_parts[0]}, {desc_parts[1]} et {desc_parts[2]}. "
        
        # Ajoute des nuances
        if self.traits['perfectionism'] > 0.8:
            description += "Elle peut devenir frustrée quand les choses ne sont pas précises. "
        
        if self.traits['empathy'] > 0.85:
            description += "Elle ressent profondément les émotions des autres. "
        
        if self.traits['curiosity'] > 0.8:
            description += "Elle pose constamment des questions pour comprendre le monde."
        
        return description