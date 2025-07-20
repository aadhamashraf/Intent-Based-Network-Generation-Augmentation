@dataclass
class EvaluationMetrics:
    technical_accuracy: float
    realism_score: float
    compliance_level: float
    research_value: float
    implementability: float
    overall_quality: float

class DataEvaluator:
    """LLM-enhanced sophisticated intent evaluation system with logging and prototyping."""

    def __init__(self):
        self.quality_thresholds = {
            'technical_accuracy': 8.0,
            'realism_score': 7.5,
            'compliance_level': 8.5,
            'research_value': 7.0,
            'implementability': 7.5,
            'overall_quality': 8.0
        }

    def _log(self, message: str):
        print(f"[DataEvaluator] {message}")

    def _ask_llm_metric(self, intent: str, metric_name: str, instructions: str) -> float:
        self._log(f"Querying LLM for {metric_name}...")
        prompt = f"""You are a senior 5G network architect and AI researcher.
        Evaluate the following network intent record and respond with a score from 0 to 10 (use decimals).

        ---
        Intent:
        {intent}

        Metric: {metric_name}
        Instructions: {instructions}
        ---
        Respond ONLY with the number.
        """.strip()

        result = subprocess.run(['ollama', 'run', 'mistral', prompt], capture_output=True, text=True)
        try:
            score = float(result.stdout.strip())
            self._log(f"Received score: {score}")
            return score
        except ValueError:
            self._log("Failed to parse score, defaulting to 0.0")
            return 0.0

    def evaluate_intent(self, intent: str) -> Dict[str, Any]:
        self._log("Evaluating single intent...")
        metrics = EvaluationMetrics(
            technical_accuracy=self._ask_llm_metric(intent, "Technical Accuracy", "Assess correctness of technologies, parameters, and terminology used in 5G context."),
            realism_score=self._ask_llm_metric(intent, "Realism Score", "Rate whether the intent reflects a real-world deployable scenario."),
            compliance_level=self._ask_llm_metric(intent, "3GPP Compliance", "Assess alignment with actual 3GPP specs and architectural flows."),
            research_value=self._ask_llm_metric(intent, "Research Value", "Rate novelty, academic insight, and uniqueness."),
            implementability=self._ask_llm_metric(intent, "Implementability", "Evaluate the practicality of deploying this in a real 5G setup."),
            overall_quality=0.0
        )

        metrics.overall_quality = sum([
            metrics.technical_accuracy,
            metrics.realism_score,
            metrics.compliance_level,
            metrics.research_value,
            metrics.implementability
        ]) / 5

        self._log(f"Final overall quality: {metrics.overall_quality:.2f}")

        return {
            'intent': intent,
            'metrics': metrics,
            'strengths': self._identify_strengths(metrics),
            'weaknesses': self._identify_weaknesses(metrics),
            'recommendations': self._generate_recommendations(metrics)
        }

    def evaluate_batch(self, intents: List[str]) -> Dict[str, Any]:
        self._log("Starting batch evaluation...")
        evaluations = [self.evaluate_intent(i) for i in intents[:5]]  # Prototype on 5 records
        overall_metrics = self._calculate_batch_metrics(evaluations)
        insights = self._generate_batch_insights(evaluations, overall_metrics)
        return {
            'overall_metrics': overall_metrics,
            'detailed_evaluations': evaluations,
            'batch_insights': insights
        }

    def _identify_strengths(self, metrics: EvaluationMetrics) -> List[str]:
        strengths = []
        if metrics.technical_accuracy >= 8.5:
            strengths.append("Excellent technical accuracy")
        if metrics.compliance_level >= 8.5:
            strengths.append("Strong 3GPP compliance")
        if metrics.research_value >= 8.0:
            strengths.append("High research potential")
        if metrics.implementability >= 8.0:
            strengths.append("Feasible for real-world deployment")
        return strengths

    def _identify_weaknesses(self, metrics: EvaluationMetrics) -> List[str]:
        weaknesses = []
        if metrics.technical_accuracy < 7.0:
            weaknesses.append("Weak technical grounding")
        if metrics.compliance_level < 7.5:
            weaknesses.append("Lacks 3GPP compliance")
        if metrics.research_value < 6.5:
            weaknesses.append("Low academic value")
        return weaknesses

    def _generate_recommendations(self, metrics: EvaluationMetrics) -> List[str]:
        recommendations = []
        if metrics.technical_accuracy < 8.0:
            recommendations.append("Review and refine 5G terminology and parameters")
        if metrics.research_value < 7.5:
            recommendations.append("Inject more experimental or innovative ideas")
        if metrics.implementability < 7.5:
            recommendations.append("Improve real-world applicability")
        return recommendations

    def _calculate_batch_metrics(self, evaluations: List[Dict[str, Any]]) -> EvaluationMetrics:
        if not evaluations:
            return EvaluationMetrics(0, 0, 0, 0, 0, 0)

        total = EvaluationMetrics(0, 0, 0, 0, 0, 0)
        for eval in evaluations:
            m = eval['metrics']
            total.technical_accuracy += m.technical_accuracy
            total.realism_score += m.realism_score
            total.compliance_level += m.compliance_level
            total.research_value += m.research_value
            total.implementability += m.implementability
            total.overall_quality += m.overall_quality

        count = len(evaluations)
        return EvaluationMetrics(
            technical_accuracy=total.technical_accuracy / count,
            realism_score=total.realism_score / count,
            compliance_level=total.compliance_level / count,
            research_value=total.research_value / count,
            implementability=total.implementability / count,
            overall_quality=total.overall_quality / count
        )

    def _generate_batch_insights(self, evaluations: List[Dict[str, Any]], metrics: EvaluationMetrics) -> List[str]:
        insights = [
            f"Overall Quality: {metrics.overall_quality:.2f}/10",
            f"Technical Accuracy: {metrics.technical_accuracy:.2f}/10",
            f"Compliance Level: {metrics.compliance_level:.2f}/10",
            f"Research Value: {metrics.research_value:.2f}/10",
        ]
        count = sum(1 for e in evaluations if e['metrics'].overall_quality >= 8.0)
        insights.append(f"{count}/{len(evaluations)} intents are high-quality")
        return insights
