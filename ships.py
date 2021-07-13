import io
import datetime
class Vehicle:
    def __init__(self, name, rank, max_rank=50):
        self.name = name
        self.rank = rank
        self.max_rank = max_rank
        self.voyage = None
    def add_voyage(self, voyage):
        self.voyage = voyage
    def delete_voyage(self):
        self.voyage = None
    def rename(self, name):
        self.name = name
    def update_rank(self, rank):
        self.rank = rank
    def __str__(self):
        if self.voyage is None:
            return "Ship: {} -- Rank: {}/{} -- Docked".format(self.name, self.rank, self.max_rank)
        else:
            # datetime formatting courtesy of 
            # https://stackoverflow.com/a/538687
            time_left = self.voyage.end_time - datetime.datetime.now()
            time_left = ''.join(str(time_left).split('.')[0])
            return "Ship: {} -- Rank: {}/{} -- {} -- Voyage complete in {}".format(\
                self.name, self.rank, self.max_rank, self.voyage.purpose, time_left)

class Voyage:
    def __init__(self, start_time=None, end_time=None, time_delta=None, purpose=None):
        if (start_time is not None) and (end_time is not None) and \
                (time_delta is not None):
            # check that the times given agree with elapsed time
            if end_time - start_time != time_delta:
                raise ValueError("Start/end times do not agree with voyage length")
            self.start_time = start_time
            self.end_time = end_time
            self.time_delta = time_delta
        elif (start_time is not None) and (end_time is not None):
            self.start_time = start_time
            self.end_time = end_time
            self.time_delta = self.end_time - self.start_time
        elif (start_time is not None) and (time_delta is not None):
            self.start_time = start_time
            self.time_delta = time_delta
            self.end_time = self.start_time + self.time_delta
        elif (time_delta is not None) and (end_time is not None):
            self.time_delta = time_delta
            self.end_time = end_time
            self.start_time = self.end_time - self.time_delta
        elif end_time is not None:
            self.time_delta = None
            self.start_time = None
            self.end_time = end_time
        else:
            raise ValueError("Not enough information provided to determine voyage start/end time")
        if purpose is not None:
            self.purpose = purpose
        else:
            self.purpose = "n/a"
    def __str__(self):
        return "Start time: {}, End time: {}, Voyage_length: {}, Purpose: {}".format(self.start_time, \
            self.end_time, self.time_delta, self.purpose)

class VehicleList:
    def __init__(self, airships=list(), submersibles=list()):
        self.airships = airships
        self.submersibles = submersibles
    def update_airships(self, airships):
        self.airships = airships
    def update_submersibles(self, submersibles):
        self.submersibles = submersibles
    def clear(self):
        self.airships = []
        self.submersibles = []
    def __str__(self):
        out_buf = io.StringIO()
        out_buf.write(u"```")
        out_buf.write(u"Airships:\n")
        for airship in self.airships:
            out_buf.write(str(airship))
            out_buf.write(u"\n")
        out_buf.write(u"\n")
        out_buf.write(u"Submersibles:\n")
        for submersible in self.submersibles:
            out_buf.write(str(submersible))
            out_buf.write(u"\n")
        out_buf.write(u"\n")
        out_buf.write(u"```")
        out_buf.seek(0)
        out_str = str(out_buf.read()).rstrip()
        return out_str
    def print_list(self):
        print(self)
