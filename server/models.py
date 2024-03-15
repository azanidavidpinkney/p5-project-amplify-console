from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

# Models go here!


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password_hash = db.Column(db.String)

    # add relationships
    projects = db.relationship("Project", backref="project_admin")
    mappings = association_proxy("projects", "mappings")

    # add serialization rules
    serialize_rules = ("-users.projects", "-users.mappings")

    # add validation


class Project(db.Model, SerializerMixin):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # add relationships
    project_admin = db.relationship("User", backref="projects")

    # add serialization rules
    serialize_rules = ("-projects.project_admin",)

    # add validation


class Mapping(db.Model, SerializerMixin):
    __tablename__ = "mappings"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    smartsheet_id = db.Column(db.String, db.ForeignKey("smartsheets.smartsheet_id"))

    # add relationships
    project = db.relationship("Project", backref="mappings")
    smartsheet = db.relationship("Smartsheet", backref="mappings")
    googlesheets = db.relationship("Googlesheet", backref="mappings")


class Smartsheet(db.Model, SerializerMixin):
    __tablename__ = "smartsheets"

    id = db.Column(db.Integer, primary_key=True)
    smartsheet_id = db.Column(db.String, primary_key=True)
    sheetname = db.Column(db.String)

    # add relationships
    mappings = db.relationship("Mapping", backref="smartsheets")
    googlesheets = association_proxy("mappings", "googlesheets")

    # add serialization rules
    serialize_rules = ("-smartsheets.mappings", "-smartsheets.googlesheets")

    # add validation


class Googlesheet(db.Model, SerializerMixin):
    __tablename__ = "googlesheets"

    id = db.Column(db.Integer, primary_key=True)
    googlesheet_id = db.Column(db.String, primary_key=True)
    mapping_id = db.Column(db.Integer, db.ForeignKey("mappings.id"))
    sheetname = db.Column(db.String)

    # add relationships
    mapping = db.relationship("Mapping", backref="googlesheets")
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

    # add serialization rules
    serialize_rules = ("-smartsheet_cells.smartsheet",)

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

    # add serialization rules
    serialize_rules = ("-googlesheet_cells.googlesheet",)

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
