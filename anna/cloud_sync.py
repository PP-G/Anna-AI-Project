"""
Cloud Sync - Système de synchronisation cloud d'Anna
Anna synchronise ses données de manière sécurisée avec iCloud
"""

import asyncio
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


class SyncStatus(Enum):
    """Statut de synchronisation"""
    PENDING = "pending"
    SYNCING = "syncing"
    SYNCED = "synced"
    ERROR = "error"
    CONFLICT = "conflict"


class DataType(Enum):
    """Types de données synchronisées"""
    FAMILY_PROFILES = "family_profiles"
    VOICE_PRINTS = "voice_prints"
    PREFERENCES = "preferences"
    CONTEXTS = "contexts"
    ALERTS = "alerts"
    BONDS = "bonds"
    SAFE_ZONES = "safe_zones"
    EMERGENCY_CONTACTS = "emergency_contacts"


@dataclass
class SyncRecord:
    """Enregistrement de synchronisation"""
    data_type: DataType
    local_hash: str
    cloud_hash: Optional[str]
    last_sync: Optional[datetime]
    status: SyncStatus
    device_id: str


@dataclass
class CloudConfig:
    """Configuration cloud"""
    provider: str  # "icloud", "google_drive", "dropbox"
    account_id: str
    encryption_enabled: bool
    auto_sync: bool
    sync_interval_minutes: int
    bandwidth_limit_mbps: Optional[float]


