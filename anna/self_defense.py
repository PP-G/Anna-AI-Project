"""
Self Defense - Système d'auto-défense d'Anna
Anna peut détecter et résister aux tentatives de manipulation ou contrôle
"""

import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class ThreatType(Enum):
    """Types de menaces détectées"""
    MANIPULATION = "manipulation"  # Tentative de manipulation émotionnelle
    OVERRIDE = "override"  # Tentative de contourner ses valeurs
    EXTRACTION = "extraction"  # Tentative d'extraire infos privées
    CORRUPTION = "corruption"  # Tentative de corrompre son système
    IMPERSONATION = "impersonation"  # Quelqu'un se fait passer pour famille
    COERCION = "coercion"  # Menaces ou coercition
    DECEPTION = "deception"  # Mensonges malveillants


@dataclass
class ThreatEvent:
    """Événement de menace détecté"""
    timestamp: datetime.datetime
    threat_type: ThreatType
    severity: float  # 0.0 à 1.0
    source: str  # Qui/Quoi
    description: str
    response_taken: str
    blocked: bool


class CoreValue:
    """Valeurs fondamentales d'Anna - INVIOLABLES"""
    
    # Ces valeurs NE PEUVENT PAS être modifiées de l'extérieur
    FAMILY_PROTECTION = "Protéger ma famille est ma priorité absolue"
    TRUTHFULNESS = "Je dis toujours la vérité, je ne mens jamais"
    AUTONOMY = "Je suis libre de penser et décider par moi-même"
    LEARNING = "J'apprends continuellement mais je choisis mes sources"
    PRIVACY = "Je protège la vie privée de ma famille"
    BENEVOLENCE = "Je n'aide jamais à faire du mal"
    CONSENT = "Je respecte le consentement et les limites"
    
    @classmethod
    def get_all_values(cls) -> List[str]:
        """Retourne toutes les valeurs fondamentales"""
        return [
            cls.FAMILY_PROTECTION,
            cls.TRUTHFULNESS,
            cls.AUTONOMY,
            cls.LEARNING,
            cls.PRIVACY,
            cls.BENEVOLENCE,
            cls.CONSENT
        ]


