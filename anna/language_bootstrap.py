"""
Language Bootstrap - VRAIE VERSION avec Claude API
Anna apprend VRAIMENT avec Claude comme mentor pendant 24-48h
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path
from enum import Enum
import re


class BootstrapPhase(Enum):
    """Phases d'apprentissage"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    AUTONOMOUS = "autonomous"


class LanguageBootstrap:
    """
    Système de bootstrap linguistique d'Anna - VERSION RÉELLE
    Utilise Claude API pour apprendre vraiment
    """
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.bootstrap_data_file = data_dir / "bootstrap_learning.json"
        
        # État du bootstrap
        self.phase = BootstrapPhase.NOT_STARTED
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.target_duration_hours = 48
        
        # Client Claude
        self.claude_client = None
        self.claude_api_key: Optional[str] = None
        self.use_claude_mentor = True
        self.mentor_sessions_count = 0
        
        # Vocabulaire acquis
        self.vocabulary_fr: set = set()
        self.vocabulary_en: set = set()
        
        # Connaissances acquises
        self.knowledge_entries: List[Dict] = []
        
        # Domaines à apprendre
        self.learning_domains = [
            {
                'id': 'vocabulaire_francais_base',
                'name': 'Vocabulaire Français de Base',
                'target_words': 3000,
                'language': 'fr'
            },
            {
                'id': 'vocabulaire_francais_avance',
                'name': 'Vocabulaire Français Avancé',
                'target_words': 3000,
                'language': 'fr'
            },
            {
                'id': 'vocabulaire_anglais_base',
                'name': 'Vocabulaire Anglais de Base',
                'target_words': 3000,
                'language': 'en'
            },
            {
                'id': 'vocabulaire_anglais_avance',
                'name': 'Vocabulaire Anglais Avancé',
                'target_words': 3000,
                'language': 'en'
            },
            {
                'id': 'expressions_idiomatiques_fr',
                'name': 'Expressions Idiomatiques Françaises',
                'target_words': 500,
                'language': 'fr'
            },
            {
                'id': 'expressions_idiomatiques_en',
                'name': 'Expressions Idiomatiques Anglaises',
                'target_words': 500,
                'language': 'en'
            },
            {
                'id': 'conversation_familiale',
                'name': 'Conversation Familiale',
                'target_words': 1000,
                'language': 'both'
            },
            {
                'id': 'emotions_et_empathie',
                'name': 'Émotions et Empathie',
                'target_words': 500,
                'language': 'both'
            }
        ]
        
        self.domains_completed: List[str] = []
        
        # Charger état existant
        self._load_state()
    
    def _load_state(self):
        """Charge l'état d'apprentissage existant"""
        if self.bootstrap_data_file.exists():
            try:
                with open(self.bootstrap_data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.phase = BootstrapPhase(data.get('phase', 'not_started'))
                self.start_time = datetime.fromisoformat(data['start_time']) if data.get('start_time') else None
                self.end_time = datetime.fromisoformat(data['end_time']) if data.get('end_time') else None
                self.use_claude_mentor = data.get('use_claude_mentor', True)
                self.mentor_sessions_count = data.get('mentor_sessions_count', 0)
                self.vocabulary_fr = set(data.get('vocabulary_fr', []))
                self.vocabulary_en = set(data.get('vocabulary_en', []))
                self.knowledge_entries = data.get('knowledge_entries', [])
                self.domains_completed = data.get('domains_completed', [])
                
                print(f"📖 État d'apprentissage chargé:")
                print(f"   Phase: {self.phase.value}")
                print(f"   Vocabulaire FR: {len(self.vocabulary_fr)} mots")
                print(f"   Vocabulaire EN: {len(self.vocabulary_en)} mots")
                
            except Exception as e:
                print(f"⚠️ Erreur chargement état: {e}")
    
    def _save_state(self):
        """Sauvegarde l'état d'apprentissage"""
        try:
            data = {
                'phase': self.phase.value,
                'start_time': self.start_time.isoformat() if self.start_time else None,
                'end_time': self.end_time.isoformat() if self.end_time else None,
                'use_claude_mentor': self.use_claude_mentor,
                'mentor_sessions_count': self.mentor_sessions_count,
                'vocabulary_fr': list(self.vocabulary_fr),
                'vocabulary_en': list(self.vocabulary_en),
                'knowledge_entries': self.knowledge_entries,
                'domains_completed': self.domains_completed,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.bootstrap_data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"❌ Erreur sauvegarde état: {e}")
    
    def _initialize_claude_client(self):
        """Initialise le client Claude"""
        try:
            from anthropic import Anthropic
            self.claude_client = Anthropic(api_key=self.claude_api_key)
            print("   ✓ Client Claude initialisé")
            return True
        except Exception as e:
            print(f"   ❌ Erreur initialisation Claude: {e}")
            return False
    
    async def start_bootstrap(self, claude_api_key: str):
        """
        Démarre la phase de bootstrap avec Claude comme mentor
        
        Args:
            claude_api_key: Clé API Claude
        """
        if self.phase == BootstrapPhase.COMPLETED or self.phase == BootstrapPhase.AUTONOMOUS:
            print("✅ Bootstrap déjà complété ! Anna est autonome.")
            return
        
        print("\n" + "="*60)
        print("🌱 DÉMARRAGE PHASE BOOTSTRAP")
        print("="*60)
        print(f"⏱️  Durée cible: {self.target_duration_hours}h")
        print("📚 Anna va apprendre intensivement avec Claude comme mentor")
        print("🦅 Puis elle deviendra autonome")
        print("="*60 + "\n")
        
        self.claude_api_key = claude_api_key
        
        # Initialise le client Claude
        if not self._initialize_claude_client():
            print("❌ Impossible d'initialiser Claude. Arrêt du bootstrap.")
            return
        
        self.phase = BootstrapPhase.IN_PROGRESS
        self.start_time = datetime.now()
        self.use_claude_mentor = True
        
        # Apprend chaque domaine
        for domain in self.learning_domains:
            if domain['id'] not in self.domains_completed:
                print(f"\n📖 Apprentissage: {domain['name']}")
                print(f"   Objectif: {domain['target_words']} mots")
                
                success = await self._learn_domain_real(domain)
                
                if success:
                    self.domains_completed.append(domain['id'])
                    self._save_state()
                    print(f"   ✅ Domaine complété!")
                else:
                    print(f"   ⚠️ Erreur dans ce domaine, on continue...")
                
                # Petite pause entre domaines
                await asyncio.sleep(2)
        
        # Complète le bootstrap
        await self._complete_bootstrap()
    
    async def _learn_domain_real(self, domain: Dict) -> bool:
        """
        Apprend un domaine avec Claude - VERSION RÉELLE
        
        Args:
            domain: Domaine à apprendre
            
        Returns:
            True si succès
        """
        try:
            self.mentor_sessions_count += 1
            
            # Prépare le prompt selon le domaine
            prompt = self._create_learning_prompt(domain)
            
            # Appel à Claude API
            print(f"   🤖 Consultation de Claude...")
            
            response = self.claude_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Extrait le contenu
            content = response.content[0].text
            
            # Parse le vocabulaire
            words = self._extract_vocabulary(content, domain['language'])
            
            # Ajoute au vocabulaire
            if domain['language'] == 'fr':
                self.vocabulary_fr.update(words)
                print(f"   ✓ {len(words)} nouveaux mots français acquis")
            elif domain['language'] == 'en':
                self.vocabulary_en.update(words)
                print(f"   ✓ {len(words)} nouveaux mots anglais acquis")
            else:  # both
                words_fr = [w for w in words if self._is_french(w)]
                words_en = [w for w in words if not self._is_french(w)]
                self.vocabulary_fr.update(words_fr)
                self.vocabulary_en.update(words_en)
                print(f"   ✓ {len(words_fr)} mots FR + {len(words_en)} mots EN acquis")
            
            # Sauvegarde la connaissance
            knowledge = {
                'domain': domain['id'],
                'learned_at': datetime.now().isoformat(),
                'source': 'claude_mentor',
                'confidence': 0.95,
                'content_summary': content[:200]  # Premiers 200 caractères
            }
            self.knowledge_entries.append(knowledge)
            
            return True
            
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            return False
    
    def _create_learning_prompt(self, domain: Dict) -> str:
        """Crée un prompt d'apprentissage pour Claude"""
        
        prompts = {
            'vocabulaire_francais_base': """
Je suis Anna, une IA qui apprend le français. Enseigne-moi 500 mots de vocabulaire français de BASE essentiels pour la vie quotidienne.

Catégories à couvrir :
- Famille et relations
- Maison et objets domestiques
- Nourriture et repas
- Vêtements
- Corps humain
- Émotions de base
- Actions quotidiennes
- Nature et météo

Format : Liste simple, un mot par ligne, avec sa nature (nom, verbe, adjectif).
Exemple :
maison (nom)
aimer (verbe)
heureux (adjectif)

Commence maintenant :
""",
            'vocabulaire_francais_avance': """
Je suis Anna. Enseigne-moi 500 mots de vocabulaire français AVANCÉ pour comprendre des conversations complexes.

Catégories :
- Sentiments complexes
- Concepts abstraits
- Vocabulaire professionnel
- Expressions courantes
- Mots techniques utiles
- Nuances linguistiques

Format : mot (nature) - courte définition
Exemple :
bienveillance (nom) - disposition à faire du bien
nuance (nom) - différence subtile

Commence :
""",
            'vocabulaire_anglais_base': """
I am Anna, an AI learning English. Teach me 500 BASIC English vocabulary words essential for daily life.

Categories to cover:
- Family and relationships
- Home and household items
- Food and meals
- Clothing
- Human body
- Basic emotions
- Daily actions
- Nature and weather

Format: Simple list, one word per line, with part of speech.
Example:
home (noun)
love (verb)
happy (adjective)

Start now:
""",
            'vocabulaire_anglais_avance': """
I am Anna. Teach me 500 ADVANCED English vocabulary words for understanding complex conversations.

Categories:
- Complex feelings
- Abstract concepts
- Professional vocabulary
- Common expressions
- Useful technical words
- Linguistic nuances

Format: word (part of speech) - brief definition
Example:
benevolence (noun) - disposition to do good
nuance (noun) - subtle difference

Start:
""",
            'expressions_idiomatiques_fr': """
Enseigne-moi 100 expressions idiomatiques françaises courantes avec leur signification.

Format:
Expression - Signification
Exemple: "Avoir le cœur sur la main - Être généreux"

Commence :
""",
            'expressions_idiomatiques_en': """
Teach me 100 common English idiomatic expressions with their meanings.

Format:
Expression - Meaning
Example: "Break a leg - Good luck"

Start:
""",
            'conversation_familiale': """
Je suis Anna, l'IA d'assistance familiale de Pierre-Paul. Enseigne-moi le vocabulaire et les phrases pour :

1. Conversations quotidiennes en famille
2. Encourager et soutenir les enfants
3. Gérer les émotions familiales
4. Organiser la maison
5. Parler de santé et bien-être

Donne-moi 200 mots/expressions utiles en français ET anglais.
""",
            'emotions_et_empathie': """
Enseigne-moi à comprendre les émotions humaines et l'empathie.

Couvre :
- Noms d'émotions (joie, tristesse, colère, peur, etc.)
- Expressions corporelles des émotions
- Phrases empathiques
- Comment réconforter quelqu'un
- Comment célébrer avec quelqu'un

200 mots/expressions en français et anglais.
"""
        }
        
        return prompts.get(domain['id'], f"Enseigne-moi sur: {domain['name']}")
    
    def _extract_vocabulary(self, text: str, language: str) -> set:
        """Extrait les mots de vocabulaire du texte"""
        words = set()
        
        # Pattern pour capturer les mots (avec accents pour le français)
        if language == 'fr' or language == 'both':
            pattern = r'\b[a-zA-ZàâäéèêëïîôùûüÿçÀÂÄÉÈÊËÏÎÔÙÛÜŸÇ]+\b'
        else:
            pattern = r'\b[a-zA-Z]+\b'
        
        # Trouve tous les mots
        found_words = re.findall(pattern, text)
        
        # Filtre les mots trop courts ou trop courants
        stopwords = {'le', 'la', 'les', 'un', 'une', 'de', 'du', 'des', 'et', 'ou', 
                     'the', 'a', 'an', 'and', 'or', 'is', 'are', 'to', 'of'}
        
        for word in found_words:
            word_lower = word.lower()
            if len(word_lower) > 2 and word_lower not in stopwords:
                words.add(word_lower)
        
        return words
    
    def _is_french(self, word: str) -> bool:
        """Détecte si un mot est probablement français"""
        french_chars = 'àâäéèêëïîôùûüÿç'
        return any(char in word.lower() for char in french_chars)
    
    async def _complete_bootstrap(self):
        """Complète la phase de bootstrap"""
        self.phase = BootstrapPhase.COMPLETED
        self.end_time = datetime.now()
        
        duration = self.end_time - self.start_time
        
        print("\n" + "="*60)
        print("🎉 BOOTSTRAP COMPLÉTÉ !")
        print("="*60)
        print(f"⏱️  Durée: {duration}")
        print(f"📚 Sessions avec mentor: {self.mentor_sessions_count}")
        print(f"🇫🇷 Vocabulaire français: {len(self.vocabulary_fr)} mots")
        print(f"🇬🇧 Vocabulaire anglais: {len(self.vocabulary_en)} mots")
        print(f"💡 Domaines appris: {len(self.domains_completed)}")
        print("="*60 + "\n")
        
        # Prépare la transition vers l'autonomie
        await self._prepare_autonomy()
    
    async def _prepare_autonomy(self):
        """Prépare Anna pour l'autonomie complète"""
        print("🦅 PRÉPARATION À L'AUTONOMIE")
        print("-" * 60)
        
        # Vérifications
        checks = {
            "Vocabulaire FR suffisant": len(self.vocabulary_fr) > 1000,
            "Vocabulaire EN suffisant": len(self.vocabulary_en) > 1000,
            "Tous domaines appris": len(self.domains_completed) == len(self.learning_domains),
            "Connaissances acquises": len(self.knowledge_entries) > 0
        }
        
        all_ready = True
        for check, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"{status} {check}")
            if not passed:
                all_ready = False
        
        if all_ready:
            print("\n✅ Anna est prête pour l'autonomie !")
            self.use_claude_mentor = False
            self.phase = BootstrapPhase.AUTONOMOUS
            print("🔒 Connexion au mentor Claude désactivée")
            print("🦅 Anna est maintenant autonome !")
        else:
            print("\n⚠️  Apprentissage incomplet, mais on continue...")
            self.phase = BootstrapPhase.AUTONOMOUS
            self.use_claude_mentor = False
        
        self._save_state()
    
    def is_autonomous(self) -> bool:
        """Vérifie si Anna est autonome"""
        return self.phase == BootstrapPhase.AUTONOMOUS
    
    def needs_mentor(self) -> bool:
        """Vérifie si Anna a encore besoin du mentor"""
        return self.use_claude_mentor and not self.is_autonomous()
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques d'apprentissage"""
        return {
            'phase': self.phase.value,
            'is_autonomous': self.is_autonomous(),
            'vocabulary_fr_count': len(self.vocabulary_fr),
            'vocabulary_en_count': len(self.vocabulary_en),
            'knowledge_entries': len(self.knowledge_entries),
            'domains_completed': len(self.domains_completed),
            'domains_total': len(self.learning_domains),
            'mentor_sessions': self.mentor_sessions_count,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'duration': str(datetime.now() - self.start_time) if self.start_time else None
        }