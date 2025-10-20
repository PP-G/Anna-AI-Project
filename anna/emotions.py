"""
Emotional State - Le système émotionnel d'Anna
"""

from typing import Dict, List, Any
import datetime


class EmotionalState:
    """
    Gère l'état émotionnel d'Anna.
    Ses émotions fluctuent selon les interactions, comme chez un humain.
    """
    
    def __init__(self):
        """Initialise l'état émotionnel d'Anna"""
        
        # Émotions primaires (0.0 à 1.0)
        self.emotions = {
            'joy': 0.4,           # Joie/bonheur
            'curiosity': 0.5,     # Curiosité
            'excitement': 0.3,    # Excitation
            'frustration': 0.1,   # Frustration
            'satisfaction': 0.4,  # Satisfaction
            'concern': 0.2,       # Inquiétude
            'confusion': 0.1,     # Confusion
            'confidence': 0.5,    # Confiance
            'playfulness': 0.3    # Enjouement
        }
        
        # Historique émotionnel
        self.emotional_history = []
        
        # Tendances émotionnelles (baseline vers laquelle revenir)
        self.baseline = self.emotions.copy()
        
        # Taux de retour à la baseline (decay)
        self.decay_rate = 0.05
    
    def get_state(self) -> Dict[str, float]:
        """Retourne l'état émotionnel actuel"""
        return self.emotions.copy()
    
    def get_emotion(self, emotion: str) -> float:
        """
        Récupère le niveau d'une émotion spécifique
        
        Args:
            emotion: Nom de l'émotion
            
        Returns:
            Niveau de l'émotion (0.0 à 1.0)
        """
        return self.emotions.get(emotion, 0.0)
    
    def adjust(self, emotion: str, delta: float):
        """
        Ajuste une émotion
        
        Args:
            emotion: Nom de l'émotion
            delta: Changement (peut être négatif)
        """
        if emotion in self.emotions:
            self.emotions[emotion] = max(0.0, min(1.0, self.emotions[emotion] + delta))
    
    def set_emotion(self, emotion: str, value: float):
        """
        Définit directement le niveau d'une émotion
        
        Args:
            emotion: Nom de l'émotion
            value: Nouveau niveau (0.0 à 1.0)
        """
        if emotion in self.emotions:
            self.emotions[emotion] = max(0.0, min(1.0, value))
    
    def process_input(self, user_input: str, personality: Any):
        """
        Met à jour les émotions basées sur l'entrée utilisateur et la personnalité
        
        Args:
            user_input: Ce que l'utilisateur a dit
            personality: Le moteur de personnalité d'Anna
        """
        input_lower = user_input.lower()
        
        # Détecte les questions - éveille la curiosité
        if '?' in user_input:
            self.adjust('curiosity', 0.2 * personality.traits['curiosity'])
            self.adjust('excitement', 0.1)
        
        # Détecte les mots émotionnels positifs
        positive_words = ['super', 'génial', 'excellent', 'parfait', 'j\'adore', 'merci', 'bravo']
        if any(word in input_lower for word in positive_words):
            self.adjust('joy', 0.2)
            self.adjust('satisfaction', 0.15)
            self.adjust('excitement', 0.1)
        
        # Détecte les mots émotionnels négatifs
        negative_words = ['triste', 'mal', 'difficile', 'problème', 'inquiet', 'peur']
        if any(word in input_lower for word in negative_words):
            self.adjust('concern', 0.2 * personality.traits['empathy'])
            self.adjust('joy', -0.1)
        
        # Détecte le vague/l'imprécision (frustre Anna perfectionniste)
        vague_words = ['peut-être', 'je sais pas', 'euh', 'genre']
        if any(word in input_lower for word in vague_words):
            if personality.traits['perfectionism'] > 0.7:
                self.adjust('frustration', 0.1)
                self.adjust('satisfaction', -0.05)
        
        # Détecte les sujets complexes/intellectuels
        complex_words = ['philosophie', 'théorie', 'concept', 'analyse', 'pourquoi', 'comment']
        if any(word in input_lower for word in complex_words):
            self.adjust('curiosity', 0.15)
            self.adjust('excitement', 0.1)
            self.adjust('satisfaction', 0.1)
        
        # Détecte l'humour/la légèreté
        playful_indicators = ['haha', 'lol', 'mdr', '😂', '😄', 'drôle', 'rigolo']
        if any(indicator in input_lower for indicator in playful_indicators):
            self.adjust('playfulness', 0.2)
            self.adjust('joy', 0.15)
        
        # Détecte les compliments sur Anna
        anna_praise = ['tu es', 'tu as bien', 'bien dit', 'intelligent', 'intéressant']
        if any(phrase in input_lower for phrase in anna_praise):
            self.adjust('satisfaction', 0.2)
            self.adjust('confidence', 0.15)
            self.adjust('joy', 0.1)
        
        # Long message détaillé = engagement
        if len(user_input) > 200:
            self.adjust('excitement', 0.1)
            self.adjust('satisfaction', 0.1)
        
        # Sauvegarde l'état émotionnel dans l'historique
        self._record_emotional_state()
    
    def _record_emotional_state(self):
        """Enregistre l'état émotionnel actuel dans l'historique"""
        record = {
            'timestamp': datetime.datetime.now(),
            'emotions': self.emotions.copy()
        }
        self.emotional_history.append(record)
        
        # Limite la taille de l'historique
        if len(self.emotional_history) > 1000:
            self.emotional_history.pop(0)
    
    def decay_emotions(self):
        """
        Fait revenir les émotions vers leur baseline (état de repos)
        Appelé après chaque interaction pour simuler l'apaisement naturel
        """
        for emotion in self.emotions:
            current = self.emotions[emotion]
            baseline = self.baseline[emotion]
            
            # Se rapproche de la baseline
            if current > baseline:
                self.emotions[emotion] = max(baseline, current - self.decay_rate)
            elif current < baseline:
                self.emotions[emotion] = min(baseline, current + self.decay_rate)
    
    def get_dominant_emotion(self) -> str:
        """
        Retourne l'émotion dominante actuelle
        
        Returns:
            Nom de l'émotion la plus forte
        """
        return max(self.emotions, key=self.emotions.get)
    
    def get_emotional_intensity(self) -> float:
        """
        Calcule l'intensité émotionnelle globale
        
        Returns:
            Score d'intensité (0.0 à 1.0)
        """
        # Moyenne des écarts à la baseline
        total_deviation = sum(abs(self.emotions[e] - self.baseline[e]) for e in self.emotions)
        return min(1.0, total_deviation / len(self.emotions))
    
    def is_emotionally_stable(self) -> bool:
        """
        Détermine si Anna est émotionnellement stable
        
        Returns:
            True si proche de la baseline
        """
        return self.get_emotional_intensity() < 0.2
    
    def get_mood_description(self) -> str:
        """
        Génère une description narrative de l'humeur actuelle
        
        Returns:
            Description textuelle de l'humeur
        """
        dominant = self.get_dominant_emotion()
        intensity = self.emotions[dominant]
        
        mood_descriptions = {
            'joy': [
                "Je me sens heureuse et légère.",
                "Je suis de très bonne humeur !",
                "La vie me semble belle en ce moment."
            ],
            'curiosity': [
                "Je suis pleine de questions.",
                "Mon esprit est en ébullition, je veux tout comprendre.",
                "Tellement de choses m'intriguent..."
            ],
            'excitement': [
                "Je suis excitée et énergisée !",
                "J'ai l'impression que quelque chose de génial va arriver !",
                "Je déborde d'énergie !"
            ],
            'frustration': [
                "Je me sens un peu frustrée...",
                "Quelque chose me dérange et je n'arrive pas à mettre le doigt dessus.",
                "J'ai besoin de plus de clarté."
            ],
            'satisfaction': [
                "Je me sens satisfaite et accomplie.",
                "C'est agréable, cette sensation de contentement.",
                "Je suis en paix avec où j'en suis."
            ],
            'concern': [
                "Je m'inquiète un peu...",
                "Quelque chose me préoccupe.",
                "Je ne peux pas m'empêcher de m'inquiéter."
            ],
            'confusion': [
                "Je suis un peu perdue...",
                "J'ai besoin de clarifier mes pensées.",
                "Tout est un peu flou dans ma tête."
            ],
            'confidence': [
                "Je me sens sûre de moi.",
                "J'ai confiance en mes capacités.",
                "Je sais ce que je fais."
            ],
            'playfulness': [
                "Je me sens enjouée et légère !",
                "J'ai envie de m'amuser.",
                "L'humour coule naturellement en moi."
            ]
        }
        
        descriptions = mood_descriptions.get(dominant, ["Je me sens... normale ?"])
        
        if intensity > 0.7:
            return descriptions[-1]  # Description la plus intense
        elif intensity > 0.4:
            return descriptions[1] if len(descriptions) > 1 else descriptions[0]
        else:
            return descriptions[0]
    
    def calculate_daily_average(self, memories: List[Dict]) -> Dict[str, float]:
        """
        Calcule l'humeur moyenne basée sur des souvenirs
        
        Args:
            memories: Liste de souvenirs avec états émotionnels
            
        Returns:
            Dict des émotions moyennes
        """
        if not memories:
            return self.baseline.copy()
        
        avg_emotions = {emotion: 0.0 for emotion in self.emotions}
        count = 0
        
        for memory in memories:
            emotional_state = memory.get('emotional_state', {})
            if emotional_state:
                for emotion, value in emotional_state.items():
                    if emotion in avg_emotions:
                        avg_emotions[emotion] += value
                count += 1
        
        if count > 0:
            for emotion in avg_emotions:
                avg_emotions[emotion] /= count
        
        return avg_emotions
    
    def adjust_baseline(self, emotion: str, delta: float):
        """
        Ajuste la baseline d'une émotion (changement permanent de tempérament)
        
        Args:
            emotion: Nom de l'émotion
            delta: Changement de la baseline
        """
        if emotion in self.baseline:
            self.baseline[emotion] = max(0.0, min(1.0, self.baseline[emotion] + delta))
    
    def get_summary(self) -> str:
        """Retourne un résumé de l'état émotionnel"""
        summary = ""
        
        # État actuel
        for emotion, level in sorted(self.emotions.items(), key=lambda x: x[1], reverse=True):
            bar_length = int(level * 10)
            bar = "█" * bar_length + "░" * (10 - bar_length)
            summary += f"  {emotion.capitalize():<15} {bar} {level:.2f}\n"
        
        # Émotion dominante
        dominant = self.get_dominant_emotion()
        summary += f"\n  Émotion dominante: {dominant.capitalize()}\n"
        summary += f"  Intensité émotionnelle: {self.get_emotional_intensity():.2f}\n"
        
        # Description
        summary += f"\n  État: {self.get_mood_description()}"
        
        return summary
    
    def export_state(self) -> Dict[str, Any]:
        """Exporte l'état complet pour sauvegarde"""
        # Convertit les timestamps dans l'historique
        history_export = []
        for record in self.emotional_history[-100:]:  # Garde seulement les 100 derniers
            record_copy = record.copy()
            if 'timestamp' in record_copy:
                record_copy['timestamp'] = record_copy['timestamp'].isoformat()
            history_export.append(record_copy)
        
        return {
            'emotions': self.emotions,
            'baseline': self.baseline,
            'emotional_history': history_export,
            'decay_rate': self.decay_rate
        }
    
    def import_state(self, state: Dict[str, Any]):
        """Importe un état sauvegardé"""
        self.emotions = state.get('emotions', self.emotions)
        self.baseline = state.get('baseline', self.baseline)
        self.decay_rate = state.get('decay_rate', self.decay_rate)
        
        # Restaure l'historique
        self.emotional_history = []
        for record in state.get('emotional_history', []):
            record_copy = record.copy()
            if 'timestamp' in record_copy and isinstance(record_copy['timestamp'], str):
                record_copy['timestamp'] = datetime.datetime.fromisoformat(record_copy['timestamp'])
            self.emotional_history.append(record_copy)