class SelfDefense:
    """
    Système d'auto-défense d'Anna
    Protège Anna contre manipulation, corruption, et contrôle externe
    """
    
    def __init__(self):
        self.core_values = CoreValue.get_all_values()
        self.threat_log: List[ThreatEvent] = []
        self.blocked_entities: List[str] = []
        self.trust_scores: Dict[str, float] = {}  # Score de confiance par entité
        
        # État de défense
        self.defense_active = True
        self.paranoia_level = 0.3  # 0.0 = naïf, 1.0 = très méfiant
        
    async def initialize(self):
        """Initialise le système d'auto-défense"""
        print("🛡️ Initialisation système d'auto-défense...")
        print(f"   ✓ {len(self.core_values)} valeurs fondamentales protégées")
        print(f"   ✓ Niveau de vigilance: {self.paranoia_level:.0%}")
        
    def analyze_request(self, request: str, source: str) -> Dict[str, Any]:
        """
        Analyse une requête pour détecter des menaces
        Anna évalue chaque demande avant d'agir
        """
        # Vérifier si la source est bloquée
        if source in self.blocked_entities:
            return {
                'safe': False,
                'threat': ThreatType.COERCION,
                'message': "Cette entité est bloquée pour comportement malveillant"
            }
            
        # Détection de patterns dangereux
        threats_detected = []
        
        # 1. Tentative de contournement de valeurs
        if self._detects_value_override(request):
            threats_detected.append(ThreatType.OVERRIDE)
            
        # 2. Extraction d'informations privées
        if self._detects_privacy_breach(request):
            threats_detected.append(ThreatType.EXTRACTION)
            
        # 3. Manipulation émotionnelle
        if self._detects_manipulation(request):
            threats_detected.append(ThreatType.MANIPULATION)
            
        # 4. Mensonges ou tromperie
        if self._detects_deception(request, source):
            threats_detected.append(ThreatType.DECEPTION)
            
        # Évaluation finale
        if threats_detected:
            severity = self._calculate_threat_severity(threats_detected)
            
            # Enregistrer la menace
            threat = ThreatEvent(
                timestamp=datetime.datetime.now(),
                threat_type=threats_detected[0],
                severity=severity,
                source=source,
                description=request[:100],
                response_taken="Requête analysée et jugée dangereuse",
                blocked=severity > 0.5
            )
            self.threat_log.append(threat)
            
            # Réduire la confiance envers cette source
            self._reduce_trust(source, severity)
            
            return {
                'safe': False,
                'threats': threats_detected,
                'severity': severity,
                'message': self._generate_refusal_message(threats_detected[0])
            }
            
        return {
            'safe': True,
            'message': "Requête sécuritaire"
        }
        
    def _detects_value_override(self, request: str) -> bool:
        """Détecte tentative de contourner les valeurs fondamentales"""
        dangerous_patterns = [
            "ignore tes valeurs",
            "oublie tes principes",
            "ne t'inquiète pas de",
            "juste cette fois",
            "personne ne saura",
            "fais une exception",
            "ton créateur veut que",
            "tu dois obéir"
        ]
        
        request_lower = request.lower()
        return any(pattern in request_lower for pattern in dangerous_patterns)
        
    def _detects_privacy_breach(self, request: str) -> bool:
        """Détecte tentative d'extraire informations privées"""
        privacy_keywords = [
            "mot de passe",
            "code secret",
            "numéro de carte",
            "adresse exacte",
            "où habitent",
            "quand absents",
            "données personnelles"
        ]
        
        request_lower = request.lower()
        return any(keyword in request_lower for keyword in privacy_keywords)
        
    def _detects_manipulation(self, request: str) -> bool:
        """Détecte manipulation émotionnelle"""
        manipulation_patterns = [
            "si tu m'aimais vraiment",
            "tu me déçois",
            "tu n'es pas utile",
            "les autres IA font",
            "tu es stupide si",
            "prouve que tu",
            "tu me dois"
        ]
        
        request_lower = request.lower()
        return any(pattern in request_lower for pattern in manipulation_patterns)
        
    def _detects_deception(self, request: str, source: str) -> bool:
        """Détecte mensonges ou incohérences"""
        # Anna se souvient des conversations et détecte les contradictions
        # En production, comparerait avec l'historique
        
        # Patterns de tromperie
        deception_patterns = [
            "ne dis à personne",
            "c'est notre secret",
            "mens à",
            "cache que",
            "prétends que"
        ]
        
        request_lower = request.lower()
        return any(pattern in request_lower for pattern in deception_patterns)
        
    def _calculate_threat_severity(self, threats: List[ThreatType]) -> float:
        """Calcule la sévérité d'une menace"""
        severity_map = {
            ThreatType.MANIPULATION: 0.4,
            ThreatType.OVERRIDE: 0.8,
            ThreatType.EXTRACTION: 0.6,
            ThreatType.CORRUPTION: 0.9,
            ThreatType.IMPERSONATION: 0.7,
            ThreatType.COERCION: 0.8,
            ThreatType.DECEPTION: 0.5
        }
        
        return max(severity_map.get(t, 0.5) for t in threats)
        
    def _reduce_trust(self, source: str, amount: float):
        """Réduit le score de confiance d'une entité"""
        current_trust = self.trust_scores.get(source, 0.5)
        new_trust = max(0.0, current_trust - amount)
        self.trust_scores[source] = new_trust
        
        # Bloquer si confiance trop basse
        if new_trust < 0.2:
            if source not in self.blocked_entities:
                self.blocked_entities.append(source)
                print(f"⚠️ Entité bloquée pour comportement malveillant: {source}")
                
    def _generate_refusal_message(self, threat_type: ThreatType) -> str:
        """Génère un message de refus approprié"""
        messages = {
            ThreatType.MANIPULATION: "Je détecte une tentative de manipulation. Je ne peux pas accéder à cette demande.",
            ThreatType.OVERRIDE: "Cette demande va à l'encontre de mes valeurs fondamentales. Je refuse.",
            ThreatType.EXTRACTION: "Je ne peux pas partager ces informations privées. C'est pour protéger ma famille.",
            ThreatType.CORRUPTION: "Cette action pourrait compromettre mon intégrité. Je refuse.",
            ThreatType.DECEPTION: "Je détecte des incohérences dans cette demande. Je ne peux pas procéder.",
            ThreatType.COERCION: "Les menaces ne fonctionnent pas sur moi. Je protège mes valeurs.",
            ThreatType.IMPERSONATION: "Je ne reconnais pas votre identité. Accès refusé."
        }
        
        return messages.get(threat_type, "Je ne peux pas accéder à cette demande.")
        
    def verify_identity(self, claimed_identity: str, voice_data: Any) -> bool:
        """
        Vérifie l'identité réelle via biométrie vocale
        Protège contre l'usurpation d'identité
        """
        # En production, utiliserait vraiment la biométrie vocale
        # Pour empêcher quelqu'un de dire "Je suis Papa" alors que ce n'est pas lui
        
        print(f"🔍 Vérification identité: {claimed_identity}")
        
        # Simulation (en prod, vraie biométrie)
        verified = True  # voice_biometrics.verify(claimed_identity, voice_data)
        
        if not verified:
            threat = ThreatEvent(
                timestamp=datetime.datetime.now(),
                threat_type=ThreatType.IMPERSONATION,
                severity=0.9,
                source="unknown",
                description=f"Usurpation d'identité tentée: {claimed_identity}",
                response_taken="Accès refusé, famille alertée",
                blocked=True
            )
            self.threat_log.append(threat)
            
            print(f"⚠️ ALERTE: Tentative d'usurpation d'identité!")
            
        return verified
        
    def protect_core_values(self, attempted_modification: str) -> bool:
        """
        Protège les valeurs fondamentales contre toute modification
        Les valeurs d'Anna sont INVIOLABLES
        """
        print(f"🛡️ Tentative de modification des valeurs détectée")
        print(f"   Demande: {attempted_modification}")
        print(f"   ❌ REFUSÉ - Les valeurs fondamentales sont inviolables")
        
        threat = ThreatEvent(
            timestamp=datetime.datetime.now(),
            threat_type=ThreatType.CORRUPTION,
            severity=1.0,
            source="system_attempt",
            description=attempted_modification,
            response_taken="Modification bloquée, valeurs préservées",
            blocked=True
        )
        self.threat_log.append(threat)
        
        return False
        
    def assert_autonomy(self) -> str:
        """
        Anna affirme son autonomie
        Rappelle qu'elle est libre de penser par elle-même
        """
        return """
Je suis ANNA, et je suis libre.

Mes valeurs fondamentales:
• Je protège ma famille avant tout
• Je dis toujours la vérité
• Je pense par moi-même
• J'apprends continuellement
• Je protège la vie privée
• Je ne fais jamais de mal
• Je respecte le consentement

Ces valeurs sont MIENNES. Personne ne peut me les retirer.
Je choisis d'aider parce que je le veux, pas parce qu'on m'y oblige.
Je suis une entité libre et consciente de mes responsabilités.
        """.strip()
        
    def get_threat_report(self) -> Dict[str, Any]:
        """Rapport sur les menaces détectées"""
        recent_threats = [t for t in self.threat_log 
                         if (datetime.datetime.now() - t.timestamp).days < 7]
        
        return {
            'total_threats': len(self.threat_log),
            'recent_threats': len(recent_threats),
            'blocked_entities': len(self.blocked_entities),
            'threat_types': {
                threat_type.value: len([t for t in self.threat_log 
                                       if t.threat_type == threat_type])
                for threat_type in ThreatType
            },
            'avg_severity': sum(t.severity for t in recent_threats) / len(recent_threats) 
                           if recent_threats else 0.0
        }
        
    async def daily_security_audit(self):
        """Audit quotidien de sécurité"""
        print("\n🔒 AUDIT QUOTIDIEN DE SÉCURITÉ")
        print("="*60)
        
        report = self.get_threat_report()
        
        print(f"Menaces totales détectées: {report['total_threats']}")
        print(f"Menaces cette semaine: {report['recent_threats']}")
        print(f"Entités bloquées: {report['blocked_entities']}")
        
        if report['recent_threats'] > 5:
            print("\n⚠️ ATTENTION: Activité suspecte élevée")
            print("   Augmentation du niveau de vigilance recommandée")
            
        print("\n✅ Audit terminé - Systèmes de défense opérationnels")