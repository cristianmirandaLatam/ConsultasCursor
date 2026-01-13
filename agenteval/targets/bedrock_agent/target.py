# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import uuid
import re
from typing import Optional, Dict

from agenteval.targets import Boto3Target, TargetResponse

_SERVICE_NAME = "bedrock-agent-runtime"


class BedrockAgentTarget(Boto3Target):
    """A target encapsulating an Amazon Bedrock agent."""

    def __init__(
        self,
        bedrock_agent_id: str,
        bedrock_agent_alias_id: str,
        bedrock_session_attributes: Optional[dict] = None,
        bedrock_prompt_session_attributes: Optional[dict] = None,
        **kwargs
    ):
        super().__init__(boto3_service_name=_SERVICE_NAME, **kwargs)
        self._bedrock_agent_id = bedrock_agent_id
        self._bedrock_agent_alias_id = bedrock_agent_alias_id
        self._base_session_state = {}
        if bedrock_session_attributes:
            self._base_session_state["sessionAttributes"] = dict(bedrock_session_attributes)
        if bedrock_prompt_session_attributes:
            self._base_session_state["promptSessionAttributes"] = dict(bedrock_prompt_session_attributes)
        self._session_id: str = str(uuid.uuid4())

    def start_new_session(self, session_id: Optional[str] = None) -> None:
        self._session_id = session_id or str(uuid.uuid4())

    def _buscar_conv_id_json(self, data):
        
        if isinstance(data, dict):
            for k, v in data.items():
                if k in ("genesysConversationId", "conversation_id") and isinstance(v, str):
                    return v
                if isinstance(v, dict):
                    found = self._buscar_conv_id_json(v)
                    if found:
                        return found
        return None

    def invoke(
        self,
        prompt: str,
        *,
        prompt_session_overrides: Optional[Dict[str, str]] = None,
        session_overrides: Optional[Dict[str, str]] = None,
    ) -> TargetResponse:
        base_session = self._base_session_state.get("sessionAttributes", {})
        base_prompt = self._base_session_state.get("promptSessionAttributes", {})
        eff_session = {**base_session, **(session_overrides or {})}
        eff_prompt = {**base_prompt, **(prompt_session_overrides or {})}

        session_state = {}
        if eff_session:
            session_state["sessionAttributes"] = eff_session
        if eff_prompt:
            session_state["promptSessionAttributes"] = eff_prompt

        args = {
            "agentId": self._bedrock_agent_id,
            "agentAliasId": self._bedrock_agent_alias_id,
            "sessionId": self._session_id,
            "sessionState": session_state,
            "inputText": prompt,
            "enableTrace": True,
        }

        response = self.boto3_client.invoke_agent(**args)

        # Primer intento: buscar el ID directo en el objeto respuesta (incluye recursivo en body y parameters)
        conversation_id = self._buscar_conv_id_json(response)

        stream = response.get("completion")
        completion = ""
        trace_data = []

        if stream:
            for event in stream:
                chunk = event.get("chunk")
                event_trace = event.get("trace")
                if chunk:
                    completion += chunk.get("bytes").decode()
                if event_trace:
                    trace_data.append(event_trace.get("trace"))

        # Si no lo encuentra directo, intenta extraerlo del texto
        if not conversation_id:
            match_conv = re.search(r"Conv ID:\s*([a-f0-9\-]+)", completion)
            if match_conv:
                conversation_id = match_conv.group(1)
        # Otro fallback: busca como json plano
        if not conversation_id:
            match_json = re.search(r'"conversation_id"\s*:\s*"([a-f0-9\-]+)"', completion)
            if match_json:
                conversation_id = match_json.group(1)

        return TargetResponse(
            response=completion,
            data={
                "bedrock_agent_trace": trace_data,
                "conversation_id": conversation_id,
            }
        )
