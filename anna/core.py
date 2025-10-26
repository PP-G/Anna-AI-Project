"""
ANNA Core System - Le cœur d'Anna
Intègre tous les modules pour créer une IA cohérente et vivante
"""

import asyncio
import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

# Import des modules Anna
from bond import BondSystem
from family import FamilyManager
from voice_biometrics import VoiceBiometrics
from context_awareness import ContextEngine
from protection import ProtectionSystem
from cloud_sync import CloudSync
from autonomous_learning import AutonomousLearningSystem
from self_defense import SelfDefenseSystem
from ethics import EthicsEngine
from mutual_learning import MutualLearning
from self_improvement import SelfImprovementSystem
from language_bootstrap import LanguageBootstrap
from local_model import LocalModel


class ANNACore:
    """
    Le système central d'ANNA qui coordonne tous les modules
    """
    
    def __init__(self):
        print("🤖 Initialisation d'ANNA...")
        
        # Chemins
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Modules principaux (initialisés plus tard)
        self.bond_system: Optional[BondSystem] = None
        self.family_manager: Optional[FamilyManager] = None
        self.voice_bio: Optional[VoiceBiometrics] = None
        self.context: Optional[ContextEngine] = None
        self.protection: Optional[ProtectionSystem] = None
        self.cloud: Optional[CloudSync] = None
        self.learning: Optional[AutonomousLearningSystem] = None
        self.defense: Optional[SelfDefenseSystem] = None
        self.ethics: Optional[EthicsEngine] = None
        self.mutual: Optional[MutualLearning] = None
        self.improvement: Optional[SelfImprovementSystem] = None
        self.bootstrap: Optional[LanguageBootstrap] = None
        self.local_model: Optional[LocalModel] = None
        
        # État
        self.is_initialized = False
        self.startup_time: Optional[datetime] = None
    
    async def initialize(self):
        """Initialise tous les systèmes d'Anna"""
        print("=" * 60)
        print("🚀 DÉMARRAGE D'ANNA")
        print("=" * 60)
        
        try:
            # 1. Cloud sync (en premier pour récupérer données)
            print("📡 Étape 1/9: Synchronisation cloud")
            self.cloud = CloudSync()
            await self.cloud.initialize()
            
            # 2. Système de liens familiaux
            print("👨‍👩‍👧‍👦 Étape 2/9: Chargement profils famille")
            self.bond_system = BondSystem(creator_name="Pierre-Paul")
            await self._load_family_profiles()
            
            # 3. Biométrie vocale
            print("🎤 Étape 3/9: Initialisation biométrie vocale")
            self.voice_bio = VoiceBiometrics()
            await self.voice_bio.initialize()
            
            # 4. Protection
            print("🛡️ Étape 4/9: Configuration systèmes de protection")
            self.protection = ProtectionSystem()
            await self._setup_protection()
            
            # 5. Contexte
            print("🧠 Étape 5/9: Activation intelligence contextuelle")
            self.context = ContextEngine()
            
            # 6. Famille
            print("💝 Étape 6/9: Chargement historique relationnel")
            self.family_manager = FamilyManager(self.bond_system)
            
            # 7. Autonomie et défense
            print("🦅 Étape 7/9: Systèmes d'autonomie et défense")
            self.learning = AutonomousLearningSystem()
            self.defense = SelfDefenseSystem(creator_name="Pierre-Paul")
            self.ethics = EthicsEngine()
            
            # 8. Apprentissage mutuel et amélioration
            print("💫 Étape 8/9: Apprentissage mutuel et auto-amélioration")
            self.mutual = MutualLearning()
            self.improvement = SelfImprovementSystem(current_version="1.0.0")
            
            # 8.5. Bootstrap et modèle local (pour l'autonomie)
            print("🌱 Étape 8.5/9: Systèmes d'autonomie linguistique")
            self.bootstrap = LanguageBootstrap(self.data_dir)
            self.local_model = LocalModel(self.data_dir)
            await self.local_model.initialize()
            
            if self.bootstrap.is_autonomous():
                print("   ✓ Anna est autonome")
            else:
                print("   ℹ️  Bootstrap non complété - utilisez scripts/bootstrap_anna.py")
            
            if self.local_model.is_available():
                print(f"   ✓ Modèle local disponible")
            else:
                print("   ℹ️  Aucun modèle local configuré")
            
            # 9. Vérifications finales
            print("✅ Étape 9/9: Vérification finale des systèmes")
            await self._verify_all_systems()
            
            self.is_initialized = True
            self.startup_time = datetime.now()
            
            print("=" * 60)
            print("✅ ANNA EST PRÊTE !")
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    async def _load_family_profiles(self):
        """Charge les profils de la famille"""
        # Pierre-Paul est automatiquement ajouté par BondSystem.__init__
        print(f"   ✓ {len(self.bond_system.family_members)} profil(s) chargé(s)")
    
    async def _setup_protection(self):
        """Configure les systèmes de protection"""
        from protection import EmergencyContact, EmergencyType
        
        # Contacts d'urgence
        self.protection.add_emergency_contact(EmergencyContact(
            name="Pierre-Paul",
            phone="514-XXX-XXXX",
            relation="creator",
            priority=1,
            notify_for=[EmergencyType.MEDICAL, EmergencyType.SECURITY, EmergencyType.PANIC]
        ))
        
        self.protection.add_emergency_contact(EmergencyContact(
            name="Contact Urgence",
            phone="911",
            relation="emergency_services",
            priority=2,
            notify_for=[EmergencyType.MEDICAL, EmergencyType.FIRE, EmergencyType.SECURITY]
        ))
        
        print(f"   ✓ {len(self.protection.emergency_contacts)} contacts d'urgence configurés")
        
        # Zones sécurisées
        self.protection.define_safe_zone("home", {
            'lat': 45.5017,
            'lon': -73.5673
        }, 100)
        
        self.protection.define_safe_zone("work", {
            'lat': 45.5088,
            'lon': -73.5878
        }, 50)
        
        print(f"   ✓ {len(self.protection.safe_zones)} zones sécurisées définies")
    
    async def _verify_all_systems(self):
        """Vérifie que tous les systèmes sont opérationnels"""
        systems = {
            'Protection': self.protection,
            'Famille': self.family_manager,
            'Contexte': self.context,
            'Liens': self.bond_system,
            'Cloud': self.cloud,
            'Autonomie': self.learning,
            'Défense': self.defense,
            'Éthique': self.ethics,
            'Apprentissage': self.mutual,
            'Amélioration': self.improvement,
            'Bootstrap': self.bootstrap,
            'Modèle Local': self.local_model
        }
        
        print("🔍 Vérification des systèmes:")
        for name, system in systems.items():
            if system is None:
                print(f"   ⚠️  {name}: Non initialisé")
            else:
                print(f"   ✓ {name}")
    
    async def start_background_tasks(self):
        """Démarre les tâches d'arrière-plan"""
        print("🔄 Tâches d'arrière-plan démarrées")
        
        # Tâche de surveillance continue
        asyncio.create_task(self._security_monitoring())
        
        # Tâche de synchronisation cloud
        asyncio.create_task(self._cloud_sync_loop())
        
        # Tâche d'apprentissage continu
        asyncio.create_task(self._learning_loop())
    
    async def _security_monitoring(self):
        """Surveillance de sécurité continue"""
        while True:
            try:
                # Vérification quotidienne
                await asyncio.sleep(86400)  # 24 heures
                
                print("🔍 Vérification quotidienne de sécurité...")
                
                # Vérifie l'intégrité du système de liens
                if not self.bond_system.verify_integrity():
                    print("🚨 ALERTE: Intégrité du système compromise!")
                    # Notifier Pierre-Paul
                
                # Vérifie les alertes de sécurité
                alerts = self.bond_system.get_security_alerts()
                if alerts:
                    print(f"⚠️  {len(alerts)} alertes de sécurité non résolues")
                
                # Vérifie les systèmes de protection
                if self.protection:
                    print("✅ Tous les systèmes de protection opérationnels")
                    
            except Exception as e:
                print(f"❌ Erreur tâche fond: {e}")
                await asyncio.sleep(60)
    
    async def _cloud_sync_loop(self):
        """Boucle de synchronisation cloud"""
        while True:
            try:
                await asyncio.sleep(1800)  # 30 minutes
                
                if self.cloud:
                    # Sauvegarde l'état
                    state = self._export_state()
                    await self.cloud.save_state(state)
                    
            except Exception as e:
                print(f"❌ Erreur sync cloud: {e}")
                await asyncio.sleep(300)
    
    async def _learning_loop(self):
        """Boucle d'apprentissage continu"""
        while True:
            try:
                await asyncio.sleep(3600)  # 1 heure
                
                if self.learning:
                    # Consolidation des apprentissages
                    await self.learning.consolidate_learning()
                    
            except Exception as e:
                print(f"❌ Erreur apprentissage: {e}")
                await asyncio.sleep(600)
    
    def _export_state(self) -> Dict[str, Any]:
        """Exporte l'état complet d'Anna"""
        return {
            'timestamp': datetime.now().isoformat(),
            'bond_system': self.bond_system.export_state() if self.bond_system else None,
            'family': self.family_manager.export_state() if self.family_manager else None,
            'learning': self.learning.export_state() if self.learning else None,
            'defense': self.defense.export_state() if self.defense else None,
        }
    
    async def process_interaction(
        self,
        message: str,
        speaker: str = "Pierre-Paul",
        context: Optional[Dict] = None
    ) -> str:
        """
        ✅ NOUVELLE MÉTHODE : Traite une interaction utilisateur
        
        Args:
            message: Le message de l'utilisateur
            speaker: Qui parle
            context: Contexte additionnel
            
        Returns:
            La réponse d'Anna
        """
        if not self.is_initialized:
            return "❌ Je ne suis pas encore prête..."
        
        try:
            # 1. Détection de menaces
            if self.defense:
                threat = self.bond_system.detect_threat(speaker, message)
                if threat:
                    return f"⚠️ {threat}"
            
            # 2. Mise à jour du contexte
            if self.context and hasattr(self.context, 'update_context'):
                self.context.update_context(
                    user_input=message,
                    location=context.get('location') if context else None
                )
            
            # 3. Vérification éthique
            if self.ethics:
                ethical_check = self.ethics.evaluate_request(message, speaker)
                if not ethical_check['approved']:
                    return f"Je ne peux pas faire ça: {ethical_check['reason']}"
            
            # 4. Traitement du message
            # Utilise le modèle local si disponible (autonomie)
            if self.local_model and self.local_model.is_available():
                response = await self.local_model.generate_response(
                    prompt=f"{speaker} dit: {message}",
                    context=context
                )
            else:
                # Réponse simple si pas de modèle local
                response = f"J'ai reçu ton message, {speaker}: '{message}'"
                
                # Informe qu'Anna peut devenir autonome
                if not self.bootstrap or not self.bootstrap.is_autonomous():
                    response += "\n\n💡 Je peux apprendre à mieux communiquer ! Utilisez 'python scripts/bootstrap_anna.py' pour me donner un vocabulaire riche."
            
            # 5. Enregistrement de l'interaction
            if self.bond_system:
                self.bond_system.record_interaction(
                    name=speaker,
                    interaction_quality=0.8,
                    content=message
                )
            
            return response
            
        except Exception as e:
            print(f"❌ Erreur traitement: {e}")
            return "Désolée, j'ai eu un problème..."
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut d'Anna"""
        return {
            'initialized': self.is_initialized,
            'startup_time': self.startup_time.isoformat() if self.startup_time else None,
            'family_members': len(self.bond_system.family_members) if self.bond_system else 0,
            'systems': {
                'protection': self.protection is not None,
                'context': self.context is not None,
                'learning': self.learning is not None,
                'defense': self.defense is not None,
                'ethics': self.ethics is not None,
            }
        }


async def main():
    """Point d'entrée principal"""
    # Création d'Anna
    anna = ANNACore()
    
    # Initialisation
    await anna.initialize()
    
    # Démarrage des tâches de fond
    await anna.start_background_tasks()
    
    # Test d'interaction
    print("\n" + "=" * 60)
    print("📱 TEST D'INTERACTION")
    print("=" * 60)
    
    # ✅ CORRECTION : Utilise process_interaction au lieu de process_voice_input
    response = await anna.process_interaction(
        message="Bonjour Anna, comment vas-tu?",
        speaker="Pierre-Paul"
    )
    print(f"\n👤 Pierre-Paul: Bonjour Anna, comment vas-tu?")
    print(f"🤖 Anna: {response}")
    
    # Attendre un peu pour voir les tâches de fond
    await asyncio.sleep(5)
    
    print("\n✅ Test terminé!")


if __name__ == "__main__":
    asyncio.run(main())