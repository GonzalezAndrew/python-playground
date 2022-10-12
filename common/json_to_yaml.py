import yaml
import json

json_str = """
{
    "liveoak-sandbox": {
        "us-east-1": {
            "unused-security-groups": [
                {
                    "GroupName": "default",
                    "GroupId": "sg-0aec3619dacc91f3e"
                },
                {
                    "GroupName": "default",
                    "GroupId": "sg-06862ff6d7a5e629f"
                },
                {
                    "GroupName": "rds-launch-wizard-1",
                    "GroupId": "sg-066715611da4b734a"
                },
                {
                    "GroupName": "bee29091-2048game-2048ingr-6fa0",
                    "GroupId": "sg-037c995d3f499ae42"
                },
                {
                    "GroupName": "tokbox-testing-sg",
                    "GroupId": "sg-002b2143b1683156f"
                }
            ]
        },
        "us-east-2": {

        }
    }
}
"""

json_dict = {
    "liveoak-dev": {
        "us-east-1": {
            "unused-security-groups": [
                {"GroupName": "default", "GroupId": "sg-035b8f8557cb115b3"},
                {"GroupName": "default", "GroupId": "sg-142dbe5e"},
                {
                    "GroupName": "EC2ContainerService-default-EcsSecurityGroup-80SC5Y9CS7MQ",
                    "GroupId": "sg-06983ed793f7f8b7e",
                },
            ]
        }
    }
}

json_payload = json.loads(json_str)
test = json.loads(json.dumps(json_dict))
yaml_payload = yaml.dump(json_payload, sort_keys=False)
print(yaml_payload)
print(type(json_dict))
print(type(json_payload))

data = {}
test_2 = "testing"
test_3 = "testing2"
data[test_2] = {}
data[test_2][test_3] = {"1": 1}
