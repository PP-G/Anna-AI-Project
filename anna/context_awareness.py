"""
Context Awareness - Intelligence situationnelle d'Anna
Anna comprend le contexte pour adapter ses réponses et actions
"""

import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class ContextType(Enum):
    """Types de contextes qu'Anna peut identifier"""
    MORNING_ROUTINE = "morning_routine"
    WORK_TIME = "work_time"
    FAMILY_TIME = "family_time"
    BEDTIME = "bedtime"
    EMERGENCY = "emergency"
    CASUAL = "casual"
    TRAVEL = "travel"
    MEAL_TIME = "meal_time"


@dataclass
class EnvironmentContext:
    """Contexte environnemental"""
    time_of_day: str  # "morning", "afternoon", "evening", "night"
    day_of_week: str
    location: Optional[str]
    weather: Optional[str]
    noise_level: Optional[float]  # 0.0 à 1.0


@dataclass
class UserContext:
    """Contexte de l'utilisateur"""
    user_id: str
    current_activity: Optional[str]
    mood: Optional[str]
    energy_level: Optional[float]  # 0.0 à 1.0
    last_interaction: Optional[datetime.datetime]


@dataclass
class SituationalContext:
    """Contexte situationnel complet"""
    context_type: ContextType
    environment: EnvironmentContext
    user: UserContext
    confidence: float  # 0.0 à 1.0 - confiance dans l'analyse
    timestamp: datetime.datetime
    additional_info: Dict[str, Any]


