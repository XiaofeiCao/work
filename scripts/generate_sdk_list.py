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
    "azure-resourcemanager-perf"
)
deprecated_projects = (
    "azure-resourcemanager-machinelearningservices",
    "azure-resourcemanager-loadtestservice",
    "azure-resourcemanager-batchai"
)

readme_template = """
# MGMT SDK for azure-json migration

Generated At: {date_time}

## Summary

- total: {count}
- migrated: {migrated_count}

## Detail

|Index|SDK|Version|Last Released|TypeSpec|Swagger|Migration Status|
|--|--|--|--|--|--|--|"""

def main():
    (parser, args) = parse_args()
    args = vars(args)
    sdk_root = args["sdk_root"]
    listing = glob.glob(f'{sdk_root}/sdk/*/azure-resourcemanager-*')
    sdk_to_swagger = get_sdk_to_swagger_mapping(sdk_root)
    packages = []
    for package_dir in listing:
        package_dir_segments = package_dir.split("/")
        sdk_name = package_dir_segments[len(package_dir_segments) - 1]

        if re.match(".*-generated", package_dir) or sdk_name in exclude_projects or sdk_name in deprecated_projects:
            continue
        if os.path.exists(os.path.join(package_dir, "tsp-location.yaml")):
            typespec = True
        else: 
            typespec = False

        module_info_file = os.path.join(package_dir, "src/main/java/module-info.java")
        if not os.path.exists(module_info_file):
             continue
        with open(module_info_file, "r") as fin:
            pom_content = fin.read()
            if not pom_content.__contains__("jackson"):
                migration_status = "MIGRATED"
            else: 
                migration_status = "NOT_MIGRATED"

        changelog_file = os.path.join(package_dir, "CHANGELOG.md")
        with open(changelog_file, "r") as fin:
            changelog_content = fin.read()
        
        last_release_date_regex = f'## ([\\-|\w|\\.]+) \\(([\\-|\d]+)\\)'
        search_result = re.search(last_release_date_regex, changelog_content)
        version = search_result.group(1)
        last_release_date = search_result.group(2)

        swagger = "" if typespec else sdk_to_swagger[sdk_name] if sdk_to_swagger.__contains__(sdk_name) else sdk_name.split("-")[len(sdk_name.split("-"))-1]
        if package_dir.__contains__("sdk/resourcemanager"):
            swagger = ""

        packages.append({
            "sdk_name": sdk_name,
            "version": version,
            "last_release_date": last_release_date,
            "typespec": "yes" if typespec else "no",
            "migration_status": migration_status,
            "swagger": swagger
        })
    
    packages.sort(key=lambda package: package["last_release_date"])

    table_content = readme_template\
        .replace("{count}", f'{len(packages)}')\
        .replace("{migrated_count}", f'{len([p for p in packages if p["migration_status"] == "MIGRATED"])}')\
        .replace("{date_time}", f'{datetime.datetime.now()}')

    index=1
    for package in packages:
        table_content += f'\n|{index}| {package["sdk_name"]} | {package["version"]} | {package["last_release_date"]} | {package["typespec"]} | {package["swagger"]} | {package["migration_status"] } |'
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
            swagger = "/".join(service_segments)
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