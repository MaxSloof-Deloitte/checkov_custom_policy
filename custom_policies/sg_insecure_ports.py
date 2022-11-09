from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.cloudformation.checks.resource.base_resource_check import BaseResourceCheck

"""
Based on AbsSecurityGroupUnrestricedIngress class
The ALLSecurityGroupUnrestrictedIngress returns FAIL when any port allows 0.0.0.0:0

"""


class MultiplePortsAnyIngressSecurityGroup(BaseResourceCheck):
    def __init__(self, check_id, port_list):
        name = f"Ensure no security groups allow any ingress to any insecure ports ({', '.join(str(port)for port in port_list)})"
        supported_resources = [
            "AWS::EC2::SecurityGroup",
            "AWS::EC2::SecurityGroupIngress",
        ]
        self.port_list = port_list
        categories = [CheckCategories.NETWORKING]
        super().__init__(
            name=name,
            id=check_id,
            categories=categories,
            supported_resources=supported_resources,
        )

    def scan_resource_conf(self, conf):

        rules = []
        if conf["Type"] == "AWS::EC2::SecurityGroup":
            if "Properties" in conf.keys():
                if "SecurityGroupIngress" in conf["Properties"].keys():
                    rules = conf["Properties"]["SecurityGroupIngress"]
        elif conf["Type"] == "AWS::EC2::SecurityGroupIngress":
            if "Properties" in conf.keys():
                rules = []
                rules.append(conf["Properties"])

        if not isinstance(rules, list):
            return CheckResult.UNKNOWN

        for rule in rules:
            if rule.__contains__("FromPort") and rule.__contains__("ToPort"):
                if isinstance(rule["FromPort"], int) and isinstance(
                    rule["ToPort"], int
                ):
                    if (
                        int(rule["FromPort"]) == int(rule["ToPort"])
                        and int(rule["FromPort"]) in self.port_list
                    ):
                        return CheckResult.FAILED
        return CheckResult.PASSED


MultiplePortsAnyIngressSecurityGroup("CUSTOM_AWS_NET1", port_list=[20, 21, 23, 80])
