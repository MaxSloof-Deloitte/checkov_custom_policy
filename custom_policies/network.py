from checkov.cloudformation.checks.resource.aws.AbsSecurityGroupUnrestrictedIngress import (
    AbsSecurityGroupUnrestrictedIngress,
)


class SecurityGroupUnrestrictedIngress1234(AbsSecurityGroupUnrestrictedIngress):
    def __init__(self):
        super().__init__(check_id="CKV_AWS_MAX1", port=1234)


check = SecurityGroupUnrestrictedIngress1234()


class SecurityGroupUnrestrictedIngress443(AbsSecurityGroupUnrestrictedIngress):
    def __init__(self):
        super().__init__(check_id="CKV_AWS_MAX2", port=443)


check = SecurityGroupUnrestrictedIngress443()
