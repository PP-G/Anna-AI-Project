"""
Memory Database - Système de mémoire permanente d'Anna
Base de données SQLite avec synchronisation iCloud pour ne JAMAIS rien oublier
"""

import sqlite3
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum


class MemoryType(Enum):
    """Types de souvenirs"""
    CONVERSATION = "conversation"
    LEARNING = "learning"
    PREFERENCE = "preference"
    EVENT = "event"
    CONCEPT = "concept"
    RELATIONSHIP = "relationship"


class ImportanceLevel(Enum):
    """Niveau d'importance des souvenirs"""
    TRIVIAL = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5


@dataclass
class Memory:
    """Structure d'un souvenir"""
    id: Optional[int]
    memory_type: MemoryType
    content: str
    metadata: Dict[str, Any]
    speaker: Optional[str]
    timestamp: datetime
    importance: ImportanceLevel
    tags: List[str]
    context: Optional[str]
    emotions: Optional[Dict[str, float]]
    
    def to_dict(self) -> Dict:
        """Convertit en dictionnaire"""
        return {
            'id': self.id,
            'memory_type': self.memory_type.value,
            'content': self.content,
            'metadata': json.dumps(self.metadata),
            'speaker': self.speaker,
            'timestamp': self.timestamp.isoformat(),
            'importance': self.importance.value,
            'tags': json.dumps(self.tags),
            'context': self.context,
            'emotions': json.dumps(self.emotions) if self.emotions else None
        }


