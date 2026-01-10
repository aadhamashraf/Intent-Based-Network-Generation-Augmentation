import subprocess
import json
from dataclasses import dataclass
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

@dataclass
class EvaluationMetrics:
    technical_accuracy: float
    realism_score: float
    compliance_level: float
    research_value: float
    implementability: float
    overall_quality: float
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'technical_accuracy': self.technical_accuracy,
            'realism_score': self.realism_score,
            'compliance_level': self.compliance_level,
            'research_value': self.research_value,
            'implementability': self.implementability,
            'overall_quality': self.overall_quality
        }

@dataclass
class DetailedEvaluationMetrics:
    grammar_score: float
    intent_clarity: float
    domain_relevance: float
    linguistic_naturalness: float
    terminology_accuracy: float
    hallucination_risk: str
    label_confidence: float
    is_confusing: bool
    issues_detected: List[str]
    expert_feedback: str
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'grammar_score': self.grammar_score,
            'intent_clarity': self.intent_clarity,
            'domain_relevance': self.domain_relevance,
            'linguistic_naturalness': self.linguistic_naturalness,
            'terminology_accuracy': self.terminology_accuracy,
            'hallucination_risk': self.hallucination_risk,
            'label_confidence': self.label_confidence,
            'is_confusing': self.is_confusing,
            'issues_detected': self.issues_detected,
            'expert_feedback': self.expert_feedback
        }

