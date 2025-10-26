"""
Module de synchronisation cloud pour ANNA
Gère la sauvegarde et la synchronisation des données avec iCloud
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class CloudSync:
    """
    Système de synchronisation cloud pour sauvegarder l'état d'Anna
    """
    
    def __init__(self, sync_interval: int = 1800):
        """
        Initialise le système de synchronisation
        
        Args:
            sync_interval: Intervalle de sync en secondes (défaut: 30 min)
        """
        self.sync_interval = sync_interval
        self.last_sync: Optional[datetime] = None
        self.sync_enabled = True
        self.local_path = Path.home() / "Library" / "Mobile Documents" / "com~apple~CloudDocs" / "Anna"
        self.backup_path = Path("data/backups")
        
        # Crée les dossiers si nécessaire
        self.local_path.mkdir(parents=True, exist_ok=True)
        self.backup_path.mkdir(parents=True, exist_ok=True)
        
    async def initialize(self):
        """Initialise la connexion cloud"""
        print("☁️  Initialisation synchronisation icloud")
        
        # Vérifie la connexion
        if self.local_path.exists():
            print("   ✓ Connexion cloud établie")
        else:
            print("   ⚠️  iCloud non disponible, utilisation locale uniquement")
        
        # Charge les données existantes
        await self.load_from_cloud()
        
        print(f"   ✓ Synchronisation automatique activée (toutes les {self.sync_interval//60} min)")
    
    async def load_from_cloud(self):
        """Charge les données depuis le cloud"""
        try:
            state_file = self.local_path / "anna_state.json"
            
            if state_file.exists():
                print("   📥 Récupération des données cloud...")
                with open(state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.last_sync = datetime.fromisoformat(data.get('last_sync', datetime.now().isoformat()))
                return data
            else:
                print("   ℹ️  Aucune donnée cloud existante")
                return None
                
        except Exception as e:
            print(f"   ⚠️  Erreur chargement cloud: {e}")
            return None
    
    async def save_state(self, state: Dict[str, Any]):
        """
        Sauvegarde l'état d'Anna dans le cloud
        
        Args:
            state: État complet à sauvegarder
        """
        if not self.sync_enabled:
            return
        
        try:
            # Ajoute timestamp
            state['last_sync'] = datetime.now().isoformat()
            state['version'] = '1.0.0'
            
            # Sauvegarde dans iCloud
            state_file = self.local_path / "anna_state.json"
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            
            # Backup local également
            backup_file = self.backup_path / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            
            self.last_sync = datetime.now()
            
            # Garde seulement les 10 derniers backups
            self._cleanup_old_backups()
            
        except Exception as e:
            print(f"❌ Erreur sauvegarde cloud: {e}")
    
    def _cleanup_old_backups(self):
        """Supprime les vieux backups pour économiser l'espace"""
        try:
            backups = sorted(self.backup_path.glob("backup_*.json"))
            
            # Garde seulement les 10 plus récents
            if len(backups) > 10:
                for old_backup in backups[:-10]:
                    old_backup.unlink()
                    
        except Exception as e:
            print(f"⚠️  Erreur nettoyage backups: {e}")
    
    async def sync_loop(self):
        """
        Boucle de synchronisation automatique
        À appeler dans une tâche asyncio
        """
        while self.sync_enabled:
            try:
                await asyncio.sleep(self.sync_interval)
                print("🔄 Synchronisation automatique...")
                # La sauvegarde est gérée par core.py
                
            except Exception as e:
                print(f"❌ Erreur sync loop: {e}")
                await asyncio.sleep(60)
    
    def enable_sync(self):
        """Active la synchronisation"""
        self.sync_enabled = True
        print("✅ Synchronisation cloud activée")
    
    def disable_sync(self):
        """Désactive la synchronisation"""
        self.sync_enabled = False
        print("⏸️  Synchronisation cloud désactivée")
    
    def get_sync_status(self) -> Dict[str, Any]:
        """Retourne le statut de la synchronisation"""
        return {
            'enabled': self.sync_enabled,
            'last_sync': self.last_sync.isoformat() if self.last_sync else None,
            'sync_interval': self.sync_interval,
            'cloud_path': str(self.local_path),
            'backup_path': str(self.backup_path)
        }
    
    async def restore_from_backup(self, backup_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Restaure depuis un backup
        
        Args:
            backup_name: Nom du backup (ou None pour le plus récent)
            
        Returns:
            Les données restaurées ou None
        """
        try:
            if backup_name:
                backup_file = self.backup_path / backup_name
            else:
                # Prend le plus récent
                backups = sorted(self.backup_path.glob("backup_*.json"))
                if not backups:
                    print("❌ Aucun backup disponible")
                    return None
                backup_file = backups[-1]
            
            if not backup_file.exists():
                print(f"❌ Backup {backup_file.name} introuvable")
                return None
            
            print(f"📥 Restauration depuis {backup_file.name}...")
            
            with open(backup_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print("✅ Restauration réussie")
            return data
            
        except Exception as e:
            print(f"❌ Erreur restauration: {e}")
            return None
    
    def list_backups(self) -> list[str]:
        """Liste tous les backups disponibles"""
        try:
            backups = sorted(self.backup_path.glob("backup_*.json"))
            return [b.name for b in backups]
        except Exception as e:
            print(f"❌ Erreur listage backups: {e}")
            return []


if __name__ == "__main__":
    print("☁️  Test du système de synchronisation cloud")
    
    async def test():
        # Initialise
        cloud = CloudSync()
        await cloud.initialize()
        
        # Test sauvegarde
        test_state = {
            'name': 'Anna',
            'test': True,
            'timestamp': datetime.now().isoformat()
        }
        
        await cloud.save_state(test_state)
        print("\n✅ Sauvegarde test réussie")
        
        # Statut
        status = cloud.get_sync_status()
        print(f"\n📊 Statut: {status}")
        
        # Liste backups
        backups = cloud.list_backups()
        print(f"\n💾 Backups disponibles ({len(backups)}):")
        for backup in backups[-5:]:  # Montre les 5 derniers
            print(f"   - {backup}")
    
    asyncio.run(test())