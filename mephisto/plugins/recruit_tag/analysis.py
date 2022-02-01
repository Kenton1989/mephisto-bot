from typing import List, Tuple, Dict
import itertools

import recruit_tag.recruit_data as db


class TagsAndOperators:
    def __init__(self, tags: Tuple[str], operators: Tuple[str]):
        self._tags = tuple(tags)
        self._operators = tuple(operators)

    def tags(self) -> Tuple[str]:
        return self._tags

    def operators(self) -> Tuple[str]:
        return self._operators

    def __str__(self):
        tags = '+'.join(self.tags())
        ops = '/'.join(self.operators())
        return f'{tags}:\n{ops}'

    def key(self):
        return (len(self.operators()), len(self.tags()), self.tags())


def rank6_analysis(tag_list: List[str], max_selected: int = 2) -> List[TagsAndOperators]:
    if db.RANK6_TAG not in tag_list:
        raise NoRank6Error('no rank6 tag detected')

    tag_list.remove(db.RANK6_TAG)

    res = []
    for tag_cnt in range(1, max_selected+1):
        for comb in itertools.combinations(tag_list, tag_cnt):
            operators = set(db.RANK6_ALL)
            for tag in comb:
                operators.intersection_update(db.TAG_TO_OPERATOR.get(tag, ()))
            if len(operators) > 0:
                res.append(TagsAndOperators(comb, tuple(operators)))

    res.sort(key=TagsAndOperators.key)
    return res


class NoRank6Error(Exception):
    pass
