CREATE TABLE osm_nodes (
    node BIGINT NOT NULL,
    lon FLOAT NOT NULL,
    lat FLOAT NOT NULL,
	PRIMARY KEY(node)
);

CREATE TABLE osm_ways (
    way BIGINT NOT NULL,
	PRIMARY KEY(way)
);

CREATE TABLE osm_relations (
    relation BIGINT NOT NULL,
	PRIMARY KEY(relation)
);

CREATE TABLE osm_nodes_tags (
    node BIGINT NOT NULL,
    k NVARCHAR(255) NOT NULL,
    v TEXT NOT NULL,
	PRIMARY KEY(node, k, v),
	FOREIGN KEY (node) REFERENCES osm_nodes(node)
);

CREATE TABLE osm_ways_tags (
    way BIGINT NOT NULL,
    k NVARCHAR(255) NOT NULL,
    v TEXT NOT NULL,
	PRIMARY KEY(way, k, v),
	FOREIGN KEY (way) REFERENCES osm_ways(way)
);

CREATE TABLE osm_relations_tags (
    relation BIGINT NOT NULL,
    k NVARCHAR(255) NOT NULL,
    v TEXT NOT NULL,
	PRIMARY KEY(relation, k, v),
	FOREIGN KEY (relation) REFERENCES osm_relations(relation)
);

CREATE TABLE osm_relations_members (
    relation BIGINT NOT NULL,
    nr INTEGER NOT NULL,
    ref BIGINT NOT NULL,
    role NVARCHAR(50),
    type NVARCHAR(10),
    PRIMARY KEY(relation, nr),
	FOREIGN KEY (relation) REFERENCES osm_relations (relation)
);

CREATE TABLE osm_ways_nds (
    way BIGINT NOT NULL,
    nr INTEGER NOT NULL,
    node BIGINT NOT NULL,
	PRIMARY KEY (way, nr),
	FOREIGN KEY (node) REFERENCES osm_nodes (node)
);

CREATE INDEX idx_osm_nodes_tags_k ON osm_nodes_tags(k);
CREATE INDEX idx_osm_ways_tags_k ON osm_ways_tags(k);
CREATE INDEX idx_osm_relations_tags_k ON osm_relations_tags(k);
