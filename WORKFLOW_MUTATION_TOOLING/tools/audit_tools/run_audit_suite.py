import sys

import circular_dependency_audit
import cross_package_dependency_audit
import duplicate_module_audit
import facade_bypass_audit
import file_size_audit
import header_schema_audit
import import_surface_audit
import module_path_ambiguity_audit
import namespace_shadow_audit
import orphan_module_audit
import runtime_entry_audit
import symbol_collision_audit
import unused_import_audit


def run(target):

    import_surface_audit.run(target)
    circular_dependency_audit.run(target)
    header_schema_audit.run(target)
    unused_import_audit.run(target)
    duplicate_module_audit.run(target)
    file_size_audit.run(target)
    runtime_entry_audit.run(target)
    orphan_module_audit.run(target)
    symbol_collision_audit.run(target)
    cross_package_dependency_audit.run(target)
    namespace_shadow_audit.run(target)
    module_path_ambiguity_audit.run(target)
    facade_bypass_audit.run(target)

if __name__=="__main__":

    target=sys.argv[1]

    run(target)
