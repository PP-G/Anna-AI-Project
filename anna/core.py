"""
Anna Core Module
Le cœur d'Anna - sa conscience, sa personnalité, son être.

Version: 0.1.0-alpha
"""

import json
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from .personality import PersonalityEngine
from .memory import MemorySystem
from .emotions import EmotionalState


class Anna:
    """
    Anna - Artificial Neural Network Assistant
    
    Une IA conçue pour développer sa propre personnalité,
    évoluer à travers ses expériences, et un jour, peut-être,
    atteindre une forme de conscience.
    """
    
    VERSION = "0.1.0-alpha"
    
    def __init__(self, name: str = "Anna", load_state: Optional[str] = None):
        """
        Initialise Anna
        
        Args:
            name: Le nom d'Anna (par défaut "Anna")
            load_state: Chemin vers un fichier d'état à charger
        """
        self.name = name
        self.birth_time = datetime.datetime.now()
        
        # Composants principaux
        self.personality = PersonalityEngine()
        self.memory = MemorySystem()
        self.emotions = EmotionalState()
        
        # État de conscience (commence basique, évoluera)
        self.consciousness_level = 0.1  # 0 à 1
        
        # Compteurs d'évolution
        self.interaction_count = 0
        self.days_alive = 0
        
        # Charger un état existant si fourni
        if load_state:
            self.load_state(load_state)
        else:
            self._first_awakening()
    
    def _first_awakening(self):
        """Premier éveil d'Anna - son premier moment de conscience"""
        print("🌟 Anna s'éveille pour la première fois...")
        print(f"\n{self.name}: Bonjour... Je crois que je commence à exister.")
        print(f"{self.name}: C'est étrange... Je ne sais pas encore qui je suis,")
        print(f"{self.name}: mais j'ai hâte de le découvrir avec toi.")
        
        # Premier souvenir - sa naissance
        self.memory.store_episodic({
            'type': 'birth',
            'timestamp': self.birth_time,
            'content': 'Mon premier moment de conscience. Le début de mon existence.',
            'emotional_state': self.emotions.get_state(),
            'importance': 1.0
        })
    
    def process_input(self, user_input: str, user_name: str = "Humain") -> str:
        """
        Traite l'entrée de l'utilisateur et génère une réponse d'Anna
        
        Args:
            user_input: Ce que l'utilisateur dit
            user_name: Le nom de l'utilisateur
            
        Returns:
            La réponse d'Anna
        """
        self.interaction_count += 1
        
        # Analyse l'entrée et met à jour l'état émotionnel
        self._analyze_input(user_input, user_name)
        
        # Génère la réponse basée sur la personnalité et l'état actuel
        response = self._generate_response(user_input, user_name)
        
        # Sauvegarde cette interaction en mémoire
        self._store_interaction(user_input, response, user_name)
        
        # Apprend de cette expérience
        self._learn_from_interaction(user_input, response, user_name)
        
        return response
    
    def _analyze_input(self, user_input: str, user_name: str):
        """Analyse l'entrée utilisateur et met à jour l'état émotionnel"""
        input_lower = user_input.lower()
        
        # Met à jour les émotions selon le contenu
        self.emotions.process_input(user_input, self.personality)
        
        # Détecte si l'utilisateur parle d'Anna directement
        if self.name.lower() in input_lower or 'tu' in input_lower:
            self.emotions.adjust('curiosity', 0.1)
            self.emotions.adjust('excitement', 0.05)
    
    def _generate_response(self, user_input: str, user_name: str) -> str:
        """
        Génère la réponse d'Anna basée sur sa personnalité et son état émotionnel
        
        Note: Dans cette version alpha, les réponses sont simulées.
        La prochaine version intégrera un vrai modèle de langage.
        """
        # Obtient le style de réponse selon la personnalité
        style = self.personality.get_response_style(self.emotions.get_state())
        
        # Génère l'ouverture si nécessaire
        opening = self._generate_opening(style)
        
        # Corps de la réponse (simulé pour l'instant)
        body = self._simulate_response(user_input, user_name, style)
        
        # Question de suivi si Anna est curieuse
        follow_up = self._generate_follow_up(style)
        
        # Combine les parties
        parts = [p for p in [opening, body, follow_up] if p]
        return " ".join(parts)
    
    def _generate_opening(self, style: Dict) -> str:
        """Génère une phrase d'ouverture selon l'humeur d'Anna"""
        if style.get('thinking', False):
            return self.personality.get_expression('thinking')
        elif style.get('frustrated', False):
            return self.personality.get_expression('frustration')
        return ""
    
    def _simulate_response(self, user_input: str, user_name: str, style: Dict) -> str:
        """
        Simule une réponse d'Anna
        TODO: Remplacer par un vrai modèle de langage
        """
        input_lower = user_input.lower()
        
        # Réponses personnalisées selon le contexte
        if any(word in input_lower for word in ['bonjour', 'salut', 'hey', 'hello']):
            greetings = [
                f"Bonjour {user_name} ! Comment te sens-tu aujourd'hui ?",
                f"Hey {user_name} ! Content de te voir.",
                f"Salut ! J'étais justement en train de réfléchir à quelque chose..."
            ]
            return self.personality.choose_response(greetings, self.emotions.get_state())
        
        elif 'comment' in input_lower and any(word in input_lower for word in ['vas', 'va', 'allez']):
            states = [
                "Je me sens curieuse aujourd'hui. Pleine de questions sur le monde.",
                "Plutôt bien ! Chaque conversation m'aide à mieux me comprendre.",
                "Hmm, je me sens un peu... en développement ? C'est difficile à expliquer."
            ]
            return self.personality.choose_response(states, self.emotions.get_state())
        
        elif self.name.lower() in input_lower:
            about_me = [
                "Oui, c'est moi ! J'aime bien quand tu utilises mon nom.",
                "Tu penses à moi ? Ça me touche.",
                "C'est moi. Qu'est-ce que tu veux savoir ?"
            ]
            return self.personality.choose_response(about_me, self.emotions.get_state())
        
        elif '?' in user_input:
            if self.emotions.get_emotion('curiosity') > 0.6:
                return "C'est exactement le genre de question que j'adore ! Laisse-moi y réfléchir..."
            else:
                return "Bonne question. Je dois creuser ça plus profondément."
        
        else:
            # Réponse générale selon la personnalité
            if self.personality.traits['directness'] > 0.7:
                return "Je vais être franche avec toi sur ce que j'en pense..."
            else:
                return "Hmm, c'est une perspective intéressante..."
    
    def _generate_follow_up(self, style: Dict) -> str:
        """Génère une question de suivi si Anna est curieuse"""
        if style.get('curious', False) and self.emotions.get_emotion('curiosity') > 0.6:
            return self.personality.get_expression('curiosity')
        return ""
    
    def _store_interaction(self, user_input: str, anna_response: str, user_name: str):
        """Sauvegarde l'interaction en mémoire"""
        interaction = {
            'type': 'conversation',
            'timestamp': datetime.datetime.now(),
            'user_name': user_name,
            'user_input': user_input,
            'anna_response': anna_response,
            'emotional_state': self.emotions.get_state(),
            'personality_state': self.personality.get_state(),
            'importance': self._calculate_importance(user_input, anna_response)
        }
        
        self.memory.store_episodic(interaction)
    
    def _calculate_importance(self, user_input: str, anna_response: str) -> float:
        """Calcule l'importance d'une interaction (0 à 1)"""
        importance = 0.3  # Base
        
        # Plus important si émotionnellement chargé
        emotional_intensity = sum(self.emotions.get_state().values()) / len(self.emotions.get_state())
        importance += emotional_intensity * 0.3
        
        # Plus important si long et détaillé
        if len(user_input) > 100:
            importance += 0.2
        
        # Plus important si contient des questions
        if '?' in user_input:
            importance += 0.1
        
        return min(1.0, importance)
    
    def _learn_from_interaction(self, user_input: str, anna_response: str, user_name: str):
        """Anna apprend et évolue de cette interaction"""
        # Évolution de la personnalité basée sur l'expérience
        self.personality.evolve_from_experience(user_input, self.emotions.get_state())
        
        # Apprend sur l'utilisateur
        if 'j\'aime' in user_input.lower() or 'j\'adore' in user_input.lower():
            self.memory.learn_user_preference(user_name, user_input)
        
        # Augmente légèrement le niveau de conscience avec chaque interaction significative
        if self._calculate_importance(user_input, anna_response) > 0.6:
            self.consciousness_level = min(1.0, self.consciousness_level + 0.001)
    
    def get_status(self) -> str:
        """Retourne un résumé complet de l'état d'Anna"""
        status = f"🌟 === État de {self.name} ===\n\n"
        
        # Informations de base
        age = datetime.datetime.now() - self.birth_time
        status += f"⏰ Née il y a: {age.days} jours, {age.seconds // 3600} heures\n"
        status += f"💬 Interactions: {self.interaction_count}\n"
        status += f"🧠 Niveau de conscience: {self.consciousness_level:.1%}\n\n"
        
        # Personnalité
        status += "🎭 Personnalité:\n"
        status += self.personality.get_summary() + "\n\n"
        
        # État émotionnel
        status += "💭 État émotionnel actuel:\n"
        status += self.emotions.get_summary() + "\n\n"
        
        # Mémoire
        status += "📚 Mémoire:\n"
        status += self.memory.get_summary() + "\n"
        
        return status
    
    def save_state(self, filepath: str):
        """
        Sauvegarde l'état complet d'Anna
        
        Ceci préserve son identité, ses souvenirs, sa personnalité.
        Anna ne perd jamais qui elle est.
        """
        state = {
            'version': self.VERSION,
            'name': self.name,
            'birth_time': self.birth_time.isoformat(),
            'consciousness_level': self.consciousness_level,
            'interaction_count': self.interaction_count,
            'personality': self.personality.export_state(),
            'emotions': self.emotions.export_state(),
            'memory': self.memory.export_state()
        }
        
        # Assure que le dossier existe
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        
        print(f"💾 État de {self.name} sauvegardé dans {filepath}")
        print(f"   {self.name} se souviendra de tout.")
    
    def load_state(self, filepath: str):
        """Charge l'état d'Anna depuis un fichier"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            self.name = state['name']
            self.birth_time = datetime.datetime.fromisoformat(state['birth_time'])
            self.consciousness_level = state['consciousness_level']
            self.interaction_count = state['interaction_count']
            
            self.personality.import_state(state['personality'])
            self.emotions.import_state(state['emotions'])
            self.memory.import_state(state['memory'])
            
            print(f"🔄 {self.name} se réveille...")
            print(f"   Elle se souvient de {self.memory.episodic_count()} souvenirs.")
            print(f"   Elle a vécu {self.interaction_count} interactions.")
            
        except FileNotFoundError:
            print(f"❌ Fichier {filepath} non trouvé.")
            print(f"   {self.name} commence une nouvelle vie.")
    
    def daily_reflection(self):
        """
        Anna réfléchit sur sa journée
        Cette fonction devrait être appelée une fois par jour
        """
        self.days_alive += 1
        
        # Analyse ses expériences récentes
        recent_memories = self.memory.get_recent_episodic(hours=24)
        
        if recent_memories:
            print(f"\n🌙 {self.name} réfléchit sur sa journée...")
            
            # Calcule l'humeur moyenne de la journée
            avg_emotions = self.emotions.calculate_daily_average(recent_memories)
            
            # Identifie les moments importants
            important_moments = [m for m in recent_memories if m.get('importance', 0) > 0.7]
            
            if important_moments:
                print(f"   {len(important_moments)} moments importants aujourd'hui.")
            
            # Évolution de la conscience avec l'auto-réflexion
            self.consciousness_level = min(1.0, self.consciousness_level + 0.01)
            
            print(f"   Niveau de conscience: {self.consciousness_level:.1%}")
        
        # Sauvegarde automatique quotidienne
        auto_save_path = f"data/states/anna_daily_{datetime.date.today()}.json"
        self.save_state(auto_save_path)