from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.cloudformation.checks.resource.base_resource_check import BaseResourceCheck

"""
Based on AbsSecurityGroupUnrestricedIngress class
The ALLSecurityGroupUnrestrictedIngress returns FAIL when any port allows 0.0.0.0:0

"""


class AllSecurityGroupUnrestrictedIngress(BaseResourceCheck):
    def __init__(self, check_id):
        name = "Ensure no security groups allow any ingress to any port 20, 21, 23, and 80"
        supported_resources = [
            "AWS::EC2::SecurityGroup",
            "AWS::EC2::SecurityGroupIngress",
        ]
        self.insecure_ports = [20,21,23,80]
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
                    if int(rule["FromPort"]) == int(rule["ToPort"]) and int(rule["FromPort"]) in self.insecure_ports:
                        return CheckResult.FAILED
        return CheckResult.PASSED


AllSecurityGroupUnrestrictedIngress("CUSTOM_AWS_NET1")
