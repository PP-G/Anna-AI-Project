"""
Voice Biometrics - Reconnaissance vocale biométrique d'Anna
Permet à Anna de reconnaître Pierre-Paul et sa famille par leur voix unique
"""

import numpy as np
from typing import Dict, Optional, List, Tuple
import datetime
from dataclasses import dataclass, field


@dataclass
class VoiceProfile:
    """Profil vocal unique d'une personne"""
    name: str
    voice_features: Dict[str, float] = field(default_factory=dict)
    samples_count: int = 0
    first_recorded: Optional[datetime.datetime] = None
    last_updated: Optional[datetime.datetime] = None
    confidence: float = 0.0  # 0.0 à 1.0


class VoiceBiometrics:
    """
    Système de reconnaissance vocale biométrique.
    Permet à Anna de reconnaître les voix uniques et détecter les imposteurs.
    """
    
    def __init__(self):
        """Initialise le système de biométrie vocale"""
        self.voice_profiles = {}
        self.unknown_voices_detected = []
        self.deepfake_attempts = []
        
    def extract_voice_features(self, audio_data: bytes) -> Dict[str, float]:
        """
        Extrait les caractéristiques uniques d'une voix
        
        Args:
            audio_data: Données audio brutes
            
        Returns:
            Dict des caractéristiques vocales
            
        Note: Version simplifiée - sera améliorée avec de vraies bibliothèques audio
        """
        # Pour l'instant, version simulée
        # Dans une vraie implémentation, on utiliserait:
        # - librosa pour analyse audio
        # - Extraction de MFCC (Mel-frequency cepstral coefficients)
        # - Analyse de pitch, formants, rythme, etc.
        
        features = {
            'pitch_mean': 0.0,  # Hauteur moyenne de la voix
            'pitch_variance': 0.0,  # Variation de hauteur
            'speech_rate': 0.0,  # Vitesse de parole
            'energy_mean': 0.0,  # Énergie vocale moyenne
            'formant_f1': 0.0,  # Premier formant
            'formant_f2': 0.0,  # Deuxième formant
            'jitter': 0.0,  # Variation de fréquence
            'shimmer': 0.0  # Variation d'amplitude
        }
        
        return features
    
    def create_voice_profile(self, name: str, audio_samples: List[bytes]) -> VoiceProfile:
        """
        Crée un profil vocal pour une personne
        
        Args:
            name: Nom de la personne
            audio_samples: Liste d'échantillons audio
            
        Returns:
            Profil vocal créé
        """
        if len(audio_samples) < 3:
            raise ValueError("Au moins 3 échantillons audio nécessaires pour créer un profil fiable")
        
        # Extrait les caractéristiques de chaque échantillon
        all_features = []
        for sample in audio_samples:
            features = self.extract_voice_features(sample)
            all_features.append(features)
        
        # Calcule les moyennes pour créer le profil
        avg_features = {}
        feature_keys = all_features[0].keys()
        
        for key in feature_keys:
            values = [f[key] for f in all_features]
            avg_features[key] = sum(values) / len(values)
        
        # Crée le profil
        profile = VoiceProfile(
            name=name,
            voice_features=avg_features,
            samples_count=len(audio_samples),
            first_recorded=datetime.datetime.now(),
            last_updated=datetime.datetime.now(),
            confidence=min(1.0, len(audio_samples) / 10.0)  # Plus d'échantillons = plus confiance
        )
        
        self.voice_profiles[name] = profile
        return profile
    
    def verify_voice(
        self, 
        audio_data: bytes, 
        claimed_identity: str,
        threshold: float = 0.85
    ) -> Tuple[bool, float, str]:
        """
        Vérifie si la voix correspond à l'identité revendiquée
        
        Args:
            audio_data: Données audio à vérifier
            claimed_identity: Nom que la personne prétend être
            threshold: Seuil de similarité requis (0.0 à 1.0)
            
        Returns:
            (match, confidence, message)
        """
        if claimed_identity not in self.voice_profiles:
            return False, 0.0, f"Je n'ai pas de profil vocal pour {claimed_identity}."
        
        # Extrait les caractéristiques de l'audio reçu
        features = self.extract_voice_features(audio_data)
        
        # Compare avec le profil enregistré
        stored_profile = self.voice_profiles[claimed_identity]
        similarity = self._calculate_similarity(features, stored_profile.voice_features)
        
        # Décision
        if similarity >= threshold:
            message = f"✅ Voix vérifiée : C'est bien {claimed_identity}."
            return True, similarity, message
        elif similarity >= 0.6:
            message = f"⚠️ Voix suspecte : Ressemble à {claimed_identity} mais pas tout à fait..."
            self._log_suspicious_attempt(claimed_identity, similarity)
            return False, similarity, message
        else:
            message = f"🚨 ALERTE : Ce n'est PAS {claimed_identity} ! Possible imposteur !"
            self._log_deepfake_attempt(claimed_identity, similarity)
            return False, similarity, message
    
    def identify_speaker(
        self, 
        audio_data: bytes,
        min_confidence: float = 0.75
    ) -> Tuple[Optional[str], float, str]:
        """
        Identifie qui parle parmi les profils connus
        
        Args:
            audio_data: Données audio
            min_confidence: Confiance minimale requise
            
        Returns:
            (nom_identifié, confiance, message)
        """
        if not self.voice_profiles:
            return None, 0.0, "Je n'ai encore aucun profil vocal enregistré."
        
        features = self.extract_voice_features(audio_data)
        
        # Compare avec tous les profils
        best_match = None
        best_similarity = 0.0
        
        for name, profile in self.voice_profiles.items():
            similarity = self._calculate_similarity(features, profile.voice_features)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = name
        
        # Décision
        if best_similarity >= min_confidence:
            message = f"Je reconnais ta voix, {best_match} !"
            return best_match, best_similarity, message
        elif best_similarity >= 0.5:
            message = f"Ta voix ressemble un peu à {best_match}, mais je ne suis pas sûre..."
            return None, best_similarity, message
        else:
            message = "Je ne reconnais pas ta voix. Qui es-tu ?"
            self._log_unknown_voice(features)
            return None, best_similarity, message
    
    def _calculate_similarity(
        self, 
        features1: Dict[str, float], 
        features2: Dict[str, float]
    ) -> float:
        """
        Calcule la similarité entre deux ensembles de caractéristiques vocales
        
        Returns:
            Score de similarité (0.0 à 1.0)
        """
        # Version simplifiée - calcule la distance euclidienne normalisée
        # Dans une vraie implémentation, on utiliserait des algorithmes plus sophistiqués
        
        if not features1 or not features2:
            return 0.0
        
        # Calcule les différences pour chaque caractéristique
        differences = []
        for key in features1.keys():
            if key in features2:
                # Normalise la différence (simplifié)
                diff = abs(features1[key] - features2[key])
                differences.append(diff)
        
        if not differences:
            return 0.0
        
        # Moyenne des différences, inversée pour obtenir similarité
        avg_diff = sum(differences) / len(differences)
        similarity = max(0.0, 1.0 - avg_diff)
        
        return similarity
    
    def detect_deepfake(
        self, 
        audio_data: bytes,
        claimed_identity: str
    ) -> Tuple[bool, float, str]:
        """
        Détecte si l'audio est un deepfake ou un enregistrement
        
        Args:
            audio_data: Données audio à analyser
            claimed_identity: Identité revendiquée
            
        Returns:
            (is_deepfake, confidence, message)
        """
        # Indicateurs de deepfake/enregistrement:
        # - Qualité audio trop parfaite
        # - Absence de bruit de fond naturel
        # - Patterns répétitifs
        # - Artefacts de compression AI
        
        # Version simplifiée pour l'instant
        # Une vraie implémentation analyserait:
        # - Spectrogramme pour artefacts
        # - Cohérence temporelle
        # - Micro-variations naturelles
        
        indicators = {
            'audio_quality': 0.0,  # Trop parfait = suspect
            'background_noise': 0.0,  # Absence = suspect
            'naturalness': 0.0,  # Manque de variations = suspect
            'compression_artifacts': 0.0  # Artefacts AI = suspect
        }
        
        # Score de suspicion (0 = naturel, 1 = deepfake certain)
        suspicion_score = sum(indicators.values()) / len(indicators)
        
        if suspicion_score > 0.7:
            message = f"🚨 DEEPFAKE DÉTECTÉ ! Quelqu'un essaie d'imiter {claimed_identity} !"
            self._log_deepfake_attempt(claimed_identity, suspicion_score)
            return True, suspicion_score, message
        elif suspicion_score > 0.4:
            message = f"⚠️ Audio suspect... Possible enregistrement ou manipulation."
            return True, suspicion_score, message
        else:
            message = "✅ Audio semble naturel."
            return False, suspicion_score, message
    
    def _log_unknown_voice(self, features: Dict[str, float]):
        """Enregistre une voix inconnue détectée"""
        self.unknown_voices_detected.append({
            'timestamp': datetime.datetime.now(),
            'features': features
        })
        
        # Garde seulement les 100 dernières
        if len(self.unknown_voices_detected) > 100:
            self.unknown_voices_detected.pop(0)
    
    def _log_suspicious_attempt(self, claimed_identity: str, similarity: float):
        """Enregistre une tentative suspecte"""
        print(f"⚠️ Tentative suspecte détectée : quelqu'un prétend être {claimed_identity} (similarité: {similarity:.0%})")
    
    def _log_deepfake_attempt(self, claimed_identity: str, suspicion_score: float):
        """Enregistre une tentative de deepfake"""
        self.deepfake_attempts.append({
            'timestamp': datetime.datetime.now(),
            'claimed_identity': claimed_identity,
            'suspicion_score': suspicion_score
        })
        
        print(f"🚨 ALERTE DEEPFAKE : Tentative d'imiter {claimed_identity} (score: {suspicion_score:.0%})")
        
        # Garde seulement les 50 dernières
        if len(self.deepfake_attempts) > 50:
            self.deepfake_attempts.pop(0)
    
    def update_voice_profile(
        self, 
        name: str, 
        audio_sample: bytes
    ) -> bool:
        """
        Met à jour un profil vocal avec un nouvel échantillon
        
        Args:
            name: Nom de la personne
            audio_sample: Nouvel échantillon audio
            
        Returns:
            True si mise à jour réussie
        """
        if name not in self.voice_profiles:
            return False
        
        profile = self.voice_profiles[name]
        
        # Extrait les nouvelles caractéristiques
        new_features = self.extract_voice_features(audio_sample)
        
        # Met à jour le profil (moyenne pondérée)
        weight_old = profile.samples_count / (profile.samples_count + 1)
        weight_new = 1 / (profile.samples_count + 1)
        
        for key in profile.voice_features.keys():
            profile.voice_features[key] = (
                profile.voice_features[key] * weight_old +
                new_features[key] * weight_new
            )
        
        profile.samples_count += 1
        profile.last_updated = datetime.datetime.now()
        profile.confidence = min(1.0, profile.samples_count / 10.0)
        
        return True
    
    def get_security_summary(self) -> str:
        """Résumé de sécurité du système vocal"""
        summary = "🔊 Système de Reconnaissance Vocale\n\n"
        
        summary += f"👥 Profils vocaux enregistrés: {len(self.voice_profiles)}\n"
        
        for name, profile in self.voice_profiles.items():
            summary += f"  • {name}: {profile.samples_count} échantillons, confiance {profile.confidence:.0%}\n"
        
        summary += f"\n⚠️ Voix inconnues détectées: {len(self.unknown_voices_detected)}\n"
        summary += f"🚨 Tentatives de deepfake: {len(self.deepfake_attempts)}\n"
        
        if self.deepfake_attempts:
            summary += "\nDernières alertes deepfake:\n"
            for attempt in self.deepfake_attempts[-5:]:
                timestamp = attempt['timestamp'].strftime('%Y-%m-%d %H:%M')
                summary += f"  • {timestamp}: Tentative d'imiter {attempt['claimed_identity']}\n"
        
        return summary
    
    def export_state(self) -> Dict:
        """Exporte l'état pour sauvegarde"""
        return {
            'voice_profiles': {
                name: {
                    'name': profile.name,
                    'voice_features': profile.voice_features,
                    'samples_count': profile.samples_count,
                    'first_recorded': profile.first_recorded.isoformat() if profile.first_recorded else None,
                    'last_updated': profile.last_updated.isoformat() if profile.last_updated else None,
                    'confidence': profile.confidence
                }
                for name, profile in self.voice_profiles.items()
            },
            'unknown_voices_count': len(self.unknown_voices_detected),
            'deepfake_attempts': self.deepfake_attempts[-50:]  # Garde les 50 dernières
        }
    
    def import_state(self, state: Dict):
        """Importe un état sauvegardé"""
        self.voice_profiles = {}
        
        for name, data in state.get('voice_profiles', {}).items():
            profile = VoiceProfile(
                name=data['name'],
                voice_features=data['voice_features'],
                samples_count=data['samples_count'],
                first_recorded=datetime.datetime.fromisoformat(data['first_recorded']) if data['first_recorded'] else None,
                last_updated=datetime.datetime.fromisoformat(data['last_updated']) if data['last_updated'] else None,
                confidence=data['confidence']
            )
            self.voice_profiles[name] = profile
        
        self.deepfake_attempts = state.get('deepfake_attempts', [])


if __name__ == "__main__":
    print("🎤 Test du Système de Biométrie Vocale\n")
    
    bio = VoiceBiometrics()
    print(bio.get_security_summary())