class MemoryDatabase:
    """
    Système de base de données permanente pour Anna
    Stocke TOUS les souvenirs avec synchronisation iCloud
    """
    
    def __init__(self, db_path: Path, cloud_sync_path: Optional[Path] = None):
        self.db_path = db_path
        self.cloud_sync_path = cloud_sync_path or db_path.parent / "icloud_backup"
        self.connection: Optional[sqlite3.Connection] = None
        
        # Statistiques
        self.stats = {
            'total_memories': 0,
            'conversations': 0,
            'learnings': 0,
            'last_consolidation': None
        }
    
    async def initialize(self):
        """Initialise la base de données"""
        print("💾 Initialisation base de données mémoire...")
        
        # Crée le dossier si nécessaire
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Connexe à la base de données
        self.connection = sqlite3.connect(
            str(self.db_path),
            check_same_thread=False
        )
        self.connection.row_factory = sqlite3.Row
        
        # Crée les tables
        await self._create_tables()
        
        # Charge les statistiques
        await self._load_stats()
        
        print(f"   ✓ Base de données initialisée")
        print(f"   ✓ {self.stats['total_memories']} souvenirs en mémoire")
        
    async def _create_tables(self):
        """Crée les tables de la base de données"""
        cursor = self.connection.cursor()
        
        # Table principale des souvenirs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_type TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT,
                speaker TEXT,
                timestamp TEXT NOT NULL,
                importance INTEGER NOT NULL,
                tags TEXT,
                context TEXT,
                emotions TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Index pour recherche rapide
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON memories(timestamp)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_speaker 
            ON memories(speaker)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_importance 
            ON memories(importance)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_memory_type 
            ON memories(memory_type)
        ''')
        
        # Table d'index pour recherche full-text
        cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts 
            USING fts5(content, tags, context)
        ''')
        
        # Table de consolidation (résumés de périodes)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consolidations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                period_start TEXT NOT NULL,
                period_end TEXT NOT NULL,
                summary TEXT NOT NULL,
                key_events TEXT,
                learnings TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des concepts appris
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS concepts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                definition TEXT,
                related_memories TEXT,
                first_learned TEXT NOT NULL,
                confidence REAL DEFAULT 1.0,
                usage_count INTEGER DEFAULT 0
            )
        ''')
        
        # Table des préférences
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person TEXT NOT NULL,
                category TEXT NOT NULL,
                preference TEXT NOT NULL,
                confidence REAL DEFAULT 1.0,
                first_noted TEXT NOT NULL,
                last_confirmed TEXT
            )
        ''')
        
        self.connection.commit()
    
    async def store_memory(self, memory: Memory) -> int:
        """
        Stocke un souvenir dans la base de données
        
        Returns:
            ID du souvenir créé
        """
        cursor = self.connection.cursor()
        
        # Insère dans la table principale
        mem_dict = memory.to_dict()
        del mem_dict['id']  # Auto-increment
        
        columns = ', '.join(mem_dict.keys())
        placeholders = ', '.join(['?' for _ in mem_dict])
        
        cursor.execute(
            f'INSERT INTO memories ({columns}) VALUES ({placeholders})',
            list(mem_dict.values())
        )
        
        memory_id = cursor.lastrowid
        
        # Insère dans l'index full-text
        cursor.execute(
            'INSERT INTO memories_fts (rowid, content, tags, context) VALUES (?, ?, ?, ?)',
            (memory_id, memory.content, json.dumps(memory.tags), memory.context or '')
        )
        
        self.connection.commit()
        self.stats['total_memories'] += 1
        
        # Synchronise avec iCloud de manière asynchrone
        asyncio.create_task(self._sync_to_cloud())
        
        return memory_id
    
    async def store_conversation(
        self,
        user_message: str,
        anna_response: str,
        speaker: str,
        context: Optional[Dict] = None,
        importance: ImportanceLevel = ImportanceLevel.MEDIUM
    ) -> Tuple[int, int]:
        """
        Stocke une conversation complète (message + réponse)
        
        Returns:
            (user_memory_id, anna_memory_id)
        """
        timestamp = datetime.now()
        
        # Message utilisateur
        user_memory = Memory(
            id=None,
            memory_type=MemoryType.CONVERSATION,
            content=user_message,
            metadata={'role': 'user', 'conversation_context': context or {}},
            speaker=speaker,
            timestamp=timestamp,
            importance=importance,
            tags=self._extract_tags(user_message),
            context=json.dumps(context) if context else None,
            emotions=None
        )
        
        user_id = await self.store_memory(user_memory)
        
        # Réponse d'Anna
        anna_memory = Memory(
            id=None,
            memory_type=MemoryType.CONVERSATION,
            content=anna_response,
            metadata={'role': 'anna', 'reply_to': user_id},
            speaker='Anna',
            timestamp=timestamp,
            importance=importance,
            tags=self._extract_tags(anna_response),
            context=json.dumps(context) if context else None,
            emotions=None
        )
        
        anna_id = await self.store_memory(anna_memory)
        
        self.stats['conversations'] += 1
        
        return (user_id, anna_id)
    
    async def store_learning(
        self,
        concept: str,
        definition: str,
        source: str,
        importance: ImportanceLevel = ImportanceLevel.MEDIUM
    ) -> int:
        """Stocke un apprentissage"""
        cursor = self.connection.cursor()
        
        # Vérifie si le concept existe déjà
        cursor.execute('SELECT id, usage_count FROM concepts WHERE name = ?', (concept,))
        existing = cursor.fetchone()
        
        if existing:
            # Met à jour
            cursor.execute(
                'UPDATE concepts SET usage_count = ?, definition = ? WHERE id = ?',
                (existing['usage_count'] + 1, definition, existing['id'])
            )
            self.connection.commit()
            return existing['id']
        else:
            # Crée nouveau
            cursor.execute(
                '''INSERT INTO concepts (name, definition, first_learned, related_memories)
                   VALUES (?, ?, ?, ?)''',
                (concept, definition, datetime.now().isoformat(), json.dumps([]))
            )
            concept_id = cursor.lastrowid
            
            # Crée aussi un souvenir
            memory = Memory(
                id=None,
                memory_type=MemoryType.LEARNING,
                content=f"Appris: {concept} - {definition}",
                metadata={'source': source, 'concept_id': concept_id},
                speaker=None,
                timestamp=datetime.now(),
                importance=importance,
                tags=[concept, 'apprentissage'],
                context=source,
                emotions=None
            )
            
            await self.store_memory(memory)
            self.connection.commit()
            self.stats['learnings'] += 1
            
            return concept_id
    
    async def search_memories(
        self,
        query: Optional[str] = None,
        memory_type: Optional[MemoryType] = None,
        speaker: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        min_importance: Optional[ImportanceLevel] = None,
        tags: Optional[List[str]] = None,
        limit: int = 50
    ) -> List[Dict]:
        """
        Recherche dans les souvenirs avec filtres multiples
        
        Args:
            query: Texte à rechercher (full-text search)
            memory_type: Type de souvenir
            speaker: Personne qui a parlé
            start_date: Date de début
            end_date: Date de fin
            min_importance: Importance minimale
            tags: Tags à rechercher
            limit: Nombre max de résultats
            
        Returns:
            Liste de souvenirs correspondants
        """
        cursor = self.connection.cursor()
        
        # Construction de la requête
        if query:
            # Recherche full-text
            sql = '''
                SELECT m.* FROM memories m
                JOIN memories_fts fts ON m.id = fts.rowid
                WHERE memories_fts MATCH ?
            '''
            params = [query]
        else:
            sql = 'SELECT * FROM memories WHERE 1=1'
            params = []
        
        # Filtres
        if memory_type:
            sql += ' AND memory_type = ?'
            params.append(memory_type.value)
        
        if speaker:
            sql += ' AND speaker = ?'
            params.append(speaker)
        
        if start_date:
            sql += ' AND timestamp >= ?'
            params.append(start_date.isoformat())
        
        if end_date:
            sql += ' AND timestamp <= ?'
            params.append(end_date.isoformat())
        
        if min_importance:
            sql += ' AND importance >= ?'
            params.append(min_importance.value)
        
        if tags:
            # Recherche dans les tags JSON
            tag_conditions = ' OR '.join(['tags LIKE ?' for _ in tags])
            sql += f' AND ({tag_conditions})'
            params.extend([f'%{tag}%' for tag in tags])
        
        sql += ' ORDER BY timestamp DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        
        # Convertit en dictionnaires
        memories = []
        for row in rows:
            mem_dict = dict(row)
            # Parse les champs JSON
            if mem_dict['metadata']:
                mem_dict['metadata'] = json.loads(mem_dict['metadata'])
            if mem_dict['tags']:
                mem_dict['tags'] = json.loads(mem_dict['tags'])
            if mem_dict['emotions']:
                mem_dict['emotions'] = json.loads(mem_dict['emotions'])
            memories.append(mem_dict)
        
        return memories
    
    async def get_recent_conversations(
        self,
        speaker: Optional[str] = None,
        hours: int = 24,
        limit: int = 50
    ) -> List[Dict]:
        """Récupère les conversations récentes"""
        start_date = datetime.now() - timedelta(hours=hours)
        
        return await self.search_memories(
            memory_type=MemoryType.CONVERSATION,
            speaker=speaker,
            start_date=start_date,
            limit=limit
        )
    
    async def get_important_memories(
        self,
        min_importance: ImportanceLevel = ImportanceLevel.HIGH,
        limit: int = 100
    ) -> List[Dict]:
        """Récupère les souvenirs importants"""
        return await self.search_memories(
            min_importance=min_importance,
            limit=limit
        )
    
    async def consolidate_memories(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """
        Consolide les souvenirs d'une période en résumé
        (Utilisé pour les sessions nocturnes)
        """
        print(f"\n🧠 Consolidation des souvenirs ({start_date.date()} à {end_date.date()})...")
        
        # Récupère tous les souvenirs de la période
        memories = await self.search_memories(
            start_date=start_date,
            end_date=end_date,
            limit=1000
        )
        
        if not memories:
            print("   ℹ️  Aucun souvenir à consolider")
            return {}
        
        # Analyse les souvenirs
        conversations_count = sum(1 for m in memories if m['memory_type'] == MemoryType.CONVERSATION.value)
        learnings_count = sum(1 for m in memories if m['memory_type'] == MemoryType.LEARNING.value)
        important_count = sum(1 for m in memories if m['importance'] >= ImportanceLevel.HIGH.value)
        
        # Identifie les événements clés
        key_events = [
            m for m in memories 
            if m['importance'] >= ImportanceLevel.HIGH.value
        ][:10]
        
        # Crée le résumé
        summary = f"""
Période: {start_date.date()} à {end_date.date()}
- {conversations_count} conversations
- {learnings_count} apprentissages
- {important_count} souvenirs importants
        """.strip()
        
        # Stocke la consolidation
        cursor = self.connection.cursor()
        cursor.execute(
            '''INSERT INTO consolidations (period_start, period_end, summary, key_events, learnings)
               VALUES (?, ?, ?, ?, ?)''',
            (
                start_date.isoformat(),
                end_date.isoformat(),
                summary,
                json.dumps([e['content'] for e in key_events]),
                json.dumps([m for m in memories if m['memory_type'] == MemoryType.LEARNING.value])
            )
        )
        self.connection.commit()
        
        self.stats['last_consolidation'] = datetime.now()
        
        print(f"   ✓ Consolidation terminée")
        print(f"   ✓ {len(key_events)} événements clés identifiés")
        
        return {
            'summary': summary,
            'key_events': key_events,
            'total_memories': len(memories),
            'conversations': conversations_count,
            'learnings': learnings_count
        }
    
    async def _sync_to_cloud(self):
        """Synchronise la base de données avec iCloud"""
        try:
            # Crée le dossier de backup si nécessaire
            self.cloud_sync_path.mkdir(parents=True, exist_ok=True)
            
            # Copie la base de données
            import shutil
            backup_path = self.cloud_sync_path / f"memory_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            shutil.copy2(self.db_path, backup_path)
            
            # Garde seulement les 10 derniers backups
            backups = sorted(self.cloud_sync_path.glob("memory_backup_*.db"))
            if len(backups) > 10:
                for old_backup in backups[:-10]:
                    old_backup.unlink()
            
        except Exception as e:
            print(f"   ⚠️  Erreur synchronisation cloud: {e}")
    
    async def _load_stats(self):
        """Charge les statistiques"""
        cursor = self.connection.cursor()
        
        cursor.execute('SELECT COUNT(*) as count FROM memories')
        self.stats['total_memories'] = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM memories WHERE memory_type = ?', 
                      (MemoryType.CONVERSATION.value,))
        self.stats['conversations'] = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM memories WHERE memory_type = ?',
                      (MemoryType.LEARNING.value,))
        self.stats['learnings'] = cursor.fetchone()['count']
    
    def _extract_tags(self, text: str) -> List[str]:
        """Extrait des tags pertinents d'un texte"""
        # Mots-clés simples pour l'instant
        # TODO: Améliorer avec NLP
        keywords = []
        
        # Mots importants communs
        important_words = {
            'amour', 'famille', 'travail', 'projet', 'urgent', 'important',
            'love', 'family', 'work', 'project', 'urgent', 'important',
            'problème', 'solution', 'idée', 'question', 'réponse',
            'problem', 'solution', 'idea', 'question', 'answer'
        }
        
        words = text.lower().split()
        for word in words:
            clean_word = word.strip('.,!?;:')
            if clean_word in important_words:
                keywords.append(clean_word)
        
        return list(set(keywords))[:5]  # Max 5 tags
    
    async def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques de la base de données"""
        await self._load_stats()
        
        cursor = self.connection.cursor()
        
        # Taille de la base de données
        db_size = self.db_path.stat().st_size / (1024 * 1024)  # MB
        
        # Concepts appris
        cursor.execute('SELECT COUNT(*) as count FROM concepts')
        concepts_count = cursor.fetchone()['count']
        
        return {
            **self.stats,
            'database_size_mb': round(db_size, 2),
            'concepts_learned': concepts_count,
            'cloud_sync_enabled': self.cloud_sync_path.exists()
        }
    
    async def close(self):
        """Ferme la connexion à la base de données"""
        if self.connection:
            # Dernière synchronisation
            await self._sync_to_cloud()
            self.connection.close()
            print("💾 Base de données fermée et synchronisée")


# Test
async def test_memory_database():
    """Teste le système de base de données"""
    from pathlib import Path
    
    db_path = Path(__file__).parent.parent / "data" / "memory.db"
    db = MemoryDatabase(db_path)
    
    await db.initialize()
    
    # Stocke une conversation
    print("\n📝 Test stockage conversation...")
    await db.store_conversation(
        user_message="Bonjour Anna, comment vas-tu?",
        anna_response="Bonjour Pierre-Paul ! Je vais très bien, merci !",
        speaker="Pierre-Paul",
        importance=ImportanceLevel.MEDIUM
    )
    
    # Stocke un apprentissage
    print("\n📚 Test stockage apprentissage...")
    await db.store_learning(
        concept="Python",
        definition="Langage de programmation",
        source="conversation",
        importance=ImportanceLevel.HIGH
    )
    
    # Recherche
    print("\n🔍 Test recherche...")
    results = await db.search_memories(query="bonjour", limit=10)
    print(f"   ✓ {len(results)} résultats trouvés")
    
    # Statistiques
    print("\n📊 Statistiques:")
    stats = await db.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    await db.close()


if __name__ == "__main__":
    asyncio.run(test_memory_database())