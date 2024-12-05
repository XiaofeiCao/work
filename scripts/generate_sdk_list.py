import argparse;
import glob;
import os;
import re;
import sys;
import datetime;
import yaml;

GROUP_ID = "com.azure.resourcemanager"
exclude_projects = (
    "azure-resourcemanager-samples",
    "azure-resourcemanager-test",
    "azure-resourcemanager",
    "azure-resourcemanager-perf",
    # service define two success response with different body: 
    # https://github.com/Azure/azure-rest-api-specs/pull/23172#issuecomment-1475702721
    "azure-resourcemanager-commerce",
    # service never fixed backend: https://github.com/Azure/azure-sdk-for-java/pull/42223#issuecomment-2401690656
    "azure-resourcemanager-azureadexternalidentities"
)
deprecated_projects = (
    "azure-resourcemanager-machinelearningservices",
    "azure-resourcemanager-loadtestservice",
    "azure-resourcemanager-batchai",
    "azure-resourcemanager-videoanalyzer",
    # specs deleted from repo, will be merged into security
    "azure-resourcemanager-securitydevops",
    # service decomissioned: https://github.com/Azure/azure-rest-api-specs/pull/26818
    "azure-resourcemanager-deploymentmanager"
)

readme_template = """
# MGMT SDK for azure-json migration

Generated At: {date_time}

## Summary

- total: {count}
- migrated: {migrated_count}
- need javadoc fix: {javadoc_fix}

## Detail

|Index|SDK|Version|Last Released|From|Migration Status|Tag|Swagger|Need Javadoc fix|
|--|--|--|--|--|--|--|--|--|"""

not_planned_template = """

## Not planned

### resourcemanagerhybrid

|Index|SDK|Version|Last Released|
|--|--|--|--|"""

def main():
    (parser, args) = parse_args()
    args = vars(args)
    sdk_root = args["sdk_root"]
    listing = glob.glob(f'{sdk_root}/sdk/*/azure-resourcemanager-*')
    sdk_to_swagger = get_sdk_to_swagger_mapping(sdk_root)
    packages = []
    resourcemanagerhybrid_packages = []
    for package_dir in listing:
        not_planned = False
        tag = ""
        version = ""
        package_dir_segments = package_dir.split("/")
        sdk_name = package_dir_segments[len(package_dir_segments) - 1]
        javadoc_fix = False

        if re.match(".*-generated", package_dir) or sdk_name in exclude_projects or sdk_name in deprecated_projects:
            continue
        if re.match(".*resourcemanagerhybrid.*", package_dir):
            not_planned = True
        if os.path.exists(os.path.join(package_dir, "tsp-location.yaml")):
            typespec = True
        else: 
            typespec = False

        module_info_file = os.path.join(package_dir, "src/main/java/module-info.java")
        if not os.path.exists(module_info_file):
             continue
        with open(module_info_file, "r") as fin:
            module_info_file_content = fin.read()
            if not module_info_file_content.__contains__("jackson"):
                migration_status = "MIGRATED"
            else: 
                migration_status = "NOT_MIGRATED"

        changelog_file = os.path.join(package_dir, "CHANGELOG.md")
        with open(changelog_file, "r") as fin:
            changelog_content = fin.read()
        
        last_release_date_regex = '## ([\\-|\w|\\.]+) \\(([\\-|\d]+)\\)'
        search_result = re.search(last_release_date_regex, changelog_content)
        version = search_result.group(1)
        last_release_date = search_result.group(2)

        if not typespec:
            package_tag_regex = " Package tag ([\\-|\w]+)\\."
            tag_search_result = re.search(package_tag_regex, changelog_content)
            if tag_search_result:
                tag = tag_search_result.group(1)

        pom_file = os.path.join(package_dir, "pom.xml")
        with open(pom_file, "r") as fin:
            pom_content = fin.read()
            if pom_content.__contains__("<doclintMissingInclusion>-</doclintMissingInclusion>"):
                javadoc_fix = True

        swagger = "" if typespec else sdk_to_swagger[sdk_name] if sdk_to_swagger.__contains__(sdk_name) else sdk_name.split("-")[len(sdk_name.split("-"))-1]
        if package_dir.__contains__("sdk/resourcemanager"):
            swagger = ""

        if not_planned:
            resourcemanagerhybrid_packages.append({
                "sdk_name": sdk_name,
                "version": version,
                "last_release_date": last_release_date
            })
        else: 
            packages.append({
                "sdk_name": sdk_name,
                "version": version,
                "last_release_date": last_release_date,
                "from": "TypeSpec" if typespec else "Swagger",
                "migration_status": migration_status,
                "swagger": swagger,
                "package_tag": tag if not typespec else "",
                "javadoc_fix": javadoc_fix
            })
    
    packages.sort(key=lambda package: package["last_release_date"])

    table_content = readme_template\
        .replace("{count}", f'{len(packages)}')\
        .replace("{migrated_count}", f'{len([p for p in packages if p["migration_status"] == "MIGRATED"])}')\
        .replace("{date_time}", f'{datetime.datetime.now()}')\
        .replace("{javadoc_fix}", f'{len([p for p in packages if p["javadoc_fix"] == True])}')

    index=1
    for package in packages:
        migration_status = ":white_check_mark:" if package["migration_status"] == "MIGRATED" else ":white_large_square:"
        table_content += f'\n|{index}| {package["sdk_name"]} | {package["version"]} | {package["last_release_date"]} | {package["from"]} | { migration_status } | {package["package_tag"]} | {package["swagger"]} | {package["javadoc_fix"]} |'
        index+=1
    table_content += not_planned_template
    index=1
    for hybridsdk in resourcemanagerhybrid_packages:
        table_content += f'\n|{index}| {hybridsdk["sdk_name"]} | {hybridsdk["version"]} | {hybridsdk["last_release_date"]} |'
        index+=1
    with open(os.path.join(sys.path[0], "../sdk_list.md"), "w") as fout:
        fout.write(table_content)


def get_sdk_to_swagger_mapping(sdk_root: str) -> dict:
    result: dict = {}
    api_specs_file = os.path.join(sdk_root, "eng/automation/api-specs.yaml")
    with open(api_specs_file) as fin:
        api_specs = yaml.safe_load(fin)
    for service in api_specs:
        swagger=service
        if service.__contains__("/"):
            service_segments = service.split("/")
            service_segments.insert(0, "specification")
            service_segments.insert(2, "resource-manager")
            swagger = "/".join(service_segments) + "/readme.md"
        if api_specs[service].__contains__("suffix"):
            if api_specs[service]["suffix"] == "generated":
                continue
            elif api_specs[service].__contains__("service"):
                result[f'azure-resourcemanager-{api_specs[service]["service"]}-{api_specs[service]["suffix"]}'] = swagger
        elif api_specs[service].__contains__("service"):
            result[f'azure-resourcemanager-{api_specs[service]["service"]}'] = swagger
    return result


def parse_args() -> (argparse.ArgumentParser, argparse.Namespace):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sdk-root",
        help="azure-sdk-for-java root folder",
    )

    return (parser, parser.parse_args())

if __name__ == "__main__":
    main()