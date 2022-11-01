from checkov.cloudformation.checks.resource.aws.AbsSecurityGroupUnrestrictedIngress import (
    AbsSecurityGroupUnrestrictedIngress,
)


class SecurityGroupUnrestrictedIngressAny(AbsSecurityGroupUnrestrictedIngress):
    def __init__(self, check_id, test_port):
        super().__init__(check_id=check_id, port=test_port)


for port in [25, 443, 2222]:
    SecurityGroupUnrestrictedIngressAny(
        check_id=f"CKV_AWS_CUSTOM_PORT{port}", test_port=port
    )
