# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from typing import Optional, Dict, Any
from agenteval.targets import BaseTarget, TargetResponse


class LangChainAgentTarget(BaseTarget):
    """Target para agentes de LangChain."""

    def __init__(
        self,
        agent_endpoint: str,  # URL del endpoint donde está desplegado
        session_attributes: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        """
        Inicializa el target de LangChain.
        
        Args:
            agent_endpoint: URL del endpoint del agente LangChain
            session_attributes: Atributos de sesión (entityId, country, etc.)
            **kwargs: Configuración adicional (aws_region, aws_profile, etc.)
        """
        self.agent_endpoint = agent_endpoint
        self.session_attributes = session_attributes or {}
        self.session_id = None
        self.additional_config = kwargs

    def start_new_session(self, session_id: Optional[str] = None) -> None:
        """Inicia una nueva sesión con el agente."""
        import uuid
        self.session_id = session_id or str(uuid.uuid4())

    def invoke(self, prompt: str) -> TargetResponse:
        """
        Invoca al agente LangChain.
        
        Args:
            prompt: El mensaje del usuario
            
        Returns:
            TargetResponse con la respuesta del agente
        """
        import requests
        
        # Inicializar sesión si no existe
        if self.session_id is None:
            self.start_new_session()
        
        # Preparar el payload según tu API de LangChain
        # NOTA: Ajusta esta estructura según la API real de tu agente
        payload = {
            "input": prompt,
            "session_id": self.session_id,
            "config": {
                "configurable": {
                    **self.session_attributes
                }
            }
        }
        
        try:
            # Invocar el endpoint de LangChain
            response = requests.post(
                f"{self.agent_endpoint}/invoke",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Extraer la respuesta (adapta según tu estructura)
            # Formatos comunes:
            # - data["output"]
            # - data["response"]
            # - data["result"]
            agent_response = data.get("output") or data.get("response") or data.get("result", "")
            
            # Extraer conversation_id si existe
            conversation_id = data.get("conversation_id") or data.get("conversationId")
            
            return TargetResponse(
                response=agent_response,
                data={
                    "langchain_trace": data.get("trace", []),
                    "conversation_id": conversation_id,
                    "metadata": data.get("metadata", {}),
                    "raw_response": data  # Para debugging
                }
            )
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP Error {e.response.status_code}: {e.response.text[:200]}"
            return TargetResponse(
                response=f"Error: {error_msg}",
                data={"error": error_msg, "status_code": e.response.status_code}
            )
        
        except requests.exceptions.ConnectionError as e:
            error_msg = f"Connection Error: No se pudo conectar a {self.agent_endpoint}"
            return TargetResponse(
                response=f"Error: {error_msg}",
                data={"error": str(e), "endpoint": self.agent_endpoint}
            )
        
        except requests.exceptions.Timeout:
            error_msg = "Timeout: El agente no respondió en 60 segundos"
            return TargetResponse(
                response=f"Error: {error_msg}",
                data={"error": error_msg}
            )
        
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            return TargetResponse(
                response=f"Error: {error_msg}",
                data={"error": str(e), "type": type(e).__name__}
            )

