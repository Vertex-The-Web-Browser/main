import sqlite3

class SessionHistory:
    '''
    Class to keep track of session history, used for implementing forward and
    back buttons. Consists of a list to keep track of history, and a pointer which
    indicates where we are in the list of history. 
    Contains function add_uri to add a uri to history, function prev_uri which returns previous
    page, and function next_uri which returns next page.
    '''
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    def __init__(self):
        '''
        Initialises an empty list for session history
        '''
        self.history = []
        self.history_ptr = -1
        SessionHistory.cur.execute("CREATE TABLE IF NOT EXISTS history(id integer primary key autoincrement, uri varchar(2000), timestamp datetime default CURRENT_TIMESTAMP);")
        SessionHistory.con.commit()


    def add_uri(self, uri):
        '''
        If history pointer is at the end of the list, then the uri is appended to history.
        If history pointer is somewhere in the middle, then all elements after it are
        discarded and then the new element is appended.
        '''

        if len(self.history) != self.history_ptr + 1:
            self.history = self.history[:self.history_ptr + 1]

        self.history.append(uri)
        self.history_ptr += 1
        SessionHistory.cur.execute("INSERT INTO history(uri) VALUES(?)",(uri,))
        SessionHistory.con.commit()

    def curr_uri(self):
        '''
        Returns current uri. Returns None if history is empty
        '''

        if self.history_ptr == -1:
            return None
        else:
            return self.history[self.history_ptr]


    def prev_uri(self):
        '''
        Returns the previous uri. Changes history pointer accordingly. Returns None if
        history pointer is on the first uri or if history is empty
        '''

        if self.history_ptr <= 0:
            return None
        
        self.history_ptr -= 1
        return self.history[self.history_ptr]  


    def next_uri(self):
        '''
        Returns the next uri. Changes history pointer accordingly. Returns None if
        history pointer is on the last uri or if history is empty
        '''   

        if self.history_ptr == len(self.history) - 1:
            return None

        self.history_ptr += 1
        return self.history[self.history_ptr] 