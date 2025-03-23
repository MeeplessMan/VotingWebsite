from app import db
from datetime import datetime
from models import User, Vote, Ballot, Candidate, Election

def get_current_election():
    return Election.query.filter(Election.election_status == 'active').first()

def check_election_status():
    current_election = get_current_election()
    if current_election:
        return True
    else:
        return False
    
def get_ballot_status(ballot_id):
    ballot = Ballot.query.get(ballot_id)
    if(ballot.election.election_status != 'active' and ballot.status == True):
        ballot.status = False
        db.session.commit()
    return ballot.status

def get_ballot_candidates(ballot_id):
    ballot = Ballot.query.get(ballot_id)
    return ballot.candidates

def increase_vote(candidate_id):
    candidate = Candidate.query.get(candidate_id)
    if candidate:
        candidate.number_votes += 1
        db.session.commit()
        return True

def get_ballot(ballot_id):
    return Ballot.query.get(ballot_id)

def get_candidate(candidate_id):
    return Candidate.query.get(candidate_id)
