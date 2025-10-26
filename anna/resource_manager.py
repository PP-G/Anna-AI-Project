"""
Resource Manager - Gestionnaire de ressources pour Anna
Contrôle l'utilisation CPU/RAM et gère l'apprentissage en arrière-plan
"""

import asyncio
import psutil
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Any, List
from enum import Enum
from dataclasses import dataclass


class PerformanceMode(Enum):
    """Modes de performance disponibles"""
    MINIMAL = "minimal"      # 10-20% CPU - Pour jeux, rendu vidéo
    LOW = "low"              # 20-40% CPU - Travail normal
    MEDIUM = "medium"        # 40-60% CPU - Par défaut
    HIGH = "high"            # 60-80% CPU - Conversations importantes
    BACKGROUND = "background" # 5-10% CPU - Apprentissage silencieux


@dataclass
class ResourceLimits:
    """Limites de ressources pour un mode"""
    max_cpu_percent: float
    max_memory_mb: float
    max_threads: int
    response_timeout_sec: float
    learning_enabled: bool


class ResourceManager:
    """
    Gestionnaire de ressources pour Anna
    Contrôle l'utilisation CPU/RAM et coordonne l'apprentissage en arrière-plan
    """
    
    def __init__(self):
        self.current_mode = PerformanceMode.MEDIUM
        self.process = psutil.Process()
        
        # Définition des limites par mode
        self.mode_limits = {
            PerformanceMode.MINIMAL: ResourceLimits(
                max_cpu_percent=20.0,
                max_memory_mb=200.0,
                max_threads=2,
                response_timeout_sec=30.0,
                learning_enabled=False
            ),
            PerformanceMode.LOW: ResourceLimits(
                max_cpu_percent=40.0,
                max_memory_mb=400.0,
                max_threads=4,
                response_timeout_sec=15.0,
                learning_enabled=True
            ),
            PerformanceMode.MEDIUM: ResourceLimits(
                max_cpu_percent=60.0,
                max_memory_mb=800.0,
                max_threads=6,
                response_timeout_sec=10.0,
                learning_enabled=True
            ),
            PerformanceMode.HIGH: ResourceLimits(
                max_cpu_percent=80.0,
                max_memory_mb=1500.0,
                max_threads=8,
                response_timeout_sec=5.0,
                learning_enabled=True
            ),
            PerformanceMode.BACKGROUND: ResourceLimits(
                max_cpu_percent=10.0,
                max_memory_mb=150.0,
                max_threads=2,
                response_timeout_sec=60.0,
                learning_enabled=True
            )
        }
        
        # Configuration d'apprentissage en arrière-plan
        self.background_learning_config = {
            'enabled': True,
            'schedule': [
                {'hour': 2, 'duration_minutes': 60},   # 2h du matin, 1h
                {'hour': 14, 'duration_minutes': 30},  # 14h, 30min
            ],
            'min_idle_minutes': 15,  # Attendre 15min d'inactivité
            'max_cpu_threshold': 50.0  # S'arrêter si CPU > 50%
        }
        
        # État
        self.background_learning_active = False
        self.last_activity = datetime.now()
        self.monitoring_active = False
        
        # Statistiques
        self.stats = {
            'mode_changes': 0,
            'background_sessions': 0,
            'total_background_time': 0,
            'cpu_violations': 0,
            'memory_violations': 0,
            'last_mode_change': None
        }
    
    async def initialize(self):
        """Initialise le gestionnaire de ressources"""
        print("🎮 Initialisation gestionnaire de ressources...")
        
        # Détecte les ressources système disponibles
        cpu_count = psutil.cpu_count()
        total_memory = psutil.virtual_memory().total / (1024**3)  # GB
        
        print(f"   ℹ️  CPU disponibles: {cpu_count}")
        print(f"   ℹ️  Mémoire totale: {total_memory:.1f} GB")
        print(f"   ✓ Mode actuel: {self.current_mode.value.upper()}")
        
        # Démarre la surveillance
        asyncio.create_task(self._monitor_resources())
        asyncio.create_task(self._schedule_background_learning())
        
        self.monitoring_active = True
    
    async def set_mode(self, mode: PerformanceMode, reason: str = "manual"):
        """
        Change le mode de performance
        
        Args:
            mode: Nouveau mode
            reason: Raison du changement (manual, auto, emergency)
        """
        old_mode = self.current_mode
        self.current_mode = mode
        
        limits = self.mode_limits[mode]
        
        print(f"\n🎮 Changement de mode: {old_mode.value.upper()} → {mode.value.upper()}")
        print(f"   Raison: {reason}")
        print(f"   CPU max: {limits.max_cpu_percent}%")
        print(f"   Mémoire max: {limits.max_memory_mb} MB")
        print(f"   Apprentissage: {'✓' if limits.learning_enabled else '✗'}")
        
        self.stats['mode_changes'] += 1
        self.stats['last_mode_change'] = datetime.now()
        
        # Arrête l'apprentissage en arrière-plan si mode trop bas
        if mode in [PerformanceMode.MINIMAL, PerformanceMode.LOW]:
            if self.background_learning_active:
                await self._stop_background_learning()
    
    async def request_mode_from_message(self, message: str) -> bool:
        """
        Détecte et applique un changement de mode depuis un message
        
        Returns:
            True si un mode a été changé
        """
        message_lower = message.lower()
        
        # Patterns de demande
        if any(phrase in message_lower for phrase in [
            'utilise moins de ressources',
            'économise',
            'ralentis',
            'use less resources',
            'slow down'
        ]):
            await self.set_mode(PerformanceMode.LOW, "user_request")
            return True
        
        elif any(phrase in message_lower for phrase in [
            'j\'ai besoin de performance',
            'libère des ressources',
            'i need performance',
            'free up resources'
        ]):
            await self.set_mode(PerformanceMode.MINIMAL, "user_request")
            return True
        
        elif any(phrase in message_lower for phrase in [
            'mode normal',
            'par défaut',
            'normal mode',
            'default'
        ]):
            await self.set_mode(PerformanceMode.MEDIUM, "user_request")
            return True
        
        elif any(phrase in message_lower for phrase in [
            'utilise plus de ressources',
            'performance maximale',
            'use more resources',
            'maximum performance'
        ]):
            await self.set_mode(PerformanceMode.HIGH, "user_request")
            return True
        
        elif any(phrase in message_lower for phrase in [
            'apprends en arrière-plan',
            'apprentissage silencieux',
            'learn in background',
            'silent learning'
        ]):
            await self._start_background_learning()
            return True
        
        return False
    
    def get_current_limits(self) -> ResourceLimits:
        """Retourne les limites du mode actuel"""
        return self.mode_limits[self.current_mode]
    
    async def check_resources(self) -> Dict[str, Any]:
        """
        Vérifie l'utilisation actuelle des ressources
        
        Returns:
            Dict avec CPU%, mémoire, statut
        """
        try:
            # CPU
            cpu_percent = self.process.cpu_percent(interval=0.1)
            
            # Mémoire
            memory_info = self.process.memory_info()
            memory_mb = memory_info.rss / (1024**2)
            
            # Threads
            num_threads = self.process.num_threads()
            
            # Limites actuelles
            limits = self.get_current_limits()
            
            # Violations
            cpu_ok = cpu_percent <= limits.max_cpu_percent
            memory_ok = memory_mb <= limits.max_memory_mb
            
            if not cpu_ok:
                self.stats['cpu_violations'] += 1
            if not memory_ok:
                self.stats['memory_violations'] += 1
            
            return {
                'cpu_percent': cpu_percent,
                'memory_mb': memory_mb,
                'num_threads': num_threads,
                'mode': self.current_mode.value,
                'cpu_ok': cpu_ok,
                'memory_ok': memory_ok,
                'cpu_limit': limits.max_cpu_percent,
                'memory_limit': limits.max_memory_mb,
                'within_limits': cpu_ok and memory_ok
            }
        
        except Exception as e:
            print(f"   ⚠️  Erreur vérification ressources: {e}")
            return {
                'cpu_percent': 0,
                'memory_mb': 0,
                'num_threads': 0,
                'mode': self.current_mode.value,
                'cpu_ok': True,
                'memory_ok': True,
                'within_limits': True
            }
    
    async def _monitor_resources(self):
        """Surveillance continue des ressources"""
        while self.monitoring_active:
            try:
                resources = await self.check_resources()
                
                # Si dépassement important (>150% des limites), passe en mode inférieur
                if not resources['within_limits']:
                    cpu_ratio = resources['cpu_percent'] / resources['cpu_limit']
                    memory_ratio = resources['memory_mb'] / resources['memory_limit']
                    
                    if cpu_ratio > 1.5 or memory_ratio > 1.5:
                        # Urgence : descend d'un niveau
                        await self._downgrade_mode_emergency()
                
                # Attendre avant prochaine vérification
                await asyncio.sleep(10)  # Vérifie toutes les 10 secondes
            
            except Exception as e:
                print(f"   ⚠️  Erreur monitoring: {e}")
                await asyncio.sleep(30)
    
    async def _downgrade_mode_emergency(self):
        """Descend d'un mode en cas d'urgence"""
        mode_order = [
            PerformanceMode.HIGH,
            PerformanceMode.MEDIUM,
            PerformanceMode.LOW,
            PerformanceMode.MINIMAL
        ]
        
        current_index = mode_order.index(self.current_mode)
        if current_index < len(mode_order) - 1:
            new_mode = mode_order[current_index + 1]
            await self.set_mode(new_mode, "emergency_downgrade")
    
    async def _schedule_background_learning(self):
        """Planifie les sessions d'apprentissage en arrière-plan"""
        while self.monitoring_active:
            try:
                if not self.background_learning_config['enabled']:
                    await asyncio.sleep(60)
                    continue
                
                now = datetime.now()
                
                # Vérifie si on est dans une plage horaire planifiée
                for schedule in self.background_learning_config['schedule']:
                    target_hour = schedule['hour']
                    duration = schedule['duration_minutes']
                    
                    # Si on est à l'heure prévue (± 5 minutes)
                    if abs(now.hour - target_hour) == 0 and now.minute < 5:
                        # Vérifie l'inactivité
                        idle_time = (now - self.last_activity).total_seconds() / 60
                        
                        if idle_time >= self.background_learning_config['min_idle_minutes']:
                            # Vérifie le CPU système
                            system_cpu = psutil.cpu_percent(interval=1)
                            
                            if system_cpu < self.background_learning_config['max_cpu_threshold']:
                                # Lance l'apprentissage
                                await self._start_background_learning(duration)
                
                # Attendre avant prochaine vérification
                await asyncio.sleep(60)  # Vérifie chaque minute
            
            except Exception as e:
                print(f"   ⚠️  Erreur planification: {e}")
                await asyncio.sleep(300)
    
    async def _start_background_learning(self, duration_minutes: int = 60):
        """
        Démarre une session d'apprentissage en arrière-plan
        
        Args:
            duration_minutes: Durée de la session
        """
        if self.background_learning_active:
            print("   ℹ️  Apprentissage déjà actif")
            return
        
        print(f"\n🌙 Démarrage apprentissage en arrière-plan ({duration_minutes} min)...")
        
        # Passe en mode BACKGROUND
        old_mode = self.current_mode
        await self.set_mode(PerformanceMode.BACKGROUND, "background_learning")
        
        self.background_learning_active = True
        self.stats['background_sessions'] += 1
        start_time = datetime.now()
        
        try:
            # Durée de la session
            end_time = start_time + timedelta(minutes=duration_minutes)
            
            while datetime.now() < end_time and self.background_learning_active:
                # Vérifie le CPU système
                system_cpu = psutil.cpu_percent(interval=1)
                
                if system_cpu > self.background_learning_config['max_cpu_threshold']:
                    print(f"   ⚠️  CPU système trop élevé ({system_cpu}%), pause...")
                    await asyncio.sleep(60)
                    continue
                
                # Ici : Appelle les systèmes d'apprentissage
                # TODO: Intégrer continuous_learning.background_learning_session()
                # TODO: Intégrer memory_database.consolidate_memories()
                
                print(f"   📚 Apprentissage en cours... (CPU: {system_cpu:.1f}%)")
                
                # Pause entre les cycles d'apprentissage
                await asyncio.sleep(300)  # 5 minutes entre chaque cycle
            
            # Fin de la session
            duration = (datetime.now() - start_time).total_seconds() / 60
            self.stats['total_background_time'] += duration
            
            print(f"\n✅ Session d'apprentissage terminée ({duration:.1f} min)")
        
        except Exception as e:
            print(f"   ❌ Erreur pendant l'apprentissage: {e}")
        
        finally:
            self.background_learning_active = False
            # Retour au mode précédent
            await self.set_mode(old_mode, "end_background_learning")
    
    async def _stop_background_learning(self):
        """Arrête l'apprentissage en arrière-plan"""
        if self.background_learning_active:
            print("\n⏹️  Arrêt de l'apprentissage en arrière-plan...")
            self.background_learning_active = False
    
    def mark_activity(self):
        """Marque une activité utilisateur (réinitialise le timer d'inactivité)"""
        self.last_activity = datetime.now()
    
    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques"""
        return {
            **self.stats,
            'current_mode': self.current_mode.value,
            'background_learning_active': self.background_learning_active,
            'minutes_since_activity': (datetime.now() - self.last_activity).total_seconds() / 60
        }
    
    def get_mode_description(self, mode: PerformanceMode) -> str:
        """Retourne une description d'un mode"""
        descriptions = {
            PerformanceMode.MINIMAL: "Mode minimal (10-20% CPU) - Pour jeux, rendu vidéo, travaux intensifs",
            PerformanceMode.LOW: "Mode léger (20-40% CPU) - Pour travail normal avec Anna en arrière-plan",
            PerformanceMode.MEDIUM: "Mode normal (40-60% CPU) - Équilibre optimal pour conversations régulières",
            PerformanceMode.HIGH: "Mode haute performance (60-80% CPU) - Pour conversations importantes et complexes",
            PerformanceMode.BACKGROUND: "Mode arrière-plan (5-10% CPU) - Apprentissage silencieux"
        }
        return descriptions[mode]
    
    async def shutdown(self):
        """Arrête le gestionnaire de ressources"""
        print("🎮 Arrêt gestionnaire de ressources...")
        self.monitoring_active = False
        
        if self.background_learning_active:
            await self._stop_background_learning()
        
        print("   ✓ Ressources libérées")


