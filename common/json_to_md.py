import json
from pytablewriter import MarkdownTableWriter

test = {
    "liveoak-sandbox (671758882420)": [
        {
            "us-east-1": [
                {
                    "Description": "default VPC security group",
                    "GroupId": "sg-0aec3619dacc91f3e",
                    "GroupName": "default",
                },
                {
                    "Description": "default VPC security group",
                    "GroupId": "sg-06862ff6d7a5e629f",
                    "GroupName": "default",
                },
                {
                    "Description": "Created from the RDS Management Console: 2020/06/18 13:42:08",
                    "GroupId": "sg-066715611da4b734a",
                    "GroupName": "rds-launch-wizard-1",
                },
                {
                    "Description": "managed LoadBalancer securityGroup by ALB Ingress Controller",
                    "GroupId": "sg-037c995d3f499ae42",
                    "GroupName": "bee29091-2048game-2048ingr-6fa0",
                },
                {
                    "Description": "For temporarily testing the tokbox proxy",
                    "GroupId": "sg-002b2143b1683156f",
                    "GroupName": "tokbox-testing-sg",
                },
                {
                    "Description": "Security group for Kubernetes ELB a7c4e36e4c38c4a01b2c02959658eca1 (kube-system/traefik)",
                    "GroupId": "sg-06a19893379801133",
                    "GroupName": "k8s-elb-a7c4e36e4c38c4a01b2c02959658eca1",
                },
                {
                    "Description": "managed LoadBalancer securityGroup by ALB Ingress Controller",
                    "GroupId": "sg-03c21e35bf6d54540",
                    "GroupName": "e6eaf167-2048game-2048ingr-6fa0",
                },
                {
                    "Description": "Communication between all nodes in the cluster",
                    "GroupId": "sg-03347790e48ed4bb6",
                    "GroupName": "eksctl-staging-cluster-ClusterSharedNodeSecurityGroup-4N98RSRAXHWP",
                },
                {
                    "Description": "default VPC security group",
                    "GroupId": "sg-0feeb0e8b8b035df8",
                    "GroupName": "default",
                },
                {
                    "Description": "lo-pritunl-vpn",
                    "GroupId": "sg-02d41fcd5f8e1a321",
                    "GroupName": "lo-pritunl-vpn",
                },
                {
                    "Description": "WEB traffic",
                    "GroupId": "sg-01d23bd2e6bef2d54",
                    "GroupName": "test-INFRA-389",
                },
                {
                    "Description": "default VPC security group",
                    "GroupId": "sg-0a5c3d6502956a674",
                    "GroupName": "default",
                },
                {
                    "Description": "default VPC security group",
                    "GroupId": "sg-059e89348d554e42f",
                    "GroupName": "default",
                },
                {
                    "Description": "default VPC security group",
                    "GroupId": "sg-0756e88ccfeb4253c",
                    "GroupName": "default",
                },
                {
                    "Description": "allow all outbound traffic",
                    "GroupId": "sg-068c592b19151e76c",
                    "GroupName": "allow all outbound",
                },
                {
                    "Description": "Communication between all nodes in the cluster",
                    "GroupId": "sg-0364c92fb26371500",
                    "GroupName": "eksctl-demo-cluster-ClusterSharedNodeSecurityGroup-K5KPWQ5VMEDX",
                },
                {
                    "Description": "[k8s] Managed SecurityGroup for LoadBalancer",
                    "GroupId": "sg-0e239987657db0d12",
                    "GroupName": "k8s-2048game-2048ingr-6537e819e0",
                },
                {
                    "Description": "Communication between the control plane and worker nodegroups",
                    "GroupId": "sg-0809946e260c12308",
                    "GroupName": "eksctl-staging-cluster-ControlPlaneSecurityGroup-1S81ZC0BVKTTE",
                },
                {
                    "Description": "launch-wizard-3 created 2020-12-09T16:31:25.249-06:00",
                    "GroupId": "sg-07aa1ee2a21c64eee",
                    "GroupName": "launch-wizard-3",
                },
                {
                    "Description": "Created from the RDS Management Console: 2020/06/18 13:30:30",
                    "GroupId": "sg-008521f7e3f40696b",
                    "GroupName": "rds-launch-wizard",
                },
                {
                    "Description": "Security group for all nodes in the cluster.",
                    "GroupId": "sg-0ecefc899e35d258d",
                    "GroupName": "loa-sandbox-use1-1a20220316215837375100000008",
                },
                {
                    "Description": "launch-wizard-4 created 2020-12-09T16:49:37.557-06:00",
                    "GroupId": "sg-03be0e9bbd8b8ae5b",
                    "GroupName": "launch-wizard-4",
                },
                {
                    "Description": "default VPC security group",
                    "GroupId": "sg-08c192abf2c2c3578",
                    "GroupName": "default",
                },
                {
                    "Description": "shared ssh",
                    "GroupId": "sg-0b80bbb0780e43080",
                    "GroupName": "ssh from shared public subnets",
                },
                {
                    "Description": "EKS created security group applied to ENI that is attached to EKS Control Plane master nodes, as well as any managed workloads.",
                    "GroupId": "sg-023959045fb11731d",
                    "GroupName": "eks-cluster-sg-staging-1897523141",
                },
                {
                    "Description": "launch-wizard-2 created 2020-11-06T14:55:39.728-08:00",
                    "GroupId": "sg-07f4be649a6abd5cf",
                    "GroupName": "launch-wizard-2",
                },
                {
                    "Description": "launch-wizard-1 created 2020-07-10T12:07:57.250-05:00",
                    "GroupId": "sg-0f468754c4f8f76fa",
                    "GroupName": "launch-wizard-1",
                },
                {
                    "Description": "Allows SSH connections and HTTP(s) connections from office",
                    "GroupId": "sg-090c1c57bd9667b29",
                    "GroupName": "lo-pritunl-whitelist",
                },
                {
                    "Description": "ssh from vpn",
                    "GroupId": "sg-0f7ab5537926a1773",
                    "GroupName": "ssh from vpn",
                },
                {
                    "Description": "default VPC security group",
                    "GroupId": "sg-0c0b88354acca1dba",
                    "GroupName": "default",
                },
                {
                    "Description": "Managed by Terraform",
                    "GroupId": "sg-041cac3e14249d14e",
                    "GroupName": "liveoaksandbox-rds-stg",
                },
                {
                    "Description": "managed LoadBalancer securityGroup by ALB Ingress Controller",
                    "GroupId": "sg-09c7e81d8b8efde04",
                    "GroupName": "bee29091-kubesystem-traefi-8c52",
                },
                {
                    "Description": "Security group for Kubernetes ELB ade0305bfdf6945f69292e19bd35f2e8 (kube-system/traefik)",
                    "GroupId": "sg-0b137419f2162959c",
                    "GroupName": "k8s-elb-ade0305bfdf6945f69292e19bd35f2e8",
                },
                {
                    "Description": "launch-wizard-2 created 2020-09-24T23:06:47.613-05:00",
                    "GroupId": "sg-0def3b9165a52ce2e",
                    "GroupName": "bam-sg",
                },
                {
                    "Description": "consul rules for communicating within shared vpc",
                    "GroupId": "sg-034c3efd3b3035aee",
                    "GroupName": "consul server",
                },
            ]
        },
        {
            "us-east-2": [
                {
                    "Description": "default VPC security group",
                    "GroupId": "sg-0842f8f2c443c3f89",
                    "GroupName": "default",
                },
                {
                    "Description": "hsm client",
                    "GroupId": "sg-0ceca379386c8470c",
                    "GroupName": "hsm-client",
                },
                {
                    "Description": "default VPC security group",
                    "GroupId": "sg-2a3c174f",
                    "GroupName": "default",
                },
            ]
        },
        {
            "eu-west-1": [
                {
                    "Description": "default VPC security group",
                    "GroupId": "sg-8adcf2c2",
                    "GroupName": "default",
                }
            ]
        },
        {
            "us-west-2": [
                {
                    "Description": "default VPC security group",
                    "GroupId": "sg-0c3ae44b",
                    "GroupName": "default",
                }
            ]
        },
    ]
}


data = []

for k, v in test.items():
    for i in v:
        if isinstance(i, dict):
            for region, b in i.items():
                # print(region)
                writer = MarkdownTableWriter()
                writer.table_name = region
                writer.headers = ["Group Name", "Group Id", "Description"]
                matrix = []
                if len(b) != 0:
                    for a in b:
                        values = []
                        description = a.get("Description", "")
                        group_id = a.get("GroupId", "")
                        group_name = a.get("GroupName", "")

                        values.append(group_name)
                        values.append(group_id)
                        values.append(description)
                        matrix.append(values)
                writer.value_matrix = matrix
                data.append(writer.dumps())

with open("report.md", "w") as out:
    for i in data:
        out.write("%s\n" % i)