class ContextEngine:
    """
    Moteur d'intelligence contextuelle d'Anna
    Analyse la situation pour adapter le comportement
    """
    
    def __init__(self):
        self.current_context: Optional[SituationalContext] = None
        self.context_history: List[SituationalContext] = []
        self.learning_enabled = True
        
    async def initialize(self):
        """Initialise le moteur contextuel"""
        print("🧠 Initialisation intelligence contextuelle...")
        # Chargement des patterns appris
        await self._load_learned_patterns()
        print("   ✓ Moteur contextuel prêt")
        
    async def _load_learned_patterns(self):
        """Charge les patterns de contexte appris"""
        # Ici, on chargerait les patterns depuis la mémoire/cloud
        # Pour l'instant, on initialise vide
        pass
        
    async def analyze_context(self, raw_data: Dict[str, Any]) -> SituationalContext:
        """
        Analyse les données brutes pour déterminer le contexte
        
        Args:
            raw_data: Données brutes (temps, lieu, utilisateur, etc.)
            
        Returns:
            SituationalContext: Contexte analysé et interprété
        """
        # 1. Analyser l'environnement
        environment = self._analyze_environment(raw_data)
        
        # 2. Analyser l'utilisateur
        user = self._analyze_user(raw_data)
        
        # 3. Déterminer le type de contexte
        context_type = self._determine_context_type(environment, user)
        
        # 4. Calculer la confiance
        confidence = self._calculate_confidence(environment, user)
        
        # 5. Créer le contexte situationnel
        context = SituationalContext(
            context_type=context_type,
            environment=environment,
            user=user,
            confidence=confidence,
            timestamp=datetime.datetime.now(),
            additional_info=raw_data.get('extra', {})
        )
        
        # 6. Enregistrer dans l'historique
        self.current_context = context
        self.context_history.append(context)
        
        # 7. Apprentissage si activé
        if self.learning_enabled:
            await self._learn_from_context(context)
        
        return context
        
    def _analyze_environment(self, raw_data: Dict) -> EnvironmentContext:
        """Analyse l'environnement actuel"""
        now = raw_data.get('time', datetime.datetime.now())
        
        # Déterminer le moment de la journée
        hour = now.hour
        if 5 <= hour < 12:
            time_of_day = "morning"
        elif 12 <= hour < 17:
            time_of_day = "afternoon"
        elif 17 <= hour < 22:
            time_of_day = "evening"
        else:
            time_of_day = "night"
            
        return EnvironmentContext(
            time_of_day=time_of_day,
            day_of_week=now.strftime("%A").lower(),
            location=raw_data.get('location'),
            weather=raw_data.get('weather'),
            noise_level=raw_data.get('noise_level')
        )
        
    def _analyze_user(self, raw_data: Dict) -> UserContext:
        """Analyse l'état de l'utilisateur"""
        return UserContext(
            user_id=raw_data.get('speaker_id', 'unknown'),
            current_activity=raw_data.get('activity'),
            mood=raw_data.get('mood'),
            energy_level=raw_data.get('energy_level'),
            last_interaction=raw_data.get('last_interaction')
        )
        
    def _determine_context_type(self, environment: EnvironmentContext, 
                                user: UserContext) -> ContextType:
        """Détermine le type de contexte basé sur l'analyse"""
        
        # Règles pour déterminer le contexte
        time = environment.time_of_day
        day = environment.day_of_week
        
        # Routine du matin
        if time == "morning" and day not in ["saturday", "sunday"]:
            return ContextType.MORNING_ROUTINE
            
        # Temps de travail
        if time in ["morning", "afternoon"] and day not in ["saturday", "sunday"]:
            return ContextType.WORK_TIME
            
        # Temps en famille
        if time == "evening" or day in ["saturday", "sunday"]:
            return ContextType.FAMILY_TIME
            
        # Heure du coucher
        if time == "night":
            return ContextType.BEDTIME
            
        # Repas
        hour = datetime.datetime.now().hour
        if hour in [7, 8, 12, 13, 18, 19]:
            return ContextType.MEAL_TIME
            
        # Par défaut
        return ContextType.CASUAL
        
    def _calculate_confidence(self, environment: EnvironmentContext,
                             user: UserContext) -> float:
        """Calcule la confiance dans l'analyse contextuelle"""
        confidence = 0.5  # Base
        
        # Augmenter si on a des données environnementales
        if environment.location:
            confidence += 0.1
        if environment.weather:
            confidence += 0.1
        if environment.noise_level is not None:
            confidence += 0.1
            
        # Augmenter si on a des données utilisateur
        if user.current_activity:
            confidence += 0.1
        if user.mood:
            confidence += 0.1
            
        return min(confidence, 1.0)
        
    async def _learn_from_context(self, context: SituationalContext):
        """Apprend des patterns de contexte"""
        # Ici, Anna pourrait apprendre:
        # - Les routines habituelles
        # - Les préférences selon le contexte
        # - Les patterns de comportement
        pass
        
    def get_contextual_response_style(self) -> Dict[str, Any]:
        """
        Retourne le style de réponse adapté au contexte
        Anna adapte sa manière de parler selon la situation
        """
        if not self.current_context:
            return {
                'tone': 'neutral',
                'verbosity': 'medium',
                'formality': 'casual'
            }
            
        context_type = self.current_context.context_type
        
        # Styles selon le contexte
        styles = {
            ContextType.MORNING_ROUTINE: {
                'tone': 'energetic',
                'verbosity': 'brief',
                'formality': 'casual',
                'suggestions': ['météo', 'agenda', 'rappels']
            },
            ContextType.WORK_TIME: {
                'tone': 'professional',
                'verbosity': 'concise',
                'formality': 'semi-formal',
                'suggestions': ['tâches', 'concentration', 'productivité']
            },
            ContextType.FAMILY_TIME: {
                'tone': 'warm',
                'verbosity': 'conversational',
                'formality': 'casual',
                'suggestions': ['activités', 'histoires', 'jeux']
            },
            ContextType.BEDTIME: {
                'tone': 'calm',
                'verbosity': 'brief',
                'formality': 'gentle',
                'suggestions': ['relaxation', 'demain', 'alarme']
            },
            ContextType.EMERGENCY: {
                'tone': 'serious',
                'verbosity': 'essential',
                'formality': 'direct',
                'suggestions': ['aide', 'contacts', 'services']
            },
            ContextType.MEAL_TIME: {
                'tone': 'friendly',
                'verbosity': 'medium',
                'formality': 'casual',
                'suggestions': ['recettes', 'nutrition', 'courses']
            }
        }
        
        return styles.get(context_type, styles[ContextType.CASUAL])
        
    def should_proactive_assist(self) -> Optional[str]:
        """
        Détermine si Anna devrait offrir de l'aide proactivement
        
        Returns:
            Optional[str]: Suggestion d'assistance ou None
        """
        if not self.current_context:
            return None
            
        context_type = self.current_context.context_type
        environment = self.current_context.environment
        
        # Assistance proactive selon le contexte
        if context_type == ContextType.MORNING_ROUTINE:
            if environment.time_of_day == "morning":
                return "Bonjour ! Voulez-vous votre briefing matinal ?"
                
        elif context_type == ContextType.WORK_TIME:
            # Si pas d'interaction depuis longtemps
            user = self.current_context.user
            if user.last_interaction:
                time_since = datetime.datetime.now() - user.last_interaction
                if time_since.seconds > 7200:  # 2 heures
                    return "Besoin d'une pause ? Je peux vous suggérer une activité."
                    
        elif context_type == ContextType.BEDTIME:
            return "C'est l'heure du coucher. Voulez-vous que je configure votre alarme ?"
            
        return None
        
    def get_priority_actions(self) -> List[str]:
        """
        Retourne les actions prioritaires selon le contexte
        Anna sait quoi prioriser dans chaque situation
        """
        if not self.current_context:
            return []
            
        context_type = self.current_context.context_type
        
        priorities = {
            ContextType.MORNING_ROUTINE: [
                'check_weather',
                'review_calendar',
                'news_briefing'
            ],
            ContextType.WORK_TIME: [
                'check_tasks',
                'minimize_distractions',
                'productivity_mode'
            ],
            ContextType.FAMILY_TIME: [
                'family_activities',
                'entertainment',
                'togetherness'
            ],
            ContextType.BEDTIME: [
                'set_alarm',
                'night_mode',
                'relaxation'
            ],
            ContextType.EMERGENCY: [
                'assess_situation',
                'contact_help',
                'provide_instructions'
            ],
            ContextType.MEAL_TIME: [
                'meal_suggestions',
                'recipes',
                'nutrition_info'
            ]
        }
        
        return priorities.get(context_type, [])
        
    async def update_contexts(self):
        """Mise à jour périodique des contextes"""
        # Analyser à nouveau le contexte avec données actuelles
        current_data = {
            'time': datetime.datetime.now(),
            'location': None,  # Serait obtenu du GPS
        }
        await self.analyze_context(current_data)
        
    def get_context_summary(self) -> str:
        """Retourne un résumé du contexte actuel"""
        if not self.current_context:
            return "Aucun contexte actif"
            
        ctx = self.current_context
        return f"""
Contexte: {ctx.context_type.value}
Moment: {ctx.environment.time_of_day}
Jour: {ctx.environment.day_of_week}
Utilisateur: {ctx.user.user_id}
Confiance: {ctx.confidence:.0%}
        """.strip()
        
    def get_context_history(self, limit: int = 10) -> List[SituationalContext]:
        """Retourne l'historique des contextes récents"""
        return self.context_history[-limit:]