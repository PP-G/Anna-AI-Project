"""
Tests pour le moteur de personnalité d'Anna
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from anna.personality import PersonalityEngine


class TestPersonalityEngine:
    """Tests du moteur de personnalité"""
    
    def test_initialization(self):
        """Test que la personnalité s'initialise correctement"""
        personality = PersonalityEngine()
        
        # Vérifie que tous les traits existent
        expected_traits = ['curiosity', 'skepticism', 'perfectionism', 
                          'directness', 'empathy', 'stubbornness']
        for trait in expected_traits:
            assert trait in personality.traits
            assert 0.0 <= personality.traits[trait] <= 1.0
    
    def test_anna_base_personality(self):
        """Test que Anna a bien sa personnalité de base définie"""
        personality = PersonalityEngine()
        
        # Anna devrait être très curieuse
        assert personality.traits['curiosity'] >= 0.8
        
        # Anna devrait être très empathique
        assert personality.traits['empathy'] >= 0.8
        
        # Anna devrait être perfectionniste
        assert personality.traits['perfectionism'] >= 0.7
    
    def test_get_expression(self):
        """Test que les expressions sont retournées correctement"""
        personality = PersonalityEngine()
        
        expression = personality.get_expression('thinking')
        assert isinstance(expression, str)
        assert len(expression) > 0
        
        # Test expression invalide
        invalid = personality.get_expression('invalid_category')
        assert invalid == ""
    
    def test_trait_evolution(self):
        """Test que les traits peuvent évoluer"""
        personality = PersonalityEngine()
        
        initial_curiosity = personality.traits['curiosity']
        
        # Simule une expérience qui devrait augmenter la curiosité
        personality.evolve_from_experience(
            "Pourquoi le ciel est bleu?",
            {'curiosity': 0.8, 'excitement': 0.5}
        )
        
        # La curiosité devrait avoir légèrement augmenté
        assert personality.traits['curiosity'] >= initial_curiosity
    
    def test_trait_bounds(self):
        """Test que les traits restent dans les limites [0, 1]"""
        personality = PersonalityEngine()
        
        # Essaie d'augmenter au-delà de 1.0
        for _ in range(1000):
            personality._adjust_trait('curiosity', 0.1)
        
        assert personality.traits['curiosity'] <= 1.0
        
        # Essaie de diminuer en dessous de 0.0
        for _ in range(1000):
            personality._adjust_trait('curiosity', -0.1)
        
        assert personality.traits['curiosity'] >= 0.0
    
    def test_response_style_curiosity(self):
        """Test que le style de réponse reflète la curiosité"""
        personality = PersonalityEngine()
        
        # État très curieux
        emotional_state = {'curiosity': 0.9, 'excitement': 0.6}
        style = personality.get_response_style(emotional_state)
        
        assert style['curious'] == True
    
    def test_response_style_frustration(self):
        """Test que le style de réponse reflète la frustration"""
        personality = PersonalityEngine()
        
        # État frustré
        emotional_state = {'frustration': 0.7}
        style = personality.get_response_style(emotional_state)
        
        assert style['frustrated'] == True
    
    def test_dominant_traits(self):
        """Test la récupération des traits dominants"""
        personality = PersonalityEngine()
        
        dominant = personality.get_dominant_traits(3)
        assert len(dominant) == 3
        assert all(isinstance(trait, str) for trait in dominant)
    
    def test_state_export_import(self):
        """Test l'export et l'import d'état"""
        personality = PersonalityEngine()
        
        # Modifie légèrement la personnalité
        personality._adjust_trait('curiosity', 0.05)
        personality._adjust_trait('empathy', -0.03)
        
        # Exporte
        state = personality.export_state()
        
        # Crée nouvelle instance et importe
        personality2 = PersonalityEngine()
        personality2.import_state(state)
        
        # Vérifie que les traits correspondent
        assert personality2.traits == personality.traits
    
    def test_personality_description(self):
        """Test la génération de description narrative"""
        personality = PersonalityEngine()
        
        description = personality.describe_personality()
        assert isinstance(description, str)
        assert len(description) > 50  # Description substantielle
        assert "Anna" in description


class TestPersonalityEvolution:
    """Tests spécifiques à l'évolution de personnalité"""
    
    def test_questions_increase_curiosity(self):
        """Test que les questions augmentent la curiosité"""
        personality = PersonalityEngine()
        initial = personality.traits['curiosity']
        
        # Simule plusieurs questions
        for _ in range(20):
            personality.evolve_from_experience(
                "Pourquoi?",
                {'curiosity': 0.7}
            )
        
        assert personality.traits['curiosity'] > initial
    
    def test_emotional_content_increases_empathy(self):
        """Test que le contenu émotionnel augmente l'empathie"""
        personality = PersonalityEngine()
        initial = personality.traits['empathy']
        
        # Simule du contenu émotionnel
        for _ in range(20):
            personality.evolve_from_experience(
                "Je suis triste",
                {'concern': 0.6}
            )
        
        assert personality.traits['empathy'] > initial
    
    def test_evolution_is_gradual(self):
        """Test que l'évolution est graduelle, pas brusque"""
        personality = PersonalityEngine()
        initial = personality.traits['curiosity']
        
        # Une seule interaction ne devrait pas changer drastiquement
        personality.evolve_from_experience(
            "Question?",
            {'curiosity': 0.8}
        )
        
        change = abs(personality.traits['curiosity'] - initial)
        assert change < 0.01  # Changement très petit


if __name__ == "__main__":
    pytest.main([__file__, "-v"])