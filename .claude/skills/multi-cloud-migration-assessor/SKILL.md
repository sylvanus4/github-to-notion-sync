---
name: msp-multi-cloud-migration-assessor
description: >-
  MSP migration impact assessment: discover assets in the source cloud account
  (compute, databases, storage, networking, containers, identity), map
  inter-resource dependencies, analyze cross-cloud service compatibility,
  score risk across 6 dimensions (data loss, downtime, compatibility,
  compliance, cost, security), estimate effort and cost, and produce a
  structured migration assessment report with phased migration plan outline —
  all read-only (Tier 1), zero infrastructure changes. Composes
  compliance-governance for regulatory gap analysis and evaluation-engine for
  readiness scoring. Use when the user asks to assess cloud migration,
  migration impact assessment, cloud migration readiness, cross-cloud
  migration analysis, migration feasibility study, or needs a structured
  assessment before migrating workloads between AWS and GCP (or within the
  same provider). Do NOT use for executing any migration steps (creating
  resources, transferring data, modifying DNS), Terraform module generation
  for target infra (use msp-terraform-module-generator), daily infrastructure
  operations without migration context, or cost-only analysis without
  migration scope (use msp-cost-anomaly-explainer). Korean triggers: 클라우드
  마이그레이션 평가, 마이그레이션 영향 분석, 멀티클라우드 이관 평가, 마이그레이션 준비도 평가, 워크로드 이관 분석.
---

# Multi-Cloud Migration Impact Assessor

## Usage

- A customer is considering migrating workloads from AWS to GCP or vice versa
- Intra-cloud migration assessment needed (region-to-region, account consolidation)
- Pre-migration due diligence required before a migration project starts
- Customer requests a migration feasibility study with effort/cost estimates
- `/msp-migration-assess` with source account and target cloud

## Prerequisites

- Source cloud: Read access to all resource discovery APIs
- AWS: EC2, RDS, S3, EKS, Lambda, IAM, VPC, Route53, Config
- GCP: Compute Engine, Cloud SQL, GCS, GKE, Cloud Functions, IAM, VPC, Cloud DNS
- `tenant_id`, source `account_id`/`project_id`, `target_cloud`
- `migration_scope` (full-account or specific-workloads)

## Workflow

### Step 1 — Asset Discovery (Parallel Fan-out)

Launch 4 parallel discovery agents:

#### Agent 1 — Compute & Serverless
```
AWS path:
  EC2 DescribeInstances (all regions enabled)
  Lambda ListFunctions
  ECS ListClusters + ListServices
  EKS DescribeCluster + ListNodegroups
  Collect: instance types, AMIs, runtimes, container images, K8s versions

GCP path:
  Compute Engine instances.list (all zones)
  Cloud Functions ListFunctions
  Cloud Run ListServices
  GKE DescribeClusters + NodePools
  Collect: machine types, images, runtimes, container images, K8s versions
```

#### Agent 2 — Data Resources
```
AWS path:
  RDS DescribeDBInstances + DescribeDBClusters
  DynamoDB ListTables + DescribeTable
  S3 ListBuckets + GetBucketMetrics
  EBS DescribeVolumes
  ElastiCache DescribeCacheClusters
  Collect: engine versions, storage volumes, access patterns

GCP path:
  Cloud SQL ListInstances
  Firestore/Bigtable ListInstances
  Cloud Storage ListBuckets + GetMetrics
  Persistent Disk list
  Memorystore ListInstances
  Collect: engine versions, storage volumes, access patterns
```

#### Agent 3 — Networking & DNS
```
AWS path:
  VPC DescribeVpcs, DescribeSubnets, DescribeRouteTables
  Transit Gateway, Direct Connect, VPN connections
  Route 53 ListHostedZones + ListResourceRecordSets
  ELB/ALB/NLB DescribeLoadBalancers
  Collect: CIDR ranges, peering, hybrid connectivity, DNS records

GCP path:
  VPC Networks, Subnets
  Cloud Interconnect, Cloud VPN
  Cloud DNS ListManagedZones + ListResourceRecordSets
  Load Balancers (HTTP(S), TCP, Internal)
  Collect: CIDR ranges, peering, hybrid connectivity, DNS records
```

#### Agent 4 — Identity & Security
```
AWS path:
  IAM ListRoles, ListPolicies, ListUsers
  SAML/OIDC identity providers
  KMS ListKeys
  Collect: role count, policy complexity, federation setup

GCP path:
  IAM bindings per project
  Service accounts ListServiceAccounts
  Workload Identity configurations
  Cloud KMS ListKeyRings
  Collect: binding count, SA complexity, federation setup
```

### Step 2 — Dependency Mapping

```
Analyze inter-resource connections:
  - Network: Security Group / Firewall rules referencing other resources
  - Data: Which compute accesses which databases/storage
  - API: Service-to-service calls (from CloudTrail/Audit Logs patterns)
  - Auth: IAM roles assumed by which services

Identify:
  - Circular dependencies (resources that must migrate together as a group)
  - External dependencies (SaaS services, on-prem systems, third-party APIs)
  - Migration order constraints (database before application, etc.)

Output: dependency_map with service_dependencies, external_dependencies,
        circular_dependencies
```

### Step 3 — Compatibility Analysis

```
Map each source service to target cloud equivalent using service mapping table:

Full compatibility (lift-and-shift):
  EC2 ↔ Compute Engine, RDS MySQL/PostgreSQL ↔ Cloud SQL,
  S3 ↔ Cloud Storage, EKS ↔ GKE, Route 53 ↔ Cloud DNS

Partial compatibility (re-platform):
  Aurora ↔ AlloyDB/Cloud SQL, Lambda ↔ Cloud Functions/Cloud Run,
  SQS/SNS ↔ Pub/Sub, CloudFormation ↔ Terraform

No direct equivalent (re-architect):
  DynamoDB ↔ Firestore/Bigtable (data model change),
  IAM (policy model differs significantly)

For each resource:
  - Determine migration method: lift-and-shift / re-platform / re-architect
  - Identify specific compatibility gaps
  - Estimate data migration requirements (volume, method, downtime)
```

