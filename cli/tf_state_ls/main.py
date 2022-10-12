import argparse
import json

import boto3


def args():
    parser = argparse.ArgumentParser()


def get_state_s3(bucket_name, filename):
    session = boto3.Session()
    s3 = session.resource("s3")
    obj = s3.Object(bucket_name, filename)
    filecontent = obj.get()["Body"].read().decode("utf-8")

    return json.loads(filecontent)


def list_resources(resources):
    for resource in resources:
        data = ""
        resource_mode = resource["mode"]
        resource_module = resource.get("module", None)
        resource_type = resource["type"]
        resource_name = resource["name"]

        if resource_mode == "data":
            data = resource_mode + "." + resource_type + "." + resource_name
        elif resource_mode == "managed":
            if resource_module:
                data = resource_module + "." + resource_type + "." + resource_name
            else:
                data = resource_type + "." + resource_name

        print(f"{data}")


def show_resource(resources, search):
    search_keywords = search.split(".")
    print(search_keywords)
    if len(search_keywords) != 0:
        if search_keywords[0] == "data":
            resource = list(
                filter(
                    lambda x: x["mode"] == search_keywords[0]
                    and x["type"] == search_keywords[1]
                    and x["name"] == search_keywords[2],
                    resources,
                ),
            )
        elif "module" in search_keywords[0]:
            module = search_keywords[0] + "." + search_keywords[1]
            resource = list(
                filter(
                    lambda x: x["module"] == module
                    and x["type"] == search_keywords[2]
                    and x["name"] == search_keywords[3],
                    resources,
                ),
            )
        print(resource)


def main():
    bucket_name = "terraform-tools-staging-us"
    filename = "tools-staging-us-cdp-tools-confluence.tfstate"

    statefile = get_state_s3(bucket_name, filename)
    resources = statefile["resources"]
    list_resources(resources)
    show_resource(resources, "data.aws_caller_identity.current")
    # show_resource(resources, "module.confluence-alb.aws_acm_certificate.default_cert")


if __name__ == "__main__":
    main()
