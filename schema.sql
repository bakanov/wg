CREATE TABLE ships (
    ship TEXT NOT NULL PRIMARY KEY, 
    weapon TEXT NOT NULL, 
    hull TEXT NOT NULL, 
    engine TEXT NOT NULL,
    FOREIGN KEY(weapon) REFERENCES weapons(weapon),
    FOREIGN KEY(hull) REFERENCES hulls(hull),
    FOREIGN KEY(engine) REFERENCES engines(engine)
);
CREATE TABLE engines (
    engine TEXT NOT NULL PRIMARY KEY, 
    power INTEGER NOT NULL, 
    type INTEGER NOT NULL
);
CREATE TABLE hulls (
    hull TEXT NOT NULL PRIMARY KEY, 
    armor INTEGER NOT NULL, 
    type INTEGER NOT NULL, 
    capacity INTEGER NOT NULL
);
CREATE TABLE weapons (
    weapon TEXT NOT NULL PRIMARY KEY, 
    reload_speed INTEGER NOT NULL, 
    rotational_speed INTEGER NOT NULL, 
    diameter INTEGER NOT NULL, 
    power_volley INTEGER NOT NULL, 
    count INTEGER NOT NULL
);
