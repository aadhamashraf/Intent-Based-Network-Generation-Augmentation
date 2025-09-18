# BaseIntentGenerator for shared parameter logic
from typing import Dict, Any
import time
import uuid

class BaseIntentGenerator:
    def __init__(self, constraint_engine=None):
        self.constraint_engine = constraint_engine

    def generate_base_params(self, intent_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate parameters common to all intent types."""
        base_params = {
            'timestamp': time.time(),
            'request_id': str(uuid.uuid4()),
            'intent_type': intent_type,
        }
        if self.constraint_engine:
            base_params['qos_parameters'] = self.constraint_engine.generate_constrained_qos_parameters(
                context.get('slice_type', ''),
                context.get('priority', ''),
                context.get('location', '')
            )
        return base_params
