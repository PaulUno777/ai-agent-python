from functions.get_files_info import get_files_info


def print_result(label, result):
    print(f"Result for {label} directory:")
    indent = "    " if result.startswith("Error:") else "  "
    for line in result.splitlines():
        print(f"{indent}{line}")


print_result("current", get_files_info("calculator", "."))
print_result("'pkg'", get_files_info("calculator", "pkg"))
print_result("'/bin'", get_files_info("calculator", "/bin"))
print_result("'../'", get_files_info("calculator", "../"))
