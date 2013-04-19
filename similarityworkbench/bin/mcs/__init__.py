#!/usr/bin/python
# -*- coding: utf-8 -*-

import Cmcs


class Graph:

    def __init__(self, filename):
        self.content = file(filename).read()
        self.storage = Cmcs.read_graph(filename)
        if self.storage is None:
            raise 'The graph file is not valid'

    def __str__(self):
        return self.content


class SDFGraph(Graph):

    def __init__(self, sdf):
        self.content = sdf
        self.storage = Cmcs.parse_sdf(sdf)
        if self.storage is None:
            raise 'The SDF is not valid'

    def sub(self, indices):
        if self.storage is None:
            return None
        result = []
        buf = self.content.split('\n')
        buf = [i.replace('\r', '') for i in buf]
        result.append(buf[0] + '_SUBSDF')
        result.append(buf[1] + ' GENERATED BY PYMCS')
        result.append(buf[2])
        result.append('place holder')
        n_atoms = int((buf[3])[:3])
        n_bonds = int((buf[3])[3:6])
        atom_map = dict()
        new_id = 1
        for i in range(n_atoms):
            if i in indices:
                result.append(buf[4 + i])
                atom_map[i + 1] = new_id
                new_id += 1
        _n_bonds = 0
        for i in range(n_bonds):
            line = buf[4 + n_atoms + i]
            a = int(line[:3])
            b = int(line[3:6])
            if a - 1 in indices and b - 1 in indices:
                result.append('%3d%3d%s' % (atom_map[a], atom_map[b],
                              line[6:]))
                _n_bonds += 1
        result[3] = '%3d%3d' % (len(indices), _n_bonds) + (buf[3])[6:]
        result.append('$$$$\n')

        sdf = '\n'.join(result)
        return SDFGraph(sdf)

    @classmethod
    def from_file(cls, sdffile):
        content = file(sdffile).read()
        self = cls(content)
        return self


def mcs(
    graph1,
    graph2,
    max_components=1,
    lower_bound=0,
    timeout=None,
    ):

    assert isinstance(graph1, Graph)
    assert isinstance(graph2, Graph)
    if timeout:
        assert isinstance(timeout, int)
        Cmcs.set_timeout(timeout)
    size = Cmcs.max(graph1.storage, graph2.storage, max_components,
                    lower_bound, 1)
    match = dict()
    for i in range(size):
        match[Cmcs.get_best(1, i)] = Cmcs.get_best(2, i)

    return match


