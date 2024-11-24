from dataclasses import dataclass
from typing import List, Dict, Callable, Optional
from datetime import datetime
from ..device import Device, Battery, SolarPanel, DeviceStatus

class EnergyDistribution:
    """Class to handle energy distribution priorities and neighbor interactions"""
    def __init__(self):
        self.neighbor_sharing_enabled = False
        self.grid_connection_enabled = True
        self.neighbor_energy_provided = 0
        self.grid_energy_provided = 0
        self.energy_shared_to_neighbors = 0
        self.energy_exported_to_grid = 0
        
    def share_to_neighbor(self, available_energy: float) -> float:
        """Share surplus energy with neighbors"""
        if not self.neighbor_sharing_enabled:
            return 0
        # Simulate neighbor capacity (could be replaced with actual neighbor system integration)
        max_neighbor_capacity = 5.0  # kWh
        shared_energy = min(available_energy, max_neighbor_capacity)
        self.energy_shared_to_neighbors += shared_energy
        return shared_energy

    def export_to_grid(self, available_energy: float) -> float:
        """Export surplus energy to grid"""
        if not self.grid_connection_enabled:
            return 0
        self.energy_exported_to_grid += available_energy
        return available_energy

class EnergyManagementSystem:
    def __init__(self, 
                 devices: List[Device],
                 stationary_battery: Battery,
                 ev_battery: Optional[Battery],
                 solar_panel: SolarPanel):
        self.devices = devices
        self.stationary_battery = stationary_battery
        self.ev_battery = ev_battery
        self.solar_panel = solar_panel
        self.energy_history: List[Dict] = []
        self.v2h_controller = V2HController()
        self.v2h_enabled = False
        self.energy_distributor = EnergyDistribution()
        
    # ... (previous methods remain the same until manage_energy)

    def manage_energy(self, 
                     duration_hours: float,
                     weather_data: Dict,
                     request_energy_from_neighbor: Optional[Callable] = None) -> Dict:
        """
        Enhanced energy management with strict priority rules for surplus and deficit scenarios.
        Priority for surplus: VE -> Stationary Battery -> Dynamic Charging -> Neighbors -> Grid
        Priority for deficit: Stationary Battery -> V2H -> Neighbors -> Grid
        """
        produced_energy = self.calculate_produced_energy(duration_hours)
        consumed_energy = self.calculate_consumed_energy(duration_hours)
        energy_balance = produced_energy - consumed_energy
        actions_taken = []
        
        if energy_balance > 0:  # Surplus energy handling
            surplus = energy_balance
            
            # 1. Priority: Charge Electric Vehicle (VE)
            if self.ev_battery and self.ev_battery.current_charge / self.ev_battery.capacity < 0.8:
                charged = self.charge_battery(self.ev_battery, surplus)
                if charged > 0:
                    surplus -= charged
                    actions_taken.append({
                        'action': 'charge_ev',
                        'amount': charged,
                        'priority': 1,
                        'message': f"Charged EV with {charged:.2f} kWh"
                    })
            
            # 2. Priority: Charge Stationary Battery
            if surplus > 0 and self.stationary_battery.current_charge / self.stationary_battery.capacity < 0.8:
                charged = self.charge_battery(self.stationary_battery, surplus)
                if charged > 0:
                    surplus -= charged
                    actions_taken.append({
                        'action': 'charge_stationary',
                        'amount': charged,
                        'priority': 2,
                        'message': f"Charged stationary battery with {charged:.2f} kWh"
                    })
            
            # 3. Priority: Dynamic Charging (if implemented)
            if surplus > 0 and hasattr(self, 'dynamic_charging_available'):
                # Implementation for dynamic charging would go here
                pass
            
            # 4. Priority: Share with Neighbors
            if surplus > 0:
                shared = self.energy_distributor.share_to_neighbor(surplus)
                if shared > 0:
                    surplus -= shared
                    actions_taken.append({
                        'action': 'share_neighbors',
                        'amount': shared,
                        'priority': 4,
                        'message': f"Shared {shared:.2f} kWh with neighbors"
                    })
            
            # 5. Priority: Export to Grid
            if surplus > 0:
                exported = self.energy_distributor.export_to_grid(surplus)
                actions_taken.append({
                    'action': 'export_grid',
                    'amount': exported,
                    'priority': 5,
                    'message': f"Exported {exported:.2f} kWh to grid"
                })
        
        else:  # Deficit energy handling
            deficit = abs(energy_balance)
            
            # 1. Priority: Discharge Stationary Battery
            if self.stationary_battery.current_charge / self.stationary_battery.capacity > 0.2:
                discharged = self.discharge_battery(self.stationary_battery, deficit)
                if discharged > 0:
                    deficit -= discharged
                    actions_taken.append({
                        'action': 'discharge_stationary',
                        'amount': discharged,
                        'priority': 1,
                        'message': f"Discharged stationary battery providing {discharged:.2f} kWh"
                    })
            
            # 2. Priority: Use V2H (Vehicle-to-Home)
            if deficit > 0 and self.v2h_enabled and self.ev_battery:
                if self.v2h_controller.check_safety_conditions(self.ev_battery):
                    discharged = self.discharge_battery(self.ev_battery, deficit, is_ev=True)
                    if discharged > 0:
                        deficit -= discharged
                        actions_taken.append({
                            'action': 'v2h',
                            'amount': discharged,
                            'priority': 2,
                            'message': f"V2H provided {discharged:.2f} kWh"
                        })
            
            # 3. Priority: Borrow from Neighbors
            if deficit > 0 and request_energy_from_neighbor:
                borrowed = request_energy_from_neighbor(deficit)
                if borrowed > 0:
                    deficit -= borrowed
                    actions_taken.append({
                        'action': 'borrow_neighbors',
                        'amount': borrowed,
                        'priority': 3,
                        'message': f"Borrowed {borrowed:.2f} kWh from neighbors"
                    })
            
            # 4. Priority: Draw from Grid
            if deficit > 0:
                actions_taken.append({
                    'action': 'grid_supply',
                    'amount': deficit,
                    'priority': 4,
                    'message': f"Drew {deficit:.2f} kWh from grid"
                })
        
        # Record management history with priority information
        management_record = {
            'timestamp': datetime.utcnow(),
            'produced_energy': produced_energy,
            'consumed_energy': consumed_energy,
            'energy_balance': energy_balance,
            'battery_soc': self.stationary_battery.current_charge / self.stationary_battery.capacity * 100,
            'ev_battery_soc': self.ev_battery.current_charge / self.ev_battery.capacity * 100 if self.ev_battery else None,
            'v2h_status': self.get_v2h_status(),
            'actions': actions_taken,
            'neighbor_energy_shared': self.energy_distributor.energy_shared_to_neighbors,
            'grid_energy_exported': self.energy_distributor.energy_exported_to_grid
        }
        self.energy_history.append(management_record)
        
        return management_record

    def get_priority_stats(self) -> Dict:
        """Get statistics about energy distribution priorities"""
        return {
            'surplus_distribution': {
                'ev_charging_total': sum(action['amount'] for record in self.energy_history 
                                       for action in record['actions'] if action['action'] == 'charge_ev'),
                'stationary_charging_total': sum(action['amount'] for record in self.energy_history 
                                               for action in record['actions'] if action['action'] == 'charge_stationary'),
                'neighbor_sharing_total': self.energy_distributor.energy_shared_to_neighbors,
                'grid_export_total': self.energy_distributor.energy_exported_to_grid
            },
            'deficit_handling': {
                'stationary_discharge_total': sum(action['amount'] for record in self.energy_history 
                                                for action in record['actions'] if action['action'] == 'discharge_stationary'),
                'v2h_total': sum(action['amount'] for record in self.energy_history 
                                for action in record['actions'] if action['action'] == 'v2h'),
                'neighbor_borrowed_total': sum(action['amount'] for record in self.energy_history 
                                             for action in record['actions'] if action['action'] == 'borrow_neighbors'),
                'grid_supply_total': sum(action['amount'] for record in self.energy_history 
                                       for action in record['actions'] if action['action'] == 'grid_supply')
            }
        }
    