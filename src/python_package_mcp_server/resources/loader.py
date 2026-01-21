"""Resource loader for file-based resource management."""

import importlib
import re
from pathlib import Path
from typing import Any, Callable

import yaml
from mcp.types import Resource, ResourceTemplate

import structlog

logger = structlog.get_logger(__name__)


class ResourceFile:
    """Represents a resource loaded from a file."""

    def __init__(
        self,
        uri: str,
        name: str,
        description: str,
        mime_type: str,
        handler_module: str,
        handler_function: str,
        category: str = "general",
        uri_template: str | None = None,
    ):
        """Initialize resource file.

        Args:
            uri: Resource URI
            name: Resource name
            description: Resource description
            mime_type: MIME type
            handler_module: Python module path for handler (e.g., "resources.packages")
            handler_function: Function name in handler module
            category: Resource category
            uri_template: URI template for resource templates (optional)
        """
        self.uri = uri
        self.name = name
        self.description = description
        self.mime_type = mime_type
        self.handler_module = handler_module
        self.handler_function = handler_function
        self.category = category
        self.uri_template = uri_template or uri
        self._handler: Callable[[str, dict[str, Any] | None], str] | None = None

    def to_resource(self) -> Resource:
        """Convert to MCP Resource object."""
        return Resource(
            uri=self.uri,
            name=self.name,
            description=self.description,
            mimeType=self.mime_type,
        )

    def to_resource_template(self) -> ResourceTemplate:
        """Convert to MCP ResourceTemplate object."""
        return ResourceTemplate(
            uriTemplate=self.uri_template,
            name=self.name,
            description=self.description,
        )

    def get_handler(self) -> Callable[[str, dict[str, Any] | None], str]:
        """Get or load the handler function.

        Returns:
            Handler function

        Raises:
            ImportError: If handler module/function cannot be imported
        """
        if self._handler is None:
            try:
                module = importlib.import_module(self.handler_module)
                self._handler = getattr(module, self.handler_function)
            except (ImportError, AttributeError) as e:
                logger.error(
                    "failed_to_load_handler",
                    module=self.handler_module,
                    function=self.handler_function,
                    error=str(e),
                )
                raise ImportError(
                    f"Cannot load handler {self.handler_module}.{self.handler_function}: {e}"
                )
        return self._handler

    def read(self, uri: str, params: dict[str, Any] | None = None) -> str:
        """Read resource content using handler.

        Args:
            uri: Resource URI (may differ from self.uri for template-based resources)
            params: Optional parameters for resource reading

        Returns:
            Resource content as string
        """
        handler = self.get_handler()
        # Handler signature varies:
        # - handler(uri: str) -> str
        # - handler(uri: str, params: dict | None) -> str
        # Try with params first, fallback to uri-only
        import inspect
        sig = inspect.signature(handler)
        param_count = len(sig.parameters)
        
        if param_count >= 2:
            # Handler accepts params
            return handler(uri, params)
        else:
            # Handler only accepts uri
            return handler(uri)


class ResourceLoader:
    """Loads resources from YAML files."""

    def __init__(self, resources_dir: Path | None = None):
        """Initialize resource loader.

        Args:
            resources_dir: Directory containing resource files (default: resources/ relative to this file)
        """
        if resources_dir is None:
            resources_dir = Path(__file__).parent
        
        self.resources_dir = Path(resources_dir)
        self._resources: dict[str, ResourceFile] = {}
        self._load_resources()

    def _load_resources(self) -> None:
        """Load all resources from files."""
        if not self.resources_dir.exists():
            logger.warning("resources_directory_not_found", path=str(self.resources_dir))
            return

        # Load from subdirectories: python, project, codebase, dart, typescript
        categories = ["python", "project", "codebase", "dart", "typescript"]
        
        for category in categories:
            category_dir = self.resources_dir / category
            if not category_dir.exists():
                continue
            
            for yaml_file in category_dir.glob("*.yaml"):
                try:
                    resource = self._load_resource_file(yaml_file, category)
                    if resource:
                        self._resources[resource.uri] = resource
                        logger.debug("resource_loaded", uri=resource.uri, category=category)
                except Exception as e:
                    logger.error("failed_to_load_resource", file=str(yaml_file), error=str(e))

    def _load_resource_file(self, file_path: Path, category: str) -> ResourceFile | None:
        """Load a single resource file.

        Args:
            file_path: Path to .yaml file
            category: Resource category

        Returns:
            ResourceFile object or None if failed
        """
        content = file_path.read_text(encoding="utf-8")
        
        try:
            metadata = yaml.safe_load(content)
        except Exception as e:
            logger.error("failed_to_parse_yaml", file=str(file_path), error=str(e))
            return None
        
        if not metadata:
            logger.warning("empty_yaml", file=str(file_path))
            return None
        
        # Extract metadata
        uri = metadata.get("uri")
        if not uri:
            logger.warning("no_uri", file=str(file_path))
            return None
        
        name = metadata.get("name") or file_path.stem
        description = metadata.get("description", "")
        mime_type = metadata.get("mimeType", "application/json")
        handler_module = metadata.get("handler", {}).get("module")
        handler_function = metadata.get("handler", {}).get("function")
        uri_template = metadata.get("uriTemplate")
        
        if not handler_module or not handler_function:
            logger.warning("no_handler", file=str(file_path))
            return None
        
        return ResourceFile(
            uri=uri,
            name=name,
            description=description,
            mime_type=mime_type,
            handler_module=handler_module,
            handler_function=handler_function,
            category=category,
            uri_template=uri_template,
        )

    def list_resources(self) -> list[Resource]:
        """List all loaded resources.

        Returns:
            List of Resource objects
        """
        return [resource.to_resource() for resource in self._resources.values()]

    def list_resource_templates(self) -> list[ResourceTemplate]:
        """List all resource templates.

        Returns:
            List of ResourceTemplate objects
        """
        return [resource.to_resource_template() for resource in self._resources.values()]

    def read_resource(self, uri: str, params: dict[str, Any] | None = None) -> str:
        """Read a resource by URI.

        Args:
            uri: Resource URI
            params: Optional parameters

        Returns:
            Resource content as string

        Raises:
            ValueError: If resource not found
        """
        uri_str = str(uri)
        uri_base = uri_str.split("?")[0]  # Remove query params for matching
        
        # Try exact match first
        if uri_str in self._resources:
            return self._resources[uri_str].read(uri_str, params)
        
        # Try base URI match (without query params)
        if uri_base in self._resources:
            return self._resources[uri_base].read(uri_str, params)
        
        # Try prefix match for dynamic resources (e.g., codebase://file?path=...)
        for resource_uri, resource in self._resources.items():
            resource_base = resource_uri.split("?")[0]
            if uri_base.startswith(resource_base) or resource_base.startswith(uri_base):
                return resource.read(uri_str, params)
        
        raise ValueError(f"Unknown resource URI: {uri_str}")

    def reload(self) -> None:
        """Reload all resources from files."""
        self._resources.clear()
        self._load_resources()
        logger.info("resources_reloaded", count=len(self._resources))


# Global resource loader instance
_resource_loader: ResourceLoader | None = None


def get_resource_loader() -> ResourceLoader:
    """Get or create the global resource loader instance.

    Returns:
        ResourceLoader instance
    """
    global _resource_loader
    if _resource_loader is None:
        _resource_loader = ResourceLoader()
    return _resource_loader
