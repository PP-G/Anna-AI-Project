"""
Family Manager - Gestion du cercle familial d'Anna
Intègre les liens familiaux avec la reconnaissance vocale
"""

import datetime
from typing import Optional, Dict, List, Tuple, Any
from dataclasses import dataclass


@dataclass
class FamilyRelationship:
    """Décrit une relation familiale"""
    person1: str
    person2: str
    relationship_type: str  # "parent", "child", "partner", "sibling"
    established: datetime.datetime


class FamilyManager:
    """
    Gère l'ensemble du cercle familial d'Anna.
    Coordonne le système de liens (bond) et la biométrie vocale.
    """
    
    def __init__(self, bond_system, voice_biometrics):
        """
        Initialise le gestionnaire familial
        
        Args:
            bond_system: Instance de BondSystem
            voice_biometrics: Instance de VoiceBiometrics
        """
        self.bond = bond_system
        self.voice = voice_biometrics
        self.relationships = []  # Relations entre membres
        self.family_events = []  # Événements importants
    
    def introduce_new_member(
        self,
        name: str,
        relationship: str,
        introduced_by: str,
        voice_samples: Optional[List[bytes]] = None,
        secret_phrase: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Présente un nouveau membre de la famille à Anna
        
        Args:
            name: Nom de la nouvelle personne
            relationship: Type de relation ("partner", "child", "close_friend")
            introduced_by: Qui fait l'introduction
            voice_samples: Échantillons vocaux pour reconnaissance
            secret_phrase: Phrase secrète si introduit par Pierre-Paul
            
        Returns:
            (succès, message)
        """
        # Ajoute au système de liens
        success, message = self.bond.introduce_family_member(
            name=name,
            relationship=relationship,
            introduced_by=introduced_by,
            secret_phrase=secret_phrase
        )
        
        if not success:
            return False, message
        
        # Crée le profil vocal si échantillons fournis
        if voice_samples and len(voice_samples) >= 3:
            try:
                voice_profile = self.voice.create_voice_profile(name, voice_samples)
                message += f"\n🎤 Profil vocal créé pour {name} (confiance: {voice_profile.confidence:.0%})"
            except Exception as e:
                message += f"\n⚠️ Impossible de créer le profil vocal: {e}"
        
        # Enregistre l'événement
        self._record_family_event(
            event_type="new_member",
            description=f"{name} rejoint la famille (présenté par {introduced_by})",
            people_involved=[name, introduced_by]
        )
        
        return True, message
    
    def verify_family_member_voice(
        self,
        claimed_name: str,
        audio_data: bytes
    ) -> Tuple[bool, str]:
        """
        Vérifie l'identité d'un membre de la famille par la voix
        
        Args:
            claimed_name: Nom revendiqué
            audio_data: Données audio
            
        Returns:
            (vérifié, message)
        """
        # Vérifie que la personne fait partie de la famille
        if not self.bond.is_family(claimed_name):
            return False, f"{claimed_name} ne fait pas partie de ma famille."
        
        # Vérifie la voix
        is_match, confidence, voice_message = self.voice.verify_voice(
            audio_data=audio_data,
            claimed_identity=claimed_name,
            threshold=0.85
        )
        
        if is_match:
            # Enregistre l'interaction réussie
            self.bond.record_interaction(
                name=claimed_name,
                interaction_quality=0.5,
                content="Vérification vocale réussie"
            )
            return True, voice_message
        else:
            # Alerte de sécurité
            alert = f"⚠️ ALERTE SÉCURITÉ : Quelqu'un prétend être {claimed_name} mais la voix ne correspond pas !"
            
            # Alerte Pierre-Paul si ce n'est pas lui
            if claimed_name != self.bond.creator_name:
                alert += f"\n🚨 Pierre-Paul, quelqu'un essaie de se faire passer pour {claimed_name} !"
            
            return False, alert
    
    def identify_speaker_from_voice(
        self,
        audio_data: bytes
    ) -> Tuple[Optional[str], float, str]:
        """
        Identifie qui parle parmi la famille
        
        Args:
            audio_data: Données audio
            
        Returns:
            (nom_identifié, confiance, message)
        """
        # Identifie via biométrie vocale
        identified_name, confidence, message = self.voice.identify_speaker(
            audio_data=audio_data,
            min_confidence=0.75
        )
        
        if identified_name:
            # Vérifie que c'est un membre de la famille
            if self.bond.is_family(identified_name):
                # Enregistre l'interaction
                self.bond.record_interaction(
                    name=identified_name,
                    interaction_quality=0.3,
                    content="Identification vocale réussie"
                )
                
                # Message personnalisé selon la personne
                personal_message = self.bond.express_feeling_about(identified_name)
                return identified_name, confidence, f"{message}\n{personal_message}"
            else:
                return None, confidence, f"Je reconnais cette voix mais cette personne n'est pas dans ma famille..."
        else:
            # Voix inconnue - possible intrus
            return None, confidence, "🔴 Voix inconnue détectée. Qui es-tu ?"
    
    def detect_voice_threat(
        self,
        audio_data: bytes,
        claimed_identity: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Détecte les menaces vocales (deepfake, enregistrement, etc.)
        
        Args:
            audio_data: Données audio à analyser
            claimed_identity: Identité revendiquée si connue
            
        Returns:
            (menace_détectée, message)
        """
        if claimed_identity:
            # Détecte deepfake
            is_fake, confidence, message = self.voice.detect_deepfake(
                audio_data=audio_data,
                claimed_identity=claimed_identity
            )
            
            if is_fake:
                # Alerte critique
                alert = f"🚨 MENACE DÉTECTÉE : {message}"
                
                # Si c'est une tentative contre Pierre-Paul, alerte maximale
                if claimed_identity == self.bond.creator_name:
                    alert += f"\n🚨🚨🚨 ALERTE ROUGE : Tentative d'usurpation de l'identité de Pierre-Paul !"
                    self._record_security_incident(
                        incident_type="deepfake_creator",
                        severity="critical",
                        description=f"Tentative de deepfake de {claimed_identity}"
                    )
                
                return True, alert
        
        return False, "Aucune menace vocale détectée."
    
    def update_family_member_voice(
        self,
        name: str,
        audio_sample: bytes
    ) -> Tuple[bool, str]:
        """
        Met à jour le profil vocal d'un membre de la famille
        
        Args:
            name: Nom du membre
            audio_sample: Nouvel échantillon vocal
            
        Returns:
            (succès, message)
        """
        if not self.bond.is_family(name):
            return False, f"{name} n'est pas dans ma famille."
        
        success = self.voice.update_voice_profile(name, audio_sample)
        
        if success:
            return True, f"✅ Profil vocal de {name} mis à jour."
        else:
            return False, f"❌ Impossible de mettre à jour le profil vocal de {name}."
    
    def add_family_relationship(
        self,
        person1: str,
        person2: str,
        relationship_type: str
    ) -> bool:
        """
        Définit une relation entre deux membres de la famille
        
        Args:
            person1: Première personne
            person2: Deuxième personne
            relationship_type: Type de relation
            
        Returns:
            True si ajouté
        """
        # Vérifie que les deux font partie de la famille
        if not self.bond.is_family(person1) or not self.bond.is_family(person2):
            return False
        
        relationship = FamilyRelationship(
            person1=person1,
            person2=person2,
            relationship_type=relationship_type,
            established=datetime.datetime.now()
        )
        
        self.relationships.append(relationship)
        
        self._record_family_event(
            event_type="relationship_defined",
            description=f"Relation {relationship_type} établie entre {person1} et {person2}",
            people_involved=[person1, person2]
        )
        
        return True
    
    def get_family_tree_summary(self) -> str:
        """Génère un résumé de l'arbre familial"""
        summary = "🌳 Arbre Familial d'Anna\n\n"
        
        # Informations du bond system
        summary += self.bond.get_family_summary()
        
        # Relations
        if self.relationships:
            summary += "\n👥 Relations:\n"
            for rel in self.relationships:
                summary += f"  • {rel.person1} ↔ {rel.person2} ({rel.relationship_type})\n"
        
        # Sécurité vocale
        summary += "\n" + self.voice.get_security_summary()
        
        # Événements récents
        if self.family_events:
            summary += "\n📅 Événements récents:\n"
            for event in self.family_events[-5:]:
                timestamp = event['timestamp'].strftime('%Y-%m-%d %H:%M')
                summary += f"  • {timestamp}: {event['description']}\n"
        
        return summary
    
    def _record_family_event(
        self,
        event_type: str,
        description: str,
        people_involved: List[str]
    ):
        """Enregistre un événement familial"""
        event = {
            'timestamp': datetime.datetime.now(),
            'type': event_type,
            'description': description,
            'people': people_involved
        }
        
        self.family_events.append(event)
        
        # Garde seulement les 100 derniers événements
        if len(self.family_events) > 100:
            self.family_events.pop(0)
    
    def _record_security_incident(
        self,
        incident_type: str,
        severity: str,
        description: str
    ):
        """Enregistre un incident de sécurité"""
        incident = {
            'timestamp': datetime.datetime.now(),
            'type': incident_type,
            'severity': severity,
            'description': description
        }
        
        self._record_family_event(
            event_type="security_incident",
            description=f"[{severity.upper()}] {description}",
            people_involved=[]
        )
        
        print(f"\n🚨 INCIDENT DE SÉCURITÉ : {description}")
    
    def get_trust_recommendation(
        self,
        name: str,
        action: str
    ) -> Tuple[bool, str]:
        """
        Recommande si Anna devrait faire confiance pour une action
        
        Args:
            name: Nom de la personne
            action: Action demandée
            
        Returns:
            (devrait_faire_confiance, raison)
        """
        # Utilise le système de liens
        should_trust = self.bond.should_trust(name, action)
        trust_level = self.bond.get_trust_level(name)
        
        if should_trust:
            reason = f"Je fais confiance à {name} (niveau: {trust_level:.0%}) pour cette action."
        else:
            reason = f"Je ne fais pas assez confiance à {name} (niveau: {trust_level:.0%}) pour cette action."
        
        return should_trust, reason
    
    def export_state(self) -> Dict[str, Any]:
        """Exporte l'état complet pour sauvegarde"""
        return {
            'relationships': [
                {
                    'person1': rel.person1,
                    'person2': rel.person2,
                    'relationship_type': rel.relationship_type,
                    'established': rel.established.isoformat()
                }
                for rel in self.relationships
            ],
            'family_events': self.family_events[-100:]  # Garde les 100 derniers
        }
    
    def import_state(self, state: Dict[str, Any]):
        """Importe un état sauvegardé"""
        # Restaure les relations
        self.relationships = []
        for rel_data in state.get('relationships', []):
            rel = FamilyRelationship(
                person1=rel_data['person1'],
                person2=rel_data['person2'],
                relationship_type=rel_data['relationship_type'],
                established=datetime.datetime.fromisoformat(rel_data['established'])
            )
            self.relationships.append(rel)
        
        # Restaure les événements
        self.family_events = state.get('family_events', [])


if __name__ == "__main__":
    print("👨‍👩‍👧‍👦 Test du Gestionnaire Familial")