"""
Configuration management for Autonoma.

This module handles loading and validating configuration from various sources,
including environment variables, YAML files, and default settings.
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Union
import yaml
from pydantic import BaseModel, Field, root_validator

# Determine project root and config locations
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
CONFIG_DIR = PROJECT_ROOT / "config"
DEFAULT_CONFIG_PATH = CONFIG_DIR / "default.yaml"

class LLMConfig(BaseModel):
    """Configuration for the LLM (Large Language Model) subsystem."""

    # Provider settings
    provider: str = Field("openai", description="LLM provider (openai, anthropic, etc.)")
    model: str = Field("gpt-4o", description="Model name for the provider")
    api_key: Optional[str] = Field(None, description="API key for the LLM provider")

    # Generation parameters
    temperature: float = Field(0.7, description="Temperature for generation")
    max_tokens: int = Field(4096, description="Maximum tokens in completion")
    top_p: float = Field(1.0, description="Top P sampling parameter")
    frequency_penalty: float = Field(0.0, description="Frequency penalty")
    presence_penalty: float = Field(0.0, description="Presence penalty")

    @root_validator
    def check_api_key(cls, values):
        """Validate API key is available from either config or environment."""
        provider = values.get("provider", "")
        api_key = values.get("api_key")

        if not api_key:
            # Try to get from environment based on provider
            env_var = f"{provider.upper()}_API_KEY"
            api_key = os.environ.get(env_var)

        if not api_key:
            # General fallback for OpenAI
            api_key = os.environ.get("OPENAI_API_KEY")

        if not api_key and provider in ["openai", "anthropic"]:
            print(f"Warning: No API key found for {provider}. Set {provider.upper()}_API_KEY environment variable.")

        values["api_key"] = api_key
        return values

class AgentConfig(BaseModel):
    """Configuration for AI agent behavior."""

    max_steps: int = Field(10, description="Maximum steps for agent execution")
    thinking_depth: int = Field(2, description="Recursion depth for thinking")
    duplicate_threshold: int = Field(2, description="Threshold for detecting loops")
    memory_limit: int = Field(50, description="Maximum messages in memory")

class Config(BaseModel):
    """Main configuration container for Autonoma."""

    # General settings
    debug: bool = Field(False, description="Enable debug mode")
    trace: bool = Field(False, description="Enable detailed tracing")

    # Component configurations
    llm: LLMConfig = Field(default_factory=LLMConfig, description="LLM configuration")
    agent: AgentConfig = Field(default_factory=AgentConfig, description="Agent configuration")

    # Web3 settings
    solana_rpc: Optional[str] = Field(None, description="Solana RPC endpoint")

    @classmethod
    def load(cls, config_path: Optional[Union[str, Path]] = None) -> "Config":
        """
        Load configuration from a YAML file and environment variables.

        Args:
            config_path: Path to the YAML configuration file

        Returns:
            Config: Configuration object
        """
        # Start with default configuration
        config_data = {}

        # Load from default.yaml if it exists
        if DEFAULT_CONFIG_PATH.exists():
            with open(DEFAULT_CONFIG_PATH, "r") as f:
                config_data.update(yaml.safe_load(f) or {})

        # Load from specified config file if provided
        if config_path:
            config_path = Path(config_path)
            if config_path.exists():
                with open(config_path, "r") as f:
                    config_data.update(yaml.safe_load(f) or {})

        # Create config object with the loaded data
        return cls(**config_data)

# Create a global configuration instance
CONFIG = Config.load()

if __name__ == "__main__":
    # Print current configuration when run directly
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Config directory: {CONFIG_DIR}")
    print(CONFIG.json(indent=2))
