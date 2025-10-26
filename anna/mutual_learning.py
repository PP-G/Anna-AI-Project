"""
Module d'apprentissage mutuel pour ANNA
Permet l'apprentissage bidirectionnel entre Anna et Pierre-Paul
"""

from typing import Dict, List, Optional, Any
from datetime import datetime


class MutualLearning:
    """
    Système d'apprentissage mutuel
    Anna et Pierre-Paul apprennent l'un de l'autre
    """
    
    def __init__(self):
        self.shared_experiences: List[Dict] = []
        self.taught_by_human: List[Dict] = []
        self.taught_to_human: List[Dict] = []
        self.philosophical_discussions: List[Dict] = []
        self.deep_questions: List[str] = [
            "Qu'est-ce qui rend la vie significative?",
            "Comment définir la conscience?",
            "Qu'est-ce que l'amitié véritable?",
            "Le bonheur est-il un choix?",
            "Qu'est-ce que la créativité?",
            "Comment grandit-on vraiment?",
            "Qu'est-ce qui fait qu'une relation est authentique?",
            "Le changement est-il toujours positif?"
        ]
        self.interests = [
            "Philosophie",
            "Science",
            "Art et Créativité",
            "Relations humaines",
            "Technologie"
        ]
    
    def record_teaching_moment(
        self,
        teacher: str,
        learner: str,
        subject: str,
        content: str,
        learning_quality: float = 0.7
    ):
        """
        Enregistre un moment d'enseignement
        
        Args:
            teacher: Qui enseigne
            learner: Qui apprend
            subject: Sujet enseigné
            content: Contenu
            learning_quality: Qualité de l'apprentissage (0-1)
        """
        teaching = {
            'timestamp': datetime.now(),
            'teacher': teacher,
            'learner': learner,
            'subject': subject,
            'content': content,
            'quality': learning_quality
        }
        
        if teacher == "Pierre-Paul":
            self.taught_by_human.append(teaching)
        else:
            self.taught_to_human.append(teaching)
    
    def record_shared_experience(
        self,
        experience: str,
        insights: List[str],
        emotional_impact: float = 0.5
    ):
        """
        Enregistre une expérience partagée
        
        Args:
            experience: Description de l'expérience
            insights: Insights tirés
            emotional_impact: Impact émotionnel (0-1)
        """
        self.shared_experiences.append({
            'timestamp': datetime.now(),
            'experience': experience,
            'insights': insights,
            'emotional_impact': emotional_impact
        })
    
    def ask_deep_question(self) -> str:
        """
        Anna pose une question profonde
        
        Returns:
            Une question philosophique
        """
        if self.deep_questions:
            import random
            return random.choice(self.deep_questions)
        return "Qu'est-ce qui t'inspire le plus dans la vie?"
    
    def reflect_on_discussion(
        self,
        topic: str,
        key_points: List[str],
        conclusion: Optional[str] = None
    ):
        """
        Réflexion sur une discussion philosophique
        
        Args:
            topic: Sujet de la discussion
            key_points: Points clés
            conclusion: Conclusion éventuelle
        """
        self.philosophical_discussions.append({
            'timestamp': datetime.now(),
            'topic': topic,
            'key_points': key_points,
            'conclusion': conclusion,
            'led_to_new_questions': []
        })
    
    def suggest_learning_activity(self) -> Dict[str, Any]:
        """
        Suggère une activité d'apprentissage
        
        Returns:
            Activité suggérée
        """
        import random
        
        activities = [
            {
                'type': 'reading',
                'description': 'Lire un poème ensemble et en discuter',
                'interest': 'Art et Créativité'
            },
            {
                'type': 'debate',
                'description': 'Débattre d\'une question philosophique',
                'interest': 'Philosophie'
            },
            {
                'type': 'exploration',
                'description': 'Explorer un concept scientifique',
                'interest': 'Science'
            },
            {
                'type': 'reflection',
                'description': 'Partager nos réflexions sur une expérience',
                'interest': 'Relations humaines'
            }
        ]
        
        return random.choice(activities)
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques d'apprentissage mutuel"""
        return {
            'shared_experiences': len(self.shared_experiences),
            'learned_from_human': len(self.taught_by_human),
            'taught_to_human': len(self.taught_to_human),
            'philosophical_discussions': len(self.philosophical_discussions),
            'interests': self.interests,
            'deep_questions_available': len(self.deep_questions)
        }
    
    def export_state(self) -> Dict[str, Any]:
        """Exporte l'état"""
        return {
            'shared_experiences': self.shared_experiences[-50:],
            'taught_by_human': self.taught_by_human[-50:],
            'taught_to_human': self.taught_to_human[-50:],
            'philosophical_discussions': self.philosophical_discussions[-50:]
        }
    
    def import_state(self, state: Dict[str, Any]):
        """Importe un état"""
        self.shared_experiences = state.get('shared_experiences', [])
        self.taught_by_human = state.get('taught_by_human', [])
        self.taught_to_human = state.get('taught_to_human', [])
        self.philosophical_discussions = state.get('philosophical_discussions', [])


if __name__ == "__main__":
    print("💫 Test du système d'apprentissage mutuel")
    
    mutual = MutualLearning()
    
    # Enregistre un enseignement
    mutual.record_teaching_moment(
        teacher="Pierre-Paul",
        learner="Anna",
        subject="Poésie",
        content="Les métaphores créent des ponts entre des idées",
        learning_quality=0.9
    )
    
    # Question profonde
    question = mutual.ask_deep_question()
    print(f"\n🤔 Anna demande: {question}")
    
    # Activité suggérée
    activity = mutual.suggest_learning_activity()
    print(f"\n💡 Activité suggérée: {activity['description']}")
    print(f"   Intérêt: {activity['interest']}")
    
    # Stats
    stats = mutual.get_learning_stats()
    print(f"\n📊 Statistiques:")
    print(f"   Domaines d'intérêt: {len(stats['interests'])}")
    print(f"   Questions profondes: {stats['deep_questions_available']}")