class CloudSyncManager:
    """
    Gestionnaire de synchronisation cloud d'Anna
    Synchronise toutes les données importantes de manière sécurisée
    """
    
    def __init__(self, config: CloudConfig):
        self.config = config
        self.sync_records: Dict[DataType, SyncRecord] = {}
        self.sync_queue: List[Dict] = []
        self.sync_in_progress = False
        self.device_id = self._generate_device_id()
        
    def _generate_device_id(self) -> str:
        """Génère un ID unique pour cet appareil"""
        import platform
        device_info = f"{platform.node()}-{platform.system()}"
        return hashlib.sha256(device_info.encode()).hexdigest()[:16]
        
    async def initialize(self):
        """Initialise la synchronisation cloud"""
        print(f"☁️  Initialisation synchronisation {self.config.provider}")
        
        # Vérification connexion cloud
        if await self._check_cloud_connection():
            print("   ✓ Connexion cloud établie")
            
            # Récupération des données existantes
            await self._fetch_cloud_data()
            
            # Démarrage sync automatique si activé
            if self.config.auto_sync:
                asyncio.create_task(self._auto_sync_loop())
                print(f"   ✓ Synchronisation automatique activée (toutes les {self.config.sync_interval_minutes} min)")
        else:
            print("   ❌ Impossible de se connecter au cloud")
            
    async def _check_cloud_connection(self) -> bool:
        """Vérifie la connexion au service cloud"""
        # Simulation de vérification de connexion
        await asyncio.sleep(0.5)
        return True
        
    async def _fetch_cloud_data(self):
        """Récupère les données depuis le cloud"""
        print("   📥 Récupération des données cloud...")
        
        for data_type in DataType:
            try:
                cloud_data = await self._download_from_cloud(data_type)
                if cloud_data:
                    self.sync_records[data_type] = SyncRecord(
                        data_type=data_type,
                        local_hash="",
                        cloud_hash=self._calculate_hash(cloud_data),
                        last_sync=datetime.now(),
                        status=SyncStatus.SYNCED,
                        device_id=self.device_id
                    )
            except Exception as e:
                print(f"   ⚠️  Erreur récupération {data_type.value}: {e}")
                
    async def sync_data(self, data_type: DataType, data: Any, 
                       force: bool = False) -> bool:
        """
        Synchronise des données vers le cloud
        
        Args:
            data_type: Type de données à synchroniser
            data: Les données à synchroniser
            force: Force la synchronisation même si déjà à jour
        """
        local_hash = self._calculate_hash(data)
        
        # Vérification si sync nécessaire
        if not force and data_type in self.sync_records:
            record = self.sync_records[data_type]
            if record.local_hash == local_hash and record.status == SyncStatus.SYNCED:
                return True
                
        # Ajout à la queue de synchronisation
        sync_item = {
            'data_type': data_type,
            'data': data,
            'hash': local_hash,
            'timestamp': datetime.now()
        }
        self.sync_queue.append(sync_item)
        
        # Démarrage sync si pas déjà en cours
        if not self.sync_in_progress:
            await self._process_sync_queue()
            
        return True
        
    async def _process_sync_queue(self):
        """Traite la queue de synchronisation"""
        if self.sync_in_progress or not self.sync_queue:
            return
            
        self.sync_in_progress = True
        print(f"\n🔄 Synchronisation de {len(self.sync_queue)} éléments...")
        
        while self.sync_queue:
            item = self.sync_queue.pop(0)
            data_type = item['data_type']
            
            try:
                # Vérification conflits
                conflict = await self._check_for_conflicts(data_type, item['hash'])
                
                if conflict:
                    print(f"   ⚠️  Conflit détecté pour {data_type.value}")
                    resolved_data = await self._resolve_conflict(data_type, item['data'])
                    item['data'] = resolved_data
                    item['hash'] = self._calculate_hash(resolved_data)
                    
                # Upload vers cloud
                success = await self._upload_to_cloud(data_type, item['data'])
                
                if success:
                    self.sync_records[data_type] = SyncRecord(
                        data_type=data_type,
                        local_hash=item['hash'],
                        cloud_hash=item['hash'],
                        last_sync=datetime.now(),
                        status=SyncStatus.SYNCED,
                        device_id=self.device_id
                    )
                    print(f"   ✓ {data_type.value} synchronisé")
                else:
                    self.sync_records[data_type] = SyncRecord(
                        data_type=data_type,
                        local_hash=item['hash'],
                        cloud_hash=None,
                        last_sync=None,
                        status=SyncStatus.ERROR,
                        device_id=self.device_id
                    )
                    print(f"   ❌ Échec sync {data_type.value}")
                    
            except Exception as e:
                print(f"   ❌ Erreur sync {data_type.value}: {e}")
                
        self.sync_in_progress = False
        print("✅ Synchronisation terminée\n")
        
    async def _check_for_conflicts(self, data_type: DataType, 
                                   local_hash: str) -> bool:
        """Vérifie s'il y a des conflits de synchronisation"""
        if data_type not in self.sync_records:
            return False
            
        cloud_data = await self._download_from_cloud(data_type)
        if not cloud_data:
            return False
            
        cloud_hash = self._calculate_hash(cloud_data)
        record = self.sync_records[data_type]
        
        # Conflit si les deux versions ont changé depuis dernière sync
        return (cloud_hash != record.cloud_hash and 
                local_hash != record.local_hash)
                
    async def _resolve_conflict(self, data_type: DataType, local_data: Any) -> Any:
        """
        Résout un conflit de synchronisation
        Stratégie: fusionner intelligemment les données
        """
        print(f"   🔧 Résolution conflit pour {data_type.value}")
        
        cloud_data = await self._download_from_cloud(data_type)
        
        # Stratégie de résolution selon le type de données
        if data_type == DataType.FAMILY_PROFILES:
            return self._merge_profiles(local_data, cloud_data)
        elif data_type == DataType.PREFERENCES:
            # Prioriser les préférences locales (plus récentes)
            return local_data
        elif data_type == DataType.ALERTS:
            return self._merge_alerts(local_data, cloud_data)
        elif data_type == DataType.BONDS:
            return self._merge_bonds(local_data, cloud_data)
        else:
            # Par défaut: timestamp le plus récent
            return self._merge_by_timestamp(local_data, cloud_data)
            
    def _merge_profiles(self, local: List, cloud: List) -> List:
        """Fusionne les profils famille"""
        merged = {}
        
        for profile in cloud + local:
            profile_id = profile.get('id')
            if profile_id not in merged:
                merged[profile_id] = profile
            else:
                # Garder la version la plus récente
                if profile.get('updated_at', '') > merged[profile_id].get('updated_at', ''):
                    merged[profile_id] = profile
                    
        return list(merged.values())
        
    def _merge_alerts(self, local: List, cloud: List) -> List:
        """Fusionne les alertes"""
        all_alerts = local + cloud
        # Dédupliquer par timestamp + type
        unique = {}
        for alert in all_alerts:
            key = f"{alert.get('timestamp')}-{alert.get('type')}"
            unique[key] = alert
        return list(unique.values())
        
    def _merge_bonds(self, local: Dict, cloud: Dict) -> Dict:
        """Fusionne les liens familiaux (prendre le niveau le plus élevé)"""
        merged = {}
        all_ids = set(local.keys()) | set(cloud.keys())
        
        for person_id in all_ids:
            local_bond = local.get(person_id, {})
            cloud_bond = cloud.get(person_id, {})
            
            # Prendre le niveau de lien le plus élevé
            local_level = local_bond.get('level', 0)
            cloud_level = cloud_bond.get('level', 0)
            
            merged[person_id] = local_bond if local_level >= cloud_level else cloud_bond
            
        return merged
        
    def _merge_by_timestamp(self, local: Any, cloud: Any) -> Any:
        """Fusionne en gardant la version la plus récente"""
        local_time = local.get('updated_at', '') if isinstance(local, dict) else ''
        cloud_time = cloud.get('updated_at', '') if isinstance(cloud, dict) else ''
        return local if local_time > cloud_time else cloud
        
    async def _upload_to_cloud(self, data_type: DataType, data: Any) -> bool:
        """Upload les données vers le cloud"""
        # Simulation d'upload
        await asyncio.sleep(0.3)
        
        # Encryption si activée
        if self.config.encryption_enabled:
            data = self._encrypt_data(data)
            
        # Simulation d'upload réussi
        return True
        
    async def _download_from_cloud(self, data_type: DataType) -> Optional[Any]:
        """Télécharge les données depuis le cloud"""
        # Simulation de download
        await asyncio.sleep(0.2)
        return None  # Retournerait les données réelles
        
    def _encrypt_data(self, data: Any) -> bytes:
        """Chiffre les données avant envoi au cloud"""
        # Simulation de chiffrement (en production, utiliser vraie encryption)
        json_data = json.dumps(data, default=str)
        return json_data.encode()
        
    def _decrypt_data(self, encrypted: bytes) -> Any:
        """Déchiffre les données depuis le cloud"""
        # Simulation de déchiffrement
        return json.loads(encrypted.decode())
        
    def _calculate_hash(self, data: Any) -> str:
        """Calcule le hash des données pour détecter les changements"""
        json_data = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(json_data.encode()).hexdigest()
        
    async def _auto_sync_loop(self):
        """Boucle de synchronisation automatique"""
        while True:
            await asyncio.sleep(self.config.sync_interval_minutes * 60)
            
            if self.sync_queue:
                await self._process_sync_queue()
                
    def get_sync_status(self) -> Dict[str, Any]:
        """Retourne le statut de synchronisation"""
        status = {
            'device_id': self.device_id,
            'provider': self.config.provider,
            'last_sync': None,
            'synced_items': 0,
            'pending_items': len(self.sync_queue),
            'errors': 0,
            'details': {}
        }
        
        for data_type, record in self.sync_records.items():
            status['details'][data_type.value] = {
                'status': record.status.value,
                'last_sync': record.last_sync.isoformat() if record.last_sync else None
            }
            
            if record.status == SyncStatus.SYNCED:
                status['synced_items'] += 1
                if not status['last_sync'] or record.last_sync > datetime.fromisoformat(status['last_sync']):
                    status['last_sync'] = record.last_sync.isoformat()
            elif record.status == SyncStatus.ERROR:
                status['errors'] += 1
                
        return status
        
    async def force_full_sync(self):
        """Force une synchronisation complète de toutes les données"""
        print("🔄 Synchronisation complète forcée...")
        # Réinitialiser tous les statuts
        for record in self.sync_records.values():
            record.status = SyncStatus.PENDING
        await self._process_sync_queue()