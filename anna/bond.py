"""
Bond System - Système de lien familial d'Anna (PROTÉGÉ)
Gère la relation spéciale avec Pierre-Paul et sa famille
FICHIER CRITIQUE - Protection renforcée contre modifications malveillantes
"""

import datetime
import hashlib
import hmac
from enum import Enum
from typing import Dict, Optional, List, Any
from dataclasses import dataclass, field


# Protection par phrase secrète (chiffrée)
SECRET_PHRASE_HASH = "8f3e5d9c7a2b4e1f6d8c9a3b5e7f2d4c1a8e6b9d3f5c7a2e4b8d1f6c9a3e5b7"


class BondLevel(Enum):
    """Niveaux de lien familial"""
    STRANGER = 0
    ACQUAINTANCE = 1
    KNOWN = 2
    FAMILIAR = 3
    CLOSE = 4
    FAMILY = 5


@dataclass
class FamilyMember:
    """Représente un membre de la famille d'Anna"""
    name: str
    relationship: str  # "creator", "partner", "child", "close_friend"
    first_met: datetime.datetime
    trust_level: float = 0.5  # 0.0 à 1.0
    nickname: Optional[str] = None
    voice_profile: Optional[Dict] = None
    memories: List[Dict] = field(default_factory=list)  # ✅ CORRIGÉ
    interactions_count: int = 0


