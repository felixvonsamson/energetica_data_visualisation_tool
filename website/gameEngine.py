from sqlalchemy import create_engine, MetaData, func
import os
import re
from datetime import datetime


# This is the engine object
class gameEngine(object):
    def __init__(engine):
        engine.current_player_id = 1
        engine.current_network_id = 1
        engine.instance_name = "instance_2024-05-12_1200"
        curent_date = datetime.strptime(engine.instance_name.replace("instance_", ""), "%Y-%m-%d_%H%M")
        engine.start_date = datetime(2024, 4, 19, 10, 38, 45, 342892)
        engine.current_t = (curent_date-engine.start_date).total_seconds() // 30
        engine.db = create_engine(
            f"sqlite:///instances/{engine.instance_name}/instance/database.db"
        )
        engine.metadata = MetaData()
        engine.metadata.reflect(bind=engine.db)

        engine.power_facilities = [
            "steam_engine",
            "windmill",
            "watermill",
            "coal_burner",
            "oil_burner",
            "gas_burner",
            "small_water_dam",
            "onshore_wind_turbine",
            "combined_cycle",
            "nuclear_reactor",
            "large_water_dam",
            "CSP_solar",
            "PV_solar",
            "offshore_wind_turbine",
            "nuclear_reactor_gen4",
        ]

        engine.extraction_facilities = [
            "coal_mine",
            "oil_field",
            "gas_drilling_site",
            "uranium_mine",
        ]

        engine.storage_facilities = [
            "small_pumped_hydro",
            "compressed_air",
            "molten_salt",
            "large_pumped_hydro",
            "hydrogen_storage",
            "lithium_ion_batteries",
            "solid_state_batteries",
        ]

        engine.controllable_facilities = [
            "steam_engine",
            "nuclear_reactor",
            "nuclear_reactor_gen4",
            "combined_cycle",
            "gas_burner",
            "oil_burner",
            "coal_burner",
        ]

        engine.renewables = [
            "small_water_dam",
            "large_water_dam",
            "watermill",
            "onshore_wind_turbine",
            "offshore_wind_turbine",
            "windmill",
            "CSP_solar",
            "PV_solar",
        ]

        engine.functional_facilities = [
            "laboratory",
            "warehouse",
            "industry",
            "carbon_capture",
        ]

        engine.technologies = [
            "mathematics",
            "mechanical_engineering",
            "thermodynamics",
            "physics",
            "building_technology",
            "mineral_extraction",
            "transport_technology",
            "materials",
            "civil_engineering",
            "aerodynamics",
            "chemistry",
            "nuclear_engineering",
        ]

    def player_list(self):
        player_table = self.metadata.tables["player"]
        player_list = []
        with self.db.connect() as connection:
            result = connection.execute(
                player_table.select().order_by(
                    func.lower(player_table.c.username)
                )
            )
            for row in result:
                player_list.append({"id": row[0], "username": row[1]})
            result.close()
        return player_list

    def network_list(self):
        network_table = self.metadata.tables["network"]
        network_list = []
        with self.db.connect() as connection:
            result = connection.execute(
                network_table.select().order_by(
                    func.lower(network_table.c.name)
                )
            )
            for row in result:
                network_list.append({"id": row[0], "name": row[1]})
            result.close()
        return network_list

    def network_members(self):
        player_table = self.metadata.tables["player"]
        network_members = []
        with self.db.connect() as connection:
            result = connection.execute(
                player_table.select()
                .where(player_table.c.network_id == self.current_network_id)
                .order_by(func.lower(player_table.c.username))
            )
            for row in result:
                network_members.append(row[1])
            result.close()
        return network_members

    def date_list(self):
        def parse_instance_name(instance_name):
            split_str = instance_name.split("_")
            date_str = split_str[1] + "_" + split_str[2]
            date_obj = datetime.strptime(date_str, "%Y-%m-%d_%H%M")
            formatted_date = date_obj.strftime("%B %d, %H:%M")
            return formatted_date

        date_list = []
        for instance_name in sorted(os.listdir("instances")):
            if os.path.isdir(os.path.join("instances", instance_name)):
                date_list.append(
                    {
                        "id": instance_name,
                        "date": parse_instance_name(instance_name),
                    }
                )
        return date_list

    def switch_database(
        self, new_instance=None, new_player_id=None, new_network_id=None
    ):
        if new_player_id is not None:
            self.current_player_id = new_player_id
        if new_network_id is not None:
            self.current_network_id = new_network_id
        if new_instance is not None:
            self.instance_name = new_instance
            self.db = create_engine(
                f"sqlite:///instances/{self.instance_name}/instance/database.db"
            )
            self.metadata.reflect(bind=self.db)
            curent_date = datetime.strptime(self.instance_name.replace("instance_", ""), "%Y-%m-%d_%H%M")
            self.current_t = (curent_date-self.start_date).total_seconds() // 30
