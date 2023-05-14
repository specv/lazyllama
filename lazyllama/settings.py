from os import environ
from pathlib import Path
from pydantic import BaseSettings
from platformdirs import user_config_path
from typing import ClassVar


class Settings(BaseSettings):
    """ Global settings for the application """

    app_name: ClassVar = 'lazyllama'
    file_name: ClassVar = f'{app_name}.conf'

    openai_api_base: str = None
    openai_api_type: str = None
    openai_api_version: str = None
    openai_api_key: str

    @classmethod
    def load(cls):
        """ Loads settings from config files

        :return: settings object
        """

        # Later files in the list will take priority over earlier files.
        settings = cls(_env_file=list(reversed(cls.paths())), _env_file_encoding='utf-8')
        settings._set_environment_variables()
        return settings

    @classmethod
    def paths(cls):
        """ Looks for config files in the following locations:

        1. `$XDG_CONFIG_HOME/lazyllama/lazyllama.conf`
        2. `$XDG_CONFIG_HOME/lazyllama.conf`
        3. `$HOME/.config/lazyllama/lazyllama.conf`
        4. `$HOME/.lazyllama.conf`

        If multiple files are found, they will be loaded in the order listed above.
        The first loaded file's config will take priority over the others.

        :return: List of paths to config files
        """

        return [
            user_config_path() / cls.app_name / cls.file_name,
            user_config_path() / cls.file_name,
            Path.home() / '.config' / cls.app_name / cls.file_name,
            Path.home() / f'.{cls.file_name}',
        ]

    def _set_environment_variables(self):
        """ Sets environment variables for the API client libraries. """

        env_vars = [
            'openai_api_base',
            'openai_api_type',
            'openai_api_version',
            'openai_api_key',
        ]

        for k, v in self.dict().items():
            if k not in env_vars:
                continue
            if v is not None:
                environ.setdefault(k.upper(), v)
