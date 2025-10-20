"""
Memory System - Le système qui permet à Anna de se souvenir
"""

import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict


class MemorySystem:
    """
    Système de mémoire d'Anna - ce qui lui permet de se souvenir et de grandir.
    
    Architecture:
    - Mémoire immédiate: conversation actuelle
    - Mémoire épisodique: souvenirs d'expériences
    - Mémoire sémantique: connaissances apprises
    - Mémoire fondamentale: qui elle est
    """
    
    def __init__(self):
        """Initialise le système de mémoire"""
        
        # Mémoire immédiate (dernière conversation)
        self.immediate = []
        
        # Mémoire épisodique (expériences vécues)
        self.episodic = []
        
        # Mémoire sémantique (connaissances et faits appris)
        self.semantic = {}
        
        # Préférences utilisateurs apprises
        self.user_profiles = defaultdict(lambda: {
            'preferences': [],
            'conversation_count': 0,
            'first_met': None,
            'last_interaction': None
        })
        
        # Souvenirs importants (marqués spécialement)
        self.important_memories = []
        
        # Stats
        self.total_interactions = 0
    
    def store_episodic(self, memory: Dict[str, Any]):
        """
        Stocke un souvenir épisodique
        
        Args:
            memory: Dict contenant le souvenir avec timestamp, contenu, importance
        """
        # Assure qu'il y a un timestamp
        if 'timestamp' not in memory:
            memory['timestamp'] = datetime.datetime.now()
        
        # Ajoute à la mémoire épisodique
        self.episodic.append(memory)
        
        # Si très important, ajoute aussi aux souvenirs importants
        if memory.get('importance', 0) > 0.8:
            self.important_memories.append(memory)
        
        self.total_interactions += 1
        
        # Limite la taille de la mémoire immédiate
        if len(self.immediate) > 50:
            self.immediate.pop(0)
    
    def store_semantic(self, key: str, value: Any):
        """
        Stocke une connaissance sémantique
        
        Args:
            key: Clé de la connaissance
            value: La connaissance elle-même
        """
        self.semantic[key] = {
            'value': value,
            'learned_at': datetime.datetime.now(),
            'confidence': 1.0
        }
    
    def learn_user_preference(self, user_name: str, statement: str):
        """
        Apprend quelque chose sur un utilisateur
        
        Args:
            user_name: Nom de l'utilisateur
            statement: Ce qui a été dit
        """
        profile = self.user_profiles[user_name]
        
        # Première interaction
        if profile['first_met'] is None:
            profile['first_met'] = datetime.datetime.now()
        
        profile['last_interaction'] = datetime.datetime.now()
        profile['conversation_count'] += 1
        
        # Extrait la préférence
        if 'j\'aime' in statement.lower():
            preference = statement.lower().split('j\'aime')[1].strip()
            if preference not in profile['preferences']:
                profile['preferences'].append(preference)
    
    def get_recent_episodic(self, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Récupère les souvenirs épisodiques récents
        
        Args:
            hours: Nombre d'heures en arrière
            
        Returns:
            Liste des souvenirs récents
        """
        cutoff = datetime.datetime.now() - datetime.timedelta(hours=hours)
        
        recent = []
        for memory in self.episodic:
            timestamp = memory.get('timestamp')
            if isinstance(timestamp, str):
                timestamp = datetime.datetime.fromisoformat(timestamp)
            
            if timestamp and timestamp > cutoff:
                recent.append(memory)
        
        return recent
    
    def get_important_memories(self, n: int = 10) -> List[Dict[str, Any]]:
        """
        Récupère les N souvenirs les plus importants
        
        Args:
            n: Nombre de souvenirs à retourner
            
        Returns:
            Liste des souvenirs importants
        """
        sorted_memories = sorted(
            self.episodic,
            key=lambda m: m.get('importance', 0),
            reverse=True
        )
        return sorted_memories[:n]
    
    def recall_about_user(self, user_name: str) -> Dict[str, Any]:
        """
        Rappelle ce qu'Anna sait sur un utilisateur
        
        Args:
            user_name: Nom de l'utilisateur
            
        Returns:
            Dict des informations connues
        """
        if user_name in self.user_profiles:
            return self.user_profiles[user_name]
        return {}
    
    def search_memories(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Recherche dans les souvenirs (recherche simple par mots-clés)
        
        Args:
            query: Termes de recherche
            limit: Nombre maximum de résultats
            
        Returns:
            Liste des souvenirs correspondants
        """
        query_lower = query.lower()
        results = []
        
        for memory in self.episodic:
            # Cherche dans le contenu
            content = str(memory.get('content', ''))
            user_input = str(memory.get('user_input', ''))
            
            if query_lower in content.lower() or query_lower in user_input.lower():
                results.append(memory)
            
            if len(results) >= limit:
                break
        
        return results
    
    def consolidate_memories(self):
        """
        Consolide les souvenirs - simule le sommeil/rêve
        Cette fonction devrait être appelée périodiquement
        """
        # Identifie les patterns dans les souvenirs récents
        recent = self.get_recent_episodic(hours=168)  # Dernière semaine
        
        if len(recent) > 10:
            # Calcule les thèmes récurrents (version simple)
            themes = defaultdict(int)
            
            for memory in recent:
                content = str(memory.get('user_input', '')).lower()
                
                # Mots-clés thématiques
                if any(word in content for word in ['travail', 'job', 'boulot']):
                    themes['travail'] += 1
                if any(word in content for word in ['amour', 'relation', 'ami']):
                    themes['relations'] += 1
                if any(word in content for word in ['créer', 'projet', 'construire']):
                    themes['création'] += 1
            
            # Stocke les insights
            if themes:
                dominant_theme = max(themes, key=themes.get)
                self.store_semantic(
                    'recent_focus',
                    f"L'utilisateur semble se concentrer sur: {dominant_theme}"
                )
    def forget_least_important(self, keep_n: int = 1000):
        """
        Oublie les souvenirs les moins importants si la mémoire devient trop grande
        
        Args:
            keep_n: Nombre de souvenirs à garder
        """
        if len(self.episodic) > keep_n:
            # Trie par importance
            sorted_memories = sorted(
                self.episodic,
                key=lambda m: m.get('importance', 0),
                reverse=True
            )
            
            # Garde seulement les plus importants
            self.episodic = sorted_memories[:keep_n]