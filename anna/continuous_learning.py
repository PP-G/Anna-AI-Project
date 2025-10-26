"""
Continuous Learning - Système d'apprentissage continu d'Anna
Anna apprend automatiquement de CHAQUE conversation et s'améliore en continu
"""

import asyncio
import re
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional, Any, Tuple
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
import json


class LearningType(Enum):
    """Types d'apprentissage"""
    NEW_WORD = "new_word"
    NEW_CONCEPT = "new_concept"
    PREFERENCE = "preference"
    CORRECTION = "correction"
    EXPRESSION = "expression"
    PATTERN = "pattern"


@dataclass
class LearningItem:
    """Un élément appris"""
    learning_type: LearningType
    content: str
    context: str
    language: str  # 'fr' ou 'en'
    confidence: float
    source: str  # qui a enseigné cela
    timestamp: datetime
    usage_count: int = 0
    last_used: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class ContinuousLearningSystem:
    """
    Système d'apprentissage continu pour Anna
    Apprend automatiquement de chaque conversation
    """
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.vocabulary_path = data_dir / "vocabulary.json"
        self.concepts_path = data_dir / "concepts.json"
        self.preferences_path = data_dir / "preferences.json"
        
        # Vocabulaire en croissance
        self.vocabulary_fr: Set[str] = set()
        self.vocabulary_en: Set[str] = set()
        
        # Concepts appris
        self.concepts: Dict[str, LearningItem] = {}
        
        # Préférences utilisateur
        self.user_preferences: Dict[str, List[LearningItem]] = {}
        
        # Patterns de communication
        self.communication_patterns: Dict[str, int] = {}
        
        # Statistiques d'apprentissage
        self.stats = {
            'total_words_learned': 0,
            'total_concepts_learned': 0,
            'total_preferences_learned': 0,
            'total_corrections_received': 0,
            'last_learning_session': None,
            'conversations_analyzed': 0
        }
        
        # Configuration
        self.config = {
            'min_word_length': 3,
            'max_word_length': 50,
            'confidence_threshold': 0.5,
            'auto_save_interval': 10,  # Sauvegarde tous les 10 apprentissages
            'background_learning_enabled': True
        }
        
        # Mots à ignorer (stopwords)
        self.french_stopwords = {
            'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du',
            'et', 'ou', 'mais', 'donc', 'or', 'ni', 'car',
            'je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils', 'elles',
            'ce', 'cet', 'cette', 'ces',
            'mon', 'ton', 'son', 'ma', 'ta', 'sa', 'mes', 'tes', 'ses',
            'à', 'au', 'aux', 'en', 'par', 'pour', 'sur', 'dans', 'avec'
        }
        
        self.english_stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'if', 'then',
            'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'this', 'that', 'these', 'those',
            'my', 'your', 'his', 'her', 'its', 'our', 'their',
            'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from'
        }
    
    async def initialize(self):
        """Initialise le système d'apprentissage"""
        print("🧠 Initialisation système d'apprentissage continu...")
        
        # Charge les données existantes
        await self._load_vocabulary()
        await self._load_concepts()
        await self._load_preferences()
        
        print(f"   ✓ Vocabulaire FR: {len(self.vocabulary_fr)} mots")
        print(f"   ✓ Vocabulaire EN: {len(self.vocabulary_en)} mots")
        print(f"   ✓ Concepts appris: {len(self.concepts)}")
        print(f"   ✓ Préférences: {sum(len(prefs) for prefs in self.user_preferences.values())}")
    
    async def analyze_conversation(
        self,
        user_message: str,
        anna_response: str,
        speaker: str,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Analyse une conversation et en extrait des apprentissages
        
        Returns:
            Résumé des apprentissages effectués
        """
        self.stats['conversations_analyzed'] += 1
        
        learnings = {
            'new_words_fr': [],
            'new_words_en': [],
            'new_concepts': [],
            'preferences': [],
            'corrections': [],
            'patterns': []
        }
        
        # 1. Analyse du message utilisateur
        user_learnings = await self._analyze_message(
            user_message,
            speaker,
            context
        )
        
        # 2. Détecte les corrections dans le message utilisateur
        corrections = self._detect_corrections(user_message, anna_response)
        if corrections:
            learnings['corrections'].extend(corrections)
            self.stats['total_corrections_received'] += len(corrections)
        
        # 3. Détecte les préférences
        preferences = self._detect_preferences(user_message, speaker)
        if preferences:
            learnings['preferences'].extend(preferences)
            self.stats['total_preferences_learned'] += len(preferences)
        
        # 4. Extrait nouveaux mots et concepts
        new_words_fr, new_words_en = await self._extract_new_words(user_message)
        learnings['new_words_fr'] = new_words_fr
        learnings['new_words_en'] = new_words_en
        
        new_concepts = await self._extract_concepts(user_message, context)
        learnings['new_concepts'] = new_concepts
        
        # 5. Analyse les patterns de communication
        patterns = self._analyze_communication_patterns(user_message, speaker)
        learnings['patterns'] = patterns
        
        # 6. Met à jour les statistiques
        self.stats['total_words_learned'] += len(new_words_fr) + len(new_words_en)
        self.stats['total_concepts_learned'] += len(new_concepts)
        
        # 7. Sauvegarde automatique si nécessaire
        if self.stats['conversations_analyzed'] % self.config['auto_save_interval'] == 0:
            await self.save_all()
        
        return learnings
    
    async def _analyze_message(
        self,
        message: str,
        speaker: str,
        context: Optional[Dict]
    ) -> Dict[str, Any]:
        """Analyse en profondeur un message"""
        analysis = {
            'language': self._detect_language(message),
            'sentiment': self._analyze_sentiment(message),
            'complexity': self._analyze_complexity(message),
            'topics': self._extract_topics(message)
        }
        
        return analysis
    
    async def _extract_new_words(
        self,
        text: str
    ) -> Tuple[List[str], List[str]]:
        """
        Extrait les nouveaux mots du texte
        
        Returns:
            (nouveaux_mots_fr, nouveaux_mots_en)
        """
        new_words_fr = []
        new_words_en = []
        
        # Nettoie et tokenise le texte
        words = self._tokenize(text)
        
        for word in words:
            # Ignore si trop court ou trop long
            if len(word) < self.config['min_word_length'] or len(word) > self.config['max_word_length']:
                continue
            
            # Détecte la langue du mot
            language = self._detect_word_language(word)
            
            if language == 'fr':
                # Vérifie si c'est un nouveau mot français
                if word not in self.vocabulary_fr and word not in self.french_stopwords:
                    if self._is_valid_word(word, 'fr'):
                        self.vocabulary_fr.add(word)
                        new_words_fr.append(word)
            
            elif language == 'en':
                # Vérifie si c'est un nouveau mot anglais
                if word not in self.vocabulary_en and word not in self.english_stopwords:
                    if self._is_valid_word(word, 'en'):
                        self.vocabulary_en.add(word)
                        new_words_en.append(word)
        
        return new_words_fr, new_words_en
    
    async def _extract_concepts(
        self,
        text: str,
        context: Optional[Dict]
    ) -> List[str]:
        """Extrait les concepts importants d'un texte"""
        concepts = []
        
        # Patterns pour détecter des définitions/explications
        definition_patterns = [
            r'(.+) est (.+)',
            r'(.+) signifie (.+)',
            r'(.+) veut dire (.+)',
            r'(.+) is (.+)',
            r'(.+) means (.+)',
        ]
        
        for pattern in definition_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                concept = match.group(1).strip()
                definition = match.group(2).strip()
                
                # Stocke le concept
                if concept and definition and len(concept) < 50:
                    learning_item = LearningItem(
                        learning_type=LearningType.NEW_CONCEPT,
                        content=concept,
                        context=definition,
                        language=self._detect_language(text),
                        confidence=0.8,
                        source=text,
                        timestamp=datetime.now()
                    )
                    
                    self.concepts[concept.lower()] = learning_item
                    concepts.append(concept)
        
        return concepts
    
    def _detect_corrections(
        self,
        user_message: str,
        anna_previous_response: str
    ) -> List[Dict[str, str]]:
        """Détecte si l'utilisateur corrige Anna"""
        corrections = []
        
        # Patterns de correction
        correction_patterns = [
            r'non, (?:c\'est|plutôt) (.+)',
            r'en fait, (.+)',
            r'actually, (.+)',
            r'no, (?:it\'s|rather) (.+)',
            r'tu veux dire (.+)',
            r'you mean (.+)'
        ]
        
        for pattern in correction_patterns:
            matches = re.finditer(pattern, user_message, re.IGNORECASE)
            for match in matches:
                correction = match.group(1).strip()
                corrections.append({
                    'type': 'correction',
                    'correction': correction,
                    'original_context': anna_previous_response
                })
        
        return corrections
    
    def _detect_preferences(
        self,
        message: str,
        speaker: str
    ) -> List[LearningItem]:
        """Détecte les préférences exprimées"""
        preferences = []
        
        # Patterns de préférences
        preference_patterns = [
            (r'j\'aime (.+)', 'positive', 'fr'),
            (r'je préfère (.+)', 'positive', 'fr'),
            (r'je déteste (.+)', 'negative', 'fr'),
            (r"je n'aime pas (.+)", 'negative', 'fr'),
            (r'i like (.+)', 'positive', 'en'),
            (r'i prefer (.+)', 'positive', 'en'),
            (r'i hate (.+)', 'negative', 'en'),
            (r"i don't like (.+)", 'negative', 'en'),
        ]
        
        for pattern, sentiment, language in preference_patterns:
            matches = re.finditer(pattern, message, re.IGNORECASE)
            for match in matches:
                preference = match.group(1).strip()
                
                learning_item = LearningItem(
                    learning_type=LearningType.PREFERENCE,
                    content=preference,
                    context=message,
                    language=language,
                    confidence=0.9,
                    source=speaker,
                    timestamp=datetime.now(),
                    metadata={'sentiment': sentiment}
                )
                
                if speaker not in self.user_preferences:
                    self.user_preferences[speaker] = []
                
                self.user_preferences[speaker].append(learning_item)
                preferences.append(learning_item)
        
        return preferences
    
    def _analyze_communication_patterns(
        self,
        message: str,
        speaker: str
    ) -> List[Dict[str, Any]]:
        """Analyse les patterns de communication de l'utilisateur"""
        patterns = []
        
        # Longueur moyenne des messages
        message_length = len(message.split())
        pattern_key = f"{speaker}_avg_message_length"
        
        if pattern_key not in self.communication_patterns:
            self.communication_patterns[pattern_key] = message_length
        else:
            # Moyenne mobile
            current_avg = self.communication_patterns[pattern_key]
            self.communication_patterns[pattern_key] = (current_avg * 0.9) + (message_length * 0.1)
        
        patterns.append({
            'type': 'message_length',
            'value': message_length,
            'average': self.communication_patterns[pattern_key]
        })
        
        # Détecte le ton (questions, exclamations, etc.)
        if '?' in message:
            patterns.append({'type': 'question', 'detected': True})
        
        if '!' in message:
            patterns.append({'type': 'exclamation', 'detected': True})
        
        return patterns
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenise un texte en mots"""
        # Nettoie le texte
        text = text.lower()
        text = re.sub(r'[^\w\s\-\'àâäéèêëïîôùûüÿæœç]', ' ', text)
        
        # Split en mots
        words = text.split()
        
        # Nettoie chaque mot
        cleaned_words = []
        for word in words:
            word = word.strip('-\'')
            if word:
                cleaned_words.append(word)
        
        return cleaned_words
    
    def _detect_language(self, text: str) -> str:
        """Détecte la langue d'un texte"""
        # Heuristique simple basée sur des mots communs
        french_indicators = ['le', 'la', 'les', 'de', 'des', 'est', 'sont', 'être']
        english_indicators = ['the', 'is', 'are', 'be', 'have', 'has']
        
        text_lower = text.lower()
        
        french_count = sum(1 for word in french_indicators if word in text_lower)
        english_count = sum(1 for word in english_indicators if word in text_lower)
        
        if french_count > english_count:
            return 'fr'
        elif english_count > french_count:
            return 'en'
        else:
            return 'fr'  # Défaut français
    
    def _detect_word_language(self, word: str) -> str:
        """Détecte la langue d'un mot individuel"""
        # Caractères français
        french_chars = 'àâäéèêëïîôùûüÿæœç'
        
        if any(char in word for char in french_chars):
            return 'fr'
        
        # Si le mot est dans le vocabulaire existant
        if word in self.vocabulary_fr:
            return 'fr'
        if word in self.vocabulary_en:
            return 'en'
        
        # Heuristique: mots courts en majuscule = probablement anglais
        if word.isupper() and len(word) <= 4:
            return 'en'
        
        # Défaut: utilise la détection de langue du contexte
        return 'fr'
    
    def _is_valid_word(self, word: str, language: str) -> bool:
        """Vérifie si un mot est valide"""
        # Pas seulement des chiffres
        if word.isdigit():
            return False
        
        # Pas trop de caractères répétés
        if len(set(word)) < len(word) / 3:
            return False
        
        # Au moins une voyelle
        vowels = 'aeiouàâäéèêëïîôùûüÿ' if language == 'fr' else 'aeiou'
        if not any(char in vowels for char in word):
            return False
        
        return True
    
    def _analyze_sentiment(self, text: str) -> str:
        """Analyse basique du sentiment"""
        positive_words = {
            'bien', 'bon', 'super', 'génial', 'excellent', 'merci', 'content', 'heureux',
            'good', 'great', 'excellent', 'thanks', 'happy', 'wonderful'
        }
        
        negative_words = {
            'mal', 'mauvais', 'problème', 'erreur', 'triste', 'fâché',
            'bad', 'problem', 'error', 'sad', 'angry', 'terrible'
        }
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _analyze_complexity(self, text: str) -> str:
        """Analyse la complexité du texte"""
        words = text.split()
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        
        if avg_word_length < 4:
            return 'simple'
        elif avg_word_length < 6:
            return 'medium'
        else:
            return 'complex'
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extrait les topics principaux"""
        # Très simplifié pour l'instant
        # TODO: Améliorer avec NLP
        
        topic_keywords = {
            'technologie': ['ordinateur', 'code', 'programme', 'logiciel', 'computer', 'software'],
            'famille': ['famille', 'papa', 'maman', 'frère', 'sœur', 'family', 'parent'],
            'travail': ['travail', 'emploi', 'job', 'career', 'projet', 'project'],
            'émotion': ['content', 'triste', 'fâché', 'heureux', 'happy', 'sad', 'angry'],
        }
        
        detected_topics = []
        text_lower = text.lower()
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_topics.append(topic)
        
        return detected_topics
    
    async def background_learning_session(self):
        """
        Session d'apprentissage en arrière-plan
        Anna apprend de sources externes pendant son temps libre
        """
        print("\n🌙 Session d'apprentissage en arrière-plan...")
        
        # TODO: Implémenter l'apprentissage de sources externes
        # - Lire des articles approuvés
        # - Analyser des livres
        # - Apprendre de nouvelles expressions
        
        self.stats['last_learning_session'] = datetime.now()
        
        print("   ✓ Session d'apprentissage terminée")
    
    async def save_all(self):
        """Sauvegarde toutes les données d'apprentissage"""
        await self._save_vocabulary()
        await self._save_concepts()
        await self._save_preferences()
        
    async def _load_vocabulary(self):
        """Charge le vocabulaire"""
        if self.vocabulary_path.exists():
            with open(self.vocabulary_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.vocabulary_fr = set(data.get('fr', []))
                self.vocabulary_en = set(data.get('en', []))
    
    async def _save_vocabulary(self):
        """Sauvegarde le vocabulaire"""
        data = {
            'fr': list(self.vocabulary_fr),
            'en': list(self.vocabulary_en),
            'last_updated': datetime.now().isoformat()
        }
        
        self.vocabulary_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.vocabulary_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    async def _load_concepts(self):
        """Charge les concepts"""
        if self.concepts_path.exists():
            with open(self.concepts_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Reconstruit les LearningItem
                for key, item_data in data.items():
                    self.concepts[key] = LearningItem(
                        learning_type=LearningType(item_data['learning_type']),
                        content=item_data['content'],
                        context=item_data['context'],
                        language=item_data['language'],
                        confidence=item_data['confidence'],
                        source=item_data['source'],
                        timestamp=datetime.fromisoformat(item_data['timestamp']),
                        usage_count=item_data.get('usage_count', 0),
                        last_used=datetime.fromisoformat(item_data['last_used']) if item_data.get('last_used') else None,
                        metadata=item_data.get('metadata', {})
                    )
    
    async def _save_concepts(self):
        """Sauvegarde les concepts"""
        data = {}
        for key, item in self.concepts.items():
            data[key] = {
                'learning_type': item.learning_type.value,
                'content': item.content,
                'context': item.context,
                'language': item.language,
                'confidence': item.confidence,
                'source': item.source,
                'timestamp': item.timestamp.isoformat(),
                'usage_count': item.usage_count,
                'last_used': item.last_used.isoformat() if item.last_used else None,
                'metadata': item.metadata
            }
        
        self.concepts_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.concepts_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    async def _load_preferences(self):
        """Charge les préférences"""
        if self.preferences_path.exists():
            with open(self.preferences_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for speaker, prefs_data in data.items():
                    self.user_preferences[speaker] = []
                    for pref_data in prefs_data:
                        self.user_preferences[speaker].append(LearningItem(
                            learning_type=LearningType(pref_data['learning_type']),
                            content=pref_data['content'],
                            context=pref_data['context'],
                            language=pref_data['language'],
                            confidence=pref_data['confidence'],
                            source=pref_data['source'],
                            timestamp=datetime.fromisoformat(pref_data['timestamp']),
                            usage_count=pref_data.get('usage_count', 0),
                            last_used=datetime.fromisoformat(pref_data['last_used']) if pref_data.get('last_used') else None,
                            metadata=pref_data.get('metadata', {})
                        ))
    
    async def _save_preferences(self):
        """Sauvegarde les préférences"""
        data = {}
        for speaker, prefs in self.user_preferences.items():
            data[speaker] = []
            for pref in prefs:
                data[speaker].append({
                    'learning_type': pref.learning_type.value,
                    'content': pref.content,
                    'context': pref.context,
                    'language': pref.language,
                    'confidence': pref.confidence,
                    'source': pref.source,
                    'timestamp': pref.timestamp.isoformat(),
                    'usage_count': pref.usage_count,
                    'last_used': pref.last_used.isoformat() if pref.last_used else None,
                    'metadata': pref.metadata
                })
        
        self.preferences_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.preferences_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques d'apprentissage"""
        return {
            **self.stats,
            'vocabulary_fr_size': len(self.vocabulary_fr),
            'vocabulary_en_size': len(self.vocabulary_en),
            'total_vocabulary': len(self.vocabulary_fr) + len(self.vocabulary_en),
            'concepts_learned': len(self.concepts),
            'users_tracked': len(self.user_preferences),
            'total_preferences': sum(len(prefs) for prefs in self.user_preferences.values())
        }


# Test
async def test_continuous_learning():
    """Teste le système d'apprentissage continu"""
    from pathlib import Path
    
    data_dir = Path(__file__).parent.parent / "data"
    learning = ContinuousLearningSystem(data_dir)
    
    await learning.initialize()
    
    # Test analyse conversation
    print("\n📝 Test analyse conversation...")
    learnings = await learning.analyze_conversation(
        user_message="J'aime beaucoup la programmation Python. C'est fascinant!",
        anna_response="Je suis contente que tu aimes Python!",
        speaker="Pierre-Paul",
        context={'location': 'home'}
    )
    
    print(f"   ✓ Nouveaux mots FR: {learnings['new_words_fr']}")
    print(f"   ✓ Nouveaux mots EN: {learnings['new_words_en']}")
    print(f"   ✓ Concepts: {learnings['new_concepts']}")
    print(f"   ✓ Préférences: {len(learnings['preferences'])}")
    
    # Sauvegarde
    await learning.save_all()
    
    # Statistiques
    print("\n📊 Statistiques:")
    stats = learning.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")


if __name__ == "__main__":
    asyncio.run(test_continuous_learning())