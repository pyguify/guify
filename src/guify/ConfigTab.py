import os
import sqlite3

CONFIG_FILE_NAME = 'config.sqlite3'
CONFIG_TABLE_NAME = 'configurations'


class ConfigTab:
    DEFAULT_PATH = os.path.join(os.getcwd(), CONFIG_FILE_NAME)

    def __init__(self, config_path=DEFAULT_PATH) -> None:
        self.config_path = config_path
        self.__init_config__()

    def __init_config__(self) -> None:
        if not os.path.isfile(self.config_path):
            self.__create_config__()

    def __create_config__(self) -> None:
        conn = sqlite3.connect(self.config_path)
        c = conn.cursor()
        c.execute(f'''
            CREATE TABLE {CONFIG_TABLE_NAME} (
                id INTEGER PRIMARY KEY,
                section TEXT,
                key TEXT,
                value TEXT,
                UNIQUE(section, key)
            )
        ''')
        conn.commit()
        c.execute(f'''
            CREATE TRIGGER unique_key_per_section
            BEFORE INSERT ON {CONFIG_TABLE_NAME}
            BEGIN
                SELECT CASE
                    WHEN (
                        SELECT 1
                        FROM {CONFIG_TABLE_NAME} AS c1
                        WHERE c1.section = NEW.section AND c1.key = NEW.key AND c1.value = NEW.value
                        LIMIT 1
                    ) IS NOT NULL
                    THEN RAISE(ABORT, 'Duplicate key for the same section and value.')
                END;
            END
        ''')
        conn.commit()
        c.close()
        conn.close()

    def get(self, section: str, key: str):
        '''
        Get a specific value from the config file.
        :param section: The section of the ini file.
        :param key: The key of the value you want to get.
        :rtype: str
        '''
        conn = sqlite3.connect(self.config_path)
        c = conn.cursor()
        c.execute(
            f'''SELECT value FROM {CONFIG_TABLE_NAME} WHERE section = '{section}' AND key = '{key}' ''')
        value = c.fetchone()
        c.close()
        conn.close()
        return value[0] if value else None

    def get_section(self, section: str):
        '''
        Get the entire section as a dictionary
        :param section: The section of the ini file.
        :rtype: dict
        '''
        conn = sqlite3.connect(self.config_path)
        c = conn.cursor()

        c.execute(
            f'''SELECT key, value FROM {CONFIG_TABLE_NAME} WHERE section = '{section}' ''')
        section = c.fetchall()
        c.close()
        conn.close()
        return dict(section)

    def get_all_sections(self):
        '''
        Get all unique (DISTINCT) sections
        :rtype: list
        '''
        conn = sqlite3.connect(self.config_path)
        c = conn.cursor()
        c.execute(
            f'''SELECT DISTINCT section FROM {CONFIG_TABLE_NAME}''')
        sections = c.fetchall()
        c.close()
        conn.close()
        return [section[0] for section in sections]

    def get_all(self):
        '''
        Get the entire config file as a dictionary
        :rtype: dict
        '''
        conn = sqlite3.connect(self.config_path)
        c = conn.cursor()
        c.execute(
            f'''SELECT section, key, value FROM {CONFIG_TABLE_NAME}''')
        rows = c.fetchall()
        c.close()
        conn.close()
        config = {}
        for section, key, value in rows:
            if section not in config:
                config[section] = {}
            config[section][key] = value
        return dict(config)

    def insert(self, section: str, key: str, value: str):
        '''
        :param section: The section of the ini file.
        :param key: The key of the value you want to set.
        :param value: The value you want to set.
        :rtype: None
        '''
        conn = sqlite3.connect(self.config_path)
        c = conn.cursor()

        try:
            c.execute(
                f'''INSERT INTO {CONFIG_TABLE_NAME} VALUES (NULL, '{section}', '{key}', '{value}') ''')
        except sqlite3.IntegrityError:
            pass
        conn.commit()
        c.close()
        conn.close()

    def update_value(self, section: str, key, value):
        '''
        :param section: The section of the ini file.
        :param key: The key of the value you want to set.
        :param value: The value you want to set.
        :rtype: None
        '''
        conn = sqlite3.connect(self.config_path)
        c = conn.cursor()

        c.execute(
            f'''UPDATE {CONFIG_TABLE_NAME} SET value = '{value}' WHERE section = '{section}' AND key = '{key}' ''')
        conn.commit()
        c.close()
        conn.close()

    def update_section_name(self, oldName: str, newName: str):
        '''
        :param section: The section of the ini file.
        :param section_dict: The dictionary to parse.
        :rtype: None
        '''
        all_sections = self.get_all_sections()
        if oldName not in all_sections:
            return False, f'Section {oldName} does not exist.'

        if oldName == newName:
            return True, f"Section name is the same as the old name"

        if newName in all_sections:
            return False, f'Section {newName} already exists.'

        conn = sqlite3.connect(self.config_path)
        c = conn.cursor()
        try:
            c.execute(
                f'''UPDATE {CONFIG_TABLE_NAME} SET section = '{newName}' WHERE section = '{oldName}' ''')
        except sqlite3.IntegrityError as e:
            retval = False, f'Error: {e.sqlite_errorname}'
        else:
            retval = True, f'Section {oldName} updated to {newName}.'
        finally:
            conn.commit()
            c.close()
            conn.close()
            return retval

    def update_key(self, section: str, key: str, new_key: str):
        '''
        :param section: The section of the ini file.
        :param key: The key of the value you want to set.
        :param new_key: The new key of the value you want to set.
        :rtype: None
        '''
        section_dict = self.get_section(section)
        if key not in section_dict.keys():
            return False, f'Key "{key}" does not exist in section "{section}".'
        if new_key == key:
            return True, f"Key is the same as the old key"
        if new_key in section_dict.keys():
            return False, f'Key "{new_key}" already exists in section "{section}".'
        conn = sqlite3.connect(self.config_path)
        c = conn.cursor()
        try:
            c.execute(
                f'''UPDATE {CONFIG_TABLE_NAME} SET key = '{new_key}' WHERE section = '{section}' AND key = '{key}' ''')
        except sqlite3.IntegrityError:
            retval = False, f'Key "{new_key}" already exists in section "{section}".'
        else:
            retval = True, f'Key "{key}" updated to "{new_key}".'

        finally:
            conn.commit()
            c.close()
            conn.close()
            return retval

    def delete(self, section: str, key: str):
        '''
        :param section: The section of the ini file.
        :param key: The key of the value you want to set.
        :rtype: None
        '''
        conn = sqlite3.connect(self.config_path)
        c = conn.cursor()

        c.execute(
            f'''DELETE FROM {CONFIG_TABLE_NAME} WHERE section = '{section}' AND key = '{key}' ''')
        conn.commit()
        c.close()
        conn.close()

    def delete_section(self, section: str):
        '''
        :param section: The section of the ini file.
        :rtype: None
        '''
        all_section = self.get_all_sections()
        if section not in all_section:
            return False, f'Section {section} does not exist.'

        conn = sqlite3.connect(self.config_path)
        c = conn.cursor()
        try:
            c.execute(
                f'''DELETE FROM {CONFIG_TABLE_NAME} WHERE section = '{section}' ''')
        except sqlite3.IntegrityError as e:
            retval = False, f'Error: {e.sqlite_errorname}'
        else:
            retval = True, f'Section {section} deleted.'
        finally:
            conn.commit()
            c.close()
            conn.close()
            return retval
