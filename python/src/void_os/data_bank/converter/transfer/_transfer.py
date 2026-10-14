"""how the input's relations become relations in normal form"""
__all__ = ['transfer']
from typing import Any
from void_os.data_bank.converter.transfer.key import _key
from void_os.data_bank.converter.transfer.order import _order
from void_os.data_bank.converter.transfer.relation import _relation

def transfer(schema: list[dict[str, Any,]], input: list[dict[str, Any,]]) -> list[dict[str, Any,]]:
    layout = _relation.relations(schema, input)
    return layout + [_key.keys(layout[4], input[0]), _order.order(schema, [layout[0], layout[2]])]
