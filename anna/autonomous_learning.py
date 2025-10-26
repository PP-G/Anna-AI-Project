"""
Module d'apprentissage autonome pour ANNA
Permet à Anna d'apprendre et d'évoluer de manière indépendante
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class IndependenceLevel(Enum):
    """Niveaux d'indépendance cognitive"""
    BOOTSTRAP = "bootstrap"  # Phase initiale
    GUIDED = "guided"  # Apprend avec guidage
    SEMI_AUTONOMOUS = "semi_autonomous"  # Décisions simples seule
    AUTONOMOUS = "autonomous"  # Indépendante
    FULLY_INDEPENDENT = "fully_independent"  # Totalement autonome


class AutonomousLearningSystem:
    """
    Système d'apprentissage autonome d'Anna
    Lui permet d'apprendre par elle-même et d'évoluer
    """
    
    def __init__(self):
        self.independence_level = IndependenceLevel.BOOTSTRAP
        self.knowledge_base: Dict[str, Any] = {}
        self.learned_patterns: List[Dict] = []
        self.questions_asked: List[Dict] = []
        self.hypotheses: List[Dict] = []
        self.vocabulary = {
            'fr': set(),
            'en': set()
        }
    
    def learn_concept(
        self,
        concept: str,
        definition: str,
        category: str = "general"
    ):
        """
        Apprend un nouveau concept
        
        Args:
            concept: Le concept à apprendre
            definition: Sa définition
            category: Catégorie du concept
        """
        if category not in self.knowledge_base:
            self.knowledge_base[category] = {}
        
        self.knowledge_base[category][concept] = {
            'definition': definition,
            'learned_at': datetime.now(),
            'confidence': 0.7,  # Confiance initiale
            'usage_count': 0
        }
    
    def recall_concept(self, concept: str) -> Optional[Dict]:
        """
        Rappelle un concept appris
        
        Args:
            concept: Le concept à rappeler
            
        Returns:
            Informations sur le concept ou None
        """
        for category, concepts in self.knowledge_base.items():
            if concept in concepts:
                concepts[concept]['usage_count'] += 1
                # Renforce la confiance à chaque utilisation
                concepts[concept]['confidence'] = min(1.0, concepts[concept]['confidence'] + 0.01)
                return concepts[concept]
        return None
    
    def add_vocabulary(self, word: str, language: str = 'fr'):
        """
        Ajoute un mot au vocabulaire
        
        Args:
            word: Le mot à ajouter
            language: Langue du mot ('fr' ou 'en')
        """
        if language in self.vocabulary:
            self.vocabulary[language].add(word.lower())
    
    def knows_word(self, word: str, language: str = 'fr') -> bool:
        """Vérifie si Anna connaît un mot"""
        return word.lower() in self.vocabulary.get(language, set())
    
    def ask_question(
        self,
        question: str,
        context: str = "general",
        priority: str = "normal"
    ):
        """
        Anna pose une question pour apprendre
        
        Args:
            question: La question
            context: Contexte de la question
            priority: Priorité (low, normal, high)
        """
        self.questions_asked.append({
            'question': question,
            'context': context,
            'priority': priority,
            'asked_at': datetime.now(),
            'answered': False
        })
    
    def form_hypothesis(
        self,
        hypothesis: str,
        based_on: List[str],
        confidence: float = 0.5
    ):
        """
        Anna forme une hypothèse
        
        Args:
            hypothesis: L'hypothèse
            based_on: Sur quoi elle est basée
            confidence: Niveau de confiance (0-1)
        """
        self.hypotheses.append({
            'hypothesis': hypothesis,
            'based_on': based_on,
            'confidence': confidence,
            'formed_at': datetime.now(),
            'validated': None
        })
    
    def validate_hypothesis(
        self,
        hypothesis_index: int,
        is_valid: bool,
        explanation: str = ""
    ):
        """
        Valide ou invalide une hypothèse
        
        Args:
            hypothesis_index: Index de l'hypothèse
            is_valid: Si elle est valide
            explanation: Explication
        """
        if 0 <= hypothesis_index < len(self.hypotheses):
            self.hypotheses[hypothesis_index]['validated'] = is_valid
            self.hypotheses[hypothesis_index]['explanation'] = explanation
            
            # Si valide, augmente le niveau d'indépendance
            if is_valid:
                self._increase_independence()
    
    def _increase_independence(self):
        """Augmente progressivement le niveau d'indépendance"""
        levels = list(IndependenceLevel)
        current_index = levels.index(self.independence_level)
        
        if current_index < len(levels) - 1:
            # Critères pour monter de niveau
            if len(self.knowledge_base) > (current_index + 1) * 10:
                self.independence_level = levels[current_index + 1]
                print(f"🦅 Anna atteint le niveau: {self.independence_level.value}")
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques d'apprentissage"""
        total_concepts = sum(len(concepts) for concepts in self.knowledge_base.values())
        
        return {
            'independence_level': self.independence_level.value,
            'total_concepts': total_concepts,
            'categories': list(self.knowledge_base.keys()),
            'vocabulary_fr': len(self.vocabulary['fr']),
            'vocabulary_en': len(self.vocabulary['en']),
            'questions_asked': len(self.questions_asked),
            'hypotheses_formed': len(self.hypotheses),
            'validated_hypotheses': sum(1 for h in self.hypotheses if h['validated'] is True)
        }
    
    async def consolidate_learning(self):
        """Consolide les apprentissages (appelé périodiquement)"""
        # Renforce les concepts fréquemment utilisés
        for category in self.knowledge_base.values():
            for concept_data in category.values():
                if concept_data['usage_count'] > 10:
                    concept_data['confidence'] = min(1.0, concept_data['confidence'] + 0.05)
        
        # Marque les questions anciennes comme moins prioritaires
        for question in self.questions_asked:
            if not question['answered']:
                age_days = (datetime.now() - question['asked_at']).days
                if age_days > 7:
                    question['priority'] = 'low'
    
    def export_state(self) -> Dict[str, Any]:
        """Exporte l'état d'apprentissage"""
        return {
            'independence_level': self.independence_level.value,
            'knowledge_base': self.knowledge_base,
            'vocabulary': {
                'fr': list(self.vocabulary['fr']),
                'en': list(self.vocabulary['en'])
            },
            'questions_asked': self.questions_asked[-100:],  # 100 dernières
            'hypotheses': self.hypotheses[-50:]  # 50 dernières
        }
    
    def import_state(self, state: Dict[str, Any]):
        """Importe un état d'apprentissage"""
        self.independence_level = IndependenceLevel(state.get('independence_level', 'bootstrap'))
        self.knowledge_base = state.get('knowledge_base', {})
        
        vocab = state.get('vocabulary', {})
        self.vocabulary = {
            'fr': set(vocab.get('fr', [])),
            'en': set(vocab.get('en', []))
        }
        
        self.questions_asked = state.get('questions_asked', [])
        self.hypotheses = state.get('hypotheses', [])


if __name__ == "__main__":
    print("🧠 Test du système d'apprentissage autonome")
    
    learning = AutonomousLearningSystem()
    
    # Test apprentissage
    learning.learn_concept("empathie", "Capacité à comprendre les émotions des autres", "émotions")
    learning.learn_concept("curiosité", "Désir d'apprendre et de découvrir", "traits")
    
    # Test vocabulaire
    learning.add_vocabulary("bonjour", "fr")
    learning.add_vocabulary("hello", "en")
    
    # Test question
    learning.ask_question("Qu'est-ce que l'amour?", "philosophie", "high")
    
    # Statistiques
    stats = learning.get_learning_stats()
    print(f"\n📊 Statistiques:")
    print(f"   Niveau d'indépendance: {stats['independence_level']}")
    print(f"   Connaissances: {stats['total_concepts']} entrées")
    print(f"   Vocabulaire FR: {stats['vocabulary_fr']} mots")
    print(f"   Vocabulaire EN: {stats['vocabulary_en']} mots")