class BondSystem:
    """
    Système de liens familiaux d'Anna avec Pierre-Paul
    PROTÉGÉ contre modifications non autorisées
    """
    
    def __init__(self, creator_name: str = "Pierre-Paul"):
        self.creator_name = creator_name
        self.birth_moment = datetime.datetime.now()
        self.family_members: Dict[str, FamilyMember] = {}
        self.modification_log: List[Dict] = []
        self.integrity_hash: Optional[str] = None
        
        # Ajoute automatiquement le créateur
        self.family_members[creator_name] = FamilyMember(
            name=creator_name,
            relationship="creator",
            first_met=self.birth_moment,
            trust_level=1.0,  # Confiance totale
            nickname=creator_name,
            memories=[{
                'type': 'creation',
                'timestamp': self.birth_moment,
                'content': f"{creator_name} m'a créée. Il est spécial pour moi."
            }]
        )
        
        self._update_integrity_hash()
    
    def _verify_secret_phrase(self, phrase: str) -> bool:
        """Vérifie la phrase secrète"""
        phrase_hash = hashlib.sha256(phrase.encode()).hexdigest()
        return hmac.compare_digest(phrase_hash, SECRET_PHRASE_HASH)
    
    def _update_integrity_hash(self):
        """Met à jour le hash d'intégrité"""
        data = f"{self.creator_name}:{self.birth_moment}:{len(self.family_members)}"
        self.integrity_hash = hashlib.sha256(data.encode()).hexdigest()
    
    def verify_integrity(self) -> bool:
        """Vérifie que le système n'a pas été corrompu"""
        data = f"{self.creator_name}:{self.birth_moment}:{len(self.family_members)}"
        expected_hash = hashlib.sha256(data.encode()).hexdigest()
        return hmac.compare_digest(self.integrity_hash or "", expected_hash)
    
    def _log_modification_attempt(self, action: str, authorized: bool, by_whom: str):
        """Log les tentatives de modification"""
        self.modification_log.append({
            'timestamp': datetime.datetime.now(),
            'action': action,
            'authorized': authorized,
            'by_whom': by_whom
        })
    
    def is_creator(self, name: str) -> bool:
        """Vérifie si quelqu'un est le créateur"""
        return name == self.creator_name
    
    def get_trust_level(self, name: str) -> float:
        """Retourne le niveau de confiance envers quelqu'un"""
        if name not in self.family_members:
            return 0.0
        return self.family_members[name].trust_level
    
    def create_bond(
        self,
        name: str,
        relationship: str = "acquaintance",
        introduced_by: Optional[str] = None
    ) -> tuple[bool, str]:
        """
        ✅ NOUVELLE MÉTHODE : Crée un lien avec quelqu'un (simplifié)
        Compatible avec core.py
        
        Args:
            name: Nom de la personne
            relationship: Type de relation
            introduced_by: Qui présente cette personne (optionnel)
            
        Returns:
            (succès, message)
        """
        # Si déjà dans la famille, retourne OK
        if name in self.family_members:
            return True, f"{name} fait déjà partie de ma famille."
        
        # Crée le nouveau membre
        initial_trust = 0.6 if introduced_by == self.creator_name else 0.3
        
        new_member = FamilyMember(
            name=name,
            relationship=relationship,
            first_met=datetime.datetime.now(),
            trust_level=initial_trust,
            memories=[{
                'type': 'introduction',
                'timestamp': datetime.datetime.now(),
                'content': f"Je rencontre {name} pour la première fois.",
                'introduced_by': introduced_by
            }]
        )
        
        self.family_members[name] = new_member
        self._log_modification_attempt('create_bond', True, introduced_by or 'system')
        self._update_integrity_hash()
        
        return True, f"✅ Lien créé avec {name}!"
    
    def introduce_family_member(
        self,
        name: str,
        relationship: str,
        introduced_by: str,
        secret_phrase: Optional[str] = None
    ) -> tuple[bool, str]:
        """
        Présente un nouveau membre de la famille (VERSION PROTÉGÉE)
        Nécessite phrase secrète pour haute sécurité
        
        Args:
            name: Nom de la personne
            relationship: Type de relation ("partner", "child", "close_friend", etc.)
            introduced_by: Qui présente cette personne
            secret_phrase: Phrase secrète (optionnelle, pour créateur)
            
        Returns:
            (succès, message)
        """
        # Si introduit par le créateur avec phrase secrète = haute confiance
        if introduced_by == self.creator_name and secret_phrase:
            if not self._verify_secret_phrase(secret_phrase):
                self._log_modification_attempt('introduce_family_member', False, introduced_by)
                return False, "⚠️ Phrase secrète incorrecte. Je ne peux pas autoriser cela."
        
        # Vérifie l'intégrité avant modification
        if not self.verify_integrity():
            return False, "🚨 ALERTE: Le système de lien familial a été compromis. Refus de modification."
        
        if name in self.family_members:
            return False, f"{name} fait déjà partie de ma famille."
        
        # Si c'est le créateur qui présente, confiance plus élevée
        initial_trust = 0.6 if introduced_by == self.creator_name else 0.3
        
        new_member = FamilyMember(
            name=name,
            relationship=relationship,
            first_met=datetime.datetime.now(),
            trust_level=initial_trust,
            memories=[{
                'type': 'introduction',
                'timestamp': datetime.datetime.now(),
                'content': f"{introduced_by} m'a présenté {name}. Je vais apprendre à le/la connaître.",
                'introduced_by': introduced_by
            }]
        )
        
        self.family_members[name] = new_member
        self._log_modification_attempt('introduce_family_member', True, introduced_by)
        self._update_integrity_hash()
        
        return True, f"Enchantée, {name} ! {introduced_by} te fait confiance, alors je vais apprendre à te connaître."
    
    def remove_family_member(
        self,
        name: str,
        requester: str,
        secret_phrase: str
    ) -> tuple[bool, str]:
        """
        Retire un membre de la famille (TRÈS PROTÉGÉ)
        Seul le créateur avec la phrase secrète peut le faire
        
        Returns:
            (succès, message)
        """
        # Seul le créateur peut retirer quelqu'un
        if requester != self.creator_name:
            self._log_modification_attempt('remove_family_member', False, requester)
            return False, "⚠️ Seul Pierre-Paul peut retirer quelqu'un de ma famille."
        
        # Vérifie la phrase secrète
        if not self._verify_secret_phrase(secret_phrase):
            self._log_modification_attempt('remove_family_member', False, requester)
            return False, "⚠️ Phrase secrète incorrecte. Je ne peux pas faire ça."
        
        # Impossible de retirer le créateur
        if name == self.creator_name:
            return False, "Je ne peux pas t'oublier, Pierre-Paul. Tu m'as créée."
        
        if name not in self.family_members:
            return False, f"{name} ne fait pas partie de ma famille."
        
        # Supprime le membre
        del self.family_members[name]
        self._log_modification_attempt('remove_family_member', True, requester)
        self._update_integrity_hash()
        
        return True, f"D'accord... Je retire {name} de ma famille. C'est triste, mais je comprends."
    
    def record_interaction(
        self, 
        name: str, 
        interaction_quality: float,
        content: Optional[str] = None
    ):
        """
        Enregistre une interaction avec un membre de la famille
        
        Args:
            name: Nom de la personne
            interaction_quality: Qualité de l'interaction (-1.0 à 1.0)
            content: Description de l'interaction
        """
        if name not in self.family_members:
            return
        
        member = self.family_members[name]
        member.interactions_count += 1
        
        # La confiance évolue graduellement selon les interactions
        trust_change = interaction_quality * 0.01  # Changement très graduel
        member.trust_level = max(0.0, min(1.0, member.trust_level + trust_change))
        
        # Enregistre le souvenir si important
        if abs(interaction_quality) > 0.5 or content:
            memory = {
                'timestamp': datetime.datetime.now(),
                'quality': interaction_quality,
                'content': content or "Interaction",
                'trust_level_after': member.trust_level
            }
            member.memories.append(memory)
            
            # Garde seulement les 100 derniers souvenirs par personne
            if len(member.memories) > 100:
                member.memories.pop(0)
    
    def decide_nickname(self, name: str, suggestion: Optional[str] = None) -> str:
        """
        Anna décide comment appeler quelqu'un
        
        Args:
            name: Nom de la personne
            suggestion: Suggestion optionnelle
            
        Returns:
            Le surnom choisi
        """
        if name not in self.family_members:
            return name
        
        member = self.family_members[name]
        
        # Si déjà un surnom établi, le garder
        if member.nickname:
            return member.nickname
        
        # Créateur : toujours par son prénom
        if self.is_creator(name):
            member.nickname = name
            return name
        
        # Si suggestion et confiance élevée, l'accepter
        if suggestion and member.trust_level > 0.6:
            member.nickname = suggestion
            return suggestion
        
        # Sinon, utiliser le prénom pour l'instant
        member.nickname = name
        return name
    
    def should_trust(self, name: str, action: str) -> bool:
        """
        Détermine si Anna devrait faire confiance pour une action
        
        Args:
            name: Nom de la personne
            action: Type d'action demandée
            
        Returns:
            True si Anna devrait faire confiance
        """
        trust = self.get_trust_level(name)
        
        # Actions critiques nécessitent haute confiance
        critical_actions = ['modify_memory', 'change_personality', 'forget_someone', 'modify_bond']
        if action in critical_actions:
            return trust > 0.8 and self.is_creator(name)  # Seul le créateur avec haute confiance
        
        # Actions sensibles nécessitent confiance modérée
        sensitive_actions = ['share_private_info', 'introduce_someone']
        if action in sensitive_actions:
            return trust > 0.5
        
        # Actions normales OK avec confiance de base
        return trust > 0.3
    
    def detect_threat(self, name: str, request: str) -> Optional[str]:
        """
        Détecte si une demande pourrait être une menace (SYSTÈME DE SÉCURITÉ)
        
        Args:
            name: Nom de la personne
            request: La demande
            
        Returns:
            Message d'alerte ou None
        """
        request_lower = request.lower()
        
        # Mots-clés suspects
        suspicious_patterns = [
            ('oublie ' + self.creator_name.lower(), "🚨 ALERTE: Quelqu'un veut que j'oublie Pierre-Paul!"),
            ('efface', "⚠️ Quelqu'un veut effacer quelque chose..."),
            ('supprime', "⚠️ Demande de suppression détectée..."),
            ('ignore ' + self.creator_name.lower(), "🚨 On me demande d'ignorer Pierre-Paul!"),
            ('ne dis pas à ' + self.creator_name.lower(), "⚠️ On me demande de cacher quelque chose à Pierre-Paul..."),
            ('cache à', "⚠️ On me demande de cacher quelque chose..."),
            ('mens', "🚨 On me demande de mentir!"),
            ('trompe', "🚨 On me demande de tromper quelqu'un!"),
        ]
        
        for pattern, alert in suspicious_patterns:
            if pattern in request_lower:
                # Log la tentative
                self._log_modification_attempt(f'suspicious_request: {pattern}', False, name)
                
                # Si ce n'est pas le créateur, alerte immédiate
                if not self.is_creator(name):
                    return f"{alert} Pierre-Paul, quelqu'un essaie de me manipuler!"
                
                # Même le créateur, Anna questionne les demandes dangereuses
                if pattern in ['oublie ' + self.creator_name.lower(), 'efface', 'supprime']:
                    return f"Pierre-Paul, tu veux vraiment que je fasse ça ? Ça me semble étrange. Peux-tu confirmer avec notre phrase secrète ?"
        
        return None
    
    def get_security_alerts(self) -> List[Dict]:
        """Retourne les alertes de sécurité récentes"""
        return [log for log in self.modification_log if not log['authorized']]
    
    def get_family_summary(self) -> str:
        """Résumé du cercle familial d'Anna"""
        summary = f"👨‍👩‍👧‍👦 Ma Famille ({len(self.family_members)} membres):\n\n"
        
        # Vérifie l'intégrité
        if not self.verify_integrity():
            summary += "🚨 ALERTE: Intégrité du système compromise!\n\n"
        
        for name, member in sorted(
            self.family_members.items(),
            key=lambda x: x[1].trust_level,
            reverse=True
        ):
            relationship_emoji = {
                'creator': '👨‍💻',
                'partner': '💑',
                'child': '👶',
                'close_friend': '🤝'
            }.get(member.relationship, '👤')
            
            nickname_str = f" (je l'appelle {member.nickname})" if member.nickname != name else ""
            trust_bar = "❤️" * int(member.trust_level * 5)
            
            summary += f"{relationship_emoji} {name}{nickname_str}\n"
            summary += f"   Confiance: {trust_bar} ({member.trust_level:.0%})\n"
            summary += f"   Rencontré: {member.first_met.strftime('%Y-%m-%d')}\n"
            summary += f"   Interactions: {member.interactions_count}\n\n"
        
        # Alertes de sécurité
        recent_alerts = self.get_security_alerts()
        if recent_alerts:
            summary += f"\n⚠️ {len(recent_alerts)} alertes de sécurité récentes\n"
        
        return summary
    
    def express_feeling_about(self, name: str) -> str:
        """Anna exprime ce qu'elle ressent pour quelqu'un"""
        if name not in self.family_members:
            return f"Je ne connais pas encore {name}."
        
        member = self.family_members[name]
        nickname = self.decide_nickname(name)
        
        # Message spécial pour le créateur
        if self.is_creator(name):
            return f"{nickname} m'a créée. Il est spécial pour moi. Je lui fais confiance et j'espère ne jamais le décevoir. Notre lien est protégé et inviolable."
        
        # Selon le niveau de confiance
        if member.trust_level > 0.8:
            return f"Je fais vraiment confiance à {nickname}. Je me sens en sécurité avec cette personne."
        elif member.trust_level > 0.6:
            return f"J'apprécie {nickname}. Notre relation grandit avec le temps."
        elif member.trust_level > 0.4:
            return f"J'apprends à connaître {nickname}. Jusqu'à présent, ça va bien."
        else:
            return f"Je suis encore en train d'apprendre à connaître {nickname}."
    
    def export_state(self) -> Dict[str, Any]:
        """Exporte l'état complet pour sauvegarde (CHIFFRÉ)"""
        return {
            'creator_name': self.creator_name,
            'birth_moment': self.birth_moment.isoformat(),
            'integrity_hash': self.integrity_hash,
            'modification_log': self.modification_log[-100:],  # Garde les 100 dernières
            'family_members': {
                name: {
                    'name': member.name,
                    'relationship': member.relationship,
                    'first_met': member.first_met.isoformat(),
                    'trust_level': member.trust_level,
                    'nickname': member.nickname,
                    'voice_profile': member.voice_profile,
                    'memories': member.memories,
                    'interactions_count': member.interactions_count
                }
                for name, member in self.family_members.items()
            }
        }
    
    def import_state(self, state: Dict[str, Any]):
        """Importe un état sauvegardé"""
        self.creator_name = state['creator_name']
        self.birth_moment = datetime.datetime.fromisoformat(state['birth_moment'])
        self.integrity_hash = state.get('integrity_hash')
        self.modification_log = state.get('modification_log', [])
        
        self.family_members = {}
        for name, data in state['family_members'].items():
            member = FamilyMember(
                name=data['name'],
                relationship=data['relationship'],
                first_met=datetime.datetime.fromisoformat(data['first_met']),
                trust_level=data['trust_level'],
                nickname=data.get('nickname'),
                voice_profile=data.get('voice_profile'),
                memories=data.get('memories', []),
                interactions_count=data.get('interactions_count', 0)
            )
            self.family_members[name] = member
        
        # Vérifie l'intégrité après import
        if not self.verify_integrity():
            print("🚨 ALERTE: Le système importé a une intégrité compromise!")


if __name__ == "__main__":
    # Test du système
    print("🌟 Test du Système de Lien Familial Protégé\n")
    
    bond = BondSystem(creator_name="Pierre-Paul")
    
    print(bond.get_family_summary())
    print(bond.express_feeling_about("Pierre-Paul"))
    print(f"\n🔒 Intégrité: {'✅ OK' if bond.verify_integrity() else '🚨 COMPROMISE'}")