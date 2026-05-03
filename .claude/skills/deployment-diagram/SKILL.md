---
name: deployment-diagram
description: >-
  Create cloud architecture and deployment topology diagrams using PlantUML
  with official cloud provider stencil icons (AWS, Azure, GCP, Alibaba Cloud,
  IBM Cloud, Kubernetes, OpenStack). Supports multi-cloud, hybrid, and
  on-premise topologies with provider-specific icon libraries. Use when the
  user asks to "create deployment diagram", "cloud architecture diagram",
  "infrastructure diagram", "cloud topology", "K8s deployment diagram", "AWS
  architecture", "Azure diagram", "GCP topology", "배포 다이어그램", "클라우드 아키텍처",
  "인프라 다이어그램", "쿠버네티스 배포", or needs to visualize cloud infrastructure with
  vendor-specific icons. Do NOT use for application architecture layers (use
  architecture-diagram skill). Do NOT use for BPMN business workflows (use
  workflow-diagram skill). Do NOT use for generic flowcharts (use flowchart
  skill). Do NOT use for class/object relationships (use class-diagram skill).
---

# Deployment Diagram Generator

**Quick Start:** Pick cloud provider -> Set direction -> Define nodes/services with stencil icons -> Group in regions/VPCs -> Connect with arrows.

## Critical Rules

### Rule 1: PlantUML Code Fence
Always output inside ` ```plantuml ` fenced code blocks with `@startuml` / `@enduml`.

### Rule 2: Direction
Use `left to right direction` for horizontal layouts (recommended for wide diagrams). Omit for vertical.

### Rule 3: Stencil Icon Syntax
Use `<<mxgraph.<provider>.<icon>>>` stereotype to apply cloud provider icons:
```
agent my_service <<mxgraph.aws4.lambda>> as "Lambda\nFunction"
```
Icons receive vendor-appropriate colors automatically.

### Rule 4: Provider Icon Libraries

#### AWS (`mxgraph.aws4.*`)
| Icon | Stencil | Use For |
|---|---|---|
| EC2 | `mxgraph.aws4.ec2` | Compute instances |
| Lambda | `mxgraph.aws4.lambda` | Serverless functions |
| S3 | `mxgraph.aws4.s3` | Object storage |
| RDS | `mxgraph.aws4.rds` | Relational database |
| DynamoDB | `mxgraph.aws4.dynamodb` | NoSQL database |
| ELB/ALB | `mxgraph.aws4.elastic_load_balancing` | Load balancer |
| CloudFront | `mxgraph.aws4.cloudfront` | CDN |
| VPC | `mxgraph.aws4.vpc` | Network boundary |
| EKS | `mxgraph.aws4.eks` | Kubernetes service |
| SQS | `mxgraph.aws4.sqs` | Message queue |
| SNS | `mxgraph.aws4.sns` | Notification service |
| API Gateway | `mxgraph.aws4.api_gateway` | API management |
| Route53 | `mxgraph.aws4.route_53` | DNS |
| IAM | `mxgraph.aws4.iam` | Identity & access |

#### Azure (`mxgraph.azure.*`)
| Icon | Stencil | Use For |
|---|---|---|
| VM | `mxgraph.azure.virtual_machine` | Compute |
| App Service | `mxgraph.azure.app_services` | PaaS web |
| AKS | `mxgraph.azure.kubernetes_services` | Kubernetes |
| SQL Database | `mxgraph.azure.sql_databases` | Database |
| Blob Storage | `mxgraph.azure.blob_storage` | Object storage |
| Functions | `mxgraph.azure.function_apps` | Serverless |
| VNet | `mxgraph.azure.virtual_networks` | Network |
| Load Balancer | `mxgraph.azure.load_balancers` | Load balancer |

#### GCP (`mxgraph.gcp2.*`)
| Icon | Stencil | Use For |
|---|---|---|
| Compute Engine | `mxgraph.gcp2.compute_engine` | Compute |
| GKE | `mxgraph.gcp2.google_kubernetes_engine` | Kubernetes |
| Cloud Functions | `mxgraph.gcp2.cloud_functions` | Serverless |
| Cloud SQL | `mxgraph.gcp2.cloud_sql` | Database |
| Cloud Storage | `mxgraph.gcp2.cloud_storage` | Object storage |
| Pub/Sub | `mxgraph.gcp2.cloud_pubsub` | Messaging |
| BigQuery | `mxgraph.gcp2.bigquery` | Data warehouse |

#### Kubernetes (`mxgraph.kubernetes.*`)
| Icon | Stencil | Use For |
|---|---|---|
| Pod | `mxgraph.kubernetes.pod` | Pod |
| Service | `mxgraph.kubernetes.svc` | Service |
| Deployment | `mxgraph.kubernetes.deploy` | Deployment |
| Ingress | `mxgraph.kubernetes.ing` | Ingress controller |
| ConfigMap | `mxgraph.kubernetes.cm` | Configuration |
| Secret | `mxgraph.kubernetes.secret` | Secrets |
| PV | `mxgraph.kubernetes.pv` | Persistent Volume |
| Namespace | `mxgraph.kubernetes.ns` | Namespace |

### Rule 5: Container Shapes
| Shape | Syntax | Use For |
|---|---|---|
| Region / VPC | `rectangle "us-east-1" { }` | Cloud region |
| Cluster | `package "EKS Cluster" { }` | K8s cluster |
| Availability Zone | `rectangle "AZ-a" { }` | AZ boundary |
| External | `cloud "Internet" { }` | External systems |
| On-prem | `node "Data Center" { }` | Physical infra |

### Rule 6: Connection Types
| Type | Syntax | Meaning |
|---|---|---|
| Solid | `-->` | Data flow / network |
| Dashed | `..>` | Async / eventual |
| Labeled | `--> : "HTTPS"` | Protocol / port |

## Template: AWS Three-Tier Architecture

```plantuml
@startuml
left to right direction
skinparam backgroundColor white

