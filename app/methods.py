from app import db
import datetime
from app.models import User, Vote, Ballot, Candidate, Election
import os

class Methods:
    def __init__(self):
        pass

    def get_current_election():
        current_election = Election.query.filter(Election.election_status == 'active').first()
        if current_election:
            return current_election
        else:
            return None
    
    def set_election_status(election_id, status):
        election = Election.query.get(election_id)
        if election == None:
            return False
        if(status == 'active'):
            active = Election.query.filter(Election.election_status == 'active').first()
            if active:
                return False
            if election.election_status == 'inactive':
                etemp = election.start_time.strftime('%Y-%m-%d %H:%M:%S')
                dtemp = election.end_time.strftime('%Y-%m-%d %H:%M:%S')
                today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if etemp >= today and dtemp <= today:
                    election.election_status = status
                    ballots = Ballot.query.filter(Ballot.election_id == election_id).all()
                    for b in ballots:
                        b.status = True
                    db.session.commit()
                    return True
                else:
                    return False
            else:
                return False
        elif(status == 'completed'):
            dtemp = election.end_time.strftime('%Y-%m-%d %H:%M:%S')
            today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if dtemp >= today:
                return False
            else:
                election.election_status = status
                ballots = Ballot.query.filter(Ballot.election_id == election_id).all()
                for b in ballots:
                    b.status = False
                db.session.commit()
                return True
        else:
            return False
    def set_ballot_status(ballot_id, status):
        ballot = Ballot.query.get(ballot_id)
        if ballot:
            election = Election.query.get(ballot.election_id)
            if(election.election_status == 'active'):
                if(status == True):
                    ballot.status = status
                    db.session.commit()
                    return True
                elif(status == False):
                    ballot.status = status
                    db.session.commit()
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
        
    def get_upcoming_election():
        elections = Election.query.filter(Election.election_status == 'inactive').all()
        upcoming_election = None
        for e in elections:
            etemp = e.start_time.strftime('%Y-%m-%d %H:%M:%S')
            today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if etemp > today:
                upcoming_election = e
                continue
            if upcoming_election:
                utemp = upcoming_election.start_time.strftime('%Y-%m-%d %H:%M:%S')
                if etemp < utemp:
                    upcoming_election = e
                    continue
        return upcoming_election
                
    def get_recent_election():
        recent_election = Election.query.order_by(Election.end_time).first()
        if recent_election:
            return recent_election
        else:
            return None

    def get_election_status(self):
        current_election = self.get_current_election()
        if current_election:
            return current_election.election_status
        else:
            return None

    def check_election_status(self):
        current_election = self.get_current_election()
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
        return False

    def get_ballot(ballot_id):
        return Ballot.query.get(ballot_id)

    def get_candidate(candidate_id):
        return Candidate.query.get(candidate_id)
    
    def check_dut_email(email):
        if email.endswith('@dut4life.ac.za') or email.endswith('@dut.ac.za'):
            return True
        else:
            return False
    def create_ballot(campus, selections, election_id):
        ballot = Ballot(campus=campus, selections=selections, election_id=election_id)
        db.session.add(ballot)
        db.session.commit()
        return True
    
    def create_election(election_name, start_time, end_time):
        elections = Election.query.all()
        for e in elections:
            start = int(start_time.strftime('%Y%m%d%H%M%S'))
            end = int(end_time.strftime('%Y%m%d%H%M%S'))
            start1 = int(e.start_time.strftime('%Y%m%d%H%M%S'))
            end1 = int(e.end_time.strftime('%Y%m%d%H%M%S'))
            overlap = max(0, min(end, end1) - max(start, start1))
            if overlap > 0:
                print('overlap')
                return False
        try:   
            election = Election(election_name=election_name, start_time=start_time, end_time=end_time, election_status='inactive')
        except:
            return False
        db.session.add(election)
        db.session.commit()
        return True
    
    def update_election(election_id, election_name, start_time, end_time, status):
        election = Election.query.get(election_id)
        elections = Election.query.all()
        for e in elections:
            if e.id != election_id:
                start = int(start_time.strftime('%Y%m%d%H%M%S'))
                end = int(end_time.strftime('%Y%m%d%H%M%S'))
                start1 = int(e.start_time.strftime('%Y%m%d%H%M%S'))
                end1 = int(e.end_time.strftime('%Y%m%d%H%M%S'))
                overlap = max(0, min(end, end1) - max(start, start1))
                if overlap > 0:
                    print('overlap')
                    return False
        try:
            election.election_name = election_name
        except:
            return False
        election.start_time = start_time
        election.end_time = end_time
        db.session.commit()
        return True
    
    def delete_election(election_id):
        election = Election.query.get(election_id)
        if election.election_status == 'active':
            return False
        ballots = Ballot.query.filter(Ballot.election_id == election_id).all()
        for b in ballots:
            candidates = Candidate.query.filter(Candidate.ballot_id == b.id).all()
            for c in candidates:
                try:
                    os.remove(os.path.join('app/static/images', str(c.id)+'.jpg'))
                except:
                    pass
                db.session.delete(c)
            vote = Vote.query.filter(Vote.ballot_id == b.id).all()
            for v in vote:
                db.session.delete(v)
            db.session.delete(b)
        db.session.delete(election)
        db.session.commit()
        return True
    
    def create_candidate(fullname, manifesto, ballot_id):
        candidate = Candidate.query.filter(Candidate.fullname == fullname, Candidate.ballot_id==ballot_id).first()
        temp = None
        if candidate:
            return False
        ballot = Ballot.query.get(ballot_id)
        if ballot.status == True:
            return False
        try:
            temp = Candidate(fullname=fullname, manifesto=manifesto, campus=ballot.campus, ballot_id=ballot_id)
        except:
            return False
        print(temp.fullname)
        db.session.add(temp)
        db.session.commit()
        return True
    
    def check_image(image):
        if image.split('.')[-1] in ['jpg']:
            return True
        return False
    
    def delete_candidate(candidate_id):
        candidate = Candidate.query.get(candidate_id)
        if candidate:
            ballot= Ballot.query.get(candidate.ballot_id)
            if ballot.status == True:
                return False
            if ballot.election.election_status == 'active' or ballot.election.election_status == 'completed':
                return False
            try:
                os.remove(os.path.join('app/static/images', str(candidate.id)+'.jpg'))
            except:
                pass
            db.session.delete(candidate)
            db.session.commit()
            return True
        return False