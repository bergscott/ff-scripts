import random

class League(object):
    def __init__(self, name):
        """
        create a new League object and give it name name. Initialize empty dicts
        for teams and divisions.

        name: a string
        """
        self.name = str(name)
        self.teams = {}
        self.divisions = set()
        
    def get_name(self):
        """
        Return the name of the League.

        returns: a string
        """
        return self.name
    
    def set_name(self, name):
        """
        Set the name of the league to NAME.

        name: a string
        """
        self.name = name
        
    def create_team(self, team_name):
        """
        Instantiates a new Team object and sets its name to TEAM_NAME.
        Adds key of TEAM_NAME to self.names and sets its value to the new
        Team object.

        team_name: a string 
        """
        self.teams[team_name] = Team(team_name)
        
    def remove_team(self, team_name):
        """
        If TEAM_NAME is key in self.teams, deletes that entry from self.teams,
        otherwise raises error.

        team_name: a string in self.teams.keys()
        """
        if team_name in self.teams:
            del self.teams[team_name]
        else: raise ValueError(team_name + ' is not in league.')
        
    def get_team(self, team_name):
        """
        Return the Team object in self.teams with name attribute TEAM_NAME.

        team_name: a string in self.teams.keys()
        Returns: a Team object
        """
        try:
            return self.teams[team_name]
        except:
            raise ValueError(team_name + ' is not in League.')
        
    def get_team_dict(self):
        """
        Return the dictionary of teams in the league.
        
        returns: a dict
        """
        return self.teams
    
    def add_division(self, division_name):
        """
        Adds an entry to the self.divisions set with DIVISION_NAME

        division_name: a string
        """
        self.divisions.add(division_name)
        
    def remove_division(self, division_name):
        """
        Deletes entry with key DIVISON_NAME from self.divisions set.

        division_name: a string in self.divisions
        """
        if division_name in self.divisions:
            self.divisions.remove(division_name)
        else: raise ValueError(division_name + ' is not a division in league.')
        
    def get_divisions(self):
        """
        Returns set of division names in the league.

        returns: a set of strings
        """
        return self.divisions
        
    def shuffle_divisions(self):
        """
        Randomly evenly assigns divisions from self.divisions to teams in
        self.teams.
        Mutates the name attributes of the Team objects in self.teams
        """
        # map divisions to size (number of teams in division (initial: 0))
        divisions = {}
        for d in self.divisions:
            divisions[d] = 0  
        # calculate maximum division size
        max_teams = len(self.teams) / len(divisions)
        large_divs_remaining = len(self.teams) % len(divisions)
        if large_divs_remaining > 0: max_teams += 1
        # randomly assign a division to each team, update dict
        for t in self:
            d = random.choice(divisions.keys())
            t._set_division(d)
            divisions[d] += 1
            # if division is full, remove it from dict, update max size
            if divisions[d] >= max_teams:
                del divisions[d]
                if large_divs_remaining > 1:
                    large_divs_remaining -= 1
                elif large_divs_remaining == 1:
                    max_teams -= 1
                    large_divs_remaining = -1

    def assign_team_to_division(self, team_name, division_name):
        """
        Sets the division attribute of the Team object with name TEAM_NAME in
        self.teams to DIVISION_NAME. Checks to make sure division is found in
        self.divisions and if not, raises error.
        
        team_name: a string in self.teams.keys()
        division_name: a string in self.divisions.keys()
        """
        try:
            if division_name in self.divisions:
                self.teams[team_name]._set_division(division_name)
            else: raise ValueError(division_name +
                    ' is not a division in league')
        except KeyError:
            raise ValueError(team_name + ' is not in League')
        
    def __iter__(self):
        """
        Yields each Team object in self.teams
        """
        for t in self.teams.values():
            yield t
            
    def __str__(self):
        """
        Returns a string representation of the league containing its name and
        teams sorted by their divisions.  If a team in self.teams has no
        division or a division not in self.divisions, it is sorted under
        '<Not Assigned>'.

        returns: a string
        """
        result = 'League Name: ' + self.name + '\nTeams and Divisions:\n'
        divisions = {}
        for d in self.divisions:
            divisions[d] = []
        for t in self:
            try: divisions[t.get_division()].append(t.get_name())
            except KeyError:
                if '<Not Assigned>' in divisions:
                    divisions['<Not Assigned>'].append(t.get_name())
                else: divisions['<Not Assigned>'] = [t.get_name(),]
        sorted_divs = sorted(divisions.keys(), key=str.lower)
        for d in sorted_divs:
            result = result + 'Division Name: ' + d + '\n'
            if len(divisions[d]) > 0:
                for t in divisions[d]:
                    result = result + '\t' + t + '\n'
            else: result = result + '\t<empty>\n'
        return result[:-1]
            
class Team(object):
    """
    Represents a fantasy sports team in a league.
    Teams should be created within League objects with the League.create_team
    method.
    """
    def __init__(self, name):
        """
        Initializes a Team with the given name and sets its initial owner and
        division to None

        name: a string
        """
        self.name = str(name)
        self.owner = None
        self.division = None

    def get_name(self):
        """
        Returns the name of the team.

        returns: a string
        """
        return self.name

    def set_owner(self, owner):
        """
        Sets the name of the team's owner to OWNER.

        owner: a string
        """
        self.owner = str(owner)

    def get_owner(self):
        """
        Returns the name of the owner of the team.

        returns: a string
        """
        return self.owner    
    
    def _set_division(self, division):
        """
        Sets which division the team belongs to. Should only be called by
        methods in a League object to maintain compatibility.
        
        division: a string
        """
        self.division = division               

    def get_division(self):
        """
        Returns the name of the division the team belongs to.

        returns: a string
        """
        return self.division    

    def __str__(self):
        """
        Returns a string representation of a Team (its name)

        returns: a string
        """
        return self.name

grassmasters = League('Frozen Grassmasters of Lambeau')
grassmasters.create_team('Training Camp Hookie')
grassmasters.create_team('T-bone Chicken')
grassmasters.create_team('Dark Helmet')
grassmasters.create_team('Wish Sandwiches')

grassmasters.create_team('Flaming Moes')
grassmasters.create_team('Jello Puddin\' Pops')
grassmasters.create_team('The Schlubs')
grassmasters.create_team('Kentucky Clears')

grassmasters.create_team('Mother of Dragons')
grassmasters.create_team('Demaryius Targaryen')
grassmasters.create_team('Winter is Coming')
grassmasters.create_team('King in the North')

grassmasters.add_division('Beer')
grassmasters.add_division('Cheese')
grassmasters.add_division('Sausage')

grassmasters.shuffle_divisions()

print grassmasters

