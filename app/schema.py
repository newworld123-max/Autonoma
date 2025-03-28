"""
Schema definitions for Autonoma.

This module defines the core data structures used throughout the application,
including message formats, agent states, and tool specifications.
"""

from enum import Enum
from typing import Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field

# Type aliases
ROLE_TYPE = Literal["user", "assistant", "system", "tool"]

class AgentState(str, Enum):
    """Possible states for an agent during execution."""

    IDLE = "idle"
    RUNNING = "running"
    THINKING = "thinking"
    FINISHED = "finished"
    ERROR = "error"
    WAITING = "waiting"

class Message(BaseModel):
    """Message format for agent memory and communication."""

    role: ROLE_TYPE = Field(..., description="Role of the message sender")
    content: str = Field(..., description="Content of the message")
    base64_image: Optional[str] = Field(None, description="Base64 encoded image, if any")
    tool_call_id: Optional[str] = Field(None, description="ID for tool calls")
    metadata: Optional[Dict] = Field(None, description="Additional metadata")

    @classmethod
    def system_message(cls, content: str, **kwargs) -> "Message":
        """Create a system message."""
        return cls(role="system", content=content, **kwargs)

    @classmethod
    def user_message(cls, content: str, **kwargs) -> "Message":
        """Create a user message."""
        return cls(role="user", content=content, **kwargs)

    @classmethod
    def assistant_message(cls, content: str, **kwargs) -> "Message":
        """Create an assistant message."""
        return cls(role="assistant", content=content, **kwargs)

    @classmethod
    def tool_message(cls, content: str, tool_call_id: Optional[str] = None, **kwargs) -> "Message":
        """Create a tool message."""
        return cls(role="tool", content=content, tool_call_id=tool_call_id, **kwargs)

class Memory(BaseModel):
    """Container for agent memory."""

    messages: List[Message] = Field(default_factory=list, description="List of messages in memory")
    max_messages: int = Field(50, description="Maximum number of messages to retain")

    def add_message(self, message: Message) -> None:
        """Add a message to memory with limit enforcement."""
        self.messages.append(message)
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def clear(self) -> None:
        """Clear all messages from memory."""
        self.messages = []

    def get_last_n_messages(self, n: int) -> List[Message]:
        """Get the last N messages from memory."""
        return self.messages[-n:] if n < len(self.messages) else self.messages

class ToolParameter(BaseModel):
    """Parameter definition for a tool."""

    name: str = Field(..., description="Name of the parameter")
    type: str = Field(..., description="Type of the parameter")
    description: str = Field(..., description="Description of the parameter")
    required: bool = Field(False, description="Whether the parameter is required")

class Tool(BaseModel):
    """Tool definition that agents can use."""

    name: str = Field(..., description="Name of the tool")
    description: str = Field(..., description="Description of the tool's functionality")
    parameters: List[ToolParameter] = Field(default_factory=list, description="Parameters for the tool")

    def to_openai_format(self) -> Dict:
        """Convert to OpenAI function calling format."""
        params_properties = {}
        required_params = []

        for param in self.parameters:
            params_properties[param.name] = {
                "type": param.type,
                "description": param.description
            }
            if param.required:
                required_params.append(param.name)

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": params_properties,
                    "required": required_params
                }
            }
        }

class ToolCall(BaseModel):
    """Representation of a tool call from an agent."""

    id: str = Field(..., description="Unique identifier for the tool call")
    tool: str = Field(..., description="Name of the tool to call")
    parameters: Dict = Field(default_factory=dict, description="Parameters for the tool call")

class Result(BaseModel):
    """Result of a completed task."""

    success: bool = Field(..., description="Whether the task was successful")
    content: str = Field(..., description="Content of the result")
    metadata: Optional[Dict] = Field(None, description="Additional metadata")

class Task(BaseModel):
    """Task representation for agent execution."""

    id: str = Field(..., description="Unique identifier for the task")
    description: str = Field(..., description="Description of the task")
    priority: int = Field(1, description="Priority level (1-5, higher means more important)")
    status: str = Field("pending", description="Current status of the task")
    dependencies: List[str] = Field(default_factory=list, description="IDs of dependencies")
    result: Optional[Result] = Field(None, description="Result after completion")
