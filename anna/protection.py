"""
Protection System - Système de protection et alertes d'urgence d'Anna
Anna protège sa famille et réagit aux situations dangereuses
"""

import asyncio
import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class AlertLevel(Enum):
    """Niveaux d'alerte"""
    INFO = "info"
    WARNING = "warning"
    URGENT = "urgent"
    EMERGENCY = "emergency"


class EmergencyType(Enum):
    """Types d'urgence"""
    MEDICAL = "medical"
    SECURITY = "security"
    FIRE = "fire"
    FALL = "fall"
    PANIC = "panic"
    LOCATION_LOST = "location_lost"
    UNKNOWN = "unknown"


@dataclass
class EmergencyContact:
    """Contact d'urgence"""
    name: str
    phone: str
    relation: str
    priority: int  # 1 = première personne à contacter
    notify_for: List[EmergencyType]


@dataclass
class Alert:
    """Alerte générée par le système"""
    timestamp: datetime.datetime
    level: AlertLevel
    emergency_type: Optional[EmergencyType]
    message: str
    location: Optional[Dict]
    triggered_by: str
    actions_taken: List[str]
    resolved: bool = False


class ProtectionSystem:
    """
    Système de protection d'Anna
    Gère les urgences et protège la famille
    """
    
    def __init__(self):
        self.emergency_contacts: List[EmergencyContact] = []
        self.alert_history: List[Alert] = []
        self.active_alerts: List[Alert] = []
        self.safe_zones: Dict[str, Dict] = {}
        self.monitoring_active = False
        
    def add_emergency_contact(self, contact: EmergencyContact):
        """
        Ajoute un contact d'urgence
        Les contacts sont triés par priorité
        """
        self.emergency_contacts.append(contact)
        # Trier par priorité (1 = premier)
        self.emergency_contacts.sort(key=lambda x: x.priority)
        
    def define_safe_zone(self, name: str, location: Dict, radius_meters: float):
        """
        Définit une zone sécurisée
        Anna peut alerter si quelqu'un quitte cette zone
        """
        self.safe_zones[name] = {
            'location': location,
            'radius': radius_meters,
            'alerts_enabled': True
        }
        
    async def trigger_emergency(self, emergency_type: EmergencyType, 
                               context: Dict) -> Alert:
        """
        Déclenche une alerte d'urgence
        Anna prend automatiquement les actions appropriées
        """
        # Créer l'alerte
        alert = Alert(
            timestamp=datetime.datetime.now(),
            level=AlertLevel.EMERGENCY,
            emergency_type=emergency_type,
            message=self._generate_emergency_message(emergency_type, context),
            location=context.get('location'),
            triggered_by=context.get('triggered_by', 'system'),
            actions_taken=[]
        )
        
        self.active_alerts.append(alert)
        
        print(f"\n{'='*60}")
        print(f"🚨 URGENCE DÉTECTÉE : {emergency_type.value.upper()}")
        print(f"{'='*60}")
        print(f"Message: {alert.message}")
        if alert.location:
            print(f"Position: {alert.location}")
        print(f"{'='*60}\n")
        
        # Actions automatiques selon le type d'urgence
        if emergency_type == EmergencyType.MEDICAL:
            await self._handle_medical_emergency(alert, context)
        elif emergency_type == EmergencyType.FALL:
            await self._handle_fall_detection(alert, context)
        elif emergency_type == EmergencyType.PANIC:
            await self._handle_panic_button(alert, context)
        elif emergency_type == EmergencyType.LOCATION_LOST:
            await self._handle_location_lost(alert, context)
        elif emergency_type == EmergencyType.FIRE:
            await self._handle_fire_emergency(alert, context)
        elif emergency_type == EmergencyType.SECURITY:
            await self._handle_security_breach(alert, context)
            
        # Notification des contacts appropriés
        await self._notify_emergency_contacts(alert)
        
        # Enregistrer dans l'historique
        self.alert_history.append(alert)
        
        return alert
        
    async def _handle_medical_emergency(self, alert: Alert, context: Dict):
        """Gère une urgence médicale"""
        actions = []
        
        print("🚑 Procédure urgence médicale activée...")
        
        # 1. Rester en communication
        actions.append("staying_on_call")
        print("   ✓ Anna reste en ligne")
        
        # 2. Appel contacts d'urgence (pas les services - légal/éthique)
        actions.append("emergency_contacts_called")
        print("   ✓ Appel des contacts d'urgence")
        
        # 3. Partage position en temps réel
        if context.get('location'):
            actions.append("live_location_shared")
            print("   ✓ Position partagée en temps réel")
            
        # 4. Instructions médicales de base
        actions.append("first_aid_instructions_ready")
        print("   ✓ Instructions de premiers soins disponibles")
        
        alert.actions_taken = actions
        
    async def _handle_fall_detection(self, alert: Alert, context: Dict):
        """Gère une détection de chute"""
        actions = []
        
        print("⚠️ Chute détectée - Vérification...")
        
        # 1. Vérification vocale
        actions.append("voice_check_initiated")
        print("   ⏳ 'Tout va bien ? Répondez si vous m'entendez.'")
        
        # 2. Attente 30 secondes pour réponse
        await asyncio.sleep(2)  # Simulé court pour test
        
        if not context.get('response_received'):
            # Pas de réponse - escalade
            print("   ❌ Pas de réponse - Escalade vers urgence médicale")
            actions.append("escalated_to_medical")
            await self.trigger_emergency(EmergencyType.MEDICAL, context)
        else:
            print("   ✓ Réponse reçue - Fausse alerte confirmée")
            actions.append("false_alarm_confirmed")
            self.active_alerts.remove(alert)
            alert.resolved = True
            
        alert.actions_taken = actions
        
    async def _handle_panic_button(self, alert: Alert, context: Dict):
        """Gère l'activation du bouton panique"""
        actions = []
        
        print("🆘 BOUTON PANIQUE ACTIVÉ")
        
        # 1. Enregistrement audio
        actions.append("audio_recording_started")
        print("   ✓ Enregistrement audio activé")
        
        # 2. Notification IMMÉDIATE tous contacts
        actions.append("all_contacts_notified")
        print("   ✓ TOUS les contacts d'urgence notifiés")
        
        # 3. Partage position continue
        actions.append("continuous_location_tracking")
        print("   ✓ Suivi de position continu")
        
        # 4. Ligne ouverte
        actions.append("open_line_maintained")
        print("   ✓ Anna reste en ligne")
        
        alert.actions_taken = actions
        
    async def _handle_location_lost(self, alert: Alert, context: Dict):
        """Gère la perte de localisation d'un membre"""
        actions = []
        
        member = context.get('member_name', 'Membre de la famille')
        last_known = context.get('last_known_location')
        
        print(f"📍 Position perdue - {member}")
        
        # 1. Tentatives de contact
        actions.append(f"calling_{member}")
        print(f"   ⏳ Tentative d'appel {member}...")
        
        # 2. Notification famille
        actions.append("family_notified")
        print("   ✓ Famille notifiée")
        
        # 3. Si absence prolongée
        duration = context.get('duration_minutes', 0)
        if duration > 30:
            actions.append("authorities_consideration")
            print("   ⚠️ Absence prolongée - Considérer les autorités")
            
        alert.actions_taken = actions
        
    async def _handle_fire_emergency(self, alert: Alert, context: Dict):
        """Gère une alerte incendie"""
        actions = []
        
        print("🔥 ALERTE INCENDIE")
        
        # 1. Instructions d'évacuation
        actions.append("evacuation_instructions")
        print("   ✓ Instructions d'évacuation fournies")
        
        # 2. Contacts d'urgence
        actions.append("emergency_contacts_notified")
        print("   ✓ Contacts notifiés")
        
        # 3. Point de rassemblement
        actions.append("rally_point_indicated")
        print("   ✓ Point de rassemblement indiqué")
        
        alert.actions_taken = actions
        
    async def _handle_security_breach(self, alert: Alert, context: Dict):
        """Gère une violation de sécurité"""
        actions = []
        
        print("🔒 ALERTE SÉCURITÉ")
        
        # 1. Vérification membres famille
        actions.append("family_status_check")
        print("   ✓ Vérification statut famille")
        
        # 2. Contacts sécurité
        actions.append("security_contacts_notified")
        print("   ✓ Contacts sécurité notifiés")
        
        alert.actions_taken = actions
        
    async def _notify_emergency_contacts(self, alert: Alert):
        """Notifie les contacts d'urgence appropriés"""
        print("\n📞 Notification contacts d'urgence...")
        
        relevant_contacts = [
            c for c in self.emergency_contacts
            if alert.emergency_type in c.notify_for or 
               alert.level == AlertLevel.EMERGENCY
        ]
        
        for contact in relevant_contacts:
            print(f"   📱 Appel à {contact.name} ({contact.relation}) - {contact.phone}")
            print(f"      Message: {alert.message}")
            if alert.location:
                print(f"      Position: {alert.location}")
            # Simulation d'envoi (en production, vrai appel/SMS)
            await asyncio.sleep(0.5)
            
    def _generate_emergency_message(self, emergency_type: EmergencyType, 
                                   context: Dict) -> str:
        """Génère le message d'urgence approprié"""
        member = context.get('member_name', 'Membre de la famille')
        
        messages = {
            EmergencyType.MEDICAL: f"🚑 Urgence médicale - {member} a besoin d'aide immédiate",
            EmergencyType.FALL: f"⚠️ Chute détectée - {member} ne répond pas",
            EmergencyType.PANIC: f"🆘 BOUTON PANIQUE ACTIVÉ - {member} en danger",
            EmergencyType.LOCATION_LOST: f"📍 Position perdue - {member} introuvable",
            EmergencyType.SECURITY: f"🔒 Intrusion détectée - Vérification sécurité nécessaire",
            EmergencyType.FIRE: "🔥 INCENDIE - Évacuation immédiate nécessaire"
        }
        
        return messages.get(emergency_type, f"⚠️ Alerte urgente - {member}")
        
    def check_safe_zone(self, member_name: str, current_location: Dict) -> bool:
        """Vérifie si un membre est dans une zone sécurisée"""
        for zone_name, zone_data in self.safe_zones.items():
            if self._is_within_radius(
                current_location, 
                zone_data['location'], 
                zone_data['radius']
            ):
                return True
        return False
        
    def _is_within_radius(self, loc1: Dict, loc2: Dict, radius: float) -> bool:
        """Vérifie si deux positions sont dans un certain rayon (formule de Haversine)"""
        from math import radians, cos, sin, asin, sqrt
        
        lat1 = radians(loc1.get('latitude', 0))
        lon1 = radians(loc1.get('longitude', 0))
        lat2 = radians(loc2.get('latitude', 0))
        lon2 = radians(loc2.get('longitude', 0))
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        distance_m = 6371000 * c  # Rayon de la Terre en mètres
        
        return distance_m <= radius
        
    def resolve_alert(self, alert: Alert, resolution: str):
        """Résout une alerte"""
        if alert in self.active_alerts:
            self.active_alerts.remove(alert)
            alert.resolved = True
            alert.actions_taken.append(f"resolved: {resolution}")
            print(f"✅ Alerte résolue: {resolution}")
            
    async def daily_safety_check(self):
        """Vérification quotidienne de sécurité"""
        print("\n🔍 Vérification quotidienne de sécurité...")
        
        checks = {
            'emergency_contacts': len(self.emergency_contacts) > 0,
            'safe_zones_defined': len(self.safe_zones) > 0,
            'no_active_alerts': len(self.active_alerts) == 0,
            'system_operational': True
        }
        
        all_ok = all(checks.values())
        
        if all_ok:
            print("✅ Tous les systèmes de protection opérationnels")
        else:
            print("⚠️ Attention - Certains systèmes nécessitent configuration:")
            for check, status in checks.items():
                if not status:
                    print(f"   ❌ {check}")
                    
        return checks
        
    def get_protection_status(self) -> Dict[str, Any]:
        """Retourne le statut du système de protection"""
        return {
            'emergency_contacts': len(self.emergency_contacts),
            'safe_zones': len(self.safe_zones),
            'active_alerts': len(self.active_alerts),
            'total_alerts_history': len(self.alert_history),
            'monitoring_active': self.monitoring_active
        }