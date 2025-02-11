"""
osint_url_extractor.py

An OSINT plugin for ChitraGupt that extracts URLs from a text file.
This plugin registers a command 'extract-urls' which accepts a single parameter 'filename'
of type DataType.STRING. The command opens the file, reads its contents, extracts all URLs
using a regular expression, and logs the extracted URLs via the framework's logger.
"""

import re
import typing

import chitragupt.core.plugin as plugin_mod
import chitragupt.abc.generic as abc_generic

# Create the plugin instance.
osint_url_extractor: plugin_mod.ChitraguptPlugin = plugin_mod.ChitraguptPlugin(
    name="osint_url_extractor",
    description="Extracts URLs from a text file for OSINT purposes."
)

@osint_url_extractor.register(
    command_name="extract-urls",
    filename=plugin_mod.DataType.STRING  # Use the DataType enum member.
)
def extract_urls_command(
    framework: typing.Any,
    cmd_str: str,
    filename: str,
) -> None:
    """
    Extract URLs from a text file.

    Opens the specified text file, reads its content, extracts all URLs using a regular
    expression, and logs the list of extracted URLs via the framework's logger.

    Parameters
    ----------
    framework : Any
        The CLI framework instance.
    cmd_str : str
        The original command string that invoked this command.
    filename : str
        The path to the text file from which URLs should be extracted.

    Returns
    -------
    None

    Raises
    ------
    Exception
        If the file cannot be read or URL extraction fails.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()
        # Regular expression pattern to extract URLs (starting with http:// or https://)
        pattern = r"https?://[^\s]+"
        urls = re.findall(pattern, text)
        if urls:
            framework.logger.log(
                message=f"Extracted URLs from '{filename}': {urls}",
                log_type=plugin_mod.LogType.INFO,
            )
        else:
            framework.logger.log(
                message=f"No URLs found in '{filename}'.",
                log_type=plugin_mod.LogType.INFO,
            )
    except Exception as e:
        framework.logger.log(
            message=f"Error extracting URLs from '{filename}': {e}",
            log_type=plugin_mod.LogType.ERROR,
        )

def load(framework: typing.Any, cmd_str: str) -> None:
    """
    Load the osint_url_extractor plugin into the framework.

    Registers the osint_url_extractor plugin with the framework.

    Parameters
    ----------
    framework : Any
        The CLI framework instance.
    cmd_str : str
        The command string that triggered the plugin load (unused).

    Returns
    -------
    None
    """
    framework.add_plugin(osint_url_extractor)
