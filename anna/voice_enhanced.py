"""
Enhanced Voice System - Voix améliorée pour Anna
Voix plus naturelle avec support multi-langue (FR-CA, FR-FR, EN-US, EN-CA, etc.)
"""

import platform
from anna.voice import VoiceSystem
from typing import Dict, Optional, List

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False


class EnhancedVoiceSystem(VoiceSystem):
    """
    Version améliorée du système vocal d'Anna.
    Support multi-langue et meilleurs réglages pour une voix plus naturelle.
    """
    
    def __init__(self, personality_traits: Optional[Dict[str, float]] = None):
        """Initialise le système vocal amélioré avec support multi-langue"""
        
        # Langues supportées par ordre de priorité
        self.supported_languages = [
            {'code': 'fr-CA', 'name': 'Français Canadien', 'priority': 1},
            {'code': 'fr-FR', 'name': 'Français France', 'priority': 2},
            {'code': 'fr-BE', 'name': 'Français Belgique', 'priority': 3},
            {'code': 'fr-CH', 'name': 'Français Suisse', 'priority': 4},
            {'code': 'en-CA', 'name': 'Anglais Canadien', 'priority': 5},
            {'code': 'en-US', 'name': 'Anglais Américain', 'priority': 6},
            {'code': 'en-GB', 'name': 'Anglais Britannique', 'priority': 7},
            {'code': 'en-AU', 'name': 'Anglais Australien', 'priority': 8},
        ]
        
        # Langue préférée (français canadien par défaut)
        self.preferred_language = 'fr-CA'
        self.current_language = 'fr-CA'
        
        # Initialise le système de base
        super().__init__(personality_traits)
        
        print("🌍 Support multi-langue activé:")
        print("   ✅ Français: Canada, France, Belgique, Suisse")
        print("   ✅ Anglais: Canada, USA, UK, Australie")
    
    def _configure_voice(self):
        """Configure la voix d'Anna avec les meilleures options disponibles"""
        if not self.tts_engine:
            return
        
        # Récupère les voix disponibles
        voices = self.tts_engine.getProperty('voices')
        
        print("\n🎵 Recherche de la meilleure voix disponible...")
        
        # Priorités de sélection pour macOS
        if platform.system() == 'Darwin':  # macOS
            best_voice = self._select_best_macos_voice(voices)
        else:
            best_voice = self._select_best_voice_generic(voices)
        
        if best_voice:
            self.tts_engine.setProperty('voice', best_voice['id'])
            print(f"✅ Voix sélectionnée: {best_voice['name']}")
            print(f"   Langue: {best_voice['lang']}")
        else:
            print("⚠️  Voix par défaut utilisée")
        
        # Configuration avancée pour une voix plus naturelle
        self._configure_advanced_settings()
    
    def _select_best_macos_voice(self, voices) -> Optional[Dict]:
        """Sélectionne la meilleure voix sur macOS"""
        
        # Voix françaises premium sur macOS (par ordre de préférence)
        preferred_french_voices = [
            'Amélie',      # Voix premium française féminine
            'Thomas',      # Voix premium française masculine
            'Audrey',      # Voix française alternative
        ]
        
        # Voix anglaises premium (backup)
        preferred_english_voices = [
            'Samantha',    # Meilleure voix anglaise féminine
            'Alex',        # Voix anglaise naturelle
            'Victoria',    # Voix anglaise britannique
        ]
        
        voice_list = []
        
        for voice in voices:
            voice_info = {
                'id': voice.id,
                'name': voice.name,
                'lang': voice.languages[0] if voice.languages else 'unknown'
            }
            voice_list.append(voice_info)
        
        # Cherche d'abord les voix françaises premium
        for pref_name in preferred_french_voices:
            for voice_info in voice_list:
                if pref_name.lower() in voice_info['name'].lower():
                    return voice_info
        
        # Sinon, cherche une voix française quelconque
        for voice_info in voice_list:
            if 'fr' in voice_info['lang'].lower():
                return voice_info
        
        # Backup: meilleures voix anglaises
        for pref_name in preferred_english_voices:
            for voice_info in voice_list:
                if pref_name.lower() in voice_info['name'].lower():
                    return voice_info
        
        # Dernière option: première voix féminine trouvée
        for voice_info in voice_list:
            if 'female' in voice_info['name'].lower() or 'femme' in voice_info['name'].lower():
                return voice_info
        
        return voice_list[0] if voice_list else None
    
    def _select_best_voice_generic(self, voices) -> Optional[Dict]:
        """Sélection de voix pour Windows/Linux"""
        voice_list = []
        
        for voice in voices:
            voice_info = {
                'id': voice.id,
                'name': voice.name,
                'lang': voice.languages[0] if voice.languages else 'unknown'
            }
            voice_list.append(voice_info)
        
        # Cherche voix française féminine
        for voice_info in voice_list:
            if 'fr' in voice_info['lang'].lower():
                if 'female' in voice_info['name'].lower() or 'femme' in voice_info['name'].lower():
                    return voice_info
        
        # Sinon voix féminine anglaise
        for voice_info in voice_list:
            if 'female' in voice_info['name'].lower():
                return voice_info
        
        return voice_list[0] if voice_list else None
    
    def _configure_advanced_settings(self):
        """Configure les paramètres avancés pour une voix naturelle"""
        if not self.tts_engine:
            return
        
        # Débit de parole naturel basé sur la personnalité
        base_rate = 175  # Un peu plus lent que par défaut pour être plus naturel
        
        # Ajustements selon la personnalité
        if self.personality_traits.get('curiosity', 0) > 0.8:
            base_rate += 15  # Anna curieuse parle un peu plus vite
        
        if self.personality_traits.get('perfectionism', 0) > 0.8:
            base_rate -= 15  # Anna perfectionniste parle plus posément
        
        if self.personality_traits.get('playfulness', 0) > 0.7:
            base_rate += 10  # Anna enjouée parle avec plus d'énergie
        
        # Applique le débit
        self.tts_engine.setProperty('rate', base_rate)
        
        # Volume naturel (ni trop fort, ni trop faible)
        self.tts_engine.setProperty('volume', 0.85)
        
        print(f"🎚️  Débit: {base_rate} mots/min")
        print(f"🔊 Volume: 85%")
    
    def listen_multilingual(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[Dict]:
        """
        Écoute en multi-langue avec détection automatique
        
        Returns:
            Dict avec 'text', 'language', 'confidence' ou None
        """
        if not self.stt_enabled or not self.recognizer or not self.microphone:
            print("❌ Système d'écoute non disponible")
            return None
        
        try:
            print("🎤 Anna vous écoute en multi-langue... (parlez maintenant)")
            
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            print("🔄 Anna analyse la langue et le contenu...")
            
            # Essaie toutes les langues par ordre de priorité
            for lang_info in self.supported_languages:
                lang_code = lang_info['code']
                lang_name = lang_info['name']
                
                try:
                    text = self.recognizer.recognize_google(audio, language=lang_code)
                    
                    # Succès !
                    print(f"✅ Compris en {lang_name}: {text}")
                    
                    # Met à jour la langue courante
                    self.current_language = lang_code
                    
                    return {
                        'text': text,
                        'language': lang_code,
                        'language_name': lang_name,
                        'confidence': 0.9
                    }
                    
                except Exception:
                    # Cette langue n'a pas fonctionné, essaie la suivante
                    continue
            
            # Aucune langue n'a fonctionné
            print("❌ Anna n'a pas pu comprendre dans aucune langue")
            return None
            
        except Exception as e:
            print(f"❌ Erreur lors de l'écoute: {e}")
            return None
    
    def _adjust_voice_for_emotion(self, emotional_state: Dict[str, float]):
        """Ajuste la voix de manière plus subtile selon l'émotion"""
        if not self.tts_engine:
            return
        
        base_rate = 175
        base_volume = 0.85
        
        # Émotions qui accélèrent légèrement
        if emotional_state.get('excitement', 0) > 0.7:
            base_rate += 20
            base_volume = 0.9
        elif emotional_state.get('joy', 0) > 0.7:
            base_rate += 10
        
        # Émotions qui ralentissent
        if emotional_state.get('concern', 0) > 0.6:
            base_rate -= 15
            base_volume = 0.80
        elif emotional_state.get('confusion', 0) > 0.5:
            base_rate -= 10
        
        # Frustration = un peu plus rapide et fort
        if emotional_state.get('frustration', 0) > 0.6:
            base_rate += 12
            base_volume = 0.90
        
        # Curiosité = légèrement plus vif
        if emotional_state.get('curiosity', 0) > 0.7:
            base_rate += 8
        
        # Applique avec des limites raisonnables
        final_rate = max(140, min(210, base_rate))
        final_volume = max(0.7, min(1.0, base_volume))
        
        self.tts_engine.setProperty('rate', final_rate)
        self.tts_engine.setProperty('volume', final_volume)
    
    def speak_with_pause(self, text: str, emotional_state: Optional[Dict[str, float]] = None):
        """
        Parle avec des pauses naturelles pour ponctuation
        
        Args:
            text: Texte à dire
            emotional_state: État émotionnel
        """
        if not self.tts_enabled or not self.tts_engine:
            print(f"[Anna]: {text}")
            return
        
        try:
            # Ajuste la voix
            if emotional_state:
                self._adjust_voice_for_emotion(emotional_state)
            
            # Ajoute des pauses naturelles
            text_with_pauses = self._add_natural_pauses(text)
            
            print(f"🗣️  Anna: {text}")
            self.tts_engine.say(text_with_pauses)
            self.tts_engine.runAndWait()
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    def _add_natural_pauses(self, text: str) -> str:
        """Ajoute des pauses naturelles dans le texte"""
        # Remplace la ponctuation par des pauses
        text = text.replace('...', ' ... ')  # Pause longue
        text = text.replace('. ', '.  ')     # Pause après point
        text = text.replace('! ', '!  ')     # Pause après exclamation
        text = text.replace('? ', '?  ')     # Pause après question
        text = text.replace(', ', ',  ')     # Petite pause après virgule
        
        return text
    
    def get_supported_languages(self) -> List[Dict]:
        """Retourne la liste des langues supportées"""
        return self.supported_languages.copy()
    
    def set_preferred_language(self, lang_code: str):
        """
        Définit la langue préférée
        
        Args:
            lang_code: Code de langue (ex: 'fr-CA', 'en-US')
        """
        valid_codes = [lang['code'] for lang in self.supported_languages]
        
        if lang_code in valid_codes:
            self.preferred_language = lang_code
            self.current_language = lang_code
            print(f"✅ Langue préférée: {lang_code}")
        else:
            print(f"❌ Langue {lang_code} non supportée")
            print(f"   Langues disponibles: {', '.join(valid_codes)}")
    
    def list_available_voices(self):
        """Liste toutes les voix disponibles"""
        if not self.tts_engine:
            print("❌ TTS non disponible")
            return
        
        voices = self.tts_engine.getProperty('voices')
        
        print(f"\n🎤 {len(voices)} voix disponibles:\n")
        
        for i, voice in enumerate(voices, 1):
            lang = voice.languages[0] if voice.languages else 'unknown'
            print(f"{i}. {voice.name}")
            print(f"   ID: {voice.id}")
            print(f"   Langue: {lang}")
            print()


# Fonction de test
def test_enhanced_voice():
    """Test de la voix améliorée"""
    print("🎙️ Test de la Voix Améliorée Multi-langue d'Anna\n")
    
    # Créer le système
    voice = EnhancedVoiceSystem()
    
    # Afficher les langues supportées
    print("\n🌍 Langues supportées:")
    for lang in voice.get_supported_languages():
        print(f"   • {lang['name']} ({lang['code']})")
    
    # Test de parole
    if voice.tts_enabled:
        print("\n🗣️  Test de parole:\n")
        
        # Test en français
        voice.speak("Bonjour ! Je comprends le français du Canada, de France, de Belgique et de Suisse.")
        
        import time
        time.sleep(1)
        
        # Test avec émotion
        print("\n😊 Test avec excitation:")
        voice.speak(
            "C'est génial ! Je peux maintenant comprendre plein d'accents différents !",
            emotional_state={'excitement': 0.8, 'joy': 0.7}
        )


if __name__ == "__main__":
    test_enhanced_voice()