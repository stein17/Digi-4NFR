from Components.Converter.Converter import Converter
from Components.Element import cached
from enigma import eEPGCache

class rmEventName(Converter, object):
	NAME = 0
	SHORT_DESCRIPTION = 1
	EXTENDED_DESCRIPTION = 2
	ID = 3
	NEXT_NAME = 4
        NEXT_DESCRIPTION = 5
	
	def __init__(self, type):
		Converter.__init__(self, type)
		self.epgcache = eEPGCache.getInstance()
		if type == "Description":
			self.type = self.SHORT_DESCRIPTION
		elif type == "ExtendedDescription":
			self.type = self.EXTENDED_DESCRIPTION
		elif type == "ID":
			self.type = self.ID
		elif type == "NextName":
                        self.type = self.NEXT_NAME
                elif type == "NextDescription":
                        self.type = self.NEXT_DESCRIPTION
		else:
			self.type = self.NAME

	@cached
	def getText(self):
		event = self.source.event
		if event is None:
			return ""
			
		if self.type == self.NAME:
			return event.getEventName()
		elif self.type == self.SHORT_DESCRIPTION:
			return event.getShortDescription()
		elif self.type == self.EXTENDED_DESCRIPTION:
			return event.getExtendedDescription()
		elif self.type == self.ID:
			return str(event.getEventId())
		elif self.type == self.NEXT_NAME or self.type == self.NEXT_DESCRIPTION:
                        reference = self.source.service
                        info = reference and self.source.info
                        if info is not None:
                        	nextEvent = self.epgcache.lookupEvent(['SETX', (reference.toString(), 1, -1)])
                                if self.type == self.NEXT_NAME:
                                        return nextEvent[0][2]
                                else:
                                        if nextEvent[0][1] != "":
                                                return nextEvent[0][1]
                                        else:
                                                return nextEvent[0][0]

		return ""
		
	text = property(getText)