### Step 4 — Risk Assessment

```
Score 6 risk dimensions (CRITICAL/HIGH/MEDIUM/LOW):

data_loss_risk:
  Backup status, replication configuration, data validation requirements

downtime_risk:
  Stateful services, cut-over complexity, DNS propagation

compatibility_risk:
  No-equivalent services, version gaps, API differences

compliance_risk:
  Run compliance-governance for data residency, regulatory requirements
  Check target cloud certifications match source

cost_risk:
  Pricing model differences, reserved instance loss, data transfer costs

security_risk:
  IAM model translation complexity, encryption key portability,
  network security policy translation

Calculate overall_risk from highest individual dimension
```

### Step 5 — Effort & Cost Estimation

```
Effort estimate:
  - Person-days per resource category (based on migration method)
  - Phases: preparation, migration, validation, cutover, cleanup
  - Critical path duration (dependency-constrained)
  - Parallel execution tracks

Cost estimate:
  - Data transfer egress costs (source cloud → target cloud)
  - Temporary parallel running costs (both environments active)
  - Tooling costs (migration services, DMS, etc.)
  - Professional services estimate
  - Target monthly running cost projection
  - Break-even calculation (months until migration cost is recovered)
```

### Step 6 — Migration Plan Outline

```
Recommend approach:
  big-bang: Small environments, simple dependencies → single cutover weekend
  phased: Complex environments → migrate by workload groups over weeks/months
  hybrid: Critical services phased, non-critical in batches

Define phases based on dependency map:
  Phase 1: Non-dependent, stateless services
  Phase 2: Database migration with replication
  Phase 3: Stateful application cutover
  Phase 4: DNS cutover and traffic shift
  Phase 5: Decommission source resources

Per phase: workloads, duration, rollback strategy
List prerequisites and go/no-go criteria
```

### Step 7 — Report Assembly

```
Compile all sections:
  asset_inventory, dependency_map, compatibility_analysis,
  risk_assessment, effort_estimate, cost_estimate, migration_plan_outline

Run evaluation-engine for completeness and quality scoring
Generate executive summary with overall risk and recommendation
Produce structured JSON + markdown summary
```

## Cross-Cloud Service Mapping Reference

| AWS | GCP | Compatibility | Migration Method |
|-----|-----|---------------|------------------|
| EC2 | Compute Engine | Full | Lift-and-shift (image conversion) |
| RDS MySQL/PostgreSQL | Cloud SQL | Full | DMS / native replication |
| RDS Aurora | Cloud SQL / AlloyDB | Partial | Re-platform |
| DynamoDB | Firestore / Bigtable | Partial | Re-architect (data model) |
| S3 | Cloud Storage | Full | gsutil / Storage Transfer |
| EKS | GKE | Full | K8s manifest migration |
| Lambda | Cloud Functions / Cloud Run | Partial | Runtime adaptation |
| Route 53 | Cloud DNS | Full | Record export/import |
| IAM | Cloud IAM | Partial | Policy translation |
| CloudFormation | Terraform | Partial | IaC rewrite |

## Output Schema

```json
{
  "schema_version": "1.0.0",
  "skill": "multi-cloud-migration-assessor",
  "source": {"cloud": "", "account_id": "", "region": ""},
  "target": {"cloud": "", "region": ""},
  "asset_inventory": {"total_resources": 0, "by_type": {}, "total_data_volume_gb": 0},
  "dependency_map": {"service_dependencies": [], "external_dependencies": [], "circular_dependencies": []},
  "compatibility_analysis": {"direct_equivalent": [], "no_equivalent": [], "data_migration": []},
  "risk_assessment": {"overall_risk": "", "risk_factors": [], "compliance_gaps": []},
  "effort_estimate": {"total_person_days": 0, "critical_path_days": 0, "phases": []},
  "cost_estimate": {"migration_cost": {}, "target_monthly_cost": 0, "break_even_months": 0},
  "migration_plan_outline": {"recommended_approach": "", "phases": [], "prerequisites": []},
  "audit_entry": {"skill_version": "1.0.0", "tier": 1, "mutations": []}
}
```

## Governance

**Tier 1 — Read-only discovery and analysis.** No infrastructure changes.

Prohibited:
- Creating or modifying any cloud resources in source or target
- Initiating data transfer or replication
- Modifying DNS records
- Changing IAM policies, roles, or bindings
- Creating migration infrastructure (DMS instances, VPN tunnels)
- Executing any migration steps

## Error Handling

| Error | Recovery |
|-------|----------|
| Region not enabled for discovery | Report scanned vs unscanned regions; note coverage gap |
| API rate limiting during asset discovery | Exponential backoff; paginate large result sets; report partial results |
| Cross-account resources detected | Scope to authorized accounts; flag for human review |
| Unknown/new service types | Classify as "other" with raw API data; flag for manual mapping |
| Large environment (>5000 resources) | Enable pagination; aggregate by category; warn about longer processing |

## Subagent Contract

When invoked via `Task`:
- Caller provides: `tenant_id`, `source_account_id`/`source_project_id`, `target_cloud`, `migration_scope`, `correlation_id`
- Optional: `target_region`, `workload_filter`, `compliance_requirements`, `budget_constraint`
- Returns: Full JSON output with all assessment sections