cloud "Internet" as inet {
  agent users as "Users"
}

rectangle "AWS Region: us-east-1" {
  agent cf <<mxgraph.aws4.cloudfront>> as "CloudFront\nCDN"
  agent alb <<mxgraph.aws4.elastic_load_balancing>> as "Application\nLoad Balancer"

  rectangle "Public Subnet" {
    agent web1 <<mxgraph.aws4.ec2>> as "Web Server 1"
    agent web2 <<mxgraph.aws4.ec2>> as "Web Server 2"
  }

  rectangle "Private Subnet" {
    agent app1 <<mxgraph.aws4.ec2>> as "App Server 1"
    agent app2 <<mxgraph.aws4.ec2>> as "App Server 2"
    agent cache <<mxgraph.aws4.elasticache>> as "ElastiCache\nRedis"
  }

  rectangle "Data Subnet" {
    agent rds_primary <<mxgraph.aws4.rds>> as "RDS Primary\nPostgreSQL"
    agent rds_replica <<mxgraph.aws4.rds>> as "RDS Read\nReplica"
    agent s3 <<mxgraph.aws4.s3>> as "S3\nAssets"
  }
}

users --> cf
cf --> alb
alb --> web1
alb --> web2
web1 --> app1
web2 --> app2
app1 --> cache
app2 --> cache
app1 --> rds_primary
app2 --> rds_primary
rds_primary --> rds_replica
app1 ..> s3
app2 ..> s3
@enduml
```

## Template: Kubernetes Microservices Deployment

```plantuml
@startuml
left to right direction
skinparam backgroundColor white

cloud "Internet" as inet

rectangle "Kubernetes Cluster" {
  agent ingress <<mxgraph.kubernetes.ing>> as "Ingress\nController"

  package "frontend-ns" {
    agent fe_deploy <<mxgraph.kubernetes.deploy>> as "Frontend\nDeployment"
    agent fe_svc <<mxgraph.kubernetes.svc>> as "Frontend\nService"
    agent fe_pod1 <<mxgraph.kubernetes.pod>> as "Pod 1"
    agent fe_pod2 <<mxgraph.kubernetes.pod>> as "Pod 2"
  }

  package "backend-ns" {
    agent api_deploy <<mxgraph.kubernetes.deploy>> as "API\nDeployment"
    agent api_svc <<mxgraph.kubernetes.svc>> as "API\nService"
    agent api_pod1 <<mxgraph.kubernetes.pod>> as "Pod 1"
    agent api_pod2 <<mxgraph.kubernetes.pod>> as "Pod 2"
    agent api_pod3 <<mxgraph.kubernetes.pod>> as "Pod 3"
    agent cm <<mxgraph.kubernetes.cm>> as "ConfigMap"
    agent sec <<mxgraph.kubernetes.secret>> as "DB Secret"
  }

  package "data-ns" {
    agent db_deploy <<mxgraph.kubernetes.deploy>> as "PostgreSQL\nStatefulSet"
    agent db_svc <<mxgraph.kubernetes.svc>> as "DB\nService"
    agent db_pv <<mxgraph.kubernetes.pv>> as "Persistent\nVolume"
  }
}

inet --> ingress
ingress --> fe_svc
fe_svc --> fe_pod1
fe_svc --> fe_pod2
fe_deploy ..> fe_pod1
fe_deploy ..> fe_pod2
fe_pod1 --> api_svc
api_svc --> api_pod1
api_svc --> api_pod2
api_svc --> api_pod3
api_deploy ..> api_pod1
api_pod1 --> db_svc
db_svc --> db_deploy
db_deploy --> db_pv
api_pod1 ..> cm
api_pod1 ..> sec
@enduml
```

## Template: Multi-Cloud / Hybrid Topology

```plantuml
@startuml
left to right direction
skinparam backgroundColor white

node "On-Premise Data Center" as onprem {
  agent ad as "Active\nDirectory"
  agent legacy_db as "Oracle DB\n(Legacy)"
}

rectangle "AWS" {
  agent eks <<mxgraph.aws4.eks>> as "EKS\nCluster"
  agent rds <<mxgraph.aws4.rds>> as "Aurora\nPostgreSQL"
  agent s3 <<mxgraph.aws4.s3>> as "S3\nData Lake"
}

rectangle "GCP" {
  agent gke <<mxgraph.gcp2.google_kubernetes_engine>> as "GKE\nML Cluster"
  agent bq <<mxgraph.gcp2.bigquery>> as "BigQuery\nAnalytics"
}

cloud "Internet" as inet

inet --> eks : "HTTPS"
eks --> rds : "TCP/5432"
eks --> s3 : "S3 API"
eks ..> gke : "gRPC"
gke --> bq : "BigQuery API"
s3 ..> bq : "Data Sync"
onprem --> eks : "VPN"
ad ..> eks : "LDAP/SAML"
legacy_db ..> rds : "DMS Migration"
@enduml
```

## Best Practices

1. **Group by network boundary** -- use `rectangle` for regions, VPCs, subnets, and AZs
2. **Use provider-specific icons** -- `mxgraph.aws4.*`, `mxgraph.azure.*`, `mxgraph.gcp2.*` for clarity
3. **Label connections with protocols** -- `HTTPS`, `gRPC`, `TCP/5432` on arrows
4. **Separate data plane from control plane** -- show management traffic as dashed arrows
5. **Show redundancy** -- include replicas, multi-AZ, and failover paths
6. **Use consistent naming** -- `<service>_<role>` pattern for IDs
7. **Output format** -- always output inside ` ```plantuml ` fenced code blocks
