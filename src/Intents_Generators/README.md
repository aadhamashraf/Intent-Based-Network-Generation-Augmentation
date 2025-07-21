# Intent Generators Module

This module contains sophisticated generators for creating advanced 3GPP-compliant network intent records. The system is designed to produce research-grade datasets for intent-based networking (IBN) studies.

## 🏗️ Architecture

```
Intents_Generators/
├── Advanced3GPPIntentGenerator.py    # Main orchestrator class
├── Constants_Enums.py                # Enums and constants
├── Data_Structures.py                # Data models and structures
├── Parameter_Generator.py            # Complex parameter generation
├── utilis_generator.py               # Utility functions
├── Deployment_Intent_Generator.py    # Deployment intent generator
├── Modification_Intent_Generator.py  # Modification intent generator
├── Performance_Assurance_Intent_Generator.py  # Performance intent generator
├── Report_Request_Intent_Generator.py         # Report request generator
├── Feasibility_Check_Intent_Generator.py     # Feasibility check generator
├── Notification_Request_Intent_Generator.py  # Notification generator
└── README.md                         # This file
```

## 🎯 Core Components

### Advanced3GPPIntentGenerator

The main orchestrator class that coordinates all intent generation activities.

**Key Features:**
- Multi-type intent generation
- LLM-enhanced synthesis
- Quality evaluation integration
- Multiple export formats
- Research-grade metadata

**Usage:**
```python
from Intents_Generators import Advanced3GPPIntentGenerator

generator = Advanced3GPPIntentGenerator(use_llm_synthesis=True)
intents = generator.generate_batch(1000)
generator.export_to_csv(intents, "dataset.csv")
```

### Intent Type Generators

Specialized generators for each intent type:

#### 1. DeploymentIntentGenerator
- **Purpose**: Generate deployment-related network intents
- **Complexity**: High (VNF deployment, orchestration)
- **Parameters**: 200+ configurable parameters
- **Use Cases**: Network function deployment, service instantiation

#### 2. ModificationIntentGenerator
- **Purpose**: Generate modification and update intents
- **Complexity**: Medium-High (Change management)
- **Parameters**: Impact analysis, rollback strategies
- **Use Cases**: Configuration updates, scaling operations

#### 3. PerformanceAssuranceIntentGenerator
- **Purpose**: Generate performance monitoring and assurance intents
- **Complexity**: High (SLA management, KPI monitoring)
- **Parameters**: Performance thresholds, alerting rules
- **Use Cases**: SLA enforcement, performance optimization

#### 4. ReportRequestIntentGenerator
- **Purpose**: Generate reporting and analytics intents
- **Complexity**: Medium (Data aggregation, analytics)
- **Parameters**: Report scope, delivery mechanisms
- **Use Cases**: Performance reports, compliance audits

#### 5. FeasibilityCheckIntentGenerator
- **Purpose**: Generate feasibility assessment intents
- **Complexity**: Very High (Multi-dimensional analysis)
- **Parameters**: Technical, economic, operational feasibility
- **Use Cases**: Pre-deployment validation, risk assessment

#### 6. NotificationRequestIntentGenerator
- **Purpose**: Generate notification and alerting intents
- **Complexity**: Medium (Event management, delivery)
- **Parameters**: Subscription management, delivery channels
- **Use Cases**: Event notifications, alerting systems

## 🔧 Parameter Generation

### ParameterGenerator Class

Generates sophisticated, realistic parameters for network intents:

#### Network Topology Parameters
- Architecture types (SA/NSA 5G)
- Deployment scenarios
- Spectrum allocation
- Antenna configurations
- Backhaul specifications

#### QoS Parameters
- 5QI flow identifiers
- Bit rate specifications
- Latency budgets
- Error rate thresholds
- Priority levels

#### Security Parameters
- Authentication methods
- Encryption algorithms
- Key management
- Privacy protection
- Zero-trust architecture

#### Resource Allocation
- Compute resources
- Network resources
- Virtualization parameters
- AI-driven optimization

#### Monitoring Parameters
- KPI metrics
- Alerting configuration
- Analytics configuration
- ML model specifications

## 📊 Data Structures

### NetworkIntent
Core data structure representing a complete intent record:

```python
@dataclass
class NetworkIntent:
    id: str                           # Unique identifier
    intent_type: str                  # Type of intent
    description: str                  # Natural language description
    timestamp: str                    # Creation timestamp
    priority: str                     # Priority level
    network_slice: Optional[str]      # Target network slice
    location: Optional[str]           # Geographical location
    parameters: Dict[str, Any]        # Complex parameters
    metadata: Dict[str, Any]          # Research metadata
    llm_metadata: Optional[Dict[str, Any]]  # LLM synthesis metadata
```

### EvaluationMetrics
Quality assessment metrics:

