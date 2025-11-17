

celery_beat-1    | Traceback (most recent call last):
celery_beat-1    |   File "/usr/local/bin/nautobot-server", line 8, in <module>
celery_beat-1    |     sys.exit(main())
celery_beat-1    |              ^^^^^^
celery_beat-1    |   File "/usr/local/lib/python3.12/site-packages/nautobot/core/cli/__init__.py", line 301, in main
celery_beat-1    |     execute_from_command_line([sys.argv[0], *unparsed_args])
celery_beat-1    |   File "/usr/local/lib/python3.12/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
celery_beat-1    |     utility.execute()
celery_beat-1    |   File "/usr/local/lib/python3.12/site-packages/django/core/management/__init__.py", line 416, in execute
celery_beat-1    |     django.setup()
celery_beat-1    |   File "/usr/local/lib/python3.12/site-packages/django/__init__.py", line 24, in setup
celery_beat-1    |     apps.populate(settings.INSTALLED_APPS)
celery_beat-1    |   File "/usr/local/lib/python3.12/site-packages/django/apps/registry.py", line 124, in populate
celery_beat-1    |     app_config.ready()
celery_beat-1    |   File "/usr/local/lib/python3.12/site-packages/nautobot/extras/plugins/__init__.py", line 147, in ready
celery_beat-1    |     jobs = import_object(f"{self.__module__}.{self.jobs}")
celery_beat-1    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery_beat-1    |   File "/usr/local/lib/python3.12/site-packages/nautobot/extras/plugins/utils.py", line 46, in import_object
celery_beat-1    |     spec.loader.exec_module(module)
celery_beat-1    |   File "<frozen importlib._bootstrap_external>", line 999, in exec_module
celery_beat-1    |   File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
celery_beat-1    |   File "/usr/local/lib/python3.12/site-packages/nautobot_ssot_fortimanager/jobs.py", line 11, in <module>
celery_beat-1    |     from nautobot_ssot_fortimanager.diffsync.adapters.fmanager import FortiManagerFWRulesAdapter
celery_beat-1    |   File "/usr/local/lib/python3.12/site-packages/nautobot_ssot_fortimanager/diffsync/adapters/fmanager.py", line 8, in <module>
celery_beat-1    |     from nautobot_ssot_fortimanager.diffsync.models.base import FqdnFWDiffSyncModel, IPAddressDiffSyncModel
celery_beat-1    |   File "/usr/local/lib/python3.12/site-packages/nautobot_ssot_fortimanager/diffsync/models/base.py", line 50, in <module>
celery_beat-1    |     class FqdnFWDiffSyncModel(NautobotModel):
celery_beat-1    |   File "/usr/local/lib/python3.12/site-packages/pydantic/_internal/_model_construction.py", line 251, in __new__
celery_beat-1    |     super(cls, cls).__pydantic_init_subclass__(**kwargs)  # type: ignore[misc]
celery_beat-1    |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery_beat-1    |   File "/usr/local/lib/python3.12/site-packages/diffsync/__init__.py", line 138, in __pydantic_init_subclass__
celery_beat-1    |     raise AttributeError(f"_identifiers {cls._identifiers} references missing or un-annotated attr {attr}")
celery_beat-1    | AttributeError: _identifiers ('name',) references missing or un-annotated attr name
celery_worker-1  | Traceback (most recent call last):
celery_worker-1  |   File "/usr/local/bin/nautobot-server", line 8, in <module>
celery_worker-1  |     sys.exit(main())
celery_worker-1  |              ^^^^^^
celery_worker-1  |   File "/usr/local/lib/python3.12/site-packages/nautobot/core/cli/__init__.py", line 301, in main
celery_worker-1  |     execute_from_command_line([sys.argv[0], *unparsed_args])
celery_worker-1  |   File "/usr/local/lib/python3.12/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
celery_worker-1  |     utility.execute()
celery_worker-1  |   File "/usr/local/lib/python3.12/site-packages/django/core/management/__init__.py", line 416, in execute
celery_worker-1  |     django.setup()
celery_worker-1  |   File "/usr/local/lib/python3.12/site-packages/django/__init__.py", line 24, in setup
celery_worker-1  |     apps.populate(settings.INSTALLED_APPS)
celery_worker-1  |   File "/usr/local/lib/python3.12/site-packages/django/apps/registry.py", line 124, in populate
celery_worker-1  |     app_config.ready()
celery_worker-1  |   File "/usr/local/lib/python3.12/site-packages/nautobot/extras/plugins/__init__.py", line 147, in ready
celery_worker-1  |     jobs = import_object(f"{self.__module__}.{self.jobs}")
celery_worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery_worker-1  |   File "/usr/local/lib/python3.12/site-packages/nautobot/extras/plugins/utils.py", line 46, in import_object
celery_worker-1  |     spec.loader.exec_module(module)
celery_worker-1  |   File "<frozen importlib._bootstrap_external>", line 999, in exec_module
celery_worker-1  |   File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
celery_worker-1  |   File "/usr/local/lib/python3.12/site-packages/nautobot_ssot_fortimanager/jobs.py", line 11, in <module>
celery_worker-1  |     from nautobot_ssot_fortimanager.diffsync.adapters.fmanager import FortiManagerFWRulesAdapter
celery_worker-1  |   File "/usr/local/lib/python3.12/site-packages/nautobot_ssot_fortimanager/diffsync/adapters/fmanager.py", line 8, in <module>
celery_worker-1  |     from nautobot_ssot_fortimanager.diffsync.models.base import FqdnFWDiffSyncModel, IPAddressDiffSyncModel
celery_worker-1  |   File "/usr/local/lib/python3.12/site-packages/nautobot_ssot_fortimanager/diffsync/models/base.py", line 50, in <module>
celery_worker-1  |     class FqdnFWDiffSyncModel(NautobotModel):
celery_worker-1  |   File "/usr/local/lib/python3.12/site-packages/pydantic/_internal/_model_construction.py", line 251, in __new__
celery_worker-1  |     super(cls, cls).__pydantic_init_subclass__(**kwargs)  # type: ignore[misc]
celery_worker-1  |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery_worker-1  |   File "/usr/local/lib/python3.12/site-packages/diffsync/__init__.py", line 138, in __pydantic_init_subclass__
celery_worker-1  |     raise AttributeError(f"_identifiers {cls._identifiers} references missing or un-annotated attr {attr}")
celery_worker-1  | AttributeError: _identifiers ('name',) references missing or un-annotated attr name
celery_beat-1    | 
celery_worker-1  | 
celery_beat-1 exited with code 1
celery_worker-1 exited with code 1