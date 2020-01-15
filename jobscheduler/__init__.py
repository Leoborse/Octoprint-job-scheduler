# coding=utf-8

# https://codeload.github.com/Leoborse/Octoprint-job-scheduler/zip/master

from __future__ import absolute_import
import octoprint.plugin

class JobSchedulerPlugin(
        octoprint.plugin.StartupPlugin,
        octoprint.plugin.TemplatePlugin,
        octoprint.plugin.SettingsPlugin):
    def on_after_startup(self):
        self._logger.info("Job Scheduler! (more: %s)" % self._settings.get(["url"]))

    def get_settings_defaults(self):
        return dict(
            pluginenabled=true,
            startenabled=true,
            starttime=7,
            pauseenabled=true,
            pauseday=8,
            pausenight=21,
            telegramenabled=true,
            telegramtoken='aaa:bbbbbbbbb....',
            telegramchatid=123456789
        )

    def get_template_configs(self):
		return [
			dict(type="navbar", custom_bindings=False),
			dict(type="settings", custom_bindings=False)
		]

def get_implementation_class():
	return JobSchedulerPlugin()

__plugin_name__ = "A Job Scheduler"
__plugin_implementation__ = get_implementation_class()
__plugin_hooks__ = {}
#	"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
#	"octoprint.server.http.routes": __plugin_implementation__.route_hook