# Test
async def test_resource_manager():
    """Teste le gestionnaire de ressources"""
    
    print("🧪 Test du gestionnaire de ressources\n")
    
    manager = ResourceManager()
    await manager.initialize()
    
    # Vérifie les ressources
    print("\n📊 Vérification ressources actuelles...")
    resources = await manager.check_resources()
    print(f"   CPU: {resources['cpu_percent']:.1f}% / {resources['cpu_limit']:.1f}%")
    print(f"   Mémoire: {resources['memory_mb']:.1f} MB / {resources['memory_limit']:.1f} MB")
    print(f"   Threads: {resources['num_threads']}")
    print(f"   Dans les limites: {'✓' if resources['within_limits'] else '✗'}")
    
    # Test changement de mode
    print("\n🎮 Test changement de mode...")
    await manager.set_mode(PerformanceMode.LOW, "test")
    await asyncio.sleep(1)
    
    resources = await manager.check_resources()
    print(f"   CPU: {resources['cpu_percent']:.1f}% / {resources['cpu_limit']:.1f}%")
    
    # Test détection depuis message
    print("\n💬 Test détection depuis message...")
    changed = await manager.request_mode_from_message("Anna, utilise moins de ressources")
    print(f"   Mode changé: {'✓' if changed else '✗'}")
    
    # Statistiques
    print("\n📊 Statistiques:")
    stats = manager.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Description des modes
    print("\n📋 Modes disponibles:")
    for mode in PerformanceMode:
        print(f"\n{mode.value.upper()}:")
        print(f"   {manager.get_mode_description(mode)}")
    
    await manager.shutdown()


if __name__ == "__main__":
    asyncio.run(test_resource_manager())