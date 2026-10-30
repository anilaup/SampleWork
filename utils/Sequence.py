class Sequencer:
    #Similar to DB Sequencers
    start_no = 100000000
    increment = 1
    keyTracker = dict()  # to keep track of all keys

    @staticmethod
    def NextVal():
        Sequencer.start_no += Sequencer.increment
        return Sequencer.start_no

    @staticmethod
    def SetCurrentRecId(recType, idx):
        Sequencer.keyTracker[recType] = idx

    @staticmethod
    def GetCurrentRecId(recType):
        return Sequencer.keyTracker.get(recType)

    @staticmethod
    def ResetRecIds():
        Sequencer.keyTracker = dict()

