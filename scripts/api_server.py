#!/usr/bin/env python3
"""
FastAPI server for Intent-Based Network Generation Augmentation toolkit.
"""
import sys
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from fastapi import FastAPI, HTTPException, BackgroundTasks
    from fastapi.responses import FileResponse
    from pydantic import BaseModel
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    print("FastAPI not available. Install with: pip install fastapi uvicorn")

if FASTAPI_AVAILABLE:
    from Intents_Generators.Advanced3GPPIntentGenerator import Advanced3GPPIntentGenerator
    from Evaluation.evaluation_metric import DataEvaluator
    from augmentation_utils import paraphrase, back_translate, synonym_augment

    app = FastAPI(
        title="Intent-Based Network Generation API",
        description="API for generating, augmenting, and evaluating 3GPP network intents",
        version="2.0.0"
    )

    generator = Advanced3GPPIntentGenerator(use_llm_synthesis=False)
    evaluator = DataEvaluator()

    class GenerationRequest(BaseModel):
        num_records: int = 10
        use_llm_synthesis: bool = False
        seed: Optional[int] = None

    class AugmentationRequest(BaseModel):
        text: str
        techniques: List[str] = ["synonym"]

    class EvaluationRequest(BaseModel):
        intents: List[str]

    class GenerationResponse(BaseModel):
        success: bool
        message: str
        data: Optional[Dict[str, Any]] = None

    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "message": "Intent-Based Network Generation API",
            "version": "2.0.0",
            "endpoints": [
                "/generate",
                "/augment",
                "/evaluate",
                "/health"
            ]
        }

    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "generator_ready": generator is not None,
            "evaluator_ready": evaluator is not None
        }

    @app.post("/generate", response_model=GenerationResponse)
    async def generate_intents(request: GenerationRequest, background_tasks: BackgroundTasks):
        """Generate network intents."""
        try:
            if request.seed:
                import random
                random.seed(request.seed)
            
            generator.use_llm_synthesis = request.use_llm_synthesis
            
            intents = generator.generate_batch(request.num_records)
            
            intent_data = []
            for intent in intents:
                intent_dict = {
                    "id": intent.id,
                    "intent_type": intent.intent_type,
                    "description": intent.description,
                    "timestamp": intent.timestamp,
                    "priority": intent.priority,
                    "network_slice": intent.network_slice,
                    "location": intent.location,
                    "metadata": intent.metadata
                }
                intent_data.append(intent_dict)
            
            filename = f"api_generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            background_tasks.add_task(save_intents_to_file, intents, filename)
            
            return GenerationResponse(
                success=True,
                message=f"Generated {len(intents)} intents successfully",
                data={
                    "intents": intent_data,
                    "count": len(intents),
                    "filename": filename
                }
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/augment")
    async def augment_text(request: AugmentationRequest):
        """Augment text using specified techniques."""
        try:
            results = {}
            
            for technique in request.techniques:
                if technique == "synonym":
                    results[technique] = synonym_augment(request.text)
                elif technique == "paraphrase":
                    results[technique] = paraphrase(request.text)
                elif technique == "backtranslate":
                    results[technique] = back_translate(request.text)
                else:
                    results[technique] = f"Unknown technique: {technique}"
            
            return {
                "success": True,
                "original": request.text,
                "augmented": results
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/evaluate")
    async def evaluate_intents(request: EvaluationRequest):
        """Evaluate intent quality."""
        try:
            result = evaluator.evaluate_batch(request.intents)
            
            return {
                "success": True,
                "evaluation": {
                    "overall_quality": result['overall_metrics'].overall_quality,
                    "technical_accuracy": result['overall_metrics'].technical_accuracy,
                    "compliance_level": result['overall_metrics'].compliance_level,
                    "research_value": result['overall_metrics'].research_value,
                    "insights": result['batch_insights']
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Evaluation requires LLM setup (Ollama)"
            }

    @app.get("/download/{filename}")
    async def download_file(filename: str):
        """Download generated files."""
        file_path = os.path.join("output", filename)
        if os.path.exists(file_path):
            return FileResponse(file_path, filename=filename)
        else:
            raise HTTPException(status_code=404, detail="File not found")

    def save_intents_to_file(intents, filename):
        """Background task to save intents to file."""
        try:
            os.makedirs("output", exist_ok=True)
            filepath = os.path.join("output", filename)
            generator.export_to_json(intents, filepath)
            print(f"Saved intents to {filepath}")
        except Exception as e:
            print(f"Error saving file: {e}")

else:
    class DummyApp:
        def __init__(self):
            print("FastAPI not available. Please install with: pip install fastapi uvicorn")
    
    app = DummyApp()

if __name__ == "__main__":
    if FASTAPI_AVAILABLE:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        print("FastAPI not available. Install with: pip install fastapi uvicorn")