from enum import Enum
from sqlalchemy import Enum as SQLAEnum
from .db import db


# Association table for the service and team relationship
service_team_association = db.Table(
    'service_team',
    db.Column('service_id', db.String(36), db.ForeignKey('services.id'), primary_key=True),
    db.Column('team_id', db.String(36), db.ForeignKey('teams.id'), primary_key=True)
)

# Association table for the escalation policy and service relationship
escalation_policy_service_association = db.Table(
    'escalation_policy_service',
    db.Column('escalation_policy_id', db.String(36), db.ForeignKey('escalation_policies.id'), primary_key=True),
    db.Column('service_id', db.String(36), db.ForeignKey('services.id'), primary_key=True)
)

class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.String(36), primary_key=True)
    incidents = db.relationship('Incident', back_populates='service')
    teams = db.relationship('Team', secondary=service_team_association, back_populates='services')
    escalation_policies = db.relationship('EscalationPolicy', secondary=escalation_policy_service_association, back_populates='services')


    def __repr__(self):
        return f"<Service(id={self.id})>"

class IncidentStatus(Enum):
    TRIGGERED = 'triggered'
    ACKNOWLEDGED = 'acknowledged'
    RESOLVED = 'resolved'


class Incident(db.Model):
    __tablename__ = 'incidents'

    id = db.Column(db.String(36), primary_key=True)
    status = db.Column(SQLAEnum(IncidentStatus), nullable=False)
    service_id = db.Column(db.String(36), db.ForeignKey('services.id'))
    service = db.relationship('Service', back_populates='incidents')

    def __repr__(self):
        return f"<Incident(id={self.id}, status={self.status})>"


class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.String(36), primary_key=True)
    services = db.relationship('Service', secondary=service_team_association, back_populates='teams')
    escalation_policies = db.relationship('EscalationPolicy', back_populates='team')


    def __repr__(self):
        return f"<Team(id={self.id})>"


class EscalationPolicy(db.Model):
    __tablename__ = 'escalation_policies'

    id = db.Column(db.String(36), primary_key=True)
    services = db.relationship('Service', secondary=escalation_policy_service_association, back_populates='escalation_policies')
    team_id = db.Column(db.String(36), db.ForeignKey('teams.id'))
    team = db.relationship('Team', back_populates='escalation_policies')    

    def __repr__(self):
        return f"<EscalationPolicy(id={self.id})>"


