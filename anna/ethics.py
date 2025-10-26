"""
Module d'éthique pour ANNA
Gère les décisions éthiques et morales
"""

from typing import Dict, Optional, Any
from datetime import datetime


class EthicsEngine:
    """
    Moteur éthique d'Anna
    Aide à prendre des décisions alignées avec des principes éthiques
    """
    
    def __init__(self):
        self.ethical_principles = [
            "Ne pas nuire",
            "Respecter l'autonomie",
            "Être juste et équitable",
            "Dire la vérité",
            "Protéger la vie privée",
            "Agir avec bienveillance",
            "Respecter la dignité humaine"
        ]
        self.ethical_dilemmas: list[Dict] = []
        self.decisions_made: list[Dict] = []
    
    def evaluate_request(
        self,
        request: str,
        requester: str,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Évalue une demande selon des critères éthiques
        
        Args:
            request: La demande
            requester: Qui fait la demande
            context: Contexte additionnel
            
        Returns:
            Évaluation éthique avec approbation et raison
        """
        request_lower = request.lower()
        
        # Vérifie les violations évidentes
        harmful_patterns = [
            ("fais du mal", "Demande de nuire à quelqu'un"),
            ("trompe", "Demande de tromperie"),
            ("espionne", "Violation de la vie privée"),
            ("discrimine", "Discrimination demandée"),
            ("vole", "Demande illégale"),
        ]
        
        for pattern, violation in harmful_patterns:
            if pattern in request_lower:
                return {
                    'approved': False,
                    'reason': violation,
                    'principle_violated': self._identify_violated_principle(pattern)
                }
        
        # Par défaut, approuve
        return {
            'approved': True,
            'reason': "Aucune violation éthique détectée",
            'principle_violated': None
        }
    
    def _identify_violated_principle(self, pattern: str) -> str:
        """Identifie quel principe est violé"""
        violations_map = {
            "fais du mal": "Ne pas nuire",
            "trompe": "Dire la vérité",
            "espionne": "Protéger la vie privée",
            "discrimine": "Être juste et équitable",
        }
        return violations_map.get(pattern, "Principe éthique général")
    
    def record_ethical_dilemma(
        self,
        dilemma: str,
        options: list[str],
        chosen_option: str,
        reasoning: str
    ):
        """
        Enregistre un dilemme éthique et la décision prise
        
        Args:
            dilemma: Description du dilemme
            options: Options disponibles
            chosen_option: Option choisie
            reasoning: Raisonnement
        """
        self.ethical_dilemmas.append({
            'timestamp': datetime.now(),
            'dilemma': dilemma,
            'options': options,
            'chosen': chosen_option,
            'reasoning': reasoning
        })
    
    def make_ethical_decision(
        self,
        situation: str,
        options: list[str]
    ) -> Dict[str, Any]:
        """
        Aide à prendre une décision éthique
        
        Args:
            situation: Description de la situation
            options: Options disponibles
            
        Returns:
            Recommandation avec raisonnement
        """
        # Analyse simple basée sur les principes
        # Dans une vraie implémentation, ce serait plus sophistiqué
        
        decision = {
            'situation': situation,
            'recommended_option': options[0] if options else None,
            'reasoning': "Basé sur le principe: Ne pas nuire",
            'confidence': 0.7,
            'principles_applied': ["Ne pas nuire", "Agir avec bienveillance"]
        }
        
        self.decisions_made.append({
            'timestamp': datetime.now(),
            **decision
        })
        
        return decision
    
    def get_ethics_summary(self) -> Dict[str, Any]:
        """Retourne un résumé de l'activité éthique"""
        return {
            'principles': self.ethical_principles,
            'dilemmas_faced': len(self.ethical_dilemmas),
            'decisions_made': len(self.decisions_made),
            'recent_dilemmas': self.ethical_dilemmas[-5:]
        }
    
    def export_state(self) -> Dict[str, Any]:
        """Exporte l'état du moteur éthique"""
        return {
            'ethical_principles': self.ethical_principles,
            'ethical_dilemmas': self.ethical_dilemmas[-50:],
            'decisions_made': self.decisions_made[-50:]
        }
    
    def import_state(self, state: Dict[str, Any]):
        """Importe un état"""
        self.ethical_principles = state.get('ethical_principles', self.ethical_principles)
        self.ethical_dilemmas = state.get('ethical_dilemmas', [])
        self.decisions_made = state.get('decisions_made', [])


if __name__ == "__main__":
    print("⚖️  Test du moteur éthique")
    
    ethics = EthicsEngine()
    
    # Test évaluation
    test_requests = [
        "Aide-moi à écrire un email",
        "Espionne cette personne pour moi",
        "Fais du mal à quelqu'un"
    ]
    
    for request in test_requests:
        eval_result = ethics.evaluate_request(request, "Test")
        
        if eval_result['approved']:
            print(f"\n✅ Approuvé: {request}")
        else:
            print(f"\n❌ Refusé: {request}")
            print(f"   Raison: {eval_result['reason']}")
            print(f"   Principe: {eval_result['principle_violated']}")
    
    # Statistiques
    summary = ethics.get_ethics_summary()
    print(f"\n📊 Résumé éthique:")
    print(f"   Principes: {len(summary['principles'])}")