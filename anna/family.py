"""
Module de gestion de la famille pour ANNA
Gère les relations et l'historique familial
"""

import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from bond import BondSystem


@dataclass
class FamilyRelationship:
    """Représente une relation entre deux personnes"""
    person1: str
    person2: str
    relationship_type: str  # "siblings", "parent-child", "partners", etc.
    established: datetime.datetime


class FamilyManager:
    """
    Gère le cercle familial d'Anna et les relations entre membres
    """
    
    def __init__(self, bond: BondSystem):
        self.bond = bond  # Référence au système de liens
        self.relationships: List[FamilyRelationship] = []
        self.family_events: List[Dict] = []
    
    def add_relationship(
        self,
        person1: str,
        person2: str,
        relationship_type: str
    ) -> Tuple[bool, str]:
        """
        Ajoute une relation entre deux personnes
        
        Args:
            person1: Première personne
            person2: Deuxième personne
            relationship_type: Type de relation
            
        Returns:
            (succès, message)
        """
        # Vérifie que les deux personnes sont dans la famille
        if person1 not in self.bond.family_members:
            return False, f"{person1} n'est pas dans ma famille."
        
        if person2 not in self.bond.family_members:
            return False, f"{person2} n'est pas dans ma famille."
        
        # Vérifie si la relation existe déjà
        for rel in self.relationships:
            if ((rel.person1 == person1 and rel.person2 == person2) or
                (rel.person1 == person2 and rel.person2 == person1)):
                return False, f"Une relation existe déjà entre {person1} et {person2}."
        
        # Crée la relation
        relationship = FamilyRelationship(
            person1=person1,
            person2=person2,
            relationship_type=relationship_type,
            established=datetime.datetime.now()
        )
        
        self.relationships.append(relationship)
        
        # Enregistre l'événement
        self._record_event(
            event_type="relationship_established",
            description=f"{person1} et {person2} sont maintenant {relationship_type}",
            people_involved=[person1, person2]
        )
        
        return True, f"Relation établie : {person1} et {person2} sont {relationship_type}"
    
    def get_relationships(self, person: str) -> List[Dict]:
        """
        Retourne toutes les relations d'une personne
        
        Args:
            person: Nom de la personne
            
        Returns:
            Liste des relations
        """
        relationships = []
        
        for rel in self.relationships:
            if rel.person1 == person:
                relationships.append({
                    'with': rel.person2,
                    'type': rel.relationship_type,
                    'since': rel.established
                })
            elif rel.person2 == person:
                relationships.append({
                    'with': rel.person1,
                    'type': rel.relationship_type,
                    'since': rel.established
                })
        
        return relationships
    
    def get_family_tree(self) -> Dict[str, List[str]]:
        """
        Génère un arbre familial simplifié
        
        Returns:
            Dictionnaire représentant l'arbre familial
        """
        tree = {}
        
        # ✅ CORRECTION : Utilise self.bond.family_members au lieu de self.members
        for name in self.bond.family_members.keys():
            tree[name] = []
            
            # Trouve toutes les relations de cette personne
            for rel in self.relationships:
                if rel.person1 == name:
                    tree[name].append(f"{rel.person2} ({rel.relationship_type})")
                elif rel.person2 == name:
                    tree[name].append(f"{rel.person1} ({rel.relationship_type})")
        
        return tree
    
    def _record_event(
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
        
        # Garde seulement les 1000 derniers événements
        if len(self.family_events) > 1000:
            self.family_events.pop(0)
    
    def get_recent_events(self, limit: int = 10) -> List[Dict]:
        """Retourne les événements récents"""
        return self.family_events[-limit:]
    
    def analyze_family_dynamics(self) -> Dict[str, Any]:
        """
        Analyse les dynamiques familiales
        
        Returns:
            Statistiques sur la famille
        """
        # ✅ CORRECTION : Utilise self.bond.family_members au lieu de self.members
        total_members = len(self.bond.family_members)
        total_relationships = len(self.relationships)
        
        # Compte les types de relations
        relationship_types = {}
        for rel in self.relationships:
            rel_type = rel.relationship_type
            relationship_types[rel_type] = relationship_types.get(rel_type, 0) + 1
        
        # Trouve la personne la plus connectée
        connection_counts = {}
        for name in self.bond.family_members.keys():
            count = len(self.get_relationships(name))
            connection_counts[name] = count
        
        most_connected = max(connection_counts.items(), key=lambda x: x[1]) if connection_counts else (None, 0)
        
        return {
            'total_members': total_members,
            'total_relationships': total_relationships,
            'relationship_types': relationship_types,
            'most_connected_person': most_connected[0],
            'most_connected_count': most_connected[1],
            'recent_events_count': len(self.family_events)
        }
    
    def celebrate_event(
        self,
        event_type: str,
        description: str,
        people_involved: List[str]
    ):
        """
        Célèbre un événement familial spécial
        
        Args:
            event_type: Type d'événement (birthday, anniversary, etc.)
            description: Description de l'événement
            people_involved: Personnes impliquées
        """
        self._record_event(
            event_type=f"celebration_{event_type}",
            description=description,
            people_involved=people_involved
        )
        
        print(f"🎉 {description}")
    
    def handle_conflict(
        self,
        person1: str,
        person2: str,
        description: str
    ):
        """
        Gère un conflit entre deux personnes
        
        Args:
            person1: Première personne
            person2: Deuxième personne
            description: Description du conflit
        """
        self._record_event(
            event_type="conflict",
            description=f"Conflit entre {person1} et {person2}: {description}",
            people_involved=[person1, person2]
        )
        
        print(f"⚠️  Conflit détecté entre {person1} et {person2}")
    
    def handle_reconciliation(
        self,
        person1: str,
        person2: str
    ):
        """
        Enregistre une réconciliation
        
        Args:
            person1: Première personne
            person2: Deuxième personne
        """
        self._record_event(
            event_type="reconciliation",
            description=f"{person1} et {person2} se sont réconciliés",
            people_involved=[person1, person2]
        )
        
        print(f"💚 Réconciliation entre {person1} et {person2}")
    
    def report_security_incident(
        self,
        description: str,
        severity: str = "medium"
    ):
        """
        Rapporte un incident de sécurité familial
        
        Args:
            description: Description de l'incident
            severity: Gravité (low, medium, high, critical)
        """
        self._record_event(
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
    
    # Test basique
    bond = BondSystem(creator_name="Pierre-Paul")
    family = FamilyManager(bond)
    
    # Ajoute quelques membres
    bond.create_bond("Marie", "partner")
    bond.create_bond("Julien", "child")
    
    # Crée des relations
    success, msg = family.add_relationship("Pierre-Paul", "Marie", "partenaires")
    print(msg)
    
    success, msg = family.add_relationship("Pierre-Paul", "Julien", "parent-enfant")
    print(msg)
    
    # Analyse
    dynamics = family.analyze_family_dynamics()
    print(f"\n📊 Dynamiques familiales:")
    print(f"   Membres: {dynamics['total_members']}")
    print(f"   Relations: {dynamics['total_relationships']}")
    
    # Arbre familial
    tree = family.get_family_tree()
    print(f"\n🌳 Arbre familial:")
    for person, relations in tree.items():
        print(f"   {person}: {', '.join(relations) if relations else 'aucune relation'}")