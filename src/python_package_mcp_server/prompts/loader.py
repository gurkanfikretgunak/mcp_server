"""Prompt loader for file-based prompt management."""

import re
from pathlib import Path
from typing import Any

import yaml
from mcp.types import Prompt, PromptArgument, PromptMessage, TextContent, GetPromptResult

import structlog

logger = structlog.get_logger(__name__)


class PromptFile:
    """Represents a prompt loaded from a file."""

    def __init__(
        self,
        name: str,
        description: str,
        arguments: list[dict[str, Any]],
        template: str,
        category: str = "general",
    ):
        """Initialize prompt file.

        Args:
            name: Prompt name
            description: Prompt description
            arguments: List of argument definitions
            template: Prompt template text (supports {argument_name} placeholders)
            category: Prompt category (general, dart, typescript)
        """
        self.name = name
        self.description = description
        self.arguments = arguments
        self.template = template
        self.category = category

    def to_prompt(self) -> Prompt:
        """Convert to MCP Prompt object."""
        return Prompt(
            name=self.name,
            description=self.description,
            arguments=[
                PromptArgument(
                    name=arg["name"],
                    description=arg.get("description", ""),
                    required=arg.get("required", False),
                )
                for arg in self.arguments
            ],
        )

    def render(self, arguments: dict[str, str] | None = None) -> GetPromptResult:
        """Render prompt template with arguments.

        Args:
            arguments: Dictionary of argument values

        Returns:
            GetPromptResult with rendered prompt
        """
        arguments = arguments or {}
        
        # Start with template
        prompt_text = self.template
        
        # First, replace placeholders with argument values or defaults
        # Build a dict of all values (arguments + defaults)
        all_values = {}
        
        # Add provided arguments
        all_values.update(arguments)
        
        # Add defaults from argument definitions
        for arg_def in self.arguments:
            arg_name = arg_def["name"]
            if arg_name not in all_values and "default" in arg_def:
                all_values[arg_name] = arg_def["default"]
        
        # Replace all placeholders (but not conditional syntax)
        # Protect conditional syntax first
        protected_conditionals = []
        conditional_pattern = r"(\{if\s+\w+\}.*?\{endif\})"
        
        def protect_conditional(match):
            idx = len(protected_conditionals)
            protected_conditionals.append(match.group(1))
            return f"__COND_{idx}__"
        
        # Protect conditionals
        protected_text = re.sub(conditional_pattern, protect_conditional, prompt_text, flags=re.DOTALL)
        
        # Replace placeholders
        for arg_name, arg_value in all_values.items():
            placeholder = f"{{{arg_name}}}"
            protected_text = protected_text.replace(placeholder, str(arg_value))
        
        # Restore conditionals
        for idx, conditional in enumerate(protected_conditionals):
            protected_text = protected_text.replace(f"__COND_{idx}__", conditional)
        
        prompt_text = protected_text
        
        # Now process conditionals
        def process_conditionals(text):
            """Process conditional blocks recursively."""
            pattern = r"\{if\s+(\w+)\}(.*?)(?:\{else\}(.*?))?\{endif\}"
            
            def replace_match(match):
                arg_name = match.group(1)
                if_content = match.group(2) or ""
                else_content = match.group(3) or ""
                
                # Check if argument exists and has a truthy value
                if arg_name in all_values and all_values[arg_name]:
                    return process_conditionals(if_content)
                elif else_content:
                    return process_conditionals(else_content)
                return ""
            
            # Process multiple times for nested conditionals
            max_iterations = 10
            for _ in range(max_iterations):
                new_text = re.sub(pattern, replace_match, text, flags=re.DOTALL)
                if new_text == text:
                    break
                text = new_text
            return text
        
        prompt_text = process_conditionals(prompt_text)
        
        # Clean up extra blank lines
        prompt_text = re.sub(r"\n{3,}", "\n\n", prompt_text)
        prompt_text = prompt_text.strip()
        
        return GetPromptResult(
            description=self.description,
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=prompt_text),
                ),
            ],
        )


class PromptLoader:
    """Loads prompts from markdown files."""

    def __init__(self, prompts_dir: Path | None = None):
        """Initialize prompt loader.

        Args:
            prompts_dir: Directory containing prompt files (default: prompts/ relative to this file)
        """
        if prompts_dir is None:
            prompts_dir = Path(__file__).parent
        
        self.prompts_dir = Path(prompts_dir)
        self._prompts: dict[str, PromptFile] = {}
        self._load_prompts()

    def _load_prompts(self) -> None:
        """Load all prompts from files."""
        if not self.prompts_dir.exists():
            logger.warning("prompts_directory_not_found", path=str(self.prompts_dir))
            return

        # Load from subdirectories: general, dart, typescript
        categories = ["general", "dart", "typescript"]
        
        for category in categories:
            category_dir = self.prompts_dir / category
            if not category_dir.exists():
                continue
            
            for md_file in category_dir.glob("*.md"):
                try:
                    prompt = self._load_prompt_file(md_file, category)
                    if prompt:
                        self._prompts[prompt.name] = prompt
                        logger.debug("prompt_loaded", name=prompt.name, category=category)
                except Exception as e:
                    logger.error("failed_to_load_prompt", file=str(md_file), error=str(e))

    def _load_prompt_file(self, file_path: Path, category: str) -> PromptFile | None:
        """Load a single prompt file.

        Args:
            file_path: Path to .md file
            category: Prompt category

        Returns:
            PromptFile object or None if failed
        """
        content = file_path.read_text(encoding="utf-8")
        
        # Parse frontmatter (YAML between --- markers)
        frontmatter_match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
        
        if not frontmatter_match:
            logger.warning("no_frontmatter_found", file=str(file_path))
            return None
        
        frontmatter_text = frontmatter_match.group(1)
        template_text = frontmatter_match.group(2).strip()
        
        try:
            metadata = yaml.safe_load(frontmatter_text)
        except Exception as e:
            logger.error("failed_to_parse_frontmatter", file=str(file_path), error=str(e))
            return None
        
        if not metadata:
            logger.warning("empty_frontmatter", file=str(file_path))
            return None
        
        # Extract metadata
        name = metadata.get("name") or file_path.stem
        description = metadata.get("description", "")
        arguments = metadata.get("arguments", [])
        
        if not description:
            logger.warning("no_description", file=str(file_path))
        
        return PromptFile(
            name=name,
            description=description,
            arguments=arguments,
            template=template_text,
            category=category,
        )

    def list_prompts(self) -> list[Prompt]:
        """List all loaded prompts.

        Returns:
            List of Prompt objects
        """
        return [prompt.to_prompt() for prompt in self._prompts.values()]

    def get_prompt(self, name: str, arguments: dict[str, str] | None = None) -> GetPromptResult:
        """Get a prompt with filled arguments.

        Args:
            name: Prompt name
            arguments: Prompt arguments

        Returns:
            GetPromptResult with rendered prompt

        Raises:
            ValueError: If prompt not found
        """
        if name not in self._prompts:
            raise ValueError(f"Unknown prompt: {name}")
        
        return self._prompts[name].render(arguments)

    def reload(self) -> None:
        """Reload all prompts from files."""
        self._prompts.clear()
        self._load_prompts()
        logger.info("prompts_reloaded", count=len(self._prompts))


# Global prompt loader instance
_prompt_loader: PromptLoader | None = None


def get_prompt_loader() -> PromptLoader:
    """Get or create the global prompt loader instance.

    Returns:
        PromptLoader instance
    """
    global _prompt_loader
    if _prompt_loader is None:
        _prompt_loader = PromptLoader()
    return _prompt_loader
