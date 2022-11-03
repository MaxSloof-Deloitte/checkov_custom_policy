from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.cloudformation.checks.resource.base_resource_check import BaseResourceCheck

"""
This policy checks whether an ingress rule in a NACL allows 0.0.0.0/0 over a certain port
This is done by either checking whether access to that port has specifically been allowed, 
or whether traffic over all ports has been allowed

"""


class NACLCheck(BaseResourceCheck):
    def __init__(self, check_id, port):
        name = f"Ensure no Network ACLs allow ingress from 0.0.0.0:0 to port {port}"
        supported_resources = [
            "AWS::EC2::NetworkAclEntry",
        ]
        categories = [CheckCategories.NETWORKING]
        self.port = port
        super().__init__(
            name=name,
            id=check_id,
            categories=categories,
            supported_resources=supported_resources,
        )

    def scan_resource_conf(self, conf):

        rules = []
        if conf["Type"] == "AWS::EC2::NetworkAclEntry":
            if "Properties" in conf.keys():
                rules.append(conf["Properties"])

        if not isinstance(rules, list):
            return CheckResult.UNKNOWN

        for rule in rules:
            if rule["Egress"] == False:

                if rule["RuleAction"] == "allow":
                    try:
                        if rule["PortRange"].__contains__("From") and rule[
                            "PortRange"
                        ].__contains__("To"):

                            if int(rule["PortRange"]["From"]) == int(self.port) and int(
                                rule["PortRange"]["To"]
                            ) == int(self.port):
                                if (
                                    "CidrBlock" in rule.keys()
                                    and rule["CidrBlock"] == "0.0.0.0/0"
                                ):  # nosec  # nosec
                                    return CheckResult.FAILED
                                elif "CidrBlock" in rule.keys() and rule[
                                    "CidrBlock"
                                ] in [
                                    "::/0",
                                    "0000:0000:0000:0000:0000:0000:0000:0000/0",
                                ]:
                                    return CheckResult.FAILED
                    except:
                        if "PortRange" not in rule.keys():
                            if (
                                "CidrBlock" in rule.keys()
                                and rule["CidrBlock"] == "0.0.0.0/0"
                            ):  # nosec  # nosec
                                return CheckResult.FAILED
                            elif "CidrBlock" in rule.keys() and rule["CidrBlock"] in [
                                "::/0",
                                "0000:0000:0000:0000:0000:0000:0000:0000/0",
                            ]:
                                return CheckResult.FAILED
        return CheckResult.PASSED


for port in [22, 3389]:
    NACLCheck(f"CUSTOM_AWS_NET_NACL{port}", port)
