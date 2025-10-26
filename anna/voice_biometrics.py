"""
Module de biométrie vocale pour ANNA
Reconnaissance et gestion des profils vocaux de la famille
"""

import asyncio
from typing import Dict, Optional, List, Any
from datetime import datetime


class VoiceBiometrics:
    """
    Système de reconnaissance vocale et biométrie
    Permet à Anna de reconnaître les voix de sa famille
    """
    
    def __init__(self):
        self.voice_profiles: Dict[str, Dict] = {}
        self.recognition_enabled = False
        self.last_speaker: Optional[str] = None
        self.confidence_threshold = 0.75
    
    async def initialize(self):
        """Initialise le système de biométrie vocale"""
        print("🎤 Initialisation biométrie vocale...")
        
        # Pour l'instant, système en mode "simulation"
        # Dans une vraie implémentation, on initialiserait les modèles ML
        self.recognition_enabled = True
        
        print("   ✓ Système vocal prêt (enregistrements à faire)")
    
    def create_voice_profile(
        self,
        name: str,
        voice_samples: Optional[List[bytes]] = None
    ) -> bool:
        """
        Crée un profil vocal pour quelqu'un
        
        Args:
            name: Nom de la personne
            voice_samples: Échantillons vocaux (optionnel pour l'instant)
            
        Returns:
            Succès de la création
        """
        if name in self.voice_profiles:
            print(f"⚠️  Profil vocal pour {name} existe déjà")
            return False
        
        self.voice_profiles[name] = {
            'name': name,
            'created_at': datetime.now(),
            'samples_count': len(voice_samples) if voice_samples else 0,
            'last_recognized': None,
            'recognition_count': 0,
            'voice_characteristics': {}  # À remplir avec ML
        }
        
        print(f"✅ Profil vocal créé pour {name}")
        return True
    
    def add_voice_sample(
        self,
        name: str,
        sample: bytes
    ) -> bool:
        """
        Ajoute un échantillon vocal au profil
        
        Args:
            name: Nom de la personne
            sample: Échantillon audio
            
        Returns:
            Succès de l'ajout
        """
        if name not in self.voice_profiles:
            print(f"❌ Aucun profil vocal pour {name}")
            return False
        
        self.voice_profiles[name]['samples_count'] += 1
        self.voice_profiles[name]['last_updated'] = datetime.now()
        
        print(f"✅ Échantillon ajouté pour {name} ({self.voice_profiles[name]['samples_count']} total)")
        return True
    
    async def recognize_speaker(
        self,
        audio_data: bytes
    ) -> tuple[Optional[str], float]:
        """
        Reconnaît le locuteur depuis l'audio
        
        Args:
            audio_data: Données audio
            
        Returns:
            (nom_reconnu, niveau_confiance)
        """
        if not self.recognition_enabled:
            return None, 0.0
        
        # Simulation pour l'instant
        # Dans une vraie implémentation, on utiliserait un modèle ML
        
        # Si on a des profils, retourne le plus probable
        if self.voice_profiles:
            # Pour la simulation, retourne le premier profil avec confiance moyenne
            first_name = list(self.voice_profiles.keys())[0]
            confidence = 0.8
            
            self.voice_profiles[first_name]['last_recognized'] = datetime.now()
            self.voice_profiles[first_name]['recognition_count'] += 1
            self.last_speaker = first_name
            
            return first_name, confidence
        
        return None, 0.0
    
    def verify_speaker(
        self,
        audio_data: bytes,
        claimed_name: str
    ) -> tuple[bool, float]:
        """
        Vérifie si l'audio correspond à une personne spécifique
        
        Args:
            audio_data: Données audio
            claimed_name: Nom revendiqué
            
        Returns:
            (vérifié, niveau_confiance)
        """
        if claimed_name not in self.voice_profiles:
            return False, 0.0
        
        # Simulation
        # Dans une vraie implémentation, on comparerait avec le profil
        confidence = 0.85
        verified = confidence > self.confidence_threshold
        
        return verified, confidence
    
    def get_voice_profile(self, name: str) -> Optional[Dict]:
        """Retourne le profil vocal d'une personne"""
        return self.voice_profiles.get(name)
    
    def list_profiles(self) -> List[str]:
        """Liste tous les profils vocaux enregistrés"""
        return list(self.voice_profiles.keys())
    
    def remove_voice_profile(self, name: str) -> bool:
        """
        Supprime un profil vocal
        
        Args:
            name: Nom de la personne
            
        Returns:
            Succès de la suppression
        """
        if name not in self.voice_profiles:
            return False
        
        del self.voice_profiles[name]
        print(f"🗑️  Profil vocal de {name} supprimé")
        return True
    
    def get_recognition_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques de reconnaissance"""
        total_recognitions = sum(
            profile['recognition_count'] 
            for profile in self.voice_profiles.values()
        )
        
        return {
            'enabled': self.recognition_enabled,
            'profiles_count': len(self.voice_profiles),
            'total_recognitions': total_recognitions,
            'last_speaker': self.last_speaker,
            'confidence_threshold': self.confidence_threshold
        }
    
    def export_state(self) -> Dict[str, Any]:
        """Exporte l'état du système vocal"""
        return {
            'voice_profiles': {
                name: {
                    'name': profile['name'],
                    'created_at': profile['created_at'].isoformat(),
                    'samples_count': profile['samples_count'],
                    'recognition_count': profile['recognition_count']
                }
                for name, profile in self.voice_profiles.items()
            },
            'recognition_enabled': self.recognition_enabled,
            'confidence_threshold': self.confidence_threshold
        }
    
    def import_state(self, state: Dict[str, Any]):
        """Importe un état sauvegardé"""
        profiles_data = state.get('voice_profiles', {})
        
        self.voice_profiles = {}
        for name, data in profiles_data.items():
            self.voice_profiles[name] = {
                'name': data['name'],
                'created_at': datetime.fromisoformat(data['created_at']),
                'samples_count': data['samples_count'],
                'recognition_count': data.get('recognition_count', 0),
                'last_recognized': None,
                'voice_characteristics': {}
            }
        
        self.recognition_enabled = state.get('recognition_enabled', False)
        self.confidence_threshold = state.get('confidence_threshold', 0.75)


if __name__ == "__main__":
    print("🎤 Test du système de biométrie vocale")
    
    async def test():
        # Initialise
        voice = VoiceBiometrics()
        await voice.initialize()
        
        # Crée un profil
        voice.create_voice_profile("Pierre-Paul")
        
        # Simule reconnaissance
        audio_test = b"audio_data_simulation"
        recognized, confidence = await voice.recognize_speaker(audio_test)
        
        if recognized:
            print(f"\n✅ Locuteur reconnu: {recognized} (confiance: {confidence:.0%})")
        else:
            print("\n❌ Aucun locuteur reconnu")
        
        # Statistiques
        stats = voice.get_recognition_stats()
        print(f"\n📊 Statistiques:")
        print(f"   Profils: {stats['profiles_count']}")
        print(f"   Reconnaissances: {stats['total_recognitions']}")
    
    asyncio.run(test())