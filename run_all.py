# run_all.py
import subprocess
from utils.excel_reader import excel_to_json


def main():
    # 1) Excel -> JSON
    excel_to_json("data/TestData.xlsx", "data/json/cases.json")

    # 2) Run pytest + Allure
    subprocess.run(
        ["pytest", "--alluredir=allure-results"],
        check=False
    )

    print("Done. Use Allure or CI to publish the report.")


if __name__ == "__main__":
    main()
