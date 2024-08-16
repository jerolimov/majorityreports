import json
from pydantic_yaml import to_yaml_str

from v1alpha1.namespace import (
    NamespaceQuery,
    NamespaceFilter,
    Namespace,
    NamespaceMeta,
    NamespaceSpec,
    NamespaceList,
    ListMeta,
)

nq = NamespaceQuery(
    filter=NamespaceFilter(
        labelSelector={
            "testdata": "yeah",
        },
    ),
    exclude=NamespaceFilter(
        names=["asdasd"],
    ),
)

n = Namespace(
    meta=NamespaceMeta(
        name="asd",
        labels={
            "testdata": "yeah",
        },
    ),
    spec=NamespaceSpec(),
)

nl = NamespaceList(
    meta=ListMeta(),
    items=[n],
)

print()
print("query:")
print(nq.model_dump_json(indent=2, exclude_none=True))
print
print("n", n)
print()
print("json schema:")
print(json.dumps(NamespaceQuery.model_json_schema(), indent=2))
print()
print("json:")
print(nl.model_dump_json(indent=2, exclude_none=True))
print()
print("yaml:")
print(to_yaml_str(nl, exclude_none=True))
