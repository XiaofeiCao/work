import argparse;
import glob;
import os;
import re;

GROUP_ID = "com.azure.resourcemanager"

def main():
    (parser, args) = parse_args()
    args = vars(args)
    sdk_root = args["sdk_root"]
    listing = glob.glob(f'{sdk_root}/sdk/*/azure-resourcemanager-*')
    version_client_file = os.path.join(sdk_root, "eng/versioning/version_client.txt")
    version_client_content = None
    with open(version_client_file, "r") as fin:
            version_client_content = fin.read()

    table_content = """
    |index|sdk|version|lastReleased|\n
    |--|--|--|--|
    """
    count=0
    for package_dir in listing:
        if os.path.exists(os.path.join(package_dir, "tsp-location.yaml")) \
            or re.match(f'{sdk_root}/sdk/resourcemanager.*', package_dir) or re.match(".*-generated", package_dir):
                continue

        pom_file = os.path.join(package_dir, "pom.xml")
        if not os.path.exists(pom_file):
             continue
        with open(pom_file, "r") as fin:
            pom_content = fin.read()
            if pom_content.__contains__("azure-json"):
                 continue
        
        package_dir_segments = package_dir.split("/")
        sdk_name = package_dir_segments[len(package_dir_segments) - 1]

        version_regex = f'{GROUP_ID}:{sdk_name};([\\-|\w|\\.]+);[\\-|\w|\\.]+'
        version = re.search(version_regex, version_client_content).group(1)

        changelog_file = os.path.join(package_dir, "CHANGELOG.MD")
        with open(changelog_file, "r") as fin:
            changelog_content = fin.read()
        
        last_release_date_regex = f'## {version} \\(([\\-|\d]+)\\)'
        last_release_date = re.search(last_release_date_regex, changelog_content).group(1)
        print(last_release_date)

        print(sdk_name)
        count=count+1
        table_content += f'\n| {count} | {sdk_name} | {version} | {last_release_date} |'
    print(count)
    print(table_content)
    

def parse_args() -> (argparse.ArgumentParser, argparse.Namespace):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sdk-root",
        help="azure-sdk-for-java root folder",
    )

    return (parser, parser.parse_args())

if __name__ == "__main__":
    main()