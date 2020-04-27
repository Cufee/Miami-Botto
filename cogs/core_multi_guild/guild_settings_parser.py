import rapidjson
import os
from datetime import datetime


class GetSettings():
    def __init__(self):
        pass

    async def parse(self, guild):
        self.guild = guild
        # Open settings with read
        with open(f'{os.path.dirname(os.path.realpath(__file__))}/cache/guild_settings.json') as settings_json:
            all_settings = rapidjson.load(settings_json)
        # Get settings by guild ID key
        guild_settings = all_settings.get(str(guild.id))
        # If guild not in settings, add guild to settings with default parameters
        if not guild_settings:
            new_guild_settings = await self.add_guild()
            guild_settings = new_guild_settings.get(str(guild.id))
        return guild_settings

    async def add_guild(self):
        # Open guild settings
        with open(f'{os.path.dirname(os.path.realpath(__file__))}/cache/guild_settings.json') as settings_json:
            all_settings = rapidjson.load(settings_json)
        # Make a copy of default settings
        new_guild_settings = all_settings.get('default').copy()
        # Adjust the name and date_joined
        new_guild_settings.update({"name": self.guild.name, "information": {
                                  "date_joined": datetime.now().strftime("%D at %H:%M")}})
        # Add new guild to settings
        all_settings.update(
            {str(self.guild.id): new_guild_settings})
        # Write to file
        with open(f'{os.path.dirname(os.path.realpath(__file__))}/cache/guild_settings.json', 'w') as settings_json:
            rapidjson.dump(all_settings, settings_json, indent=4)
        return all_settings

    async def update_feature(self, guild, feature, key, value=None):
        # Open guild settings
        with open(f'{os.path.dirname(os.path.realpath(__file__))}/cache/guild_settings.json') as settings_json:
            all_settings = rapidjson.load(settings_json)

        # Get value of feature flag
        guild_feature_flag = all_settings.get(
            str(guild.id)).get('feature_flags').get(feature)
        if guild_feature_flag == None:
            return guild_feature_flag
        guild_feature_flag_value = guild_feature_flag.get(key)

        # If feature flag is bool, flip it
        if isinstance(guild_feature_flag_value, bool) and value is None:
            guild_feature_flag_value = not guild_feature_flag_value
            all_settings.get(
                str(guild.id)).get('feature_flags').get(feature).update({key: guild_feature_flag_value})
            # Save to file
            with open(f'{os.path.dirname(os.path.realpath(__file__))}/cache/guild_settings.json', 'w') as settings_json:
                rapidjson.dump(all_settings, settings_json, indent=4)
            return guild_feature_flag_value

        # If feature flag is not boo, return None
        if not isinstance(guild_feature_flag, bool) and value is not None:
            guild_feature_flag_value = value
            all_settings.get(
                str(guild.id)).get('feature_flags').get(feature).update({key: guild_feature_flag_value})
            # Save to file
            with open(f'{os.path.dirname(os.path.realpath(__file__))}/cache/guild_settings.json', 'w') as settings_json:
                rapidjson.dump(all_settings, settings_json, indent=4)
            return guild_feature_flag_value

        else:
            # Handling any other errors
            print(f'Error {feature} flag returned {guild_feature_flag}')
