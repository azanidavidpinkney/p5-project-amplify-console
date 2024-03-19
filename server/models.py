from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

# Models go here!


class Product(db.Model, SerializerMixin):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # add relationships
    mappings = db.relationship("Mapping", backref="product")

    # add serialization rules
    serialize_rules = ("-products.mappings",)


class Project(db.Model, SerializerMixin):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # add relationships
    mappings = db.relationship("Mapping", backref="project")

    # add serialization rules
    serialize_rules = ("-projects.project_admin",)

    # add validation


class Mapping(db.Model, SerializerMixin):
    __tablename__ = "mappings"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    smartsheet_id = db.Column(db.String, db.ForeignKey("smartsheets.smartsheet_id"))
    googlesheet_id = db.Column(db.String, db.ForeignKey("googlesheets.googlesheet_id"))
    name = db.Column(db.String)

    # add relationships
    project = db.relationship("Project", backref="mappings")
    product = db.relationship("Product", backref="mappings")
    smartsheet = db.relationship("Smartsheet", backref="mappings")
    googlesheet = db.relationship("Googlesheet", backref="mappings")


class Smartsheet(db.Model, SerializerMixin):
    __tablename__ = "smartsheets"

    id = db.Column(db.Integer, primary_key=True)
    smartsheet_id = db.Column(db.String, primary_key=True)
    sheetname = db.Column(db.String)

    # add relationships
    mappings = db.relationship("Mapping", backref="smartsheets")
    googlesheet = association_proxy("mappings", "googlesheets")

    # add serialization rules
    serialize_rules = ("-smartsheets.mappings", "-smartsheets.googlesheet")

    # add validation


class Googlesheet(db.Model, SerializerMixin):
    __tablename__ = "googlesheets"

    id = db.Column(db.Integer, primary_key=True)
    googlesheet_id = db.Column(db.String, primary_key=True)
    sheetname = db.Column(db.String)

    # add relationships
    mappings = db.relationship("Mapping", backref="googlesheets")
    smartsheet = association_proxy("mapping", "smartsheet")

    # add serialization rules
    serialize_rules = ("-googlesheets.mapping", "-googlesheets.smartsheet")

    # add validation


class SmartsheetCell(db.Model, SerializerMixin):
    __tablename__ = "smartsheet_cells"

    id = db.Column(db.Integer, primary_key=True)
    smartsheet_id = db.Column(db.String, db.ForeignKey("smartsheets.smartsheet_id"))
    row_id = db.Column(db.String)
    column_id = db.Column(db.String)
    value = db.Column(db.String)

    # add relationships
    smartsheet = db.relationship("Smartsheet", backref="cells")
    mappings = association_proxy("smartsheet", "mappings")

    # add serialization rules
    serialize_rules = ("-smartsheet_cells.smartsheet", "-smartsheet_cells.mappings")

    # add validation


class GooglesheetCell(db.Model, SerializerMixin):
    __tablename__ = "googlesheet_cells"

    id = db.Column(db.Integer, primary_key=True)
    googlesheet_id = db.Column(db.String, db.ForeignKey("googlesheets.googlesheet_id"))
    tab_id = db.Column(db.String)
    row_id = db.Column(db.String)
    column_id = db.Column(db.String)
    value = db.Column(db.String)

    # add relationships
    googlesheet = db.relationship("Googlesheet", backref="cells")
    mappings = association_proxy("googlesheet", "mappings")

    # add serialization rules
    serialize_rules = ("-googlesheet_cells.googlesheet", "-googlesheet_cells.mappings")

    # add validation


class Pairing(db.Model, SerializerMixin):
    __tablename__ = "pairings"

    id = db.Column(db.Integer, primary_key=True)
    gs_cell_id = db.Column(db.Integer, db.ForeignKey("googlesheet_cells.id"))
    ss_cell_id = db.Column(db.Integer, db.ForeignKey("smartsheet_cells.id"))

    # add relationships
    gs_cell = db.relationship("GooglesheetCell", backref="pairings")
    ss_cell = db.relationship("SmartsheetCell", backref="pairings")
    smartsheet = association_proxy("ss_cell", "smartsheet")
    googlesheet = association_proxy("gs_cell", "googlesheet")

    # add serialization rules
    serialize_rules = (
        "-pairings.ss_cell",
        "-pairings.gs_cell",
        "-pairings.smartsheet",
        "-pairings.googlesheet",
    )

    # add validation