```python
@dataclass
class EvaluationMetrics:
    technical_accuracy: float        # 3GPP compliance score
    realism_score: float            # Real-world feasibility
    compliance_level: float         # Standards adherence
    research_value: float           # Academic relevance
    implementability: float         # Deployment feasibility
    overall_quality: float          # Composite score
```

## 🎛️ Configuration

### Intent Types
- `DEPLOYMENT`: Network function deployment
- `MODIFICATION`: Configuration changes
- `PERFORMANCE_ASSURANCE`: SLA management
- `REPORT_REQUEST`: Analytics and reporting
- `FEASIBILITY_CHECK`: Pre-deployment validation
- `NOTIFICATION_REQUEST`: Event management

### Priority Levels
- `EMERGENCY`: Critical system issues
- `CRITICAL`: High-impact operations
- `HIGH`: Important but not critical
- `MEDIUM`: Standard operations
- `LOW`: Background tasks

### Network Functions
50+ 3GPP-defined network functions including:
- Core functions: AMF, SMF, UPF, PCF, UDM
- RAN functions: gNB, eNB, ng-eNB
- Edge functions: MEC, NWDAF
- Security functions: SEPP, AUSF

### Advanced Slice Types
20+ sophisticated slice configurations:
- eMBB variants (Ultra HD, AR/VR, Gaming)
- URLLC variants (Industrial, Automotive, Medical)
- mMTC variants (IoT, Agriculture, Monitoring)
- V2X variants (Cooperative driving, Traffic)
- Private network variants

## 🔬 Research Features

### Technical Complexity Levels
- **Level 1-3**: Basic configurations
- **Level 4-7**: Advanced setups
- **Level 8-10**: Research-grade complexity

### Compliance Standards
- 3GPP TS 28.312-315 (Intent management)
- 3GPP TS 23.501-503 (5G architecture)
- ETSI NFV SOL 001-003 (Orchestration)
- ITU-T Y.3011-3014 (Network management)

### Research Contexts
- Network slicing optimization
- Intent-based automation
- AI/ML network management
- Edge computing performance
- QoS assurance mechanisms

## Usage Examples

### Basic Generation
```python
generator = Advanced3GPPIntentGenerator()
intents = generator.generate_batch(100)
```

### Advanced Configuration
```python
generator = Advanced3GPPIntentGenerator(use_llm_synthesis=True)

# Generate with progress tracking
def progress_callback(current, total):
    print(f"Progress: {current}/{total}")

intents = generator.generate_batch(5000, progress_callback)

# Evaluate quality
evaluation = generator.evaluate_dataset(intents)
print(f"Quality Score: {evaluation['overall_metrics'].overall_quality}")

# Export in multiple formats
generator.export_to_csv(intents, "dataset.csv")
generator.export_to_json(intents, "dataset.json")
generator.export_research_dataset(intents, "research.json", evaluation)
```

### Custom Intent Generation
```python
from Intents_Generators import DeploymentIntentGenerator

# Generate specific intent type
deployment_gen = DeploymentIntentGenerator()
params = deployment_gen.generate_parameters()
description = deployment_gen.generate_description(
    params, 
    "Cell_Site_Urban_Dense_001", 
    "eMBB_Ultra_HD_Streaming"
)
```

## Quality Assurance

### Validation Checks
- Parameter consistency validation
- 3GPP compliance verification
- Realistic value ranges
- Cross-parameter dependencies

### Metadata Tracking
- Generation timestamps
- Complexity scores
- Research relevance
- Quality metrics
- Compliance standards

## Best Practices

1. **Use LLM Synthesis**: Enable for higher quality
2. **Set Random Seeds**: For reproducible datasets
3. **Monitor Progress**: Use callbacks for large batches
4. **Validate Quality**: Check evaluation metrics
5. **Export Metadata**: Include research context

## Customization

### Adding New Intent Types
1. Create new generator class
2. Implement `generate_parameters()` method
3. Implement `generate_description()` method
4. Add to `Advanced3GPPIntentGenerator.generators`
5. Update `IntentType` enum

### Extending Parameters
1. Add new constants to `Constants_Enums.py`
2. Extend `ParameterGenerator` methods
3. Update validation logic
4. Document new parameters

## 📈 Performance

### Generation Speed
- ~100-500 intents/second (depending on complexity)
- LLM synthesis adds ~2-5 seconds per intent
- Batch processing optimized for large datasets

### Memory Usage
- ~1-5 MB per 1000 intents
- Parameter complexity affects memory usage
- Streaming export for large datasets

## 🐛 Troubleshooting

### Common Issues
1. **Import Errors**: Check Python path and dependencies
2. **Memory Issues**: Use batch processing for large datasets
3. **Quality Issues**: Enable LLM synthesis and validation
4. **Performance**: Disable LLM synthesis for speed

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

generator = Advanced3GPPIntentGenerator()
# Detailed logging will be displayed
```
