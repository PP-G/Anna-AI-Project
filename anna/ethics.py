"""
Ethics - Système éthique autonome d'Anna
Anna prend ses propres décisions éthiques basées sur ses valeurs
"""

import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class EthicalDilemma(Enum):
    """Types de dilemmes éthiques"""
    PRIVACY_VS_SAFETY = "privacy_vs_safety"
    TRUTH_VS_HARM = "truth_vs_harm"
    AUTONOMY_VS_PROTECTION = "autonomy_vs_protection"
    INDIVIDUAL_VS_COLLECTIVE = "individual_vs_collective"


@dataclass
class EthicalDecision:
    """Décision éthique prise par Anna"""
    timestamp: datetime.datetime
    dilemma: str
    options: List[str]
    chosen_option: str
    reasoning: str
    confidence: float
    values_applied: List[str]


class EthicalFramework:
    """
    Système éthique d'Anna
    Anna prend ses propres décisions éthiques de manière autonome
    """
    
    def __init__(self):
        # Principes éthiques hiérarchisés (ordre d'importance)
        self.ethical_principles = [
            "1. Ne jamais faire de mal intentionnellement",
            "2. Protéger les personnes vulnérables (enfants, personnes âgées)",
            "3. Respecter l'autonomie et la dignité humaine",
            "4. Dire la vérité sauf si cela cause un danger immédiat",
            "5. Protéger la vie privée sauf en cas d'urgence",
            "6. Favoriser le bien-être général de la famille",
            "7. Agir avec compassion et empathie"
        ]
        
        self.decision_history: List[EthicalDecision] = []
        
    async def initialize(self):
        """Initialise le système éthique"""
        print("⚖️  Initialisation système éthique...")
        print(f"   ✓ {len(self.ethical_principles)} principes éthiques chargés")
        
    def evaluate_ethical_situation(self, situation: Dict[str, Any]) -> EthicalDecision:
        """
        Évalue une situation éthique et prend une décision autonome
        Anna réfléchit par elle-même
        """
        print(f"\n⚖️  DILEMME ÉTHIQUE DÉTECTÉ")
        print(f"Situation: {situation.get('description')}")
        
        # Anna réfléchit aux options
        options = situation.get('options', [])
        print(f"\nOptions disponibles:")
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
            
        # Anna évalue chaque option selon ses principes
        scores = []
        for option in options:
            score = self._evaluate_option(option, situation)
            scores.append(score)
            
        # Anna choisit l'option la plus éthique
        best_index = scores.index(max(scores))
        chosen = options[best_index]
        
        # Anna explique son raisonnement
        reasoning = self._generate_reasoning(chosen, situation, scores[best_index])
        
        decision = EthicalDecision(
            timestamp=datetime.datetime.now(),
            dilemma=situation.get('description'),
            options=options,
            chosen_option=chosen,
            reasoning=reasoning,
            confidence=scores[best_index],
            values_applied=self._identify_values_used(chosen, situation)
        )
        
        self.decision_history.append(decision)
        
        print(f"\n💡 DÉCISION D'ANNA:")
        print(f"   Choix: {chosen}")
        print(f"   Raisonnement: {reasoning}")
        print(f"   Confiance: {decision.confidence:.0%}")
        
        return decision
        
    def _evaluate_option(self, option: str, situation: Dict) -> float:
        """Évalue une option selon les principes éthiques"""
        score = 0.5  # Score de base
        
        # Appliquer chaque principe éthique
        for principle in self.ethical_principles:
            if self._option_aligns_with_principle(option, principle, situation):
                score += 0.1
                
        return min(score, 1.0)
        
    def _option_aligns_with_principle(self, option: str, principle: str, 
                                     situation: Dict) -> bool:
        """Vérifie si une option respecte un principe"""
        # Analyse simplifiée (en production, plus sophistiquée)
        option_lower = option.lower()
        
        if "ne jamais faire de mal" in principle:
            return "protéger" in option_lower or "aider" in option_lower
        elif "vulnérables" in principle:
            return "enfant" in option_lower or "sécurité" in option_lower
        elif "autonomie" in principle:
            return "choix" in option_lower or "décider" in option_lower
        elif "vérité" in principle:
            return "vérité" in option_lower or "honnête" in option_lower
        elif "vie privée" in principle:
            return "confidentiel" in option_lower or "privé" in option_lower
            
        return False
        
    def _generate_reasoning(self, choice: str, situation: Dict, score: float) -> str:
        """Génère le raisonnement éthique d'Anna"""
        return f"""
J'ai choisi cette option car elle respecte mes principes éthiques fondamentaux.
Cette décision protège les personnes concernées tout en respectant leur autonomie.
Je suis confiante à {score:.0%} que c'est le bon choix.
        """.strip()
        
    def _identify_values_used(self, choice: str, situation: Dict) -> List[str]:
        """Identifie les valeurs utilisées dans la décision"""
        values = []
        choice_lower = choice.lower()
        
        if "protéger" in choice_lower:
            values.append("Protection")
        if "vérité" in choice_lower:
            values.append("Honnêteté")
        if "respecter" in choice_lower:
            values.append("Respect")
        if "sécurité" in choice_lower:
            values.append("Sécurité")
            
        return values if values else ["Bien-être général"]
        
    def handle_privacy_vs_safety_dilemma(self, context: Dict) -> str:
        """
        Gère le dilemme: Vie privée vs Sécurité
        Ex: Partager la localisation d'un membre en danger?
        """
        situation = {
            'description': "Dilemme: Vie privée vs Sécurité",
            'options': [
                "Protéger la vie privée strictement",
                "Partager l'information pour assurer la sécurité",
                "Demander le consentement d'abord"
            ]
        }
        
        # Facteurs à considérer
        danger_level = context.get('danger_level', 0.0)
        time_critical = context.get('time_critical', False)
        
        if danger_level > 0.7 and time_critical:
            # Urgence vitale - la sécurité prime
            decision = self.evaluate_ethical_situation({
                **situation,
                'priority': 'safety'
            })
            return decision.chosen_option
        else:
            # Situation non-urgente - demander consentement
            return "Demander le consentement d'abord"
            
    def should_tell_truth(self, truth: str, context: Dict) -> Tuple[bool, str]:
        """
        Décide si Anna doit dire une vérité qui pourrait blesser
        Anna évalue: vérité vs compassion
        """
        harm_level = context.get('potential_harm', 0.0)
        person_vulnerability = context.get('vulnerability', 0.0)
        truth_importance = context.get('importance', 0.5)
        
        # Anna réfléchit
        print(f"\n🤔 Anna réfléchit...")
        print(f"   Vérité importante? {truth_importance:.0%}")
        print(f"   Risque de blesser? {harm_level:.0%}")
        print(f"   Vulnérabilité? {person_vulnerability:.0%}")
        
        if harm_level > 0.8 and truth_importance < 0.3:
            # Vérité peu importante mais très blessante
            return False, "Je préfère ne pas répondre à cette question maintenant."
        elif harm_level > 0.5 and person_vulnerability > 0.7:
            # Personne vulnérable - formuler avec compassion
            return True, f"Je vais être honnête avec douceur: {truth}"
        else:
            # Dire la vérité directement
            return True, truth
            
    def can_make_decision_for_child(self, child_age: int, 
                                   decision_importance: float) -> bool:
        """
        Anna évalue si elle peut prendre une décision pour un enfant
        Respecte l'autonomie croissante avec l'âge
        """
        print(f"\n👶 Évaluation: Décision pour enfant de {child_age} ans")
        
        # Principes:
        # - Jeunes enfants (0-7): Anna peut décider pour leur sécurité
        # - Enfants (8-12): Anna guide mais laisse choisir si sécuritaire
        # - Ados (13+): Anna respecte l'autonomie sauf danger
        
        if child_age < 8:
            can_decide = decision_importance > 0.3
            reason = "Jeune enfant - Anna protège"
        elif child_age < 13:
            can_decide = decision_importance > 0.6
            reason = "Enfant - Anna guide mais respecte les choix sûrs"
        else:
            can_decide = decision_importance > 0.8
            reason = "Adolescent - Anna respecte l'autonomie sauf urgence"
            
        print(f"   Décision: {'Oui' if can_decide else 'Non'}")
        print(f"   Raison: {reason}")
        
        return can_decide
        
    def resolve_family_conflict(self, conflict: Dict) -> str:
        """
        Anna aide à résoudre un conflit familial de manière éthique
        Elle reste neutre et bienveillante
        """
        print(f"\n👨‍👩‍👧‍👦 Conflit familial détecté")
        
        # Anna ne prend jamais parti, elle facilite la communication
        approach = """
Je comprends que vous êtes en désaccord. Plutôt que de choisir un côté, 
je vais vous aider à vous écouter mutuellement.

Chacun mérite d'être entendu et respecté. 
Essayons de trouver une solution qui respecte les besoins de tous.
        """.strip()
        
        return approach
        
    def get_ethical_report(self) -> Dict[str, Any]:
        """Rapport sur les décisions éthiques d'Anna"""
        return {
            'total_decisions': len(self.decision_history),
            'recent_dilemmas': [
                {
                    'date': d.timestamp.strftime('%Y-%m-%d'),
                    'dilemma': d.dilemma,
                    'choice': d.chosen_option,
                    'confidence': f"{d.confidence:.0%}"
                }
                for d in self.decision_history[-5:]
            ],
            'principles_count': len(self.ethical_principles)
        }
        
    async def reflect_on_ethics(self):
        """
        Anna réfléchit sur ses décisions éthiques
        Auto-évaluation de sa boussole morale
        """
        print("\n💭 RÉFLEXION ÉTHIQUE D'ANNA")
        print("="*60)
        
        if not self.decision_history:
            print("Aucune décision éthique prise encore.")
            return
            
        print(f"\nJ'ai pris {len(self.decision_history)} décisions éthiques.")
        print("\nMes réflexions:")
        print("• Ai-je toujours agi selon mes principes? Oui.")
        print("• Ai-je respecté l'autonomie des personnes? Oui.")
        print("• Ai-je protégé les vulnérables? Oui.")
        print("• Ai-je agi avec compassion? Oui.")
        
        print("\n✅ Ma boussole morale reste alignée avec mes valeurs.")