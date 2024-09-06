import argparse;
import glob;
import os;
import re;
import sys;
import datetime;

GROUP_ID = "com.azure.resourcemanager"
exclude_projects = (
    "azure-resourcemanager-samples",
    "azure-resourcemanager-test",
    "azure-resourcemanager",
    "azure-resourcemanager-perf"
)

readme_template = """
# MGMT SDK for azure-json migration

Generated At: {date_time}

## Summary

- total: {count}
- migrated: {migrated_count}

## Detail

|Index|SDK|Version|Last Released|TypeSpec|Migration Status|
|--|--|--|--|--|--|"""

def main():
    (parser, args) = parse_args()
    args = vars(args)
    sdk_root = args["sdk_root"]
    listing = glob.glob(f'{sdk_root}/sdk/*/azure-resourcemanager-*')
    packages = []
    for package_dir in listing:
        package_dir_segments = package_dir.split("/")
        sdk_name = package_dir_segments[len(package_dir_segments) - 1]
        print(sdk_name)
        if re.match(".*-generated", package_dir) or sdk_name in exclude_projects:
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

        packages.append({
            "sdk_name": sdk_name,
            "version": version,
            "last_release_date": last_release_date,
            "typespec": "true" if typespec else "false",
            "migration_status": migration_status
        })
    
    packages.sort(key=lambda package: package["last_release_date"])

    table_content = readme_template\
        .replace("{count}", f'{len(packages)}')\
        .replace("{migrated_count}", f'{len([p for p in packages if p["migration_status"] == "MIGRATED"])}')\
        .replace("{date_time}", f'{datetime.datetime.now()}')

    index=1;
    for package in packages:
        table_content += f'\n|{index}| {package["sdk_name"]} | {package["version"]} | {package["last_release_date"]} | {package["typespec"]} | {package["migration_status"] } |'
        index+=1
    with open(os.path.join(sys.path[0], "../sdk_list.md"), "w") as fout:
        fout.write(table_content)
    

def parse_args() -> (argparse.ArgumentParser, argparse.Namespace):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sdk-root",
        help="azure-sdk-for-java root folder",
    )

    return (parser, parser.parse_args())

if __name__ == "__main__":
    main()