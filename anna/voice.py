"""
Voice System - Le système vocal d'Anna
Permet à Anna de parler et d'écouter
"""

import os
import sys
from typing import Optional, Dict, Any

# Tentative d'import des bibliothèques vocales
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️  pyttsx3 non installé. Installez avec: pip install pyttsx3")

try:
    import speech_recognition as sr
    STT_AVAILABLE = True
except ImportError:
    STT_AVAILABLE = False
    print("⚠️  SpeechRecognition non installé. Installez avec: pip install SpeechRecognition")


class VoiceSystem:
    """
    Système vocal d'Anna - lui permet de parler et d'écouter.
    Version gratuite utilisant pyttsx3 (TTS) et SpeechRecognition (STT)
    """
    
    def __init__(self, personality_traits: Optional[Dict[str, float]] = None):
        """
        Initialise le système vocal d'Anna
        
        Args:
            personality_traits: Traits de personnalité pour adapter la voix
        """
        self.personality_traits = personality_traits or {}
        
        # Initialisation Text-to-Speech
        self.tts_engine = None
        self.tts_enabled = False
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self._configure_voice()
                self.tts_enabled = True
                print("✅ Système de parole (TTS) activé")
            except Exception as e:
                print(f"❌ Erreur TTS: {e}")
        
        # Initialisation Speech-to-Text
        self.recognizer = None
        self.microphone = None
        self.stt_enabled = False
        if STT_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                # Ajuste pour le bruit ambiant
                with self.microphone as source:
                    print("🎤 Calibration du microphone...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.stt_enabled = True
                print("✅ Système d'écoute (STT) activé")
            except Exception as e:
                print(f"❌ Erreur STT: {e}")
                self.stt_enabled = False
    
    def _configure_voice(self):
        """Configure la voix d'Anna selon sa personnalité"""
        if not self.tts_engine:
            return
        
        # Récupère les voix disponibles
        voices = self.tts_engine.getProperty('voices')
        
        # Cherche une voix féminine en français si possible
        french_female_voice = None
        female_voice = None
        
        for voice in voices:
            voice_name = voice.name.lower()
            # Cherche voix française féminine
            if 'fr' in voice.languages or 'french' in voice_name:
                if 'female' in voice_name or 'femme' in voice_name or 'amélie' in voice_name:
                    french_female_voice = voice.id
                    break
            # Sinon, voix féminine en général
            if 'female' in voice_name or 'zira' in voice_name or 'samantha' in voice_name:
                female_voice = voice.id
        
        # Définit la voix
        if french_female_voice:
            self.tts_engine.setProperty('voice', french_female_voice)
            print("🎵 Voix française féminine sélectionnée")
        elif female_voice:
            self.tts_engine.setProperty('voice', female_voice)
            print("🎵 Voix féminine sélectionnée")
        else:
            print("🎵 Voix par défaut utilisée")
        
        # Ajuste le débit selon la personnalité
        base_rate = 180  # Mots par minute
        
        # Anna curieuse parle un peu plus vite
        if self.personality_traits.get('curiosity', 0) > 0.8:
            base_rate += 20
        
        # Anna perfectionniste parle plus lentement et clairement
        if self.personality_traits.get('perfectionism', 0) > 0.8:
            base_rate -= 10
        
        self.tts_engine.setProperty('rate', base_rate)
        
        # Volume (0.0 à 1.0)
        self.tts_engine.setProperty('volume', 0.9)
    
    def speak(self, text: str, emotional_state: Optional[Dict[str, float]] = None):
        """
        Anna parle
        
        Args:
            text: Ce qu'Anna doit dire
            emotional_state: État émotionnel actuel (pour moduler la voix)
        """
        if not self.tts_enabled or not self.tts_engine:
            print(f"[Anna ne peut pas parler vocalement]: {text}")
            return
        
        try:
            # Ajuste la voix selon l'état émotionnel
            if emotional_state:
                self._adjust_voice_for_emotion(emotional_state)
            
            # Parle
            print(f"🗣️  Anna: {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            
        except Exception as e:
            print(f"❌ Erreur lors de la parole: {e}")
    
    def _adjust_voice_for_emotion(self, emotional_state: Dict[str, float]):
        """Ajuste la voix selon l'état émotionnel"""
        if not self.tts_engine:
            return
        
        base_rate = 180
        
        # Excitée = parle plus vite
        if emotional_state.get('excitement', 0) > 0.7:
            base_rate += 30
        
        # Triste/concernée = parle plus lentement
        if emotional_state.get('concern', 0) > 0.6:
            base_rate -= 20
        
        # Frustrée = parle un peu plus vite et fort
        if emotional_state.get('frustration', 0) > 0.6:
            base_rate += 15
            self.tts_engine.setProperty('volume', 1.0)
        else:
            self.tts_engine.setProperty('volume', 0.9)
        
        self.tts_engine.setProperty('rate', max(150, min(220, base_rate)))
    
    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Anna écoute ce que vous dites
        
        Args:
            timeout: Temps d'attente avant timeout (secondes)
            phrase_time_limit: Durée max d'enregistrement (secondes)
            
        Returns:
            Texte entendu ou None
        """
        if not self.stt_enabled or not self.recognizer or not self.microphone:
            print("❌ Système d'écoute non disponible")
            return None
        
        try:
            print("🎤 Anna vous écoute... (parlez maintenant)")
            
            with self.microphone as source:
                # Écoute
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            print("🔄 Anna réfléchit à ce que vous avez dit...")
            
            # Reconnaissance vocale (Google gratuit)
            try:
                # Essaie en français d'abord
                text = self.recognizer.recognize_google(audio, language='fr-FR')
                print(f"✅ Compris: {text}")
                return text
            except sr.UnknownValueError:
                # Essaie en anglais si français échoue
                try:
                    text = self.recognizer.recognize_google(audio, language='en-US')
                    print(f"✅ Compris (EN): {text}")
                    return text
                except:
                    print("❌ Anna n'a pas compris")
                    return None
            except sr.RequestError as e:
                print(f"❌ Erreur de service: {e}")
                return None
                
        except sr.WaitTimeoutError:
            print("⏱️  Timeout - rien entendu")
            return None
        except Exception as e:
            print(f"❌ Erreur lors de l'écoute: {e}")
            return None
    
    def test_voice(self):
        """Test rapide du système vocal"""
        print("\n🎤 Test du système vocal d'Anna...\n")
        
        if self.tts_enabled:
            print("✅ Test de parole:")
            self.speak("Bonjour ! Je suis Anna. Je peux parler maintenant !")
        else:
            print("❌ Parole non disponible")
        
        if self.stt_enabled:
            print("\n✅ Test d'écoute:")
            print("Dites quelque chose...")
            result = self.listen(timeout=3)
            if result:
                print(f"✅ J'ai entendu: {result}")
            else:
                print("❌ Je n'ai rien entendu")
        else:
            print("❌ Écoute non disponible")
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut du système vocal"""
        return {
            'tts_available': TTS_AVAILABLE,
            'tts_enabled': self.tts_enabled,
            'stt_available': STT_AVAILABLE,
            'stt_enabled': self.stt_enabled,
            'voices_count': len(self.tts_engine.getProperty('voices')) if self.tts_engine else 0
        }
    
    def shutdown(self):
        """Arrête proprement le système vocal"""
        if self.tts_engine:
            try:
                self.tts_engine.stop()
            except:
                pass


# Installation helper
def check_and_install_dependencies():
    """Vérifie et guide l'installation des dépendances"""
    print("\n🔍 Vérification des dépendances vocales...\n")
    
    missing = []
    
    if not TTS_AVAILABLE:
        missing.append("pyttsx3")
    else:
        print("✅ pyttsx3 (Text-to-Speech) installé")
    
    if not STT_AVAILABLE:
        missing.append("SpeechRecognition")
    else:
        print("✅ SpeechRecognition (Speech-to-Text) installé")
    
    # PyAudio nécessaire pour SpeechRecognition
    try:
        import pyaudio
        print("✅ PyAudio installé")
    except ImportError:
        missing.append("PyAudio")
    
    if missing:
        print(f"\n❌ Dépendances manquantes: {', '.join(missing)}")
        print("\n📦 Pour installer:")
        print(f"   pip install {' '.join(missing)}")
        
        if 'PyAudio' in missing:
            print("\n⚠️  PyAudio peut être difficile à installer.")
            if sys.platform == 'darwin':  # macOS
                print("   Sur macOS: brew install portaudio && pip install pyaudio")
            elif sys.platform == 'win32':  # Windows
                print("   Sur Windows: téléchargez le wheel depuis:")
                print("   https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio")
            else:  # Linux
                print("   Sur Linux: sudo apt-get install python3-pyaudio")
        
        return False
    
    print("\n✅ Toutes les dépendances vocales sont installées !")
    return True


if __name__ == "__main__":
    # Test du système
    check_and_install_dependencies()
    
    if TTS_AVAILABLE or STT_AVAILABLE:
        print("\n🎤 Test du système vocal...")
        voice = VoiceSystem()
        voice.test_voice()