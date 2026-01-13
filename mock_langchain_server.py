#!/usr/bin/env python3
"""
Servidor mock de LangChain para probar la integración.
Este servidor simula las respuestas de un agente LangChain.

Uso:
    python mock_langchain_server.py
    
    Luego en otro terminal:
    python agente-evaluador.py --archivos HU611_langchain.yml
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import uuid
from datetime import datetime

# Respuestas mock para diferentes consultas
RESPUESTAS_MOCK = {
    "equipaje": """Hola! Con gusto te ayudo con la información sobre equipaje.

El equipaje permitido varía según la tarifa adquirida. Para tu orden de vuelo, tienes:

**Equipaje de mano:**
- 1 pieza de hasta 8kg
- Dimensiones máximas: 55 x 35 x 25 cm

**Equipaje facturado:**
- Para tarifa Básica: No incluye equipaje facturado
- Para tarifa Plus: 1 pieza de hasta 23kg
- Para tarifa Top: 2 piezas de hasta 23kg cada una

¿Tienes alguna otra consulta sobre tu equipaje?""",
    
    "nacional": """Para tu vuelo nacional, el equipaje permitido es:

**Equipaje de cabina:**
- 1 bolso o mochila de hasta 8kg
- Dimensiones: 55 x 35 x 25 cm

**Equipaje de bodega** (según tu tarifa):
- Tarifa Light: No incluye
- Tarifa Plus: 1 maleta de 23kg
- Tarifa Top: 2 maletas de 23kg cada una

¿Necesitas saber algo más?""",

    "internacional": """Para tu vuelo internacional, tienes derecho a:

**Equipaje de cabina:**
- 1 pieza personal de hasta 8kg
- 1 equipaje de mano de hasta 10kg en cabina premium

**Equipaje facturado:**
- Tarifa Economy: 1 pieza de 23kg
- Tarifa Premium Economy: 2 piezas de 23kg
- Tarifa Business: 2 piezas de 32kg

¿Te gustaría información adicional?""",

    "cabina_bodega": """Por supuesto, te explico sobre equipaje de cabina y bodega:

**Equipaje de cabina:**
- Dimensiones máximas: 55x35x25 cm
- Peso máximo: 8-10kg dependiendo de la tarifa
- Debe caber en el compartimento superior

**Equipaje de bodega:**
- Varía según tu tarifa y destino
- Para vuelos con conexión, tu equipaje será transferido automáticamente
- Incluye tag de seguimiento

Para tu reserva específica con conexión, aplican las políticas de la tarifa que adquiriste.

¿Tienes más preguntas sobre tu equipaje?""",

    "default": """Entiendo tu consulta sobre equipaje. 

El equipaje permitido depende de tu tarifa y destino. Te recomiendo revisar los detalles específicos de tu orden de vuelo.

¿En qué más puedo ayudarte?"""
}

class MockLangChainHandler(BaseHTTPRequestHandler):
    """Handler para simular respuestas de LangChain."""
    
    def do_POST(self):
        """Maneja requests POST."""
        if self.path == '/invoke':
            try:
                # Leer el payload
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                payload = json.loads(post_data.decode('utf-8'))
                
                # Extraer input del usuario
                user_input = payload.get('input', '').lower()
                session_id = payload.get('session_id', str(uuid.uuid4()))
                config = payload.get('config', {})
                
                print(f"\n{'='*60}")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Nueva consulta")
                print(f"Session ID: {session_id}")
                print(f"Input: {user_input}")
                print(f"Config: {json.dumps(config, indent=2)}")
                
                # Determinar respuesta según el contenido
                response_text = self._get_mock_response(user_input)
                
                # Preparar respuesta
                response_data = {
                    "output": response_text,
                    "conversation_id": f"mock-conv-{session_id[:8]}",
                    "trace": [
                        {
                            "step": "agent_executor",
                            "action": "process_input",
                            "timestamp": datetime.now().isoformat()
                        },
                        {
                            "step": "llm_call",
                            "model": "mock-llm",
                            "timestamp": datetime.now().isoformat()
                        }
                    ],
                    "metadata": {
                        "session_id": session_id,
                        "mock_server": True,
                        "timestamp": datetime.now().isoformat()
                    }
                }
                
                print(f"Response: {response_text[:100]}...")
                print(f"{'='*60}\n")
                
                # Enviar respuesta
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
                
            except Exception as e:
                print(f"ERROR: {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_response = {
                    "error": str(e),
                    "output": "Error procesando la solicitud"
                }
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def _get_mock_response(self, user_input: str) -> str:
        """Determina qué respuesta mock usar según el input."""
        # Normalizar input
        input_lower = user_input.lower()
        
        # Detectar tipo de consulta
        if any(word in input_lower for word in ['tarifa', 'orden de vuelo', 'cuál es']):
            return RESPUESTAS_MOCK['equipaje']
        elif 'nacional' in input_lower:
            return RESPUESTAS_MOCK['nacional']
        elif 'internacional' in input_lower:
            return RESPUESTAS_MOCK['internacional']
        elif 'cabina' in input_lower and 'bodega' in input_lower:
            return RESPUESTAS_MOCK['cabina_bodega']
        elif any(word in input_lower for word in ['no', 'nada', 'gracias', 'eso']):
            return "Perfecto! Fue un gusto ayudarte. Si necesitas más información en el futuro, no dudes en contactarnos. ¡Buen viaje! 🛫"
        else:
            return RESPUESTAS_MOCK['default']
    
    def log_message(self, format, *args):
        """Suprimir logs automáticos de HTTPServer."""
        pass


def run_server(port=8000):
    """Inicia el servidor mock."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, MockLangChainHandler)
    
    print("\n" + "="*60)
    print("🚀 Servidor Mock de LangChain iniciado")
    print("="*60)
    print(f"📍 URL: http://localhost:{port}")
    print(f"📍 Endpoint: http://localhost:{port}/invoke")
    print("\nPara usar en tus tests, configura:")
    print(f"  agent_endpoint: http://localhost:{port}")
    print("\nPresiona Ctrl+C para detener")
    print("="*60 + "\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor detenido")
        httpd.server_close()


if __name__ == '__main__':
    run_server()