class DataEvaluator:
    """LLM-enhanced sophisticated intent evaluation system with detailed criteria."""

    def __init__(self):
        self.quality_thresholds = {
            'grammar_score': 4.0,
            'intent_clarity': 4.0,
            'domain_relevance': 4.0,
            'linguistic_naturalness': 3.5,
            'terminology_accuracy': 4.0,
            'label_confidence': 4.0,
            'overall_quality': 4.0
        }

    def check_dependencies(self) -> Dict[str, bool]:
        """Check availability of external dependencies (Ollama)."""
        status = {"ollama_installed": False, "mistral_model_available": False}
        
        # Check Ollama executable
        try:
            subprocess.run(['ollama', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            status["ollama_installed"] = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return status

        # Check for Mistral model
        try:
            result = subprocess.run(['ollama', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            if b'mistral' in result.stdout:
                status["mistral_model_available"] = True
        except subprocess.CalledProcessError:
            pass
            
        return status

    def _log(self, message: str):
        print(f"[DataEvaluator] {message}")

    def _build_evaluation_prompt(self, text: str, label: str = "Unknown") -> str:
        """Build the detailed evaluation prompt."""
        return f"""You are an expert in both telecommunications (5G networking) and computational linguistics.
Your task is to critically evaluate the following intent sample and score it across multiple expert criteria.

--- TEXT: "{text}" LABEL: "{label}" ---

Please evaluate and respond with a JSON object containing these fields:

1. grammar_score (1-5): Rate grammar and sentence construction.
2. intent_clarity (1-5): Is the intent of the request unambiguous?
3. domain_relevance (1-5): How appropriate is this text for a 5G intent dataset?
4. linguistic_naturalness (1-5): How human-like and natural is the phrasing?
5. terminology_accuracy (1-5): Are technical terms used correctly (e.g., slices, URLLC, gNB)?
6. hallucination_risk: "None", "Low", "Medium", or "High"
7. label_confidence: How confident are you that the label is correct? (1-5)
8. is_confusing (true/false): Would a model likely misclassify this input?
9. issues_detected: List of critical issues (e.g., "ambiguous phrasing", "domain mismatch", "grammar errors")
10. expert_feedback: Suggest improvement if any.

Respond ONLY with a valid JSON object in this format:
{{
  "grammar_score": 4.5,
  "intent_clarity": 4.0,
  "domain_relevance": 5.0,
  "linguistic_naturalness": 4.2,
  "terminology_accuracy": 4.8,
  "hallucination_risk": "Low",
  "label_confidence": 4.5,
  "is_confusing": false,
  "issues_detected": ["minor grammar issue"],
  "expert_feedback": "Consider rephrasing for better clarity"
}}"""

    def _query_llm_detailed(self, prompt: str, retries: int = 2) -> Dict[str, Any]:
        """Query LLM with detailed evaluation prompt."""
        self._log("Querying LLM for detailed evaluation...")
        
        for attempt in range(retries + 1):
            try:
                result = subprocess.run(
                    ['ollama', 'run', 'mistral', '--format', 'json'],
                    input=prompt.encode('utf-8'),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=60,
                    check=True
                )
                
                response_text = result.stdout.decode('utf-8').strip()
                self._log(f"Raw LLM response: {response_text[:200]}...")
                
                # Try to parse JSON response
                evaluation_data = json.loads(response_text)
                
                # Validate required fields
                required_fields = [
                    'grammar_score', 'intent_clarity', 'domain_relevance',
                    'linguistic_naturalness', 'terminology_accuracy', 'hallucination_risk',
                    'label_confidence', 'is_confusing', 'issues_detected', 'expert_feedback'
                ]
                
                for field in required_fields:
                    if field not in evaluation_data:
                        raise ValueError(f"Missing required field: {field}")
                
                self._log("Successfully parsed detailed evaluation")
                return evaluation_data
                
            except subprocess.TimeoutExpired:
                self._log(f"LLM timeout on attempt {attempt + 1}")
            except subprocess.CalledProcessError as e:
                self._log(f"LLM process error: {e.stderr.decode('utf-8')}")
            except json.JSONDecodeError as e:
                self._log(f"JSON parsing error: {e}")
            except Exception as e:
                self._log(f"Unexpected error: {e}")
        
        # Return default evaluation if all attempts fail
        self._log("All LLM attempts failed, returning default evaluation")
        return self._get_default_evaluation()

    def _get_default_evaluation(self) -> Dict[str, Any]:
        """Return default evaluation when LLM is unavailable."""
        return {
            "grammar_score": 4.0,
            "intent_clarity": 4.0,
            "domain_relevance": 4.0,
            "linguistic_naturalness": 4.0,
            "terminology_accuracy": 4.0,
            "hallucination_risk": "Low",
            "label_confidence": 4.0,
            "is_confusing": False,
            "issues_detected": ["LLM evaluation unavailable"],
            "expert_feedback": "Unable to perform detailed evaluation - LLM service unavailable"
        }

    def evaluate_intent_detailed(self, intent: str, label: str = "Unknown") -> Dict[str, Any]:
        """Evaluate a single intent with detailed criteria."""
        self._log(f"Evaluating intent: {intent[:50]}...")
        
        prompt = self._build_evaluation_prompt(intent, label)
        evaluation_data = self._query_llm_detailed(prompt)
        
        # Create detailed metrics object
        detailed_metrics = DetailedEvaluationMetrics(
            grammar_score=float(evaluation_data.get('grammar_score', 4.0)),
            intent_clarity=float(evaluation_data.get('intent_clarity', 4.0)),
            domain_relevance=float(evaluation_data.get('domain_relevance', 4.0)),
            linguistic_naturalness=float(evaluation_data.get('linguistic_naturalness', 4.0)),
            terminology_accuracy=float(evaluation_data.get('terminology_accuracy', 4.0)),
            hallucination_risk=evaluation_data.get('hallucination_risk', 'Low'),
            label_confidence=float(evaluation_data.get('label_confidence', 4.0)),
            is_confusing=bool(evaluation_data.get('is_confusing', False)),
            issues_detected=evaluation_data.get('issues_detected', []),
            expert_feedback=evaluation_data.get('expert_feedback', '')
        )
        
        # Calculate overall quality score
        overall_quality = (
            detailed_metrics.grammar_score +
            detailed_metrics.intent_clarity +
            detailed_metrics.domain_relevance +
            detailed_metrics.linguistic_naturalness +
            detailed_metrics.terminology_accuracy
        ) / 5
        
        # Convert to legacy format for compatibility
        legacy_metrics = EvaluationMetrics(
            technical_accuracy=detailed_metrics.terminology_accuracy,
            realism_score=detailed_metrics.domain_relevance,
            compliance_level=detailed_metrics.domain_relevance,
            research_value=detailed_metrics.intent_clarity,
            implementability=detailed_metrics.linguistic_naturalness,
            overall_quality=overall_quality
        )
        
        return {
            'intent': intent,
            'label': label,
            'detailed_metrics': detailed_metrics,
            'legacy_metrics': legacy_metrics,
            'strengths': self._identify_strengths_detailed(detailed_metrics),
            'weaknesses': self._identify_weaknesses_detailed(detailed_metrics),
            'recommendations': self._generate_recommendations_detailed(detailed_metrics)
        }

    def evaluate_intent(self, intent: str) -> Dict[str, Any]:
        """Legacy method for backward compatibility."""
        return self.evaluate_intent_detailed(intent, "Unknown")

    def evaluate_batch(self, intents: List[str], labels: List[str] = None) -> Dict[str, Any]:
        """Evaluate a batch of intents with detailed criteria."""
        self._log(f"Starting detailed batch evaluation of {len(intents)} intents...")
        
        if labels is None:
            labels = ["Unknown"] * len(intents)
        
        # Limit to first 5 for prototype/demo
        sample_size = min(5, len(intents))
        evaluations = []
        
        for i in range(sample_size):
            evaluation = self.evaluate_intent_detailed(intents[i], labels[i] if i < len(labels) else "Unknown")
            evaluations.append(evaluation)
        
        # Calculate batch metrics
        overall_metrics = self._calculate_batch_metrics_detailed(evaluations)
        insights = self._generate_batch_insights_detailed(evaluations, overall_metrics)
        
        return {
            'overall_metrics': overall_metrics,
            'detailed_evaluations': evaluations,
            'batch_insights': insights,
            'evaluation_summary': self._create_evaluation_summary(evaluations)
        }

    def _identify_strengths_detailed(self, metrics: DetailedEvaluationMetrics) -> List[str]:
        """Identify strengths based on detailed metrics."""
        strengths = []
        
        if metrics.grammar_score >= 4.5:
            strengths.append("Excellent grammar and sentence construction")
        if metrics.intent_clarity >= 4.5:
            strengths.append("Very clear and unambiguous intent")
        if metrics.domain_relevance >= 4.5:
            strengths.append("Highly relevant to 5G domain")
        if metrics.linguistic_naturalness >= 4.0:
            strengths.append("Natural and human-like phrasing")
        if metrics.terminology_accuracy >= 4.5:
            strengths.append("Accurate technical terminology usage")
        if metrics.hallucination_risk in ["None", "Low"]:
            strengths.append("Low risk of model hallucination")
        if metrics.label_confidence >= 4.0:
            strengths.append("High confidence in label accuracy")
        if not metrics.is_confusing:
            strengths.append("Clear and unconfusing for model classification")
        
        return strengths

    def _identify_weaknesses_detailed(self, metrics: DetailedEvaluationMetrics) -> List[str]:
        """Identify weaknesses based on detailed metrics."""
        weaknesses = []
        
        if metrics.grammar_score < 3.0:
            weaknesses.append("Poor grammar and sentence construction")
        if metrics.intent_clarity < 3.0:
            weaknesses.append("Ambiguous or unclear intent")
        if metrics.domain_relevance < 3.0:
            weaknesses.append("Poor relevance to 5G domain")
        if metrics.linguistic_naturalness < 3.0:
            weaknesses.append("Unnatural or robotic phrasing")
        if metrics.terminology_accuracy < 3.0:
            weaknesses.append("Incorrect technical terminology")
        if metrics.hallucination_risk in ["High", "Medium"]:
            weaknesses.append(f"{metrics.hallucination_risk} risk of model hallucination")
        if metrics.label_confidence < 3.0:
            weaknesses.append("Low confidence in label accuracy")
        if metrics.is_confusing:
            weaknesses.append("Likely to confuse model classification")
        
        # Add specific issues detected
        if metrics.issues_detected:
            weaknesses.extend([f"Issue: {issue}" for issue in metrics.issues_detected])
        
        return weaknesses

    def _generate_recommendations_detailed(self, metrics: DetailedEvaluationMetrics) -> List[str]:
        """Generate recommendations based on detailed metrics."""
        recommendations = []
        
        if metrics.grammar_score < 4.0:
            recommendations.append("Improve grammar and sentence structure")
        if metrics.intent_clarity < 4.0:
            recommendations.append("Clarify the intent to reduce ambiguity")
        if metrics.domain_relevance < 4.0:
            recommendations.append("Enhance relevance to 5G networking domain")
        if metrics.linguistic_naturalness < 4.0:
            recommendations.append("Make phrasing more natural and human-like")
        if metrics.terminology_accuracy < 4.0:
            recommendations.append("Verify and correct technical terminology")
        if metrics.hallucination_risk in ["High", "Medium"]:
            recommendations.append("Reduce complexity to minimize hallucination risk")
        if metrics.is_confusing:
            recommendations.append("Simplify or restructure to reduce confusion")
        
        # Add expert feedback if available
        if metrics.expert_feedback and metrics.expert_feedback.strip():
            recommendations.append(f"Expert suggestion: {metrics.expert_feedback}")
        
        return recommendations

    def _calculate_batch_metrics_detailed(self, evaluations: List[Dict[str, Any]]) -> EvaluationMetrics:
        """Calculate batch metrics from detailed evaluations."""
        if not evaluations:
            return EvaluationMetrics(0, 0, 0, 0, 0, 0)

        # Calculate averages from detailed metrics
        total_grammar = sum(eval['detailed_metrics'].grammar_score for eval in evaluations)
        total_clarity = sum(eval['detailed_metrics'].intent_clarity for eval in evaluations)
        total_relevance = sum(eval['detailed_metrics'].domain_relevance for eval in evaluations)
        total_naturalness = sum(eval['detailed_metrics'].linguistic_naturalness for eval in evaluations)
        total_terminology = sum(eval['detailed_metrics'].terminology_accuracy for eval in evaluations)
        
        count = len(evaluations)
        
        # Map to legacy metrics for compatibility
        technical_accuracy = total_terminology / count
        realism_score = total_relevance / count
        compliance_level = total_relevance / count
        research_value = total_clarity / count
        implementability = total_naturalness / count
        overall_quality = (total_grammar + total_clarity + total_relevance + total_naturalness + total_terminology) / (5 * count)
        
        return EvaluationMetrics(
            technical_accuracy=technical_accuracy,
            realism_score=realism_score,
            compliance_level=compliance_level,
            research_value=research_value,
            implementability=implementability,
            overall_quality=overall_quality
        )

    def _generate_batch_insights_detailed(self, evaluations: List[Dict[str, Any]], metrics: EvaluationMetrics) -> List[str]:
        """Generate batch insights from detailed evaluations."""
        insights = [
            f"Overall Quality: {metrics.overall_quality:.2f}/5",
            f"Technical Accuracy: {metrics.technical_accuracy:.2f}/5",
            f"Domain Relevance: {metrics.realism_score:.2f}/5",
            f"Intent Clarity: {metrics.research_value:.2f}/5",
        ]
        
        # Count high-quality intents
        high_quality_count = sum(1 for eval in evaluations 
                                if eval['detailed_metrics'].grammar_score >= 4.0 
                                and eval['detailed_metrics'].intent_clarity >= 4.0)
        insights.append(f"{high_quality_count}/{len(evaluations)} intents are high-quality")
        
        # Count confusing intents
        confusing_count = sum(1 for eval in evaluations if eval['detailed_metrics'].is_confusing)
        if confusing_count > 0:
            insights.append(f"{confusing_count}/{len(evaluations)} intents may confuse models")
        
        # Hallucination risk summary
        high_risk_count = sum(1 for eval in evaluations 
                             if eval['detailed_metrics'].hallucination_risk in ["High", "Medium"])
        if high_risk_count > 0:
            insights.append(f"{high_risk_count}/{len(evaluations)} intents have medium/high hallucination risk")
        
        return insights

    def _create_evaluation_summary(self, evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a comprehensive evaluation summary."""
        if not evaluations:
            return {}
        
        # Aggregate statistics
        grammar_scores = [eval['detailed_metrics'].grammar_score for eval in evaluations]
        clarity_scores = [eval['detailed_metrics'].intent_clarity for eval in evaluations]
        relevance_scores = [eval['detailed_metrics'].domain_relevance for eval in evaluations]
        naturalness_scores = [eval['detailed_metrics'].linguistic_naturalness for eval in evaluations]
        terminology_scores = [eval['detailed_metrics'].terminology_accuracy for eval in evaluations]
        
        # Risk distribution
        risk_distribution = {}
        for eval in evaluations:
            risk = eval['detailed_metrics'].hallucination_risk
            risk_distribution[risk] = risk_distribution.get(risk, 0) + 1
        
        # Common issues
        all_issues = []
        for eval in evaluations:
            all_issues.extend(eval['detailed_metrics'].issues_detected)
        
        issue_counts = {}
        for issue in all_issues:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
        
        return {
            'score_averages': {
                'grammar_score': sum(grammar_scores) / len(grammar_scores),
                'intent_clarity': sum(clarity_scores) / len(clarity_scores),
                'domain_relevance': sum(relevance_scores) / len(relevance_scores),
                'linguistic_naturalness': sum(naturalness_scores) / len(naturalness_scores),
                'terminology_accuracy': sum(terminology_scores) / len(terminology_scores)
            },
            'risk_distribution': risk_distribution,
            'common_issues': dict(sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
            'confusing_intents_count': sum(1 for eval in evaluations if eval['detailed_metrics'].is_confusing),
            'total_evaluated': len(evaluations)
        }
