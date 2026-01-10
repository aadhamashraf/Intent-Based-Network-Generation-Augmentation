import random
from enum import Enum
from typing import List, Any

class IntentType(Enum):
    DEPLOYMENT = "Deployment Intent"
    MODIFICATION = "Modification Intent"
    PERFORMANCE_ASSURANCE = "Performance Assurance Intent"
    REPORT_REQUEST = "Intent Report Request"
    FEASIBILITY_CHECK = "Intent Feasibility Check"
    NOTIFICATION_REQUEST = "Regular Notification Request"

class Priority(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    EMERGENCY = "EMERGENCY"

NETWORK_FUNCTIONS = [
    'AMF', 'SMF', 'UPF', 'PCF', 'UDM', 'AUSF', 'NRF', 'NSSF', 'NEF', 'AF',
    'gNB', 'eNB', 'ng-eNB', 'UE', 'N3IWF', 'TNGF', 'TWIF', 'W-AGF',
    'SEPP', 'SCP', 'BSF', 'CHF', 'UDSF', 'UNEF', 'UCMF', 'UDR',
    'NWDAF', 'ADRF', 'DCCF', 'CEF', 'CBCF', 'GMLC', 'LMF', 'SLF'
]

ADVANCED_SLICE_TYPES = [
    'eMBB_Ultra_HD_Streaming', 'eMBB_AR_VR_Immersive', 'eMBB_Cloud_Gaming',
    'URLLC_Industrial_Automation', 'URLLC_Autonomous_Vehicles', 'URLLC_Remote_Surgery',
    'URLLC_Critical_Infrastructure', 'URLLC_Tactile_Internet',
    'mMTC_Smart_Agriculture', 'mMTC_Environmental_Monitoring', 'mMTC_Asset_Tracking',
    'V2X_Cooperative_Driving', 'V2X_Traffic_Management', 'V2X_Emergency_Services',
    'Private_Network_Manufacturing', 'Private_Network_Healthcare', 'Private_Network_Education',
    'Edge_Computing_MEC', 'Network_Slicing_Orchestration', 'Multi_Access_Edge_Computing'
]

QOS_FLOW_IDENTIFIERS = [
    '5QI_1_Conversational_Voice', '5QI_2_Conversational_Video', '5QI_3_Real_Time_Gaming',
    '5QI_4_Non_Conversational_Video', '5QI_5_IMS_Signaling', '5QI_6_Video_TCP',
    '5QI_7_Voice_Video_Gaming', '5QI_8_Video_TCP_Premium', '5QI_9_Video_TCP_Background',
    '5QI_65_Mission_Critical_User_Plane', '5QI_66_Mission_Critical_Signaling',
    '5QI_67_Mission_Critical_Video', '5QI_69_Mission_Critical_Delay_Sensitive',
    '5QI_70_Mission_Critical_Data', '5QI_75_V2X_Messages', '5QI_79_V2X_Video',
    '5QI_80_Low_Latency_eMBB', '5QI_82_Discrete_Automation_Small_Packets',
    '5QI_83_Discrete_Automation_Large_Packets', '5QI_84_Intelligent_Transport_Systems',
    '5QI_85_Electricity_Distribution_High_Voltage'
]

ADVANCED_LOCATIONS = [
    'Cell_Site_Urban_Dense_001_GPS_40.7589_74.0060', 'Cell_Site_Suburban_002_GPS_34.0522_118.2437',
    'Industrial_Zone_Manufacturing_A7_GPS_41.8781_87.6298', 'Campus_Network_University_Hub_12_GPS_42.3601_71.0589',
    'Airport_Terminal_International_3_GPS_40.6413_73.7781', 'Highway_Corridor_Mile_45_GPS_39.7392_104.9903',
    'Port_Authority_Container_Zone_2_GPS_33.7701_118.1937', 'Medical_District_Hospital_C4_GPS_29.7604_95.3698',
    'Stadium_Sports_Complex_Network_01_GPS_40.7505_73.9934', 'Shopping_Mall_Commercial_Area_9_GPS_37.7749_122.4194',
    'Business_Park_Technology_Sector_15_GPS_37.4419_122.1430', 'Residential_High_Density_Block_A23_GPS_40.7831_73.9712',
    'Smart_City_IoT_Hub_Downtown_GPS_41.8781_87.6298', 'Edge_Data_Center_Facility_07_GPS_39.0458_76.6413',
    'Rural_Coverage_Extension_Point_R12_GPS_44.9778_93.2650', 'Underground_Metro_Station_M15_GPS_40.7505_73.9934'
]

RESEARCH_CONTEXTS = [
    'Network_Slicing_Optimization_Study', 'Intent_Based_Automation_Research',
    'AI_ML_Network_Management_Analysis', 'Edge_Computing_Performance_Evaluation',
    'QoS_Assurance_Mechanism_Study', 'Network_Function_Virtualization_Research',
    'Service_Orchestration_Efficiency_Analysis', 'Resource_Allocation_Algorithm_Study',
    'Network_Security_Intent_Framework', 'Multi_Tenant_Isolation_Research',
    'Latency_Optimization_Study', 'Bandwidth_Management_Analysis',
    'Fault_Tolerance_Mechanism_Research', 'Scalability_Performance_Evaluation',
    'Energy_Efficiency_Optimization_Study', 'Cross_Domain_Orchestration_Research'
]

COMPLIANCE_STANDARDS = [
    '3GPP_TS_28.312', '3GPP_TS_28.313', '3GPP_TS_28.314', '3GPP_TS_28.315',
    '3GPP_TS_23.501', '3GPP_TS_23.502', '3GPP_TS_23.503', '3GPP_TS_29.500',
    'ETSI_NFV_SOL_001', 'ETSI_NFV_SOL_002', 'ETSI_NFV_SOL_003',
    'ITU_T_Y.3011', 'ITU_T_Y.3012', 'ITU_T_Y.3013', 'ITU_T_Y.3014',
    'IETF_RFC_8309', 'IETF_RFC_8329', 'IETF_RFC_8453', 'IETF_RFC_8568',
    'TM_Forum_IG1176', 'TM_Forum_IG1177', 'ONF_TR_526', 'ONF_TR_527'
]

RADIO_PARAMETERS = [
    'RSRP', 'RSRQ', 'SINR', 'CQI', 'PMI', 'RI', 'HARQ_ACK_NACK',
    'CSI_RS', 'SRS', 'PUCCH', 'PUSCH', 'PDCCH', 'PDSCH', 'PRACH'
]

PROTOCOL_PARAMETERS = [
    'RRC_Connection_Setup_Time', 'NAS_Attach_Procedure_Latency',
    'PDU_Session_Establishment_Time', 'Handover_Interruption_Time',
    'Service_Request_Response_Time', 'Authentication_Procedure_Latency'
]

PERFORMANCE_METRICS = [
    'End_to_End_Latency', 'Jitter_Variation', 'Packet_Loss_Rate',
    'Throughput_Capacity', 'Connection_Density', 'Mobility_Success_Rate',
    'Service_Availability', 'Network_Efficiency', 'Resource_Utilization']

# Vendor and Infrastructure Constants
TELECOM_VENDORS = ['Ericsson', 'Nokia', 'Huawei', 'Samsung', 'ZTE', 'Cisco', 'Juniper', 'Dell', 'HPE']
CLOUD_PROVIDERS = ['AWS', 'Azure', 'GCP', 'IBM Cloud', 'Oracle Cloud']
CONTAINER_RUNTIMES = ['Docker', 'Containerd', 'CRI-O', 'Podman']
IMAGE_REGISTRIES = ['Docker Hub', 'Harbor', 'Quay', 'ECR', 'GCR']
SERVICE_MESHES = ['Istio', 'Linkerd', 'Consul Connect', 'Envoy']
ORCHESTRATION_TOOLS = ['Terraform', 'Ansible', 'CloudFormation', 'Pulumi']
CONFIG_MANAGEMENT_TOOLS = ['Puppet', 'Chef', 'SaltStack', 'Ansible']
